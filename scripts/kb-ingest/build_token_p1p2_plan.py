#!/usr/bin/env python3
"""
T3-4-3：Sprint 3 Token 消耗与降级复盘 + P1/P2 资产训练排期

两部分：
① **Token 复盘**：汇总 Sprint 3 全任务 Token 消耗（按任务/按日），核 §12 预算与降级事件
   （2026-07-15 批训练超默认 300 万 → TL 授权临时 8M 闸），提炼单位成本与效率洞察。
② **P1/P2 排期**：以 P0 实测单位成本（表 ~5.6K/张、子程序 ~2.5K/个）+ 依赖图中心度分层，
   估算 P1（次核心，主动训练）/ P2（长尾，按需 + RAG 兜底）的资产量、Token 与预算日，给排期建议。

纯本地、无 AI、无 DB；台账与资产总量为已核实数据（附来源），估算为纯计算（可单测）。

用法：
  python3 build_token_p1p2_plan.py --out docs/S3-4-3_Token复盘与P1P2排期.md

关联需求单：REQ-MES-AI-20260715-001（T3-4-3）
作者：AI（芯智云匠）  日期：2026-07-16
"""
import argparse
import collections
from pathlib import Path

TASK_NO = "REQ-MES-AI-20260715-001"

# ── Sprint 3 Token 台账（已核实，附来源）─────────────────────────────
LEDGER = [
    {"task": "S3-1 表卡片理解训练（95 张）", "date": "2026-07-15", "tokens": 532207,
     "src": "docs/S3-1_表字段理解报告.md"},
    {"task": "S3-2 存储过程理解训练（1308 卡片）", "date": "2026-07-15", "tokens": 3289621,
     "src": "docs/S3-2_存储过程理解报告.md（含 14 次补跑）"},
    {"task": "T3-1-4/5 SQL 场景验证（30 题）", "date": "2026-07-15", "tokens": 66771,
     "src": "docs/S3-1_SQL验证报告.md"},
    {"task": "表标签抽取（hybrid 检索调优）", "date": "2026-07-15", "tokens": 26000,
     "src": "mes_table_labels.json（Kimi 抽 95 表中文名/别名）"},
    {"task": "T3-3-1 状态机反推（34 字段）", "date": "2026-07-15", "tokens": 23962,
     "src": "S3-3 报告 第一部分"},
    {"task": "T3-3-2 追溯链路（13 边）", "date": "2026-07-16", "tokens": 21650,
     "src": "S3-3 报告 第二部分"},
    {"task": "T3-3-3 核心流程（12 组）", "date": "2026-07-16", "tokens": 29325,
     "src": "S3-3 报告 第三部分"},
    {"task": "T3-3-4 验证题库（21 题 + 接地校验）", "date": "2026-07-16", "tokens": 0,
     "src": "确定性生成，无 AI 调用"},
    {"task": "T3-3-5 报告完稿", "date": "2026-07-16", "tokens": 0, "src": "纯本地，无 AI"},
    {"task": "S3-4-1 系统理解总报告", "date": "2026-07-16", "tokens": 0, "src": "纯本地汇总，无 AI"},
    {"task": "S3-4-3 本复盘报告", "date": "2026-07-16", "tokens": 0, "src": "纯本地，无 AI"},
]

# ── §12 预算阈值 ─────────────────────────────────────────────────────
BUDGET = {"daily_default": 3_000_000, "degrade": 2_500_000, "pause": 3_000_000,
          "temp_gate": 8_000_000}

# ── P0 实测单位成本 ──────────────────────────────────────────────────
P0 = {"table_tokens": 532207, "table_n": 95,          # 表卡片
      "subprog_tokens": 3289621, "subprog_n": 1308,   # 子程序
      "p0_units": 60, "p0_subprograms": 1401}         # Top60 包 → 1401 子程序

# ── 资产总量（依赖图 / census）───────────────────────────────────────
ASSETS = {"tables_total": 2249, "units_total": 5101,
          "tables_p0_rank": 100, "units_p0_rank": 60}

# ── P1/P2 分层（按中心度 rank，与 P0 Top-N 选取口径一致）──────────────
#   表 score@rank: 100→20, 200→11, 300→9, 500→6, 1000→4（长尾快速衰减）
#   过程 score@rank: 60→46, 150→32, 300→22, 500→14
TIERS = {
    "P1": {"table_rank": (101, 400), "unit_rank": (61, 200),
           "subprog_per_unit": 12},   # 次核心包较小，保守估 ~12 子程序/包（P0 均 23.4）
    "P2": {"table_rank": (401, 2249), "unit_rank": (201, 5101),
           "subprog_per_unit": 8},
}
VARIANT_DEDUP = 0.07   # 厂区/产线变体去重实测省比（P0 跳 79/~1480≈5-7%）


