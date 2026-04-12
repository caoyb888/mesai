# 芯智云匠 · API 接口规范文档
## 山东芯通 MES AI 智能体资产化项目

| 项目 | 内容 |
|------|------|
| 文件编号 | AI-MES-API-2026-001 |
| 版本号 | V1.1 |
| 规范标准 | OpenAPI 3.0.3 |
| 编写日期 | 2026年4月 |
| 编写单位 | 乙方技术团队 |
| 关联数据库设计 | AI-MES-DB-2026-001 (V1.1) |
| 文件状态 | 正式发布 |

### 版本变更说明（V1.0 → V1.1）

| # | 变更类型 | 变更内容 |
|---|--------|--------|
| 1 | **新增接口** | `POST /knowledge/documents/upload`：物理文件上传接口，支持 PDF/MD/DOCX，知识摄入流程闭环 |
| 2 | **新增接口** | `GET /tasks/export`：任务列表 Excel 导出 |
| 3 | **新增接口** | `GET /cost/stat/export`：多维度成本统计 Excel 导出 |
| 4 | **新增接口** | `GET /monitor/inspections/export`：巡检报告列表 Excel 导出 |
| 5 | **新增接口** | `GET /cost/daily/export`：Token 日消耗 Excel 导出 |
| 6 | **完善** | 导出接口统一响应头规范、文件命名规则、异步导出与同步导出的选择策略 |

---

## 目录

