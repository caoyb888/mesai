## 表：itsm_ticket_comment（工单评论表，支持提单人与处理人沟通，支持内部备注）

**模块**：工单核心  |  **PostgreSQL Schema**：public（SQL中直接写表名，禁止添加任何schema前缀）  |  **来源文件**：03_工单核心.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `ticket_id` | `BIGINT` | 否 | `` | 工单ID |
| `user_id` | `BIGINT` | 否 | `` | 评论人ID |
| `content` | `TEXT` | 否 | `` | 评论内容，支持富文本HTML |
| `is_internal` | `SMALLINT` | 否 | `0` | 0=公开（用户和运维均可见） 1=内部（仅运维可见） |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 更新时间 |
| `created_by` | `BIGINT` | 否 | `0` | 创建人 |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记 |

> *chunk_type: table_card | chunk_id: 工单核心_itsm_ticket_comment_table_card*
