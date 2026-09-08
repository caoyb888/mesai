#!/usr/bin/env python3
"""
PL/SQL 存储过程解析器 → 引用表 / 写副作用 / 调用链 / 状态流转 / 硬编码·PII 候选

用途：消费 db_introspect.py 产出的元数据 JSON（program_units[].source），对每个
     PL/SQL 程序单元（存储过程/函数/包体/触发器）做轻量静态分析，抽取：
       · read_tables    —— FROM/JOIN 引用的表（读）
       · write_tables   —— INSERT/UPDATE/DELETE/MERGE 命中的表（写副作用）
       · calls          —— 调用的其它过程/函数/包（过程→过程边）
       · set_assignments—— UPDATE ... SET 列=字面量（状态流转候选，喂断言库）
       · literals       —— 字符串字面量中的硬编码/PII 候选（喂 S5-2 脱敏、Gitleaks）

产出：
  ① 分析报告 Markdown（每单元一节 + 硬编码·PII 汇总）
  ② 依赖边 CSV（供 dependency_graph.py 构图：过程→表读/写、过程→过程调用）
  ③ 硬编码·PII 候选 CSV（供脱敏层与安全审计）

方法与边界（务实的启发式，非完整 PL/SQL 语法分析）：
  · 先用状态机剥离「注释 + 字符串字面量」，再在纯代码上做正则匹配，避免注释/字符串里的
    表名造成误报；字符串字面量单独留存用于硬编码/PII 识别。
  · FROM 子句按逗号连接解析（兼容老式 Oracle 逗号连接）；子查询由其内部 FROM 另行命中。
  · 调用识别排除内置函数与关键字；包限定调用（pkg.proc）一律保留。
  · 已知局限：动态 SQL（EXECUTE IMMEDIATE 拼接串）无法静态解析 → 单独标记 has_dynamic_sql。

用法：
    python proc_parser.py --self-test
    python proc_parser.py --input metadata_mesapuser.json \
        --out-report proc_report.md --out-edges proc_edges.csv --out-literals proc_literals.csv
    python proc_parser.py --source-file some_proc.sql

关联任务：S2.9-4 存储过程提取与依赖图谱（AI-MES-PLAN-ADJ-2026-001）
作者：AI（芯智云匠）
日期：2026-07-06
"""

import os
import re
import sys
import csv
import json
import argparse
import logging
from dataclasses import dataclass, field, asdict
from typing import Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))


# ── 词法：剥离注释、提取字符串字面量 ─────────────────────────

_IDENT_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$#")
_QUOTE_CLOSE = {"(": ")", "[": "]", "{": "}", "<": ">"}


def split_code(src: str, keep_strings: bool = False) -> tuple[str, list[str]]:
    """把 PL/SQL 源码拆为（纯代码, 字符串字面量列表）。
    注释一律用空格占位；字符串默认也占位（避免其内容被误当表名/调用），
    keep_strings=True 时保留字符串（供状态流转挖掘需要字面量值的场景）。"""
    out: list[str] = []
    literals: list[str] = []
    i, n = 0, len(src)

    def _prev_nonspace() -> str:
        for ch in reversed(out):
            if not ch.isspace():
                return ch
        return ""

    while i < n:
        c = src[i]
        nxt = src[i + 1] if i + 1 < n else ""

        # 行注释 --
        if c == "-" and nxt == "-":
            i += 2
            while i < n and src[i] != "\n":
                i += 1
            out.append(" ")
        # 块注释 /* */
        elif c == "/" and nxt == "*":
            i += 2
            while i < n and not (src[i] == "*" and i + 1 < n and src[i + 1] == "/"):
                i += 1
            i += 2
            out.append(" ")
        # q 引号字符串 q'[...]' / q'{...}' / q'!...!'
        elif c in "qQ" and nxt == "'" and _prev_nonspace() not in _IDENT_CHARS:
            open_delim = src[i + 2] if i + 2 < n else ""
            close_delim = _QUOTE_CLOSE.get(open_delim, open_delim)
            j = i + 3
            buf: list[str] = []
            while j < n:
                if src[j] == close_delim and j + 1 < n and src[j + 1] == "'":
                    break
                buf.append(src[j])
                j += 1
            val = "".join(buf)
            literals.append(val)
            out.append("'" + val.replace("'", "''") + "'" if keep_strings else " ")
            i = j + 2
        # 普通字符串 '...'（'' 为转义单引号）
        elif c == "'":
            j = i + 1
            buf = []
            while j < n:
                if src[j] == "'":
                    if j + 1 < n and src[j + 1] == "'":
                        buf.append("'")
                        j += 2
                        continue
                    break
                buf.append(src[j])
                j += 1
            val = "".join(buf)
            literals.append(val)
            out.append("'" + val.replace("'", "''") + "'" if keep_strings else " ")
            i = j + 1
        else:
            out.append(c)
            i += 1

    return "".join(out), literals


