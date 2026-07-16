#!/usr/bin/env python3
"""
PL/SQL 子程序「二次切分」器 → 二级训练片段

用途：一级切分器 plsql_splitter.py 把大包体切成顶层子程序单元后，仍会残留少量
     「单个子程序就超上下文/超训练行上限」的超大过程（本库 P1 批为 16 个 >1200 行，
     且**无嵌套子程序**——无法再按子程序边界切）。本工具对这类**扁平巨型子程序**
     做**基于控制流结构的递归二次切分**，产出可训练的二级片段（S3-2 后续补训）。

方法（务实、保覆盖、失败可回退，不丢码）：
  1. 复用 plsql_splitter.mask_code 掩码注释/字符串（长度保留、偏移对齐）；
  2. 剥离「声明段」= 过程签名 + 局部变量/游标/类型（首个顶层 BEGIN 之前），作各片段共享上下文；
  3. 取 BEGIN..END 之间的「可执行体」，按**顶层语句边界**（深度0且括号0处的 `;`）贪心打包
     成 ≤ 行预算 的窗口；
  4. 若单条顶层语句本身超预算（典型：一整棵 IF..ELSIF 分支树 / 一个 LOOP），**递归降级**
     进入其内部块体（IF 的 THEN 体 / LOOP 体 / BEGIN 体）继续按语句边界切；
  5. 无法结构化再切的巨型单语句（如一条 1400 行的 SELECT/INSERT）→ **硬窗口切**（优先空行处），
     并打 hard_cut 标记提示人工复核（失败模式是段偏大/边界不齐，绝不丢码）。

块深度模型（关键）：开块关键字 {BEGIN, IF, LOOP, CASE} 各 +1；每个 END 各 -1（END 后紧跟
  IF/LOOP/CASE 的收尾标签一并消费，不重复计数）。由于 IF↔END IF、LOOP↔END LOOP、
  CASE(语句)↔END CASE、CASE(表达式)↔END、BEGIN↔END 均一开一合，计数天然平衡。

覆盖率保证：所有片段的「本片段语句体」按原始偏移精确切片，拼接 == 可执行体（逐字符校验，
  不满足即抛错）。声明段在每个片段重复出现（共享上下文），不计入覆盖。

用法：
    python plsql_second_split.py --self-test
    python plsql_second_split.py --input split_p1.json --min-lines 1201 \
        --max-lines 1000 --out-json split_p1_l2.json --out-report split_p1_l2_report.md

关联任务：S3-2 存储过程理解 · 超大过程二次切分（REQ-MES-AI-20260716-001 遗留项）
作者：AI（芯智云匠）
日期：2026-07-16
"""

import os
import re
import sys
import json
import argparse
import logging
from dataclasses import dataclass, field, asdict

# 复用一级切分器已充分测试的掩码逻辑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plsql_splitter import mask_code

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# 词法单元：关键字 / 分号 / 括号（在掩码文本上匹配，偏移与原文一一对应）
_TOK = re.compile(
    r"(?P<kw>\b(?:BEGIN|END|IF|LOOP|CASE|THEN)\b)|(?P<semi>;)|(?P<lp>\()|(?P<rp>\))",
    re.I,
)
_OPENERS = {"BEGIN", "IF", "LOOP", "CASE"}


def _line_count(s: str) -> int:
    return s.count("\n") + 1 if s else 0


# ── 词法扫描（返回带偏移的 token 流；END 收尾标签已合并）──────────────
def _tokens(mask: str):
    toks = list(_TOK.finditer(mask))
    out = []
    j = 0
    while j < len(toks):
        m = toks[j]
        g = m.lastgroup
        if g == "kw":
            w = m.group().upper()
            if w == "END":
                # 合并紧随其后的 IF/LOOP/CASE 收尾标签（END IF / END LOOP / END CASE）。
                # 关键：必须**紧邻**（其间仅空白）才合并——否则形如 F(CASE..END, CASE..END)
                # 表达式列表里，前一个 CASE 表达式的裸 END 后面跟着的新 CASE 开块会被误吞，
                # 导致漏计一个 CASE 开块（净 -1，过程体深度失衡 → 截断）。
                consumed_end = m.end()
                if (j + 1 < len(toks) and toks[j + 1].lastgroup == "kw"
                        and toks[j + 1].group().upper() in ("IF", "LOOP", "CASE")
                        and mask[m.end():toks[j + 1].start()].strip() == ""):
                    consumed_end = toks[j + 1].end()
                    j += 1
                out.append(("END", m.start(), consumed_end))
            elif w in _OPENERS:
                out.append((w, m.start(), m.end()))
            elif w == "THEN":
                out.append(("THEN", m.start(), m.end()))
        elif g == "semi":
            out.append((";", m.start(), m.end()))
        elif g == "lp":
            out.append(("(", m.start(), m.end()))
        elif g == "rp":
            out.append((")", m.start(), m.end()))
        j += 1
    return out


