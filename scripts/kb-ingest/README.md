# scripts/kb-ingest —— 知识库素材工具链

MES AI 项目的**知识库素材抽取与治理工具集**：从数据库/文档中抽取结构化素材，
清洗、分析、对账后，供知识库向量化入库与 AI 理解训练使用。

工具分两代：

| 代次 | 面向 | 说明 |
|------|------|------|
| **真实 MES 接入期（S2.9）** | 真实 Oracle 库 | 本轮新增的自省/治理/分析/对账工具链（下方第一节） |
| **ITSM 验证期（S2-1/S2-2）** | ITSM 替身系统 | 早期跑通全链路用的解析/入库/训练脚本（下方第二节） |

> 关联计划：`docs/Plan_Adjustment_RealMES_2026.md`（AI-MES-PLAN-ADJ-2026-001）
> 安全红线：连接凭据仅从环境变量注入（禁硬编码，Gitleaks）；对生产库仅只读；
> 发往外部 AI 前必须脱敏；文档/库不一致只出清单**不静默修改**（CLAUDE.md 第四/十章）。

---

## 一、真实 MES Oracle 工具链（S2.9）

真实 MES 为 **Oracle**（克隆测试副本），schema 主要为 `MESAPUSER`（业务）/ `SCOAPUSER`（框架），
约 2121 表 / 8 万字段，业务逻辑大量在 **PL/SQL 存储过程/包** 中，注释含**中/韩/英三语**且部分乱码。
五个工具共享同一「自省 JSON」契约，端到端管道如下：

```
Oracle ──→ db_introspect.py ──→ metadata.json
   ├─ encoding_normalizer.py ──→ 注释乱码清单（也可直接治理 data_dictionary_full.csv）
   ├─ proc_parser.py ──────────→ 依赖边.csv + 硬编码·PII.csv
   │         └─ dependency_graph.py ──→ P0 核心资产报告（表/过程分级）
   └─ dict_reconcile.py（× data_dictionary_full.csv）──→ 对账差异清单 + 字典反哺清单
```

| 脚本 | Story | 输入 | 产出 |
|------|-------|------|------|
| `db_introspect.py` | S2.9-2 | Oracle 连接（env） | 结构化元数据 JSON（表/字段/约束/索引/注释 + PL/SQL 源码/签名） |
| `encoding_normalizer.py` | S2.9-3 | 自省 JSON **或** 字典 CSV | 注释乱码清单（三级分级）+ 清洗建议 CSV |
| `proc_parser.py` | S2.9-4 | 自省 JSON | 依赖边 CSV、硬编码/PII 候选 CSV、分析报告 |
| `dependency_graph.py` | S2.9-4 | 依赖边 CSV（可多份） | P0/P1/P2 核心资产报告、表/过程指标 CSV |
| `dict_reconcile.py` | S2.9-5 | 自省 JSON + 字典 CSV | 对账差异清单 + ⭐字典反哺库空注释清单 |

### 环境准备

```bash
# 依赖：自省需 oracledb（thin 模式，免装 Oracle 客户端）；其余工具纯标准库无需安装
pip install oracledb

# 连接凭据（切勿写入代码或命令行，放 .env / 环境变量）
export MES_DB_USER=<只读账号>
export MES_DB_PASSWORD=<密码>
export MES_DB_DSN=host:1521/service_name      # 形如 10.x.x.x:1521/ORCLPDB
export MES_DBMS=oracle                        # 默认 oracle
```

> **每个工具都支持 `--self-test`**：用内置假数据/真实字典 CSV 运行，无需连库，低配机秒级完成，
> 用于验证逻辑与输出结构。拿到测试机前即可先熟悉各工具输出。

### 逐步用法（拿到测试机后）

```bash
# 1) 自省真实库（S2.9-2）
#    结构盘点：大库先只拉结构、不拉源码（MESAPUSER 达 193 万行源码）；DBA 账号加 --use-dba
python db_introspect.py --owner MESAPUSER --no-source --use-dba --out meta_mes.json   # 约 28s
python db_introspect.py --owner SCOAPUSER --use-dba --out meta_sco.json
#    无库预览输出结构：python db_introspect.py --self-test --out sample.json
#
#    P0 源码深析：只拉 dependency_graph 选出的 P0 单元源码（逗号或文件名单）
python db_introspect.py --owner MESAPUSER --use-dba \
    --source-units 'BSQM_MECH_PC_TEST,BSCH_BATCHA_PLT_JOB2' --out meta_p0.json
python db_introspect.py --owner MESAPUSER --use-dba \
    --source-units-file p0_units.txt --out meta_p0.json   # 每行一个单元名，# 为注释

# 2) 编码治理（S2.9-3）——产《注释乱码清单》
python encoding_normalizer.py --input meta_mes.json \
    --out-report 注释乱码清单.md --out-cleaned cleaned_comments.csv
#    也可直接治理现成字典 CSV（无需连库）：
python encoding_normalizer.py --input-csv ../../docs/data_dictionary_full.csv \
    --out-report 注释乱码清单.md

# 3) 存储过程静态分析（S2.9-4）——产依赖边 + 硬编码/PII 候选
python proc_parser.py --input meta_mes.json \
    --out-report proc_report.md --out-edges edges.csv --out-literals pii.csv

# 4) 依赖图谱与核心资产分级（S2.9-4）——产 P0 核心资产集
python dependency_graph.py --edges edges.csv --units meta_mes.json \
    --out-report 核心资产.md --out-tables tables.csv --out-procs procs.csv

# 5) 字典对账（S2.9-5）——自省结果 vs 甲方字典
python dict_reconcile.py --introspect meta_mes.json meta_sco.json \
    --dict-csv ../../docs/data_dictionary_full.csv \
    --out-report 对账.md --out-csv discrepancies.csv
```

