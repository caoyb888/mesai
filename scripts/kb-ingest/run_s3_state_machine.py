#!/usr/bin/env python3
"""
T3-3-1：业务流程状态机反推（以过程为锚）

从 P0 存储过程静态分析的 set_assignments（列=字面量状态写入）反推状态字段的候选状态机，
结合 SCO 代码字典解码状态值，经 Kimi 合成【状态清单+含义 / 流转顺序与触发过程 / 不确定点】。
全程经 ai-gateway 脱敏门。

用法：
  AI_GATEWAY_URL=http://127.0.0.1:8000 python3 run_s3_state_machine.py \
    --meta <meta_p0.json> --code-dict <glossary_code_mapping.csv> \
    --out-report docs/S3-3_业务流程理解报告.md --out-cards <持久目录/state_machine>

关联需求单：REQ-MES-AI-20260715-001
作者：AI（芯智云匠）  日期：2026-07-15
"""
import os
import re
import csv
import sys
import json
import time
import argparse
import urllib.request
import collections
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent))
from proc_parser import analyze_metadata

AI_GATEWAY_URL = os.environ.get("AI_GATEWAY_URL", "http://127.0.0.1:8000")
TASK_NO = "REQ-MES-AI-20260715-001"

STATE_COL = re.compile(r"_(ST|STS|STAT|YN|FL|FLAG|GB|TP|CD)$")


def load_transitions(meta_path):
    """聚合 (表.列) → {值: set(写入包)}，过滤为「短码状态字段」（去消息/备注噪声）"""
    meta = json.load(open(meta_path, encoding="utf-8"))
    agg = collections.defaultdict(lambda: collections.defaultdict(set))
    for a in analyze_metadata(meta):
        for s in a.set_assignments:
            v = (s.get("value") or "").strip()
            if v and len(v) <= 4 and STATE_COL.search(s["column"]):   # 短码 + 状态列名
                agg[(s["table"], s["column"])][v].add(a.name)
    # 仅保留有 ≥1 个取值的字段
    return {k: v for k, v in agg.items() if v}


