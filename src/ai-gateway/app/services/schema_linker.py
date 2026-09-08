"""
Schema Linking 服务（MES 取数生成前置，B2.2）
文档编号：AI-MES-GW-2026-004
关联需求单：REQ-MES-AI-20260730-002
作者：AI（芯智云匠）
日期：2026-08-01

背景（M1 基线失败归因）：首轮结果正确率 2.4%，主因是表选错/列选错——
整表卡片上下文信息密度低，模型在多个相似表（计划表↔实绩表、切割表↔板坯表）之间选错。

本服务在生成前做**确定性候选表/列抽取**：
- 候选表来源双路：① RAG 检索到的表卡片（[表] 标记 / source_file）；② 问题中与字典表名逐字相同的 token；
- 数据源：docs/data_dictionary_full.csv（all_tab_columns 导出，含真实 DATA_TYPE）；
- 输出：相关表的**最小列子集**（列名+真实类型），注入上下文替代模型"从卡片散文里猜列"。

列裁剪口径（F6.3）：每表 ≤60 列，字典物理顺序（≈业务主列在前）；
问题中逐字出现的列名与代码类后缀列（_CD/_TY/_GRD 等）优先保留。
类型信息是关键弹药：VARCHAR2(14) 直接可见，预防"字符串时间列当 DATE 用"（M1 失败类型 2）。

开关：SCHEMA_LINKING_ENABLED（默认 false）。
G 段约定：schema linking 改变首轮正常路径行为，须 F5 档位 B 复测确认无退化后才可默认开启。
"""

import csv
import functools
import logging
import os
import re

log = logging.getLogger(__name__)

_TOKEN_RE = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")
_TABLE_MARK_RE = re.compile(r"\[表\]\s*([A-Za-z][A-Za-z0-9_]*)")

MAX_TABLES = 4
MAX_COLS_PER_TABLE = 60
_CODE_SUFFIXES = ("_CD", "_TY", "_GRD", "_YN", "_FG", "_TP", "_ST", "_FL", "_DTM", "_DT", "_TM", "_NO")


class SchemaLinker:
    """列级数据字典直查：table → [(列名, 类型, 长度, 注释)]（字典物理顺序）"""

    def __init__(self, csv_path: str):
        self._tables: dict[str, list[tuple[str, str, str, str]]] = {}
        self._load(csv_path)

    def _load(self, csv_path: str) -> None:
        with open(csv_path, encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)  # 表头：SCHEMA,TABLE_NAME,COLUMN_NAME,DATA_TYPE,LEN,COL_COMMENT,SOURCE
            for row in reader:
                if len(row) < 6:
                    continue
                schema, table, col, dtype, length, comment = (c.strip() for c in row[:6])
                if schema != "MESAPUSER" or not table or not col:
                    continue
                type_str = f"{dtype}({length})" if dtype in ("VARCHAR2", "CHAR", "NCHAR", "NVARCHAR2") and length else dtype
                self._tables.setdefault(table.upper(), []).append((col.upper(), type_str, length, comment))
        log.info("[SchemaLinking] 数据字典加载完成 tables=%d path=%s", len(self._tables), csv_path)

    def _candidate_tables(self, question: str, docs) -> list[str]:
        """双路候选表：RAG 文档中的表标记 + 问题/文档中与字典表名逐字相同的 token（按出现顺序去重）"""
        found: list[str] = []
        seen: set = set()

        def add(name: str):
            t = name.upper()
            if t in self._tables and t not in seen:
                seen.add(t)
                found.append(t)

        for d in docs:
            for m in _TABLE_MARK_RE.findall(d.content or ""):
                add(m)
            src = (d.metadata.get("source_file") or d.metadata.get("source") or "")
            base = os.path.basename(src)
            if base.lower().endswith(".md"):
                add(base[:-3])
        for token in _TOKEN_RE.findall(question or ""):
            add(token)
        # 文档全文 token 兜底（卡片散文里的表名）
        for d in docs:
            for token in _TOKEN_RE.findall(d.content or ""):
                add(token)
        return found[:MAX_TABLES]

    def link(self, question: str, docs, max_cols: int = MAX_COLS_PER_TABLE) -> str:
        """
        生成最小列子集上下文文本；无候选表时返回空串（不注入）。
        列裁剪：问题中逐字出现的列与代码/时间/编号类后缀列优先，其余按字典顺序补足 max_cols。
        """
        tables = self._candidate_tables(question, docs)
        if not tables:
            return ""
        question_tokens = {t.upper() for t in _TOKEN_RE.findall(question or "")}
        sections = []
        for table in tables:
            cols = self._tables[table]
            prioritized = [c for c in cols
                           if c[0] in question_tokens or c[0].endswith(_CODE_SUFFIXES)]
            rest = [c for c in cols if c not in prioritized]
            selected = (prioritized + rest)[:max_cols]
            def _fmt(c):
                name, type_str, _len, comment = c
                comment = (comment or "").strip()
                return f"{name} {type_str}" + (f"（{comment}）" if comment and comment != "空" else "")
            col_str = ", ".join(_fmt(c) for c in selected)
            suffix = f"（共 {len(cols)} 列，仅列前 {len(selected)} 列）" if len(cols) > max_cols else ""
            sections.append(f"- {table}{suffix}：{col_str}")
        return ("[Schema Linking] 相关表的真实结构（生成 SQL 只能使用下列表与列，"
                "注意列的真实类型与括号内业务含义）：\n" + "\n".join(sections))


def _default_dict_path() -> str:
    services_dir = os.path.dirname(os.path.abspath(__file__))
    gateway_root = os.path.dirname(os.path.dirname(services_dir))
    project_root = os.path.dirname(os.path.dirname(gateway_root))
    return os.path.join(project_root, "docs", "data_dictionary_full.csv")


@functools.lru_cache(maxsize=1)
def get_schema_linker() -> "SchemaLinker | None":
    """
    单例获取。开关默认关闭（SCHEMA_LINKING_ENABLED=true 才启用，G 段约定）；
    字典文件缺失或加载失败返回 None（降级不阻断主链路）。
    """
    if os.environ.get("SCHEMA_LINKING_ENABLED", "").strip().lower() not in ("1", "true", "yes"):
        return None
    path = os.environ.get("DATA_DICT_CSV", "").strip() or _default_dict_path()
    if not os.path.exists(path):
        log.warning("[SchemaLinking] 数据字典不存在，schema linking 停用 path=%s", path)
        return None
    try:
        return SchemaLinker(path)
    except Exception as e:
        log.error("[SchemaLinking] 加载失败，schema linking 停用 path=%s err=%s", path, e, exc_info=True)
        return None