def _statement_spans(src: str):
    """把 src 视作一个块体，返回顶层语句的 (start,end) 偏移列表（含结尾 `;`）。
    顶层 = 块深度0 且括号深度0 处的 `;` 作为边界。"""
    mask = mask_code(src)
    toks = _tokens(mask)
    depth = paren = 0
    spans = []
    start = 0
    for (kind, s, e) in toks:
        if kind == "(":
            paren += 1
        elif kind == ")":
            paren = max(0, paren - 1)
        elif kind == "END":
            depth -= 1
        elif kind in _OPENERS:
            depth += 1
        elif kind == ";" and depth == 0 and paren == 0:
            spans.append((start, e))
            start = e
    if start < len(src):
        # 尾段（即使仅空白）也必须保留，保证片段拼接逐字符还原
        spans.append((start, len(src)))
    return spans


def _split_body(src: str):
    """定位过程/块的可执行体：返回 (decl, region, tail)。
    decl = 首个顶层 BEGIN 之前（签名+声明），region = BEGIN..匹配END 之间，tail = END 及之后。
    无顶层 BEGIN 时返回 (None, src, "")（当作纯语句块处理）。"""
    mask = mask_code(src)
    toks = _tokens(mask)
    depth = 0
    body_begin = None
    idx = 0
    for i, (kind, s, e) in enumerate(toks):
        if kind == "BEGIN" and depth == 0:
            body_begin = (s, e)
            idx = i
            break
        if kind == "END":
            depth -= 1
        elif kind in _OPENERS:
            depth += 1
    if body_begin is None:
        return None, src, ""
    decl = src[:body_begin[0]]
    # 关键：过程体内 depth 会在每条顶层语句结束时回到 0；过程的**终结 END** 是
    # **最后一次** depth 回到 0 的那个 END（此后仅剩空白/注释）。取首次归零会把
    # 「首条语句短」的过程从中间截断、把后续代码丢进 tail（曾致 836 行丢失）。
    depth = 1
    body_end = None
    for (kind, s, e) in toks[idx + 1:]:
        if kind in _OPENERS:
            depth += 1
        elif kind == "END":
            depth -= 1
            if depth == 0:
                body_end = (s, e)   # 记录每次归零，循环结束后即为最后一次（终结 END）
    if body_end is None:
        return decl, src[body_begin[1]:], ""
    region = src[body_begin[1]:body_end[0]]
    tail = src[body_end[0]:]
    return decl, region, tail


def _leading_block(src: str):
    """若语句以 IF/LOOP/BEGIN 开头，返回 (prefix, inner, suffix) 用于递归降级：
    prefix=块头（IF..THEN / ..LOOP / BEGIN），inner=内部体，suffix=END..。
    不可降级（CASE / 无开块 / 巨型单 SQL）返回 None。"""
    mask = mask_code(src)
    toks = _tokens(mask)
    if not toks:
        return None
    # 找第一个开块关键字
    first = None
    fi = 0
    for i, (kind, s, e) in enumerate(toks):
        if kind in _OPENERS:
            first = (kind, s, e)
            fi = i
            break
        if kind == ";":
            # 首个 token 就是语句结束（无开块）→ 不可降级
            break
    if first is None:
        return None
    kind, s, e = first
    # 定位块头结束位置
    if kind == "IF":
        # 匹配该 IF 的收尾 THEN（深度回到该 IF 层、括号0）
        depth = 0
        header_end = None
        for (k, ts, te) in toks[fi + 1:]:
            if k == "(":
                continue
            if k in _OPENERS:
                depth += 1
            elif k == "END":
                depth -= 1
            elif k == "THEN" and depth == 0:
                header_end = te
                break
        if header_end is None:
            return None
    else:  # LOOP / BEGIN / CASE(语句)：块头即关键字本身，选择子/循环头并入内部体首片
        header_end = e
    # 匹配该开块的 END
    depth = 1
    end_span = None
    for (k, ts, te) in toks[fi + 1:]:
        if k in _OPENERS:
            depth += 1
        elif k == "END":
            depth -= 1
            if depth == 0:
                end_span = (ts, te)
                break
    if end_span is None:
        return None
    prefix = src[:header_end]
    inner = src[header_end:end_span[0]]
    suffix = src[end_span[0]:]
    if not inner.strip():
        return None
    return prefix, inner, suffix


