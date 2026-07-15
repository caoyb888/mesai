#!/usr/bin/env python3
"""
T3-3-3：质量判定(BSQM) / 生产调度(BSCH) 核心流程理解（以过程为锚）

在 S3-2「逐过程理解」之上，做**流程编排级**理解：按核心流程组聚合各包子程序的
读写数据流 + 子程序调用编排（内部/跨包）+ 状态写入 + 源码中文/韩文注释（业务意图），
经 Kimi 合成【流程用途 / 输入→处理步骤→输出 / 状态流转 / 关键业务规则 / 变体差异 /
不确定点】；末尾各出一份「质量判定」「生产调度」家族流程总览。
证据来自 split_all.json（60 P0 包切分后的真实子程序体）。全程经 ai-gateway 脱敏门，
只据证据推断、不臆造，缺证据一律标「待确认」。

用法：
  AI_GATEWAY_URL=http://127.0.0.1:8000 python3 run_s3_core_process.py \
    --split <split_all.json> \
    --out-report docs/S3-3_业务流程理解报告.md --out-cards <持久目录/core_process>

关联需求单：REQ-MES-AI-20260715-001（T3-3-3）
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from proc_parser import analyze_source

AI_GATEWAY_URL = os.environ.get("AI_GATEWAY_URL", "http://127.0.0.1:8000")
TASK_NO = "REQ-MES-AI-20260715-001"
SECTION_MARKER = "<!-- T3-3-3-COREPROCESS -->"

CJK = re.compile(r"[一-鿿가-힣]")   # 中文 + 韩文

# ── 核心流程组（curated：中文名, 主包, 变体包, 家族）──────────────────
#   变体 = 按厂区(LZ莱芜/RZ日照/SHIP发货)、产线(GH/GK/HC)、母子(B0025/G0025) 分化的近似包
FAMILY = {"BSQM": "质量判定", "BSCH": "生产调度"}
PROCESS_GROUPS = [
    # —— 质量判定 BSQM ——
    ("试样批次(LOT)成形与检验结果", "BSQM_SMP_LOTFORM_RSLT",
     ["BSQM_SMP_LOTFORM_RSLT_GH1", "BSQM_SMP_LOTFORM_RSLT_GH2",
      "BSQM_SMP_LOTFORM_RSLT_GK", "BSQM_SMP_LOTFORM_RSLT_HC",
      "BSQM_SMP_LOTFORM_RSLT_RZ"], "BSQM"),
    ("标准力学性能试验与判定", "BSQM_STD_MECH_TEST",
     ["BSQM_INF_LIMS_MEC_TEST"], "BSQM"),
    ("综合判定(总判)", "BSQM_TOT_JDG_RSLT_CB", [], "BSQM"),
    ("质保书(材质证明书 MTC)签发", "BSQM_MTC_ISSUE",
     ["BSQM_MTC_ISSUE_HB", "BSQM_MTC_ISSUE_LZ", "BSQM_MTC_ISSUE_RZ",
      "BSQM_MTC_ISSUE_SHIP", "BSQM_MTC_ISSUE_SHIP_YC",
      "BSQM_MTC_ISSUE_SHIP_YC1"], "BSQM"),
    ("质量设计公共", "BSQM_QLT_DSN_COMMON", [], "BSQM"),
    # —— 生产调度 BSCH ——
    ("生产计划调整", "BSCH_PLAN_ADJUST", [], "BSCH"),
    ("计划时间排程", "BSCH_PLAN_TIME_SCHEDULE",
     ["BSCH_PLAN_TIME_SCHEDULE2"], "BSCH"),
    ("计划查询与批次选择", "BSCH_PLAN_SEARCH", ["BSCH_BATCH_SELECT2"], "BSCH"),
    ("计划结果确认", "BSCH_PLAN_RSLT_CONF", [], "BSCH"),
    ("生产指令下达", "BSCH_PROD_INST", [], "BSCH"),
    ("厚板作业指令", "BSCH_WORK_INST_PLT", [], "BSCH"),
    ("板坯批处理作业", "BSCH_BATCHA_PLT_JOB2",
     ["BSCH_B0025", "BSCH_B0025S", "BSCH_B0025_HEAT_NO", "BSCH_G0025"], "BSCH"),
]


# ── 纯逻辑（可单测，不依赖 DB/AI）─────────────────────────────────────
def norm_table(t):
    """去 owner 前缀（MESAPUSER.T → T），统一表名（§14 无 schema 前缀）"""
    return t.split(".", 1)[1] if "." in t else t


def extract_comments(src, cap=22):
    """抽源码中「含≥3个中/韩字」的注释行作业务意图线索，去码噪、去重、限量"""
    out, seen = [], set()

    def push(txt):
        txt = txt.strip()
        if (len(CJK.findall(txt)) >= 3 and "||" not in txt
                and "PR_ADD_LOG" not in txt.upper() and txt not in seen):
            seen.add(txt)
            out.append(txt[:60])

    for line in src.splitlines():
        if len(out) >= cap:
            break
        m = re.search(r"--\s?(.*)", line)
        if m:
            push(m.group(1))
    for m in re.finditer(r"/\*(.*?)\*/", src, re.S):
        for l in m.group(1).splitlines():
            if len(out) >= cap:
                break
            push(l)
    return out[:cap]


def classify_calls(calls, own_names):
    """调用分类：内部（同包子程序）/ 外部（限定名 pkg.proc，业务包 BS* 优先）"""
    own = set(own_names)
    internal = sorted({c for c in calls if c in own})
    external = sorted({c for c in calls if "." in c})
    external.sort(key=lambda c: (not c.upper().startswith("BS"), c))  # BS* 业务包排前
    return internal, external


def analyze_package(pkg_obj):
    """聚合一个包的全部子程序 → 读写表/状态写/调用编排/子程序清单/注释"""
    reads, writes = set(), set()
    states, comments = [], []
    all_calls = set()
    subprograms = []
    own_names = [u.get("name", "") for u in pkg_obj.get("units", [])]
    for u in pkg_obj.get("units", []):
        src = u.get("source") or ""
        a = analyze_source(src, name=u.get("name", ""))
        reads |= {norm_table(t) for t in a.read_tables}
        writes |= {norm_table(w["table"]) for w in a.write_tables}
        all_calls |= set(a.calls)
        for s in a.set_assignments:
            states.append(f"{norm_table(s['table'])}.{s['column']}={s['value']}")
        comments += extract_comments(src)
        subprograms.append({"name": u.get("name", ""), "kind": u.get("kind", ""),
                            "lines": int(u.get("line_count", 0) or 0)})
    internal, external = classify_calls(all_calls, own_names)
    # 注释去重保序
    seen, uniq_c = set(), []
    for c in comments:
        if c not in seen:
            seen.add(c)
            uniq_c.append(c)
    return {
        "reads": sorted(reads), "writes": sorted(writes),
        "states": states, "internal_calls": internal, "external_calls": external,
        "subprograms": subprograms, "comments": uniq_c,
        "total_lines": int(pkg_obj.get("total_lines", 0) or 0),
        "unit_count": int(pkg_obj.get("unit_count", 0) or 0),
    }


def variant_delta(primary_agg, var_agg):
    """变体相对主包的差异摘要：规模 + 主包没有的独有写表"""
    extra_writes = sorted(set(var_agg["writes"]) - set(primary_agg["writes"]))
    return {"unit_count": var_agg["unit_count"], "total_lines": var_agg["total_lines"],
            "extra_writes": extra_writes[:8]}


# ── AI 合成 ────────────────────────────────────────────────────────
SYS = """你是芯智云匠 MES AI 开发工程师，服务于山东芯通微电子。
正在从真实钢板/卷材 MES（Oracle，owner=MESAPUSER）的存储过程切分子程序，
理解「质量判定(BSQM) / 生产调度(BSCH)」的核心业务流程（流程编排级，非单过程）。
纪律：只据给定的「读写表 + 子程序清单 + 调用编排 + 状态写 + 源码中文注释」推断，
不臆造未出现的表/过程；证据不足处（动态 SQL、跨包未覆盖）逐条标「待确认」。中文输出。"""

PROMPT = """[核心流程] {zh}（主包 {pkg}，家族 {fam}）
[规模] {units} 子程序 / {lines} 行
[输入·读表]
{reads}
[输出·写表]
{writes}
[状态写入（列=字面量）]
{states}
[子程序清单（编排单元）]
{subs}
[跨包调用（业务编排/接口）]
{ext}
[源码中文注释（业务意图线索）]
{comments}
[同族变体包（相对主包差异）]
{variants}