# ── 纯逻辑（可单测）─────────────────────────────────────────────────
def total_tokens(ledger=LEDGER):
    return sum(r["tokens"] for r in ledger)


def by_date(ledger=LEDGER):
    d = collections.OrderedDict()
    for r in ledger:
        d[r["date"]] = d.get(r["date"], 0) + r["tokens"]
    return d


def unit_cost(tokens, n):
    return tokens / n if n else 0.0


def tier_span(rank_lo, rank_hi):
    """rank 区间的资产个数（含端点）"""
    return max(0, rank_hi - rank_lo + 1)


def project_tier(tier, cost_table, cost_subprog):
    """估算某层 Token：表数×表单价 + 子程序数（含变体去重）×子程序单价"""
    n_tables = tier_span(*tier["table_rank"])
    n_units = tier_span(*tier["unit_rank"])
    n_subprog_raw = n_units * tier["subprog_per_unit"]
    n_subprog = round(n_subprog_raw * (1 - VARIANT_DEDUP))
    tok_tables = round(n_tables * cost_table)
    tok_subprog = round(n_subprog * cost_subprog)
    return {"n_tables": n_tables, "n_units": n_units, "n_subprog": n_subprog,
            "tok_tables": tok_tables, "tok_subprog": tok_subprog,
            "tok_total": tok_tables + tok_subprog}


def budget_days(tokens, daily=BUDGET["daily_default"]):
    """按每日预算需的训练日（向上取整近似，保留一位小数）"""
    import math
    return math.ceil(tokens / daily * 10) / 10 if daily else 0.0


def crossed_thresholds(day_tokens):
    """返回当日跨过的 §12 阈值名（降级/暂停）"""
    hit = []
    if day_tokens >= BUDGET["degrade"]:
        hit.append("降级(250万)")
    if day_tokens >= BUDGET["pause"]:
        hit.append("暂停(300万)")
    return hit


