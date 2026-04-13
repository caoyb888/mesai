package com.xingtong.mesai.module.system.annotation;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * 细粒度权限校验注解
 *
 * <p>标注在 Controller 方法上，声明调用该接口所需的权限标识。
 * <p>由 {@link com.xingtong.mesai.module.system.aspect.PermissionAspect} 在方法调用前拦截校验。
 * <p>权限标识与 {@link com.xingtong.mesai.module.system.enums.RolePermissionMatrix} 中定义的 key 对应。
 *
 * <p>使用示例：
 * <pre>
 *   {@code @RequirePermission("system:admin")}
 *   public ResultVO<?> createUser(...) { ... }
 * </pre>
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-5）
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface RequirePermission {

    /**
     * 所需权限标识（对应 RolePermissionMatrix 中的 key，如 "system:admin"）。
     */
    String value();
}
