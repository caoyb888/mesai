"""
MES 取数接口（NL → Oracle SELECT）单元测试
关联需求单：REQ-MES-AI-20260716-001
作者：AI（芯智云匠）
日期：2026-07-18

测试策略：
- RAG 检索使用 Mock（本地测试环境无 ChromaDB 与 embedding 模型）
- LLM Provider 使用 Mock（复用网关 _get_provider 钩子，不发起真实 API）
- 覆盖：正常生成 / JSON 围栏剥离 / 不可答（generated=false）/ 非 JSON 兜底 /
        预算超限 / Provider 异常 / 检索失败 / 入参校验
"""

import json
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.models import GatewayResponse, UsageInfo, BudgetStatus
from app.services.rag_service import RagDocument
from app.services.token_service import TokenBudgetService, get_token_service


# ── 测试夹具 ─────────────────────────────────────────────────

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


def _doc(doc_id: str, content: str = "表结构示例", dist: float = 0.2) -> RagDocument:
    return RagDocument(
        doc_id=doc_id,
        content=content,
        distance=dist,
        metadata={"source_file": f"{doc_id}.md", "chunk_type": "s3_table"},
    )


def _mock_rag(table_docs=None, proc_docs=None):
    """构造 Mock RAG 服务：按 kind 返回不同卡片，format_context 返回拼接文本"""
    rag = MagicMock()

    def _retrieve_for_mes(question, top_n=None, kind=None):
        if kind == "proc":
            return proc_docs if proc_docs is not None else []
        return table_docs if table_docs is not None else []

    rag.retrieve_for_mes.side_effect = _retrieve_for_mes
    rag.format_context.side_effect = lambda docs: "\n".join(d.content for d in docs)
    return rag


def _mock_provider(content: str, tokens: int = 300):
    """构造 Mock LLM Provider（.chat 返回 GatewayResponse，content 即 LLM 原文）"""
    provider = AsyncMock()
    provider.chat.return_value = GatewayResponse(
        task_no="REQ-MES-AI-20260716-001",
        content=content,
        provider="kimi",
        model="moonshot-v1-32k",
        usage=UsageInfo(prompt_tokens=200, completion_tokens=tokens - 200, total_tokens=tokens),
        response_time_ms=520,
        call_seq=1,
    )
    return provider


_OK_JSON = json.dumps({
    "generated": True,
    "sql": "SELECT COIL_NO, HEAT_NO, ROLLING_DATE FROM SHR_HCOIL_ROLLING_RSLT "
           "WHERE ROLLING_DATE >= TRUNC(SYSDATE) - 30 FETCH FIRST 200 ROWS ONLY",
    "explanation": "查询近30天热轧钢卷轧制实绩，涉及实绩表 SHR_HCOIL_ROLLING_RSLT。",
    "referenced_tables": ["SHR_HCOIL_ROLLING_RSLT"],
    "referenced_columns": ["COIL_NO", "HEAT_NO", "ROLLING_DATE"],
    "unanswerable_reason": None,
}, ensure_ascii=False)


# ── 正常生成 SELECT ─────────────────────────────────────────

@pytest.mark.asyncio
async def should_generate_select_when_valid_request(client):
    """should_生成Oracle_SELECT_when_知识库命中表结构"""
    rag = _mock_rag(table_docs=[_doc("SHR_HCOIL_ROLLING_RSLT")], proc_docs=[])
    with patch("app.routers.mes_sql.get_rag_service", return_value=rag), \
         patch("app.routers.gateway._get_provider", return_value=_mock_provider(_OK_JSON)):
        resp = await client.post("/v1/ai/mes-sql", json={
            "question": "查询最近一个月热轧钢卷的轧制实绩",
        })
    assert resp.status_code == 200
    data = resp.json()
    assert data["generated"] is True
    assert data["sql"].upper().startswith("SELECT")
    assert "SHR_HCOIL_ROLLING_RSLT" in data["sql"]
    assert data["referenced_tables"] == ["SHR_HCOIL_ROLLING_RSLT"]
    assert "COIL_NO" in data["referenced_columns"]
    assert data["unanswerable_reason"] is None
    assert data["tokens_used"] == 300
    assert len(data["context_docs"]) == 1


# ── JSON 被 Markdown 围栏包裹时仍能解析 ─────────────────────

@pytest.mark.asyncio
async def should_strip_fence_when_json_wrapped(client):
    """should_剥离```json围栏_when_模型加了Markdown围栏"""
    fenced = f"```json\n{_OK_JSON}\n```"
    rag = _mock_rag(table_docs=[_doc("SHR_HCOIL_ROLLING_RSLT")], proc_docs=[])
    with patch("app.routers.mes_sql.get_rag_service", return_value=rag), \
         patch("app.routers.gateway._get_provider", return_value=_mock_provider(fenced)):
        resp = await client.post("/v1/ai/mes-sql", json={
            "question": "查询最近一个月热轧钢卷的轧制实绩",
        })
    assert resp.status_code == 200
    data = resp.json()
    assert data["generated"] is True
    assert data["sql"].upper().startswith("SELECT")


