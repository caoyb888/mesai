package com.xingtong.mesai.config;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.context.annotation.Configuration;

/**
 * MyBatis Mapper 扫描配置
 *
 * <p>将 @MapperScan 从启动类提取到独立配置类，便于 @WebMvcTest 等测试切片按需排除，
 * 避免测试上下文因缺少 sqlSessionFactory 而加载失败。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 基础配置
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-8 测试基础设施）
 */
@Configuration
@MapperScan("com.xingtong.mesai.module.*.mapper")
public class MyBatisMapperScanConfig {
}