# ── 标识符归一 ────────────────────────────────────────────────

def _norm_ident(s: str) -> str:
    """去引号并大写（Oracle 默认大写存储）；保留 schema. 限定"""
    return s.replace('"', "").strip().upper()


_TABLE_RE = r'("?[A-Za-z_][\w$#]*"?(?:\.\s*"?[A-Za-z_][\w$#]*"?)?)'


# ── 表引用：读（FROM / JOIN）──────────────────────────────────

# FROM 子句到此类关键字为止
_FROM_STOP = {
    "WHERE", "GROUP", "ORDER", "HAVING", "CONNECT", "START", "UNION", "MINUS",
    "INTERSECT", "MODEL", "FETCH", "FOR", "LOOP", "ON", "USING", "SET", "WHEN",
    "RETURNING", "INTO", "JOIN", "LEFT", "RIGHT", "INNER", "OUTER", "CROSS", "FULL",
}


def _from_clause_tables(code: str) -> set[str]:
    """解析每个 FROM 子句的逗号连接表清单（子查询跳过，由内部 FROM 另行命中）"""
    tables: set[str] = set()
    for m in re.finditer(r"\bFROM\b", code, re.I):
        i, n = m.end(), len(code)
        depth = 0
        item: list[str] = []

        def _flush(chars: list[str]):
            token = "".join(chars).strip()
            if not token or token.startswith("("):
                return
            first = re.match(r'\s*("?[A-Za-z_][\w$#]*"?(?:\.\s*"?[A-Za-z_][\w$#]*"?)?)', token)
            if first:
                tables.add(_norm_ident(first.group(1)))

        while i < n:
            c = code[i]
            if c == "(":
                depth += 1
                item.append(c)
            elif c == ")":
                if depth == 0:
                    break
                depth -= 1
                item.append(c)
            elif c == ";":
                break
            elif c == "," and depth == 0:
                _flush(item)
                item = []
            elif depth == 0 and (c.isspace() or c in _IDENT_CHARS):
                # 到停用词则结束该 FROM 子句
                wm = re.match(r"\s*([A-Za-z_][\w$#]*)", code[i:])
                if wm and wm.group(1).upper() in _FROM_STOP and not item_has_table(item):
                    break
                if wm and wm.group(1).upper() in _FROM_STOP and item_has_table(item):
                    _flush(item)
                    item = []
                    break
                item.append(c)
                i += 1
                continue
            else:
                item.append(c)
            i += 1
        _flush(item)

    # JOIN 表
    for m in re.finditer(r"\bJOIN\s+" + _TABLE_RE, code, re.I):
        tables.add(_norm_ident(m.group(1)))
    tables.discard("DUAL")
    return tables


def item_has_table(item: list[str]) -> bool:
    return bool("".join(item).strip())


# ── 表引用：写（INSERT / UPDATE / DELETE / MERGE）─────────────

def _write_tables(code: str) -> list[dict]:
    hits: dict[tuple[str, str], None] = {}
    for m in re.finditer(r"\bINSERT\s+INTO\s+" + _TABLE_RE, code, re.I):
        hits[(_norm_ident(m.group(1)), "INSERT")] = None
    for m in re.finditer(r"\bMERGE\s+INTO\s+" + _TABLE_RE, code, re.I):
        hits[(_norm_ident(m.group(1)), "MERGE")] = None
    for m in re.finditer(r"\bDELETE\s+(?:FROM\s+)?" + _TABLE_RE, code, re.I):
        hits[(_norm_ident(m.group(1)), "DELETE")] = None
    # UPDATE：排除 "FOR UPDATE" 游标锁定
    for m in re.finditer(r"(?<!for )\bUPDATE\s+" + _TABLE_RE, code, re.I):
        tab = _norm_ident(m.group(1))
        if tab in ("SET", "OF"):
            continue
        hits[(tab, "UPDATE")] = None
    agg: dict[str, set] = {}
    for (tab, op) in hits:
        agg.setdefault(tab, set()).add(op)
    return [{"table": t, "ops": sorted(ops)} for t, ops in sorted(agg.items())]


