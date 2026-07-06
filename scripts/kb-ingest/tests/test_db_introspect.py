"""
数据库自省器单元测试（假数据，无需真实 Oracle）

覆盖：组装逻辑（表/字段/注释/约束/索引/程序单元/参数）、
     配置从环境变量加载、DBMS 工厂、摘要统计、JSON 序列化、自测样例。

关联任务：S2.9-2 数据库自省与资产盘点（AI-MES-PLAN-ADJ-2026-001）
作者：AI（芯智云匠）
日期：2026-07-06
"""

import sys
import json
from datetime import datetime
from pathlib import Path

import pytest

# 将父目录加入 sys.path 以导入被测模块
sys.path.insert(0, str(Path(__file__).parent.parent))

from db_introspect import (
    Introspector,
    FakeMetadataProvider,
    DbConfig,
    get_provider,
    build_self_test_provider,
    OracleMetadataProvider,
    SchemaMetadata,
    _as_bool,
)

FIXED_NOW = datetime(2026, 7, 6, 8, 0, 0)


# ── 测试夹具：一份包含各类元素的假数据 ────────────────────────

def sample_provider() -> FakeMetadataProvider:
    return FakeMetadataProvider(
        charset="ZHS16GBK",
        tables=[
            {"name": "WO_MASTER", "comment": "工单主表", "num_rows": 1000},
            {"name": "WO_ROUTE", "comment": None, "num_rows": 50},
        ],
        columns=[
            # 故意乱序 position，验证组装时按 position 排序
            {"table": "WO_MASTER", "name": "WO_STATUS", "data_type": "VARCHAR2",
             "length": 2, "nullable": "N", "data_default": "'10'", "position": 2},
            {"table": "WO_MASTER", "name": "WO_ID", "data_type": "VARCHAR2",
             "length": 30, "nullable": "N", "data_default": None, "position": 1},
            {"table": "WO_ROUTE", "name": "WO_ID", "data_type": "VARCHAR2",
             "length": 30, "nullable": "N", "data_default": None, "position": 1},
            # 归属于不存在的表，应被忽略
            {"table": "GHOST_TABLE", "name": "X", "data_type": "NUMBER",
             "length": 22, "nullable": "Y", "data_default": None, "position": 1},
        ],
        column_comments=[
            {"table": "WO_MASTER", "column": "WO_ID", "comment": "工单号"},
            {"table": "WO_MASTER", "column": "WO_STATUS", "comment": "工单状态"},
        ],
        constraints=[
            {"table": "WO_MASTER", "name": "PK_WO", "ctype": "P",
             "column": "WO_ID", "position": 1, "ref_owner": None, "ref_table": None},
            {"table": "WO_ROUTE", "name": "FK_ROUTE_WO", "ctype": "R",
             "column": "WO_ID", "position": 1, "ref_owner": "MESAPUSER", "ref_table": "WO_MASTER"},
        ],
        indexes=[
            {"table": "WO_MASTER", "name": "IX_ST", "unique": "NONUNIQUE",
             "column": "WO_STATUS", "position": 1},
        ],
        program_units=[
            {"name": "FC_CALC", "object_type": "FUNCTION", "status": "VALID"},
            {"name": "PKG_WO", "object_type": "PACKAGE", "status": "VALID"},
        ],
        program_source=[
            # 故意乱序行号，验证按 line 组装
            {"name": "FC_CALC", "type": "FUNCTION", "line": 2, "text": "BEGIN RETURN 1; END;\n"},
            {"name": "FC_CALC", "type": "FUNCTION", "line": 1, "text": "FUNCTION FC_CALC RETURN NUMBER IS\n"},
        ],
        program_arguments=[
            {"object_name": "FC_CALC", "argument_name": "P_IN",
             "data_type": "NUMBER", "in_out": "IN", "position": 1},
        ],
    )


def build_sample() -> SchemaMetadata:
    return Introspector(sample_provider()).build("MESAPUSER", now=FIXED_NOW)


# ── 表与字段 ──────────────────────────────────────────────────

def test_tables_built():
    meta = build_sample()
    names = {t.name for t in meta.tables}
    assert names == {"WO_MASTER", "WO_ROUTE"}
    assert meta.owner == "MESAPUSER"
    assert meta.nls_charset == "ZHS16GBK"
    assert meta.extracted_at == "2026-07-06T08:00:00"


