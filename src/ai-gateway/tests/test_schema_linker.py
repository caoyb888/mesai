"""
Schema Linking 与自纠错重试协议单元测试
关联需求单：REQ-MES-AI-20260730-002（B2.1 重试反馈 / B2.2 Schema Linking）
作者：AI（芯智云匠）
日期：2026-08-01

覆盖：
- SchemaLinker：字典加载、双路候选表、列裁剪与优先级、类型格式化、上限
- 开关：SCHEMA_LINKING_ENABLED 默认关闭 / 开启生效 / 文件缺失降级
- 端点：retry_feedback 进入用户消息（含失败 SQL/原因/真实列清单/修正指令）
- 端点：schema linking 注入文档位于上下文最前（开关开启时）
"""

import json
import os
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.models import GatewayResponse, UsageInfo
from app.services import schema_linker as sl_module
from app.services.schema_linker import SchemaLinker
from app.services.rag_service import RagDocument


DICT_CSV = """﻿SCHEMA,TABLE_NAME,COLUMN_NAME,DATA_TYPE,LEN,COL_COMMENT,SOURCE
MESAPUSER,SMS_HEAT,HEAT_NO,VARCHAR2,20,,空
MESAPUSER,SMS_HEAT,HEAT_STS,VARCHAR2,2,,空
MESAPUSER,SMS_HEAT,CRT_TM,TIMESTAMP(7),11,,空
MESAPUSER,SQM_CHEM_JDG,MTRL_NO,VARCHAR2,20,,空
MESAPUSER,SQM_CHEM_JDG,CHEM_JUDG,VARCHAR2,1,,空
MESAPUSER,SQM_CHEM_JDG,CHEM_JUDG_DTM,VARCHAR2,14,,空
SCOAPUSER,SCO_CODE_DETAIL,CD,VARCHAR2,10,,空
"""


@pytest.fixture
def dict_csv(tmp_path):
    p = tmp_path / "dict.csv"
    p.write_text(DICT_CSV, encoding="utf-8")
    return str(p)


def _doc(doc_id: str, content: str) -> RagDocument:
    return RagDocument(
        doc_id=doc_id, content=content, distance=0.2,
        metadata={"source_file": f"{doc_id}.md", "chunk_type": "s3_table"},
    )


# ── SchemaLinker 单元测试 ────────────────────────────────────

def test_load_only_mesapuser(dict_csv):
    """仅加载 MESAPUSER 业务表（框架 schema 不进 linking 上下文）"""
    linker = SchemaLinker(dict_csv)
    assert "SMS_HEAT" in linker._tables
    assert "SCO_CODE_DETAIL" not in linker._tables


def test_link_from_card_table_mark(dict_csv):
    """候选表来源①：卡片 [表] 标记"""
    linker = SchemaLinker(dict_csv)
    docs = [_doc("SMS_HEAT", "[表] SMS_HEAT 炼钢炉次表，记录冶炼实绩")]
    out = linker.link("2024年7月冶炼多少炉钢", docs)
    assert "SMS_HEAT" in out
    assert "HEAT_NO VARCHAR2(20)" in out
    assert "CRT_TM TIMESTAMP(7)" in out


def test_link_from_question_token(dict_csv):
    """候选表来源②：问题中逐字出现的表名 token"""
    linker = SchemaLinker(dict_csv)
    out = linker.link("统计 SQM_CHEM_JDG 中不合格的记录数", [])
    assert "SQM_CHEM_JDG" in out
    assert "CHEM_JUDG_DTM VARCHAR2(14)" in out   # 真实类型可见（防 TRUNC 误用）


def test_link_empty_when_no_candidate(dict_csv):
    """无候选表时返回空串（不注入）"""
    linker = SchemaLinker(dict_csv)
    assert linker.link("今天天气怎么样", []) == ""


def test_column_prioritization(dict_csv):
    """列裁剪：代码/时间类后缀列优先进入子集"""
    linker = SchemaLinker(dict_csv)
    out = linker.link("查炉次", [_doc("SMS_HEAT", "[表] SMS_HEAT")], max_cols=2)
    # HEAT_STS（_STS 不在后缀表）/ HEAT_NO（_NO 在）等优先级：max_cols=2 时应含 HEAT_NO
    line = [l for l in out.splitlines() if "SMS_HEAT" in l][0]
    assert "HEAT_NO" in line
    assert "仅列前 2 列" in line


# ── 开关测试 ─────────────────────────────────────────────────

def test_switch_default_off(dict_csv, monkeypatch):
    """默认关闭：未设环境变量时 get_schema_linker 返回 None"""
    monkeypatch.delenv("SCHEMA_LINKING_ENABLED", raising=False)
    monkeypatch.setenv("DATA_DICT_CSV", dict_csv)
    sl_module.get_schema_linker.cache_clear()
    assert sl_module.get_schema_linker() is None


def test_switch_on(dict_csv, monkeypatch):
    """开启：SCHEMA_LINKING_ENABLED=true 时返回实例"""
    monkeypatch.setenv("SCHEMA_LINKING_ENABLED", "true")
    monkeypatch.setenv("DATA_DICT_CSV", dict_csv)
    sl_module.get_schema_linker.cache_clear()
    try:
        assert isinstance(sl_module.get_schema_linker(), SchemaLinker)
    finally:
        sl_module.get_schema_linker.cache_clear()


