"""
PL/SQL 包体子程序切分器单元测试（纯本地）

覆盖：长度保留掩码、包级 PREAMBLE 抽取、顶层子程序识别、嵌套/前向声明排除、
     命名 END 配对、裸 END 回退标记、END IF/LOOP/CASE 不误判、批处理与报告。

关联任务：S3-0 T3-0-4 大包子程序级切分（AI-MES-S3PLAN-2026-001）
作者：AI（芯智云匠）
日期：2026-07-06
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from plsql_splitter import (
    mask_code, split_package_body, split_metadata, render_report, _is_definition,
)


PKG = """PACKAGE BODY PKG AS
  G_VAR NUMBER := 0;
  CURSOR C_ALL IS SELECT 1 FROM DUAL;
  PROCEDURE PR_FWD(A NUMBER);
  PROCEDURE PR_ONE(A NUMBER) IS
  BEGIN
    IF A > 0 THEN G_VAR := 1; END IF;
    OTHER_PKG.DO(A);
  END PR_ONE;
  FUNCTION FN_TWO RETURN NUMBER IS
    PROCEDURE NESTED IS BEGIN NULL; END NESTED;
  BEGIN
    NESTED();
    RETURN G_VAR;
  END FN_TWO;
END PKG;
"""


def _subs(src=PKG):
    return split_package_body(src, package="PKG")


# ── 掩码 ──────────────────────────────────────────────────────

def test_mask_preserves_length():
    src = "A -- comment PROCEDURE X\nB '文字PROCEDURE' C"
    m = mask_code(src)
    assert len(m) == len(src)

def test_mask_hides_keywords_in_comment_and_string():
    src = "X -- PROCEDURE FAKE\nY 'END PKG;' Z"
    m = mask_code(src)
    assert "PROCEDURE" not in m
    assert "END PKG" not in m
    assert "X" in m and "Y" in m and "Z" in m


# ── 顶层子程序识别 ────────────────────────────────────────────

def test_top_level_count():
    names = [u.name for u in _subs() if u.kind != "PREAMBLE"]
    assert names == ["PR_ONE", "FN_TWO"]        # 恰两个顶层

def test_nested_excluded():
    names = [u.name for u in _subs() if u.kind != "PREAMBLE"]
    assert "NESTED" not in names

def test_forward_decl_excluded():
    names = [u.name for u in _subs() if u.kind != "PREAMBLE"]
    assert "PR_FWD" not in names

def test_preamble_extracted():
    pre = [u for u in _subs() if u.kind == "PREAMBLE"]
    assert len(pre) == 1
    assert "G_VAR" in pre[0].source and "C_ALL" in pre[0].source

def test_named_end_closes_subprogram():
    one = next(u for u in _subs() if u.name == "PR_ONE")
    assert one.source.rstrip().endswith("END PR_ONE;")
    assert one.fallback is False

def test_function_contains_nested_body():
    fn = next(u for u in _subs() if u.name == "FN_TWO")
    assert "NESTED" in fn.source and fn.source.rstrip().endswith("END FN_TWO;")

def test_end_if_not_mistaken_for_subprogram_end():
    one = next(u for u in _subs() if u.name == "PR_ONE")
    assert "END IF;" in one.source           # 控制块 END 保留在子程序体内


# ── 前向声明判定 ──────────────────────────────────────────────

def test_is_definition():
    m = mask_code("PROCEDURE P(A NUMBER) IS BEGIN NULL; END P;")
    assert _is_definition(m, m.index("(")) is True
    m2 = mask_code("PROCEDURE P(A NUMBER);")
    assert _is_definition(m2, m2.index("(")) is False


# ── 裸 END 回退 ───────────────────────────────────────────────

def test_bare_end_triggers_fallback():
    src = ("PACKAGE BODY P AS\n"
           "PROCEDURE A IS BEGIN NULL; END;\n"       # 裸 END → 命名配对失败
           "PROCEDURE B IS BEGIN NULL; END B;\n"
           "END P;\n")
    subs = [u for u in split_package_body(src, package="P") if u.kind != "PREAMBLE"]
    a = next(u for u in subs if u.name == "A")
    assert a.fallback is True                 # 标记回退供人工复核
    b = next(u for u in subs if u.name == "B")
    assert b.fallback is False


# ── 批处理与报告 ──────────────────────────────────────────────

def test_split_metadata_and_report():
    meta = {"owner": "O", "program_units": [
        {"name": "PKG", "object_type": "PACKAGE BODY", "source": PKG},
        {"name": "SMALL", "object_type": "PACKAGE BODY",
         "source": "PACKAGE BODY SMALL AS\nPROCEDURE X IS BEGIN NULL; END X;\nEND SMALL;\n"},
        {"name": "SPEC", "object_type": "PACKAGE", "source": "PACKAGE SPEC AS END;"},  # 非包体
    ]}
    res = split_metadata(meta, min_lines=0)
    pkgs = {p["package"]: p for p in res["packages"]}
    assert "PKG" in pkgs and "SMALL" in pkgs
    assert "SPEC" not in pkgs                  # 规格不切
    assert pkgs["PKG"]["unit_count"] == 2
    md = render_report(res)
    assert "大包子程序切分报告" in md and "PKG" in md

def test_min_lines_filter():
    meta = {"owner": "O", "program_units": [
        {"name": "SMALL", "object_type": "PACKAGE BODY",
         "source": "PACKAGE BODY SMALL AS\nPROCEDURE X IS BEGIN NULL; END X;\nEND SMALL;\n"},
    ]}
    assert split_metadata(meta, min_lines=1000)["packages"] == []
