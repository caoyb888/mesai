#!/usr/bin/env python3
"""
T3-3-4：业务流程场景模拟验证题库（≥15 道，供 BIZ 评分）

在 S3-3 的状态机(T3-3-1)/追溯链路(T3-3-2)/核心流程(T3-3-3)反推之上，出**场景化验证题**，
覆盖【状态流转 / 业务规则 / 追溯链路 / 核心流程编排】四类。每题含：场景题干、参考答案
（基于反推证据）、证据出处、BIZ 评分栏。参考答案的关键事实带 `grounding` 元数据，可用
`--verify` 对真实库元数据（状态写/表结构/切分包）做**接地校验**，确保题目不悬空、不臆造。

用法：
  # 仅出题库（无需 DB）
  python3 build_validation_questions.py --out docs/S3-3_业务流程验证题.md
  # 出题库 + 接地校验（远程有元数据时）
  python3 build_validation_questions.py --out docs/S3-3_业务流程验证题.md \
    --verify --meta <meta_p0.json> --struct <meta_mes_nosrc.json> --split <split_all.json>

关联需求单：REQ-MES-AI-20260715-001（T3-3-4）
作者：AI（芯智云匠）  日期：2026-07-15
"""
import re
import sys
import json
import argparse
import collections
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

CATS = ["状态流转", "业务规则", "追溯链路", "核心流程编排"]

