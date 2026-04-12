package com.xingtong.mesai.common.util;

import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.module.task.mapper.SeqCounterMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.ValueOperations;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * TaskNoGenerator 单元测试
 *
 * <p>覆盖场景：
 * <ol>
 *   <li>Redis 正常：格式校验、首次创建、连续递增、当日第一条</li>
 *   <li>Redis 降级：切换 MySQL 乐观锁路径、重试成功、重试耗尽</li>
 *   <li>边界条件：序列号超过 999 时扩展为 4 位</li>
 * </ol>
 *
 * @author AI
 * @date 2026-04-12
 * 关联需求单: T0-2-4
 */
@ExtendWith(MockitoExtension.class)
@DisplayName("TaskNoGenerator - 需求单编号生成器单元测试")
class TaskNoGeneratorTest {

    @Mock
    private StringRedisTemplate redisTemplate;

    @Mock
    private ValueOperations<String, String> valueOps;

    @Mock
    private SeqCounterMapper seqCounterMapper;

    @InjectMocks
    private TaskNoGenerator taskNoGenerator;

    private String today;

    @BeforeEach
    void setUp() {
        today = LocalDate.now().format(DateTimeFormatter.ofPattern("yyyyMMdd"));
        when(redisTemplate.opsForValue()).thenReturn(valueOps);
    }

    // ── Redis 正常路径 ────────────────────────────────────────

    @Test
    @DisplayName("should_返回正确格式_when_Redis正常首次生成")
    void should_returnCorrectFormat_when_redisFirstIncrement() {
        // Given
        when(valueOps.increment(anyString())).thenReturn(1L);

        // When
        String taskNo = taskNoGenerator.nextTaskNo();

        // Then
        assertThat(taskNo).matches("REQ-MES-AI-\\d{8}-\\d{3}");
        assertThat(taskNo).isEqualTo("REQ-MES-AI-" + today + "-001");
    }

    @Test
    @DisplayName("should_序列号递增不重复_when_连续调用三次")
    void should_sequentialAndUnique_when_calledThreeTimes() {
        // Given
        when(valueOps.increment(anyString())).thenReturn(1L, 2L, 3L);

        // When
        String no1 = taskNoGenerator.nextTaskNo();
        String no2 = taskNoGenerator.nextTaskNo();
        String no3 = taskNoGenerator.nextTaskNo();

        // Then
        assertThat(no1).endsWith("-001");
        assertThat(no2).endsWith("-002");
        assertThat(no3).endsWith("-003");
        assertThat(no1).isNotEqualTo(no2);
        assertThat(no2).isNotEqualTo(no3);
    }

    @Test
    @DisplayName("should_首次创建时设置TTL_when_Redis返回seq为1")
    void should_setTtlOnFirstCreate_when_seqIsOne() {
        // Given
        when(valueOps.increment(anyString())).thenReturn(1L);

        // When
        taskNoGenerator.nextTaskNo();

        // Then
        // seq == 1 时应调用 expireAt 设置过期时间
        verify(redisTemplate, times(1)).expireAt(
                argThat(key -> key.startsWith("seq:TASK_NO:")),
                any(java.util.Date.class)
        );
    }

    @Test
    @DisplayName("should_非首次不重置TTL_when_Redis返回seq大于1")
    void should_notResetTtl_when_seqGreaterThanOne() {
        // Given
        when(valueOps.increment(anyString())).thenReturn(5L);

        // When
        taskNoGenerator.nextTaskNo();

        // Then
        verify(redisTemplate, never()).expireAt(anyString(), any(java.util.Date.class));
    }

    @Test
    @DisplayName("should_序列号扩展为4位_when_当日序列超过999")
    void should_expandToFourDigits_when_seqExceeds999() {
        // Given
        when(valueOps.increment(anyString())).thenReturn(1000L);

        // When
        String taskNo = taskNoGenerator.nextTaskNo();

        // Then
        assertThat(taskNo).endsWith("-1000");
        assertThat(taskNo).matches("REQ-MES-AI-\\d{8}-\\d{4}");
    }

