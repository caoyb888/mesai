package com.xingtong.mesai.common.filter;

import com.xingtong.mesai.common.util.RequestIdHolder;
import org.slf4j.MDC;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Optional;
import java.util.UUID;

/**
 * 请求 ID 过滤器
 *
 * <p>每个 HTTP 请求自动生成唯一 RequestId，贯穿请求全生命周期：
 * <ul>
 *   <li>写入 MDC（日志格式中的 %X{requestId}）</li>
 *   <li>写入 RequestIdHolder（业务代码通过 RequestIdHolder.get() 取值）</li>
 *   <li>回传到响应头 X-Request-Id（前端可用于报障追踪）</li>
 * </ul>
 *
 * <p>优先级设为最高（HIGHEST_PRECEDENCE），确保所有后续过滤器的日志均含 requestId。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 * @module 公共基础组件
 * @related REQ-MES-AI-20260412-005（S1-5 后端项目骨架）
 */
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class RequestIdFilter implements Filter {

    private static final String HEADER_X_REQUEST_ID = "X-Request-Id";
    private static final String MDC_KEY = "requestId";

    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest) req;
        HttpServletResponse response = (HttpServletResponse) res;

        // 优先使用客户端传入的 X-Request-Id，否则服务端生成
        String requestId = Optional.ofNullable(request.getHeader(HEADER_X_REQUEST_ID))
                .filter(s -> !s.isBlank())
                .orElse("req-" + UUID.randomUUID().toString().replace("-", "").substring(0, 16));

        MDC.put(MDC_KEY, requestId);
        RequestIdHolder.set(requestId);
        response.setHeader(HEADER_X_REQUEST_ID, requestId);

        try {
            chain.doFilter(req, res);
        } finally {
            // 必须清理，防止线程池复用时污染下一个请求
            MDC.remove(MDC_KEY);
            RequestIdHolder.clear();
        }
    }
}