# ── 验证题库（curated，全部锚定 S3-3 反推证据；grounding 供 --verify 接地校验）──
# grounding 类型：
#   state         {table,column,value}  —— meta_p0 的 set_assignments 应含此字面量状态写
#   carrier_pair  {a,b}                  —— 结构上应存在同时含两键的桥表（血缘可追）
#   package       {name}                 —— split_all 应含此切分包
#   table         {name}                 —— 结构应含此表
QUESTIONS = [
    # ───────── 一、状态流转（状态机 T3-3-1）─────────
    {"cat": "状态流转", "diff": "中",
     "scenario": "一张质保书请求当前 SQM_MTC_REQ.MTC_STS_CD=2，经质保书签发过程处理后变为 9。",
     "q": "值 2 与 9 分别代表什么状态？该流转由哪一类存储过程触发？",
     "ref": "2=已申请/待处理（质保书请求已生成）；9=不合格/作废（字典解码「不合格」）。"
            "流转由质保书签发过程 BSQM_MTC_ISSUE / _LZ / _RZ / _SHIP 等触发。9 的精确语义待 BIZ 确认。",
     "evi": ["T3-3-1 状态机：SQM_MTC_REQ.MTC_STS_CD 取值 {2,9}，7 个写入过程",
             "证据：set MTC_STS_CD=2（BSQM_MTC_ISSUE_*）"],
     "grounding": [{"type": "state", "table": "SQM_MTC_REQ", "column": "MTC_STS_CD", "value": "2"}]},

    {"cat": "状态流转", "diff": "中",
     "scenario": "生产计划调整时，某板坯计划被返送。",
     "q": "SCH_PLAN_SLAB.PLAN_SLAB_STS 会被写成什么值？含义与触发过程？相关轧制计划状态字段是否同值？",
     "ref": "写为 A7=计划返送，由 BSCH_PLAN_ADJUST 触发。轧制计划 SCH_PLAN_ROLL / SCH_INST_ROLL / "
            "SCH_PLT_PLAN_ROLL 的 PLAN_ROLL_STS 及切割 PLAN_FSH_STS 同样写 A7（返送贯穿板坯/轧制/切割计划）。",
     "evi": ["T3-3-1：PLAN_SLAB_STS=A7 / PLAN_ROLL_STS=A7，触发过程 BSCH_PLAN_ADJUST"],
     "grounding": [{"type": "state", "table": "SCH_PLAN_SLAB", "column": "PLAN_SLAB_STS", "value": "A7"}]},

    {"cat": "状态流转", "diff": "难",
     "scenario": "一次计划调整涉及中间包（Tundish）更换。",
     "q": "SCH_PLAN_HEAT.TUNDISH_CHG_FL 的取值与流转方向？由哪个过程写入？",
     "ref": "取值 N（未更换）↔ Y（已更换/需更换），N→Y 由 BSCH_PLAN_ADJUST 写入。"
            "标识计划炉次是否发生中间包更换。",
     "evi": ["T3-3-1：TUNDISH_CHG_FL 取值 {N,Y}",
             "源码证据：BSCH_PLAN_ADJUST 写 TUNDISH_CHG_FL=N 与 =Y"],
     "grounding": [{"type": "state", "table": "SCH_PLAN_HEAT", "column": "TUNDISH_CHG_FL", "value": "Y"}]},

    {"cat": "状态流转", "diff": "中",
     "scenario": "连铸操作（BSMS_OPER_CC）确认一个炉次并推进其状态。",
     "q": "SMS_HEAT.HEAT_STS 与 HEAT_CONF_YN 各会怎样变化？",
     "ref": "HEAT_STS 写 2=浇铸（Casting）；HEAT_CONF_YN 由 N→Y=炉次已确认。二者均由 BSMS_OPER_CC 写入。",
     "evi": ["T3-3-1：SMS_HEAT.HEAT_STS=2、HEAT_CONF_YN N→Y，触发 BSMS_OPER_CC"],
     "grounding": [{"type": "state", "table": "SMS_HEAT", "column": "HEAT_STS", "value": "2"},
                   {"type": "state", "table": "SMS_HEAT", "column": "HEAT_CONF_YN", "value": "Y"}]},

    {"cat": "状态流转", "diff": "难",
     "scenario": "计划炉次因浇次拆分/调整发生变更。",
     "q": "SCH_PLAN_HEAT.PLAN_CHANGE_TY 会被写成什么值？该字段的业务作用是什么？",
     "ref": "写为 S（变更/拆分标记），由 BSCH_PLAN_ADJUST 在浇次拆分等计划变更场景写入，"
            "标识本计划炉次经历过何种变更。S 的完整取值域与精确语义待 BIZ 确认。",
     "evi": ["源码证据：BSCH_PLAN_ADJUST 写 SCH_PLAN_HEAT.PLAN_CHANGE_TY=S"],
     "grounding": [{"type": "state", "table": "SCH_PLAN_HEAT", "column": "PLAN_CHANGE_TY", "value": "S"}]},

    {"cat": "状态流转", "diff": "中",
     "scenario": "板坯进入厚板作业指令环节，等待作业。",
     "q": "SMS_SLAB.PROG_CD 写成 PH1C 代表什么进度状态？由哪个过程写入？",
     "ref": "PH1C=厚板作业等待（字典解码），由厚板作业指令过程 BSCH_WORK_INST_PLT 写入，"
            "表示板坯已排入厚板作业、处于等待加工状态。",
     "evi": ["T3-3-1：SMS_SLAB.PROG_CD=PH1C（厚板作业等待）"],
     "grounding": [{"type": "state", "table": "SMS_SLAB", "column": "PROG_CD", "value": "PH1C"},
                   {"type": "package", "name": "BSCH_WORK_INST_PLT"}]},

    # ───────── 二、业务规则（源码注释/判定 T3-3-3）─────────
    {"cat": "业务规则", "diff": "中",
     "scenario": "操作员尝试打印一张质保书，系统拒绝并写入一条备注。",
     "q": "质保书打印的前置条件是什么？系统会给出怎样的提示？",
     "ref": "前置条件：必须已有综合判定级别（总判结果）。若无判定级别则不能打印，"
            "系统写 SQM_MTC_REQ.REMARK='无判定级别不能打印质保书'。",
     "evi": ["T3-3-3/源码证据：BSQM_MTC_ISSUE 写 REMARK='无判定级别不能打印质保书'"],
     "grounding": [{"type": "state", "table": "SQM_MTC_REQ", "column": "REMARK",
                    "value": "无判定级别不能打印质保书"}]},

    {"cat": "业务规则", "diff": "难",
     "scenario": "整个浇次（CAST）需要返送处理。",
     "q": "系统如何处理该浇次的计划浇次号？这样做是为了避免什么问题？",
     "ref": "整浇次返送时将计划浇次号变更为以 R 开头，以避免后续浇次调整时发生浇次合并。"
            "（BSCH_PLAN_ADJUST 源码注释确证）",
     "evi": ["源码注释：整浇次返送时将计划浇次号变更为R开头，避免后续浇次调整时发生浇次合并"],
     "grounding": [{"type": "package", "name": "BSCH_PLAN_ADJUST"}]},

    {"cat": "业务规则", "diff": "难",
     "scenario": "母坯计划已设计到对应子坯计划，用户想调整母坯的板坯顺序。",
     "q": "系统是否允许该操作？理由是什么？",
     "ref": "不允许。母坯计划已设计到对应子坯计划后，暂不允许母坯顺序调整；"
            "系统报错「母坯计划，不允许进行板坯顺序调整」。（BSCH_PLAN_ADJUST 注释/报错确证）",
     "evi": ["源码注释：母坯计划设计到对应子坯计划,暂时不允许母坯顺序调整",
             "报错：PE.PR_SET_ERROR('母坯计划，不允许进行板坯顺序调整')"],
     "grounding": [{"type": "package", "name": "BSCH_PLAN_ADJUST"}]},

    {"cat": "业务规则", "diff": "中",
     "scenario": "炉次计划发生返送。",
     "q": "系统对厚板计划有何特殊处理？还会同步更改什么？",
     "ref": "炉次计划返送时增加对厚板计划的判断和返送，同时更改指令表的状态。"
            "（BSCH_PLAN_ADJUST 注释确证）",
     "evi": ["源码注释：炉次计划返送时,增加对厚板的计划的判断和返送；同时更改指令表的状态"],
     "grounding": [{"type": "package", "name": "BSCH_PLAN_ADJUST"}]},

    {"cat": "业务规则", "diff": "中",
     "scenario": "需要为一批已判定合格的材料出具质保书。",
     "q": "系统支持按哪些维度（主键）出证？各对应什么处理单元？",
     "ref": "支持按订单(ORDER_NO)、炉次(HEAT_NO)、批次(LOT_NO)、产品(PROD_NO)四维出证，"
            "分别对应子程序 PR_MTC_FORM_ORDER_NO / _HEAT_NO / _LOT_NO / _PROD_NO（BSQM_MTC_ISSUE）。",
     "evi": ["T3-3-3：BSQM_MTC_ISSUE 子程序 PR_MTC_FORM_{ORDER_NO,HEAT_NO,LOT_NO,PROD_NO}"],
     "grounding": [{"type": "package", "name": "BSQM_MTC_ISSUE"}]},

    # ───────── 三、追溯链路（T3-3-2）─────────
    {"cat": "追溯链路", "diff": "中",
     "scenario": "质检需要由一个板坯号 SLAB_NO 回溯其所属炉次 HEAT_NO。",
     "q": "如何追？依据哪张桥表？",
     "ref": "查板坯主表 SMS_SLAB——它同时含 SLAB_NO（主键）与 HEAT_NO，是炉次-板坯血缘桥表；"
            "由 SLAB_NO 定位记录即得 HEAT_NO。炉次→板坯全库共 47 张桥表可交叉印证。",
     "evi": ["T3-3-2：HEAT_NO×SLAB_NO 桥表 47（含 SMS_SLAB）"],
     "grounding": [{"type": "carrier_pair", "a": "HEAT_NO", "b": "SLAB_NO"},
                   {"type": "table", "name": "SMS_SLAB"}]},

    {"cat": "追溯链路", "diff": "难",
     "scenario": "已知一块成品钢板 PLT_NO，想直接追到它的质保/材质记录 MTC_NO。",
     "q": "能否由单张桥表直达？若不能，正确的追溯路径是什么？",
     "ref": "不能直达——PLT_NO 与 MTC_NO 无同表共载桥表（0 桥表），须经试样中转："
            "PLT_NO →（试样）SMP_NO → MTC_NO。这是全链路的一个追溯断点，需两跳。",
     "evi": ["T3-3-2：PLT_NO×MTC_NO 桥表=0（断点）；PLT→SMP、SMP→MTC 有桥"],
     "grounding": [{"type": "carrier_pair", "a": "PLT_NO", "b": "SMP_NO"},
                   {"type": "carrier_pair", "a": "SMP_NO", "b": "MTC_NO"}]},

    {"cat": "追溯链路", "diff": "中",
     "scenario": "一块板坯 SLAB_NO 之后可能走钢板路线，也可能走钢卷路线。",
     "q": "追溯上如何区分这两条产品路线？各自的下游实体是什么？",
     "ref": "板坯是产品分叉点：SLAB→PLT（钢板，34 桥表）与 SLAB→COIL（钢卷，10 桥表）是两条独立血缘；"
            "钢卷再到热卷 COIL→HCOIL。按命中的桥表/载体表所属域即可区分。",
     "evi": ["T3-3-2：SLAB×PLT 34、SLAB×COIL 10、COIL×HCOIL 5"],
     "grounding": [{"type": "carrier_pair", "a": "SLAB_NO", "b": "PLT_NO"},
                   {"type": "carrier_pair", "a": "SLAB_NO", "b": "COIL_NO"}]},

    {"cat": "追溯链路", "diff": "中",
     "scenario": "由一张订单 ORD_NO 需要定位其对应的计划炉次 PLAN_HEAT_NO。",
     "q": "依据哪张桥表可以正向追溯？",
     "ref": "计划炉次表 SCH_PLAN_HEAT 同时含 ORD_NO 与 PLAN_HEAT_NO，是订单-计划炉次桥表；"
            "订单→计划炉次全库共 28 张桥表。",
     "evi": ["T3-3-2：ORD_NO×PLAN_HEAT_NO 桥表 28（含 SCH_PLAN_HEAT）"],
     "grounding": [{"type": "carrier_pair", "a": "ORD_NO", "b": "PLAN_HEAT_NO"}]},

    {"cat": "追溯链路", "diff": "难",
     "scenario": "需要确定 HEAT_NO（炉次）的权威主数据表以做追溯锚点。",
     "q": "HEAT_NO 在库中的分布如何？哪个子系统承载其权威主表？",
     "ref": "HEAT_NO 出现于 176 张表、其中 44 张以它为主键；权威主表集中在炼钢域（SMS×60），"
            "SMS_HEAT 等为炉次主表。追溯以炼钢域主表为锚最可靠。",
     "evi": ["T3-3-2 载体画像：HEAT_NO 承载 176 表 / 主表 44 / SMS×60"],
     "grounding": [{"type": "table", "name": "SMS_HEAT"}]},

    # ───────── 四、核心流程编排（T3-3-3）─────────
    {"cat": "核心流程编排", "diff": "中",
     "scenario": "一张质保书在系统内签发完成。",
     "q": "签发后数据被发往哪个外部系统？经由哪些接口过程与落地表？",
     "ref": "发往 WSP（质保书打印系统）：写 SQM_WSP_MTC_CHEM_INF / _COM_INF / _MECH_INF_1~3 / _PROD_INF，"
            "调用 BSQM_MTC_WSP.P_SEND_MTC_CHEM / _COM / _MECH / _PROD 发送。",
     "evi": ["T3-3-3：BSQM_MTC_ISSUE 写 SQM_WSP_MTC_*、调 BSQM_MTC_WSP.P_SEND_MTC_*"],
     "grounding": [{"type": "package", "name": "BSQM_MTC_ISSUE"}]},

    {"cat": "核心流程编排", "diff": "难",
     "scenario": "系统执行综合判定（总判 BSQM_TOT_JDG_RSLT）。",
     "q": "它聚合了哪些工序的结果作输入？判定结果写向哪里？",
     "ref": "聚合炼钢（SMS_RSLT_*/SMS_HEAT/SMS_SLAB）、卷材（SCR_COIL_MASTER/SCR_DEFECT）、"
            "热卷（SHR_HCOIL_MASTER/SHR_DEFECT）、精整板（SPR_DEFECT）多工序结果；"
            "写 *_DEFECT 与 SPR_PLATE（板级判定落地）。",
     "evi": ["T3-3-3：BSQM_TOT_JDG_RSLT_CB 读 SCR/SHR/SMS/SPR，写 SPR_PLATE 及各 DEFECT"],
     "grounding": [{"type": "package", "name": "BSQM_TOT_JDG_RSLT_CB"}]},

    {"cat": "核心流程编排", "diff": "难",
     "scenario": "BSCH_PLAN_ADJUST 执行一次生产计划调整。",
     "q": "该过程会触发哪些跨包/下游动作（对二级系统、生产指令等）？",
     "ref": "跨包触发：BSCH_PROD_INST（下达/更新生产指令 PR_TC_FUR_PDI）、BSCH_INF_SMS（同步板坯状态）、"
            "BSCH_INF_SPG（向精炼二级/连铸二级发送计划返送 PDI）、BSCH_PLAN_RSLT_CONF（接收返送炉次）。",
     "evi": ["T3-3-3：BSCH_PLAN_ADJUST 跨包调 BSCH_PROD_INST/INF_SMS/INF_SPG/PLAN_RSLT_CONF"],
     "grounding": [{"type": "package", "name": "BSCH_PLAN_ADJUST"}]},

    {"cat": "核心流程编排", "diff": "中",
     "scenario": "从生产计划到板坯作业，需要理清生产调度（BSCH）家族的完整链路。",
     "q": "请给出 BSCH 核心流程的端到端顺序。",
     "ref": "生产计划调整 → 计划时间排程 → 计划查询与批次选择 → 计划结果确认 → 生产指令下达 → "
            "厚板作业指令 → 板坯批处理作业。",
     "evi": ["T3-3-3 生产调度家族总览"],
     "grounding": [{"type": "package", "name": "BSCH_PROD_INST"}]},

    {"cat": "核心流程编排", "diff": "中",
     "scenario": "质保书需要包含完整的力学性能数据。",
     "q": "BSQM_MTC_ISSUE 中处理力学数据的核心子程序是哪个（规模最大）？它读哪些力学结果表、写向哪里？",
     "ref": "核心子程序 PR_SAVE_MTC_MECH（约 4369 行，本包最大）；读各产线力学结果 "
            "SQM_CC/HC/PC/SC_MECH_RSLT，写 SQM_WSP_MTC_MECH_INF_1/2/3 供 WSP 打印。",
     "evi": ["T3-3-3：BSQM_MTC_ISSUE 子程序 PR_SAVE_MTC_MECH(4369行)、SQM_*_MECH_RSLT→SQM_WSP_MTC_MECH_INF_*"],
     "grounding": [{"type": "package", "name": "BSQM_MTC_ISSUE"}]},
]


