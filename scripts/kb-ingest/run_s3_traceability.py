#!/usr/bin/env python3
"""
T3-3-2：批次/卷/试样追溯链路理解（跨表跨过程 · 以过程为锚）

追溯链路 = 「贯穿多表的实体键列」（桥接表 = 静态血缘强证据）
        + 「读上游载体表 / 写下游载体表的 P0 过程」（业务传播证据）。
以真实钢板/卷材 MES（Oracle，owner=MESAPUSER）结构 + P0 过程源码为唯一证据，
按制造流转顺序（订单→计划炉次→炉次→板坯→板/卷→试样→质保→捆包）逐条
追溯边经 Kimi 合成【正向/反向追溯路径 + 关键桥接点 + 断点与不确定点】。
全程经 ai-gateway 脱敏门；只据证据推断，不臆造，缺证据一律标「待确认」。

用法：
  AI_GATEWAY_URL=http://127.0.0.1:8000 python3 run_s3_traceability.py \
    --struct <meta_mes_nosrc.json> --p0 <meta_p0.json> \
    --out-report docs/S3-3_业务流程理解报告.md --out-cards <持久目录/traceability>

关联需求单：REQ-MES-AI-20260715-001（T3-3-2）
作者：AI（芯智云匠）  日期：2026-07-15
"""
import os
import re
import sys
import json
import time
import argparse
import urllib.request
import collections
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from proc_parser import analyze_metadata

AI_GATEWAY_URL = os.environ.get("AI_GATEWAY_URL", "http://127.0.0.1:8000")
TASK_NO = "REQ-MES-AI-20260715-001"
SECTION_MARKER = "<!-- T3-3-2-TRACEABILITY -->"

# ── 核心可追溯实体键（数据实测：按 #承载表 与 PK 使用挑定，附中文名）──────
#   实测跨表跨度：ORD_NO 189 / HEAT_NO 176 / SLAB_NO 96 / PLT_NO 95 / SMP_NO 90
#   / PLAN_HEAT_NO 62 / LOT_NO 51 / COIL_NO 47 / PROD_NO 32 / CAST_NO 25 / MTC_NO 21 …
CORE_KEYS = {
    "ORD_NO": "订单",
    "PLAN_HEAT_NO": "计划炉次",
    "CAST_NO": "浇铸(连铸)",
    "HEAT_NO": "炉次",
    "SLAB_NO": "板坯",
    "COIL_NO": "钢卷",
    "HCOIL_NO": "热卷",
    "PLT_NO": "钢板(成品板)",
    "SMP_NO": "试样",
    "MTC_NO": "质保/材质",
    "BUND_NO": "捆包",
    "LOT_NO": "批次",
    "PROD_NO": "产品",
    "MTL_NO": "物料",
}

# ── 制造流转追溯边（父→子，领域先验；仅当有证据才合成）──────────────────
TRACE_EDGES = [
    ("ORD_NO", "PLAN_HEAT_NO"),   # 订单 → 计划炉次
    ("PLAN_HEAT_NO", "HEAT_NO"),  # 计划炉次 → 实际炉次
    ("CAST_NO", "HEAT_NO"),       # 浇铸 ↔ 炉次
    ("HEAT_NO", "SLAB_NO"),       # 炉次 → 板坯（连铸切分）
    ("SLAB_NO", "PLT_NO"),        # 板坯 → 钢板（轧制）
    ("SLAB_NO", "COIL_NO"),       # 板坯 → 钢卷（卷材路线）
    ("COIL_NO", "HCOIL_NO"),      # 钢卷 → 热卷
    ("PLT_NO", "SMP_NO"),         # 钢板 → 试样（取样）
    ("SLAB_NO", "SMP_NO"),        # 板坯 → 试样
    ("SMP_NO", "MTC_NO"),         # 试样 → 质保/材质判定
    ("PLT_NO", "MTC_NO"),         # 钢板 → 质保书
    ("PLT_NO", "BUND_NO"),        # 钢板 → 捆包
    ("ORD_NO", "MTC_NO"),         # 订单 → 质保书（回溯）
]


