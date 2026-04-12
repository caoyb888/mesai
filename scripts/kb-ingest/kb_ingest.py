#!/usr/bin/env python3
"""
知识库向量化入库主脚本

功能：
1. 读取 DDL 解析器输出的 Markdown 表卡片（parsed/ 目录）
2. 读取数据字典 Markdown 文件（data-dict/ 目录）
3. 通过 LangChain 文本分块（chunk_size=800, overlap=128）
4. 调用 Kimi Embedding API 生成向量
5. 写入 ChromaDB（向量检索）
6. 写入 MySQL ai_kb_document + ai_kb_chunk（元数据 + 状态管理）

用法：
    python kb_ingest.py \
        --module    工艺管理 \
        --ddl-dir   docs/knowledge-base/mes-ddl/02-工艺管理/parsed/ \
        --dict-file docs/knowledge-base/data-dict/02-工艺管理.md \
        --collection mes_db_structure \
        [--dry-run]   # 只验证不写入

前置条件：
    - .env 文件中设置 AI_API_KEY、DB_URL、DB_USERNAME、DB_PASSWORD
    - ChromaDB 服务已启动（本地模式不需要独立服务）
    - MySQL mes_ai_knowledge Schema 已初始化

关联任务：S2-1 T2-1-1
作者：AI（芯智云匠）
日期：2026-04-12
"""

import os
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

# Token 计数（估算用，无需精确）
try:
    import tiktoken
    _ENC = tiktoken.get_encoding("cl100k_base")
    def count_tokens(text: str) -> int:
        return len(_ENC.encode(text))
except Exception:
    def count_tokens(text: str) -> int:
        return len(text) // 4   # 粗估：4字符≈1 token


# ── 配置加载 ──────────────────────────────────────────────────

def load_config() -> dict:
    """从 .env 文件或环境变量加载配置"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    cfg = {
        "ai_api_key":     os.environ.get("AI_API_KEY", ""),
        "ai_api_base_url":os.environ.get("AI_API_BASE_URL", "https://api.moonshot.cn/v1"),
        "ai_model":       os.environ.get("AI_EMBED_MODEL", "moonshot-v1-embedding"),
        "db_url":         os.environ.get("DB_URL", ""),
        "db_username":    os.environ.get("DB_USERNAME", ""),
        "db_password":    os.environ.get("DB_PASSWORD", ""),
        # ChromaDB 本地持久化目录（不需要独立服务）
        "chroma_persist_dir": os.environ.get(
            "CHROMA_PERSIST_DIR", "./data/chromadb"
        ),
    }

    if not cfg["ai_api_key"]:
        log.error("AI_API_KEY 未设置，请配置 .env 文件")
        sys.exit(1)

    return cfg


# ── 文本分块器 ────────────────────────────────────────────────

class ChunkSplitter:
    """
    Markdown 文档分块策略：
    - table_card chunk：每个 ## 二级标题块作为一个 chunk（通常一张表）
    - 超过 900 tokens 的 chunk 自动分割（保留上下文重叠 128 tokens）
    - 保留块的元数据（chunk_id 从 Markdown 尾注提取）
    """

    MAX_CHUNK_TOKENS = 800
    OVERLAP_TOKENS   = 128

    def split_markdown_file(self, md_path: Path, chunk_type: str) -> list[dict]:
        """
        将 Markdown 文件按 ## 标题分割为 chunk 列表。

        返回格式：
        [
            {
                "text": "...",
                "chunk_type": "table_card",
                "chunk_id": "process_route_table_card",
                "token_count": 350,
                "source_file": "process_route.md"
            },
            ...
        ]
        """
        content = md_path.read_text(encoding="utf-8")
        sections = self._split_by_h2(content)
        chunks = []
        for section in sections:
            chunk_id = self._extract_chunk_id(section)
            token_count = count_tokens(section)

            if token_count <= self.MAX_CHUNK_TOKENS:
                chunks.append({
                    "text": section.strip(),
                    "chunk_type": chunk_type,
                    "chunk_id": chunk_id or f"{md_path.stem}_{len(chunks):03d}",
                    "token_count": token_count,
                    "source_file": md_path.name,
                })
            else:
                # 超大 chunk：按段落二次分割
                sub_chunks = self._split_large_section(section, chunk_id, md_path.stem)
                chunks.extend([{**c, "chunk_type": chunk_type, "source_file": md_path.name}
                                for c in sub_chunks])

        return chunks

    def _split_by_h2(self, content: str) -> list[str]:
        """按 ## 二级标题分割 Markdown"""
        import re
        parts = re.split(r"(?=^## )", content, flags=re.MULTILINE)
        return [p.strip() for p in parts if p.strip()]

    def _extract_chunk_id(self, text: str) -> Optional[str]:
        """从 chunk 尾注提取 chunk_id"""
        import re
        m = re.search(r"chunk_id:\s*([^\s\|*]+)", text)
        return m.group(1) if m else None

    def _split_large_section(
        self, text: str, base_id: Optional[str], stem: str
    ) -> list[dict]:
        """将超大 section 按段落分割，保留 overlap"""
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        result = []
        current_texts = []
        current_tokens = 0

        for para in paragraphs:
            para_tokens = count_tokens(para)
            if current_tokens + para_tokens > self.MAX_CHUNK_TOKENS and current_texts:
                chunk_text = "\n\n".join(current_texts)
                result.append({
                    "text": chunk_text,
                    "chunk_id": f"{base_id or stem}_{len(result):03d}",
                    "token_count": current_tokens,
                })
                # 保留 overlap：取最后若干段
                overlap_texts = []
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
                "text": "\n\n".join(current_texts),
                "chunk_id": f"{base_id or stem}_{len(result):03d}",
                "token_count": current_tokens,
            })
        return result


