"""
T3-3-4 验证题库纯逻辑单元测试（无 DB / 无外部 AI）

覆盖：题库规模与四类齐全、类别/难度统计、题库渲染（评分模板/证据/分类分组）、
     接地校验（state/carrier_pair/table/package 命中与跳过）、接地报告。

关联需求单：REQ-MES-AI-20260715-001（T3-3-4）
作者：AI（芯智云匠）  日期：2026-07-15
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from build_validation_questions import (
    QUESTIONS, CATS, category_stats, render_bank, scoring_note,
    verify_one, verify_all, render_grounding_report,
)


# ── 题库结构 ──────────────────────────────────────────────────
def test_question_bank_min_15_and_four_categories():
    assert len(QUESTIONS) >= 15
    cats = {q["cat"] for q in QUESTIONS}
    assert cats == set(CATS)               # 四类齐全
    for c in CATS:                          # 每类至少 3 题
        assert sum(1 for q in QUESTIONS if q["cat"] == c) >= 3


def test_every_question_has_required_fields():
    for q in QUESTIONS:
        for f in ("cat", "diff", "scenario", "q", "ref", "evi", "grounding"):
            assert f in q and q[f] != "", f"缺字段 {f}: {q.get('scenario')}"
        assert q["diff"] in ("中", "难")
        assert isinstance(q["evi"], list) and q["evi"]


def test_category_stats():
    cat_c, diff_c = category_stats(QUESTIONS)
    assert sum(cat_c.values()) == len(QUESTIONS)
    assert sum(diff_c.values()) == len(QUESTIONS)


# ── 渲染 ──────────────────────────────────────────────────────
def test_render_bank_has_scoring_and_all_questions():
    md = render_bank(QUESTIONS)
    assert "评分汇总" in md and "准确率" in md
    assert "≥90%" in md
    # 每题编号连续出现
    for i in range(1, len(QUESTIONS) + 1):
        assert f"Q{i}．" in md
    # 四类标题都在
    for c in CATS:
        assert f"## {c}" in md


def test_render_bank_grouped_and_biz_marks():
    md = render_bank(QUESTIONS)
    assert md.count("☐ 正确") == len(QUESTIONS)   # 每题一个评分栏
    assert "BIZ 批注" in md


def test_scoring_note_formula():
    assert "0.5" in scoring_note() and "准确率" in scoring_note()


# ── 接地校验 ──────────────────────────────────────────────────
def test_verify_one_state_hit_and_miss():
    sw = {("SMS_HEAT", "HEAT_STS", "2")}
    ok, _ = verify_one({"type": "state", "table": "SMS_HEAT", "column": "HEAT_STS", "value": "2"},
                       sw, None, None, None)
    assert ok is True
    miss, _ = verify_one({"type": "state", "table": "SMS_HEAT", "column": "HEAT_STS", "value": "9"},
                         sw, None, None, None)
    assert miss is False


def test_verify_one_carrier_pair():
    col2tabs = {"HEAT_NO": {"SMS_HEAT", "SMS_SLAB"}, "SLAB_NO": {"SMS_SLAB"}}
    ok, desc = verify_one({"type": "carrier_pair", "a": "HEAT_NO", "b": "SLAB_NO"},
                          None, None, col2tabs, None)
    assert ok is True and "SMS_SLAB" not in desc  # desc 只报数量
    miss, _ = verify_one({"type": "carrier_pair", "a": "HEAT_NO", "b": "COIL_NO"},
                         None, None, col2tabs, None)
    assert miss is False


def test_verify_one_table_and_package():
    ok_t, _ = verify_one({"type": "table", "name": "SMS_HEAT"}, None, {"SMS_HEAT"}, None, None)
    ok_p, _ = verify_one({"type": "package", "name": "BSQM_MTC_ISSUE"}, None, None, None, {"BSQM_MTC_ISSUE"})
    assert ok_t is True and ok_p is True


def test_verify_one_skip_when_source_missing():
    ok, desc = verify_one({"type": "state", "table": "T", "column": "C", "value": "1"},
                          None, None, None, None)
    assert ok is None and "SKIP" in desc


def test_verify_all_counts_and_report():
    # 提供全部数据源，令题库所有接地断言尽量命中
    sw, tables, col2tabs, packages = set(), set(), {}, set()
    # 收集题库需要的断言并全部塞入数据源 → 全命中
    for q in QUESTIONS:
        for gr in q["grounding"]:
            if gr["type"] == "state":
                sw.add((gr["table"], gr["column"], gr["value"]))
            elif gr["type"] == "carrier_pair":
                col2tabs.setdefault(gr["a"], set()).add("BRIDGE_T")
                col2tabs.setdefault(gr["b"], set()).add("BRIDGE_T")
            elif gr["type"] == "table":
                tables.add(gr["name"])
            elif gr["type"] == "package":
                packages.add(gr["name"])
    rows, n_ok, n_fail, n_skip = verify_all(QUESTIONS, sw, tables, col2tabs, packages)
    assert n_fail == 0 and n_skip == 0 and n_ok == len(rows)
    rep = render_grounding_report(rows, n_ok, n_fail, n_skip)
    assert "接地无悬空" in rep


def test_verify_all_reports_miss():
    rows, n_ok, n_fail, n_skip = verify_all(
        [{"cat": "状态流转", "grounding": [
            {"type": "state", "table": "T", "column": "C", "value": "X"}]}],
        set(), set(), {}, set())
    assert n_fail == 1
    rep = render_grounding_report(rows, n_ok, n_fail, n_skip)
    assert "⚠️" in rep and "未命中" in rep
