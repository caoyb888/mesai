#!/usr/bin/env python3
"""
PL/SQL 包体子程序切分器 → 训练单元

用途：把大包体（>数千行，超 AI 上下文）按顶层 PROCEDURE/FUNCTION 切成独立子程序单元，
     每个子程序 + 包级声明（共享上下文）= 一个可训练理解单元（S3-0 T3-0-4 / 喂 S3-2）。

方法（务实启发式，针对本库主流写法「命名闭合 END 子程序名;」）：
  1. 长度保留掩码：剥离注释与字符串（替为空格、保留换行与偏移），避免其中关键字干扰匹配；
  2. 顶层子程序 = `PROCEDURE|FUNCTION 名` 头 ↔ 首个 `END 同名;`（名字配对，天然跳过嵌套）；
  3. 前向声明（签名后紧跟 `;`、无 IS/AS）跳过；命名 END 缺失时回退到「下一个顶层头之前」；
  4. 包级声明段（首个子程序前的变量/常量/游标）单独抽出，作各子程序的共享上下文。

已知边界：极端不规范嵌套/裸 END 密集的包，切分可能不精确 → 报告标注 fallback 段供人工复核。

用法：
    python plsql_splitter.py --self-test
    python plsql_splitter.py --input meta_p0.json --min-lines 5000 \
        --out-json split_units.json --out-report split_report.md

关联任务：S3-0 T3-0-4 大包子程序级切分（AI-MES-S3PLAN-2026-001）
作者：AI（芯智云匠）
日期：2026-07-06
"""

import os
import re
import sys
import json
import argparse
import logging
from dataclasses import dataclass, field, asdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

_QUOTE_CLOSE = {"(": ")", "[": "]", "{": "}", "<": ">"}
_IDENT = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$#")


def mask_code(src: str) -> str:
    """返回与 src 等长的掩码：注释与字符串内容替为空格（保留换行），代码原样。
    用于在'干净'文本上定位关键字，同时按偏移切回原始源码。"""
    out = []
    i, n = 0, len(src)

    def prev_nonspace():
        for ch in reversed(out):
            if not ch.isspace():
                return ch
        return ""

    while i < n:
        c = src[i]
        nx = src[i + 1] if i + 1 < n else ""
        if c == "-" and nx == "-":
            while i < n and src[i] != "\n":
                out.append(" "); i += 1
        elif c == "/" and nx == "*":
            while i < n and not (src[i] == "*" and i + 1 < n and src[i + 1] == "/"):
                out.append("\n" if src[i] == "\n" else " "); i += 1
            if i < n:
                out.append(" "); out.append(" "); i += 2       # 掩掉 */
        elif c in "qQ" and nx == "'" and prev_nonspace() not in _IDENT:
            od = src[i + 2] if i + 2 < n else ""
            cd = _QUOTE_CLOSE.get(od, od)
            out.append(" "); out.append(" "); out.append(" "); j = i + 3
            while j < n and not (src[j] == cd and j + 1 < n and src[j + 1] == "'"):
                out.append("\n" if src[j] == "\n" else " "); j += 1
            out.append(" "); out.append(" "); i = j + 2
        elif c == "'":
            out.append(" "); j = i + 1
            while j < n:
                if src[j] == "'":
                    if j + 1 < n and src[j + 1] == "'":
                        out.append(" "); out.append(" "); j += 2; continue
                    break
                out.append("\n" if src[j] == "\n" else " "); j += 1
            out.append(" "); i = j + 1
        else:
            out.append(c); i += 1
    return "".join(out)


@dataclass
class SubUnit:
    package: str
    name: str
    kind: str                 # PROCEDURE / FUNCTION / PREAMBLE
    start_line: int
    line_count: int
    source: str
    fallback: bool = False    # 未按命名 END 精确闭合、回退到下一头

    def to_dict(self):
        return asdict(self)


