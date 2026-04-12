#!/usr/bin/env python3
"""
PostgreSQL DDL 解析器 → Markdown 表卡片

将甲方提供的 PostgreSQL DDL 文件解析为结构化 Markdown，
每张表生成一个独立的 .md 文件（即一个知识库 chunk 的原材料）。

用法：
    python ddl_parser.py --input mes-ddl/02-工艺管理/raw/ \
                         --output mes-ddl/02-工艺管理/parsed/ \
                         --module 工艺管理

输出示例（process_route.md）：
    ## 表：process_route（工艺路线主表）
    **模块**：工艺管理 | **Schema**：public
    **业务说明**：定义产品的生产工艺路径，由多个工序组成。
    ...

关联任务：S2-1 T2-1-1
作者：AI（芯智云匠）
日期：2026-04-12
"""

import re
import sys
import argparse
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)


# ── 数据模型 ──────────────────────────────────────────────────

@dataclass
class ColumnDef:
    name: str
    data_type: str
    nullable: bool = True
    default: Optional[str] = None
    comment: Optional[str] = None
    is_primary: bool = False


@dataclass
class IndexDef:
    name: str
    columns: list[str]
    unique: bool = False
    index_type: str = "BTREE"


@dataclass
class TableDef:
    schema: str
    name: str
    comment: Optional[str] = None
    columns: list[ColumnDef] = field(default_factory=list)
    indexes: list[IndexDef] = field(default_factory=list)
    primary_key: list[str] = field(default_factory=list)
    module: str = ""
    source_file: str = ""


# ── DDL 解析器 ────────────────────────────────────────────────

