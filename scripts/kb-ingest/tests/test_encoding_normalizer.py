"""
注释编码治理器单元测试（纯本地，无外部依赖）

覆盖：三级分级（clean/recoverable/garbled/empty）、乱码修复、
     JSON/CSV 输入适配、清单渲染、统计、自测样例一致性。

关联任务：S2.9-3 编码治理与注释质量分级（AI-MES-PLAN-ADJ-2026-001）
作者：AI（芯智云匠）
日期：2026-07-06
"""

import sys
import csv
import json
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from encoding_normalizer import (
    analyze, process, tally, render_report, write_cleaned,
    iter_from_json, iter_from_csv, CommentItem,
    SELF_TEST_SAMPLES,
    TIER_EMPTY, TIER_CLEAN, TIER_RECOVERABLE, TIER_GARBLED,
    _looks_garbled, _is_qmark_loss, _score,
)


# ── 分级：clean / empty ───────────────────────────────────────

@pytest.mark.parametrize("text", ["工单主表", "生产批次号", "inventory order", "OK?", "Y/N"])
def test_clean(text):
    assert analyze(text).tier == TIER_CLEAN


@pytest.mark.parametrize("text", ["인장시험", "시편번호", "작업지시"])
def test_korean_is_clean(text):
    """本 MES 为韩系系统，韩文注释是合法内容，不得误判为乱码"""
    assert analyze(text).tier == TIER_CLEAN


@pytest.mark.parametrize("text", [None, "", "   ", "\t\n"])
def test_empty(text):
    r = analyze(text)
    assert r.tier == TIER_EMPTY


# ── 分级：recoverable（真实 Oracle 乱码两种形态）──────────────

def test_recover_gbk_as_latin1():
    """'工单' 的 GBK 字节被当 Latin-1 解码 → 可恢复"""
    r = analyze("¹¤µ¥")
    assert r.tier == TIER_RECOVERABLE
    assert r.repaired == "工单"
    assert r.method == "latin1→gb18030"
    assert 0.0 < r.confidence <= 1.0


def test_recover_utf8_as_latin1():
    """'工单' 的 UTF-8 字节被当 Latin-1 解码 → 可恢复，且不误选 gbk 逆变换"""
    r = analyze("å·¥å\x8d\x95")
    assert r.tier == TIER_RECOVERABLE
    assert r.repaired == "工单"          # 关键：应选 utf-8 而非 gbk（后者得 '宸ュ崟'）
    assert r.method == "latin1→utf-8"


def test_recover_keeps_original():
    r = analyze("¹¤µ¥")
    assert r.original == "¹¤µ¥"          # 原文完整保留，不静默改源


# ── 分级：garbled ─────────────────────────────────────────────

def test_garbled_replacement_char():
    r = analyze("工�单")
    assert r.tier == TIER_GARBLED
    assert r.repaired == r.original       # 不可恢复时保留原文

def test_garbled_question_mark_loss():
    assert analyze("????").tier == TIER_GARBLED
    assert analyze("？？？").tier == TIER_GARBLED

def test_garbled_control_char():
    assert analyze("工\x00单").tier == TIER_GARBLED


# ── 判定辅助 ──────────────────────────────────────────────────

def test_looks_garbled():
    assert _looks_garbled("¹¤µ¥") is True
    assert _looks_garbled("工单") is False
    assert _looks_garbled("normal english") is False

def test_qmark_loss_threshold():
    assert _is_qmark_loss("????") is True
    assert _is_qmark_loss("OK?") is False   # 单问号不算丢失

def test_score_prefers_common_hanzi():
    # 正确修复 '工单' 应比错误修复 '宸ュ崟'（含片假名）得分高
    assert _score("工单") > _score("宸ュ崟")


# ── 输入适配：JSON ────────────────────────────────────────────

def test_iter_from_json(tmp_path):
    meta = {
        "owner": "MESAPUSER",
        "tables": [{
            "name": "WO_MASTER", "comment": "工单主表",
            "columns": [
                {"name": "WO_ID", "comment": "工单号"},
                {"name": "WO_STATUS", "comment": "¹¤µ¥"},
            ],
        }],
    }
    p = tmp_path / "meta.json"
    p.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    items = list(iter_from_json(str(p)))
    assert len(items) == 3                       # 1 表级 + 2 字段
    assert items[0].kind == "table" and items[0].column is None
    assert items[0].text == "工单主表"
    assert {i.column for i in items if i.column} == {"WO_ID", "WO_STATUS"}


# ── 输入适配：CSV ─────────────────────────────────────────────

def test_iter_from_csv(tmp_path):
    p = tmp_path / "dict.csv"
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["SCHEMA", "TABLE_NAME", "COLUMN_NAME", "DATA_TYPE", "LEN", "COL_COMMENT", "SOURCE"])
        w.writerow(["MESAPUSER", "APP_REPORT", "NAME", "VARCHAR2", "100", "报表名称", "DB注释(中文)"])
        w.writerow(["MESAPUSER", "APP_REPORT", "URL", "VARCHAR2", "300", "", "空"])
    items = list(iter_from_csv(str(p)))
    assert len(items) == 2
    assert items[0].owner == "MESAPUSER"
    assert items[0].table == "APP_REPORT"
    assert items[0].text == "报表名称"
    assert items[0].source_hint == "DB注释(中文)"


# ── 端到端：process / tally / limit ──────────────────────────

def _sample_items():
    return iter([
        CommentItem("O", "T", "C1", "column", "工单主表"),
        CommentItem("O", "T", "C2", "column", ""),
        CommentItem("O", "T", "C3", "column", "¹¤µ¥"),
        CommentItem("O", "T", "C4", "column", "工�单"),
    ])

def test_tally_counts():
    processed = process(_sample_items())
    c = tally(processed)
    assert c["total"] == 4
    assert c[TIER_CLEAN] == 1
    assert c[TIER_EMPTY] == 1
    assert c[TIER_RECOVERABLE] == 1
    assert c[TIER_GARBLED] == 1

def test_process_limit():
    processed = process(_sample_items(), limit=2)
    assert len(processed) == 2


# ── 输出：报告与清洗文件 ──────────────────────────────────────

def test_render_report_sections():
    processed = process(_sample_items())
    md = render_report(processed)
    assert "# 注释乱码清单" in md
    assert "可修复" in md and "不可恢复" in md
    assert "工单" in md                    # 修复建议出现在报告中
    assert "MESAPUSER" not in md          # 本样例 owner=O

def test_write_cleaned_only_suggests_recoverable(tmp_path):
    processed = process(_sample_items())
    out = tmp_path / "cleaned.csv"
    write_cleaned(processed, str(out))
    rows = list(csv.DictReader(open(out, encoding="utf-8")))
    by_col = {r["COLUMN"]: r for r in rows}
    # 仅 recoverable 行给出修复建议，其余建议列为空
    assert by_col["C3"]["REPAIRED_SUGGESTION"] == "工单"
    assert by_col["C1"]["REPAIRED_SUGGESTION"] == ""   # clean 不改
    assert by_col["C4"]["REPAIRED_SUGGESTION"] == ""   # garbled 不猜


# ── 自测样例与代码期望一致 ────────────────────────────────────

def test_self_test_samples_consistent():
    for text, expect in SELF_TEST_SAMPLES:
        assert analyze(text).tier == expect, f"{text!r} 期望 {expect}"
