"""
AI 网关路由层
关联任务: T1-2-1 / T1-2-3 / T1-2-4
作者: AI
日期: 2026-04-12
"""

import logging
from fastapi import APIRouter, HTTPException, Depends

from app.config import get_settings, Settings
from app.models import GatewayRequest, GatewayResponse, BudgetStatus
from app.services.desensitize import desensitize
from app.services.token_service import get_token_service, TokenBudgetService
from app.services.llm.base import LLMProviderError

log = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/ai", tags=["AI网关"])

# 任务调用序号计数器（生产环境应从 ai_exec_log 查询，Sprint 3 后替换）
_call_seq_counter: dict[str, int] = {}


def _get_provider():
    """根据配置创建 LLM Provider 实例（工厂方法）"""
    settings = get_settings()
    provider_name = settings.ai_provider.lower()

    if provider_name in ("kimi", "openai", "openai_compatible"):
        from app.services.llm.openai_compatible import OpenAICompatibleProvider
        return OpenAICompatibleProvider()
    elif provider_name == "claude":
        # Sprint 1 阶段，生产切换时启用
        raise HTTPException(status_code=501, detail="Claude 原生 Provider 将在生产阶段启用")
    else:
        raise HTTPException(status_code=400, detail=f"不支持的 AI_PROVIDER：{provider_name}")


@router.post("/chat", response_model=GatewayResponse, summary="AI 对话接口（统一入口）")
async def chat(
    request: GatewayRequest,
    token_service: TokenBudgetService = Depends(get_token_service),
    settings: Settings = Depends(get_settings),
):
    """
    AI 统一对话接口

    处理流程：
    1. 预算检查（超限则拒绝非紧急请求）
    2. PII 脱敏（所有消息内容强制过滤）
    3. 调用 LLM Provider（含重试）
    4. Token 消耗累计与告警检查
    5. 返回标准化响应

    安全说明：
    - 所有消息内容经 desensitize() 过滤后才发送至外部 API（CLAUDE.md 4.2）
    - AI_API_KEY 通过环境变量注入，不出现在任何日志或响应中
    """

    # ── 步骤1：预算检查 ────────────────────────────────────────
    budget = token_service.check_budget()
    if budget.is_paused:
        log.warning("[网关] Token 预算已超限，拒绝非紧急请求，任务：%s", request.task_no)
        raise HTTPException(
            status_code=429,
            detail={
                "code": 60004,
                "message": "当日 Token 预算已超限，非紧急任务已暂停",
                "used_tokens": budget.used_tokens,
                "daily_budget": budget.daily_budget,
            }
        )

    # ── 步骤2：PII 脱敏 ────────────────────────────────────────
    desensitized_messages = []
    total_hits = 0
    for msg in request.messages:
        clean_content, hits = desensitize(msg.content)
        total_hits += hits
        desensitized_messages.append(msg.model_copy(update={"content": clean_content}))
    if total_hits > 0:
        log.warning(
            "[网关] 脱敏处理命中 %d 处敏感信息，任务：%s（请排查上游数据）",
            total_hits, request.task_no
        )
    clean_request = request.model_copy(update={"messages": desensitized_messages})

    # ── 步骤3：调用 LLM ───────────────────────────────────────
    call_seq = _call_seq_counter.get(request.task_no, 0) + 1
    _call_seq_counter[request.task_no] = call_seq

    provider = _get_provider()
    try:
        response = await provider.chat(clean_request, call_seq)
    except LLMProviderError as e:
        log.error(
            "[AI网关] 调用失败，任务编号：%s，重试次数：%d，错误：%s",
            request.task_no, settings.ai_max_retries, str(e),
            exc_info=True
        )
        raise HTTPException(
            status_code=502,
            detail={"code": 90003, "message": "AI 网关调用失败", "detail": str(e)}
        )

    # ── 步骤4：Token 消耗累计 ──────────────────────────────────
    token_service.add_usage(
        tokens=response.usage.total_tokens,
        task_no=request.task_no,
        caller=request.caller,
    )

    return response


@router.get("/budget/status", response_model=BudgetStatus, summary="查询当日 Token 预算状态")
async def get_budget_status(
    token_service: TokenBudgetService = Depends(get_token_service),
):
    """查询当日 Token 消耗与预算状态（巡检和监控使用）"""
    return token_service.check_budget()


@router.get("/health", summary="健康检查")
async def health():
    """网关服务健康检查（CI/CD 和巡检探活使用）"""
    settings = get_settings()
    return {
        "status": "ok",
        "provider": settings.ai_provider,
        "model": settings.ai_model,
    }
