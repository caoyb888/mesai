## 表：itsm_calendar_event（运维日历事件表，记录巡检计划、变更窗口、维护期等）

**模块**：运维日历与排班  |  **Schema**：itsm  |  **来源文件**：06_运维日历与排班.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `title` | `VARCHAR(128)` | 否 | `` | 事件标题 |
| `event_type` | `VARCHAR(32)` | 否 | `` | 事件类型：INSPECTION例行巡检 CHANGE_WINDOW变更窗口 MAINTENANCE系统维护期 ASSET_SCAN资产扫描 ON_DUTY值班排班 |
| `description` | `TEXT` | 是 | `` | 详细描述 |
| `start_time` | `TIMESTAMPTZ` | 否 | `` | 开始时间 |
| `end_time` | `TIMESTAMPTZ` | 否 | `` | 结束时间 |
| `all_day` | `BOOLEAN` | 否 | `FALSE` | 是否全天事件 |
| `related_group_id` | `BIGINT` | 是 | `` | 关联用户组（可选） |
| `color` | `VARCHAR(16)` | 是 | `` | 日历显示颜色（十六进制，如#FF5733） |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 更新时间 |
| `created_by` | `BIGINT` | 否 | `0` | 创建人 |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记 |

> *chunk_type: table_card | chunk_id: 运维日历与排班_itsm_calendar_event_table_card*
