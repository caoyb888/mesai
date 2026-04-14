## 表：itsm_form_field（动态表单字段定义表，支持无代码配置服务表单，定义字段类型、校验规则等）

**模块**：服务配置引擎  |  **PostgreSQL Schema**：public（SQL中直接写表名，禁止添加任何schema前缀）  |  **来源文件**：02_服务配置引擎.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `model_id` | `BIGINT` | 否 | `` | 所属服务模型ID |
| `field_key` | `VARCHAR(64)` | 否 | `` | 字段唯一键，如apply_reason，用于JSON数据存储 |
| `field_type` | `VARCHAR(32)` | 否 | `` | 字段类型：TEXT单行文本 TEXTAREA多行文本 SELECT单选下拉 MULTI_SELECT多选 DATE日期 DATETIME日期时间 FILE文件上传 CI_REF配置项关联 USER_REF人员选择器 CASCADE级联选择器 |
| `label` | `VARCHAR(64)` | 否 | `` | 前端显示标签 |
| `placeholder` | `VARCHAR(128)` | 是 | `` | 输入提示文本 |
| `required` | `BOOLEAN` | 否 | `FALSE` | 是否必填 |
| `options_json` | `TEXT` | 是 | `` | 下拉/多选选项，JSON数组格式：[{"label":"选项名","value":"值"}] |
| `validation_json` | `TEXT` | 是 | `` | 自定义校验规则，JSON格式：{"minLength":2,"maxLength":100} |
| `default_value` | `VARCHAR(256)` | 是 | `` | 默认值 |
| `sort_order` | `INTEGER` | 否 | `0` | 字段排序 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 更新时间 |
| `created_by` | `BIGINT` | 否 | `0` | 创建人 |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记 |

> *chunk_type: table_card | chunk_id: 服务配置引擎_itsm_form_field_table_card*
