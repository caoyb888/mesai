#!/usr/bin/env python3
"""
API 接口文档知识库入库脚本

功能：
1. 读取 api_parser.py 输出的 Markdown 接口卡片（parsed/ 目录）
2. 通过 LangChain 风格文本分块（chunk_size=800, overlap=128）
3. 使用本地 Embedding 模型（all-MiniLM-L6-v2，无需 API Key）生成向量
4. 写入 ChromaDB（向量检索），集合名：itsm_api_docs
5. 可选写入 MySQL ai_kb_document + ai_kb_chunk（需配置 .env）

用法：
    # 仅 ChromaDB（不需要 API Key）
    python kb_ingest_api.py \
        --api-dir   docs/knowledge-base/api-docs/itsm/parsed/ \
        --system    itsm \
        --collection itsm_api_docs \
        --embed-mode local

    # 验证模式（不写入）
    python kb_ingest_api.py --api-dir ... --dry-run

关联任务：S2-2 T2-2-1
作者：AI（芯智云匠）
日期：2026-04-13
需求单：REQ-MES-AI-20260412-005
"""

import os
import re
import sys
import uuid
import hashlib
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

# ── Token 估算 ───────────────────────────────────────────────

try:
    import tiktoken
    _ENC = tiktoken.get_encoding("cl100k_base")
    def count_tokens(text: str) -> int:
        return len(_ENC.encode(text))
except Exception:
    def count_tokens(text: str) -> int:
        return len(text) // 4


# ── 配置加载 ─────────────────────────────────────────────────

