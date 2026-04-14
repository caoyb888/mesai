## 表：itsm_permission（权限资源表，存储菜单、按钮、API接口级权限定义）

**模块**：用户与权限  |  **PostgreSQL Schema**：public（SQL中直接写表名，禁止添加任何schema前缀）  |  **来源文件**：01_用户与权限.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `code` | `VARCHAR(128)` | 否 | `` | 权限编码，如ticket:create，用于前端按钮显隐控制 |
| `name` | `VARCHAR(64)` | 否 | `` | 权限显示名称 |
| `type` | `VARCHAR(16)` | 否 | `` | 权限类型：MENU菜单项 BUTTON页面按钮 API后端接口 |
| `resource_path` | `VARCHAR(256)` | 是 | `` | 前端路由路径或后端接口路径 |
| `parent_id` | `BIGINT` | 否 | `0` | 父权限ID，构建权限树结构 |
| `sort_order` | `INTEGER` | 否 | `0` | 同级排序 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 更新时间 |
| `created_by` | `BIGINT` | 否 | `0` | 创建人 |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记 |

> *chunk_type: table_card | chunk_id: 用户与权限_itsm_permission_table_card*
