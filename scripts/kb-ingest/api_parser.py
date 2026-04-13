#!/usr/bin/env python3
"""
OpenAPI 3.0 接口文档解析器 → Markdown 接口卡片

将 OpenAPI YAML/JSON 文件按 Tag（模块）解析为结构化 Markdown，
每个 Tag 生成一个独立的 .md 文件（即一个知识库 chunk 集合的原材料）。
同时生成一个全局概览文件（api_overview.md）。

用法：
    python api_parser.py \
        --input  docs/knowledge-base/api-docs/itsm/raw/ \
        --output docs/knowledge-base/api-docs/itsm/parsed/ \
        --system itsm

输出示例（认证.md）：
    ## 模块：认证（Auth）
    **系统**：itsm | **接口数**：6
    **模块说明**：登录、登出、Token 刷新、密码管理
    ...

关联任务：S2-2 T2-2-1
作者：AI（芯智云匠）
日期：2026-04-13
需求单：REQ-MES-AI-20260412-005
"""

import re
import sys
import yaml
import json
import argparse
import logging
from pathlib import Path
from typing import Any, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)


# ── 工具函数 ──────────────────────────────────────────────────

def _resolve_ref(ref: str, components: dict) -> dict:
    """解析 $ref 引用，返回 Schema 定义"""
    if not ref.startswith("#/components/schemas/"):
        return {}
    schema_name = ref.split("/")[-1]
    return components.get("schemas", {}).get(schema_name, {})


def _schema_to_table_rows(
    schema: dict,
    components: dict,
    prefix: str = "",
    depth: int = 0,
    visited: Optional[set] = None,
) -> list[str]:
    """
    将 Schema 对象递归展开为 Markdown 表格行列表。
    每行格式：| 字段名 | 类型 | 必填 | 说明 |
    """
    if visited is None:
        visited = set()

    rows = []
    if depth > 3:
        return rows

    # 解引用
    if "$ref" in schema:
        ref_name = schema["$ref"].split("/")[-1]
        if ref_name in visited:
            return [f"| {prefix}... | （循环引用 {ref_name}）| - | - |"]
        visited = visited | {ref_name}
        schema = _resolve_ref(schema["$ref"], components)

    # allOf 合并
    if "allOf" in schema:
        for sub in schema["allOf"]:
            rows.extend(_schema_to_table_rows(sub, components, prefix, depth, visited))
        return rows

    props = schema.get("properties", {})
    required_fields = set(schema.get("required", []))

    for field_name, field_schema in props.items():
        full_name = f"{prefix}{field_name}" if prefix else field_name
        required_mark = "✅" if field_name in required_fields else ""

        # 解引用嵌套
        actual_schema = field_schema
        if "$ref" in field_schema:
            ref_name = field_schema["$ref"].split("/")[-1]
            actual_schema = _resolve_ref(field_schema["$ref"], components)
            field_type = f"object({ref_name})"
        elif field_schema.get("type") == "array":
            items = field_schema.get("items", {})
            if "$ref" in items:
                field_type = f"array({items['$ref'].split('/')[-1]})"
            else:
                field_type = f"array({items.get('type', 'object')})"
        else:
            field_type = field_schema.get("type", "object")
            if "enum" in field_schema:
                enum_vals = "/".join(str(v) for v in field_schema["enum"])
                field_type = f"{field_type}[{enum_vals}]"

        desc = field_schema.get("description", actual_schema.get("description", ""))
        desc = desc.replace("\n", " ").replace("|", "｜")[:80]

        rows.append(f"| `{full_name}` | {field_type} | {required_mark} | {desc} |")

        # 展开嵌套对象（仅展开一层）
        if depth == 0 and actual_schema.get("properties"):
            nested_rows = _schema_to_table_rows(
                actual_schema, components, f"{full_name}.", depth + 1, visited
            )
            rows.extend(nested_rows)

    return rows


