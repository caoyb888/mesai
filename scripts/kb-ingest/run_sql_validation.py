#!/usr/bin/env python3
"""
T3-1-4 / T3-1-5：真实 MES 表/字段 SQL 场景验证

流程（全程经 ai-gateway 脱敏门；表结构上下文来自 mes_s3_understanding RAG 召回）：
  ① 授权题库（6 模块×5 题，锚定真实 P0 表）
  ② 每题 RAG 召回相关表卡片 → 注入 → Kimi 生成 Oracle SQL
  ③ 规则自动初评（表命中/禁 SELECT */参数化/完整性）
  ④ 产验证报告 + 人工终评单（≥85% 为验收目标，终评由 TL/BIZ 填）

用法：
  AI_GATEWAY_URL=http://127.0.0.1:8000 CHROMA_PERSIST_DIR=<chromadb> \
  HF_ENDPOINT=https://hf-mirror.com python3 run_sql_validation.py --out docs/S3-1_SQL验证报告.md

关联需求单：REQ-MES-AI-20260715-001
作者：AI（芯智云匠）  日期：2026-07-15
"""
import os
import re
import sys
import json
import time
import argparse
import urllib.request
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kb_ingest import LocalEmbedder

AI_GATEWAY_URL = os.environ.get("AI_GATEWAY_URL", "http://127.0.0.1:8000")
PERSIST = os.environ.get("CHROMA_PERSIST_DIR", "scripts/kb-ingest/data/chromadb")
COLLECTION = "mes_s3_understanding"
TASK_NO = "REQ-MES-AI-20260715-001"

