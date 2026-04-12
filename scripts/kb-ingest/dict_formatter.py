#!/usr/bin/env python3
"""
数据字典格式化器：Excel/Word → Markdown

将甲方提供的数据字典文件（Excel .xlsx 或 Word .docx）转换为
标准化的 Markdown 格式，供知识库入库使用。

用法：
    # 处理 Excel 格式
    python dict_formatter.py --input data-dict/02-工艺管理.xlsx \
                              --output data-dict/02-工艺管理.md \
                              --module 工艺管理

    # 处理 Word 格式
    python dict_formatter.py --input data-dict/02-工艺管理.docx \
                              --output data-dict/02-工艺管理.md \
                              --module 工艺管理

Excel 表头要求（必须包含以下列名之一）：
    表名 / 字段名 / 字段类型 / 中文名称 / 枚举值 / 说明 / 备注

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
class FieldEntry:
    table_name: str
    field_name: str
    field_type: str = ""
    chinese_name: str = ""
    enum_values: str = ""
    description: str = ""
    is_required: bool = False
    remarks: str = ""


@dataclass
class TableDict:
    table_name: str
    table_comment: str = ""
    module: str = ""
    fields: list[FieldEntry] = field(default_factory=list)


# ── Excel 解析器 ──────────────────────────────────────────────

class ExcelDictParser:
    """
    解析数据字典 Excel 文件。

    假设 Excel 结构为：
    - Sheet 1（或以模块名命名）：字段清单
    - 必要列：表名、字段名、字段类型、中文名称
    - 可选列：枚举值、说明、是否必填、备注
    """

    # 列名别名映射（容忍甲方表头不统一）
    _COLUMN_ALIASES = {
        "table_name":    ["表名", "table_name", "TABLE_NAME", "tablename", "表格名称"],
        "field_name":    ["字段名", "field_name", "FIELD_NAME", "fieldname", "列名", "column_name"],
        "field_type":    ["字段类型", "field_type", "TYPE", "数据类型", "类型"],
        "chinese_name":  ["中文名称", "中文名", "chinese_name", "名称", "字段说明"],
        "enum_values":   ["枚举值", "取值范围", "可选值", "enum_values", "值域"],
        "description":   ["说明", "备注", "description", "REMARKS", "remark", "描述"],
        "is_required":   ["是否必填", "必填", "NOT NULL", "required", "非空"],
    }

    def parse(self, file_path: Path, module: str = "") -> list[TableDict]:
        try:
            from openpyxl import load_workbook
        except ImportError:
            log.error("缺少 openpyxl 依赖，请运行：pip install openpyxl")
            sys.exit(1)

        wb = load_workbook(file_path, read_only=True, data_only=True)
        all_tables: dict[str, TableDict] = {}

        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            rows = list(ws.iter_rows(values_only=True))
            if len(rows) < 2:
                continue

            # 识别表头行
            header_row = self._find_header_row(rows)
            if header_row is None:
                log.warning("Sheet '%s' 未找到有效表头，跳过", sheet_name)
                continue

            col_map = self._map_columns(rows[header_row])
            if "table_name" not in col_map or "field_name" not in col_map:
                log.warning("Sheet '%s' 缺少 [表名/字段名] 列，跳过", sheet_name)
                continue

            # 解析数据行
            for row in rows[header_row + 1:]:
                if all(v is None for v in row):
                    continue
                entry = self._parse_row(row, col_map, module)
                if not entry:
                    continue

                tname = entry.table_name.strip()
                if tname not in all_tables:
                    all_tables[tname] = TableDict(
                        table_name=tname,
                        module=module
                    )
                all_tables[tname].fields.append(entry)

        wb.close()
        result = list(all_tables.values())
        log.info("解析完成：%s → %d 张表的字段信息", file_path.name, len(result))
        return result

    def _find_header_row(self, rows: list) -> Optional[int]:
        """找到包含 [表名 / 字段名] 关键词的行索引"""
        for i, row in enumerate(rows[:10]):   # 只检查前10行
            row_str = " ".join(str(v) for v in row if v is not None).lower()
            if any(k in row_str for k in ["表名", "table", "字段名", "field"]):
                return i
        return None

    def _map_columns(self, header: tuple) -> dict[str, int]:
        """将表头列映射到标准字段名"""
        col_map = {}
        for idx, cell in enumerate(header):
            if cell is None:
                continue
            cell_str = str(cell).strip()
            for std_name, aliases in self._COLUMN_ALIASES.items():
                if cell_str in aliases:
                    col_map[std_name] = idx
                    break
        return col_map

    def _parse_row(self, row: tuple, col_map: dict, module: str) -> Optional[FieldEntry]:
        def get(key: str) -> str:
            idx = col_map.get(key)
            if idx is None or idx >= len(row):
                return ""
            val = row[idx]
            return str(val).strip() if val is not None else ""

        table_name = get("table_name")
        field_name = get("field_name")
        if not table_name or not field_name:
            return None

        # 跳过合并单元格造成的空行（table_name 重复但 field_name 为空）
        if field_name in ("字段名", "field_name", "FIELD_NAME"):
            return None

        required_raw = get("is_required").lower()
        is_required = required_raw in ("是", "y", "yes", "true", "1", "not null", "✓", "√")

        return FieldEntry(
            table_name=table_name,
            field_name=field_name,
            field_type=get("field_type"),
            chinese_name=get("chinese_name"),
            enum_values=get("enum_values"),
            description=get("description"),
            is_required=is_required,
            remarks=""
        )


# ── Markdown 渲染器 ───────────────────────────────────────────

class DictMarkdownRenderer:
    """将 TableDict 列表渲染为 Markdown 数据字典文档"""

    def render_module(self, tables: list[TableDict], module: str) -> str:
        lines = [
            f"# {module} 模块 · 数据字典",
            "",
            f"**模块**：{module}",
            f"**包含表数**：{len(tables)}",
            f"**chunk_type**：data_dict",
            "",
            "---",
            "",
        ]

        for table in tables:
            lines.append(self._render_table(table))
            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    def _render_table(self, table: TableDict) -> str:
        lines = [
            f"## {table.table_name}",
            "",
        ]
        if table.table_comment:
            lines.append(f"**说明**：{table.table_comment}")
            lines.append("")

        if not table.fields:
            lines.append("*（暂无字段信息）*")
            return "\n".join(lines)

        # 判断是否有枚举值列
        has_enum = any(f.enum_values for f in table.fields)

        if has_enum:
            lines.append("| 字段名 | 中文名称 | 类型 | 必填 | 枚举值 / 说明 |")
            lines.append("|--------|--------|------|------|------------|")
            for f in table.fields:
                required = "✓" if f.is_required else ""
                desc = f.enum_values or f.description
                lines.append(
                    f"| `{f.field_name}` | {f.chinese_name} "
                    f"| `{f.field_type}` | {required} | {desc} |"
                )
        else:
            lines.append("| 字段名 | 中文名称 | 类型 | 必填 | 说明 |")
            lines.append("|--------|--------|------|------|------|")
            for f in table.fields:
                required = "✓" if f.is_required else ""
                lines.append(
                    f"| `{f.field_name}` | {f.chinese_name} "
                    f"| `{f.field_type}` | {required} | {f.description} |"
                )

        lines.append("")
        lines.append(
            f"> *chunk_id: {table.module}_{table.table_name}_data_dict*"
        )
        return "\n".join(lines)


# ── Word 解析器（简化版）─────────────────────────────────────

class WordDictParser:
    """
    解析 Word 数据字典。
    Word 文件中的表格按 [表名行 + 字段行] 结构解析。
    """

    def parse(self, file_path: Path, module: str = "") -> list[TableDict]:
        try:
            from docx import Document
        except ImportError:
            log.error("缺少 python-docx 依赖，请运行：pip install python-docx")
            sys.exit(1)

        doc = Document(file_path)
        all_tables: list[TableDict] = []

        for tbl in doc.tables:
            rows = [[cell.text.strip() for cell in row.cells] for row in tbl.rows]
            if len(rows) < 2:
                continue
            table_dict = self._parse_word_table(rows, module)
            if table_dict:
                all_tables.append(table_dict)

        log.info("解析完成：%s → %d 张表", file_path.name, len(all_tables))
        return all_tables

    def _parse_word_table(self, rows: list[list[str]], module: str) -> Optional[TableDict]:
        """尝试将 Word 表格解析为 TableDict"""
        if not rows:
            return None

        # 第一行可能是表名标题行
        first_row = rows[0]
        table_name = ""
        if len(first_row) == 1:
            table_name = first_row[0]
            header_row_idx = 1
        else:
            # 查找表名列
            header_row_idx = 0
            for i, cell in enumerate(first_row):
                if "表名" in cell or "table" in cell.lower():
                    header_row_idx = 0
                    break

        if not table_name and len(rows) > 1:
            # 从第二行尝试找表名
            for row in rows[:3]:
                for cell in row:
                    if cell and not any(
                        h in cell.lower()
                        for h in ["字段", "field", "类型", "type"]
                    ):
                        table_name = cell
                        break
                if table_name:
                    break

        if not table_name:
            return None

        table = TableDict(table_name=table_name, module=module)

        # 简单解析：每行视为一个字段
        for row in rows[header_row_idx + 1:]:
            if len(row) >= 2 and row[0] and row[0] != table_name:
                field_entry = FieldEntry(
                    table_name=table_name,
                    field_name=row[0],
                    chinese_name=row[1] if len(row) > 1 else "",
                    field_type=row[2] if len(row) > 2 else "",
                    description=row[-1] if len(row) > 3 else "",
                )
                table.fields.append(field_entry)

        return table if table.fields else None


# ── 主程序 ────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description="数据字典格式化器（Excel/Word → Markdown）")
    p.add_argument("--input",  required=True, help="数据字典文件路径（.xlsx / .docx）")
    p.add_argument("--output", required=True, help="输出 Markdown 文件路径")
    p.add_argument("--module", default="",    help="MES 模块名称")
    return p.parse_args()


def main():
    args = parse_args()
    input_path  = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    suffix = input_path.suffix.lower()
    if suffix == ".xlsx":
        parser = ExcelDictParser()
    elif suffix in (".docx", ".doc"):
        parser = WordDictParser()
    else:
        log.error("不支持的文件格式：%s（仅支持 .xlsx / .docx）", suffix)
        sys.exit(1)

    tables = parser.parse(input_path, module=args.module)
    if not tables:
        log.warning("未解析到任何表信息，请检查文件格式")
        sys.exit(0)

    renderer = DictMarkdownRenderer()
    md_content = renderer.render_module(tables, args.module)
    output_path.write_text(md_content, encoding="utf-8")
    log.info("输出完成：%s（%d 张表）", output_path, len(tables))


if __name__ == "__main__":
    main()