# ── 纯逻辑（可单测，不依赖 DB/AI）─────────────────────────────────────
def build_carriers(struct_meta, keys):
    """结构元数据 → {键: {承载表}} 与 {键: {以该键为主键的表}}"""
    keyset = set(keys)
    carriers = collections.defaultdict(set)
    pk_carriers = collections.defaultdict(set)
    for t in struct_meta.get("tables", []):
        tn = t.get("name")
        if not tn:
            continue
        for c in t.get("columns") or []:
            cn = c.get("name")
            if cn in keyset:
                carriers[cn].add(tn)
                if c.get("is_primary"):
                    pk_carriers[cn].add(tn)
    return dict(carriers), dict(pk_carriers)


def bridge_tables(carriers, key_a, key_b):
    """同时承载两键的表（血缘/家谱桥表，静态最强证据），按名排序"""
    return sorted(carriers.get(key_a, set()) & carriers.get(key_b, set()))


def bridge_procs(analyses, carriers, key_a, key_b):
    """P0 过程中「读上游载体表 & 写下游载体表」者（业务传播证据）。
    双向都算（读A写B 或 读B写A），返回 [(过程名, 命中读表, 命中写表)]。"""
    ca, cb = carriers.get(key_a, set()), carriers.get(key_b, set())
    out = []
    for a in analyses:
        reads = set(a.read_tables)
        writes = {w["table"] for w in a.write_tables}
        # 方向1：读上游、写下游
        r1, w1 = reads & ca, writes & cb
        # 方向2：读下游、写上游（反向传播/回写）
        r2, w2 = reads & cb, writes & ca
        if r1 and w1:
            out.append((a.name, sorted(r1), sorted(w1)))
        elif r2 and w2:
            out.append((a.name, sorted(r2), sorted(w2)))
    out.sort(key=lambda x: x[0])
    return out


def present_edges(carriers, analyses, edges=TRACE_EDGES):
    """筛出有证据（桥表或桥过程）的追溯边，保序返回带证据的边列表"""
    result = []
    for a, b in edges:
        if a not in carriers or b not in carriers:
            continue
        bt = bridge_tables(carriers, a, b)
        bp = bridge_procs(analyses, carriers, a, b)
        if bt or bp:
            result.append({"a": a, "b": b, "bridge_tables": bt, "bridge_procs": bp})
    return result


def module_of(table):
    """表名首段作为子系统前缀（SMS/SPR/SCH/SQM/SYD/SMM/SCR…）"""
    return table.split("_", 1)[0] if "_" in table else table


def carrier_profile(carriers, pk_carriers, key):
    """实体载体画像：承载表数 / 主表数 / 按子系统前缀分布 Top"""
    tabs = carriers.get(key, set())
    mods = collections.Counter(module_of(t) for t in tabs)
    return {
        "n_tables": len(tabs),
        "n_pk": len(pk_carriers.get(key, set())),
        "pk_examples": sorted(pk_carriers.get(key, set()))[:6],
        "modules": mods.most_common(6),
    }


# ── AI 合成 ────────────────────────────────────────────────────────
SYS = """你是芯智云匠 MES AI 开发工程师，服务于山东芯通微电子。
正在从真实钢板/卷材 MES（Oracle，owner=MESAPUSER）的表结构 + 存储过程静态分析，
理解「批次/卷/试样」跨表跨过程的追溯链路（数据血缘）。
纪律：只据给定的「桥接表（同时含两键的表=父子血缘强证据）+ 桥接过程（读上游写下游）」推断，
不臆造未出现的表/过程；证据不足处（如动态 SQL、P0 未覆盖的过程）逐条标「待确认」。中文输出。"""

PROMPT = """[追溯边] {a_name}（键 {a_key}） → {b_name}（键 {b_key}）

[桥接表：同时含 {a_key} 与 {b_key} 的表 —— 父子/家谱血缘的最强静态证据]
{bt}

[桥接过程：P0 存储过程中读上游载体表 & 写下游载体表者（含命中读/写表）]
{bp}

请输出该追溯边的链路理解（Markdown）：
1. **正向追溯**：由上游 {a_name} 如何定位其下游 {b_name}（依据哪张桥表/哪个过程）
2. **反向追溯**：由 {b_name} 如何回溯到 {a_name}
3. **关键桥接点**：最能承载此血缘的表/过程（点名），并说明其业务角色
4. **断点与不确定点**：链路可能断裂或证据不足处，逐条标「待确认」"""