    @Test
    @DisplayName("should_抛出BizException_when_序列号超出单日上限9999")
    void should_throwBizException_when_seqExceedsMaxPerDay() {
        // Given
        when(valueOps.increment(anyString())).thenReturn(10000L);

        // When / Then
        assertThatThrownBy(() -> taskNoGenerator.nextTaskNo())
                .isInstanceOf(BizException.class)
                .hasMessageContaining("上限");
    }

    // ── MySQL 降级路径 ────────────────────────────────────────

    @Test
    @DisplayName("should_降级MySQL成功_when_Redis抛出异常")
    void should_fallbackToMysql_when_redisThrowsException() {
        // Given：Redis 抛出异常触发降级
        when(valueOps.increment(anyString()))
                .thenThrow(new RuntimeException("Redis connection refused"));
        // MySQL 路径：第一次乐观锁成功
        doNothing().when(seqCounterMapper).initIfAbsent(anyString(), anyString(), anyString());
        when(seqCounterMapper.incrementAndGet(anyString(), anyString())).thenReturn(1);
        when(seqCounterMapper.getCurrentVal(anyString())).thenReturn(1L);

        // When
        String taskNo = taskNoGenerator.nextTaskNo();

        // Then
        assertThat(taskNo).isEqualTo("REQ-MES-AI-" + today + "-001");
        verify(seqCounterMapper, times(1)).incrementAndGet(anyString(), anyString());
    }

    @Test
    @DisplayName("should_乐观锁重试后成功_when_MySQL首次冲突")
    void should_retryAndSucceed_when_mysqlOptimisticLockConflictOnce() {
        // Given：Redis 不可用；MySQL 第1次冲突(返回0)，第2次成功(返回1)
        when(valueOps.increment(anyString()))
                .thenThrow(new RuntimeException("Redis unavailable"));
        doNothing().when(seqCounterMapper).initIfAbsent(anyString(), anyString(), anyString());
        when(seqCounterMapper.incrementAndGet(anyString(), anyString()))
                .thenReturn(0)   // 第1次：并发冲突
                .thenReturn(1);  // 第2次：成功
        when(seqCounterMapper.getCurrentVal(anyString())).thenReturn(2L);

        // When
        String taskNo = taskNoGenerator.nextTaskNo();

        // Then
        assertThat(taskNo).isEqualTo("REQ-MES-AI-" + today + "-002");
        verify(seqCounterMapper, times(2)).incrementAndGet(anyString(), anyString());
    }

    @Test
    @DisplayName("should_抛出BizException_when_MySQL重试5次全部失败")
    void should_throwBizException_when_mysqlRetryExhausted() {
        // Given：Redis 不可用；MySQL 5次全部冲突
        when(valueOps.increment(anyString()))
                .thenThrow(new RuntimeException("Redis unavailable"));
        doNothing().when(seqCounterMapper).initIfAbsent(anyString(), anyString(), anyString());
        when(seqCounterMapper.incrementAndGet(anyString(), anyString())).thenReturn(0);

        // When / Then
        assertThatThrownBy(() -> taskNoGenerator.nextTaskNo())
                .isInstanceOf(BizException.class)
                .hasMessageContaining("序列号生成失败");

        verify(seqCounterMapper, times(5)).incrementAndGet(anyString(), anyString());
    }

    // ── 格式校验 ─────────────────────────────────────────────

    @Test
    @DisplayName("should_包含当前日期_when_生成任意编号")
    void should_containCurrentDate_when_generateAnyTaskNo() {
        // Given
        when(valueOps.increment(anyString())).thenReturn(42L);

        // When
        String taskNo = taskNoGenerator.nextTaskNo();

        // Then
        assertThat(taskNo).contains(today);
        assertThat(taskNo).startsWith("REQ-MES-AI-");
    }
}
