-- ============================================================
-- 芯智云匠 MES AI 平台 · mes_ai_monitor Schema 初始化脚本
-- 文档编号: AI-MES-DB-2026-002
-- 关联任务: T1-3-2
-- 数据库设计文档: docs/MES_AI_Database_Design.md V1.1
-- 作者: AI
-- 日期: 2026-04-12
-- 说明: 幂等脚本（IF NOT EXISTS），可重复执行
-- ============================================================

-- ── Schema 创建 ──────────────────────────────────────────────
CREATE DATABASE IF NOT EXISTS mes_ai_monitor
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE mes_ai_monitor;

-- ── ai_inspection_report ─────────────────────────────────────
-- 分区表：PARTITION BY RANGE(YEAR(created_at))，保留 2 年
CREATE TABLE IF NOT EXISTS ai_inspection_report (
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
  PRIMARY KEY (id, created_at),
  KEY        uniq_inspection_no  (report_no),
  KEY        idx_inspection_date (inspect_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='AI 每日系统巡检报告'
  PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p2027 VALUES LESS THAN (2028),
    PARTITION pmax  VALUES LESS THAN MAXVALUE
  );


-- ── ai_alert_record ──────────────────────────────────────────
-- 分区表：PARTITION BY RANGE(YEAR(created_at))，保留 2 年
CREATE TABLE IF NOT EXISTS ai_alert_record (
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
  PRIMARY KEY (id, created_at),
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


-- ── ai_slow_sql_record ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS ai_slow_sql_record (
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

-- ============================================================
-- END OF V2__mes_ai_monitor_schema.sql
-- ============================================================
