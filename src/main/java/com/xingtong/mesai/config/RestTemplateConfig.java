package com.xingtong.mesai.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;

/**
 * RestTemplate 配置
 *
 * <p>提供全局 RestTemplate Bean，用于 Spring Boot 服务间 HTTP 调用（如调用 AI 网关）。
 * 超时时间通过配置注入，不硬编码。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 公共配置
 * @related REQ-MES-AI-20260412-005（S2.5 演示MVP）
 */
@Configuration
public class RestTemplateConfig {

    @Value("${ai.gateway.timeout-seconds:120}")
    private int timeoutSeconds;

    /**
     * 全局 RestTemplate，超时时间与 AI 网关超时配置保持一致
     */
    @Bean
    public RestTemplate restTemplate(RestTemplateBuilder builder) {
        return builder
                .setConnectTimeout(Duration.ofSeconds(10))
                .setReadTimeout(Duration.ofSeconds(timeoutSeconds))
                .build();
    }
}
