package com.xingtong.mesai.module.system.dto;

import lombok.Data;

import javax.validation.constraints.NotBlank;

/**
 * Token 强制吊销请求 DTO
 *
 * <p>对应 POST /system/auth/revoke 请求体（需 system:admin 权限）。
 * <p>管理员强制使指定用户的所有 Token 失效（踢出登录）。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-3）
 */
@Data
public class TokenRevokeRequest {

    /** 被吊销的目标用户名 */
    @NotBlank(message = "username 不能为空")
    private String username;
}
