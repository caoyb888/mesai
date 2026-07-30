"""
MES 取数接口路由（自然语言 → Oracle 只读 SELECT 生成）
文档编号：AI-MES-GW-2026-002
关联需求单：REQ-MES-AI-20260716-001
作者：AI（芯智云匠）
日期：2026-07-18

恢复原始系统设计：AI 基于真实 MES 数据库结构知识，生成满足需求的 SELECT 查询 SQL。
  POST /v1/ai/mes-sql
    - 接收自然语言取数需求
    - 从 S3 理解卡片集合 mes_s3_understanding 做标签驱动 hybrid 检索（表 + 存储过程）
    - 复用网关统一链路（PII 脱敏 → Token 预算管控 → LLM Provider → 用量计入）生成 SQL
    - 严格接地：只引用检索到的真实表/字段，禁止臆造；只生成只读 SELECT
    - 返回结构化结果（sql + explanation + referenced_tables + context_docs）

安全边界（与后端协同）：
  本端点只“生成” SQL，不执行。SQL 的安全校验（仅 SELECT / 禁 DDL·DML / 禁 SELECT *）
  与只读执行（Oracle 只读数据源 + 行数封顶）由 Spring Boot 后端 messql 模块完成。
"""

import json
import time
import logging
from typing import Annotated, Optional

from fastapi import APIRouter, HTTPException, Depends

from app.config import get_settings, Settings
from app.models import (
    MesSqlRequest, MesSqlResponse, ContextDoc,
    GatewayRequest, Message,
)
from app.services.rag_service import get_rag_service, RagDocument
from app.services.code_dict import get_code_dict_service
from app.services.token_service import get_token_service, TokenBudgetService
from app.routers.gateway import chat as gateway_chat

log = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/ai", tags=["MES取数"])

# ── 系统角色 Prompt（Oracle 方言 + 只读 + 接地约束，防表名/字段臆造）─────────
_MES_SQL_SYSTEM = """你是芯智云匠项目的 MES 数据查询工程师，服务于山东芯通微电子（钢板/卷材钢厂 MES 系统）。
任务：根据业务取数需求，生成一条可直接执行的 Oracle 只读 SELECT 查询。

数据库事实：
- 数据库为 Oracle，表属主为 MESAPUSER；SQL 中直接写表名即可，不要臆加 schema 前缀。
- 本库日期时间字段绝大多数为 VARCHAR2(14) 字符串，格式 yyyymmddhh24miss（如 20241128160055），不是 DATE 类型。

生成铁律：
1. 只依据下方【知识库上下文】中真实存在的表、字段生成 SQL，禁止臆造任何表名或字段名。
2. 只能生成 SELECT 查询，严禁 INSERT/UPDATE/DELETE/MERGE 及任何 DDL（CREATE/ALTER/DROP/TRUNCATE）。
3. 禁止 SELECT *，必须显式列出每个返回字段，字段名必须来自上下文中的真实字段。
4. 只输出单条语句，不要以分号结尾，不要包含多条语句或注释注入。
5. 分页/限行使用 Oracle 语法 FETCH FIRST n ROWS ONLY（或 ROWNUM），不要使用 LIMIT。
6. 时间范围过滤：对 *_DTM / *_DT 等字符串时间字段必须用字符串比较（如 field >= TO_CHAR(SYSDATE-n,'YYYYMMDDHH24MISS')），禁止对其使用 TRUNC/TO_DATE/DATE 运算；仅当上下文明确标注某列为 DATE 类型时才可使用 DATE 函数。模糊匹配用 LIKE '%关键词%'。
7. 如果知识库上下文中找不到能满足需求的表或字段，不要编造，必须将 generated 置为 false 并在 unanswerable_reason 说明缺少什么。
8. 字段名必须与上下文逐字一致，禁止任何形式的“近似改写”（漏词/加词/简写，如把 PROD_TOT_JDG_DTM 写成 PROD_JDG_DTM）。
9. 代码类字段（*_CD / *_TY / *_GRD 等）的过滤值必须使用上下文中给出的代码值；需求中的中文业务词（如“不合格”）须先映射为代码值再过滤，上下文中无映射时在 explanation 中说明，禁止直接拿中文标签对代码字段做等值过滤。

只输出一个 JSON 对象（不要包裹任何额外文字或 Markdown 围栏），结构如下：
{
  "generated": true 或 false,
  "sql": "生成的 Oracle SELECT（未生成时为空字符串）",
  "explanation": "中文说明：查询逻辑、涉及的表与字段、关键条件",
  "referenced_tables": ["引用到的表名（英文）"],
  "referenced_columns": ["引用到的关键字段名（英文）"],
  "unanswerable_reason": "未能生成时填写缺少的表/字段说明，成功时为 null"
}"""