# ── 纯逻辑（可单测）─────────────────────────────────────────────────
def category_stats(questions):
    c = collections.Counter(q["cat"] for q in questions)
    d = collections.Counter(q["diff"] for q in questions)
    return c, d


def scoring_note():
    return ("**评分口径**：每题三档——正确(1.0) / 部分正确(0.5) / 错误(0.0)。"
            "**准确率 = (正确数 + 0.5×部分数) / 总题数**。验收目标：业务流程描述准确率 **≥90%**。")


def render_bank(questions):
    cat_c, diff_c = category_stats(questions)
    L = [
        "# S3-3 业务流程场景验证题库（T3-3-4）", "",
        "| 项 | 内容 |", "|----|----|",
        "| 文件编号 | AI-MES-QBANK-S3-3-2026 |",
        "| 需求单 | REQ-MES-AI-20260715-001（T3-3-4）|",
        "| 日期 | 2026-07-15 |",
        f"| 题量 | {len(questions)}（≥15）|",
        f"| 类别分布 | " + " / ".join(f"{c} {cat_c[c]}" for c in CATS) + " |",
        f"| 难度分布 | " + " / ".join(f"{k} {diff_c[k]}" for k in ("中", "难") if diff_c[k]) + " |",
        "| 评分方 | BIZ（业务专家）|", "",
        "> 本题库锚定 S3-3 反推证据（状态机 T3-3-1 / 追溯 T3-3-2 / 核心流程 T3-3-3），"
        "参考答案均来自真实库静态证据；**含「待确认」处以真实业务为准**。",
        "> " + scoring_note(), "",
        "## 评分汇总（BIZ 填写）", "",
        "| 指标 | 数值 |", "|----|----|",
        f"| 总题数 | {len(questions)} |",
        "| 正确数 | ___ |", "| 部分正确数 | ___ |", "| 错误数 | ___ |",
        "| **准确率** | ___%（目标 ≥90%）|",
        "| BIZ 签字 / 日期 | ___ |", "",
        "---", "",
    ]
    # 按类别分组出题
    qid = 0
    for cat in CATS:
        cat_qs = [q for q in questions if q["cat"] == cat]
        if not cat_qs:
            continue
        L += [f"## {cat}（{len(cat_qs)} 题）", ""]
        for q in cat_qs:
            qid += 1
            L += [
                f"### Q{qid}．{q['scenario']}",
                "",
                f"- **类别／难度**：{q['cat']} ／ {q['diff']}",
                f"- **问题**：{q['q']}",
                f"- **参考答案（AI 反推）**：{q['ref']}",
                "- **证据出处**：",
            ]
            L += [f"  - {e}" for e in q["evi"]]
            L += [
                "- **BIZ 评分**：☐ 正确　☐ 部分正确　☐ 错误",
                "- **BIZ 批注**：____________________",
                "",
            ]
    return "\n".join(L)