def _render_request_body(request_body: dict, components: dict) -> str:
    """渲染请求体说明"""
    if not request_body:
        return ""

    lines = ["\n**请求体（application/json）：**\n"]
    lines.append("| 字段 | 类型 | 必填 | 说明 |")
    lines.append("|------|------|------|------|")

    content = request_body.get("content", {})
    schema = content.get("application/json", {}).get("schema", {})

    rows = _schema_to_table_rows(schema, components)
    if rows:
        lines.extend(rows)
    else:
        lines.append("| （见接口说明）| - | - | - |")

    return "\n".join(lines)


def _render_parameters(parameters: list, components: dict) -> str:
    """渲染路径/查询参数说明"""
    if not parameters:
        return ""

    # 展开 $ref 参数引用
    resolved = []
    comp_params = components.get("parameters", {})
    for p in parameters:
        if "$ref" in p:
            param_name = p["$ref"].split("/")[-1]
            p = comp_params.get(param_name, p)
        resolved.append(p)

    path_params = [p for p in resolved if p.get("in") == "path"]
    query_params = [p for p in resolved if p.get("in") == "query"]

    lines = []
    if path_params:
        lines.append("\n**路径参数：**\n")
        lines.append("| 参数名 | 类型 | 必填 | 说明 |")
        lines.append("|--------|------|------|------|")
        for p in path_params:
            schema = p.get("schema", {})
            ptype = schema.get("type", "string")
            req = "✅" if p.get("required") else ""
            desc = p.get("description", "").replace("|", "｜")
            lines.append(f"| `{p['name']}` | {ptype} | {req} | {desc} |")

    if query_params:
        lines.append("\n**查询参数：**\n")
        lines.append("| 参数名 | 类型 | 必填 | 说明 |")
        lines.append("|--------|------|------|------|")
        for p in query_params:
            schema = p.get("schema", {})
            ptype = schema.get("type", "string")
            if "enum" in schema:
                ptype += f"[{'/'.join(str(v) for v in schema['enum'])}]"
            req = "✅" if p.get("required") else ""
            desc = p.get("description", "").replace("|", "｜")
            lines.append(f"| `{p['name']}` | {ptype} | {req} | {desc} |")

    return "\n".join(lines)


def _render_response(responses: dict, components: dict) -> str:
    """渲染响应说明（只取 200）"""
    resp_200 = responses.get("200", {})
    if not resp_200:
        return ""

    desc = resp_200.get("description", "")
    content = resp_200.get("content", {})
    schema = content.get("application/json", {}).get("schema", {})

    lines = [f"\n**响应（200）：** {desc}\n"]

    # 展开响应结构
    rows = _schema_to_table_rows(schema, components)
    if rows:
        lines.append("| 字段 | 类型 | 必填 | 说明 |")
        lines.append("|------|------|------|------|")
        lines.extend(rows[:20])  # 最多展示 20 行，避免 chunk 过大

    return "\n".join(lines)


# ── 核心解析逻辑 ──────────────────────────────────────────────

