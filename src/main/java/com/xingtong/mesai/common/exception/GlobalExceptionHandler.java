package com.xingtong.mesai.common.exception;

import com.xingtong.mesai.common.result.ResultCode;
import com.xingtong.mesai.common.result.ResultVO;
import com.xingtong.mesai.common.util.RequestIdHolder;
import lombok.extern.slf4j.Slf4j;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.http.HttpStatus;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;

import javax.servlet.http.HttpServletRequest;
import java.util.stream.Collectors;

/**
 * 全局异常处理器
 *
 * <p>统一捕获所有未处理异常，转换为规范的 ResultVO 响应。
 * <p>保证任何情况下 API 均返回规范格式，不向客户端暴露系统内部信息。
 * <p>捕获优先级：BizException → 校验异常 → 类型异常 → 权限异常 → 唯一键 → 兜底
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 * @module 公共基础组件
 * @related REQ-MES-AI-20260412-005（S1-5 后端项目骨架）
 */
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * 处理业务异常（BizException）
     *
     * <p>HTTP 状态码 200：业务失败用 ResultVO.code 区分，不使用 4xx/5xx 表达业务错误。
     * <p>日志级别 INFO：业务失败是正常流程，非系统错误，不应产生告警噪音。
     */
    @ExceptionHandler(BizException.class)
    public ResultVO<?> handleBizException(BizException e, HttpServletRequest request) {
        log.info("业务异常 [{}] code={} message={} path={}",
                RequestIdHolder.get(),
                e.getResultCode().getCode(),
                e.getMessage(),
                request.getRequestURI());

        String message = e.getDetail() != null
                ? e.getResultCode().getMessage() + "：" + e.getDetail()
                : e.getResultCode().getMessage();
        return ResultVO.fail(e.getResultCode(), message);
    }

    /**
     * 处理参数校验异常（@Valid / @Validated 触发）
     *
     * <p>HTTP 状态码 400：入参格式错误属于客户端错误。
     * <p>收集所有字段校验错误，拼接为友好提示，一次性返回所有错误信息。
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ResultVO<?> handleValidationException(MethodArgumentNotValidException e) {
        String errorMsg = e.getBindingResult().getFieldErrors().stream()
                .map(FieldError::getDefaultMessage)
                .collect(Collectors.joining("；"));
        log.warn("请求参数校验失败：{}", errorMsg);
        return ResultVO.fail(ResultCode.PARAM_INVALID, errorMsg);
    }

    /**
     * 处理参数类型转换异常（路径变量类型不匹配、JSON 格式错误等）
     *
     * <p>HTTP 状态码 400。
     */
    @ExceptionHandler({MethodArgumentTypeMismatchException.class,
                       HttpMessageNotReadableException.class})
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ResultVO<?> handleParamTypeException(Exception e) {
        log.warn("请求参数类型错误：{}", e.getMessage());
        return ResultVO.fail(ResultCode.PARAM_INVALID, "请求参数格式不正确");
    }

    /**
     * 处理权限不足异常（Spring Security AccessDeniedException）
     *
     * <p>HTTP 状态码 403：已认证但无对应权限。
     */
    @ExceptionHandler(AccessDeniedException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public ResultVO<?> handleAccessDeniedException(AccessDeniedException e,
                                                    HttpServletRequest request) {
        String username = extractCurrentUsername();
        log.warn("权限不足 [{}] path={} user={}",
                RequestIdHolder.get(),
                request.getRequestURI(),
                username);
        return ResultVO.fail(ResultCode.PERMISSION_DENIED, "权限不足，请联系管理员授权");
    }

    /**
     * 处理数据库唯一键冲突（DuplicateKeyException）
     *
     * <p>HTTP 状态码 200（业务层面的并发冲突，不属于服务端错误）。
     */
    @ExceptionHandler(DuplicateKeyException.class)
    public ResultVO<?> handleDuplicateKeyException(DuplicateKeyException e) {
        log.warn("数据库唯一键冲突：{}", e.getMessage());
        return ResultVO.fail(ResultCode.DUPLICATE_KEY);
    }

    /**
     * 兜底处理：所有未预期的 Exception
     *
     * <p>HTTP 状态码 500：服务端内部错误。
     * <p>注意：绝不将异常堆栈信息暴露给客户端，仅返回 requestId 供运维排查。
     */
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ResultVO<?> handleUnexpectedException(Exception e, HttpServletRequest request) {
        log.error("系统内部错误 [{}] path={} error={}",
                RequestIdHolder.get(),
                request.getRequestURI(),
                e.getMessage(), e);

        return ResultVO.fail(ResultCode.INTERNAL_ERROR,
                "请联系运维人员，追踪ID：" + RequestIdHolder.get());
    }

    // ── 私有工具方法 ─────────────────────────────────────────────

    /**
     * 安全地获取当前认证用户名（SecurityContextHolder 可能为空）
     */
    private String extractCurrentUsername() {
        try {
            var auth = SecurityContextHolder.getContext().getAuthentication();
            return auth != null ? auth.getName() : "anonymous";
        } catch (Exception ex) {
            return "unknown";
        }
    }
}