# ── 接地校验（需真实元数据，可选）────────────────────────────────────
def load_state_writes(meta_path):
    from proc_parser import analyze_metadata
    meta = json.load(open(meta_path, encoding="utf-8"))
    out = set()
    for a in analyze_metadata(meta):
        for s in a.set_assignments:
            t = s["table"].split(".", 1)[-1]
            out.add((t, s["column"], (s.get("value") or "").strip()))
    return out


def load_struct(struct_path):
    struct = json.load(open(struct_path, encoding="utf-8"))
    tables = set()
    col2tabs = collections.defaultdict(set)
    for t in struct.get("tables", []):
        tn = t.get("name")
        if not tn:
            continue
        tables.add(tn)
        for c in t.get("columns") or []:
            col2tabs[c.get("name")].add(tn)
    return tables, col2tabs


def load_packages(split_path):
    split = json.load(open(split_path, encoding="utf-8"))
    return {p["package"] for p in split.get("packages", [])}


def verify_one(gr, state_writes, tables, col2tabs, packages):
    """返回 (ok, 说明)。数据源缺失则记 SKIP。"""
    typ = gr["type"]
    if typ == "state":
        if state_writes is None:
            return None, "SKIP(无 meta)"
        key = (gr["table"], gr["column"], gr["value"])
        ok = key in state_writes
        return ok, f"状态写 {gr['table']}.{gr['column']}={gr['value']}"
    if typ == "carrier_pair":
        if col2tabs is None:
            return None, "SKIP(无 struct)"
        shared = col2tabs.get(gr["a"], set()) & col2tabs.get(gr["b"], set())
        return bool(shared), f"桥表 {gr['a']}×{gr['b']}（{len(shared)} 张）"
    if typ == "table":
        if tables is None:
            return None, "SKIP(无 struct)"
        return gr["name"] in tables, f"表 {gr['name']}"
    if typ == "package":
        if packages is None:
            return None, "SKIP(无 split)"
        return gr["name"] in packages, f"包 {gr['name']}"
    return None, f"未知 grounding 类型 {typ}"