class ApiParser:
    """OpenAPI 3.0 文档解析器，按 Tag 生成 Markdown"""

    def __init__(self, system_name: str):
        self.system_name = system_name

    def parse_file(self, yaml_path: Path) -> dict[str, str]:
        """
        解析 OpenAPI YAML 文件。

        返回：
            dict[tag_slug, markdown_content]
            包含一个特殊 key "overview" 对应全局概览
        """
        with open(yaml_path, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)

        info = doc.get("info", {})
        tags_meta = {t["name"]: t.get("description", "") for t in doc.get("tags", [])}
        components = doc.get("components", {})
        paths = doc.get("paths", {})

        # 按 Tag 分组所有接口
        tag_ops: dict[str, list[dict]] = {tag: [] for tag in tags_meta}
        for path, methods in paths.items():
            for method, operation in methods.items():
                if method not in ("get", "post", "put", "patch", "delete"):
                    continue
                for tag in operation.get("tags", ["未分类"]):
                    tag_ops.setdefault(tag, []).append({
                        "method": method.upper(),
                        "path": path,
                        "operation": operation,
                    })

        results: dict[str, str] = {}

        # 生成全局概览
        results["overview"] = self._render_overview(info, tags_meta, tag_ops, components)

        # 生成各模块 Markdown
        for tag, ops in tag_ops.items():
            tag_desc = tags_meta.get(tag, "")
            results[tag] = self._render_tag_module(tag, tag_desc, ops, components)

        log.info(
            "解析完成：%d 个 Tag，%d 个接口",
            len(tag_ops),
            sum(len(v) for v in tag_ops.values()),
        )
        return results

    def _render_overview(
        self,
        info: dict,
        tags_meta: dict,
        tag_ops: dict,
        components: dict,
    ) -> str:
        """生成全局 API 概览 Markdown"""
        title = info.get("title", self.system_name + " API")
        version = info.get("version", "1.0.0")
        desc = info.get("description", "").strip()

        total_ops = sum(len(v) for v in tag_ops.values())
        schemas = list(components.get("schemas", {}).keys())

        lines = [
            f"## {self.system_name.upper()} API 总览",
            "",
            f"**系统**：{title} | **版本**：{version} | **接口总数**：{total_ops} | **数据模型数**：{len(schemas)}",
            "",
        ]

        # 提取认证方式说明
        auth_lines = [l for l in desc.split("\n") if l.strip()]
        if auth_lines:
            lines.append("**系统说明：**")
            lines.extend(auth_lines[:12])
            lines.append("")

        # 模块汇总表
        lines.append("**模块汇总：**")
        lines.append("")
        lines.append("| 模块 | 接口数 | 说明 |")
        lines.append("|------|--------|------|")
        for tag, ops in tag_ops.items():
            tag_desc = tags_meta.get(tag, "").replace("|", "｜")
            lines.append(f"| {tag} | {len(ops)} | {tag_desc} |")

        lines.append("")

        # 通用响应结构
        api_resp_schema = components.get("schemas", {}).get("ApiResponse", {})
        if api_resp_schema:
            lines.append("**统一响应结构（ApiResponse）：**")
            lines.append("")
            lines.append("| 字段 | 类型 | 说明 |")
            lines.append("|------|------|------|")
            for field, fschema in api_resp_schema.get("properties", {}).items():
                ftype = fschema.get("type", "object")
                fdesc = fschema.get("description", "").replace("|", "｜")
                lines.append(f"| `{field}` | {ftype} | {fdesc} |")
            lines.append("")

        # 常用 Schema
        lines.append("**常用数据模型：**")
        lines.append("")
        lines.append("| Schema 名 | 用途 |")
        lines.append("|-----------|------|")
        schema_desc_map = {
            "PageRequest": "分页请求参数（page/pageSize/orderBy/orderDir）",
            "PageResponse": "分页响应结构（list/total/page/pageSize/totalPages）",
            "LoginResponseData": "登录成功返回（accessToken/refreshToken/expiresIn/userInfo）",
            "UserBasicInfo": "用户基本信息（工号/姓名/邮件/角色/部门）",
            "CreateTicketRequest": "创建工单请求体（modelId/title/priority/formData）",
            "TicketBasicInfo": "工单基本信息（工单号/状态/标题/优先级/SLA截止）",
            "SlaPolicy": "SLA策略（响应时限/解决时限/服务时间类型）",
            "SlaStatistics": "SLA统计（达标率/平均时长/违约数）",
        }
        for schema_name in schemas:
            sdesc = schema_desc_map.get(schema_name, "")
            lines.append(f"| `{schema_name}` | {sdesc} |")

        lines.extend([
            "",
            "---",
            f"*chunk_id: {self.system_name}_api_overview*",
            f"*chunk_type: api_overview*",
            f"*关联任务：S2-2 T2-2-1 · 作者：AI（芯智云匠）· 日期：2026-04-13*",
        ])
        return "\n".join(lines)

    def _render_tag_module(
        self,
        tag: str,
        tag_desc: str,
        ops: list[dict],
        components: dict,
    ) -> str:
        """生成单个 Tag 模块的 Markdown"""
        slug = re.sub(r"[^\w\u4e00-\u9fff]", "_", tag)

        lines = [
            f"## 模块：{tag}",
            "",
            f"**系统**：{self.system_name.upper()} | "
            f"**接口数**：{len(ops)} | "
            f"**模块说明**：{tag_desc}",
            "",
        ]

        # 接口速查表
        lines.append("### 接口速查表")
        lines.append("")
        lines.append("| 方法 | 路径 | 说明 | 是否需要鉴权 |")
        lines.append("|------|------|------|------------|")
        for item in ops:
            op = item["operation"]
            auth_required = "security" not in op or op.get("security") != []
            auth_mark = "✅ JWT" if auth_required else "❌ 免鉴权"
            summary = op.get("summary", "").replace("|", "｜")
            lines.append(
                f"| **{item['method']}** | `{item['path']}` | {summary} | {auth_mark} |"
            )
        lines.append("")

        # 详细接口说明
        lines.append("### 接口详情")
        lines.append("")
        for item in ops:
            op = item["operation"]
            method = item["method"]
            path = item["path"]
            summary = op.get("summary", "")
            description = op.get("description", "")
            operation_id = op.get("operationId", "")

            lines.append(f"#### {method} {path}")
            lines.append("")
            if summary:
                lines.append(f"**功能**：{summary}")
            if description:
                lines.append(f"**说明**：{description}")
            if operation_id:
                lines.append(f"**operationId**：`{operation_id}`")

            # 鉴权说明
            if "security" in op:
                if op["security"] == []:
                    lines.append("**鉴权**：❌ 免鉴权接口")
                else:
                    lines.append("**鉴权**：✅ 需要 Bearer Token")
            else:
                lines.append("**鉴权**：✅ 需要 Bearer Token（全局默认）")

            # 参数
            params_md = _render_parameters(op.get("parameters", []), components)
            if params_md:
                lines.append(params_md)

            # 请求体
            body_md = _render_request_body(op.get("requestBody", {}), components)
            if body_md:
                lines.append(body_md)

            # 响应
            resp_md = _render_response(op.get("responses", {}), components)
            if resp_md:
                lines.append(resp_md)

            lines.append("")

        lines.extend([
            "---",
            f"*chunk_id: {self.system_name}_{slug}_api_module*",
            f"*chunk_type: api_module*",
            f"*关联任务：S2-2 T2-2-1 · 作者：AI（芯智云匠）· 日期：2026-04-13*",
        ])
        return "\n".join(lines)


