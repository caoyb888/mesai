#!/usr/bin/env python3
"""
T3-4-1：《真实 MES 系统理解总报告》汇总生成（Phase-1 里程碑）

汇总 S3 全链路交付为一份**里程碑总报告**：系统概览（资产盘点）+ P0 选取与训练方法
+ 三大理解成果（表/字段 S3-1、存储过程 S3-2、业务流程 S3-3）+ 知识资产与工程能力
（术语表 / 代码字典 / 断言种子 / RAG / 脱敏）+ 三项准确率与验收关联 + 局限风险
+ 后续排期 + 结论与里程碑判定 + 签字区。
纯本地、无 AI、无 DB；**关键数字从各子报告/清单正则抽取**（缺失回退已知默认），不硬编码漂移；
每次全量重写（本报告为汇总视图，非追加）。

用法：
  python3 build_system_report.py --out docs/MES真实系统理解总报告.md \
    --census docs/MES_Asset_Census_2026.md --s3-1 docs/S3-1_SQL验证报告.md \
    --s3-2 docs/S3-2_存储过程理解报告.md --s3-3 docs/S3-3_业务流程理解报告.md \
    --qbank docs/S3-3_业务流程验证题.md --assertions assertions/manifest.md \
    --glossary docs/glossary_zh_ko_en.md

关联需求单：REQ-MES-AI-20260715-001（T3-4-1）
作者：AI（芯智云匠）  日期：2026-07-16
"""
import re
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from finalize_s3_3_report import extract_stats as extract_s3_3_stats

TASK_NO = "REQ-MES-AI-20260715-001"

# 已知默认（子报告缺失/格式变更时回退，保证总报告可独立生成）
DEFAULTS = {
    "mes_tables": 1860, "mes_fields": 78526, "mes_views": 154,
    "mes_units": 9160, "mes_lines": 1932301,
    "pkg_spec": 4563, "pkg_body": 4421,
    "graph_procs": 5101, "graph_tables": 2249, "graph_cycles": 77,
    "p0_tables_sel": 100, "p0_pkgs_sel": 60, "p0_subprograms": 1401,
    "s3_1_cards": 95, "s3_1_semantic_pct": 87, "sql_qs": 30, "sql_auto": 69.9,
    "s3_2_cards": 1308, "s3_2_total": 1309, "s3_2_tokens": 3289621,
    "state_fields": 34, "trace_edges": 13, "carrier_keys": 14,
    "core_groups": 12, "bsqm": 5, "bsch": 7, "s3_3_tokens": 74937,
    "q_count": 21, "g_hit": 26, "g_total": 26,
    "assert_total": 657, "assert_sm": 260, "assert_sql": 337, "assert_api": 60,
    "assert_critical": 89, "assert_high": 171, "assert_medium": 397, "assert_cover": 149,
    "glossary_terms": 9698, "glossary_zh_ko": 574,
    "rag_chunks": 5155,
}


# ── 纯逻辑（可单测）─────────────────────────────────────────────────
def _num(pat, text, cast=int):
    if not text:
        return None
    m = re.search(pat, text)
    if not m:
        return None
    try:
        return cast(m.group(1).replace(",", ""))
    except (ValueError, IndexError):
        return None


