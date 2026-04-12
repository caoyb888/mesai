"""
AI 网关请求/响应数据模型
关联任务: T1-2-1
作者: AI
日期: 2026-04-12
"""

from typing import Optional
from pydantic import BaseModel, Field


class Message(BaseModel):
    """对话消息"""
    role: str = Field(..., description="角色：system / user / assistant")
    content: str = Field(..., description="消息内容（发送前已完成 PII 脱敏）")


class GatewayRequest(BaseModel):
    """AI 网关统一入参"""
    task_no: str = Field(..., description="需求单编号，格式 REQ-MES-AI-YYYYMMDD-NNN")
    messages: list[Message] = Field(..., description="对话消息列表")
    caller: str = Field(..., description="调用来源模块，如 task_service / kb_service")
    dept: Optional[str] = Field(None, description="所属部门，用于 Token 成本分摊")
    module: Optional[str] = Field(None, description="所属 MES 模块，用于成本分摊")
    max_tokens: Optional[int] = Field(None, description="最大生成 Token 数，不传则由 Provider 默认")
    temperature: Optional[float] = Field(0.3, description="生成温度，默认 0.3（代码生成场景）")
    stream: bool = Field(False, description="是否流式响应（当前阶段仅支持非流式）")


class UsageInfo(BaseModel):
    """Token 消耗明细"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class GatewayResponse(BaseModel):
    """AI 网关统一响应"""
    task_no: str
    content: str = Field(..., description="AI 生成内容")
    provider: str = Field(..., description="实际使用的 AI 提供商，如 kimi / claude")
    model: str = Field(..., description="实际使用的模型名称")
    usage: UsageInfo
    response_time_ms: int = Field(..., description="本次调用耗时（毫秒）")
    call_seq: int = Field(..., description="本任务内调用序号（从 1 开始）")


class BudgetStatus(BaseModel):
    """当日 Token 预算状态"""
    date: str
    used_tokens: int
    daily_budget: int
    usage_rate: float
    is_degraded: bool = Field(..., description="是否已触发降级（RAG Top-5 → Top-3）")
    is_paused: bool = Field(..., description="是否已暂停非紧急任务")