def load_config() -> dict:
    """从 .env 文件或环境变量加载配置"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    return {
        "ai_api_key":     os.environ.get("AI_API_KEY", ""),
        "ai_api_base_url":os.environ.get("AI_API_BASE_URL", "https://api.moonshot.cn/v1"),
        "ai_model":       os.environ.get("AI_EMBED_MODEL", "moonshot-v1-embedding"),
        "db_url":         os.environ.get("DB_URL", ""),
        "db_username":    os.environ.get("DB_USERNAME", ""),
        "db_password":    os.environ.get("DB_PASSWORD", ""),
        "chroma_persist_dir": os.environ.get(
            "CHROMA_PERSIST_DIR", str(Path(__file__).parent / "data/chromadb")
        ),
    }


# ── 文本分块器（适配 API 文档结构）──────────────────────────

class ApiChunkSplitter:
    """
    API 文档分块策略：
    - overview 文件：整体作为一个 api_overview chunk
    - 各模块文件：按 #### 接口详情拆分为独立 api_endpoint chunk
      若整个文件 tokens ≤ 800，则作为单个 api_module chunk
    - 超过 800 tokens 的模块文件：按 #### 四级标题拆分后，
      若单个接口 chunk 仍过大，进一步按段落分割
    """

    MAX_CHUNK_TOKENS = 800
    OVERLAP_TOKENS   = 100

    def split_file(self, md_path: Path) -> list[dict]:
        """拆分单个 Markdown 文件为 chunk 列表"""
        content = md_path.read_text(encoding="utf-8")
        stem = md_path.stem

        # overview 文件：整体一个 chunk
        if stem == "overview":
            return [{
                "text":        content.strip(),
                "chunk_type":  "api_overview",
                "chunk_id":    self._extract_chunk_id(content) or f"itsm_api_overview",
                "token_count": count_tokens(content),
                "source_file": md_path.name,
                "module":      "总览",
            }]

        # 模块文件
        module_name = stem  # 例如："工单核心"、"认证"
        total_tokens = count_tokens(content)

        if total_tokens <= self.MAX_CHUNK_TOKENS:
            # 整个模块作为单 chunk
            return [{
                "text":        content.strip(),
                "chunk_type":  "api_module",
                "chunk_id":    self._extract_chunk_id(content) or f"itsm_{stem}_api_module",
                "token_count": total_tokens,
                "source_file": md_path.name,
                "module":      module_name,
            }]

        # 拆分为：① 模块头（速查表）chunk + ② 各接口 endpoint chunk
        chunks = []

        # 速查表 chunk（包含 ## 标题到第一个 #### 之间的内容）
        header_match = re.split(r"(?=^#### )", content, maxsplit=1, flags=re.MULTILINE)
        header_part = header_match[0].strip()
        # 去掉最后的 --- 元数据行，保留到 ### 接口详情
        header_body = re.split(r"^### 接口详情", header_part, flags=re.MULTILINE)
        if len(header_body) >= 1:
            summary_text = header_body[0].strip()
            # 加上速查表（如果在第一部分）
            if "### 接口速查表" in summary_text or "接口速查表" in header_part:
                chunks.append({
                    "text":        summary_text,
                    "chunk_type":  "api_module_summary",
                    "chunk_id":    f"itsm_{stem}_summary",
                    "token_count": count_tokens(summary_text),
                    "source_file": md_path.name,
                    "module":      module_name,
                })

        # 按 #### 分割各接口
        endpoint_sections = re.split(r"(?=^#### )", content, flags=re.MULTILINE)
        for section in endpoint_sections:
            section = section.strip()
            if not section or not section.startswith("####"):
                continue

            # 提取接口方法+路径作为 ID
            m = re.match(r"####\s+(\w+)\s+(/[^\n]*)", section)
            if m:
                method = m.group(1).lower()
                path_slug = re.sub(r"[^\w]", "_", m.group(2))
                chunk_id = f"itsm_{stem}_{method}{path_slug}"
            else:
                chunk_id = f"itsm_{stem}_endpoint_{len(chunks):03d}"

            tok = count_tokens(section)
            if tok <= self.MAX_CHUNK_TOKENS:
                chunks.append({
                    "text":        section,
                    "chunk_type":  "api_endpoint",
                    "chunk_id":    chunk_id,
                    "token_count": tok,
                    "source_file": md_path.name,
                    "module":      module_name,
                })
            else:
                # 过大接口（含大量字段）→ 进一步按段落分割
                sub_chunks = self._split_large(section, chunk_id, md_path.name, module_name)
                chunks.extend(sub_chunks)

        if not chunks:
            # 兜底：整个文件作为单 chunk
            return [{
                "text":        content.strip(),
                "chunk_type":  "api_module",
                "chunk_id":    f"itsm_{stem}_fallback",
                "token_count": total_tokens,
                "source_file": md_path.name,
                "module":      module_name,
            }]

        return chunks

    def _extract_chunk_id(self, text: str) -> Optional[str]:
        m = re.search(r"chunk_id:\s*([^\s\|*\n]+)", text)
        return m.group(1) if m else None

    def _split_large(
        self,
        text: str,
        base_id: str,
        source_file: str,
        module: str,
    ) -> list[dict]:
        """将超大 section 按段落进一步分割"""
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        result = []
        current_texts: list[str] = []
        current_tokens = 0

        for para in paragraphs:
            para_tokens = count_tokens(para)
            if current_tokens + para_tokens > self.MAX_CHUNK_TOKENS and current_texts:
                chunk_text = "\n\n".join(current_texts)
                result.append({
                    "text":        chunk_text,
                    "chunk_type":  "api_endpoint",
                    "chunk_id":    f"{base_id}_{len(result):03d}",
                    "token_count": current_tokens,
                    "source_file": source_file,
                    "module":      module,
                })
                # 保留 overlap
                overlap_texts: list[str] = []
                overlap_tokens = 0
                for t in reversed(current_texts):
                    t_tok = count_tokens(t)
                    if overlap_tokens + t_tok > self.OVERLAP_TOKENS:
                        break
                    overlap_texts.insert(0, t)
                    overlap_tokens += t_tok
                current_texts = overlap_texts + [para]
                current_tokens = overlap_tokens + para_tokens
            else:
                current_texts.append(para)
                current_tokens += para_tokens

        if current_texts:
            result.append({
                "text":        "\n\n".join(current_texts),
                "chunk_type":  "api_endpoint",
                "chunk_id":    f"{base_id}_{len(result):03d}",
                "token_count": current_tokens,
                "source_file": source_file,
                "module":      module,
            })
        return result


# ── ChromaDB 写入（复用 kb_ingest.py 逻辑）─────────────────

class ChromaWriter:
    """写入 ChromaDB 向量库"""

    def __init__(self, persist_dir: str, collection_name: str):
        try:
            import chromadb
        except ImportError:
            log.error("缺少 chromadb 依赖，请运行：pip install chromadb")
            sys.exit(1)

        import chromadb
        self._client = chromadb.PersistentClient(path=persist_dir)
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        log.info("ChromaDB 集合：%s（%s）", collection_name, persist_dir)
        log.info("现有文档数：%d", self._collection.count())

    def upsert_chunks(self, chunks: list[dict], vectors: list[list[float]]) -> int:
        """批量写入 chunk（upsert 幂等）"""
        ids       = [c["chunk_id"] for c in chunks]
        documents = [c["text"] for c in chunks]
        metadatas = [{
            "module":      c["module"],
            "chunk_type":  c["chunk_type"],
            "source_file": c["source_file"],
            "token_count": c["token_count"],
            "ingested_at": datetime.now().isoformat(),
        } for c in chunks]

        self._collection.upsert(
            ids=ids,
            embeddings=vectors,
            documents=documents,
            metadatas=metadatas,
        )
        log.info("ChromaDB upsert 完成：%d 条，集合总量：%d",
                 len(chunks), self._collection.count())
        return len(chunks)

    def query(self, query_text: str, n_results: int = 5) -> list[dict]:
        """检索最相关 chunk（用于验证）"""
        from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
        ef = DefaultEmbeddingFunction()
        vector = ef([query_text])[0]
        results = self._collection.query(
            query_embeddings=[vector],
            n_results=n_results,
        )
        hits = []
        for i, doc in enumerate(results["documents"][0]):
            hits.append({
                "text":     doc,
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            })
        return hits


# ── 本地 Embedding ────────────────────────────────────────────

class LocalEmbedder:
    """ChromaDB 内置 all-MiniLM-L6-v2，无需外部 API Key"""

    def __init__(self):
        from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
        self._ef = DefaultEmbeddingFunction()
        log.info("本地 Embedding 初始化完成（all-MiniLM-L6-v2）")

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return list(self._ef(texts))


# ── MySQL 写入（可选）────────────────────────────────────────

class MySQLWriter:
    """写入 MySQL ai_kb_document / ai_kb_chunk（可选，DB_URL 为空则跳过）"""

    def __init__(self, cfg: dict):
        if not cfg["db_url"]:
            log.info("DB_URL 未配置，跳过 MySQL 写入")
            self._conn = None
            return
        try:
            import pymysql
            raw_url = cfg["db_url"]
            sep = "://"
            db_url = raw_url[raw_url.index(sep) + len(sep):]
            host_port, _, rest = db_url.partition("/")
            database = rest.split("?")[0]
            host, _, port = host_port.partition(":")
            self._conn = pymysql.connect(
                host=host,
                port=int(port) if port else 3306,
                database=database,
                user=cfg["db_username"],
                password=cfg["db_password"],
                charset="utf8mb4",
                autocommit=False,
            )
            log.info("MySQL 连接成功：%s/%s", host, database)
        except Exception as e:
            log.warning("MySQL 连接失败，跳过元数据写入：%s", e)
            self._conn = None

    def upsert_document(
        self,
        doc_title: str,
        module: str,
        source_file: str,
        chunk_count: int,
        total_tokens: int,
    ) -> Optional[int]:
        if not self._conn:
            return None
        try:
            import pymysql
            content_hash = hashlib.md5(f"{module}:{source_file}".encode()).hexdigest()
            with self._conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO mes_ai_knowledge.ai_kb_document
                        (title, doc_type, module, source_path,
                         content_hash, chunk_count, total_tokens,
                         sync_status, created_at, updated_at)
                    VALUES (%s, 'API_DOC', %s, %s, %s, %s, %s,
                            'SUCCESS', NOW(), NOW())
                    ON DUPLICATE KEY UPDATE
                        chunk_count  = VALUES(chunk_count),
                        total_tokens = VALUES(total_tokens),
                        sync_status  = 'SUCCESS',
                        updated_at   = NOW()
                """, (doc_title, module, source_file,
                      content_hash, chunk_count, total_tokens))
                doc_id = cur.lastrowid or cur.execute(
                    "SELECT id FROM mes_ai_knowledge.ai_kb_document "
                    "WHERE content_hash=%s", (content_hash,)
                )
                self._conn.commit()
                return doc_id
        except Exception as e:
            log.warning("ai_kb_document 写入失败：%s", e)
            if self._conn:
                self._conn.rollback()
            return None

    def upsert_chunks(self, doc_id: Optional[int], chunks: list[dict]) -> int:
        if not self._conn or doc_id is None:
            return 0
        count = 0
        try:
            with self._conn.cursor() as cur:
                for chunk in chunks:
                    cur.execute("""
                        INSERT INTO mes_ai_knowledge.ai_kb_chunk
                            (doc_id, chunk_seq, chunk_type, content,
                             token_count, chroma_id, sync_status,
                             last_sync_at, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s,
                                'SUCCESS', NOW(), NOW(), NOW())
                        ON DUPLICATE KEY UPDATE
                            content      = VALUES(content),
                            token_count  = VALUES(token_count),
                            sync_status  = 'SUCCESS',
                            last_sync_at = NOW(),
                            updated_at   = NOW()
                    """, (
                        doc_id, count,
                        chunk["chunk_type"], chunk["text"],
                        chunk["token_count"], chunk["chunk_id"],
                    ))
                    count += 1
            self._conn.commit()
        except Exception as e:
            log.warning("ai_kb_chunk 写入失败：%s", e)
            if self._conn:
                self._conn.rollback()
        return count

    def close(self):
        if self._conn:
            self._conn.close()