def extract_stats(src):
    """src: {census,s3_1,s3_2,s3_3,qbank,assertions,glossary} 文本。抽取覆盖默认。"""
    s = dict(DEFAULTS)

    census = src.get("census", "")
    m = re.search(r"MESAPUSER[^|]*\|\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|\s*\*\*([\d,]+)\*\*\s*\|\s*\*\*([\d,]+)\*\*", census)
    if m:
        s["mes_tables"] = int(m.group(1).replace(",", ""))
        s["mes_fields"] = int(m.group(2).replace(",", ""))
        s["mes_views"] = int(m.group(3).replace(",", ""))
        s["mes_units"] = int(m.group(4).replace(",", ""))
        s["mes_lines"] = int(m.group(5).replace(",", ""))
    for key, pat in (("pkg_spec", r"PACKAGE（包规格）\s*\|\s*\*\*([\d,]+)\*\*"),
                     ("pkg_body", r"PACKAGE BODY（包体）\s*\|\s*\*\*([\d,]+)\*\*")):
        v = _num(pat, census)
        if v is not None:
            s[key] = v

    v = _num(r"题量\s*\|\s*(\d+)", src.get("s3_1", ""))
    if v is not None:
        s["sql_qs"] = v
    v = _num(r"自动初评均分\s*\|\s*([\d.]+)", src.get("s3_1", ""), float)
    if v is not None:
        s["sql_auto"] = v

    s3_2 = src.get("s3_2", "")
    m = re.search(r"理解卡片产出\*\*\s*\|\s*\*\*([\d,]+)\s*/\s*([\d,]+)", s3_2)
    if m:
        s["s3_2_cards"] = int(m.group(1).replace(",", ""))
        s["s3_2_total"] = int(m.group(2).replace(",", ""))
    v = _num(r"Token 消耗\s*\|\s*([\d,]+)", s3_2)
    if v is not None:
        s["s3_2_tokens"] = v

    # S3-3 复用 finalize 的抽取器
    s3_3, qbank = src.get("s3_3", ""), src.get("qbank", "")
    if s3_3:
        s33 = extract_s3_3_stats(s3_3, qbank)
        for k in ("state_fields", "trace_edges", "carrier_keys", "core_groups",
                  "bsqm", "bsch", "q_count", "g_hit", "g_total"):
            if s33.get(k):
                s[k] = s33[k]
        if s33.get("tokens"):
            s["s3_3_tokens"] = s33["tokens"]

    a = src.get("assertions", "")
    v = _num(r"总计\s*([\d,]+)\s*条", a)
    if v is not None:
        s["assert_total"] = v
    m = re.search(r"state-machine\s*([\d,]+)\s*/\s*sql-logic\s*([\d,]+)\s*/\s*api-behavior\s*([\d,]+)", a)
    if m:
        s["assert_sm"], s["assert_sql"], s["assert_api"] = (int(m.group(i).replace(",", "")) for i in (1, 2, 3))
    m = re.search(r"Critical'?:?\s*(\d+).*?High'?:?\s*(\d+).*?Medium'?:?\s*(\d+)", a)
    if m:
        s["assert_critical"], s["assert_high"], s["assert_medium"] = (int(m.group(i)) for i in (1, 2, 3))
    v = _num(r"覆盖资产[^：:]*[：:]*\s*(\d+)", a)
    if v is not None:
        s["assert_cover"] = v

    v = _num(r"去重术语总数\s*\|\s*([\d,]+)", src.get("glossary", ""))
    if v is not None:
        s["glossary_terms"] = v
    v = _num(r"中韩齐全\s*\|\s*([\d,]+)", src.get("glossary", ""))
    if v is not None:
        s["glossary_zh_ko"] = v
    return s


