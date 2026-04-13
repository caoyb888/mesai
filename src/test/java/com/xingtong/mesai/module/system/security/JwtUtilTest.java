package com.xingtong.mesai.module.system.security;

import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.common.result.ResultCode;
import io.jsonwebtoken.Claims;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

/**
 * JwtUtil 单元测试
 *
 * <p>覆盖 Token 生成、解析、有效期、类型校验、伪造签名检测等核心场景。
 * <p>纯单元测试，不加载 Spring Context，测试执行速度快。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-8）
 */
class JwtUtilTest {

    /** 测试用 Base64 密钥（32字节，仅用于测试） */
    private static final String TEST_SECRET =
            "dGVzdC1zZWNyZXQtZm9yLXVuaXQtdGVzdC0zMmJ5dGVzIQ==";

    private JwtUtil jwtUtil;

    @BeforeEach
    void setUp() {
        JwtProperties props = new JwtProperties();
        props.setSecret(TEST_SECRET);
        props.setAccessTokenExpireSeconds(3600L);   // 1 小时
        props.setRefreshTokenExpireSeconds(86400L);  // 1 天

        jwtUtil = new JwtUtil(props);
        jwtUtil.init();
    }

    // ── 生成 Token 基础测试 ───────────────────────────────────────

    @Test
    void generateAccessToken_shouldReturnNonBlankToken() {
        String token = jwtUtil.generateAccessToken("alice", "IT_MANAGER");
        assertThat(token).isNotBlank();
        // JWT 格式：header.payload.signature
        assertThat(token.split("\\.")).hasSize(3);
    }

    @Test
    void generateRefreshToken_shouldReturnNonBlankToken() {
        String token = jwtUtil.generateRefreshToken("alice", "IT_MANAGER");
        assertThat(token).isNotBlank();
    }

    // ── 解析 access token ─────────────────────────────────────────

    @Test
    void parseAccessToken_validToken_shouldReturnCorrectClaims() {
        String token  = jwtUtil.generateAccessToken("bob", "TECH_LEAD");
        Claims claims = jwtUtil.parseAccessToken(token);

        assertThat(jwtUtil.getUsername(claims)).isEqualTo("bob");
        assertThat(jwtUtil.getRole(claims)).isEqualTo("TECH_LEAD");
        assertThat(jwtUtil.getJti(claims)).isNotBlank();
    }

    @Test
    void parseAccessToken_withRefreshToken_shouldThrowTokenInvalid() {
        // refresh token 不应被当作 access token 使用
        String refreshToken = jwtUtil.generateRefreshToken("bob", "TECH_LEAD");

        assertThatThrownBy(() -> jwtUtil.parseAccessToken(refreshToken))
                .isInstanceOf(BizException.class)
                .satisfies(ex -> assertThat(((BizException) ex).getResultCode())
                        .isEqualTo(ResultCode.TOKEN_INVALID));
    }

    // ── 解析 refresh token ────────────────────────────────────────

    @Test
    void parseRefreshToken_validToken_shouldReturnCorrectClaims() {
        String token  = jwtUtil.generateRefreshToken("carol", "IT_REVIEWER");
        Claims claims = jwtUtil.parseRefreshToken(token);

        assertThat(jwtUtil.getUsername(claims)).isEqualTo("carol");
        assertThat(jwtUtil.getRole(claims)).isEqualTo("IT_REVIEWER");
    }

    @Test
    void parseRefreshToken_withAccessToken_shouldThrowTokenInvalid() {
        // access token 不应被当作 refresh token 使用
        String accessToken = jwtUtil.generateAccessToken("carol", "IT_REVIEWER");

        assertThatThrownBy(() -> jwtUtil.parseRefreshToken(accessToken))
                .isInstanceOf(BizException.class)
                .satisfies(ex -> assertThat(((BizException) ex).getResultCode())
                        .isEqualTo(ResultCode.TOKEN_INVALID));
    }

    // ── 无效 / 伪造 Token ─────────────────────────────────────────

    @Test
    void parseToken_invalidSignature_shouldThrowTokenInvalid() {
        String token = jwtUtil.generateAccessToken("dave", "MANAGER");
        // 篡改签名部分
        String tampered = token.substring(0, token.lastIndexOf('.') + 1) + "invalidsignature";

        assertThatThrownBy(() -> jwtUtil.parseToken(tampered))
                .isInstanceOf(BizException.class)
                .satisfies(ex -> assertThat(((BizException) ex).getResultCode())
                        .isEqualTo(ResultCode.TOKEN_INVALID));
    }

    @Test
    void parseToken_malformedToken_shouldThrowTokenInvalid() {
        assertThatThrownBy(() -> jwtUtil.parseToken("not.a.jwt"))
                .isInstanceOf(BizException.class)
                .satisfies(ex -> assertThat(((BizException) ex).getResultCode())
                        .isEqualTo(ResultCode.TOKEN_INVALID));
    }

    @Test
    void parseToken_blankToken_shouldThrowTokenInvalid() {
        assertThatThrownBy(() -> jwtUtil.parseToken(""))
                .isInstanceOf(Exception.class);
    }

    // ── 有效期相关 ────────────────────────────────────────────────

    @Test
    void getRemainingSeconds_freshToken_shouldBePositive() {
        String token  = jwtUtil.generateAccessToken("eve", "BUSINESS_USER");
        Claims claims = jwtUtil.parseAccessToken(token);

        long remaining = jwtUtil.getRemainingSeconds(claims);
        assertThat(remaining).isGreaterThan(0L).isLessThanOrEqualTo(3600L);
    }

    // ── JTI 唯一性 ────────────────────────────────────────────────

    @Test
    void generateAccessToken_consecutiveCalls_shouldProduceDifferentJti() {
        String token1 = jwtUtil.generateAccessToken("frank", "IT_MANAGER");
        String token2 = jwtUtil.generateAccessToken("frank", "IT_MANAGER");

        Claims claims1 = jwtUtil.parseAccessToken(token1);
        Claims claims2 = jwtUtil.parseAccessToken(token2);

        // 每次生成的 JTI 应不同（UUID）
        assertThat(jwtUtil.getJti(claims1)).isNotEqualTo(jwtUtil.getJti(claims2));
    }
}
