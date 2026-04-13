package com.xingtong.mesai.module.system.controller;

import com.xingtong.mesai.module.system.mapper.SysUserMapper;
import com.xingtong.mesai.module.system.security.JwtProperties;
import com.xingtong.mesai.module.system.security.JwtUtil;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * HealthController 测试
 *
 * <p>验证 GET /system/health 的响应格式和关键字段。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-8）
 */
@WebMvcTest(
    controllers = HealthController.class,
    excludeAutoConfiguration = com.xingtong.mesai.config.MyBatisMapperScanConfig.class
)
@AutoConfigureMockMvc(addFilters = false)
class HealthControllerTest {

    @Autowired
    private MockMvc mockMvc;

    // SecurityConfig 的构造依赖
    @MockBean
    private JwtUtil jwtUtil;
    @MockBean
    private JwtProperties jwtProperties;
    @MockBean
    private SysUserMapper sysUserMapper;
    @MockBean
    private StringRedisTemplate redisTemplate;

    @Test
    void health_shouldReturn200WithStatusUp() throws Exception {
        mockMvc.perform(get("/system/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(0))
                .andExpect(jsonPath("$.data.status").value("UP"))
                .andExpect(jsonPath("$.data.app").value("mesai"))
                .andExpect(jsonPath("$.data.serverTime").isNotEmpty());
    }

    @Test
    void health_shouldNotRequireAuthentication() throws Exception {
        // 无任何 Token 也应返回 200（白名单接口）
        mockMvc.perform(get("/system/health"))
                .andExpect(status().isOk());
    }
}