_HDR_RE = re.compile(r'\b(PROCEDURE|FUNCTION)\s+"?([A-Za-z_][\w$#]*)"?', re.I)
_BODY_RE = re.compile(r'\bPACKAGE\s+BODY\s+"?[A-Za-z_][\w$#]*"?\s+(?:AS|IS)\b', re.I)


def _is_definition(mask: str, header_end: int) -> bool:
    """定义（后接 IS/AS）返回 True；前向声明（先遇到 ;）返回 False"""
    m_semi = mask.find(";", header_end)
    m_is = re.search(r'\b(IS|AS)\b', mask[header_end:header_end + 8000], re.I)
    is_pos = header_end + m_is.start() if m_is else -1
    if m_semi == -1:
        return is_pos != -1
    if is_pos == -1:
        return False
    return is_pos < m_semi


def split_package_body(src: str, package: str = "") -> list[SubUnit]:
    mask = mask_code(src)
    bm = _BODY_RE.search(mask)
    body_start = bm.end() if bm else 0

    headers = []          # (start, header_end, name, kind)
    for m in _HDR_RE.finditer(mask):
        if m.start() < body_start:
            continue
        if not _is_definition(mask, m.end()):
            continue      # 前向声明，跳过
        headers.append((m.start(), m.end(), m.group(2).upper(), m.group(1).upper()))

    # 每个头找命名 END
    ends = []
    for (st, he, name, kind) in headers:
        em = re.search(r'\bEND\s+"?' + re.escape(name) + r'"?\s*;', mask[he:], re.I)
        ends.append(he + em.end() if em else None)

    # 顶层扫描（跳过被包含的嵌套头）
    tops = []
    cur_end = -1
    for i, (st, he, name, kind) in enumerate(headers):
        if st < cur_end:
            continue
        end = ends[i]
        fallback = end is None
        if fallback:
            end = headers[i + 1][0] if i + 1 < len(headers) else len(src)
        tops.append((st, end, name, kind, fallback))
        cur_end = end

    units: list[SubUnit] = []
    # 包级声明（preamble）
    first = tops[0][0] if tops else len(src)
    pre = src[body_start:first].strip()
    if pre:
        units.append(SubUnit(package, package, "PREAMBLE",
                             src[:body_start].count("\n") + 1,
                             pre.count("\n") + 1, pre))
    for (st, end, name, kind, fb) in tops:
        seg = src[st:end]
        units.append(SubUnit(package, name, kind, src[:st].count("\n") + 1,
                             seg.count("\n") + 1, seg, fallback=fb))
    return units


# ── 批处理入口 ────────────────────────────────────────────────

def split_metadata(meta: dict, min_lines: int = 0) -> dict:
    owner = meta.get("owner", "")
    out = {"owner": owner, "packages": []}
    for u in meta.get("program_units", []):
        if u.get("object_type") != "PACKAGE BODY" or not u.get("source"):
            continue
        if (u["source"].count("\n") + 1) < min_lines:
            continue
        subs = split_package_body(u["source"], package=u["name"])
        out["packages"].append({
            "package": u["name"],
            "total_lines": u["source"].count("\n") + 1,
            "unit_count": sum(1 for s in subs if s.kind != "PREAMBLE"),
            "units": [s.to_dict() for s in subs],
        })
    return out


def render_report(result: dict) -> str:
    pkgs = result["packages"]
    tot_units = sum(p["unit_count"] for p in pkgs)
    fb = sum(1 for p in pkgs for s in p["units"] if s.get("fallback"))
    L = [f"# 大包子程序切分报告（owner={result['owner']}）", "",
         f"包 **{len(pkgs)}** ｜ 切出子程序单元 **{tot_units}** ｜ 回退段 {fb}", "",
         "> 由 `plsql_splitter.py` 生成。每个子程序 + 包级 PREAMBLE = 一个训练理解单元。", "",
         "| 包 | 总行 | 子程序数 | 最大子程序行 | 回退 |",
         "|----|------|---------|-------------|------|"]
    for p in sorted(pkgs, key=lambda x: x["total_lines"], reverse=True):
        subs = [s for s in p["units"] if s["kind"] != "PREAMBLE"]
        mx = max((s["line_count"] for s in subs), default=0)
        pfb = sum(1 for s in p["units"] if s.get("fallback"))
        L.append(f"| {p['package']} | {p['total_lines']} | {p['unit_count']} | {mx} | {pfb or ''} |")
    L.append("")
    return "\n".join(L)


