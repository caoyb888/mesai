## 表：itsm_roster_team（值班团队表，定义可排班的团队，如"基础设施值班组"）

**模块**：运维日历与排班  |  **Schema**：itsm  |  **来源文件**：06_运维日历与排班.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `name` | `VARCHAR(64)` | 否 | `` | 团队名称 |
| `description` | `VARCHAR(256)` | 是 | `` | 团队描述 |
| `group_id` | `BIGINT` | 是 | `` | 关联用户组ID |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 更新时间 |
| `created_by` | `BIGINT` | 否 | `0` | 创建人 |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记 |

> *chunk_type: table_card | chunk_id: 运维日历与排班_itsm_roster_team_table_card*
