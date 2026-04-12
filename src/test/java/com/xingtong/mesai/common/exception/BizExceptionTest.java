package com.xingtong.mesai.common.exception;

import com.xingtong.mesai.common.result.ResultCode;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * BizException 业务异常 单元测试
 *
 * <p>覆盖构造方法、静态工厂方法和快捷构造方法。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 * @module 公共基础组件
 * @related REQ-MES-AI-20260412-005（S1-5 后端项目骨架）
 */
class BizExceptionTest {

    @Test
    void constructor_withResultCodeOnly_shouldSetCorrectFields() {
        BizException ex = new BizException(ResultCode.RESOURCE_NOT_FOUND);

        assertThat(ex.getResultCode()).isEqualTo(ResultCode.RESOURCE_NOT_FOUND);
        assertThat(ex.getDetail()).isNull();
        assertThat(ex.getMessage()).isEqualTo("资源不存在");
    }

    @Test
    void constructor_withDetail_shouldAppendDetailToMessage() {
        BizException ex = new BizException(ResultCode.RESOURCE_NOT_FOUND, "需求单=REQ-001");

        assertThat(ex.getResultCode()).isEqualTo(ResultCode.RESOURCE_NOT_FOUND);
        assertThat(ex.getDetail()).isEqualTo("需求单=REQ-001");
        assertThat(ex.getMessage()).contains("资源不存在");
        assertThat(ex.getMessage()).contains("需求单=REQ-001");
    }

    @Test
    void of_staticFactory_shouldReturnBizException() {
        // TaskNoGenerator 使用此方法，必须正常工作
        BizException ex = BizException.of(ResultCode.SYSTEM_BUSY, "序列号生成失败");

        assertThat(ex).isInstanceOf(BizException.class);
        assertThat(ex.getResultCode()).isEqualTo(ResultCode.SYSTEM_BUSY);
        assertThat(ex.getDetail()).isEqualTo("序列号生成失败");
    }

    @Test
    void notFound_shouldReturnCorrectCodeAndDetail() {
        BizException ex = BizException.notFound("需求单", 123L);

        assertThat(ex.getResultCode()).isEqualTo(ResultCode.RESOURCE_NOT_FOUND);
        assertThat(ex.getDetail()).contains("需求单");
        assertThat(ex.getDetail()).contains("123");
    }

    @Test
    void invalidStatus_shouldReturnCorrectCodeAndDetail() {
        BizException ex = BizException.invalidStatus("DRAFT", "AI_RUNNING");

        assertThat(ex.getResultCode()).isEqualTo(ResultCode.TASK_STATUS_INVALID);
        assertThat(ex.getDetail()).contains("DRAFT");
        assertThat(ex.getDetail()).contains("AI_RUNNING");
    }

    @Test
    void permissionDenied_shouldReturnCorrectCode() {
        BizException ex = BizException.permissionDenied("需要 task:write 权限");

        assertThat(ex.getResultCode()).isEqualTo(ResultCode.PERMISSION_DENIED);
        assertThat(ex.getDetail()).contains("task:write");
    }

    @Test
    void bizException_shouldBeRuntimeException() {
        // BizException 必须是 RuntimeException 子类，以便 Spring @Transactional 自动回滚
        BizException ex = new BizException(ResultCode.INTERNAL_ERROR);
        assertThat(ex).isInstanceOf(RuntimeException.class);
    }
}
