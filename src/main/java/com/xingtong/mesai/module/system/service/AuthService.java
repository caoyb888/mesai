package com.xingtong.mesai.module.system.service;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.common.result.ResultCode;
import com.xingtong.mesai.module.system.dto.LoginRequest;
import com.xingtong.mesai.module.system.dto.TokenRefreshRequest;
import com.xingtong.mesai.module.system.dto.TokenRevokeRequest;
import com.xingtong.mesai.module.system.entity.SysUser;
import com.xingtong.mesai.module.system.enums.UserRole;
import com.xingtong.mesai.module.system.mapper.SysUserMapper;
import com.xingtong.mesai.module.system.security.JwtAuthenticationFilter;
import com.xingtong.mesai.module.system.security.JwtProperties;
import com.xingtong.mesai.module.system.security.JwtUtil;
import com.xingtong.mesai.module.system.vo.LoginVO;
import io.jsonwebtoken.Claims;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.concurrent.TimeUnit;

/**
 * 认证服务
 *
 * <p>负责登录、Token 刷新、登出、强制吊销四个认证场景的核心业务逻辑。
 * <p>Token 存储策略（Redis）：
 * <ul>
 *   <li>登出/吊销：将 access token 的 jti 写入黑名单，有效期与 Token 剩余时间一致</li>
 *   <li>刷新令牌：将 refresh token 的 jti 写入黑名单（令牌轮换，旧 refresh token 立即失效）</li>
 *   <li>强制吊销：将该用户所有 Token 标记失效（通过 user 维度的版本号实现）</li>
 * </ul>
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-1/2/3）
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class AuthService {

    /**
     * Redis Key：用户令牌版本号（revoke 时自增，JTI 中携带版本号可实现整体失效）。
     * 格式：jwt:user:version:{username}
     */
    private static final String USER_VERSION_KEY_PREFIX = "jwt:user:version:";

    private final SysUserMapper        sysUserMapper;
    private final JwtUtil              jwtUtil;
    private final JwtProperties        jwtProperties;
    private final PasswordEncoder      passwordEncoder;
    private final StringRedisTemplate  redisTemplate;

    // ── 登录 ──────────────────────────────────────────────────────

    /**
     * 用户名 + 密码登录，返回 accessToken + refreshToken。
     *
     * @param request 登录请求（username + password）
     * @return 登录 VO（含双 Token 及用户基本信息）
     */
    public LoginVO login(LoginRequest request) {
        // 1. 查询用户
        SysUser user = findActiveUserByUsername(request.getUsername());

        // 2. BCrypt 验证密码（禁止在日志中打印明文密码）
        if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            log.warn("登录失败：密码错误 username={}", request.getUsername());
            throw new BizException(ResultCode.TOKEN_INVALID, "用户名或密码错误");
        }

        // 3. 生成双 Token
        String role         = user.getRole();
        String accessToken  = jwtUtil.generateAccessToken(user.getUsername(), role);
        String refreshToken = jwtUtil.generateRefreshToken(user.getUsername(), role);

        log.info("用户登录成功：username={} role={}", user.getUsername(), role);

        return buildLoginVO(user, accessToken, refreshToken);
    }

    // ── 刷新 ──────────────────────────────────────────────────────

    /**
     * 使用 refreshToken 换取新的 accessToken + refreshToken（令牌轮换）。
     *
     * <p>旧 refreshToken 在成功换取后立即加入黑名单，防止重放攻击。
     *
     * @param request 刷新请求（refreshToken）
     * @return 新的登录 VO
     */
    public LoginVO refresh(TokenRefreshRequest request) {
        // 1. 解析并校验 refreshToken（type=refresh 验证在内部完成）
        Claims claims = jwtUtil.parseRefreshToken(request.getRefreshToken());

        // 2. 检查 refreshToken 是否已被吊销（轮换后的旧 token）
        String oldJti = jwtUtil.getJti(claims);
        if (isBlacklisted(oldJti)) {
            log.warn("Token 刷新失败：refreshToken 已吊销 jti={}", oldJti);
            throw new BizException(ResultCode.TOKEN_REVOKED);
        }

        // 3. 验证用户仍然有效
        String username = jwtUtil.getUsername(claims);
        SysUser user    = findActiveUserByUsername(username);

        // 4. 将旧 refreshToken 加入黑名单（剩余有效期）
        long remainingSec = jwtUtil.getRemainingSeconds(claims);
        blacklist(oldJti, remainingSec);

        // 5. 生成新的双 Token
        String role            = user.getRole();
        String newAccessToken  = jwtUtil.generateAccessToken(username, role);
        String newRefreshToken = jwtUtil.generateRefreshToken(username, role);

        log.info("Token 刷新成功：username={}", username);

        return buildLoginVO(user, newAccessToken, newRefreshToken);
    }

    // ── 登出 ──────────────────────────────────────────────────────

    /**
     * 用户主动登出：将当前 accessToken 加入黑名单。
     *
     * @param accessToken 当前请求携带的 access token（已经过过滤器校验）
     */
    public void logout(String accessToken) {
        try {
            Claims claims = jwtUtil.parseAccessToken(accessToken);
            String jti    = jwtUtil.getJti(claims);
            long remaining = jwtUtil.getRemainingSeconds(claims);
            blacklist(jti, remaining);
            log.info("用户登出成功：jti={}", jti);
        } catch (BizException e) {
            // Token 已过期或无效，视为已登出，不报错
            log.debug("登出时 Token 已失效：{}", e.getMessage());
        }
    }

    // ── 强制吊销 ─────────────────────────────────────────────────

    /**
     * 管理员强制吊销指定用户的所有 Token（踢出登录）。
     *
     * <p>实现方式：在 Redis 中设置该用户的版本号（或标记），
     * JwtAuthenticationFilter 在认证时检查该版本号；
     * 此处通过设置一个用户维度的黑名单标记（有效期 = refreshToken 最大有效期），
     * 过滤器中检查该标记以拒绝所有旧 Token。
     *
     * @param request 吊销请求（目标 username）
     */
    public void revoke(TokenRevokeRequest request) {
        String username = request.getUsername();

        // 验证目标用户存在
        SysUser target = sysUserMapper.selectOne(
                new LambdaQueryWrapper<SysUser>().eq(SysUser::getUsername, username));
        if (target == null) {
            throw BizException.notFound("用户", username);
        }

        // 设置用户维度的吊销标记（有效期 = refreshToken 最大有效期）
        String key = USER_VERSION_KEY_PREFIX + username;
        redisTemplate.opsForValue().set(key, "revoked",
                jwtProperties.getRefreshTokenExpireSeconds(), TimeUnit.SECONDS);

        log.info("强制吊销用户所有 Token：targetUsername={}", username);
    }

    // ── 私有工具方法 ─────────────────────────────────────────────

    /**
     * 查询启用状态的用户，不存在或已禁用时抛出 BizException。
     */
    private SysUser findActiveUserByUsername(String username) {
        SysUser user = sysUserMapper.selectOne(
                new LambdaQueryWrapper<SysUser>().eq(SysUser::getUsername, username));
        if (user == null) {
            throw new BizException(ResultCode.TOKEN_INVALID, "用户名或密码错误");
        }
        if (!Integer.valueOf(1).equals(user.getIsActive())) {
            throw new BizException(ResultCode.TOKEN_REVOKED, "账号已被禁用");
        }
        return user;
    }

    /** 将 jti 写入 Redis 黑名单，有效期 = Token 剩余时间 */
    private void blacklist(String jti, long remainingSeconds) {
        if (remainingSeconds <= 0) {
            return;
        }
        try {
            redisTemplate.opsForValue().set(
                    JwtAuthenticationFilter.BLACKLIST_KEY_PREFIX + jti,
                    "1",
                    remainingSeconds,
                    TimeUnit.SECONDS);
        } catch (Exception e) {
            log.error("写入 Redis 黑名单失败 jti={}：{}", jti, e.getMessage());
            throw new BizException(ResultCode.REDIS_OPERATION_FAILED, "登出操作失败，请稍后重试");
        }
    }

    /** 检查 jti 是否在 Redis 黑名单 */
    private boolean isBlacklisted(String jti) {
        try {
            return Boolean.TRUE.equals(
                    redisTemplate.hasKey(JwtAuthenticationFilter.BLACKLIST_KEY_PREFIX + jti));
        } catch (Exception e) {
            log.error("查询 Redis 黑名单失败 jti={}：{}", jti, e.getMessage());
            return false;
        }
    }

    /** 组装登录响应 VO */
    private LoginVO buildLoginVO(SysUser user, String accessToken, String refreshToken) {
        Claims accessClaims = jwtUtil.parseAccessToken(accessToken);
        long expiresIn      = jwtUtil.getRemainingSeconds(accessClaims);

        String roleDisplayName;
        try {
            roleDisplayName = UserRole.fromCode(user.getRole()).getDisplayName();
        } catch (IllegalArgumentException e) {
            roleDisplayName = user.getRole();
        }

        return LoginVO.builder()
                .accessToken(accessToken)
                .refreshToken(refreshToken)
                .tokenType("Bearer")
                .expiresIn(expiresIn)
                .username(user.getUsername())
                .realName(user.getRealName())
                .role(user.getRole())
                .roleDisplayName(roleDisplayName)
                .build();
    }
}