class PostgresDDLParser:
    """
    解析 PostgreSQL DDL 脚本，提取表结构信息。

    支持的 DDL 语法：
    - CREATE TABLE [schema.]table_name (...)
    - COMMENT ON TABLE ... IS '...'
    - COMMENT ON COLUMN ... IS '...'
    - CREATE [UNIQUE] INDEX ... ON ...
    - ALTER TABLE ... ADD CONSTRAINT ... PRIMARY KEY (...)
    """

    # 匹配 CREATE TABLE（含可选 IF NOT EXISTS、schema 前缀）
    _RE_CREATE_TABLE = re.compile(
        r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?"
        r"(?:([\"'\w]+)\.)?"        # schema（可选）
        r"([\"'\w]+)\s*\(",         # 表名
        re.IGNORECASE
    )

    # 匹配 COMMENT ON TABLE
    _RE_TABLE_COMMENT = re.compile(
        r"COMMENT\s+ON\s+TABLE\s+"
        r"(?:[\"'\w]+\.)?([\"'\w]+)"  # 表名
        r"\s+IS\s+'((?:[^']|'')*)'",  # 注释内容（允许内嵌 ''）
        re.IGNORECASE | re.DOTALL
    )

    # 匹配 COMMENT ON COLUMN
    _RE_COLUMN_COMMENT = re.compile(
        r"COMMENT\s+ON\s+COLUMN\s+"
        r"(?:[\"'\w]+\.)?"          # schema（可选）
        r"([\"'\w]+)"               # 表名
        r"\.([\"'\w]+)"             # 列名
        r"\s+IS\s+'((?:[^']|'')*)'",
        re.IGNORECASE | re.DOTALL
    )

    # 匹配 CREATE [UNIQUE] INDEX
    _RE_CREATE_INDEX = re.compile(
        r"CREATE\s+(UNIQUE\s+)?INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?"
        r"([\"'\w]+)\s+ON\s+"       # 索引名
        r"(?:[\"'\w]+\.)?([\"'\w]+)"  # 表名
        r"\s+(?:USING\s+(\w+)\s+)?"  # 索引类型（可选）
        r"\(([^)]+)\)",              # 列列表
        re.IGNORECASE
    )

    # 匹配 NOT NULL
    _RE_NOT_NULL = re.compile(r"\bNOT\s+NULL\b", re.IGNORECASE)

    # 匹配 DEFAULT 值
    _RE_DEFAULT = re.compile(r"\bDEFAULT\s+(\S+(?:\s+\S+)?)", re.IGNORECASE)

    # 匹配 PRIMARY KEY 内联声明
    _RE_INLINE_PK = re.compile(r"\bPRIMARY\s+KEY\b", re.IGNORECASE)

    def parse_file(self, sql_path: Path, module: str = "") -> list[TableDef]:
        """解析单个 SQL 文件，返回所有表定义列表"""
        content = sql_path.read_text(encoding="utf-8", errors="replace")
        # 统一换行符，移除行注释（-- ...）但保留块内容
        content = self._strip_line_comments(content)
        tables = self._parse_create_tables(content, module, str(sql_path.name))
        self._apply_comments(content, tables)
        self._parse_indexes(content, tables)
        log.info("解析完成：%s → %d 张表", sql_path.name, len(tables))
        return tables

    def _strip_line_comments(self, sql: str) -> str:
        """移除 SQL 行注释（-- ...），保留字符串内的 '--'"""
        lines = []
        for line in sql.splitlines():
            # 简单处理：找第一个不在单引号内的 '--'
            in_quote = False
            result = []
            i = 0
            while i < len(line):
                c = line[i]
                if c == "'" and (i == 0 or line[i-1] != "\\"):
                    in_quote = not in_quote
                    result.append(c)
                elif not in_quote and line[i:i+2] == "--":
                    break   # 注释开始，截断本行
                else:
                    result.append(c)
                i += 1
            lines.append("".join(result))
        return "\n".join(lines)

    def _parse_create_tables(
        self, sql: str, module: str, source_file: str
    ) -> list[TableDef]:
        """提取所有 CREATE TABLE 块"""
        tables: list[TableDef] = []
        pos = 0
        while True:
            m = self._RE_CREATE_TABLE.search(sql, pos)
            if not m:
                break
            schema = self._strip_quotes(m.group(1) or "public")
            table_name = self._strip_quotes(m.group(2))
            body_start = m.end()
            body, body_end = self._extract_paren_block(sql, body_start - 1)
            table = TableDef(
                schema=schema,
                name=table_name,
                module=module,
                source_file=source_file
            )
            self._parse_columns(body, table)
            tables.append(table)
            pos = body_end
        return tables

    def _extract_paren_block(self, sql: str, start: int) -> tuple[str, int]:
        """提取匹配括号之间的内容（起始位置为第一个 '(' ）"""
        depth = 0
        result = []
        i = start
        while i < len(sql):
            c = sql[i]
            if c == "(":
                depth += 1
                if depth > 1:
                    result.append(c)
            elif c == ")":
                depth -= 1
                if depth == 0:
                    return "".join(result), i + 1
                else:
                    result.append(c)
            else:
                if depth > 0:
                    result.append(c)
            i += 1
        return "".join(result), i

    def _parse_columns(self, body: str, table: TableDef) -> None:
        """解析表体中的列定义（跳过 CONSTRAINT / CHECK 等）"""
        # 按逗号分割，但要忽略嵌套括号内的逗号
        parts = self._split_top_level_commas(body)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            upper = part.upper()
            # 跳过约束定义行
            if upper.startswith(("CONSTRAINT", "CHECK", "FOREIGN KEY",
                                   "UNIQUE (", "UNIQUE(", "EXCLUDE")):
                continue
            # PRIMARY KEY (...) 提取主键列
            if upper.startswith("PRIMARY KEY"):
                pk_match = re.search(r"\(([^)]+)\)", part)
                if pk_match:
                    table.primary_key = [
                        self._strip_quotes(c.strip())
                        for c in pk_match.group(1).split(",")
                    ]
                continue
            # 尝试解析列定义
            col = self._parse_column_def(part)
            if col:
                if self._RE_INLINE_PK.search(part):
                    table.primary_key = [col.name]
                    col.is_primary = True
                table.columns.append(col)

    def _parse_column_def(self, line: str) -> Optional[ColumnDef]:
        """解析单行列定义，返回 ColumnDef 或 None"""
        # 第一个 token 为列名，第二个为类型（可能含空格，如 DOUBLE PRECISION）
        tokens = line.split()
        if len(tokens) < 2:
            return None
        col_name = self._strip_quotes(tokens[0])
        # 跳过以大写关键字开头的行（误判保护）
        if tokens[0].upper() in ("PRIMARY", "UNIQUE", "CHECK",
                                  "CONSTRAINT", "FOREIGN", "INDEX"):
            return None

        # 提取数据类型（可能有括号，如 VARCHAR(50)）
        data_type = self._extract_data_type(line, tokens)

        nullable = not bool(self._RE_NOT_NULL.search(line))
        default_match = self._RE_DEFAULT.search(line)
        default = default_match.group(1) if default_match else None

        return ColumnDef(
            name=col_name,
            data_type=data_type,
            nullable=nullable,
            default=default
        )

    def _extract_data_type(self, line: str, tokens: list[str]) -> str:
        """从列定义行提取数据类型（含长度参数）"""
        # 跳过列名，取后续直到遇到约束关键字
        stop_keywords = {"NOT", "NULL", "DEFAULT", "PRIMARY", "UNIQUE",
                         "REFERENCES", "CHECK", "CONSTRAINT", "GENERATED"}
        parts = []
        for tok in tokens[1:]:
            if tok.upper() in stop_keywords:
                break
            parts.append(tok)
        return " ".join(parts).rstrip(",").strip()

    def _split_top_level_commas(self, text: str) -> list[str]:
        """按顶层逗号分割（忽略括号内的逗号）"""
        result = []
        depth = 0
        current = []
        for c in text:
            if c == "(":
                depth += 1
                current.append(c)
            elif c == ")":
                depth -= 1
                current.append(c)
            elif c == "," and depth == 0:
                result.append("".join(current))
                current = []
            else:
                current.append(c)
        if current:
            result.append("".join(current))
        return result

    def _apply_comments(self, sql: str, tables: list[TableDef]) -> None:
        """将 COMMENT ON TABLE/COLUMN 注释应用到对应的 TableDef"""
        table_map = {t.name.lower(): t for t in tables}

        # 表注释
        for m in self._RE_TABLE_COMMENT.finditer(sql):
            tname = self._strip_quotes(m.group(1)).lower()
            if tname in table_map:
                table_map[tname].comment = m.group(2).replace("''", "'")

        # 列注释
        for m in self._RE_COLUMN_COMMENT.finditer(sql):
            tname = self._strip_quotes(m.group(1)).lower()
            cname = self._strip_quotes(m.group(2)).lower()
            comment = m.group(3).replace("''", "'")
            if tname in table_map:
                for col in table_map[tname].columns:
                    if col.name.lower() == cname:
                        col.comment = comment
                        break

    def _parse_indexes(self, sql: str, tables: list[TableDef]) -> None:
        """将 CREATE INDEX 信息添加到对应表"""
        table_map = {t.name.lower(): t for t in tables}
        for m in self._RE_CREATE_INDEX.finditer(sql):
            is_unique = bool(m.group(1))
            idx_name = self._strip_quotes(m.group(2))
            tname = self._strip_quotes(m.group(3)).lower()
            idx_type = m.group(4) or "BTREE"
            cols = [c.strip().rstrip(")").strip() for c in m.group(5).split(",")]
            if tname in table_map:
                table_map[tname].indexes.append(IndexDef(
                    name=idx_name,
                    columns=cols,
                    unique=is_unique,
                    index_type=idx_type.upper()
                ))

    @staticmethod
    def _strip_quotes(s: str) -> str:
        """移除 SQL 标识符引号"""
        if s:
            return s.strip('"\'` ')
        return s or ""


