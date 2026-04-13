## 表：itsm_user_group_member（用户组成员关联表，多对多关系）

**模块**：用户与权限  |  **Schema**：itsm  |  **来源文件**：01_用户与权限.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `group_id` | `BIGINT` | 否 | `` | 用户组ID |
| `user_id` | `BIGINT` | 否 | `` | 用户ID |
| `role_in_group` | `VARCHAR(32)` | 否 | `'MEMBER'` | 组内角色：MEMBER普通成员 LEADER组长 |
| `joined_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 加入时间 |

> *chunk_type: table_card | chunk_id: 用户与权限_itsm_user_group_member_table_card*