# ── 知识库无依据：generated=false ───────────────────────────

@pytest.mark.asyncio
async def should_mark_unanswerable_when_generated_false(client):
    """should_标记不可答_when_知识库无对应表字段"""
    payload = json.dumps({
        "generated": False,
        "sql": "",
        "explanation": "",
        "referenced_tables": [],
        "referenced_columns": [],
        "unanswerable_reason": "知识库中未检索到设备能耗相关的表",
    }, ensure_ascii=False)
    rag = _mock_rag(table_docs=[_doc("T1")], proc_docs=[])
    with patch("app.routers.mes_sql.get_rag_service", return_value=rag), \
         patch("app.routers.gateway._get_provider", return_value=_mock_provider(payload)):
        resp = await client.post("/v1/ai/mes-sql", json={
            "question": "查询每台设备的实时能耗曲线数据",
        })
    assert resp.status_code == 200
    data = resp.json()
    assert data["generated"] is False
    assert data["sql"] == ""
    assert "能耗" in data["unanswerable_reason"]


# ── 非 JSON 输出兜底：视为未生成 ────────────────────────────

@pytest.mark.asyncio
async def should_fallback_when_non_json_output(client):
    """should_兜底为未生成_when_模型未按JSON输出"""
    rag = _mock_rag(table_docs=[_doc("T1")], proc_docs=[])
    with patch("app.routers.mes_sql.get_rag_service", return_value=rag), \
         patch("app.routers.gateway._get_provider",
               return_value=_mock_provider("这是一段普通文字，没有 JSON。")):
        resp = await client.post("/v1/ai/mes-sql", json={
            "question": "查询最近一个月热轧钢卷的轧制实绩",
        })
    assert resp.status_code == 200
    data = resp.json()
    assert data["generated"] is False
    assert data["sql"] == ""
    assert data["unanswerable_reason"] == "LLM 输出格式异常"


# ── 预算超限（复用网关预算闸）───────────────────────────────

@pytest.mark.asyncio
async def should_return_429_when_budget_exceeded(client):
    """should_返回429_when_Token预算超限（复用网关预算闸）"""
    mock_svc = MagicMock(spec=TokenBudgetService)
    mock_svc.check_budget.return_value = BudgetStatus(
        date="20260718", used_tokens=3_100_000, daily_budget=3_000_000,
        usage_rate=1.03, is_degraded=True, is_paused=True,
    )
    rag = _mock_rag(table_docs=[_doc("T1")], proc_docs=[])
    app.dependency_overrides[get_token_service] = lambda: mock_svc
    try:
        with patch("app.routers.mes_sql.get_rag_service", return_value=rag), \
             patch("app.routers.gateway._get_provider", return_value=_mock_provider(_OK_JSON)):
            resp = await client.post("/v1/ai/mes-sql", json={
                "question": "查询最近一个月热轧钢卷的轧制实绩",
            })
        assert resp.status_code == 429
        assert resp.json()["detail"]["code"] == 60004
    finally:
        app.dependency_overrides.clear()


# ── Provider 异常（复用网关 502 处理）───────────────────────

@pytest.mark.asyncio
async def should_return_502_when_provider_error(client):
    """should_返回502_when_Provider抛出LLMProviderError"""
    from app.services.llm.base import LLMProviderError
    rag = _mock_rag(table_docs=[_doc("T1")], proc_docs=[])
    provider = AsyncMock()
    provider.chat.side_effect = LLMProviderError("kimi", "API超时", retryable=False)
    with patch("app.routers.mes_sql.get_rag_service", return_value=rag), \
         patch("app.routers.gateway._get_provider", return_value=provider):
        resp = await client.post("/v1/ai/mes-sql", json={
            "question": "查询最近一个月热轧钢卷的轧制实绩",
        })
    assert resp.status_code == 502
    assert resp.json()["detail"]["code"] == 90003


# ── 检索失败降级为 500 ──────────────────────────────────────

@pytest.mark.asyncio
async def should_return_500_when_retrieval_fails(client):
    """should_返回500_when_RAG检索抛异常"""
    rag = MagicMock()
    rag.retrieve_for_mes.side_effect = RuntimeError("chromadb 集合不存在")
    with patch("app.routers.mes_sql.get_rag_service", return_value=rag):
        resp = await client.post("/v1/ai/mes-sql", json={
            "question": "查询最近一个月热轧钢卷的轧制实绩",
        })
    assert resp.status_code == 500
    assert "知识库检索失败" in resp.json()["detail"]


# ── 入参校验（问题过短）─────────────────────────────────────

@pytest.mark.asyncio
async def should_return_422_when_question_too_short(client):
    """should_返回422_when_问题长度不足5"""
    resp = await client.post("/v1/ai/mes-sql", json={"question": "少"})
    assert resp.status_code == 422
