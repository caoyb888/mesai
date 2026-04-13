## 表：itsm_ticket（工单主表，ITSM系统核心数据表，记录服务请求、故障申报等全生命周期）

**模块**：工单核心  |  **Schema**：itsm  |  **来源文件**：03_工单核心.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 雪花算法主键 |
| `ticket_no` | `VARCHAR(32)` | 否 | `` | 业务编号，格式TK-YYYY-XXXXXX，流水号由Redis INCR生成，供用户可读 |
| `model_id` | `BIGINT` | 否 | `` | 服务模型ID，决定表单结构和处理流程 |
| `title` | `VARCHAR(256)` | 否 | `` | 工单标题 |
| `description` | `TEXT` | 是 | `` | 工单详细描述 |
| `status` | `VARCHAR(32)` | 否 | `'Created'` | FSM状态：Created已创建→Pending待处理→Processing处理中→Pending_Review待审核→Closed已关闭 |
| `priority` | `VARCHAR(16)` | 否 | `'MEDIUM'` | 优先级：LOW低 MEDIUM中 HIGH高 CRITICAL紧急 |
| `source` | `VARCHAR(16)` | 否 | `'PORTAL'` | 工单来源：PORTAL用户门户 API外部接口 WORKBENCH运维台直录 MONITOR监控系统自动创建 |
| `created_user_id` | `BIGINT` | 否 | `` | 提单人ID |
| `assigned_group_id` | `BIGINT` | 是 | `` | 当前处理用户组ID |
| `assigned_user_id` | `BIGINT` | 是 | `` | 当前处理人ID，接单后分配 |
| `form_data_json` | `TEXT` | 是 | `` | 动态表单填写数据，JSON格式，key与form_field.field_key对应 |
| `sla_deadline_response` | `TIMESTAMPTZ` | 是 | `` | 响应截止时间，由SLA引擎计算 |
| `sla_deadline_resolve` | `TIMESTAMPTZ` | 是 | `` | 解决截止时间 |
| `response_at` | `TIMESTAMPTZ` | 是 | `` | 实际响应时间，进入Processing状态时记录 |
| `resolved_at` | `TIMESTAMPTZ` | 是 | `` | 实际解决时间，进入Closed状态时记录 |
| `sla_response_status` | `VARCHAR(16)` | 是 | `` | SLA响应状态：NORMAL正常 WARNING预警(80%阈值) BREACH已违约 |
| `sla_resolve_status` | `VARCHAR(16)` | 是 | `` | SLA解决状态 |
| `close_reason` | `VARCHAR(512)` | 是 | `` | 关闭原因说明 |
| `closed_at` | `TIMESTAMPTZ` | 是 | `` | 关闭时间 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 最后更新时间 |
| `created_by` | `BIGINT` | 否 | `0` | 创建人 |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记 |

> *chunk_type: table_card | chunk_id: 工单核心_itsm_ticket_table_card*
