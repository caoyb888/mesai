package com.xingtong.mesai.module.system.security;

import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.common.result.ResultCode;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import java.nio.charset.StandardCharsets;
import java.security.Key;
import java.util.Base64;
import java.util.Date;
import java.util.UUID;

/**
 * JWT 工具类
 *
 * <p>基于 jjwt 0.11.5，提供 accessToken / refreshToken 的生成、解析与校验。
 * <p>签名算法：HMAC-SHA256；密钥通过 JwtProperties 注入，禁止硬编码。
 * <p>Claims 说明：
 * <ul>
 *   <li>sub  - 用户名（唯一标识）</li>
 *   <li>jti  - 随机 UUID（用于 Redis 黑名单精确吊销）</li>
 *   <li>role - 角色代码</li>
 *   <li>type - "access" 或 "refresh"（防止 refresh Token 被当作 access Token 使用）</li>
 * </ul>
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-1）
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class JwtUtil {

    private static final String CLAIM_ROLE = "role";
    private static final String CLAIM_TYPE = "type";
    private static final String TYPE_ACCESS  = "access";
    private static final String TYPE_REFRESH = "refresh";

    private final JwtProperties jwtProperties;

    /** HMAC-SHA256 签名密钥（启动时根据配置构建，不可变） */
    private Key signingKey;

    /**
     * 初始化签名密钥。
     * 支持两种格式的 secret：Base64 编码字符串 或 普通 UTF-8 字符串。
     */
    @PostConstruct
    public void init() {
        String secret = jwtProperties.getSecret();
        byte[] keyBytes;
        try {
            keyBytes = Base64.getDecoder().decode(secret);
        } catch (IllegalArgumentException e) {
            // 非 Base64 格式时直接使用 UTF-8 字节
            keyBytes = secret.getBytes(StandardCharsets.UTF_8);
        }
        this.signingKey = Keys.hmacShaKeyFor(keyBytes);
        log.info("JWT 签名密钥初始化完成，accessToken 有效期={}s，refreshToken 有效期={}s",
                jwtProperties.getAccessTokenExpireSeconds(),
                jwtProperties.getRefreshTokenExpireSeconds());
    }

    // ── 生成 Token ────────────────────────────────────────────────

    /**
     * 生成访问令牌（access token）。
     *
     * @param username 用户名
     * @param role     角色代码
     * @return JWT 字符串
     */
    public String generateAccessToken(String username, String role) {
        return buildToken(username, role, TYPE_ACCESS, jwtProperties.getAccessTokenExpireSeconds());
    }

    /**
     * 生成刷新令牌（refresh token）。
     *
     * @param username 用户名
     * @param role     角色代码
     * @return JWT 字符串
     */
    public String generateRefreshToken(String username, String role) {
        return buildToken(username, role, TYPE_REFRESH, jwtProperties.getRefreshTokenExpireSeconds());
    }

    // ── 解析 Token ────────────────────────────────────────────────

    /**
     * 解析并校验 Token，返回 Claims。
     *
     * <p>异常统一转换为 BizException：
     * <ul>
     *   <li>过期 → TOKEN_EXPIRED</li>
     *   <li>签名非法 / 格式错误 → TOKEN_INVALID</li>
     * </ul>
     *
     * @param token JWT 字符串
     * @return 有效的 Claims 对象
     */
    public Claims parseToken(String token) {
        try {
            return Jwts.parserBuilder()
                    .setSigningKey(signingKey)
                    .build()
                    .parseClaimsJws(token)
                    .getBody();
        } catch (ExpiredJwtException e) {
            log.debug("JWT 已过期：jti={}", extractJtiSafe(e));
            throw new BizException(ResultCode.TOKEN_EXPIRED);
        } catch (JwtException e) {
            log.warn("JWT 签名校验失败：{}", e.getMessage());
            throw new BizException(ResultCode.TOKEN_INVALID);
        }
    }

    /**
     * 解析 access token，并验证 type=access。
     *
     * @param token JWT 字符串
     * @return 有效的 Claims
     */
    public Claims parseAccessToken(String token) {
        Claims claims = parseToken(token);
        if (!TYPE_ACCESS.equals(claims.get(CLAIM_TYPE, String.class))) {
            throw new BizException(ResultCode.TOKEN_INVALID);
        }
        return claims;
    }

    /**
     * 解析 refresh token，并验证 type=refresh。
     *
     * @param token JWT 字符串
     * @return 有效的 Claims
     */
    public Claims parseRefreshToken(String token) {
        Claims claims = parseToken(token);
        if (!TYPE_REFRESH.equals(claims.get(CLAIM_TYPE, String.class))) {
            throw new BizException(ResultCode.TOKEN_INVALID);
        }
        return claims;
    }

    // ── Claims 字段提取 ───────────────────────────────────────────

    /**
     * 从 Claims 中提取用户名（sub 字段）。
     */
    public String getUsername(Claims claims) {
        return claims.getSubject();
    }

    /**
     * 从 Claims 中提取角色代码（role 字段）。
     */
    public String getRole(Claims claims) {
        return claims.get(CLAIM_ROLE, String.class);
    }

    /**
     * 从 Claims 中提取 JWT ID（jti 字段），用于黑名单存储。
     */
    public String getJti(Claims claims) {
        return claims.getId();
    }

    /**
     * 计算 Token 的剩余有效秒数（用于响应 expiresIn 字段）。
     */
    public long getRemainingSeconds(Claims claims) {
        long expireMs = claims.getExpiration().getTime();
        long nowMs    = System.currentTimeMillis();
        return Math.max(0L, (expireMs - nowMs) / 1000L);
    }

    // ── 私有工具方法 ─────────────────────────────────────────────

    private String buildToken(String username, String role, String type, long expireSeconds) {
        long nowMs    = System.currentTimeMillis();
        long expireMs = nowMs + expireSeconds * 1000L;
        return Jwts.builder()
                .setId(UUID.randomUUID().toString())
                .setSubject(username)
                .claim(CLAIM_ROLE, role)
                .claim(CLAIM_TYPE, type)
                .setIssuedAt(new Date(nowMs))
                .setExpiration(new Date(expireMs))
                .signWith(signingKey, SignatureAlgorithm.HS256)
                .compact();
    }

    /**
     * 安全地从过期异常中提取 jti（仅用于 DEBUG 日志，不影响主流程）。
     */
    private String extractJtiSafe(ExpiredJwtException e) {
        try {
            return e.getClaims().getId();
        } catch (Exception ignored) {
            return "unknown";
        }
    }
}
