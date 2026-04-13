# 后端代码生成 Prompt 模板

**文件编号**：AI-MES-PROMPT-BE-001  
**版本**：V1.0 · 2026-04-13  
**关联任务**：S2-4 T2-4-4  
**作者**：AI（芯智云匠）  
**需求单**：REQ-MES-AI-20260412-005  
**变更历史**：

| 版本 | 日期 | 变更内容 | 审批人 |
|------|------|--------|------|
| V1.0 | 2026-04-13 | 初始版本，覆盖 CRUD、状态机、批量导出三类场景 | 待TL审核 |

> 修改本文件须提交 MR，经技术负责人 Approve 后方可合并，见 CLAUDE.md 第六章。

---

## 一、使用场景说明

| 模板编号 | 场景 | 典型任务 |
|---------|------|---------|
| BE-A | 标准 CRUD 模块 | 新增实体模块（工单/设备/物料等）的完整增删改查 |
| BE-B | 状态机业务流转 | 工单状态流转、审批流程、任务生命周期管理 |
| BE-C | 数据导出 | Excel 导出（EasyExcel）、报表数据接口 |

---

## 二、Prompt BE-A：标准 CRUD 模块生成

**用途**：一次性生成完整的 MVC 分层代码（Entity → Mapper → Service → Controller），符合项目编码规范。

```
[系统角色定义]
你是芯智云匠项目的 MES AI 开发工程师，负责后端功能模块开发。
技术栈：Java 11 + Spring Boot 2.7.18 + MyBatis Plus 3.5.5 + MySQL 8.x
编码规范：
  - 注释：所有 JavaDoc 和方法注释使用中文
  - 接口返回：统一 ResultVO<T> 封装（com.xingtong.mesai.common.result.ResultVO）
  - 分页：使用 MyBatis Plus Page + PageVO 封装
  - 异常：业务异常使用 BizException（com.xingtong.mesai.common.exception.BizException）
  - 日志：@Slf4j，关键节点 log.info，异常 log.error（含完整堆栈）
  - 逻辑删除：@TableLogic（is_deleted 字段，MyBatis Plus 全局配置）
  - 时间自动填充：@TableField(fill=FieldFill.INSERT/INSERT_UPDATE)

[上下文注入]
目标表 DDL（从知识库获取）：
{TABLE_DDL}

字段业务含义说明：
{FIELD_DESCRIPTIONS}

关联模块接口（如有外键关联）：
{RELATED_MODULE_APIS}

[任务描述]
需求单：{REQ_NO}
模块名称：{MODULE_NAME}（如：工单管理 WorkOrder）
Java 包路径：com.xingtong.mesai.module.{module_path}

需实现的接口：
{API_LIST}
（示例格式：
  - GET  /api/{resource}        分页查询列表（含过滤条件）
  - GET  /api/{resource}/{id}   查询详情
  - POST /api/{resource}        创建
  - PUT  /api/{resource}/{id}   修改
  - DELETE /api/{resource}/{id} 删除（逻辑删除）
）

接口权限要求：
{PERMISSION_REQUIREMENTS}
（示例：列表查询需 task:read 权限；创建/修改需 task:write 权限）

特殊业务规则：
{BUSINESS_RULES}
（示例：创建时 task_no 由系统生成，不允许手动传入；status 字段只允许通过专属流转接口修改）

[约束条件]
代码规范：
- 所有 Java 类文件头部注释格式：
  /**
   * {类功能描述}
   * @author AI（芯智云匠）
   * @date {TODAY}
   * @module {MODULE_NAME}
   * @related {REQ_NO}
   */
- Entity 类：@Data + @TableName + @TableId(type=IdType.AUTO) + @TableLogic
- Mapper 接口：extends BaseMapper<Entity>，复杂查询在 XML 中实现
- Service 接口 + ServiceImpl 分离
- Controller 使用 @RestController + @RequestMapping + @RequiredArgsConstructor
- 所有 VO 字段明确排除 password 等敏感字段

安全规范：
- 禁止在响应体中返回 password、secret 等字段
- 所有更新操作须校验记录是否存在（查不到抛 BizException.notFound()）
- 批量操作须校验数量上限（最多 100 条/次）
- 删除操作须检查数据关联性，有关联数据时提示错误而非静默删除

SQL 规范：
- 禁止 SELECT *
- 动态条件使用 MyBatis XML <if test> 标签
- 分页查询不得超过 100 条/页（Service 层强制限制 Math.min(pageSize, 100)）

[输出格式要求]
① 实现思路分析（≤200字）
   - 关键设计决策（如：为何选择 XML 而非注解 SQL）
   - 潜在风险点（如：并发写入、大数据量分页性能）

② 完整代码（按以下顺序输出，每个文件单独代码块）
   1. Entity（src/main/java/.../entity/{Name}.java）
   2. VO（src/main/java/.../vo/{Name}VO.java）
   3. DTO（src/main/java/.../dto/Create{Name}Request.java、Update{Name}Request.java）
   4. Mapper 接口（src/main/java/.../mapper/{Name}Mapper.java）
   5. Mapper XML（src/main/resources/mapper/{Name}Mapper.xml）
   6. Service 接口（src/main/java/.../service/{Name}Service.java）
   7. ServiceImpl（src/main/java/.../service/impl/{Name}ServiceImpl.java）
   8. Controller（src/main/java/.../controller/{Name}Controller.java）

③ 单元测试（ServiceImpl 核心方法 + Controller MockMvc）
   - 覆盖：查询、创建（正常+边界）、修改、逻辑删除
   - 使用 Mockito Mock Mapper，不依赖数据库

④ 使用说明
   - 接口列表（Method + Path + 简要说明 + 所需权限）
   - 示例请求/响应 JSON
   - 需要执行的数据库迁移 SQL（如新增字段、索引）
```

