## 表：itsm_ticket_flow_log（工单流转日志，不可删除，全量记录每次状态变更，用于审计和流程分析）

**模块**：工单核心  |  **Schema**：itsm  |  **来源文件**：03_工单核心.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 主键 |
| `ticket_id` | `BIGINT` | 否 | `` | 工单ID |
| `from_status` | `VARCHAR(32)` | 是 | `` | 流转前状态，NULL表示初始创建 |
| `to_status` | `VARCHAR(32)` | 否 | `` | 流转后状态 |
| `action` | `VARCHAR(64)` | 否 | `` | 触发动作：AUTO_ROUTE自动分单 CLAIM接单 TRANSFER转单 SUSPEND挂起 RESUME恢复 SUBMIT_REVIEW提交审核 APPROVE审批通过 REJECT驳回 CLOSE关闭 |
| `actor_type` | `VARCHAR(16)` | 否 | `'USER'` | 操作者类型：USER人工操作 SYSTEM系统自动 |
| `operator_id` | `BIGINT` | 是 | `` | 操作人ID，SYSTEM操作时为NULL |
| `remark` | `VARCHAR(1024)` | 是 | `` | 备注/处理说明 |
| `extra_json` | `TEXT` | 是 | `` | 扩展数据，如转单目标组信息 |
| `operated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 操作时间 |

> *chunk_type: table_card | chunk_id: 工单核心_itsm_ticket_flow_log_table_card*
