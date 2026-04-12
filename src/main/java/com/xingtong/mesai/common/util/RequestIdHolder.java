package com.xingtong.mesai.common.util;

/**
 * 请求 ID 线程上下文持有者
 *
 * <p>由 {@code RequestIdFilter} 在请求开始时写入，请求结束时清理。
 * <p>全链路均可通过 {@code RequestIdHolder.get()} 取得当前请求的追踪 ID，
 * 无需在方法间显式传递。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 * @module 公共基础组件
 * @related REQ-MES-AI-20260412-005（S1-5 后端项目骨架）
 */
public final class RequestIdHolder {

    private static final ThreadLocal<String> HOLDER = new ThreadLocal<>();

    private RequestIdHolder() {
        // 工具类，禁止实例化
    }

    /**
     * 获取当前请求 ID；若不在 HTTP 请求上下文中则返回空字符串
     */
    public static String get() {
        String id = HOLDER.get();
        return id != null ? id : "";
    }

    /**
     * 设置当前请求 ID（仅由 RequestIdFilter 调用）
     */
    public static void set(String requestId) {
        HOLDER.set(requestId);
    }

    /**
     * 清理 ThreadLocal，防止线程池复用时数据污染（仅由 RequestIdFilter 调用）
     */
    public static void clear() {
        HOLDER.remove();
    }
}
