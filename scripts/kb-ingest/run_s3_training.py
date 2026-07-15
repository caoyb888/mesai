#!/usr/bin/env python3
"""
S3-1 / S3-2：真实 MES P0 资产理解训练执行脚本

流程（全部经 AI 网关 /v1/ai/chat，脱敏在网关侧强制生效，CLAUDE.md 4.2）：
  · S3-1 表/字段理解：读 P0 表卡片 jsonl → 拼理解 Prompt → 调网关 → 存理解卡片
  · S3-2 存储过程理解：读子程序切分 split_all.json → 拼理解 Prompt → 调网关 → 存逻辑卡片
  · smoke：仅发 1 个最小请求，验证「素材→脱敏→Kimi→回包」整条链路

用法：
  # 先起网关（另一进程，env 注入 AI_API_KEY / AI_MODEL）
  python3 run_s3_training.py --phase smoke                    # 链路冒烟（1 表）
  python3 run_s3_training.py --phase tables --limit 3         # 表理解小批校准
  python3 run_s3_training.py --phase procs  --limit 5         # 存储过程理解小批
  python3 run_s3_training.py --phase tables                   # 全量 95 表

环境变量：
  AI_GATEWAY_URL   默认 http://localhost:8000
  S3_CARDS         P0 表卡片 jsonl，默认 /home/xintong/mes-s3-data/s3-0/p0_table_cards.jsonl
  S3_SPLIT         子程序切分 json，默认 /home/xintong/mes-s3-data/s3-0/split_all.json
  S3_OUT           产物目录，默认 /home/xintong/mes-s3-data/s3-train

关联需求单：REQ-MES-AI-20260715-001（批训练需求单，TL+IT 已授权）
作者：AI（芯智云匠）
日期：2026-07-15
"""

import os
import re
import sys
import json
import time
import logging
import argparse
import urllib.request
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

AI_GATEWAY_URL = os.environ.get("AI_GATEWAY_URL", "http://localhost:8000")
S3_CARDS = os.environ.get("S3_CARDS", "/home/xintong/mes-s3-data/s3-0/p0_table_cards.jsonl")
S3_SPLIT = os.environ.get("S3_SPLIT", "/home/xintong/mes-s3-data/s3-0/split_all.json")
S3_OUT = Path(os.environ.get("S3_OUT", "/home/xintong/mes-s3-data/s3-train"))

TASK_NO = "REQ-MES-AI-20260715-001"


