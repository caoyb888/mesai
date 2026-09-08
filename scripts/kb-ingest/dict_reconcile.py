#!/usr/bin/env python3
"""
数据字典对账器 → 自省结果 vs 甲方字典 差异清单

用途：把 db_introspect.py 产出的元数据 JSON（真实库自省）与甲方数据字典
     data_dictionary_full.csv 逐字段对账，产出差异清单，供「文档更正请求」流程。

对账类别：
  · table_missing_in_dict —— 库有表、字典无（字典漏记）
  · table_missing_in_db   —— 字典有表、库无（字典过期/表已删）
  · col_missing_in_dict   —— 库有字段、字典无
  · col_missing_in_db     —— 字典有字段、库无
  · type_mismatch         —— 同字段类型不一致（高优先）
  · length_mismatch       —— 长度不一致（可选，NUMBER/TIMESTAMP 噪声大，默认关闭）
  · comment_db_empty      —— 库注释空、字典有 → 【字典可反哺库空注释】
  · comment_dict_empty    —— 库有注释、字典空 → 字典可补录
  · comment_conflict      —— 两侧注释都有且不同 → 需人工判定

原则（对齐 CLAUDE.md 第十章）：只产差异清单，不静默修改；修复须走 IT 审核。

用法：
    python dict_reconcile.py --self-test
    python dict_reconcile.py --introspect metadata_mesapuser.json metadata_scoapuser.json \
        --dict-csv ../../docs/data_dictionary_full.csv \
        --out-report reconcile_report.md --out-csv discrepancies.csv

关联任务：S2.9-5 字典对账（AI-MES-PLAN-ADJ-2026-001）
作者：AI（芯智云匠）
日期：2026-07-06
"""

import os
import sys
import csv
import json
import argparse
import logging
from dataclasses import dataclass
from typing import Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

# ── 类别与严重度 ──────────────────────────────────────────────
CAT_TABLE_MISS_DICT = "table_missing_in_dict"
CAT_TABLE_MISS_DB = "table_missing_in_db"
CAT_COL_MISS_DICT = "col_missing_in_dict"
CAT_COL_MISS_DB = "col_missing_in_db"
CAT_TYPE = "type_mismatch"
CAT_LENGTH = "length_mismatch"
CAT_CMT_DB_EMPTY = "comment_db_empty"
CAT_CMT_DICT_EMPTY = "comment_dict_empty"
CAT_CMT_CONFLICT = "comment_conflict"

SEVERITY = {
    CAT_TYPE: "high",
    CAT_TABLE_MISS_DB: "medium",
    CAT_TABLE_MISS_DICT: "medium",
    CAT_COL_MISS_DB: "medium",
    CAT_COL_MISS_DICT: "medium",
    CAT_CMT_CONFLICT: "medium",
    CAT_LENGTH: "low",
    CAT_CMT_DB_EMPTY: "low",
    CAT_CMT_DICT_EMPTY: "low",
}


@dataclass
class Discrepancy:
    owner: str
    table: str
    column: str          # 表级差异时为空
    category: str
    db_value: str = ""
    dict_value: str = ""

    @property
    def severity(self) -> str:
        return SEVERITY.get(self.category, "low")


# ── 归一 ──────────────────────────────────────────────────────

def _up(s: Optional[str]) -> str:
    return (s or "").replace('"', "").strip().upper()

def _base_type(s: Optional[str]) -> str:
    """取基础类型名（去精度/长度）：VARCHAR2(20) → VARCHAR2"""
    return _up(s).split("(")[0].split()[0] if s else ""

def _cmt(s: Optional[str]) -> str:
    return (s or "").strip()


# ── 索引构建 ──────────────────────────────────────────────────

def index_from_introspect(paths: list[str]):
    cols: dict[tuple, dict] = {}
    tables: set[tuple] = set()
    owners: set[str] = set()
    for path in paths:
        with open(path, encoding="utf-8") as f:
            meta = json.load(f)
        owner = _up(meta.get("owner", ""))
        owners.add(owner)
        for t in meta.get("tables", []):
            tname = _up(t.get("name"))
            tables.add((owner, tname))
            for c in t.get("columns", []):
                cols[(owner, tname, _up(c.get("name")))] = {
                    "type": c.get("data_type"),
                    "length": c.get("length"),
                    "comment": c.get("comment"),
                }
    return cols, tables, owners