# ── Markdown 渲染器 ───────────────────────────────────────────

class MarkdownRenderer:
    """
    将 TableDef 渲染为知识库 chunk 所需的 Markdown 格式。

    每个表卡片包含：
    1. 表头（表名 + 中文说明）
    2. 元数据（模块/Schema/Source）
    3. 字段明细表
    4. 索引信息
    5. 主键说明
    """

    def render(self, table: TableDef) -> str:
        lines = []

        # ── 表头 ─────────────────────────────────────────────
        display_comment = table.comment or "（暂无说明，待补充）"
        lines.append(f"## 表：{table.name}（{display_comment}）")
        lines.append("")
        lines.append(
            f"**模块**：{table.module or '待分类'}  |  "
            f"**Schema**：{table.schema}  |  "
            f"**来源文件**：{table.source_file}"
        )
        lines.append("")

        # ── 主键信息 ─────────────────────────────────────────
        if table.primary_key:
            lines.append(f"**主键**：`{'`, `'.join(table.primary_key)}`")
            lines.append("")

        # ── 字段明细 ─────────────────────────────────────────
        lines.append("### 字段明细")
        lines.append("")
        lines.append("| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |")
        lines.append("|--------|--------|------|------|------|")

        for col in table.columns:
            nullable_str = "是" if col.nullable else "否"
            default_str = col.default or ""
            comment_str = col.comment or ""
            # 主键标记
            if col.name in table.primary_key or col.is_primary:
                comment_str = f"🔑 {comment_str}" if comment_str else "🔑 主键"
            lines.append(
                f"| `{col.name}` | `{col.data_type}` | {nullable_str} "
                f"| `{default_str}` | {comment_str} |"
            )

        lines.append("")

        # ── 索引信息 ─────────────────────────────────────────
        if table.indexes:
            lines.append("### 索引")
            lines.append("")
            lines.append("| 索引名 | 类型 | 列 |")
            lines.append("|--------|------|-----|")
            for idx in table.indexes:
                idx_type = "唯一索引" if idx.unique else "普通索引"
                cols_str = "`, `".join(idx.columns)
                lines.append(
                    f"| `{idx.name}` | {idx_type} ({idx.index_type}) | `{cols_str}` |"
                )
            lines.append("")

        # ── 尾注 ─────────────────────────────────────────────
        lines.append(
            f"> *chunk_type: table_card | "
            f"chunk_id: {table.module}_{table.name}_table_card*"
        )
        lines.append("")

        return "\n".join(lines)