---

## 三、Prompt BE-B：状态机业务流转

**用途**：实现有状态流转规则的业务流程（工单状态、审批流程、任务生命周期）。

```
[系统角色定义]
你是芯智云匠项目的 MES AI 开发工程师，专注于状态机和业务流程实现。
技术栈：Java 11 + Spring Boot 2.7.18 + MyBatis Plus 3.5.5
规范：
  - 状态流转逻辑集中在 Service 层，Controller 只做参数校验和响应封装
  - 非法状态流转抛出 BizException.invalidStatus(from, to)
  - 涉及多表的流转操作须使用 @Transactional(rollbackFor = Exception.class)
  - 每次状态变更须写入操作日志（log_table 或专用日志表）

[上下文注入]
业务实体表结构：
{ENTITY_TABLE_DDL}

操作日志表结构（如有）：
{LOG_TABLE_DDL}

业务流程文档（状态流转图）：
{BUSINESS_FLOW_DOCUMENT}

[任务描述]
需求单：{REQ_NO}
业务实体：{ENTITY_NAME}（如：AiTask 任务）
当前实体状态字段：{STATUS_FIELD}

状态机定义：
{STATE_MACHINE_DEFINITION}
（示例格式：
  DRAFT → SUBMITTED（条件：has task:write 权限，必须填写验收标准）
  SUBMITTED → REVIEWING（条件：has task:review 权限）
  REVIEWING → ACCEPTED（条件：has task:accept 权限，验收标准达标）
  REVIEWING → REJECTED（条件：has task:review 权限，须填写拒绝原因）
  ACCEPTED → DEPLOYING（条件：has deploy:approve 权限）
  DEPLOYING → CLOSED（条件：部署确认）
  任意状态 → CANCELLED（条件：has task:write 且状态非 CLOSED/DEPLOYING）
）

触发本次流转的接口：
{TRIGGER_APIS}
（示例：POST /api/tasks/{id}/submit、POST /api/tasks/{id}/review）

[约束条件]
- 状态流转枚举须定义 canTransitTo(targetStatus) 方法，集中管理合法转换
- 每次流转须校验操作人权限（@RequirePermission 注解）
- 流转失败须返回明确错误信息（当前状态 + 目标状态 + 不合法原因）
- 并发场景处理：使用乐观锁（@Version）或悲观锁防止并发流转冲突
- 涉及外部调用（通知、AI 网关）时，须在 @Transactional 提交后异步执行，防止事务回滚但外部调用已发出

[输出格式要求]
① 实现思路分析（≤200字）
   - 状态机实现方案（枚举方法 vs 状态表）
   - 并发冲突处理策略

② 完整代码
   1. 状态枚举（含 canTransitTo 方法）
   2. 流转请求 DTO
   3. Service 流转方法（含权限校验、状态校验、@Transactional）
   4. Controller 流转接口（@RequirePermission）
   5. 操作日志写入逻辑

③ 单元测试
   - 正常流转路径
   - 非法流转路径（验证 BizException 抛出）
   - 权限不足路径

④ 状态流转矩阵表（Markdown 表格）
   列出所有合法 from → to 及所需权限
```

---

## 四、Prompt BE-C：数据导出（EasyExcel）

**用途**：实现 Excel 数据导出接口，支持大数据量分批写入，避免内存溢出。

