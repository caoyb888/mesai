#!/usr/bin/env python3
"""
注释编码治理器 → 乱码修复 + 质量三级分级 + 《注释乱码清单》

用途：消费 db_introspect.py 产出的元数据 JSON（或甲方数据字典 CSV），
     对表/字段注释做「乱码修复 + 质量分级」，并产出：
       ① 清洗建议文件（CSV）——修复后的注释作为【建议】，不覆盖原始源；
       ② 《注释乱码清单》（Markdown）——recoverable（可修复待确认）+ garbled（不可恢复）。

设计原则（对齐 CLAUDE.md）：
  · 不静默改源：修复结果一律标记为「建议 / 待人工确认」，原文完整保留；
  · 零新依赖：仅用 Python 标准库（codecs/csv/json/unicodedata），低配机即可跑；
  · 可直接消费甲方现成的 data_dictionary_full.csv，无需连库即可先出乱码清单。

质量三级（tier）：
  · clean       ——注释本身可读（中文/英文/数字），无需处理；
  · recoverable ——原文疑似乱码，但找到可信逆变换恢复出有效中文（给出修复建议，待确认）；
  · garbled     ——含替换符/控制字符/问号化，或无可信修复方案，需人工/甲方确认。
  （另有 empty：注释为空/纯空白，单独统计，联动"字段注释为空"目标清单。）

Oracle 中文库典型乱码：GBK 字节被当 Latin-1 解码（→ latin-1→gb18030 恢复），
或 UTF-8 字节被当 Latin-1 解码（→ latin-1→utf-8 恢复）。

用法：
    # 自测（内置样例，低配机秒出，验证分级逻辑）
    python encoding_normalizer.py --self-test

    # 直接治理甲方数据字典 CSV（当前即可跑）
    python encoding_normalizer.py --input-csv ../../docs/data_dictionary_full.csv \
        --out-cleaned cleaned_comments.csv --out-report 注释乱码清单.md

    # 治理自省 JSON（拿到测试机自省后）
    python encoding_normalizer.py --input metadata_mesapuser.json \
        --out-cleaned cleaned_comments.csv --out-report 注释乱码清单.md

关联任务：S2.9-3 编码治理与注释质量分级（AI-MES-PLAN-ADJ-2026-001）
作者：AI（芯智云匠）
日期：2026-07-06
"""

import os
import sys
import csv
import json
import argparse
import logging
from dataclasses import dataclass
from typing import Optional, Iterator, Callable

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))  # 字典 CSV 可能含超长注释

# ── 质量分级常量 ──────────────────────────────────────────────
TIER_EMPTY = "empty"
TIER_CLEAN = "clean"
TIER_RECOVERABLE = "recoverable"
TIER_GARBLED = "garbled"


# ── 字符分类（打分依据）──────────────────────────────────────

# 关键：本 MES 为韩系系统，注释含中/韩/英多语言。
# 「可读语言」（中文/韩文/假名/CJK 标点）绝不判为乱码；
# 真正的乱码信号仅限 Latin-1 补充区（GBK/UTF-8 字节被当 Latin-1 解码所致）。

def _is_good_cjk(o: int) -> bool:
    """得分奖励字符：常用汉字 + 谚文（韩文），正确解码后的主体内容"""
    return (0x4E00 <= o <= 0x9FFF          # CJK 统一表意（常用汉字）
            or 0xAC00 <= o <= 0xD7A3       # 谚文音节（韩文，合法内容）
            or 0x1100 <= o <= 0x11FF)      # 谚文字母

def _is_readable(o: int) -> bool:
    """人类可读字符（判定 clean 用）：汉字/韩文/假名/CJK 标点/全角/ASCII"""
    return (_is_good_cjk(o)
            or 0x3040 <= o <= 0x30FF       # 平/片假名（日文，可读）
            or 0x3000 <= o <= 0x303F       # CJK 标点
            or 0xFF00 <= o <= 0xFFEF       # 全角 / 半角形式
            or _is_ascii_print(o))

def _is_mojibake(o: int) -> bool:
    """真正的乱码信号：拉丁-1 补充 + 拉丁扩展-A（错误字符集解码高发区）"""
    return 0x0080 <= o <= 0x024F

def _is_penalized(o: int) -> bool:
    """得分惩罚字符（用于修复候选择优）：假名/罕用扩展汉字混入 = 错误解码迹象"""
    return (0x3040 <= o <= 0x30FF          # 假名（错解码常零星混入汉字间）
            or 0x3400 <= o <= 0x4DBF       # CJK 扩展 A（罕用）
            or o >= 0x20000)               # CJK 扩展 B+（罕用）