# ── Kimi Embedding ────────────────────────────────────────────

class KimiEmbedder:
    """
    使用 Kimi（月之暗面）Embedding API 生成文本向量。

    API 兼容 OpenAI Embeddings 接口，模型：moonshot-v1-embedding
    输出维度：1536（与 text-embedding-ada-002 相同）
    """

    BATCH_SIZE = 20   # 每批最多嵌入的文本数

    def __init__(self, cfg: dict):
        try:
            from openai import OpenAI
        except ImportError:
            log.error("缺少 openai 依赖，请运行：pip install openai")
            sys.exit(1)

        self._client = OpenAI(
            api_key=cfg["ai_api_key"],
            base_url=cfg["ai_api_base_url"]
        )
        self._model = cfg["ai_model"]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """批量生成向量，自动分批以避免超过 API 限制"""
        all_vectors = []
        for i in range(0, len(texts), self.BATCH_SIZE):
            batch = texts[i:i + self.BATCH_SIZE]
            try:
                response = self._client.embeddings.create(
                    input=batch,
                    model=self._model
                )
                vectors = [item.embedding for item in response.data]
                all_vectors.extend(vectors)
                log.debug("嵌入批次 %d/%d 完成", i // self.BATCH_SIZE + 1,
                          (len(texts) + self.BATCH_SIZE - 1) // self.BATCH_SIZE)
            except Exception as e:
                log.error("Embedding API 调用失败（批次 %d）：%s", i, e)
                raise
        return all_vectors


# ── ChromaDB 写入 ─────────────────────────────────────────────

class ChromaWriter:
    """
    将向量 chunk 写入 ChromaDB 集合。

    使用本地持久化模式（无需独立服务），数据存储于磁盘。
    集合名称：mes_db_structure（与 Tech Spec 10.6 节知识库相关设计对应）
    """

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
            metadata={"hnsw:space": "cosine"}   # 余弦相似度
        )
        log.info("ChromaDB 集合：%s（%s）",
                 collection_name, persist_dir)

    def upsert_chunks(
        self,
        chunks: list[dict],
        vectors: list[list[float]],
        module: str
    ) -> int:
        """批量写入 chunk（使用 upsert 避免重复）"""
        ids        = [c["chunk_id"] for c in chunks]
        documents  = [c["text"] for c in chunks]
        metadatas  = [{
            "module":      module,
            "chunk_type":  c["chunk_type"],
            "source_file": c["source_file"],
            "token_count": c["token_count"],
            "ingested_at": datetime.now().isoformat(),
        } for c in chunks]

        self._collection.upsert(
            ids=ids,
            embeddings=vectors,
            documents=documents,
            metadatas=metadatas
        )
        log.info("ChromaDB upsert 完成：%d 条", len(chunks))
        return len(chunks)


