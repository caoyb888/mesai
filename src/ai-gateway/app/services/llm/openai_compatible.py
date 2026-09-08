"""
OpenAI 兼容 Provider（支持 Kimi / OpenAI / 其他兼容服务）
关联任务: T1-2-2（开发阶段使用 Kimi API）
作者: AI
日期: 2026-04-12

配置说明：
    AI_PROVIDER=kimi
    AI_API_KEY=<Kimi API Key，通过环境变量注入，禁止硬编码>
    AI_API_BASE_URL=https://api.moonshot.cn/v1
    AI_MODEL=moonshot-v1-8k

切换至生产 Claude 时，修改环境变量即可，代码无需变更：
    AI_PROVIDER=claude
    AI_API_KEY=<Claude API Key>
    AI_API_BASE_URL=https://api.anthropic.com/v1
    AI_MODEL=claude-sonnet-4-6
"""

import time
import logging
import asyncio
from openai import AsyncOpenAI, APITimeoutError, APIConnectionError, AuthenticationError

from app.config import get_settings
from app.models import GatewayRequest, GatewayResponse, UsageInfo
from app.services.llm.base import BaseLLMProvider, LLMProviderError

log = logging.getLogger(__name__)


class OpenAICompatibleProvider(BaseLLMProvider):
    """
    OpenAI 兼容接口 Provider
    支持：Kimi（月之暗面）/ OpenAI / 其他兼容服务
    """

    def __init__(self):
        settings = get_settings()
        if not settings.ai_api_key:
            raise ValueError(
                "AI_API_KEY 未配置，请通过环境变量注入（CLAUDE.md 4.1 禁止硬编码）"
            )
        self._client = AsyncOpenAI(
            api_key=settings.ai_api_key,
            base_url=settings.ai_api_base_url,
            timeout=settings.ai_request_timeout,
            max_retries=0,   # 重试由网关层统一管理
        )
        self._model = settings.ai_model
        self._provider = settings.ai_provider
        self._max_retries = settings.ai_max_retries
        self._retry_delay = settings.ai_retry_delay

    def provider_name(self) -> str:
        return self._provider

    async def chat(self, request: GatewayRequest, call_seq: int) -> GatewayResponse:
        """
        调用 OpenAI 兼容接口
        包含重试逻辑：网络超时/连接错误最多重试 max_retries 次
        """
        messages = [{"role": m.role, "content": m.content} for m in request.messages]
        # kimi-k* 为推理模型：temperature 仅允许 1；正文前有 reasoning，需放大 max_tokens
        _is_reasoning = str(self._model).startswith("kimi-k")
        kwargs = {
            "model": self._model,
            "messages": messages,
            "temperature": 1 if _is_reasoning else request.temperature,
        }
        _mt = request.max_tokens or (2048 if _is_reasoning else 0)
        if _mt:
            kwargs["max_tokens"] = max(_mt, 2048) if _is_reasoning else _mt

        last_error = None
        for attempt in range(1, self._max_retries + 1):
            try:
                t0 = time.time()
                log.info(
                    "[AI网关] 调用 %s，任务编号：%s，调用序号：%d，第 %d/%d 次",
                    self._provider, request.task_no, call_seq, attempt, self._max_retries
                )
                response = await self._client.chat.completions.create(**kwargs)
                elapsed_ms = int((time.time() - t0) * 1000)

                _msg = response.choices[0].message
                content = _msg.content or ""
                if not content and _is_reasoning:
                    content = (getattr(_msg, "reasoning_content", None)
                               or (getattr(_msg, "model_extra", None) or {}).get("reasoning_content")
                               or "")
                usage = response.usage

                log.info(
                    "[AI网关] 调用成功，任务：%s，序号：%d，耗时：%dms，"
                    "prompt_tokens：%d，completion_tokens：%d，total：%d",
                    request.task_no, call_seq, elapsed_ms,
                    usage.prompt_tokens, usage.completion_tokens, usage.total_tokens
                )

                return GatewayResponse(
                    task_no=request.task_no,
                    content=content,
                    provider=self._provider,
                    model=self._model,
                    usage=UsageInfo(
                        prompt_tokens=usage.prompt_tokens,
                        completion_tokens=usage.completion_tokens,
                        total_tokens=usage.total_tokens,
                    ),
                    response_time_ms=elapsed_ms,
                    call_seq=call_seq,
                )

            except AuthenticationError as e:
                # 认证失败不重试，直接抛出
                log.error("[AI网关] 认证失败（%s），请检查 AI_API_KEY 配置：%s",
                          self._provider, str(e))
                raise LLMProviderError(self._provider, f"API Key 无效：{e}", retryable=False)

            except (APITimeoutError, APIConnectionError) as e:
                last_error = e
                log.warning(
                    "[AI网关] 网络异常，第 %d/%d 次，%s：%s",
                    attempt, self._max_retries, type(e).__name__, str(e)
                )
                if attempt < self._max_retries:
                    await asyncio.sleep(self._retry_delay * attempt)  # 指数退避

            except Exception as e:
                last_error = e
                log.error("[AI网关] 未预期异常，第 %d 次：%s", attempt, str(e), exc_info=True)
                if attempt < self._max_retries:
                    await asyncio.sleep(self._retry_delay)

        log.error(
            "[AI网关] 调用失败，任务编号：%s，重试次数：%d，错误：%s",
            request.task_no, self._max_retries, str(last_error)
        )
        raise LLMProviderError(
            self._provider,
            f"调用失败（已重试 {self._max_retries} 次）：{last_error}",
            retryable=False
        )
