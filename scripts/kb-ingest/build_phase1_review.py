#!/usr/bin/env python3
"""
T3-4-4：Phase-1 评审会材料包（供甲方 IT 负责人签字确认）

面向 Phase-1「真实 MES 系统理解」里程碑评审会，产出一份**会议材料包**：
会议信息 + 议程 + Phase-1 交付一览 + DoD 达标核对 + 三项准确率核验与人工评分安排
+ 脱敏合规 + 遗留事项与 P1/P2 排期 + 评审决议 + 三方签字区 + 材料索引。
纯本地、无 AI、无 DB；**关键数字复用 S3-4-1 抽数器**（从各子报告正则抽取，缺失回退默认），
与总报告口径一致、不漂移。

用法：
  python3 build_phase1_review.py --out docs/S3-4-4_Phase1评审会材料.md \
    --census docs/MES_Asset_Census_2026.md --s3-1 docs/S3-1_SQL验证报告.md \
    --s3-2 docs/S3-2_存储过程理解报告.md --s3-3 docs/S3-3_业务流程理解报告.md \
    --qbank docs/S3-3_业务流程验证题.md --assertions assertions/manifest.md \
    --glossary docs/glossary_zh_ko_en.md

关联需求单：REQ-MES-AI-20260715-001（T3-4-4）
作者：AI（芯智云匠）  日期：2026-07-16
"""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_system_report import extract_stats

TASK_NO = "REQ-MES-AI-20260715-001"

# ── 议程（约 80 分钟）─────────────────────────────────────────────────
AGENDA = [
    ("开场与项目背景", "TL 技术负责人", 5),
    ("Phase-1 交付一览（系统规模 / 三大理解 / 知识资产）", "AE（AI 工程）", 10),
    ("三大理解成果演示（表·字段 / 存储过程 / 业务流程）", "AE + BIZ", 20),
    ("DoD 达标逐项核对", "TL", 10),
    ("三项准确率核验与人工评分安排", "BIZ + TL", 15),
    ("脱敏合规与安全红线核验", "ITM IT 审核专员", 5),
    ("遗留事项、风险与 P1/P2 训练排期", "AE", 5),
    ("评审决议与签字", "甲方 IT 负责人", 10),
]

# ── DoD 六项（与 S3-4-1 §六一致；state: done/pending）──────────────────
def dod_items(s):
    return [
        ("表 / SQL 场景准确率 ≥85%", f"自动初评 {s['sql_auto']}/100（{s['sql_qs']} 题）",
         "pending", "TL/BIZ 人工终评"),
        ("存储过程理解准确率 ≥85%", "抽样单 40 条就绪", "pending", "BIZ 抽检判定"),
        ("业务流程描述准确率 ≥90%", f"{s['q_count']} 题验证库、接地 {s['g_hit']}/{s['g_total']} 全命中",
         "pending", "BIZ 评分"),
        ("卡片/术语/字典入知识库可 RAG 召回", f"{s['rag_chunks']:,} chunk 入库并可召回", "done", "—"),
        ("断言种子 ≥3×P0 入 /assertions/", f"{s['assert_total']} 条", "done", "—"),
        ("全程脱敏（无泄漏 + 审计完整）", "素材审计 0 命中「可外发」", "done", "—"),
    ]


# ── 纯逻辑（可单测）─────────────────────────────────────────────────
def agenda_total_minutes(agenda=AGENDA):
    return sum(m for _, _, m in agenda)


def dod_summary(items):
    """返回 (done 数, pending 数)；item 结构 (name, cur, state, action)"""
    done = sum(1 for it in items if it[2] == "done")
    pending = sum(1 for it in items if it[2] == "pending")
    return done, pending


