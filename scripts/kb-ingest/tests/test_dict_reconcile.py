"""
数据字典对账器单元测试（纯本地，无外部依赖）

覆盖：各差异类别、表级/列级、类型/注释/长度、范围限定(scope)、整表缺失不逐列刷屏、
     JSON/CSV 索引构建、统计与输出。

关联任务：S2.9-5 字典对账（AI-MES-PLAN-ADJ-2026-001）
作者：AI（芯智云匠）
日期：2026-07-06
"""

import sys
import csv
import json
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from dict_reconcile import (
    reconcile, tally, render_report, write_csv,
    index_from_introspect, index_from_dict_csv, build_self_test,
    Discrepancy,
    CAT_TABLE_MISS_DICT, CAT_TABLE_MISS_DB, CAT_COL_MISS_DICT, CAT_COL_MISS_DB,
    CAT_TYPE, CAT_LENGTH, CAT_CMT_DB_EMPTY, CAT_CMT_DICT_EMPTY, CAT_CMT_CONFLICT,
)


def _cat_of(ds, o, t, c):
    return next((d.category for d in ds if (d.owner, d.table, d.column) == (o, t, c)), None)


# ── 自测样例全类别 ────────────────────────────────────────────

def test_self_test_all_categories():
    ds = reconcile(*build_self_test()[:4], build_self_test()[4])
    cats = {d.category for d in ds}
    assert {CAT_TABLE_MISS_DICT, CAT_TABLE_MISS_DB, CAT_TYPE,
            CAT_CMT_DB_EMPTY, CAT_COL_MISS_DICT, CAT_COL_MISS_DB} <= cats


# ── 单类别精确判定 ────────────────────────────────────────────

def _pair():
    db_cols = {("O", "T", "A"): {"type": "VARCHAR2", "length": 10, "comment": "甲"}}
    db_tables = {("O", "T")}
    dict_cols = {("O", "T", "A"): {"type": "VARCHAR2", "length": 10, "comment": "甲"}}
    dict_tables = {("O", "T")}
    return db_cols, db_tables, dict_cols, dict_tables

def test_identical_no_discrepancy():
    db_c, db_t, dc, dt = _pair()
    assert reconcile(db_c, db_t, dc, dt, {"O"}) == []

def test_type_mismatch():
    db_c, db_t, dc, dt = _pair()
    dc[("O", "T", "A")]["type"] = "NUMBER"
    ds = reconcile(db_c, db_t, dc, dt, {"O"})
    d = ds[0]
    assert d.category == CAT_TYPE and d.db_value == "VARCHAR2" and d.dict_value == "NUMBER"
    assert d.severity == "high"

def test_base_type_ignores_precision():
    db_c, db_t, dc, dt = _pair()
    db_c[("O", "T", "A")]["type"] = "VARCHAR2(10)"
    dc[("O", "T", "A")]["type"] = "VARCHAR2"
    assert reconcile(db_c, db_t, dc, dt, {"O"}) == []      # 基础类型相同

def test_comment_db_empty_is_repair_source():
    db_c, db_t, dc, dt = _pair()
    db_c[("O", "T", "A")]["comment"] = ""
    ds = reconcile(db_c, db_t, dc, dt, {"O"})
    assert _cat_of(ds, "O", "T", "A") == CAT_CMT_DB_EMPTY
    assert ds[0].dict_value == "甲"

def test_comment_dict_empty():
    db_c, db_t, dc, dt = _pair()
    dc[("O", "T", "A")]["comment"] = ""
    assert _cat_of(reconcile(db_c, db_t, dc, dt, {"O"}), "O", "T", "A") == CAT_CMT_DICT_EMPTY

def test_comment_conflict():
    db_c, db_t, dc, dt = _pair()
    dc[("O", "T", "A")]["comment"] = "乙"
    assert _cat_of(reconcile(db_c, db_t, dc, dt, {"O"}), "O", "T", "A") == CAT_CMT_CONFLICT