def _is_ascii_print(o: int) -> bool:
    return 0x20 <= o <= 0x7E

def _is_control(o: int) -> bool:
    return (o < 0x20 and o not in (0x09, 0x0A, 0x0D)) or o == 0x7F


@dataclass
class _Stats:
    total_nonspace: int = 0
    good_cjk: int = 0        # 汉字 + 韩文（得分奖励、置信度分子）
    ascii_print: int = 0
    mojibake: int = 0        # Latin-1 补充区 = 真正的乱码信号
    penalized: int = 0       # 假名/罕用扩展汉字（择优惩罚，非乱码判据）
    replacement: int = 0
    control: int = 0
    qmark: int = 0


def _stats(s: str) -> _Stats:
    st = _Stats()
    for ch in s:
        o = ord(ch)
        if ch.isspace():
            continue
        st.total_nonspace += 1
        if ch == "�":
            st.replacement += 1
        elif ch in ("?", "？", "¿"):
            st.qmark += 1
            if _is_ascii_print(o):
                st.ascii_print += 1
        elif _is_control(o):
            st.control += 1
        elif _is_good_cjk(o):
            st.good_cjk += 1
        elif _is_ascii_print(o):
            st.ascii_print += 1
        elif _is_mojibake(o):
            st.mojibake += 1
        elif _is_penalized(o):
            st.penalized += 1
    return st


def _score(s: str) -> int:
    """越高越可读：奖励汉字/韩文/ASCII，重罚替换符/控制符，罚乱码信号与假名混入"""
    st = _stats(s)
    return (st.good_cjk * 3 + st.ascii_print
            - st.mojibake * 3 - st.penalized * 2
            - st.replacement * 10 - st.control * 10)


def _cjk_ratio(s: str) -> float:
    st = _stats(s)
    return st.good_cjk / st.total_nonspace if st.total_nonspace else 0.0


def _is_qmark_loss(s: str) -> bool:
    """疑似字符集转换丢失（整体问号化），不可恢复"""
    st = _stats(s)
    return st.qmark >= 2 and st.total_nonspace > 0 and st.qmark / st.total_nonspace > 0.6


def _looks_garbled(s: str) -> bool:
    st = _stats(s)
    if st.total_nonspace == 0:
        return False
    if st.replacement > 0 or st.control > 0:
        return True
    # 大量 Latin-1 补充区字符 = GBK/UTF-8 被错当 Latin-1 解码（典型 mojibake）
    if st.mojibake / st.total_nonspace > 0.30:
        return True
    return False


# ── 修复逆变换（仅 stdlib codecs）────────────────────────────

def _via_latin1_gbk(s: str) -> str:
    return s.encode("latin-1").decode("gb18030")

def _via_latin1_utf8(s: str) -> str:
    return s.encode("latin-1").decode("utf-8")

def _via_cp1252_gbk(s: str) -> str:
    return s.encode("cp1252").decode("gb18030")

REPAIR_TRANSFORMS: list[tuple[str, Callable[[str], str]]] = [
    ("latin1→gb18030", _via_latin1_gbk),
    ("latin1→utf-8", _via_latin1_utf8),
    ("cp1252→gb18030", _via_cp1252_gbk),
]


@dataclass
class RepairResult:
    tier: str
    original: str
    repaired: str
    method: Optional[str] = None
    confidence: float = 0.0
    note: str = ""


def analyze(text: Optional[str]) -> RepairResult:
    """对单条注释做分级与修复建议"""
    if text is None or not str(text).strip():
        return RepairResult(TIER_EMPTY, text or "", "", None, 0.0, "空注释")

    raw = str(text)
    if _is_qmark_loss(raw):
        return RepairResult(TIER_GARBLED, raw, raw, None, 0.0,
                            "疑似字符集转换丢失（问号化），不可恢复")
    if not _looks_garbled(raw):
        return RepairResult(TIER_CLEAN, raw, raw, None, 1.0, "无需处理")

    # 疑似乱码 → 尝试各逆变换，取得分最高者
    best_name, best_text, best_score = None, raw, _score(raw)
    for name, fn in REPAIR_TRANSFORMS:
        try:
            cand = fn(raw)
        except (UnicodeError, LookupError):
            continue
        if not cand or cand == raw:
            continue
        sc = _score(cand)
        if sc > best_score:
            best_name, best_text, best_score = name, cand, sc

    if best_name and _stats(best_text).good_cjk > 0 and not _looks_garbled(best_text):
        return RepairResult(TIER_RECOVERABLE, raw, best_text, best_name,
                            round(_cjk_ratio(best_text), 2),
                            f"经 {best_name} 修复，待人工确认")

    return RepairResult(TIER_GARBLED, raw, raw, None, 0.0,
                        "未找到可信修复方案，需人工/甲方确认")