# ── 验证题库（锚定真实 P0 表，业务场景 + 期望表 + 检查点）──────────
QUESTION_BANK = {
    "订单管理": [
        {"id": "MES-ORD-01", "q": "查询某客户（客户号已知）的所有订单头，显示订单号、下单日期、订单状态和客户名称。",
         "tables": ["SSD_ORDER_HEAD", "SSD_CUSTOMER"], "checks": ["JOIN客户表", "按客户过滤"]},
        {"id": "MES-ORD-02", "q": "查询某订单（订单号已知）的所有订单明细行，显示行号、物料/产品、数量和规格。",
         "tables": ["SSD_ORDER_LINE"], "checks": ["按订单号过滤", "明细字段"]},
        {"id": "MES-ORD-03", "q": "统计各客户的订单数量，按订单数降序取前 10。",
         "tables": ["SSD_ORDER_HEAD", "SSD_CUSTOMER"], "checks": ["GROUP BY", "COUNT", "TOP N"]},
        {"id": "MES-ORD-04", "q": "查询某订单的订单头及其所有明细行（一对多联查），显示订单号、客户、每行数量。",
         "tables": ["SSD_ORDER_HEAD", "SSD_ORDER_LINE"], "checks": ["头-行JOIN", "一对多"]},
        {"id": "MES-ORD-05", "q": "查询本月新增的订单明细行及其所属订单头信息。",
         "tables": ["SSD_ORDER_HEAD", "SSD_ORDER_LINE"], "checks": ["月份过滤", "JOIN"]},
    ],
    "炼钢板坯": [
        {"id": "MES-SMS-01", "q": "查询某热号（HEAT_NO）下生产的所有板坯，显示板坯号、重量、钢种和生产日期。",
         "tables": ["SMS_SLAB"], "checks": ["按热号过滤", "字段选择"]},
        {"id": "MES-SMS-02", "q": "查询指定订单（ORD_NO）关联的板坯清单及其状态（SLAB_STS）。",
         "tables": ["SMS_SLAB"], "checks": ["按订单过滤", "状态字段"]},
        {"id": "MES-SMS-03", "q": "统计某日各钢种的板坯数量与总重量。",
         "tables": ["SMS_SLAB"], "checks": ["GROUP BY钢种", "SUM重量", "日期过滤"]},
        {"id": "MES-SMS-04", "q": "查询已发送 ERP（ERP_POSTING_YN='Y'）但尚未冷却完成（COOLING_COMP_YN='N'）的板坯。",
         "tables": ["SMS_SLAB"], "checks": ["多标志位组合", "Y/N过滤"]},
        {"id": "MES-SMS-05", "q": "查询某热号的炼钢结果及其下属板坯（热号→板坯联查）。",
         "tables": ["SMS_RSLT_HEAT", "SMS_SLAB"], "checks": ["热号JOIN板坯"]},
    ],
    "卷材": [
        {"id": "MES-SCR-01", "q": "查询某订单的所有钢卷，显示卷号、净重和最终判定等级（FINAL_JDG_CD）。",
         "tables": ["SCR_COIL_MASTER"], "checks": ["按订单过滤", "判定等级字段"]},
        {"id": "MES-SCR-02", "q": "查询处于 Hold 状态（HOLD_YN='Y'）的钢卷清单。",
         "tables": ["SCR_COIL_MASTER"], "checks": ["Hold标志过滤"]},
        {"id": "MES-SCR-03", "q": "查询某钢卷（COIL_NO）的缺陷记录。",
         "tables": ["SCR_COIL_MASTER", "SCR_DEFECT"], "checks": ["卷-缺陷JOIN"]},
        {"id": "MES-SCR-04", "q": "统计各最终判定等级的钢卷数量与总净重。",
         "tables": ["SCR_COIL_MASTER"], "checks": ["GROUP BY判定", "COUNT+SUM"]},
        {"id": "MES-SCR-05", "q": "查询尚未发送 ERP（SEND_ERP_YN='N'）的钢卷。",
         "tables": ["SCR_COIL_MASTER"], "checks": ["ERP标志过滤"]},
    ],
    "质量": [
        {"id": "MES-QM-01", "q": "查询某订单（订单号+行号）的质量综合信息。",
         "tables": ["SQM_ORD_COM"], "checks": ["复合主键过滤"]},
        {"id": "MES-QM-02", "q": "查询某材料/产品的化学成分检验结果及其判定。",
         "tables": ["SQM_CHEM_RSLT", "SQM_CHEM_JDG"], "checks": ["结果JOIN判定"]},
        {"id": "MES-QM-03", "q": "查询综合判定结果为不合格的记录。",
         "tables": ["SQM_TOT_JDG_RSLT"], "checks": ["判定值过滤"]},
        {"id": "MES-QM-04", "q": "查询某质保书（MTC）的综合信息。",
         "tables": ["SQM_MTC_COM"], "checks": ["按MTC过滤"]},
        {"id": "MES-QM-05", "q": "统计某期间各综合判定结果的数量分布。",
         "tables": ["SQM_TOT_JDG_RSLT"], "checks": ["GROUP BY判定", "期间过滤"]},
    ],
    "调度": [
        {"id": "MES-SCH-01", "q": "查询某计划的板坯设计结果，显示计划号、板坯设计信息。",
         "tables": ["SCH_SLAB_DESIGN_RESULT", "SCH_PLAN_SLAB"], "checks": ["计划-设计关联"]},
        {"id": "MES-SCH-02", "q": "查询某热次计划及其加热设计结果（热号→设计联查）。",
         "tables": ["SCH_PLAN_HEAT", "SCH_HEAT_DESIGN_RESULT"], "checks": ["计划JOIN设计"]},
        {"id": "MES-SCH-03", "q": "查询某轧制批次（SCH_ROLL_BATCH）包含的计划。",
         "tables": ["SCH_ROLL_BATCH"], "checks": ["按批次过滤"]},
        {"id": "MES-SCH-04", "q": "统计某日各计划的板坯设计数量。",
         "tables": ["SCH_PLAN_SLAB"], "checks": ["GROUP BY", "日期过滤"]},
        {"id": "MES-SCH-05", "q": "查询待执行的热次设计计划。",
         "tables": ["SCH_PLAN_HEAT"], "checks": ["状态过滤"]},
    ],
    "提货发货": [
        {"id": "MES-SYD-01", "q": "查询某提货单（SYD_DISP_ORD）的明细。",
         "tables": ["SYD_DISP_ORD", "SYD_DISP_ORD_DETAIL"], "checks": ["单-明细JOIN"]},
        {"id": "MES-SYD-02", "q": "查询某提货单明细关联的物料信息。",
         "tables": ["SYD_DISP_ORD_DETAIL", "SYD_DISP_ORD_DETAIL_MTL"], "checks": ["明细-物料JOIN"]},
        {"id": "MES-SYD-03", "q": "统计某期间各提货单的物料数量。",
         "tables": ["SYD_DISP_ORD", "SYD_DISP_ORD_DETAIL_MTL"], "checks": ["GROUP BY", "期间过滤"]},
        {"id": "MES-SYD-04", "q": "查询今日的提货单列表。",
         "tables": ["SYD_DISP_ORD"], "checks": ["日期过滤"]},
        {"id": "MES-SYD-05", "q": "查询某提货单的完整信息（单头 + 明细 + 物料三层联查）。",
         "tables": ["SYD_DISP_ORD", "SYD_DISP_ORD_DETAIL", "SYD_DISP_ORD_DETAIL_MTL"], "checks": ["三表JOIN"]},
    ],
}