def index_from_dict_csv(path: str):
    cols: dict[tuple, dict] = {}
    tables: set[tuple] = set()
    owners: set[str] = set()
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            owner = _up(row.get("SCHEMA"))
            tname = _up(row.get("TABLE_NAME"))
            col = _up(row.get("COLUMN_NAME"))
            owners.add(owner)
            tables.add((owner, tname))
            cols[(owner, tname, col)] = {
                "type": row.get("DATA_TYPE"),
                "length": row.get("LEN"),
                "comment": row.get("COL_COMMENT"),
            }
    return cols, tables, owners


# ── 对账 ──────────────────────────────────────────────────────

def reconcile(db_cols, db_tables, dict_cols, dict_tables,
              scope_owners, check_length: bool = False) -> list[Discrepancy]:
    """仅对账 scope_owners（通常为已自省的 schema），保证缺失判定有依据。"""
    out: list[Discrepancy] = []
    db_t = {t for t in db_tables if t[0] in scope_owners}
    dict_t = {t for t in dict_tables if t[0] in scope_owners}

    # 表级差异
    for (o, t) in sorted(db_t - dict_t):
        out.append(Discrepancy(o, t, "", CAT_TABLE_MISS_DICT))
    for (o, t) in sorted(dict_t - db_t):
        out.append(Discrepancy(o, t, "", CAT_TABLE_MISS_DB))

    common_tables = db_t & dict_t

    # 列级差异（仅两侧都存在的表，避免整表缺失时逐列刷屏）
    for key, dbv in db_cols.items():
        o, t, c = key
        if o not in scope_owners or (o, t) not in common_tables:
            continue
        dv = dict_cols.get(key)
        if dv is None:
            out.append(Discrepancy(o, t, c, CAT_COL_MISS_DICT, _base_type(dbv["type"])))
            continue
        # 类型
        if _base_type(dbv["type"]) != _base_type(dv["type"]):
            out.append(Discrepancy(o, t, c, CAT_TYPE,
                                   _base_type(dbv["type"]), _base_type(dv["type"])))
        # 长度（可选）
        if check_length and str(dbv.get("length") or "") != str(dv.get("length") or ""):
            out.append(Discrepancy(o, t, c, CAT_LENGTH,
                                   str(dbv.get("length") or ""), str(dv.get("length") or "")))
        # 注释
        db_c, dict_c = _cmt(dbv["comment"]), _cmt(dv["comment"])
        if db_c == dict_c:
            pass
        elif not db_c and dict_c:
            out.append(Discrepancy(o, t, c, CAT_CMT_DB_EMPTY, "", dict_c))
        elif db_c and not dict_c:
            out.append(Discrepancy(o, t, c, CAT_CMT_DICT_EMPTY, db_c, ""))
        else:
            out.append(Discrepancy(o, t, c, CAT_CMT_CONFLICT, db_c, dict_c))

    # 字典有、库无的列（两侧都存在的表内）
    for key, dv in dict_cols.items():
        o, t, c = key
        if o not in scope_owners or (o, t) not in common_tables:
            continue
        if key not in db_cols:
            out.append(Discrepancy(o, t, c, CAT_COL_MISS_DB, "", _base_type(dv["type"])))

    return out


def tally(discrepancies: list[Discrepancy]) -> dict:
    by_cat: dict[str, int] = {}
    by_sev: dict[str, int] = {}
    for d in discrepancies:
        by_cat[d.category] = by_cat.get(d.category, 0) + 1
        by_sev[d.severity] = by_sev.get(d.severity, 0) + 1
    return {"total": len(discrepancies), "by_category": by_cat, "by_severity": by_sev}


# ── 输出 ──────────────────────────────────────────────────────

def write_csv(discrepancies: list[Discrepancy], path: str):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["OWNER", "TABLE", "COLUMN", "CATEGORY", "SEVERITY", "DB_VALUE", "DICT_VALUE"])
        for d in discrepancies:
            w.writerow([d.owner, d.table, d.column, d.category, d.severity, d.db_value, d.dict_value])
    log.info("差异清单已写入：%s（%d 条）", path, len(discrepancies))


