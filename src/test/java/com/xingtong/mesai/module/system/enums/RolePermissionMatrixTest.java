package com.xingtong.mesai.module.system.enums;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.EnumSource;

import java.util.Set;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

/**
 * RolePermissionMatrix + UserRole 单元测试
 *
 * <p>验证角色权限矩阵的完整性与边界条件，确保权限分配符合 API 规范 2.4 节。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-8）
 */
class RolePermissionMatrixTest {

    // ── UserRole 枚举测试 ─────────────────────────────────────────

    @Test
    void userRole_allValues_shouldHaveNonBlankCodeAndDisplayName() {
        for (UserRole role : UserRole.values()) {
            assertThat(role.getCode()).isNotBlank();
            assertThat(role.getDisplayName()).isNotBlank();
        }
    }

    @Test
    void userRole_fromCode_validCode_shouldReturnCorrectRole() {
        assertThat(UserRole.fromCode("IT_MANAGER")).isEqualTo(UserRole.IT_MANAGER);
        assertThat(UserRole.fromCode("TECH_LEAD")).isEqualTo(UserRole.TECH_LEAD);
        assertThat(UserRole.fromCode("AI_AGENT")).isEqualTo(UserRole.AI_AGENT);
    }

    @Test
    void userRole_fromCode_caseInsensitive_shouldWork() {
        // fromCode 使用 equalsIgnoreCase
        assertThat(UserRole.fromCode("it_manager")).isEqualTo(UserRole.IT_MANAGER);
        assertThat(UserRole.fromCode("Tech_Lead")).isEqualTo(UserRole.TECH_LEAD);
    }

    @Test
    void userRole_fromCode_unknownCode_shouldThrowIllegalArgument() {
        assertThatThrownBy(() -> UserRole.fromCode("UNKNOWN_ROLE"))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("未知角色代码");
    }

    // ── 权限矩阵测试：TECH_LEAD（全量权限）────────────────────────

    @Test
    void techLead_shouldHaveSystemAdminPermission() {
        assertThat(RolePermissionMatrix.hasPermission(UserRole.TECH_LEAD, "system:admin")).isTrue();
    }

    @Test
    void techLead_shouldHaveAllCriticalPermissions() {
        Set<String> perms = RolePermissionMatrix.getPermissions(UserRole.TECH_LEAD);
        assertThat(perms).contains(
                "task:read", "task:write", "task:review", "task:accept", "task:export",
                "approval:write", "deploy:approve", "exec_log:write", "artifact:write",
                "monitor:read", "monitor:export", "knowledge:upload",
                "assertion:manage", "cost:read", "cost:export", "system:admin"
        );
    }

    // ── 权限矩阵测试：BUSINESS_USER（最小权限）────────────────────

    @Test
    void businessUser_shouldNotHaveSystemAdmin() {
        assertThat(RolePermissionMatrix.hasPermission(UserRole.BUSINESS_USER, "system:admin"))
                .isFalse();
    }

    @Test
    void businessUser_shouldNotHaveDeployApprove() {
        assertThat(RolePermissionMatrix.hasPermission(UserRole.BUSINESS_USER, "deploy:approve"))
                .isFalse();
    }

    @Test
    void businessUser_shouldHaveTaskReadAndWrite() {
        assertThat(RolePermissionMatrix.hasPermission(UserRole.BUSINESS_USER, "task:read")).isTrue();
        assertThat(RolePermissionMatrix.hasPermission(UserRole.BUSINESS_USER, "task:write")).isTrue();
    }

    // ── 权限矩阵测试：IT_MANAGER vs IT_REVIEWER ───────────────────

    @Test
    void itManager_shouldHaveDeployApproveAndSystemAdmin_butItReviewerShouldNot() {
        assertThat(RolePermissionMatrix.hasPermission(UserRole.IT_MANAGER, "deploy:approve")).isTrue();
        assertThat(RolePermissionMatrix.hasPermission(UserRole.IT_MANAGER, "system:admin")).isTrue();

        assertThat(RolePermissionMatrix.hasPermission(UserRole.IT_REVIEWER, "deploy:approve")).isFalse();
        assertThat(RolePermissionMatrix.hasPermission(UserRole.IT_REVIEWER, "system:admin")).isFalse();
    }

    @Test
    void itManager_shouldContainAllItReviewerPermissions() {
        // IT_MANAGER 的权限是 IT_REVIEWER 的超集
        Set<String> reviewerPerms = RolePermissionMatrix.getPermissions(UserRole.IT_REVIEWER);
        Set<String> managerPerms  = RolePermissionMatrix.getPermissions(UserRole.IT_MANAGER);
        assertThat(managerPerms).containsAll(reviewerPerms);
    }

    // ── 权限矩阵测试：AI_AGENT（服务账号）───────────────────────

    @Test
    void aiAgent_shouldHaveExecLogWrite_butNotSystemAdmin() {
        assertThat(RolePermissionMatrix.hasPermission(UserRole.AI_AGENT, "exec_log:write")).isTrue();
        assertThat(RolePermissionMatrix.hasPermission(UserRole.AI_AGENT, "artifact:write")).isTrue();
        assertThat(RolePermissionMatrix.hasPermission(UserRole.AI_AGENT, "system:admin")).isFalse();
        assertThat(RolePermissionMatrix.hasPermission(UserRole.AI_AGENT, "task:write")).isFalse();
    }

    // ── 权限矩阵测试：MANAGER（只读）────────────────────────────

    @Test
    void manager_shouldOnlyHaveReadAndExportPermissions() {
        assertThat(RolePermissionMatrix.hasPermission(UserRole.MANAGER, "task:read")).isTrue();
        assertThat(RolePermissionMatrix.hasPermission(UserRole.MANAGER, "task:export")).isTrue();
        assertThat(RolePermissionMatrix.hasPermission(UserRole.MANAGER, "cost:read")).isTrue();

        // MANAGER 不应有任何写权限
        assertThat(RolePermissionMatrix.hasPermission(UserRole.MANAGER, "task:write")).isFalse();
        assertThat(RolePermissionMatrix.hasPermission(UserRole.MANAGER, "system:admin")).isFalse();
        assertThat(RolePermissionMatrix.hasPermission(UserRole.MANAGER, "approval:write")).isFalse();
    }

    // ── 权限集合不可修改性 ────────────────────────────────────────

    @ParameterizedTest
    @EnumSource(UserRole.class)
    void getPermissions_allRoles_shouldReturnNonNullSet(UserRole role) {
        Set<String> perms = RolePermissionMatrix.getPermissions(role);
        assertThat(perms).isNotNull();
        // 验证返回的集合是不可修改的
        assertThatThrownBy(() -> perms.add("fake:permission"))
                .isInstanceOf(UnsupportedOperationException.class);
    }

    // ── 未知权限标识 ──────────────────────────────────────────────

    @Test
    void hasPermission_unknownPermission_shouldReturnFalse() {
        // 任何角色都不应拥有不存在的权限标识
        assertThat(RolePermissionMatrix.hasPermission(UserRole.TECH_LEAD, "nonexistent:perm"))
                .isFalse();
    }
}
