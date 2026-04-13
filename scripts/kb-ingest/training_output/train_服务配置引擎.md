# 训练结果：服务配置引擎

**训练时间**：2026-04-13T10:57:39.038866

**Tokens**：{'prompt_tokens': 1993, 'completion_tokens': 718, 'total_tokens': 2711}

---

1. **表清单确认**

| 表名                 | 中文业务含义                             |
|---------------------|--------------------------------------|
| itsm_form_field      | 动态表单字段定义表，用于定义服务表单的字段类型、校验规则等 |
| itsm_service_catalog | 服务目录表，支持多级分类树，如IT服务->账号权限->邮箱开通    |
| itsm_service_model   | 服务模型表，定义每类服务的表单结构、处理流程与SLA策略       |
| itsm_workflow_def    | 工作流定义表，FSM有限状态机配置持久化，支持热更新           |

2. **核心实体识别**

- **itsm_service_model（服务模型表）**：这是该模块中最重要的表之一，因为它定义了每类服务的表单结构、处理流程与SLA策略。业务角色可能包括服务管理员，他们负责定义和维护服务模型，以及服务请求者，他们通过服务模型提交服务请求。

- **itsm_workflow_def（工作流定义表）**：这张表也非常重要，因为它包含了FSM有限状态机配置，这些配置决定了服务请求的处理流程。业务角色可能包括流程设计师，他们负责设计和更新工作流，以及服务处理人员，他们根据工作流指导服务请求的处理。

3. **主键与外键梳理**

```
+----------------+         +----------------+         +----------------+
| itsm_form_field |         | itsm_service_catalog |         | itsm_service_model |
+----------------+         +----------------+         +----------------+
| id             |         | id             |         | id             |
+----------------+         +----------------+         +----------------+
         |                         |                         |
         |                         |                         |
         v                         v                         v
         |                         |                         |
         |                         |                         |
+----------------+         +----------------+         +----------------+
| itsm_workflow_def |         | itsm_service_model |         | itsm_form_field |
+----------------+         +----------------+         +----------------+
| id             |         | id             |         | id             |
+----------------+         +----------------+         +----------------+
```

- `itsm_form_field` 的 `model_id` 外键关联 `itsm_service_model` 的 `id`。
- `itsm_service_model` 的 `catalog_id` 外键关联 `itsm_service_catalog` 的 `id`。
- `itsm_service_model` 的 `workflow_def_id` 外键关联 `itsm_workflow_def` 的 `id`。

4. **关键状态字段**

- **itsm_service_model（服务模型表）**：
  - `status` 字段：1表示服务上线，0表示服务下线。

- **itsm_workflow_def（工作流定义表）**：
  - `status` 字段：1表示流程启用，0表示流程禁用。

- **itsm_form_field、itsm_service_catalog、itsm_service_model、itsm_workflow_def**：
  - `is_deleted` 字段：0表示未删除，1表示已删除（逻辑删除）。

5. **疑问记录**

- `itsm_form_field` 表中的 `validation_json` 字段：自定义校验规则的具体格式和规则待补充。
- `itsm_workflow_def` 表中的 `allow_close_states` 字段：具体的操作逻辑和状态含义待补充。