"""
T3-4-3 Token 复盘与 P1/P2 排期纯逻辑单元测试（无 DB / 无外部 AI）

覆盖：台账合计、按日聚合、单位成本、层跨度/投影（含变体去重）、预算日、
     阈值跨越判定、报告组装关键内容。

关联需求单：REQ-MES-AI-20260715-001（T3-4-3）
作者：AI（芯智云匠）  日期：2026-07-16
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from build_token_p1p2_plan import (
    LEDGER, BUDGET, P0, TIERS, VARIANT_DEDUP,
    total_tokens, by_date, unit_cost, tier_span, project_tier,
    budget_days, crossed_thresholds, build_report,
)


# ── 台账 ─────────────────────────────────────────────────────
def test_total_tokens_matches_ledger_sum():
    assert total_tokens() == sum(r["tokens"] for r in LEDGER)
    # 已知合计 ~3.99M
    assert 3_900_000 < total_tokens() < 4_050_000


def test_by_date_two_days_and_0715_dominant():
    d = by_date()
    assert set(d) == {"2026-07-15", "2026-07-16"}
    assert d["2026-07-15"] > d["2026-07-16"]
    assert d["2026-07-15"] == sum(r["tokens"] for r in LEDGER if r["date"] == "2026-07-15")


def test_deterministic_tasks_zero_tokens():
    zero = [r for r in LEDGER if r["tokens"] == 0]
    assert any("验证题库" in r["task"] for r in zero)
    assert any("总报告" in r["task"] for r in zero)


# ── 单位成本 ──────────────────────────────────────────────────
def test_unit_cost_table_and_subprog():
    ct = unit_cost(P0["table_tokens"], P0["table_n"])
    cs = unit_cost(P0["subprog_tokens"], P0["subprog_n"])
    assert 5000 < ct < 6000       # ~5.6K/表
    assert 2000 < cs < 3000       # ~2.5K/子程序
    assert unit_cost(100, 0) == 0.0


# ── 分层投影 ──────────────────────────────────────────────────
def test_tier_span_inclusive():
    assert tier_span(101, 400) == 300
    assert tier_span(61, 200) == 140
    assert tier_span(5, 5) == 1
    assert tier_span(10, 1) == 0


def test_project_tier_p1_math():
    ct, cs = 5600.0, 2500.0
    p = project_tier(TIERS["P1"], ct, cs)
    assert p["n_tables"] == 300 and p["n_units"] == 140
    raw = 140 * TIERS["P1"]["subprog_per_unit"]
    assert p["n_subprog"] == round(raw * (1 - VARIANT_DEDUP))
    assert p["tok_tables"] == round(300 * ct)
    assert p["tok_subprog"] == round(p["n_subprog"] * cs)
    assert p["tok_total"] == p["tok_tables"] + p["tok_subprog"]


def test_project_tier_p2_larger_than_p1():
    ct, cs = 5600.0, 2500.0
    p1 = project_tier(TIERS["P1"], ct, cs)
    p2 = project_tier(TIERS["P2"], ct, cs)
    assert p2["n_tables"] > p1["n_tables"]     # 长尾更大
    assert p2["tok_total"] > p1["tok_total"]


# ── 预算 ─────────────────────────────────────────────────────
def test_budget_days_scales_with_gate():
    tok = 5_600_000
    d_default = budget_days(tok, BUDGET["daily_default"])
    d_gate = budget_days(tok, BUDGET["temp_gate"])
    assert d_default > d_gate                   # 大闸更少天
    assert d_gate <= 1.0                        # 8M 闸内一日可完成 5.6M
    assert budget_days(0) == 0.0


def test_crossed_thresholds():
    assert crossed_thresholds(3_900_000) == ["降级(250万)", "暂停(300万)"]
    assert crossed_thresholds(2_600_000) == ["降级(250万)"]
    assert crossed_thresholds(50_000) == []


# ── 报告 ─────────────────────────────────────────────────────
def test_build_report_has_both_parts_and_numbers():
    md = build_report()
    assert "Token 消耗复盘" in md and "预算与降级复盘" in md
    assert "P1/P2 资产分层与训练排期" in md
    assert "TL 授权临时 8M 闸" in md
    assert "P0（已训）" in md and "P1（次核心" in md and "P2（长尾" in md
    # 07-15 超预算标注
    assert "降级(250万)" in md and "暂停(300万)" in md


def test_build_report_p2_on_demand_strategy():
    md = build_report()
    assert "按需增量" in md and "RAG 兜底" in md
    assert "不主动全训" in md
