#!/usr/bin/env python3
"""
存储过程依赖图谱 → 核心资产分级（P0/P1/P2）

用途：消费 proc_parser.py 产出的依赖边 CSV（可多份：MESAPUSER + SCOAPUSER），
     构建两张图并计算指标，产出【P0 核心资产集】，作为分批理解训练与 Token 预算控制依据：
       · 过程 → 表     （READ / WRITE 边）——识别高被引表、状态承载表（写入密集）
       · 过程 → 过程   （CALL 边）        ——识别入口过程、枢纽过程、调用环

分级思路（可解释、可测试）：
  · 表评分   = 被读过程数 + 2 × 被写过程数（写入权重更高：状态承载表更核心）
  · 过程评分 = 读表数 + 3 × 写表数 + 调用数 + 入口加权
  · 按评分降序分位：Top p0 → P0，其后 p1 → P1，其余 P2
  · 过程 P0 兜底：入口过程（无人调用且有实际动作）∪ 写入任一 P0 表的过程

入口过程（entry-point）：调用入度为 0（无其它过程调用它）且自身有读/写/调用动作，
                       通常是顶层业务操作（触发器、对外接口过程），优先训练理解。

用法：
    python dependency_graph.py --self-test
    python dependency_graph.py --edges proc_edges_mesapuser.csv proc_edges_scoapuser.csv \
        --units metadata_mesapuser.json \
        --out-report core_assets.md --out-tables tables.csv --out-procs procs.csv

关联任务：S2.9-4 存储过程提取与依赖图谱（AI-MES-PLAN-ADJ-2026-001）
作者：AI（芯智云匠）
日期：2026-07-06
"""

import os
import sys
import csv
import json
import math
import argparse
import logging
from dataclasses import dataclass, field
from typing import Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

TIER_P0, TIER_P1, TIER_P2 = "P0", "P1", "P2"


# ── 节点模型 ──────────────────────────────────────────────────

@dataclass
class TableNode:
    name: str
    read_by: set = field(default_factory=set)     # 读它的过程 key
    written_by: set = field(default_factory=set)   # 写它的过程 key
    ops: set = field(default_factory=set)          # INSERT/UPDATE/DELETE/MERGE
    tier: str = TIER_P2

    @property
    def read_procs(self) -> int:
        return len(self.read_by)

    @property
    def write_procs(self) -> int:
        return len(self.written_by)

    @property
    def score(self) -> int:
        return self.read_procs + 2 * self.write_procs


@dataclass
class ProcNode:
    owner: str
    name: str
    reads: set = field(default_factory=set)        # 读的表
    writes: set = field(default_factory=set)       # 写的表
    calls: set = field(default_factory=set)        # 调用的过程 key（已解析）
    called_by: set = field(default_factory=set)    # 调用它的过程 key
    inferred: bool = False                          # 仅因被调用而推断出的节点（无自身分析）
    tier: str = TIER_P2

    @property
    def key(self) -> str:
        return f"{self.owner}.{self.name}"

    @property
    def is_entry(self) -> bool:
        has_action = bool(self.reads or self.writes or self.calls)
        return has_action and len(self.called_by) == 0

    @property
    def score(self) -> int:
        return (len(self.reads) + 3 * len(self.writes) + len(self.calls)
                + (2 if self.is_entry else 0))


# ── 依赖图 ────────────────────────────────────────────────────