1. [总体说明](#一总体说明)
2. [鉴权规范](#二鉴权规范)
3. [通用约定](#三通用约定)
4. [错误码规范](#四错误码规范)
5. [任务管理模块](#五任务管理模块)
6. [评审与授权模块](#六评审与授权模块)
7. [部署管理模块](#七部署管理模块)
8. [运维监控模块](#八运维监控模块)
9. [知识库模块](#九知识库模块)
10. [断言库模块](#十断言库模块)
11. [成本统计模块](#十一成本统计模块)
12. [系统管理模块](#十二系统管理模块)
13. [导出接口规范（Export）](#十三导出接口规范export)
14. [Schema 定义（Components）](#十四schema-定义components)
15. [附录](#十五附录)

---

## 一、总体说明

### 1.1 服务信息

```yaml
openapi: 3.0.3
info:
  title: 芯智云匠 MES AI 任务管理平台 API
  description: |
    山东芯通微电子 MES AI 智能体资产化项目后端接口规范。
    本 API 服务于四类使用方：
      - 业务人员：提交需求单、跟踪任务状态、参与验收
      - IT 专员/负责人：评审需求、人工授权、部署审批
      - AI Agent：写入执行日志、代码交付物、测试报告、巡检报告
      - 管理层：查阅 Token 成本、ROI 报告、巡检数据（含 Excel 导出）
  version: "1.1.0"
  contact:
    name: 乙方技术团队

servers:
  - url: https://ai-mes.xingtong.internal/api/v1
    description: 内网生产环境（仅限内网访问）
  - url: https://ai-mes-test.xingtong.internal/api/v1
    description: 内网测试环境
```

### 1.2 基础路径规则

| 规则 | 说明 |
|------|------|
| Base URL | `https://ai-mes.xingtong.internal/api/v1` |
| 协议 | HTTPS（内网自签证书） |
| 字符编码 | UTF-8 |
| 时间格式 | ISO 8601，`yyyy-MM-dd'T'HH:mm:ss+08:00`（东八区） |
| 日期格式 | `yyyy-MM-dd` |
| 分页参数 | `page`（从 1 开始）、`pageSize`（默认 20，最大 100） |
| 排序参数 | `sortBy` 字段名，`sortOrder` 枚举 `asc`/`desc` |
| 逻辑删除 | 所有列表接口默认过滤 `is_deleted=1` 的记录 |
| 文件上传 | `Content-Type: multipart/form-data`，单文件上限 **50MB** |
| 文件下载 | `Accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |

### 1.3 模块与路径映射

| 模块 | 路径前缀 | 说明 |
|------|--------|------|
| 任务管理 | `/tasks` | 需求单全生命周期 + 导出 |
| 评审与授权 | `/reviews`, `/approvals` | IT 评审、人工授权网关 |
| 部署管理 | `/deployments` | 部署申请与审批 |
| 运维监控 | `/monitor` | 巡检报告、告警记录 + 导出 |
| 知识库 | `/knowledge` | 文档管理、**文件上传**、向量块查询 |
| 断言库 | `/assertions` | 断言定义、批次执行、结果 |
| 成本统计 | `/cost` | Token 日报、ROI 汇总 + **导出** |
| 系统管理 | `/system` | 用户、健康检查、配置 |

---

## 二、鉴权规范

### 2.1 鉴权方案

本系统采用 **JWT Bearer Token** 鉴权，结合 **RBAC 角色权限控制**。

```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        通过 POST /system/auth/login 获取 access_token。
        所有接口（健康检查、登录除外）在 Request Header 中携带：
          Authorization: Bearer <access_token>
        文件下载接口亦可通过 Query Parameter 传入 Token：
          ?token=<access_token>
        （用于浏览器直链下载场景，有效期限制为 5 分钟的一次性下载 Token）
```

### 2.2 获取 Token

**`POST /system/auth/login`**  权限：公开

**Request Body：**

```json
{
  "username": "zhangsan",
  "password": "••••••••"
}
```

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "tokenType": "Bearer",
    "expiresIn": 28800,
    "refreshToken": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4...",
    "userInfo": {
      "userId": 1001,
      "username": "zhangsan",
      "realName": "张三",
      "role": "IT_REVIEWER",
      "dept": "IT部",
      "permissions": ["task:read", "task:review", "approval:write"]
    }
  }
}
```

### 2.3 刷新 Token

**`POST /system/auth/refresh`**  权限：公开

**Request Body：** `{ "refreshToken": "..." }`

**Response 200：** 同登录响应结构，返回新 `accessToken`。

### 2.4 角色与权限矩阵

| 角色代码 | 角色名称 | 说明 |
|--------|--------|------|
| `BUSINESS_USER` | 业务人员 | 提交需求、查看自己的任务、参与验收 |
| `IT_REVIEWER` | IT 评审专员 | 评审需求、查看全部任务、执行授权 |
| `IT_MANAGER` | IT 负责人 | IT_REVIEWER 全部权限 + 部署审批 + 配置管理 |
| `TECH_LEAD` | 技术负责人 | 全部权限，管理断言库、审批 Prompt 变更 |
| `AI_AGENT` | AI 智能体 | 写入执行日志、代码交付物、测试报告（服务账号） |
| `MANAGER` | 管理层（只读） | 查看报告、成本统计、Excel 导出，无写权限 |

| 权限标识 | BUSINESS_USER | IT_REVIEWER | IT_MANAGER | TECH_LEAD | AI_AGENT | MANAGER |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|
| `task:read` | 仅自己 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `task:write` | ✓ | — | — | ✓ | — | — |
| `task:review` | — | ✓ | ✓ | ✓ | — | — |
| `task:accept` | ✓ | ✓ | ✓ | ✓ | — | — |
| `task:export` | — | ✓ | ✓ | ✓ | — | ✓ |
| `approval:write` | — | ✓ | ✓ | ✓ | — | — |
| `deploy:approve` | — | — | ✓ | ✓ | — | — |
| `exec_log:write` | — | — | — | ✓ | ✓ | — |
| `artifact:write` | — | — | — | ✓ | ✓ | — |
| `monitor:read` | — | ✓ | ✓ | ✓ | — | ✓ |
| `monitor:export` | — | ✓ | ✓ | ✓ | — | ✓ |
| `knowledge:upload` | — | ✓ | ✓ | ✓ | — | — |
| `assertion:manage` | — | — | — | ✓ | — | — |
| `cost:read` | — | ✓ | ✓ | ✓ | — | ✓ |
| `cost:export` | — | ✓ | ✓ | ✓ | — | ✓ |
| `system:admin` | — | — | ✓ | ✓ | — | — |

### 2.5 Token 安全要求

- `accessToken` 有效期 **8 小时**，`refreshToken` 有效期 **7 天**
- AI Agent 使用独立服务账号 Token，有效期 **30 天**，需定期轮换
- 所有 Token 均通过 HMAC-SHA256 签名，密钥存储于 HashiCorp Vault
- 文件下载一次性 Token 有效期 **5 分钟**，通过 `POST /system/auth/download-token` 换取
- Token 泄露后可通过 `POST /system/auth/revoke` 立即吊销

### 2.6 获取文件下载一次性 Token

**`POST /system/auth/download-token`**  权限：对应模块的 export 权限

**描述：** 用于浏览器直链下载场景，换取一个 5 分钟有效的一次性下载 Token，可附在导出接口 URL 的 `?token=` 参数上。

**Request Body：** `{ "resourcePath": "/cost/stat/export?month=2026-04&groupBy=dept" }`

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "downloadToken": "dl-one-time-token-xxxx",
    "expiresIn": 300,
    "resourcePath": "/cost/stat/export?month=2026-04&groupBy=dept"
  }
}
```

---

## 三、通用约定

### 3.1 统一响应结构

所有**非文件下载**接口均返回以下统一结构（对应后端 `ResultVO<T>`）：

```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "timestamp": "2026-04-11T10:30:00+08:00",
  "requestId": "req-uuid-xxxx"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | integer | 业务状态码，`0` 表示成功，非 0 表示业务错误 |
| `message` | string | 提示信息（成功时为 `"success"`） |
| `data` | object/array/null | 业务数据，失败时为 `null` |
| `timestamp` | string | 服务端响应时间（ISO 8601） |
| `requestId` | string | 链路追踪 ID，排查问题时提供此值 |

### 3.2 分页响应结构

列表接口的 `data` 字段统一使用以下结构：

```json
{
  "list": [],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 158,
    "totalPages": 8
  }
}
```

### 3.3 文件下载响应规范

所有导出/下载接口不使用 `ResultVO` 包装，直接返回文件字节流：

```
HTTP 200 OK
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename*=UTF-8''<URL编码的文件名>.xlsx
Content-Length: <字节数>
X-Request-Id: req-uuid-xxxx
```

**文件命名规则：**

| 接口 | 文件名格式 | 示例 |
|------|--------|------|
| 任务列表导出 | `tasks_export_{yyyyMMdd_HHmmss}.xlsx` | `tasks_export_20260411_103000.xlsx` |
| 成本统计导出 | `cost_stat_{month}_{groupBy}_{yyyyMMdd}.xlsx` | `cost_stat_2026-04_dept_20260411.xlsx` |
| Token 日报导出 | `token_daily_{dateFrom}_{dateTo}.xlsx` | `token_daily_20260401_20260411.xlsx` |
| 巡检报告导出 | `inspection_export_{dateFrom}_{dateTo}.xlsx` | `inspection_export_20260401_20260411.xlsx` |
| 知识文档列表导出 | `knowledge_docs_{yyyyMMdd}.xlsx` | `knowledge_docs_20260411.xlsx` |

**文件下载失败时（如权限不足、参数错误）：**  
HTTP 状态码 ≠ 200，响应体为标准 `ResultVO` 错误结构（JSON 格式）。

### 3.4 文件上传规范

```
POST /knowledge/documents/upload
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
```

| 约束项 | 规则 |
|--------|------|
| 允许格式 | `.pdf` `.md` `.docx` `.xlsx` `.txt` |
| 单文件大小上限 | **50 MB** |
| 单次上传文件数 | 最多 **5** 个 |
| 文件名编码 | UTF-8，服务端存储时统一进行 sanitize 处理 |
| 存储路径 | 上传后存储至内网文件服务器（路径由服务端分配，客户端无需指定） |
| 同名文件处理 | 以文档编码（`docCode`）为唯一键，重复上传视为版本更新 |

### 3.5 请求头规范

| Header | 必填 | 说明 |
|--------|------|------|
| `Authorization` | ✓（公开接口除外） | `Bearer <token>` |
| `Content-Type` | 写操作必填 | JSON 接口：`application/json; charset=UTF-8`；上传接口：`multipart/form-data` |
| `Accept` | 下载接口必填 | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| `X-Request-Id` | 建议 | 客户端生成的请求 UUID，用于链路追踪 |

### 3.6 异步导出 vs 同步导出策略

| 导出数据量 | 策略 | 接口行为 |
|--------|------|--------|
| **预估 ≤ 5000 行** | 同步导出 | 直接返回文件字节流，`Content-Type: .xlsx` |
| **预估 > 5000 行** | 异步导出 | 返回 `{ "jobId": "export-job-xxxx", "estimatedSeconds": 30 }`，客户端轮询 `GET /system/export-jobs/{jobId}` 获取下载链接 |

本项目当前预计各导出场景的数据量均 ≤ 5000 行，**全部采用同步导出**。未来数据增长后可无缝切换为异步模式，接口 URL 不变，仅响应结构变化。

---

## 四、错误码规范

### 4.1 HTTP 状态码使用规则

| HTTP 状态码 | 使用场景 |
|-----------|--------|
| `200 OK` | 请求成功（业务成功/失败均返回 200，通过 `code` 字段区分） |
| `400 Bad Request` | 请求参数格式错误（JSON 解析失败、参数类型不匹配） |
| `401 Unauthorized` | Token 缺失、过期或签名无效 |
| `403 Forbidden` | Token 有效但权限不足 |
| `404 Not Found` | 路由不存在（**注意**：资源不存在返回 HTTP 200 + 业务错误码 10004） |
| `413 Payload Too Large` | 上传文件超过 50MB 限制 |
| `415 Unsupported Media Type` | 上传了不支持的文件格式 |
| `429 Too Many Requests` | 请求频率超限 |
| `500 Internal Server Error` | 服务端未捕获异常 |
| `503 Service Unavailable` | 服务启动中或依赖不可用 |

### 4.2 业务错误码定义

#### 通用错误（1xxxx）

| code | 标识 | message | 说明 |
|------|------|---------|------|
| `10001` | `PARAM_MISSING` | 缺少必填参数：{fieldName} | 请求体缺少必填字段 |
| `10002` | `PARAM_INVALID` | 参数格式错误：{fieldName} | 字段值不合法 |
| `10003` | `PARAM_TOO_LONG` | 参数超出最大长度：{fieldName} | 超过字段长度限制 |
| `10004` | `RESOURCE_NOT_FOUND` | 资源不存在：{resourceType}={id} | 查询的业务对象不存在 |
| `10005` | `RESOURCE_DELETED` | 资源已被删除：{resourceType}={id} | 操作了已逻辑删除的记录 |
| `10006` | `DUPLICATE_KEY` | 唯一键冲突：{fieldName} | 如 task_no、docCode 重复 |
| `10007` | `OPERATION_FORBIDDEN` | 当前状态不允许该操作 | 状态机约束 |
| `10008` | `CONCURRENT_CONFLICT` | 并发冲突，请稍后重试 | 乐观锁冲突 |
| `10009` | `DATA_INTEGRITY_ERROR` | 数据完整性校验失败 | 关联数据不一致 |

#### 鉴权错误（2xxxx）

| code | 标识 | message | 说明 |
|------|------|---------|------|
| `20001` | `TOKEN_MISSING` | 请求头缺少 Authorization | 未携带 Token |
| `20002` | `TOKEN_EXPIRED` | Token 已过期，请重新登录 | accessToken 超时 |
| `20003` | `TOKEN_INVALID` | Token 签名无效 | Token 被篡改 |
| `20004` | `TOKEN_REVOKED` | Token 已被吊销 | 主动登出或强制下线 |
| `20005` | `PERMISSION_DENIED` | 权限不足：需要 {permission} | RBAC 权限校验失败 |
| `20006` | `DOWNLOAD_TOKEN_EXPIRED` | 下载 Token 已过期或已使用 | 一次性下载 Token 失效 |

#### 任务模块错误（3xxxx）

| code | 标识 | message | 说明 |
|------|------|---------|------|
| `30001` | `TASK_STATUS_INVALID` | 任务状态流转非法：{from} → {to} | 状态机约束违反 |
| `30002` | `TASK_NOT_REVIEWABLE` | 任务不在可评审状态 | 非 SUBMITTED 状态 |
| `30003` | `TASK_NOT_ACCEPTABLE` | 任务不在可验收状态 | 非 PENDING_REVIEW 状态 |
| `30004` | `TASK_ALREADY_REVIEWED` | 任务已完成评审 | 重复评审 |
| `30005` | `TASK_NO_GENERATE_FAIL` | 任务编号生成失败，请重试 | Redis 和 DB 均不可用 |
| `30006` | `ACCEPT_CRITERIA_REQUIRED` | 提交任务需填写验收标准 | 验收标准为空 |
| `30007` | `EXPORT_NO_DATA` | 导出范围内无数据，请调整筛选条件 | 导出结果为空 |
| `30008` | `EXPORT_RANGE_TOO_LARGE` | 导出数据量超过上限，请缩小时间范围 | 超过异步阈值且未启用异步 |

#### 授权模块错误（4xxxx）

| code | 标识 | message | 说明 |
|------|------|---------|------|
| `40001` | `APPROVAL_EXPIRED` | 授权已超时，请重新发起 | expire_at 已过 |
| `40002` | `APPROVAL_ALREADY_DECIDED` | 授权已处理，无法重复操作 | 已 APPROVED/REJECTED |
| `40003` | `APPROVAL_NOT_PENDING` | 授权不在待处理状态 | 非 PENDING 状态 |
| `40004` | `DDL_CHANGE_NEED_DBA` | DDL 变更需 DBA 审批 | 角色约束 |

#### 部署模块错误（5xxxx）

| code | 标识 | message | 说明 |
|------|------|---------|------|
| `50001` | `DEPLOY_NOT_ACCEPTED` | 任务未通过验收，无法发起部署 | 状态约束 |
| `50002` | `DEPLOY_ROLLBACK_PLAN_EMPTY` | 回退方案不能为空 | 必填规则 |
| `50003` | `DEPLOY_ALREADY_APPLIED` | 该任务已有待审批的部署申请 | 重复申请 |
| `50004` | `DEPLOY_APPROVAL_REQUIRED` | 部署需 IT 负责人签批 | 权限约束 |

#### AI 执行模块错误（6xxxx）

| code | 标识 | message | 说明 |
|------|------|---------|------|
| `60001` | `EXEC_LOG_NOT_DESENSITIZED` | 日志内容未经脱敏处理，拒绝写入 | **安全红线** |
| `60002` | `HARDCODE_DETECTED` | 代码包含硬编码敏感信息，拒绝提交 | **安全红线** |
| `60003` | `SONAR_CRITICAL_EXIST` | SonarQube 存在 Critical 问题，拒绝提交 | 质量门禁 |
| `60004` | `TOKEN_BUDGET_EXCEEDED` | 当日 Token 预算已超限，非紧急任务已暂停 | 成本控制 |
| `60005` | `TASK_NOT_RUNNING` | 任务不在 AI_RUNNING 状态，无法写入日志 | 状态约束 |

#### 知识库/断言模块错误（7xxxx）

| code | 标识 | message | 说明 |
|------|------|---------|------|
| `70001` | `CHUNK_SYNC_PENDING` | 向量块尚未同步完成，请稍后查询 | 同步状态约束 |
| `70002` | `ASSERTION_CHANGE_NEED_APPROVAL` | 断言库修改需技术负责人审批 | 权限约束 |
| `70003` | `ASSERTION_BATCH_RUNNING` | 当前已有断言批次在执行中 | 并发控制 |
| `70004` | `CRITICAL_ASSERTION_FAILED` | Critical 断言失败，变更已被阻断 | 断言阻断 |

#### 文件处理错误（8xxxx）

| code | 标识 | message | 说明 |
|------|------|---------|------|
| `80001` | `FILE_FORMAT_NOT_SUPPORTED` | 不支持的文件格式：{extension}，仅允许 PDF/MD/DOCX/XLSX/TXT | 格式校验 |
| `80002` | `FILE_SIZE_EXCEEDED` | 文件大小超过限制（最大 50MB）：{filename} | 大小校验 |
| `80003` | `FILE_COUNT_EXCEEDED` | 单次最多上传 5 个文件 | 数量限制 |
| `80004` | `FILE_PARSE_FAILED` | 文件解析失败，请检查文件是否损坏：{filename} | 解析错误 |
| `80005` | `FILE_VIRUS_DETECTED` | 文件安全扫描未通过：{filename} | 安全扫描（预留） |
| `80006` | `STORAGE_UNAVAILABLE` | 文件存储服务暂不可用，请稍后重试 | 存储服务异常 |

### 4.3 错误响应示例

```json
{
  "code": 80001,
  "message": "不支持的文件格式：.exe，仅允许 PDF/MD/DOCX/XLSX/TXT",
  "data": null,
  "timestamp": "2026-04-11T10:30:00+08:00",
  "requestId": "req-a1b2c3d4"
}
```

---

## 五、任务管理模块

### 5.1 创建需求单

**`POST /tasks`**  权限：`task:write`

**描述：** 业务人员创建新的 MES AI 功能开发需求单。`taskNo` 由服务端通过 Redis 分布式递增自动生成，客户端无需传入。

**Request Body：**

```json
{
  "title": "新增设备点检记录功能（含前端页面）",
  "taskType": "FEAT",
  "priority": 2,
  "dept": "生产技术部",
  "module": "设备管理",
  "bizBackground": "目前设备点检记录只能纸质登记，无法实时查询历史数据，影响设备维护效率。",
  "funcDesc": "开发设备点检记录功能，包括：点检记录的新增、查询、导出；历史数据查看；点检状态统计报表。",
  "inputData": "设备编号、点检项目、点检结果、点检人、点检时间",
  "expectedOutput": "点检记录列表、统计报表（日/周/月）、Excel 导出",
  "bizRules": "点检状态：正常/异常/待复查。异常状态需触发告警通知相关负责人。",
  "modulesInvolved": ["设备管理", "报表中心"],
  "deviceInvolved": "涉及所有在线设备，通过现有设备管理接口读取设备列表",
  "acceptCriteria": [
    {
      "condition": "点检记录可正常新增",
      "expected": "提交后数据库记录创建成功，返回记录 ID",
      "result": null
    },
    {
      "condition": "历史记录可按设备号和时间范围查询",
      "expected": "返回分页列表，响应时间 ≤ 2 秒",
      "result": null
    },
    {
      "condition": "Excel 导出功能正常",
      "expected": "导出文件格式正确，数据与页面展示一致",
      "result": null
    }
  ],
  "perfRequirement": "列表查询响应时间 ≤ 2 秒，并发用户 ≥ 10",
  "expectedFinishDate": "2026-04-18",
  "remark": ""
}
```

**Request 字段说明：**

| 字段 | 类型 | 必填 | 约束 | 说明 |
|------|------|:---:|------|------|
| `title` | string | ✓ | 最大 100 字符 | 需求标题 |
| `taskType` | string | ✓ | 枚举见下表 | 任务类型 |
| `priority` | integer | ✓ | 1-4 | 1-紧急 2-高 3-中 4-低 |
| `dept` | string | ✓ | 最大 50 字符 | 所属部门（成本分摊维度） |
| `module` | string | ✗ | 最大 50 字符 | 所属 MES 模块（成本分摊维度） |
| `bizBackground` | string | ✗ | — | 业务背景 |
| `funcDesc` | string | ✗ | — | 功能描述 |
| `inputData` | string | ✗ | — | 输入数据说明 |
| `expectedOutput` | string | ✗ | — | 期望输出 |
| `bizRules` | string | ✗ | — | 业务规则 |
| `modulesInvolved` | array[string] | ✗ | — | 涉及模块列表 |
| `deviceInvolved` | string | ✗ | — | 涉及设备 |
| `acceptCriteria` | array[AcceptCriterion] | ✗ | — | 验收标准，提交时 result 为 null |
| `perfRequirement` | string | ✗ | 最大 500 字符 | 性能要求 |
| `expectedFinishDate` | string | ✗ | `yyyy-MM-dd` | 期望完成日期 |
| `remark` | string | ✗ | — | 备注 |

**taskType 枚举说明：**

| 值 | 说明 |
|----|------|
| `FEAT` | 新功能开发 |
| `FIX` | 功能修改 |
| `REPORT` | 报表开发 |
| `QUERY` | 数据查询 |
| `API` | 接口开发 |
| `BUG` | 缺陷修复 |
| `PERF` | 性能优化 |

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1024,
    "taskNo": "REQ-MES-AI-20260411-003",
    "status": "DRAFT",
    "createdAt": "2026-04-11T10:30:00+08:00"
  }
}
```

---

### 5.2 提交需求单

**`POST /tasks/{taskId}/submit`**  权限：`task:write`

**描述：** 将草稿状态的需求单提交至 IT 评审队列，提交时校验验收标准不能为空。

| Path 参数 | 类型 | 必填 | 说明 |
|--------|------|:---:|------|
| `taskId` | integer(int64) | ✓ | 任务主键 ID |

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "taskId": 1024,
    "taskNo": "REQ-MES-AI-20260411-003",
    "fromStatus": "DRAFT",
    "toStatus": "SUBMITTED",
    "submittedAt": "2026-04-11T10:35:00+08:00"
  }
}
```

**可能的错误码：** `10004` `30001` `30006`

---

### 5.3 获取任务详情

**`GET /tasks/{taskId}`**  权限：`task:read`

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1024,
    "taskNo": "REQ-MES-AI-20260411-003",
    "title": "新增设备点检记录功能（含前端页面）",
    "taskType": "FEAT",
    "priority": 2,
    "status": "AI_RUNNING",
    "dept": "生产技术部",
    "module": "设备管理",
    "submitterId": 201,
    "submitterName": "李工",
    "bizBackground": "...",
    "funcDesc": "...",
    "acceptCriteria": [
      { "condition": "点检记录可正常新增", "expected": "...", "result": null }
    ],
    "perfRequirement": "列表查询响应时间 ≤ 2 秒",
    "expectedFinishDate": "2026-04-18",
    "estimatedHours": 6.0,
    "actualHours": null,
    "qualityScore": null,
    "reviewRecord": {
      "reviewerId": 301,
      "reviewerName": "王工",
      "reviewResult": "APPROVED",
      "reviewOpinion": "需求清晰，可执行",
      "estimatedHours": 6.0,
      "planStartTime": "2026-04-11T14:00:00+08:00",
      "reviewTime": "2026-04-11T11:00:00+08:00"
    },
    "executionProgress": {
      "currentStage": "CODEGEN",
      "progressPct": 65,
      "estimatedRemainingMinutes": 45,
      "stages": [
        { "stage": "UNDERSTAND", "status": "DONE",    "completedAt": "2026-04-11T14:05:00+08:00" },
        { "stage": "PLAN",       "status": "DONE",    "completedAt": "2026-04-11T14:12:00+08:00" },
        { "stage": "CODEGEN",    "status": "RUNNING", "completedAt": null },
        { "stage": "TEST",       "status": "PENDING", "completedAt": null },
        { "stage": "REPORT",     "status": "PENDING", "completedAt": null }
      ]
    },
    "pendingApproval": {
      "gateId": 88,
      "gateType": "PLAN_CONFIRM",
      "gateTitle": "实现方案确认",
      "status": "APPROVED",
      "approvedAt": "2026-04-11T14:18:00+08:00"
    },
    "createdAt": "2026-04-11T10:30:00+08:00",
    "updatedAt": "2026-04-11T14:45:00+08:00"
  }
}
```

---

### 5.4 查询任务列表

**`GET /tasks`**  权限：`task:read`

**描述：** 分页查询任务列表。`BUSINESS_USER` 角色仅能查看自己提交的任务。

**Query Parameters：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|:---:|------|------|
| `page` | integer | ✗ | `1` | 页码 |
| `pageSize` | integer | ✗ | `20` | 每页条数（最大 100） |
| `status` | string | ✗ | — | 按状态筛选，多值逗号分隔 |
| `taskType` | string | ✗ | — | 任务类型 |
| `priority` | integer | ✗ | — | 优先级 |
| `dept` | string | ✗ | — | 部门 |
| `module` | string | ✗ | — | MES 模块 |
| `keyword` | string | ✗ | — | 关键词（标题、任务编号、提交人） |
| `dateFrom` | string | ✗ | — | 创建日期起（`yyyy-MM-dd`） |
| `dateTo` | string | ✗ | — | 创建日期止（`yyyy-MM-dd`） |
| `sortBy` | string | ✗ | `createdAt` | 排序字段 |
| `sortOrder` | string | ✗ | `desc` | `asc`/`desc` |

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 1024,
        "taskNo": "REQ-MES-AI-20260411-003",
        "title": "新增设备点检记录功能",
        "taskType": "FEAT",
        "priority": 2,
        "status": "AI_RUNNING",
        "dept": "生产技术部",
        "module": "设备管理",
        "submitterName": "李工",
        "estimatedHours": 6.0,
        "progressPct": 65,
        "createdAt": "2026-04-11T10:30:00+08:00",
        "updatedAt": "2026-04-11T14:45:00+08:00"
      }
    ],
    "pagination": {
      "page": 1, "pageSize": 20, "total": 47, "totalPages": 3
    }
  }
}
```

---

### 5.5 导出任务列表（Excel）

**`GET /tasks/export`**  权限：`task:export`

**描述：** 按筛选条件将任务列表导出为 Excel 文件（同步导出，上限 5000 条）。筛选参数与 5.4 节列表接口完全一致，不含分页参数（全量导出）。

**Query Parameters：** 同 5.4 节（去除 `page`/`pageSize`/`sortBy`/`sortOrder`，其余参数相同）

**Request Headers：**

```
Authorization: Bearer <token>
Accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
```

**Response 200（文件流）：**

```
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename*=UTF-8''tasks_export_20260411_103000.xlsx
Content-Length: 48320
```

**Excel 文件结构：**

| 列名 | 对应字段 | 说明 |
|------|--------|------|
| 任务编号 | `taskNo` | REQ-MES-AI-... |
| 需求标题 | `title` | — |
| 任务类型 | `taskType` | 中文映射：FEAT→新功能 等 |
| 优先级 | `priority` | 中文映射：1→紧急 等 |
| 当前状态 | `status` | 中文映射 |
| 所属部门 | `dept` | — |
| 所属模块 | `module` | — |
| 提交人 | `submitterName` | — |
| 预估工时(h) | `estimatedHours` | — |
| 实际工时(h) | `actualHours` | — |
| 质量评分 | `qualityScore` | — |
| 创建时间 | `createdAt` | `yyyy-MM-dd HH:mm:ss` |
| 完成时间 | `updatedAt` | 仅 CLOSED/ROLLBACK 状态有意义 |

**可能的错误码：** `20005`（权限不足）、`30007`（无数据）、`30008`（超量限制）

---

### 5.6 更新需求单

**`PUT /tasks/{taskId}`**  权限：`task:write`

**描述：** 更新 `DRAFT` 或 `REJECTED` 状态的需求单，其他状态禁止修改（PATCH 语义，只更新传入的字段）。

**Request Body：** 同创建接口，字段均为选填。

**Response 200：** `{ "taskId": 1024, "updatedAt": "..." }`

**可能的错误码：** `10007`

---

### 5.7 验收任务

**`POST /tasks/{taskId}/accept`**  权限：`task:accept`

**Request Body：**

```json
{
  "result": "ACCEPTED",
  "criteriaResults": [
    { "condition": "点检记录可正常新增", "expected": "...", "result": "PASS" },
    { "condition": "历史记录可按设备号和时间范围查询", "expected": "...", "result": "PASS" }
  ],
  "issues": [],
  "remark": "功能符合需求，验收通过"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `result` | string | ✓ | `ACCEPTED`（通过）/ `REJECTED`（退回重做） |
| `criteriaResults` | array | ✗ | 验收条件结果，`result` 枚举 `PASS`/`FAIL`/`NA` |
| `issues` | array[string] | ✗ | 问题清单（退回时填写） |
| `remark` | string | ✗ | 备注 |

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "taskId": 1024,
    "fromStatus": "PENDING_REVIEW",
    "toStatus": "ACCEPTED",
    "acceptedAt": "2026-04-11T16:00:00+08:00"
  }
}
```

---

### 5.8 获取任务操作历史

**`GET /tasks/{taskId}/history`**  权限：`task:read`

**Response 200：** 分页列表，每项含 `operator`、`action`、`fromStatus`、`toStatus`、`remark`、`createdAt`。

---

### 5.9 AI 写入执行日志

**`POST /tasks/{taskId}/exec-logs`**  权限：`exec_log:write`

**描述：** AI Agent 在任务执行过程中写入每次模型调用的日志。服务端强制校验 `isDesensitized=true`，否则返回 `60001` 拒绝写入。

**Request Body：**

```json
{
  "callSeq": 3,
  "modelName": "claude-sonnet-4",
  "logType": "OUTPUT",
  "stage": "CODEGEN",
  "promptHash": "a3f2e1b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2",
  "promptTokens": 12500,
  "completionTokens": 3800,
  "totalTokens": 16300,
  "estimatedCostCny": 0.2445,
  "latencyMs": 8420,
  "content": "已生成 EquipmentCheckController.java，共 187 行。设备序列号已脱敏为 [DEVICE_SN_***]。",
  "isDesensitized": true
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `callSeq` | integer | ✓ | 本任务内调用序号（从 1 开始） |
| `modelName` | string | ✓ | 模型名称，如 `claude-sonnet-4` |
| `logType` | string | ✓ | `INFO`/`WARN`/`ERROR`/`OUTPUT` |
| `stage` | string | ✓ | `UNDERSTAND`/`PLAN`/`CODEGEN`/`TEST`/`REPORT` |
| `promptHash` | string | ✗ | Prompt SHA256（64位 hex） |
| `promptTokens` | integer | ✓ | Prompt Token 数 |
| `completionTokens` | integer | ✓ | Completion Token 数 |
| `totalTokens` | integer | ✓ | 合计 Token 数 |
| `estimatedCostCny` | number | ✗ | 预估费用（元），按模型单价实时计算 |
| `latencyMs` | integer | ✗ | 响应延迟（毫秒） |
| `content` | string | ✗ | 日志内容（**必须已脱敏**） |
| `isDesensitized` | boolean | ✓ | **必须为 true，否则返回 60001** |

**Response 200：** `{ "logId": 88001, "createdAt": "..." }`

**可能的错误码：** `60001` `60005` `60004`

---

### 5.10 AI 提交代码交付物

**`POST /tasks/{taskId}/artifacts`**  权限：`artifact:write`

**描述：** 提交代码文件元数据，服务端异步触发硬编码扫描（Gitleaks）和 SonarQube 检查。

**Request Body：**

```json
{
  "artifacts": [
    {
      "filePath": "src/main/java/com/xingtong/mes/controller/EquipmentCheckController.java",
      "fileType": "JAVA",
      "fileSizeBytes": 8240,
      "linesOfCode": 187,
      "gitCommitHash": "a1b2c3d4e5f6789012345678901234567890abcd",
      "gitBranch": "feature/REQ-MES-AI-20260411-003"
    }
  ]
}
```

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "submittedCount": 1,
    "artifactIds": [20011],
    "scanStatus": "PENDING",
    "message": "代码已提交，硬编码扫描和 SonarQube 检查将在 1-3 分钟内完成"
  }
}
```

---

### 5.11 获取代码交付物列表

**`GET /tasks/{taskId}/artifacts`**  权限：`task:read`

**Response 200：** 列表，每项含 `filePath`、`fileType`、`gitCommitHash`、`hasHardcode`、`sonarStatus`、`sonarCriticalCount`、`createdAt`。

---

### 5.12 提交测试报告

**`POST /tasks/{taskId}/test-reports`**  权限：`artifact:write`

**Request Body：**

```json
{
  "reportType": "UNIT",
  "testTool": "JUnit",
  "totalCases": 24,
  "passedCases": 24,
  "failedCases": 0,
  "coveragePct": 78.5,
  "p0DiffCount": 0,
  "p1DiffCount": 0,
  "reportSummary": "单元测试全部通过，覆盖率 78.5%，满足 ≥70% 要求",
  "reportDetailUrl": "/git/repos/mes-ai/reports/REQ-20260411-003-unit.html",
  "isPassed": true
}
```

**Response 200：** `{ "reportId": 30011, "isPassed": true, "createdAt": "..." }`

---

### 5.13 实时执行进展（WebSocket）

**`WebSocket: /ws/tasks/{taskId}/progress`**

**连接鉴权：** URL 携带 `?token=<accessToken>`

**服务端推送消息格式：**

```json
{
  "type": "PROGRESS_UPDATE",
  "taskId": 1024,
  "stage": "CODEGEN",
  "progressPct": 72,
  "message": "正在生成 EquipmentCheckController.java...",
  "timestamp": "2026-04-11T14:52:30+08:00"
}
```

| `type` 值 | 说明 |
|---------|------|
| `PROGRESS_UPDATE` | 阶段进度更新 |
| `STAGE_COMPLETE` | 某执行阶段完成 |
| `APPROVAL_REQUIRED` | 出现需要人工授权的节点，AI 已暂停 |
| `TASK_COMPLETE` | AI 执行完成，进入 PENDING_REVIEW |
| `TASK_FAILED` | 任务执行失败 |
| `LOG_LINE` | 实时日志行推送 |

---

## 六、评审与授权模块

### 6.1 IT 评审需求单

**`POST /reviews`**  权限：`task:review`

**Request Body：**

```json
{
  "taskId": 1024,
  "reviewResult": "APPROVED",
  "reviewOpinion": "需求描述清晰，验收标准明确，可分配 AI 执行",
  "estimatedHours": 6.0,
  "assignMode": "AUTO",
  "planStartTime": "2026-04-11T14:00:00+08:00"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `taskId` | integer | ✓ | 任务 ID |
| `reviewResult` | string | ✓ | `APPROVED`/`REJECTED`/`PENDING_INFO` |
| `reviewOpinion` | string | ✗ | 评审意见（REJECTED 时建议填写） |
| `estimatedHours` | number | ✗ | 预估工时 |
| `assignMode` | string | ✗ | `AUTO`/`MANUAL`，默认 `AUTO` |
| `planStartTime` | string | ✗ | 计划开始时间 |

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "reviewId": 4001,
    "taskId": 1024,
    "reviewResult": "APPROVED",
    "taskNewStatus": "APPROVED",
    "reviewTime": "2026-04-11T11:00:00+08:00"
  }
}
```

**可能的错误码：** `30002` `30004`

---

### 6.2 查询待评审任务列表

**`GET /reviews/pending`**  权限：`task:review`

**描述：** 查询所有 `SUBMITTED` 状态的待评审任务，按提交时间升序（先进先出）。支持同任务列表的筛选参数。

**Response 200：** 同任务列表格式，每项额外包含 `waitingHours`（等待评审时长，小时）。

---

### 6.3 查询授权网关列表

**`GET /approvals`**  权限：`approval:write`

**Query Parameters：** `status`、`gateType`、`taskId`、`page`、`pageSize`

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 88,
        "taskId": 1024,
        "taskNo": "REQ-MES-AI-20260411-003",
        "taskTitle": "新增设备点检记录功能",
        "gateType": "PLAN_CONFIRM",
        "gateTitle": "实现方案确认",
        "gateContent": "1. 新增 equipment_check 表（无需修改现有表）\n2. 修改 EquipmentService\n3. 新增前端页面 equipment-check.vue",
        "status": "PENDING",
        "expireAt": "2026-04-11T16:30:00+08:00",
        "createdAt": "2026-04-11T14:30:00+08:00"
      }
    ],
    "pagination": { "page": 1, "pageSize": 20, "total": 3, "totalPages": 1 }
  }
}
```

---

### 6.4 执行授权操作

**`POST /approvals/{gateId}/decide`**  权限：`approval:write`（DDL 变更类型需 `system:admin`）

**Request Body：**

```json
{
  "decision": "APPROVED",
  "remark": "方案合理，授权执行"
}
```

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "gateId": 88,
    "decision": "APPROVED",
    "approverName": "王工",
    "approvedAt": "2026-04-11T14:45:00+08:00"
  }
}
```

**可能的错误码：** `40001` `40002` `40004`

---

### 6.5 AI 创建授权请求

**`POST /approvals`**  权限：`exec_log:write`（AI_AGENT）

**描述：** AI Agent 在执行过程中遇到需要人工确认的节点时，主动创建授权请求并暂停执行。

**Request Body：**

```json
{
  "taskId": 1024,
  "gateType": "PLAN_CONFIRM",
  "gateTitle": "实现方案确认",
  "gateContent": "AI 已完成需求分析，请确认实现方案...",
  "expireMinutes": 120
}
```

| `gateType` | 建议 `expireMinutes` | 说明 |
|--------|------|------|
| `PLAN_CONFIRM` | 120 | 方案确认，2 小时超时 |
| `DDL_CHANGE` | 0（不超时） | DDL 变更，须人工明确批准 |
| `DEPLOY` | 0（不超时） | 部署上线，须人工明确批准 |
| `EMERGENCY` | 30 | 紧急修复，30 分钟内响应 |

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "gateId": 88,
    "status": "PENDING",
    "expireAt": "2026-04-11T16:30:00+08:00",
    "notifyMessage": "已通过企业微信机器人通知 IT 专员"
  }
}
```

---

## 七、部署管理模块

### 7.1 发起部署申请

**`POST /deployments`**  权限：`task:write`（IT_REVIEWER 及以上）

**Request Body：**

```json
{
  "taskId": 1024,
  "planDeployTime": "2026-04-12T02:00:00+08:00",
  "rollbackPlan": "回退方案：\n1. 执行 SQL: DROP TABLE IF EXISTS equipment_check;\n2. git revert a1b2c3d4\n3. systemctl restart mes-backend\n预计回退耗时：5 分钟",
  "remark": "低峰期凌晨 2 点部署"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `taskId` | integer | ✓ | 任务 ID（必须为 ACCEPTED 状态） |
| `planDeployTime` | string | ✓ | 计划部署时间（ISO 8601） |
| `rollbackPlan` | string | ✓ | 回退方案（**必填，不能为空**） |
| `remark` | string | ✗ | 备注 |

**Response 200：** `{ "deployId": 5001, "taskId": 1024, "status": "PENDING_APPROVAL", "createdAt": "..." }`

**可能的错误码：** `50001` `50002` `50003`

---

### 7.2 IT 负责人审批部署

**`POST /deployments/{deployId}/approve`**  权限：`deploy:approve`

**Request Body：** `{ "approveResult": "APPROVED", "remark": "..." }`

**Response 200：** `{ "deployId": 5001, "approveResult": "APPROVED", "taskNewStatus": "DEPLOYING", "approveTime": "..." }`

---

### 7.3 记录部署结果

**`POST /deployments/{deployId}/result`**  权限：`deploy:approve`

**Request Body：**

```json
{
  "deployResult": "SUCCESS",
  "actualDeployTime": "2026-04-12T02:05:00+08:00",
  "deployLog": "02:05 开始部署\n02:06:30 数据库脚本执行完成\n02:08 服务重启完成\n02:08:30 健康检查通过"
}
```

**Response 200：** `{ "deployId": 5001, "deployResult": "SUCCESS", "taskFinalStatus": "CLOSED" }`

---

### 7.4 查询部署记录

**`GET /deployments`**  权限：`task:read`

**Query Parameters：** `taskId`、`deployResult`、`dateFrom`、`dateTo`、`page`、`pageSize`

**Response 200：** 分页列表，每项含部署记录完整字段。

---

## 八、运维监控模块

### 8.1 获取巡检报告列表

**`GET /monitor/inspections`**  权限：`monitor:read`

**Query Parameters：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `overallStatus` | string | `NORMAL`/`WARNING`/`CRITICAL` |
| `dateFrom` | string | 巡检日期起（`yyyy-MM-dd`） |
| `dateTo` | string | 巡检日期止（`yyyy-MM-dd`） |
| `page` | integer | 页码 |
| `pageSize` | integer | 每页条数 |

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 7001,
        "reportNo": "INSP-MES-AI-20260411",
        "inspectDate": "2026-04-11",
        "overallStatus": "WARNING",
        "alertCount": 3,
        "criticalCount": 0,
        "slowSqlCount": 2,
        "diskUsagePct": 72.5,
        "memoryUsagePct": 68.3,
        "itConfirmStatus": "PENDING",
        "createdAt": "2026-04-11T07:28:00+08:00"
      }
    ],
    "pagination": { "page": 1, "pageSize": 20, "total": 30, "totalPages": 2 }
  }
}
```

---

### 8.2 导出巡检报告列表（Excel）

**`GET /monitor/inspections/export`**  权限：`monitor:export`

**描述：** 将巡检报告摘要列表导出为 Excel，供管理层定期汇报使用。筛选参数与 8.1 节相同（去除分页参数）。

**Query Parameters：** `overallStatus`、`dateFrom`（**建议**填写，否则默认近 30 天）、`dateTo`

**Request Headers：**

```
Authorization: Bearer <token>
Accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
```

**Response 200（文件流）：**

```
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename*=UTF-8''inspection_export_20260401_20260411.xlsx
```

**Excel 文件结构（Sheet 1：巡检汇总）：**

| 列名 | 说明 |
|------|------|
| 报告编号 | `reportNo` |
| 巡检日期 | `inspectDate` |
| 整体状态 | `overallStatus`（中文映射） |
| 告警总数 | `alertCount` |
| Critical 告警数 | `criticalCount` |
| 慢 SQL 数量 | `slowSqlCount` |
| 磁盘使用率(%) | `diskUsagePct` |
| 内存使用率(%) | `memoryUsagePct` |
| 数据库活跃连接 | `dbConnActive` |
| IT 确认状态 | `itConfirmStatus`（中文映射） |
| IT 确认人 | `itConfirmUser` |
| 报告生成时间 | `createdAt` |

**Excel 文件结构（Sheet 2：告警明细）：** 同期所有告警记录，含 `alertLevel`、`alertType`、`alertTitle`、`resolveStatus`。

**可能的错误码：** `20005`（权限不足）、`30007`（无数据）

---

### 8.3 获取巡检报告详情

**`GET /monitor/inspections/{inspectionId}`**  权限：`monitor:read`

**Response 200：** 返回巡检报告完整字段，包含 `reportContent`（完整 Markdown 正文）、`aiSuggestions`。

---

### 8.4 AI 提交巡检报告

**`POST /monitor/inspections`**  权限：`exec_log:write`（AI_AGENT）

**Request Body：**

```json
{
  "reportNo": "INSP-MES-AI-20260411",
  "inspectDate": "2026-04-11",
  "inspectStartTime": "2026-04-11T07:00:00+08:00",
  "inspectEndTime": "2026-04-11T07:28:00+08:00",
  "overallStatus": "WARNING",
  "alertCount": 3,
  "criticalCount": 0,
  "errorLogSummary": "发现 3 种 ERROR 日志，最高频次：NullPointerException in ReportService (12次)",
  "slowSqlCount": 2,
  "diskUsagePct": 72.5,
  "memoryUsagePct": 68.3,
  "dbConnActive": 45,
  "reportContent": "# 系统巡检日报\n\n日期：2026-04-11\n...",
  "aiSuggestions": "建议优化 ReportService 中的空指针处理逻辑；慢 SQL 已记录，建议添加复合索引"
}
```

**Response 200：** `{ "inspectionId": 7001, "reportNo": "INSP-MES-AI-20260411", "createdAt": "..." }`

---

### 8.5 IT 确认巡检报告

**`POST /monitor/inspections/{inspectionId}/confirm`**  权限：`monitor:read`（IT 角色）

**Request Body：** `{ "confirmStatus": "CONFIRMED", "remark": "已阅，已安排处理慢 SQL 问题" }`

**Response 200：** 返回确认时间和确认人信息。

---

### 8.6 查询告警记录

**`GET /monitor/alerts`**  权限：`monitor:read`

**Query Parameters：** `alertLevel`、`alertType`、`resolveStatus`、`inspectionId`、`dateFrom`、`dateTo`、`page`、`pageSize`

**Response 200：** 分页列表，每项含告警完整字段。

---

### 8.7 处理告警

**`PUT /monitor/alerts/{alertId}/resolve`**  权限：`monitor:read`（IT 角色）

**Request Body：** `{ "resolveStatus": "RESOLVED", "resolveRemark": "..." }`

---

### 8.8 AI 上报实时告警

**`POST /monitor/alerts`**  权限：`exec_log:write`（AI_AGENT）

**描述：** AI 发现 Critical 级异常时立即上报，不等待巡检报告生成。

**Request Body：**

```json
{
  "inspectionId": null,
  "alertType": "SERVICE_DOWN",
  "alertLevel": "CRITICAL",
  "alertTitle": "MES 后端服务不可达",
  "alertContent": "健康检查接口 /health 连续 3 次无响应，判定服务宕机",
  "metricName": "service_health",
  "metricValue": 0,
  "thresholdValue": 1,
  "notifyChannel": "WECHAT_BOT"
}
```

**Response 200：** `{ "alertId": 9001, "notifySent": true, "createdAt": "..." }`

---

## 九、知识库模块

### 9.1 获取文档列表

**`GET /knowledge/documents`**  权限：`task:read`

**Query Parameters：** `docType`、`module`、`vectorStatus`、`isActive`（默认 true）、`keyword`、`page`、`pageSize`

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 101,
        "docCode": "KB-DB-001",
        "docName": "MES 数据库数据字典 V2.3",
        "docType": "DB_SCHEMA",
        "module": null,
        "version": "2.3",
        "fileFormat": "PDF",
        "fileSizeBytes": 2048000,
        "chunkCount": 248,
        "syncedChunkCount": 248,
        "vectorStatus": "DONE",
        "lastVectorizedAt": "2026-04-10T23:00:00+08:00",
        "isActive": true,
        "createdBy": "zhangsan",
        "createdAt": "2026-04-01T10:00:00+08:00"
      }
    ],
    "pagination": { "page": 1, "pageSize": 20, "total": 18, "totalPages": 1 }
  }
}
```

