## 表：itsm_dept（部门表，支持无限层级树形组织结构）

**模块**：用户与权限  |  **PostgreSQL Schema**：public（SQL中直接写表名，禁止添加任何schema前缀）  |  **来源文件**：01_用户与权限.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 雪花算法主键 |
| `name` | `VARCHAR(64)` | 否 | `` | 部门名称 |
| `parent_id` | `BIGINT` | 否 | `0` | 父部门ID，0表示顶级部门 |
| `sort_order` | `INTEGER` | 否 | `0` | 同级部门排序序号 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 更新时间 |
| `created_by` | `BIGINT` | 否 | `0` | 创建人ID |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记 |

> *chunk_type: table_card | chunk_id: 用户与权限_itsm_dept_table_card*
