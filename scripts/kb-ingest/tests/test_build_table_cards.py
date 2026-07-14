"""
P0 表卡片生成器单元测试（纯本地，不连库）

覆盖：类型格式化、字典/热度加载、单表卡片组装（语义填充/主键/覆盖率）、
     P0 名单解析（注释行/大小写）、缺失结构处理、Markdown 渲染要点、JSONL 结构。

关联任务：S3-0 T3-1 P0 表卡片素材（AI-MES-S3PLAN-2026-001）
关联需求单：REQ-MES-AI-20260706-001
作者：AI（芯智云匠）
日期：2026-07-14
"""

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from build_table_cards import (
    fmt_type,
    load_p0_tables,
    load_dict,
    load_table_heat,
    build_card,
    render_card_md,
    render_doc,
)


# ---------------------------------------------------------------------------
# 类型格式化
# ---------------------------------------------------------------------------
def test_fmt_type_varchar_with_length():
    assert fmt_type({"data_type": "VARCHAR2", "length": 30}) == "VARCHAR2(30)"


def test_fmt_type_number_no_length():
    assert fmt_type({"data_type": "NUMBER", "length": 22}) == "NUMBER"


def test_fmt_type_date():
    assert fmt_type({"data_type": "DATE", "length": None}) == "DATE"


# ---------------------------------------------------------------------------
# P0 名单解析
# ---------------------------------------------------------------------------
def test_load_p0_tables_skips_comments_and_uppercases(tmp_path):
    p = tmp_path / "p0.txt"
    p.write_text("# 标题注释\nsms_slab\nSQM_ORD_COM\n\n", encoding="utf-8")
    assert load_p0_tables(str(p)) == ["SMS_SLAB", "SQM_ORD_COM"]


# ---------------------------------------------------------------------------
# 字典加载（含逗号引号语义）
# ---------------------------------------------------------------------------
def test_load_dict_handles_quoted_comma_comment(tmp_path):
    p = tmp_path / "dict.csv"
    with open(p, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["SCHEMA", "TABLE_NAME", "COLUMN_NAME", "DATA_TYPE", "LEN", "COL_COMMENT", "SOURCE"])
        w.writerow(["MESAPUSER", "SMS_SLAB", "SLAB_NO", "VARCHAR2", "30", "板坯号，唯一标识", "DB注释(中文)"])
        w.writerow(["MESAPUSER", "SMS_SLAB", "STS", "VARCHAR2", "2", "", "空"])
    idx = load_dict(str(p))
    assert idx[("SMS_SLAB", "SLAB_NO")] == ("板坯号，唯一标识", "DB注释(中文)")
    assert idx[("SMS_SLAB", "STS")] == ("", "空")


def test_load_table_heat(tmp_path):
    p = tmp_path / "tables.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["TABLE", "READ_PROCS", "WRITE_PROCS", "OPS", "SCORE", "TIER"])
        w.writerow(["SMS_SLAB", "149", "19", "DELETE/INSERT/UPDATE", "187", "P0"])
    heat = load_table_heat(str(p))
    assert heat["SMS_SLAB"]["read"] == "149" and heat["SMS_SLAB"]["tier"] == "P0"


# ---------------------------------------------------------------------------
# 单表卡片组装
# ---------------------------------------------------------------------------
_META_TBL = {
    "owner": "MESAPUSER",
    "name": "SMS_SLAB",
    "num_rows": 1000,
    "columns": [
        {"name": "SLAB_NO", "data_type": "VARCHAR2", "length": 30, "nullable": False,
         "position": 1, "is_primary": True},
        {"name": "STS", "data_type": "VARCHAR2", "length": 2, "nullable": True,
         "position": 2, "is_primary": False},
        {"name": "WGT", "data_type": "NUMBER", "length": 22, "nullable": True,
         "position": 3, "is_primary": False},
    ],
}
_DICT = {
    ("SMS_SLAB", "SLAB_NO"): ("板坯号", "DB注释(中文)"),
    ("SMS_SLAB", "WGT"): ("重量", "SCO_DATA_DIC(D)"),
    # STS 无语义 → 缺口
}
_HEAT = {"SMS_SLAB": {"read": "149", "write": "19", "ops": "DELETE/INSERT/UPDATE",
                      "score": "187", "tier": "P0"}}


def test_build_card_fields_and_coverage():
    card = build_card("SMS_SLAB", _META_TBL, _DICT, _HEAT)
    assert card["pk"] == ["SLAB_NO"]
    assert card["col_total"] == 3
    assert card["col_filled"] == 2      # SLAB_NO + WGT 有语义，STS 空
    assert card["score"] == "187"
    # 列按 position 排序，主键/语义正确落位
    slab = card["columns"][0]
    assert slab["name"] == "SLAB_NO" and slab["is_pk"] and slab["semantic"] == "板坯号"
    sts = card["columns"][1]
    assert sts["semantic"] == "" and sts["source"] == ""


def test_build_card_column_order_by_position():
    shuffled = dict(_META_TBL)
    shuffled["columns"] = list(reversed(_META_TBL["columns"]))
    card = build_card("SMS_SLAB", shuffled, _DICT, _HEAT)
    assert [c["name"] for c in card["columns"]] == ["SLAB_NO", "STS", "WGT"]


def test_render_card_md_contains_key_bits():
    card = build_card("SMS_SLAB", _META_TBL, _DICT, _HEAT)
    md = render_card_md(card)
    assert "### SMS_SLAB" in md
    assert "板坯号" in md
    assert "被读 149" in md
    assert "MESAPUSER" in md
    assert "语义覆盖**：2/3" in md


def test_render_doc_stats_and_missing():
    card = build_card("SMS_SLAB", _META_TBL, _DICT, _HEAT)
    doc = render_doc([card], "MESAPUSER", missing=["V_SOME_VIEW"])
    assert "卡片数（P0 表）：**1**" in doc
    assert "V_SOME_VIEW" in doc          # 缺失结构应提示
    assert "切勿把 owner 当作表名的一部分" in doc  # 防前缀误导须知


def test_jsonl_roundtrip_shape():
    card = build_card("SMS_SLAB", _META_TBL, _DICT, _HEAT)
    line = json.dumps(card, ensure_ascii=False)
    back = json.loads(line)
    assert back["table"] == "SMS_SLAB" and len(back["columns"]) == 3
