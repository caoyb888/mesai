package com.xingtong.mesai.module.system.dto;

import lombok.Data;

import javax.validation.constraints.NotBlank;

/**
 * Token 刷新请求 DTO
 *
 * <p>对应 POST /system/auth/refresh 请求体。
 * <p>携带有效的 refreshToken 换取新的 accessToken + refreshToken（令牌轮换）。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-2）
 */
@Data
public class TokenRefreshRequest {

    /** 刷新令牌 */
    @NotBlank(message = "refreshToken 不能为空")
    private String refreshToken;
}
