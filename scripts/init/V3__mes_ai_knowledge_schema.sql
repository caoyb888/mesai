-- ============================================================
-- 芯智云匠 MES AI 平台 · mes_ai_knowledge Schema 初始化脚本
-- 文档编号: AI-MES-DB-2026-003
-- 关联任务: T1-3-3
-- 数据库设计文档: docs/MES_AI_Database_Design.md V1.1
-- 作者: AI
-- 日期: 2026-04-12
-- 说明: 幂等脚本（IF NOT EXISTS），可重复执行
-- ============================================================

-- ── Schema 创建 ──────────────────────────────────────────────
CREATE DATABASE IF NOT EXISTS mes_ai_knowledge
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE mes_ai_knowledge;

-- ── ai_kb_document ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ai_kb_document (
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


-- ── ai_kb_chunk ──────────────────────────────────────────────
-- V1.1 变更：新增 sync_status、last_sync_at、last_sync_error、sync_retry_count
CREATE TABLE IF NOT EXISTS ai_kb_chunk (
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


-- ── ai_assertion ─────────────────────────────────────────────
-- 业务逻辑断言库，修改须经技术负责人审批
CREATE TABLE IF NOT EXISTS ai_assertion (
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


-- ── ai_assertion_run ─────────────────────────────────────────
-- 分区表：PARTITION BY RANGE(YEAR(created_at))，保留 2 年
CREATE TABLE IF NOT EXISTS ai_assertion_run (
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
  PRIMARY KEY (id, created_at),
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


-- ── ai_assertion_batch ───────────────────────────────────────
-- V1.1 变更：新增 related_task_id、related_commit_hash、trigger_source
CREATE TABLE IF NOT EXISTS ai_assertion_batch (
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


-- ── ai_token_stat ────────────────────────────────────────────
-- V1.1 新增：Token 多维度成本汇总（部门/模块/任务类型 ROI 分析）
CREATE TABLE IF NOT EXISTS ai_token_stat (
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
  KEY        idx_token_stat_month  (stat_month),
  KEY        idx_token_stat_dept   (dept, stat_month),
  KEY        idx_token_stat_module (module, stat_month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Token 多维度成本汇总（支持部门/模块/任务类型 ROI 分析，由定时任务从 ai_exec_log 聚合）';

-- ============================================================
-- END OF V3__mes_ai_knowledge_schema.sql
-- ============================================================
