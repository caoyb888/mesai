"""
ITSM 演示接口路由
关联任务：S2.5 演示MVP
作者：AI（芯智云匠）
日期：2026-04-13

提供面向演示场景的 AI 能力接口：
  POST /v1/ai/itsm-demo
    - 接收自然语言需求
    - RAG 检索 ITSM 知识库上下文（ChromaDB）
    - 调用 LLM 生成 SQL 或 Vue 组件代码
    - 返回结构化结果（generated_code + explanation + context_docs）
"""

import time
import logging
from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.models import DemoRequest, DemoResponse, ContextDoc
from app.services.rag_service import get_rag_service, COLLECTION_DB, COLLECTION_API

log = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/ai", tags=["ITSM演示"])

# ── Prompt 模板 ──────────────────────────────────────────────────

_SYSTEM_ROLE_SQL = """你是芯智云匠项目的 MES AI 开发工程师，专注于 ITSM 系统的数据库查询优化。
技术栈：MySQL 8.x，MyBatis Plus，中文注释。
任务类型：根据业务描述生成可执行的 SELECT 查询 SQL。
规范：
  - 禁止 SELECT *，必须明确列出所有返回字段
  - 所有 WHERE 条件使用参数化占位符（:param 格式，便于演示）
  - 逻辑删除字段（is_deleted = 0）必须包含在 WHERE 中
  - 超过3张表的 JOIN 须附执行计划说明
  - 字符串模糊搜索用 CONCAT('%', :param, '%') 而非直接拼接
  - 每个 SQL 片段需有中文注释说明其作用"""

_SYSTEM_ROLE_DML = """你是芯智云匠项目的 MES AI 开发工程师，专注于 ITSM 系统的数据维护操作。
技术栈：MySQL 8.x，中文注释。
任务类型：根据业务描述生成数据变更 SQL（INSERT/UPDATE/DELETE）。
规范：
  - 所有 DML 操作必须包含 WHERE 条件，禁止全表更新或删除
  - 参数使用占位符（:param 格式，便于演示）
  - UPDATE 操作必须更新 updated_at 字段
  - DELETE 操作优先使用逻辑删除（UPDATE is_deleted = 1），而非物理删除
  - 批量操作须说明建议批次大小（≤ 500 条/批）
  - 每个关键步骤需有中文注释"""

_SYSTEM_ROLE_FE = """你是芯智云匠项目的 MES AI 前端开发工程师，服务于山东芯通微电子。
技术栈：Vue 3 + Element Plus + Axios + Pinia。
任务类型：根据业务描述生成完整的 Vue 3 单文件组件（SFC）。
规范：
  - 组件名 PascalCase，文件名 kebab-case
  - 使用 <script setup> 语法（Composition API）
  - 接口调用通过 /api 封装层，不直接调用 axios
  - 增删改操作必须有 ElMessageBox.confirm 二次确认弹窗
  - 所有中文注释
  - 分页默认 10 条/页，支持切换
  - 表格数据为空时展示 el-empty
  - 接口失败时 ElMessage.error 提示，不静默失败"""


def _build_prompt(mode: str, question: str, context: str) -> list[dict]:
    """根据模式构建 LLM 对话消息"""
    if mode == "sql":
        system = _SYSTEM_ROLE_SQL
        task_prefix = "请根据以下 ITSM 数据库结构知识，生成满足需求的 SELECT 查询 SQL："
        output_instruction = (
            "请按以下格式输出：\n"
            "【SQL代码】\n```sql\n<SQL内容>\n```\n\n"
            "【说明】\n<解释查询逻辑、涉及的表、关键条件，以及索引使用建议>"
        )
    elif mode == "dml":
        system = _SYSTEM_ROLE_DML
        task_prefix = "请根据以下 ITSM 数据库结构知识，生成满足需求的数据变更 SQL："
        output_instruction = (
            "请按以下格式输出：\n"
            "【SQL代码】\n```sql\n<SQL内容>\n```\n\n"
            "【说明】\n<解释变更逻辑、影响范围、安全注意事项，以及建议在测试环境验证的步骤>"
        )
    else:  # fe_component
        system = _SYSTEM_ROLE_FE
        task_prefix = "请根据以下 ITSM 接口文档，生成满足需求的 Vue 3 组件："
        output_instruction = (
            "请按以下格式输出：\n"
            "【组件代码】\n```vue\n<完整.vue单文件组件>\n```\n\n"
            "【说明】\n<解释组件功能、Props/Emits说明、依赖的接口、使用方式>"
        )

    user_message = (
        f"[上下文注入]\n"
        f"以下是从知识库检索到的相关文档（Top-{5}，按相关度排序）：\n\n"
        f"{context}\n\n"
        f"[任务描述]\n"
        f"{task_prefix}\n"
        f"需求：{question}\n\n"
        f"[输出格式要求]\n"
        f"{output_instruction}"
    )

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user_message},
    ]