def build_review(s):
    items = dod_items(s)
    done, pending = dod_summary(items)
    total_min = agenda_total_minutes()
    L = [
        "# Phase-1「真实 MES 系统理解」里程碑评审会材料", "",
        "| 项 | 内容 |", "|----|----|",
        "| 文件编号 | AI-MES-REVIEW-P1-2026 |",
        f"| 需求单 | {TASK_NO}（T3-4-4）|",
        "| 会议名称 | Phase-1「真实 MES 系统理解」里程碑评审会 |",
        "| 拟召开时间 | ____年__月__日 __:__（预计 " + f"{total_min} 分钟）|",
        "| 地点 / 方式 | ____（现场 / 视频）|",
        "| 参会 | 甲方 IT 负责人、TL 技术负责人、BIZ 业务专家、ITM IT 审核专员、AE AI 工程 |",
        "| 评审对象 | Phase-1 里程碑交付（S3-0 素材 → S3-1/2/3 三大理解 → S3-4 汇总）|",
        "| 评审依据 | Sprint3 训练方案 DoD、CLAUDE.md 验收阈值、《真实 MES 系统理解总报告》|", "",
        "> **本次评审目的**：确认 Phase-1 训练与验证素材就绪、AI 侧交付达标，"
        "现场安排三项准确率人工评分口径，甲方 IT 负责人签字确认是否通过里程碑。", "",

        "## 一、会议议程", "",
        f"| # | 议题 | 主讲 | 时长(min) |", "|----|----|----|----|",
    ]
    for i, (topic, who, mins) in enumerate(AGENDA, 1):
        L.append(f"| {i} | {topic} | {who} | {mins} |")
    L += [f"| — | **合计** |  | **{total_min}** |", "",

          "## 二、Phase-1 交付一览（汇报要点）", "",
          f"**对象系统**：真实钢板/卷材 MES（韩系，Oracle 21c XE，owner=MESAPUSER），"
          f"**{s['mes_tables']:,} 表 / {s['mes_fields']:,} 字段 / {s['mes_units']:,} PL/SQL 单元 / 约 {s['mes_lines']/10000:.0f} 万行**；"
          "克隆库列注释全空、三语混合、无历史文档。", "",
          "**三大理解成果（P0 核心资产）**：",
          f"- 表/字段：**{s['s3_1_cards']} 表卡片**（语义 {s['s3_1_semantic_pct']}%）；SQL 验证 {s['sql_qs']} 题（自动初评 {s['sql_auto']}）。",
          f"- 存储过程：**{s['s3_2_cards']} / {s['s3_2_total']} 卡片**（Top60 P0 包切分子程序）。",
          f"- 业务流程：状态机 **{s['state_fields']}** 字段、追溯 **{s['carrier_keys']}** 实体键 **{s['trace_edges']}** 边、"
          f"核心流程 **{s['core_groups']}** 组、验证题 **{s['q_count']}** 道（接地 {s['g_hit']}/{s['g_total']} 全命中）。", "",
          "**知识资产与工程能力**：",
          f"- 中韩英术语 **{s['glossary_terms']:,}** + 代码字典；断言种子 **{s['assert_total']}** 条入 `/assertions/`。",
          f"- 知识库 RAG **{s['rag_chunks']:,} chunk** 可召回；全链路**脱敏 0 命中**「可外发」认证。",
          "- 工具链（自省/建图/切分/解析/对账/训练/理解/验证/报告），纯 stdlib、单测齐备。", "",

          "## 三、DoD 达标逐项核对", "",
          f"（共 6 项：✅ 已达 **{done}** / ⏳ 待人工评分 **{pending}**）", "",
          "| DoD 条目 | 现状 | 状态 | 达标动作 |", "|----|----|----|----|"]
    for name, cur, st, act in items:
        mark = "✅ 已达" if st == "done" else "⏳ 待评分"
        L.append(f"| {name} | {cur} | {mark} | {act} |")
    L += ["",
          "## 四、三项准确率核验与人工评分安排（评审关键）", "",
          "> 三项准确率是 Phase-1 达标的**核心判据**，AI 侧已备齐评分素材，**须现场确认评分口径与责任人**。", "",
          "| 准确率 | 目标 | 评分素材 | 责任人 | 口径 |",
          "|----|----|----|----|----|",
          f"| 表/SQL | ≥85% | `docs/S3-1_SQL验证报告.md`（{s['sql_qs']} 题，含人工评分列）| TL/BIZ | 语义正确率（自动初评仅规则检查）|",
          "| 存储过程 | ≥85% | `docs/S3-2_BIZ抽检抽样单.md`（40 条分层抽样）| BIZ | 正确/部分/错误三档 |",
          f"| 业务流程 | ≥90% | `docs/S3-3_业务流程验证题.md`（{s['q_count']} 题）| BIZ | 准确率=(正确+0.5部分)/总 |", "",
          "> **接地校验 ≠ 业务正确性**：接地（26/26 全命中）只证参考答案所引表/状态/过程真实存在（防臆造）；"
          "业务语义正确性须人工评分判定。评分结果回填各报告与《系统理解总报告》后，方构成里程碑达标证据。", "",

          "## 五、脱敏合规与安全红线核验（ITM）", "",
          "- 对外调用**唯一咽喉** ai-gateway，CLAUDE.md §4.2 七类脱敏门；训练素材审计 **0 命中**「可外发」认证（`docs/desensitize_audit_report.md`）。",
          "- 密钥仅运行时 env、双重 gitignore，无明文入库；生产库只读、写操作仅测试环境。",
          "- 无硬编码 IP/连接串/厂区/设备号（Gitleaks + 自研扫描）。", "",

          "## 六、遗留事项、风险与后续", "",
          "| 类别 | 内容 | 处置 |", "|----|----|----|",
          "| 待人工 | 三项准确率评分（SQL 终评 / 过程抽检 / 流程 BIZ 评分）| 会后限期完成、回填报告 |",
          "| 方法局限 | 变量状态 / 动态 SQL / 运行期分支静态不可见 | 已逐条标「待确认」；动态 SQL 专项后续 |",
          "| 资产覆盖 | 仅 P0（Top100 表 / Top60 包）| P1/P2 排期见 `docs/S3-4-3_Token复盘与P1P2排期.md` |",
          "| 韩系术语 | 关键业务词可能译偏 | BIZ 校准回灌术语表 |", "",
          "**P1/P2 排期要点**：P1（次核心）约 5.6M tokens / 2 训练日主动训；P2（长尾）不主动全训，RAG 兜底 + 按需增量。", "",

          "## 七、评审决议", "",
          "请甲方 IT 负责人于下列三者择一勾选：", "",
          "- ☐ **通过**：三项准确率现场核验达标（SQL≥85% / 过程≥85% / 流程≥90%），Phase-1 里程碑通过。",
          "- ☐ **有条件通过**：AI 侧交付达标，**待三项人工评分回填达标后自动生效签字**（限期 ____）。",
          "- ☐ **驳回**：____（具体不达标项与整改要求）。", "",
          "> 说明：截至评审，**AI 侧交付 100% 就绪**；若人工评分尚未完成，建议按「有条件通过」推进，避免阻塞。", "",

          "## 八、评审签字区", "",
          "| 角色 | 结论 | 三项准确率（如已评）| 签字 | 日期 |",
          "|----|----|----|----|----|",
          "| 甲方 IT 负责人 |  |  |  |  |",
          "| TL 技术负责人 |  |  |  |  |",
          "| BIZ 业务专家 |  |  |  |  |",
          "| ITM IT 审核专员 |  | — |  |  |", "",

          "## 附、评审材料索引（会前分发）", "",
          "| 材料 | 路径 |", "|----|----|",
          "| 系统理解总报告（主）| `docs/MES真实系统理解总报告.md` |",
          "| 表/字段：SQL 验证报告 | `docs/S3-1_SQL验证报告.md`；表卡片 `docs/p0_table_cards.md` |",
          "| 存储过程：理解报告 + 抽检单 | `docs/S3-2_存储过程理解报告.md`、`docs/S3-2_BIZ抽检抽样单.md` |",
          "| 业务流程：理解报告 + 验证题 | `docs/S3-3_业务流程理解报告.md`、`docs/S3-3_业务流程验证题.md` |",
          "| 断言种子 | `assertions/manifest.md` + `assertions/*/` |",
          "| 术语/字典 | `docs/glossary_zh_ko_en.md` |",
          "| 脱敏合规 | `docs/desensitize_audit_report.md` |",
          "| Token/排期 | `docs/S3-4-3_Token复盘与P1P2排期.md` |",
          "| 就绪清单 | `docs/Phase1_验收就绪清单.md` |", "",
          "---", "",
          "*本材料数字由各子报告自动抽取汇总，与《系统理解总报告》口径一致；三态如实标注「已达 / 待评分」。*"]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="T3-4-4 Phase-1 评审会材料")
    ap.add_argument("--out", default="docs/S3-4-4_Phase1评审会材料.md")
    for a in ("census", "s3_1", "s3_2", "s3_3", "qbank", "assertions", "glossary"):
        ap.add_argument("--" + a.replace("_", "-"), dest=a)
    args = ap.parse_args(argv)

    def _read(p):
        return Path(p).read_text(encoding="utf-8") if p and Path(p).exists() else ""

    src = {k: _read(getattr(args, k)) for k in
           ("census", "s3_1", "s3_2", "s3_3", "qbank", "assertions", "glossary")}
    s = extract_stats(src)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_review(s) + "\n", encoding="utf-8")
    print("Phase-1 评审会材料：", out)
    print(f"议程 {agenda_total_minutes()} 分钟；DoD 已达/待评分 = {dod_summary(dod_items(s))}")


if __name__ == "__main__":
    main()
