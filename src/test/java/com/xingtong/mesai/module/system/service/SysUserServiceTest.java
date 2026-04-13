package com.xingtong.mesai.module.system.service;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.common.result.PageVO;
import com.xingtong.mesai.common.result.ResultCode;
import com.xingtong.mesai.module.system.dto.CreateUserRequest;
import com.xingtong.mesai.module.system.entity.SysUser;
import com.xingtong.mesai.module.system.mapper.SysUserMapper;
import com.xingtong.mesai.module.system.vo.UserVO;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.time.LocalDateTime;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

/**
 * SysUserService 单元测试
 *
 * <p>覆盖分页查询和用户创建两个核心场景，含正常路径与边界条件。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-8）
 */
@ExtendWith(MockitoExtension.class)
class SysUserServiceTest {

    @Mock
    private SysUserMapper sysUserMapper;

    @Spy
    private PasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    @InjectMocks
    private SysUserService sysUserService;

    private UserVO sampleVO;

    @BeforeEach
    void setUp() {
        sampleVO = new UserVO();
        sampleVO.setUserId(1L);
        sampleVO.setUsername("alice");
        sampleVO.setRealName("爱丽丝");
        sampleVO.setRole("IT_MANAGER");
        sampleVO.setIsActive(1);
        sampleVO.setCreatedAt(LocalDateTime.now());
    }

    // ── 分页查询 ──────────────────────────────────────────────────

    @Test
    void listUsers_noFilter_shouldReturnPageVO() {
        Page<UserVO> mockPage = new Page<>(1, 20);
        mockPage.setRecords(List.of(sampleVO));
        mockPage.setTotal(1);

        when(sysUserMapper.selectUserPage(any(Page.class), any(), any(), any(), any()))
                .thenReturn(mockPage);

        PageVO<UserVO> result = sysUserService.listUsers(1, 20, null, null, null, null);

        assertThat(result.getList()).hasSize(1);
        assertThat(result.getPagination().getTotal()).isEqualTo(1L);
        assertThat(result.getPagination().getPage()).isEqualTo(1);
        assertThat(result.getPagination().getPageSize()).isEqualTo(20);
    }

    @Test
    void listUsers_pageSizeExceedsMax_shouldClampTo100() {
        Page<UserVO> mockPage = new Page<>(1, 100);
        mockPage.setRecords(List.of());
        mockPage.setTotal(0);

        when(sysUserMapper.selectUserPage(any(Page.class), any(), any(), any(), any()))
                .thenReturn(mockPage);

        // 传入超大 pageSize = 500，应被限制为 100
        PageVO<UserVO> result = sysUserService.listUsers(1, 500, null, null, null, null);

        assertThat(result.getPagination().getPageSize()).isEqualTo(100);
    }

    @Test
    void listUsers_emptyResult_shouldReturnEmptyList() {
        Page<UserVO> mockPage = new Page<>(1, 20);
        mockPage.setRecords(List.of());
        mockPage.setTotal(0);

        when(sysUserMapper.selectUserPage(any(Page.class), any(), any(), any(), any()))
                .thenReturn(mockPage);

        PageVO<UserVO> result = sysUserService.listUsers(1, 20, "MANAGER", null, null, null);

        assertThat(result.getList()).isEmpty();
        assertThat(result.getPagination().getTotal()).isEqualTo(0L);
    }

    // ── 创建用户 ──────────────────────────────────────────────────

    @Test
    void createUser_validRequest_shouldReturnUserVOWithoutPassword() {
        // 模拟用户名不重复
        when(sysUserMapper.selectCount(any(LambdaQueryWrapper.class))).thenReturn(0L);
        // 模拟 insert 成功（MyBatis Plus insert 返回 1）
        when(sysUserMapper.insert(any(SysUser.class))).thenReturn(1);

        CreateUserRequest req = buildRequest("bob", "TECH_LEAD");
        UserVO vo = sysUserService.createUser(req);

        assertThat(vo.getUsername()).isEqualTo("bob");
        assertThat(vo.getRole()).isEqualTo("TECH_LEAD");
        assertThat(vo.getRealName()).isEqualTo("测试用户");
        // 确认 password 字段不在 VO 中（UserVO 本身不含此字段）
        verify(passwordEncoder).encode("Pass@12345");
    }

    @Test
    void createUser_duplicateUsername_shouldThrowDuplicateKey() {
        when(sysUserMapper.selectCount(any(LambdaQueryWrapper.class))).thenReturn(1L);

        CreateUserRequest req = buildRequest("existing", "IT_REVIEWER");

        assertThatThrownBy(() -> sysUserService.createUser(req))
                .isInstanceOf(BizException.class)
                .satisfies(ex -> assertThat(((BizException) ex).getResultCode())
                        .isEqualTo(ResultCode.DUPLICATE_KEY));
    }

    @Test
    void createUser_invalidRole_shouldThrowParamInvalid() {
        CreateUserRequest req = buildRequest("newuser", "INVALID_ROLE");

        assertThatThrownBy(() -> sysUserService.createUser(req))
                .isInstanceOf(BizException.class)
                .satisfies(ex -> assertThat(((BizException) ex).getResultCode())
                        .isEqualTo(ResultCode.PARAM_INVALID));
    }

    @Test
    void createUser_allValidRoles_shouldBeAccepted() {
        // 验证 6 种合法角色均可创建用户
        String[] validRoles = {
            "BUSINESS_USER", "IT_REVIEWER", "IT_MANAGER", "TECH_LEAD", "AI_AGENT", "MANAGER"
        };
        when(sysUserMapper.selectCount(any(LambdaQueryWrapper.class))).thenReturn(0L);
        when(sysUserMapper.insert(any(SysUser.class))).thenReturn(1);

        for (String role : validRoles) {
            CreateUserRequest req = buildRequest("user_" + role.toLowerCase(), role);
            UserVO vo = sysUserService.createUser(req);
            assertThat(vo.getRole()).isEqualTo(role);
        }
    }

    // ── 工具方法 ──────────────────────────────────────────────────

    private CreateUserRequest buildRequest(String username, String role) {
        CreateUserRequest req = new CreateUserRequest();
        req.setUsername(username);
        req.setRealName("测试用户");
        req.setPassword("Pass@12345");
        req.setRole(role);
        req.setDept("IT部门");
        req.setEmail("test@xingtong.com");
        req.setIsActive(1);
        return req;
    }
}
