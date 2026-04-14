package com.xingtong.mesai.config;

import com.zaxxer.hikari.HikariDataSource;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

import javax.sql.DataSource;

/**
 * 主数据源显式配置（MySQL 8.x MES AI 平台库）
 *
 * <p>由于项目中存在 ITSM 次级数据源（ItsmDataSourceConfig），Spring Boot 的
 * DataSourceAutoConfiguration 会因检测到已有 DataSource Bean 而退让，不再自动
 * 创建主数据源。本类显式声明 @Primary 主数据源，确保 MyBatis/Spring Data 以
 * MySQL 主库为默认数据源。
 *
 * <p>连接信息通过环境变量注入，禁止硬编码（CLAUDE.md 4.1节）。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 基础配置
 * @related REQ-MES-AI-20260412-005（S2.5 演示MVP）
 */
@Slf4j
@Configuration
public class PrimaryDataSourceConfig {

    @Value("${spring.datasource.url}")
    private String url;

    @Value("${spring.datasource.username}")
    private String username;

    @Value("${spring.datasource.password}")
    private String password;

    @Value("${spring.datasource.driver-class-name:com.mysql.cj.jdbc.Driver}")
    private String driverClassName;

    @Value("${spring.datasource.hikari.pool-name:HikariPool-MesAI}")
    private String poolName;

    @Value("${spring.datasource.hikari.maximum-pool-size:10}")
    private int maxPoolSize;

    @Value("${spring.datasource.hikari.minimum-idle:2}")
    private int minIdle;

    @Value("${spring.datasource.hikari.connection-timeout:30000}")
    private long connectionTimeout;

    @Value("${spring.datasource.hikari.idle-timeout:600000}")
    private long idleTimeout;

    @Value("${spring.datasource.hikari.max-lifetime:1800000}")
    private long maxLifetime;

    /**
     * MES AI 平台主数据源（MySQL 8.x）
     *
     * <p>标记 @Primary，确保 MyBatis Plus 和 JdbcTemplate 默认注入此数据源，
     * 而非 ITSM 演示数据源。
     */
    @Primary
    @Bean("dataSource")
    public DataSource dataSource() {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl(url);
        ds.setUsername(username);
        ds.setPassword(password);
        ds.setDriverClassName(driverClassName);
        ds.setPoolName(poolName);
        ds.setMaximumPoolSize(maxPoolSize);
        ds.setMinimumIdle(minIdle);
        ds.setConnectionTimeout(connectionTimeout);
        ds.setIdleTimeout(idleTimeout);
        ds.setMaxLifetime(maxLifetime);
        ds.setConnectionTestQuery("SELECT 1");
        log.info("主数据源（MySQL）已初始化，连接池：{}", poolName);
        return ds;
    }
}
