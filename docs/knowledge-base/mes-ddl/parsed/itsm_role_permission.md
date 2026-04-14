## 表：itsm_role_permission（角色权限关联表，定义角色拥有的权限集合）

**模块**：用户与权限  |  **PostgreSQL Schema**：public（SQL中直接写表名，禁止添加任何schema前缀）  |  **来源文件**：01_用户与权限.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `role_id` | `BIGINT` | 否 | `` | 角色ID |
| `permission_id` | `BIGINT` | 否 | `` | 权限ID |

> *chunk_type: table_card | chunk_id: 用户与权限_itsm_role_permission_table_card*