# ── UPDATE ... SET 列=字面量（状态流转候选）────────────────────

def _set_assignments(code: str) -> list[dict]:
    out: list[dict] = []
    for m in re.finditer(r"(?<!for )\bUPDATE\s+" + _TABLE_RE + r"(.*?)(?=;|\bWHERE\b|$)",
                         code, re.I | re.S):
        tab = _norm_ident(m.group(1))
        body = m.group(2)
        if not re.search(r"\bSET\b", body, re.I):
            continue
        for a in re.finditer(r"([A-Za-z_][\w$#]*)\s*=\s*(?:'([^']*)'|(\d+))", body):
            val = a.group(2) if a.group(2) is not None else a.group(3)
            out.append({"table": tab, "column": a.group(1).upper(), "value": val})
    return out


# ── 调用识别（过程/函数/包）───────────────────────────────────

_BUILTINS = {
    "SUBSTR", "SUBSTRB", "INSTR", "NVL", "NVL2", "COALESCE", "TO_CHAR", "TO_DATE",
    "TO_NUMBER", "TO_TIMESTAMP", "TRIM", "LTRIM", "RTRIM", "UPPER", "LOWER", "INITCAP",
    "LENGTH", "LENGTHB", "DECODE", "COUNT", "SUM", "MAX", "MIN", "AVG", "ROUND", "TRUNC",
    "CEIL", "FLOOR", "MOD", "ABS", "SIGN", "POWER", "SQRT", "GREATEST", "LEAST",
    "REPLACE", "TRANSLATE", "LPAD", "RPAD", "CONCAT", "EXTRACT", "ADD_MONTHS",
    "LAST_DAY", "MONTHS_BETWEEN", "NEXT_DAY", "SYSDATE", "SYSTIMESTAMP", "CURRENT_DATE",
    "ROW_NUMBER", "RANK", "DENSE_RANK", "LEAD", "LAG", "LISTAGG", "REGEXP_REPLACE",
    "REGEXP_SUBSTR", "REGEXP_INSTR", "REGEXP_LIKE", "CAST", "USER", "USERENV", "NULLIF",
    "RATIO_TO_REPORT", "WM_CONCAT",
}
_KEYWORDS = {
    "IF", "ELSIF", "CASE", "WHEN", "WHILE", "LOOP", "FORALL", "FOR", "VALUES", "INTO",
    "AND", "OR", "NOT", "IN", "EXISTS", "RETURN", "OPEN", "FETCH", "CLOSE", "EXIT",
    "SELECT", "FROM", "WHERE", "GROUP", "ORDER", "SET", "UPDATE", "INSERT", "DELETE",
    "MERGE", "BEGIN", "END", "DECLARE", "IS", "AS", "THEN", "ELSE", "NULL", "BY",
    "ON", "USING", "TABLE", "TYPE", "ROWTYPE", "CURSOR", "PRAGMA", "RAISE",
}
# Oracle 数据类型名——出现在变量/参数声明的 类型(长度) 中，非调用
_TYPES = {
    "VARCHAR2", "VARCHAR", "NVARCHAR2", "CHAR", "NCHAR", "NUMBER", "INTEGER", "INT",
    "SMALLINT", "DECIMAL", "DEC", "NUMERIC", "FLOAT", "REAL", "DOUBLE", "BINARY_INTEGER",
    "PLS_INTEGER", "BINARY_FLOAT", "BINARY_DOUBLE", "BOOLEAN", "DATE", "TIMESTAMP",
    "INTERVAL", "CLOB", "NCLOB", "BLOB", "BFILE", "RAW", "LONG", "ROWID", "UROWID",
    "XMLTYPE", "VARRAY", "REF",
}


