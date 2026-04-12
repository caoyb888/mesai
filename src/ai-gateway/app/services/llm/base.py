"""
LLM Provider 抽象基类
关联任务: T1-2-1
作者: AI
日期: 2026-04-12

新增 Provider 只需继承本类并实现 chat() 方法。
切换 Provider 仅需修改环境变量 AI_PROVIDER，无需改动业务代码。
"""

from abc import ABC, abstractmethod
from app.models import GatewayRequest, GatewayResponse


class BaseLLMProvider(ABC):
    """LLM 提供商抽象基类"""

    @abstractmethod
    async def chat(self, request: GatewayRequest, call_seq: int) -> GatewayResponse:
        """
        发起对话请求

        :param request: 网关统一入参（消息已完成 PII 脱敏）
        :param call_seq: 本任务内调用序号（从 1 开始）
        :return: 网关统一响应
        :raises: LLMProviderError - API 调用失败时抛出
        """

    @abstractmethod
    def provider_name(self) -> str:
        """返回提供商标识，如 kimi / claude"""


class LLMProviderError(Exception):
    """LLM Provider 调用异常"""
    def __init__(self, provider: str, message: str, retryable: bool = True):
        super().__init__(message)
        self.provider = provider
        self.retryable = retryable   # 是否可重试（超时可重试，认证失败不重试）
