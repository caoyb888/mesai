## 表：itsm_audit_log（系统审计日志，永久保留，满足等保三级合规要求，记录所有关键操作）

**模块**：通知与审计  |  **Schema**：itsm  |  **来源文件**：07_通知与审计.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `user_id` | `BIGINT` | 是 | `` | 操作人ID，NULL表示未登录/系统操作 |
| `account_no` | `VARCHAR(64)` | 是 | `` | 操作人账号（冗余，防用户删除后丢失） |
| `login_ip` | `VARCHAR(64)` | 是 | `` | 登录/操作IP地址 |
| `user_agent` | `TEXT` | 是 | `` | 浏览器UA，可识别是否使用推荐的Chrome环境 |
| `trace_id` | `VARCHAR(64)` | 是 | `` | 请求链路追踪ID，用于分布式追踪 |
| `module` | `VARCHAR(32)` | 否 | `` | 操作模块，如TICKET/USER/SYSTEM |
| `action` | `VARCHAR(64)` | 否 | `` | 操作动作，如CREATE/UPDATE/DELETE/LOGIN |
| `resource_type` | `VARCHAR(64)` | 是 | `` | 操作资源类型，如TICKET/USER/KB_ARTICLE |
| `resource_id` | `VARCHAR(64)` | 是 | `` | 操作资源ID |
| `before_json` | `TEXT` | 是 | `` | 变更前数据快照（JSON），CREATE操作为NULL |
| `after_json` | `TEXT` | 是 | `` | 变更后数据快照（JSON） |
| `result` | `VARCHAR(16)` | 否 | `` | 操作结果：SUCCESS成功 FAIL失败 |
| `error_msg` | `VARCHAR(512)` | 是 | `` | 失败错误信息 |
| `operated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 操作时间 |

> *chunk_type: table_card | chunk_id: 通知与审计_itsm_audit_log_table_card*
