## 表：itsm_user_role（用户角色关联表，多对多关系）

**模块**：用户与权限  |  **Schema**：itsm  |  **来源文件**：01_用户与权限.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `user_id` | `BIGINT` | 否 | `` | 用户ID |
| `role_id` | `BIGINT` | 否 | `` | 角色ID |
| `granted_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 授权时间 |
| `granted_by` | `BIGINT` | 否 | `` | 授权人ID |

> *chunk_type: table_card | chunk_id: 用户与权限_itsm_user_role_table_card*
