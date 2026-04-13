## 表：itsm_attachment（附件元数据表，文件实体存储于MinIO对象存储，此表仅存元数据）

**模块**：附件管理  |  **Schema**：itsm  |  **来源文件**：08_附件管理.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `ref_type` | `VARCHAR(32)` | 否 | `` | 关联业务类型：TICKET工单 KB_ARTICLE知识条目 COMMENT评论 |
| `ref_id` | `BIGINT` | 否 | `` | 关联业务ID |
| `file_name` | `VARCHAR(256)` | 否 | `` | 原始文件名 |
| `file_size` | `BIGINT` | 否 | `` | 文件大小（字节），最大20MB（20971520字节） |
| `file_type` | `VARCHAR(64)` | 否 | `` | MIME类型，如application/pdf image/png |
| `file_ext` | `VARCHAR(16)` | 否 | `` | 文件扩展名，如pdf png docx |
| `bucket_name` | `VARCHAR(64)` | 否 | `` | MinIO bucket名称 |
| `object_key` | `VARCHAR(512)` | 否 | `` | MinIO对象路径，格式：{ref_type}/{year}/{month}/{uuid}.{ext} |
| `md5` | `VARCHAR(32)` | 是 | `` | 文件MD5哈希，用于完整性校验 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 上传时间 |
| `created_by` | `BIGINT` | 否 | `0` | 上传人ID |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记 |

> *chunk_type: table_card | chunk_id: 附件管理_itsm_attachment_table_card*
