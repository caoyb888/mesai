## 表：itsm_roster_team_member（值班团队成员表，定义团队成员及轮班顺序）

**模块**：运维日历与排班  |  **PostgreSQL Schema**：public（SQL中直接写表名，禁止添加任何schema前缀）  |  **来源文件**：06_运维日历与排班.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `team_id` | `BIGINT` | 否 | `` | 团队ID |
| `user_id` | `BIGINT` | 否 | `` | 用户ID |
| `sort_order` | `INTEGER` | 否 | `0` | 轮班顺序，数字小的先值班 |
| `joined_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 加入团队时间 |

> *chunk_type: table_card | chunk_id: 运维日历与排班_itsm_roster_team_member_table_card*
