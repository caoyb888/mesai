## 模块：SLA 管理

**系统**：ITSM | **接口数**：5 | **模块说明**：SLA 策略、节假日、统计报表

### 接口速查表

| 方法 | 路径 | 说明 | 是否需要鉴权 |
|------|------|------|------------|
| **GET** | `/sla-policies` | 获取 SLA 策略列表 | ✅ JWT |
| **POST** | `/sla-policies` | 创建 SLA 策略 | ✅ JWT |
| **GET** | `/holidays` | 获取节假日列表 | ✅ JWT |
| **POST** | `/holidays/batch` | 批量导入节假日 | ✅ JWT |
| **GET** | `/sla/statistics` | SLA 统计报表 | ✅ JWT |

### 接口详情

#### GET /sla-policies

**功能**：获取 SLA 策略列表
**operationId**：`listSlaPolicies`
**鉴权**：✅ 需要 Bearer Token（全局默认）

**响应（200）：** SLA 策略列表

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `code` | integer | ✅ | 业务状态码，6 位数字 |
| `message` | string | ✅ | 提示信息（中文） |
| `data` | object | ✅ | 业务数据，失败时为 null |
| `traceId` | string | ✅ | 链路追踪 ID |
| `data` | array(SlaPolicy) |  |  |

#### POST /sla-policies

**功能**：创建 SLA 策略
**operationId**：`createSlaPolicy`
**鉴权**：✅ 需要 Bearer Token（全局默认）

**请求体（application/json）：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | ✅ |  |
| `serviceTimeType` | string | ✅ |  |
| `serviceTimeJson` | object |  |  |
| `responseMedium` | integer |  |  |
| `responseHigh` | integer |  |  |
| `responseCritical` | integer |  |  |
| `resolveLow` | integer |  |  |
| `resolveMedium` | integer |  |  |
| `resolveHigh` | integer |  |  |
| `resolveCritical` | integer |  |  |
| `createdWarnMinutes` | integer |  |  |
| `createdEscalateMinutes` | integer |  |  |
| `warnThresholdPct` | integer |  |  |

**响应（200）：** 创建成功

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `code` | integer | ✅ | 业务状态码，6 位数字 |
| `message` | string | ✅ | 提示信息（中文） |
| `data` | object | ✅ | 业务数据，失败时为 null |
| `traceId` | string | ✅ | 链路追踪 ID |

#### GET /holidays

**功能**：获取节假日列表
**operationId**：`listHolidays`
**鉴权**：✅ 需要 Bearer Token（全局默认）

**查询参数：**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `year` | integer | ✅ |  |

**响应（200）：** 节假日列表

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `code` | integer | ✅ | 业务状态码，6 位数字 |
| `message` | string | ✅ | 提示信息（中文） |
| `data` | object | ✅ | 业务数据，失败时为 null |
| `traceId` | string | ✅ | 链路追踪 ID |
| `data` | array(Holiday) |  |  |

#### POST /holidays/batch

**功能**：批量导入节假日
**operationId**：`batchImportHolidays`
**鉴权**：✅ 需要 Bearer Token（全局默认）

**请求体（application/json）：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `year` | integer | ✅ |  |
| `holidays` | array(Holiday) | ✅ |  |

**响应（200）：** 导入成功

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `code` | integer | ✅ | 业务状态码，6 位数字 |
| `message` | string | ✅ | 提示信息（中文） |
| `data` | object | ✅ | 业务数据，失败时为 null |
| `traceId` | string | ✅ | 链路追踪 ID |

#### GET /sla/statistics

**功能**：SLA 统计报表
**operationId**：`getSlaStatistics`
**鉴权**：✅ 需要 Bearer Token（全局默认）

**查询参数：**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `startDate` | string | ✅ |  |
| `endDate` | string | ✅ |  |
| `groupId` | string |  |  |
| `modelId` | string |  |  |

**响应（200）：** 统计报表

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `code` | integer | ✅ | 业务状态码，6 位数字 |
| `message` | string | ✅ | 提示信息（中文） |
| `data` | object | ✅ | 业务数据，失败时为 null |
| `traceId` | string | ✅ | 链路追踪 ID |
| `data` | object(SlaStatistics) |  |  |
| `data.totalTickets` | integer |  |  |
| `data.responseAchieveRate` | number |  | 响应达成率（0-1） |
| `data.resolveAchieveRate` | number |  |  |
| `data.avgResponseMinutes` | integer |  |  |
| `data.avgResolveMinutes` | integer |  |  |
| `data.breachCount` | integer |  |  |
| `data.byPriority` | object |  |  |

---
*chunk_id: itsm_SLA_管理_api_module*
*chunk_type: api_module*
*关联任务：S2-2 T2-2-1 · 作者：AI（芯智云匠）· 日期：2026-04-13*