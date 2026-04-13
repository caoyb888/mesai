package com.xingtong.mesai.module.system.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.common.result.ResultCode;
import com.xingtong.mesai.module.system.dto.LoginRequest;
import com.xingtong.mesai.module.system.dto.TokenRefreshRequest;
import com.xingtong.mesai.module.system.dto.TokenRevokeRequest;
import com.xingtong.mesai.module.system.mapper.SysUserMapper;
import com.xingtong.mesai.module.system.security.JwtProperties;
import com.xingtong.mesai.module.system.security.JwtUtil;
import com.xingtong.mesai.module.system.service.AuthService;
import com.xingtong.mesai.module.system.vo.LoginVO;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * AuthController MockMvc 测试
 *
 * <p>禁用 Spring Security 过滤器，专注于控制器层的请求绑定、参数校验、响应格式测试。
 * <p>AuthService 用 MockBean 替代，隔离业务逻辑依赖。
 * <p>通过 excludeFilters 排除 @Mapper 接口，避免 @WebMvcTest 误扫描 MyBatis Mapper。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-8）
 */
@WebMvcTest(
    controllers = AuthController.class,
    excludeAutoConfiguration = com.xingtong.mesai.config.MyBatisMapperScanConfig.class
)
@AutoConfigureMockMvc(addFilters = false)   // 禁用 Security 过滤器链，专注控制器逻辑
class AuthControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private AuthService authService;

    // SecurityConfig 的构造依赖（@WebMvcTest 会实例化 SecurityConfig Bean）
    @MockBean
    private JwtUtil jwtUtil;
    @MockBean
    private JwtProperties jwtProperties;
    @MockBean
    private SysUserMapper sysUserMapper;
    @MockBean
    private StringRedisTemplate redisTemplate;

    // ── POST /system/auth/login ───────────────────────────────────

    @Test
    void login_validRequest_shouldReturn200WithTokens() throws Exception {
        LoginVO mockVO = LoginVO.builder()
                .accessToken("mock.access.token")
                .refreshToken("mock.refresh.token")
                .tokenType("Bearer")
                .expiresIn(28800L)
                .username("alice")
                .role("IT_MANAGER")
                .roleDisplayName("IT负责人")
                .build();
        when(authService.login(any())).thenReturn(mockVO);

        LoginRequest req = new LoginRequest();
        req.setUsername("alice");
        req.setPassword("Correct@123");

        mockMvc.perform(post("/system/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(0))
                .andExpect(jsonPath("$.data.accessToken").value("mock.access.token"))
                .andExpect(jsonPath("$.data.tokenType").value("Bearer"))
                .andExpect(jsonPath("$.data.username").value("alice"));
    }

    @Test
    void login_emptyUsername_shouldReturn400() throws Exception {
        LoginRequest req = new LoginRequest();
        req.setUsername("");          // 空用户名，@NotBlank 触发
        req.setPassword("Pass@123");

        mockMvc.perform(post("/system/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value(ResultCode.PARAM_INVALID.getCode()));
    }

    @Test
    void login_emptyPassword_shouldReturn400() throws Exception {
        LoginRequest req = new LoginRequest();
        req.setUsername("alice");
        req.setPassword("");          // 空密码，@NotBlank 触发

        mockMvc.perform(post("/system/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isBadRequest());
    }

    @Test
    void login_wrongCredentials_shouldReturn200WithErrorCode() throws Exception {
        when(authService.login(any())).thenThrow(
                new BizException(ResultCode.TOKEN_INVALID, "用户名或密码错误"));

        LoginRequest req = new LoginRequest();
        req.setUsername("alice");
        req.setPassword("WrongPass");

        mockMvc.perform(post("/system/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(ResultCode.TOKEN_INVALID.getCode()));
    }

    @Test
    void login_missingBody_shouldReturn400() throws Exception {
        mockMvc.perform(post("/system/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))      // 空 JSON，必填字段缺失
                .andExpect(status().isBadRequest());
    }

    // ── POST /system/auth/refresh ─────────────────────────────────

    @Test
    void refresh_validRequest_shouldReturn200() throws Exception {
        LoginVO mockVO = LoginVO.builder()
                .accessToken("new.access.token")
                .refreshToken("new.refresh.token")
                .tokenType("Bearer")
                .expiresIn(28800L)
                .username("alice")
                .role("IT_MANAGER")
                .roleDisplayName("IT负责人")
                .build();
        when(authService.refresh(any())).thenReturn(mockVO);

        TokenRefreshRequest req = new TokenRefreshRequest();
        req.setRefreshToken("old.refresh.token");

        mockMvc.perform(post("/system/auth/refresh")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(0))
                .andExpect(jsonPath("$.data.accessToken").value("new.access.token"));
    }

    @Test
    void refresh_emptyToken_shouldReturn400() throws Exception {
        TokenRefreshRequest req = new TokenRefreshRequest();
        req.setRefreshToken("");    // @NotBlank 触发

        mockMvc.perform(post("/system/auth/refresh")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isBadRequest());
    }

    // ── POST /system/auth/logout ──────────────────────────────────

    @Test
    void logout_withToken_shouldReturn200() throws Exception {
        doNothing().when(authService).logout(anyString());

        mockMvc.perform(post("/system/auth/logout")
                        .header("Authorization", "Bearer some.valid.token"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(0));
    }

    @Test
    void logout_withoutToken_shouldReturn200() throws Exception {
        // 无 Token 也应正常返回（幂等登出）
        mockMvc.perform(post("/system/auth/logout"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(0));
    }

    // ── POST /system/auth/revoke ──────────────────────────────────

    @Test
    void revoke_validRequest_shouldReturn200() throws Exception {
        doNothing().when(authService).revoke(any());

        TokenRevokeRequest req = new TokenRevokeRequest();
        req.setUsername("target_user");

        mockMvc.perform(post("/system/auth/revoke")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(0));
    }

    @Test
    void revoke_emptyUsername_shouldReturn400() throws Exception {
        TokenRevokeRequest req = new TokenRevokeRequest();
        req.setUsername("");    // @NotBlank 触发

        mockMvc.perform(post("/system/auth/revoke")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isBadRequest());
    }
}
