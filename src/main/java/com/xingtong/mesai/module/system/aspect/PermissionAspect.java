package com.xingtong.mesai.module.system.aspect;

import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.module.system.annotation.RequirePermission;
import com.xingtong.mesai.module.system.enums.RolePermissionMatrix;
import com.xingtong.mesai.module.system.enums.UserRole;
import com.xingtong.mesai.module.system.security.LoginUserDetails;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

/**
 * RBAC 权限校验切面
 *
 * <p>在标注了 {@link RequirePermission} 的方法执行前，
 * 从 SecurityContext 中取出当前用户的角色，查询权限矩阵，
 * 判断是否拥有所需权限；无权限则抛出 BizException（PERMISSION_DENIED）。
 *
 * <p>拦截点：所有标注了 {@code @RequirePermission} 的方法。
 * <p>依赖：JWT 过滤器已完成认证并填充 SecurityContext（即本切面只在认证通过后触发）。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-5）
 */
@Slf4j
@Aspect
@Component
public class PermissionAspect {

    /**
     * 前置通知：方法执行前校验权限。
     *
     * @param requirePermission 注解实例（由 Spring AOP 自动注入）
     */
    @Before("@annotation(requirePermission)")
    public void checkPermission(RequirePermission requirePermission) {
        String requiredPerm = requirePermission.value();

        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !authentication.isAuthenticated()) {
            log.warn("RBAC 校验：SecurityContext 中无有效认证信息，权限={}",  requiredPerm);
            throw BizException.permissionDenied("用户未认证");
        }

        Object principal = authentication.getPrincipal();
        if (!(principal instanceof LoginUserDetails)) {
            // 匿名用户或其他认证主体，直接拒绝
            throw BizException.permissionDenied(requiredPerm);
        }

        LoginUserDetails userDetails = (LoginUserDetails) principal;
        String roleCode = userDetails.getSysUser().getRole();

        UserRole role;
        try {
            role = UserRole.fromCode(roleCode);
        } catch (IllegalArgumentException e) {
            log.warn("RBAC 校验：未知角色代码 {}，拒绝访问", roleCode);
            throw BizException.permissionDenied(requiredPerm);
        }

        boolean hasPermission = RolePermissionMatrix.hasPermission(role, requiredPerm);
        if (!hasPermission) {
            log.warn("RBAC 权限不足：user={} role={} requiredPerm={}",
                    userDetails.getUsername(), roleCode, requiredPerm);
            throw BizException.permissionDenied(
                    "角色 [" + role.getDisplayName() + "] 无权执行此操作，所需权限：" + requiredPerm);
        }

        log.debug("RBAC 校验通过：user={} role={} perm={}", userDetails.getUsername(), roleCode, requiredPerm);
    }
}
