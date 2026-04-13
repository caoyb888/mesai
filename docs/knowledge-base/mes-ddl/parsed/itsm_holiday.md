## 表：itsm_holiday（节假日日历表，SLA时间计算时排除休息日，支持调休工作日设置）

**模块**：SLA引擎  |  **Schema**：itsm  |  **来源文件**：04_SLA 引擎.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `holiday_date` | `DATE` | 否 | `` | 节假日日期 |
| `name` | `VARCHAR(64)` | 否 | `` | 节假日名称，如"元旦"、"春节" |
| `year` | `SMALLINT` | 否 | `` | 所属年份，方便按年查询 |
| `is_workday` | `SMALLINT` | 否 | `0` | 0=法定休息日 1=法定调休工作日（如周末上班） |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `created_by` | `BIGINT` | 否 | `0` | 创建人 |

> *chunk_type: table_card | chunk_id: SLA引擎_itsm_holiday_table_card*
