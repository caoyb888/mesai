## 表：itsm_ticket_ci_map（工单与CMDB配置项关联表，支持多对多，记录故障影响范围）

**模块**：工单核心  |  **PostgreSQL Schema**：public（SQL中直接写表名，禁止添加任何schema前缀）  |  **来源文件**：03_工单核心.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `ticket_id` | `BIGINT` | 否 | `` | 工单ID |
| `ci_id` | `BIGINT` | 否 | `` | CMDB配置项ID（外系统主键） |
| `ci_type` | `VARCHAR(64)` | 否 | `` | CI类型，如SERVER服务器/DATABASE数据库/NETWORK网络设备 |
| `ci_name` | `VARCHAR(128)` | 是 | `` | CI名称冗余存储，防止CMDB数据变更后历史记录失效 |
| `relation_type` | `VARCHAR(32)` | 否 | `'AFFECTED'` | 关联类型：AFFECTED受影响资产 CAUSED_BY故障根因 RELATED相关资产 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `created_by` | `BIGINT` | 否 | `0` | 创建人 |

> *chunk_type: table_card | chunk_id: 工单核心_itsm_ticket_ci_map_table_card*