def _retrieve(question: str, top_n: int) -> list[RagDocument]:
    """
    从 MES 理解卡片集合检索表 + 存储过程上下文（auto 混合）。

    表与过程各检索 top_n 条后交替归并（表优先），按 doc_id 去重，截断至 top_n；
    取数以表结构为主，故表卡片优先。
    """
    rag = get_rag_service()
    tables = rag.retrieve_for_mes(question, top_n=top_n, kind="table")
    procs = rag.retrieve_for_mes(question, top_n=top_n, kind="proc")
    merged: list[RagDocument] = []
    seen: set = set()
    for pair in zip(tables, procs):
        for d in pair:
            if d.doc_id not in seen:
                seen.add(d.doc_id)
                merged.append(d)
    for d in tables[len(procs):] + procs[len(tables):]:
        if d.doc_id not in seen:
            seen.add(d.doc_id)
            merged.append(d)
    return merged[:top_n]


def _inject_code_dict(question: str, docs: list[RagDocument]) -> list[RagDocument]:
    """
    代码字典定向注入（铁律 9 的弹药供给）。

    扫描问题与检索卡片内容中的大写标识符，凡命中 SCO_CODE_DETAIL 代码组的，
    把该组的可用码值作为一条补充上下文追加（列名=代码组逐字约定，无向量歧义）。
    字典不可用（CSV 缺失/加载失败）时原样返回，降级不阻断主链路。
    """
    cds = get_code_dict_service()
    if cds is None:
        return docs
    groups = cds.lookup_in_texts([question] + [d.content for d in docs])
    if not groups:
        return docs
    content = (
        "[代码字典] 以下代码字段的可用码值（源自 SCO_CODE_DETAIL，"
        "对这些字段过滤时必须使用码值而非中文标签）：\n"
        + cds.format_groups(groups)
    )
    injected = RagDocument(
        doc_id="code_dict:injected",
        content=content,
        distance=0.0,
        metadata={"source": "SCO_CODE_DETAIL 代码字典", "type": "code_dict"},
    )
    log.info("[MES取数] 代码字典注入 groups=%d (%s)", len(groups), "/".join(groups.keys()))
    return docs + [injected]


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
        f"【取数需求】\n{question}"
    )


def _extract_json(content: str) -> Optional[dict]:
    """
    从 LLM 响应中稳健解析 JSON 对象。

    容忍 ```json 围栏与前后多余文字：优先剥离围栏，再截取首个 '{' 到末个 '}'。
    解析失败返回 None（交由上层走兜底：视为未生成）。
    """
    if not content:
        return None
    text = content.strip()
    # 剥离 Markdown 代码围栏
    if "```" in text:
        fence = text.find("```")
        after = text[fence + 3:]
        if after[:4].lower() == "json":
            after = after[4:]
        end = after.find("```")
        if end >= 0:
            text = after[:end].strip()
    # 截取首个 { 到末个 }
    start = text.find("{")
    last = text.rfind("}")
    if start < 0 or last <= start:
        return None
    try:
        obj = json.loads(text[start:last + 1])
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        return None


def _as_str_list(val) -> list[str]:
    """将模型输出的任意值归一为字符串列表（防御 LLM 返回 null/字符串/混合类型）"""
    if isinstance(val, list):
        return [str(x).strip() for x in val if x is not None and str(x).strip()]
    if isinstance(val, str) and val.strip():
        return [val.strip()]
    return []


