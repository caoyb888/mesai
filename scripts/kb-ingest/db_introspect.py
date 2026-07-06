#!/usr/bin/env python3
"""
数据库自省器（DBMS 适配层）→ 结构化元数据 JSON

用途：只读直连真实 MES 库（Oracle），自动抽取 schema / 表 / 字段 / 约束 / 索引 / 注释，
     以及【存储过程 / 函数 / 包 / 触发器】源码与签名，产出结构化 JSON，
     作为知识库入库与 AI 理解训练的一手素材。取代 ITSM 验证阶段手工整理 SQL 文件的方式。

设计要点：
  1. DBMS 适配层：MetadataProvider 抽象接口 + OracleMetadataProvider 实现，
     后续可扩展 PostgreSQL / MySQL；具体 SQL 仅存在于各 Provider 内。
  2. 可测试：元数据「组装逻辑」（Introspector）与「SQL 取数」（Provider）解耦，
     单测用 FakeMetadataProvider 注入假数据，无需真实 Oracle。
  3. 低配友好：oracledb thin 模式（免装 Oracle 客户端），懒加载；
     支持 --self-test 用假数据产出样例 JSON，无库也能验证输出结构。
  4. 安全红线：连接凭据仅从环境变量注入（禁硬编码，Gitleaks）；仅发 SELECT（只读）。

用法：
    # 无库自测（低配机即可跑，产出样例 JSON 结构）
    python db_introspect.py --self-test --out sample_metadata.json

    # 真实库自省（凭据来自 .env / 环境变量，禁止写在命令行）
    export MES_DB_USER=... MES_DB_PASSWORD=... MES_DB_DSN=host:1521/orclpdb
    python db_introspect.py --owner MESAPUSER --out metadata_mesapuser.json

关联任务：S2.9-2 数据库自省与资产盘点（真实 MES 接入版计划 AI-MES-PLAN-ADJ-2026-001）
作者：AI（芯智云匠）
日期：2026-07-06
"""

import os
import sys
import json
import argparse
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


# ── 数据模型 ──────────────────────────────────────────────────
# 说明：所有模型均为 DBMS 无关的中间表示，Provider 负责把各库的原始行
#       转成下列 dict 结构，Introspector 再组装为 dataclass。

@dataclass
class ColumnMeta:
    """字段元数据"""
    name: str
    data_type: str
    length: Optional[int] = None
    nullable: bool = True
    data_default: Optional[str] = None
    comment: Optional[str] = None       # 原始注释（可能为空/乱码，交 encoding_normalizer 处理）
    position: int = 0
    is_primary: bool = False


@dataclass
class ConstraintMeta:
    """约束元数据（P=主键 / U=唯一 / R=外键）"""
    name: str
    ctype: str
    columns: list[str] = field(default_factory=list)
    ref_owner: Optional[str] = None
    ref_table: Optional[str] = None


@dataclass
class IndexMeta:
    """索引元数据"""
    name: str
    unique: bool = False
    columns: list[str] = field(default_factory=list)


@dataclass
class TableMeta:
    """表元数据"""
    owner: str
    name: str
    comment: Optional[str] = None
    num_rows: Optional[int] = None
    columns: list[ColumnMeta] = field(default_factory=list)
    constraints: list[ConstraintMeta] = field(default_factory=list)
    indexes: list[IndexMeta] = field(default_factory=list)


@dataclass
class ArgumentMeta:
    """子程序参数（存储过程 / 函数）"""
    name: Optional[str]
    data_type: Optional[str]
    in_out: Optional[str] = None        # IN / OUT / IN/OUT
    position: int = 0


@dataclass
class ProgramUnitMeta:
    """PL/SQL 程序单元：存储过程 / 函数 / 包 / 触发器 / 类型"""
    owner: str
    name: str
    object_type: str                    # PROCEDURE / FUNCTION / PACKAGE / PACKAGE BODY / TRIGGER / TYPE ...
    status: Optional[str] = None        # VALID / INVALID
    source: Optional[str] = None        # PL/SQL 源码（按行组装）
    arguments: list[ArgumentMeta] = field(default_factory=list)