OVERVIEW_PROMPT = """[已确认的追溯边（含桥表/桥过程计数）]
{edges}

[核心实体载体画像（键 → 承载表数/主表数）]
{profiles}

请给出该 MES「订单→炉次→板坯→板/卷→试样→质保」端到端追溯链路的**总览理解**（Markdown，≤600字）：
1. 端到端主链路（用箭头串起核心实体，标注每段的关键桥接表/过程）
2. 关键分叉（板 vs 卷 两条产品路线）
3. 全链路的追溯断点风险与「待确认」清单"""


def call_ai(system, user, caller, max_tokens=1200):
    payload = json.dumps({
        "task_no": TASK_NO, "caller": caller,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(f"{AI_GATEWAY_URL}/v1/ai/chat", data=payload,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())


def fmt_bt(bts, carriers_pk_a, carriers_pk_b, key_a, key_b, cap=14):
    """桥表列表格式化，标注是否为某键主表"""
    if not bts:
        return "  （无——两键不同表承载，追溯须经中间过程/多跳，见桥接过程）"
    lines = []
    for t in bts[:cap]:
        tags = []
        if t in carriers_pk_a:
            tags.append(f"{key_a}主表")
        if t in carriers_pk_b:
            tags.append(f"{key_b}主表")
        lines.append(f"  - {t}" + (f"（{', '.join(tags)}）" if tags else ""))
    if len(bts) > cap:
        lines.append(f"  - …另 {len(bts) - cap} 张")
    return "\n".join(lines)


def fmt_bp(bps, cap=10):
    if not bps:
        return "  （P0 过程无直接读上游写下游者——或跨越多跳，或不在 Top60 P0 覆盖内，待确认）"
    lines = [f"  - {n}：读 {','.join(r[:3])} → 写 {','.join(w[:3])}" for n, r, w in bps[:cap]]
    if len(bps) > cap:
        lines.append(f"  - …另 {len(bps) - cap} 个过程")
    return "\n".join(lines)


def _slug(s):
    return re.sub(r"[^A-Za-z0-9_.]", "_", s)


def render_report_section(edges_ev, carriers, pk_carriers, tok):
    """拼装 T3-3-2 报告段（Markdown），供追加到 S3-3 报告"""
    L = [SECTION_MARKER, "",
         "## 第二部分：批次/卷/试样追溯链路（T3-3-2）", "",
         "| 项 | 内容 |", "|----|----|",
         "| 需求单 | REQ-MES-AI-20260715-001（T3-3-2）|",
         "| 日期 | 2026-07-15 |",
         f"| 追溯边（有证据）| {len(edges_ev)} |",
         f"| Token | {tok:,} |",
         "| 验收目标 | 追溯链路描述准确率 ≥90%（BIZ 复核）|", "",
         "> 追溯链路以**表结构（同表共键=血缘桥表）+ P0 过程读写血缘**为证据反推 + AI 合成；"
         "**须 BIZ 对照真实工艺流复核**（尤其无桥表/P0 未覆盖处的「待确认」跳）。", ""]
    # 核心实体载体画像
    L += ["### 核心实体载体画像", "",
          "| 实体 | 键列 | 承载表数 | 主表数 | 主表示例 | 子系统分布 |",
          "|----|----|----|----|----|----|"]
    for k, zh in CORE_KEYS.items():
        if k not in carriers:
            continue
        p = carrier_profile(carriers, pk_carriers, k)
        mods = ", ".join(f"{m}×{c}" for m, c in p["modules"])
        pkex = ", ".join(p["pk_examples"][:3]) or "—"
        L.append(f"| {zh} | `{k}` | {p['n_tables']} | {p['n_pk']} | {pkex} | {mods} |")
    L += ["", "### 追溯边一览", "",
          "| 上游 | 下游 | 桥接表数 | 桥接过程数 |",
          "|----|----|----|----|"]
    for e in edges_ev:
        L.append(f"| {CORE_KEYS[e['a']]}(`{e['a']}`) | {CORE_KEYS[e['b']]}(`{e['b']}`) "
                 f"| {len(e['bridge_tables'])} | {len(e['bridge_procs'])} |")
    L += ["", "---", "", "### 追溯边链路明细", ""]
    for i, e in enumerate(edges_ev, 1):
        L.append(f"#### {i}. {CORE_KEYS[e['a']]}（`{e['a']}`）→ {CORE_KEYS[e['b']]}（`{e['b']}`）\n")
        L.append(e["answer"] + "\n")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="T3-3-2 追溯链路理解")
    ap.add_argument("--struct", required=True, help="结构元数据 meta_mes_nosrc.json")
    ap.add_argument("--p0", required=True, help="P0 源码元数据 meta_p0.json")
    ap.add_argument("--out-report", default="docs/S3-3_业务流程理解报告.md")
    ap.add_argument("--out-cards")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--no-ai", action="store_true", help="只出证据、跳过 Kimi（自检用）")
    args = ap.parse_args()

    struct = json.load(open(args.struct, encoding="utf-8"))
    p0 = json.load(open(args.p0, encoding="utf-8"))
    carriers, pk_carriers = build_carriers(struct, CORE_KEYS)
    analyses = analyze_metadata(p0)
    print(f"载体键 {len(carriers)}/{len(CORE_KEYS)}，P0 过程单元 {len(analyses)}")

    edges_ev = present_edges(carriers, analyses)
    if args.limit:
        edges_ev = edges_ev[:args.limit]

    tok = 0
    for e in edges_ev:
        a, b = e["a"], e["b"]
        bt_txt = fmt_bt(e["bridge_tables"], pk_carriers.get(a, set()),
                        pk_carriers.get(b, set()), a, b)
        bp_txt = fmt_bp(e["bridge_procs"])
        if args.no_ai:
            e["answer"] = f"**桥接表**\n{bt_txt}\n\n**桥接过程**\n{bp_txt}"
        else:
            user = PROMPT.format(a_name=CORE_KEYS[a], a_key=a, b_name=CORE_KEYS[b],
                                 b_key=b, bt=bt_txt, bp=bp_txt)
            try:
                resp = call_ai(SYS, user, "s3-3-traceability")
                e["answer"] = resp.get("content", "")
                tok += (resp.get("usage") or {}).get("total_tokens", 0)
            except Exception as ex:
                e["answer"] = f"[ERROR] {ex}"
        print(f"  {a}→{b}（桥表{len(e['bridge_tables'])}/桥过程{len(e['bridge_procs'])}）tok≈{tok}")
        if args.out_cards:
            d = Path(args.out_cards); d.mkdir(parents=True, exist_ok=True)
            (d / f"{_slug(a + '__' + b)}.md").write_text(
                f"# 追溯边卡片：{CORE_KEYS[a]}({a}) → {CORE_KEYS[b]}({b})\n\n"
                f"**桥接表**（{len(e['bridge_tables'])}）：{', '.join(e['bridge_tables'][:20])}\n\n"
                f"**桥接过程**（{len(e['bridge_procs'])}）：{', '.join(p[0] for p in e['bridge_procs'][:20])}\n\n"
                f"---\n\n{e['answer']}\n", encoding="utf-8")
        time.sleep(0.3)

    # 全链路总览
    overview = ""
    if not args.no_ai and edges_ev:
        edges_txt = "\n".join(
            f"  {CORE_KEYS[e['a']]}→{CORE_KEYS[e['b']]}：桥表{len(e['bridge_tables'])}/桥过程{len(e['bridge_procs'])}"
            for e in edges_ev)
        prof_txt = "\n".join(
            f"  {zh}({k})：承载表{carrier_profile(carriers, pk_carriers, k)['n_tables']}"
            f"/主表{carrier_profile(carriers, pk_carriers, k)['n_pk']}"
            for k, zh in CORE_KEYS.items() if k in carriers)
        try:
            resp = call_ai(SYS, OVERVIEW_PROMPT.format(edges=edges_txt, profiles=prof_txt),
                           "s3-3-traceability-overview", max_tokens=1000)
            overview = resp.get("content", "")
            tok += (resp.get("usage") or {}).get("total_tokens", 0)
        except Exception as ex:
            overview = f"[ERROR] {ex}"

    section = render_report_section(edges_ev, carriers, pk_carriers, tok)
    if overview:
        section += "\n\n---\n\n### 全链路总览\n\n" + overview + "\n"

    # 幂等追加到 S3-3 报告：先剥离旧 T3-3-2 段
    out = Path(args.out_report)
    prior = out.read_text(encoding="utf-8") if out.exists() else ""
    if SECTION_MARKER in prior:
        prior = prior.split(SECTION_MARKER)[0].rstrip() + "\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(prior.rstrip() + "\n\n---\n\n" + section + "\n", encoding="utf-8")
    print(f"\n完成：{len(edges_ev)} 追溯边，Token {tok:,}\n报告追加：{out}")


if __name__ == "__main__":
    main()