### 各工具要点

- **`db_introspect.py`** — DBMS 适配层（`MetadataProvider` 抽象 + `OracleMetadataProvider`，`ALL_*`/`DBA_*` 视图，
  仅 SELECT）；`oracledb` 懒加载；`SchemaMetadata.summary()` 直接给资产盘点摘要。
  关键选项：`--no-source`（只拉结构，大库先用）、`--use-dba`（DBA 账号走 DBA_* 视图）、
  `--source-units` / `--source-units-file`（**只拉指定 P0 单元的源码**，闭合"P0 分级→拉源码→深析"）；
  内置 `arraysize/prefetchrows=5000` 批量取行——实测 MESAPUSER 1860 表结构自省仅 28s。
- **`encoding_normalizer.py`** — 三级分级 `clean/recoverable/garbled`（+`empty`）；
  修复 Latin-1→GB18030/UTF-8 逆变换（GBK/UTF-8 字节被当 Latin-1 解码的典型 Oracle 乱码）；
  **韩文/中文/英文均视为可读，不误判**；修复结果仅作**建议**，不静默改源。
  注意：字典 CSV 中乱码多已被导出降级为 `????`（不可逆），**可恢复乱码只在直连库拿原始字节时出现**。
- **`proc_parser.py`** — 先剥离注释+字符串再匹配（避免注释/字符串里的表名误报），
  抽 读表(FROM/JOIN 含逗号连接)/写表(INSERT/UPDATE/DELETE/MERGE)/调用链/状态流转(SET 列=字面量)/
  硬编码·PII 候选(IP/连接串/邮箱/厂区码/长数字)；动态 SQL 标记 `has_dynamic_sql`。
- **`dependency_graph.py`** — 表评分=被读过程数+2×被写过程数；入口过程=调用入度 0 且有动作；
  过程 P0 兜底=入口且有写/编排调用 ∪ 写入 P0 表；含调用环检测；可选 `--units` 提升调用解析率。
- **`dict_reconcile.py`** — 9 类差异；整表缺失只报表级不逐列刷屏；
  ⭐ 专列「字典可反哺库空注释」清单（字典→库修复候选），呼应 `docs/data_dictionary.md` 定位。

---

## 二、ITSM 验证期脚本（S2-1 / S2-2）

早期以 ITSM 系统为替身跑通「解析 → 入库 → 训练 → 验证」全链路的脚本，产出见 `training_output/`。
真实 MES 接入后，解析入口由上述自省工具替代，但入库/训练/验证环节仍复用：

| 脚本 | 用途 |
|------|------|
| `ddl_parser.py` | PostgreSQL DDL → Markdown 表卡片（ITSM 期手工 SQL 用；真实 MES 改由 `db_introspect` 供料） |
| `api_parser.py` | OpenAPI 3.0 接口文档 → Markdown 接口卡片 |
| `dict_formatter.py` | 数据字典 Excel/Word → Markdown |
| `kb_ingest.py` | 知识库向量化入库主脚本（ChromaDB + Kimi Embedding API） |
| `kb_ingest_api.py` | 接口文档知识库入库 |
| `run_training.py` | AI 数据库理解训练执行（S2-1 T2-1-3） |
| `run_api_training.py` | AI 接口文档理解训练执行（S2-2 T2-2-3） |
| `validate_ingestion.py` | 知识库入库验证 |

`training_output/` 存放 ITSM 验证版训练/验证产物（如《S2-1 数据库结构理解报告_ITSM验证版》）。

---

## 三、测试

```bash
# 一次性安装 pytest（本机为 PEP668 外部管理环境，二选一）
pip install --user --break-system-packages pytest
#   或使用 venv： python3 -m venv .venv && .venv/bin/pip install pytest

# 运行全部单测（S2.9 工具链纯标准库，无需连库/联网）
python3 -m pytest tests/ -q
```

`tests/` 覆盖 S2.9 五个工具（`test_db_introspect` / `test_encoding_normalizer` /
`test_proc_parser` / `test_dependency_graph` / `test_dict_reconcile`）及 ITSM 期 `test_ddl_parser`，
均用假数据/真实字典 CSV，不依赖真实 Oracle。

---

## 四、约定

- **只读**：对真实库只发 SELECT；生产库禁写（本副本亦按只读对待）。
- **禁硬编码**：连接串/密码/密钥走环境变量；`proc_parser` 会额外扫出 PL/SQL 内嵌硬编码/PII 候选交脱敏层。
- **不静默改**：乱码修复、字典差异均只出**建议/清单**，回填须经人工/IT 审核（CLAUDE.md）。
- **中文注释**：新增脚本文件头须标注用途/作者(AI)/日期/关联 Story。
- **新增依赖须审批**：本目录 `requirements.txt` 为 ITSM 期入库工具所用；S2.9 工具链除 `oracledb` 外为纯标准库。
