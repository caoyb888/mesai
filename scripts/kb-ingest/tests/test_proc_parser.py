"""
PL/SQL 存储过程解析器单元测试（纯本地，无外部依赖）

覆盖：词法剥离、读表(含逗号连接/子查询/JOIN)、写表(INSERT/UPDATE/DELETE/MERGE)、
     FOR UPDATE 排除、调用识别与过滤、状态流转、硬编码/PII 分类、动态 SQL、
     JSON 输入、边/清单输出。

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

from proc_parser import (
    split_code, analyze_source, analyze_metadata,
    classify_literal, write_edges, write_literals, render_report,
    _from_clause_tables, _write_tables, _calls, _set_assignments,
)


def _read(src):
    code, _ = split_code(src)
    return _from_clause_tables(code)


# ── 词法剥离 ──────────────────────────────────────────────────

def test_split_code_strips_comments_and_strings():
    code, lits = split_code("A -- FROM X\nB /* JOIN Y */ C 'hello''world'")
    assert "FROM X" not in code and "JOIN Y" not in code
    assert "hello'world" in lits           # '' 转义正确还原
    assert "A" in code and "B" in code and "C" in code

def test_split_code_keep_strings():
    code, _ = split_code("SET S = '90'", keep_strings=True)
    assert "'90'" in code

def test_q_quote_string():
    code, lits = split_code("V := q'[it's a test]';")
    assert "it's a test" in lits
    assert "q'" not in code


# ── 读表 ──────────────────────────────────────────────────────

def test_read_comma_join():
    assert _read("SELECT * FROM WO_MASTER a, WO_ROUTE b WHERE a.x=b.x") == {"WO_MASTER", "WO_ROUTE"}

def test_read_ansi_join():
    t = _read("SELECT * FROM WO_MASTER a JOIN WO_ROUTE b ON a.x=b.x")
    assert t == {"WO_MASTER", "WO_ROUTE"}

def test_read_schema_qualified():
    assert "MESAPUSER.WO_MASTER" in _read("SELECT 1 FROM MESAPUSER.WO_MASTER")

def test_read_subquery_inner_from_captured():
    t = _read("SELECT * FROM (SELECT id FROM INNER_TAB) v WHERE v.id>0")
    assert "INNER_TAB" in t

def test_read_dual_excluded():
    assert _read("SELECT SYSDATE FROM DUAL") == set()

def test_comment_table_not_captured():
    assert _read("SELECT 1 FROM REAL_TAB -- FROM FAKE_TAB\n") == {"REAL_TAB"}


# ── 写表 ──────────────────────────────────────────────────────

def _writes(src):
    code, _ = split_code(src)
    return {w["table"]: set(w["ops"]) for w in _write_tables(code)}

def test_write_insert_update_delete_merge():
    w = _writes("INSERT INTO T1 VALUES(1); UPDATE T2 SET a=1; "
                "DELETE FROM T3; MERGE INTO T4 USING S ON (1=1);")
    assert w["T1"] == {"INSERT"}
    assert w["T2"] == {"UPDATE"}
    assert w["T3"] == {"DELETE"}
    assert w["T4"] == {"MERGE"}

def test_delete_without_from():
    assert "T5" in _writes("DELETE T5 WHERE x=1")

def test_for_update_not_a_write():
    assert _writes("SELECT * FROM T FOR UPDATE") == {}


# ── 调用识别 ──────────────────────────────────────────────────

def test_calls_and_builtin_filter():
    a = analyze_source("BEGIN X := NVL(FC_CALC(1), 0); PKG_A.PROC_B(2); END;")
    assert "FC_CALC" in a.calls
    assert "PKG_A.PROC_B" in a.calls
    assert "NVL" not in a.calls              # 内置过滤

def test_insert_target_not_a_call():
    a = analyze_source("INSERT INTO WO_HISTORY(ID) VALUES(1);")
    assert "WO_HISTORY" not in a.calls       # 表名不算调用
    assert any(w["table"] == "WO_HISTORY" for w in a.write_tables)

def test_type_names_not_calls():
    """变量/参数声明中的 类型(长度) 不算调用（真实库暴露的误判）"""
    a = analyze_source("DECLARE V VARCHAR2(50); C VARCHAR(10); N NUMBER; "
                       "BEGIN V := FC_REAL(1); END;")
    assert "VARCHAR2" not in a.calls
    assert "VARCHAR" not in a.calls
    assert "NUMBER" not in a.calls
    assert "FC_REAL" in a.calls

def test_self_signature_not_a_call():
    """无 name 时从源码识别声明名，并过滤自身签名的括号，避免自引用调用"""
    a = analyze_source("PROCEDURE SP_X(P IN NUMBER) IS BEGIN NULL; END;")
    assert a.name == "SP_X"                   # 声明名被识别
    assert "SP_X" not in a.calls              # 自身签名不算调用

def test_package_body_member_defs_not_calls():
    """包体内多个子程序定义头不算调用；跨包调用仍保留"""
    src = ("PACKAGE BODY PKG IS "
           "PROCEDURE SUB_A(P NUMBER) IS BEGIN OTHER_PKG.DO_IT(P); END; "
           "FUNCTION SUB_B RETURN NUMBER IS BEGIN RETURN SUB_A_HELPER(1); END; "
           "END PKG;")
    a = analyze_source(src, name="PKG", object_type="PACKAGE BODY")
    assert "SUB_A" not in a.calls and "SUB_B" not in a.calls   # 定义头不算调用
    assert "OTHER_PKG.DO_IT" in a.calls                        # 跨包调用保留


# ── 状态流转 ──────────────────────────────────────────────────

def test_set_assignments():
    code, _ = split_code("UPDATE WO_MASTER SET WO_STATUS='90', QTY=5 WHERE ID=1", keep_strings=True)
    sa = _set_assignments(code)
    pairs = {(s["column"], s["value"]) for s in sa}
    assert ("WO_STATUS", "90") in pairs
    assert ("QTY", "5") in pairs


# ── 硬编码 / PII 分类 ─────────────────────────────────────────

@pytest.mark.parametrize("val,kind", [
    ("192.168.1.100", "ip"),
    ("jdbc:oracle:thin:@//h:1521/orcl", "db_conn"),
    ("(HOST=10.0.0.1)(PORT=1521)", "db_conn"),
    ("ops@corp.com", "email"),
    ("FAB-NJ-01", "site_code"),
    ("EMP0012345", None),                    # 无 6+ 连续数字 → 不入清单
    ("20260101999", "long_number"),
    ("hello world", None),
])
def test_classify_literal(val, kind):
    assert classify_literal(val) == kind

def test_literals_collected_from_source():
    a = analyze_source("BEGIN INSERT INTO LOG(M) VALUES('conn=192.168.0.1'); END;")
    assert any(l["kind"] == "ip" for l in a.literals)


# ── 动态 SQL 标记 ─────────────────────────────────────────────

def test_dynamic_sql_flag():
    assert analyze_source("BEGIN EXECUTE IMMEDIATE 'DROP TABLE X'; END;").has_dynamic_sql is True
    assert analyze_source("BEGIN NULL; END;").has_dynamic_sql is False


# ── JSON 输入与输出 ───────────────────────────────────────────

def test_analyze_metadata():
    meta = {
        "owner": "MESAPUSER",
        "program_units": [
            {"name": "SP_A", "object_type": "PROCEDURE",
             "source": "BEGIN UPDATE T SET S='1'; END;"},
            {"name": "EMPTY_ONE", "object_type": "PROCEDURE", "source": None},  # 无源码跳过
        ],
    }
    res = analyze_metadata(meta)
    assert len(res) == 1
    assert res[0].name == "SP_A"
    assert res[0].owner == "MESAPUSER"

def test_write_edges(tmp_path):
    a = analyze_source("SELECT 1 FROM RT; UPDATE WT SET S='1'; BEGIN P.Q(); END;",
                       owner="O", name="U")
    out = tmp_path / "edges.csv"
    write_edges([a], str(out))
    rows = list(csv.DictReader(open(out, encoding="utf-8")))
    kinds = {(r["EDGE_TYPE"], r["TARGET"]) for r in rows}
    assert ("READ", "RT") in kinds
    assert ("WRITE", "WT") in kinds
    assert ("CALL", "P.Q") in kinds

def test_write_literals_count(tmp_path):
    a = analyze_source("BEGIN INSERT INTO L(M) VALUES('192.168.1.1'); END;", owner="O", name="U")
    out = tmp_path / "lit.csv"
    n = write_literals([a], str(out))
    assert n == 1

def test_render_report_contains_sections():
    a = analyze_source("UPDATE WO SET WO_STATUS='90';", owner="MESAPUSER", name="SP_X")
    md = render_report([a])
    assert "存储过程静态分析报告" in md
    assert "MESAPUSER.SP_X" in md
    assert "状态流转候选" in md