@dataclass
class SchemaMetadata:
    """一个 schema（owner）的完整自省结果"""
    owner: str
    dbms: str
    nls_charset: Optional[str] = None
    extracted_at: Optional[str] = None
    tables: list[TableMeta] = field(default_factory=list)
    program_units: list[ProgramUnitMeta] = field(default_factory=list)

    def summary(self) -> dict:
        """资产盘点摘要（供《MES 资产盘点报告》使用）"""
        unit_by_type: dict[str, int] = {}
        for u in self.program_units:
            unit_by_type[u.object_type] = unit_by_type.get(u.object_type, 0) + 1
        total_cols = sum(len(t.columns) for t in self.tables)
        empty_comment = sum(
            1 for t in self.tables for c in t.columns if not (c.comment or "").strip()
        )
        return {
            "owner": self.owner,
            "dbms": self.dbms,
            "nls_charset": self.nls_charset,
            "table_count": len(self.tables),
            "column_count": total_cols,
            "empty_comment_columns": empty_comment,
            "program_unit_count": len(self.program_units),
            "program_units_by_type": unit_by_type,
        }

    def to_dict(self) -> dict:
        return asdict(self)


# ── DBMS 适配层：Provider 抽象接口 ────────────────────────────
# 每个方法返回「已规整为 dict 的原始行列表」，SQL/连接细节由具体实现封装。
# Introspector 只依赖本接口，从而可用 FakeMetadataProvider 完成单元测试。

class MetadataProvider(ABC):
    """DBMS 元数据取数接口（DBMS 无关）"""

    @abstractmethod
    def charset(self) -> Optional[str]:
        """数据库字符集（如 Oracle NLS_CHARACTERSET）"""

    @abstractmethod
    def tables(self, owner: str) -> list[dict]:
        """键：name, comment, num_rows"""

    @abstractmethod
    def columns(self, owner: str) -> list[dict]:
        """键：table, name, data_type, length, nullable, data_default, position"""

    @abstractmethod
    def column_comments(self, owner: str) -> list[dict]:
        """键：table, column, comment"""

    @abstractmethod
    def constraints(self, owner: str) -> list[dict]:
        """键：table, name, ctype, column, position, ref_owner, ref_table"""

    @abstractmethod
    def indexes(self, owner: str) -> list[dict]:
        """键：table, name, unique, column, position"""

    @abstractmethod
    def program_units(self, owner: str) -> list[dict]:
        """键：name, object_type, status"""

    @abstractmethod
    def program_source(self, owner: str, names=None) -> list[dict]:
        """键：name, type, line, text；names 非空时仅取这些单元的源码"""

    @abstractmethod
    def program_arguments(self, owner: str) -> list[dict]:
        """键：object_name, argument_name, data_type, in_out, position"""

    def close(self) -> None:
        """释放连接（默认无操作）"""


# ── 组装逻辑：Introspector（DBMS 无关，核心可测试单元）────────

