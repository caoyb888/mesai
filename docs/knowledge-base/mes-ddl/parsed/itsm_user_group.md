## 表：itsm_user_group（用户组表，工单分配与权限控制的基本单元，如一线支持组、二线运维组）

**模块**：用户与权限  |  **Schema**：itsm  |  **来源文件**：01_用户与权限.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键ID |
| `name` | `VARCHAR(64)` | 否 | `` | 用户组名称，如"应用运维一组" |
| `dept_id` | `BIGINT` | 是 | `` | 所属部门ID，可选 |
| `description` | `VARCHAR(256)` | 是 | `` | 组描述说明 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 更新时间 |
| `created_by` | `BIGINT` | 否 | `0` | 创建人 |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记 |

> *chunk_type: table_card | chunk_id: 用户与权限_itsm_user_group_table_card*
