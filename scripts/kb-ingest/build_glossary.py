#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中韩英术语对照表构建器（Sprint 3 · T3-0-5）
====================================================
文件用途：从 SCOAPUSER.SCO_CODE_DETAIL 代码字典抽取术语，按 Unicode 字符类别
          将 CD_NM / CD_DESC 逐格归类到「中/韩/英」三列，产出术语对照表
          （机读 CSV + Markdown 文档）。英文（或中文）缺口列作为后续 Kimi
          批量补译的 TODO，本脚本不调用任何外部 AI，纯 Python 标准库实现。
作者：AI（芯智云匠 MES AI 开发工程师）
日期：2026-07-14
关联需求单：REQ-MES-AI-20260706-001（占位，待补正式单号）
关键约束：
  - 数据库口令仅经运行时环境变量注入（MES_DB_*），严禁落盘。
  - 术语值为钢厂通用工艺名词，无 PII；但仍不打印工号/批次等敏感字面量。
  - 语种判定基于字符 Unicode 区段，不依赖列名假设（本库列≠语言）。
"""
import os
import sys
import csv
import argparse
from collections import defaultdict


# ---------------------------------------------------------------------------
# 语种判定：基于字符 Unicode 区段。优先级 韩 > 中 > 英。
# 理由：本 MES 为韩系系统，CD_NM 为中文本地化名、CD_DESC 多为韩文，
#       但存在英文/空值混入，故逐格判定而非按列假设。
# ---------------------------------------------------------------------------
def classify_lang(text):
    """返回 'ko'/'zh'/'en'/None（纯数字或符号无法归类）。"""
    if not text:
        return None
    has_hangul = has_han = has_latin = False
    for ch in text:
        o = ord(ch)
        # 韩文：谚文音节 + 兼容字母 + 字母区
        if 0xAC00 <= o <= 0xD7A3 or 0x1100 <= o <= 0x11FF or 0x3130 <= o <= 0x318F:
            has_hangul = True
        # 中文：CJK 统一表意 + 扩展A + 兼容表意
        elif 0x4E00 <= o <= 0x9FFF or 0x3400 <= o <= 0x4DBF or 0xF900 <= o <= 0xFAFF:
            has_han = True
        elif ("A" <= ch <= "Z") or ("a" <= ch <= "z"):
            has_latin = True
    if has_hangul:
        return "ko"
    if has_han:
        return "zh"
    if has_latin:
        return "en"
    return None


def slot_row(cd_nm, cd_desc):
    """把 CD_NM / CD_DESC 两个候选值按语种落到 zh/ko/en 三槽位。"""
    slots = {"zh": "", "ko": "", "en": ""}
    for val in (cd_nm, cd_desc):
        if val is None:
            continue
        v = val.strip()
        if not v:
            continue
        lang = classify_lang(v)
        if lang and not slots[lang]:
            slots[lang] = v
    return slots


def fetch_rows(dsn, user, password, only_active):
    """连库拉取 SCO_CODE_DETAIL 术语行。口令仅运行时使用，不落盘。"""
    import oracledb  # 延迟导入：无 DB 场景（如单测）也能加载本模块

    conn = oracledb.connect(user=user, password=password, dsn=dsn)
    try:
        cur = conn.cursor()
        where = "where use_yn = 'Y'" if only_active else ""
        cur.execute(
            "select master_cd, cd_val, cd_nm, cd_desc, use_yn "
            "from SCOAPUSER.SCO_CODE_DETAIL " + where + " "
            "order by master_cd, disp_seq, cd_val"
        )
        return cur.fetchall()
    finally:
        conn.close()


def build_entries(rows):
    """行级映射：每条 (master_cd, cd_val) → 中/韩/英 三列。"""
    entries = []
    for master_cd, cd_val, cd_nm, cd_desc, use_yn in rows:
        slots = slot_row(cd_nm, cd_desc)
        entries.append(
            {
                "master_cd": master_cd or "",
                "cd_val": cd_val or "",
                "zh": slots["zh"],
                "ko": slots["ko"],
                "en": slots["en"],
                "use_yn": use_yn or "",
            }
        )
    return entries


def dedup_terms(entries):
    """术语级去重：按 (zh, ko, en) 三元组合并，统计出现次数与示例代码组。"""
    bucket = {}
    for e in entries:
        key = (e["zh"], e["ko"], e["en"])
        if key == ("", "", ""):
            continue  # 三语皆空（纯数字/符号代码）跳过
        if key not in bucket:
            bucket[key] = {
                "zh": e["zh"],
                "ko": e["ko"],
                "en": e["en"],
                "count": 0,
                "sample_group": e["master_cd"],
                "groups": set(),
            }
        bucket[key]["count"] += 1
        bucket[key]["groups"].add(e["master_cd"])
    terms = list(bucket.values())
    # 排序：有中文的优先，其次按中文/韩文字典序，便于人工校对
    terms.sort(key=lambda t: (t["zh"] == "", t["zh"], t["ko"], t["en"]))
    return terms


def coverage_stats(terms):
    """统计三语覆盖情况，定位翻译缺口。"""
    total = len(terms)
    has_zh = sum(1 for t in terms if t["zh"])
    has_ko = sum(1 for t in terms if t["ko"])
    has_en = sum(1 for t in terms if t["en"])
    all_three = sum(1 for t in terms if t["zh"] and t["ko"] and t["en"])
    zh_ko = sum(1 for t in terms if t["zh"] and t["ko"])
    need_en = sum(1 for t in terms if not t["en"])
    need_zh = sum(1 for t in terms if not t["zh"])
    return {
        "total": total,
        "has_zh": has_zh,
        "has_ko": has_ko,
        "has_en": has_en,
        "all_three": all_three,
        "zh_ko": zh_ko,
        "need_en": need_en,
        "need_zh": need_zh,
    }


def write_terms_csv(path, terms):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["中文(zh)", "韩文(ko)", "英文(en)", "出现次数", "示例代码组", "关联代码组数"])
        for t in terms:
            w.writerow([t["zh"], t["ko"], t["en"], t["count"], t["sample_group"], len(t["groups"])])


def write_mapping_csv(path, entries):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["代码组(master_cd)", "代码值(cd_val)", "中文(zh)", "韩文(ko)", "英文(en)", "启用(use_yn)"])
        for e in entries:
            w.writerow([e["master_cd"], e["cd_val"], e["zh"], e["ko"], e["en"], e["use_yn"]])


def write_markdown(path, terms, stats, entries, sample_n=60):
    st = stats
    pct = lambda n: f"{n} ({n * 100 // max(st['total'], 1)}%)"
    lines = []
    lines.append("# 中韩英术语对照表（Sprint 3 · T3-0-5）\n")
    lines.append("> 关联需求单：REQ-MES-AI-20260706-001 ｜ 生成脚本：`scripts/kb-ingest/build_glossary.py`")
    lines.append("> 数据源：`SCOAPUSER.SCO_CODE_DETAIL`（代码字典，自带中/韩双语，部分英文）")
    lines.append("> 生成方式：逐格 Unicode 语种判定，纯标准库，**未调用外部 AI**。\n")
    lines.append("## 一、方法说明\n")
    lines.append("本 MES 为韩系系统，代码字典中 `CD_NM` 多为中文本地化名、`CD_DESC` 多为韩文，")
    lines.append("但存在英文混入、语言错位、空值等情况（**列 ≠ 语言**）。故本表对每个候选值")
    lines.append("按字符 Unicode 区段逐格判定语种（韩文谚文 / CJK 表意 / 拉丁字母），")
    lines.append("再落位到「中 / 韩 / 英」三列，空缺列即为后续需补译的缺口。\n")
    lines.append("**结构性说明**：源表每条仅 `CD_NM` / `CD_DESC` 两个名字列，单条最多承载两种")
    lines.append("语言，故「三语齐全」天然为 0——本表由字典产出的是**双语对**（多为中-韩或")
    lines.append("中-英），三语补全须由 Kimi 翻译第三语（T3-0-5 收尾，见第三节）。")
    lines.append("实测该克隆字典已大量本地化为中文，韩文仅约占 1/5。\n")
    lines.append("## 二、覆盖统计（术语级去重后）\n")
    lines.append("| 指标 | 数量 |")
    lines.append("|------|------|")
    lines.append(f"| 去重术语总数 | {st['total']} |")
    lines.append(f"| 含中文 | {pct(st['has_zh'])} |")
    lines.append(f"| 含韩文 | {pct(st['has_ko'])} |")
    lines.append(f"| 含英文 | {pct(st['has_en'])} |")
    lines.append(f"| 中韩齐全 | {pct(st['zh_ko'])} |")
    lines.append(f"| **三语齐全** | {pct(st['all_three'])} |")
    lines.append(f"| 缺英文（待补译 TODO） | {pct(st['need_en'])} |")
    lines.append(f"| 缺中文（待补译 TODO） | {pct(st['need_zh'])} |")
    lines.append("")
    lines.append("## 三、缺口与后续（T3-0-5 收尾）\n")
    lines.append(f"- **英文缺口 {st['need_en']} 条**：字典本身极少提供英文，需 Kimi 批量译（外部 AI，")
    lines.append("  须先获训练需求单批准 + 走脱敏审计，见 `Sprint3_Training_Plan_2026.md` 未决事项 #4）。")
    lines.append(f"- **中文缺口 {st['need_zh']} 条**：多为英文/韩文-only 的代码枚举，Kimi 译中后 BIZ 复核。")
    lines.append("- 源码内韩文术语（非字典）尚未并入本表：需 P0 源码（`meta_p0.json`）抽取，属增量。")
    lines.append("- 完整机读表见同目录 CSV，本文件仅列样例。\n")
    lines.append(f"## 四、术语样例（前 {sample_n} 条，完整见 CSV）\n")
    lines.append("| 中文 | 韩文 | 英文 | 次数 |")
    lines.append("|------|------|------|------|")
    for t in terms[:sample_n]:
        zh = t["zh"].replace("|", "\\|")
        ko = t["ko"].replace("|", "\\|")
        en = t["en"].replace("|", "\\|")
        lines.append(f"| {zh} | {ko} | {en} | {t['count']} |")
    lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description="中韩英术语对照表构建器（T3-0-5）")
    ap.add_argument("--out-dir", required=True, help="产物输出目录（持久化，勿用会话级 scratchpad）")
    ap.add_argument("--all", action="store_true", help="含未启用代码（默认仅 use_yn=Y）")
    ap.add_argument("--from-csv", help="离线模式：从已导出的 SCO_CODE_DETAIL CSV 读入，跳过连库")
    ap.add_argument("--sample-n", type=int, default=60, help="Markdown 样例条数")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    if args.from_csv:
        rows = []
        with open(args.from_csv, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                rows.append(
                    (r.get("MASTER_CD"), r.get("CD_VAL"), r.get("CD_NM"), r.get("CD_DESC"), r.get("USE_YN"))
                )
    else:
        user = os.environ.get("MES_DB_USER")
        password = os.environ.get("MES_DB_PASSWORD")
        dsn = os.environ.get("MES_DB_DSN")
        if not (user and password and dsn):
            print("[错误] 缺少 MES_DB_USER / MES_DB_PASSWORD / MES_DB_DSN 环境变量", file=sys.stderr)
            sys.exit(2)
        rows = fetch_rows(dsn, user, password, only_active=not args.all)

    entries = build_entries(rows)
    terms = dedup_terms(entries)
    stats = coverage_stats(terms)

    terms_csv = os.path.join(args.out_dir, "glossary_zh_ko_en.csv")
    mapping_csv = os.path.join(args.out_dir, "glossary_code_mapping.csv")
    md_path = os.path.join(args.out_dir, "glossary_zh_ko_en.md")
    write_terms_csv(terms_csv, terms)
    write_mapping_csv(mapping_csv, entries)
    write_markdown(md_path, terms, stats, entries, sample_n=args.sample_n)

    print(f"[完成] 行级映射 {len(entries)} 条 → {mapping_csv}")
    print(f"[完成] 去重术语 {stats['total']} 条 → {terms_csv}")
    print(f"[完成] 对照表文档 → {md_path}")
    print(f"[统计] 含中 {stats['has_zh']} / 含韩 {stats['has_ko']} / 含英 {stats['has_en']} "
          f"/ 三语齐全 {stats['all_three']} / 缺英 {stats['need_en']} / 缺中 {stats['need_zh']}")


if __name__ == "__main__":
    main()