def test_columns_sorted_by_position():
    meta = build_sample()
    wo = next(t for t in meta.tables if t.name == "WO_MASTER")
    assert [c.name for c in wo.columns] == ["WO_ID", "WO_STATUS"]
    assert wo.columns[0].nullable is False  # 'N' → False


def test_orphan_column_ignored():
    """归属不存在表的字段应被丢弃，不建幽灵表"""
    meta = build_sample()
    assert all(t.name != "GHOST_TABLE" for t in meta.tables)


def test_column_comment_backfilled():
    meta = build_sample()
    wo = next(t for t in meta.tables if t.name == "WO_MASTER")
    cmap = {c.name: c for c in wo.columns}
    assert cmap["WO_ID"].comment == "工单号"
    assert cmap["WO_STATUS"].comment == "工单状态"


# ── 约束与索引 ────────────────────────────────────────────────

def test_primary_key_flagged():
    meta = build_sample()
    wo = next(t for t in meta.tables if t.name == "WO_MASTER")
    cmap = {c.name: c for c in wo.columns}
    assert cmap["WO_ID"].is_primary is True
    assert cmap["WO_STATUS"].is_primary is False
    pk = next(c for c in wo.constraints if c.ctype == "P")
    assert pk.columns == ["WO_ID"]


def test_foreign_key_reference_captured():
    meta = build_sample()
    route = next(t for t in meta.tables if t.name == "WO_ROUTE")
    fk = next(c for c in route.constraints if c.ctype == "R")
    assert fk.ref_table == "WO_MASTER"
    assert fk.columns == ["WO_ID"]


def test_index_built():
    meta = build_sample()
    wo = next(t for t in meta.tables if t.name == "WO_MASTER")
    assert len(wo.indexes) == 1
    assert wo.indexes[0].name == "IX_ST"
    assert wo.indexes[0].unique is False
    assert wo.indexes[0].columns == ["WO_STATUS"]


# ── 程序单元（存储过程/函数/包）──────────────────────────────

def test_program_units_built():
    meta = build_sample()
    types = {(u.name, u.object_type) for u in meta.program_units}
    assert types == {("FC_CALC", "FUNCTION"), ("PKG_WO", "PACKAGE")}


def test_program_source_assembled_in_line_order():
    meta = build_sample()
    fc = next(u for u in meta.program_units if u.name == "FC_CALC")
    assert fc.source == "FUNCTION FC_CALC RETURN NUMBER IS\nBEGIN RETURN 1; END;\n"


def test_program_arguments_attached_to_function():
    meta = build_sample()
    fc = next(u for u in meta.program_units if u.name == "FC_CALC")
    assert len(fc.arguments) == 1
    assert fc.arguments[0].name == "P_IN"
    assert fc.arguments[0].in_out == "IN"


def test_package_has_no_arguments():
    """PACKAGE 不挂子程序参数（仅 PROCEDURE/FUNCTION）"""
    meta = build_sample()
    pkg = next(u for u in meta.program_units if u.name == "PKG_WO")
    assert pkg.arguments == []


# ── 摘要与序列化 ──────────────────────────────────────────────

def test_summary_counts():
    s = build_sample().summary()
    assert s["table_count"] == 2
    assert s["column_count"] == 3          # WO_MASTER 2 + WO_ROUTE 1（幽灵字段不计）
    assert s["program_unit_count"] == 2
    assert s["program_units_by_type"] == {"FUNCTION": 1, "PACKAGE": 1}


def test_empty_comment_columns_counted():
    s = build_sample().summary()
    # WO_ROUTE.WO_ID 无注释 → 1 个空注释字段
    assert s["empty_comment_columns"] == 1


def test_json_serializable():
    meta = build_sample()
    text = json.dumps(meta.to_dict(), ensure_ascii=False)
    back = json.loads(text)
    assert back["owner"] == "MESAPUSER"
    assert "工单主表" in text  # 中文不被转义


# ── 配置与工厂 ────────────────────────────────────────────────

def test_config_from_env_ok(monkeypatch):
    monkeypatch.setenv("MES_DB_USER", "itsm_readonly")
    monkeypatch.setenv("MES_DB_PASSWORD", "x")
    monkeypatch.setenv("MES_DB_DSN", "h:1521/orclpdb")
    cfg = DbConfig.from_env()
    assert cfg.user == "itsm_readonly"
    assert cfg.dbms == "oracle"


