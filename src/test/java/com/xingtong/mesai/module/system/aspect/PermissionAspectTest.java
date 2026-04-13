package com.xingtong.mesai.module.system.aspect;

import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.common.result.ResultCode;
import com.xingtong.mesai.module.system.annotation.RequirePermission;
import com.xingtong.mesai.module.system.entity.SysUser;
import com.xingtong.mesai.module.system.security.LoginUserDetails;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

/**
 * PermissionAspect 单元测试
 *
 * <p>直接调用切面的 checkPermission 方法，模拟不同 SecurityContext 状态，
 * 验证权限校验逻辑的正确性（有权 → 通过，无权 → 抛出 PERMISSION_DENIED）。
 * <p>纯单元测试，不加载 Spring Context。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-8）
 */
class PermissionAspectTest {

    private final PermissionAspect aspect = new PermissionAspect();

    @BeforeEach
    void clearContext() {
        SecurityContextHolder.clearContext();
    }

    @AfterEach
    void cleanUp() {
        SecurityContextHolder.clearContext();
    }

    // ── 有权限：TECH_LEAD + system:admin ─────────────────────────

    @Test
    void checkPermission_techLeadWithSystemAdmin_shouldPass() {
        setAuthenticatedUser("admin", "TECH_LEAD");
        RequirePermission annotation = mockAnnotation("system:admin");

        // 不应抛出任何异常
        aspect.checkPermission(annotation);
    }

    // ── 有权限：IT_MANAGER + system:admin ────────────────────────

    @Test
    void checkPermission_itManagerWithSystemAdmin_shouldPass() {
        setAuthenticatedUser("manager", "IT_MANAGER");
        RequirePermission annotation = mockAnnotation("system:admin");

        aspect.checkPermission(annotation);
    }

    // ── 无权限：BUSINESS_USER 尝试 system:admin ──────────────────

    @Test
    void checkPermission_businessUserLacksSystemAdmin_shouldThrowPermissionDenied() {
        setAuthenticatedUser("alice", "BUSINESS_USER");
        RequirePermission annotation = mockAnnotation("system:admin");

        assertThatThrownBy(() -> aspect.checkPermission(annotation))
                .isInstanceOf(BizException.class)
                .satisfies(ex -> assertThat(((BizException) ex).getResultCode())
                        .isEqualTo(ResultCode.PERMISSION_DENIED));
    }

    // ── 无权限：IT_REVIEWER 尝试 deploy:approve ──────────────────

    @Test
    void checkPermission_itReviewerLacksDeployApprove_shouldThrowPermissionDenied() {
        setAuthenticatedUser("reviewer", "IT_REVIEWER");
        RequirePermission annotation = mockAnnotation("deploy:approve");

        assertThatThrownBy(() -> aspect.checkPermission(annotation))
                .isInstanceOf(BizException.class)
                .satisfies(ex -> assertThat(((BizException) ex).getResultCode())
                        .isEqualTo(ResultCode.PERMISSION_DENIED));
    }

    // ── 有权限：IT_REVIEWER + knowledge:upload ───────────────────

    @Test
    void checkPermission_itReviewerWithKnowledgeUpload_shouldPass() {
        setAuthenticatedUser("reviewer", "IT_REVIEWER");
        RequirePermission annotation = mockAnnotation("knowledge:upload");

        aspect.checkPermission(annotation);
    }

    // ── 未认证：SecurityContext 为空 ─────────────────────────────

    @Test
    void checkPermission_noAuthentication_shouldThrowPermissionDenied() {
        // SecurityContext 已被 clearContext 清空
        RequirePermission annotation = mockAnnotation("task:read");

        assertThatThrownBy(() -> aspect.checkPermission(annotation))
                .isInstanceOf(BizException.class)
                .satisfies(ex -> assertThat(((BizException) ex).getResultCode())
                        .isEqualTo(ResultCode.PERMISSION_DENIED));
    }

    // ── 无效角色代码 ──────────────────────────────────────────────

    @Test
    void checkPermission_invalidRoleCode_shouldThrowPermissionDenied() {
        setAuthenticatedUser("weird", "INVALID_ROLE");
        RequirePermission annotation = mockAnnotation("task:read");

        assertThatThrownBy(() -> aspect.checkPermission(annotation))
                .isInstanceOf(BizException.class)
                .satisfies(ex -> assertThat(((BizException) ex).getResultCode())
                        .isEqualTo(ResultCode.PERMISSION_DENIED));
    }

    // ── MANAGER 只读权限正向验证 ──────────────────────────────────

    @Test
    void checkPermission_managerWithCostRead_shouldPass() {
        setAuthenticatedUser("boss", "MANAGER");
        aspect.checkPermission(mockAnnotation("cost:read"));
        aspect.checkPermission(mockAnnotation("task:read"));
        aspect.checkPermission(mockAnnotation("monitor:read"));
    }

    @Test
    void checkPermission_managerTriesTaskWrite_shouldThrowPermissionDenied() {
        setAuthenticatedUser("boss", "MANAGER");
        assertThatThrownBy(() -> aspect.checkPermission(mockAnnotation("task:write")))
                .isInstanceOf(BizException.class)
                .satisfies(ex -> assertThat(((BizException) ex).getResultCode())
                        .isEqualTo(ResultCode.PERMISSION_DENIED));
    }

    // ── AI_AGENT 专属权限 ────────────────────────────────────────

    @Test
    void checkPermission_aiAgentWithExecLogWrite_shouldPass() {
        setAuthenticatedUser("ai-agent-01", "AI_AGENT");
        aspect.checkPermission(mockAnnotation("exec_log:write"));
        aspect.checkPermission(mockAnnotation("artifact:write"));
    }

    // ── 工具方法 ──────────────────────────────────────────────────

    /** 构建并设置认证 SecurityContext */
    private void setAuthenticatedUser(String username, String roleCode) {
        SysUser user = new SysUser();
        user.setUsername(username);
        user.setRole(roleCode);
        user.setIsActive(1);
        user.setPassword("$2a$10$placeholder");

        LoginUserDetails userDetails = new LoginUserDetails(user);
        UsernamePasswordAuthenticationToken auth =
                new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
        SecurityContextHolder.getContext().setAuthentication(auth);
    }

    /** 模拟 @RequirePermission 注解实例 */
    private RequirePermission mockAnnotation(String permission) {
        RequirePermission annotation = mock(RequirePermission.class);
        when(annotation.value()).thenReturn(permission);
        return annotation;
    }
}
