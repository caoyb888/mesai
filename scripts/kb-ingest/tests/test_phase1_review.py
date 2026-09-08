"""
T3-4-4 Phase-1 评审会材料纯逻辑单元测试（无 DB / 无外部 AI）

覆盖：议程时长合计、DoD 项与三态汇总（3 已达/3 待评分）、材料组装
     （议程/交付一览/DoD/三准确率核验/决议/签字区/材料索引/数字复用）。

关联需求单：REQ-MES-AI-20260715-001（T3-4-4）
作者：AI（芯智云匠）  日期：2026-07-16
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from build_phase1_review import (
    AGENDA, agenda_total_minutes, dod_items, dod_summary, build_review,
)
from build_system_report import DEFAULTS


def _stats(**over):
    s = dict(DEFAULTS)
    s.update(over)
    return s


# ── 议程 ─────────────────────────────────────────────────────
def test_agenda_total_minutes():
    assert agenda_total_minutes() == sum(m for _, _, m in AGENDA)
    assert agenda_total_minutes() == 80


def test_agenda_has_signoff_and_accuracy_topics():
    topics = " ".join(t for t, _, _ in AGENDA)
    assert "签字" in topics and "准确率" in topics and "脱敏" in topics


# ── DoD ──────────────────────────────────────────────────────
def test_dod_items_six_and_three_states():
    items = dod_items(_stats())
    assert len(items) == 6
    done, pending = dod_summary(items)
    assert done == 3 and pending == 3          # RAG/断言/脱敏 已达；三准确率 待评分


def test_dod_reflects_stats():
    items = dod_items(_stats(sql_auto=69.9, sql_qs=30, q_count=21, g_hit=26, g_total=26,
                             assert_total=657, rag_chunks=5155))
    joined = " | ".join(str(x) for it in items for x in it)
    assert "69.9" in joined and "30" in joined
    assert "657" in joined and "5,155" in joined
    assert "26/26" in joined


# ── 组装 ─────────────────────────────────────────────────────
def test_build_review_sections():
    s = _stats(mes_tables=1860, s3_1_cards=95, s3_2_cards=1308, s3_2_total=1309,
               state_fields=34, trace_edges=13, carrier_keys=14, core_groups=12,
               q_count=21, g_hit=26, g_total=26, assert_total=657, glossary_terms=9698,
               rag_chunks=5155)
    md = build_review(s)
    for sec in ("会议议程", "Phase-1 交付一览", "DoD 达标逐项核对",
                "三项准确率核验", "脱敏合规", "遗留事项", "评审决议",
                "评审签字区", "评审材料索引"):
        assert sec in md, f"缺章节 {sec}"


def test_build_review_decision_options_and_conditional():
    md = build_review(_stats())
    assert "☐ **通过**" in md and "☐ **有条件通过**" in md and "☐ **驳回**" in md
    assert "AI 侧交付 100% 就绪" in md


def test_build_review_numbers_and_signoff_roles():
    md = build_review(_stats(mes_tables=1860, assert_total=657, rag_chunks=5155,
                             q_count=21, g_hit=26, g_total=26))
    assert "1,860" in md and "657" in md and "5,155" in md
    for role in ("甲方 IT 负责人", "TL 技术负责人", "BIZ 业务专家", "ITM IT 审核专员"):
        assert role in md
    assert "接地校验 ≠ 业务正确性" in md


def test_build_review_material_index_links():
    md = build_review(_stats())
    for path in ("docs/MES真实系统理解总报告.md", "docs/S3-3_业务流程验证题.md",
                 "assertions/manifest.md", "docs/S3-4-3_Token复盘与P1P2排期.md"):
        assert path in md