def test_switch_on_but_file_missing(monkeypatch):
    """开启但文件缺失：降级 None 不阻断"""
    monkeypatch.setenv("SCHEMA_LINKING_ENABLED", "true")
    monkeypatch.setenv("DATA_DICT_CSV", "/nonexistent/dict.csv")
    sl_module.get_schema_linker.cache_clear()
    try:
        assert sl_module.get_schema_linker() is None
    finally:
        sl_module.get_schema_linker.cache_clear()


# ── 端点测试 ─────────────────────────────────────────────────

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


def _mock_rag(docs):
    rag = MagicMock()
    rag.retrieve_for_mes.side_effect = lambda question, top_n=None, kind=None: (
        docs if kind != "proc" else []
    )
    rag.format_context.side_effect = lambda ds: "\n".join(d.content for d in ds)
    return rag


def _mock_provider():
    provider = AsyncMock()
    provider.chat.return_value = GatewayResponse(
        task_no="T",
        content=json.dumps({
            "generated": True,
            "sql": "SELECT COIL_NO FROM SHR_HCOIL_ROLLING_RSLT",
            "explanation": "修正后生成。",
            "referenced_tables": ["SHR_HCOIL_ROLLING_RSLT"],
            "referenced_columns": ["COIL_NO"],
            "unanswerable_reason": None,
        }, ensure_ascii=False),
        provider="kimi", model="moonshot-v1-32k",
        usage=UsageInfo(prompt_tokens=100, completion_tokens=50, total_tokens=150),
        response_time_ms=100, call_seq=1,
    )
    return provider


@pytest.mark.asyncio
async def test_retry_feedback_enters_user_message(client):
    """B2.1：retry_feedback 的失败 SQL/原因/真实列清单/修正指令全部进入用户消息"""
    provider = _mock_provider()
    with patch("app.routers.mes_sql.get_rag_service", return_value=_mock_rag([_doc("T1", "卡片")])), \
         patch("app.routers.mes_sql.get_code_dict_service", return_value=None), \
         patch("app.routers.mes_sql.get_schema_linker", return_value=None), \
         patch("app.routers.gateway._get_provider", return_value=provider):
        resp = await client.post("/v1/ai/mes-sql", json={
            "question": "查询钢卷轧制实绩表的卷号和规格",
            "top_n": 3,
            "retry_feedback": {
                "failed_sql": "SELECT COIL_NO, SPEC_CD FROM SHR_HCOIL_ROLLING_RSLT",
                "error_message": "ORA-00904: \"SPEC_CD\": invalid identifier",
                "real_schema": "SHR_HCOIL_ROLLING_RSLT(COIL_NO VARCHAR2(20), RLG_THK NUMBER, RLG_WTH NUMBER)",
            },
        })

    assert resp.status_code == 200
    sent = provider.chat.call_args.args[0].messages[-1].content
    assert "上轮失败反馈" in sent
    assert "SPEC_CD" in sent                       # 失败 SQL 原文
    assert "ORA-00904" in sent                     # 失败原因
    assert "RLG_THK NUMBER" in sent                # 真实列清单
    assert "修正" in sent


@pytest.mark.asyncio
async def test_retry_feedback_ora_text_desensitized(client):
    """F6.2：retry_feedback 中 ORA 错误文本携带的敏感值（批次号等）入模前必须经脱敏门"""
    provider = _mock_provider()
    with patch("app.routers.mes_sql.get_rag_service", return_value=_mock_rag([_doc("T1", "卡片")])), \
         patch("app.routers.mes_sql.get_code_dict_service", return_value=None), \
         patch("app.routers.mes_sql.get_schema_linker", return_value=None), \
         patch("app.routers.gateway._get_provider", return_value=provider):
        resp = await client.post("/v1/ai/mes-sql", json={
            "question": "查询批次轧制实绩",
            "top_n": 3,
            "retry_feedback": {
                "failed_sql": "SELECT COIL_NO FROM T WHERE LOT_NO='LOTAB202601001'",
                "error_message": "ORA-01722: invalid number，批次 LOTAB202601001 转换失败",
                "real_schema": "",
            },
        })

    assert resp.status_code == 200
    sent = provider.chat.call_args.args[0].messages[-1].content
    assert "LOTAB202601001" not in sent      # 原始批次号不得入模
    assert "[LOT_NO_***]" in sent            # 已被脱敏门替换


@pytest.mark.asyncio
async def test_schema_linking_injected_first_when_enabled(client, dict_csv):
    """B2.2：开关开启时 schema linking 文档位于上下文最前，内容含真实列类型"""
    provider = _mock_provider()
    linker = SchemaLinker(dict_csv)
    with patch("app.routers.mes_sql.get_rag_service",
               return_value=_mock_rag([_doc("SMS_HEAT", "[表] SMS_HEAT 炉次表")])), \
         patch("app.routers.mes_sql.get_code_dict_service", return_value=None), \
         patch("app.routers.mes_sql.get_schema_linker", return_value=linker), \
         patch("app.routers.gateway._get_provider", return_value=provider):
        resp = await client.post("/v1/ai/mes-sql",
                                 json={"question": "2024年7月冶炼多少炉钢", "top_n": 3})

    assert resp.status_code == 200
    data = resp.json()
    assert data["context_docs"][0]["doc_type"] == "schema_linking"
    sent = provider.chat.call_args.args[0].messages[-1].content
    assert "Schema Linking" in sent
    assert "HEAT_NO VARCHAR2(20)" in sent