# ── 输入适配 ──────────────────────────────────────────────────

@dataclass
class CommentItem:
    owner: str
    table: str
    column: Optional[str]     # None 表示表级注释
    kind: str                 # table / column
    text: Optional[str]
    source_hint: str = ""     # CSV 的 SOURCE 列等原始标注（仅供参考）


def iter_from_json(path: str) -> Iterator[CommentItem]:
    """从 db_introspect 产出的元数据 JSON 读取表/字段注释"""
    with open(path, encoding="utf-8") as f:
        meta = json.load(f)
    owner = meta.get("owner", "")
    for t in meta.get("tables", []):
        tname = t.get("name", "")
        yield CommentItem(owner, tname, None, "table", t.get("comment"))
        for c in t.get("columns", []):
            yield CommentItem(owner, tname, c.get("name"), "column", c.get("comment"))


def iter_from_csv(path: str) -> Iterator[CommentItem]:
    """从数据字典 CSV 读取（列：SCHEMA,TABLE_NAME,COLUMN_NAME,DATA_TYPE,LEN,COL_COMMENT,SOURCE）"""
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield CommentItem(
                owner=row.get("SCHEMA", ""),
                table=row.get("TABLE_NAME", ""),
                column=row.get("COLUMN_NAME"),
                kind="column",
                text=row.get("COL_COMMENT"),
                source_hint=row.get("SOURCE", ""),
            )


# ── 处理与输出 ────────────────────────────────────────────────

@dataclass
class ProcessedItem:
    item: CommentItem
    result: RepairResult


def process(items: Iterator[CommentItem], limit: Optional[int] = None) -> list[ProcessedItem]:
    out: list[ProcessedItem] = []
    for i, it in enumerate(items):
        if limit is not None and i >= limit:
            break
        out.append(ProcessedItem(it, analyze(it.text)))
    return out


def tally(processed: list[ProcessedItem]) -> dict[str, int]:
    counts = {TIER_EMPTY: 0, TIER_CLEAN: 0, TIER_RECOVERABLE: 0, TIER_GARBLED: 0}
    for p in processed:
        counts[p.result.tier] = counts.get(p.result.tier, 0) + 1
    counts["total"] = len(processed)
    return counts


def write_cleaned(processed: list[ProcessedItem], path: str) -> None:
    """输出清洗【建议】CSV（不覆盖原始源；REPAIRED 仅为建议）"""
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["OWNER", "TABLE", "COLUMN", "KIND", "TIER",
                    "ORIGINAL", "REPAIRED_SUGGESTION", "METHOD", "CONFIDENCE"])
        for p in processed:
            r, it = p.result, p.item
            w.writerow([it.owner, it.table, it.column or "", it.kind, r.tier,
                        r.original, r.repaired if r.tier == TIER_RECOVERABLE else "",
                        r.method or "", f"{r.confidence:.2f}"])
    log.info("清洗建议已写入：%s", path)


def render_report(processed: list[ProcessedItem]) -> str:
    """生成《注释乱码清单》Markdown（recoverable + garbled）"""
    counts = tally(processed)
    rec = [p for p in processed if p.result.tier == TIER_RECOVERABLE]
    gar = [p for p in processed if p.result.tier == TIER_GARBLED]

    lines = [
        "# 注释乱码清单（编码治理产出）",
        "",
        "> 由 `encoding_normalizer.py` 生成。**修复列为建议，须人工/甲方确认后方可回填**（CLAUDE.md：不静默改源）。",
        "",
        "## 汇总",
        "",
        "| 分级 | 数量 | 说明 |",
        "|------|------|------|",
        f"| clean 可读 | {counts[TIER_CLEAN]} | 无需处理 |",
        f"| recoverable 可修复 | {counts[TIER_RECOVERABLE]} | 已给修复建议，待确认 |",
        f"| garbled 不可恢复 | {counts[TIER_GARBLED]} | 需人工/甲方确认 |",
        f"| empty 空注释 | {counts[TIER_EMPTY]} | 联动「字段注释为空」清单 |",
        f"| **合计** | **{counts['total']}** | |",
        "",
        f"## 一、可修复（{len(rec)}，待确认）",
        "",
        "| 序 | 位置 | 原文 | 修复建议 | 方法 | 置信 |",
        "|----|------|------|---------|------|------|",
    ]
    for i, p in enumerate(rec, 1):
        loc = _loc(p.item)
        lines.append(f"| {i} | {loc} | `{_esc(p.result.original)}` | "
                     f"{_esc(p.result.repaired)} | {p.result.method} | {p.result.confidence:.2f} |")

    lines += ["", f"## 二、不可恢复（{len(gar)}，需人工/甲方确认）", "",
              "| 序 | 位置 | 原文 | 说明 |", "|----|------|------|------|"]
    for i, p in enumerate(gar, 1):
        lines.append(f"| {i} | {_loc(p.item)} | `{_esc(p.result.original)}` | {p.result.note} |")

    lines.append("")
    return "\n".join(lines)


