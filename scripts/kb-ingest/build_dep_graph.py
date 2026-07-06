#!/usr/bin/env python3
"""
全量依赖图谱构建器（内存安全批处理编排）

用途：对一个 schema 的全部 PL/SQL 程序单元构建完整依赖图谱与 P0 分级，
     用于 Sprint 3 训练前的 P0 资产选取（S3-0 T3-0-1/T3-0-2）。

内存安全：193 万行源码不一次性载入。按单元名分批（每批 --batch-size 个）从库拉源码，
         逐单元跑 proc_parser 静态分析，只把「边」累加进 dependency_graph，随即丢弃源码。

复用（均已单测）：
  · db_introspect.OracleMetadataProvider —— 只读拉 program_units / program_source（按名过滤+批量取行）
  · proc_parser.analyze_source           —— 抽读表/写表/调用
  · dependency_graph.DependencyGraph     —— 构图 + 分级 + 环检测 + 报告

产出：core_assets.md（P0 报告）、tables.csv、procs.csv、edges.csv、p0_units.txt（P0 单元名单，
     可直接喂 `db_introspect --source-units-file` 拉 P0 源码深析）。

用法：
    python build_dep_graph.py --self-test
    export MES_DB_USER=... MES_DB_PASSWORD=... MES_DB_DSN=host:1521/XEPDB1
    python build_dep_graph.py --owner MESAPUSER --use-dba --out-dir ./graph_mes

关联任务：S3-0 训练素材准备与 P0 选取（AI-MES-S3PLAN-2026-001）
作者：AI（芯智云匠）
日期：2026-07-06
"""

