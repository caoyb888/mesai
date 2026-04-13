## 表：itsm_kb_category（知识库分类表，支持多级分类树）

**模块**：知识库  |  **Schema**：itsm  |  **来源文件**：05_知识库.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `name` | `VARCHAR(64)` | 否 | `` | 分类名称 |
| `parent_id` | `BIGINT` | 否 | `0` | 父分类ID，0表示顶级 |
| `sort_order` | `INTEGER` | 否 | `0` | 同级排序 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 更新时间 |
| `created_by` | `BIGINT` | 否 | `0` | 创建人 |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记 |

> *chunk_type: table_card | chunk_id: 知识库_itsm_kb_category_table_card*
