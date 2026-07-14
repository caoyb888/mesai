"""
脱敏审计工具单元测试（纯本地，复用网关脱敏引擎）

覆盖：PL/SQL 源码 JSON 逐单元审计、纯文本逐行定位、CSV 逐行、类型分派、
     命中明细累加、报告渲染（含结论/分类/采样）、无命中 PASS 结论。

关联任务：S3 训练前置——脱敏审计门
作者：AI（芯智云匠）
日期：2026-07-14
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from audit_materials import (
    audit_plsql_json,
    audit_text_file,
    audit_csv_file,
    dispatch,
    render_report,
)


def test_audit_text_file_locates_hits(tmp_path):
    p = tmp_path / "cards.md"
    p.write_text("正常行无敏感\n服务器 192.168.1.100 异常\n", encoding="utf-8")
    acc = []
    n = audit_text_file(str(p), acc)
    assert n == 2
    assert len(acc) == 1
    assert acc[0]["category"] == "IP_ADDR"
    assert acc[0]["location"] == "L2"
    assert acc[0]["material"] == "cards.md"


def test_audit_plsql_json_iterates_source_units(tmp_path):
    p = tmp_path / "meta.json"
    data = {
        "program_units": [
            {"name": "PKG_A", "object_type": "PACKAGE BODY",
             "source": "BEGIN v := 192.168.0.9; END;"},
            {"name": "PKG_B", "object_type": "PACKAGE BODY", "source": None},  # 无源码跳过
            {"name": "PKG_C", "object_type": "PACKAGE BODY",
             "source": "-- 纯业务无敏感 SELECT SLAB_NO FROM SMS_SLAB"},
        ]
    }
    p.write_text(json.dumps(data), encoding="utf-8")
    acc = []
    audited = audit_plsql_json(str(p), acc)
    assert audited == 2                       # PKG_B 无源码不计
    assert len(acc) == 1
    assert acc[0]["location"] == "PACKAGE BODY PKG_A"
    assert acc[0]["category"] == "IP_ADDR"


def test_audit_csv_file(tmp_path):
    import csv as _csv
    p = tmp_path / "gloss.csv"
    with open(p, "w", newline="", encoding="utf-8-sig") as f:
        w = _csv.writer(f)
        w.writerow(["zh", "ko", "en"])
        w.writerow(["热轧废钢", "열연고철", ""])   # 业务术语，无敏感
    acc = []
    n = audit_csv_file(str(p), acc)
    assert n == 2 and acc == []                 # 业务术语不应命中


def test_dispatch_by_extension(tmp_path):
    j = tmp_path / "m.json"
    j.write_text(json.dumps({"program_units": [{"name": "X", "object_type": "PROC",
                                                 "source": "BEGIN END;"}]}), encoding="utf-8")
    kind, cnt = dispatch(str(j), [])
    assert kind == "plsql" and cnt == 1

    t = tmp_path / "a.md"
    t.write_text("hello\n", encoding="utf-8")
    kind, _ = dispatch(str(t), [])
    assert kind == "text"


def test_render_report_pass_when_no_hits():
    doc = render_report([], {"cards.md": ("text", 100)})
    assert "未命中任何脱敏规则" in doc
    assert "cards.md" in doc


def test_render_report_lists_categories_and_samples():
    acc = [
        {"material": "meta.json", "location": "PKG_A", "category": "IP_ADDR",
         "name": "内网IP", "match": "192.168.0.9"},
        {"material": "cards.md", "location": "L2", "category": "DEVICE_SN",
         "name": "设备序列号", "match": "AB1234567"},
    ]
    doc = render_report(acc, {"meta.json": ("plsql", 2), "cards.md": ("text", 10)})
    assert "命中 2 处" in doc
    assert "IP_ADDR" in doc and "DEVICE_SN" in doc
    assert "192.168.0.9" in doc          # 明细采样含命中串供核验
