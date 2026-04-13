## 表：itsm_kb_article（知识条目主表，内容体存于版本表，支持版本管理和生命周期控制）

**模块**：知识库  |  **Schema**：itsm  |  **来源文件**：05_知识库.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `category_id` | `BIGINT` | 否 | `` | 所属分类ID |
| `title` | `VARCHAR(256)` | 否 | `` | 知识标题 |
| `summary` | `VARCHAR(512)` | 是 | `` | 摘要，用于列表展示 |
| `keywords` | `VARCHAR(256)` | 是 | `` | 关键词，逗号分隔，辅助全文搜索 |
| `status` | `VARCHAR(32)` | 否 | `'Draft'` | 生命周期：Draft草稿→Pending_Review待审核→Published已发布/Rejected驳回，Published可归档为Archived |
| `current_version` | `INTEGER` | 否 | `1` | 当前版本号，对应itsm_kb_article_version的版本 |
| `probe_ref_id` | `VARCHAR(128)` | 是 | `` | 监控探针关联标识，故障发生时自动推荐相关知识条目 |
| `published_at` | `TIMESTAMPTZ` | 是 | `` | 发布时间 |
| `published_by` | `BIGINT` | 是 | `` | 发布人ID |
| `reviewer_id` | `BIGINT` | 是 | `` | 审核人ID |
| `reviewed_at` | `TIMESTAMPTZ` | 是 | `` | 审核时间 |
| `review_comment` | `VARCHAR(512)` | 是 | `` | 审核意见 |
| `view_count` | `INTEGER` | 否 | `0` | 浏览次数统计 |
| `useful_count` | `INTEGER` | 否 | `0` | 被标记为有用次数 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 更新时间 |
| `created_by` | `BIGINT` | 否 | `0` | 创建人 |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记 |

> *chunk_type: table_card | chunk_id: 知识库_itsm_kb_article_table_card*