def _hard_split(src: str, max_lines: int):
    """结构化无法再切时的兜底：按行硬切成 ≤max_lines 的窗口，优先在窗口尾部空行处断。
    返回精确切片列表（拼接==src）。"""
    lines = src.splitlines(keepends=True)
    segs = []
    i = 0
    n = len(lines)
    while i < n:
        hi = min(i + max_lines, n)
        cut = hi
        if hi < n:
            # 在窗口后 20% 内找空行断点，使片段更自洽
            lo = i + int(max_lines * 0.8)
            for k in range(hi - 1, max(lo, i + 1), -1):
                if not lines[k].strip():
                    cut = k + 1
                    break
        segs.append("".join(lines[i:cut]))
        i = cut
    return segs


def chunk_region(src: str, max_lines: int, depth: int = 0):
    """把一个块体按顶层语句贪心打包成 ≤max_lines 的片段；超大语句递归降级。
    返回 (segments, hard_flags)：segments 为原文精确切片，拼接==src。"""
    if _line_count(src) <= max_lines or depth > 12:
        if _line_count(src) <= max_lines:
            return [src], [False]
        # 深度兜底：硬切
        segs = _hard_split(src, max_lines)
        return segs, [True] * len(segs)

    spans = _statement_spans(src)
    if len(spans) <= 1:
        # 单条超大语句 → 尝试降级进内部块
        blk = _leading_block(src)
        if blk is None:
            segs = _hard_split(src, max_lines)
            return segs, [True] * len(segs)
        prefix, inner, suffix = blk
        inner_segs, inner_hard = chunk_region(inner, max_lines, depth + 1)
        # 块头并入首片、块尾并入末片，保持逐字符拼接
        inner_segs[0] = prefix + inner_segs[0]
        inner_segs[-1] = inner_segs[-1] + suffix
        return inner_segs, inner_hard

    segments, hard_flags = [], []
    cur = ""
    for (s, e) in spans:
        stmt = src[s:e]
        sl = _line_count(stmt)
        if sl > max_lines:
            if cur:
                segments.append(cur); hard_flags.append(False); cur = ""
            sub, subh = chunk_region(stmt, max_lines, depth + 1)
            segments.extend(sub); hard_flags.extend(subh)
            continue
        if cur and _line_count(cur) + sl > max_lines:
            segments.append(cur); hard_flags.append(False); cur = ""
        cur += stmt
    if cur:
        segments.append(cur); hard_flags.append(False)
    return segments, hard_flags


# ── 单元级二次切分 ────────────────────────────────────────────
@dataclass
class L2Unit:
    package: str
    name: str            # 形如 PR_XXX#p03
    parent: str          # 原子程序名
    kind: str
    part: int
    part_total: int
    start_line: int      # 本片段语句体在原过程中的起始行（绝对）
    seg_lines: int       # 本片段语句体行数（不含声明段）
    line_count: int      # 训练卡实际行数（声明段+说明+语句体）
    hard_cut: bool
    source: str          # 训练用完整片段文本（含共享声明段）
    l2: bool = True

    def to_dict(self):
        return asdict(self)


def _note(parent, part, total, hard):
    tag = "（含硬切边界，可能不在语句边界，理解时容忍段首/段尾不完整）" if hard else ""
    return (f"-- 【二次切分片段 {part}/{total}｜父过程 {parent}】"
            f"以下为「共享声明段」+「本片段语句体」；整体职责见同父其它片段{tag}\n")