_CAT_TITLE = {
    CAT_TYPE: "类型不一致（高优先）",
    CAT_TABLE_MISS_DICT: "库有表·字典漏记",
    CAT_TABLE_MISS_DB: "字典有表·库无（字典过期）",
    CAT_COL_MISS_DICT: "库有字段·字典漏记",
    CAT_COL_MISS_DB: "字典有字段·库无",
    CAT_CMT_CONFLICT: "注释冲突（两侧不同）",
    CAT_CMT_DB_EMPTY: "库注释空·字典可反哺",
    CAT_CMT_DICT_EMPTY: "字典注释空·可补录",
    CAT_LENGTH: "长度不一致",
}
_CAT_ORDER = [CAT_TYPE, CAT_TABLE_MISS_DICT, CAT_TABLE_MISS_DB, CAT_COL_MISS_DICT,
              CAT_COL_MISS_DB, CAT_CMT_CONFLICT, CAT_CMT_DB_EMPTY, CAT_CMT_DICT_EMPTY, CAT_LENGTH]


def _esc(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ⏎ ")


def render_report(discrepancies: list[Discrepancy], scope_owners) -> str:
    t = tally(discrepancies)
    grouped: dict[str, list] = {}
    for d in discrepancies:
        grouped.setdefault(d.category, []).append(d)

    L = [
        "# 数据字典对账报告",
        "",
        f"对账范围 schema：{', '.join(sorted(scope_owners)) or '—'} ｜ 差异合计 **{t['total']}**"
        f"（高 {t['by_severity'].get('high', 0)} / 中 {t['by_severity'].get('medium', 0)}"
        f" / 低 {t['by_severity'].get('low', 0)}）",
        "",
        "> 由 `dict_reconcile.py` 生成。差异仅供「文档更正请求」，**不得静默修改字典或库**（CLAUDE.md 第十章）。",
        "",
        "## 汇总",
        "",
        "| 类别 | 数量 | 严重度 |",
        "|------|------|--------|",
    ]
    for cat in _CAT_ORDER:
        n = t["by_category"].get(cat, 0)
        if n:
            L.append(f"| {_CAT_TITLE[cat]} | {n} | {SEVERITY[cat]} |")

    # 特别小结：字典可反哺库空注释（高价值）
    repair = grouped.get(CAT_CMT_DB_EMPTY, [])
    L += ["", f"## ⭐ 字典可反哺库空注释（{len(repair)}，字典→库修复候选）", ""]
    if repair:
        L += ["| 位置 | 字典注释 |", "|------|---------|"]
        for d in repair[:200]:
            L.append(f"| {d.owner}.{d.table}.{d.column} | {_esc(d.dict_value)} |")
        if len(repair) > 200:
            L.append(f"| … | 其余 {len(repair) - 200} 条见 CSV |")
    else:
        L.append("（无）")

    # 各类别明细（截断展示，完整见 CSV）
    for cat in _CAT_ORDER:
        items = grouped.get(cat, [])
        if not items or cat == CAT_CMT_DB_EMPTY:
            continue
        L += ["", f"## {_CAT_TITLE[cat]}（{len(items)}）", "",
              "| 位置 | 库值 | 字典值 |", "|------|------|--------|"]
        for d in items[:100]:
            loc = f"{d.owner}.{d.table}" + (f".{d.column}" if d.column else "")
            L.append(f"| {loc} | {_esc(d.db_value)} | {_esc(d.dict_value)} |")
        if len(items) > 100:
            L.append(f"| … | 其余 {len(items) - 100} 条见 CSV | |")

    L.append("")
    return "\n".join(L)


# ── 自测样例 ──────────────────────────────────────────────────

def build_self_test():
    """构造覆盖各类别的库/字典索引对"""
    db_cols = {
        ("MESAPUSER", "WO_MASTER", "WO_ID"): {"type": "VARCHAR2", "length": 30, "comment": "工单号"},
        ("MESAPUSER", "WO_MASTER", "WO_STATUS"): {"type": "VARCHAR2", "length": 2, "comment": ""},        # 库空
        ("MESAPUSER", "WO_MASTER", "QTY"): {"type": "NUMBER", "length": 22, "comment": "数量"},
        ("MESAPUSER", "WO_MASTER", "NEW_COL"): {"type": "DATE", "length": 7, "comment": "库新增字段"},     # 字典无
    }
    db_tables = {("MESAPUSER", "WO_MASTER"), ("MESAPUSER", "WO_EXTRA")}                                    # 字典无 WO_EXTRA
    dict_cols = {
        ("MESAPUSER", "WO_MASTER", "WO_ID"): {"type": "VARCHAR2", "length": 30, "comment": "工单号"},       # 一致
        ("MESAPUSER", "WO_MASTER", "WO_STATUS"): {"type": "VARCHAR2", "length": 2, "comment": "工单状态"},   # 字典可反哺
        ("MESAPUSER", "WO_MASTER", "QTY"): {"type": "VARCHAR2", "length": 20, "comment": "数量"},           # 类型不一致
        ("MESAPUSER", "WO_MASTER", "OLD_COL"): {"type": "CHAR", "length": 1, "comment": "字典遗留字段"},     # 库无
    }
    dict_tables = {("MESAPUSER", "WO_MASTER"), ("MESAPUSER", "DICT_ONLY_TAB")}                             # 库无
    return db_cols, db_tables, dict_cols, dict_tables, {"MESAPUSER"}


def _run_self_test() -> int:
    db_cols, db_tables, dict_cols, dict_tables, scope = build_self_test()
    ds = reconcile(db_cols, db_tables, dict_cols, dict_tables, scope)
    cats = {d.category for d in ds}
    cat_of = lambda o, t, c: next((d.category for d in ds
                                   if (d.owner, d.table, d.column) == (o, t, c)), None)
    checks = {
        "WO_EXTRA 库有表·字典无": Discrepancy("MESAPUSER", "WO_EXTRA", "", CAT_TABLE_MISS_DICT) in ds,
        "DICT_ONLY_TAB 字典有表·库无": Discrepancy("MESAPUSER", "DICT_ONLY_TAB", "", CAT_TABLE_MISS_DB) in ds,
        "QTY 类型不一致": cat_of("MESAPUSER", "WO_MASTER", "QTY") == CAT_TYPE,
        "WO_STATUS 字典可反哺": cat_of("MESAPUSER", "WO_MASTER", "WO_STATUS") == CAT_CMT_DB_EMPTY,
        "NEW_COL 库有字段·字典无": cat_of("MESAPUSER", "WO_MASTER", "NEW_COL") == CAT_COL_MISS_DICT,
        "OLD_COL 字典有字段·库无": cat_of("MESAPUSER", "WO_MASTER", "OLD_COL") == CAT_COL_MISS_DB,
        "WO_ID 一致不报差异": cat_of("MESAPUSER", "WO_MASTER", "WO_ID") is None,
    }
    failed = sum(0 if ok else 1 for ok in checks.values())
    for name, ok in checks.items():
        print(f"  {'✓' if ok else '✗'} {name}")
    print(f"自测结果：{len(checks) - failed}/{len(checks)} 通过")
    print("--- 对账报告 ---")
    print(render_report(ds, scope))
    return failed


# ── CLI ───────────────────────────────────────────────────────

def run(args):
    if args.self_test:
        raise SystemExit(_run_self_test())
    if not args.introspect or not args.dict_csv:
        raise SystemExit("请同时指定 --introspect（自省 JSON，可多份）与 --dict-csv（字典 CSV）")
    for p in args.introspect + [args.dict_csv]:
        if not os.path.exists(p):
            raise SystemExit(f"输入不存在：{p}")

    db_cols, db_tables, db_owners = index_from_introspect(args.introspect)
    dict_cols, dict_tables, _ = index_from_dict_csv(args.dict_csv)
    scope = db_owners                                  # 以已自省的 schema 为对账范围
    ds = reconcile(db_cols, db_tables, dict_cols, dict_tables, scope, check_length=args.check_length)

    log.info("对账统计：%s", json.dumps(tally(ds), ensure_ascii=False))
    if args.out_report:
        with open(args.out_report, "w", encoding="utf-8") as f:
            f.write(render_report(ds, scope))
        log.info("对账报告已写入：%s", args.out_report)
    if args.out_csv:
        write_csv(ds, args.out_csv)
    return ds


def main(argv=None):
    p = argparse.ArgumentParser(description="数据字典对账器（自省 vs 甲方字典）")
    p.add_argument("--introspect", nargs="+", help="db_introspect 产出的元数据 JSON（可多份）")
    p.add_argument("--dict-csv", dest="dict_csv", help="数据字典 CSV（data_dictionary_full.csv）")
    p.add_argument("--out-report", dest="out_report", help="对账报告 Markdown")
    p.add_argument("--out-csv", dest="out_csv", help="差异清单 CSV")
    p.add_argument("--check-length", dest="check_length", action="store_true",
                   help="额外对账字段长度（NUMBER/TIMESTAMP 噪声大，默认关闭）")
    p.add_argument("--self-test", action="store_true", help="运行内置样例自测")
    run(p.parse_args(argv))


if __name__ == "__main__":
    main()
