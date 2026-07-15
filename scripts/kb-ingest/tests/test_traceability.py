"""
T3-3-2 追溯链路纯逻辑单元测试（无 DB / 无外部 AI）

覆盖：载体表提取（含主键标注）、桥接表（同表共键）、桥接过程（读上游写下游，双向）、
     有证据边筛选与保序、子系统前缀、实体载体画像、报告段幂等标记。

关联需求单：REQ-MES-AI-20260715-001（T3-3-2）
作者：AI（芯智云匠）  日期：2026-07-15
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from proc_parser import ProcAnalysis
from run_s3_traceability import (
    build_carriers, bridge_tables, bridge_procs, present_edges,
    module_of, carrier_profile, render_report_section, SECTION_MARKER,
    CORE_KEYS,
)


def _col(name, pk=False):
    return {"name": name, "is_primary": pk}


# 迷你结构元数据：模拟炉次→板坯→板/试样 血缘
STRUCT = {
    "tables": [
        {"name": "SMS_HEAT", "columns": [_col("HEAT_NO", pk=True), _col("HEAT_STS")]},
        # 家谱桥表：同时含 HEAT_NO 与 SLAB_NO
        {"name": "SMS_SLAB", "columns": [_col("SLAB_NO", pk=True), _col("HEAT_NO"), _col("ORD_NO")]},
        # 板坯→板 桥表
        {"name": "SPR_PLATE", "columns": [_col("PLT_NO", pk=True), _col("SLAB_NO")]},
        # 试样表：只含 PLT_NO 与 SMP_NO（板→试样桥表）
        {"name": "SQM_SMP", "columns": [_col("SMP_NO", pk=True), _col("PLT_NO")]},
        # 订单主表
        {"name": "SOR_ORDER", "columns": [_col("ORD_NO", pk=True)]},
        # 无关键列的表不应进入任何载体
        {"name": "TOAD_PLAN_TABLE", "columns": [_col("STATEMENT_ID")]},
        # 无名表容错
        {"columns": [_col("HEAT_NO")]},
    ]
}


def _pa(name, reads, writes):
    return ProcAnalysis(owner="MESAPUSER", name=name, object_type="PACKAGE BODY",
                        read_tables=list(reads),
                        write_tables=[{"table": t} for t in writes])


# ── 载体提取 ──────────────────────────────────────────────────
def test_build_carriers_maps_keys_to_tables():
    carriers, pk = build_carriers(STRUCT, CORE_KEYS)
    assert carriers["HEAT_NO"] == {"SMS_HEAT", "SMS_SLAB"}
    assert carriers["SLAB_NO"] == {"SMS_SLAB", "SPR_PLATE"}
    assert carriers["PLT_NO"] == {"SPR_PLATE", "SQM_SMP"}


def test_build_carriers_pk_flag_separated():
    _, pk = build_carriers(STRUCT, CORE_KEYS)
    assert pk["HEAT_NO"] == {"SMS_HEAT"}        # SMS_SLAB 里 HEAT_NO 非主键
    assert pk["SLAB_NO"] == {"SMS_SLAB"}


def test_build_carriers_ignores_nameless_table_and_noise_columns():
    carriers, _ = build_carriers(STRUCT, CORE_KEYS)
    # 无名表虽含 HEAT_NO 也被跳过（无表名无法追溯）
    assert all(t for k in carriers for t in carriers[k])
    assert "STATEMENT_ID" not in carriers


# ── 桥接表 ────────────────────────────────────────────────────
def test_bridge_tables_shared_key_table():
    carriers, _ = build_carriers(STRUCT, CORE_KEYS)
    assert bridge_tables(carriers, "HEAT_NO", "SLAB_NO") == ["SMS_SLAB"]
    assert bridge_tables(carriers, "SLAB_NO", "PLT_NO") == ["SPR_PLATE"]


def test_bridge_tables_none_when_disjoint():
    carriers, _ = build_carriers(STRUCT, CORE_KEYS)
    # HEAT_NO 与 SMP_NO 无同表共载
    assert bridge_tables(carriers, "HEAT_NO", "SMP_NO") == []


# ── 桥接过程（双向）───────────────────────────────────────────
def test_bridge_procs_read_upstream_write_downstream():
    carriers, _ = build_carriers(STRUCT, CORE_KEYS)
    procs = [_pa("BSMS_OPER_CC", reads=["SMS_HEAT"], writes=["SMS_SLAB"])]
    hits = bridge_procs(procs, carriers, "HEAT_NO", "SLAB_NO")
    assert hits and hits[0][0] == "BSMS_OPER_CC"
    assert hits[0][1] == ["SMS_HEAT"] and hits[0][2] == ["SMS_SLAB"]


def test_bridge_procs_reverse_direction_counts():
    carriers, _ = build_carriers(STRUCT, CORE_KEYS)
    # 读下游 SPR_PLATE(PLT/SLAB) 写上游 SMS_SLAB(SLAB/HEAT) —— 反向回写也算血缘
    procs = [_pa("BSPR_BACK", reads=["SPR_PLATE"], writes=["SMS_SLAB"])]
    hits = bridge_procs(procs, carriers, "HEAT_NO", "SLAB_NO")
    assert hits and hits[0][0] == "BSPR_BACK"


def test_bridge_procs_ignores_unrelated():
    carriers, _ = build_carriers(STRUCT, CORE_KEYS)
    procs = [_pa("BSOR_ONLY", reads=["SOR_ORDER"], writes=["SOR_ORDER"])]
    assert bridge_procs(procs, carriers, "HEAT_NO", "SLAB_NO") == []


def test_bridge_procs_sorted_by_name():
    carriers, _ = build_carriers(STRUCT, CORE_KEYS)
    procs = [_pa("ZBSMS", reads=["SMS_HEAT"], writes=["SMS_SLAB"]),
             _pa("ABSMS", reads=["SMS_HEAT"], writes=["SMS_SLAB"])]
    names = [h[0] for h in bridge_procs(procs, carriers, "HEAT_NO", "SLAB_NO")]
    assert names == sorted(names)


# ── 有证据边筛选与保序 ────────────────────────────────────────
def test_present_edges_keeps_only_evidenced_and_ordered():
    carriers, _ = build_carriers(STRUCT, CORE_KEYS)
    procs = [_pa("BSMS_OPER_CC", reads=["SMS_HEAT"], writes=["SMS_SLAB"])]
    edges = present_edges(carriers, procs)
    pairs = [(e["a"], e["b"]) for e in edges]
    # 有桥表的边保留：HEAT→SLAB、SLAB→PLT、PLT→SMP、ORD 相关
    assert ("HEAT_NO", "SLAB_NO") in pairs
    assert ("SLAB_NO", "PLT_NO") in pairs
    assert ("PLT_NO", "SMP_NO") in pairs
    # 保序：HEAT→SLAB 必在 SLAB→PLT 之前（遵循 TRACE_EDGES 制造流转序）
    assert pairs.index(("HEAT_NO", "SLAB_NO")) < pairs.index(("SLAB_NO", "PLT_NO"))


def test_present_edges_skips_missing_keys_and_no_evidence():
    # 只有炉次表、无任何下游 → 所有边无证据
    tiny = {"tables": [{"name": "SMS_HEAT", "columns": [_col("HEAT_NO", pk=True)]}]}
    carriers, _ = build_carriers(tiny, CORE_KEYS)
    assert present_edges(carriers, []) == []


# ── 辅助 ──────────────────────────────────────────────────────
def test_module_of_prefix():
    assert module_of("SMS_HEAT") == "SMS"
    assert module_of("SPR_PLATE_INFO") == "SPR"
    assert module_of("NOUNDERSCORE") == "NOUNDERSCORE"


def test_carrier_profile_counts_and_modules():
    carriers, pk = build_carriers(STRUCT, CORE_KEYS)
    p = carrier_profile(carriers, pk, "HEAT_NO")
    assert p["n_tables"] == 2 and p["n_pk"] == 1
    assert p["pk_examples"] == ["SMS_HEAT"]
    mods = dict(p["modules"])
    assert mods.get("SMS") == 2


# ── 报告段 ────────────────────────────────────────────────────
def test_render_report_section_has_marker_and_edges():
    carriers, pk = build_carriers(STRUCT, CORE_KEYS)
    edges = [{"a": "HEAT_NO", "b": "SLAB_NO", "bridge_tables": ["SMS_SLAB"],
              "bridge_procs": [("BSMS_OPER_CC", ["SMS_HEAT"], ["SMS_SLAB"])],
              "answer": "正向：由炉次定位板坯。"}]
    md = render_report_section(edges, carriers, pk, 1234)
    assert SECTION_MARKER in md
    assert "追溯链路" in md
    assert "SMS_SLAB" not in md or "炉次" in md   # 明细含合成答案
    assert "1,234" in md                          # Token 千分位
    assert "核心实体载体画像" in md