def second_split_unit(unit: dict, max_lines: int):
    """对一个超大子程序单元做二次切分，返回 L2Unit 列表。"""
    src = unit["source"]
    pkg = unit["package"]
    parent = unit["name"]
    kind = unit.get("kind", "PROCEDURE")
    base_line = unit.get("start_line", 1)

    decl, region, tail = _split_body(src)
    decl = decl or ""
    decl_lines = _line_count(decl) if decl.strip() else 0
    # 语句体直接切到 max_lines；声明段作为共享上下文另行附加（重复出现、不计预算）。
    # 训练卡输入行数 ≈ 语句体 + 声明段，仍在模型上下文内；输出 token 由 proc_max_tokens 另控。
    segs, hard = chunk_region(region, max_lines)

    # 覆盖率校验①：片段语句体拼接必须逐字符等于可执行体
    if "".join(segs) != region:
        raise AssertionError(f"{pkg}.{parent} 二次切分覆盖率校验失败（拼接≠原体）")
    # 覆盖率校验②：tail 只能是「终结 END + 空白/注释」，不得含被丢弃的实质语句
    #（防 _split_body 截断把真实代码丢进 tail——曾致 TITLE 丢 836 行的静默 bug）
    tail_mask = mask_code(tail or "")
    tail_body = re.sub(r'^\s*END\b[^\n;]*;?', '', tail_mask, count=1, flags=re.I)
    if tail_body.strip():
        raise AssertionError(
            f"{pkg}.{parent} tail 含未覆盖代码（疑似过程体被截断）：{repr((tail or '')[:120])}")

    # 计算每片段起始绝对行（decl 行数 + 之前片段累计行）
    region_start_line = base_line + decl_lines  # region 在原过程中的起始行（近似）
    total = len(segs)
    out = []
    consumed = 0  # region 内已消费行数
    for i, (seg, hc) in enumerate(zip(segs, hard), 1):
        note = _note(parent, i, total, hc)
        head = decl.rstrip() + "\n" if decl.strip() else ""
        full = f"{note}{head}{seg}"
        out.append(L2Unit(
            package=pkg,
            name=f"{parent}#p{i:02d}",
            parent=parent,
            kind=kind,
            part=i,
            part_total=total,
            start_line=region_start_line + consumed,
            seg_lines=_line_count(seg),
            line_count=_line_count(full),
            hard_cut=hc,
            source=full,
        ).to_dict())
        consumed += seg.count("\n")
    return out


def second_split_metadata(split_meta: dict, min_lines: int, max_lines: int):
    """遍历一级切分结果，对所有 >min_lines-1（即 ≥min_lines）的子程序做二次切分。"""
    owner = split_meta.get("owner", "")
    by_pkg = {}
    stats = []
    for pkg in split_meta.get("packages", []):
        for u in pkg.get("units", []):
            if u.get("kind") not in ("PROCEDURE", "FUNCTION"):
                continue
            if u.get("line_count", 0) < min_lines:
                continue
            l2units = second_split_unit(u, max_lines)
            by_pkg.setdefault(u["package"], []).extend(l2units)
            hard = sum(1 for x in l2units if x["hard_cut"])
            stats.append({
                "unit": f'{u["package"]}.{u["name"]}',
                "orig_lines": u["line_count"],
                "parts": len(l2units),
                "hard_cuts": hard,
                "max_part_lines": max((x["seg_lines"] for x in l2units), default=0),
            })
    packages = [{"package": p, "units": us} for p, us in by_pkg.items()]
    return {"owner": owner, "l2": True, "packages": packages}, stats


def render_report(stats, min_lines, max_lines):
    tot_parts = sum(s["parts"] for s in stats)
    tot_hard = sum(s["hard_cuts"] for s in stats)
    L = [f"# 超大过程二次切分报告",
         "",
         f"源阈值 ≥{min_lines} 行 ｜ 片段行预算 ≤{max_lines} 行 ｜ "
         f"输入超大过程 **{len(stats)}** 个 → 二级片段 **{tot_parts}** 个 ｜ 硬切片段 {tot_hard}",
         "",
         "> 由 `plsql_second_split.py` 生成。每个二级片段 = 共享声明段 + 一段语句体，"
         "拼接逐字符还原原过程可执行体（已断言）。hard_cut=按行硬切、边界可能不齐，需理解时容忍。",
         "",
         "| 父过程 | 原行数 | 片段数 | 最大片段行 | 硬切 |",
         "|--------|-------:|------:|----------:|-----:|"]
    for s in sorted(stats, key=lambda x: -x["orig_lines"]):
        L.append(f"| {s['unit']} | {s['orig_lines']} | {s['parts']} | "
                 f"{s['max_part_lines']} | {s['hard_cuts'] or ''} |")
    L.append("")
    return "\n".join(L)


