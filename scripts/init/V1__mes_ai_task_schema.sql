-- ============================================================
-- 芯智云匠 MES AI 平台 · mes_ai_task Schema 初始化脚本
-- 文档编号: AI-MES-DB-2026-001
-- 关联任务: T1-3-1
-- 数据库设计文档: docs/MES_AI_Database_Design.md V1.1
-- 作者: AI
-- 日期: 2026-04-12
-- 说明: 幂等脚本（IF NOT EXISTS），可重复执行
-- ============================================================

-- ── Schema 创建 ──────────────────────────────────────────────
CREATE DATABASE IF NOT EXISTS mes_ai_task
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE mes_ai_task;

-- ── ai_task_req ──────────────────────────────────────────────
-- V1.1 变更：新增 module 字段（成本分摊维度）
CREATE TABLE IF NOT EXISTS ai_task_req (
  id                   BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '主键 ID',
  task_no              VARCHAR(32)     NOT NULL                 COMMENT '任务编号 REQ-MES-AI-YYYYMMDD-NNN（由 Redis 分布式递增生成，禁止手动修改）',
  title                VARCHAR(100)    NOT NULL                 COMMENT '需求标题（≤50汉字）',
  task_type            VARCHAR(20)     NOT NULL                 COMMENT '任务类型 FEAT/FIX/REPORT/QUERY/API/BUG/PERF',
  priority             TINYINT         NOT NULL DEFAULT 3       COMMENT '优先级 1紧急 2高 3中 4低',
  status               VARCHAR(20)     NOT NULL DEFAULT 'DRAFT' COMMENT '状态机 DRAFT/SUBMITTED/IT_REVIEW/APPROVED/AI_EXECUTING/PENDING_ACCEPT/ACCEPTED/CLOSED/REJECTED',
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


-- ── ai_task_history ──────────────────────────────────────────
-- 分区表：PARTITION BY RANGE(YEAR(created_at))，保留 3 年
CREATE TABLE IF NOT EXISTS ai_task_history (
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
  PRIMARY KEY (id, created_at),
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


-- ── ai_exec_log ──────────────────────────────────────────────
-- V1.1 变更：新增 dept、module、estimated_cost_cny 字段
-- 分区表：PARTITION BY RANGE(YEAR(created_at))，保留 2 年
CREATE TABLE IF NOT EXISTS ai_exec_log (
  id                  BIGINT      NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  task_id             BIGINT      NOT NULL               COMMENT '关联任务 ID',
  task_no             VARCHAR(32) NOT NULL               COMMENT '冗余任务编号',
  dept                VARCHAR(50)                        COMMENT '所属部门（从 ai_task_req 冗余，用于成本分摊）',
  module              VARCHAR(50)                        COMMENT '所属 MES 模块（从 ai_task_req 冗余，用于成本分摊）',
  call_seq            INT         NOT NULL               COMMENT '本任务内调用序号（从 1 开始）',
  model_name          VARCHAR(50) NOT NULL               COMMENT '调用模型名称，如 claude-sonnet-4-6',
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
  PRIMARY KEY (id, created_at),
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


-- ── ai_code_artifact ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ai_code_artifact (
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


-- ── ai_test_report ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ai_test_report (
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


-- ── ai_review_record ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ai_review_record (
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


-- ── ai_approval_gate ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ai_approval_gate (
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


-- ── ai_deploy_record ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ai_deploy_record (
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


-- ── ai_token_daily ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ai_token_daily (
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


-- ── ai_seq_counter ───────────────────────────────────────────
-- 注：此表已在 mysql-seq-fallback-init.sql 中创建，此处保持幂等
CREATE TABLE IF NOT EXISTS ai_seq_counter (
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

-- ============================================================
-- END OF V1__mes_ai_task_schema.sql
-- ============================================================
