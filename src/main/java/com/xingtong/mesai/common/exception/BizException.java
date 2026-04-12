package com.xingtong.mesai.common.exception;

import com.xingtong.mesai.common.result.ResultCode;
import lombok.Getter;

/**
 * 业务异常基类
 *
 * <p>所有可预期的业务失败（状态不合法、权限不足、资源不存在等）均通过本类表达。
 * <p>不应使用原生 RuntimeException 直接抛出业务错误，统一使用本类以保证：
 * <ul>
 *   <li>错误码与 API 规范一致（ResultCode 枚举）</li>
 *   <li>GlobalExceptionHandler 可精确捕获并返回规范响应</li>
 *   <li>日志级别统一为 INFO（业务失败是正常流程，非系统错误）</li>
 * </ul>
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 * @module 公共基础组件
 * @related REQ-MES-AI-20260412-005（S1-5 后端项目骨架）
 */
@Getter
public class BizException extends RuntimeException {

    /** 业务错误码（对应 ResultCode 枚举） */
    private final ResultCode resultCode;

    /**
     * 额外的错误上下文信息
     * 用于动态错误 message，如资源 ID、字段名、状态转换路径
     */
    private final String detail;

    // ── 构造方法 ─────────────────────────────────────────────────

    public BizException(ResultCode resultCode) {
        super(resultCode.getMessage());
        this.resultCode = resultCode;
        this.detail = null;
    }

    public BizException(ResultCode resultCode, String detail) {
        super(resultCode.getMessage() + "：" + detail);
        this.resultCode = resultCode;
        this.detail = detail;
    }

    public BizException(ResultCode resultCode, String detail, Throwable cause) {
        super(resultCode.getMessage() + "：" + detail, cause);
        this.resultCode = resultCode;
        this.detail = detail;
    }

    // ── 静态工厂方法（快捷构造，提升可读性）─────────────────────

    /**
     * 通用工厂方法（TaskNoGenerator 等工具类使用）
     */
    public static BizException of(ResultCode resultCode, String detail) {
        return new BizException(resultCode, detail);
    }

    /**
     * 快捷构造：资源不存在
     *
     * @param resourceType 资源类型名称，如 "需求单" / "审批记录"
     * @param id           资源 ID
     */
    public static BizException notFound(String resourceType, Object id) {
        return new BizException(ResultCode.RESOURCE_NOT_FOUND, resourceType + "=" + id);
    }

    /**
     * 快捷构造：任务状态流转非法
     *
     * @param from 当前状态
     * @param to   目标状态
     */
    public static BizException invalidStatus(String from, String to) {
        return new BizException(ResultCode.TASK_STATUS_INVALID, from + " → " + to);
    }

    /**
     * 快捷构造：权限不足
     *
     * @param detail 所需权限描述
     */
    public static BizException permissionDenied(String detail) {
        return new BizException(ResultCode.PERMISSION_DENIED, detail);
    }
}
