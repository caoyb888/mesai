#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MES 取数（mes-sql）Text-to-SQL 评测脚本
文档编号：AI-MES-EVAL-2026-001
关联需求单：REQ-MES-AI-20260730-002（B1 评测基线，验收口径 F1）
作者：AI（芯智云匠）
日期：2026-07-31

功能：
  对题库逐题调用后端 /mes-sql/query（系统端到端：生成→安全校验→schema 校验→只读执行），
  并在同一次运行中背靠背执行 golden SQL（防数据漂移，F1.2），按「结果集等价」判分。

评分口径（F1.2 落档）：
  - 结果集等价：值序列化后按行做多重集合比对，允许行序差异；列按位置对齐（不按别名）；
    数值统一定点 6 位小数比较；NULL 与空串不等价。
  - golden SQL 返回空集的题目：单独标记，排除出主指标，另计入"空集题目"子集报告（防假阳性）。
  - 非确定性处理：temperature=0（由调用方 --temperature 指定，默认 0），每题重复 N 次取多数票；
    报告给出每项指标按采样轮的波动区间（min~max），不只报单点值。

指标（F1.3，主指标集 = 全部非空集题）：
  生成率 / schema 校验通过率 / 首轮执行成功率 / 首轮结果正确率 / 端到端准确率
  （基线 A 档无重试，端到端 = 首轮；B2 落地后端到端含重试结果）

运行环境：须在能访问后端与 MES 只读库的机器上运行（远程共享机）。
依赖：python-oracledb（ai-gateway venv 已具备）；其余纯 stdlib。

用法：
  python3 scripts/verify/mes_sql_eval.py \
    --questions scripts/verify/mes_sql_eval_questions.jsonl \
    --samples 3 --temperature 0 \
    --out-json /tmp/eval_baseline.json --out-md docs/M1_Text2SQL基线报告.md

环境变量：
  EVAL_API_BASE    后端地址（默认 http://127.0.0.1:8095）
  EVAL_USERNAME    登录账号（默认 admin）
  EVAL_PASSWORD    登录密码（必填，不入库不入命令行历史时可用 read -s 注入）
  MES_ENV_FILE     MES 凭据 env 文件（默认 ~/mes-s3-data/p1/mesdb.env，repo 外）
