#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P0 表卡片生成器（Sprint 3 · S3-0 / T3-1 素材）
====================================================
文件用途：为 Top-N P0 核心表拼装「表卡片」——结构（来自 db_introspect 盘点 JSON）
          + 列语义（来自字典 CSV，克隆库注释全空故字典是唯一语义源）
          + 热度画像（来自依赖图 tables.csv：被读/写过程数、操作类型、中心度）。
          产出人读 Markdown（供评审/RAG）+ 机读 JSONL（供入库切块）。
背景：本库为 Oracle，owner=MESAPUSER；克隆库列注释为空，语义全靠字典 CSV 反哺。
      卡片头部明确标注 owner 使用规则，避免 LLM 误把 owner 当表名前缀（见 CLAUDE.md 14.2）。
作者：AI（芯智云匠 MES AI 开发工程师）
日期：2026-07-14
关联需求单：REQ-MES-AI-20260706-001（占位，待补正式单号）
纯 Python 标准库，不连库、不调外部 AI。
"""
import os
import csv
import json
import sys
import argparse


# ---------------------------------------------------------------------------
# 数据加载
# ---------------------------------------------------------------------------
def load_p0_tables(path):
    """读 p0_phase1_tables.txt（# 开头为注释），返回表名列表（保序）。"""
    names = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                names.append(line.upper())
    return names


def load_meta_tables(path):
    """读盘点 JSON，返回 {表名大写: 表条目}。"""
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    tables = d.get("tables", [])
    if isinstance(tables, dict):
        tables = list(tables.values())
    return {(t.get("name") or "").upper(): t for t in tables}, d.get("owner", "")