---

### 9.2 上传知识文档（物理文件）

**`POST /knowledge/documents/upload`**  权限：`knowledge:upload`

**描述：** 上传物理文件到服务器并自动创建文档元数据记录，是 RAG 知识摄入流程的入口。上传后文件进入解析队列，解析完成后自动触发向量化。

> ⚠ **与 9.3 节的区别：** 本接口同时完成"物理文件存储 + 元数据创建"；9.3 节仅录入元数据（适用于文件已存在于内网文件服务器的场景）。

**Content-Type：** `multipart/form-data`

**Form Fields：**

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|:---:|------|
| `files` | File[] | ✓ | 上传的文件，最多 5 个，单文件 ≤ 50MB |
| `docType` | string | ✓ | 文档类型：`DB_SCHEMA`/`API`/`FLOW`/`DEVICE`/`HISTORY`/`CODE`/`STANDARD` |
| `module` | string | ✗ | 所属 MES 模块（如"工单管理"、"设备管理"） |
| `version` | string | ✗ | 文档版本号，默认 `"1.0"` |
| `autoVectorize` | boolean | ✗ | 上传后是否立即触发向量化，默认 `true` |
| `docCodePrefix` | string | ✗ | 文档编码前缀（如 `KB-API`），服务端自动追加序号，如不填则系统自动分配 |

