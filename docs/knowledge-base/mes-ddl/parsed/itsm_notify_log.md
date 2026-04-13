## 表：itsm_notify_log（通知发送日志表，记录所有消息推送历史，用于追踪和重试）

**模块**：通知与审计  |  **Schema**：itsm  |  **来源文件**：07_通知与审计.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `channel_type` | `VARCHAR(32)` | 否 | `` | 使用的渠道类型 |
| `ticket_id` | `BIGINT` | 是 | `` | 关联工单ID，可为空（如审核通知） |
| `recipient` | `VARCHAR(128)` | 否 | `` | 接收人（手机号/邮箱/用户ID） |
| `subject` | `VARCHAR(256)` | 是 | `` | 标题（邮件使用） |
| `content` | `TEXT` | 否 | `` | 发送内容 |
| `status` | `VARCHAR(16)` | 否 | `'PENDING'` | 发送状态：PENDING待发送 SENT已发送 FAILED发送失败 SKIPPED渠道已禁用跳过 |
| `retry_count` | `SMALLINT` | 否 | `0` | 已重试次数 |
| `error_msg` | `VARCHAR(512)` | 是 | `` | 失败错误信息 |
| `sent_at` | `TIMESTAMPTZ` | 是 | `` | 实际发送时间 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 记录创建时间 |

> *chunk_type: table_card | chunk_id: 通知与审计_itsm_notify_log_table_card*
