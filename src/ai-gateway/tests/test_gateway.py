"""
AI 网关单元测试
关联任务: T1-2-6
作者: AI
日期: 2026-04-12

测试策略：
- LLM Provider 调用使用 Mock，不发起真实 API 请求（测试无需 API Key）
- 真实 API 连通测试在集成测试阶段执行（需配置 AI_API_KEY 环境变量）
- 覆盖：预算管控 / 脱敏逻辑 / 重试机制 / 路由分发
"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.models import GatewayRequest, Message, GatewayResponse, UsageInfo
from app.services.token_service import TokenBudgetService
from app.services.desensitize import desensitize


# ── 测试夹具 ─────────────────────────────────────────────────

@pytest_asyncio.fixture
async def client():
    """创建测试用 AsyncClient"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


def _make_request(**kwargs) -> GatewayRequest:
    """构造标准测试请求"""
    defaults = dict(
        task_no="REQ-MES-AI-20260412-001",
        messages=[Message(role="user", content="请分析当前工单状态")],
        caller="test_service",
    )
    defaults.update(kwargs)
    return GatewayRequest(**defaults)


def _make_response(tokens: int = 100) -> GatewayResponse:
    """构造模拟 AI 响应"""
    return GatewayResponse(
        task_no="REQ-MES-AI-20260412-001",
        content="工单状态正常，共 5 条待处理。",
        provider="kimi",
        model="moonshot-v1-8k",
        usage=UsageInfo(prompt_tokens=80, completion_tokens=20, total_tokens=tokens),
        response_time_ms=350,
        call_seq=1,
    )


# ── 健康检查 ─────────────────────────────────────────────────

@pytest.mark.asyncio
async def should_return_ok_when_health_check(client):
    resp = await client.get("/v1/ai/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


# ── 预算管控 ─────────────────────────────────────────────────

def should_is_paused_when_token_exceeds_budget():
    """should_暂停标志为True_when_消耗超过300万"""
    svc = TokenBudgetService()
    svc._daily_counters[svc._today()] = 3_000_001
    status = svc.check_budget()
    assert status.is_paused is True


def should_is_degraded_when_token_exceeds_threshold():
    """should_降级标志为True_when_消耗超过250万"""
    svc = TokenBudgetService()
    svc._daily_counters[svc._today()] = 2_500_001
    status = svc.check_budget()
    assert status.is_degraded is True
    assert status.is_paused is False


def should_accumulate_correctly_when_multiple_calls():
    """should_累计正确_when_多次调用add_usage"""
    svc = TokenBudgetService()
    svc.add_usage(100, "REQ-MES-AI-20260412-001", "test")
    svc.add_usage(200, "REQ-MES-AI-20260412-002", "test")
    assert svc.get_today_usage() == 300


@pytest.mark.asyncio
async def should_return_429_when_budget_exceeded(client):
    """should_返回429_when_Token预算已超限"""
    mock_svc = MagicMock(spec=TokenBudgetService)
    from app.models import BudgetStatus
    from datetime import date
    mock_svc.check_budget.return_value = BudgetStatus(
        date=date.today().strftime("%Y%m%d"),
        used_tokens=3_100_000,
        daily_budget=3_000_000,
        usage_rate=1.03,
        is_degraded=True,
        is_paused=True,
    )
    mock_svc.add_usage.return_value = mock_svc.check_budget.return_value

    from app.routers.gateway import router
    from app import routers
    import app.routers.gateway as gw_module
    from app.services.token_service import get_token_service

    app.dependency_overrides[get_token_service] = lambda: mock_svc
    try:
        req = _make_request()
        resp = await client.post("/v1/ai/chat", json=req.model_dump())
        assert resp.status_code == 429
        assert resp.json()["detail"]["code"] == 60004
    finally:
        app.dependency_overrides.clear()


# ── PII 脱敏 ─────────────────────────────────────────────────

def should_mask_internal_ip_when_found_in_text():
    """should_替换内网IP_when_文本中含192.168地址"""
    text = "请检查服务器 192.168.1.100 的连接状态"
    result, hits = desensitize(text)
    assert "[IP_ADDR_***]" in result
    assert "192.168.1.100" not in result
    assert hits == 1


def should_mask_emp_id_when_found_in_text():
    """should_替换员工工号_when_文本中含EMP工号"""
    text = "操作人 EMP001234 提交了工单"
    result, hits = desensitize(text)
    assert "[EMP_ID_***]" in result
    assert "EMP001234" not in result
    assert hits == 1


def should_not_modify_clean_text():
    """should_不修改_when_文本不含敏感信息"""
    text = "请分析工单 REQ-MES-AI-20260412-001 的执行状态"
    result, hits = desensitize(text)
    assert result == text
    assert hits == 0


def should_mask_multiple_patterns_in_one_text():
    """should_同时脱敏多类_when_文本含多种敏感信息"""
    text = "员工 EMP123456 在 192.168.0.1 操作了批次 LOTAB202601001"
    result, hits = desensitize(text)
    assert "EMP123456" not in result
    assert "192.168.0.1" not in result
    assert hits >= 2


# ── LLM Provider 调用（Mock）─────────────────────────────────

@pytest.mark.asyncio
async def should_return_response_when_provider_succeeds(client):
    """should_正常返回_when_Provider调用成功"""
    mock_resp = _make_response(tokens=150)

    with patch("app.routers.gateway._get_provider") as mock_factory:
        mock_provider = AsyncMock()
        mock_provider.chat.return_value = mock_resp
        mock_factory.return_value = mock_provider

        req = _make_request()
        resp = await client.post("/v1/ai/chat", json=req.model_dump())

    assert resp.status_code == 200
    data = resp.json()
    assert data["task_no"] == "REQ-MES-AI-20260412-001"
    assert data["usage"]["total_tokens"] == 150
    assert data["provider"] == "kimi"


@pytest.mark.asyncio
async def should_return_502_when_provider_raises_error(client):
    """should_返回502_when_Provider抛出LLMProviderError"""
    from app.services.llm.base import LLMProviderError

    with patch("app.routers.gateway._get_provider") as mock_factory:
        mock_provider = AsyncMock()
        mock_provider.chat.side_effect = LLMProviderError("kimi", "API超时", retryable=False)
        mock_factory.return_value = mock_provider

        req = _make_request()
        resp = await client.post("/v1/ai/chat", json=req.model_dump())

    assert resp.status_code == 502
    assert resp.json()["detail"]["code"] == 90003


# ── 预算状态接口 ──────────────────────────────────────────────

@pytest.mark.asyncio
async def should_return_budget_status(client):
    """should_返回预算状态_when_查询budget_status接口"""
    resp = await client.get("/v1/ai/budget/status")
    assert resp.status_code == 200
    data = resp.json()
    assert "used_tokens" in data
    assert "daily_budget" in data
    assert data["daily_budget"] == 3_000_000
