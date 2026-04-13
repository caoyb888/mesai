package com.xingtong.mesai.module.system.security;

import com.xingtong.mesai.module.system.entity.SysUser;
import com.xingtong.mesai.module.system.enums.RolePermissionMatrix;
import com.xingtong.mesai.module.system.enums.UserRole;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * Spring Security UserDetails 实现
 *
 * <p>封装 SysUser 实体，向 Spring Security 提供认证所需信息。
 * <p>GrantedAuthority 列表来自 RolePermissionMatrix，格式为 "PERMISSION_xxx"，
 *    同时包含角色本身 "ROLE_xxx"（兼容 hasRole 表达式）。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-5）
 */
public class LoginUserDetails implements UserDetails {

    /** 底层 SysUser 实体 */
    private final SysUser sysUser;

    /** 权限集合（构造时解析，避免重复计算） */
    private final Collection<? extends GrantedAuthority> authorities;

    public LoginUserDetails(SysUser sysUser) {
        this.sysUser = sysUser;
        this.authorities = buildAuthorities(sysUser.getRole());
    }

    // ── 公开访问底层实体 ─────────────────────────────────────────

    /** 获取底层 SysUser 实体（供服务层使用） */
    public SysUser getSysUser() {
        return sysUser;
    }

    // ── UserDetails 接口实现 ─────────────────────────────────────

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return authorities;
    }

    @Override
    public String getPassword() {
        return sysUser.getPassword();
    }

    @Override
    public String getUsername() {
        return sysUser.getUsername();
    }

    /**
     * 账号未过期（本项目不使用账号过期机制，由 is_active 控制启用/禁用）
     */
    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    /**
     * 账号未锁定（本项目不使用账号锁定机制）
     */
    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    /**
     * 凭证未过期（密码不设置有效期）
     */
    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    /**
     * 账号是否启用：映射 is_active = 1
     */
    @Override
    public boolean isEnabled() {
        return Integer.valueOf(1).equals(sysUser.getIsActive());
    }

    // ── 私有工具方法 ─────────────────────────────────────────────

    /**
     * 根据角色代码构建权限集合。
     * 包含：ROLE_{角色代码} + 所有细粒度权限标识（大写并加 PERMISSION_ 前缀）。
     */
    private static Set<GrantedAuthority> buildAuthorities(String roleCode) {
        Set<GrantedAuthority> result;
        try {
            UserRole role = UserRole.fromCode(roleCode);
            result = RolePermissionMatrix.getPermissions(role).stream()
                    .map(perm -> (GrantedAuthority) new SimpleGrantedAuthority(
                            "PERMISSION_" + perm.replace(":", "_").toUpperCase()))
                    .collect(Collectors.toSet());
            // 同时添加角色本身（供 @PreAuthorize("hasRole(...)") 使用）
            result.add(new SimpleGrantedAuthority("ROLE_" + role.getCode()));
        } catch (IllegalArgumentException e) {
            // 未知角色代码：返回空权限集，用户无法通过任何权限校验
            result = Set.of();
        }
        return result;
    }
}