def load_dict(path):
    """读字典 CSV，返回 {(表名大写, 列名大写): (语义注释, 来源)}。"""
    idx = {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            tbl = (r.get("TABLE_NAME") or "").strip().upper()
            col = (r.get("COLUMN_NAME") or "").strip().upper()
            if not tbl or not col:
                continue
            comment = (r.get("COL_COMMENT") or "").strip()
            source = (r.get("SOURCE") or "").strip()
            idx[(tbl, col)] = (comment, source)
    return idx


def load_table_heat(path):
    """读依赖图 tables.csv，返回 {表名大写: {read, write, ops, score, tier}}。"""
    idx = {}
    if not path or not os.path.exists(path):
        return idx
    with open(path, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            name = (r.get("TABLE") or "").strip().upper()
            if not name:
                continue
            idx[name] = {
                "read": r.get("READ_PROCS", ""),
                "write": r.get("WRITE_PROCS", ""),
                "ops": r.get("OPS", ""),
                "score": r.get("SCORE", ""),
                "tier": r.get("TIER", ""),
            }
    return idx


# ---------------------------------------------------------------------------
# 卡片构建
# ---------------------------------------------------------------------------
def fmt_type(col):
    """把类型 + 长度格式化为 VARCHAR2(30) / NUMBER 等展示形式。"""
    dt = col.get("data_type") or ""
    length = col.get("length")
    if dt in ("VARCHAR2", "CHAR", "NVARCHAR2", "NCHAR", "RAW") and length:
        return f"{dt}({length})"
    return dt


def build_card(tbl_name, meta_tbl, dict_idx, heat):
    """组装单表卡片的结构化数据。"""
    owner = meta_tbl.get("owner", "")
    columns = meta_tbl.get("columns", []) or []
    pk_cols = [c["name"] for c in columns if c.get("is_primary")]
    card_cols = []
    filled = 0
    for c in sorted(columns, key=lambda x: x.get("position") or 0):
        cname = c.get("name", "")
        comment, source = dict_idx.get((tbl_name, cname.upper()), ("", ""))
        if comment:
            filled += 1
        card_cols.append(
            {
                "name": cname,
                "type": fmt_type(c),
                "nullable": bool(c.get("nullable", True)),
                "is_pk": bool(c.get("is_primary")),
                "semantic": comment,
                "source": source,
            }
        )
    h = heat.get(tbl_name, {})
    return {
        "table": tbl_name,
        "owner": owner,
        "num_rows": meta_tbl.get("num_rows"),
        "pk": pk_cols,
        "score": h.get("score", ""),
        "tier": h.get("tier", ""),
        "read_procs": h.get("read", ""),
        "write_procs": h.get("write", ""),
        "ops": h.get("ops", ""),
        "col_total": len(card_cols),
        "col_filled": filled,
        "columns": card_cols,
    }


def render_card_md(card):
    """把单表卡片渲染为 Markdown。"""
    L = []
    L.append(f"### {card['table']}\n")
    pk = "、".join(card["pk"]) if card["pk"] else "（无显式主键）"
    heat = (f"中心度 SCORE={card['score']}｜被读 {card['read_procs']} 过程 / "
            f"被写 {card['write_procs']} 过程｜操作 {card['ops'] or '—'}")
    cov = f"{card['col_filled']}/{card['col_total']}"
    L.append(f"- **Owner**：`{card['owner']}`（Oracle；同库同用户直接写表名，跨 schema 才加 `{card['owner']}.` 前缀）")
    L.append(f"- **画像**：{card['tier']}｜{heat}")
    L.append(f"- **行数(克隆库)**：{card['num_rows']}　**主键**：{pk}　**语义覆盖**：{cov}")
    L.append("")
    L.append("| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |")
    L.append("|---|------|------|----|----|------|------|")
    for i, c in enumerate(card["columns"], 1):
        nul = "Y" if c["nullable"] else "N"
        pkm = "✓" if c["is_pk"] else ""
        sem = (c["semantic"] or "").replace("|", "\\|").replace("\n", " ")
        src = c["source"] or ""
        L.append(f"| {i} | {c['name']} | {c['type']} | {nul} | {pkm} | {sem} | {src} |")
    L.append("")
    return "\n".join(L)


def render_doc(cards, owner, missing):
    """渲染全量表卡片 Markdown 文档（含头部说明 + 覆盖统计）。"""
    total_cols = sum(c["col_total"] for c in cards)
    filled_cols = sum(c["col_filled"] for c in cards)
    pct = filled_cols * 100 // max(total_cols, 1)
    L = []
    L.append("# P0 核心表卡片（Sprint 3 · S3-0 素材）\n")
    L.append("> 关联需求单：REQ-MES-AI-20260706-001 ｜ 生成脚本：`scripts/kb-ingest/build_table_cards.py`")
    L.append("> 结构源：`db_introspect` 盘点 JSON ｜ 语义源：字典 CSV（`data_dictionary_full.csv`）"
             "｜ 热度源：依赖图 `tables.csv`")
    L.append("> 纯本地拼装，**未调用外部 AI**。每张卡片 = 一个「表字段理解」训练/RAG 单元。\n")
    L.append("## 使用须知（务必先读）\n")
    L.append(f"1. **Owner/Schema**：本库为 Oracle，所有 P0 表属 `{owner}`。SQL 中若以 `{owner}` "
             f"用户连接则**直接写表名**；跨 schema 访问才加 `{owner}.` 前缀。**切勿把 owner 当作表名的一部分**。")
    L.append("2. **列语义来源于字典 CSV**：克隆库列注释全空，语义（中文/英文）由生产库导出的字典反哺；")
    L.append("   `来源` 列标注该语义出处（DB注释(中文)/DB注释(非中文)/SCO_DATA_DIC/空）。`空` = 该列暂无语义，属缺口。")
    L.append("3. **画像**中「被读/被写过程数」来自 PL/SQL 静态依赖图，反映该表在业务中的热度与读写角色。\n")
    L.append("## 覆盖统计\n")
    L.append(f"- 卡片数（P0 表）：**{len(cards)}**")
    L.append(f"- 字段总数：**{total_cols}**　有语义：**{filled_cols}（{pct}%）**　语义缺口：**{total_cols - filled_cols}**")
    if missing:
        L.append(f"- ⚠️ 未在盘点中找到结构（可能为视图/已删）：{len(missing)} 张 → {', '.join(missing)}")
    L.append("")
    L.append("---\n")
    for c in cards:
        L.append(render_card_md(c))
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="P0 表卡片生成器（S3-0）")
    ap.add_argument("--meta", required=True, help="db_introspect 盘点 JSON（含结构，可 --no-source）")
    ap.add_argument("--dict-csv", required=True, help="列语义字典 CSV")
    ap.add_argument("--p0-tables", required=True, help="P0 表名单 txt（p0_phase1_tables.txt）")
    ap.add_argument("--tables-csv", help="依赖图 tables.csv（热度画像，可选）")
    ap.add_argument("--out-md", required=True, help="输出全量表卡片 Markdown")
    ap.add_argument("--out-jsonl", help="输出机读 JSONL（每表一行，供入库切块，可选）")
    args = ap.parse_args()

    p0 = load_p0_tables(args.p0_tables)
    meta_idx, owner = load_meta_tables(args.meta)
    dict_idx = load_dict(args.dict_csv)
    heat = load_table_heat(args.tables_csv)

    cards, missing = [], []
    for name in p0:
        mt = meta_idx.get(name)
        if not mt:
            missing.append(name)
            continue
        cards.append(build_card(name, mt, dict_idx, heat))

    doc = render_doc(cards, owner, missing)
    with open(args.out_md, "w", encoding="utf-8") as f:
        f.write(doc)

    if args.out_jsonl:
        with open(args.out_jsonl, "w", encoding="utf-8") as f:
            for c in cards:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")

    total_cols = sum(c["col_total"] for c in cards)
    filled_cols = sum(c["col_filled"] for c in cards)
    print(f"[完成] 表卡片 {len(cards)} 张 → {args.out_md}")
    if args.out_jsonl:
        print(f"[完成] 机读 JSONL → {args.out_jsonl}")
    print(f"[统计] 字段 {total_cols} / 有语义 {filled_cols}"
          f"（{filled_cols * 100 // max(total_cols, 1)}%）/ 缺口 {total_cols - filled_cols}"
          f" / 未找到结构 {len(missing)}")


if __name__ == "__main__":
    main()
