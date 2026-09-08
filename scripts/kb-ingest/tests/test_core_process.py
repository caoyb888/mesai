"""
T3-3-3 核心流程纯逻辑单元测试（无 DB / 无外部 AI）

覆盖：表名归一（去 owner）、CJK 注释抽取与去码噪、调用分类（内部/外部 BS* 优先）、
     包聚合（读写/状态/调用/子程序/注释）、变体差异、报告段幂等标记。

关联需求单：REQ-MES-AI-20260715-001（T3-3-3）
作者：AI（芯智云匠）  日期：2026-07-15
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from run_s3_core_process import (
    norm_table, extract_comments, classify_calls, analyze_package,
    variant_delta, render_report_section, build_user_prompt,
    SECTION_MARKER, FAMILY,
)


# ── 表名归一 ──────────────────────────────────────────────────
def test_norm_table_strips_owner():
    assert norm_table("MESAPUSER.SCH_PLAN_HEAT") == "SCH_PLAN_HEAT"
    assert norm_table("SCH_PLAN_HEAT") == "SCH_PLAN_HEAT"


# ── 注释抽取 ──────────────────────────────────────────────────
def test_extract_comments_keeps_cjk_line_comment():
    src = "SELECT 1 FROM DUAL; -- 生成质保书时向WSP传数据\nX := 2;"
    cs = extract_comments(src)
    assert any("生成质保书" in c for c in cs)


def test_extract_comments_drops_code_noise_and_short():
    # 含 || 视为代码噪声；CJK 少于3字丢弃
    src = ("-- J.DB_GRADE||','||J.DB_INFO AS 结果,--注释\n"
           "-- 好\n"
           "-- PL.PR_ADD_LOG('BSQM_MTC_ISSUE.X','I', 传参数据入库记录\n")
    cs = extract_comments(src)
    assert all("||" not in c for c in cs)
    assert all("PR_ADD_LOG" not in c.upper() for c in cs)
    assert "好" not in cs                      # 仅1个CJK字，丢弃


def test_extract_comments_block_and_dedup_and_cap():
    src = "/* 浇次拆分处理逻辑说明 */\n-- 浇次拆分处理逻辑说明\n" + \
          "".join(f"-- 第{i}条不同的中文注释行说明\n" for i in range(30))
    cs = extract_comments(src, cap=10)
    assert len(cs) <= 10
    assert cs.count("浇次拆分处理逻辑说明") == 1   # 块注释与行注释去重


# ── 调用分类 ──────────────────────────────────────────────────
def test_classify_calls_internal_vs_external():
    calls = ["PR_MTC_FORM2", "BSQM_MTC_WSP.P_SEND_MTC_CHEM", "PL.PR_ADD_LOG"]
    internal, external = classify_calls(calls, own_names=["PR_MTC_FORM2", "BSQM_MTC_ISSUE"])
    assert internal == ["PR_MTC_FORM2"]
    assert "BSQM_MTC_WSP.P_SEND_MTC_CHEM" in external and "PL.PR_ADD_LOG" in external


def test_classify_calls_business_pkg_ranked_first():
    calls = ["ZZ.util", "PL.log", "BSCH_PROD_INST.PR_TC_FUR_PDI"]
    _, external = classify_calls(calls, own_names=[])
    assert external[0] == "BSCH_PROD_INST.PR_TC_FUR_PDI"   # BS* 业务包排前


# ── 包聚合 ────────────────────────────────────────────────────
def _pkg():
    return {
        "package": "BSQM_MTC_ISSUE", "total_lines": 100, "unit_count": 2,
        # 驱动子程序 PR_MTC_MAIN 调用兄弟子程序 PR_MTC_FORM2（跨子程序=内部调用）
        "units": [
            {"name": "PR_MTC_MAIN", "kind": "PROCEDURE", "line_count": 10,
             "source": ("PROCEDURE PR_MTC_MAIN IS BEGIN\n"
                        "  -- 质保书主流程说明入口\n"
                        "  PR_MTC_FORM2();\nEND;")},
            {"name": "PR_MTC_FORM2", "kind": "PROCEDURE", "line_count": 90,
             "source": ("PROCEDURE PR_MTC_FORM2 IS BEGIN\n"
                        "  -- 生成质保书请求写入状态\n"
                        "  UPDATE SQM_MTC_REQ SET MTC_STS_CD = '2' WHERE X=1;\n"
                        "  INSERT INTO MESAPUSER.SQM_WSP_MTC_CHEM_INF VALUES(1);\n"
                        "  SELECT A FROM SQM_MTC_REQ;\n"
                        "  BSQM_MTC_WSP.P_SEND_MTC_CHEM(1);\nEND;")},
        ],
    }


def test_analyze_package_aggregates_flow():
    agg = analyze_package(_pkg())
    assert "SQM_MTC_REQ" in agg["reads"]
    # 写表去 owner 前缀归一
    assert "SQM_WSP_MTC_CHEM_INF" in agg["writes"]
    assert "SQM_MTC_REQ" in agg["writes"]
    assert "SQM_MTC_REQ.MTC_STS_CD=2" in agg["states"]
    assert "PR_MTC_FORM2" in agg["internal_calls"]
    assert "BSQM_MTC_WSP.P_SEND_MTC_CHEM" in agg["external_calls"]
    assert any("质保书" in c for c in agg["comments"])
    assert agg["unit_count"] == 2 and agg["total_lines"] == 100


def test_analyze_package_dedups_comments():
    pkg = {"package": "P", "total_lines": 5, "unit_count": 1,
           "units": [{"name": "P", "kind": "PREAMBLE", "line_count": 5,
                      "source": "-- 相同的中文注释内容\n-- 相同的中文注释内容\n"}]}
    agg = analyze_package(pkg)
    assert agg["comments"].count("相同的中文注释内容") == 1


# ── 变体差异 ──────────────────────────────────────────────────
def test_variant_delta_extra_writes():
    primary = {"writes": ["SQM_MTC_REQ"], "unit_count": 2, "total_lines": 100}
    var = {"writes": ["SQM_MTC_REQ", "SQM_SHIP_EXTRA"], "unit_count": 3, "total_lines": 120}
    d = variant_delta(primary, var)
    assert d["extra_writes"] == ["SQM_SHIP_EXTRA"]
    assert d["unit_count"] == 3 and d["total_lines"] == 120


# ── prompt / 报告段 ───────────────────────────────────────────
def test_build_user_prompt_includes_evidence():
    agg = analyze_package(_pkg())
    variants = [("BSQM_MTC_ISSUE_SHIP", variant_delta(agg, {"writes": ["EXTRA_T"],
                 "unit_count": 1, "total_lines": 50}))]
    p = build_user_prompt("质保书签发", "BSQM_MTC_ISSUE", "BSQM", agg, variants)
    assert "质保书签发" in p and "BSQM_MTC_ISSUE" in p
    assert "SQM_MTC_REQ.MTC_STS_CD=2" in p
    assert "BSQM_MTC_ISSUE_SHIP" in p            # 变体列出
    assert "EXTRA_T" in p                        # 变体独有写表


def test_render_report_section_marker_and_overview():
    groups = [{"zh": "质保书签发", "pkg": "BSQM_MTC_ISSUE", "fam": "BSQM", "units": 13,
               "lines": 7477, "n_reads": 12, "n_writes": 7, "answer": "流程用途：签发质保书。",
               "writes": ["SQM_MTC_REQ"]}]
    md = render_report_section(groups, {"BSQM": "质量判定总览内容"}, 9999)
    assert SECTION_MARKER in md
    assert "核心流程理解" in md
    assert "质量判定总览内容" in md
    assert "9,999" in md
    assert FAMILY["BSQM"] in md


def test_render_report_section_family_counts():
    groups = [
        {"zh": "A", "pkg": "BSQM_X", "fam": "BSQM", "units": 1, "lines": 1,
         "n_reads": 1, "n_writes": 1, "answer": "x", "writes": []},
        {"zh": "B", "pkg": "BSCH_Y", "fam": "BSCH", "units": 1, "lines": 1,
         "n_reads": 1, "n_writes": 1, "answer": "y", "writes": []},
    ]
    md = render_report_section(groups, {}, 0)
    assert "BSQM 1 / BSCH 1" in md
