# 芯智云匠 · 数据库设计文档
## 山东芯通 MES AI 智能体资产化项目

| 项目 | 内容 |
|------|------|
| 文件编号 | AI-MES-DB-2026-001 |
| 版本号 | V1.1 |
| 编写日期 | 2026年4月 |
| 编写单位 | 乙方技术团队 |
| 关联方案 | AI-MES-TECH-2026-001 (V1.1) |
| 文件状态 | 正式发布 |

### 版本变更说明（V1.0 → V1.1）

| # | 优化项 | 变更内容 |
|---|--------|--------|
| 1 | **版本联动追溯** | `ai_assertion_batch` 新增 `related_task_id`、`related_commit_hash`、`trigger_source` 字段，实现"代码提交 → 断言验证 → 阻断决策"完整链路 |
| 2 | **Token 成本分摊** | `ai_exec_log` 新增 `dept`、`module`、`estimated_cost_cny` 字段；新增 `ai_token_stat` 多维度汇总表，支持按部门/模块/任务类型生成 ROI 报告 |
| 3 | **向量同步状态** | `ai_kb_chunk` 新增 `sync_status`、`last_sync_at`、`last_sync_error` 字段，AI 检索时仅返回 `sync_status = 'SUCCESS'` 的记录 |
| 4 | **并发 task_no 生成** | 明确 `task_no` 生成策略为 Redis 分布式递增 + 日期后缀，补充序列号管理表 `ai_seq_counter` 及应用层生成规范 |

---

## 目录