class Introspector:
    """把 Provider 的原始行组装为 SchemaMetadata"""

    def __init__(self, provider: MetadataProvider):
        self.provider = provider

    def build(self, owner: str, now: Optional[datetime] = None,
              include_source: bool = True, source_units=None) -> SchemaMetadata:
        """include_source=False 时只取程序单元清单（名/类型/状态），不拉 PL/SQL 源码。
        source_units 给定单元名集合时，仅拉这些单元的源码（P0 子集深析用），优先于 include_source。
        大库（如 MESAPUSER 达 193 万行源码）先做结构盘点应关源码，再按 P0 名单单独拉取。"""
        log.info("开始自省 owner=%s（含源码=%s，指定单元=%s）",
                 owner, include_source, len(source_units) if source_units else "全部/无")
        tables = self._build_tables(owner)
        units = self._build_program_units(owner, include_source=include_source,
                                         source_units=source_units)
        meta = SchemaMetadata(
            owner=owner,
            dbms=getattr(self.provider, "dbms", "unknown"),
            nls_charset=self.provider.charset(),
            extracted_at=(now or datetime.now()).isoformat(timespec="seconds"),
            tables=tables,
            program_units=units,
        )
        log.info(
            "自省完成：%d 张表 / %d 个字段 / %d 个程序单元",
            len(meta.tables),
            sum(len(t.columns) for t in meta.tables),
            len(meta.program_units),
        )
        return meta

    # -- 表 --------------------------------------------------
    def _build_tables(self, owner: str) -> list[TableMeta]:
        tmap: dict[str, TableMeta] = {}
        for r in self.provider.tables(owner):
            tmap[r["name"]] = TableMeta(
                owner=owner,
                name=r["name"],
                comment=r.get("comment"),
                num_rows=r.get("num_rows"),
            )

        # 字段（按 position 排序）
        cols = sorted(
            self.provider.columns(owner),
            key=lambda r: (r["table"], r.get("position", 0)),
        )
        colmap: dict[tuple[str, str], ColumnMeta] = {}
        for r in cols:
            t = tmap.get(r["table"])
            if t is None:
                continue  # 字段所属表不在表清单中（视图/临时表等），跳过
            c = ColumnMeta(
                name=r["name"],
                data_type=r["data_type"],
                length=r.get("length"),
                nullable=_as_bool(r.get("nullable"), default=True),
                data_default=r.get("data_default"),
                position=r.get("position", 0),
            )
            t.columns.append(c)
            colmap[(r["table"], r["name"])] = c

        # 字段注释回填
        for r in self.provider.column_comments(owner):
            c = colmap.get((r["table"], r["column"]))
            if c is not None:
                c.comment = r.get("comment")

        # 约束（按 name 聚合列；标记主键字段）
        cons: dict[tuple[str, str], ConstraintMeta] = {}
        for r in sorted(
            self.provider.constraints(owner),
            key=lambda r: (r["table"], r["name"], r.get("position", 0)),
        ):
            key = (r["table"], r["name"])
            cm = cons.get(key)
            if cm is None:
                cm = ConstraintMeta(
                    name=r["name"],
                    ctype=r["ctype"],
                    ref_owner=r.get("ref_owner"),
                    ref_table=r.get("ref_table"),
                )
                cons[key] = cm
                t = tmap.get(r["table"])
                if t is not None:
                    t.constraints.append(cm)
            if r.get("column"):
                cm.columns.append(r["column"])
                if cm.ctype == "P":
                    c = colmap.get((r["table"], r["column"]))
                    if c is not None:
                        c.is_primary = True

        # 索引（按 name 聚合列）
        idx: dict[tuple[str, str], IndexMeta] = {}
        for r in sorted(
            self.provider.indexes(owner),
            key=lambda r: (r["table"], r["name"], r.get("position", 0)),
        ):
            key = (r["table"], r["name"])
            im = idx.get(key)
            if im is None:
                im = IndexMeta(name=r["name"], unique=_as_bool(r.get("unique"), default=False))
                idx[key] = im
                t = tmap.get(r["table"])
                if t is not None:
                    t.indexes.append(im)
            if r.get("column"):
                im.columns.append(r["column"])

        return list(tmap.values())

    # -- 程序单元（存储过程/函数/包/触发器）------------------
    def _build_program_units(self, owner: str, include_source: bool = True,
                             source_units=None) -> list[ProgramUnitMeta]:
        umap: dict[tuple[str, str], ProgramUnitMeta] = {}
        for r in self.provider.program_units(owner):
            key = (r["name"], r["object_type"])
            umap[key] = ProgramUnitMeta(
                owner=owner,
                name=r["name"],
                object_type=r["object_type"],
                status=r.get("status"),
            )

        # 参数（不含源码时仍保留，供签名理解）
        argmap = self._arguments(owner)

        # 决定是否拉源码及拉哪些：source_units 优先于 include_source
        want = {str(n).upper() for n in source_units} if source_units else None
        if want is None and not include_source:
            for (name, otype), u in umap.items():
                if otype in ("PROCEDURE", "FUNCTION") and name in argmap:
                    u.arguments = argmap[name]
            return list(umap.values())

        # 源码按 (name, type) 分组、按行号组装（want 非空时 provider 已过滤）
        srcmap: dict[tuple[str, str], list[tuple[int, str]]] = {}
        for r in self.provider.program_source(owner, names=(list(want) if want else None)):
            srcmap.setdefault((r["name"], r["type"]), []).append(
                (r.get("line", 0), r.get("text", ""))
            )
        for key, lines in srcmap.items():
            lines.sort(key=lambda x: x[0])
            source = "".join(text for _, text in lines)
            u = umap.get(key)
            if u is not None:
                u.source = source

        # 参数按 object_name 归属到 过程/函数
        for (name, otype), u in umap.items():
            if otype in ("PROCEDURE", "FUNCTION") and name in argmap:
                u.arguments = argmap[name]

        return list(umap.values())

    def _arguments(self, owner: str) -> dict[str, list[ArgumentMeta]]:
        """按 object_name 归集子程序参数"""
        argmap: dict[str, list[ArgumentMeta]] = {}
        for r in sorted(
            self.provider.program_arguments(owner),
            key=lambda r: (r["object_name"], r.get("position", 0)),
        ):
            argmap.setdefault(r["object_name"], []).append(
                ArgumentMeta(
                    name=r.get("argument_name"),
                    data_type=r.get("data_type"),
                    in_out=r.get("in_out"),
                    position=r.get("position", 0),
                )
            )
        return argmap


