#!/usr/bin/env python3
"""
过程中文标签抽取器：为存储过程用 Kimi 抽「2-10 字中文业务名 + 3-6 个中文别名/关键词」，
产 父过程名→标签 索引，供 rag_service 的 proc hybrid 词法检索精确匹配中文名
（治超大过程被二次切分后、纯向量召回被近义过程/相关表挤出 Top-3 的问题）。

与 build_table_labels.py 对称，区别：
  · 卡片可能是「二次切分片段」（stem 形如 <PKG>.<PROC>_pNN）→ 按**父过程**（去 _pNN 后缀）
    聚合同父各片段的「用途」再抽标签，一父一标签；
  · 输出键＝父过程名 <PKG>.<PROC>，与 rag_service 的 proc 父级分组一致。

全程经 ai-gateway 脱敏门。产物 JSON 供查询端共用（committable）。

用法：
  AI_GATEWAY_URL=http://127.0.0.1:8000 python3 build_proc_labels.py \
    --cards-dir <s3-train-p1-l2/procs> --out src/ai-gateway/app/services/mes_proc_labels.json
  # 可选 --only-parents-file 只对清单内父过程抽（默认对 cards-dir 下全部父过程）

关联需求单：REQ-MES-AI-20260716-001（超大过程二次切分 hybrid 调优）
作者：AI（芯智云匠）  日期：2026-07-17
"""
import os
import re
import sys
import json
import time
import argparse
from collections import defaultdict
from pathlib import Path
import urllib.request

AI_GATEWAY_URL = os.environ.get("AI_GATEWAY_URL", "http://127.0.0.1:8000")
TASK_NO = "REQ-MES-AI-20260716-001"

SYS = "你是钢厂 MES 数据专家。给定一个存储过程的英文名与中文用途，输出用于中文检索的业务标签。"
PROMPT = """过程名：{name}
用途（可能来自该过程被二次切分的多个片段，已合并）：
{purpose}

只输出一行 JSON（不要解释、不要代码围栏）：
{{"label":"<2-10字最贴切的中文业务名>","aliases":["<中文别名或核心业务关键词>", ...]}}
要求：
- label 为最能代表**本过程**职责的中文名，须由上面的过程名与用途归纳得出；
- aliases 3-6 个，均为用户可能用来检索**本过程**的中文说法（同义词/关键业务名词）；
- **严禁照抄本提示中出现的任何示例词**；label 与 aliases 必须紧扣本过程用途，与其它过程不相关的词一律不要。"""

_PNN = re.compile(r"_p\d+$", re.I)


def parent_of(stem: str) -> str:
    """片段卡 stem <PKG>.<PROC>_pNN → 父过程 <PKG>.<PROC>；非片段原样返回"""
    return _PNN.sub("", stem)


def purpose_of(md: str, n=200) -> str:
    """抽卡片「用途」段（proc 卡片 PROMPT_PROC 第1节）"""
    body = md.split("\n---\n", 1)[-1]
    m = re.search(r"#*\s*\d*\.?\s*\*{0,2}用途[^\n]*\n(.+?)(?=\n#+\s|\n\d+\.\s|\n\*\*|\Z)",
                  body, re.S)
    p = (m.group(1) if m else body).strip("-* `\n")
    return re.sub(r"\s+", " ", p)[:n]


def call_ai(name, purpose):
    payload = json.dumps({
        "task_no": TASK_NO, "caller": "s3-proc-labels",
        "messages": [{"role": "system", "content": SYS},
                     {"role": "user", "content": PROMPT.format(name=name, purpose=purpose)}],
        "max_tokens": 140,
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
    ap = argparse.ArgumentParser(description="过程中文标签抽取器")
    ap.add_argument("--cards-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only-parents-file", help="仅对清单内父过程抽（每行一个 PKG.PROC）")
    args = ap.parse_args()

    only = None
    if args.only_parents_file:
        only = {ln.strip() for ln in Path(args.only_parents_file).read_text().splitlines() if ln.strip()}

    # 按父过程聚合同父片段的用途
    by_parent = defaultdict(list)
    for p in sorted(Path(args.cards_dir).glob("*.md")):
        parent = parent_of(p.stem)
        if only and parent not in only:
            continue
        by_parent[parent].append(purpose_of(p.read_text(encoding="utf-8")))

    labels, tok, fail = {}, 0, 0
    parents = sorted(by_parent)
    for i, parent in enumerate(parents, 1):
        # 合并同父片段用途，去重后截断
        seen, merged = set(), []
        for pu in by_parent[parent]:
            key = pu[:40]
            if pu and key not in seen:
                seen.add(key)
                merged.append(pu)
        purpose = " / ".join(merged)[:600] or "（无用途文本，仅据过程名推断）"
        try:
            resp = call_ai(parent, purpose)
            tok += (resp.get("usage") or {}).get("total_tokens", 0)
            lab = parse_label(resp.get("content", ""))
        except Exception as e:
            lab = None
            print(f"  [{i}/{len(parents)}] {parent} 调用失败：{e}")
        if lab:
            labels[parent] = lab
            print(f"  [{i}/{len(parents)}] {parent} → {lab['label']} {lab['aliases']}")
        else:
            fail += 1
            print(f"  [{i}/{len(parents)}] {parent} → 解析失败")
        time.sleep(0.3)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(labels, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n完成：{len(labels)}/{len(parents)} 个父过程有标签（失败 {fail}），Token {tok:,}")
    print(f"输出：{out}")


if __name__ == "__main__":
    main()