1. [文档概述](#一文档概述)
2. [实体关系模型（ERD）](#二实体关系模型erd)
3. [Schema 详细设计](#三schema-详细设计)
   - 3.1 [mes_ai_task（任务管理）](#31-schema-mes_ai_task任务管理)
   - 3.2 [mes_ai_monitor（运维监控）](#32-schema-mes_ai_monitor运维监控)
   - 3.3 [mes_ai_knowledge（知识库与断言库）](#33-schema-mes_ai_knowledge知识库与断言库)
   - 3.4 [mes_ai_audit（安全审计）](#34-schema-mes_ai_audit安全审计)
4. [完整建表 DDL](#四完整建表-ddl)
5. [索引策略](#五索引策略)
6. [分区策略](#六分区策略)
7. [字段注释规范](#七字段注释规范)
8. [优化设计补充说明](#八优化设计补充说明)
9. [附录](#九附录)

---

## 一、文档概述

### 1.1 设计范围

本文档覆盖芯智云匠项目 AI 任务管理平台的全部数据库设计，共涉及 **4 个 Schema，22 张核心业务表**（V1.1 新增 `ai_token_stat`、`ai_seq_counter` 共 2 张）：

| Schema | 用途 | 核心表数 | V1.1 变化 |
|--------|------|--------|--------|
| `mes_ai_task` | AI 任务全生命周期管理 | 10 | 新增 `ai_seq_counter`；`ai_exec_log` 新增 3 个字段 |
| `mes_ai_monitor` | 系统运维监控 | 3 | 无变化 |
| `mes_ai_knowledge` | 知识库与断言库 | 5 | `ai_kb_chunk` 新增 3 个字段；`ai_assertion_batch` 新增 3 个字段；新增 `ai_token_stat` |
| `mes_ai_audit` | 安全审计 | 3 | 无变化 |

### 1.2 技术选型

| 技术项 | 选型 | 说明 |
|--------|------|------|
| 数据库引擎 | MySQL 8.0.x | 与 MES 主系统保持一致，充分利用 8.0 分区与窗口函数特性 |
| 字符集 | utf8mb4 / utf8mb4_unicode_ci | 完整支持中文及 emoji，统一全库字符集 |
| 存储引擎 | InnoDB | 全部表使用 InnoDB，支持事务、行锁 |
| 时间字段 | DATETIME | 精度到秒，业务层统一 UTC+8 存储 |
| 主键策略 | BIGINT AUTO_INCREMENT | 单机顺序自增，分布式扩展时切换为 Snowflake |
| 序列号策略 | Redis INCR + 日期后缀 | `task_no` 等业务编号使用分布式递增，见第八章 |
| ORM 框架 | MyBatis Plus 3.x | 配合 Spring Boot 2.7 |

### 1.3 命名规范

| 对象类型 | 命名规则 | 示例 |
|--------|--------|------|
| Schema | `mes_ai_{模块}` | `mes_ai_task` |
| 表名 | 全小写 snake_case，含业务前缀 | `ai_task_req`, `ai_exec_log` |
| 字段名 | 全小写 snake_case | `task_no`, `created_at` |
| 主键 | `id`（BIGINT） | `id` |
| 外键字段 | `{关联表名}_id` | `task_id` |
| 状态字段 | `status`（VARCHAR） | `status`, `sync_status` |
| 时间字段 | `{动作}_at` / `{动作}_time` | `created_at`, `last_sync_at` |
| 布尔字段 | `is_{描述}`（TINYINT 0/1） | `is_deleted`, `is_active` |
| 索引 | `idx_{表名简写}_{字段}` | `idx_task_req_status` |
| 唯一索引 | `uniq_{表名简写}_{字段}` | `uniq_task_req_no` |

---

## 二、实体关系模型（ERD）

### 2.1 核心实体关系

| 主实体 | 关系 | 从实体 | 关联字段 | 说明 |
|--------|------|--------|--------|------|
| `ai_task_req` | 1:N | `ai_task_history` | `task_id` | 每张需求单有多条状态变更历史 |
| `ai_task_req` | 1:N | `ai_exec_log` | `task_id` | 每张需求单有多条 AI 调用日志 |
| `ai_task_req` | 1:N | `ai_code_artifact` | `task_id` | 每张需求单可生成多个代码文件 |
| `ai_task_req` | 1:N | `ai_test_report` | `task_id` | 每张需求单有一份或多份测试报告 |
| `ai_task_req` | 1:1 | `ai_review_record` | `task_id` | 每张需求单有唯一一条 IT 评审记录 |
| `ai_task_req` | 1:1 | `ai_deploy_record` | `task_id` | 每张需求单有唯一一条部署审批记录 |
| `ai_task_req` | 1:N | `ai_approval_gate` | `task_id` | 每张需求单可有多个人工授权节点 |
| `ai_task_req` | 1:N | `ai_assertion_batch` | `related_task_id` | **[V1.1新增]** 任务触发的断言批次 |
| `ai_code_artifact` | N:1 | `ai_assertion_batch` | `related_commit_hash` | **[V1.1新增]** 代码提交对应的断言验证批次 |
| `ai_inspection_report` | 1:N | `ai_alert_record` | `inspection_id` | 每份巡检报告可产生多条告警 |
| `ai_kb_document` | 1:N | `ai_kb_chunk` | `doc_id` | 每个文档切分为多个向量块 |
| `ai_assertion` | 1:N | `ai_assertion_run` | `assertion_id` | 每个断言可被多次执行 |
| `ai_assertion_batch` | 1:N | `ai_assertion_run` | `run_batch_id` | 每个批次包含多条断言执行记录 |

### 2.2 V1.1 新增关键链路图

```
代码变更链路（版本联动追溯）：
─────────────────────────────────────────────────────────────────────
ai_task_req          ai_code_artifact         ai_assertion_batch
(related_task_id) ←── task_id           commit_hash ──► related_commit_hash
       └─────────────────────────────────────────► related_task_id
                                                        │
                                               trigger_source = 'PROMPT_CHANGE'
                                                        │
                                               block_action = 'BLOCKED/PASSED'
                                                        │
                                               ai_assertion_run (明细)
─────────────────────────────────────────────────────────────────────

Token 成本分摊链路（ROI 分析）：
─────────────────────────────────────────────────────────────────────
ai_exec_log                          ai_token_stat（汇总）
  dept ────────────────────────────► dept
  module ──────────────────────────► module
  estimated_cost_cny ─────────────► total_cost_cny
  task_type（来自 ai_task_req）────► task_type
─────────────────────────────────────────────────────────────────────

向量同步状态链路：
─────────────────────────────────────────────────────────────────────
ai_kb_document ──► ai_kb_chunk
                      sync_status = 'SUCCESS' / 'PENDING' / 'FAILED'
                      last_sync_error（失败原因）
                      AI 检索时 WHERE sync_status = 'SUCCESS'
─────────────────────────────────────────────────────────────────────
```

### 2.3 需求单状态机（`ai_task_req.status`）

```
DRAFT ──► SUBMITTED ──► REVIEWING ──► REJECTED ──► DRAFT（修改重提）
                              │
                              ▼ IT 批准
                          APPROVED
                              │
                              ▼ 系统调度
                         AI_RUNNING ◄── PENDING_REVIEW（退回重做）
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
            PENDING_REVIEW           FAILED
                    │                   │
                    ▼ 验收通过           ▼ 重新执行
                 ACCEPTED           AI_RUNNING
                    │
                    ▼ IT 签批
                 DEPLOYING
                    │
            ┌───────┴───────┐
            ▼               ▼
          CLOSED         ROLLBACK
```

| 当前状态 | 允许流转到 | 触发条件 | 操作人 |
|--------|--------|--------|------|
| `DRAFT` | `SUBMITTED` | 业务人员点击提交 | 业务人员 |
| `SUBMITTED` | `REVIEWING` | IT 专员领取评审 | IT 专员 |
| `REVIEWING` | `APPROVED` / `REJECTED` | IT 评审结论 | IT 专员 |
| `REJECTED` | `DRAFT` | 业务人员修改后重新提交 | 业务人员 |
| `APPROVED` | `AI_RUNNING` | IT 专员或系统自动调度 | 系统/IT |
| `AI_RUNNING` | `PENDING_REVIEW` / `FAILED` | AI 完成或异常终止 | 系统/AI |
| `FAILED` | `AI_RUNNING` / `REJECTED` | 技术负责人决策 | 技术负责人 |
| `PENDING_REVIEW` | `ACCEPTED` / `AI_RUNNING` | 甲方验收结论 | IT + 业务 |
| `ACCEPTED` | `DEPLOYING` | IT 负责人签批上线 | IT 负责人 |
| `DEPLOYING` | `CLOSED` / `ROLLBACK` | 部署成功或失败回退 | 系统/IT |

---

## 三、Schema 详细设计

### 3.1 Schema: `mes_ai_task`（任务管理）

---

#### 3.1.1 `ai_task_req`（需求主表）

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `task_no` | VARCHAR(32) | ✓ | — | 任务编号 `REQ-MES-AI-YYYYMMDD-NNN`，由 Redis 分布式递增生成，唯一索引 |
| `title` | VARCHAR(100) | ✓ | — | 需求标题，不超过 50 汉字 |
| `task_type` | VARCHAR(20) | ✓ | — | 任务类型：`FEAT`/`FIX`/`REPORT`/`QUERY`/`API`/`BUG`/`PERF` |
| `priority` | TINYINT | ✓ | `3` | 优先级：1-紧急 2-高 3-中 4-低 |
| `status` | VARCHAR(20) | ✓ | `'DRAFT'` | 状态机，见 2.3 节 |
| `submitter_id` | BIGINT | ✓ | — | 提交人用户 ID |
| `submitter_name` | VARCHAR(50) | ✓ | — | 提交人姓名（冗余自用户表，避免跨库 JOIN） |
| `dept` | VARCHAR(50) | ✓ | — | 所属部门（用于成本分摊统计） |
| `module` | VARCHAR(50) | ✗ | NULL | 所属 MES 模块（用于成本分摊统计） |
| `biz_background` | TEXT | ✗ | NULL | 业务背景描述 |
| `func_desc` | TEXT | ✗ | NULL | 功能详细描述 |
| `input_data` | TEXT | ✗ | NULL | 输入数据说明 |
| `expected_output` | TEXT | ✗ | NULL | 期望输出说明 |
| `biz_rules` | TEXT | ✗ | NULL | 业务规则及计算公式 |
| `modules_involved` | VARCHAR(200) | ✗ | NULL | 涉及模块（逗号分隔） |
| `device_involved` | VARCHAR(200) | ✗ | NULL | 涉及设备型号及通讯方式 |
| `accept_criteria` | TEXT | ✗ | NULL | 验收标准（JSON 数组，每项含 condition/expected/result） |
| `perf_requirement` | VARCHAR(500) | ✗ | NULL | 性能要求 |
| `expected_finish_date` | DATE | ✗ | NULL | 期望完成日期 |
| `estimated_hours` | DECIMAL(6,1) | ✗ | NULL | AI 预估执行工时（小时） |
| `actual_hours` | DECIMAL(6,1) | ✗ | NULL | AI 实际执行工时（小时） |
| `quality_score` | TINYINT | ✗ | NULL | 综合质量评分（0-100） |
| `remark` | TEXT | ✗ | NULL | 备注 |
| `is_deleted` | TINYINT(1) | ✓ | `0` | 逻辑删除：0-有效 1-已删除 |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 创建时间（UTC+8） |
| `updated_at` | DATETIME | ✓ | CURRENT_TIMESTAMP ON UPDATE | 最后更新时间（UTC+8） |

> ⛔ `task_no` 由应用层通过 Redis 分布式递增生成，禁止在数据库层自动生成，禁止手动修改。生成规范见第八章 8.4 节。

---

#### 3.1.2 `ai_task_history`（操作历史表）

**数据只增不改不删，保留 3 年。**

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `task_id` | BIGINT | ✓ | — | 关联 `ai_task_req.id` |
| `task_no` | VARCHAR(32) | ✓ | — | 冗余任务编号，便于日志独立查询 |
| `operator` | VARCHAR(50) | ✓ | — | 操作人账号（系统操作填 `SYSTEM`/`AI`） |
| `operator_role` | VARCHAR(20) | ✓ | — | 操作人角色：`USER`/`AI`/`IT`/`MANAGER` |
| `action` | VARCHAR(50) | ✓ | — | 操作动作：`SUBMIT`/`APPROVE`/`REJECT`/`START`/`COMPLETE` 等 |
| `from_status` | VARCHAR(20) | ✗ | NULL | 变更前状态 |
| `to_status` | VARCHAR(20) | ✗ | NULL | 变更后状态 |
| `ip_address` | VARCHAR(50) | ✗ | NULL | 操作人 IP（脱敏后存储） |
| `remark` | TEXT | ✗ | NULL | 操作备注 |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 操作时间（精确到秒，只增不改） |

---

#### 3.1.3 `ai_exec_log`（AI 执行日志表）

**V1.1 新增字段：`dept`、`module`、`estimated_cost_cny`，用于 Token 成本分摊与 ROI 分析。**

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `task_id` | BIGINT | ✓ | — | 关联任务 ID |
| `task_no` | VARCHAR(32) | ✓ | — | 冗余任务编号 |
| `dept` | VARCHAR(50) | ✗ | NULL | **[V1.1新增]** 所属部门（从 ai_task_req 冗余，用于成本分摊） |
| `module` | VARCHAR(50) | ✗ | NULL | **[V1.1新增]** 所属 MES 模块（从 ai_task_req 冗余，用于成本分摊） |
| `call_seq` | INT | ✓ | — | 本任务内调用序号（从 1 开始） |
| `model_name` | VARCHAR(50) | ✓ | — | 调用的模型名称，如 `claude-sonnet-4` |
| `log_type` | VARCHAR(10) | ✓ | — | 日志类型：`INFO`/`WARN`/`ERROR`/`OUTPUT` |
| `stage` | VARCHAR(30) | ✓ | — | 执行阶段：`UNDERSTAND`/`PLAN`/`CODEGEN`/`TEST`/`REPORT` |
| `prompt_hash` | CHAR(64) | ✗ | NULL | Prompt 内容 SHA256，便于查重与审计 |
| `prompt_tokens` | INT | ✓ | `0` | 本次调用 Prompt 端消耗 Token 数 |
| `completion_tokens` | INT | ✓ | `0` | 本次调用 Completion 端消耗 Token 数 |
| `total_tokens` | INT | ✓ | `0` | 本次调用合计 Token 数 |
| `estimated_cost_cny` | DECIMAL(8,4) | ✗ | NULL | **[V1.1新增]** 本次调用预估费用（人民币元），按模型单价实时计算写入 |
| `latency_ms` | INT | ✗ | NULL | API 响应延迟（毫秒） |
| `content` | MEDIUMTEXT | ✗ | NULL | 日志内容（必须已脱敏） |
| `is_desensitized` | TINYINT(1) | ✓ | `1` | 是否已脱敏（必须为 1 才可写入，强制校验） |
| `error_code` | VARCHAR(50) | ✗ | NULL | 错误码（正常时为 NULL） |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 日志时间（UTC+8） |

> ⛔ `is_desensitized=0` 的记录禁止写入。`estimated_cost_cny` 由应用层在写入时按当前模型单价计算，单价配置统一维护在系统配置表中。

---

#### 3.1.4 `ai_code_artifact`（代码交付物表）

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `task_id` | BIGINT | ✓ | — | 关联任务 ID |
| `file_path` | VARCHAR(500) | ✓ | — | 文件在 Git 仓库中的相对路径 |
| `file_type` | VARCHAR(20) | ✓ | — | 文件类型：`JAVA`/`VUE`/`SQL`/`XML`/`MD`/`TEST` |
| `file_size_bytes` | INT | ✗ | NULL | 文件字节大小 |
| `lines_of_code` | INT | ✗ | NULL | 代码行数（不含注释和空行） |
| `git_commit_hash` | CHAR(40) | ✗ | NULL | 文件对应的 Git Commit Hash（关联 `ai_assertion_batch.related_commit_hash`） |
| `git_branch` | VARCHAR(100) | ✗ | NULL | 所在 Git 分支 |
| `has_hardcode` | TINYINT(1) | ✓ | `0` | 硬编码扫描结果：0-通过 1-有违规 |
| `sonar_status` | VARCHAR(20) | ✗ | NULL | SonarQube 扫描状态：`PASS`/`FAIL`/`PENDING` |
| `sonar_critical_count` | INT | ✓ | `0` | SonarQube Critical 级别问题数（目标=0） |
| `remark` | VARCHAR(500) | ✗ | NULL | 备注 |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 代码生成时间 |

---

#### 3.1.5 `ai_test_report`（测试报告表）

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `task_id` | BIGINT | ✓ | — | 关联任务 ID |
| `report_type` | VARCHAR(20) | ✓ | — | 报告类型：`UNIT`/`API`/`REGRESSION`/`MANUAL` |
| `test_tool` | VARCHAR(50) | ✗ | NULL | 测试工具：`JUnit`/`Postman`/`GoReplay`/`Manual` |
| `total_cases` | INT | ✓ | `0` | 测试用例总数 |
| `passed_cases` | INT | ✓ | `0` | 通过用例数 |
| `failed_cases` | INT | ✓ | `0` | 失败用例数 |
| `coverage_pct` | DECIMAL(5,2) | ✗ | NULL | 代码覆盖率（%），目标 ≥ 70% |
| `p0_diff_count` | INT | ✓ | `0` | 回归测试 P0 级差异数（目标=0，否则阻断） |
| `p1_diff_count` | INT | ✓ | `0` | 回归测试 P1 级差异数（目标<3） |
| `report_summary` | TEXT | ✗ | NULL | 报告摘要（AI 自动生成） |
| `report_detail_url` | VARCHAR(500) | ✗ | NULL | 详细报告文件路径或外部链接 |
| `is_passed` | TINYINT(1) | ✓ | `0` | 是否通过：1-通过 0-未通过 |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 报告生成时间 |

---

#### 3.1.6 `ai_review_record`（IT 评审记录）

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `task_id` | BIGINT | ✓ | — | 关联任务 ID（唯一索引，一单一评审） |
| `reviewer_id` | BIGINT | ✓ | — | IT 评审人用户 ID |
| `reviewer_name` | VARCHAR(50) | ✓ | — | IT 评审人姓名 |
| `review_result` | VARCHAR(20) | ✓ | — | 评审结论：`APPROVED`/`REJECTED`/`PENDING_INFO` |
| `review_opinion` | TEXT | ✗ | NULL | 评审意见 |
| `estimated_hours` | DECIMAL(6,1) | ✗ | NULL | 评审人预估 AI 执行工时（小时） |
| `assign_mode` | VARCHAR(20) | ✓ | `'AUTO'` | 分配方式：`AUTO`/`MANUAL` |
| `plan_start_time` | DATETIME | ✗ | NULL | 计划开始执行时间 |
| `review_time` | DATETIME | ✓ | CURRENT_TIMESTAMP | 评审完成时间 |

---

#### 3.1.7 `ai_approval_gate`（人工授权网关记录）

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `task_id` | BIGINT | ✓ | — | 关联任务 ID |
| `gate_type` | VARCHAR(30) | ✓ | — | 授权类型：`PLAN_CONFIRM`/`DDL_CHANGE`/`DEPLOY`/`EMERGENCY` |
| `gate_title` | VARCHAR(200) | ✓ | — | 授权事项标题 |
| `gate_content` | TEXT | ✗ | NULL | 待授权内容摘要（AI 生成的方案说明） |
| `status` | VARCHAR(20) | ✓ | `'PENDING'` | 授权状态：`PENDING`/`APPROVED`/`REJECTED`/`TIMEOUT` |
| `approver_id` | BIGINT | ✗ | NULL | 授权人用户 ID |
| `approver_name` | VARCHAR(50) | ✗ | NULL | 授权人姓名 |
| `approver_ip` | VARCHAR(50) | ✗ | NULL | 授权人操作 IP（脱敏后存储） |
| `approve_remark` | TEXT | ✗ | NULL | 授权备注 |
| `expire_at` | DATETIME | ✓ | — | 授权超时时间 |
| `approved_at` | DATETIME | ✗ | NULL | 实际授权时间 |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 授权请求创建时间 |

> ⛔ 授权记录禁止物理删除，保留期限不少于 3 年（合规审计要求）。

---

#### 3.1.8 `ai_deploy_record`（部署记录表）

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `task_id` | BIGINT | ✓ | — | 关联任务 ID（唯一索引） |
| `applicant_id` | BIGINT | ✓ | — | 申请部署人员用户 ID |
| `plan_deploy_time` | DATETIME | ✓ | — | 计划部署时间 |
| `rollback_plan` | TEXT | ✓ | — | 回退方案（必填，AI 生成草稿，IT 审核确认） |
| `approver_id` | BIGINT | ✗ | NULL | IT 负责人审批人用户 ID |
| `approve_result` | VARCHAR(20) | ✗ | NULL | 审批结论：`APPROVED`/`REJECTED` |
| `approve_time` | DATETIME | ✗ | NULL | 审批时间 |
| `actual_deploy_time` | DATETIME | ✗ | NULL | 实际部署时间 |
| `deploy_result` | VARCHAR(20) | ✗ | NULL | 部署结果：`SUCCESS`/`ROLLBACK`/`PARTIAL` |
| `deploy_log` | TEXT | ✗ | NULL | 部署执行日志摘要 |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 记录创建时间 |

---

#### 3.1.9 `ai_token_daily`（Token 日消耗汇总表）

> 注意：V1.1 新增了多维度汇总表 `ai_token_stat`（见 3.3.6 节），`ai_token_daily` 保留用于简单的日总量监控与预算预警，`ai_token_stat` 用于细粒度的 ROI 报告。

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `stat_date` | DATE | ✓ | — | 统计日期 |
| `model_name` | VARCHAR(50) | ✓ | — | 模型名称 |
| `total_calls` | INT | ✓ | `0` | 当日 API 调用总次数 |
| `prompt_tokens` | BIGINT | ✓ | `0` | 当日 Prompt Token 总量 |
| `completion_tokens` | BIGINT | ✓ | `0` | 当日 Completion Token 总量 |
| `total_tokens` | BIGINT | ✓ | `0` | 当日合计 Token 总量 |
| `budget_limit` | BIGINT | ✓ | `3000000` | 当日预算上限（默认 300 万 Token/天） |
| `alert_triggered` | TINYINT(1) | ✓ | `0` | 是否触发超限告警：1-已告警 |
| `total_cost_cny` | DECIMAL(10,4) | ✗ | NULL | 当日实际总费用（人民币元，由 ai_exec_log 聚合） |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 汇总写入时间 |
| `updated_at` | DATETIME | ✓ | CURRENT_TIMESTAMP ON UPDATE | 最后更新时间 |

---

#### 3.1.10 `ai_seq_counter`（序列号计数表）【V1.1 新增】

用于在 Redis 不可用时的降级兜底，正常情况下序列号由 Redis 生成。

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `seq_key` | VARCHAR(50) | ✓ | — | 序列号键，如 `TASK_NO_20260411`，唯一索引 |
| `seq_type` | VARCHAR(20) | ✓ | — | 序列号类型：`TASK_NO`/`REPORT_NO`/`BATCH_NO` 等 |
| `current_val` | INT | ✓ | `0` | 当前已使用的最大序号 |
| `date_str` | CHAR(8) | ✓ | — | 日期字符串 `YYYYMMDD`（序列号按天重置） |
| `remark` | VARCHAR(200) | ✗ | NULL | 备注 |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 创建时间 |
| `updated_at` | DATETIME | ✓ | CURRENT_TIMESTAMP ON UPDATE | 更新时间 |

> ⚠ 本表仅作为 Redis 故障时的降级方案，正常运行时不写入此表。应用层需实现自动切换逻辑，详见第八章 8.4 节。

---

### 3.2 Schema: `mes_ai_monitor`（运维监控）

---

#### 3.2.1 `ai_inspection_report`（巡检报告主表）

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `report_no` | VARCHAR(32) | ✓ | — | 报告编号 `INSP-MES-AI-YYYYMMDD`，唯一索引 |
| `inspect_date` | DATE | ✓ | — | 巡检日期 |
| `inspect_start_time` | DATETIME | ✓ | — | 巡检开始时间 |
| `inspect_end_time` | DATETIME | ✗ | NULL | 巡检结束时间 |
| `overall_status` | VARCHAR(20) | ✓ | — | 整体状态：`NORMAL`/`WARNING`/`CRITICAL` |
| `alert_count` | INT | ✓ | `0` | 告警总数 |
| `critical_count` | INT | ✓ | `0` | Critical 级告警数 |
| `error_log_summary` | TEXT | ✗ | NULL | 近 24h ERROR 日志摘要（去重，按频次排序） |
| `slow_sql_count` | INT | ✓ | `0` | 首次巡检发现的慢 SQL 数量（执行 >2 秒） |
| `disk_usage_pct` | DECIMAL(5,2) | ✗ | NULL | 磁盘使用率（%），告警阈值 80% |
| `memory_usage_pct` | DECIMAL(5,2) | ✗ | NULL | 内存使用率（%），告警阈值 85% |
| `db_conn_active` | INT | ✗ | NULL | 数据库当前活跃连接数 |
| `report_content` | LONGTEXT | ✗ | NULL | 完整报告内容（Markdown 格式） |
| `ai_suggestions` | TEXT | ✗ | NULL | AI 自动生成的处置建议 |
| `it_confirm_status` | VARCHAR(20) | ✗ | NULL | IT 确认状态：`PENDING`/`CONFIRMED`/`ESCALATED` |
| `it_confirm_user` | VARCHAR(50) | ✗ | NULL | IT 确认人姓名 |
| `it_confirm_time` | DATETIME | ✗ | NULL | IT 确认时间 |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 报告生成时间 |

---

#### 3.2.2 `ai_alert_record`（告警记录表）

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `inspection_id` | BIGINT | ✗ | NULL | 关联巡检报告 ID（实时告警可为 NULL） |
| `alert_type` | VARCHAR(50) | ✓ | — | 告警类型：`DISK`/`MEMORY`/`SERVICE_DOWN`/`SLOW_SQL`/`ERROR_LOG`/`API_FAIL` |
| `alert_level` | VARCHAR(10) | ✓ | — | 告警级别：`CRITICAL`/`HIGH`/`MEDIUM`/`LOW` |
| `alert_title` | VARCHAR(200) | ✓ | — | 告警标题 |
| `alert_content` | TEXT | ✗ | NULL | 告警详细内容 |
| `metric_name` | VARCHAR(100) | ✗ | NULL | 指标名称（如 `disk_usage_pct`） |
| `metric_value` | DECIMAL(12,4) | ✗ | NULL | 触发告警时的指标实测值 |
| `threshold_value` | DECIMAL(12,4) | ✗ | NULL | 告警阈值 |
| `notify_sent` | TINYINT(1) | ✓ | `0` | 是否已发送通知：1-已发送 |
| `notify_channel` | VARCHAR(50) | ✗ | NULL | 通知渠道：`WECHAT_BOT`/`EMAIL`/`SMS` |
| `resolve_status` | VARCHAR(20) | ✓ | `'OPEN'` | 处理状态：`OPEN`/`PROCESSING`/`RESOLVED`/`IGNORED` |
| `resolve_time` | DATETIME | ✗ | NULL | 解决时间 |
| `resolve_remark` | VARCHAR(500) | ✗ | NULL | 处理说明 |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 告警产生时间 |

---

#### 3.2.3 `ai_slow_sql_record`（慢 SQL 记录）

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `inspection_id` | BIGINT | ✗ | NULL | 关联巡检报告 ID |
| `db_schema` | VARCHAR(50) | ✓ | — | 数据库 Schema 名 |
| `sql_digest` | CHAR(64) | ✓ | — | SQL 模板 SHA256（参数化后计算，用于去重聚合） |
| `sql_template` | TEXT | ✗ | NULL | SQL 语句模板（参数替换为占位符 `?`） |
| `exec_count` | INT | ✓ | `1` | 统计周期内执行次数 |
| `avg_exec_ms` | INT | ✓ | — | 平均执行时间（毫秒） |
| `max_exec_ms` | INT | ✓ | — | 最慢一次执行时间（毫秒） |
| `rows_examined_avg` | BIGINT | ✗ | NULL | 平均扫描行数 |
| `has_index_suggestion` | TINYINT(1) | ✓ | `0` | AI 是否已生成索引优化建议 |
| `index_suggestion` | TEXT | ✗ | NULL | AI 生成的索引优化 SQL |
| `resolve_status` | VARCHAR(20) | ✓ | `'OPEN'` | 处理状态：`OPEN`/`PROCESSING`/`RESOLVED` |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 记录时间 |

---

### 3.3 Schema: `mes_ai_knowledge`（知识库与断言库）

---

#### 3.3.1 `ai_kb_document`（知识库文档元数据）

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `doc_code` | VARCHAR(50) | ✓ | — | 文档编码（唯一），如 `KB-DB-001` |
| `doc_name` | VARCHAR(200) | ✓ | — | 文档名称 |
| `doc_type` | VARCHAR(30) | ✓ | — | 文档类型：`DB_SCHEMA`/`API`/`FLOW`/`DEVICE`/`HISTORY`/`CODE`/`STANDARD` |
| `module` | VARCHAR(50) | ✗ | NULL | 所属 MES 模块 |
| `source_path` | VARCHAR(500) | ✗ | NULL | 原始文档存储路径 |
| `file_format` | VARCHAR(20) | ✗ | NULL | 原始格式：`PDF`/`WORD`/`EXCEL`/`SQL`/`MD` |
| `version` | VARCHAR(20) | ✓ | `'1.0'` | 文档版本号 |
| `chunk_count` | INT | ✓ | `0` | 已切分的向量块总数 |
| `synced_chunk_count` | INT | ✓ | `0` | 已成功同步至向量数据库的块数（`sync_status=SUCCESS`） |
| `vector_status` | VARCHAR(20) | ✓ | `'PENDING'` | 整体向量化状态：`PENDING`/`PROCESSING`/`DONE`/`PARTIAL`/`FAILED` |
| `last_vectorized_at` | DATETIME | ✗ | NULL | 最近一次向量化完成时间 |
| `is_active` | TINYINT(1) | ✓ | `1` | 是否启用（逻辑删除用） |
| `created_by` | VARCHAR(50) | ✓ | — | 录入人 |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 录入时间 |
| `updated_at` | DATETIME | ✓ | CURRENT_TIMESTAMP ON UPDATE | 更新时间 |

---

#### 3.3.2 `ai_kb_chunk`（知识块索引表）

**V1.1 新增字段：`sync_status`、`last_sync_at`、`last_sync_error`，确保 AI 检索只命中已成功同步的块。**

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `doc_id` | BIGINT | ✓ | — | 关联 `ai_kb_document.id` |
| `chunk_index` | INT | ✓ | — | 块在文档中的序号（从 0 开始） |
| `vector_id` | VARCHAR(100) | ✗ | NULL | 向量数据库中的记录 ID（同步成功后才写入） |
| `chunk_text` | TEXT | ✓ | — | 块文本内容（用于召回后展示） |
| `token_count` | INT | ✓ | — | 块的 Token 数量（512-1024 token） |
| `start_char` | INT | ✗ | NULL | 块在原文中的起始字符位置 |
| `end_char` | INT | ✗ | NULL | 块在原文中的结束字符位置 |
| `sync_status` | VARCHAR(20) | ✓ | `'PENDING'` | **[V1.1新增]** 向量同步状态：`PENDING`/`SYNCING`/`SUCCESS`/`FAILED` |
| `last_sync_at` | DATETIME | ✗ | NULL | **[V1.1新增]** 最近一次同步操作时间 |
| `last_sync_error` | TEXT | ✗ | NULL | **[V1.1新增]** 最近一次同步失败的错误信息（成功时置 NULL） |
| `sync_retry_count` | TINYINT | ✓ | `0` | **[V1.1新增]** 同步失败重试次数（超过 3 次停止重试，人工介入） |
| `hit_count` | INT | ✓ | `0` | 被检索命中的累计次数 |
| `last_hit_at` | DATETIME | ✗ | NULL | 最近一次被命中时间 |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 切块时间 |

> ⚠ AI 检索调用时，查询条件必须包含 `WHERE sync_status = 'SUCCESS'`，禁止查询未完成同步的块，避免无效召回影响生成质量。

**`sync_status` 状态流转：**

```
PENDING ──► SYNCING ──► SUCCESS（向量 ID 写入，可被检索）
                └──────► FAILED（记录 last_sync_error，retry_count +1）
                              │ retry_count < 3：自动重试
                              │ retry_count ≥ 3：停止重试，人工介入
                              ▼
                          FAILED（最终态，等待人工处理）
```

---

#### 3.3.3 `ai_assertion`（业务逻辑断言定义表）

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `assertion_id` | VARCHAR(20) | ✓ | — | 断言编号，如 `SM-WO-001`，唯一索引 |
| `assertion_name` | VARCHAR(200) | ✓ | — | 断言名称 |
| `category` | VARCHAR(30) | ✓ | — | 断言分类：`STATE_MACHINE`/`SQL_LOGIC`/`API_BEHAVIOR`/`CODE_GEN` |
| `priority` | VARCHAR(10) | ✓ | — | 优先级：`CRITICAL`/`HIGH`/`MEDIUM` |
| `description` | TEXT | ✓ | — | 断言说明 |
| `prompt_text` | TEXT | ✓ | — | 发给 AI 的测试 Prompt |
| `expected_keywords` | TEXT | ✓ | — | 期望响应中包含的关键词（JSON 数组） |
| `expected_excludes` | TEXT | ✗ | NULL | 响应中不应出现的词（JSON 数组） |
| `scoring_method` | VARCHAR(30) | ✓ | `'keyword_match'` | 评分方式：`keyword_match`/`llm_judge` |
| `pass_threshold` | DECIMAL(4,2) | ✓ | `0.90` | 通过阈值（0.0-1.0） |
| `related_module` | VARCHAR(50) | ✗ | NULL | 关联 MES 模块 |
| `is_active` | TINYINT(1) | ✓ | `1` | 是否启用 |
| `created_by` | VARCHAR(50) | ✓ | — | 创建人 |
| `approved_by` | VARCHAR(50) | ✗ | NULL | 技术负责人审批人（修改须审批） |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 创建时间 |
| `updated_at` | DATETIME | ✓ | CURRENT_TIMESTAMP ON UPDATE | 更新时间 |

---

#### 3.3.4 `ai_assertion_run`（断言执行记录表）

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `run_batch_id` | VARCHAR(50) | ✓ | — | 批次 ID（同一次触发共享） |
| `assertion_id` | BIGINT | ✓ | — | 关联断言定义 ID |
| `trigger_type` | VARCHAR(30) | ✓ | — | 触发类型：`MODEL_UPGRADE`/`PROMPT_CHANGE`/`SCHEDULED` |
| `model_name` | VARCHAR(50) | ✓ | — | 测试时使用的模型版本 |
| `ai_response` | TEXT | ✗ | NULL | AI 原始响应内容（脱敏后） |
| `keyword_hit_rate` | DECIMAL(4,2) | ✗ | NULL | 关键词命中率（0.0-1.0） |
| `exclude_violation` | TINYINT(1) | ✓ | `0` | 是否触发排除词：1-有违反 |
| `is_passed` | TINYINT(1) | ✓ | `0` | 本条断言是否通过：1-通过 |
| `score` | DECIMAL(4,2) | ✗ | NULL | 综合评分 |
| `fail_reason` | TEXT | ✗ | NULL | 失败原因（通过时为 NULL） |
| `latency_ms` | INT | ✗ | NULL | API 响应延迟（毫秒） |
| `tokens_used` | INT | ✓ | `0` | 本次测试消耗 Token 数 |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 执行时间 |

---

#### 3.3.5 `ai_assertion_batch`（断言批次汇总表）

**V1.1 新增字段：`related_task_id`、`related_commit_hash`、`trigger_source`，实现代码变更与断言验证的完整链路追踪。**

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `run_batch_id` | VARCHAR(50) | ✓ | — | 批次 ID，唯一索引，格式 `RUN-YYYYMMDD-HHMM` |
| `trigger_type` | VARCHAR(30) | ✓ | — | 触发类型：`MODEL_UPGRADE`/`PROMPT_CHANGE`/`SCHEDULED` |
| `trigger_source` | VARCHAR(200) | ✗ | NULL | **[V1.1新增]** 触发来源描述（如 Prompt 文件路径、模型版本变更说明） |
| `related_task_id` | BIGINT | ✗ | NULL | **[V1.1新增]** 关联触发此次断言的任务 ID（`PROMPT_CHANGE` 类型必填） |
| `related_commit_hash` | CHAR(40) | ✗ | NULL | **[V1.1新增]** 关联触发此次断言的 Git Commit Hash（与 `ai_code_artifact.git_commit_hash` 关联） |
| `model_name` | VARCHAR(50) | ✓ | — | 测试模型版本 |
| `total_count` | INT | ✓ | `0` | 本批次断言总数 |
| `passed_count` | INT | ✓ | `0` | 通过数 |
| `critical_failed` | INT | ✓ | `0` | Critical 级失败数（目标=0，否则 BLOCKED） |
| `high_failed` | INT | ✓ | `0` | High 级失败数（目标<3） |
| `medium_failed` | INT | ✓ | `0` | Medium 级失败数（目标<5） |
| `pass_rate_pct` | DECIMAL(5,2) | ✓ | — | 全量通过率（%），目标 ≥ 95% |
| `block_action` | VARCHAR(20) | ✓ | — | 阻断动作：`BLOCKED`/`WARNED`/`PASSED` |
| `notified` | TINYINT(1) | ✓ | `0` | 是否已发送通知 |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 批次开始时间 |
| `finished_at` | DATETIME | ✗ | NULL | 批次完成时间 |

**版本联动追溯查询示例：**

```sql
-- 查询某次代码提交触发的断言验证结果，以及最终阻断决策
SELECT
    b.run_batch_id,
    b.trigger_type,
    b.trigger_source,
    b.related_task_id,
    b.related_commit_hash,
    b.critical_failed,
    b.pass_rate_pct,
    b.block_action,
    b.created_at AS test_time
FROM ai_assertion_batch b
WHERE b.related_commit_hash = 'abc123...'
ORDER BY b.created_at DESC;

-- 从代码交付物反查断言验证情况
SELECT
    a.file_path,
    a.git_commit_hash,
    b.pass_rate_pct,
    b.block_action,
    b.critical_failed
FROM ai_code_artifact a
LEFT JOIN ai_assertion_batch b ON a.git_commit_hash = b.related_commit_hash
WHERE a.task_id = 123;
```

---

#### 3.3.6 `ai_token_stat`（Token 多维度汇总表）【V1.1 新增】

支持按部门、模块、任务类型、模型生成月度 ROI 分析报告。

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `stat_date` | DATE | ✓ | — | 统计日期 |
| `stat_month` | CHAR(7) | ✓ | — | 统计月份 `YYYY-MM`（冗余，用于月度汇总查询） |
| `model_name` | VARCHAR(50) | ✓ | — | 模型名称 |
| `dept` | VARCHAR(50) | ✓ | — | 部门（`ALL` 表示全部门汇总行） |
| `module` | VARCHAR(50) | ✓ | — | MES 模块（`ALL` 表示全模块汇总行） |
| `task_type` | VARCHAR(20) | ✓ | — | 任务类型（`ALL` 表示全类型汇总行） |
| `total_calls` | INT | ✓ | `0` | 该维度当日调用总次数 |
| `total_tokens` | BIGINT | ✓ | `0` | 该维度当日 Token 总量 |
| `total_cost_cny` | DECIMAL(10,4) | ✓ | `0.0000` | 该维度当日总费用（人民币元） |
| `task_count` | INT | ✓ | `0` | 该维度当日任务数 |
| `avg_cost_per_task` | DECIMAL(8,4) | ✗ | NULL | 该维度当日单任务平均费用（人民币元） |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 汇总写入时间 |

> ⚠ 本表由每日定时任务从 `ai_exec_log` 聚合写入，幂等执行（先 DELETE 当日数据，再 INSERT）。`dept`/`module`/`task_type` 使用 `ALL` 作为通配符维度，实现多层级汇总。

**ROI 报告查询示例：**

```sql
-- 月度各部门 Token 费用汇总（领导汇报用）
SELECT
    dept,
    SUM(total_cost_cny)    AS month_cost_cny,
    SUM(total_tokens)      AS month_tokens,
    SUM(task_count)        AS month_tasks,
    ROUND(SUM(total_cost_cny) / NULLIF(SUM(task_count), 0), 4) AS avg_cost_per_task
FROM ai_token_stat
WHERE stat_month = '2026-04'
  AND module   = 'ALL'
  AND task_type = 'ALL'
  AND dept    != 'ALL'
GROUP BY dept
ORDER BY month_cost_cny DESC;

-- 月度各模块费用占比
SELECT
    module,
    SUM(total_cost_cny) AS month_cost_cny,
    ROUND(SUM(total_cost_cny) / SUM(SUM(total_cost_cny)) OVER () * 100, 2) AS cost_pct
FROM ai_token_stat
WHERE stat_month = '2026-04'
  AND dept     = 'ALL'
  AND task_type = 'ALL'
  AND module   != 'ALL'
GROUP BY module
ORDER BY month_cost_cny DESC;
```

---

### 3.4 Schema: `mes_ai_audit`（安全审计）

独立 Schema，物理隔离，**数据只写不改不删，保留期 3 年以上**。

---

#### 3.4.1 `ai_desensitize_log`（脱敏操作审计日志）

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `task_id` | BIGINT | ✗ | NULL | 关联任务 ID（非任务上下文可为 NULL） |
| `request_time` | DATETIME | ✓ | CURRENT_TIMESTAMP | 请求时间（UTC+8） |
| `rule_hits` | VARCHAR(500) | ✓ | — | 命中的脱敏规则列表（JSON 数组） |
| `hit_count` | INT | ✓ | `0` | 本次请求命中脱敏规则的字段总数 |
| `original_hash` | CHAR(64) | ✓ | — | 原始内容 SHA256（用于溯源审计，不存储原文） |
| `desensitized_size_bytes` | INT | ✓ | — | 脱敏后内容字节大小 |
| `target_model` | VARCHAR(50) | ✓ | — | 目标 AI 模型名称 |
| `is_blocked` | TINYINT(1) | ✓ | `0` | 是否因脱敏失败而阻断请求：1-已阻断 |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 审计写入时间（只增不改，保留 3 年） |

---

#### 3.4.2 `ai_hardcode_scan_log`（硬编码扫描审计日志）

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `git_commit_hash` | CHAR(40) | ✓ | — | 被扫描的 Git Commit Hash |
| `git_branch` | VARCHAR(100) | ✓ | — | 分支名 |
| `task_id` | BIGINT | ✗ | NULL | 关联任务 ID |
| `scan_tool` | VARCHAR(50) | ✓ | — | 扫描工具：`GITLEAKS`/`CUSTOM_SCRIPT` |
| `scan_result` | VARCHAR(10) | ✓ | — | 扫描结果：`PASS`/`FAIL` |
| `violation_count` | INT | ✓ | `0` | 发现违规数量（CI/CD 只允许 0 通过） |
| `violation_types` | VARCHAR(500) | ✗ | NULL | 违规类型清单（JSON 数组） |
| `is_pipeline_blocked` | TINYINT(1) | ✓ | `0` | 是否阻断了 CI/CD 流水线：1-已阻断 |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 扫描时间 |

---

#### 3.4.3 `ai_operation_audit`（操作审计总日志）

| 字段名 | 类型 | NOT NULL | 默认值 | 说明 |
|--------|------|--------|--------|------|
| `id` | BIGINT | ✓ | AUTO_INCREMENT | 主键 |
| `user_id` | BIGINT | ✗ | NULL | 操作用户 ID（系统自动操作为 NULL） |
| `username` | VARCHAR(50) | ✓ | — | 操作用户名（AI 操作填 `AI_AGENT`） |
| `user_role` | VARCHAR(20) | ✓ | — | 用户角色 |
| `action_module` | VARCHAR(50) | ✓ | — | 操作模块 |
| `action_type` | VARCHAR(50) | ✓ | — | 操作类型 |
| `resource_type` | VARCHAR(50) | ✗ | NULL | 操作资源类型（如 `TASK`/`DEPLOYMENT`） |
| `resource_id` | VARCHAR(50) | ✗ | NULL | 操作资源 ID |
| `action_desc` | VARCHAR(500) | ✓ | — | 操作描述 |
| `request_ip` | VARCHAR(50) | ✗ | NULL | 请求 IP（脱敏后存储） |
| `request_method` | VARCHAR(10) | ✗ | NULL | HTTP 方法 |
| `request_url` | VARCHAR(500) | ✗ | NULL | 请求 URL |
| `response_code` | INT | ✗ | NULL | HTTP 响应码 |
| `is_success` | TINYINT(1) | ✓ | `1` | 操作是否成功：1-成功 0-失败 |
| `fail_reason` | VARCHAR(500) | ✗ | NULL | 失败原因 |
| `created_at` | DATETIME | ✓ | CURRENT_TIMESTAMP | 操作时间（只增不改，保留 3 年） |

---

## 四、完整建表 DDL

> ⚠ 执行前请确认已授予相应数据库创建权限，并确认测试环境与正式环境网络隔离。以下仅列出 V1.1 新增或变更的 DDL，完整 DDL 在原有基础上合并执行。

```sql
-- ================================================================
-- 芯智云匠 MES AI 智能体资产化项目
-- 数据库建表 DDL V1.1 | 2026-04-11
-- 字符集：utf8mb4 | 引擎：InnoDB | 时区：UTC+8
-- ================================================================

-- ── Schema 创建 ─────────────────────────────────────────────────
CREATE DATABASE IF NOT EXISTS mes_ai_task     DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS mes_ai_monitor  DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS mes_ai_knowledge DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS mes_ai_audit    DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ================================================================
USE mes_ai_task;
-- ================================================================

-- ── ai_task_req ──────────────────────────────────────────────────
-- V1.1 变更：新增 module 字段（成本分摊维度）
CREATE TABLE ai_task_req (
  id                   BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '主键 ID',
  task_no              VARCHAR(32)     NOT NULL                 COMMENT '任务编号 REQ-MES-AI-YYYYMMDD-NNN（由 Redis 分布式递增生成，禁止手动修改）',
  title                VARCHAR(100)    NOT NULL                 COMMENT '需求标题（≤50汉字）',
  task_type            VARCHAR(20)     NOT NULL                 COMMENT '任务类型 FEAT/FIX/REPORT/QUERY/API/BUG/PERF',
  priority             TINYINT         NOT NULL DEFAULT 3       COMMENT '优先级 1紧急 2高 3中 4低',
  status               VARCHAR(20)     NOT NULL DEFAULT 'DRAFT' COMMENT '状态机（见设计文档 2.3 节）',
  submitter_id         BIGINT          NOT NULL                 COMMENT '提交人用户 ID',
  submitter_name       VARCHAR(50)     NOT NULL                 COMMENT '提交人姓名（冗余自用户表，避免跨库 JOIN）',
  dept                 VARCHAR(50)     NOT NULL                 COMMENT '所属部门（用于 Token 成本分摊统计）',
  module               VARCHAR(50)                              COMMENT '所属 MES 模块（用于 Token 成本分摊统计）',
  biz_background       TEXT                                     COMMENT '业务背景描述',
  func_desc            TEXT                                     COMMENT '功能详细描述',
  input_data           TEXT                                     COMMENT '输入数据说明',
  expected_output      TEXT                                     COMMENT '期望输出说明',
  biz_rules            TEXT                                     COMMENT '业务规则及计算公式',
  modules_involved     VARCHAR(200)                             COMMENT '涉及模块（逗号分隔）',
  device_involved      VARCHAR(200)                             COMMENT '涉及设备型号及通讯方式',
  accept_criteria      TEXT                                     COMMENT '验收标准（JSON 数组，每项含 condition/expected/result）',
  perf_requirement     VARCHAR(500)                             COMMENT '性能要求',
  expected_finish_date DATE                                     COMMENT '期望完成日期',
  estimated_hours      DECIMAL(6,1)                             COMMENT 'AI 预估执行工时（小时）',
  actual_hours         DECIMAL(6,1)                             COMMENT 'AI 实际执行工时（小时）',
  quality_score        TINYINT                                  COMMENT '综合质量评分 0-100，月度付款评估使用',
  remark               TEXT                                     COMMENT '备注',
  is_deleted           TINYINT(1)      NOT NULL DEFAULT 0       COMMENT '逻辑删除 0有效 1已删除',
  created_at           DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP     COMMENT '创建时间（UTC+8）',
  updated_at           DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
                                       ON UPDATE CURRENT_TIMESTAMP            COMMENT '最后更新时间（UTC+8）',
  PRIMARY KEY (id),
  UNIQUE KEY  uniq_task_req_no             (task_no),
  KEY         idx_task_req_status          (status),
  KEY         idx_task_req_type            (task_type),
  KEY         idx_task_req_submitter       (submitter_id),
  KEY         idx_task_req_created         (created_at),
  KEY         idx_task_req_dept_module     (dept, module),
  KEY         idx_task_req_priority_status (priority, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='MES AI 功能开发需求主表';


-- ── ai_task_history ──────────────────────────────────────────────
CREATE TABLE ai_task_history (
  id            BIGINT      NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  task_id       BIGINT      NOT NULL               COMMENT '关联 ai_task_req.id',
  task_no       VARCHAR(32) NOT NULL               COMMENT '冗余任务编号，便于日志独立查询',
  operator      VARCHAR(50) NOT NULL               COMMENT '操作人账号（系统操作填 SYSTEM 或 AI）',
  operator_role VARCHAR(20) NOT NULL               COMMENT '操作人角色 USER/AI/IT/MANAGER',
  action        VARCHAR(50) NOT NULL               COMMENT '操作动作 SUBMIT/APPROVE/REJECT/START/COMPLETE 等',
  from_status   VARCHAR(20)                        COMMENT '变更前状态',
  to_status     VARCHAR(20)                        COMMENT '变更后状态',
  ip_address    VARCHAR(50)                        COMMENT '操作人 IP（脱敏后存储）',
  remark        TEXT                               COMMENT '操作备注',
  created_at    DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间（精确到秒，只增不改，保留 3 年）',
  PRIMARY KEY (id),
  KEY idx_task_history_task (task_id),
  KEY idx_task_history_time (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='需求单操作历史审计（只增不改，保留 3 年）'
  PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p2027 VALUES LESS THAN (2028),
    PARTITION p2028 VALUES LESS THAN (2029),
    PARTITION pmax  VALUES LESS THAN MAXVALUE
);


-- ── ai_exec_log ──────────────────────────────────────────────────
-- V1.1 变更：新增 dept、module、estimated_cost_cny 字段
CREATE TABLE ai_exec_log (
  id                  BIGINT      NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  task_id             BIGINT      NOT NULL               COMMENT '关联任务 ID',
  task_no             VARCHAR(32) NOT NULL               COMMENT '冗余任务编号',
  dept                VARCHAR(50)                        COMMENT '所属部门（从 ai_task_req 冗余，用于成本分摊）',
  module              VARCHAR(50)                        COMMENT '所属 MES 模块（从 ai_task_req 冗余，用于成本分摊）',
  call_seq            INT         NOT NULL               COMMENT '本任务内调用序号（从 1 开始）',
  model_name          VARCHAR(50) NOT NULL               COMMENT '调用模型名称，如 claude-sonnet-4',
  log_type            VARCHAR(10) NOT NULL               COMMENT '日志类型 INFO/WARN/ERROR/OUTPUT',
  stage               VARCHAR(30) NOT NULL               COMMENT '执行阶段 UNDERSTAND/PLAN/CODEGEN/TEST/REPORT',
  prompt_hash         CHAR(64)                           COMMENT 'Prompt 内容 SHA256，用于查重与审计',
  prompt_tokens       INT         NOT NULL DEFAULT 0     COMMENT '本次调用 Prompt 端消耗 Token 数',
  completion_tokens   INT         NOT NULL DEFAULT 0     COMMENT '本次调用 Completion 端消耗 Token 数',
  total_tokens        INT         NOT NULL DEFAULT 0     COMMENT '本次调用合计 Token 数',
  estimated_cost_cny  DECIMAL(8,4)                       COMMENT '本次调用预估费用（人民币元，按模型单价实时计算写入）',
  latency_ms          INT                                COMMENT 'API 响应延迟（毫秒）',
  content             MEDIUMTEXT                         COMMENT '日志内容（必须已脱敏，is_desensitized=1 才可写入）',
  is_desensitized     TINYINT(1)  NOT NULL DEFAULT 1     COMMENT '是否已脱敏（必须为 1 才可写入，强制校验）',
  error_code          VARCHAR(50)                        COMMENT '错误码（正常时为 NULL）',
  created_at          DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '日志时间（UTC+8）',
  PRIMARY KEY (id),
  KEY idx_exec_log_task       (task_id),
  KEY idx_exec_log_model      (model_name, created_at),
  KEY idx_exec_log_dept       (dept, created_at),
  KEY idx_exec_log_module     (module, created_at),
  KEY idx_exec_log_time       (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='AI 模型调用执行日志（含 Token 消耗与成本分摊）'
  PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p2027 VALUES LESS THAN (2028),
    PARTITION pmax  VALUES LESS THAN MAXVALUE
);


-- ── ai_code_artifact ─────────────────────────────────────────────
CREATE TABLE ai_code_artifact (
  id                   BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  task_id              BIGINT       NOT NULL               COMMENT '关联任务 ID',
  file_path            VARCHAR(500) NOT NULL               COMMENT '文件在 Git 仓库中的相对路径',
  file_type            VARCHAR(20)  NOT NULL               COMMENT '文件类型 JAVA/VUE/SQL/XML/MD/TEST',
  file_size_bytes      INT                                 COMMENT '文件字节大小',
  lines_of_code        INT                                 COMMENT '代码行数（不含注释和空行）',
  git_commit_hash      CHAR(40)                            COMMENT 'Git Commit Hash（关联 ai_assertion_batch.related_commit_hash，实现版本联动追溯）',
  git_branch           VARCHAR(100)                        COMMENT '所在 Git 分支',
  has_hardcode         TINYINT(1)   NOT NULL DEFAULT 0     COMMENT '硬编码扫描结果 0通过（无硬编码）1检测到违规',
  sonar_status         VARCHAR(20)                         COMMENT 'SonarQube 扫描状态 PASS/FAIL/PENDING',
  sonar_critical_count INT          NOT NULL DEFAULT 0     COMMENT 'SonarQube Critical 级别问题数（目标=0）',
  remark               VARCHAR(500)                        COMMENT '备注',
  created_at           DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '代码生成时间',
  PRIMARY KEY (id),
  KEY idx_code_artifact_task        (task_id),
  KEY idx_code_artifact_type        (file_type),
  KEY idx_code_artifact_commit_hash (git_commit_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='AI 生成代码交付物元数据（代码内容存 Git，本表记录元数据）';


-- ── ai_test_report ───────────────────────────────────────────────
CREATE TABLE ai_test_report (
  id                BIGINT        NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  task_id           BIGINT        NOT NULL               COMMENT '关联任务 ID',
  report_type       VARCHAR(20)   NOT NULL               COMMENT '报告类型 UNIT/API/REGRESSION/MANUAL',
  test_tool         VARCHAR(50)                          COMMENT '测试工具 JUnit/Postman/GoReplay/Manual',
  total_cases       INT           NOT NULL DEFAULT 0     COMMENT '测试用例总数',
  passed_cases      INT           NOT NULL DEFAULT 0     COMMENT '通过用例数',
  failed_cases      INT           NOT NULL DEFAULT 0     COMMENT '失败用例数',
  coverage_pct      DECIMAL(5,2)                         COMMENT '代码覆盖率(%)，目标≥70%',
  p0_diff_count     INT           NOT NULL DEFAULT 0     COMMENT '回归测试 P0 级差异数（目标=0，否则阻断）',
  p1_diff_count     INT           NOT NULL DEFAULT 0     COMMENT '回归测试 P1 级差异数（目标<3）',
  report_summary    TEXT                                 COMMENT '报告摘要（AI 自动生成）',
  report_detail_url VARCHAR(500)                         COMMENT '详细报告文件路径或外部链接',
  is_passed         TINYINT(1)    NOT NULL DEFAULT 0     COMMENT '是否通过 1通过 0未通过',
  created_at        DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '报告生成时间',
  PRIMARY KEY (id),
  KEY idx_test_report_task (task_id),
  KEY idx_test_report_type (report_type, is_passed)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='AI 任务测试报告';


-- ── ai_review_record ─────────────────────────────────────────────
CREATE TABLE ai_review_record (
  id              BIGINT        NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  task_id         BIGINT        NOT NULL               COMMENT '关联任务 ID（唯一索引，一单一评审）',
  reviewer_id     BIGINT        NOT NULL               COMMENT 'IT 评审人用户 ID',
  reviewer_name   VARCHAR(50)   NOT NULL               COMMENT 'IT 评审人姓名',
  review_result   VARCHAR(20)   NOT NULL               COMMENT '评审结论 APPROVED/REJECTED/PENDING_INFO',
  review_opinion  TEXT                                 COMMENT '评审意见',
  estimated_hours DECIMAL(6,1)                         COMMENT '评审人预估 AI 执行工时（小时）',
  assign_mode     VARCHAR(20)   NOT NULL DEFAULT 'AUTO' COMMENT '分配方式 AUTO自动调度/MANUAL手动指定',
  plan_start_time DATETIME                             COMMENT '计划开始执行时间',
  review_time     DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '评审完成时间',
  PRIMARY KEY (id),
  UNIQUE KEY uniq_review_task (task_id),
  KEY        idx_review_reviewer (reviewer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='IT 需求评审记录';


-- ── ai_approval_gate ─────────────────────────────────────────────
CREATE TABLE ai_approval_gate (
  id             BIGINT        NOT NULL AUTO_INCREMENT    COMMENT '主键 ID',
  task_id        BIGINT        NOT NULL                   COMMENT '关联任务 ID',
  gate_type      VARCHAR(30)   NOT NULL                   COMMENT '授权类型 PLAN_CONFIRM/DDL_CHANGE/DEPLOY/EMERGENCY',
  gate_title     VARCHAR(200)  NOT NULL                   COMMENT '授权事项标题',
  gate_content   TEXT                                     COMMENT '待授权内容摘要（AI 生成的方案说明）',
  status         VARCHAR(20)   NOT NULL DEFAULT 'PENDING' COMMENT '授权状态 PENDING/APPROVED/REJECTED/TIMEOUT',
  approver_id    BIGINT                                   COMMENT '授权人用户 ID',
  approver_name  VARCHAR(50)                              COMMENT '授权人姓名',
  approver_ip    VARCHAR(50)                              COMMENT '授权人操作 IP（脱敏后存储）',
  approve_remark TEXT                                     COMMENT '授权备注',
  expire_at      DATETIME      NOT NULL                   COMMENT '授权超时时间（超时自动置为 TIMEOUT）',
  approved_at    DATETIME                                 COMMENT '实际授权时间',
  created_at     DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '授权请求创建时间',
  PRIMARY KEY (id),
  KEY idx_approval_gate_task   (task_id),
  KEY idx_approval_gate_status (status, expire_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='人工授权网关记录（禁止物理删除，保留 3 年）';


-- ── ai_deploy_record ─────────────────────────────────────────────
CREATE TABLE ai_deploy_record (
  id                 BIGINT    NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  task_id            BIGINT    NOT NULL               COMMENT '关联任务 ID（唯一索引）',
  applicant_id       BIGINT    NOT NULL               COMMENT '申请部署人员用户 ID',
  plan_deploy_time   DATETIME  NOT NULL               COMMENT '计划部署时间',
  rollback_plan      TEXT      NOT NULL               COMMENT '回退方案（必填，AI 生成草稿，IT 审核确认）',
  approver_id        BIGINT                           COMMENT 'IT 负责人审批人用户 ID',
  approve_result     VARCHAR(20)                      COMMENT '审批结论 APPROVED/REJECTED',
  approve_time       DATETIME                         COMMENT '审批时间',
  actual_deploy_time DATETIME                         COMMENT '实际部署时间',
  deploy_result      VARCHAR(20)                      COMMENT '部署结果 SUCCESS/ROLLBACK/PARTIAL',
  deploy_log         TEXT                             COMMENT '部署执行日志摘要',
  created_at         DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  PRIMARY KEY (id),
  UNIQUE KEY uniq_deploy_task (task_id),
  KEY        idx_deploy_time  (plan_deploy_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='正式环境部署审批记录';


-- ── ai_token_daily ───────────────────────────────────────────────
CREATE TABLE ai_token_daily (
  id                BIGINT         NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  stat_date         DATE           NOT NULL               COMMENT '统计日期',
  model_name        VARCHAR(50)    NOT NULL               COMMENT '模型名称',
  total_calls       INT            NOT NULL DEFAULT 0     COMMENT '当日 API 调用总次数',
  prompt_tokens     BIGINT         NOT NULL DEFAULT 0     COMMENT '当日 Prompt Token 总量',
  completion_tokens BIGINT         NOT NULL DEFAULT 0     COMMENT '当日 Completion Token 总量',
  total_tokens      BIGINT         NOT NULL DEFAULT 0     COMMENT '当日合计 Token 总量',
  budget_limit      BIGINT         NOT NULL DEFAULT 3000000 COMMENT '当日预算上限（默认 300 万 Token/天）',
  alert_triggered   TINYINT(1)     NOT NULL DEFAULT 0     COMMENT '是否触发超限告警 1已告警 0正常',
  total_cost_cny    DECIMAL(10,4)                         COMMENT '当日实际总费用（人民币元，由 ai_exec_log 聚合）',
  created_at        DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP     COMMENT '汇总写入时间',
  updated_at        DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP
                                   ON UPDATE CURRENT_TIMESTAMP            COMMENT '最后更新时间',
  PRIMARY KEY (id),
  UNIQUE KEY uniq_token_daily_date_model (stat_date, model_name),
  KEY        idx_token_daily_date        (stat_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Token 日消耗汇总（预算预警用，细粒度分析见 ai_token_stat）';


-- ── ai_seq_counter【V1.1 新增】────────────────────────────────────
CREATE TABLE ai_seq_counter (
  id          BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  seq_key     VARCHAR(50)  NOT NULL               COMMENT '序列号键，如 TASK_NO_20260411，唯一索引',
  seq_type    VARCHAR(20)  NOT NULL               COMMENT '序列号类型 TASK_NO/REPORT_NO/BATCH_NO 等',
  current_val INT          NOT NULL DEFAULT 0     COMMENT '当前已使用的最大序号',
  date_str    CHAR(8)      NOT NULL               COMMENT '日期字符串 YYYYMMDD（序列号按天重置）',
  remark      VARCHAR(200)                        COMMENT '备注',
  created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP     COMMENT '创建时间',
  updated_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
                           ON UPDATE CURRENT_TIMESTAMP            COMMENT '更新时间',
  PRIMARY KEY (id),
  UNIQUE KEY uniq_seq_key      (seq_key),
  KEY        idx_seq_type_date (seq_type, date_str)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='序列号降级兜底表（正常使用 Redis，Redis 故障时降级至此表）';


-- ================================================================
USE mes_ai_monitor;
-- ================================================================

-- ── ai_inspection_report ─────────────────────────────────────────
CREATE TABLE ai_inspection_report (
  id                 BIGINT        NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  report_no          VARCHAR(32)   NOT NULL               COMMENT '报告编号 INSP-MES-AI-YYYYMMDD',
  inspect_date       DATE          NOT NULL               COMMENT '巡检日期',
  inspect_start_time DATETIME      NOT NULL               COMMENT '巡检开始时间',
  inspect_end_time   DATETIME                             COMMENT '巡检结束时间',
  overall_status     VARCHAR(20)   NOT NULL               COMMENT '整体状态 NORMAL/WARNING/CRITICAL',
  alert_count        INT           NOT NULL DEFAULT 0     COMMENT '告警总数',
  critical_count     INT           NOT NULL DEFAULT 0     COMMENT 'Critical 级告警数',
  error_log_summary  TEXT                                 COMMENT '近 24h ERROR 日志摘要（去重，按频次排序）',
  slow_sql_count     INT           NOT NULL DEFAULT 0     COMMENT '首次巡检发现的慢 SQL 数量（执行>2秒）',
  disk_usage_pct     DECIMAL(5,2)                         COMMENT '磁盘使用率(%)，告警阈值 80%',
  memory_usage_pct   DECIMAL(5,2)                         COMMENT '内存使用率(%)，告警阈值 85%',
  db_conn_active     INT                                  COMMENT '数据库当前活跃连接数',
  report_content     LONGTEXT                             COMMENT '完整报告内容（Markdown 格式）',
  ai_suggestions     TEXT                                 COMMENT 'AI 自动生成的处置建议',
  it_confirm_status  VARCHAR(20)                          COMMENT 'IT 确认状态 PENDING/CONFIRMED/ESCALATED',
  it_confirm_user    VARCHAR(50)                          COMMENT 'IT 确认人姓名',
  it_confirm_time    DATETIME                             COMMENT 'IT 确认时间',
  created_at         DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '报告生成时间',
  PRIMARY KEY (id),
  UNIQUE KEY uniq_inspection_no  (report_no),
  KEY        idx_inspection_date (inspect_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='AI 每日系统巡检报告'
  PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p2027 VALUES LESS THAN (2028),
    PARTITION pmax  VALUES LESS THAN MAXVALUE
);


-- ── ai_alert_record ──────────────────────────────────────────────
CREATE TABLE ai_alert_record (
  id              BIGINT       NOT NULL AUTO_INCREMENT  COMMENT '主键 ID',
  inspection_id   BIGINT                               COMMENT '关联巡检报告 ID（实时告警可为 NULL）',
  alert_type      VARCHAR(50)  NOT NULL                COMMENT '告警类型 DISK/MEMORY/SERVICE_DOWN/SLOW_SQL/ERROR_LOG/API_FAIL',
  alert_level     VARCHAR(10)  NOT NULL                COMMENT '告警级别 CRITICAL/HIGH/MEDIUM/LOW',
  alert_title     VARCHAR(200) NOT NULL                COMMENT '告警标题',
  alert_content   TEXT                                 COMMENT '告警详细内容',
  metric_name     VARCHAR(100)                         COMMENT '指标名称（如 disk_usage_pct）',
  metric_value    DECIMAL(12,4)                        COMMENT '触发告警时的指标实测值',
  threshold_value DECIMAL(12,4)                        COMMENT '告警阈值',
  notify_sent     TINYINT(1)   NOT NULL DEFAULT 0      COMMENT '是否已发送通知 1已发送 0未发送',
  notify_channel  VARCHAR(50)                          COMMENT '通知渠道 WECHAT_BOT/EMAIL/SMS',
  resolve_status  VARCHAR(20)  NOT NULL DEFAULT 'OPEN' COMMENT '处理状态 OPEN/PROCESSING/RESOLVED/IGNORED',
  resolve_time    DATETIME                             COMMENT '解决时间',
  resolve_remark  VARCHAR(500)                         COMMENT '处理说明',
  created_at      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '告警产生时间',
  PRIMARY KEY (id),
  KEY idx_alert_level_status (alert_level, resolve_status),
  KEY idx_alert_inspection   (inspection_id),
  KEY idx_alert_time         (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='系统告警记录'
  PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p2027 VALUES LESS THAN (2028),
    PARTITION pmax  VALUES LESS THAN MAXVALUE
);


-- ── ai_slow_sql_record ───────────────────────────────────────────
CREATE TABLE ai_slow_sql_record (
  id                   BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  inspection_id        BIGINT                              COMMENT '关联巡检报告 ID',
  db_schema            VARCHAR(50)  NOT NULL               COMMENT '数据库 Schema 名',
  sql_digest           CHAR(64)     NOT NULL               COMMENT 'SQL 模板 SHA256（参数化后计算，用于去重聚合）',
  sql_template         TEXT                                COMMENT 'SQL 语句模板（参数替换为占位符 ?）',
  exec_count           INT          NOT NULL DEFAULT 1     COMMENT '统计周期内执行次数',
  avg_exec_ms          INT          NOT NULL               COMMENT '平均执行时间（毫秒）',
  max_exec_ms          INT          NOT NULL               COMMENT '最慢一次执行时间（毫秒）',
  rows_examined_avg    BIGINT                              COMMENT '平均扫描行数',
  has_index_suggestion TINYINT(1)   NOT NULL DEFAULT 0     COMMENT 'AI 是否已生成索引优化建议',
  index_suggestion     TEXT                                COMMENT 'AI 生成的索引优化 SQL',
  resolve_status       VARCHAR(20)  NOT NULL DEFAULT 'OPEN' COMMENT '处理状态 OPEN/PROCESSING/RESOLVED',
  created_at           DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
  PRIMARY KEY (id),
  KEY idx_slow_sql_inspection (inspection_id),
  KEY idx_slow_sql_digest     (sql_digest)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='慢 SQL 记录（执行时间>2秒，AI 自动分析并生成优化建议）';


-- ================================================================
USE mes_ai_knowledge;
-- ================================================================

-- ── ai_kb_document ───────────────────────────────────────────────
CREATE TABLE ai_kb_document (
  id                  BIGINT       NOT NULL AUTO_INCREMENT    COMMENT '主键 ID',
  doc_code            VARCHAR(50)  NOT NULL                   COMMENT '文档编码（唯一），如 KB-DB-001',
  doc_name            VARCHAR(200) NOT NULL                   COMMENT '文档名称',
  doc_type            VARCHAR(30)  NOT NULL                   COMMENT '文档类型 DB_SCHEMA/API/FLOW/DEVICE/HISTORY/CODE/STANDARD',
  module              VARCHAR(50)                             COMMENT '所属 MES 模块',
  source_path         VARCHAR(500)                            COMMENT '原始文档存储路径',
  file_format         VARCHAR(20)                             COMMENT '原始格式 PDF/WORD/EXCEL/SQL/MD',
  version             VARCHAR(20)  NOT NULL DEFAULT '1.0'     COMMENT '文档版本号',
  chunk_count         INT          NOT NULL DEFAULT 0         COMMENT '已切分的向量块总数',
  synced_chunk_count  INT          NOT NULL DEFAULT 0         COMMENT '已成功同步至向量数据库的块数',
  vector_status       VARCHAR(20)  NOT NULL DEFAULT 'PENDING' COMMENT '整体向量化状态 PENDING/PROCESSING/DONE/PARTIAL/FAILED',
  last_vectorized_at  DATETIME                                COMMENT '最近一次向量化完成时间',
  is_active           TINYINT(1)   NOT NULL DEFAULT 1         COMMENT '是否启用（逻辑删除用）',
  created_by          VARCHAR(50)  NOT NULL                   COMMENT '录入人',
  created_at          DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP     COMMENT '录入时间',
  updated_at          DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
                                   ON UPDATE CURRENT_TIMESTAMP            COMMENT '更新时间',
  PRIMARY KEY (id),
  UNIQUE KEY uniq_kb_doc_code   (doc_code),
  KEY        idx_kb_doc_type    (doc_type),
  KEY        idx_kb_doc_module  (module),
  KEY        idx_kb_doc_vstatus (vector_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='RAG 知识库文档元数据';


-- ── ai_kb_chunk ──────────────────────────────────────────────────
-- V1.1 变更：新增 sync_status、last_sync_at、last_sync_error、sync_retry_count
CREATE TABLE ai_kb_chunk (
  id               BIGINT       NOT NULL AUTO_INCREMENT    COMMENT '主键 ID',
  doc_id           BIGINT       NOT NULL                   COMMENT '关联 ai_kb_document.id',
  chunk_index      INT          NOT NULL                   COMMENT '块在文档中的序号（从 0 开始）',
  vector_id        VARCHAR(100)                            COMMENT '向量数据库中的记录 ID（同步成功后才写入）',
  chunk_text       TEXT         NOT NULL                   COMMENT '块文本内容（用于召回后展示）',
  token_count      INT          NOT NULL                   COMMENT '块的 Token 数量（512-1024 token）',
  start_char       INT                                     COMMENT '块在原文中的起始字符位置',
  end_char         INT                                     COMMENT '块在原文中的结束字符位置',
  sync_status      VARCHAR(20)  NOT NULL DEFAULT 'PENDING' COMMENT '向量同步状态 PENDING/SYNCING/SUCCESS/FAILED（AI 检索仅查 SUCCESS）',
  last_sync_at     DATETIME                                COMMENT '最近一次同步操作时间',
  last_sync_error  TEXT                                    COMMENT '最近一次同步失败的错误信息（成功时为 NULL）',
  sync_retry_count TINYINT      NOT NULL DEFAULT 0         COMMENT '同步失败重试次数（超过 3 次停止重试，需人工介入）',
  hit_count        INT          NOT NULL DEFAULT 0         COMMENT '被检索命中的累计次数',
  last_hit_at      DATETIME                                COMMENT '最近一次被命中时间',
  created_at       DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '切块时间',
  PRIMARY KEY (id),
  UNIQUE KEY uniq_kb_chunk_vector  (vector_id),
  KEY        idx_kb_chunk_doc      (doc_id),
  KEY        idx_kb_chunk_sync     (sync_status, doc_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='RAG 知识库向量块（AI 检索必须 WHERE sync_status = SUCCESS）';


-- ── ai_assertion ─────────────────────────────────────────────────
CREATE TABLE ai_assertion (
  id                BIGINT       NOT NULL AUTO_INCREMENT          COMMENT '主键 ID',
  assertion_id      VARCHAR(20)  NOT NULL                         COMMENT '断言编号，如 SM-WO-001（唯一）',
  assertion_name    VARCHAR(200) NOT NULL                         COMMENT '断言名称',
  category          VARCHAR(30)  NOT NULL                         COMMENT '断言分类 STATE_MACHINE/SQL_LOGIC/API_BEHAVIOR/CODE_GEN',
  priority          VARCHAR(10)  NOT NULL                         COMMENT '优先级 CRITICAL/HIGH/MEDIUM',
  description       TEXT         NOT NULL                         COMMENT '断言说明',
  prompt_text       TEXT         NOT NULL                         COMMENT '发给 AI 的测试 Prompt',
  expected_keywords TEXT         NOT NULL                         COMMENT '期望响应中包含的关键词（JSON 数组）',
  expected_excludes TEXT                                          COMMENT '响应中不应出现的词（JSON 数组）',
  scoring_method    VARCHAR(30)  NOT NULL DEFAULT 'keyword_match' COMMENT '评分方式 keyword_match/llm_judge',
  pass_threshold    DECIMAL(4,2) NOT NULL DEFAULT 0.90            COMMENT '通过阈值（0.0-1.0）',
  related_module    VARCHAR(50)                                   COMMENT '关联 MES 模块',
  is_active         TINYINT(1)   NOT NULL DEFAULT 1               COMMENT '是否启用',
  created_by        VARCHAR(50)  NOT NULL                         COMMENT '创建人',
  approved_by       VARCHAR(50)                                   COMMENT '技术负责人审批人（修改须审批）',
  created_at        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP     COMMENT '创建时间',
  updated_at        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
                                 ON UPDATE CURRENT_TIMESTAMP             COMMENT '更新时间',
  PRIMARY KEY (id),
  UNIQUE KEY uniq_assertion_id      (assertion_id),
  KEY        idx_assertion_priority (priority, is_active),
  KEY        idx_assertion_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='MES 业务逻辑断言库（Prompt Drift 监控，修改须技术负责人审批）';


-- ── ai_assertion_run ─────────────────────────────────────────────
CREATE TABLE ai_assertion_run (
  id                BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  run_batch_id      VARCHAR(50)  NOT NULL               COMMENT '批次 ID，格式 RUN-YYYYMMDD-HHMM',
  assertion_id      BIGINT       NOT NULL               COMMENT '关联断言定义 ID',
  trigger_type      VARCHAR(30)  NOT NULL               COMMENT '触发类型 MODEL_UPGRADE/PROMPT_CHANGE/SCHEDULED',
  model_name        VARCHAR(50)  NOT NULL               COMMENT '测试时使用的模型版本',
  ai_response       TEXT                                COMMENT 'AI 原始响应内容（脱敏后）',
  keyword_hit_rate  DECIMAL(4,2)                        COMMENT '关键词命中率（0.0-1.0）',
  exclude_violation TINYINT(1)   NOT NULL DEFAULT 0     COMMENT '是否触发排除词 1有违反',
  is_passed         TINYINT(1)   NOT NULL DEFAULT 0     COMMENT '本条断言是否通过 1通过',
  score             DECIMAL(4,2)                        COMMENT '综合评分',
  fail_reason       TEXT                                COMMENT '失败原因（通过时为 NULL）',
  latency_ms        INT                                 COMMENT 'API 响应延迟（毫秒）',
  tokens_used       INT          NOT NULL DEFAULT 0     COMMENT '本次测试消耗 Token 数',
  created_at        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '执行时间',
  PRIMARY KEY (id),
  KEY idx_assertion_run_batch     (run_batch_id),
  KEY idx_assertion_run_assertion (assertion_id),
  KEY idx_assertion_run_time      (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='断言执行记录'
  PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p2027 VALUES LESS THAN (2028),
    PARTITION pmax  VALUES LESS THAN MAXVALUE
);


-- ── ai_assertion_batch ───────────────────────────────────────────
-- V1.1 变更：新增 related_task_id、related_commit_hash、trigger_source
CREATE TABLE ai_assertion_batch (
  id                   BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  run_batch_id         VARCHAR(50)  NOT NULL               COMMENT '批次 ID，格式 RUN-YYYYMMDD-HHMM（唯一）',
  trigger_type         VARCHAR(30)  NOT NULL               COMMENT '触发类型 MODEL_UPGRADE/PROMPT_CHANGE/SCHEDULED',
  trigger_source       VARCHAR(200)                        COMMENT '触发来源描述（如变更的 Prompt 文件路径、模型版本号）',
  related_task_id      BIGINT                              COMMENT '关联触发此次断言的任务 ID（PROMPT_CHANGE 类型必填，关联 ai_task_req.id）',
  related_commit_hash  CHAR(40)                            COMMENT '关联触发此次断言的 Git Commit Hash（关联 ai_code_artifact.git_commit_hash）',
  model_name           VARCHAR(50)  NOT NULL               COMMENT '测试模型版本',
  total_count          INT          NOT NULL DEFAULT 0     COMMENT '本批次断言总数',
  passed_count         INT          NOT NULL DEFAULT 0     COMMENT '通过数',
  critical_failed      INT          NOT NULL DEFAULT 0     COMMENT 'Critical 级失败数（目标=0，否则 BLOCKED）',
  high_failed          INT          NOT NULL DEFAULT 0     COMMENT 'High 级失败数（目标<3）',
  medium_failed        INT          NOT NULL DEFAULT 0     COMMENT 'Medium 级失败数（目标<5）',
  pass_rate_pct        DECIMAL(5,2) NOT NULL               COMMENT '全量通过率(%)，目标≥95%',
  block_action         VARCHAR(20)  NOT NULL               COMMENT '阻断动作 BLOCKED/WARNED/PASSED',
  notified             TINYINT(1)   NOT NULL DEFAULT 0     COMMENT '是否已发送通知',
  created_at           DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '批次开始时间',
  finished_at          DATETIME                            COMMENT '批次完成时间',
  PRIMARY KEY (id),
  UNIQUE KEY uniq_batch_id           (run_batch_id),
  KEY        idx_batch_trigger       (trigger_type, created_at),
  KEY        idx_batch_task          (related_task_id),
  KEY        idx_batch_commit        (related_commit_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='断言批次汇总（含版本联动追溯字段）';


-- ── ai_token_stat【V1.1 新增】────────────────────────────────────
CREATE TABLE ai_token_stat (
  id                BIGINT        NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  stat_date         DATE          NOT NULL               COMMENT '统计日期',
  stat_month        CHAR(7)       NOT NULL               COMMENT '统计月份 YYYY-MM（冗余，用于月度汇总查询）',
  model_name        VARCHAR(50)   NOT NULL               COMMENT '模型名称',
  dept              VARCHAR(50)   NOT NULL               COMMENT '部门（ALL 表示全部门汇总行）',
  module            VARCHAR(50)   NOT NULL               COMMENT 'MES 模块（ALL 表示全模块汇总行）',
  task_type         VARCHAR(20)   NOT NULL               COMMENT '任务类型（ALL 表示全类型汇总行）',
  total_calls       INT           NOT NULL DEFAULT 0     COMMENT '该维度当日 API 调用次数',
  total_tokens      BIGINT        NOT NULL DEFAULT 0     COMMENT '该维度当日 Token 总量',
  total_cost_cny    DECIMAL(10,4) NOT NULL DEFAULT 0.0000 COMMENT '该维度当日总费用（人民币元）',
  task_count        INT           NOT NULL DEFAULT 0     COMMENT '该维度当日任务数',
  avg_cost_per_task DECIMAL(8,4)                         COMMENT '该维度当日单任务平均费用（人民币元）',
  created_at        DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '汇总写入时间',
  PRIMARY KEY (id),
  UNIQUE KEY uniq_token_stat_dim (stat_date, model_name, dept, module, task_type),
  KEY        idx_token_stat_month (stat_month),
  KEY        idx_token_stat_dept  (dept, stat_month),
  KEY        idx_token_stat_module (module, stat_month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Token 多维度成本汇总（支持部门/模块/任务类型 ROI 分析，由定时任务从 ai_exec_log 聚合）';


-- ================================================================
USE mes_ai_audit;
-- ================================================================

-- ── ai_desensitize_log ───────────────────────────────────────────
CREATE TABLE ai_desensitize_log (
  id                      BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  task_id                 BIGINT                              COMMENT '关联任务 ID（非任务上下文可为 NULL）',
  request_time            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '请求时间（UTC+8）',
  rule_hits               VARCHAR(500) NOT NULL               COMMENT '命中的脱敏规则列表（JSON 数组）',
  hit_count               INT          NOT NULL DEFAULT 0     COMMENT '本次请求命中脱敏规则的字段总数',
  original_hash           CHAR(64)     NOT NULL               COMMENT '原始内容 SHA256（用于溯源审计，不存储原文）',
  desensitized_size_bytes INT          NOT NULL               COMMENT '脱敏后内容字节大小',
  target_model            VARCHAR(50)  NOT NULL               COMMENT '目标 AI 模型名称',
  is_blocked              TINYINT(1)   NOT NULL DEFAULT 0     COMMENT '是否因脱敏失败而阻断请求 1已阻断',
  created_at              DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '审计写入时间（只增不改，保留 3 年）',
  PRIMARY KEY (id),
  KEY idx_desens_task (task_id),
  KEY idx_desens_time (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='脱敏层操作审计日志（只增不改，保留 3 年）'
  PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p2027 VALUES LESS THAN (2028),
    PARTITION p2028 VALUES LESS THAN (2029),
    PARTITION pmax  VALUES LESS THAN MAXVALUE
);


-- ── ai_hardcode_scan_log ─────────────────────────────────────────
CREATE TABLE ai_hardcode_scan_log (
  id                  BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  git_commit_hash     CHAR(40)     NOT NULL               COMMENT '被扫描的 Git Commit Hash',
  git_branch          VARCHAR(100) NOT NULL               COMMENT '分支名',
  task_id             BIGINT                              COMMENT '关联任务 ID',
  scan_tool           VARCHAR(50)  NOT NULL               COMMENT '扫描工具 GITLEAKS/CUSTOM_SCRIPT',
  scan_result         VARCHAR(10)  NOT NULL               COMMENT '扫描结果 PASS/FAIL',
  violation_count     INT          NOT NULL DEFAULT 0     COMMENT '发现违规数量（CI/CD 只允许 0 通过）',
  violation_types     VARCHAR(500)                        COMMENT '违规类型清单（JSON 数组）',
  is_pipeline_blocked TINYINT(1)   NOT NULL DEFAULT 0     COMMENT '是否阻断了 CI/CD 流水线 1已阻断',
  created_at          DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '扫描时间',
  PRIMARY KEY (id),
  KEY idx_hardcode_scan_task   (task_id),
  KEY idx_hardcode_scan_result (scan_result, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='硬编码扫描审计日志（CI/CD 自动写入）';


-- ── ai_operation_audit ───────────────────────────────────────────
CREATE TABLE ai_operation_audit (
  id            BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  user_id       BIGINT                              COMMENT '操作用户 ID（系统自动操作为 NULL）',
  username      VARCHAR(50)  NOT NULL               COMMENT '操作用户名（AI 操作填 AI_AGENT）',
  user_role     VARCHAR(20)  NOT NULL               COMMENT '用户角色',
  action_module VARCHAR(50)  NOT NULL               COMMENT '操作模块',
  action_type   VARCHAR(50)  NOT NULL               COMMENT '操作类型',
  resource_type VARCHAR(50)                         COMMENT '操作资源类型（如 TASK/DEPLOYMENT）',
  resource_id   VARCHAR(50)                         COMMENT '操作资源 ID',
  action_desc   VARCHAR(500) NOT NULL               COMMENT '操作描述',
  request_ip    VARCHAR(50)                         COMMENT '请求 IP（脱敏后存储）',
  request_method VARCHAR(10)                        COMMENT 'HTTP 方法',
  request_url   VARCHAR(500)                        COMMENT '请求 URL',
  response_code INT                                 COMMENT 'HTTP 响应码',
  is_success    TINYINT(1)   NOT NULL DEFAULT 1     COMMENT '操作是否成功 1成功 0失败',
  fail_reason   VARCHAR(500)                        COMMENT '失败原因',
  created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间（只增不改，保留 3 年）',
  PRIMARY KEY (id),
  KEY idx_op_audit_user   (user_id, created_at),
  KEY idx_op_audit_module (action_module, action_type),
  KEY idx_op_audit_time   (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='系统操作审计总日志（只增不改，保留 3 年）'
  PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p2027 VALUES LESS THAN (2028),
    PARTITION p2028 VALUES LESS THAN (2029),
    PARTITION pmax  VALUES LESS THAN MAXVALUE
);

-- ================================================================
-- END OF DDL V1.1
-- ================================================================
```

---

## 五、索引策略

### 5.1 索引设计原则

| 原则 | 说明 |
|------|------|
| 业务驱动 | 每个索引须对应明确的查询场景，禁止为"以防万一"而建索引 |
| 最左前缀 | 复合索引列顺序：等值列 > 范围列 > 排序列 |
| 覆盖索引 | 高频列表查询应使用覆盖索引，避免回表 |
| 基数控制 | 状态类低基数字段不单独建索引，与高基数列组合 |
| 写入影响 | 每张表不超过 6 个索引，批量导入前可临时禁用索引 |
| 定期评审 | 每季度执行 `sys.schema_unused_indexes` 检查，清理无用索引 |

### 5.2 V1.1 新增索引说明

| 表名 | 索引名 | 字段 | 新增原因 |
|------|--------|------|--------|
| `ai_task_req` | `idx_task_req_dept_module` | `dept, module` | 支持按部门+模块的成本分摊聚合查询 |
| `ai_exec_log` | `idx_exec_log_dept` | `dept, created_at` | 支持按部门日汇总统计 Token 消耗 |
| `ai_exec_log` | `idx_exec_log_module` | `module, created_at` | 支持按模块日汇总统计 Token 消耗 |
| `ai_code_artifact` | `idx_code_artifact_commit_hash` | `git_commit_hash` | 支持从 commit hash 反查代码交付物，实现版本联动追溯 |
| `ai_assertion_batch` | `idx_batch_task` | `related_task_id` | 支持从任务 ID 查找关联的断言验证批次 |
| `ai_assertion_batch` | `idx_batch_commit` | `related_commit_hash` | 支持从 commit hash 直接查找断言阻断决策 |
| `ai_kb_chunk` | `idx_kb_chunk_sync` | `sync_status, doc_id` | 支持快速过滤 SUCCESS 状态的块，AI 检索专用 |
| `ai_token_stat` | `idx_token_stat_dept` | `dept, stat_month` | 支持月度各部门费用汇总查询 |
| `ai_token_stat` | `idx_token_stat_module` | `module, stat_month` | 支持月度各模块费用汇总查询 |

### 5.3 慢查询监控阈值

| 监控指标 | 阈值 | 响应措施 |
|--------|------|--------|
| SQL 执行时间 | > 2 秒 | 记录至 `ai_slow_sql_record`，AI 自动生成 EXPLAIN 分析和索引建议 |
| 全表扫描 | `rows_examined` > 10 万行 | 强制优化，禁止上正式环境 |
| 索引使用频率 | 命中 < 1 次/周 | 季度评审时标记为候选删除索引 |
| 索引碎片率 | > 30% | 低峰期执行 `OPTIMIZE TABLE` |

---

## 六、分区策略

### 6.1 分区表清单

| 表名 | Schema | 分区字段 | 数据保留策略 |
|------|--------|--------|--------|
| `ai_task_history` | `mes_ai_task` | `created_at`（YEAR） | 保留 3 年，每年 1 月清理 |
| `ai_exec_log` | `mes_ai_task` | `created_at`（YEAR） | 保留 2 年，每年 1 月清理 |
| `ai_inspection_report` | `mes_ai_monitor` | `created_at`（YEAR） | 保留 2 年 |
| `ai_alert_record` | `mes_ai_monitor` | `created_at`（YEAR） | 保留 2 年 |
| `ai_assertion_run` | `mes_ai_knowledge` | `created_at`（YEAR） | 保留 2 年 |
| `ai_desensitize_log` | `mes_ai_audit` | `created_at`（YEAR） | 保留 3 年（合规要求） |
| `ai_operation_audit` | `mes_ai_audit` | `created_at`（YEAR） | 保留 3 年（合规要求） |

### 6.2 分区管理运维 SQL

> ⛔ 以下 SQL 须经 IT 负责人书面授权，执行前须完成备份确认，删除分区操作不可恢复。

```sql
-- 每年 1 月：添加新年分区
ALTER TABLE mes_ai_task.ai_task_history
  ADD PARTITION (PARTITION p2029 VALUES LESS THAN (2030));

-- 每年 1 月：删除超期历史分区（须备份确认 + 书面授权）
ALTER TABLE mes_ai_task.ai_task_history    DROP PARTITION p2025;
ALTER TABLE mes_ai_audit.ai_operation_audit DROP PARTITION p2025;

-- 查看分区数据量
SELECT TABLE_SCHEMA, TABLE_NAME, PARTITION_NAME,
       TABLE_ROWS,
       ROUND(DATA_LENGTH/1024/1024, 2)  AS data_mb,
       ROUND(INDEX_LENGTH/1024/1024, 2) AS index_mb
FROM   information_schema.PARTITIONS
WHERE  TABLE_SCHEMA IN ('mes_ai_task','mes_ai_monitor','mes_ai_knowledge','mes_ai_audit')
  AND  PARTITION_NAME IS NOT NULL
ORDER BY TABLE_SCHEMA, TABLE_NAME, PARTITION_NAME;
```

---

## 七、字段注释规范

### 7.1 注释编写规则

| 规则项 | 要求 | 示例 |
|--------|------|------|
| 语言 | 所有字段 COMMENT 使用中文，禁止英文或混用 | `COMMENT '任务编号'` |
| 枚举值说明 | 枚举/状态字段必须列出全部取值及含义 | `COMMENT '优先级 1紧急 2高 3中 4低'` |
| 关联字段 | 外键字段注明关联表名 | `COMMENT '关联 ai_task_req.id'` |
| 业务含义 | 描述业务含义，而非字段名的直接翻译 | `COMMENT '首次巡检发现的慢 SQL 数量（执行>2秒）'` |
| 单位标注 | 数值字段须标注单位 | `COMMENT '响应延迟（毫秒）'` |
| 默认值说明 | 有特定含义的默认值须说明 | `COMMENT '预算上限（默认 300 万 Token/天）'` |
| 特殊约束 | 有业务约束的字段须注明 | `COMMENT '是否已脱敏（必须为 1 才可写入，强制校验）'` |
| 时区 | 时间字段统一标注时区 | `COMMENT '创建时间（UTC+8）'` |
| 版本标注 | V1.1 新增字段注明 | `COMMENT '所属部门（V1.1新增，用于成本分摊）'` |

### 7.2 特殊字段注释约定

| 字段类型 | 注释格式 | 示例 |
|--------|--------|------|
| 逻辑删除 | 含义及取值 | `COMMENT '逻辑删除 0有效 1已删除'` |
| JSON 字段 | 说明 JSON 结构 | `COMMENT '验收标准（JSON 数组，每项含 condition/expected/result）'` |
| 冗余字段 | 注明冗余原因 | `COMMENT '提交人姓名（冗余自用户表，避免跨库 JOIN）'` |
| Hash 字段 | 说明算法和用途 | `COMMENT '原始内容 SHA256（用于溯源审计，不存储原文）'` |
| 汇总维度字段 | 说明通配符含义 | `COMMENT '部门（ALL 表示全部门汇总行）'` |
| 降级兜底字段 | 说明使用场景 | `COMMENT '序列号降级兜底，正常使用 Redis，Redis 故障时降级'` |

---

## 八、优化设计补充说明

### 8.1 版本联动追溯（优化项 1）

**问题回顾：** 断言批次与代码交付物之间缺乏关联，无法在数据库层面定位"哪次提交导致了 Prompt 漂移"。

**解决方案：**

在 `ai_assertion_batch` 新增三个字段，形成完整链路：

```
ai_task_req.id
    └──► ai_assertion_batch.related_task_id     （任务维度溯源）
    └──► ai_code_artifact.git_commit_hash
               └──► ai_assertion_batch.related_commit_hash  （代码维度溯源）
    └──► ai_assertion_batch.trigger_source      （触发来源文字说明）
```

**写入规范：**

- `trigger_type = 'PROMPT_CHANGE'` 时：`related_task_id` 必填，`related_commit_hash` 必填（写入触发该 Prompt 变更的 CI commit hash）
- `trigger_type = 'MODEL_UPGRADE'` 时：`trigger_source` 填写模型版本变更说明，`related_commit_hash` 可为 NULL
- `trigger_type = 'SCHEDULED'` 时：两个关联字段均可为 NULL

### 8.2 Token 成本分摊（优化项 2）

**问题回顾：** 仅按模型统计，无法回答"哪个部门花了多少钱"。

**两层设计：**

| 层次 | 表 | 粒度 | 用途 |
|------|------|------|------|
| 明细层 | `ai_exec_log`（新增 `dept`、`module`、`estimated_cost_cny`） | 每次 API 调用 | 原始数据，支持任意维度二次聚合 |
| 汇总层 | `ai_token_stat`（新增表） | 日/月 × 部门 × 模块 × 任务类型 | 预聚合，直接服务报表查询，毫秒级响应 |

**定时任务规范（每日 01:00 执行）：**

```sql
-- 幂等写入当日汇总（先删后插）
DELETE FROM mes_ai_knowledge.ai_token_stat WHERE stat_date = CURDATE() - INTERVAL 1 DAY;

INSERT INTO mes_ai_knowledge.ai_token_stat
  (stat_date, stat_month, model_name, dept, module, task_type,
   total_calls, total_tokens, total_cost_cny, task_count, avg_cost_per_task)
SELECT
  DATE(e.created_at)                          AS stat_date,
  DATE_FORMAT(e.created_at, '%Y-%m')          AS stat_month,
  e.model_name,
  COALESCE(e.dept,   'UNKNOWN')               AS dept,
  COALESCE(e.module, 'UNKNOWN')               AS module,
  COALESCE(r.task_type, 'UNKNOWN')            AS task_type,
  COUNT(*)                                    AS total_calls,
  SUM(e.total_tokens)                         AS total_tokens,
  SUM(e.estimated_cost_cny)                   AS total_cost_cny,
  COUNT(DISTINCT e.task_id)                   AS task_count,
  ROUND(SUM(e.estimated_cost_cny) /
        NULLIF(COUNT(DISTINCT e.task_id), 0), 4) AS avg_cost_per_task
FROM mes_ai_task.ai_exec_log e
LEFT JOIN mes_ai_task.ai_task_req r ON e.task_id = r.id
WHERE DATE(e.created_at) = CURDATE() - INTERVAL 1 DAY
GROUP BY stat_date, stat_month, e.model_name, dept, module, task_type;
```

### 8.3 向量同步状态（优化项 3）

**问题回顾：** MySQL 记录了文档和分块，但向量数据库可能尚未完成索引，导致 AI 检索时命中空数据。

**解决方案：**

`ai_kb_chunk` 新增四个字段，实现向量同步的完整生命周期管理：

```
切块完成写入 MySQL
    sync_status = 'PENDING'
         │
         ▼ 异步向量化任务启动
    sync_status = 'SYNCING'
         │
    ┌────┴────┐
    ▼         ▼
 SUCCESS    FAILED
vector_id  last_sync_error 写入
写入         sync_retry_count +1
         │
    retry_count < 3：重新入队
    retry_count ≥ 3：人工介入，告警通知
```

**AI 检索时必须使用的查询模板：**

```sql
-- 正确写法：仅返回已成功同步的块
SELECT chunk_text, vector_id, hit_count
FROM mes_ai_knowledge.ai_kb_chunk
WHERE doc_id IN (
    SELECT id FROM mes_ai_knowledge.ai_kb_document
    WHERE doc_type = 'DB_SCHEMA' AND is_active = 1
)
AND sync_status = 'SUCCESS'   -- 关键过滤条件，禁止省略
ORDER BY hit_count DESC
LIMIT 5;
```

**监控查询（每日巡检应包含此项）：**

```sql
-- 检查向量同步异常状态
SELECT
    d.doc_name,
    COUNT(*) AS failed_chunks,
    MAX(c.sync_retry_count) AS max_retries,
    MAX(c.last_sync_at) AS last_attempt
FROM mes_ai_knowledge.ai_kb_chunk c
JOIN mes_ai_knowledge.ai_kb_document d ON c.doc_id = d.id
WHERE c.sync_status = 'FAILED'
GROUP BY d.id, d.doc_name
ORDER BY failed_chunks DESC;
```

### 8.4 task_no 生成规范（优化项 4）

**问题回顾：** 高并发提交时，基于时间戳+数据库的生成方案存在重复风险。

**推荐方案：Redis 分布式递增 + 日期后缀**

```
task_no 格式：REQ-MES-AI-{YYYYMMDD}-{NNN}
示例：          REQ-MES-AI-20260411-001

Redis Key：    seq:TASK_NO:{YYYYMMDD}
Redis 命令：   INCR seq:TASK_NO:20260411  → 返回递增整数
TTL 设置：     key 过期时间 = 当日 23:59:59（自动按天重置）
格式化：       左补零至 3 位（001, 002 ... 999）
```

**应用层生成逻辑（伪代码）：**

```java
public String generateTaskNo() {
    String dateStr = LocalDate.now().format(DateTimeFormatter.BASIC_ISO_DATE); // "20260411"
    String redisKey = "seq:TASK_NO:" + dateStr;
    
    try {
        // 正常路径：Redis 分布式递增
        long seq = redisTemplate.opsForValue().increment(redisKey);
        redisTemplate.expireAt(redisKey, endOfToday()); // 设置当日过期
        return String.format("REQ-MES-AI-%s-%03d", dateStr, seq);
        
    } catch (RedisException e) {
        // 降级路径：MySQL 乐观锁递增（ai_seq_counter 表）
        log.warn("Redis 不可用，降级至数据库序列号生成: {}", e.getMessage());
        return generateTaskNoFromDB(dateStr);
    }
}

private String generateTaskNoFromDB(String dateStr) {
    String seqKey = "TASK_NO_" + dateStr;
    // 使用 UPDATE + SELECT 实现乐观锁递增，避免并发冲突
    int updated = seqCounterMapper.incrementAndGet(seqKey, dateStr);
    if (updated == 0) {
        seqCounterMapper.insertInitial(seqKey, "TASK_NO", dateStr);
        updated = seqCounterMapper.incrementAndGet(seqKey, dateStr);
    }
    int currentVal = seqCounterMapper.getCurrentVal(seqKey);
    return String.format("REQ-MES-AI-%s-%03d", dateStr, currentVal);
}
```

**`ai_seq_counter` 操作 SQL：**

```sql
-- 递增（使用 UPDATE 返回影响行数判断是否成功，避免并发重复）
UPDATE ai_seq_counter
SET    current_val = current_val + 1,
       updated_at  = NOW()
WHERE  seq_key  = 'TASK_NO_20260411'
  AND  date_str = '20260411';

-- 查询当前值
SELECT current_val FROM ai_seq_counter WHERE seq_key = 'TASK_NO_20260411';

-- 初始化（INSERT IGNORE 避免并发重复插入）
INSERT IGNORE INTO ai_seq_counter (seq_key, seq_type, current_val, date_str)
VALUES ('TASK_NO_20260411', 'TASK_NO', 1, '20260411');
```

**注意事项：**

- `seq` 最大值 999，单日需求单超过 999 条时自动扩展为 4 位（`%04d`），扩展逻辑需同步更新 `task_no` 字段长度
- 每日零点后，Redis Key 自动过期，新的一天从 001 重新开始
- 应用层在写入 `ai_task_req` 时，`task_no` 已在 Service 层生成完毕，数据库层 `UNIQUE KEY` 作为最终兜底保障，若出现极端并发冲突则抛出异常并重试

---

## 九、附录

### 附录 A：表清单汇总（V1.1）

| 序号 | Schema | 表名 | 中文说明 | 记录类型 | V1.1 变化 |
|------|--------|------|--------|--------|--------|
| 1 | `mes_ai_task` | `ai_task_req` | 需求主表 | 业务主表 | 新增 `module` 字段 |
| 2 | `mes_ai_task` | `ai_task_history` | 操作历史 | 审计只增，分区保留 3 年 | 无 |
| 3 | `mes_ai_task` | `ai_exec_log` | AI 执行日志 | 日志分区，保留 2 年 | 新增 `dept`/`module`/`estimated_cost_cny` |
| 4 | `mes_ai_task` | `ai_code_artifact` | 代码交付物元数据 | 业务表 | 无（注释更新） |
| 5 | `mes_ai_task` | `ai_test_report` | 测试报告 | 业务表 | 无 |
| 6 | `mes_ai_task` | `ai_review_record` | IT 评审记录 | 业务表 | 无 |
| 7 | `mes_ai_task` | `ai_approval_gate` | 人工授权网关 | 审计，保留 3 年 | 无 |
| 8 | `mes_ai_task` | `ai_deploy_record` | 部署记录 | 业务表 | 无 |
| 9 | `mes_ai_task` | `ai_token_daily` | Token 日消耗 | 汇总统计 | 新增 `total_cost_cny` |
| 10 | `mes_ai_task` | `ai_seq_counter` | 序列号降级兜底 | 配置表 | **V1.1 新增** |
| 11 | `mes_ai_monitor` | `ai_inspection_report` | 巡检报告 | 日志分区，保留 2 年 | 无 |
| 12 | `mes_ai_monitor` | `ai_alert_record` | 告警记录 | 日志分区，保留 2 年 | 无 |
| 13 | `mes_ai_monitor` | `ai_slow_sql_record` | 慢 SQL 记录 | 业务表 | 无 |
| 14 | `mes_ai_knowledge` | `ai_kb_document` | 知识文档元数据 | 配置/业务表 | 新增 `synced_chunk_count` |
| 15 | `mes_ai_knowledge` | `ai_kb_chunk` | 知识向量块索引 | 业务表 | 新增 `sync_status`/`last_sync_at`/`last_sync_error`/`sync_retry_count` |
| 16 | `mes_ai_knowledge` | `ai_assertion` | 业务断言定义 | 配置表，修改须审批 | 无 |
| 17 | `mes_ai_knowledge` | `ai_assertion_run` | 断言执行记录 | 日志分区，保留 2 年 | 无 |
| 18 | `mes_ai_knowledge` | `ai_assertion_batch` | 断言批次汇总 | 汇总表 | 新增 `related_task_id`/`related_commit_hash`/`trigger_source` |
| 19 | `mes_ai_knowledge` | `ai_token_stat` | Token 多维度汇总 | 汇总表 | **V1.1 新增** |
| 20 | `mes_ai_audit` | `ai_desensitize_log` | 脱敏审计日志 | 审计分区，保留 3 年 | 无 |
| 21 | `mes_ai_audit` | `ai_hardcode_scan_log` | 硬编码扫描日志 | 审计表 | 无 |
| 22 | `mes_ai_audit` | `ai_operation_audit` | 操作审计总日志 | 审计分区，保留 3 年 | 无 |

### 附录 B：版本历史

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|--------|
| V1.0 | 2026-04-11 | AI 技术负责人 | 初稿，覆盖 4 个 Schema、20 张核心表 |
| V1.1 | 2026-04-11 | AI 技术负责人 | 版本联动追溯（断言批次新增 3 字段）；Token 成本分摊（exec_log 新增 3 字段 + 新增 ai_token_stat 表）；向量同步状态（kb_chunk 新增 4 字段）；task_no 并发生成规范（新增 ai_seq_counter 表 + 应用层规范） |

### 附录 C：关联文件

| 文件编号 | 文件名称 | 状态 |
|--------|--------|------|
| AI-MES-TECH-2026-001 | MES AI 智能体机器人技术方案 V1.1 | 已发布 |
| AI-MES-CLAUDE-2026-001 | CLAUDE.md 开发行为规范 V1.0 | 已发布 |
| AI-MES-DB-2026-001 | 数据库设计文档 V1.1（本文件） | 已发布 |
| AI-MES-TECH-2026-002 | AI 智能体部署操作手册 | 待编写 |
| AI-MES-TECH-2026-004 | 知识库维护手册 | 待编写 |
| AI-MES-TECH-2026-005 | 断言库维护手册 | 待编写 |

---

*芯智云匠——山东芯通 MES 岗位 AI 智能体资产化项目*
*数据库设计文档 AI-MES-DB-2026-001 V1.1 · 2026年4月*
*内部文件，未经授权禁止外传*
