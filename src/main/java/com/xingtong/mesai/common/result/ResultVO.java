package com.xingtong.mesai.common.result;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.xingtong.mesai.common.util.RequestIdHolder;
import lombok.Data;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;

/**
 * 统一 API 响应封装
 *
 * <p>所有 REST 接口返回值必须使用本类封装，禁止直接返回裸对象或 Map。
 * <p>响应结构：
 * <pre>
 * {
 *   "code": 0,               // 0=成功，非0=业务失败
 *   "message": "success",    // 提示信息
 *   "data": { ... },         // 业务数据（成功时为非null，失败时省略）
 *   "timestamp": "2026-04-12T07:30:00+08:00",
 *   "requestId": "req-xxxxxxxxxxxxxxxx"
 * }
 * </pre>
 *
 * @param <T> 业务数据类型
 * @author AI（芯智云匠）
 * @date 2026-04-12
 * @module 公共基础组件
 * @related REQ-MES-AI-20260412-005（S1-5 后端项目骨架）
 */
@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ResultVO<T> {

    /** 业务状态码，0 表示成功，非 0 表示业务错误 */
    private Integer code;

    /** 提示信息 */
    private String message;

    /** 业务数据（null 时 JSON 序列化省略） */
    private T data;

    /** 服务端响应时间（ISO 8601，东八区） */
    private String timestamp;

    /** 链路追踪 ID，便于日志定位 */
    private String requestId;

    private ResultVO(Integer code, String message, T data) {
        this.code = code;
        this.message = message;
        this.data = data;
        this.timestamp = LocalDateTime.now()
                .atZone(ZoneId.of("Asia/Shanghai"))
                .format(DateTimeFormatter.ISO_OFFSET_DATE_TIME);
        this.requestId = RequestIdHolder.get();
    }

    // ── 静态工厂方法 ─────────────────────────────────────────────

    /**
     * 成功响应（含业务数据）
     */
    public static <T> ResultVO<T> success(T data) {
        return new ResultVO<>(0, "success", data);
    }

    /**
     * 成功响应（无数据，如删除/修改操作）
     */
    public static <T> ResultVO<T> success() {
        return new ResultVO<>(0, "success", null);
    }

    /**
     * 业务失败（使用 ResultCode 中的默认 message）
     */
    public static <T> ResultVO<T> fail(ResultCode code) {
        return new ResultVO<>(code.getCode(), code.getMessage(), null);
    }

    /**
     * 业务失败（自定义 message，用于动态错误描述）
     */
    public static <T> ResultVO<T> fail(ResultCode code, String message) {
        return new ResultVO<>(code.getCode(), message, null);
    }
}
