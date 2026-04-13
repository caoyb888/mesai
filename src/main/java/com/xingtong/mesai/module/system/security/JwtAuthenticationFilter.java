package com.xingtong.mesai.module.system.security;

import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.common.result.ResultCode;
import com.xingtong.mesai.module.system.entity.SysUser;
import com.xingtong.mesai.module.system.mapper.SysUserMapper;
import io.jsonwebtoken.Claims;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * JWT 认证过滤器
 *
 * <p>每次请求执行一次（继承 OncePerRequestFilter），完成如下职责：
 * <ol>
 *   <li>从请求头 {@code Authorization: Bearer <token>} 中提取 JWT</li>
 *   <li>解析并校验 JWT（签名、有效期、类型为 access）</li>
 *   <li>查询 Redis 黑名单，判断 Token 是否已被吊销</li>
 *   <li>从数据库加载用户信息，构建 {@link LoginUserDetails} 注入 SecurityContext</li>
 * </ol>
 *
 * <p>失败时不直接抛异常，而是将错误码写入 request attribute，
 * 由 {@link com.xingtong.mesai.module.system.security.SecurityConfig} 中配置的
 * AuthenticationEntryPoint 统一返回规范响应。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-4）
 */
@Slf4j
@RequiredArgsConstructor
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    /** Authorization 请求头名称 */
    private static final String HEADER_AUTHORIZATION = "Authorization";

    /** Bearer Token 前缀 */
    private static final String BEARER_PREFIX = "Bearer ";

    /** Redis 黑名单 Key 前缀：blacklist:{jti} */
    public static final String BLACKLIST_KEY_PREFIX = "jwt:blacklist:";

    private final JwtUtil              jwtUtil;
    private final SysUserMapper        sysUserMapper;
    private final StringRedisTemplate  redisTemplate;

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain)
            throws ServletException, IOException {

        String token = extractToken(request);
        if (token == null) {
            // 无 Token，继续放行（由 SecurityConfig 的 authorizeRequests 决定是否需要认证）
            filterChain.doFilter(request, response);
            return;
        }

        try {
            // 1. 解析并校验 JWT（签名 + 有效期 + type=access）
            Claims claims = jwtUtil.parseAccessToken(token);

            // 2. 检查黑名单（logout / revoke 操作会将 jti 放入 Redis 黑名单）
            String jti = jwtUtil.getJti(claims);
            if (isBlacklisted(jti)) {
                log.debug("JWT 已被吊销：jti={}", jti);
                setAuthError(request, ResultCode.TOKEN_REVOKED);
                filterChain.doFilter(request, response);
                return;
            }

            // 3. 从数据库加载用户（校验账号存在且未被删除/禁用）
            String username = jwtUtil.getUsername(claims);
            SysUser sysUser = loadUser(username);
            if (sysUser == null) {
                log.warn("JWT 认证失败：用户不存在 username={}", username);
                setAuthError(request, ResultCode.TOKEN_INVALID);
                filterChain.doFilter(request, response);
                return;
            }
            if (!Integer.valueOf(1).equals(sysUser.getIsActive())) {
                log.warn("JWT 认证失败：账号已禁用 username={}", username);
                setAuthError(request, ResultCode.TOKEN_REVOKED);
                filterChain.doFilter(request, response);
                return;
            }

            // 4. 构建认证对象，注入 SecurityContext
            LoginUserDetails userDetails = new LoginUserDetails(sysUser);
            UsernamePasswordAuthenticationToken authentication =
                    new UsernamePasswordAuthenticationToken(
                            userDetails, null, userDetails.getAuthorities());
            SecurityContextHolder.getContext().setAuthentication(authentication);

            log.debug("JWT 认证成功：username={} role={}", username, sysUser.getRole());

        } catch (BizException e) {
            // parseAccessToken 抛出的 TOKEN_EXPIRED / TOKEN_INVALID
            log.debug("JWT 校验失败：{}", e.getMessage());
            setAuthError(request, e.getResultCode());
        }

        filterChain.doFilter(request, response);
    }

    // ── 私有工具方法 ─────────────────────────────────────────────

    /** 从 Authorization 请求头提取 Bearer Token，格式不符时返回 null */
    private String extractToken(HttpServletRequest request) {
        String header = request.getHeader(HEADER_AUTHORIZATION);
        if (StringUtils.hasText(header) && header.startsWith(BEARER_PREFIX)) {
            return header.substring(BEARER_PREFIX.length());
        }
        return null;
    }

    /** 检查 jti 是否在 Redis 黑名单中 */
    private boolean isBlacklisted(String jti) {
        try {
            return Boolean.TRUE.equals(redisTemplate.hasKey(BLACKLIST_KEY_PREFIX + jti));
        } catch (Exception e) {
            // Redis 不可用时，保守放行（不因缓存故障阻断所有请求）
            log.error("Redis 黑名单查询失败，jti={}，错误：{}", jti, e.getMessage());
            return false;
        }
    }

    /** 通过 MyBatis Plus BaseMapper 根据用户名查询用户 */
    private SysUser loadUser(String username) {
        try {
            return sysUserMapper.selectOne(
                    new com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper<SysUser>()
                            .eq(SysUser::getUsername, username));
        } catch (Exception e) {
            log.error("加载用户失败 username={}：{}", username, e.getMessage());
            return null;
        }
    }

    /** 将认证错误码记录到 request attribute，供 EntryPoint 读取 */
    private void setAuthError(HttpServletRequest request, ResultCode resultCode) {
        request.setAttribute("AUTH_ERROR_CODE", resultCode);
    }
}
