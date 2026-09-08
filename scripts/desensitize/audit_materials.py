#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脱敏审计工具（S3 训练前置合规门）
====================================================
文件用途：对将要外发给外部 AI（Kimi）的训练素材——P0 源码 / 表卡片 / 术语表——
          逐条运行**与网关同一套**脱敏规则（desensitize_verbose），统计命中并定位，
          产出「脱敏审计报告」，作为 S3-1/S3-2 训练前的合规证据与误报排查依据。
设计：复用 `src/ai-gateway/app/services/desensitize.py`（单一真源，避免规则漂移，
      呼应 CLAUDE.md 14.1「入库/查询须同一模型」的同源原则）。
作者：AI（芯智云匠 MES AI 开发工程师）
日期：2026-07-14
关联需求单：REQ-MES-AI-20260706-001（占位，待补正式单号）
纯 Python 标准库 + 复用网关脱敏模块；不连库、不调外部 AI。
"""
import os
import sys
import csv
import json
import argparse
from collections import Counter, defaultdict

# 复用网关脱敏引擎（单一真源）
_HERE = os.path.dirname(os.path.abspath(__file__))
_GATEWAY = os.path.abspath(os.path.join(_HERE, "..", "..", "src", "ai-gateway"))
sys.path.insert(0, _GATEWAY)
from app.services.desensitize import desensitize_verbose  # noqa: E402


def _record(hits_acc, material, location, hits):
    """把一段文本的命中明细累加到全局清单。"""
    for h in hits:
        hits_acc.append({
            "material": material,
            "location": location,
            "category": h["category"],
            "name": h["name"],
            "match": h["match"],
        })


def audit_plsql_json(path, hits_acc):
    """审计 db_introspect 源码 JSON：逐个带源码的程序单元审其源码。"""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    units = data.get("program_units", [])
    audited = 0
    for u in units:
        src = u.get("source")
        if not src:
            continue
        audited += 1
        name = f"{u.get('object_type','')} {u.get('name','')}".strip()
        _, hits = desensitize_verbose(src)
        _record(hits_acc, os.path.basename(path), name, hits)
    return audited


def audit_text_file(path, hits_acc):
    """审计纯文本/Markdown：逐行审，定位到行号。"""
    n = 0
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            n += 1
            _, hits = desensitize_verbose(line)
            _record(hits_acc, os.path.basename(path), f"L{i}", hits)
    return n


def audit_csv_file(path, hits_acc):
    """审计 CSV：逐行拼接单元格后审，定位到行号。"""
    n = 0
    with open(path, encoding="utf-8-sig", newline="") as f:
        for i, row in enumerate(csv.reader(f), 1):
            n += 1
            _, hits = desensitize_verbose(" ".join(row))
            _record(hits_acc, os.path.basename(path), f"row{i}", hits)
    return n


def dispatch(path, hits_acc):
    """按文件类型选择审计方式。"""
    lower = path.lower()
    if lower.endswith(".json"):
        # 仅当含 program_units 时按 PL/SQL 源码审，否则按文本
        try:
            with open(path, encoding="utf-8") as f:
                head = json.load(f)
            if isinstance(head, dict) and "program_units" in head:
                return "plsql", audit_plsql_json(path, hits_acc)
        except (json.JSONDecodeError, OSError):
            pass
        return "text", audit_text_file(path, hits_acc)
    if lower.endswith(".csv"):
        return "csv", audit_csv_file(path, hits_acc)
    return "text", audit_text_file(path, hits_acc)


def render_report(hits_acc, audited_summary, sample_n=20):
    """渲染脱敏审计报告 Markdown。"""
    by_cat = Counter(h["category"] for h in hits_acc)
    by_mat = Counter(h["material"] for h in hits_acc)
    L = []
    L.append("# 脱敏审计报告（S3 训练前置合规门）\n")
    L.append("> 关联需求单：REQ-MES-AI-20260706-001 ｜ 工具：`scripts/desensitize/audit_materials.py`")
    L.append("> 规则源：`src/ai-gateway/app/services/desensitize.py`（与网关外发同一套，CLAUDE.md 4.2 全 7 类）")
    L.append("> 目的：确认外发 Kimi 的训练素材无敏感信息泄露；命中项供人工核验误报/真实风险。\n")
    verdict = "✅ 未命中任何脱敏规则（素材可外发）" if not hits_acc \
        else f"⚠️ 命中 {len(hits_acc)} 处，需人工核验（见下方明细；多为业务标识误报时可放行）"
    L.append(f"## 结论：{verdict}\n")
    L.append("## 一、受审素材\n")
    L.append("| 素材文件 | 审计单位数 | 方式 |")
    L.append("|----------|-----------|------|")
    for mat, (kind, cnt) in audited_summary.items():
        L.append(f"| {mat} | {cnt} | {kind} |")
    L.append("")
    L.append("## 二、命中分类统计\n")
    if not hits_acc:
        L.append("（无命中）\n")
    else:
        L.append("| 类别 | 命中数 |")
        L.append("|------|--------|")
        for cat, c in by_cat.most_common():
            L.append(f"| {cat} | {c} |")
        L.append("")
        L.append("### 按素材\n")
        L.append("| 素材 | 命中数 |")
        L.append("|------|--------|")
        for mat, c in by_mat.most_common():
            L.append(f"| {mat} | {c} |")
        L.append("")
        L.append(f"## 三、命中明细采样（每类前 {sample_n} 条，供人工核验）\n")
        grouped = defaultdict(list)
        for h in hits_acc:
            grouped[h["category"]].append(h)
        for cat, items in grouped.items():
            L.append(f"### {cat}（{items[0]['name']}），共 {len(items)} 处\n")
            L.append("| 素材 | 位置 | 命中串 |")
            L.append("|------|------|--------|")
            for h in items[:sample_n]:
                m = h["match"].replace("|", "\\|")
                L.append(f"| {h['material']} | {h['location']} | `{m}` |")
            L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="脱敏审计工具（S3 训练前置合规门）")
    ap.add_argument("--material", action="append", required=True,
                    help="待审素材文件（可重复）：P0源码JSON / 表卡片md / 术语表csv 等")
    ap.add_argument("--out-report", required=True, help="输出脱敏审计报告 Markdown")
    ap.add_argument("--out-json", help="输出命中明细 JSON（可选）")
    ap.add_argument("--sample-n", type=int, default=20, help="每类明细采样条数")
    ap.add_argument("--strict", action="store_true",
                    help="严格模式：有任何命中即以退出码 1 结束（供 CI 门禁）")
    args = ap.parse_args()

    hits_acc = []
    audited_summary = {}
    for path in args.material:
        if not os.path.exists(path):
            print(f"[警告] 素材不存在，跳过：{path}", file=sys.stderr)
            continue
        kind, cnt = dispatch(path, hits_acc)
        audited_summary[os.path.basename(path)] = (kind, cnt)

    report = render_report(hits_acc, audited_summary, sample_n=args.sample_n)
    with open(args.out_report, "w", encoding="utf-8") as f:
        f.write(report)
    if args.out_json:
        with open(args.out_json, "w", encoding="utf-8") as f:
            json.dump(hits_acc, f, ensure_ascii=False, indent=2)

    by_cat = Counter(h["category"] for h in hits_acc)
    print(f"[完成] 审计报告 → {args.out_report}")
    print(f"[统计] 素材 {len(audited_summary)} 份 / 总命中 {len(hits_acc)} 处"
          f" / 分类 {dict(by_cat)}")
    if args.strict and hits_acc:
        print("[严格模式] 存在命中，退出码 1", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