# ── 自测 ──────────────────────────────────────────────────────
_ST_BLOCKS = """PROCEDURE PR_BLK IS
  V_X NUMBER;
BEGIN
  BEGIN
    INSERT INTO T1 VALUES(1);
    INSERT INTO T1 VALUES(2);
  END;
  BEGIN
    UPDATE T2 SET A=1;
    UPDATE T2 SET A=2;
  END;
  OTHER.CALL(V_X);
END PR_BLK;
"""

_ST_IF = """PROCEDURE PR_IF(P IN VARCHAR2, C OUT SYS_REFCURSOR) IS
BEGIN
  IF P = 'A' THEN
    OPEN C FOR SELECT 1 FROM DUAL;
    OPEN C FOR SELECT 2 FROM DUAL;
  ELSIF P = 'B' THEN
    OPEN C FOR SELECT 3 FROM DUAL;
    OPEN C FOR SELECT 4 FROM DUAL;
  ELSE
    OPEN C FOR SELECT 5 FROM DUAL;
  END IF;
END PR_IF;
"""


def _run_self_test() -> int:
    checks = {}

    # 1) 块结构：小预算下按顶层 BEGIN 块打包，覆盖率精确
    decl1, region1, _ = _split_body(_ST_BLOCKS)
    segs1, hard1 = chunk_region(region1, 5)
    u1 = {"package": "PKG", "name": "PR_BLK", "kind": "PROCEDURE",
          "line_count": _line_count(_ST_BLOCKS), "source": _ST_BLOCKS, "start_line": 1}
    l1 = second_split_unit(u1, max_lines=5)
    checks["块结构：多片段"] = len(segs1) >= 2
    checks["块结构：语句体拼接还原"] = "".join(segs1) == region1
    checks["块结构：每片段≤预算"] = all(_line_count(s) <= 5 for s in segs1)
    checks["块结构：无硬切"] = not any(hard1)
    checks["块结构：单元装配含声明段"] = all(decl1.strip().splitlines()[0] in x["source"] for x in l1)

    # 2) IF 降级：整棵 IF 是单条顶层语句 → 递归进 THEN 体切分
    u2 = {"package": "PKG", "name": "PR_IF", "kind": "PROCEDURE",
          "line_count": _line_count(_ST_IF), "source": _ST_IF, "start_line": 1}
    l2 = second_split_unit(u2, max_lines=4)
    decl2, region2, _ = _split_body(_ST_IF)
    segs2, _ = chunk_region(region2, 4)
    checks["IF降级：拆出多片段"] = len(l2) >= 2
    checks["IF降级：覆盖率精确"] = "".join(segs2) == region2
    checks["IF降级：非全硬切"] = any(not x["hard_cut"] for x in l2)

    # 3) 硬切兜底：一条无法结构化的巨型单语句
    giant = "PROCEDURE PR_G IS\nBEGIN\n" + "SELECT " + ",\n".join(f"C{i}" for i in range(60)) + " INTO V FROM DUAL;\nEND PR_G;\n"
    _, gregion, _ = _split_body(giant)
    gsegs, ghard = chunk_region(gregion, 20)
    checks["硬切：产生片段"] = len(gsegs) >= 2
    checks["硬切：标记 hard_cut"] = any(ghard)
    checks["硬切：覆盖率精确"] = "".join(gsegs) == gregion

    # 4) 深度平衡：statement_spans 对含 END IF/END LOOP/CASE END 不错乱
    mixed = ("x1;\n"
             "IF a THEN b; END IF;\n"
             "FOR i IN 1..9 LOOP c; END LOOP;\n"
             "y := CASE WHEN a THEN 1 ELSE 2 END;\n"
             "z1;\n")
    spans = _statement_spans(mixed)
    nonblank = [(s, e) for (s, e) in spans if mixed[s:e].strip()]
    checks["深度平衡：5 条顶层语句"] = len(nonblank) == 5
    checks["深度平衡：拼接还原"] = "".join(mixed[s:e] for (s, e) in spans) == mixed

    # 5) 截断防护：过程体首条语句很短（IF..END IF;），其后仍有大量代码，
    #    _split_body 必须取「终结 END」而非首次归零，否则后续代码被丢进 tail
    trunc = ("PROCEDURE PR_T IS\n  V NUMBER;\nBEGIN\n"
             "  IF A THEN NULL; END IF;\n"        # 短首语句，此处 depth 首次归零
             "  V := 1;\n  V := 2;\n  INSERT INTO T VALUES(V);\n"
             "END PR_T;\n")
    dT, regT, tailT = _split_body(trunc)
    checks["截断防护：region 含末条 INSERT"] = "INSERT INTO T" in regT
    checks["截断防护：tail 仅终结 END"] = tailT.strip().upper().startswith("END PR_T")
    # 全过程可通过 second_split_unit 且不触发 tail 断言
    try:
        second_split_unit({"package": "PKG", "name": "PR_T", "kind": "PROCEDURE",
                           "line_count": _line_count(trunc), "source": trunc,
                           "start_line": 1}, max_lines=3)
        checks["截断防护：单元装配不抛错"] = True
    except AssertionError:
        checks["截断防护：单元装配不抛错"] = False

    # 6) CASE 语句降级：整条 CASE..END CASE 作单条超大语句时应能进 WHEN 臂切分
    case_src = ("CASE X\n"
                + "".join(f"  WHEN {i} THEN S{i}A; S{i}B;\n" for i in range(6))
                + "END CASE;\n")
    csegs, chard = chunk_region(case_src, 3)
    checks["CASE降级：拆多片段"] = len(csegs) >= 2
    checks["CASE降级：覆盖率精确"] = "".join(csegs) == case_src
    checks["CASE降级：非全硬切"] = not all(chard)

    # 7) CASE 表达式列表：裸 END 后紧跟逗号+新 CASE，不得误吞开块（深度须平衡）
    expr = ("s0;\n"
            "X := F(CASE WHEN a THEN 1 END, CASE WHEN b THEN 2 END);\n"
            "s1;\n")
    espans = _statement_spans(expr)
    enb = [(s, e) for (s, e) in espans if expr[s:e].strip()]
    checks["CASE表达式列表：3 条顶层语句"] = len(enb) == 3
    # 相邻 END CASE（语句）仍应正确合并、深度平衡
    stmt_case = "s0;\nCASE x WHEN 1 THEN a; END CASE;\ns1;\n"
    snb = [(s, e) for (s, e) in _statement_spans(stmt_case) if stmt_case[s:e].strip()]
    checks["END CASE 语句：3 条顶层语句"] = len(snb) == 3

    failed = sum(0 if ok else 1 for ok in checks.values())
    for n, ok in checks.items():
        print(f"  {'✓' if ok else '✗'} {n}")
    print(f"自测：{len(checks) - failed}/{len(checks)} 通过")
    return failed


