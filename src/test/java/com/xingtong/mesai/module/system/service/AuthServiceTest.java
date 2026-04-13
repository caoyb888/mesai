package com.xingtong.mesai.module.system.service;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.common.result.ResultCode;
import com.xingtong.mesai.module.system.dto.LoginRequest;
import com.xingtong.mesai.module.system.dto.TokenRefreshRequest;
import com.xingtong.mesai.module.system.dto.TokenRevokeRequest;
import com.xingtong.mesai.module.system.entity.SysUser;
import com.xingtong.mesai.module.system.mapper.SysUserMapper;
import com.xingtong.mesai.module.system.security.JwtProperties;
import com.xingtong.mesai.module.system.security.JwtUtil;
import com.xingtong.mesai.module.system.vo.LoginVO;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentMatchers;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

/**
 * AuthService 单元测试
 *
 * <p>使用 Mockito 模拟 SysUserMapper 和 Redis，覆盖登录、刷新、登出、吊销核心场景。
 * <p>密码校验使用真实 BCryptPasswordEncoder 确保逻辑正确。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-8）
 */
@ExtendWith(MockitoExtension.class)
class AuthServiceTest {

    private static final String TEST_SECRET =
            "dGVzdC1zZWNyZXQtZm9yLXVuaXQtdGVzdC0zMmJ5dGVzIQ==";

    @Mock
    private SysUserMapper       sysUserMapper;
    @Mock
    private StringRedisTemplate redisTemplate;
    @Mock
    private ValueOperations<String, String> valueOps;

    /** 使用真实 BCrypt 确保密码校验逻辑正确 */
    @Spy
    private PasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    private JwtUtil     jwtUtil;
    private AuthService authService;

    /** 测试用的启用状态用户 */
    private SysUser activeUser;

    @BeforeEach
    void setUp() {
        // 构建真实 JwtUtil（无法用 @InjectMocks + @Spy 混用，手动构造）
        JwtProperties props = new JwtProperties();
        props.setSecret(TEST_SECRET);
        props.setAccessTokenExpireSeconds(3600L);
        props.setRefreshTokenExpireSeconds(86400L);
        jwtUtil = new JwtUtil(props);
        jwtUtil.init();

        authService = new AuthService(sysUserMapper, jwtUtil, props, passwordEncoder, redisTemplate);

        // 构建测试用用户
        activeUser = new SysUser();
        activeUser.setId(1L);
        activeUser.setUsername("alice");
        activeUser.setRealName("爱丽丝");
        activeUser.setPassword(passwordEncoder.encode("Correct@123"));
        activeUser.setRole("IT_MANAGER");
        activeUser.setIsActive(1);
    }

    // ── 登录成功 ──────────────────────────────────────────────────

    @Test
    void login_correctCredentials_shouldReturnLoginVO() {
        when(sysUserMapper.selectOne(any(LambdaQueryWrapper.class))).thenReturn(activeUser);

        LoginRequest request = new LoginRequest();
        request.setUsername("alice");
        request.setPassword("Correct@123");

        LoginVO vo = authService.login(request);

        assertThat(vo.getAccessToken()).isNotBlank();
        assertThat(vo.getRefreshToken()).isNotBlank();
        assertThat(vo.getTokenType()).isEqualTo("Bearer");
        assertThat(vo.getExpiresIn()).isGreaterThan(0L);
        assertThat(vo.getUsername()).isEqualTo("alice");
        assertThat(vo.getRole()).isEqualTo("IT_MANAGER");
        assertThat(vo.getRoleDisplayName()).isEqualTo("IT负责人");
    }

    // ── 登录失败：密码错误 ────────────────────────────────────────

    @Test
    void login_wrongPassword_shouldThrowBizException() {
        when(sysUserMapper.selectOne(any(LambdaQueryWrapper.class))).thenReturn(activeUser);

        LoginRequest request = new LoginRequest();
        request.setUsername("alice");
        request.setPassword("WrongPassword");

        assertThatThrownBy(() -> authService.login(request))
                .isInstanceOf(BizException.class)
                .satisfies(ex -> assertThat(((BizException) ex).getResultCode())
                        .isEqualTo(ResultCode.TOKEN_INVALID));
    }

    // ── 登录失败：用户不存在 ──────────────────────────────────────

    @Test
    void login_userNotFound_shouldThrowBizException() {
        when(sysUserMapper.selectOne(any(LambdaQueryWrapper.class))).thenReturn(null);

        LoginRequest request = new LoginRequest();
        request.setUsername("nonexistent");
        request.setPassword("any");

        assertThatThrownBy(() -> authService.login(request))
                .isInstanceOf(BizException.class)
                .satisfies(ex -> assertThat(((BizException) ex).getResultCode())
                        .isEqualTo(ResultCode.TOKEN_INVALID));
    }

    // ── 登录失败：账号被禁用 ──────────────────────────────────────