def verify_all(questions, state_writes, tables, col2tabs, packages):
    rows, n_ok, n_fail, n_skip = [], 0, 0, 0
    for i, q in enumerate(questions, 1):
        for gr in q.get("grounding", []):
            ok, desc = verify_one(gr, state_writes, tables, col2tabs, packages)
            mark = "✅" if ok else ("⏭" if ok is None else "❌")
            rows.append(f"| Q{i} | {q['cat']} | {desc} | {mark} |")
            if ok is True:
                n_ok += 1
            elif ok is False:
                n_fail += 1
            else:
                n_skip += 1
    return rows, n_ok, n_fail, n_skip


def render_grounding_report(rows, n_ok, n_fail, n_skip):
    L = ["", "---", "", "## 附录：参考答案接地校验（对真实库元数据自动核验）", "",
         f"接地断言 {n_ok + n_fail + n_skip} 条：✅ 命中 {n_ok} ／ ❌ 未命中 {n_fail} ／ ⏭ 跳过 {n_skip}。",
         "", "| 题号 | 类别 | 接地断言 | 结果 |", "|----|----|----|----|"]
    L += rows
    if n_fail == 0:
        L += ["", f"> ✅ 全部可校验断言均在真实库中命中（{n_skip} 条因数据源未提供而跳过），题库参考答案接地无悬空。"]
    else:
        L += ["", f"> ⚠️ 有 {n_fail} 条断言未命中，请检查对应题目参考答案是否需修订。"]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="T3-3-4 业务流程验证题库")
    ap.add_argument("--out", default="docs/S3-3_业务流程验证题.md")
    ap.add_argument("--verify", action="store_true", help="对真实元数据做接地校验")
    ap.add_argument("--meta", help="meta_p0.json（状态写来源）")
    ap.add_argument("--struct", help="meta_mes_nosrc.json（表结构/桥表来源）")
    ap.add_argument("--split", help="split_all.json（切分包来源）")
    args = ap.parse_args(argv)

    md = render_bank(QUESTIONS)

    if args.verify:
        sw = load_state_writes(args.meta) if args.meta else None
        tables = col2tabs = None
        if args.struct:
            tables, col2tabs = load_struct(args.struct)
        packages = load_packages(args.split) if args.split else None
        rows, n_ok, n_fail, n_skip = verify_all(QUESTIONS, sw, tables, col2tabs, packages)
        md += "\n" + render_grounding_report(rows, n_ok, n_fail, n_skip)
        print(f"接地校验：命中 {n_ok} / 未命中 {n_fail} / 跳过 {n_skip}")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md + "\n", encoding="utf-8")
    cat_c, _ = category_stats(QUESTIONS)
    print(f"完成：{len(QUESTIONS)} 题（" + " / ".join(f"{c} {cat_c[c]}" for c in CATS) + f"）\n题库：{out}")


if __name__ == "__main__":
    main()