# ── 网关调用 ──────────────────────────────────────────────────
def call_ai(task_no, caller, system_prompt, user_content, max_tokens, module=None):
    """调用本地 AI 网关（内容在网关侧强制脱敏后才外发 Kimi）"""
    payload = json.dumps({
        "task_no": task_no,
        "caller": caller,
        "module": module,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{AI_GATEWAY_URL}/v1/ai/chat", data=payload,
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode())


# ── 素材渲染 ──────────────────────────────────────────────────
def render_table_card(c):
    """把表卡片 JSON 渲染为紧凑 Markdown 上下文"""
    lines = [
        f"表名：{c['table']}（owner={c['owner']}，SQL 中直接写表名，勿加 owner 前缀）",
        f"数据量：约 {c.get('num_rows', '?')} 行  |  主键：{c.get('pk')}  |  "
        f"热度：被 {c.get('read_procs')} 个过程读 / {c.get('write_procs')} 个过程写，操作={c.get('ops')}",
        f"列覆盖：{c.get('col_filled')}/{c.get('col_total')} 有语义",
        "",
        "| 列名 | 类型 | PK | 可空 | 语义 | 语义来源 |",
        "|------|------|----|------|------|---------|",
    ]
    for col in c.get("columns", []):
        lines.append(
            f"| {col.get('name','')} | {col.get('type','')} | "
            f"{'PK' if col.get('is_pk') else ''} | "
            f"{'Y' if col.get('nullable') else 'N'} | "
            f"{col.get('semantic') or '—'} | {col.get('source') or '—'} |"
        )
    return "\n".join(lines)


def render_subprogram(u):
    """把子程序单元渲染为上下文"""
    return (f"包：{u['package']}  子程序：{u['name']}  类型：{u.get('kind')}  "
            f"行数：{u.get('line_count')}  起始行：{u.get('start_line')}"
            f"{'  [切分回退段，边界可能偏大]' if u.get('fallback') else ''}\n\n"
            f"```plsql\n{u.get('source','')}\n```")


# ── Prompt（S3 真实 MES 理解，只理解不生成 SQL）────────────────
SYS_TABLE = """你是芯智云匠项目的 MES AI 开发工程师，服务于山东芯通微电子。
当前在学习一套真实的韩系钢厂 MES（Oracle 21c，schema owner=MESAPUSER）。
重要事实与纪律：
- 该库列注释大量缺失或为非中文，字段语义靠「拼图」（字典 semantic + 命名规约 + 类型 + 被读写过程画像），单一来源不足采信；缺失或冲突处一律标「待补充」，禁止臆断编造。
- owner=MESAPUSER 是 schema 用户名，不是表名前缀；SQL 中直接写表名，勿加 owner 前缀（CLAUDE.md 14.2）。
- 三语环境（中/英/韩）：英文/韩文语义翻译为中文，并在括号保留原文。
- 本阶段只做「理解」，不生成任何 SQL。所有输出使用中文。"""

PROMPT_TABLE = """[任务：理解 MES 表 {table}]

以下是该表的表卡片（结构 + 列语义 + 热度画像）：

{card}

请输出（Markdown）：
1. **表用途**：1~2 句，据表名、列构成、被读写过程画像推断这张表在 MES 中的角色。
2. **核心字段语义**：挑最关键的 8~15 个字段给出中文含义（英文/韩文语义译中并保留原文）。
3. **状态/类型/标志字段**：列出形如 *_ST/*_TP/*_YN/*_FLAG/*_GB/*_STAT 等字段，说明可能取值含义；取值不明标「待字典解码」。
4. **主键与疑似关联键**：据命名 *_NO/*_ID/*_CD 推断主键与可能的外键关联，标注不确定性。
5. **语义存疑字段清单**：语义缺失或存疑的字段，逐条标「待补充」。

[约束] 证据不足即标注不确定，禁止臆断；仅中文。"""

SYS_PROC = """你是芯智云匠项目的 MES AI 开发工程师，服务于山东芯通微电子。
当前在理解一套真实韩系钢厂 MES（Oracle 21c，owner=MESAPUSER）的 PL/SQL 存储过程子程序。
纪律：
- 只依据给定源码分析，不臆断；源码未体现的表依赖/取值不要编造。
- 遇动态 SQL（EXECUTE IMMEDIATE / 拼接 SQL）明确标注为「静态分析盲区」。
- 注释可能为中/英/韩混合且不一定可靠，以代码实际逻辑为准。
- 所有输出使用中文，英文/韩文标识符译中并保留原文。"""

PROMPT_PROC = """[任务：理解 PL/SQL 子程序 {package}.{name}]

以下是（经网关脱敏后的）源码：

{source}

请输出（Markdown）：
1. **用途**：这个子程序做什么。
2. **业务规则**：关键判断、分支、校验逻辑。
3. **状态流转**：形如 UPDATE ... SET x_st='..' / 对状态字段赋值的语句，列出「字段=值」及触发条件。
4. **读写副作用**：读取哪些表；写入哪些表及 DML 类型（INSERT/UPDATE/DELETE）。
5. **调用依赖**：调用了哪些其他过程/函数。
6. **风险与不确定点**：动态 SQL 盲区、语义不明处，逐条标「待补充」。

[约束] 只据源码，不臆断；动态 SQL 标注盲区；仅中文。"""


# ── 产物写入 ──────────────────────────────────────────────────
def _slug(s):
    return re.sub(r"[^A-Za-z0-9_.-]", "_", s)


def _save(kind_dir, name, title, meta, content):
    d = S3_OUT / kind_dir
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{_slug(name)}.md").write_text(
        f"# {title}\n\n"
        + "".join(f"**{k}**：{v}  \n" for k, v in meta.items())
        + f"\n---\n\n{content}\n",
        encoding="utf-8")