def main(argv=None):
    p = argparse.ArgumentParser(description="PL/SQL 超大子程序二次切分器")
    p.add_argument("--input", help="plsql_splitter 产出的一级切分 JSON")
    p.add_argument("--min-lines", type=int, default=1201,
                   help="仅对 ≥ 此行数的子程序做二次切分（默认 1201，即 >1200）")
    p.add_argument("--max-lines", type=int, default=1000,
                   help="每个二级片段语句体的行预算")
    p.add_argument("--out-json", dest="out_json")
    p.add_argument("--out-report", dest="out_report")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)

    if args.self_test:
        raise SystemExit(_run_self_test())
    if not args.input:
        raise SystemExit("请用 --input 指定一级切分 JSON")
    with open(args.input, encoding="utf-8") as f:
        meta = json.load(f)
    result, stats = second_split_metadata(meta, args.min_lines, args.max_lines)
    tot = sum(s["parts"] for s in stats)
    log.info("二次切分：%d 个超大过程 → %d 个二级片段（硬切 %d）",
             len(stats), tot, sum(s["hard_cuts"] for s in stats))
    if args.out_json:
        with open(args.out_json, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        log.info("二级切分结果已写入：%s", args.out_json)
    if args.out_report:
        with open(args.out_report, "w", encoding="utf-8") as f:
            f.write(render_report(stats, args.min_lines, args.max_lines))
        log.info("二次切分报告已写入：%s", args.out_report)


if __name__ == "__main__":
    main()