def load_code_dict(csv_path):
    """master_cd → {cd_val: 中文}"""
    idx = collections.defaultdict(dict)
    if not csv_path or not Path(csv_path).exists():
        return idx
    with open(csv_path, encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if len(row) >= 3 and row[0] and row[1]:
                zh = (row[2] or row[3] or row[4] or "").strip()   # 中/韩/英优先
                if zh:
                    idx[row[0].strip()][row[1].strip()] = zh
    return idx


def decode_candidates(col, values, code_idx):
    """据列名/取值覆盖，给每个状态值配候选中文解码（含来源代码组）"""
    core = re.sub(r"_(CD|ST|STS|STAT|FL|FLAG|GB|TP|YN)$", "", col)
    out = collections.defaultdict(list)
    for g, m in code_idx.items():
        related = bool(core) and (core in g or g in col)
        covers = len(m) <= 25 and all(v in m for v in values)
        if related or covers:
            for v in values:
                if v in m:
                    out[v].append(f"[{g}] {m[v]}")
    return out


SYS = """你是芯智云匠 MES AI 开发工程师，服务于山东芯通微电子。
正在从真实钢厂 MES（Oracle，owner=MESAPUSER）的存储过程静态分析反推状态机。
纪律：只据给定的「状态写入证据 + 候选字典解码」推断，不臆造未出现的状态；
候选解码有多个时择最贴切并注明不确定；无解码则据命名/取值给合理推测并标「待确认」。中文输出。"""

PROMPT = """[状态字段] {table}.{column}
[观测到的状态写入（值 ← 由哪些过程写）]
{trans}
[候选字典解码]
{decode}

请输出该状态字段的状态机理解（Markdown）：
1. **状态清单**：每个值 → 业务含义（含不确定标注）
2. **流转与触发**：可能的状态流转顺序，以及各转移由哪个/类过程触发（据写入包推断）
3. **业务含义**：该字段在业务流程中的作用（如工单/质保书/板坯生命周期的哪个环节）
4. **不确定点**：证据不足处，逐条标「待确认」（如动态 SQL、缺条件上下文）"""


def call_ai(system, user, max_tokens=1200):
    payload = json.dumps({
        "task_no": TASK_NO, "caller": "s3-3-statemachine",
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(f"{AI_GATEWAY_URL}/v1/ai/chat", data=payload,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())


def _slug(s):
    return re.sub(r"[^A-Za-z0-9_.]", "_", s)


def main():
    ap = argparse.ArgumentParser(description="T3-3-1 状态机反推")
    ap.add_argument("--meta", required=True)
    ap.add_argument("--code-dict")
    ap.add_argument("--out-report", default="docs/S3-3_业务流程理解报告.md")
    ap.add_argument("--out-cards")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    trans = load_transitions(args.meta)
    code_idx = load_code_dict(args.code_dict)
    fields = sorted(trans.items(), key=lambda x: -len(x[1]))
    if args.limit:
        fields = fields[:args.limit]

    rows, tok = [], 0
    for (t, c), vals in fields:
        trans_txt = "\n".join(f"  {v} ← {', '.join(sorted(pk)[:5])}" for v, pk in sorted(vals.items()))
        dec = decode_candidates(c, list(vals.keys()), code_idx)
        dec_txt = "\n".join(f"  {v}: {'; '.join(cs[:4])}" for v, cs in dec.items()) or "  （字典无匹配，请据命名/取值推断）"
        try:
            resp = call_ai(SYS, PROMPT.format(table=t, column=c, trans=trans_txt, decode=dec_txt))
            ans = resp.get("content", "")
            tok += (resp.get("usage") or {}).get("total_tokens", 0)
        except Exception as e:
            ans = f"[ERROR] {e}"
        rows.append({"table": t, "column": c, "values": sorted(vals.keys()),
                     "n_pkgs": len(set().union(*vals.values())), "answer": ans})
        print(f"  {t}.{c}（{len(vals)}值）tok≈{tok}")
        if args.out_cards:
            d = Path(args.out_cards); d.mkdir(parents=True, exist_ok=True)
            (d / f"{_slug(t + '.' + c)}.md").write_text(
                f"# 状态机卡片：{t}.{c}\n\n**取值**：{sorted(vals.keys())}\n\n---\n\n{ans}\n", encoding="utf-8")
        time.sleep(0.3)

    # 报告
    L = [
        "# S3-3 业务流程理解报告（状态机反推 · T3-3-1）\n",
        "| 项 | 内容 |", "|----|----|",
        "| 文件编号 | AI-MES-REPORT-S3-3-2026 |",
        "| 需求单 | REQ-MES-AI-20260715-001（T3-3-1）|",
        "| 日期 | 2026-07-15 |",
        f"| 反推状态字段 | {len(rows)}（源自过程 set_assignments，代码字典解码）|",
        f"| Token | {tok:,} |",
        "| 验收目标 | 业务流程/状态机描述准确率 ≥90%（BIZ 复核）|\n",
        "> 状态机由**过程静态写入证据**反推 + 字典解码 + AI 合成；**须 BIZ 对照真实业务复核**（尤其动态 SQL 与缺条件上下文处的「待确认」项）。本报告为 S3-3 第一部分（状态机），追溯链路(T3-3-2)/核心流程(T3-3-3)/验证题(T3-3-4)续。\n",
        "## 状态字段一览\n",
        "| 表.列 | 取值 | 写入过程数 |", "|----|----|----|",
    ]
    for r in rows:
        L.append(f"| {r['table']}.{r['column']} | {', '.join(r['values'])} | {r['n_pkgs']} |")
    L += ["\n---\n", "## 状态机反推明细\n"]
    for i, r in enumerate(rows, 1):
        L.append(f"### {i}. `{r['table']}.{r['column']}`\n")
        L.append(f"{r['answer']}\n")

    out = Path(args.out_report); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"\n完成：{len(rows)} 状态字段，Token {tok:,}\n报告：{out}")


if __name__ == "__main__":
    main()
