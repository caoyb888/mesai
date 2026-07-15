#!/usr/bin/env python3
"""
S3 理解卡片 RAG 入库：把表理解卡片 + 过程逻辑卡片切块向量化写入 ChromaDB。

§14 合规：
  · 复用 kb_ingest.LocalEmbedder（paraphrase-multilingual-MiniLM-L12-v2，中文友好）
  · 入库与查询同一模型；查询显式传 query_embeddings（不依赖 Chroma 隐式 EF）
  · 换模型/换源须删集合重入（--reset）

用法：
  AI_API_KEY=$(cat kimikey) python3 ingest_s3_cards.py \
    --tables-dir /home/xintong/mes-s3-data/s3-train/tables \
    --procs-dir  /home/xintong/mes-s3-data/s3-train/procs \
    --persist-dir scripts/kb-ingest/data/chromadb \
    --collection mes_s3_understanding --reset --validate

关联需求单：REQ-MES-AI-20260715-001
作者：AI（芯智云匠）  日期：2026-07-15
"""
import re
import sys
import argparse
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kb_ingest import LocalEmbedder, ChromaWriter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def _body(md):
    """去卡片头部 meta（首个 --- 前）与代码围栏"""
    b = md.split("\n---\n", 1)[-1].strip()
    return re.sub(r"```markdown\s*|\s*```", "", b).strip()


def _section(body, header_pat):
    """抓取 '### N. **{header}**' 到下一个标题之间的正文"""
    m = re.search(r"#+\s*\d*\.?\s*\*{0,2}(?:" + header_pat + r")[^\n]*\n(.+?)(?=\n#+\s|\Z)",
                  body, re.S)
    return m.group(1).strip() if m else ""


def _windows(text, max_chars, overlap):
    if len(text) <= max_chars:
        return [text]
    out, i = [], 0
    while i < len(text):
        out.append(text[i:i + max_chars])
        i += max_chars - overlap
    return out


def chunk_card(text, asset, kind, max_chars=700, overlap=120):
    """
    卡片切块（检索调优版）：
      · 每张卡片先产一个「检索锚点」摘要 chunk（表名 + 业务用途 + 核心字段中文语义），
        天然含中文别名，强化表/过程身份信号，专治「查中文名召不回英文表名」；
      · 再产明细窗口 chunk，每块均带「[类型] 表名 用途短语」头，保证分块后身份不丢。
    """
    body = _body(text)
    if not body:
        return []
    purpose = _section(body, "表用途|用途")
    fields = _section(body, "核心字段语义|核心字段|字段语义")
    role = re.split(r"[。\n]", purpose.strip("-* `"))[0][:50] if purpose else ""
    head = f"[{'表' if kind == 'table' else '过程'}] {asset} {role}".strip()

    out = []
    # ① 检索锚点摘要（chunk 0）
    anchor = f"{head}\n业务用途：{purpose[:300]}"
    if fields:
        anchor += f"\n核心字段：{fields[:420]}"
    out.append({"chunk_id": f"{kind}:{asset}:0", "text": anchor,
                "chunk_type": f"s3_{kind}", "source_file": f"{asset}.md",
                "token_count": len(anchor) // 3})
    # ② 明细窗口（chunk 1..k），每块带身份头
    for j, piece in enumerate(_windows(body, max_chars, overlap), start=1):
        t = f"{head}\n{piece}"
        out.append({"chunk_id": f"{kind}:{asset}:{j}", "text": t,
                    "chunk_type": f"s3_{kind}", "source_file": f"{asset}.md",
                    "token_count": len(t) // 3})
    return out


def load_dir(d, kind):
    chunks = []
    files = sorted(Path(d).glob("*.md"))
    for p in files:
        chunks.extend(chunk_card(p.read_text(encoding="utf-8"), p.stem, kind))
    log.info("%s：%d 卡片 → %d chunk", kind, len(files), len(chunks))
    return chunks


def ingest(embedder, writer, chunks, module, batch=256):
    n = 0
    for i in range(0, len(chunks), batch):
        b = chunks[i:i + batch]
        vecs = embedder.embed_batch([c["text"] for c in b])
        writer.upsert_chunks(b, vecs, module=module)
        n += len(b)
        log.info("  %s 已入库 %d/%d", module, n, len(chunks))
    return n


def validate(embedder, writer, queries):
    log.info("=== 检索验证（§14.2 #4，同模型显式 query_embeddings）===")
    for q in queries:
        qv = embedder.embed_batch([q])[0]
        res = writer._collection.query(query_embeddings=[qv], n_results=3,
                                       include=["metadatas", "distances"])
        top = [(m["source_file"], round(1 - d, 3))
               for m, d in zip(res["metadatas"][0], res["distances"][0])]
        log.info("  「%s」→ Top3: %s", q, top)


def main():
    ap = argparse.ArgumentParser(description="S3 理解卡片 RAG 入库")
    ap.add_argument("--tables-dir")
    ap.add_argument("--procs-dir")
    ap.add_argument("--persist-dir", default="scripts/kb-ingest/data/chromadb")
    ap.add_argument("--collection", default="mes_s3_understanding")
    ap.add_argument("--reset", action="store_true", help="先删旧集合再入（换模型/源必用）")
    ap.add_argument("--validate", action="store_true")
    args = ap.parse_args()

    if args.reset:
        try:
            import chromadb
            chromadb.PersistentClient(path=args.persist_dir).delete_collection(args.collection)
            log.info("已删除旧集合 %s", args.collection)
        except Exception as e:
            log.info("无旧集合可删（%s）", e)

    embedder = LocalEmbedder()
    writer = ChromaWriter(args.persist_dir, args.collection)

    total = 0
    if args.tables_dir:
        total += ingest(embedder, writer, load_dir(args.tables_dir, "table"), module="表理解")
    if args.procs_dir:
        total += ingest(embedder, writer, load_dir(args.procs_dir, "proc"), module="过程理解")
    log.info("入库完成：共 %d chunk，集合=%s", total, args.collection)

    if args.validate:
        validate(embedder, writer,
                 ["板坯 slab 信息存在哪张表", "钢卷主数据表", "质量判定 BSQM 过程逻辑",
                  "成本计算过程", "删除记录的存储过程"])


if __name__ == "__main__":
    main()