def _loc(it: CommentItem) -> str:
    return f"{it.owner}.{it.table}" + (f".{it.column}" if it.column else "（表级）")

def _esc(s: str) -> str:
    """转义 Markdown 表格中的竖线与换行"""
    return (s or "").replace("|", "\\|").replace("\n", " ⏎ ").replace("\r", "")


def write_report(processed: list[ProcessedItem], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(render_report(processed))
    log.info("注释乱码清单已写入：%s", path)


# ── 自测样例 ──────────────────────────────────────────────────

SELF_TEST_SAMPLES = [
    ("工单主表", TIER_CLEAN),          # 正常中文
    ("inventory order", TIER_CLEAN),   # 正常英文
    ("인장시험", TIER_CLEAN),           # 正常韩文（本 MES 为韩系系统，合法内容）
    ("", TIER_EMPTY),                  # 空
    ("   ", TIER_EMPTY),               # 纯空白
    ("¹¤µ¥", TIER_RECOVERABLE),        # 工单：GBK 被当 Latin-1
    ("å·¥å\x8d\x95", TIER_RECOVERABLE),  # 工单：UTF-8 被当 Latin-1
    ("工�单", TIER_GARBLED),      # 含替换符
    ("????", TIER_GARBLED),            # 问号化丢失
]


def _run_self_test() -> int:
    log.info("自测：内置样例分级")
    failed = 0
    for text, expect in SELF_TEST_SAMPLES:
        r = analyze(text)
        ok = r.tier == expect
        failed += 0 if ok else 1
        flag = "✓" if ok else "✗"
        print(f"  {flag} {text!r:22} -> {r.tier:12} "
              f"{'修复=' + repr(r.repaired) if r.tier == TIER_RECOVERABLE else ''}")
    print(f"自测结果：{len(SELF_TEST_SAMPLES) - failed}/{len(SELF_TEST_SAMPLES)} 通过")
    return failed


# ── CLI ───────────────────────────────────────────────────────

def run(args) -> list[ProcessedItem]:
    if args.self_test:
        raise SystemExit(_run_self_test())

    if args.input_csv:
        if not os.path.exists(args.input_csv):
            raise SystemExit(f"输入 CSV 不存在：{args.input_csv}")
        items = iter_from_csv(args.input_csv)
    elif args.input:
        if not os.path.exists(args.input):
            raise SystemExit(f"输入 JSON 不存在：{args.input}")
        items = iter_from_json(args.input)
    else:
        raise SystemExit("请用 --input（自省 JSON）或 --input-csv（数据字典 CSV）指定输入")

    processed = process(items, limit=args.limit)
    log.info("分级统计：%s", json.dumps(tally(processed), ensure_ascii=False))

    if args.out_cleaned:
        write_cleaned(processed, args.out_cleaned)
    if args.out_report:
        write_report(processed, args.out_report)
    return processed


def main(argv=None):
    p = argparse.ArgumentParser(description="注释编码治理器（乱码修复 + 质量分级）")
    p.add_argument("--input", help="db_introspect 产出的元数据 JSON")
    p.add_argument("--input-csv", dest="input_csv", help="数据字典 CSV（data_dictionary_full.csv）")
    p.add_argument("--out-cleaned", dest="out_cleaned", help="清洗建议 CSV 输出路径")
    p.add_argument("--out-report", dest="out_report", help="《注释乱码清单》Markdown 输出路径")
    p.add_argument("--limit", type=int, default=None, help="仅处理前 N 条（低配机预览用）")
    p.add_argument("--self-test", action="store_true", help="运行内置样例自测，不读文件")
    run(p.parse_args(argv))


if __name__ == "__main__":
    main()
