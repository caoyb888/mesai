package com.xingtong.mesai.common.result;

import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * ResultVO 统一响应封装 单元测试
 *
 * <p>覆盖核心业务场景：成功响应、业务失败响应、自定义消息。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 * @module 公共基础组件
 * @related REQ-MES-AI-20260412-005（S1-5 后端项目骨架）
 */
class ResultVOTest {

    // ── success() 测试 ────────────────────────────────────────────

    @Test
    void success_withData_shouldReturnCodeZeroAndData() {
        String payload = "测试数据";
        ResultVO<String> result = ResultVO.success(payload);

        assertThat(result.getCode()).isEqualTo(0);
        assertThat(result.getMessage()).isEqualTo("success");
        assertThat(result.getData()).isEqualTo(payload);
        assertThat(result.getTimestamp()).isNotBlank();
    }

    @Test
    void success_withoutData_shouldReturnCodeZeroAndNullData() {
        ResultVO<Void> result = ResultVO.success();

        assertThat(result.getCode()).isEqualTo(0);
        assertThat(result.getMessage()).isEqualTo("success");
        assertThat(result.getData()).isNull();
    }

    @Test
    void success_shouldContainTimestamp() {
        ResultVO<String> result = ResultVO.success("data");

        // 验证时间戳格式包含时区偏移（ISO 8601 with offset）
        assertThat(result.getTimestamp()).contains("+08:00");
    }

    // ── fail() 测试 ───────────────────────────────────────────────

    @Test
    void fail_withResultCode_shouldReturnCorrectCodeAndMessage() {
        ResultVO<?> result = ResultVO.fail(ResultCode.RESOURCE_NOT_FOUND);

        assertThat(result.getCode()).isEqualTo(10004);
        assertThat(result.getMessage()).isEqualTo("资源不存在");
        assertThat(result.getData()).isNull();
    }

    @Test
    void fail_withCustomMessage_shouldOverrideDefaultMessage() {
        String customMsg = "需求单 REQ-123 不存在";
        ResultVO<?> result = ResultVO.fail(ResultCode.RESOURCE_NOT_FOUND, customMsg);

        assertThat(result.getCode()).isEqualTo(10004);
        assertThat(result.getMessage()).isEqualTo(customMsg);
    }

    @Test
    void fail_withInternalError_shouldReturnCode99999() {
        ResultVO<?> result = ResultVO.fail(ResultCode.INTERNAL_ERROR);

        assertThat(result.getCode()).isEqualTo(99999);
        assertThat(result.getData()).isNull();
    }

    // ── ResultCode 枚举测试 ───────────────────────────────────────

    @Test
    void resultCode_systemBusy_shouldExist() {
        // SYSTEM_BUSY 为 TaskNoGenerator 降级路径使用，必须存在
        assertThat(ResultCode.SYSTEM_BUSY.getCode()).isEqualTo(90004);
        assertThat(ResultCode.SYSTEM_BUSY.getMessage()).isNotBlank();
    }

    @Test
    void resultCode_allCodes_shouldBeUnique() {
        // 验证所有错误码唯一，防止枚举值重复导致业务混乱
        long distinctCount = java.util.Arrays.stream(ResultCode.values())
                .map(ResultCode::getCode)
                .distinct()
                .count();
        assertThat(distinctCount).isEqualTo(ResultCode.values().length);
    }
}