**允许的文件格式：**

| 格式 | MIME Type | 说明 |
|------|--------|------|
| `.pdf` | `application/pdf` | 技术方案、标准文档（推荐） |
| `.md` | `text/markdown` | Markdown 格式文档（推荐，向量化效果最佳） |
| `.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | Word 文档 |
| `.xlsx` | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` | 数据字典、字段清单 |
| `.txt` | `text/plain` | 纯文本，如 SQL DDL 文件 |

**Request 示例（curl）：**

```bash
curl -X POST \
  https://ai-mes.xingtong.internal/api/v1/knowledge/documents/upload \
  -H "Authorization: Bearer <token>" \
  -F "files=@MES接口文档V3.1.pdf" \
  -F "files=@设备通讯协议说明.md" \
  -F "docType=API" \
  -F "module=设备管理" \
  -F "version=3.1" \
  -F "autoVectorize=true" \
  -F "docCodePrefix=KB-API"
```

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "uploadedCount": 2,
    "documents": [
      {
        "id": 102,
        "docCode": "KB-API-004",
        "docName": "MES接口文档V3.1",
        "docType": "API",
        "module": "设备管理",
        "version": "3.1",
        "fileFormat": "PDF",
        "fileSizeBytes": 1843200,
        "storedPath": "/internal-storage/knowledge/2026/04/KB-API-004.pdf",
        "vectorStatus": "PENDING",
        "parseStatus": "PENDING",
        "autoVectorize": true,
        "createdAt": "2026-04-11T10:00:00+08:00",
        "message": "文件已上传，正在解析，完成后将自动触发向量化"
      },
      {
        "id": 103,
        "docCode": "KB-API-005",
        "docName": "设备通讯协议说明",
        "docType": "API",
        "module": "设备管理",
        "version": "3.1",
        "fileFormat": "MD",
        "fileSizeBytes": 45600,
        "storedPath": "/internal-storage/knowledge/2026/04/KB-API-005.md",
        "vectorStatus": "PENDING",
        "parseStatus": "PARSING",
        "autoVectorize": true,
        "createdAt": "2026-04-11T10:00:00+08:00",
        "message": "文件已上传，解析中（MD 文件通常 30 秒内完成）"
      }
    ],
    "failedFiles": []
  }
}
```

**部分成功响应（某文件格式不支持）：**

```json
{
  "code": 0,
  "message": "部分文件上传成功",
  "data": {
    "uploadedCount": 1,
    "documents": [ { ... } ],
    "failedFiles": [
      {
        "filename": "系统架构图.pptx",
        "errorCode": 80001,
        "errorMessage": "不支持的文件格式：.pptx，仅允许 PDF/MD/DOCX/XLSX/TXT"
      }
    ]
  }
}
```

**文件处理状态流转：**

```
文件上传成功
      │
      ▼