def _parse_response(content: str, mode: str) -> tuple[str, str]:
    """
    从 LLM 响应中解析 generated_code 和 explanation

    :return: (generated_code, explanation)
    """
    if mode in ("sql", "dml"):
        code_tag = "【SQL代码】"
        explain_tag = "【说明】"
        code_fence_open = "```sql"
    else:
        code_tag = "【组件代码】"
        explain_tag = "【说明】"
        code_fence_open = "```vue"

    generated_code = ""
    explanation = ""

    # 提取代码块
    if code_tag in content:
        after_tag = content.split(code_tag, 1)[1]
        if code_fence_open in after_tag:
            inside = after_tag.split(code_fence_open, 1)[1]
            if "```" in inside:
                generated_code = inside.split("```", 1)[0].strip()
        elif explain_tag in after_tag:
            # 没有代码围栏，直接取到【说明】之前
            generated_code = after_tag.split(explain_tag, 1)[0].strip()

    # 提取说明
    if explain_tag in content:
        explanation = content.split(explain_tag, 1)[1].strip()

    # 兜底：如果解析失败，返回原始内容
    if not generated_code:
        # 尝试提取任意代码块
        if "```" in content:
            parts = content.split("```")
            if len(parts) >= 3:
                generated_code = parts[1].strip()
                if generated_code.startswith(("sql", "vue", "javascript")):
                    generated_code = "\n".join(generated_code.split("\n")[1:]).strip()
        if not generated_code:
            generated_code = content

    if not explanation:
        explanation = "（模型未按格式输出，请查看完整响应）"

    return generated_code, explanation


@router.post(
    "/itsm-demo",
    response_model=DemoResponse,
    summary="ITSM 演示接口（RAG + 代码生成）",
    description=(
        "接收自然语言需求，RAG 检索 ITSM 知识库，调用 LLM 生成 SQL 或 Vue 组件代码。\n\n"
        "mode 参数：\n"
        "- `sql`：生成 SELECT 查询 SQL\n"
        "- `dml`：生成 INSERT/UPDATE/DELETE SQL\n"
        "- `fe_component`：生成 Vue 3 前端组件代码"
    ),
)
async def itsm_demo(request: DemoRequest) -> DemoResponse:
    """
    ITSM 演示接口：RAG → LLM → 结构化响应

    处理流程：
    1. 根据 mode 选择知识库集合（DB结构 / API文档）
    2. ChromaDB 向量检索 Top-N 相关文档
    3. 构建含上下文的 Prompt
    4. 调用 LLM（通过 AI Provider）
    5. 解析响应，返回结构化结果
    """
    start_ms = int(time.time() * 1000)
    settings = get_settings()
    mode = request.mode.lower()

    if mode not in ("sql", "dml", "fe_component"):
        raise HTTPException(status_code=400, detail=f"不支持的 mode：{mode}，可选值：sql / dml / fe_component")

    # ── 1. RAG 检索上下文 ─────────────────────────────────────────
    rag = get_rag_service()
    if mode in ("sql", "dml"):
        docs = rag.retrieve_for_sql(request.question)
    else:
        docs = rag.retrieve_for_fe_component(request.question)

    context_text = rag.format_context(docs)

    context_doc_list = [
        ContextDoc(
            source=d.metadata.get("source", "未知"),
            doc_type=d.metadata.get("type", "unknown"),
            content_preview=d.content[:200],
            relevance_score=round(max(0.0, 1.0 - d.distance), 4),
        )
        for d in docs
    ]

    # ── 2. 构建 Prompt 并调用 LLM ────────────────────────────────
    messages = _build_prompt(mode, request.question, context_text)

    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            api_key=settings.ai_api_key,
            base_url=settings.ai_api_base_url,
            timeout=settings.ai_request_timeout,
        )
        resp = await client.chat.completions.create(
            model=settings.ai_model,
            messages=messages,
            temperature=0.2,  # 代码生成用低温度，确保输出确定性
            max_tokens=4096,
        )
        raw_content = resp.choices[0].message.content or ""
        tokens_used = resp.usage.total_tokens if resp.usage else 0
    except Exception as e:
        log.error("LLM 调用失败 mode=%s err=%s", mode, e)
        raise HTTPException(status_code=502, detail=f"AI 服务调用失败：{str(e)}")

    # ── 3. 解析响应 ────────────────────────────────────────────────
    generated_code, explanation = _parse_response(raw_content, mode)

    elapsed_ms = int(time.time() * 1000) - start_ms
    log.info(
        "演示接口完成 mode=%s tokens=%d context_docs=%d elapsed=%dms",
        mode, tokens_used, len(docs), elapsed_ms,
    )

    return DemoResponse(
        mode=mode,
        question=request.question,
        generated_code=generated_code,
        explanation=explanation,
        context_docs=context_doc_list,
        tokens_used=tokens_used,
        response_time_ms=elapsed_ms,
    )
