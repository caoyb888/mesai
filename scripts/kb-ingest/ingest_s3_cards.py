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
import sys
import argparse
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kb_ingest import LocalEmbedder, ChromaWriter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def chunk_card(text, asset, kind, max_chars=700, overlap=120):
    """卡片切块：短卡片整块；长卡片定长窗口 + 重叠；每块前缀资产名利于召回。"""
    text = (text or "").strip()
    if not text:
        return []
    if len(text) <= max_chars:
        pieces = [text]
    else:
        pieces, i = [], 0
        while i < len(text):
            pieces.append(text[i:i + max_chars])
            i += max_chars - overlap
    out = []
    for j, ch in enumerate(pieces):
        body = f"[{kind}] {asset}\n{ch}"
        out.append({
            "chunk_id": f"{kind}:{asset}:{j}",
            "text": body,
            "chunk_type": f"s3_{kind}",
            "source_file": f"{asset}.md",
            "token_count": len(body) // 3,
        })
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
