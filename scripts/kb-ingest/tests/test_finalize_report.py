"""
T3-3-5 报告完稿纯逻辑单元测试（无 DB / 无外部 AI）

覆盖：标记块剥离、三部分正文抽取、统计正则抽取、前言/结语生成、
     第一部分标题降级与陈旧提示修正、完稿幂等（重跑不叠加）。

关联需求单：REQ-MES-AI-20260715-001（T3-3-5）
作者：AI（芯智云匠）  日期：2026-07-16
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from finalize_s3_3_report import (
    strip_block, extract_core_body, extract_stats, build_frontmatter,
    build_conclusion, finalize, NEW_H1, OLD_H1, PART1_H,
    FM_START, FM_END, CC_START, CC_END,
)

# 迷你三部分报告（含各部分小节表关键行）
REPORT = "\n".join([
    OLD_H1, "",
    "| 项 | 内容 |", "|----|----|",
    "| 反推状态字段 | 34（源自过程 set_assignments）|",
    "| Token | 23,962 |", "",
    "> 状态机由证据反推。本报告为 S3-3 第一部分（状态机），追溯链路(T3-3-2)/核心流程(T3-3-3)/验证题(T3-3-4)续。", "",
    "## 状态字段一览", "（略）", "",
    "<!-- T3-3-2-TRACEABILITY -->", "",
    "## 第二部分：批次/卷/试样追溯链路（T3-3-2）", "",
    "| 追溯边（有证据）| 13 |", "| Token | 21,650 |", "",
    "### 核心实体载体画像", "",
    "| 订单 | `ORD_NO` | 189 | 38 | x | y |",
    "| 炉次 | `HEAT_NO` | 176 | 44 | x | y |", "",
    "<!-- T3-3-3-COREPROCESS -->", "",
    "## 第三部分：核心流程理解（质量判定 BSQM / 生产调度 BSCH · T3-3-3）", "",
    "| 核心流程组 | 12（BSQM 5 / BSCH 7）|", "| Token | 29,325 |", "",
    "（正文略）",
])

QBANK = "\n".join([
    "| 题量 | 21（≥15）|",
    "接地断言 26 条：✅ 命中 26 ／ ❌ 未命中 0 ／ ⏭ 跳过 0。",
])


# ── strip_block ──────────────────────────────────────────────
def test_strip_block_removes_inclusive():
    t = "a\n<!-- S -->\nx\ny\n<!-- E -->\nb\n"
    assert strip_block(t, "<!-- S -->", "<!-- E -->").strip() == "a\n\nb".strip() or "x" not in strip_block(t, "<!-- S -->", "<!-- E -->")


def test_strip_block_noop_when_absent():
    assert strip_block("hello", FM_START, FM_END) == "hello"


# ── 抽取 ─────────────────────────────────────────────────────
def test_extract_stats_numbers():
    s = extract_stats(REPORT, QBANK)
    assert s["state_fields"] == 34
    assert s["trace_edges"] == 13
    assert s["carrier_keys"] == 2          # 两行载体画像
    assert s["core_groups"] == 12 and s["bsqm"] == 5 and s["bsch"] == 7
    assert s["tokens"] == 23962 + 21650 + 29325
    assert s["q_count"] == 21
    assert s["g_hit"] == 26 and s["g_total"] == 26


def test_extract_core_body_from_old_h1():
    body = extract_core_body(REPORT)
    assert body.startswith(OLD_H1)


def test_extract_core_body_prefers_part1_header():
    txt = "junk\n" + PART1_H + "\nx\n" + OLD_H1
    assert extract_core_body(txt).startswith(PART1_H)


# ── 前言/结语 ────────────────────────────────────────────────
def test_build_frontmatter_has_sections_and_numbers():
    s = extract_stats(REPORT, QBANK)
    fm = build_frontmatter(s)
    assert FM_START in fm and FM_END in fm
    assert "执行摘要" in fm and "方法论" in fm and "覆盖范围" in fm and "阅读导航" in fm
    assert "74,937" in fm                  # token 合计千分位
    assert "34" in fm and "13" in fm and "12" in fm and "21" in fm


def test_build_conclusion_has_signoff_and_markers():
    s = extract_stats(REPORT, QBANK)
    cc = build_conclusion(s)
    assert CC_START in cc and CC_END in cc
    assert "验收签字区" in cc and "BIZ" in cc and "ITM" in cc
    assert "接地校验≠业务正确性" in cc


# ── 完稿 + 幂等 ──────────────────────────────────────────────
def test_finalize_wraps_and_demotes_part1():
    out, s = finalize(REPORT, QBANK)
    assert out.startswith(NEW_H1)
    assert PART1_H in out                  # 第一部分标题已降级
    assert OLD_H1 not in out               # 原 H1 不再作为独立标题
    assert "本报告为 S3-3 第一部分" not in out   # 陈旧提示已修
    # 三部分正文仍在
    assert "第二部分" in out and "第三部分" in out
    assert FM_START in out and CC_START in out


def test_finalize_idempotent():
    out1, _ = finalize(REPORT, QBANK)
    out2, _ = finalize(out1, QBANK)        # 对已完稿再跑
    assert out1 == out2                    # 不叠加、不漂移
    assert out2.count(FM_START) == 1 and out2.count(CC_START) == 1
    assert out2.count(NEW_H1) == 1