# ── MySQL 写入 ────────────────────────────────────────────────

class MySQLWriter:
    """
    将文档元数据写入 MySQL mes_ai_knowledge 库：
    - ai_kb_document：文档级元数据（每个 Markdown 文件 1 条）
    - ai_kb_chunk：块级数据（每个 chunk 1 条，含 sync_status）

    注意：不存储向量本身（向量在 ChromaDB 中），只存引用 ID。
    """

    def __init__(self, cfg: dict):
        if not cfg["db_url"]:
            log.warning("DB_URL 未配置，跳过 MySQL 写入（仅写 ChromaDB）")
            self._conn = None
            return
        try:
            import pymysql
        except ImportError:
            log.error("缺少 pymysql 依赖，请运行：pip install pymysql")
            self._conn = None
            return

        import pymysql
        # 从 JDBC URL 解析连接参数（去掉协议前缀后取 host:port/database?params 部分）
        raw_url = cfg["db_url"]
        sep = "://"
        db_url = raw_url[raw_url.index(sep) + len(sep):]  # 跳过 scheme://
        host_port, _, rest = db_url.partition("/")
        database = rest.split("?")[0]
        host, _, port = host_port.partition(":")

        try:
            self._conn = pymysql.connect(
                host=host,
                port=int(port) if port else 3306,
                database=database,
                user=cfg["db_username"],
                password=cfg["db_password"],
                charset="utf8mb4",
                autocommit=False
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
        doc_type: str = "DDL"
    ) -> Optional[int]:
        """写入或更新 ai_kb_document 记录，返回 doc_id"""
        if not self._conn:
            return None

        try:
            with self._conn.cursor() as cur:
                # 以 (module + source_file) 为幂等键
                content_hash = hashlib.md5(
                    f"{module}:{source_file}".encode()
                ).hexdigest()

                cur.execute("""
                    INSERT INTO mes_ai_knowledge.ai_kb_document
                        (title, doc_type, module, source_path,
                         content_hash, chunk_count, total_tokens,
                         sync_status, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, 'SUCCESS', NOW(), NOW())
                    ON DUPLICATE KEY UPDATE
                        chunk_count  = VALUES(chunk_count),
                        total_tokens = VALUES(total_tokens),
                        sync_status  = 'SUCCESS',
                        updated_at   = NOW()
                """, (doc_title, doc_type, module, source_file,
                      content_hash, chunk_count, total_tokens))
                doc_id = cur.lastrowid
                self._conn.commit()
                return doc_id
        except Exception as e:
            log.error("ai_kb_document 写入失败：%s", e)
            self._conn.rollback()
            return None

    def upsert_chunks(
        self,
        doc_id: Optional[int],
        chunks: list[dict],
        module: str
    ) -> int:
        """批量写入 ai_kb_chunk 记录"""
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
                        doc_id,
                        count,
                        chunk["chunk_type"],
                        chunk["text"],
                        chunk["token_count"],
                        chunk["chunk_id"],   # ChromaDB 中的 ID
                    ))
                    count += 1
            self._conn.commit()
            log.info("ai_kb_chunk 写入完成：%d 条", count)
        except Exception as e:
            log.error("ai_kb_chunk 写入失败：%s", e)
            self._conn.rollback()
        return count

    def close(self):
        if self._conn:
            self._conn.close()


# ── 主流程 ────────────────────────────────────────────────────

