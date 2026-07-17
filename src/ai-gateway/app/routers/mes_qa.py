"""
MES 数据问答接口路由
文档编号：AI-MES-GW-2026-001
关联需求单：REQ-MES-AI-20260716-001
作者：AI（芯智云匠）
日期：2026-07-17

提供面向真实 MES 库（钢板/卷材钢厂）的自然语言数据问答能力：
  POST /v1/ai/mes-qa
    - 接收自然语言业务问题
    - 从 S3 理解卡片集合 mes_s3_understanding 做标签驱动 hybrid 检索
      （kind=table 仅表卡片 / proc 仅存储过程卡片 / auto 表+过程混合）
    - 复用网关统一链路（PII 脱敏 → Token 预算管控 → LLM Provider → 用量计入）作答
    - 回答严格接地：只依据检索到的真实表/字段/过程，禁止臆造
    - 返回结构化结果（answer + context_docs + tokens_used）

设计说明：
  LLM 调用不直接呼叫 Provider，而是复用 gateway.chat()，从而与 /v1/ai/chat
  共享同一套脱敏门（CLAUDE.md §4.2）、预算闸（§12）与用量计数，避免旁路。
"""

import time
import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from app.config import get_settings, Settings
from app.models import (
    MesQaRequest, MesQaResponse, ContextDoc,
    GatewayRequest, Message,
)
from app.services.rag_service import get_rag_service, RagDocument
from app.services.token_service import get_token_service, TokenBudgetService
from app.routers.gateway import chat as gateway_chat

log = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/ai", tags=["MES数据问答"])

# 允许的检索范围
_VALID_KINDS = ("auto", "table", "proc")

# ── 系统角色 Prompt（接地约束，防表名/字段臆造）───────────────────────
_MES_QA_SYSTEM = """你是芯智云匠项目的 MES 数据问答助手，服务于山东芯通微电子（钢板/卷材钢厂 MES 系统）。

作答铁律：
1. 只依据下方【知识库上下文】中真实存在的表、字段、存储过程回答，禁止臆造任何表名或字段名。
2. 上下文中没有依据的内容，必须明确说明“知识库中未检索到”，不得凭记忆编造。
3. 基于上下文的合理推断须显式标注“（推断）”，不得表述为确定事实。
4. 回答用中文，结构清晰；涉及表/字段/过程时同时给出准确的英文名。
5. 数据库为 Oracle，表属主为 MESAPUSER；SQL 中直接写表名即可，不要臆加 schema 前缀。"""


def _resolve_kind(kind: str) -> str:
    """校验并归一检索范围，非法值抛 400"""
    k = (kind or "auto").lower()
    if k not in _VALID_KINDS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的 kind：{kind}，可选值：{' / '.join(_VALID_KINDS)}",
        )
    return k


def _retrieve(question: str, kind: str, top_n: int) -> list[RagDocument]:
    """
    按检索范围从 MES 理解卡片集合检索上下文。

    - table / proc：单一范围检索
    - auto：表与过程各检索 top_n 条后交替归并（表优先），按 doc_id 去重，截断至 top_n
    """
    rag = get_rag_service()
    if kind in ("table", "proc"):
        return rag.retrieve_for_mes(question, top_n=top_n, kind=kind)

    # auto：混合两类，交替交织，兼顾“答案在表还是在过程”两种不确定性
    tables = rag.retrieve_for_mes(question, top_n=top_n, kind="table")
    procs = rag.retrieve_for_mes(question, top_n=top_n, kind="proc")
    merged: list[RagDocument] = []
    seen: set = set()
    for pair in zip(tables, procs):
        for d in pair:
            if d.doc_id not in seen:
                seen.add(d.doc_id)
                merged.append(d)
    # 处理两列表长度不等的尾部
    for d in tables[len(procs):] + procs[len(tables):]:
        if d.doc_id not in seen:
            seen.add(d.doc_id)
            merged.append(d)
    return merged[:top_n]