parseStatus: PENDING
      │ 解析队列处理（提取文本、分块）
      ▼
parseStatus: PARSING
      │
   ┌──┴──┐
   ▼      ▼
DONE   FAILED（记录 parseError，可重新上传）
   │
   ▼（autoVectorize=true）
vectorStatus: PROCESSING
      │
   ┌──┴──┐
   ▼      ▼
 DONE   FAILED（各 chunk 独立记录 sync_status）
```

**可能的错误码：** `80001`（格式不支持）`80002`（文件过大）`80003`（文件数超限）`80004`（解析失败）`80006`（存储不可用）`20005`（权限不足）

---

### 9.3 新增知识文档（仅元数据）

**`POST /knowledge/documents`**  权限：`system:admin`

**描述：** 仅录入文档元数据，适用于文件已存在于内网文件服务器（sourcePath 已知）的场景。需后续手动触发向量化（见 9.5 节）。

**Request Body：**

```json
{
  "docCode": "KB-API-003",
  "docName": "MES WebAPI 接口文档 V3.0",
  "docType": "API",
  "module": null,
  "sourcePath": "/docs/api/mes-api-v3.0.pdf",
  "fileFormat": "PDF",
  "version": "3.0",
  "createdBy": "lisi"
}
```

**Response 200：** 返回创建的文档 ID、`docCode`，`vectorStatus` 初始为 `PENDING`。

---

### 9.4 更新文档版本（重新上传）

**`POST /knowledge/documents/{docId}/upload`**  权限：`knowledge:upload`

**描述：** 对已存在的文档进行版本更新，上传新版本文件，旧向量块将被自动标记失效并重建。

**Content-Type：** `multipart/form-data`

**Form Fields：**

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|:---:|------|
| `file` | File | ✓ | 新版本文件（单文件，格式限制同 9.2 节） |
| `version` | string | ✓ | 新版本号（如 `3.2`） |
| `changeNote` | string | ✗ | 版本变更说明 |

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "docId": 101,
    "docCode": "KB-DB-001",
    "newVersion": "3.2",
    "previousVersion": "2.3",
    "oldChunksInvalidated": 248,
    "vectorStatus": "PENDING",
    "message": "文件已上传，旧向量块已失效，正在重新向量化"
  }
}
```

---

### 9.5 触发文档向量化

**`POST /knowledge/documents/{docId}/vectorize`**  权限：`system:admin`

**描述：** 手动触发或重新触发文档向量化任务（异步执行）。

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "docId": 101,
    "vectorStatus": "PROCESSING",
    "estimatedMinutes": 5,
    "message": "向量化任务已加入队列，可通过 GET /knowledge/documents/101 查询进度"
  }
}
```

---

### 9.6 查询向量块同步状态

**`GET /knowledge/documents/{docId}/chunks`**  权限：`task:read`

**Query Parameters：** `syncStatus`（`PENDING`/`SYNCING`/`SUCCESS`/`FAILED`）、`page`、`pageSize`

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "docId": 101,
    "totalChunks": 248,
    "syncedChunks": 245,
    "failedChunks": 3,
    "list": [
      {
        "id": 20001,
        "chunkIndex": 0,
        "vectorId": "chroma-uuid-abc123",
        "tokenCount": 892,
        "syncStatus": "SUCCESS",
        "lastSyncAt": "2026-04-10T23:05:00+08:00",
        "lastSyncError": null,
        "syncRetryCount": 0,
        "hitCount": 47,
        "lastHitAt": "2026-04-11T14:52:00+08:00"
      },
      {
        "id": 20089,
        "chunkIndex": 88,
        "vectorId": null,
        "tokenCount": 756,
        "syncStatus": "FAILED",
        "lastSyncAt": "2026-04-10T23:18:00+08:00",
        "lastSyncError": "ChromaDB connection timeout after 30s",
        "syncRetryCount": 3,
        "hitCount": 0,
        "lastHitAt": null
      }
    ],
    "pagination": { "page": 1, "pageSize": 20, "total": 248, "totalPages": 13 }
  }
}
```

> ⚠ AI 检索服务在查询向量块时，内部必须包含 `WHERE sync_status = 'SUCCESS'` 条件，禁止命中未同步的块。

---

### 9.7 重试失败的向量块同步

**`POST /knowledge/documents/{docId}/chunks/retry-failed`**  权限：`system:admin`

**描述：** 批量重置 `syncRetryCount` 并重新触发所有 `FAILED` 状态块的同步。

**Response 200：** `{ "resetCount": 3, "message": "3 个失败块已重置，将在后台重新同步" }`

---

## 十、断言库模块

### 10.1 查询断言列表

**`GET /assertions`**  权限：`task:read`

