-- ============================================================
-- 芯智云匠 MES AI 平台 · mes_ai_audit Schema 初始化脚本
-- 文档编号: AI-MES-DB-2026-004
-- 关联任务: T1-3-4
-- 数据库设计文档: docs/MES_AI_Database_Design.md V1.1
-- 作者: AI
-- 日期: 2026-04-12
-- 说明: 幂等脚本（IF NOT EXISTS），可重复执行
-- ============================================================

-- ── Schema 创建 ──────────────────────────────────────────────
CREATE DATABASE IF NOT EXISTS mes_ai_audit
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE mes_ai_audit;

-- ── ai_desensitize_log ───────────────────────────────────────
-- 脱敏层审计日志，只增不改，保留 3 年（合规要求）
CREATE TABLE IF NOT EXISTS ai_desensitize_log (
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
  PRIMARY KEY (id, created_at),
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


-- ── ai_hardcode_scan_log ─────────────────────────────────────
-- CI/CD 硬编码扫描审计日志（Gitleaks + 自研脚本写入）
CREATE TABLE IF NOT EXISTS ai_hardcode_scan_log (
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


-- ── ai_operation_audit ───────────────────────────────────────
-- 系统操作审计总日志，只增不改，保留 3 年（合规要求）
CREATE TABLE IF NOT EXISTS ai_operation_audit (
  id             BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  user_id        BIGINT                              COMMENT '操作用户 ID（系统自动操作为 NULL）',
  username       VARCHAR(50)  NOT NULL               COMMENT '操作用户名（AI 操作填 AI_AGENT）',
  user_role      VARCHAR(20)  NOT NULL               COMMENT '用户角色',
  action_module  VARCHAR(50)  NOT NULL               COMMENT '操作模块',
  action_type    VARCHAR(50)  NOT NULL               COMMENT '操作类型',
  resource_type  VARCHAR(50)                         COMMENT '操作资源类型（如 TASK/DEPLOYMENT）',
  resource_id    VARCHAR(50)                         COMMENT '操作资源 ID',
  action_desc    VARCHAR(500) NOT NULL               COMMENT '操作描述',
  request_ip     VARCHAR(50)                         COMMENT '请求 IP（脱敏后存储）',
  request_method VARCHAR(10)                         COMMENT 'HTTP 方法',
  request_url    VARCHAR(500)                        COMMENT '请求 URL',
  response_code  INT                                 COMMENT 'HTTP 响应码',
  is_success     TINYINT(1)   NOT NULL DEFAULT 1     COMMENT '操作是否成功 1成功 0失败',
  fail_reason    VARCHAR(500)                        COMMENT '失败原因',
  created_at     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间（只增不改，保留 3 年）',
  PRIMARY KEY (id, created_at),
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

-- ============================================================
-- END OF V4__mes_ai_audit_schema.sql
-- ============================================================