    @Test
    void login_disabledUser_shouldThrowTokenRevoked() {
        SysUser disabledUser = new SysUser();
        disabledUser.setUsername("bob");
        disabledUser.setPassword(passwordEncoder.encode("Pass@123"));
        disabledUser.setRole("IT_REVIEWER");
        disabledUser.setIsActive(0); // 禁用

        when(sysUserMapper.selectOne(any(LambdaQueryWrapper.class))).thenReturn(disabledUser);

        LoginRequest request = new LoginRequest();
        request.setUsername("bob");
        request.setPassword("Pass@123");

        assertThatThrownBy(() -> authService.login(request))
                .isInstanceOf(BizException.class)
                .satisfies(ex -> assertThat(((BizException) ex).getResultCode())
                        .isEqualTo(ResultCode.TOKEN_REVOKED));
    }

    // ── Token 刷新成功 ────────────────────────────────────────────

    @Test
    void refresh_validRefreshToken_shouldReturnNewTokens() {
        // 准备一个有效的 refreshToken
        String oldRefreshToken = jwtUtil.generateRefreshToken("alice", "IT_MANAGER");

        // Redis 黑名单中不存在（Token 未吊销）
        when(redisTemplate.hasKey(anyString())).thenReturn(false);
        when(sysUserMapper.selectOne(any(LambdaQueryWrapper.class))).thenReturn(activeUser);
        when(redisTemplate.opsForValue()).thenReturn(valueOps);

        TokenRefreshRequest request = new TokenRefreshRequest();
        request.setRefreshToken(oldRefreshToken);

        LoginVO vo = authService.refresh(request);

        assertThat(vo.getAccessToken()).isNotBlank();
        assertThat(vo.getRefreshToken()).isNotBlank();
        // 新旧 refreshToken 应不同（令牌轮换）
        assertThat(vo.getRefreshToken()).isNotEqualTo(oldRefreshToken);
    }

    // ── Token 刷新失败：使用 access token ────────────────────────

    @Test
    void refresh_withAccessToken_shouldThrowTokenInvalid() {
        String accessToken = jwtUtil.generateAccessToken("alice", "IT_MANAGER");

        TokenRefreshRequest request = new TokenRefreshRequest();
        request.setRefreshToken(accessToken);

        assertThatThrownBy(() -> authService.refresh(request))
                .isInstanceOf(BizException.class)
                .satisfies(ex -> assertThat(((BizException) ex).getResultCode())
                        .isEqualTo(ResultCode.TOKEN_INVALID));
    }

    // ── Token 刷新失败：refreshToken 已在黑名单 ───────────────────

    @Test
    void refresh_blacklistedRefreshToken_shouldThrowTokenRevoked() {
        String oldRefreshToken = jwtUtil.generateRefreshToken("alice", "IT_MANAGER");

        // 模拟 Redis 中已存在该 jti（Token 已吊销）
        when(redisTemplate.hasKey(anyString())).thenReturn(true);

        TokenRefreshRequest request = new TokenRefreshRequest();
        request.setRefreshToken(oldRefreshToken);

        assertThatThrownBy(() -> authService.refresh(request))
                .isInstanceOf(BizException.class)
                .satisfies(ex -> assertThat(((BizException) ex).getResultCode())
                        .isEqualTo(ResultCode.TOKEN_REVOKED));
    }

    // ── 登出成功 ──────────────────────────────────────────────────

    @Test
    void logout_validAccessToken_shouldBlacklistJti() {
        String accessToken = jwtUtil.generateAccessToken("alice", "IT_MANAGER");
        when(redisTemplate.opsForValue()).thenReturn(valueOps);

        authService.logout(accessToken);

        // 验证 jti 已被写入 Redis 黑名单
        verify(valueOps).set(
                ArgumentMatchers.startsWith("jwt:blacklist:"),
                eq("1"),
                anyLong(),
                any());
    }

    // ── 强制吊销成功 ──────────────────────────────────────────────

    @Test
    void revoke_existingUser_shouldSetUserVersionKey() {
        when(sysUserMapper.selectOne(any(LambdaQueryWrapper.class))).thenReturn(activeUser);
        when(redisTemplate.opsForValue()).thenReturn(valueOps);

        TokenRevokeRequest request = new TokenRevokeRequest();
        request.setUsername("alice");

        authService.revoke(request);

        // 验证写入了用户维度的吊销标记
        verify(valueOps).set(
                eq("jwt:user:version:alice"),
                eq("revoked"),
                anyLong(),
                any());
    }

    // ── 强制吊销失败：目标用户不存在 ─────────────────────────────

    @Test
    void revoke_nonExistentUser_shouldThrowNotFound() {
        when(sysUserMapper.selectOne(any(LambdaQueryWrapper.class))).thenReturn(null);

        TokenRevokeRequest request = new TokenRevokeRequest();
        request.setUsername("ghost");

        assertThatThrownBy(() -> authService.revoke(request))
                .isInstanceOf(BizException.class)
                .satisfies(ex -> assertThat(((BizException) ex).getResultCode())
                        .isEqualTo(ResultCode.RESOURCE_NOT_FOUND));
    }
}
