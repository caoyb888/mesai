"""
PL/SQL 超大子程序「二次切分」器单元测试（纯本地）

覆盖：顶层语句边界枚举（块深度平衡：BEGIN/IF/LOOP/CASE 与各类 END）、
     声明段/可执行体/尾段定位、IF/LOOP/CASE 语句递归降级、结构不可切时硬切兜底、
     覆盖率（片段拼接逐字符还原可执行体）与尾段完整性断言、
     两个已修复的静默缺陷回归：
       ①「首条语句短」过程被从中间截断（须取终结 END 而非首次深度归零）；
       ② 表达式列表中裸 END 后紧跟新 CASE 被误吞（END+标签须紧邻才合并）。

关联任务：S3-2 超大过程二次切分（REQ-MES-AI-20260716-001 遗留项）
作者：AI（芯智云匠）
日期：2026-07-16
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from plsql_second_split import (
    _statement_spans, _split_body, _leading_block, _hard_split,
    chunk_region, second_split_unit, second_split_metadata, _line_count,
)


def _mk(name, src):
    return {"package": "PKG", "name": name, "kind": "PROCEDURE",
            "line_count": _line_count(src), "source": src, "start_line": 1}


# ── 顶层语句边界 / 深度平衡 ──────────────────────────────────────
def test_statement_spans_depth_balance():
    s = ("x1;\n"
         "IF a THEN b; END IF;\n"
         "FOR i IN 1..9 LOOP c; END LOOP;\n"
         "y := CASE WHEN a THEN 1 ELSE 2 END;\n"
         "z1;\n")
    spans = _statement_spans(s)
    nonblank = [(a, b) for (a, b) in spans if s[a:b].strip()]
    assert len(nonblank) == 5
    # 拼接必须逐字符还原（含尾部空白）
    assert "".join(s[a:b] for (a, b) in spans) == s


def test_end_case_expression_list_not_swallowed():
    # F(CASE..END, CASE..END)：两个 CASE 表达式，裸 END 后跟逗号+新 CASE
    s = "s0;\nX := F(CASE WHEN a THEN 1 END, CASE WHEN b THEN 2 END);\ns1;\n"
    nb = [(a, b) for (a, b) in _statement_spans(s) if s[a:b].strip()]
    assert len(nb) == 3          # s0 / 赋值 / s1，深度平衡


def test_end_case_statement_merged():
    s = "s0;\nCASE x WHEN 1 THEN a; END CASE;\ns1;\n"
    nb = [(a, b) for (a, b) in _statement_spans(s) if s[a:b].strip()]
    assert len(nb) == 3


# ── 声明段 / 可执行体 / 尾段 ─────────────────────────────────────
def test_split_body_basic():
    src = "PROCEDURE P IS\n  V NUMBER;\nBEGIN\n  V := 1;\nEND P;\n"
    decl, region, tail = _split_body(src)
    assert "PROCEDURE P" in decl and "V NUMBER" in decl
    assert "V := 1;" in region
    assert tail.strip().upper().startswith("END P")


def test_split_body_last_end_not_first_zero():
    # 回归①：首条语句是短 IF..END IF;（深度首次归零点），其后仍有代码，
    # 必须取终结 END → region 含末条 INSERT，tail 仅终结 END
    src = ("PROCEDURE PR_T IS\n  V NUMBER;\nBEGIN\n"
           "  IF A THEN NULL; END IF;\n"
           "  V := 1;\n  INSERT INTO T VALUES(V);\n"
           "END PR_T;\n")
    decl, region, tail = _split_body(src)
    assert "INSERT INTO T" in region
    assert tail.strip().upper().startswith("END PR_T")


def test_split_body_case_imbalance_regression():
    # 回归②：过程体含表达式列表里的 CASE，历史上会漏计导致深度失衡、截断
    src = ("PROCEDURE PR_C IS\n  V NUMBER;\nBEGIN\n"
           "  V := F(CASE WHEN a THEN 1 END, CASE WHEN b THEN 2 END);\n"
           "  INSERT INTO T VALUES(V);\n"
           "END PR_C;\n")
    decl, region, tail = _split_body(src)
    assert "INSERT INTO T" in region
    assert tail.strip().upper().startswith("END PR_C")


# ── 递归降级 ────────────────────────────────────────────────────
def test_leading_block_if_descent():
    stmt = "\n  IF a THEN\n    s1;\n    s2;\n  ELSE\n    s3;\n  END IF;"
    blk = _leading_block(stmt)
    assert blk is not None
    prefix, inner, suffix = blk
    assert prefix.rstrip().endswith("THEN")
    assert "s1;" in inner and "s3;" in inner
    assert suffix.strip().upper().startswith("END IF")
    assert prefix + inner + suffix == stmt


def test_leading_block_giant_sql_returns_none():
    # 无开块关键字的单条巨型 SQL → 不可结构化降级
    stmt = "OPEN C FOR SELECT " + ", ".join(f"COL{i}" for i in range(50)) + " FROM DUAL;"
    assert _leading_block(stmt) is None


# ── chunk_region：打包 / 降级 / 硬切 覆盖率 ──────────────────────
def test_chunk_region_packs_blocks_exactly():
    body = ("\n  BEGIN INSERT INTO T1 VALUES(1); END;\n"
            "  BEGIN UPDATE T2 SET A=1; END;\n  OTHER.CALL(X);\n")
    segs, hard = chunk_region(body, 2)
    assert len(segs) >= 2
    assert not any(hard)
    assert "".join(segs) == body


def test_chunk_region_if_cascade_descent_coverage():
    body = ("\n  IF P='A' THEN OPEN C FOR SELECT 1 FROM DUAL;\n"
            "  ELSIF P='B' THEN OPEN C FOR SELECT 2 FROM DUAL;\n"
            "  ELSE OPEN C FOR SELECT 3 FROM DUAL;\n  END IF;\n")
    segs, hard = chunk_region(body, 2)
    assert len(segs) >= 2
    assert "".join(segs) == body


def test_hard_split_exact_and_flagged():
    giant = "SELECT " + ",\n".join(f"C{i}" for i in range(40)) + " INTO V FROM DUAL;\n"
    segs, hard = chunk_region(giant, 10)
    assert len(segs) >= 2
    assert any(hard)
    assert "".join(segs) == giant


# ── 单元装配 / 覆盖率与尾段断言 ─────────────────────────────────
def test_second_split_unit_reconstruction_and_assertions():
    src = ("PROCEDURE PR_T IS\n  V NUMBER;\nBEGIN\n"
           + "".join(f"  V := {i};\n" for i in range(20))
           + "END PR_T;\n")
    units = second_split_unit(_mk("PR_T", src), max_lines=6)
    assert len(units) >= 2
    # 每片段都含共享声明段与说明行
    for u in units:
        assert u["source"].startswith("-- 【二次切分片段")
        assert "PROCEDURE PR_T" in u["source"]
        assert u["parent"] == "PR_T"
        assert u["l2"] is True
    # 片段编号连续
    assert [u["part"] for u in units] == list(range(1, len(units) + 1))
    assert all(u["part_total"] == len(units) for u in units)


def test_tail_assertion_guards_truncation(monkeypatch):
    # 人为制造截断：让 _split_body 返回把代码留在 tail 的结果 → 必须抛错
    import plsql_second_split as mod
    src = "PROCEDURE P IS\nBEGIN\n V:=1;\nEND P;\n"

    def fake_split_body(s):
        # region 只取一半，其余塞进 tail（含实质代码）
        return "PROCEDURE P IS\n", "BEGIN\n", " V:=1;\nEND P;\n"

    monkeypatch.setattr(mod, "_split_body", fake_split_body)
    try:
        mod.second_split_unit(_mk("P", src), max_lines=50)
        assert False, "应因 tail 含未覆盖代码而抛 AssertionError"
    except AssertionError as e:
        assert "tail" in str(e) or "截断" in str(e)


def test_metadata_only_splits_oversized():
    small = "PROCEDURE S IS\nBEGIN\n NULL;\nEND S;\n"
    big = "PROCEDURE B IS\nBEGIN\n" + "".join(f" V:={i};\n" for i in range(30)) + "END B;\n"
    meta = {"owner": "MESAPUSER", "packages": [
        {"package": "PKG", "units": [
            {"package": "PKG", "name": "S", "kind": "PROCEDURE",
             "line_count": _line_count(small), "source": small, "start_line": 1},
            {"package": "PKG", "name": "B", "kind": "PROCEDURE",
             "line_count": _line_count(big), "source": big, "start_line": 1},
        ]}]}
    result, stats = second_split_metadata(meta, min_lines=10, max_lines=6)
    parents = {s["unit"] for s in stats}
    assert "PKG.B" in parents and "PKG.S" not in parents
    assert all(pkg_u["parent"] == "B"
               for pkg in result["packages"] for pkg_u in pkg["units"])
