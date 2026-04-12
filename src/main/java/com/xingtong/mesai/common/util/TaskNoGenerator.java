package com.xingtong.mesai.common.util;

import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.common.result.ResultCode;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;

import java.time.Duration;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

/**
 * 需求单编号生成器
 *
 * <p>生成格式：{@code REQ-MES-AI-{YYYYMMDD}-{NNN}}
 * <p>示例：{@code REQ-MES-AI-20260412-001}
 *
 * <p>生成策略（双保险）：
 * <ol>
 *   <li>正常路径：Redis INCR 分布式递增，键按日期隔离，当日 23:59:59 自动过期</li>
 *   <li>降级路径：Redis 不可用时，切换至 {@code ai_seq_counter} 表的乐观锁递增</li>
 * </ol>
 *
 * <p>并发安全说明：
 * <ul>
 *   <li>Redis 路径：INCR 命令原子操作，天然线程安全</li>
 *   <li>MySQL 路径：乐观锁（UPDATE WHERE current_val = old_val），冲突时最多重试 {@value MAX_RETRY} 次</li>
 *   <li>数据库层 {@code UNIQUE KEY uniq_task_req_no} 作为最终兜底，极端冲突时抛出异常</li>
 * </ul>
 *
 * <p>关联文档：docs/MES_AI_Database_Design.md 第 8.4 节
 *
 * @author AI
 * @date 2026-04-12
 * @see com.xingtong.mesai.module.task.mapper.SeqCounterMapper
 * 关联需求单: T0-2-4
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class TaskNoGenerator {

    /** Redis Key 前缀，完整 Key 格式：seq:TASK_NO:{YYYYMMDD} */
    private static final String REDIS_KEY_PREFIX = "seq:TASK_NO:";

    /** 序列号格式模板 */
    private static final String TASK_NO_FORMAT = "REQ-MES-AI-%s-%03d";

    /** 日期格式 */
    private static final DateTimeFormatter DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyyMMdd");

    /** MySQL 降级时乐观锁最大重试次数 */
    private static final int MAX_RETRY = 5;

    /** 单日序列号最大值（超过则扩展为4位，需同步更新字段长度） */
    private static final long MAX_SEQ_PER_DAY = 9999L;

    private final StringRedisTemplate redisTemplate;
    private final SeqCounterMapper seqCounterMapper;

    /**
     * 生成下一个需求单编号
     *
     * @return 需求单编号，格式 REQ-MES-AI-{YYYYMMDD}-{NNN}
     * @throws BizException 序列号超出上限或重试次数耗尽时抛出
     */
    public String nextTaskNo() {
        String dateStr = LocalDate.now().format(DATE_FORMATTER);
        try {
            return generateByRedis(dateStr);
        } catch (Exception e) {
            log.warn("[序列号生成] Redis 不可用，降级至 MySQL 乐观锁路径: {}", e.getMessage());
            return generateByMysql(dateStr);
        }
    }

    // ── 正常路径：Redis INCR ──────────────────────────────────

    /**
     * Redis 分布式递增生成序列号
     *
     * @param dateStr 当前日期字符串 YYYYMMDD
     * @return 格式化需求单编号
     */
    private String generateByRedis(String dateStr) {
        String redisKey = REDIS_KEY_PREFIX + dateStr;

        // INCR 原子递增，返回递增后的值
        Long seq = redisTemplate.opsForValue().increment(redisKey);
        if (seq == null) {
            throw new IllegalStateException("Redis INCR 返回 null，连接异常");
        }

        // 首次创建时设置过期时间（当日 23:59:59）
        // 注：若 Key 已存在，expireAt 仅更新 TTL，不影响已有值
        if (seq == 1L) {
            redisTemplate.expireAt(redisKey, endOfToday());
            log.info("[序列号生成] Redis 新建当日序列键: {}，TTL 至今日 23:59:59", redisKey);
        }

        validateSeq(seq, dateStr);
        String taskNo = formatTaskNo(dateStr, seq);
        log.info("[序列号生成] Redis 路径成功: {} (seq={})", taskNo, seq);
        return taskNo;
    }

    // ── 降级路径：MySQL 乐观锁 ────────────────────────────────

    /**
     * MySQL 乐观锁递增生成序列号（Redis 不可用时的降级兜底）
     *
     * @param dateStr 当前日期字符串 YYYYMMDD
     * @return 格式化需求单编号
     * @throws BizException 重试次数耗尽时抛出
     */
    private String generateByMysql(String dateStr) {
        String seqKey = "TASK_NO_" + dateStr;

        for (int attempt = 1; attempt <= MAX_RETRY; attempt++) {
            try {
                // 确保当日记录存在（INSERT IGNORE 防并发重复插入）
                seqCounterMapper.initIfAbsent(seqKey, "TASK_NO", dateStr);

                // 乐观锁递增（UPDATE 影响行数 > 0 表示成功）
                int updated = seqCounterMapper.incrementAndGet(seqKey, dateStr);
                if (updated > 0) {
                    long seq = seqCounterMapper.getCurrentVal(seqKey);
                    validateSeq(seq, dateStr);
                    String taskNo = formatTaskNo(dateStr, seq);
                    log.info("[序列号生成] MySQL 降级路径成功: {} (attempt={}, seq={})", taskNo, attempt, seq);
                    return taskNo;
                }
                log.warn("[序列号生成] MySQL 乐观锁冲突，第 {}/{} 次重试", attempt, MAX_RETRY);

            } catch (DuplicateKeyException e) {
                // INSERT IGNORE 极端并发下仍可能抛出，继续重试
                log.warn("[序列号生成] MySQL 并发冲突，第 {}/{} 次重试: {}", attempt, MAX_RETRY, e.getMessage());
            }
        }

        log.error("[序列号生成] MySQL 乐观锁重试 {} 次后仍失败，seqKey={}", MAX_RETRY, seqKey);
        throw BizException.of(ResultCode.SYSTEM_BUSY, "序列号生成失败，请稍后重试");
    }

    // ── 私有工具方法 ─────────────────────────────────────────

    /**
     * 格式化需求单编号
     * <p>seq ≤ 999 时使用 3 位（REQ-MES-AI-20260412-001）
     * <p>seq > 999 时自动扩展为 4 位（REQ-MES-AI-20260412-1000）
     */
    private String formatTaskNo(String dateStr, long seq) {
        if (seq <= 999) {
            return String.format(TASK_NO_FORMAT, dateStr, seq);
        }
        // 超过999时扩展为4位，注意：需同步通知DBA扩展 task_no 字段长度
        log.warn("[序列号生成] 当日序列号已超过999，扩展为4位格式: date={}, seq={}", dateStr, seq);
        return String.format("REQ-MES-AI-%s-%04d", dateStr, seq);
    }

    /**
     * 校验序列号是否超出单日上限
     */
    private void validateSeq(long seq, String dateStr) {
        if (seq > MAX_SEQ_PER_DAY) {
            log.error("[序列号生成] 单日序列号已超出上限 {}，date={}, seq={}", MAX_SEQ_PER_DAY, dateStr, seq);
            throw BizException.of(ResultCode.SYSTEM_BUSY,
                    String.format("当日需求单数量已超出上限(%d)，请联系系统管理员", MAX_SEQ_PER_DAY));
        }
    }

    /**
     * 获取当日 23:59:59 的时间戳（用于设置 Redis Key 过期时间）
     */
    private java.util.Date endOfToday() {
        LocalDateTime endOfDay = LocalDateTime.of(LocalDate.now(), LocalTime.MAX);
        return java.util.Date.from(
                endOfDay.atZone(java.time.ZoneId.of("Asia/Shanghai")).toInstant()
        );
    }
}
