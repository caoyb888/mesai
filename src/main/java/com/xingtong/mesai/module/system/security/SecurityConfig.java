package com.xingtong.mesai.module.system.security;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.xingtong.mesai.common.result.ResultCode;
import com.xingtong.mesai.common.result.ResultVO;
import com.xingtong.mesai.module.system.mapper.SysUserMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.MediaType;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

/**
 * Spring Security 配置
 *
 * <p>策略：无状态（Stateless）Session，全局 JWT 认证，按路径配置授权规则。
 * <p>放行路径（无需 Token）：
 * <ul>
 *   <li>{@code POST /system/auth/login}  - 登录</li>
 *   <li>{@code GET  /system/health}      - 健康检查</li>
 *   <li>{@code GET  /actuator/**}        - Actuator（按需开放）</li>
 * </ul>
 * <p>其余路径均需有效 JWT，权限细粒度校验由 {@code @RequirePermission} + AOP 完成。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-4）
 */
@Slf4j
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtUtil             jwtUtil;
    private final JwtProperties       jwtProperties;
    private final SysUserMapper       sysUserMapper;
    private final StringRedisTemplate redisTemplate;
    private final ObjectMapper        objectMapper;

    /**
     * BCrypt 密码编码器（工作因子默认 10，符合安全要求）。
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    /**
     * JWT 认证过滤器 Bean（手动构造，避免 Spring 双重注册）。
     */
    @Bean
    public JwtAuthenticationFilter jwtAuthenticationFilter() {
        return new JwtAuthenticationFilter(jwtUtil, sysUserMapper, redisTemplate);
    }

    /**
     * 安全过滤器链配置。
     */
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            // 禁用 CSRF（REST API + JWT 无需 CSRF 保护）
            .csrf().disable()
            // 禁用 CORS（接口通过网关统一处理跨域）
            .cors().disable()
            // 禁用 Form Login 和 HTTP Basic（使用 JWT）
            .formLogin().disable()
            .httpBasic().disable()
            // 无状态 Session（JWT 自包含，无需服务端 Session）
            .sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            .and()
            // 路径授权配置
            .authorizeRequests()
                // 登录接口（仅 POST）放行
                .antMatchers(HttpMethod.POST, "/system/auth/login").permitAll()
                // 健康检查和 Actuator 放行
                .antMatchers(HttpMethod.GET, "/system/health", "/actuator/health").permitAll()
                // 其余接口需要认证
                .anyRequest().authenticated()
            .and()
            // 未认证时（无 Token 或 Token 无效）的统一响应
            .exceptionHandling()
                .authenticationEntryPoint(this::handleAuthenticationError)
                .accessDeniedHandler(this::handleAccessDenied)
            .and()
            // 在 UsernamePasswordAuthenticationFilter 之前插入 JWT 过滤器
            .addFilterBefore(jwtAuthenticationFilter(), UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    // ── 异常处理：统一返回 ResultVO 格式 ─────────────────────────

    /**
     * 未认证（无 Token / Token 无效）处理器。
     * 优先读取过滤器设置的 AUTH_ERROR_CODE attribute，降级为 TOKEN_MISSING。
     */
    private void handleAuthenticationError(HttpServletRequest request,
                                           HttpServletResponse response,
                                           org.springframework.security.core.AuthenticationException e)
            throws IOException {
        ResultCode errorCode = (ResultCode) request.getAttribute("AUTH_ERROR_CODE");
        if (errorCode == null) {
            errorCode = ResultCode.TOKEN_MISSING;
        }
        writeJsonResponse(response, HttpServletResponse.SC_UNAUTHORIZED, ResultVO.fail(errorCode));
    }

    /**
     * 已认证但无权限（403）处理器。
     */
    private void handleAccessDenied(HttpServletRequest request,
                                    HttpServletResponse response,
                                    org.springframework.security.access.AccessDeniedException e)
            throws IOException {
        writeJsonResponse(response, HttpServletResponse.SC_FORBIDDEN,
                ResultVO.fail(ResultCode.PERMISSION_DENIED));
    }

    /** 将 ResultVO 序列化为 JSON 写入响应 */
    private void writeJsonResponse(HttpServletResponse response, int status, ResultVO<?> body)
            throws IOException {
        response.setStatus(status);
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        response.setCharacterEncoding(StandardCharsets.UTF_8.name());
        response.getWriter().write(objectMapper.writeValueAsString(body));
    }
}
