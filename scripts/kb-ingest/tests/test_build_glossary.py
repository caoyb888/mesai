"""
中韩英术语对照表构建器单元测试（纯本地，不连库）

覆盖：语种判定（韩/中/英/无）、CD_NM+CD_DESC 落槽、行级映射、
     术语级去重与合并、覆盖统计、离线 CSV 输入模式。

关联任务：S3-0 T3-0-5 中韩英术语对照表（AI-MES-S3PLAN-2026-001）
关联需求单：REQ-MES-AI-20260706-001
作者：AI（芯智云匠）
日期：2026-07-14
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from build_glossary import (
    classify_lang,
    slot_row,
    build_entries,
    dedup_terms,
    coverage_stats,
)


# ---------------------------------------------------------------------------
# 语种判定
# ---------------------------------------------------------------------------
def test_classify_korean():
    # 谚文音节应判为韩文
    assert classify_lang("열연고철") == "ko"
    assert classify_lang("1/2경질") == "ko"  # 混数字仍以谚文优先


def test_classify_chinese():
    assert classify_lang("热轧废钢") == "zh"
    assert classify_lang("1#加热炉") == "zh"  # 混数字/符号仍以汉字优先


def test_classify_english():
    assert classify_lang("Pellet") == "en"
    assert classify_lang("ROLLED CHARTERING") == "en"


def test_classify_none_for_symbols_or_empty():
    assert classify_lang("") is None
    assert classify_lang(None) is None
    assert classify_lang("235959") is None  # 纯数字无法归语种
    assert classify_lang("--//") is None


def test_classify_priority_korean_over_han():
    # 韩文优先级高于汉字（韩文汉字混排时归韩）
    assert classify_lang("열연고철A2") == "ko"


# ---------------------------------------------------------------------------
# 落槽：CD_NM / CD_DESC → zh/ko/en
# ---------------------------------------------------------------------------
def test_slot_zh_ko_pair():
    s = slot_row("热轧废钢", "열연고철")
    assert s == {"zh": "热轧废钢", "ko": "열연고철", "en": ""}


def test_slot_zh_en_pair():
    s = slot_row("球团", "Pellet")
    assert s["zh"] == "球团" and s["en"] == "Pellet" and s["ko"] == ""


def test_slot_english_only_group():
    # CD_NM 英文、CD_DESC 空 → 仅英文槽
    s = slot_row("BENT", None)
    assert s == {"zh": "", "ko": "", "en": "BENT"}


def test_slot_first_wins_same_lang():
    # 两列同语种时以先出现的 CD_NM 为准，不覆盖
    s = slot_row("加热炉", "转炉")
    assert s["zh"] == "加热炉"


def test_slot_strips_whitespace():
    s = slot_row("  球团  ", None)
    assert s["zh"] == "球团"


# ---------------------------------------------------------------------------
# 行级映射与术语去重
# ---------------------------------------------------------------------------
_ROWS = [
    ("ITEM_SPEC", "G9B14", "热轧废钢", "열연고철", "Y"),
    ("PLAN_DETAIL", "G1A001", "球团", "Pellet", "Y"),
    ("ROLL_RSN", "A2", "BENT", None, "Y"),
    ("DUP", "X1", "热轧废钢", "열연고철", "Y"),   # 与第一条同术语 → 去重合并
    ("PURE_NUM", "N1", "235959", None, "Y"),       # 三语皆空 → 去重时剔除
]


def test_build_entries_shape():
    entries = build_entries(_ROWS)
    assert len(entries) == 5
    first = entries[0]
    assert first["master_cd"] == "ITEM_SPEC"
    assert first["zh"] == "热轧废钢" and first["ko"] == "열연고철"


def test_dedup_merges_same_term_and_drops_empty():
    entries = build_entries(_ROWS)
    terms = dedup_terms(entries)
    # 5 行：热轧废钢重复 1 次合并 + 纯数字剔除 → 3 个去重术语
    assert len(terms) == 3
    steel = [t for t in terms if t["zh"] == "热轧废钢"][0]
    assert steel["count"] == 2
    assert steel["ko"] == "열연고철"
    assert len(steel["groups"]) == 2  # ITEM_SPEC + DUP


def test_coverage_stats():
    entries = build_entries(_ROWS)
    terms = dedup_terms(entries)
    st = coverage_stats(terms)
    assert st["total"] == 3
    assert st["has_zh"] == 2       # 热轧废钢、球团
    assert st["has_ko"] == 1       # 열연고철
    assert st["has_en"] == 2       # Pellet、BENT
    assert st["all_three"] == 0    # 源表两列上限，三语不可能齐全
    assert st["need_en"] == 1      # 热轧废钢缺英
    assert st["need_zh"] == 1      # BENT 缺中


# ---------------------------------------------------------------------------
# 离线 CSV 输入模式（--from-csv 路径依赖的列名解析）
# ---------------------------------------------------------------------------
def test_from_csv_column_mapping(tmp_path):
    import csv as _csv
    p = tmp_path / "detail.csv"
    with open(p, "w", newline="", encoding="utf-8-sig") as f:
        w = _csv.writer(f)
        w.writerow(["MASTER_CD", "CD_VAL", "CD_NM", "CD_DESC", "USE_YN"])
        w.writerow(["ITEM_SPEC", "G9B14", "热轧废钢", "열연고철", "Y"])
    rows = []
    with open(p, encoding="utf-8-sig") as f:
        for r in _csv.DictReader(f):
            rows.append((r["MASTER_CD"], r["CD_VAL"], r["CD_NM"], r["CD_DESC"], r["USE_YN"]))
    terms = dedup_terms(build_entries(rows))
    assert terms[0]["zh"] == "热轧废钢" and terms[0]["ko"] == "열연고철"