def _usage(resp):
    u = resp.get("usage") or {}
    return u.get("total_tokens") or u.get("total") or 0


# ── 执行阶段 ──────────────────────────────────────────────────
def load_cards():
    with open(S3_CARDS, encoding="utf-8") as f:
        return [json.loads(ln) for ln in f if ln.strip()]


def load_units(kinds):
    d = json.load(open(S3_SPLIT, encoding="utf-8"))
    units = []
    for pkg in d.get("packages", []):
        for u in pkg.get("units", []):
            if u.get("kind") in kinds:
                units.append(u)
    return units


def run_smoke():
    cards = load_cards()
    c = cards[0]
    log.info("冒烟：表 %s（%d 列），经网关发 Kimi …", c["table"], len(c.get("columns", [])))
    t0 = time.time()
    resp = call_ai(TASK_NO, "s3-smoke", SYS_TABLE,
                   PROMPT_TABLE.format(table=c["table"], card=render_table_card(c)),
                   max_tokens=600, module="smoke")
    dt = time.time() - t0
    content = resp.get("content", "")
    log.info("✅ 链路通：provider=%s model=%s tokens=%s 用时=%.1fs",
             resp.get("provider"), resp.get("model"), _usage(resp), dt)
    print("\n──────── Kimi 回包（前 800 字） ────────")
    print(content[:800])
    print("────────────────────────────────────────")
    return resp


def run_tables(limit, offset, missing_only=False):
    cards = load_cards()
    batch = cards[offset: offset + limit] if limit else cards[offset:]
    log.info("S3-1 表理解：共 %d 表，本批 %d（offset=%d，missing_only=%s）",
             len(cards), len(batch), offset, missing_only)
    total_tok, idx = 0, []
    for i, c in enumerate(batch, 1):
        if missing_only and (S3_OUT / "tables" / f"{_slug(c['table'])}.md").exists():
            continue
        log.info("  [%d/%d] %s", i, len(batch), c["table"])
        try:
            resp = call_ai(TASK_NO, "s3-1-tables", SYS_TABLE,
                           PROMPT_TABLE.format(table=c["table"], card=render_table_card(c)),
                           max_tokens=1500, module=c["table"])
        except Exception as e:
            log.error("    调用失败：%s", e)
            continue
        tok = _usage(resp)
        total_tok += tok
        _save("tables", c["table"], f"表理解卡片：{c['table']}",
              {"表名": c["table"], "owner": c["owner"], "行数": c.get("num_rows"),
               "训练时间": datetime.now().isoformat(timespec="seconds"),
               "model": resp.get("model"), "tokens": tok},
              resp.get("content", ""))
        idx.append({"table": c["table"], "tokens": tok})
        time.sleep(0.5)
    log.info("S3-1 本批完成：%d 表，累计 tokens=%d", len(idx), total_tok)
    _write_index("tables", idx, total_tok)


def _dedup_variants(units):
    """去重近似重复包：厂区/产线变体（_LZ/_RZ/_SHIP/_YC/_YC1）若其基包也在集内，则只留基包"""
    present = {u["package"] for u in units}

    def base(pkg):
        prev = None
        while prev != pkg:
            prev = pkg
            pkg = re.sub(r"_(LZ|RZ|SHIP|YC|YC1)$", "", pkg)
        return pkg

    kept, skipped = [], 0
    for u in units:
        b = base(u["package"])
        if b != u["package"] and b in present:
            skipped += 1
            continue
        kept.append(u)
    log.info("  去重：跳过 %d 个变体包子程序（保留基包）", skipped)
    return kept


