# 训练结果：SLA引擎

**训练时间**：2026-04-13T10:58:05.665494

**Tokens**：{'prompt_tokens': 1686, 'completion_tokens': 604, 'total_tokens': 2290}

---

1. **表清单确认**

| 表名 | 中文业务含义 |
|--------|--------|
| itsm_holiday | 节假日日历表，用于SLA时间计算时排除休息日，支持调休工作日设置 |
| itsm_sla_policy | SLA策略表，定义响应和解决时限，支持不同服务时间窗口 |
| itsm_sla_record | 工单SLA计算记录表，记录每工单的SLA达成情况 |

2. **核心实体识别**

- **itsm_sla_policy**：这是该模块中最重要的表之一，因为它定义了SLA策略，包括响应和解决时限，以及服务时间窗口。业务角色包括服务管理团队，他们需要根据业务需求和服务质量目标来配置这些策略。
- **itsm_sla_record**：这是另一个核心表，因为它记录了每个工单的SLA达成情况，包括响应和解决的截止时间和实际时间。业务角色包括服务支持团队和管理层，他们需要监控和分析这些数据以确保服务质量。

3. **主键与外键梳理**

```
+----------------+         +------------------+
| itsm_holiday    |         | itsm_sla_policy   |
+----------------+         +------------------+
| id (PK)        |         | id (PK)          |
+----------------+         +------------------+
        |                   |
        |                   |
        v                   v
        |                   |
+----------------+         +------------------+
| itsm_sla_record |         | itsm_sla_policy   |
+----------------+         +------------------+
| id (PK)        |         | id (PK)          |
+----------------+         +------------------+
| sla_policy_id (FK) |------>| id (PK)          |
+----------------+         +------------------+
```

4. **关键状态字段**

- **itsm_sla_policy**：
  - `is_deleted`：逻辑删除标记，0表示未删除，1表示已删除。
  - `warn_threshold_pct`：预警触发百分比，默认80%时限已用时触发告警。

- **itsm_sla_record**：
  - `response_status`：SLA响应达成状态，'NORMAL'表示正常，'WARNING'表示预警，'BREACH'表示违约。
  - `resolve_status`：SLA解决达成状态，'NORMAL'表示正常，'WARNING'表示预警，'BREACH'表示违约。

5. **疑问记录**

- `itsm_sla_policy`表中的`service_time_json`字段含义不清晰，需要进一步解释JSON格式的具体结构和内容。【待补充】
- `itsm_sla_record`表中的`response_work_minutes`和`resolve_work_minutes`字段的具体计算方法和规则未说明。【待补充】