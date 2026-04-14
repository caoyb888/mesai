## 表：itsm_workflow_def（工作流定义表，FSM有限状态机配置持久化，支持热更新）

**模块**：服务配置引擎  |  **PostgreSQL Schema**：public（SQL中直接写表名，禁止添加任何schema前缀）  |  **来源文件**：02_服务配置引擎.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `name` | `VARCHAR(64)` | 否 | `` | 流程名称 |
| `code` | `VARCHAR(64)` | 否 | `` | 流程编码，全局唯一 |
| `states_json` | `TEXT` | 否 | `` | JSON格式状态节点定义：[{"code":"Created","label":"已创建","isInitial":true}] |
| `transitions_json` | `TEXT` | 否 | `` | JSON格式转换规则：[{"from":"Created","to":"Pending","action":"AUTO_ROUTE","actor":"SYSTEM"}] |
| `allow_close_states` | `VARCHAR(256)` | 否 | `'Created` | 允许执行关闭操作的状态列表，逗号分隔，Pending状态不可关闭 |
| `version` | `INTEGER` | 否 | `1` | 版本号，变更时递增 |
| `status` | `SMALLINT` | 否 | `1` | 流程状态：1启用 0禁用 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 更新时间 |
| `created_by` | `BIGINT` | 否 | `0` | 创建人 |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记 |

> *chunk_type: table_card | chunk_id: 服务配置引擎_itsm_workflow_def_table_card*