def test_config_from_env_missing_raises(monkeypatch):
    monkeypatch.delenv("MES_DB_USER", raising=False)
    monkeypatch.delenv("MES_DB_PASSWORD", raising=False)
    monkeypatch.delenv("MES_DB_DSN", raising=False)
    with pytest.raises(EnvironmentError):
        DbConfig.from_env()


def test_get_provider_oracle():
    cfg = DbConfig(user="u", password="p", dsn="d")
    assert isinstance(get_provider("oracle", cfg), OracleMetadataProvider)

def test_use_dba_swaps_views():
    cfg = DbConfig(user="u", password="p", dsn="d")
    all_p = OracleMetadataProvider(cfg, use_dba=False)
    dba_p = OracleMetadataProvider(cfg, use_dba=True)
    assert "all_tables" in all_p._SQL["tables"]
    assert "dba_tables" in dba_p._SQL["tables"]
    assert "all_" not in dba_p._SQL["columns"]     # 全部换成 dba_


def test_get_provider_unknown_raises():
    cfg = DbConfig(user="u", password="p", dsn="d")
    with pytest.raises(NotImplementedError):
        get_provider("db2", cfg)


# ── 自测样例可正常组装（不依赖 oracledb 安装）────────────────

def test_self_test_provider_builds():
    meta = Introspector(build_self_test_provider()).build("MESAPUSER", now=FIXED_NOW)
    assert meta.summary()["table_count"] == 1
    fc = next(u for u in meta.program_units if u.name == "FC_YN_TO_BOOLEAN")
    assert "FC_YN_TO_BOOLEAN" in (fc.source or "")


def test_build_source_units_filters():
    """source_units 只拉指定单元的源码（P0 子集深析用），其余单元无源码"""
    prov = FakeMetadataProvider(
        program_units=[
            {"name": "SP_A", "object_type": "PROCEDURE", "status": "VALID"},
            {"name": "SP_B", "object_type": "PROCEDURE", "status": "VALID"},
        ],
        program_source=[
            {"name": "SP_A", "type": "PROCEDURE", "line": 1, "text": "BEGIN NULL; END;"},
            {"name": "SP_B", "type": "PROCEDURE", "line": 1, "text": "BEGIN NULL; END;"},
        ],
    )
    meta = Introspector(prov).build("O", now=FIXED_NOW, source_units=["SP_A"])
    src = {u.name: u.source for u in meta.program_units}
    assert src["SP_A"] and "BEGIN" in src["SP_A"]
    assert src["SP_B"] is None                # 未指定 → 不拉源码


def test_resolve_source_units_merges_comma_and_file(tmp_path):
    from db_introspect import _resolve_source_units
    import argparse
    f = tmp_path / "units.txt"
    f.write_text("# P0 名单\nPKG_X\nPKG_Y\n", encoding="utf-8")
    ns = argparse.Namespace(source_units="SP_A, SP_B", source_units_file=str(f))
    assert _resolve_source_units(ns) == ["SP_A", "SP_B", "PKG_X", "PKG_Y"]
    assert _resolve_source_units(argparse.Namespace(source_units=None, source_units_file=None)) is None


def test_build_no_source_keeps_signature():
    """--no-source：不拉源码但保留单元清单与参数签名（大库结构盘点用）"""
    meta = Introspector(build_self_test_provider()).build(
        "MESAPUSER", now=FIXED_NOW, include_source=False)
    fc = next(u for u in meta.program_units if u.name == "FC_YN_TO_BOOLEAN")
    assert fc.source is None            # 未拉源码
    assert len(fc.arguments) >= 1       # 参数签名仍在
    assert meta.summary()["program_unit_count"] == 1


# ── 布尔归一化辅助 ────────────────────────────────────────────

@pytest.mark.parametrize("val,expected", [
    ("Y", True), ("N", False), ("YES", True), ("NO", False),
    ("UNIQUE", True), ("NONUNIQUE", False), (1, True), (0, False),
    (True, True), (None, True),  # None → default(True)
])
def test_as_bool(val, expected):
    assert _as_bool(val, default=True) is expected