# ── 报告组装 ────────────────────────────────────────────────────────
def build_report():
    ct = unit_cost(P0["table_tokens"], P0["table_n"])
    cs = unit_cost(P0["subprog_tokens"], P0["subprog_n"])
    total = total_tokens()
    daily = by_date()
    p1 = project_tier(TIERS["P1"], ct, cs)
    p2 = project_tier(TIERS["P2"], ct, cs)
    p1_days = budget_days(p1["tok_total"])
    p1_days_gate = budget_days(p1["tok_total"], BUDGET["temp_gate"])

    L = [
        "# Sprint 3 Token 复盘与 P1/P2 资产训练排期（T3-4-3）", "",
        "| 项 | 内容 |", "|----|----|",
        "| 文件编号 | AI-MES-TOKEN-PLAN-2026 |",
        f"| 需求单 | {TASK_NO}（T3-4-3）|",
        "| 编制 | AI（芯智云匠）| 日期 | 2026-07-16 |",
        f"| Sprint 3 Token 合计 | **{total:,}**（约 {total/1e6:.2f}M）|",
        "| §12 每日预算 | 300 万（默认）；250 万降级；300 万暂停 |", "",

        "## 一、Token 消耗复盘", "",
        "### 1.1 按任务", "",
        "| 任务 | 日期 | Token | 来源 |", "|----|----|----|----|",
    ]
    for r in sorted(LEDGER, key=lambda x: -x["tokens"]):
        L.append(f"| {r['task']} | {r['date']} | {r['tokens']:,} | {r['src']} |")
    L += [f"| **合计** |  | **{total:,}** |  |", "",
          "### 1.2 按日（对照 §12 预算）", "",
          "| 日期 | Token | 占默认预算 | 跨阈值 | 处置 |", "|----|----|----|----|----|"]
    for d, tok in daily.items():
        hit = crossed_thresholds(tok)
        pct = f"{tok/BUDGET['daily_default']*100:.0f}%"
        disp = "TL 授权临时 8M 闸" if hit else "默认闸内"
        L.append(f"| {d} | {tok:,} | {pct} | {('、'.join(hit)) or '无'} | {disp} |")
    L += ["",
          "### 1.3 效率洞察", "",
          f"- **批训练是绝对大头**：S3-1+S3-2 训练 = {P0['table_tokens']+P0['subprog_tokens']:,}，"
          f"占 Sprint 3 总量 **{round((P0['table_tokens']+P0['subprog_tokens'])*100/total)}%**；"
          "理解合成类（S3-3 四部分 ≈7.5 万）与验证/报告类（确定性，**0 token**）极省。",
          "- **确定性工具替代 AI**：T3-3-4 验证题、T3-3-5 完稿、S3-4-1 总报告、本复盘均纯本地生成，**0 AI token**——"
          "把「能算的」从「问模型」剥离，是最有效的省 token 杠杆。",
          "- **已落地的省 token 措施**：输出上限压至 1200 token/单元；厂区/产线变体去重（P0 跳 79 子程序）；"
          "3 分片并发（~2h 跑完）；无 RAG 直喂卡片（训练阶段不检索）。", "",

        "## 二、预算与降级复盘", "",
        f"- **超预算事件（2026-07-15）**：当日 {daily.get('2026-07-15',0):,} tokens，"
        "跨过 §12 **降级(250万)** 与 **暂停(300万)** 双阈值。",
        "- **处置**：TL 书面授权当日临时上调网关闸 `TOKEN_PAUSE_THRESHOLD/DEGRADE_THRESHOLD=8M`（次日恢复默认），"
        "留痕于批训练需求单 `REQ-MES-AI-20260715-001`。**非静默超额**。",
        "- **§12 自动降级（Top-5→Top-3 / 压缩输出）是否触发**：训练阶段直喂表卡片/子程序源码、**不走 RAG 检索**，"
        "故 Top-5→Top-3 降级不适用；改以「输出上限 1200 + 变体去重 + 分片」主动控量。压缩输出=已默认启用。",
        f"- **2026-07-16 回落**：{daily.get('2026-07-16',0):,} tokens（默认 300 万闸内 {daily.get('2026-07-16',0)*100//BUDGET['daily_default']}%），恢复默认预算运行。",
        "- **教训**：单日跑完整 P0 批训练必然超默认 300 万日预算 → **批训练窗口须 TL 预授权临时闸，或跨日分摊**；"
        "非训练类任务应优先确定性实现以零成本产出。", "",

        "## 三、单位成本（P0 实测，作 P1/P2 估算基准）", "",
        "| 资产类型 | 实测 | 单位成本 | 说明 |", "|----|----|----|----|",
        f"| 表卡片 | {P0['table_tokens']:,} / {P0['table_n']} 张 | **~{ct:,.0f} token/张** | 结构+字典语义+热度画像合成 |",
        f"| 存储过程子程序 | {P0['subprog_tokens']:,} / {P0['subprog_n']} 个 | **~{cs:,.0f} token/个** | 输出上限 1200，含补跑重复 |",
        "| 确定性任务（验证/报告）| — | **0** | 纯本地生成 |", "",
        f"> P0 Top{P0['p0_units']} 包 → {P0['p0_subprograms']:,} 子程序，均 {P0['p0_subprograms']/P0['p0_units']:.1f} 子程序/包；"
        "P1/P2 低中心度包更小，下方按保守子程序/包估。", "",

        "## 四、P1/P2 资产分层与训练排期", "",
        "**分层口径**：沿用 P0 的**中心度 Top-N**（依赖图 SCORE 降序 rank），非百分位 TIER 列"
        f"（后者把 P0 撑到 2117 过程不可用）。全库：表 {ASSETS['tables_total']:,}、程序单元 {ASSETS['units_total']:,}。", "",
        "| 层 | 表（rank/数量）| 包单元（rank/数量）| 子程序估* | 预估 Token | 策略 |",
        "|----|----|----|----|----|----|",
        f"| **P0（已训）** | Top{ASSETS['tables_p0_rank']} / 95 | Top{ASSETS['units_p0_rank']} / 60 | {P0['p0_subprograms']:,} | "
        f"{P0['table_tokens']+P0['subprog_tokens']:,} | ✅ 完成 |",
        f"| **P1（次核心·主动训）** | {TIERS['P1']['table_rank'][0]}–{TIERS['P1']['table_rank'][1]} / {p1['n_tables']} | "
        f"{TIERS['P1']['unit_rank'][0]}–{TIERS['P1']['unit_rank'][1]} / {p1['n_units']} | ~{p1['n_subprog']:,} | "
        f"**~{p1['tok_total']:,}** | 主动批训 |",
        f"| **P2（长尾·按需）** | {TIERS['P2']['table_rank'][0]}–{TIERS['P2']['table_rank'][1]} / {p2['n_tables']:,} | "
        f"{TIERS['P2']['unit_rank'][0]}–{TIERS['P2']['unit_rank'][1]} / {p2['n_units']:,} | ~{p2['n_subprog']:,} | "
        f"~{p2['tok_total']:,}（上限参考）| RAG 兜底 + 按需增量 |",
        "",
        f"*子程序估 = 包数 × 保守子程序/包（P1 {TIERS['P1']['subprog_per_unit']}、P2 {TIERS['P2']['subprog_per_unit']}）× "
        f"(1−变体去重 {VARIANT_DEDUP:.0%})；表估 = 表数 × ~{ct:,.0f}。均为**规划上限**，实值随真实包体大小浮动。", "",
        "### 4.1 P1 排期建议（主动训练）", "",
        f"- **总量 ~{p1['tok_total']:,} tokens**（表 {p1['tok_tables']:,} + 子程序 {p1['tok_subprog']:,}）。",
        f"- 按默认 300 万/日 ≈ **{p1_days} 训练日**；若 TL 授权临时 8M 闸 ≈ **{p1_days_gate} 日**跑完。",
        "- **建议**：拆 2 个训练窗口（表批 + 过程批），过程批 TL 预授权临时闸；沿用 P0 省 token 措施（输出上限/变体去重/分片）。",
        "- 训完 P1 表/过程卡片入 `mes_s3_understanding`，跑 `validate_ingestion.py` 抽检召回，补对应断言种子。", "",
        "### 4.2 P2 策略（不主动全训）", "",
        f"- P2 长尾 {p2['n_tables']:,} 表 + {p2['n_units']:,} 单元，全量批训成本极高（表估已 ~{p2['tok_tables']:,}，过程更大），"
        "**不主动全训**。",
        "- **默认 RAG 兜底**：靠已入库 P0/P1 卡片 + 术语表 + 代码字典召回；命中 P2 资产时给出「基于结构/字典的谨慎回答 + 标待确认」。",
        "- **按需增量训练**：新需求单命中某 P2 资产时，只临时拉该资产源码增量训练该卡片（单次成本 ~5.6K/表 或 ~2.5K/子程序，可忽略）。", "",

        "## 五、结论与建议", "",
        f"1. **Sprint 3 总消耗 ~{total/1e6:.2f}M**，96% 集中在 P0 批训练；理解合成廉价、确定性任务零成本。",
        "2. **预算机制**：批训练日须 TL 预授权临时闸（默认 300 万不足单日 P0 批训）；非训练任务坚持确定性实现。",
        "3. **P1 主动训、P2 按需 + RAG 兜底**：P1 约 2 训练日（预授权闸内可 1 日）；P2 不全训，靠 RAG + 增量。",
        "4. **持续省 token 杠杆**：输出上限、变体去重、分片并发、确定性替代 AI、训练不走 RAG。", "",
        "## 附：估算假设与口径", "",
        f"- 单位成本取 P0 实测（表 ~{ct:,.0f}/张、子程序 ~{cs:,.0f}/个），P1/P2 沿用；实际随资产复杂度浮动。",
        f"- 分层按依赖图中心度 rank（与 P0 Top-N 一致）；P1 表 {TIERS['P1']['table_rank']}、包 {TIERS['P1']['unit_rank']}。",
        f"- 子程序/包保守估（P1 {TIERS['P1']['subprog_per_unit']}、P2 {TIERS['P2']['subprog_per_unit']}，P0 实测均 "
        f"{P0['p0_subprograms']/P0['p0_units']:.1f}），变体去重 {VARIANT_DEDUP:.0%}。",
        "- Token 台账为已核实数据，来源见 §1.1；确定性任务 0 token。",
    ]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="T3-4-3 Token 复盘与 P1/P2 排期")
    ap.add_argument("--out", default="docs/S3-4-3_Token复盘与P1P2排期.md")
    args = ap.parse_args(argv)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_report() + "\n", encoding="utf-8")
    print("Token 复盘与 P1/P2 排期：", out)
    print(f"Sprint3 合计 {total_tokens():,}；P1 估 {project_tier(TIERS['P1'], unit_cost(P0['table_tokens'], P0['table_n']), unit_cost(P0['subprog_tokens'], P0['subprog_n']))['tok_total']:,}")


if __name__ == "__main__":
    main()