def _calls(code: str, own_name: str = "") -> list[str]:
    """识别形如 name( 或 pkg.proc( 的调用；排除内置函数与关键字。"""
    # 先剥掉 Oracle 老式外连接算子 列(+)，否则 alias.col(+) 会被误当调用（老库大量使用）
    code = re.sub(r"\(\s*\+\s*\)", " ", code)
    found: set[str] = set()
    for m in re.finditer(r'\b("?[A-Za-z_][\w$#]*"?(?:\.\s*"?[A-Za-z_][\w$#]*"?)?)\s*\(', code):
        name = _norm_ident(m.group(1))
        if "." in name:                       # 包限定调用一律保留（含 DBMS_/UTL_ 等外部 I/O）
            found.add(name)
            continue
        if name in _BUILTINS or name in _KEYWORDS or name in _TYPES:
            continue
        found.add(name)
    found.discard(_norm_ident(own_name))       # 去掉自身声明的括号（签名）
    return sorted(found)


# ── 硬编码 / PII 候选分类（对齐 CLAUDE.md 4.1 / 4.2）──────────

_IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_SITE_RE = re.compile(r"\b[A-Z]{2,}[A-Z0-9]*-[A-Z0-9]+(?:-[A-Z0-9]+)*\b")   # 如 FAB-NJ-01
_CONN_HINT = re.compile(r"(jdbc:|@//|\(HOST=|DESCRIPTION=|SERVICE_NAME=|PORT=)", re.I)
_LONGNUM_RE = re.compile(r"\b\d{6,}\b")


def classify_literal(s: str) -> Optional[str]:
    """把字符串字面量归类为硬编码/PII 候选；返回 None 表示普通字面量（不入清单）"""
    if not s or not s.strip():
        return None
    if _CONN_HINT.search(s):
        return "db_conn"
    if _IP_RE.search(s):
        return "ip"
    if _EMAIL_RE.search(s):
        return "email"
    if _SITE_RE.search(s):
        return "site_code"
    if _LONGNUM_RE.search(s):
        return "long_number"      # 工号/批次号/序列号候选
    return None


def _has_dynamic_sql(code: str) -> bool:
    return bool(re.search(r"\bEXECUTE\s+IMMEDIATE\b|\bDBMS_SQL\b", code, re.I))


_DECL_RE = re.compile(r'\b(?:PROCEDURE|FUNCTION)\s+("?[A-Za-z_][\w$#]*"?)', re.I)


def _declared_name(code: str) -> str:
    """从源码头部识别声明的过程/函数名（用于命名）"""
    m = _DECL_RE.search(code)
    return _norm_ident(m.group(1)) if m else ""


def _declared_names(code: str) -> set:
    """本单元内所有 PROCEDURE/FUNCTION 定义/声明名。
    包体含数十子程序定义、包规格含数十声明，其定义头 `NAME(` 会被误当调用——
    这些名字须从调用中剔除（跨包 PKG.NAME 带点，不受此影响，仍保留为真实调用）。"""
    return {_norm_ident(m.group(1)) for m in _DECL_RE.finditer(code)}


# ── 单元分析 ──────────────────────────────────────────────────

@dataclass
class ProcAnalysis:
    owner: str
    name: str
    object_type: str
    read_tables: list[str] = field(default_factory=list)
    write_tables: list[dict] = field(default_factory=list)
    calls: list[str] = field(default_factory=list)
    set_assignments: list[dict] = field(default_factory=list)
    literals: list[dict] = field(default_factory=list)   # {value, kind}
    has_dynamic_sql: bool = False
    line_count: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


def analyze_source(source: str, owner: str = "", name: str = "",
                   object_type: str = "") -> ProcAnalysis:
    code, raw_literals = split_code(source or "")
    code_with_strings, _ = split_code(source or "", keep_strings=True)
    literals: list[dict] = []
    seen_lit: set[tuple[str, str]] = set()
    for lit in raw_literals:
        kind = classify_literal(lit)
        if kind and (lit, kind) not in seen_lit:
            seen_lit.add((lit, kind))
            literals.append({"value": lit, "kind": kind})

    read = sorted(_from_clause_tables(code))
    writes = _write_tables(code)
    effective_name = _norm_ident(name) if name else _declared_name(code)
    # 表名与本单元内所有子程序定义名不算调用（INSERT INTO T( 及 PROCEDURE/FUNCTION 定义头会被误捕）
    table_names = set(read) | {w["table"] for w in writes}
    own = ({effective_name} | _declared_names(code)) - {""}
    calls = [c for c in _calls(code) if c not in table_names and c not in own]

    return ProcAnalysis(
        owner=owner,
        name=effective_name,
        object_type=object_type,
        read_tables=read,
        write_tables=writes,
        calls=calls,
        set_assignments=_set_assignments(code_with_strings),
        literals=literals,
        has_dynamic_sql=_has_dynamic_sql(code),
        line_count=(source or "").count("\n") + 1 if source else 0,
    )


