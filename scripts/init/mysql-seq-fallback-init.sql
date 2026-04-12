-- ============================================================
-- MySQL 序列号降级兜底表初始化脚本
-- 文档编号: AI-MES-GIT-2026-001
-- 关联任务: T0-2-4
-- 关联文档: docs/MES_AI_Database_Design.md 第 3.1.10 节、第 8.4 节
-- 作者: AI
-- 日期: 2026-04-12
--
-- 用途: Redis 不可用时，由应用层降级至本表通过乐观锁生成序列号。
--       正常情况下此表仅作兜底，不参与主流程。
--
-- 执行环境: mes_ai_task schema（测试环境）
-- 执行前提: 已完成 Schema 初始化（T1-3 数据库初始化任务）
-- ============================================================

USE mes_ai_task;

-- ── 建表（与数据库设计文档保持一致）────────────────────────
CREATE TABLE IF NOT EXISTS ai_seq_counter (
  id          BIGINT       NOT NULL AUTO_INCREMENT          COMMENT '主键 ID',
  seq_key     VARCHAR(50)  NOT NULL                         COMMENT '序列号键，格式 TASK_NO_{YYYYMMDD}，唯一索引',
  seq_type    VARCHAR(20)  NOT NULL                         COMMENT '序列号类型 TASK_NO / REPORT_NO / BATCH_NO 等',
  current_val BIGINT       NOT NULL DEFAULT 0               COMMENT '当前序列值（下次 INCR 前的值，应用层 +1 后使用）',
  date_str    VARCHAR(8)   NOT NULL                         COMMENT '对应日期 YYYYMMDD，每日自动分组',
  description VARCHAR(100)                                  COMMENT '备注说明',
  updated_at  DATETIME     NOT NULL
              DEFAULT CURRENT_TIMESTAMP
              ON UPDATE CURRENT_TIMESTAMP                   COMMENT '最后更新时间（UTC+8）',
  PRIMARY KEY (id),
  UNIQUE KEY  uniq_seq_key (seq_key)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='序列号降级兜底表——Redis 不可用时由应用层通过乐观锁生成 task_no 等业务编号';

-- ── 初始化当日序列键（可选，首次请求时应用层会自动 INSERT IGNORE）──
-- 将 20260412 替换为当前日期，或由部署脚本动态生成
INSERT IGNORE INTO ai_seq_counter (seq_key, seq_type, current_val, date_str, description)
VALUES ('TASK_NO_20260412', 'TASK_NO', 0, '20260412', '需求单编号 REQ-MES-AI 序列（2026-04-12）');

-- ── 验证插入结果 ────────────────────────────────────────────
SELECT seq_key, seq_type, current_val, date_str, updated_at
FROM   ai_seq_counter
ORDER  BY date_str DESC
LIMIT  10;

-- ============================================================
-- 应用层使用的核心 SQL（由 SeqCounterMapper 调用，此处仅作说明）
-- ============================================================

/*
-- 1. 乐观锁递增（UPDATE 返回影响行数 > 0 表示成功，否则重试）
UPDATE ai_seq_counter
SET    current_val = current_val + 1,
       updated_at  = NOW()
WHERE  seq_key  = #{seqKey}
  AND  date_str = #{dateStr};

-- 2. 查询当前值（UPDATE 成功后调用）
SELECT current_val
FROM   ai_seq_counter
WHERE  seq_key = #{seqKey};

-- 3. 新一天首次使用时初始化（INSERT IGNORE 防并发重复）
INSERT IGNORE INTO ai_seq_counter (seq_key, seq_type, current_val, date_str, description)
VALUES (#{seqKey}, 'TASK_NO', 1, #{dateStr}, CONCAT('需求单编号序列（', #{dateStr}, '）'));
*/
