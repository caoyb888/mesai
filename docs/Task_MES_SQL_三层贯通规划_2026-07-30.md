# 任务规划：MES 数据问答 → 恢复「NL 生成 Oracle SELECT + 只读执行」原始设计

| 项 | 内容 |
|----|----|
| 关联需求单 | **REQ-MES-AI-20260730-001**（另开，见 `docs/REQ-MES-AI-20260730-001_MES取数三层贯通需求单.md`） |
| 记录日期 | 2026-07-30 |
| 状态 | 待评审 / 三个治理门待技术负责人授权 |

---

## 目标

在现有纯知识问答（`/v1/ai/mes-qa`）之外，新增取数能力：**自然语言 → 基于 mes_s3_understanding 知识库生成 Oracle 方言 SELECT → 安全校验 → 只读执行 → 返回结果行**。三层贯通，与 mes-qa 并列（保留 mes-qa 不动）。

复用两条成熟链路：
- mes-qa 的 RAG 检索（`rag.retrieve_for_mes`）
- demo 的 SQL 执行/数据源门控模式（`DemoService.executeSelect` / `ItsmDataSourceConfig` 的 `@ConditionalOnExpression`）

## ⚠️ 三个治理门（需技术负责人授权后才落地）

1. **`pom.xml` 新增 ojdbc8 依赖** — CLAUDE.md §2「未经评审不得新增依赖」。Oracle 只读执行必须它。批准本计划即视为授权此依赖。
2. **只读 MES Oracle 数据源首次接入** — §4.3/§一 职责边界「新中间件首次部署」「安全配置变更」，需真实只读账号并附回退说明。将用 `@ConditionalOnExpression` 门控，未配置 `MES_DB_URL` 时默认不注入、不执行，只返回生成的 SQL + 校验结果（优雅降级，等远程账号就绪再开）。
3. **本地无 Oracle 连接** — 端到端「真实取数」只能在远程真实 MES 只读账号上验证；本地只能验证生成 + 安全校验 + 降级路径 + Oracle 行数封顶单测。

## 分层改动

### A. AI 网关（Python）— 新 `routers/mes_sql.py`，`POST /v1/ai/mes-sql`

- RAG：复用 `retrieve_for_mes(kind=auto)` 取表+过程上下文
- 系统提示 `_MES_SQL_SYSTEM`：Oracle 方言、owner MESAPUSER、仅 SELECT、**禁止 SELECT \***、显式列名、参数化、只引用上下文中真实存在的表/字段（防臆造）、行数用 `FETCH FIRST`；输出 JSON `{sql, explanation, referenced_tables, referenced_columns, confidence, unanswerable_reason}`
- 走 `gateway_chat` 管道（脱敏→预算→provider→计量）
- `models.py` 加 `MesSqlRequest`/`MesSqlResponse`；pytest 覆盖检索调用/JSON 解析/不可答路径

### B. Spring Boot（Java）— 新模块 `module/messql`

- `MesSqlController` `POST /mes-sql/query`
- `SqlSafetyValidator`（新，安全红线核心）：单语句、必须 SELECT 开头、拦截 DDL/DML/多语句/注释注入/SELECT *
- `MesReadOnlyDataSourceConfig`：`@ConditionalOnExpression("${spring.mes.datasource.url:}")`、Hikari `read-only=true`、Oracle 驱动、`mesJdbcTemplate` bean
- 执行：`mesJdbcTemplate.queryForList(oracleRowCap(sql, 200))`，Oracle 用 `SELECT * FROM (...) WHERE ROWNUM <= 200`；未配置数据源 → `executed=false` + 原因
- DTO/VO：`MesSqlRequest(question/topN/executeSql)`、`MesSqlVO`（复用 `SqlExecutionResult`/`ContextDocVO`）
- `application-test.yml` 的 `spring.mes.datasource` 改 Oracle 占位（env 注入，零硬编码）
- JUnit：validator 全用例 + service（mock 网关 + null 数据源降级）+ 行数封顶单测，覆盖率 ≥70%

### C. 前端（Vue）— 新页 `views/mes-sql/MesSqlPage.vue`

- 输入 + 示例 + 执行开关；结果区：生成 SQL（复制按钮）+ 解释 + 引用表标签 + el-table 结果 + 截断提示 + RAG 上下文折叠 + token/延时标签 + 只读安全徽标
- `api/mesSql.js`、router、`MainLayout.vue` 菜单项

### D. 资产化（治理配套）

- Prompt 落 `/prompts/sql/mes-sql-generation.md`（§6.2）
- `/assertions` 新增 ≥3 条断言（§7.3）：SELECT 开头 / 禁 SELECT * / 只引用 KB 内表

## 验证

- **本地**：`mvn test`（Java 单测全绿）、`pytest`（网关单测）、`vite build`
- **降级路径**：未配 `MES_DB_URL` 时端到端跑通「生成+校验+返回 SQL 不执行」
- **真实取数**：需远程只读账号，届时另跑