def test_length_off_by_default():
    db_c, db_t, dc, dt = _pair()
    dc[("O", "T", "A")]["length"] = 99
    assert reconcile(db_c, db_t, dc, dt, {"O"}) == []                  # 默认不查长度
    ds = reconcile(db_c, db_t, dc, dt, {"O"}, check_length=True)
    assert _cat_of(ds, "O", "T", "A") == CAT_LENGTH


# ── 范围与整表缺失 ────────────────────────────────────────────

def test_scope_excludes_other_owner():
    db_c = {("A", "T", "X"): {"type": "N", "length": 1, "comment": ""}}
    dc = {("B", "T", "X"): {"type": "N", "length": 1, "comment": ""}}
    ds = reconcile(db_c, {("A", "T")}, dc, {("B", "T")}, {"A"})       # 仅对 A 对账
    assert all(d.owner == "A" for d in ds)
    assert any(d.category == CAT_TABLE_MISS_DICT for d in ds)          # A.T 字典无
    assert not any(d.owner == "B" for d in ds)                        # B 不在范围

def test_missing_table_not_exploded_by_column():
    """整表在字典缺失时，只报表级，不为每列刷 col_missing_in_dict"""
    db_c = {("O", "T", f"C{i}"): {"type": "N", "length": 1, "comment": ""} for i in range(5)}
    ds = reconcile(db_c, {("O", "T")}, {}, set(), {"O"})
    assert sum(1 for d in ds if d.category == CAT_TABLE_MISS_DICT) == 1
    assert not any(d.category == CAT_COL_MISS_DICT for d in ds)        # 无逐列刷屏


# ── 索引构建 ──────────────────────────────────────────────────

def test_index_from_introspect(tmp_path):
    meta = {"owner": "MESAPUSER", "tables": [
        {"name": "WO_MASTER", "columns": [
            {"name": "WO_ID", "data_type": "VARCHAR2", "length": 30, "comment": "工单号"},
        ]},
    ]}
    p = tmp_path / "m.json"
    p.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    cols, tables, owners = index_from_introspect([str(p)])
    assert ("MESAPUSER", "WO_MASTER") in tables
    assert cols[("MESAPUSER", "WO_MASTER", "WO_ID")]["comment"] == "工单号"
    assert owners == {"MESAPUSER"}

def test_index_from_dict_csv(tmp_path):
    p = tmp_path / "d.csv"
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["SCHEMA", "TABLE_NAME", "COLUMN_NAME", "DATA_TYPE", "LEN", "COL_COMMENT", "SOURCE"])
        w.writerow(["MESAPUSER", "APP_REPORT", "NAME", "VARCHAR2", "100", "报表名称", "DB注释(中文)"])
    cols, tables, owners = index_from_dict_csv(str(p))
    assert cols[("MESAPUSER", "APP_REPORT", "NAME")]["type"] == "VARCHAR2"
    assert ("MESAPUSER", "APP_REPORT") in tables


# ── 统计与输出 ────────────────────────────────────────────────

def test_tally():
    ds = reconcile(*build_self_test()[:4], build_self_test()[4])
    t = tally(ds)
    assert t["total"] == len(ds)
    assert t["by_severity"].get("high", 0) >= 1     # QTY 类型不一致

def test_render_report_has_repair_section():
    ds = reconcile(*build_self_test()[:4], build_self_test()[4])
    md = render_report(ds, {"MESAPUSER"})
    assert "数据字典对账报告" in md
    assert "字典可反哺库空注释" in md
    assert "工单状态" in md                          # WO_STATUS 的字典注释

def test_write_csv(tmp_path):
    ds = reconcile(*build_self_test()[:4], build_self_test()[4])
    out = tmp_path / "disc.csv"
    write_csv(ds, str(out))
    rows = list(csv.DictReader(open(out, encoding="utf-8")))
    assert len(rows) == len(ds)
    assert {"OWNER", "TABLE", "COLUMN", "CATEGORY", "SEVERITY", "DB_VALUE", "DICT_VALUE"} == set(rows[0].keys())