def _as_bool(val, default: bool) -> bool:
    """把各库对 nullable/unique 的多种表示（Y/N、YES/NO、1/0、bool）归一为 bool"""
    if val is None:
        return default
    if isinstance(val, bool):
        return val
    s = str(val).strip().upper()
    if s in ("Y", "YES", "1", "TRUE", "UNIQUE"):
        return True
    if s in ("N", "NO", "0", "FALSE", "NONUNIQUE"):
        return False
    return default


# ── Oracle 具体实现 ──────────────────────────────────────────
# SQL 仅在真实连接时执行；单元测试不触及本类（用 FakeMetadataProvider）。

@dataclass
class DbConfig:
    """连接配置（凭据仅从环境变量注入，禁硬编码）"""
    user: str
    password: str
    dsn: str            # 形如 host:1521/service_name
    dbms: str = "oracle"

    @classmethod
    def from_env(cls) -> "DbConfig":
        user = os.getenv("MES_DB_USER")
        password = os.getenv("MES_DB_PASSWORD")
        dsn = os.getenv("MES_DB_DSN")
        dbms = os.getenv("MES_DBMS", "oracle").lower()
        missing = [k for k, v in
                   {"MES_DB_USER": user, "MES_DB_PASSWORD": password, "MES_DB_DSN": dsn}.items()
                   if not v]
        if missing:
            raise EnvironmentError(
                "缺少数据库连接环境变量：" + ", ".join(missing) +
                "（请在 .env 中配置，切勿写入代码或命令行）"
            )
        return cls(user=user, password=password, dsn=dsn, dbms=dbms)