**Query Parameters：** `category`、`priority`、`isActive`、`relatedModule`、`keyword`、`page`、`pageSize`

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "assertionId": "SM-WO-001",
        "assertionName": "工单状态流转核心断言",
        "category": "STATE_MACHINE",
        "priority": "CRITICAL",
        "relatedModule": "工单管理",
        "passThreshold": 0.90,
        "isActive": true,
        "createdBy": "techlead",
        "approvedBy": "techlead",
        "createdAt": "2026-04-01T10:00:00+08:00"
      }
    ],
    "pagination": { "page": 1, "pageSize": 20, "total": 24, "totalPages": 2 }
  }
}
```

---

### 10.2 获取断言详情

**`GET /assertions/{assertionDbId}`**  权限：`task:read`

**Response 200：** 返回断言完整字段，包含 `promptText`、`expectedKeywords`、`expectedExcludes`。

---

### 10.3 创建断言

**`POST /assertions`**  权限：`assertion:manage`

**Request Body：**

```json
{
  "assertionId": "SM-EQ-001",
  "assertionName": "设备点检状态流转断言",
  "category": "STATE_MACHINE",
  "priority": "HIGH",
  "description": "验证设备点检记录的状态流转：正常/异常/待复查，异常状态必须触发告警",
  "promptText": "在山东芯通 MES 系统中，一条设备点检记录当前状态为"异常"。请说明：(1)允许流转的下一个状态；(2)是否必须触发告警通知；(3)如何关闭异常状态。",
  "expectedKeywords": ["告警", "通知", "待复查", "关闭"],
  "expectedExcludes": ["直接关闭", "跳过告警"],
  "scoringMethod": "keyword_match",
  "passThreshold": 0.90,
  "relatedModule": "设备管理"
}
```

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 25,
    "assertionId": "SM-EQ-001",
    "createdAt": "2026-04-11T10:00:00+08:00",
    "approvalRequired": true,
    "message": "断言已创建，需技术负责人审批后生效"
  }
}
```

---

### 10.4 手动触发断言批次测试

**`POST /assertions/batches`**  权限：`assertion:manage`

**Request Body：**

```json
{
  "triggerType": "PROMPT_CHANGE",
  "triggerSource": "prompts/backend/work-order.md 修改，commit: a1b2c3d4",
  "relatedTaskId": 1024,
  "relatedCommitHash": "a1b2c3d4e5f6789012345678901234567890abcd",
  "modelName": "claude-sonnet-4",
  "priorityFilter": null
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `triggerType` | string | ✓ | `MODEL_UPGRADE`/`PROMPT_CHANGE`/`SCHEDULED` |
| `triggerSource` | string | ✗ | 触发来源描述 |
| `relatedTaskId` | integer | ✗ | 关联任务 ID（`PROMPT_CHANGE` 类型必填） |
| `relatedCommitHash` | string | ✗ | 关联 Commit Hash（40 位），实现版本联动追溯 |
| `modelName` | string | ✓ | 测试使用的模型 |
| `priorityFilter` | string | ✗ | `CRITICAL`/`HIGH`/`MEDIUM`，null 表示全量 |

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "runBatchId": "RUN-20260411-1045",
    "status": "RUNNING",
    "totalAssertions": 24,
    "estimatedMinutes": 8,
    "message": "断言批次测试已启动，通过 GET /assertions/batches/RUN-20260411-1045 查询进度"
  }
}
```

**可能的错误码：** `70003`

---

### 10.5 查询断言批次列表

**`GET /assertions/batches`**  权限：`task:read`

**Query Parameters：** `triggerType`、`blockAction`、`relatedTaskId`、`relatedCommitHash`、`dateFrom`、`dateTo`、`page`、`pageSize`

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 301,
        "runBatchId": "RUN-20260411-1045",
        "triggerType": "PROMPT_CHANGE",
        "triggerSource": "prompts/backend/work-order.md",
        "relatedTaskId": 1024,
        "relatedCommitHash": "a1b2c3d4e5f6789012345678901234567890abcd",
        "modelName": "claude-sonnet-4",
        "totalCount": 24,
        "passedCount": 24,
        "criticalFailed": 0,
        "highFailed": 0,
        "mediumFailed": 0,
        "passRatePct": 100.0,
        "blockAction": "PASSED",
        "createdAt": "2026-04-11T10:45:00+08:00",
        "finishedAt": "2026-04-11T10:53:00+08:00"
      }
    ],
    "pagination": { "page": 1, "pageSize": 20, "total": 45, "totalPages": 3 }
  }
}
```

---

### 10.6 查询断言批次执行详情

**`GET /assertions/batches/{runBatchId}`**  权限：`task:read`

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "batch": {
      "runBatchId": "RUN-20260411-1045",
      "triggerType": "PROMPT_CHANGE",
      "blockAction": "PASSED",
      "passRatePct": 100.0,
      "totalCount": 24,
      "passedCount": 24,
      "criticalFailed": 0
    },
    "runs": [
      {
        "id": 10001,
        "assertionId": "SM-WO-001",
        "assertionName": "工单状态流转核心断言",
        "priority": "CRITICAL",
        "isPassed": true,
        "keywordHitRate": 1.0,
        "excludeViolation": false,
        "score": 1.0,
        "latencyMs": 2340,
        "tokensUsed": 850,
        "createdAt": "2026-04-11T10:45:30+08:00"
      }
    ]
  }
}
```

---

## 十一、成本统计模块

### 11.1 查询 Token 日消耗汇总

**`GET /cost/daily`**  权限：`cost:read`

**Query Parameters：** `dateFrom`、`dateTo`、`modelName`

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [
      {
        "statDate": "2026-04-11",
        "modelName": "claude-sonnet-4",
        "totalCalls": 342,
        "promptTokens": 4250000,
        "completionTokens": 1120000,
        "totalTokens": 5370000,
        "budgetLimit": 3000000,
        "alertTriggered": true,
        "totalCostCny": 80.55,
        "budgetUsagePct": 179.0
      }
    ]
  }
}
```

---

### 11.2 导出 Token 日消耗（Excel）

**`GET /cost/daily/export`**  权限：`cost:export`

**描述：** 将 Token 日消耗数据导出为 Excel，供财务和管理层核对费用。

**Query Parameters：** `dateFrom`（必填）、`dateTo`（必填）、`modelName`

**Request Headers：** `Accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

**Response 200（文件流）：**

```
Content-Disposition: attachment; filename*=UTF-8''token_daily_20260401_20260411.xlsx
```

**Excel 文件结构（Sheet 1：日消耗明细）：**

| 列名 | 说明 |
|------|------|
| 统计日期 | `statDate` |
| 模型名称 | `modelName` |
| 调用次数 | `totalCalls` |
| Prompt Token 数 | `promptTokens` |
| Completion Token 数 | `completionTokens` |
| 合计 Token 数 | `totalTokens` |
| 预算上限 | `budgetLimit` |
| 预算使用率(%) | `budgetUsagePct` |
| 是否触发告警 | `alertTriggered`（是/否） |
| 实际费用(元) | `totalCostCny` |

**Excel 文件结构（Sheet 2：统计汇总）：** 区间内按模型汇总合计行。

---

### 11.3 查询多维度 Token 成本统计（ROI 报告）

**`GET /cost/stat`**  权限：`cost:read`

**描述：** 按部门、模块、任务类型、模型多维度汇总的 ROI 分析（对应数据库 `ai_token_stat` 表）。

**Query Parameters：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `month` | string | ✓ | 统计月份，格式 `yyyy-MM` |
| `groupBy` | string | ✓ | 汇总维度：`dept`/`module`/`taskType`/`model` |
| `dept` | string | ✗ | 筛选特定部门（`groupBy=dept` 时忽略） |
| `module` | string | ✗ | 筛选特定模块 |
| `taskType` | string | ✗ | 筛选任务类型 |
| `modelName` | string | ✗ | 筛选模型 |

**Response 200（`groupBy=dept` 示例）：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "month": "2026-04",
    "groupBy": "dept",
    "summary": {
      "totalCostCny": 1240.80,
      "totalTokens": 82700000,
      "totalTasks": 38,
      "avgCostPerTask": 32.65
    },
    "items": [
      {
        "dimension": "生产技术部",
        "totalCalls": 1820,
        "totalTokens": 38500000,
        "totalCostCny": 577.50,
        "taskCount": 18,
        "avgCostPerTask": 32.08,
        "costPct": 46.5
      },
      {
        "dimension": "质量管理部",
        "totalCalls": 960,
        "totalTokens": 22400000,
        "totalCostCny": 336.00,
        "taskCount": 10,
        "avgCostPerTask": 33.60,
        "costPct": 27.1
      },
      {
        "dimension": "IT部",
        "totalCalls": 540,
        "totalTokens": 11800000,
        "totalCostCny": 177.00,
        "taskCount": 6,
        "avgCostPerTask": 29.50,
        "costPct": 14.3
      }
    ]
  }
}
```

---

### 11.4 导出多维度成本统计（Excel）

**`GET /cost/stat/export`**  权限：`cost:export`

**描述：** 将多维度成本统计数据导出为专业 Excel 报表，供管理层月度汇报使用。筛选参数与 11.3 节完全一致。

**Query Parameters：** 同 11.3 节（`month` 必填，`groupBy` 必填）

**Request Headers：** `Accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

**Response 200（文件流）：**

```
Content-Disposition: attachment; filename*=UTF-8''cost_stat_2026-04_dept_20260411.xlsx
```

**Excel 文件结构（多 Sheet 设计）：**

**Sheet 1 — 费用汇总（`groupBy` 维度）：**

| 列名 | 说明 |
|------|------|
| 维度名称 | 如"生产技术部"、"设备管理" |
| API 调用次数 | `totalCalls` |
| Token 总量 | `totalTokens` |
| 费用（元） | `totalCostCny` |
| 任务数量 | `taskCount` |
| 单任务平均费用（元） | `avgCostPerTask` |
| 费用占比(%) | `costPct` |

**Sheet 2 — 每日明细：** 该月每天的按维度消耗明细（来自 `ai_token_stat` 按日聚合）。

**Sheet 3 — 摘要对比：** 与上月同维度数据对比（环比变化），包含：本月费用、上月费用、环比变化率。

**文件末行：** 汇总合计行（字体加粗）。

**可能的错误码：** `20005`（权限不足）、`30007`（无数据，如该月无任何 Token 消耗）

---

### 11.5 获取月度 ROI 摘要报告

**`GET /cost/roi-summary`**  权限：`cost:read`

**描述：** 专为管理层汇报设计的月度 ROI 摘要，对比 AI 投入成本与等效人工成本。

**Query Parameters：** `month`（`yyyy-MM`，必填）

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "month": "2026-04",
    "aiCostSummary": {
      "contractFee": 8000.00,
      "tokenCostCny": 1240.80,
      "totalActualCost": 9240.80
    },
    "outputSummary": {
      "totalTasks": 38,
      "closedTasks": 32,
      "totalCodeLines": 14820,
      "totalTestCases": 386,
      "avgTaskQualityScore": 87.5,
      "onePassAcceptRate": 89.5
    },
    "comparisonSummary": {
      "equivalentManHours": 228.5,
      "humanCostEquivalent": 28562.50,
      "savingsEstimate": 19321.70,
      "roiMultiple": 3.09
    },
    "assertionSummary": {
      "totalBatches": 28,
      "criticalPassRate": 100.0,
      "overallPassRate": 97.8,
      "blockedCount": 0
    }
  }
}
```

---

## 十二、系统管理模块

### 12.1 健康检查

**`GET /system/health`**  权限：公开（无需 Token）

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "status": "UP",
    "timestamp": "2026-04-11T10:30:00+08:00",
    "components": {
      "database":  { "status": "UP",   "latencyMs": 12  },
      "redis":     { "status": "UP",   "latencyMs": 3   },
      "aiGateway": { "status": "UP",   "latencyMs": 245 },
      "vectorDb":  { "status": "UP",   "latencyMs": 18  },
      "fileStorage":{ "status": "UP",  "latencyMs": 5   }
    },
    "version": "1.1.0",
    "buildTime": "2026-04-11T08:00:00+08:00"
  }
}
```

---

### 12.2 查询用户列表

**`GET /system/users`**  权限：`system:admin`

**Query Parameters：** `role`、`dept`、`isActive`、`keyword`、`page`、`pageSize`

**Response 200：** 用户分页列表，不返回密码字段。

---

### 12.3 创建用户

**`POST /system/users`**  权限：`system:admin`

**Request Body：**

```json
{
  "username": "zhaoliu",
  "realName": "赵六",
  "password": "Xingtong@2026",
  "role": "IT_REVIEWER",
  "dept": "IT部",
  "email": "zhaoliu@xingtong.com"
}
```

**Response 200：** 返回新建用户 ID，不返回密码。