def _to_context_docs(docs: list[RagDocument]) -> list[ContextDoc]:
    """RagDocument → 对外 ContextDoc（兼容 S3 卡片的 source_file/chunk_type 元数据）"""
    result = []
    for d in docs:
        source = d.metadata.get("source") or d.metadata.get("source_file") or "未知来源"
        doc_type = d.metadata.get("type") or d.metadata.get("chunk_type") or "unknown"
        result.append(ContextDoc(
            source=source,
            doc_type=doc_type,
            content_preview=d.content[:200],
            relevance_score=round(max(0.0, 1.0 - d.distance), 4),
        ))
    return result


def _build_user_message(question: str, docs: list[RagDocument]) -> str:
    """拼装含 RAG 上下文的用户消息（STANDARD_TEMPLATE §上下文注入）"""
    rag = get_rag_service()
    context = rag.format_context(docs)
    return (
        f"【知识库上下文（S3 理解卡片，标签驱动 hybrid 检索 Top-{len(docs)}）】\n"
        f"{context}\n\n"
        f"【问题】\n{question}"
    )


@router.post(
    "/mes-qa",
    response_model=MesQaResponse,
    summary="MES 数据问答接口（RAG + LLM，接地作答）",
    description=(
        "接收自然语言业务问题，从真实 MES 理解知识库检索上下文并作答。\n\n"
        "kind 参数：\n"
        "- `auto`：表卡片 + 存储过程卡片混合检索（默认）\n"
        "- `table`：仅检索表/字段理解卡片\n"
        "- `proc`：仅检索存储过程逻辑卡片\n\n"
        "作答严格接地于检索结果，复用网关脱敏门与 Token 预算闸。"
    ),
)
async def mes_qa(
    request: MesQaRequest,
    token_service: Annotated[TokenBudgetService, Depends(get_token_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> MesQaResponse:
    """
    MES 数据问答：RAG 检索 → 复用网关链路调用 LLM → 结构化响应

    处理流程：
    1. 校验检索范围 kind
    2. 标签驱动 hybrid 检索 Top-N 上下文（本地向量，无 Token 消耗）
    3. 构建含上下文的 Prompt
    4. 复用 gateway.chat()：脱敏 → 预算检查 → LLM → 用量计入
    5. 组装结构化响应（answer + context_docs）
    """
    start_ms = int(time.time() * 1000)
    kind = _resolve_kind(request.kind)
    top_n = request.top_n or settings.rag_top_n

    # ── 1. RAG 检索（本地 embedding，不消耗外部 Token）──────────────
    try:
        docs = _retrieve(request.question, kind, top_n)
    except Exception as e:
        log.error("[MES问答] RAG 检索失败 kind=%s err=%s", kind, e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"知识库检索失败：{str(e)}")

    context_docs = _to_context_docs(docs)

    # ── 2. 构建 Prompt 并复用网关链路（脱敏 + 预算 + LLM + 用量）──────
    gw_request = GatewayRequest(
        task_no=request.task_no,
        caller=request.caller,
        module="mes_qa",
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        messages=[
            Message(role="system", content=_MES_QA_SYSTEM),
            Message(role="user", content=_build_user_message(request.question, docs)),
        ],
    )
    # gateway.chat 内部完成：预算超限 429 / 脱敏 / Provider 调用失败 502 / 用量计入
    gw_response = await gateway_chat(gw_request, token_service, settings)

    elapsed_ms = int(time.time() * 1000) - start_ms
    log.info(
        "[MES问答] 完成 kind=%s docs=%d tokens=%d elapsed=%dms",
        kind, len(docs), gw_response.usage.total_tokens, elapsed_ms,
    )

    return MesQaResponse(
        question=request.question,
        kind=kind,
        answer=gw_response.content,
        context_docs=context_docs,
        provider=gw_response.provider,
        model=gw_response.model,
        tokens_used=gw_response.usage.total_tokens,
        response_time_ms=elapsed_ms,
    )
