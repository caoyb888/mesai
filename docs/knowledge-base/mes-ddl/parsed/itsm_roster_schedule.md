## 表：itsm_roster_schedule（排班记录表，工单分配时查询当日值班人作为默认处理人）

**模块**：运维日历与排班  |  **Schema**：itsm  |  **来源文件**：06_运维日历与排班.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `team_id` | `BIGINT` | 否 | `` | 团队ID |
| `user_id` | `BIGINT` | 否 | `` | 值班人ID |
| `schedule_date` | `DATE` | 否 | `` | 值班日期 |
| `shift_type` | `VARCHAR(16)` | 否 | `'DAY'` | 班次类型：DAY白班 NIGHT夜班 FULL全天班 |
| `start_time` | `TIME` | 否 | `` | 班次开始时间 |
| `end_time` | `TIME` | 否 | `` | 班次结束时间 |
| `is_on_duty` | `SMALLINT` | 否 | `1` | 值班状态：1正常值班 0调班/请假 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 更新时间 |
| `created_by` | `BIGINT` | 否 | `0` | 排班创建人 |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记 |

> *chunk_type: table_card | chunk_id: 运维日历与排班_itsm_roster_schedule_table_card*
