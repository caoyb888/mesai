"""
存储过程依赖图谱单元测试（纯本地，无外部依赖）

覆盖：边加载、读/写/调用聚合、调用解析(含推断节点/跨owner/包限定)、入度与入口判定、
     核心表评分与分级、过程 P0 兜底、环检测、CSV/JSON 输入、输出。

关联任务：S2.9-4 存储过程提取与依赖图谱（AI-MES-PLAN-ADJ-2026-001）
作者：AI（芯智云匠）
日期：2026-07-06
"""

import sys
import csv
import json
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from dependency_graph import (
    DependencyGraph, build_self_test_graph, load_edges, load_units,
    write_tables_csv, write_procs_csv, render_report,
    TIER_P0, TIER_P1, TIER_P2,
)


def _g(edges):
    g = DependencyGraph()
    for e in edges:
        g.add_edge(*e)
    g.finalize()
    return g


# ── 边聚合：读/写/调用 ────────────────────────────────────────

def test_read_write_aggregation():
    g = _g([
        ("O", "P1", "READ", "T", ""),
        ("O", "P2", "READ", "T", ""),
        ("O", "P1", "WRITE", "T", "UPDATE"),
    ])
    t = g.tables["T"]
    assert t.read_procs == 2
    assert t.write_procs == 1
    assert t.ops == {"UPDATE"}
    assert t.score == 2 + 2 * 1

def test_write_ops_merge():
    g = _g([
        ("O", "P1", "WRITE", "T", "INSERT"),
        ("O", "P2", "WRITE", "T", "UPDATE/DELETE"),
    ])
    assert g.tables["T"].ops == {"INSERT", "UPDATE", "DELETE"}


# ── 调用解析与入度 ────────────────────────────────────────────

def test_call_resolves_to_existing_unit():
    g = _g([
        ("O", "CALLER", "CALL", "CALLEE", ""),
        ("O", "CALLEE", "READ", "T", ""),
    ])
    assert "O.CALLEE" in g.procs["O.CALLER"].calls
    assert "O.CALLER" in g.procs["O.CALLEE"].called_by
    assert not g.procs["O.CALLEE"].inferred

def test_call_creates_inferred_node():
    g = _g([("O", "CALLER", "CALL", "UNKNOWN_FN", "")])
    node = g.procs["O.UNKNOWN_FN"]
    assert node.inferred is True
    assert "UNKNOWN_FN" in g.external_calls

def test_package_qualified_call_resolves_to_package():
    g = _g([("O", "CALLER", "CALL", "PKG_X.SEND", "")])
    assert "O.PKG_X" in g.procs           # 包名作为节点
    assert g.procs["O.PKG_X"].inferred

def test_cross_owner_call_by_name():
    g = _g([
        ("A", "CALLER", "CALL", "SHARED", ""),
        ("B", "SHARED", "READ", "T", ""),
    ])
    assert "B.SHARED" in g.procs["A.CALLER"].calls


# ── 入口过程 ──────────────────────────────────────────────────

def test_entry_point_detection():
    g = _g([
        ("O", "TOP", "CALL", "MID", ""),
        ("O", "MID", "READ", "T", ""),
    ])
    assert g.procs["O.TOP"].is_entry is True     # 无人调用 + 有动作
    assert g.procs["O.MID"].is_entry is False    # 被调用

def test_inferred_node_not_entry():
    g = _g([("O", "CALLER", "CALL", "UNKNOWN", "")])
    assert g.procs["O.UNKNOWN"].is_entry is False  # 无自身动作


# ── 分级 ──────────────────────────────────────────────────────

def test_core_table_is_p0():
    g = build_self_test_graph()
    assert g.tables["WO_MASTER"].tier == TIER_P0

def test_entry_writer_forced_p0():
    g = build_self_test_graph()
    assert g.procs["MESAPUSER.SP_CLOSE_WORKORDER"].tier == TIER_P0

def test_readonly_entry_not_forced_p0():
    """纯只读入口（SP_REPORT）不因入口身份强制 P0"""
    g = build_self_test_graph()
    p = g.procs["MESAPUSER.SP_REPORT"]
    assert p.is_entry and not p.writes and not p.calls
    assert p.tier != TIER_P0

def test_tiers_are_assigned_to_all():
    g = build_self_test_graph()
    assert all(t.tier in (TIER_P0, TIER_P1, TIER_P2) for t in g.tables.values())
    assert all(p.tier in (TIER_P0, TIER_P1, TIER_P2) for p in g.procs.values())


# ── 环检测 ────────────────────────────────────────────────────

def test_cycle_detection():
    g = _g([
        ("O", "A", "CALL", "B", ""),
        ("O", "B", "CALL", "A", ""),
    ])
    cycles = g.find_cycles()
    assert len(cycles) >= 1
    assert set(cycles[0][:-1]) == {"O.A", "O.B"}

def test_no_false_cycle():
    g = build_self_test_graph()
    assert g.find_cycles() == []


# ── I/O ───────────────────────────────────────────────────────

def test_load_edges_csv(tmp_path):
    p = tmp_path / "edges.csv"
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["SRC_OWNER", "SRC_UNIT", "EDGE_TYPE", "TARGET", "DETAIL"])
        w.writerow(["O", "P", "READ", "T", ""])
        w.writerow(["O", "P", "WRITE", "T2", "INSERT"])
    g = DependencyGraph()
    load_edges(g, [str(p)])
    g.finalize()
    assert "T" in g.tables and "T2" in g.tables
    assert g.procs["O.P"].writes == {"T2"}

def test_load_units_registers_no_edge_functions(tmp_path):
    meta = {"owner": "O", "program_units": [
        {"name": "FC_LONELY", "object_type": "FUNCTION"},
    ]}
    p = tmp_path / "meta.json"
    p.write_text(json.dumps(meta), encoding="utf-8")
    g = DependencyGraph()
    load_units(g, str(p))
    load_edges(g, [])
    g.finalize()
    assert "O.FC_LONELY" in g.procs        # 无出边函数也注册

def test_write_csvs_and_report(tmp_path):
    g = build_self_test_graph()
    tb, pr = tmp_path / "t.csv", tmp_path / "p.csv"
    write_tables_csv(g, str(tb))
    write_procs_csv(g, str(pr))
    trows = list(csv.DictReader(open(tb, encoding="utf-8")))
    assert any(r["TABLE"] == "WO_MASTER" and r["TIER"] == "P0" for r in trows)
    prows = list(csv.DictReader(open(pr, encoding="utf-8")))
    assert any(r["NAME"] == "SP_CLOSE_WORKORDER" and r["IS_ENTRY"] == "1" for r in prows)
    md = render_report(g)
    assert "核心资产分级" in md and "WO_MASTER" in md
