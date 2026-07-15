#!/usr/bin/env python3
"""
T3-4-2：从 P0 静态分析确定性生成业务逻辑断言种子（CLAUDE.md 第七章）

来源（均为静态、不调外部 AI）：
  · 存储过程 proc_parser：set_assignments（状态流转）/ write_tables（写副作用）/ read_tables（表关系）
  · 表卡片 jsonl：主键（结构性断言）

产物：/assertions/{state-machine,sql-logic,api-behavior}/*.jsonl + manifest.md
每条断言含 level（Critical/High/Medium）、category、asset、statement、evidence、source。

用法：
  python3 build_assertion_seeds.py --meta <meta_p0.json> --cards <p0_table_cards.jsonl> --out assertions

关联需求单：REQ-MES-AI-20260715-001
作者：AI（芯智云匠）  日期：2026-07-15
"""
import os
import sys
import json
import argparse
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from proc_parser import analyze_metadata


def _emit(seq, level, category, asset, statement, evidence):
    return {"id": f"AS-{category[:2].upper()}-{seq:04d}", "level": level,
            "category": category, "asset": asset, "statement": statement,
            "evidence": evidence, "source": "static"}


def gen_from_procs(meta):
    """从 P0 包体静态分析产 状态流转 / 写副作用 / 表关系 断言"""
    sm, sl, ab = [], [], []
    for a in analyze_metadata(meta):
        pkg = a.name
        # ① 状态流转（set 列=字面量）→ state-machine，High
        for s in a.set_assignments:
            if not s.get("value"):
                continue
            sm.append(_emit(len(sm) + 1, "High", "state-machine", pkg,
                            f"包 {pkg} 存在状态写入：{s['table']}.{s['column']} 可被置为 '{s['value']}'",
                            s))
        # ② 写副作用 → sql-logic，Medium
        for w in a.write_tables:
            sl.append(_emit(len(sl) + 1, "Medium", "sql-logic", pkg,
                            f"包 {pkg} 对表 {w['table']} 执行 {'/'.join(w['ops'])}",
                            w))
        # ③ 表关系（读取集）→ api-behavior，Medium（取前若干，避免爆炸）
        if a.read_tables:
            ab.append(_emit(len(ab) + 1, "Medium", "api-behavior", pkg,
                            f"包 {pkg} 读取表：{', '.join(a.read_tables[:12])}"
                            + ("…" if len(a.read_tables) > 12 else ""),
                            {"read_tables": a.read_tables, "has_dynamic_sql": a.has_dynamic_sql}))
    return sm, sl, ab


def gen_from_cards(cards_path):
    """从表卡片产 结构性主键断言（Critical）"""
    out = []
    if not cards_path or not Path(cards_path).exists():
        return out
    for ln in open(cards_path, encoding="utf-8"):
        if not ln.strip():
            continue
        c = json.loads(ln)
        pk = c.get("pk")
        if pk:
            out.append(_emit(len(out) + 1, "Critical", "state-machine", c["table"],
                             f"表 {c['table']} 主键为 {pk}",
                             {"table": c["table"], "pk": pk, "owner": c.get("owner")}))
    return out


def write_cat(out_dir, cat, rows):
    d = out_dir / cat
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{cat}_seeds.jsonl"
    with open(p, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return p


def main():
    ap = argparse.ArgumentParser(description="P0 断言种子生成器（T3-4-2）")
    ap.add_argument("--meta", required=True, help="meta_p0.json（含 P0 包体源码）")
    ap.add_argument("--cards", help="p0_table_cards.jsonl（表卡片，产主键断言）")
    ap.add_argument("--out", default="assertions", help="断言输出根目录")
    args = ap.parse_args()

    meta = json.load(open(args.meta, encoding="utf-8"))
    out = Path(args.out)
    sm, sl, ab = gen_from_procs(meta)
    sm = gen_from_cards(args.cards) + sm  # 结构性主键断言并入 state-machine 前部

    write_cat(out, "state-machine", sm)
    write_cat(out, "sql-logic", sl)
    write_cat(out, "api-behavior", ab)

    total = len(sm) + len(sl) + len(ab)
    lv = Counter(r["level"] for r in sm + sl + ab)
    # 覆盖度：每个 P0 包断言数
    per_pkg = Counter(r["asset"] for r in sm + sl + ab)
    lt3 = [k for k, v in per_pkg.items() if v < 3]

    manifest = out / "manifest.md"
    manifest.write_text(
        "# 业务逻辑断言种子（T3-4-2，静态生成）\n\n"
        f"生成自 P0 静态分析（proc_parser + 表卡片），需求单 REQ-MES-AI-20260715-001。\n\n"
        f"- **总计 {total} 条**：state-machine {len(sm)} / sql-logic {len(sl)} / api-behavior {len(ab)}\n"
        f"- 级别分布：{dict(lv)}\n"
        f"- 覆盖资产（含表+包）：{len(per_pkg)}；断言数 <3 的资产：{len(lt3)}（多为写/状态少的只读包）\n\n"
        "> 种子为**候选**，须技术负责人审核后纳入基准库（CLAUDE.md §7.3 变更须审批）；\n"
        "> Critical=结构性主键（100% 必过）、High=状态流转、Medium=写副作用/表关系。\n",
        encoding="utf-8")
    print(f"断言种子：{total} 条（SM {len(sm)} / SL {len(sl)} / AB {len(ab)}），"
          f"级别 {dict(lv)}，覆盖资产 {len(per_pkg)}")
    print(f"输出：{out}/  manifest：{manifest}")


if __name__ == "__main__":
    main()