# ── 主程序 ────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description="PostgreSQL DDL → Markdown 表卡片解析器"
    )
    p.add_argument("--input",  required=True, help="DDL 文件或目录路径")
    p.add_argument("--output", required=True, help="输出 Markdown 文件目录")
    p.add_argument("--module", default="",    help="MES 模块名称（如：工艺管理）")
    return p.parse_args()


def main():
    args = parse_args()

    input_path  = Path(args.input)
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)

    # 收集 SQL 文件
    if input_path.is_file():
        sql_files = [input_path]
    elif input_path.is_dir():
        sql_files = sorted(input_path.glob("*.sql"))
    else:
        log.error("输入路径不存在：%s", input_path)
        sys.exit(1)

    if not sql_files:
        log.warning("未找到 .sql 文件，目录：%s", input_path)
        sys.exit(0)

    parser   = PostgresDDLParser()
    renderer = MarkdownRenderer()

    total_tables = 0
    for sql_file in sql_files:
        log.info("正在解析：%s", sql_file.name)
        try:
            tables = parser.parse_file(sql_file, module=args.module)
        except Exception as e:
            log.error("解析失败：%s → %s", sql_file.name, e)
            continue

        for table in tables:
            md_content = renderer.render(table)
            out_file = output_path / f"{table.name}.md"
            out_file.write_text(md_content, encoding="utf-8")
            log.info("  ✅ 输出：%s (%d 字段, %d 索引)",
                     out_file.name, len(table.columns), len(table.indexes))
            total_tables += 1

    log.info("解析完成，共输出 %d 张表卡片 → %s", total_tables, output_path)

    # 输出摘要 index 文件
    _write_index(output_path, args.module)


def _write_index(output_dir: Path, module: str) -> None:
    """生成该模块的表卡片索引文件"""
    md_files = sorted(output_dir.glob("*.md"))
    if not md_files:
        return
    lines = [
        f"# {module} 模块 · 表卡片索引",
        f"",
        f"**生成时间**：由 ddl_parser.py 自动生成",
        f"**文件数**：{len(md_files)}",
        f"",
        f"| 文件 | 表名 |",
        f"|------|------|",
    ]
    for f in md_files:
        if f.name == "INDEX.md":
            continue
        lines.append(f"| [{f.name}](./{f.name}) | `{f.stem}` |")
    (output_dir / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")
    log.info("索引文件已生成：%s/INDEX.md", output_dir)


if __name__ == "__main__":
    main()