SYS_SQL = """你是芯智云匠项目的 MES AI 开发工程师，服务于山东芯通微电子。
数据库：真实钢厂 MES（Oracle 21c，owner=MESAPUSER）。
SQL 规范（强制）：
- 禁止 SELECT *，必须明确列出字段
- 参数化用 :param（禁止字符串拼接 SQL）
- owner=MESAPUSER 是 schema 用户名，SQL 中直接写表名、勿加前缀
- 复杂查询（>3 表 JOIN）附执行计划/索引使用简要说明
- 表名/字段以给定的表卡片为准；卡片未覆盖的字段标注「需确认」，不臆造
输出：一段 ```sql 代码块 + 一句话说明。"""

PROMPT_SQL = """[表结构参考（RAG 召回的表理解卡片）]
{ctx}

[业务场景]
{q}

请据上面的真实表结构写出符合规范的 Oracle SQL（禁 SELECT *、参数化、勿加 owner 前缀）。"""


def rag_context(embedder, col, question, n=5):
    qv = embedder.embed_batch([question])[0]
    res = col.query(query_embeddings=[qv], n_results=n,
                    where={"chunk_type": "s3_table"}, include=["documents", "metadatas"])
    docs = res["documents"][0] if res.get("documents") else []
    return "\n\n".join(f"--- 片段{i+1} ---\n{d}" for i, d in enumerate(docs))


