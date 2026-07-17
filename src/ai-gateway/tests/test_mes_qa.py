"""
MES 数据问答接口单元测试
关联需求单：REQ-MES-AI-20260716-001
作者：AI（芯智云匠）
日期：2026-07-17

测试策略：
- RAG 检索使用 Mock（本地测试环境无 ChromaDB 与 embedding 模型）
- LLM Provider 使用 Mock（复用网关 _get_provider 钩子，不发起真实 API）
- 覆盖：正常问答 / auto 混检去重 / 检索范围校验 / 预算超限 / Provider 异常 / 入参校验
"""

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


def _mock_provider(tokens: int = 200, content: str = "热轧钢卷实绩表为 SHR_HCOIL_ROLLING_RSLT，主键 COIL_NO。"):
    """构造 Mock LLM Provider（.chat 返回 GatewayResponse）"""
    provider = AsyncMock()
    provider.chat.return_value = GatewayResponse(
        task_no="REQ-MES-AI-20260716-001",
        content=content,
        provider="kimi",
        model="moonshot-v1-32k",
        usage=UsageInfo(prompt_tokens=150, completion_tokens=tokens - 150, total_tokens=tokens),
        response_time_ms=420,
        call_seq=1,
    )
    return provider


# ── 正常问答（kind=table）────────────────────────────────────

@pytest.mark.asyncio
async def should_return_grounded_answer_when_table_question(client):
    """should_返回接地回答_when_表结构问答成功"""
    rag = _mock_rag(table_docs=[_doc("SHR_HCOIL_ROLLING_RSLT"), _doc("SHR_HCOIL_MASTER")])
    with patch("app.routers.mes_qa.get_rag_service", return_value=rag), \
         patch("app.routers.gateway._get_provider", return_value=_mock_provider(tokens=200)):
        resp = await client.post("/v1/ai/mes-qa", json={
            "question": "热轧钢卷实绩表是哪张？主键是什么？", "kind": "table",
        })
    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "table"
    assert "SHR_HCOIL_ROLLING_RSLT" in data["answer"]
    assert data["tokens_used"] == 200
    assert data["provider"] == "kimi"
    assert len(data["context_docs"]) == 2
    assert data["context_docs"][0]["source"] == "SHR_HCOIL_ROLLING_RSLT.md"
    # relevance_score = 1 - distance = 0.8
    assert abs(data["context_docs"][0]["relevance_score"] - 0.8) < 1e-6


# ── auto 混检：表+过程交织去重 ───────────────────────────────

@pytest.mark.asyncio
async def should_merge_and_dedup_when_kind_auto(client):
    """should_表过程交织去重_when_kind为auto"""
    # 表与过程各含一个重叠 doc_id（DUP），应只保留一次
    tables = [_doc("T1"), _doc("DUP")]
    procs = [_doc("P1"), _doc("DUP")]
    rag = _mock_rag(table_docs=tables, proc_docs=procs)
    with patch("app.routers.mes_qa.get_rag_service", return_value=rag), \
         patch("app.routers.gateway._get_provider", return_value=_mock_provider()):
        resp = await client.post("/v1/ai/mes-qa", json={
            "question": "板坯与炉次相关的核心表和过程有哪些？", "kind": "auto", "top_n": 5,
        })
    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "auto"
    sources = [c["source"] for c in data["context_docs"]]
    # T1/P1/DUP 三个不同身份，DUP 去重后仅一次
    assert sources.count("DUP.md") == 1
    assert set(sources) == {"T1.md", "P1.md", "DUP.md"}
    # 交织顺序：表优先 T1，其后 P1
    assert sources[0] == "T1.md"


# ── 检索范围校验 ─────────────────────────────────────────────

@pytest.mark.asyncio
async def should_return_400_when_invalid_kind(client):
    """should_返回400_when_kind非法"""
    rag = _mock_rag(table_docs=[_doc("T1")])
    with patch("app.routers.mes_qa.get_rag_service", return_value=rag), \
         patch("app.routers.gateway._get_provider", return_value=_mock_provider()):
        resp = await client.post("/v1/ai/mes-qa", json={
            "question": "这是一个足够长的问题", "kind": "view",
        })
    assert resp.status_code == 400
    assert "不支持的 kind" in resp.json()["detail"]


# ── 预算超限（复用网关预算闸）───────────────────────────────

@pytest.mark.asyncio
async def should_return_429_when_budget_exceeded(client):
    """should_返回429_when_Token预算超限（复用网关预算闸）"""
    mock_svc = MagicMock(spec=TokenBudgetService)
    mock_svc.check_budget.return_value = BudgetStatus(
        date="20260717", used_tokens=3_100_000, daily_budget=3_000_000,
        usage_rate=1.03, is_degraded=True, is_paused=True,
    )
    rag = _mock_rag(table_docs=[_doc("T1")])
    app.dependency_overrides[get_token_service] = lambda: mock_svc
    try:
        with patch("app.routers.mes_qa.get_rag_service", return_value=rag), \
             patch("app.routers.gateway._get_provider", return_value=_mock_provider()):
            resp = await client.post("/v1/ai/mes-qa", json={
                "question": "热轧钢卷实绩表是哪张？", "kind": "table",
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
    rag = _mock_rag(table_docs=[_doc("T1")])
    provider = AsyncMock()
    provider.chat.side_effect = LLMProviderError("kimi", "API超时", retryable=False)
    with patch("app.routers.mes_qa.get_rag_service", return_value=rag), \
         patch("app.routers.gateway._get_provider", return_value=provider):
        resp = await client.post("/v1/ai/mes-qa", json={
            "question": "热轧钢卷实绩表是哪张？", "kind": "table",
        })
    assert resp.status_code == 502
    assert resp.json()["detail"]["code"] == 90003


# ── 检索失败降级为 500 ──────────────────────────────────────

@pytest.mark.asyncio
async def should_return_500_when_retrieval_fails(client):
    """should_返回500_when_RAG检索抛异常"""
    rag = MagicMock()
    rag.retrieve_for_mes.side_effect = RuntimeError("chromadb 集合不存在")
    with patch("app.routers.mes_qa.get_rag_service", return_value=rag):
        resp = await client.post("/v1/ai/mes-qa", json={
            "question": "热轧钢卷实绩表是哪张？", "kind": "table",
        })
    assert resp.status_code == 500
    assert "知识库检索失败" in resp.json()["detail"]


# ── 入参校验（问题过短）─────────────────────────────────────

@pytest.mark.asyncio
async def should_return_422_when_question_too_short(client):
    """should_返回422_when_问题长度不足5"""
    resp = await client.post("/v1/ai/mes-qa", json={"question": "少", "kind": "table"})
    assert resp.status_code == 422


# ── 默认值：kind 缺省为 auto ────────────────────────────────

@pytest.mark.asyncio
async def should_default_kind_auto_when_omitted(client):
    """should_默认auto_when_未传kind"""
    rag = _mock_rag(table_docs=[_doc("T1")], proc_docs=[_doc("P1")])
    with patch("app.routers.mes_qa.get_rag_service", return_value=rag), \
         patch("app.routers.gateway._get_provider", return_value=_mock_provider()):
        resp = await client.post("/v1/ai/mes-qa", json={
            "question": "板坯与炉次相关的表和过程有哪些？",
        })
    assert resp.status_code == 200
    assert resp.json()["kind"] == "auto"