class DependencyGraph:
    def __init__(self):
        self.procs: dict[str, ProcNode] = {}
        self.tables: dict[str, TableNode] = {}
        self._raw_calls: list[tuple[str, str]] = []   # (caller_key, target_str) 延迟解析
        self.external_calls: set[str] = set()          # 未能解析到已知单元的调用

    # -- 注册 --------------------------------------------------
    def register_unit(self, owner: str, name: str, inferred: bool = False) -> ProcNode:
        key = f"{owner}.{_norm(name)}"
        node = self.procs.get(key)
        if node is None:
            node = ProcNode(owner=owner, name=_norm(name), inferred=inferred)
            self.procs[key] = node
        elif not inferred:
            node.inferred = False       # 已有推断节点被真实单元覆盖
        return node

    def _table(self, name: str) -> TableNode:
        name = _norm(name)
        t = self.tables.get(name)
        if t is None:
            t = TableNode(name=name)
            self.tables[name] = t
        return t

    def add_edge(self, src_owner: str, src_unit: str, etype: str, target: str, detail: str = ""):
        caller = self.register_unit(src_owner, src_unit)
        etype = etype.upper()
        if etype == "READ":
            t = self._table(target)
            t.read_by.add(caller.key)
            caller.reads.add(t.name)
        elif etype == "WRITE":
            t = self._table(target)
            t.written_by.add(caller.key)
            caller.writes.add(t.name)
            for op in (detail or "").split("/"):
                if op:
                    t.ops.add(op)
        elif etype == "CALL":
            self._raw_calls.append((caller.key, _norm(target)))

    # -- 解析调用并计算入度 ------------------------------------
    def finalize(self):
        name_index: dict[str, list[str]] = {}
        for key, node in self.procs.items():
            name_index.setdefault(node.name, []).append(key)

        for caller_key, target in self._raw_calls:
            resolved = self._resolve_call(caller_key, target, name_index)
            self.procs[caller_key].calls.add(resolved)
            self.procs[resolved].called_by.add(caller_key)

    def _resolve_call(self, caller_key: str, target: str, name_index: dict) -> str:
        caller_owner = caller_key.rsplit(".", 1)[0]
        pkg = target.split(".")[0] if "." in target else None
        bare = target.split(".")[-1]
        for cand in ([pkg] if pkg else []) + [bare, target]:
            key = f"{caller_owner}.{cand}"
            if key in self.procs:
                return key
            if cand in name_index:               # 跨 owner 按名匹配
                return name_index[cand][0]
        # 未解析 → 建推断节点（包名优先），归属调用方 owner
        self.external_calls.add(target)
        node = self.register_unit(caller_owner, pkg or bare, inferred=True)
        name_index.setdefault(node.name, []).append(node.key)
        return node.key

    # -- 分级 --------------------------------------------------
    def assign_tiers(self, p0: float = 0.1, p1: float = 0.3):
        _tier_by_percentile(sorted(self.tables.values(), key=lambda t: t.score, reverse=True),
                            p0, p1)
        p0_tables = {t.name for t in self.tables.values() if t.tier == TIER_P0}
        procs_sorted = sorted(self.procs.values(), key=lambda p: p.score, reverse=True)
        _tier_by_percentile(procs_sorted, p0, p1)
        # 过程 P0 兜底：入口且有写/编排调用的顶层操作 ∪ 写入任一 P0 表的过程
        # （纯只读入口不强制 P0，交由分位数排名，避免报表类过程膨胀 P0）
        for p in self.procs.values():
            if (p.is_entry and (p.writes or p.calls)) or (p.writes & p0_tables):
                p.tier = TIER_P0

    # -- 环检测（过程调用图）----------------------------------
    def find_cycles(self) -> list[list[str]]:
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {k: WHITE for k in self.procs}
        cycles: list[list[str]] = []
        stack: list[str] = []

        def dfs(u: str):
            color[u] = GRAY
            stack.append(u)
            for v in sorted(self.procs[u].calls):
                if color.get(v, BLACK) == GRAY:      # 回边 → 环
                    if v in stack:
                        cycles.append(stack[stack.index(v):] + [v])
                elif color.get(v) == WHITE:
                    dfs(v)
            stack.pop()
            color[u] = BLACK

        for k in sorted(self.procs):
            if color[k] == WHITE:
                dfs(k)
        return cycles


def _norm(s: str) -> str:
    return (s or "").replace('"', "").strip().upper()


def _tier_by_percentile(nodes_desc: list, p0: float, p1: float):
    n = len(nodes_desc)
    if n == 0:
        return
    p0_cut = max(1, math.ceil(n * p0))
    p1_cut = math.ceil(n * (p0 + p1))
    for i, node in enumerate(nodes_desc):
        node.tier = TIER_P0 if i < p0_cut else (TIER_P1 if i < p1_cut else TIER_P2)


# ── 输入 ──────────────────────────────────────────────────────

def load_edges(graph: DependencyGraph, paths: list[str]):
    for path in paths:
        with open(path, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                graph.add_edge(row.get("SRC_OWNER", ""), row.get("SRC_UNIT", ""),
                               row.get("EDGE_TYPE", ""), row.get("TARGET", ""),
                               row.get("DETAIL", ""))


def load_units(graph: DependencyGraph, path: str):
    """可选：从自省 JSON 注册所有程序单元（含无出边的函数），提升调用解析率"""
    with open(path, encoding="utf-8") as f:
        meta = json.load(f)
    owner = meta.get("owner", "")
    for u in meta.get("program_units", []):
        graph.register_unit(owner, u.get("name", ""))


# ── 输出 ──────────────────────────────────────────────────────

def write_tables_csv(graph: DependencyGraph, path: str):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["TABLE", "READ_PROCS", "WRITE_PROCS", "OPS", "SCORE", "TIER"])
        for t in sorted(graph.tables.values(), key=lambda t: t.score, reverse=True):
            w.writerow([t.name, t.read_procs, t.write_procs, "/".join(sorted(t.ops)),
                        t.score, t.tier])
    log.info("表清单已写入：%s", path)


