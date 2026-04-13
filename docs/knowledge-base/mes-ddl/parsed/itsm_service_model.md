## 表：itsm_service_model（服务模型表，定义每类服务的表单结构、处理流程与SLA策略，如"软件安装申请"）

**模块**：服务配置引擎  |  **Schema**：itsm  |  **来源文件**：02_服务配置引擎.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `catalog_id` | `BIGINT` | 否 | `` | 所属服务目录ID |
| `name` | `VARCHAR(64)` | 否 | `` | 服务名称 |
| `code` | `VARCHAR(64)` | 否 | `` | 服务编码，规则引擎按此路由到默认处理组 |
| `description` | `VARCHAR(512)` | 是 | `` | 服务描述 |
| `workflow_def_id` | `BIGINT` | 否 | `` | 绑定的工作流定义ID |
| `sla_policy_id` | `BIGINT` | 是 | `` | 关联SLA策略，为空则不计算SLA |
| `default_group_id` | `BIGINT` | 是 | `` | 默认分配用户组 |
| `status` | `SMALLINT` | 否 | `1` | 服务状态：1上线 0下线 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 更新时间 |
| `created_by` | `BIGINT` | 否 | `0` | 创建人 |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记 |

> *chunk_type: table_card | chunk_id: 服务配置引擎_itsm_service_model_table_card*
