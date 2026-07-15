"""
T3-4-1 系统理解总报告纯逻辑单元测试（无 DB / 无外部 AI）

覆盖：各子报告数字抽取（含缺失回退默认）、S3-3 复用抽取、断言/术语抽取、
     报告组装（三态/DoD/签字区/派生百分比）。

关联需求单：REQ-MES-AI-20260715-001（T3-4-1）
作者：AI（芯智云匠）  日期：2026-07-16
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from build_system_report import extract_stats, build_report, DEFAULTS


CENSUS = "\n".join([
    "| Schema | 表 | 字段 | 视图 | 程序单元 | 行数 |",
    "| **MESAPUSER**（业务） | 1,860 | 78,526 | 154 | **9,160** | **1,932,301** |",
    "| PACKAGE（包规格） | **4,563** | 40 |",
    "| PACKAGE BODY（包体） | **4,421** | 34 |",
])
S3_1 = "| 题量 | 30（6 模块×5）|\n| 自动初评均分 | 69.9/100 |"
S3_2 = "| **理解卡片产出** | **1308 / 1309（99.9%）** |\n| Token 消耗 | 3,289,621 |"
S3_3 = "\n".join([
    "| 反推状态字段 | 34 |", "| Token | 23,962 |",
    "| 追溯边（有证据）| 13 |", "| Token | 21,650 |",
    "### 核心实体载体画像",
    "| 订单 | `ORD_NO` | 189 | 38 | x | y |",
    "| 炉次 | `HEAT_NO` | 176 | 44 | x | y |",
    "### 追溯边一览",
    "| 核心流程组 | 12（BSQM 5 / BSCH 7）|", "| Token | 29,325 |",
])
QBANK = "| 题量 | 21 |\n接地断言 26 条：✅ 命中 26 ／ ❌ 未命中 0"
ASSERT = ("- **总计 657 条**：state-machine 260 / sql-logic 337 / api-behavior 60\n"
          "- 级别分布：{'Critical': 89, 'High': 171, 'Medium': 397}\n"
          "- 覆盖资产（含表+包）：149；断言数 <3 的资产：97")
GLOSS = "| 去重术语总数 | 9698 |\n| 中韩齐全 | 574 (5%) |"

SRC = {"census": CENSUS, "s3_1": S3_1, "s3_2": S3_2, "s3_3": S3_3,
       "qbank": QBANK, "assertions": ASSERT, "glossary": GLOSS}


# ── 抽取 ─────────────────────────────────────────────────────
def test_extract_census():
    s = extract_stats(SRC)
    assert s["mes_tables"] == 1860 and s["mes_fields"] == 78526
    assert s["mes_units"] == 9160 and s["mes_lines"] == 1932301
    assert s["pkg_spec"] == 4563 and s["pkg_body"] == 4421


def test_extract_s3_1_2():
    s = extract_stats(SRC)
    assert s["sql_qs"] == 30 and s["sql_auto"] == 69.9
    assert s["s3_2_cards"] == 1308 and s["s3_2_total"] == 1309
    assert s["s3_2_tokens"] == 3289621


def test_extract_s3_3_reuse():
    s = extract_stats(SRC)
    assert s["state_fields"] == 34 and s["trace_edges"] == 13
    assert s["carrier_keys"] == 2 and s["core_groups"] == 12
    assert s["bsqm"] == 5 and s["bsch"] == 7
    assert s["s3_3_tokens"] == 23962 + 21650 + 29325
    assert s["q_count"] == 21 and s["g_hit"] == 26 and s["g_total"] == 26


def test_extract_assertions_and_glossary():
    s = extract_stats(SRC)
    assert s["assert_total"] == 657
    assert s["assert_sm"] == 260 and s["assert_sql"] == 337 and s["assert_api"] == 60
    assert s["assert_critical"] == 89 and s["assert_high"] == 171 and s["assert_medium"] == 397
    assert s["assert_cover"] == 149
    assert s["glossary_terms"] == 9698 and s["glossary_zh_ko"] == 574


def test_extract_falls_back_to_defaults_when_empty():
    s = extract_stats({})
    assert s == DEFAULTS                       # 全缺 → 全默认，不报错


def test_extract_partial_keeps_defaults_for_missing():
    s = extract_stats({"glossary": GLOSS})     # 只给术语
    assert s["glossary_terms"] == 9698
    assert s["mes_tables"] == DEFAULTS["mes_tables"]   # 其余保持默认


# ── 组装 ─────────────────────────────────────────────────────
def test_build_report_sections_and_three_states():
    s = extract_stats(SRC)
    md = build_report(s)
    for sec in ("执行摘要", "系统概览", "P0 资产选取与训练方法", "理解成果",
                "知识资产与工程能力", "三项准确率与验收关联", "局限与风险",
                "后续排期", "结论与里程碑判定", "签字区"):
        assert sec in md, f"缺章节 {sec}"
    assert "待 TL/BIZ 人工终评" in md and "待 BIZ 评分" in md   # 待人工三态
    assert "接地校验≠业务正确性" in md


def test_build_report_numbers_rendered():
    s = extract_stats(SRC)
    md = build_report(s)
    assert "1,860" in md and "9,160" in md          # 千分位
    assert "657" in md and "9,698" in md
    assert "34" in md and "13" in md and "21" in md


def test_build_report_derived_percentage():
    s = extract_stats(SRC)
    md = build_report(s)
    # s3_2 卡片率 1308/1309=99.9%
    assert "99.9%" in md