def write_procs_csv(graph: DependencyGraph, path: str):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["OWNER", "NAME", "READS", "WRITES", "CALLS_OUT", "CALLED_BY",
                    "IS_ENTRY", "INFERRED", "SCORE", "TIER"])
        for p in sorted(graph.procs.values(), key=lambda p: p.score, reverse=True):
            w.writerow([p.owner, p.name, len(p.reads), len(p.writes), len(p.calls),
                        len(p.called_by), int(p.is_entry), int(p.inferred), p.score, p.tier])
    log.info("过程清单已写入：%s", path)


def render_report(graph: DependencyGraph) -> str:
    tables = sorted(graph.tables.values(), key=lambda t: t.score, reverse=True)
    procs = sorted(graph.procs.values(), key=lambda p: p.score, reverse=True)
    p0_tables = [t for t in tables if t.tier == TIER_P0]
    p0_procs = [p for p in procs if p.tier == TIER_P0]
    entries = [p for p in procs if p.is_entry]
    hubs = sorted(procs, key=lambda p: len(p.calls), reverse=True)[:10]
    written = sorted((t for t in tables if t.write_procs), key=lambda t: t.write_procs, reverse=True)
    cycles = graph.find_cycles()

    L = [
        "# 存储过程依赖图谱 · 核心资产分级",
        "",
        f"过程 **{len(graph.procs)}**（其中入口 {len(entries)}、推断节点 "
        f"{sum(1 for p in graph.procs.values() if p.inferred)}）｜ "
        f"表 **{len(graph.tables)}** ｜ 未解析外部调用 {len(graph.external_calls)} ｜ 调用环 {len(cycles)}",
        "",
        "> 由 `dependency_graph.py` 生成。P0 为优先理解训练对象；分级为启发式，供人工确认。",
        "",
        f"## 一、P0 核心表（{len(p0_tables)}）",
        "",
        "| 表 | 被读过程 | 被写过程 | 写操作 | 评分 |",
        "|----|---------|---------|--------|------|",
    ]
    for t in p0_tables:
        L.append(f"| {t.name} | {t.read_procs} | {t.write_procs} | {'/'.join(sorted(t.ops)) or '—'} | {t.score} |")

    L += ["", "## 二、状态承载表（写入密集，Top 10）", "",
          "| 表 | 被写过程 | 写操作 |", "|----|---------|--------|"]
    for t in written[:10]:
        L.append(f"| {t.name} | {t.write_procs} | {'/'.join(sorted(t.ops))} |")

    L += ["", f"## 三、入口过程（{len(entries)}，无人调用的顶层操作）", "",
          "| 过程 | 读 | 写 | 调用 | 分级 |", "|------|----|----|------|------|"]
    for p in sorted(entries, key=lambda p: p.score, reverse=True):
        L.append(f"| {p.key} | {len(p.reads)} | {len(p.writes)} | {len(p.calls)} | {p.tier} |")

    L += ["", "## 四、枢纽过程（调用扇出 Top 10）", "",
          "| 过程 | 扇出 | 被调用 | 分级 |", "|------|------|--------|------|"]
    for p in hubs:
        if p.calls:
            L.append(f"| {p.key} | {len(p.calls)} | {len(p.called_by)} | {p.tier} |")

    if cycles:
        L += ["", f"## 五、调用环（{len(cycles)}，须留意训练/测试顺序）", ""]
        for c in cycles[:20]:
            L.append(f"- {' → '.join(c)}")

    L += ["", f"## 六、P0 过程小结（{len(p0_procs)}）", "",
          ", ".join(p.key for p in p0_procs) or "—", ""]
    return "\n".join(L)


# ── 自测样例 ──────────────────────────────────────────────────