# ── 主流程 ────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="API 接口文档知识库入库脚本")
    parser.add_argument("--api-dir",    required=True, help="parsed/ 目录路径")
    parser.add_argument("--system",     default="itsm", help="系统标识（默认：itsm）")
    parser.add_argument("--collection", default="itsm_api_docs", help="ChromaDB 集合名")
    parser.add_argument("--embed-mode", choices=["local"], default="local",
                        help="向量化模式：local=本地模型（默认）")
    parser.add_argument("--dry-run", action="store_true", help="仅验证 chunk，不写入")
    args = parser.parse_args()

    cfg = load_config()
    api_dir = Path(args.api_dir)

    if not api_dir.exists():
        log.error("目录不存在：%s", api_dir)
        sys.exit(1)

    md_files = sorted(api_dir.glob("*.md"))
    if not md_files:
        log.error("未找到 Markdown 文件：%s", api_dir)
        sys.exit(1)

    # ① 加载所有 chunk
    splitter = ApiChunkSplitter()
    all_chunks: list[dict] = []
    file_chunks_map: dict[str, list[dict]] = {}

    for md_file in md_files:
        chunks = splitter.split_file(md_file)
        for c in chunks:
            # 确保 chunk_id 唯一（加系统前缀防冲突）
            if not c["chunk_id"].startswith(args.system):
                c["chunk_id"] = f"{args.system}_{c['chunk_id']}"
        file_chunks_map[md_file.name] = chunks
        all_chunks.extend(chunks)
        log.info(
            "  %-30s → %d chunks（总 tokens: %d）",
            md_file.name,
            len(chunks),
            sum(c["token_count"] for c in chunks),
        )

    total_tokens = sum(c["token_count"] for c in all_chunks)
    log.info(
        "\n汇总：%d 个文件，%d 个 chunks，约 %d tokens",
        len(md_files), len(all_chunks), total_tokens,
    )

    if args.dry_run:
        log.info("[DRY-RUN] 验证通过，chunk 分布如下：")
        from collections import Counter
        type_count = Counter(c["chunk_type"] for c in all_chunks)
        for ctype, cnt in type_count.items():
            log.info("  %-30s : %d 个", ctype, cnt)
        return

    # ② 向量化
    log.info("开始向量化（本地 Embedding）...")
    embedder = LocalEmbedder()
    texts = [c["text"] for c in all_chunks]

    # 分批处理（避免内存压力）
    BATCH = 32
    vectors: list[list[float]] = []
    for i in range(0, len(texts), BATCH):
        batch = texts[i:i + BATCH]
        vectors.extend(embedder.embed_batch(batch))
        log.info("  向量化进度：%d/%d", min(i + BATCH, len(texts)), len(texts))

    log.info("向量化完成：%d 个向量", len(vectors))

    # ③ 写入 ChromaDB
    chroma = ChromaWriter(
        persist_dir=cfg["chroma_persist_dir"],
        collection_name=args.collection,
    )
    chroma.upsert_chunks(all_chunks, vectors)

    # ④ 写入 MySQL（可选）
    mysql = MySQLWriter(cfg)
    for fname, chunks in file_chunks_map.items():
        module = chunks[0]["module"] if chunks else args.system
        doc_id = mysql.upsert_document(
            doc_title=f"ITSM API - {module}",
            module=module,
            source_file=fname,
            chunk_count=len(chunks),
            total_tokens=sum(c["token_count"] for c in chunks),
        )
        if doc_id:
            mysql.upsert_chunks(doc_id, chunks)
    mysql.close()

    log.info("✅ 入库完成：%s → %d chunks → ChromaDB[%s]",
             args.system, len(all_chunks), args.collection)


if __name__ == "__main__":
    main()