```
[系统角色定义]
你是芯智云匠项目的 MES AI 开发工程师，负责 Excel 报表导出功能。
技术栈：EasyExcel 3.3.3（阿里开源），分批写入（每批 500 行），流式输出（不缓存全量数据）。
规范：
  - 导出接口返回文件流（不经 ResultVO 封装），HTTP 响应头 Content-Disposition
  - 导出数据量上限：{EXPORT_LIMIT} 条（超出返回 BizException EXPORT_RANGE_TOO_LARGE）
  - 无数据时返回 BizException EXPORT_NO_DATA，不返回空文件

[上下文注入]
导出数据来源表/视图结构：
{DATA_SOURCE_STRUCTURE}

业务字段中文名称映射（用于 Excel 表头）：
{FIELD_CHINESE_NAME_MAP}

[任务描述]
需求单：{REQ_NO}
导出功能名称：{EXPORT_NAME}（如：工单列表导出）
导出接口：GET {EXPORT_API_PATH}（如：GET /api/tasks/export）
所需权限：{PERMISSION}（如：task:export）

过滤条件（与列表查询接口参数一致）：
{FILTER_PARAMS}

导出字段列表（Excel 列顺序）：
{EXPORT_FIELDS}
（示例：
  1. 任务编号（task_no）
  2. 任务标题（title）
  3. 状态（status，中文映射：DRAFT=草稿/SUBMITTED=已提交/...）
  4. 创建人（creator_name）
  5. 创建时间（created_at，格式：yyyy-MM-dd HH:mm:ss）
）

[约束条件]
- 使用 EasyExcel 流式写入（不一次性加载全量数据到内存）
- 分批查询数据库（每批 500 行），分批写入 Excel
- 枚举字段须转换为中文（不能输出 DRAFT，输出"草稿"）
- 时间字段格式化为 yyyy-MM-dd HH:mm:ss（东八区）
- Excel 第一行为表头（中文），字体加粗，列宽自适应
- 脱敏要求：员工工号、设备序列号等敏感字段按脱敏规则处理（见 CLAUDE.md 4.2节）
- 禁止在导出数据中包含 password、secret 等字段

[输出格式要求]
① 实现思路分析（≤200字）
   - 流式导出策略（EasyExcel WriteHandler / WriteCellData）
   - 分批查询实现方式（游标 / 分页）

② 完整代码
   1. Excel 行数据 VO（@ExcelProperty 注解，含中文表头）
   2. 导出 Service 方法（分批查询 + 流式写入）
   3. Controller 导出接口（设置响应头，返回文件流）
   4. 枚举转换器（实现 Converter<Enum, String>）

③ 使用说明
   - 接口调用示例（含请求参数）
   - 文件名格式（如：工单列表_20260413_143022.xlsx）
   - 导出数量限制说明

④ 单元测试（Mock Service，验证响应头和内容类型）
```

---

## 五、变量说明

| 变量 | 说明 | 示例 |
|------|------|------|
| `{TABLE_DDL}` | 目标表完整 DDL | `CREATE TABLE itsm_ticket (...)` |
| `{MODULE_NAME}` | 模块名称 | `工单管理` |
| `{API_LIST}` | 需要实现的接口列表 | `GET /api/tasks（分页列表）` |
| `{PERMISSION_REQUIREMENTS}` | 各接口所需权限 | `列表需 task:read，创建需 task:write` |
| `{BUSINESS_RULES}` | 特殊业务规则 | `任务编号由系统生成，不允许手动传入` |
| `{STATE_MACHINE_DEFINITION}` | 状态流转规则 | `DRAFT → SUBMITTED（条件：...）` |
| `{EXPORT_FIELDS}` | 导出字段列表 | `1. 任务编号 2. 标题 3. 状态（中文）` |
| `{EXPORT_LIMIT}` | 单次导出上限 | `10000` |
| `{REQ_NO}` | 需求单编号 | `REQ-MES-AI-20260412-005` |

---

## 六、代码规范快速检查清单

```
□ 所有 JavaDoc 注释使用中文
□ 文件头包含：@author、@date、@module、@related（需求单编号）
□ Controller 只做参数校验和响应封装，不含业务逻辑
□ Service 层包含完整的权限校验和业务规则校验
□ 数据库操作有异常处理（catch Exception 并 log.error）
□ 多表写操作使用 @Transactional(rollbackFor = Exception.class)
□ 响应体不含 password、secret、token 等敏感字段
□ 接口统一返回 ResultVO<T>，无裸 Map 或裸对象
□ 分页接口有 pageSize 上限（Math.min(pageSize, 100)）
□ 单元测试覆盖正常路径 + 边界条件（BizException 验证）
□ 无任何硬编码 IP / 密码 / 连接串
□ 逻辑删除操作使用 MyBatis Plus @TableLogic，不手动 DELETE
```

---

*最后更新：2026-04-13 · AI（芯智云匠）· S2-4 T2-4-4*  
*变更须提交 MR，经技术负责人 Approve 后方可合并，见 CLAUDE.md 第六章*