---

### 12.4 吊销 Token

**`POST /system/auth/revoke`**  权限：用户本人或 `system:admin`

**Request Body：** `{ "token": "eyJhbGci..." }`

---

### 12.5 查询系统配置

**`GET /system/configs`**  权限：`system:admin`

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "tokenBudgetDailyLimit": 3000000,
    "modelPrices": {
      "claude-sonnet-4": {
        "promptPricePerMToken": 9.00,
        "completionPricePerMToken": 45.00,
        "currency": "CNY"
      }
    },
    "alertThresholds": {
      "diskUsagePct": 80,
      "memoryUsagePct": 85,
      "slowSqlMs": 2000
    },
    "approvalExpireMinutes": {
      "PLAN_CONFIRM": 120,
      "DDL_CHANGE": 0,
      "DEPLOY": 0,
      "EMERGENCY": 30
    },
    "fileUpload": {
      "maxFileSizeMb": 50,
      "maxFilesPerRequest": 5,
      "allowedExtensions": [".pdf", ".md", ".docx", ".xlsx", ".txt"]
    }
  }
}
```

---

### 12.6 更新系统配置

**`PUT /system/configs`**  权限：`system:admin`

**Request Body：** 与查询响应的 `data` 字段结构相同，支持部分更新。

---

### 12.7 查询导出任务状态（异步导出预留）

**`GET /system/export-jobs/{jobId}`**  权限：对应模块的 export 权限

**描述：** 当前版本全部采用同步导出，本接口预留，未来数据量增大后异步导出时使用。

**Response 200：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "jobId": "export-job-xxxx",
    "status": "COMPLETED",
    "downloadUrl": "/api/v1/system/export-jobs/export-job-xxxx/download",
    "expiresAt": "2026-04-11T11:30:00+08:00",
    "fileSizeBytes": 48320
  }
}
```

---

## 十三、导出接口规范（Export）

> 本章对所有导出接口进行统一说明，是第三章"通用约定"中导出规范的完整展开。

### 13.1 导出接口汇总

| 接口 | 路径 | 权限 | 说明 |
|------|------|------|------|
| 任务列表导出 | `GET /tasks/export` | `task:export` | 任务全列表，支持同 5.4 节筛选参数 |
| Token 日报导出 | `GET /cost/daily/export` | `cost:export` | Token 日消耗，dateFrom/dateTo 必填 |
| 成本统计导出 | `GET /cost/stat/export` | `cost:export` | 多维度 ROI 报表，month/groupBy 必填 |
| 巡检报告导出 | `GET /monitor/inspections/export` | `monitor:export` | 巡检汇总 + 告警明细 |
| 知识文档列表导出 | `GET /knowledge/documents/export` | `task:read` | 文档清单及向量化状态 |

### 13.2 知识文档列表导出

**`GET /knowledge/documents/export`**  权限：`task:read`

**描述：** 导出知识库文档清单，用于文档管理和向量化状态审查。

**Query Parameters：** `docType`、`module`、`vectorStatus`、`isActive`

**Response 200（文件流）：**

```
Content-Disposition: attachment; filename*=UTF-8''knowledge_docs_20260411.xlsx
```

**Excel 文件结构：**

| 列名 | 说明 |
|------|------|
| 文档编码 | `docCode` |
| 文档名称 | `docName` |
| 文档类型 | `docType`（中文映射） |
| 所属模块 | `module` |
| 文件格式 | `fileFormat` |
| 版本号 | `version` |
| 向量块总数 | `chunkCount` |
| 已同步块数 | `syncedChunkCount` |
| 向量化状态 | `vectorStatus`（中文映射） |
| 最近向量化时间 | `lastVectorizedAt` |
| 是否启用 | `isActive`（是/否） |
| 创建人 | `createdBy` |
| 录入时间 | `createdAt` |

### 13.3 导出接口通用参数说明

所有导出接口共享以下行为规范：

**1. Token 传递方式（二选一）：**

```
# 方式 A：Header（推荐，适用于 fetch/axios 调用）
Authorization: Bearer <accessToken>
Accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet

# 方式 B：URL 参数（适用于浏览器 <a href> 直链下载）
GET /cost/stat/export?month=2026-04&groupBy=dept&token=<downloadToken>
（downloadToken 通过 POST /system/auth/download-token 换取，有效期 5 分钟）
```

**2. 超大数据集保护：**

服务端在执行查询前先进行 COUNT 预检，若预估行数 > 5000，返回：

```json
{
  "code": 30008,
  "message": "导出数据量超过上限（预估 12840 行 > 5000 行），请缩小时间范围或筛选条件",
  "data": {
    "estimatedRows": 12840,
    "maxAllowed": 5000,
    "suggestion": "建议将导出范围缩小到 30 天以内，或通过 groupBy 减少明细行数"
  }
}
```

**3. 空数据保护：**

若筛选后数据为空，返回：

```json
{
  "code": 30007,
  "message": "导出范围内无数据，请调整筛选条件",
  "data": null
}
```

**4. Excel 格式规范（全部导出接口统一）：**

| 规范项 | 要求 |
|--------|------|
| 工作簿格式 | `.xlsx`（Office Open XML） |
| 首行冻结 | 所有 Sheet 的表头行冻结 |
| 表头样式 | 背景色 `#D6E4F0`，字体加粗，居中对齐 |
| 日期时间列 | 格式化为 `yyyy-MM-dd HH:mm:ss` |
| 数值列 | 保留 2 位小数，千分位分隔符 |
| 状态字段 | 映射为中文（如 `AI_RUNNING` → `AI执行中`） |
| 布尔字段 | 映射为 `是`/`否` |
| 文件生成时间 | 在最后一个 Sheet 末行标注"导出时间：yyyy-MM-dd HH:mm:ss" |
| 最大列宽 | 自动适应内容，上限 50 个字符宽度 |

---

## 十四、Schema 定义（Components）

```yaml
components:
  schemas:

    # ── 通用响应 ────────────────────────────────────────────────
    ResultVO:
      type: object
      properties:
        code:
          type: integer
          example: 0
          description: 业务状态码，0 为成功
        message:
          type: string
          example: "success"
        data:
          nullable: true
        timestamp:
          type: string
          format: date-time
          example: "2026-04-11T10:30:00+08:00"
        requestId:
          type: string
          example: "req-a1b2c3d4"

    Pagination:
      type: object
      properties:
        page:
          type: integer
          minimum: 1
        pageSize:
          type: integer
          minimum: 1
          maximum: 100
        total:
          type: integer
        totalPages:
          type: integer

    # ── 任务相关 ─────────────────────────────────────────────────
    AcceptCriterion:
      type: object
      required: [condition, expected]
      properties:
        condition:
          type: string
          description: 验收条件描述
        expected:
          type: string
          description: 期望的结果
        result:
          type: string
          nullable: true
          enum: [PASS, FAIL, NA, null]
          description: 验收实际结果（创建时为 null，验收时填写）

    TaskStatus:
      type: string
      enum:
        - DRAFT          # 草稿
        - SUBMITTED      # 已提交，等待 IT 评审
        - REVIEWING      # IT 评审中
        - APPROVED       # IT 批准，等待 AI 执行
        - REJECTED       # IT 退回
        - AI_RUNNING     # AI 执行中
        - PENDING_REVIEW # AI 完成，等待甲方验收
        - FAILED         # AI 执行失败
        - ACCEPTED       # 甲方验收通过
        - DEPLOYING      # 部署审批和执行中
        - CLOSED         # 已完成上线
        - ROLLBACK       # 部署失败已回退

    TaskType:
      type: string
      enum: [FEAT, FIX, REPORT, QUERY, API, BUG, PERF]

    TaskSummary:
      type: object
      properties:
        id:
          type: integer
          format: int64
        taskNo:
          type: string
          example: "REQ-MES-AI-20260411-003"
        title:
          type: string
        taskType:
          $ref: '#/components/schemas/TaskType'
        priority:
          type: integer
          minimum: 1
          maximum: 4
        status:
          $ref: '#/components/schemas/TaskStatus'
        dept:
          type: string
        module:
          type: string
          nullable: true
        submitterName:
          type: string
        estimatedHours:
          type: number
          nullable: true
        progressPct:
          type: integer
          nullable: true
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time

    ExecutionStage:
      type: object
      properties:
        stage:
          type: string
          enum: [UNDERSTAND, PLAN, CODEGEN, TEST, REPORT]
        status:
          type: string
          enum: [PENDING, RUNNING, DONE, FAILED]
        completedAt:
          type: string
          format: date-time
          nullable: true

    # ── 授权网关 ─────────────────────────────────────────────────
    GateType:
      type: string
      enum: [PLAN_CONFIRM, DDL_CHANGE, DEPLOY, EMERGENCY]

    ApprovalStatus:
      type: string
      enum: [PENDING, APPROVED, REJECTED, TIMEOUT]

    ApprovalGate:
      type: object
      properties:
        id:
          type: integer
          format: int64
        taskId:
          type: integer
          format: int64
        taskNo:
          type: string
        gateType:
          $ref: '#/components/schemas/GateType'
        gateTitle:
          type: string
        gateContent:
          type: string
          nullable: true
        status:
          $ref: '#/components/schemas/ApprovalStatus'
        approverName:
          type: string
          nullable: true
        expireAt:
          type: string
          format: date-time
        approvedAt:
          type: string
          format: date-time
          nullable: true
        createdAt:
          type: string
          format: date-time

    # ── 执行日志 ─────────────────────────────────────────────────
    ExecLogCreateRequest:
      type: object
      required: [callSeq, modelName, logType, stage, promptTokens, completionTokens, totalTokens, isDesensitized]
      properties:
        callSeq:
          type: integer
          minimum: 1
        modelName:
          type: string
        logType:
          type: string
          enum: [INFO, WARN, ERROR, OUTPUT]
        stage:
          type: string
          enum: [UNDERSTAND, PLAN, CODEGEN, TEST, REPORT]
        promptHash:
          type: string
          pattern: '^[a-f0-9]{64}$'
          nullable: true
        promptTokens:
          type: integer
          minimum: 0
        completionTokens:
          type: integer
          minimum: 0
        totalTokens:
          type: integer
          minimum: 0
        estimatedCostCny:
          type: number
          nullable: true
        latencyMs:
          type: integer
          nullable: true
        content:
          type: string
          nullable: true
          description: 日志内容，必须已完成脱敏处理
        isDesensitized:
          type: boolean
          description: "必须为 true，否则服务端返回 60001"

    # ── 代码交付物 ───────────────────────────────────────────────
    CodeArtifactItem:
      type: object
      required: [filePath, fileType]
      properties:
        filePath:
          type: string
          maxLength: 500
        fileType:
          type: string
          enum: [JAVA, VUE, SQL, XML, MD, TEST]
        fileSizeBytes:
          type: integer
          nullable: true
        linesOfCode:
          type: integer
          nullable: true
        gitCommitHash:
          type: string
          pattern: '^[a-f0-9]{40}$'
          nullable: true
        gitBranch:
          type: string
          nullable: true

    # ── 知识库 ───────────────────────────────────────────────────
    DocType:
      type: string
      enum: [DB_SCHEMA, API, FLOW, DEVICE, HISTORY, CODE, STANDARD]

    VectorStatus:
      type: string
      enum: [PENDING, PROCESSING, DONE, PARTIAL, FAILED]

    SyncStatus:
      type: string
      enum: [PENDING, SYNCING, SUCCESS, FAILED]

    KnowledgeDocumentUploadResponse:
      type: object
      properties:
        id:
          type: integer
          format: int64
        docCode:
          type: string
        docName:
          type: string
        docType:
          $ref: '#/components/schemas/DocType'
        module:
          type: string
          nullable: true
        version:
          type: string
        fileFormat:
          type: string
        fileSizeBytes:
          type: integer
        storedPath:
          type: string
          description: 内网文件服务器存储路径（仅供内部管理使用）
        vectorStatus:
          $ref: '#/components/schemas/VectorStatus'
        parseStatus:
          type: string
          enum: [PENDING, PARSING, DONE, FAILED]
        autoVectorize:
          type: boolean
        createdAt:
          type: string
          format: date-time
        message:
          type: string

    FailedFileItem:
      type: object
      properties:
        filename:
          type: string
        errorCode:
          type: integer
        errorMessage:
          type: string

    # ── 监控 ─────────────────────────────────────────────────────
    AlertLevel:
      type: string
      enum: [CRITICAL, HIGH, MEDIUM, LOW]

    AlertType:
      type: string
      enum: [DISK, MEMORY, SERVICE_DOWN, SLOW_SQL, ERROR_LOG, API_FAIL]

    AlertResolveStatus:
      type: string
      enum: [OPEN, PROCESSING, RESOLVED, IGNORED]

    # ── 断言 ─────────────────────────────────────────────────────
    AssertionPriority:
      type: string
      enum: [CRITICAL, HIGH, MEDIUM]

    AssertionCategory:
      type: string
      enum: [STATE_MACHINE, SQL_LOGIC, API_BEHAVIOR, CODE_GEN]

    AssertionCreateRequest:
      type: object
      required: [assertionId, assertionName, category, priority, description, promptText, expectedKeywords]
      properties:
        assertionId:
          type: string
          pattern: '^[A-Z]{2}-[A-Z]{2}-\d{3}$'
          example: "SM-EQ-001"
          description: 断言编号，格式 XX-XX-NNN（如 SM-WO-001）
        assertionName:
          type: string
          maxLength: 200
        category:
          $ref: '#/components/schemas/AssertionCategory'
        priority:
          $ref: '#/components/schemas/AssertionPriority'
        description:
          type: string
        promptText:
          type: string
        expectedKeywords:
          type: array
          items:
            type: string
          minItems: 1
        expectedExcludes:
          type: array
          items:
            type: string
          nullable: true
        scoringMethod:
          type: string
          enum: [keyword_match, llm_judge]
          default: keyword_match
        passThreshold:
          type: number
          minimum: 0.0
          maximum: 1.0
          default: 0.90
        relatedModule:
          type: string
          nullable: true

    # ── 成本统计 ─────────────────────────────────────────────────
    CostStatItem:
      type: object
      properties:
        dimension:
          type: string
          description: 聚合维度值（部门名/模块名/任务类型/模型名）
        totalCalls:
          type: integer
        totalTokens:
          type: integer
          format: int64
        totalCostCny:
          type: number
          format: double
        taskCount:
          type: integer
        avgCostPerTask:
          type: number
          format: double
        costPct:
          type: number
          format: double
          description: 占总费用百分比

    # ── 错误响应 ─────────────────────────────────────────────────
    ErrorResponse:
      type: object
      properties:
        code:
          type: integer
          example: 30001
        message:
          type: string
          example: "任务状态流转非法：DRAFT → ACCEPTED"
        data:
          nullable: true
          example: null
        timestamp:
          type: string
          format: date-time
        requestId:
          type: string
```