def analyze_metadata(meta: dict) -> list[ProcAnalysis]:
    owner = meta.get("owner", "")
    out: list[ProcAnalysis] = []
    for u in meta.get("program_units", []):
        src = u.get("source")
        if not src:
            continue
        out.append(analyze_source(src, owner=owner, name=u.get("name", ""),
                                  object_type=u.get("object_type", "")))
    return out


# ── 输出 ──────────────────────────────────────────────────────

def write_edges(analyses: list[ProcAnalysis], path: str) -> None:
    """依赖边 CSV，供 dependency_graph.py 构图"""
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["SRC_OWNER", "SRC_UNIT", "EDGE_TYPE", "TARGET", "DETAIL"])
        for a in analyses:
            for t in a.read_tables:
                w.writerow([a.owner, a.name, "READ", t, ""])
            for wt in a.write_tables:
                w.writerow([a.owner, a.name, "WRITE", wt["table"], "/".join(wt["ops"])])
            for c in a.calls:
                w.writerow([a.owner, a.name, "CALL", c, ""])
    log.info("依赖边已写入：%s", path)


def write_literals(analyses: list[ProcAnalysis], path: str) -> int:
    """硬编码/PII 候选 CSV，供 S5-2 脱敏层与安全审计"""
    rows = 0
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["OWNER", "UNIT", "KIND", "VALUE"])
        for a in analyses:
            for lit in a.literals:
                w.writerow([a.owner, a.name, lit["kind"], lit["value"]])
                rows += 1
    log.info("硬编码/PII 候选已写入：%s（%d 条）", path, rows)
    return rows


def render_report(analyses: list[ProcAnalysis]) -> str:
    total_lit = sum(len(a.literals) for a in analyses)
    dyn = sum(1 for a in analyses if a.has_dynamic_sql)
    lines = [
        "# 存储过程静态分析报告",
        "",
        f"程序单元：**{len(analyses)}** ｜ 硬编码/PII 候选：**{total_lit}** ｜ 含动态 SQL：**{dyn}**",
        "",
        "> 由 `proc_parser.py` 生成（启发式静态分析）。硬编码/PII 候选须交 S5-2 脱敏层与 DBA 复核。",
        "",
    ]
    for a in analyses:
        lines.append(f"## {a.owner}.{a.name}（{a.object_type}，{a.line_count} 行）")
        if a.has_dynamic_sql:
            lines.append("- ⚠️ 含动态 SQL（EXECUTE IMMEDIATE / DBMS_SQL），静态分析不完整")
        lines.append(f"- 读表：{', '.join(a.read_tables) or '—'}")
        lines.append("- 写表：" + (", ".join(f"{w['table']}[{'/'.join(w['ops'])}]"
                                            for w in a.write_tables) or "—"))
        lines.append(f"- 调用：{', '.join(a.calls) or '—'}")
        if a.set_assignments:
            st = ", ".join(f"{s['table']}.{s['column']}={s['value']}" for s in a.set_assignments)
            lines.append(f"- 状态流转候选：{st}")
        if a.literals:
            lt = ", ".join(f"{l['kind']}:`{l['value']}`" for l in a.literals)
            lines.append(f"- 🔒 硬编码/PII 候选：{lt}")
        lines.append("")
    return "\n".join(lines)


# ── 自测样例 ──────────────────────────────────────────────────

