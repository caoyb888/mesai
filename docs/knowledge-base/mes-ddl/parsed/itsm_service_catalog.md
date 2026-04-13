## 表：itsm_service_catalog（服务目录表，支持多级分类树，如IT服务->账号权限->邮箱开通）

**模块**：服务配置引擎  |  **Schema**：itsm  |  **来源文件**：02_服务配置引擎.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `name` | `VARCHAR(64)` | 否 | `` | 目录名称 |
| `parent_id` | `BIGINT` | 否 | `0` | 父目录ID，0表示顶级目录 |
| `icon_url` | `VARCHAR(256)` | 是 | `` | 目录图标路径 |
| `sort_order` | `INTEGER` | 否 | `0` | 同级排序 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 更新时间 |
| `created_by` | `BIGINT` | 否 | `0` | 创建人 |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记 |

> *chunk_type: table_card | chunk_id: 服务配置引擎_itsm_service_catalog_table_card*
