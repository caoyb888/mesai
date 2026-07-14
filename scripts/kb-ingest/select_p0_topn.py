#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P0 Top-N 中心度选取器（Sprint 3 · S3-0）
====================================================
文件用途：从 build_dep_graph 产出的 procs.csv / tables.csv 中，按中心度 SCORE
          取 Top-N 单元与表，产出 p0_phase1_units.txt / p0_phase1_tables.txt，
          供 db_introspect --source-units-file 拉 P0 源码深析。
背景：dependency_graph 的百分位分级在万级图上会把 P0 撑到 2000+ 单元（过大不可训练），
      故改用「按中心度 Top-N」硬选。此前该步为即席操作未固化，本脚本将其脚本化以可复现。
作者：AI（芯智云匠 MES AI 开发工程师）
日期：2026-07-14
关联需求单：REQ-MES-AI-20260706-001（占位，待补正式单号）
纯 Python 标准库，不连库、不调外部 AI。
"""
import os
import csv
import argparse


def _read_scored(path, name_col, score_col, inferred_col=None):
    """读 CSV，返回按 SCORE 降序的 (name, score) 列表；可选剔除 INFERRED 行。"""
    rows = []
    with open(path, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if inferred_col and str(r.get(inferred_col, "0")).strip() in ("1", "True", "true"):
                continue  # 剔除推断（虚拟）节点，只保留真实单元
            name = (r.get(name_col) or "").strip()
            if not name:
                continue
            try:
                score = float(r.get(score_col) or 0)
            except ValueError:
                score = 0.0
            rows.append((name, score))
    rows.sort(key=lambda x: x[1], reverse=True)
    return rows


def select_top_units(procs_csv, top_n):
    """取过程清单 Top-N 名称（按 SCORE 降序，剔除 INFERRED，去重保序）。"""
    scored = _read_scored(procs_csv, "NAME", "SCORE", inferred_col="INFERRED")
    out, seen = [], set()
    for name, _ in scored:
        if name in seen:
            continue
        seen.add(name)
        out.append(name)
        if len(out) >= top_n:
            break
    return out


def select_top_tables(tables_csv, top_n):
    """取表清单 Top-N 名称（按 SCORE 降序，去重保序）。"""
    scored = _read_scored(tables_csv, "TABLE", "SCORE")
    out, seen = [], set()
    for name, _ in scored:
        if name in seen:
            continue
        seen.add(name)
        out.append(name)
        if len(out) >= top_n:
            break
    return out


def _write_list(path, header, names):
    with open(path, "w", encoding="utf-8") as f:
        f.write("# " + header + "\n")
        f.write("\n".join(names) + ("\n" if names else ""))


def main():
    ap = argparse.ArgumentParser(description="P0 Top-N 中心度选取器（S3-0）")
    ap.add_argument("--procs-csv", required=True, help="build_dep_graph 产出的 procs.csv")
    ap.add_argument("--tables-csv", required=True, help="build_dep_graph 产出的 tables.csv")
    ap.add_argument("--top-procs", type=int, default=60, help="选取过程/包体数（默认 60）")
    ap.add_argument("--top-tables", type=int, default=100, help="选取表数（默认 100）")
    ap.add_argument("--out-units", required=True, help="输出 p0_phase1_units.txt 路径")
    ap.add_argument("--out-tables", required=True, help="输出 p0_phase1_tables.txt 路径")
    args = ap.parse_args()

    units = select_top_units(args.procs_csv, args.top_procs)
    tables = select_top_tables(args.tables_csv, args.top_tables)
    _write_list(args.out_units, f"P0 Phase-1 核心单元 Top{args.top_procs}（按中心度 SCORE）", units)
    _write_list(args.out_tables, f"P0 Phase-1 核心表 Top{args.top_tables}（按中心度 SCORE）", tables)
    print(f"[完成] Top{args.top_procs} 单元 → {args.out_units}（实得 {len(units)}）")
    print(f"[完成] Top{args.top_tables} 表 → {args.out_tables}（实得 {len(tables)}）")


if __name__ == "__main__":
    main()