import os
import sys
import argparse
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db_introspect import DbConfig, get_provider, FakeMetadataProvider
from proc_parser import analyze_source
from dependency_graph import (
    DependencyGraph, write_tables_csv, write_procs_csv, render_report, TIER_P0,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# 只分析「实现体」；PACKAGE/TYPE 规格仅含子程序声明，会把成员声明误当调用，跳过
# （规格仍会注册为图节点，以便 PKG.PROC 调用解析）
ANALYZE_TYPES = {"PACKAGE BODY", "TYPE BODY", "PROCEDURE", "FUNCTION", "TRIGGER"}


def _assemble_sources(rows):
    """把 program_source 行按 (name,type) 组装为 {(name,type): source}"""
    buckets: dict[tuple, list] = {}
    for r in rows:
        buckets.setdefault((r["name"], r["type"]), []).append((r.get("line", 0), r.get("text", "")))
    out = {}
    for key, lines in buckets.items():
        lines.sort(key=lambda x: x[0])
        out[key] = "".join(t for _, t in lines)
    return out


def build(provider, owner: str, batch_size: int = 150, p0: float = 0.1,
          progress_every: int = 10) -> DependencyGraph:
    g = DependencyGraph()

    units = provider.program_units(owner)              # [{name, object_type, status}]
    for u in units:                                    # 先注册全部单元（含无边函数）
        g.register_unit(owner, u["name"])
    otype = {(u["name"], u["object_type"]) for u in units}
    names = sorted({u["name"] for u in units})
    log.info("owner=%s：%d 单元 / %d 去重单元名，分批 %d 拉源码分析", owner, len(units), len(names), batch_size)

    analyzed = 0
    for bi in range(0, len(names), batch_size):
        batch = names[bi:bi + batch_size]
        rows = provider.program_source(owner, names=batch)
        for (name, typ), src in _assemble_sources(rows).items():
            if (name, typ) not in otype:               # 只分析已知程序单元的类型
                continue
            if typ not in ANALYZE_TYPES:               # 跳过 PACKAGE/TYPE 规格（仅声明）
                continue
            a = analyze_source(src, owner=owner, name=name, object_type=typ)
            for t in a.read_tables:
                g.add_edge(owner, name, "READ", t)
            for w in a.write_tables:
                g.add_edge(owner, name, "WRITE", w["table"], "/".join(w["ops"]))
            for c in a.calls:
                g.add_edge(owner, name, "CALL", c)
            analyzed += 1
        if (bi // batch_size) % progress_every == 0:
            log.info("  已分析 %d 单元（%d/%d 批）", analyzed, bi // batch_size + 1,
                     (len(names) + batch_size - 1) // batch_size)

    g.finalize()
    g.assign_tiers(p0=p0)
    log.info("建图完成：过程 %d / 表 %d / 调用环 %d / 未解析外部调用 %d",
             len(g.procs), len(g.tables), len(g.find_cycles()), len(g.external_calls))
    return g


def write_outputs(g: DependencyGraph, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "core_assets.md"), "w", encoding="utf-8") as f:
        f.write(render_report(g))
    write_tables_csv(g, os.path.join(out_dir, "tables.csv"))
    write_procs_csv(g, os.path.join(out_dir, "procs.csv"))
    # P0 单元名单（去重），供 db_introspect --source-units-file 拉源码深析
    p0_names = sorted({p.name for p in g.procs.values() if p.tier == TIER_P0 and not p.inferred})
    with open(os.path.join(out_dir, "p0_units.txt"), "w", encoding="utf-8") as f:
        f.write("# P0 核心单元名单（build_dep_graph 生成）\n")
        f.write("\n".join(p0_names) + "\n")
    log.info("已写出 core_assets.md / tables.csv / procs.csv / p0_units.txt（P0 单元 %d）到 %s",
             len(p0_names), out_dir)


# ── 自测（假数据，验证批处理编排）────────────────────────────

def _self_test() -> int:
    prov = FakeMetadataProvider(
        program_units=[
            {"name": "SP_CLOSE", "object_type": "PROCEDURE", "status": "VALID"},
            {"name": "FC_CHK", "object_type": "FUNCTION", "status": "VALID"},
        ],
        program_source=[
            {"name": "SP_CLOSE", "type": "PROCEDURE", "line": 1,
             "text": "PROCEDURE SP_CLOSE IS BEGIN "},
            {"name": "SP_CLOSE", "type": "PROCEDURE", "line": 2,
             "text": "UPDATE WO SET S='9' WHERE 1=1; V:=FC_CHK(1); END;"},
            {"name": "FC_CHK", "type": "FUNCTION", "line": 1,
             "text": "FUNCTION FC_CHK RETURN NUMBER IS BEGIN SELECT 1 INTO X FROM CFG; RETURN 1; END;"},
        ],
    )
    g = build(prov, "O", batch_size=1)
    checks = {
        "WO 被写": "WO" in g.tables and g.tables["WO"].write_procs == 1,
        "CFG 被读": "CFG" in g.tables,
        "SP_CLOSE 调用 FC_CHK": "O.FC_CHK" in g.procs["O.SP_CLOSE"].calls,
        "SP_CLOSE 入口": g.procs["O.SP_CLOSE"].is_entry,
        "FC_CHK 非入口": not g.procs["O.FC_CHK"].is_entry,
    }
    failed = sum(0 if ok else 1 for ok in checks.values())
    for n, ok in checks.items():
        print(f"  {'✓' if ok else '✗'} {n}")
    print(f"自测：{len(checks) - failed}/{len(checks)} 通过")
    return failed


def main(argv=None):
    p = argparse.ArgumentParser(description="全量依赖图谱构建器（内存安全批处理）")
    p.add_argument("--owner", help="目标 schema（如 MESAPUSER）")
    p.add_argument("--out-dir", default="./dep_graph_out", help="输出目录")
    p.add_argument("--batch-size", type=int, default=150, help="每批拉源码的单元名数")
    p.add_argument("--p0", type=float, default=0.1, help="P0 分位（默认前 10%%）")
    p.add_argument("--use-dba", dest="use_dba", action="store_true", help="用 DBA_* 视图（DBA 账号更快）")
    p.add_argument("--self-test", action="store_true", help="假数据自测批处理编排")
    args = p.parse_args(argv)

    if args.self_test:
        raise SystemExit(_self_test())
    if not args.owner:
        raise SystemExit("请用 --owner 指定 schema")
    provider = get_provider("oracle", DbConfig.from_env(), use_dba=args.use_dba)
    try:
        g = build(provider, args.owner, batch_size=args.batch_size, p0=args.p0)
    finally:
        provider.close()
    write_outputs(g, args.out_dir)


if __name__ == "__main__":
    main()