---

## 十五、附录

### 附录 A：接口清单总览（共 55 个端点）

| 序号 | 方法 | 路径 | 说明 | 权限 | V1.1 |
|------|------|------|------|------|:---:|
| 1 | POST | `/system/auth/login` | 登录获取 Token | 公开 | |
| 2 | POST | `/system/auth/refresh` | 刷新 Token | 公开 | |
| 3 | POST | `/system/auth/revoke` | 吊销 Token | 本人/admin | |
| 4 | POST | `/system/auth/download-token` | 获取文件下载一次性 Token | export 权限 | ★ |
| 5 | GET | `/system/health` | 健康检查 | 公开 | |
| 6 | GET | `/system/users` | 用户列表 | system:admin | |
| 7 | POST | `/system/users` | 创建用户 | system:admin | |
| 8 | GET | `/system/configs` | 查询系统配置 | system:admin | |
| 9 | PUT | `/system/configs` | 更新系统配置 | system:admin | |
| 10 | GET | `/system/export-jobs/{jobId}` | 异步导出任务状态（预留） | export 权限 | ★ |
| 11 | POST | `/tasks` | 创建需求单 | task:write | |
| 12 | POST | `/tasks/{taskId}/submit` | 提交需求单 | task:write | |
| 13 | GET | `/tasks/{taskId}` | 获取任务详情 | task:read | |
| 14 | GET | `/tasks` | 查询任务列表 | task:read | |
| 15 | **GET** | **`/tasks/export`** | **任务列表 Excel 导出** | task:export | **★新增** |
| 16 | PUT | `/tasks/{taskId}` | 更新需求单 | task:write | |
| 17 | POST | `/tasks/{taskId}/accept` | 验收任务 | task:accept | |
| 18 | GET | `/tasks/{taskId}/history` | 操作历史 | task:read | |
| 19 | POST | `/tasks/{taskId}/exec-logs` | AI 写入执行日志 | exec_log:write | |
| 20 | POST | `/tasks/{taskId}/artifacts` | AI 提交代码交付物 | artifact:write | |
| 21 | GET | `/tasks/{taskId}/artifacts` | 获取代码交付物列表 | task:read | |
| 22 | POST | `/tasks/{taskId}/test-reports` | 提交测试报告 | artifact:write | |
| 23 | WS | `/ws/tasks/{taskId}/progress` | 实时执行进展推送 | task:read | |
| 24 | POST | `/reviews` | IT 评审需求单 | task:review | |
| 25 | GET | `/reviews/pending` | 待评审任务列表 | task:review | |
| 26 | GET | `/approvals` | 授权网关列表 | approval:write | |
| 27 | POST | `/approvals` | AI 创建授权请求 | exec_log:write | |
| 28 | POST | `/approvals/{gateId}/decide` | 执行授权操作 | approval:write | |
| 29 | POST | `/deployments` | 发起部署申请 | task:write | |
| 30 | POST | `/deployments/{deployId}/approve` | IT 审批部署 | deploy:approve | |
| 31 | POST | `/deployments/{deployId}/result` | 记录部署结果 | deploy:approve | |
| 32 | GET | `/deployments` | 查询部署记录 | task:read | |
| 33 | GET | `/monitor/inspections` | 巡检报告列表 | monitor:read | |
| 34 | **GET** | **`/monitor/inspections/export`** | **巡检报告 Excel 导出** | monitor:export | **★新增** |
| 35 | GET | `/monitor/inspections/{id}` | 巡检报告详情 | monitor:read | |
| 36 | POST | `/monitor/inspections` | AI 提交巡检报告 | exec_log:write | |
| 37 | POST | `/monitor/inspections/{id}/confirm` | IT 确认巡检报告 | monitor:read | |
| 38 | GET | `/monitor/alerts` | 查询告警记录 | monitor:read | |
| 39 | PUT | `/monitor/alerts/{id}/resolve` | 处理告警 | monitor:read | |
| 40 | POST | `/monitor/alerts` | AI 上报实时告警 | exec_log:write | |
| 41 | GET | `/knowledge/documents` | 知识文档列表 | task:read | |
| 42 | **POST** | **`/knowledge/documents/upload`** | **上传知识文档（物理文件）** | knowledge:upload | **★新增** |
| 43 | POST | `/knowledge/documents` | 新增知识文档（仅元数据） | system:admin | |
| 44 | **POST** | **`/knowledge/documents/{docId}/upload`** | **更新文档版本（重新上传）** | knowledge:upload | **★新增** |
| 45 | POST | `/knowledge/documents/{docId}/vectorize` | 触发文档向量化 | system:admin | |
| 46 | GET | `/knowledge/documents/{docId}/chunks` | 向量块同步状态 | task:read | |
| 47 | POST | `/knowledge/documents/{docId}/chunks/retry-failed` | 重试失败同步块 | system:admin | |
| 48 | **GET** | **`/knowledge/documents/export`** | **知识文档列表导出** | task:read | **★新增** |
| 49 | GET | `/assertions` | 断言列表 | task:read | |
| 50 | GET | `/assertions/{id}` | 断言详情 | task:read | |
| 51 | POST | `/assertions` | 创建断言 | assertion:manage | |
| 52 | POST | `/assertions/batches` | 手动触发断言批次测试 | assertion:manage | |
| 53 | GET | `/assertions/batches` | 断言批次列表 | task:read | |
| 54 | GET | `/assertions/batches/{runBatchId}` | 断言批次详情 | task:read | |
| 55 | GET | `/cost/daily` | Token 日消耗汇总 | cost:read | |
| 56 | **GET** | **`/cost/daily/export`** | **Token 日报 Excel 导出** | cost:export | **★新增** |
| 57 | GET | `/cost/stat` | 多维度成本统计 | cost:read | |
| 58 | **GET** | **`/cost/stat/export`** | **成本统计 Excel 导出** | cost:export | **★新增** |
| 59 | GET | `/cost/roi-summary` | 月度 ROI 摘要 | cost:read | |

> ★ 标注为 V1.1 新增接口，共 **8 个**（含 4 个导出接口、2 个文件上传接口、2 个系统辅助接口）。

### 附录 B：限流策略

| 规则 | 限制 | 说明 |
|------|------|------|
| 全局限流 | 1000 次/分钟/IP | 超出返回 HTTP 429 |
| AI_AGENT 账号 | 200 次/分钟 | 执行日志写入密集场景 |
| 登录接口 | 10 次/分钟/IP | 防暴力破解 |
| 断言批次触发 | 1 次/5分钟 | 防止重复触发 |
| 文件上传接口 | 10 次/小时/用户 | 防止资源滥用 |
| 导出接口 | 5 次/分钟/用户 | 防止重复导出占用资源 |

### 附录 C：知识摄入完整流程（文件上传至可检索）

```
步骤 1：用户通过界面选择文件
         │
         ▼
步骤 2：POST /knowledge/documents/upload
         ├── 服务端校验格式（.pdf/.md/.docx/.xlsx/.txt）
         ├── 校验大小（≤ 50MB）
         ├── 存储到内网文件服务器
         └── 创建 ai_kb_document 记录（vectorStatus=PENDING）
         │
         ▼
步骤 3：文件解析服务（异步）
         ├── 提取文本内容
         ├── 按 512-1024 token 分块
         └── 写入 ai_kb_chunk（sync_status=PENDING）
         │
         ▼
步骤 4：向量化服务（异步，autoVectorize=true 自动触发）
         ├── 读取 sync_status=PENDING 的块
         ├── 调用 Embedding 模型生成向量
         ├── 写入 ChromaDB/Milvus
         └── 更新 ai_kb_chunk.sync_status=SUCCESS / FAILED
         │
         ▼
步骤 5：AI 检索可用
         查询条件必须包含：WHERE sync_status = 'SUCCESS'
```

### 附录 D：版本历史

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|--------|
| V1.0 | 2026-04-11 | AI 技术负责人 | 初稿，覆盖 50 个端点 |
| V1.1 | 2026-04-11 | AI 技术负责人 | 新增文件上传接口（9.2 知识文档上传、9.4 版本更新）；新增 4 个 Excel 导出接口（任务/成本/Token日报/巡检）；补充知识文档列表导出；新增下载一次性 Token 接口；完善文件处理错误码（80001-80006）；补充导出接口通用规范（第十三章）；新增权限标识 `task:export`/`cost:export`/`monitor:export`/`knowledge:upload` |

### 附录 E：关联文件

| 文件编号 | 文件名称 | 状态 |
|--------|--------|------|
| AI-MES-TECH-2026-001 | MES AI 智能体机器人技术方案 V1.1 | 已发布 |
| AI-MES-CLAUDE-2026-001 | CLAUDE.md 开发行为规范 V1.0 | 已发布 |
| AI-MES-DB-2026-001 | 数据库设计文档 V1.1 | 已发布 |
| AI-MES-API-2026-001 | API 接口规范文档 V1.1（本文件） | 已发布 |

---

*芯智云匠——山东芯通 MES 岗位 AI 智能体资产化项目*
*API 接口规范文档 AI-MES-API-2026-001 V1.1 · 2026年4月*
*内部文件，未经授权禁止外传*
