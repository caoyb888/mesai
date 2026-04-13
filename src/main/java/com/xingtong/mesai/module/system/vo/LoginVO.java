package com.xingtong.mesai.module.system.vo;

import lombok.Builder;
import lombok.Data;

/**
 * 登录成功响应 VO
 *
 * <p>包含 accessToken、refreshToken 及用户基本信息，
 * 客户端后续请求在 Authorization: Bearer {accessToken} 头携带。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-1）
 */
@Data
@Builder
public class LoginVO {

    /** 访问令牌（有效期 8 小时） */
    private String accessToken;

    /** 刷新令牌（有效期 7 天，用于无感续期） */
    private String refreshToken;

    /** Token 类型（固定值 Bearer） */
    private String tokenType;

    /** 访问令牌剩余有效秒数 */
    private Long expiresIn;

    /** 当前登录用户名 */
    private String username;

    /** 当前登录用户真实姓名 */
    private String realName;

    /** 当前角色代码 */
    private String role;

    /** 当前角色中文名 */
    private String roleDisplayName;
}
