"""
AI 网关请求/响应数据模型
关联任务: T1-2-1
作者: AI
日期: 2026-04-12
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


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


# ── 演示接口（Demo）模型 ─────────────────────────────────────────

class DemoQueryMode(str):
    """演示查询模式枚举"""
    SQL = "sql"           # 生成 SELECT 查询 SQL
    DML = "dml"           # 生成 INSERT/UPDATE/DELETE SQL
    FE_COMPONENT = "fe_component"  # 生成 Vue 3 前端组件代码


class DemoRequest(BaseModel):
    """ITSM 演示查询请求"""
    question: str = Field(..., min_length=5, max_length=500, description="自然语言需求描述")
    mode: str = Field(
        "sql",
        description="生成模式：sql（查询SQL）/ dml（变更SQL）/ fe_component（Vue组件）",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "question": "查询过去7天内所有状态为OPEN的工单，按创建时间倒序排列，只取前20条",
                    "mode": "sql",
                },
                {
                    "question": "将编号为TKT-2026-001的工单状态更新为CLOSED，同时记录关闭时间",
                    "mode": "dml",
                },
                {
                    "question": "生成一个ITSM工单列表页组件，包含工单编号、标题、状态、创建时间列，支持按状态筛选",
                    "mode": "fe_component",
                },
            ]
        }
    )


class ContextDoc(BaseModel):
    """RAG 检索到的上下文文档片段"""
    source: str
    doc_type: str
    content_preview: str = Field(..., description="内容摘要（前200字符）")
    relevance_score: float = Field(..., description="相关度得分（1 - distance）")


class DemoResponse(BaseModel):
    """ITSM 演示查询响应"""
    mode: str
    question: str
    generated_code: str = Field(..., description="AI 生成的 SQL 或 Vue 组件代码")
    explanation: str = Field(..., description="AI 对生成代码的说明")
    context_docs: list[ContextDoc] = Field(default_factory=list, description="使用的知识库上下文片段")
    tokens_used: int
    response_time_ms: int


# ── MES 数据问答接口模型（真实 MES S3 理解知识库）─────────────────

class MesQaRequest(BaseModel):
    """
    MES 数据问答请求。

    面向真实 MES 库（钢板/卷材钢厂）的表结构与存储过程问答：
    先从 S3 理解卡片集合 RAG 检索（标签驱动 hybrid），再由 LLM 基于检索到的
    真实表/字段/过程作答，严格接地防臆造。
    """
    question: str = Field(..., min_length=5, max_length=500, description="自然语言业务问题")
    kind: str = Field(
        "auto",
        description="检索范围：auto（表+过程混合，默认）/ table（仅表卡片）/ proc（仅存储过程卡片）",
    )
    top_n: Optional[int] = Field(
        None, ge=1, le=10, description="RAG 检索条数，不传则用配置默认（预算降级时自动缩减）",
    )
    task_no: str = Field(
        "REQ-MES-AI-20260716-001",
        description="需求单编号，用于 Token 成本归集，格式 REQ-MES-AI-YYYYMMDD-NNN",
    )
    caller: str = Field("mes_qa", description="调用来源模块标识")
    max_tokens: Optional[int] = Field(800, ge=64, le=4096, description="最大生成 Token 数")
    temperature: float = Field(0.2, ge=0.0, le=1.0, description="生成温度，默认 0.2（问答场景求稳）")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"question": "热轧钢卷的轧制实绩数据保存在哪张表？主键是什么？", "kind": "table"},
                {"question": "质保书是通过哪些存储过程签发的？主流程是怎样的？", "kind": "proc"},
                {"question": "板坯是按炉次管理的吗？相关核心表有哪些？", "kind": "auto"},
            ]
        }
    )


class MesQaResponse(BaseModel):
    """MES 数据问答响应"""
    question: str
    kind: str = Field(..., description="实际生效的检索范围（auto/table/proc）")
    answer: str = Field(..., description="AI 基于知识库上下文生成的回答")
    context_docs: list[ContextDoc] = Field(
        default_factory=list, description="本次作答引用的知识库上下文片段（含相关度）",
    )
    provider: str = Field(..., description="实际使用的 AI 提供商")
    model: str = Field(..., description="实际使用的模型名称")
    tokens_used: int = Field(..., description="本次调用消耗 Token 总数")
    response_time_ms: int


# ── MES 取数（NL → Oracle SELECT）接口模型 ─────────────────────────

class MesSqlRequest(BaseModel):
    """
    MES 取数请求：自然语言 → Oracle 只读 SELECT 生成。

    先从 S3 理解卡片集合 RAG 检索真实表/字段/存储过程，再由 LLM 严格接地
    生成 Oracle 方言 SELECT（只读、禁 SELECT *、禁臆造表名/字段名）。
    SQL 的安全校验与只读执行在 Spring Boot 后端完成，网关侧只负责生成。
    """
    question: str = Field(..., min_length=5, max_length=500, description="自然语言取数需求")
    top_n: Optional[int] = Field(
        None, ge=1, le=10, description="RAG 检索条数，不传则用配置默认（预算降级时自动缩减）",
    )
    task_no: str = Field(
        "REQ-MES-AI-20260716-001",
        description="需求单编号，用于 Token 成本归集，格式 REQ-MES-AI-YYYYMMDD-NNN",
    )
    caller: str = Field("mes_sql", description="调用来源模块标识")
    max_tokens: Optional[int] = Field(1200, ge=64, le=4096, description="最大生成 Token 数")
    temperature: float = Field(0.1, ge=0.0, le=1.0, description="生成温度，默认 0.1（取数场景求确定性）")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"question": "查询最近一个月热轧钢卷的轧制实绩，包含卷号、炉次号、轧制日期"},
                {"question": "统计每个牌号的板坯数量，按数量倒序"},
            ]
        }
    )


class MesSqlResponse(BaseModel):
    """MES 取数响应：生成的 Oracle SELECT + 接地元数据"""
    question: str
    generated: bool = Field(..., description="是否成功生成 SQL（false 表示知识库依据不足，见 unanswerable_reason）")
    sql: str = Field("", description="生成的 Oracle 只读 SELECT（未生成时为空串）")
    explanation: str = Field("", description="对查询逻辑、涉及表/字段、关键条件的中文说明")
    referenced_tables: list[str] = Field(default_factory=list, description="SQL 引用的表名（英文，须来自知识库上下文）")
    referenced_columns: list[str] = Field(default_factory=list, description="SQL 引用的关键字段名（英文）")
    unanswerable_reason: Optional[str] = Field(None, description="未能生成 SQL 的原因（知识库无对应表/字段时填写）")
    context_docs: list[ContextDoc] = Field(
        default_factory=list, description="本次生成引用的知识库上下文片段（含相关度）",
    )
    provider: str = Field(..., description="实际使用的 AI 提供商")
    model: str = Field(..., description="实际使用的模型名称")
    tokens_used: int = Field(..., description="本次调用消耗 Token 总数")
    response_time_ms: int
