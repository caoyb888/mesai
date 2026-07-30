# 业务逻辑断言种子（静态生成，proc_parser + 表卡片，不调外部 AI）

> 种子为**候选**，须技术负责人审核后纳入基准库（CLAUDE.md §7.3 变更须审批）；
> Critical=结构性主键（100% 必过）、High=状态流转、Medium=写副作用/表关系。
> ID 命名：P0 无后缀 `AS-{ST|SQ|AP}-NNNN`；P1 带 `-P1-` 段且含 `phase:"P1"` 字段，两批 ID 零冲突。

## P0（核心）· 需求单 REQ-MES-AI-20260715-001

- **总计 657 条**：state-machine 260 / sql-logic 337 / api-behavior 60
- 级别分布：{'Critical': 89, 'High': 171, 'Medium': 397}
- 覆盖资产（含表+包）：149；断言数 <3 的资产：97（多为写/状态少的只读包）
- 文件：`*/{state-machine,sql-logic,api-behavior}_seeds.jsonl`

## P1（次核心）· 需求单 REQ-MES-AI-20260716-001（T3 批训练后置）

- **总计 980 条**：state-machine 515 / sql-logic 325 / api-behavior 140
- 级别分布：{'Critical': 235, 'High': 280, 'Medium': 465}
- 覆盖资产（含表+包）：375
- 来源：P1 静态分析——`meta_p1.json`（139 包 2352 子程序源码）+ `p1_table_cards.jsonl`（261 张 P1 表主键）
- 文件：`*/{state-machine,sql-logic,api-behavior}_seeds_p1.jsonl`；ID `AS-{ST|SQ|AP}-P1-NNNN`（各类内唯一）
- 说明：demo 垃圾表 `YOUR_TABLE_NAME` 已从清单剔除，与训练卡片一致。

**P0+P1 合计 1637 条**（Critical 324 / High 451 / Medium 862）。

## 功能契约断言 · MES 取数（mes-sql）· 需求单 REQ-MES-AI-20260716-001

- **8 条**：category=code-generation，ID `AS-CG-000N`（`source: feature-contract`，非 proc 静态分析）
- 级别：Critical 4 / High 4
- 覆盖：仅只读 SELECT（AS-CG-0001）、禁 SELECT *（0002）、接地防臆造（0003）、
  只读数据源不写（0004）、ROWNUM 行数封顶（0005）、VARCHAR2(14) 时间字段字符串比较（0006，REQ-MES-AI-20260730-001）、
  字段名逐字一致禁近似改写（0007，REQ-MES-AI-20260730-001）、代码字段禁中文标签过滤（0008，REQ-MES-AI-20260730-001）
- 文件：`code-generation/mes-sql-generation_seeds.jsonl`
- 状态：**候选**，须技术负责人审核后纳入基准库（CLAUDE.md §7.3）；对应 `/v1/ai/mes-sql` 端点与
  `SqlSafetyValidator`，其中 0001/0002/0005 已有对应 JUnit 用例（`SqlSafetyValidatorTest` / `MesSqlServiceTest`）。
