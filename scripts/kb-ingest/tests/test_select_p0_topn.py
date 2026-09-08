"""
P0 Top-N 中心度选取器单元测试（纯本地，不连库）

覆盖：按 SCORE 降序取 Top-N、剔除 INFERRED、去重保序、Top-N 边界、
     表清单选取、列表文件写出格式。

关联任务：S3-0 P0 Top-N 固化（AI-MES-S3PLAN-2026-001）
关联需求单：REQ-MES-AI-20260706-001
作者：AI（芯智云匠）
日期：2026-07-14
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from select_p0_topn import select_top_units, select_top_tables, _write_list


def _make_procs(tmp_path):
    p = tmp_path / "procs.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["OWNER", "NAME", "READS", "WRITES", "CALLS_OUT", "CALLED_BY",
                    "IS_ENTRY", "INFERRED", "SCORE", "TIER"])
        # 故意乱序，验证按 SCORE 降序
        w.writerow(["MESAPUSER", "BSCT_COST", 5, 3, 10, 8, 0, 0, "0.90", "P0"])
        w.writerow(["MESAPUSER", "BSQM_MTC_ISSUE", 4, 2, 7, 6, 0, 0, "0.75", "P0"])
        w.writerow(["MESAPUSER", "GHOST_PROC", 0, 0, 0, 1, 0, 1, "0.99", "P0"])  # INFERRED 剔除
        w.writerow(["MESAPUSER", "BSCH_PROD_INST", 3, 1, 5, 4, 0, 0, "0.60", "P1"])
        w.writerow(["MESAPUSER", "LOW_ONE", 1, 0, 1, 0, 0, 0, "0.10", "P2"])
    return str(p)


def _make_tables(tmp_path):
    p = tmp_path / "tables.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["TABLE", "READ_PROCS", "WRITE_PROCS", "OPS", "SCORE", "TIER"])
        w.writerow(["WO_MAIN", 20, 8, "R/W", "0.95", "P0"])
        w.writerow(["HEAT_LOG", 10, 3, "R/W", "0.50", "P1"])
        w.writerow(["CFG_MISC", 2, 0, "R", "0.05", "P2"])
    return str(p)


def test_units_sorted_by_score_desc(tmp_path):
    units = select_top_units(_make_procs(tmp_path), top_n=10)
    # GHOST_PROC 虽 SCORE 最高但 INFERRED=1 应被剔除
    assert units[0] == "BSCT_COST"
    assert "GHOST_PROC" not in units
    # 降序
    assert units == ["BSCT_COST", "BSQM_MTC_ISSUE", "BSCH_PROD_INST", "LOW_ONE"]


def test_units_topn_cutoff(tmp_path):
    units = select_top_units(_make_procs(tmp_path), top_n=2)
    assert units == ["BSCT_COST", "BSQM_MTC_ISSUE"]


def test_units_dedup_preserves_order(tmp_path):
    p = tmp_path / "dup.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["OWNER", "NAME", "READS", "WRITES", "CALLS_OUT", "CALLED_BY",
                    "IS_ENTRY", "INFERRED", "SCORE", "TIER"])
        w.writerow(["X", "PKG_A", 1, 1, 1, 1, 0, 0, "0.8", "P0"])
        w.writerow(["Y", "PKG_A", 1, 1, 1, 1, 0, 0, "0.7", "P0"])  # 同名去重
        w.writerow(["Z", "PKG_B", 1, 1, 1, 1, 0, 0, "0.6", "P0"])
    units = select_top_units(str(p), top_n=10)
    assert units == ["PKG_A", "PKG_B"]


def test_tables_topn(tmp_path):
    tbls = select_top_tables(_make_tables(tmp_path), top_n=2)
    assert tbls == ["WO_MAIN", "HEAT_LOG"]


def test_write_list_format(tmp_path):
    out = tmp_path / "units.txt"
    _write_list(str(out), "标题", ["A", "B", "C"])
    content = out.read_text(encoding="utf-8")
    assert content.startswith("# 标题\n")
    assert content.strip().endswith("C")
    assert content.count("\n") == 4  # 标题行 + 3 名 + 末尾换行


def test_write_list_empty(tmp_path):
    out = tmp_path / "empty.txt"
    _write_list(str(out), "空", [])
    assert out.read_text(encoding="utf-8") == "# 空\n"
