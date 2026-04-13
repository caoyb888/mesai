package com.xingtong.mesai.module.system.dto;

import lombok.Data;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;

/**
 * 创建用户请求 DTO
 *
 * <p>对应 POST /system/users 请求体（需 system:admin 权限）。
 * <p>密码服务端 BCrypt 加密后存入数据库，明文仅在服务端存活极短时间。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-6）
 */
@Data
public class CreateUserRequest {

    /** 登录账号（唯一，英文/数字/下划线，3-64位） */
    @NotBlank(message = "用户名不能为空")
    @Size(min = 3, max = 64, message = "用户名长度须为3-64个字符")
    @Pattern(regexp = "^[a-zA-Z0-9_]+$", message = "用户名只允许英文字母、数字和下划线")
    private String username;

    /** 真实姓名（1-32字符） */
    @NotBlank(message = "真实姓名不能为空")
    @Size(max = 32, message = "真实姓名不能超过32个字符")
    private String realName;

    /**
     * 初始密码（明文，服务端 BCrypt 加密存储后立即丢弃）
     * 强度要求：8-128位，包含大写字母、小写字母、数字
     */
    @NotBlank(message = "密码不能为空")
    @Size(min = 8, max = 128, message = "密码长度须为8-128个字符")
    private String password;

    /**
     * 角色代码，必须为有效枚举值。
     * 可选值：BUSINESS_USER / IT_REVIEWER / IT_MANAGER / TECH_LEAD / AI_AGENT / MANAGER
     */
    @NotBlank(message = "角色代码不能为空")
    private String role;

    /** 所属部门（可选，最长64字符） */
    @Size(max = 64, message = "部门名称不能超过64个字符")
    private String dept;

    /** 邮箱（可选，须为有效格式） */
    @Email(message = "邮箱格式不正确")
    @Size(max = 128, message = "邮箱长度不能超过128个字符")
    private String email;

    /** 账号是否启用：1-启用，0-禁用（默认启用） */
    @NotNull(message = "isActive 不能为空")
    private Integer isActive;
}