def call_ai(system, user, max_tokens=900):
    payload = json.dumps({
        "task_no": TASK_NO, "caller": "s3-1-sqlval",
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(f"{AI_GATEWAY_URL}/v1/ai/chat", data=payload,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())


def auto_score(answer, q):
    low = answer.lower()
    scores = {}
    hit = sum(1 for t in q["tables"] if t.lower() in low)
    scores["表命中"] = min(40, round(40 * hit / max(len(q["tables"]), 1)))
    comp = 30
    if "select *" in low:
        comp -= 15
    if not re.search(r":\w+|:\d+", answer):   # 参数化
        comp -= 5
    scores["规范"] = max(0, comp)
    scores["完整性"] = 20 if ("```sql" in low or "select" in low) else 5
    scores["说明"] = 10 if ("说明" in answer or "--" in answer) else 5
    total = sum(scores.values())
    return {"dims": scores, "total": total}


def main():
    ap = argparse.ArgumentParser(description="MES SQL 场景验证（T3-1-4/5）")
    ap.add_argument("--out", default="docs/S3-1_SQL验证报告.md")
    ap.add_argument("--top-n", type=int, default=5)
    args = ap.parse_args()

    import chromadb
    embedder = LocalEmbedder()
    col = chromadb.PersistentClient(path=PERSIST).get_collection(COLLECTION)

    rows, tok_total = [], 0
    for mod, qs in QUESTION_BANK.items():
        for q in qs:
            ctx = rag_context(embedder, col, q["q"], args.top_n)
            try:
                resp = call_ai(SYS_SQL, PROMPT_SQL.format(ctx=ctx, q=q["q"]))
            except Exception as e:
                resp = {"content": f"[ERROR] {e}", "usage": {}}
            ans = resp.get("content", "")
            tok = (resp.get("usage") or {}).get("total_tokens", 0)
            tok_total += tok
            sc = auto_score(ans, q)
            rows.append({"mod": mod, **q, "answer": ans, "score": sc, "tokens": tok})
            print(f"  {q['id']} 自动初评={sc['total']}/100 tok={tok}")
            time.sleep(0.4)

    # 报告
    allsc = [r["score"]["total"] for r in rows]
    avg = round(sum(allsc) / len(allsc), 1)
    ge60 = round(100 * sum(1 for s in allsc if s >= 60) / len(allsc), 1)
    L = [
        "# S3-1 表/字段 SQL 场景验证报告（真实 MES）\n",
        "| 项 | 内容 |", "|----|----|",
        "| 文件编号 | AI-MES-REPORT-S3-1-SQLVAL-2026 |",
        "| 需求单 | REQ-MES-AI-20260715-001（T3-1-4/5）|",
        "| 日期 | 2026-07-15 |",
        f"| 题量 | {len(rows)}（6 模块×5）|",
        f"| RAG 上下文 | mes_s3_understanding 表卡片 Top-{args.top_n} |",
        f"| Token 消耗 | {tok_total:,} |",
        f"| 自动初评均分 | {avg}/100 |",
        f"| 自动初评 ≥60 占比 | {ge60}% |",
        "| 验收目标 | 人工评分正确率 **≥85%** |\n",
        "> ⚠️ 自动初评仅规则检查（表命中/禁 SELECT */参数化/完整性），**不代表 SQL 语义正确**；",
        "> 语义正确率须 TL/BIZ 人工终评（下方每题「人工评分」列），<85% 的模块补训（T3-1-2）。\n",
        "## 模块自动初评汇总\n",
        "| 模块 | 题数 | 自动均分 | 最低 | 最高 | 人工均分（待填）|",
        "|----|----|----|----|----|----|",
    ]
    for mod in QUESTION_BANK:
        ms = [r["score"]["total"] for r in rows if r["mod"] == mod]
        L.append(f"| {mod} | {len(ms)} | {round(sum(ms)/len(ms),1)} | {min(ms)} | {max(ms)} | ___ |")
    L += ["\n---\n", "## 逐题明细（含 AI 生成 SQL + 人工评分列）\n"]
    for i, r in enumerate(rows, 1):
        L.append(f"### {i}. {r['id']}　（{r['mod']}）\n")
        L.append(f"**业务场景**：{r['q']}\n")
        L.append(f"**期望表**：{', '.join(r['tables'])}　**检查点**：{', '.join(r['checks'])}\n")
        L.append(f"**AI 生成 SQL 与说明**：\n\n{r['answer']}\n")
        L.append(f"**自动初评**：{r['score']['total']}/100（{r['score']['dims']}）\n")
        L.append("| 人工评分（0-100）| 语义是否正确 | 问题备注 |")
        L.append("|----|----|----|")
        L.append("|  |  |  |\n")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"\n验证完成：{len(rows)} 题，自动均分 {avg}，≥60 占比 {ge60}%，Token {tok_total:,}")
    print(f"报告：{out}")


if __name__ == "__main__":
    main()