_SELF_TEST_EDGES = [
    # SP_CLOSE_WORKORDER：读 WO_MASTER/WO_ROUTE，写 WO_MASTER/WO_HISTORY，调用两个
    ("MESAPUSER", "SP_CLOSE_WORKORDER", "READ", "WO_MASTER", ""),
    ("MESAPUSER", "SP_CLOSE_WORKORDER", "READ", "WO_ROUTE", ""),
    ("MESAPUSER", "SP_CLOSE_WORKORDER", "WRITE", "WO_MASTER", "UPDATE"),
    ("MESAPUSER", "SP_CLOSE_WORKORDER", "WRITE", "WO_HISTORY", "INSERT"),
    ("MESAPUSER", "SP_CLOSE_WORKORDER", "CALL", "FC_YN_TO_BOOLEAN", ""),
    ("MESAPUSER", "SP_CLOSE_WORKORDER", "CALL", "PKG_NOTIFY.SEND", ""),
    # SP_REPORT：只读 WO_MASTER（使其成为高被读表）
    ("MESAPUSER", "SP_REPORT", "READ", "WO_MASTER", ""),
    # FC_YN_TO_BOOLEAN：一个被调用的函数（读一张配置表）
    ("MESAPUSER", "FC_YN_TO_BOOLEAN", "READ", "SYS_CONFIG", ""),
]


def build_self_test_graph() -> DependencyGraph:
    g = DependencyGraph()
    for e in _SELF_TEST_EDGES:
        g.add_edge(*e)
    g.finalize()
    g.assign_tiers()
    return g


def _run_self_test() -> int:
    g = build_self_test_graph()
    wo = g.tables["WO_MASTER"]
    close = g.procs["MESAPUSER.SP_CLOSE_WORKORDER"]
    fc = g.procs["MESAPUSER.FC_YN_TO_BOOLEAN"]
    checks = {
        "WO_MASTER 被 2 个过程读": wo.read_procs == 2,
        "WO_MASTER 被写(UPDATE)": "UPDATE" in wo.ops,
        "WO_MASTER 判为 P0 核心表": wo.tier == TIER_P0,
        "SP_CLOSE 是入口过程": close.is_entry,
        "SP_CLOSE 调用解析出 2 个": len(close.calls) == 2,
        "FC_YN 非入口（被调用）": not fc.is_entry,
        "FC_YN 被调用入度=1": len(fc.called_by) == 1,
        "SP_CLOSE 判为 P0 过程": close.tier == TIER_P0,
        "PKG_NOTIFY 解析为推断节点": any(p.inferred and p.name == "PKG_NOTIFY"
                                       for p in g.procs.values()),
        "无虚假调用环": g.find_cycles() == [],
    }
    failed = sum(0 if ok else 1 for ok in checks.values())
    for name, ok in checks.items():
        print(f"  {'✓' if ok else '✗'} {name}")
    print(f"自测结果：{len(checks) - failed}/{len(checks)} 通过")
    print("--- 核心资产报告 ---")
    print(render_report(g))
    return failed


# ── CLI ───────────────────────────────────────────────────────

def run(args) -> DependencyGraph:
    g = DependencyGraph()
    if args.self_test:
        raise SystemExit(_run_self_test())
    if not args.edges:
        raise SystemExit("请用 --edges 指定 proc_parser 产出的依赖边 CSV（可多份）")
    for p in args.edges:
        if not os.path.exists(p):
            raise SystemExit(f"边 CSV 不存在：{p}")
    if args.units:
        load_units(g, args.units)
    load_edges(g, args.edges)
    g.finalize()
    g.assign_tiers(p0=args.p0, p1=args.p1)

    log.info("过程 %d ｜ 表 %d ｜ 调用环 %d ｜ 未解析外部调用 %d",
             len(g.procs), len(g.tables), len(g.find_cycles()), len(g.external_calls))
    if args.out_report:
        with open(args.out_report, "w", encoding="utf-8") as f:
            f.write(render_report(g))
        log.info("核心资产报告已写入：%s", args.out_report)
    if args.out_tables:
        write_tables_csv(g, args.out_tables)
    if args.out_procs:
        write_procs_csv(g, args.out_procs)
    return g


def main(argv=None):
    p = argparse.ArgumentParser(description="存储过程依赖图谱与核心资产分级")
    p.add_argument("--edges", nargs="+", help="proc_parser 产出的依赖边 CSV（可多份）")
    p.add_argument("--units", help="可选：自省 JSON，注册全部单元以提升调用解析率")
    p.add_argument("--out-report", dest="out_report", help="核心资产报告 Markdown")
    p.add_argument("--out-tables", dest="out_tables", help="表指标 CSV")
    p.add_argument("--out-procs", dest="out_procs", help="过程指标 CSV")
    p.add_argument("--p0", type=float, default=0.1, help="P0 分位（默认前 10%%）")
    p.add_argument("--p1", type=float, default=0.3, help="P1 分位（默认其后 30%%）")
    p.add_argument("--self-test", action="store_true", help="运行内置样例自测")
    run(p.parse_args(argv))


if __name__ == "__main__":
    main()
