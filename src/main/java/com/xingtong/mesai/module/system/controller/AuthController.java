package com.xingtong.mesai.module.system.controller;

import com.xingtong.mesai.common.result.ResultVO;
import com.xingtong.mesai.module.system.annotation.RequirePermission;
import com.xingtong.mesai.module.system.dto.LoginRequest;
import com.xingtong.mesai.module.system.dto.TokenRefreshRequest;
import com.xingtong.mesai.module.system.dto.TokenRevokeRequest;
import com.xingtong.mesai.module.system.service.AuthService;
import com.xingtong.mesai.module.system.vo.LoginVO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.util.StringUtils;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 认证 Controller
 *
 * <p>提供 JWT 认证相关的四个接口：
 * <ul>
 *   <li>POST /system/auth/login   - 用户登录，返回双 Token</li>
 *   <li>POST /system/auth/refresh - 刷新 accessToken（令牌轮换）</li>
 *   <li>POST /system/auth/logout  - 用户主动登出</li>
 *   <li>POST /system/auth/revoke  - 管理员强制吊销用户所有 Token</li>
 * </ul>
 *
 * <p>login 接口在 SecurityConfig 中配置为白名单，其余接口均需有效 JWT。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-1/2/3）
 */
@Slf4j
@RestController
@RequestMapping("/system/auth")
@RequiredArgsConstructor
public class AuthController {

    private static final String BEARER_PREFIX = "Bearer ";

    private final AuthService authService;

    /**
     * 用户登录。
     *
     * <p>验证用户名 + 密码（BCrypt），成功后返回 accessToken（8h）+ refreshToken（7d）。
     * <p>该接口无需 Token（白名单路径）。
     *
     * @param request 登录请求（username + password）
     * @return 登录响应 VO（accessToken、refreshToken、用户信息）
     */
    @PostMapping("/login")
    public ResultVO<LoginVO> login(@Validated @RequestBody LoginRequest request) {
        log.info("用户登录请求：username={}", request.getUsername());
        LoginVO loginVO = authService.login(request);
        return ResultVO.success(loginVO);
    }

    /**
     * 刷新 Token（令牌轮换）。
     *
     * <p>携带有效 refreshToken 换取新的 accessToken + refreshToken，
     * 旧 refreshToken 立即失效（防重放）。
     *
     * @param request 刷新请求（refreshToken）
     * @return 新的登录 VO
     */
    @PostMapping("/refresh")
    public ResultVO<LoginVO> refresh(@Validated @RequestBody TokenRefreshRequest request) {
        LoginVO loginVO = authService.refresh(request);
        return ResultVO.success(loginVO);
    }

    /**
     * 用户主动登出。
     *
     * <p>将当前请求的 accessToken 加入 Redis 黑名单，立即失效。
     * 客户端应同时清除本地存储的所有 Token。
     *
     * @param authorizationHeader Authorization 请求头（Bearer {accessToken}）
     * @return 操作成功响应
     */
    @PostMapping("/logout")
    public ResultVO<Void> logout(
            @RequestHeader(value = "Authorization", required = false) String authorizationHeader) {
        String token = extractToken(authorizationHeader);
        if (StringUtils.hasText(token)) {
            authService.logout(token);
        }
        return ResultVO.success();
    }

    /**
     * 强制吊销指定用户的所有 Token（踢出登录）。
     *
     * <p>需要 {@code system:admin} 权限（IT_MANAGER 或 TECH_LEAD）。
     * <p>适用场景：用户离职、账号异常、安全事件响应等。
     *
     * @param request 吊销请求（目标 username）
     * @return 操作成功响应
     */
    @PostMapping("/revoke")
    @RequirePermission("system:admin")
    public ResultVO<Void> revoke(@Validated @RequestBody TokenRevokeRequest request) {
        log.info("强制吊销用户 Token：targetUsername={}", request.getUsername());
        authService.revoke(request);
        return ResultVO.success();
    }

    // ── 私有工具方法 ─────────────────────────────────────────────

    /** 从 Authorization 请求头中提取 Bearer Token */
    private String extractToken(String authorizationHeader) {
        if (StringUtils.hasText(authorizationHeader)
                && authorizationHeader.startsWith(BEARER_PREFIX)) {
            return authorizationHeader.substring(BEARER_PREFIX.length());
        }
        return null;
    }
}
