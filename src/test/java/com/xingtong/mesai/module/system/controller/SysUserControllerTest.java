package com.xingtong.mesai.module.system.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.xingtong.mesai.common.result.PageVO;
import com.xingtong.mesai.common.result.ResultCode;
import com.xingtong.mesai.module.system.dto.CreateUserRequest;
import com.xingtong.mesai.module.system.mapper.SysUserMapper;
import com.xingtong.mesai.module.system.security.JwtProperties;
import com.xingtong.mesai.module.system.security.JwtUtil;
import com.xingtong.mesai.module.system.service.SysUserService;
import com.xingtong.mesai.module.system.vo.UserVO;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDateTime;
import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.isNull;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * SysUserController MockMvc 测试
 *
 * <p>覆盖用户列表分页查询（GET /system/users）和用户创建（POST /system/users）两个接口。
 * <p>禁用 Security 过滤器，专注于请求绑定、参数校验和响应格式验证。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-8）
 */
@WebMvcTest(
    controllers = SysUserController.class,
    excludeAutoConfiguration = com.xingtong.mesai.config.MyBatisMapperScanConfig.class
)
@AutoConfigureMockMvc(addFilters = false)
class SysUserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private SysUserService sysUserService;

    // SecurityConfig 的构造依赖
    @MockBean
    private JwtUtil jwtUtil;
    @MockBean
    private JwtProperties jwtProperties;
    @MockBean
    private SysUserMapper sysUserMapper;
    @MockBean
    private StringRedisTemplate redisTemplate;

    private PageVO<UserVO> mockPage;

    @BeforeEach
    void setUp() {
        UserVO vo = new UserVO();
        vo.setUserId(1L);
        vo.setUsername("alice");
        vo.setRealName("爱丽丝");
        vo.setRole("IT_MANAGER");
        vo.setIsActive(1);
        vo.setCreatedAt(LocalDateTime.now());

        PageVO.PaginationVO pagination = new PageVO.PaginationVO(1, 20, 1L, 1);
        mockPage = new PageVO<>(List.of(vo), pagination);
    }

    // ── GET /system/users ─────────────────────────────────────────

    @Test
    void listUsers_defaultParams_shouldReturn200WithList() throws Exception {
        when(sysUserService.listUsers(1, 20, null, null, null, null))
                .thenReturn(mockPage);

        mockMvc.perform(get("/system/users"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(0))
                .andExpect(jsonPath("$.data.list[0].username").value("alice"))
                .andExpect(jsonPath("$.data.pagination.total").value(1));
    }

    @Test
    void listUsers_withFilters_shouldPassFiltersToService() throws Exception {
        when(sysUserService.listUsers(2, 10, "IT_MANAGER", "IT部门", 1, "alice"))
                .thenReturn(mockPage);

        mockMvc.perform(get("/system/users")
                        .param("page", "2")
                        .param("pageSize", "10")
                        .param("role", "IT_MANAGER")
                        .param("dept", "IT部门")
                        .param("isActive", "1")
                        .param("keyword", "alice"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(0));
    }

    @Test
    void listUsers_passwordNotInResponse_shouldNotContainPasswordField() throws Exception {
        when(sysUserService.listUsers(anyInt(), anyInt(), isNull(), isNull(), isNull(), isNull()))
                .thenReturn(mockPage);

        String responseBody = mockMvc.perform(get("/system/users"))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();

        // 确认响应中不含 password 字段
        assert !responseBody.contains("\"password\"");
    }

    // ── POST /system/users ────────────────────────────────────────

    @Test
    void createUser_validRequest_shouldReturn200WithUserVO() throws Exception {
        UserVO created = new UserVO();
        created.setUserId(2L);
        created.setUsername("bob");
        created.setRealName("鲍勃");
        created.setRole("BUSINESS_USER");
        created.setIsActive(1);

        when(sysUserService.createUser(any())).thenReturn(created);

        CreateUserRequest req = buildValidRequest("bob", "BUSINESS_USER");

        mockMvc.perform(post("/system/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(0))
                .andExpect(jsonPath("$.data.username").value("bob"))
                .andExpect(jsonPath("$.data.role").value("BUSINESS_USER"));
    }

    @Test
    void createUser_emptyUsername_shouldReturn400() throws Exception {
        CreateUserRequest req = buildValidRequest("", "BUSINESS_USER");

        mockMvc.perform(post("/system/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value(ResultCode.PARAM_INVALID.getCode()));
    }

    @Test
    void createUser_shortPassword_shouldReturn400() throws Exception {
        CreateUserRequest req = buildValidRequest("carol", "IT_REVIEWER");
        req.setPassword("short");    // 少于 8 位

        mockMvc.perform(post("/system/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isBadRequest());
    }

    @Test
    void createUser_invalidEmail_shouldReturn400() throws Exception {
        CreateUserRequest req = buildValidRequest("dave", "MANAGER");
        req.setEmail("not-an-email");

        mockMvc.perform(post("/system/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isBadRequest());
    }

    @Test
    void createUser_missingIsActive_shouldReturn400() throws Exception {
        CreateUserRequest req = buildValidRequest("eve", "MANAGER");
        req.setIsActive(null);   // @NotNull 触发

        mockMvc.perform(post("/system/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isBadRequest());
    }

    // ── 工具方法 ──────────────────────────────────────────────────

    private CreateUserRequest buildValidRequest(String username, String role) {
        CreateUserRequest req = new CreateUserRequest();
        req.setUsername(username.isEmpty() ? username : username);
        req.setRealName("测试用户");
        req.setPassword("ValidPass@123");
        req.setRole(role);
        req.setDept("IT部门");
        req.setEmail("test@xingtong.com");
        req.setIsActive(1);
        return req;
    }
}