def run_procs(limit, offset, kinds, max_lines, dedup=False, shards=1, shard_id=0,
              proc_max_tokens=2000, missing_only=False):
    units = load_units(kinds)
    units = [u for u in units if u.get("line_count", 0) <= max_lines]
    if dedup:
        units = _dedup_variants(units)
    # 确定性排序（小行数底层函数优先，拓扑序），保证分片切分稳定可复现
    units.sort(key=lambda u: (u.get("line_count", 0), u["package"], u["name"]))
    if shards > 1:
        units = units[shard_id::shards]
    batch = units[offset: offset + limit] if limit else units[offset:]
    log.info("S3-2 存储过程理解：本分片候选 %d（≤%d 行，shard %d/%d），本批 %d",
             len(units), max_lines, shard_id, shards, len(batch))
    total_tok, idx = 0, []
    for i, u in enumerate(batch, 1):
        name = f"{u['package']}.{u['name']}"
        if missing_only and (S3_OUT / "procs" / f"{_slug(name)}.md").exists():
            continue
        log.info("  [%d/%d] %s（%s，%d 行）", i, len(batch), name, u.get("kind"), u.get("line_count"))
        try:
            resp = call_ai(TASK_NO, "s3-2-procs", SYS_PROC,
                           PROMPT_PROC.format(package=u["package"], name=u["name"],
                                              source=render_subprogram(u)),
                           max_tokens=proc_max_tokens, module=u["package"])
        except Exception as e:
            log.error("    调用失败：%s", e)
            continue
        tok = _usage(resp)
        total_tok += tok
        _save("procs", name, f"过程逻辑卡片：{name}",
              {"包": u["package"], "子程序": u["name"], "类型": u.get("kind"),
               "行数": u.get("line_count"),
               "训练时间": datetime.now().isoformat(timespec="seconds"),
               "model": resp.get("model"), "tokens": tok},
              resp.get("content", ""))
        idx.append({"unit": name, "kind": u.get("kind"), "lines": u.get("line_count"), "tokens": tok})
        time.sleep(0.5)
    log.info("S3-2 本批完成：%d 单元，累计 tokens=%d", len(idx), total_tok)
    _write_index("procs", idx, total_tok)


def _write_index(kind, idx, total_tok):
    S3_OUT.mkdir(parents=True, exist_ok=True)
    p = S3_OUT / f"_index_{kind}.jsonl"
    with open(p, "a", encoding="utf-8") as f:
        for r in idx:
            f.write(json.dumps({**r, "at": datetime.now().isoformat(timespec="seconds")},
                               ensure_ascii=False) + "\n")
    log.info("  索引追加：%s（本批 %d 条，tokens=%d）", p, len(idx), total_tok)


def main():
    ap = argparse.ArgumentParser(description="S3-1/S3-2 真实 MES 理解训练")
    ap.add_argument("--phase", choices=["smoke", "tables", "procs"], default="smoke")
    ap.add_argument("--limit", type=int, default=0, help="本批数量，0=全部")
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--kinds", nargs="+", default=["PROCEDURE", "FUNCTION"],
                    help="procs 阶段处理的子程序类型")
    ap.add_argument("--max-lines", type=int, default=1200,
                    help="procs 阶段单元行数上限（超大段留后续二次切分）")
    ap.add_argument("--missing", action="store_true",
                    help="tables 阶段：仅补跑尚无卡片的表（断点续跑/补漏）")
    ap.add_argument("--dedup", action="store_true",
                    help="procs 阶段：去重厂区/产线变体包，只训基包")
    ap.add_argument("--shards", type=int, default=1, help="procs 阶段：并发分片总数")
    ap.add_argument("--shard-id", type=int, default=0, help="procs 阶段：本进程分片编号 [0,shards)")
    ap.add_argument("--proc-max-tokens", type=int, default=2000,
                    help="procs 阶段：单次输出上限（压缩输出省 token）")
    args = ap.parse_args()

    log.info("====== S3 训练 · phase=%s ======", args.phase)
    log.info("网关=%s  产物目录=%s", AI_GATEWAY_URL, S3_OUT)
    if args.phase == "smoke":
        run_smoke()
    elif args.phase == "tables":
        run_tables(args.limit, args.offset, missing_only=args.missing)
    elif args.phase == "procs":
        run_procs(args.limit, args.offset, args.kinds, args.max_lines,
                  dedup=args.dedup, shards=args.shards, shard_id=args.shard_id,
                  proc_max_tokens=args.proc_max_tokens, missing_only=args.missing)
    log.info("====== 完成 ======")


if __name__ == "__main__":
    main()
