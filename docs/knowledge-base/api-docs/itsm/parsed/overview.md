## ITSM API 总览

**系统**：山信软件 ITSM API | **版本**：1.0.0 | **接口总数**：71 | **数据模型数**：35

**系统说明：**
山信软件 ITSM (IT Service Management) 系统 RESTful API 接口文档。
**认证方式说明：**
- 内部用户：使用 JWT Bearer Token 认证（`Authorization: Bearer {token}`）
- 外部系统：使用 API Key 认证（`X-API-Key: itsm_{env}_{key}`）
**设计规范：**
- 所有 ID 字段使用字符串类型传输（雪花算法 ID 避免 JS 精度丢失）
- 业务错误统一返回 HTTP 200，通过 `code` 字段区分（如 210001 表示用户名密码错误）
- 时间格式：ISO 8601（`2026-04-01T10:00:00+08:00`）
- ID 传输：字符串形式（如 `"1234567890123456789"`）

**模块汇总：**

| 模块 | 接口数 | 说明 |
|------|--------|------|
| 认证 | 6 | 登录、登出、Token 刷新、密码管理 |
| 用户与权限 | 13 | 用户管理、用户组、角色与权限配置 |
| 服务配置 | 7 | 服务目录、服务模型、工作流定义 |
| 工单核心 | 14 | 工单生命周期管理（创建、接单、转单、挂起、关闭等） |
| SLA 管理 | 5 | SLA 策略、节假日、统计报表 |
| 知识库 | 10 | 知识条目、分类、审核流程 |
| 运维日历与排班 | 5 | 日历事件、值班排班、当日值班查询 |
| 消息推送渠道 | 5 | 通知渠道配置、测试、开关控制 |
| 审计日志 | 2 | 操作审计、登录日志查询 |
| 附件管理 | 3 | 文件上传、下载、删除 |
| 系统 | 1 |  |

**统一响应结构（ApiResponse）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | integer | 业务状态码，6 位数字 |
| `message` | string | 提示信息（中文） |
| `data` | object | 业务数据，失败时为 null |
| `traceId` | string | 链路追踪 ID |

**常用数据模型：**

| Schema 名 | 用途 |
|-----------|------|
| `ApiResponse` |  |
| `PageRequest` | 分页请求参数（page/pageSize/orderBy/orderDir） |
| `PageResponse` | 分页响应结构（list/total/page/pageSize/totalPages） |
| `LoginRequest` |  |
| `LoginResponseData` | 登录成功返回（accessToken/refreshToken/expiresIn/userInfo） |
| `UserBasicInfo` | 用户基本信息（工号/姓名/邮件/角色/部门） |
| `UserDetail` |  |
| `CreateUserRequest` |  |
| `UpdateUserRequest` |  |
| `Role` |  |
| `PermissionNode` |  |
| `ServiceCatalogNode` |  |
| `ServiceModelRequest` |  |
| `FormField` |  |
| `WorkflowDef` |  |
| `WorkflowDefDetail` |  |
| `CreateTicketRequest` | 创建工单请求体（modelId/title/priority/formData） |
| `TicketBasicInfo` | 工单基本信息（工单号/状态/标题/优先级/SLA截止） |
| `TicketListItem` |  |
| `TicketDetail` |  |
| `TicketFlowLog` |  |
| `TicketComment` |  |
| `SlaPolicy` | SLA策略（响应时限/解决时限/服务时间类型） |
| `SlaPolicyRequest` |  |
| `Holiday` |  |
| `SlaStatistics` | SLA统计（达标率/平均时长/违约数） |
| `KbArticleRequest` |  |
| `KbArticleVersion` |  |
| `KbCategory` |  |
| `CalendarEvent` |  |
| `CalendarEventRequest` |  |
| `OnDutyInfo` |  |
| `NotifyChannel` |  |
| `AuditLog` |  |
| `Attachment` |  |

---
*chunk_id: itsm_api_overview*
*chunk_type: api_overview*
*关联任务：S2-2 T2-2-1 · 作者：AI（芯智云匠）· 日期：2026-04-13*