_SELF_TEST_SQL = """
PROCEDURE SP_CLOSE_WORKORDER(P_WO_ID IN VARCHAR2) IS
  V_CNT NUMBER;
BEGIN
  -- 统计在制数量（此注释含 FAKE_TABLE 不应被识别为表）
  SELECT COUNT(*) INTO V_CNT
  FROM WO_MASTER a, WO_ROUTE b
  WHERE a.WO_ID = b.WO_ID AND a.WO_ID = P_WO_ID;

  IF FC_YN_TO_BOOLEAN(P_WO_ID) = 1 THEN
    UPDATE WO_MASTER SET WO_STATUS = '90', UPD_TM = SYSDATE
    WHERE WO_ID = P_WO_ID;
    INSERT INTO WO_HISTORY(WO_ID, MEMO) VALUES (P_WO_ID, '关单 IP=192.168.1.100');
    PKG_NOTIFY.SEND(P_WO_ID);
  END IF;
END SP_CLOSE_WORKORDER;
"""


def _run_self_test() -> int:
    a = analyze_source(_SELF_TEST_SQL, owner="MESAPUSER",
                       name="SP_CLOSE_WORKORDER", object_type="PROCEDURE")
    checks = {
        "读表含 WO_MASTER": "WO_MASTER" in a.read_tables,
        "读表含 WO_ROUTE（逗号连接）": "WO_ROUTE" in a.read_tables,
        "注释中的 FAKE_TABLE 未误报": "FAKE_TABLE" not in a.read_tables,
        "写表 WO_MASTER[UPDATE]": any(w["table"] == "WO_MASTER" and "UPDATE" in w["ops"]
                                     for w in a.write_tables),
        "写表 WO_HISTORY[INSERT]": any(w["table"] == "WO_HISTORY" and "INSERT" in w["ops"]
                                      for w in a.write_tables),
        "调用含 FC_YN_TO_BOOLEAN": "FC_YN_TO_BOOLEAN" in a.calls,
        "调用含 PKG_NOTIFY.SEND": "PKG_NOTIFY.SEND" in a.calls,
        "内置 COUNT 未计入调用": "COUNT" not in a.calls,
        "状态流转 WO_STATUS=90": any(s["column"] == "WO_STATUS" and s["value"] == "90"
                                    for s in a.set_assignments),
        "PII 识别 IP 192.168.1.100": any(l["kind"] == "ip" for l in a.literals),
    }
    failed = 0
    for name, ok in checks.items():
        failed += 0 if ok else 1
        print(f"  {'✓' if ok else '✗'} {name}")
    print(f"自测结果：{len(checks) - failed}/{len(checks)} 通过")
    print("--- 分析结果 ---")
    print(json.dumps(a.to_dict(), ensure_ascii=False, indent=2))
    return failed


# ── CLI ───────────────────────────────────────────────────────

def run(args) -> list[ProcAnalysis]:
    if args.self_test:
        raise SystemExit(_run_self_test())

    if args.source_file:
        with open(args.source_file, encoding="utf-8") as f:
            src = f.read()
        # 不用文件名作单元名：让 analyze_source 从源码头部识别声明名
        analyses = [analyze_source(src)]
    elif args.input:
        with open(args.input, encoding="utf-8") as f:
            meta = json.load(f)
        analyses = analyze_metadata(meta)
    else:
        raise SystemExit("请用 --input（自省 JSON）或 --source-file（单个 .sql）指定输入")

    log.info("已分析 %d 个程序单元", len(analyses))
    if args.out_report:
        with open(args.out_report, "w", encoding="utf-8") as f:
            f.write(render_report(analyses))
        log.info("分析报告已写入：%s", args.out_report)
    if args.out_edges:
        write_edges(analyses, args.out_edges)
    if args.out_literals:
        write_literals(analyses, args.out_literals)
    return analyses


def main(argv=None):
    p = argparse.ArgumentParser(description="PL/SQL 存储过程静态分析器")
    p.add_argument("--input", help="db_introspect 产出的元数据 JSON")
    p.add_argument("--source-file", dest="source_file", help="单个 PL/SQL 源码文件")
    p.add_argument("--out-report", dest="out_report", help="分析报告 Markdown")
    p.add_argument("--out-edges", dest="out_edges", help="依赖边 CSV（供 dependency_graph.py）")
    p.add_argument("--out-literals", dest="out_literals", help="硬编码/PII 候选 CSV")
    p.add_argument("--self-test", action="store_true", help="运行内置样例自测")
    run(p.parse_args(argv))


if __name__ == "__main__":
    main()
