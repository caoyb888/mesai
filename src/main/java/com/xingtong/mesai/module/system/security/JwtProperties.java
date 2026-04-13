package com.xingtong.mesai.module.system.security;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

/**
 * JWT 配置属性绑定
 *
 * <p>对应 application-*.yml 中 security.jwt.* 配置节。
 * <p>secret 必须通过环境变量 JWT_SECRET 注入，禁止在配置文件中硬编码真实密钥。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-1）
 */
@Data
@Component
@ConfigurationProperties(prefix = "security.jwt")
public class JwtProperties {

    /**
     * HMAC-SHA256 签名密钥（Base64 编码）。
     * 生产环境通过 JWT_SECRET 环境变量注入，最小长度 32 字节。
     */
    private String secret;

    /**
     * 访问令牌有效期（秒），默认 28800（8 小时）。
     */
    private long accessTokenExpireSeconds = 28800L;

    /**
     * 刷新令牌有效期（秒），默认 604800（7 天）。
     */
    private long refreshTokenExpireSeconds = 604800L;
}
