# 训练结果：工单核心

**训练时间**：2026-04-13T10:57:53.541921

**Tokens**：{'prompt_tokens': 2170, 'completion_tokens': 691, 'total_tokens': 2861}

---

1. **表清单确认**

| 表名 | 中文业务含义 |
|------|-------------|
| itsm_ticket_ci_map | 工单与CMDB配置项关联表，支持多对多，记录故障影响范围 |
| itsm_ticket_comment | 工单评论表，支持提单人与处理人沟通，支持内部备注 |
| itsm_ticket_flow_log | 工单流转日志，不可删除，全量记录每次状态变更，用于审计和流程分析 |
| itsm_ticket | 工单主表，ITSM系统核心数据表，记录服务请求、故障申报等全生命周期 |

2. **核心实体识别**

- **itsm_ticket**：工单主表，是ITSM系统的核心，记录了工单的全生命周期信息，包括工单状态、优先级、处理人等关键业务数据。业务角色包括提单人、处理人、审核人等。
- **itsm_ticket_flow_log**：工单流转日志表，记录了工单状态变更的详细历史，对于审计和流程分析至关重要。业务角色主要是系统管理员和审计人员。

3. **主键与外键梳理**

```
+----------------+         +----------------+         +----------------+
| itsm_ticket_ci_map |<------>| itsm_ticket_comment |<------>| itsm_ticket_flow_log |
+----------------+         +----------------+         +----------------+
| ticket_id       |         | ticket_id       |         | ticket_id       |
+----------------+         +----------------+         +----------------+
| ci_id          |         |                |         |                |
+----------------+         +----------------+         +----------------+
```

- **itsm_ticket_ci_map** 表中的 `ticket_id` 字段与 **itsm_ticket** 表中的 `id` 字段关联。
- **itsm_ticket_comment** 表中的 `ticket_id` 字段与 **itsm_ticket** 表中的 `id` 字段关联。
- **itsm_ticket_flow_log** 表中的 `ticket_id` 字段与 **itsm_ticket** 表中的 `id` 字段关联。

4. **关键状态字段**

- **itsm_ticket** 表中的 `status` 字段：
  - Created：已创建
  - Pending：待处理
  - Processing：处理中
  - Pending_Review：待审核
  - Closed：已关闭

- **itsm_ticket_flow_log** 表中的 `action` 字段：
  - AUTO_ROUTE：自动分单
  - CLAIM：接单
  - TRANSFER：转单
  - SUSPEND：挂起
  - RESUME：恢复
  - SUBMIT_REVIEW：提交审核
  - APPROVE：审批通过
  - REJECT：驳回
  - CLOSE：关闭

- **itsm_ticket** 表中的 `is_deleted` 字段：
  - 0：未删除
  - 1：已删除（逻辑删除）

- **itsm_ticket_comment** 表中的 `is_deleted` 字段：
  - 0：未删除
  - 1：已删除（逻辑删除）

5. **疑问记录**

- 无字段含义不清晰或注释缺失，所有字段均有明确的业务含义和注释。