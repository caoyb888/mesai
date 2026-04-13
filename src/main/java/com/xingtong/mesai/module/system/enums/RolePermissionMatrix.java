package com.xingtong.mesai.module.system.enums;

import java.util.Arrays;
import java.util.Collections;
import java.util.EnumMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * 角色-权限矩阵
 *
 * <p>根据 AI-MES-API-2026-001 第 2.4 节权限矩阵静态定义。
 * <p>调用 {@link #getPermissions(UserRole)} 获取指定角色的权限集合。
 * <p>权限标识说明：
 * <ul>
 *   <li>{@code task:read}      - 查看任务（BUSINESS_USER 仅限自己，其他角色全量）</li>
 *   <li>{@code task:write}     - 提交任务</li>
 *   <li>{@code task:review}    - 评审任务</li>
 *   <li>{@code task:accept}    - 验收任务</li>
 *   <li>{@code task:export}    - 任务数据导出</li>
 *   <li>{@code approval:write} - 执行授权</li>
 *   <li>{@code deploy:approve} - 部署审批</li>
 *   <li>{@code exec_log:write} - 写入执行日志</li>
 *   <li>{@code artifact:write} - 写入代码交付物</li>
 *   <li>{@code monitor:read}   - 查看监控数据</li>
 *   <li>{@code monitor:export} - 导出监控数据</li>
 *   <li>{@code knowledge:upload} - 上传知识库文档</li>
 *   <li>{@code assertion:manage} - 管理断言库</li>
 *   <li>{@code cost:read}      - 查看 Token 成本</li>
 *   <li>{@code cost:export}    - 导出 Token 成本报告</li>
 *   <li>{@code system:admin}   - 系统配置/用户管理</li>
 * </ul>
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-5 RBAC权限控制）
 */
public final class RolePermissionMatrix {

    private RolePermissionMatrix() { /* 工具类，禁止实例化 */ }

    /** 角色 → 权限集合的静态映射表 */
    private static final Map<UserRole, Set<String>> MATRIX;

    static {
        Map<UserRole, Set<String>> map = new EnumMap<>(UserRole.class);

        // 业务人员：提交、查看自己任务、参与验收
        map.put(UserRole.BUSINESS_USER, setOf(
                "task:read", "task:write", "task:accept"
        ));

        // IT 评审专员：评审需求、查看全部任务、执行授权、导出、监控、成本
        map.put(UserRole.IT_REVIEWER, setOf(
                "task:read", "task:review", "task:accept", "task:export",
                "approval:write",
                "monitor:read", "monitor:export",
                "knowledge:upload",
                "cost:read", "cost:export"
        ));

        // IT 负责人：IT_REVIEWER 全部权限 + 部署审批 + 系统管理
        map.put(UserRole.IT_MANAGER, setOf(
                "task:read", "task:review", "task:accept", "task:export",
                "approval:write",
                "deploy:approve",
                "monitor:read", "monitor:export",
                "knowledge:upload",
                "cost:read", "cost:export",
                "system:admin"
        ));

        // 技术负责人：全部权限
        map.put(UserRole.TECH_LEAD, setOf(
                "task:read", "task:write", "task:review", "task:accept", "task:export",
                "approval:write",
                "deploy:approve",
                "exec_log:write",
                "artifact:write",
                "monitor:read", "monitor:export",
                "knowledge:upload",
                "assertion:manage",
                "cost:read", "cost:export",
                "system:admin"
        ));

        // AI 智能体：写入执行日志、代码交付物，可读任务（服务账号）
        map.put(UserRole.AI_AGENT, setOf(
                "task:read",
                "exec_log:write",
                "artifact:write",
                "monitor:read"
        ));

        // 管理层（只读）：报告、成本统计、导出，无写权限
        map.put(UserRole.MANAGER, setOf(
                "task:read", "task:export",
                "monitor:read", "monitor:export",
                "cost:read", "cost:export"
        ));

        MATRIX = Collections.unmodifiableMap(map);
    }

    /**
     * 获取指定角色的权限集合（不可修改）。
     *
     * @param role 角色枚举
     * @return 权限标识集合
     */
    public static Set<String> getPermissions(UserRole role) {
        return MATRIX.getOrDefault(role, Collections.emptySet());
    }

    /**
     * 判断指定角色是否拥有某权限。
     *
     * @param role       角色枚举
     * @param permission 权限标识
     * @return true 表示拥有该权限
     */
    public static boolean hasPermission(UserRole role, String permission) {
        return getPermissions(role).contains(permission);
    }

    // ── 私有工具方法 ─────────────────────────────────────────────

    @SafeVarargs
    private static <T> Set<T> setOf(T... items) {
        return Collections.unmodifiableSet(new HashSet<>(Arrays.asList(items)));
    }
}