"""

import argparse
import collections
import datetime
import getpass
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from decimal import Decimal, InvalidOperation

ROW_CAP = 200           # 与后端 MAX_RESULT_ROWS 一致，两侧同口径截断
NUM_PRECISION = 6       # 数值定点比较精度（F1.2）


# ── 凭据与连接 ────────────────────────────────────────────────

def load_mes_env(path: str) -> dict:
    """读取 repo 外 MES 凭据 env 文件（export KEY='value' 格式，保留每键首次出现）"""
    env = {}
    with open(os.path.expanduser(path), encoding="utf-8") as f:
        for line in f:
            m = re.match(r"export\s+(\w+)='?(.*?)'?\s*$", line.strip())
            if m and m.group(1) not in env:
                env[m.group(1)] = m.group(2)
    return env


def login(api_base: str, username: str, password: str) -> str:
    """登录后端拿 JWT"""
    body = json.dumps({"username": username, "password": password}).encode()
    req = urllib.request.Request(
        f"{api_base}/system/auth/login", data=body,
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    token = (data.get("data") or {}).get("accessToken") or ""
    if not token:
        raise RuntimeError(f"登录失败：{data}")
    return token


def call_mes_sql(api_base: str, token: str, question: str, temperature: float,
                 timeout: int = 120) -> dict:
    """调用后端取数接口（caller=eval 独立计量，D2）"""
    body = json.dumps({
        "question": question, "executeSql": True,
        "temperature": temperature, "caller": "eval",
    }).encode()
    req = urllib.request.Request(
        f"{api_base}/mes-sql/query", data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {token}"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"_http_error": e.code, "_body": e.read()[:300].decode("utf-8", "ignore")}
    if data.get("code") != 0:
        return {"_api_error": data.get("message", "未知错误")}
    return data.get("data") or {}


# ── golden SQL 执行与结果集等价 ───────────────────────────────

def execute_golden(cur, golden_sql: str) -> list:
    """背靠背执行 golden SQL（ROWNUM 封顶与系统执行同口径）"""
    sql = golden_sql.strip().rstrip(";")
    cur.execute(f"SELECT * FROM ({sql}) WHERE ROWNUM <= {ROW_CAP}")
    return cur.fetchall()


def serialize_value(v) -> str:
    """值序列化（等价比较用）：NULL 独立标记；数值定点 6 位；其余转字符串去尾空白"""
    if v is None:
        return "«NULL»"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, (int, float, Decimal)):
        try:
            return str(Decimal(repr(v)).quantize(Decimal(1).scaleb(-NUM_PRECISION)))
        except InvalidOperation:
            return str(v)
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.isoformat()
    s = str(v)
    return "«EMPTY»" if s == "" else s.rstrip()


def result_signature(rows, from_api: bool) -> collections.Counter:
    """结果集 → 行多重集合签名（列按位置对齐；API 行为 dict，DB 行为 tuple）"""
    sig = collections.Counter()
    for row in rows:
        values = list(row.values()) if from_api else list(row)
        sig[tuple(serialize_value(v) for v in values)] += 1
    return sig


def _is_num(v) -> bool:
    return isinstance(v, (int, float, Decimal)) and not isinstance(v, bool)


def _to_dec(v) -> Decimal:
    return v if isinstance(v, Decimal) else Decimal(repr(v))


def _decimals(d: Decimal) -> int:
    e = d.normalize().as_tuple().exponent
    return max(0, -e)


def _num_equal(a, b) -> bool:
    """数值等价：取双方较粗小数位（上限 NUM_PRECISION）后比较——吸收 golden round()、
    模型未 round 之类**纯展示差异**；对真实不同的值仍判不等（口径修订 AI-MES-EVAL-口径-2026-001）。"""
    try:
        da, db = _to_dec(a), _to_dec(b)
    except (InvalidOperation, ValueError):
        return str(a) == str(b)
    p = min(_decimals(da), _decimals(db), NUM_PRECISION)
    q = Decimal(1).scaleb(-p)
    return da.quantize(q) == db.quantize(q)


def _nonnum_key(vals) -> tuple:
    """行的非数值骨架（数值位标 N）：用于在按列对齐前先按非数值列精确配桶。"""
    out = []
    for v in vals:
        if _is_num(v):
            out.append("«N»")
        elif v is None:
            out.append("«NULL»")
        else:
            s = str(v)
            out.append("«EMPTY»" if s == "" else s.rstrip())
    return tuple(out)


def _row_vals(row, from_api):
    return list(row.values()) if from_api else list(row)


def results_equivalent(api_rows: list, db_rows: list) -> bool:
    """结果集等价判定（口径修订版）：
    ① 先按原精确多重集比对（NUM_PRECISION 定点）——完全一致直接判等，保持既有行为；
    ② 否则做**数值容差匹配**：列按位置对齐、非数值列精确、数值列按 _num_equal（较粗小数位）配对，
       行多重集合一一匹配则判等。仅放宽 round()/小数位展示差异，不放宽列数/列序/非数值内容/真实数值差。"""
    if result_signature(api_rows, from_api=True) == result_signature(db_rows, from_api=False):
        return True
    A = [_row_vals(r, True) for r in api_rows]
    B = [_row_vals(r, False) for r in db_rows]
    if len(A) != len(B):
        return False
    used = [False] * len(B)
    for ra in A:
        ka = _nonnum_key(ra)
        hit = False
        for j, rb in enumerate(B):
            if used[j] or len(ra) != len(rb) or _nonnum_key(rb) != ka:
                continue
            if all(_num_equal(x, y) for x, y in zip(ra, rb) if _is_num(x) and _is_num(y)):
                used[j] = True
                hit = True
                break
        if not hit:
            return False
    return True


# ── 单题判定 ─────────────────────────────────────────────────

VERDICTS = ["correct", "wrong_result", "exec_fail", "blocked_schema",
            "blocked_safety", "not_generated", "api_error"]


def judge_one(resp: dict, golden_rows: list) -> tuple:
    """单次采样判定：返回 (verdict, detail)"""
    if "_http_error" in resp or "_api_error" in resp:
        return "api_error", str(resp)[:200]
    if not resp.get("generated"):
        return "not_generated", (resp.get("unanswerableReason") or "")[:120]
    ex = resp.get("executionResult") or {}
    exec_type = ex.get("execType")
    err = ex.get("errorMessage") or ""
    if exec_type == "BLOCKED":
        return ("blocked_schema" if "防臆造" in err else "blocked_safety"), err[:120]
    if exec_type == "SKIPPED":
        return "exec_fail", f"SKIPPED: {err[:100]}"
    if not ex.get("success"):
        return "exec_fail", err[:120]
    api_rows = ex.get("rows") or []
    if results_equivalent(api_rows, golden_rows):
        return "correct", ""
    return "wrong_result", f"api_rows={len(api_rows)} golden_rows={len(golden_rows)}"


def majority_vote(verdicts: list) -> str:
    """多数票：correct 过半即 correct；否则取最高频非 correct 判定"""
    if verdicts.count("correct") * 2 > len(verdicts):
        return "correct"
    counts = collections.Counter(v for v in verdicts if v != "correct")
    return counts.most_common(1)[0][0] if counts else "correct"


# ── 指标计算 ─────────────────────────────────────────────────

def compute_metrics(question_verdicts: dict) -> dict:
    """
    按题判定（含每题各采样轮 verdict 列表）→ 指标。
    question_verdicts: {qid: {"category": str, "verdicts": [v1,v2,...], "majority": str,
                              "golden_empty": bool}}
    """
    main = {k: v for k, v in question_verdicts.items() if not v["golden_empty"]}
    n = len(main) or 1

    def rate(pred, use_majority=True):
        hit = sum(1 for v in main.values()
                  if pred(v["majority"] if use_majority else v["verdicts"]))
        return round(hit / n * 100, 1)

    metrics = {
        "题目总数(主指标集)": len(main),
        "空集题(另计)": sum(1 for v in question_verdicts.values() if v["golden_empty"]),
        "生成率": rate(lambda m: m not in ("not_generated", "api_error")),
        "schema校验通过率": rate(lambda m: m != "blocked_schema"),
        "首轮执行成功率": rate(lambda m: m in ("correct", "wrong_result")),
        "首轮结果正确率": rate(lambda m: m == "correct"),
        "端到端准确率": rate(lambda m: m == "correct"),   # A 档无重试，= 首轮
    }

    # 按采样轮计算波动区间（F1.2：不得只报单点值）
    n_samples = max((len(v["verdicts"]) for v in main.values()), default=0)
    per_round_correct = []
    for r in range(n_samples):
        hit = tot = 0
        for v in main.values():
            if r < len(v["verdicts"]):
                tot += 1
                hit += 1 if v["verdicts"][r] == "correct" else 0
        if tot:
            per_round_correct.append(round(hit / tot * 100, 1))
    if per_round_correct:
        metrics["首轮结果正确率_轮次波动"] = f"{min(per_round_correct)}~{max(per_round_correct)}"
        metrics["首轮结果正确率_各轮"] = per_round_correct

    # 分层统计（F1.4）
    by_cat = collections.defaultdict(lambda: [0, 0])
    for v in main.values():
        by_cat[v["category"]][1] += 1
        if v["majority"] == "correct":
            by_cat[v["category"]][0] += 1
    metrics["分层准确率"] = {
        c: f"{h}/{t} ({round(h / t * 100, 1)}%)" for c, (h, t) in sorted(by_cat.items())
    }

    # 判定分布
    metrics["判定分布"] = dict(collections.Counter(v["majority"] for v in main.values()))
    return metrics


# ── 主流程 ───────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="MES 取数 Text-to-SQL 评测（REQ-MES-AI-20260730-002）")
    ap.add_argument("--questions", required=True, help="题库 jsonl（含 golden_sql）")
    ap.add_argument("--samples", type=int, default=3, help="每题采样次数（多数票，默认 3）")
    ap.add_argument("--temperature", type=float, default=0.0, help="生成温度（默认 0，F1.2）")
    ap.add_argument("--limit", type=int, default=0, help="仅评测前 N 题（冒烟用）")
    ap.add_argument("--out-json", default="", help="明细结果 JSON 输出路径")
    ap.add_argument("--out-md", default="", help="Markdown 报告输出路径")
    args = ap.parse_args()

    api_base = os.environ.get("EVAL_API_BASE", "http://127.0.0.1:8095")
    username = os.environ.get("EVAL_USERNAME", "admin")
    password = os.environ.get("EVAL_PASSWORD") or getpass.getpass("EVAL_PASSWORD: ")
    mes_env_file = os.environ.get("MES_ENV_FILE", "~/mes-s3-data/p1/mesdb.env")

    questions = [json.loads(l) for l in open(args.questions, encoding="utf-8")]
    if args.limit:
        questions = questions[:args.limit]
    print(f"[评测] 题目 {len(questions)} × 采样 {args.samples} = {len(questions) * args.samples} 次调用")

    import oracledb
    mes_env = load_mes_env(mes_env_file)
    con = oracledb.connect(user=mes_env["MES_DB_USER"], password=mes_env["MES_DB_PASSWORD"],
                           dsn=mes_env["MES_DB_DSN"])
    cur = con.cursor()
    cur.execute("ALTER SESSION SET CURRENT_SCHEMA=MESAPUSER")

    token = login(api_base, username, password)
    print("[评测] 登录成功，开始逐题评测…")

    results = {}
    t0 = time.time()
    for i, q in enumerate(questions, 1):
        qid = q["id"]
        # 背靠背执行 golden（同一次评测运行中，F1.2 数据漂移防护）
        try:
            golden_rows = execute_golden(cur, q["golden_sql"])
            golden_empty = len(golden_rows) == 0
        except Exception as e:
            print(f"  [{qid}] golden SQL 执行失败：{e}，本题跳过")
            results[qid] = {"category": q["category"], "verdicts": ["api_error"] * args.samples,
                            "majority": "api_error", "golden_empty": False,
                            "note": f"golden 执行失败: {str(e)[:80]}"}
            continue

        verdicts, details, samples = [], [], []
        for s in range(args.samples):
            resp = call_mes_sql(api_base, token, q["question"], args.temperature)
            verdict, detail = judge_one(resp, golden_rows)
            verdicts.append(verdict)
            details.append(detail)
            samples.append({
                "sql": resp.get("sql", ""), "execType": (resp.get("executionResult") or {}).get("execType"),
                "verdict": verdict, "detail": detail,
                "tokens": resp.get("tokensUsed"), "elapsedMs": (resp.get("executionResult") or {}).get("elapsedMs"),
            })
        results[qid] = {
            "category": q["category"], "question": q["question"],
            "golden_sql": q["golden_sql"], "golden_empty": golden_empty,
            "golden_rows": len(golden_rows),
            "verdicts": verdicts, "majority": majority_vote(verdicts),
            "samples": samples,
        }
        mark = "✓" if results[qid]["majority"] == "correct" else "✗"
        print(f"  [{i}/{len(questions)}] {qid} {mark} {results[qid]['majority']}"
              f"（{'/'.join(verdicts)}）{details[0][:60] if results[qid]['majority'] != 'correct' else ''}")

    cur.close()
    con.close()
    elapsed = round(time.time() - t0, 1)

    metrics = compute_metrics(results)
    metrics["评测耗时秒"] = elapsed
    metrics["配置"] = {"samples": args.samples, "temperature": args.temperature,
                      "row_cap": ROW_CAP, "num_precision": NUM_PRECISION}

    print("\n═══ 评测指标 ═══")
    for k, v in metrics.items():
        print(f"  {k}: {v}")

    if args.out_json:
        with open(args.out_json, "w", encoding="utf-8") as f:
            json.dump({"metrics": metrics, "results": results}, f, ensure_ascii=False, indent=2)
        print(f"[评测] 明细已写入 {args.out_json}")
    if args.out_md:
        write_markdown(args.out_md, metrics, results)
        print(f"[评测] 报告已写入 {args.out_md}")


def write_markdown(path: str, metrics: dict, results: dict) -> None:
    """输出 Markdown 评测报告（可直接入 docs/）"""
    lines = [
        "# MES 取数 Text-to-SQL 评测报告",
        "",
        f"- 生成时间：{datetime.datetime.now().isoformat(timespec='seconds')}",
        f"- 配置：{metrics['配置']}",
        f"- 评测耗时：{metrics['评测耗时秒']}s",
        "",
        "## 总指标（主指标集，空集题已排除）",
        "",
        "| 指标 | 值 |",
        "|----|----|",
    ]
    for k in ["题目总数(主指标集)", "空集题(另计)", "生成率", "schema校验通过率",
              "首轮执行成功率", "首轮结果正确率", "首轮结果正确率_轮次波动", "端到端准确率"]:
        if k in metrics:
            lines.append(f"| {k} | {metrics[k]} |")
    lines += ["", "## 分层准确率（F1.4）", "", "| 类别 | 准确率 |", "|----|----|"]
    for c, v in metrics.get("分层准确率", {}).items():
        lines.append(f"| {c} | {v} |")
    lines += ["", "## 判定分布", "", "| 判定 | 题数 |", "|----|----|"]
    for v, c in sorted(metrics.get("判定分布", {}).items()):
        lines.append(f"| {v} | {c} |")
    lines += ["", "## 逐题明细", "",
              "| 题号 | 类别 | 多数票判定 | 各轮判定 | 生成 SQL（首轮） |",
              "|----|----|----|----|----|"]
    for qid, r in results.items():
        sql0 = (r.get("samples") or [{}])[0].get("sql", "").replace("|", "\\|")[:80]
        lines.append(f"| {qid} | {r['category']} | {r['majority']} | {'/'.join(r['verdicts'])} | {sql0} |")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