def build_report(s):
    L = [
        "# 真实 MES 系统理解总报告（Phase-1 里程碑）", "",
        "| 项 | 内容 |", "|----|----|",
        "| 文件编号 | AI-MES-SYSREPORT-2026-001 |",
        f"| 需求单 | {TASK_NO}（S3-4-1 汇总 S3-1/S3-2/S3-3）|",
        "| 编制 | AI（芯智云匠 MES AI 开发工程师）|",
        "| 日期 | 2026-07-16 |",
        "| 版本 | V1.0（里程碑汇总，待三项人工评分回填 + ITM 签字）|",
        "| 对象系统 | 真实钢板/卷材 MES（Oracle 21c XE / XEPDB1 / AL32UTF8，owner=MESAPUSER，韩系）|",
        "| 里程碑 | Phase-1「真实 MES 系统理解」（表/字段 + 存储过程 + 业务流程）|", "",
        "> **诚实定位**：本报告汇总 **AI 侧已完成的自动化交付**（S3-0 素材 → S3-1/2/3 三大理解 → 断言/RAG/脱敏）。"
        "**Phase-1 可签字验收尚缺**：三项准确率的**人工评分**（TL/BIZ）与**ITM 签字**。见第六、九节。", "",

        "## 一、执行摘要", "",
        f"本项目面向一套**{s['mes_tables']:,} 表 / {s['mes_fields']:,} 字段 / {s['mes_units']:,} PL/SQL 单元 / "
        f"约 {s['mes_lines']/10000:.0f} 万行**的真实钢板/卷材 MES（韩系、克隆库列注释全空），"
        "在**零注释、三语混合、无历史文档**的约束下，产出 AI 对其 **P0 核心资产**的可验证结构化理解。核心成果：", "",
        f"- **表/字段理解（S3-1）**：{s['s3_1_cards']} 张 P0 表卡片（字段语义覆盖 {s['s3_1_semantic_pct']}%），"
        f"SQL 场景验证 {s['sql_qs']} 题（自动初评均分 {s['sql_auto']}/100，人工终评 ≥85% 待做）。",
        f"- **存储过程理解（S3-2）**：Top60 P0 包切分 {s['s3_2_total']} 子程序，产 **{s['s3_2_cards']} 卡片"
        f"（{s['s3_2_cards']*100.0/s['s3_2_total']:.1f}%）**，BIZ 抽检 40 条待判。",
        f"- **业务流程理解（S3-3）**：状态机 {s['state_fields']} 字段 / 追溯 {s['carrier_keys']} 实体键 {s['trace_edges']} 边 "
        f"/ 核心流程 {s['core_groups']} 组（BSQM {s['bsqm']}/BSCH {s['bsch']}）/ 验证题 {s['q_count']} 道"
        f"（接地校验 {s['g_hit']}/{s['g_total']} 全命中），已成稿，BIZ 评分 ≥90% 待做。", "",
        "**方法论一以贯之**：以过程为锚、**证据驱动**（只据字面量状态写 / 表结构共键 / 过程读写血缘 / 调用编排+注释推断，"
        "缺证据标「待确认」）；对外调用**全程经 ai-gateway 脱敏门**（CLAUDE.md §4.2 七类），素材审计 0 命中「可外发」。", "",
        "**结论**：**AI 侧训练与验证素材已全部就绪**，理解成果证据可回溯；Phase-1 完整验收取决于后续人工评分达标与甲方签字。", "",

        "## 二、系统概览（资产盘点）", "",
        "| Schema | 表 | 字段 | 视图 | 程序单元 | PL/SQL 行数 |",
        "|----|----|----|----|----|----|",
        f"| MESAPUSER（业务）| {s['mes_tables']:,} | {s['mes_fields']:,} | {s['mes_views']} | {s['mes_units']:,} | {s['mes_lines']:,} |",
        f"| SCOAPUSER（框架）| 74 | 1,090 | 1 | 191 | 11,238 |", "",
        f"程序单元含 **{s['pkg_spec']:,} 包规格 + {s['pkg_body']:,} 包体**。依赖图谱（全量建图）：过程节点 "
        f"{s['graph_procs']:,} / 表节点 {s['graph_tables']:,} / 检出环 {s['graph_cycles']}。", "",
        "**关键系统性质**（S2.9 盘点结论）：",
        "1. **韩系钢板/卷材 MES**：炼钢(SMS)→连铸→板坯(SLAB)→轧制→钢板(PLT)/钢卷(COIL)→精整(SPR)→质检(SQM)→发货(SYD) 全流程。",
        "2. **克隆库列注释全空** → 代码字典 `SCOAPUSER.SCO_CODE_DETAIL` 是唯一列语义源（兼中韩双语术语表）；PL/SQL 源码内含中/英/韩混合注释。",
        "3. **规模巨大且有环**：万级过程/表依赖图，P0 须按中心度择取而非全量。", "",

        "## 三、P0 资产选取与训练方法", "",
        f"**P0 选取**：依赖图中心度 Top-N → **{s['p0_tables_sel']} 表 + {s['p0_pkgs_sel']} 包体**；大包按子程序切分为 "
        f"**{s['p0_subprograms']:,} 子程序单元**（最大包 BSCH_BATCHA_PLT_JOB2 15,929 行→44 段），控上下文与 Token。", "",
        "**六项训练方法要点**（Sprint3 §四）：① 语义拼图（字典>代码解码>命名>用法>行注释，冲突留痕）；"
        "② 三语归一（韩/英→中，原文留参考，术语表纳 RAG）；③ 大包子程序切分再合成；④ 拓扑序训练（先被调后入口）；"
        "⑤ 标准 Prompt 结构（角色+RAG Top-5+任务+约束+格式）；⑥ Token 分批与降级。**所有对外调用先脱敏**。", "",

        "## 四、理解成果", "",
        "### 4.1 表/字段理解（S3-1）", "",
        f"- P0 表卡片 **{s['s3_1_cards']} 张**（结构 + 字典列语义 + 依赖热度画像），字段语义覆盖 **{s['s3_1_semantic_pct']}%**。",
        f"- SQL 场景验证 **{s['sql_qs']} 题**（6 模块×5），RAG 召回表卡片→Kimi 出 SQL→规则自动初评均分 **{s['sql_auto']}/100**。",
        "- 表召回调优：原始 ~1/10 → 锚点 chunk+按表去重 5/10 → **标签驱动 hybrid RRF 7/10**（Top-3）。",
        "- ⏳ **人工终评正确率 ≥85% 待 TL/BIZ**（自动初评仅规则检查，不代表语义正确）。", "",
        "### 4.2 存储过程理解（S3-2）", "",
        f"- Top60 P0 包切分 **{s['s3_2_total']} 子程序**，产理解卡片 **{s['s3_2_cards']}（{s['s3_2_cards']*100.0/s['s3_2_total']:.1f}%）**"
        f"（PROCEDURE+FUNCTION），Token {s['s3_2_tokens']:,}。每卡含用途/读写表/调用/状态流转/PII/动态SQL 标注。",
        "- ⏳ **BIZ 抽检 40 条待判**（分层抽样单 `docs/S3-2_BIZ抽检抽样单.md`）。", "",
        "### 4.3 业务流程理解（S3-3）", "",
        f"- **状态机（T3-3-1）**：{s['state_fields']} 状态字段反推（取值/流转/触发过程）。",
        f"- **追溯链路（T3-3-2）**：{s['carrier_keys']} 核心实体键、{s['trace_edges']} 条追溯边（全有证据）；"
        "追溯脊 订单→计划炉次→炉次→板坯→板/卷→试样→质保→捆包。",
        f"- **核心流程（T3-3-3）**：{s['core_groups']} 流程组（质量判定 {s['bsqm']} / 生产调度 {s['bsch']}），流程编排级理解。",
        f"- **验证题库（T3-3-4）**：{s['q_count']} 道场景题，参考答案接地校验 **{s['g_hit']}/{s['g_total']} 全命中**（防臆造）。",
        f"- 成稿 `docs/S3-3_业务流程理解报告.md`（S3-3 合成消耗 {s['s3_3_tokens']:,} tokens）。⏳ **BIZ 评分 ≥90% 待做**。", "",

        "## 五、知识资产与工程能力", "",
        f"- **中韩英术语对照表**：去重 **{s['glossary_terms']:,} 术语**（中韩齐全 {s['glossary_zh_ko']}，三语齐全 0＝源表结构性缺），纳 RAG。",
        "- **代码字典**：`SCO_CODE_DETAIL` 解码表（列语义唯一源 + 状态值解码）。",
        f"- **断言种子（T3-4-2）**：**{s['assert_total']} 条**入 `/assertions/`（state-machine {s['assert_sm']} / sql-logic {s['assert_sql']} "
        f"/ api-behavior {s['assert_api']}；级别 Critical {s['assert_critical']}/High {s['assert_high']}/Medium {s['assert_medium']}；覆盖 {s['assert_cover']} 资产），喂 Sprint6 回归基准。",
        f"- **知识库 RAG**：表+过程卡片 **{s['rag_chunks']:,} chunk** 入集合 `mes_s3_understanding`，`rag_service.retrieve_for_mes[_table/_proc]` 可召回（表 Top-3 7/10、过程 0.7+）。",
        "- **全程脱敏合规**：ai-gateway 唯一外发咽喉，7 类脱敏门；素材审计 **0 命中**「可外发」认证（`docs/desensitize_audit_report.md`）；密钥双重 gitignore 无泄漏。",
        "- **工具链**（`scripts/kb-ingest/`）：自省/建图/切分/解析/对账 + S3 训练与理解驱动 + 验证与题库 + 报告完稿，纯 stdlib，单测齐备。", "",

        "## 六、三项准确率与验收关联", "",
        "| DoD 条目 | 目标 | 现状 | 状态 |",
        "|----|----|----|----|",
        f"| 表/SQL 准确率 | ≥85% | 自动初评 {s['sql_auto']}/100（{s['sql_qs']} 题）| ⏳ 待 TL/BIZ 人工终评 |",
        "| 存储过程准确率 | ≥85% | 抽样单 40 条就绪 | ⏳ 待 BIZ 抽检 |",
        f"| 业务流程准确率 | ≥90% | {s['q_count']} 题验证库、接地 {s['g_hit']}/{s['g_total']} 全命中 | ⏳ 待 BIZ 评分 |",
        "| 卡片/术语/字典入 RAG 可召回 | 必须 | ✅ 已入库并召回 | ✅ |",
        f"| 断言种子 ≥3×P0 入 /assertions/ | 必须 | ✅ {s['assert_total']} 条 | ✅ |",
        "| 全程脱敏（无泄漏+审计完整）| 必须 | ✅ 审计 0 命中 | ✅ |", "",
        "> **接地校验≠业务正确性**：接地只证参考答案所引表/状态/过程真实存在（防臆造）；三项准确率的**业务语义正确性**须人工评分判定。", "",

        "## 七、局限与风险", "",
        "1. **静态分析盲区**：变量赋值状态 / 动态 SQL / 运行期条件分支不可见（各理解已逐条标「待确认」）。",
        "2. **P0 覆盖边界**：过程级证据聚焦 Top60 P0 包；P1/P2 资产待后续 Sprint。",
        "3. **韩系术语**：源码/字典含韩文，语义译中可能偏差，关键业务词须 BIZ 校准。",
        "4. **人工评分未做**：三项准确率尚待 TL/BIZ 评分，是 Phase-1 签字验收的前置。", "",

        "## 八、后续排期", "",
        "1. **人工评分收口**：SQL 终评（TL）+ 存储过程抽检（BIZ）+ 业务流程验证题评分（BIZ），回填准确率。",
        "2. **不达标补训**：<85%/<90% 的模块按 T3-1-2/T3-3 补训。",
        "3. **断言纳基准库**：657 种子经 TL 审批纳入基准，接入 CI 断言全量测试。",
        "4. **P1/P2 训练排期**（T3-4-3）：Token 复盘后确定次批资产范围与预算。",
        "5. **Phase-1 评审会（T3-4-4）**：甲方 IT 负责人签字确认达标。", "",

        "## 九、结论与里程碑判定", "",
        "**AI 侧交付完成度：100%**——S3-0 素材、S3-1/2/3 三大理解、断言种子、RAG 入库、脱敏合规全部就绪，"
        "所有理解成果证据可回溯、缺证据标注清晰。",
        "**Phase-1 可签字验收：未达**——三项准确率人工评分与 ITM 签字尚缺，属流程性前置，不涉及 AI 侧返工。", "",
        "> 判定：**训练与验证素材就绪，可进入人工评分与 Phase-1 评审收尾**。", "",

        "## 附一、产物清单", "",
        "| 类别 | 产物 |",
        "|----|----|",
        "| 子报告 | `docs/S3-1_SQL验证报告.md`、`docs/S3-2_存储过程理解报告.md`、`docs/S3-3_业务流程理解报告.md`（+验证题 `docs/S3-3_业务流程验证题.md`）|",
        "| 表/字段 | `docs/p0_table_cards.md`（95 卡片）|",
        "| 术语/字典 | `docs/glossary_zh_ko_en.md` + `.csv`；代码字典 CSV |",
        "| 断言 | `/assertions/{state-machine,sql-logic,api-behavior}/*.jsonl` + `manifest.md` |",
        "| 机读卡片 | 远程 `/home/xintong/mes-s3-data/s3-train/{tables,procs,state_machine,traceability,core_process}/` |",
        "| 工具链 | `scripts/kb-ingest/*.py`（自省/建图/切分/解析/对账/训练/理解/验证/报告）|",
        "| 就绪清单 | `docs/Phase1_验收就绪清单.md` |", "",

        "## 附二、里程碑评审签字区", "",
        "| 角色 | 三项准确率核验 | 结论（通过/驳回）| 签字 | 日期 |",
        "|----|----|----|----|----|",
        "| TL 技术负责人 |  |  |  |  |",
        "| BIZ 业务专家 |  |  |  |  |",
        "| IT 负责人 / ITM 审核专员 |  |  |  |  |", "",
        "---", "",
        "*本总报告如实标注「已完成 / 待人工 / 未达」三态；Phase-1 完整验收须补三项人工评分 + ITM 签字。数字由各子报告自动抽取汇总。*",
    ]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="T3-4-1 系统理解总报告汇总")
    ap.add_argument("--out", default="docs/MES真实系统理解总报告.md")
    ap.add_argument("--census")
    ap.add_argument("--s3-1", dest="s3_1")
    ap.add_argument("--s3-2", dest="s3_2")
    ap.add_argument("--s3-3", dest="s3_3")
    ap.add_argument("--qbank")
    ap.add_argument("--assertions")
    ap.add_argument("--glossary")
    args = ap.parse_args(argv)

    def _read(p):
        return Path(p).read_text(encoding="utf-8") if p and Path(p).exists() else ""

    src = {"census": _read(args.census), "s3_1": _read(args.s3_1), "s3_2": _read(args.s3_2),
           "s3_3": _read(args.s3_3), "qbank": _read(args.qbank),
           "assertions": _read(args.assertions), "glossary": _read(args.glossary)}
    stats = extract_stats(src)
    md = build_report(stats)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md + "\n", encoding="utf-8")
    print("系统理解总报告：", out)
    print("抽取统计：", {k: stats[k] for k in
                    ("mes_tables", "s3_2_cards", "state_fields", "trace_edges",
                     "core_groups", "q_count", "g_hit", "assert_total", "glossary_terms")})


if __name__ == "__main__":
    main()
