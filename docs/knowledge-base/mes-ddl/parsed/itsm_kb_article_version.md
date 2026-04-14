## 表：itsm_kb_article_version（知识条目版本历史表，每次发布创建新版本，保留全部历史便于回溯）

**模块**：知识库  |  **PostgreSQL Schema**：public（SQL中直接写表名，禁止添加任何schema前缀）  |  **来源文件**：05_知识库.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `article_id` | `BIGINT` | 否 | `` | 知识条目ID |
| `version` | `INTEGER` | 否 | `` | 版本号，从1开始递增 |
| `content` | `TEXT` | 否 | `` | 富文本内容（HTML格式） |
| `change_note` | `VARCHAR(256)` | 是 | `` | 本版本修改说明 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 版本创建时间 |
| `created_by` | `BIGINT` | 否 | `0` | 版本创建人 |

> *chunk_type: table_card | chunk_id: 知识库_itsm_kb_article_version_table_card*