class OracleMetadataProvider(MetadataProvider):
    """基于 ALL_* 数据字典视图的 Oracle 自省实现（只读）"""

    dbms = "oracle"

    # 各逻辑查询对应的 Oracle SQL（:owner 为绑定变量；仅 SELECT）
    _SQL = {
        "charset":
            "SELECT value FROM nls_database_parameters "
            "WHERE parameter = 'NLS_CHARACTERSET'",
        "tables":
            "SELECT t.table_name, c.comments, t.num_rows "
            "FROM all_tables t "
            "LEFT JOIN all_tab_comments c "
            "  ON c.owner = t.owner AND c.table_name = t.table_name "
            "WHERE t.owner = :owner",
        "columns":
            "SELECT table_name, column_name, data_type, data_length, "
            "       nullable, data_default, column_id "
            "FROM all_tab_columns WHERE owner = :owner "
            "ORDER BY table_name, column_id",
        "column_comments":
            "SELECT table_name, column_name, comments "
            "FROM all_col_comments WHERE owner = :owner",
        "constraints":
            "SELECT c.table_name, c.constraint_name, c.constraint_type, "
            "       c.r_owner, rc.table_name AS ref_table, "
            "       cc.column_name, cc.position "
            "FROM all_constraints c "
            "JOIN all_cons_columns cc "
            "  ON cc.owner = c.owner AND cc.constraint_name = c.constraint_name "
            "LEFT JOIN all_constraints rc "
            "  ON rc.owner = c.r_owner AND rc.constraint_name = c.r_constraint_name "
            "WHERE c.owner = :owner AND c.constraint_type IN ('P','U','R') "
            "ORDER BY c.table_name, c.constraint_name, cc.position",
        "indexes":
            "SELECT i.table_name, i.index_name, i.uniqueness, "
            "       ic.column_name, ic.column_position "
            "FROM all_indexes i "
            "JOIN all_ind_columns ic "
            "  ON ic.index_owner = i.owner AND ic.index_name = i.index_name "
            "WHERE i.owner = :owner "
            "ORDER BY i.table_name, i.index_name, ic.column_position",
        "program_units":
            "SELECT object_name, object_type, status "
            "FROM all_objects WHERE owner = :owner "
            "AND object_type IN ('PROCEDURE','FUNCTION','PACKAGE','PACKAGE BODY',"
            "                    'TRIGGER','TYPE','TYPE BODY')",
        "program_source":
            "SELECT name, type, line, text "
            "FROM all_source WHERE owner = :owner "
            "ORDER BY name, type, line",
        "program_arguments":
            "SELECT object_name, argument_name, data_type, in_out, position "
            "FROM all_arguments WHERE owner = :owner "
            "ORDER BY object_name, position",
    }

    def __init__(self, config: DbConfig, use_dba: bool = False):
        self.config = config
        self._conn = None
        # DBA 账号下 DBA_* 视图比 ALL_*（逐对象权限检查）快得多；列结构一致，仅换前缀
        prefix = "dba_" if use_dba else "all_"
        self._prefix = prefix
        self._SQL = {k: v.replace("all_", prefix) for k, v in OracleMetadataProvider._SQL.items()}

    def _connection(self):
        """懒加载 oracledb（thin 模式，免装 Oracle 客户端）"""
        if self._conn is None:
            try:
                import oracledb  # 懒加载：无库自测/单测不依赖该包
            except ImportError as e:  # pragma: no cover - 环境相关
                raise RuntimeError(
                    "未安装 oracledb，请先 `pip install oracledb`（thin 模式免装客户端）"
                ) from e
            log.info("连接 Oracle：dsn=%s user=%s（只读）", self.config.dsn, self.config.user)
            self._conn = oracledb.connect(
                user=self.config.user,
                password=self.config.password,
                dsn=self.config.dsn,
            )
        return self._conn

    def _run(self, sql: str, binds: dict) -> list[dict]:
        conn = self._connection()
        cur = conn.cursor()
        try:
            # 加大批量取行，减少 LAN 往返（大库如 MESAPUSER 7.8 万字段时显著提速）
            cur.arraysize = 5000
            cur.prefetchrows = 5000
            cur.execute(sql, binds)
            cols = [d[0].lower() for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
        finally:
            cur.close()

    def _query(self, sql: str, owner: Optional[str] = None) -> list[dict]:
        return self._run(sql, {"owner": owner} if owner is not None else {})

    # -- MetadataProvider 接口实现（把 Oracle 列名映射为统一 dict 键）--
    def charset(self) -> Optional[str]:
        rows = self._query(self._SQL["charset"])
        return rows[0]["value"] if rows else None

    def tables(self, owner: str) -> list[dict]:
        return [
            {"name": r["table_name"], "comment": r.get("comments"), "num_rows": r.get("num_rows")}
            for r in self._query(self._SQL["tables"], owner)
        ]

    def columns(self, owner: str) -> list[dict]:
        return [
            {
                "table": r["table_name"], "name": r["column_name"],
                "data_type": r["data_type"], "length": r.get("data_length"),
                "nullable": r.get("nullable"), "data_default": r.get("data_default"),
                "position": r.get("column_id", 0),
            }
            for r in self._query(self._SQL["columns"], owner)
        ]

    def column_comments(self, owner: str) -> list[dict]:
        return [
            {"table": r["table_name"], "column": r["column_name"], "comment": r.get("comments")}
            for r in self._query(self._SQL["column_comments"], owner)
        ]

    def constraints(self, owner: str) -> list[dict]:
        return [
            {
                "table": r["table_name"], "name": r["constraint_name"],
                "ctype": r["constraint_type"], "column": r.get("column_name"),
                "position": r.get("position", 0),
                "ref_owner": r.get("r_owner"), "ref_table": r.get("ref_table"),
            }
            for r in self._query(self._SQL["constraints"], owner)
        ]

    def indexes(self, owner: str) -> list[dict]:
        return [
            {
                "table": r["table_name"], "name": r["index_name"],
                "unique": r.get("uniqueness"), "column": r.get("column_name"),
                "position": r.get("column_position", 0),
            }
            for r in self._query(self._SQL["indexes"], owner)
        ]

    def program_units(self, owner: str) -> list[dict]:
        return [
            {"name": r["object_name"], "object_type": r["object_type"], "status": r.get("status")}
            for r in self._query(self._SQL["program_units"], owner)
        ]

    def program_source(self, owner: str, names=None) -> list[dict]:
        if not names:
            rows = self._query(self._SQL["program_source"], owner)
        else:
            rows = []
            names = list(names)
            view = self._prefix + "source"
            for i in range(0, len(names), 1000):          # Oracle IN 列表上限 1000，分批
                chunk = names[i:i + 1000]
                binds = {"owner": owner}
                ph = []
                for j, nm in enumerate(chunk):
                    binds[f"n{j}"] = nm
                    ph.append(f":n{j}")
                sql = (f"SELECT name, type, line, text FROM {view} "
                       f"WHERE owner = :owner AND name IN ({','.join(ph)}) "
                       f"ORDER BY name, type, line")
                rows.extend(self._run(sql, binds))
        return [
            {"name": r["name"], "type": r["type"], "line": r.get("line", 0), "text": r.get("text", "")}
            for r in rows
        ]

    def program_arguments(self, owner: str) -> list[dict]:
        return [
            {
                "object_name": r["object_name"], "argument_name": r.get("argument_name"),
                "data_type": r.get("data_type"), "in_out": r.get("in_out"),
                "position": r.get("position", 0),
            }
            for r in self._query(self._SQL["program_arguments"], owner)
        ]

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None


def get_provider(dbms: str, config: DbConfig, use_dba: bool = False) -> MetadataProvider:
    """DBMS 工厂：当前支持 oracle，后续可扩展 postgres/mysql"""
    dbms = (dbms or "").lower()
    if dbms == "oracle":
        return OracleMetadataProvider(config, use_dba=use_dba)
    raise NotImplementedError(f"暂不支持的 DBMS：{dbms}（当前仅 oracle）")


# ── 自测样例（无库可跑，用于低配机验证输出结构）──────────────

def build_self_test_provider() -> MetadataProvider:
    """返回一份仿真 MES 假数据 Provider（含中文注释、乱码占位、PL/SQL 函数）"""
    return FakeMetadataProvider(
        charset="ZHS16GBK",
        tables=[
            {"name": "WO_MASTER", "comment": "工单主表", "num_rows": 128000},
        ],
        columns=[
            {"table": "WO_MASTER", "name": "WO_ID", "data_type": "VARCHAR2", "length": 30,
             "nullable": "N", "data_default": None, "position": 1},
            {"table": "WO_MASTER", "name": "WO_STATUS", "data_type": "VARCHAR2", "length": 2,
             "nullable": "N", "data_default": "'10'", "position": 2},
            {"table": "WO_MASTER", "name": "CRT_TM", "data_type": "TIMESTAMP", "length": 11,
             "nullable": "Y", "data_default": None, "position": 3},
        ],
        column_comments=[
            {"table": "WO_MASTER", "column": "WO_ID", "comment": "工单号"},
            {"table": "WO_MASTER", "column": "WO_STATUS", "comment": "����"},  # 乱码占位
        ],
        constraints=[
            {"table": "WO_MASTER", "name": "PK_WO_MASTER", "ctype": "P",
             "column": "WO_ID", "position": 1, "ref_owner": None, "ref_table": None},
        ],
        indexes=[
            {"table": "WO_MASTER", "name": "IX_WO_STATUS", "unique": "NONUNIQUE",
             "column": "WO_STATUS", "position": 1},
        ],
        program_units=[
            {"name": "FC_YN_TO_BOOLEAN", "object_type": "FUNCTION", "status": "VALID"},
        ],
        program_source=[
            {"name": "FC_YN_TO_BOOLEAN", "type": "FUNCTION", "line": 1,
             "text": "FUNCTION FC_YN_TO_BOOLEAN(P_YN IN VARCHAR2) RETURN NUMBER IS\n"},
            {"name": "FC_YN_TO_BOOLEAN", "type": "FUNCTION", "line": 2,
             "text": "BEGIN RETURN CASE WHEN P_YN='Y' THEN 1 ELSE 0 END; END;\n"},
        ],
        program_arguments=[
            {"object_name": "FC_YN_TO_BOOLEAN", "argument_name": "P_YN",
             "data_type": "VARCHAR2", "in_out": "IN", "position": 1},
            {"object_name": "FC_YN_TO_BOOLEAN", "argument_name": None,
             "data_type": "NUMBER", "in_out": "OUT", "position": 0},  # 返回值
        ],
    )


class FakeMetadataProvider(MetadataProvider):
    """假数据 Provider：供 --self-test 与单元测试使用，不连任何数据库"""

    dbms = "fake"

    def __init__(self, charset=None, tables=None, columns=None, column_comments=None,
                 constraints=None, indexes=None, program_units=None,
                 program_source=None, program_arguments=None):
        self._charset = charset
        self._tables = tables or []
        self._columns = columns or []
        self._column_comments = column_comments or []
        self._constraints = constraints or []
        self._indexes = indexes or []
        self._program_units = program_units or []
        self._program_source = program_source or []
        self._program_arguments = program_arguments or []

    def charset(self): return self._charset
    def tables(self, owner): return list(self._tables)
    def columns(self, owner): return list(self._columns)
    def column_comments(self, owner): return list(self._column_comments)
    def constraints(self, owner): return list(self._constraints)
    def indexes(self, owner): return list(self._indexes)
    def program_units(self, owner): return list(self._program_units)
    def program_source(self, owner, names=None):
        if not names:
            return list(self._program_source)
        names = {str(n).upper() for n in names}
        return [r for r in self._program_source if str(r.get("name", "")).upper() in names]
    def program_arguments(self, owner): return list(self._program_arguments)


# ── CLI ───────────────────────────────────────────────────────

def _resolve_source_units(args) -> Optional[list]:
    """合并 --source-units（逗号）与 --source-units-file（每行一个）为单元名列表"""
    names: list[str] = []
    if getattr(args, "source_units", None):
        names += [n.strip() for n in args.source_units.split(",") if n.strip()]
    if getattr(args, "source_units_file", None):
        with open(args.source_units_file, encoding="utf-8") as f:
            names += [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    return names or None


def run(args) -> SchemaMetadata:
    if args.self_test:
        log.info("自测模式：使用仿真假数据（不连接数据库）")
        provider = build_self_test_provider()
        owner = args.owner or "MESAPUSER"
    else:
        config = DbConfig.from_env()
        provider = get_provider(args.dbms or config.dbms, config, use_dba=args.use_dba)
        owner = args.owner
        if not owner:
            raise SystemExit("请用 --owner 指定 schema（如 MESAPUSER）")

    source_units = _resolve_source_units(args)
    try:
        meta = Introspector(provider).build(
            owner, include_source=not args.no_source, source_units=source_units)
    finally:
        provider.close()

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(meta.to_dict(), f, ensure_ascii=False, indent=2)
        log.info("元数据已写入：%s", args.out)

    log.info("资产盘点摘要：%s", json.dumps(meta.summary(), ensure_ascii=False))
    return meta


def main(argv=None):
    parser = argparse.ArgumentParser(description="MES 数据库自省器（Oracle 适配层）")
    parser.add_argument("--owner", help="目标 schema（如 MESAPUSER / SCOAPUSER）")
    parser.add_argument("--out", help="输出 JSON 文件路径")
    parser.add_argument("--dbms", default=None, help="DBMS 类型（默认取环境变量 MES_DBMS 或 oracle）")
    parser.add_argument("--self-test", action="store_true",
                        help="用仿真假数据产出样例 JSON，不连接数据库（低配机可跑）")
    parser.add_argument("--no-source", dest="no_source", action="store_true",
                        help="只取程序单元清单与签名，不拉 PL/SQL 源码（大库结构盘点用）")
    parser.add_argument("--use-dba", dest="use_dba", action="store_true",
                        help="用 DBA_* 视图替代 ALL_*（DBA 账号下更快；需账号有 DBA 权限）")
    parser.add_argument("--source-units", dest="source_units",
                        help="仅拉这些单元的源码（逗号分隔单元名，如 P0 包/过程）")
    parser.add_argument("--source-units-file", dest="source_units_file",
                        help="仅拉这些单元的源码（文件，每行一个单元名；# 开头为注释）")
    args = parser.parse_args(argv)
    run(args)


if __name__ == "__main__":
    main()
