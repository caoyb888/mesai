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

# ── ITSM 数据库真实表结构（用于注入 Prompt，防止 LLM 猜错表名/字段名）──────
_ITSM_DB_SCHEMA = """
数据库：itsm_dev（PostgreSQL 15.x）
所有表均在 public schema，引用时直接写表名，禁止加任何 schema 前缀。

[核心工单表]
itsm_ticket(id, ticket_no, model_id, title, description, status, priority, source,
  created_user_id, assigned_group_id, assigned_user_id, form_data_json,
  sla_deadline_response, sla_deadline_resolve, response_at, resolved_at,
  sla_response_status, sla_resolve_status, close_reason, closed_at,
  created_at, updated_at, created_by, is_deleted/*smallint,0=正常,1=删除*/)

[工单流转日志]
itsm_ticket_flow_log(id, ticket_id, from_status, to_status, action, actor_type,
  operator_id, remark, extra_json, operated_at)
-- 注意：流转表名是 itsm_ticket_flow_log，无 transition_time/transition_by 字段

[工单评论]
itsm_ticket_comment(id, ticket_id, user_id, content, is_internal, created_at, updated_at, created_by, is_deleted)

[工单附件]
itsm_attachment(id, ref_type, ref_id, file_name, file_size, file_type, file_ext,
  bucket_name, object_key, md5, created_at, created_by, is_deleted)

[工单关联配置项]
itsm_ticket_ci_map(ticket_id, ci_id, ci_type, ci_name, relation_type, created_at, created_by)

[SLA 记录]
itsm_sla_record(id, ticket_id, sla_policy_id, priority, created_at_tick,
  response_deadline, resolve_deadline, actual_response_at, actual_resolve_at,
  response_work_minutes, resolve_work_minutes, response_status, resolve_status,
  suspended_minutes, created_at, updated_at)

[SLA 策略]
itsm_sla_policy(id, name, service_time_type, service_time_json,
  response_minutes_low/medium/high/critical, resolve_minutes_low/medium/high/critical,
  warn_threshold_pct, created_at, updated_at, created_by, is_deleted)

[用户]
itsm_user(id, account_no, employee_name, password_hash, phone, email, avatar_url,
  dept_id, status, last_login_at, last_login_ip, created_at, updated_at, created_by, is_deleted)

[用户组]
itsm_user_group(id, name, dept_id, description, created_at, updated_at, created_by, is_deleted)
itsm_user_group_member(group_id, user_id, role_in_group, joined_at)

[部门]
itsm_dept(id, name, parent_id, sort_order, created_at, updated_at, created_by, is_deleted)

[角色权限]
itsm_role(id, code, name, description, is_system, created_at, updated_at, created_by, is_deleted)
itsm_permission(id, code, name, type, resource_path, parent_id, sort_order, created_at, updated_at, created_by, is_deleted)
itsm_role_permission(role_id, permission_id)
itsm_user_role(user_id, role_id, granted_at, granted_by)

[服务目录与服务模型]
itsm_service_catalog(id, name, parent_id, icon_url, sort_order, created_at, updated_at, created_by, is_deleted)
itsm_service_model(id, catalog_id, name, code, description, workflow_def_id, sla_policy_id,
  default_group_id, status, created_at, updated_at, created_by, is_deleted)

[工作流定义]
itsm_workflow_def(id, name, code, states_json, transitions_json, allow_close_states,
  version, status, created_at, updated_at, created_by, is_deleted)

[配置项 CMDB]
itsm_ci(id, ci_no, ci_type_id, ci_type_code, name, status, environment,
  owner_group_id, ip_address, hostname, attributes, description, created_at, updated_at, created_by, is_deleted)
itsm_ci_type(id, name, code, icon, attribute_schema, description, sort_order, created_at, updated_at, created_by, is_deleted)
itsm_ci_relation(id, source_ci_id, target_ci_id, relation_type, description, created_at, updated_at, created_by, is_deleted)

[知识库]
itsm_kb_article(id, category_id, title, summary, keywords, status, current_version,
  published_at, published_by, reviewer_id, reviewed_at, review_comment,
  view_count, useful_count, created_at, updated_at, created_by, is_deleted)
itsm_kb_article_version(id, article_id, version, content, change_note, created_at, created_by)
itsm_kb_category(id, name, parent_id, sort_order, created_at, updated_at, created_by, is_deleted)

[通知]
itsm_notify_log(id, channel_type, ticket_id, recipient, subject, content, status,
  retry_count, error_msg, sent_at, created_at)
itsm_notify_template(id, event_type, channel_type, subject, body_template, description, is_enabled, created_at, updated_at, created_by, is_deleted)
itsm_notify_channel(id, channel_type, name, config_json, is_enabled, rate_limit_count, daily_quota, updated_at, updated_by)

[排班]
itsm_roster_team(id, name, description, group_id, created_at, updated_at, created_by, is_deleted)
itsm_roster_team_member(team_id, user_id, sort_order, joined_at)
itsm_roster_schedule(id, team_id, user_id, schedule_date, shift_type, start_time, end_time, is_on_duty, created_at, updated_at, created_by, is_deleted)

[审计日志]
itsm_audit_log(id, user_id, account_no, login_ip, user_agent, trace_id, module, action,
  resource_type, resource_id, before_json, after_json, result, error_msg, operated_at)

[表单字段]
itsm_form_field(id, model_id, field_key, field_type, label, placeholder, required,
  options_json, validation_json, default_value, sort_order, created_at, updated_at, created_by, is_deleted)
"""

# ── Prompt 模板 ──────────────────────────────────────────────────

_SYSTEM_ROLE_SQL = f"""你是芯智云匠项目的 MES AI 开发工程师，专注于 ITSM 系统的数据库查询优化。
任务类型：根据业务描述生成可直接执行的 SELECT 查询 SQL（无需参数占位符）。

{_ITSM_DB_SCHEMA}

规范：
  - 禁止 SELECT *，必须明确列出所有返回字段，字段名必须来自上方真实表结构
  - WHERE 条件直接将业务描述中的具体值以字面量嵌入 SQL（如 title = 'ITSM数据库查询性能下降'），禁止使用任何占位符（:param、$1、? 等）
  - 有 is_deleted 字段的表，WHERE 中必须加 is_deleted = 0
  - 超过3张表的 JOIN 须附执行计划说明
  - 字符串模糊搜索用 LIKE '%关键词%' 格式
  - 每个 SQL 片段需有中文注释说明其作用"""

_SYSTEM_ROLE_DML = f"""你是芯智云匠项目的 MES AI 开发工程师，专注于 ITSM 系统的数据维护操作。
任务类型：根据业务描述生成可直接执行的数据变更 SQL（INSERT/UPDATE/DELETE，无需参数占位符）。

{_ITSM_DB_SCHEMA}

规范：
  - 所有 DML 操作必须包含 WHERE 条件，禁止全表更新或删除
  - WHERE 条件直接将业务描述中的具体值以字面量嵌入 SQL，禁止使用任何占位符（:param、$1、? 等）
  - 字段名必须来自上方真实表结构，禁止使用不存在的字段
  - UPDATE 操作必须更新 updated_at 字段（使用 NOW()）
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
