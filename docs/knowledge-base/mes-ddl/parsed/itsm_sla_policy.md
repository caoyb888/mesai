## 表：itsm_sla_policy（SLA策略表，按优先级分别定义响应和解决时限，支持不同服务时间窗口）

**模块**：SLA引擎  |  **PostgreSQL Schema**：public（SQL中直接写表名，禁止添加任何schema前缀）  |  **来源文件**：04_SLA 引擎.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `name` | `VARCHAR(64)` | 否 | `` | 策略名称 |
| `service_time_type` | `VARCHAR(16)` | 否 | `` | 服务时间类型：5x8工作日8小时 7x24全天候 CUSTOM自定义 |
| `service_time_json` | `TEXT` | 是 | `` | CUSTOM时的自定义时间段配置，JSON格式 |
| `response_minutes_low` | `INTEGER` | 是 | `` | 低优先级响应时限（分钟） |
| `response_minutes_medium` | `INTEGER` | 是 | `` | 中优先级响应时限 |
| `response_minutes_high` | `INTEGER` | 是 | `` | 高优先级响应时限 |
| `response_minutes_critical` | `INTEGER` | 是 | `` | 紧急优先级响应时限 |
| `resolve_minutes_low` | `INTEGER` | 是 | `` | 低优先级解决时限 |
| `resolve_minutes_medium` | `INTEGER` | 是 | `` | 中优先级解决时限 |
| `resolve_minutes_high` | `INTEGER` | 是 | `` | 高优先级解决时限 |
| `resolve_minutes_critical` | `INTEGER` | 是 | `` | 紧急优先级解决时限 |
| `created_warn_minutes` | `INTEGER` | 是 | `` | Created状态停留超时一级告警阈值（分钟），不可绑定SLA时仍生效 |
| `created_escalate_minutes` | `INTEGER` | 是 | `` | Created状态超时第二级升级阈值 |
| `warn_threshold_pct` | `INTEGER` | 否 | `80` | 预警触发百分比，默认80%时限已用时触发告警 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 更新时间 |
| `created_by` | `BIGINT` | 否 | `0` | 创建人 |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记 |

> *chunk_type: table_card | chunk_id: SLA引擎_itsm_sla_policy_table_card*
