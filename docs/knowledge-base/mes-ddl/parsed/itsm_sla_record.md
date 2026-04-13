## 表：itsm_sla_record（工单SLA计算记录表，每工单一行，精确记录SLA达成情况）

**模块**：SLA引擎  |  **Schema**：itsm  |  **来源文件**：04_SLA 引擎.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `ticket_id` | `BIGINT` | 否 | `` | 工单ID，唯一 |
| `sla_policy_id` | `BIGINT` | 否 | `` | 应用的SLA策略ID |
| `priority` | `VARCHAR(16)` | 否 | `` | 工单优先级 |
| `created_at_tick` | `TIMESTAMPTZ` | 否 | `` | 工单创建时间（计时起点） |
| `response_deadline` | `TIMESTAMPTZ` | 是 | `` | 响应截止时间 |
| `resolve_deadline` | `TIMESTAMPTZ` | 是 | `` | 解决截止时间 |
| `actual_response_at` | `TIMESTAMPTZ` | 是 | `` | 实际响应时间 |
| `actual_resolve_at` | `TIMESTAMPTZ` | 是 | `` | 实际解决时间 |
| `response_work_minutes` | `INTEGER` | 是 | `` | 响应阶段有效工作时长（分钟），排除节假日和非工作时段后的净时长 |
| `resolve_work_minutes` | `INTEGER` | 是 | `` | 总解决有效工作时长（分钟） |
| `response_status` | `VARCHAR(16)` | 否 | `'NORMAL'` | SLA响应达成状态：NORMAL正常 WARNING预警 BREACH违约 |
| `resolve_status` | `VARCHAR(16)` | 否 | `'NORMAL'` | SLA解决达成状态 |
| `suspended_minutes` | `INTEGER` | 否 | `0` | Suspend挂起期间累计分钟数，SLA暂停计时，关闭时从总时长中扣除 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 记录创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 记录更新时间 |

> *chunk_type: table_card | chunk_id: SLA引擎_itsm_sla_record_table_card*
