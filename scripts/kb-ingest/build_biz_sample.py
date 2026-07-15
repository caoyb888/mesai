#!/usr/bin/env python3
"""
T3-2-4：BIZ 过程理解抽检抽样单生成器（纯本地，不调外部 AI）

从 S3-2 过程逻辑卡片按模块分层抽样，抽取每张卡片的「用途/业务规则/状态流转」摘要，
生成供 BIZ 逐条判定（正确/部分正确/错误）的 Markdown 抽样单。验收目标：正确率 ≥85%。

抽样为确定性（按文件名排序 + 均匀间隔），可复现，不用随机数。

用法：
  python3 build_biz_sample.py --procs-dir <s3-train/procs> --n 40 --out docs/S3-2_BIZ抽检抽样单.md

关联需求单：REQ-MES-AI-20260715-001
作者：AI（芯智云匠）  日期：2026-07-15
"""
import re
import argparse
from pathlib import Path
from collections import defaultdict


def module_of(stem):
    """BSCH_B0025.PR_XXX → BSCH（包名前 4 位为模块前缀）"""
    return stem.split(".")[0][:4]


def extract_gist(md, max_chars=900):
    """去卡片头部 meta 与代码围栏，取正文关键段（用途/业务规则/状态流转）摘要"""
    body = md.split("\n---\n", 1)[-1].strip()
    body = re.sub(r"```markdown\s*|\s*```", "", body).strip()
    # 优先保留到「读写副作用」之前（用途+业务规则+状态流转），避免过长
    cut = re.split(r"###\s*\d\.\s*\*\*读写副作用", body, maxsplit=1)[0].strip()
    body = cut if 80 < len(cut) <= max_chars * 1.5 else body
    return (body[:max_chars] + "…") if len(body) > max_chars else body


def stratified_sample(files, n):
    """按模块占比分层 + 模块内均匀间隔抽样（确定性）"""
    by_mod = defaultdict(list)
    for f in files:
        by_mod[module_of(f.stem)].append(f)
    total = len(files)
    picks = []
    for mod, fs in sorted(by_mod.items()):
        fs = sorted(fs, key=lambda p: p.stem)
        k = max(1, round(n * len(fs) / total))
        step = max(1, len(fs) // k)
        picks += [(mod, fs[i]) for i in range(0, len(fs), step)][:k]
    # 稳定裁剪到 n（按模块名 + 文件名排序后间隔取，保持模块多样）
    picks.sort(key=lambda t: (t[0], t[1].stem))
    if len(picks) > n:
        step = len(picks) / n
        picks = [picks[int(i * step)] for i in range(n)]
    return picks


def main():
    ap = argparse.ArgumentParser(description="BIZ 过程理解抽检抽样单生成器（T3-2-4）")
    ap.add_argument("--procs-dir", required=True)
    ap.add_argument("--n", type=int, default=40, help="抽样数量")
    ap.add_argument("--out", default="docs/S3-2_BIZ抽检抽样单.md")
    args = ap.parse_args()

    files = sorted(Path(args.procs_dir).glob("*.md"), key=lambda p: p.stem)
    picks = stratified_sample(files, args.n)
    mod_dist = defaultdict(int)
    for mod, _ in picks:
        mod_dist[mod] += 1

    L = [
        "# S3-2 存储过程理解 · BIZ 抽检抽样单\n",
        "| 项 | 内容 |", "|----|----|",
        "| 文件编号 | AI-MES-BIZSAMPLE-S3-2-2026 |",
        "| 需求单 | REQ-MES-AI-20260715-001（T3-2-4）|",
        "| 日期 | 2026-07-15 |",
        f"| 抽样规模 | {len(picks)} / {len(files)} 张过程卡片（分层随模块占比）|",
        "| 验收目标 | 过程理解正确率 **≥85%**（BIZ 判定）|\n",
        "## 填写说明（BIZ）\n",
        "逐条阅读「AI 理解摘要」，对照真实业务，在**判定**列填 `正确` / `部分正确` / `错误`；",
        "`部分正确`/`错误` 请在**问题备注**列写明错在哪。完成后回填下方汇总。\n",
        "> 计分：正确=1、部分正确=0.5、错误=0；正确率 =(Σ得分)/条数。<85% 触发对应模块补训（T3-2-2）。\n",
        "## 抽样分布\n",
        "| 模块前缀 | 抽样数 |", "|----|----|",
    ]
    for m, c in sorted(mod_dist.items()):
        L.append(f"| {m} | {c} |")
    L += [
        "\n## 汇总（BIZ 填）\n",
        "| 指标 | 值 |", "|----|----|",
        "| 正确 | ___ |", "| 部分正确 | ___ |", "| 错误 | ___ |",
        "| **正确率** | ___%（目标 ≥85%）|",
        "| 是否达标 | ☐ 达标　☐ 未达标（列补训模块）|",
        "| BIZ 签字 / 日期 | ________ |\n",
        "---\n",
        "## 抽检明细\n",
    ]
    for i, (mod, f) in enumerate(picks, 1):
        gist = extract_gist(f.read_text(encoding="utf-8"))
        L.append(f"### {i}. `{f.stem}`　（模块 {mod}）\n")
        L.append("**AI 理解摘要**：\n")
        L.append(gist + "\n")
        L.append("| 判定（正确/部分正确/错误）| 问题备注 |")
        L.append("|----|----|")
        L.append("|  |  |\n")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"BIZ 抽样单：{len(picks)} 条，模块分布 {dict(sorted(mod_dist.items()))}")
    print(f"输出：{out}")


if __name__ == "__main__":
    main()
