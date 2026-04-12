package com.xingtong.mesai;

import lombok.extern.slf4j.Slf4j;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.transaction.annotation.EnableTransactionManagement;

/**
 * 芯智云匠 MES AI 智能体平台启动类
 *
 * <p>山东芯通 MES 岗位 AI 智能体资产化项目后端主入口。
 * <p>启动前置检查：
 * <ul>
 *   <li>环境变量 DB_URL / DB_USERNAME / DB_PASSWORD 必须注入</li>
 *   <li>环境变量 REDIS_HOST / REDIS_PORT 必须注入</li>
 *   <li>环境变量 JWT_SECRET 必须注入</li>
 * </ul>
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 * @module 系统启动
 * @related REQ-MES-AI-20260412-005（S1-5 后端项目骨架）
 */
@Slf4j
@SpringBootApplication
@EnableTransactionManagement
@EnableScheduling
@MapperScan("com.xingtong.mesai.module.*.mapper")
public class MesAiApplication {

    public static void main(String[] args) {
        SpringApplication.run(MesAiApplication.class, args);
        log.info("========================================================");
        log.info("  芯智云匠 MES AI 智能体平台 启动成功");
        log.info("  版本：1.0.0-SNAPSHOT  技术栈：Spring Boot 2.7 + MyBatis Plus");
        log.info("========================================================");
    }
}