# ── 入口 ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="OpenAPI → Markdown 解析器")
    parser.add_argument(
        "--input", required=True,
        help="输入目录（含 .yaml/.json 文件）或单个文件路径"
    )
    parser.add_argument(
        "--output", required=True,
        help="输出目录（parsed/）"
    )
    parser.add_argument(
        "--system", default="itsm",
        help="系统名称标识，用于 chunk_id 前缀（默认：itsm）"
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 收集 YAML/JSON 文件
    if input_path.is_file():
        yaml_files = [input_path]
    else:
        yaml_files = list(input_path.glob("*.yaml")) + \
                     list(input_path.glob("*.yml")) + \
                     list(input_path.glob("*.json"))

    if not yaml_files:
        log.error("未找到 YAML/JSON 文件：%s", args.input)
        sys.exit(1)

    api_parser = ApiParser(system_name=args.system)
    total_files = 0

    for yaml_file in yaml_files:
        log.info("解析文件：%s", yaml_file.name)
        results = api_parser.parse_file(yaml_file)

        for tag, content in results.items():
            # 文件名：overview.md 或 <tag>.md
            safe_name = re.sub(r"[^\w\u4e00-\u9fff\-]", "_", tag)
            out_file = output_dir / f"{safe_name}.md"
            out_file.write_text(content, encoding="utf-8")
            tokens_est = len(content) // 3
            log.info(
                "  → 生成 %s（约 %d tokens）",
                out_file.name, tokens_est
            )
            total_files += 1

    log.info("完成：共生成 %d 个 Markdown 文件 → %s", total_files, output_dir)


if __name__ == "__main__":
    main()
