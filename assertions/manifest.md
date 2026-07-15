# 业务逻辑断言种子（T3-4-2，静态生成）

生成自 P0 静态分析（proc_parser + 表卡片），需求单 REQ-MES-AI-20260715-001。

- **总计 657 条**：state-machine 260 / sql-logic 337 / api-behavior 60
- 级别分布：{'Critical': 89, 'High': 171, 'Medium': 397}
- 覆盖资产（含表+包）：149；断言数 <3 的资产：97（多为写/状态少的只读包）

> 种子为**候选**，须技术负责人审核后纳入基准库（CLAUDE.md §7.3 变更须审批）；
> Critical=结构性主键（100% 必过）、High=状态流转、Medium=写副作用/表关系。