# ── 自测 ──────────────────────────────────────────────────────

_SELF_TEST = """PACKAGE BODY PKG AS
  G_VAR NUMBER := 0;   -- 包级声明
  CURSOR C_ALL IS SELECT 1 FROM DUAL;
  PROCEDURE PR_FWD(A NUMBER);          -- 前向声明，应跳过
  PROCEDURE PR_ONE(A NUMBER) IS
  BEGIN
    IF A > 0 THEN G_VAR := 1; END IF;   -- END IF 不算子程序结束
    OTHER_PKG.DO(A);
  END PR_ONE;
  FUNCTION FN_TWO RETURN NUMBER IS
    PROCEDURE NESTED IS BEGIN NULL; END NESTED;  -- 嵌套，不算顶层
  BEGIN
    NESTED();
    RETURN G_VAR;
  END FN_TWO;
END PKG;
"""


def _run_self_test() -> int:
    units = split_package_body(_SELF_TEST, package="PKG")
    kinds = {(u.name, u.kind) for u in units}
    names = {u.name for u in units if u.kind != "PREAMBLE"}
    checks = {
        "有包级 PREAMBLE": ("PKG", "PREAMBLE") in kinds,
        "PREAMBLE 含 G_VAR": any(u.kind == "PREAMBLE" and "G_VAR" in u.source for u in units),
        "顶层 PR_ONE": "PR_ONE" in names,
        "顶层 FN_TWO": "FN_TWO" in names,
        "嵌套 NESTED 不算顶层": "NESTED" not in names,
        "前向声明 PR_FWD 不算单元": "PR_FWD" not in names,
        "顶层子程序恰 2 个": len(names) == 2,
        "PR_ONE 完整闭合": any(u.name == "PR_ONE" and u.source.rstrip().endswith("END PR_ONE;")
                              for u in units),
        "FN_TWO 含嵌套体": any(u.name == "FN_TWO" and "NESTED" in u.source for u in units),
    }
    failed = sum(0 if ok else 1 for ok in checks.values())
    for n, ok in checks.items():
        print(f"  {'✓' if ok else '✗'} {n}")
    print(f"自测：{len(checks) - failed}/{len(checks)} 通过")
    return failed


def main(argv=None):
    p = argparse.ArgumentParser(description="PL/SQL 包体子程序切分器")
    p.add_argument("--input", help="db_introspect 产出的元数据 JSON（含包体源码）")
    p.add_argument("--min-lines", type=int, default=0, help="仅切分总行数 ≥ 此值的包")
    p.add_argument("--out-json", dest="out_json", help="切分结果 JSON")
    p.add_argument("--out-report", dest="out_report", help="切分报告 Markdown")
    p.add_argument("--self-test", action="store_true", help="假数据自测")
    args = p.parse_args(argv)

    if args.self_test:
        raise SystemExit(_run_self_test())
    if not args.input:
        raise SystemExit("请用 --input 指定元数据 JSON")
    with open(args.input, encoding="utf-8") as f:
        meta = json.load(f)
    result = split_metadata(meta, min_lines=args.min_lines)
    tot = sum(p["unit_count"] for p in result["packages"])
    log.info("切分 %d 个包 → %d 个子程序单元", len(result["packages"]), tot)
    if args.out_json:
        with open(args.out_json, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        log.info("切分结果已写入：%s", args.out_json)
    if args.out_report:
        with open(args.out_report, "w", encoding="utf-8") as f:
            f.write(render_report(result))
        log.info("切分报告已写入：%s", args.out_report)


if __name__ == "__main__":
    main()