@router.post(
    "/mes-sql",
    response_model=MesSqlResponse,
    summary="MES 取数接口（RAG + LLM，生成 Oracle 只读 SELECT）",
    description=(
        "接收自然语言取数需求，从真实 MES 理解知识库检索上下文，生成一条 Oracle 只读 SELECT。\n\n"
        "严格接地于检索结果（防臆造表名/字段名），只生成 SELECT，禁止 SELECT *。\n"
        "本端点只负责生成；SQL 安全校验与只读执行由 Spring Boot 后端完成。"
    ),
)
async def mes_sql(
    request: MesSqlRequest,
    token_service: Annotated[TokenBudgetService, Depends(get_token_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> MesSqlResponse:
    """
    MES 取数：RAG 检索 → 复用网关链路调用 LLM 生成 Oracle SELECT → 结构化响应

    处理流程：
    1. 标签驱动 hybrid 检索 Top-N 上下文（本地向量，无 Token 消耗）
    2. 构建含上下文的 SQL 生成 Prompt
    3. 复用 gateway.chat()：脱敏 → 预算检查 → LLM → 用量计入
    4. 解析 LLM 返回的 JSON，组装结构化响应（sql + 接地元数据）
    """
    start_ms = int(time.time() * 1000)
    top_n = request.top_n or settings.rag_top_n

    # ── 1. RAG 检索（本地 embedding，不消耗外部 Token）──────────────
    try:
        docs = _retrieve(request.question, top_n)
        docs = _inject_code_dict(request.question, docs)
    except Exception as e:
        log.error("[MES取数] RAG 检索失败 err=%s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"知识库检索失败：{str(e)}")

    context_docs = _to_context_docs(docs)

    # ── 2. 构建 Prompt 并复用网关链路（脱敏 + 预算 + LLM + 用量）──────
    gw_request = GatewayRequest(
        task_no=request.task_no,
        caller=request.caller,
        module="mes_sql",
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        messages=[
            Message(role="system", content=_MES_SQL_SYSTEM),
            Message(role="user", content=_build_user_message(request.question, docs)),
        ],
    )
    gw_response = await gateway_chat(gw_request, token_service, settings)

    # ── 3. 解析 LLM 返回的 JSON ────────────────────────────────────
    parsed = _extract_json(gw_response.content)
    if parsed is None:
        # 兜底：模型未按 JSON 输出，视为未生成，原文放入说明便于排查
        generated = False
        sql = ""
        explanation = "模型未按约定 JSON 格式输出，无法安全提取 SQL，请重试或缩小问题范围。"
        referenced_tables: list[str] = []
        referenced_columns: list[str] = []
        unanswerable_reason = "LLM 输出格式异常"
    else:
        sql = (parsed.get("sql") or "").strip()
        generated = bool(parsed.get("generated")) and bool(sql)
        explanation = (parsed.get("explanation") or "").strip()
        referenced_tables = _as_str_list(parsed.get("referenced_tables"))
        referenced_columns = _as_str_list(parsed.get("referenced_columns"))
        unanswerable_reason = parsed.get("unanswerable_reason") or (
            None if generated else "知识库上下文中未找到可满足需求的表或字段"
        )

    elapsed_ms = int(time.time() * 1000) - start_ms
    log.info(
        "[MES取数] 完成 generated=%s docs=%d tokens=%d elapsed=%dms",
        generated, len(docs), gw_response.usage.total_tokens, elapsed_ms,
    )

    return MesSqlResponse(
        question=request.question,
        generated=generated,
        sql=sql,
        explanation=explanation,
        referenced_tables=referenced_tables,
        referenced_columns=referenced_columns,
        unanswerable_reason=unanswerable_reason,
        context_docs=context_docs,
        provider=gw_response.provider,
        model=gw_response.model,
        tokens_used=gw_response.usage.total_tokens,
        response_time_ms=elapsed_ms,
    )
