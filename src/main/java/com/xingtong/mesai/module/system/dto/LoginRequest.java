package com.xingtong.mesai.module.system.dto;

import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;

/**
 * 登录请求 DTO
 *
 * <p>对应 POST /system/auth/login 请求体。
 * <p>密码在服务端与 BCrypt 存储值比对，不在本 DTO 中明文传输记录到日志。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-1）
 */
@Data
public class LoginRequest {

    /** 登录账号 */
    @NotBlank(message = "用户名不能为空")
    @Size(max = 64, message = "用户名长度不能超过64个字符")
    private String username;

    /**
     * 登录密码（明文，服务端 BCrypt 验证后立即丢弃）
     * 注意：禁止在日志中打印此字段
     */
    @NotBlank(message = "密码不能为空")
    @Size(max = 128, message = "密码长度不能超过128个字符")
    private String password;
}
