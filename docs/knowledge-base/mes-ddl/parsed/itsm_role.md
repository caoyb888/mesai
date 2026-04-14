## 表：itsm_role（角色表，定义系统角色如超级管理员、运维工程师、服务台人员）

**模块**：用户与权限  |  **PostgreSQL Schema**：public（SQL中直接写表名，禁止添加任何schema前缀）  |  **来源文件**：01_用户与权限.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `code` | `VARCHAR(64)` | 否 | `` | 角色编码，如ROLE_ADMIN，用于代码层权限判断 |
| `name` | `VARCHAR(64)` | 否 | `` | 角色显示名称 |
| `description` | `VARCHAR(256)` | 是 | `` | 角色描述 |
| `is_system` | `SMALLINT` | 否 | `0` | 系统内置角色标记，1表示内置，禁止删除和修改code |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 更新时间 |
| `created_by` | `BIGINT` | 否 | `0` | 创建人 |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记 |

> *chunk_type: table_card | chunk_id: 用户与权限_itsm_role_table_card*
