package com.xingtong.mesai.common.util;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * RequestIdHolder ThreadLocal 管理 单元测试
 *
 * <p>验证 set/get/clear 操作的正确性，及线程隔离性。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 * @module 公共基础组件
 * @related REQ-MES-AI-20260412-005（S1-5 后端项目骨架）
 */
class RequestIdHolderTest {

    @AfterEach
    void tearDown() {
        // 每个测试后清理，防止线程复用时污染其他测试
        RequestIdHolder.clear();
    }

    @Test
    void get_whenNotSet_shouldReturnEmptyString() {
        // 未设置时应返回空字符串，而非 null（防止 NullPointerException）
        assertThat(RequestIdHolder.get()).isEqualTo("");
    }

    @Test
    void set_andGet_shouldReturnSameValue() {
        String requestId = "req-abc123456789";
        RequestIdHolder.set(requestId);

        assertThat(RequestIdHolder.get()).isEqualTo(requestId);
    }

    @Test
    void clear_shouldResetToEmpty() {
        RequestIdHolder.set("req-test-001");
        RequestIdHolder.clear();

        assertThat(RequestIdHolder.get()).isEqualTo("");
    }

    @Test
    void threadIsolation_shouldNotShareBetweenThreads() throws InterruptedException {
        // 主线程设置 ID
        RequestIdHolder.set("req-main-thread");

        // 子线程不应看到主线程的值
        String[] childThreadValue = new String[1];
        Thread childThread = new Thread(() -> childThreadValue[0] = RequestIdHolder.get());
        childThread.start();
        childThread.join();

        assertThat(childThreadValue[0]).isEqualTo("");
        // 主线程仍能取到自己的值
        assertThat(RequestIdHolder.get()).isEqualTo("req-main-thread");
    }
}