def load_chunks_from_dir(
    ddl_dir: Optional[Path],
    dict_file: Optional[Path],
    module: str
) -> list[dict]:
    """加载所有 Markdown chunk"""
    splitter = ChunkSplitter()
    all_chunks = []

    if ddl_dir and ddl_dir.exists():
        md_files = [f for f in ddl_dir.glob("*.md") if f.name != "INDEX.md"]
        for f in md_files:
            chunks = splitter.split_markdown_file(f, chunk_type="table_card")
            for c in chunks:
                c["module"] = module
            all_chunks.extend(chunks)
            log.info("DDL 文件：%s → %d chunks", f.name, len(chunks))

    if dict_file and dict_file.exists():
        chunks = splitter.split_markdown_file(dict_file, chunk_type="data_dict")
        for c in chunks:
            c["module"] = module
        all_chunks.extend(chunks)
        log.info("数据字典：%s → %d chunks", dict_file.name, len(chunks))

    return all_chunks


def parse_args():
    p = argparse.ArgumentParser(description="MES 知识库向量化入库脚本")
    p.add_argument("--module",     required=True, help="MES 模块名（如：工艺管理）")
    p.add_argument("--ddl-dir",    help="DDL Markdown 目录（parsed/）")
    p.add_argument("--dict-file",  help="数据字典 Markdown 文件")
    p.add_argument("--collection", default="mes_db_structure", help="ChromaDB 集合名")
    p.add_argument("--dry-run",    action="store_true", help="仅验证 chunk 不写入")
    return p.parse_args()


def main():
    args = parse_args()
    cfg = load_config()

    ddl_dir   = Path(args.ddl_dir)   if args.ddl_dir   else None
    dict_file = Path(args.dict_file) if args.dict_file else None

    # ① 加载 chunk
    chunks = load_chunks_from_dir(ddl_dir, dict_file, args.module)
    if not chunks:
        log.warning("未找到任何 chunk，请检查 --ddl-dir 和 --dict-file 参数")
        sys.exit(0)

    total_tokens = sum(c["token_count"] for c in chunks)
    log.info("准备入库：模块=%s，chunk 数=%d，总 tokens≈%d",
             args.module, len(chunks), total_tokens)

    if args.dry_run:
        log.info("[DRY-RUN] 验证通过，未执行写入")
        for i, c in enumerate(chunks[:5]):
            log.info("  chunk[%d]: id=%s type=%s tokens=%d",
                     i, c["chunk_id"], c["chunk_type"], c["token_count"])
        if len(chunks) > 5:
            log.info("  ...（共 %d 条，仅显示前 5 条）", len(chunks))
        return

    # ② 向量化
    log.info("开始向量化（Kimi Embedding API）...")
    embedder = KimiEmbedder(cfg)
    texts = [c["text"] for c in chunks]
    try:
        from tqdm import tqdm
        vectors = []
        batch_size = 20
        for i in tqdm(range(0, len(texts), batch_size), desc="Embedding"):
            batch = texts[i:i + batch_size]
            vectors.extend(embedder.embed_batch(batch))
    except ImportError:
        vectors = embedder.embed_batch(texts)

    log.info("向量化完成：%d 个向量", len(vectors))

    # ③ 写入 ChromaDB
    chroma = ChromaWriter(
        persist_dir=cfg["chroma_persist_dir"],
        collection_name=args.collection
    )
    chroma.upsert_chunks(chunks, vectors, args.module)

    # ④ 写入 MySQL（可选，连接不通时自动跳过）
    mysql = MySQLWriter(cfg)
    doc_id = mysql.upsert_document(
        doc_title=f"{args.module} · DDL + 数据字典",
        module=args.module,
        source_file=f"{args.ddl_dir or ''},{args.dict_file or ''}",
        chunk_count=len(chunks),
        total_tokens=total_tokens
    )
    mysql.upsert_chunks(doc_id, chunks, args.module)
    mysql.close()

    log.info("入库完成！模块：%s，chunk：%d，tokens：%d",
             args.module, len(chunks), total_tokens)


if __name__ == "__main__":
    main()
