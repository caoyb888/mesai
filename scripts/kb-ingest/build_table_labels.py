#!/usr/bin/env python3
"""
表中文标签抽取器：为每张 P0 表用 Kimi 抽取「2-8 字中文业务名 + 3-6 个中文别名/关键词」，
产 表名→标签 索引，供 rag_service 的 hybrid 词法检索精确匹配中文名（治近义表召回）。

全程经 ai-gateway 脱敏门。产物 JSON 供入库/查询共用（committable）。

用法：
  AI_GATEWAY_URL=http://127.0.0.1:8000 python3 build_table_labels.py \
    --cards-dir <s3-train/tables> --out src/ai-gateway/app/services/mes_table_labels.json

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

AI_GATEWAY_URL = os.environ.get("AI_GATEWAY_URL", "http://127.0.0.1:8000")
TASK_NO = "REQ-MES-AI-20260715-001"

SYS = "你是钢厂 MES 数据专家。给定一张表的英文表名与中文用途，输出用于中文检索的业务标签。"
PROMPT = """表名：{name}
用途：{purpose}

只输出一行 JSON（不要解释、不要代码围栏）：
{{"label":"<2-8字最贴切的中文业务名>","aliases":["<中文别名或核心业务关键词>", ...]}}
要求：label 为最能代表该表的中文名（如 钢卷主表/板坯/订单明细/化学成分检验/综合判定结果）；
aliases 3-6 个，覆盖用户可能用来检索本表的中文说法（含同义词，如 卷材/钢卷、板坯/slab）。"""


def _purpose(md, n=240):
    body = md.split("\n---\n", 1)[-1]
    m = re.search(r"#+\s*\d*\.?\s*\*{0,2}(?:表用途|用途)[^\n]*\n(.+?)(?=\n#+\s|\Z)", body, re.S)
    p = (m.group(1) if m else body).strip("-* `\n")
    return re.sub(r"\s+", " ", p)[:n]


def call_ai(name, purpose):
    payload = json.dumps({
        "task_no": TASK_NO, "caller": "s3-labels",
        "messages": [{"role": "system", "content": SYS},
                     {"role": "user", "content": PROMPT.format(name=name, purpose=purpose)}],
        "max_tokens": 120,
    }).encode("utf-8")
    req = urllib.request.Request(f"{AI_GATEWAY_URL}/v1/ai/chat", data=payload,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def parse_label(text):
    m = re.search(r"\{.*?\}", text, re.S)
    if not m:
        return None
    try:
        o = json.loads(m.group(0))
        lab = str(o.get("label", "")).strip()
        al = [str(a).strip() for a in o.get("aliases", []) if str(a).strip()]
        return {"label": lab, "aliases": al} if lab else None
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description="表中文标签抽取器")
    ap.add_argument("--cards-dir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    files = sorted(Path(args.cards_dir).glob("*.md"))
    labels, tok, fail = {}, 0, 0
    for i, p in enumerate(files, 1):
        name = p.stem
        try:
            resp = call_ai(name, _purpose(p.read_text(encoding="utf-8")))
            tok += (resp.get("usage") or {}).get("total_tokens", 0)
            lab = parse_label(resp.get("content", ""))
        except Exception as e:
            lab = None
            print(f"  [{i}/{len(files)}] {name} 调用失败：{e}")
        if lab:
            labels[name] = lab
            print(f"  [{i}/{len(files)}] {name} → {lab['label']} {lab['aliases']}")
        else:
            fail += 1
            print(f"  [{i}/{len(files)}] {name} → 解析失败")
        time.sleep(0.3)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(labels, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n完成：{len(labels)}/{len(files)} 张表有标签（失败 {fail}），Token {tok:,}")
    print(f"输出：{out}")


if __name__ == "__main__":
    main()