请输出该核心流程的**流程编排级**理解（Markdown）：
1. **流程用途**：这是什么业务流程，处于质保书/板坯/计划生命周期的哪个环节
2. **输入→处理步骤→输出**：按子程序/调用编排还原关键处理步骤（数据从哪些表来、经何加工、写向哪些表）
3. **关键状态流转**：本流程推动了哪些状态字段变化（结合状态写证据）
4. **关键业务规则**：从注释/判定/跨包调用能确证的规则（如厂区/产线分支、对外系统接口）
5. **变体差异**：同族变体包相对主包的差异（厂区/产线/母子坯等）
6. **不确定点**：证据不足处逐条标「待确认」"""

OVERVIEW_PROMPT = """[家族] {fam} 核心流程
[已理解的流程组（组名 → 主包/规模/关键写表）]
{groups}

请给出 {fam} 家族的**核心流程总览**（Markdown，≤600字）：
1. 端到端主流程（用箭头串起各流程组，标注每步的关键表/状态）
2. 流程组之间的编排关系（谁触发谁、共享哪些表/状态）
3. 全流程的关键业务规则与「待确认」清单"""


def call_ai(system, user, caller, max_tokens=1500):
    payload = json.dumps({
        "task_no": TASK_NO, "caller": caller,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(f"{AI_GATEWAY_URL}/v1/ai/chat", data=payload,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=200) as r:
        return json.loads(r.read().decode())


def _bullet(items, cap, empty="（无）"):
    items = list(items)
    if not items:
        return f"  {empty}"
    out = [f"  - {x}" for x in items[:cap]]
    if len(items) > cap:
        out.append(f"  - …另 {len(items) - cap} 项")
    return "\n".join(out)


def build_user_prompt(zh, pkg, fam, agg, variants):
    subs = _bullet([f"{s['name']}({s['kind']},{s['lines']}行)"
                    for s in agg["subprograms"]], 20)
    var_txt = "  （无变体）"
    if variants:
        var_txt = "\n".join(
            f"  - {vn}：{vd['unit_count']}子程序/{vd['total_lines']}行"
            + (f"，独有写表 {', '.join(vd['extra_writes'])}" if vd["extra_writes"] else "，无独有写表")
            for vn, vd in variants)
    # 状态写去重保序
    seen, uniq_states = set(), []
    for s in agg["states"]:
        if s not in seen:
            seen.add(s)
            uniq_states.append(s)
    return PROMPT.format(
        zh=zh, pkg=pkg, fam=FAMILY[fam],
        units=agg["unit_count"], lines=agg["total_lines"],
        reads=_bullet(agg["reads"], 18), writes=_bullet(agg["writes"], 14),
        states=_bullet(uniq_states, 12, "（无字面量状态写，或为变量赋值不可见——待确认）"),
        subs=subs, ext=_bullet(agg["external_calls"], 14),
        comments=_bullet(agg["comments"], 18, "（无中文注释）"), variants=var_txt)


def _slug(s):
    return re.sub(r"[^A-Za-z0-9_.]", "_", s)


def render_report_section(groups_out, overviews, tok):
    L = [SECTION_MARKER, "",
         "## 第三部分：核心流程理解（质量判定 BSQM / 生产调度 BSCH · T3-3-3）", "",
         "| 项 | 内容 |", "|----|----|",
         "| 需求单 | REQ-MES-AI-20260715-001（T3-3-3）|",
         "| 日期 | 2026-07-15 |",
         f"| 核心流程组 | {len(groups_out)}（BSQM {sum(1 for g in groups_out if g['fam']=='BSQM')} / "
         f"BSCH {sum(1 for g in groups_out if g['fam']=='BSCH')}）|",
         f"| Token | {tok:,} |",
         "| 验收目标 | 业务流程描述准确率 ≥90%（BIZ 复核）|", "",
         "> 在 S3-2 逐过程理解之上做**流程编排级**理解：按流程组聚合子程序读写流 + 调用编排 + "
         "状态写 + 源码注释 → AI 合成；**须 BIZ 对照真实工艺流复核**（动态 SQL / 变量状态不可见处已标「待确认」）。", "",
         "### 核心流程组一览", "",
         "| 家族 | 流程组 | 主包 | 子程序 | 行数 | 读表 | 写表 |",
         "|----|----|----|----|----|----|----|"]
    for g in groups_out:
        L.append(f"| {FAMILY[g['fam']]} | {g['zh']} | `{g['pkg']}` | {g['units']} "
                 f"| {g['lines']} | {g['n_reads']} | {g['n_writes']} |")
    L += ["", "---", "", "### 核心流程明细", ""]
    for i, g in enumerate(groups_out, 1):
        L.append(f"#### {i}. {g['zh']}（`{g['pkg']}` · {FAMILY[g['fam']]}）\n")
        L.append(g["answer"] + "\n")
    for fam, ov in overviews.items():
        L += [f"---\n", f"### {FAMILY[fam]}（{fam}）家族流程总览\n", ov + "\n"]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="T3-3-3 核心流程理解")
    ap.add_argument("--split", required=True, help="split_all.json（P0 包切分子程序）")
    ap.add_argument("--out-report", default="docs/S3-3_业务流程理解报告.md")
    ap.add_argument("--out-cards")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--no-ai", action="store_true")
    args = ap.parse_args()

    split = json.load(open(args.split, encoding="utf-8"))
    pkgs = {p["package"]: p for p in split.get("packages", [])}
    print(f"split 包 {len(pkgs)}，核心流程组 {len(PROCESS_GROUPS)}")

    groups = PROCESS_GROUPS[:args.limit] if args.limit else PROCESS_GROUPS
    groups_out, tok = [], 0
    for zh, pkg, var_names, fam in groups:
        if pkg not in pkgs:
            print(f"  [跳过] 主包缺失 {pkg}")
            continue
        agg = analyze_package(pkgs[pkg])
        variants = [(vn, variant_delta(agg, analyze_package(pkgs[vn])))
                    for vn in var_names if vn in pkgs]
        if args.no_ai:
            ans = (f"读表{len(agg['reads'])} 写表{len(agg['writes'])} "
                   f"跨包{len(agg['external_calls'])} 状态写{len(agg['states'])} "
                   f"注释{len(agg['comments'])} 变体{len(variants)}")
        else:
            user = build_user_prompt(zh, pkg, fam, agg, variants)
            try:
                resp = call_ai(SYS, user, "s3-3-coreprocess")
                ans = resp.get("content", "")
                tok += (resp.get("usage") or {}).get("total_tokens", 0)
            except Exception as ex:
                ans = f"[ERROR] {ex}"
        rec = {"zh": zh, "pkg": pkg, "fam": fam, "units": agg["unit_count"],
               "lines": agg["total_lines"], "n_reads": len(agg["reads"]),
               "n_writes": len(agg["writes"]), "answer": ans,
               "writes": agg["writes"]}
        groups_out.append(rec)
        print(f"  {pkg}（{agg['unit_count']}子/{agg['total_lines']}行，"
              f"变体{len(variants)}）tok≈{tok}")
        if args.out_cards:
            d = Path(args.out_cards); d.mkdir(parents=True, exist_ok=True)
            (d / f"{_slug(pkg)}.md").write_text(
                f"# 核心流程卡片：{zh}（{pkg} · {FAMILY[fam]}）\n\n"
                f"**规模**：{agg['unit_count']} 子程序 / {agg['total_lines']} 行\n\n"
                f"**读表**：{', '.join(agg['reads'][:25])}\n\n"
                f"**写表**：{', '.join(agg['writes'])}\n\n"
                f"**跨包调用**：{', '.join(agg['external_calls'][:20])}\n\n"
                f"---\n\n{ans}\n", encoding="utf-8")
        time.sleep(0.3)

    # 家族总览
    overviews = {}
    if not args.no_ai and groups_out:
        for fam in ("BSQM", "BSCH"):
            fam_groups = [g for g in groups_out if g["fam"] == fam]
            if not fam_groups:
                continue
            groups_txt = "\n".join(
                f"  {g['zh']}：主包 {g['pkg']}（{g['units']}子/{g['lines']}行），"
                f"关键写表 {', '.join(g['writes'][:6])}"
                for g in fam_groups)
            try:
                resp = call_ai(SYS, OVERVIEW_PROMPT.format(fam=FAMILY[fam], groups=groups_txt),
                               "s3-3-coreprocess-overview", max_tokens=1000)
                overviews[fam] = resp.get("content", "")
                tok += (resp.get("usage") or {}).get("total_tokens", 0)
            except Exception as ex:
                overviews[fam] = f"[ERROR] {ex}"

    section = render_report_section(groups_out, overviews, tok)
    out = Path(args.out_report)
    prior = out.read_text(encoding="utf-8") if out.exists() else ""
    if SECTION_MARKER in prior:
        prior = prior.split(SECTION_MARKER)[0].rstrip() + "\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(prior.rstrip() + "\n\n---\n\n" + section + "\n", encoding="utf-8")
    print(f"\n完成：{len(groups_out)} 核心流程组，Token {tok:,}\n报告追加：{out}")


if __name__ == "__main__":
    main()
