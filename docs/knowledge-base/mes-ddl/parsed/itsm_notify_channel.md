## 表：itsm_notify_channel（消息推送渠道配置表，每种渠道仅一行配置，支持邮件、短信、飞书、钉钉）

**模块**：通知与审计  |  **PostgreSQL Schema**：public（SQL中直接写表名，禁止添加任何schema前缀）  |  **来源文件**：07_通知与审计.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `channel_type` | `VARCHAR(32)` | 否 | `` | 渠道类型：EMAIL邮件 SMS短信 LARK飞书 DINGDING钉钉 |
| `name` | `VARCHAR(64)` | 否 | `` | 渠道显示名 |
| `config_json` | `TEXT` | 否 | `` | 渠道连接配置，AES-256加密存储，含SMTP地址/API Key等敏感信息 |
| `is_enabled` | `SMALLINT` | 否 | `0` | 强管控开关：0禁用 1启用。变更即时写入Redis，消费者实时读取 |
| `last_test_at` | `TIMESTAMPTZ` | 是 | `` | 最近一次测试连接时间 |
| `last_test_result` | `VARCHAR(16)` | 是 | `` | 最近测试结果：SUCCESS成功 FAIL失败 |
| `last_test_error` | `VARCHAR(512)` | 是 | `` | 最近测试错误信息 |
| `rate_limit_count` | `INTEGER` | 否 | `100` | 每分钟最大发送数，限流保护 |
| `daily_quota` | `INTEGER` | 是 | `` | 日发送配额（短信渠道必填），控制成本 |
| `daily_sent_count` | `INTEGER` | 否 | `0` | 今日已发送数，每日零点重置 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 最后更新时间 |
| `updated_by` | `BIGINT` | 否 | `0` | 最后更新人 |

> *chunk_type: table_card | chunk_id: 通知与审计_itsm_notify_channel_table_card*
