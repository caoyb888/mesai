package com.xingtong.mesai.module.demo.config;

import com.zaxxer.hikari.HikariDataSource;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnExpression;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;
import javax.sql.DataSource;

/**
 * ITSM 测试数据库次级数据源配置
 *
 * <p>仅在 itsm.datasource.url 非空时激活，用于演示接口的 SQL 执行功能。
 * 连接信息通过环境变量注入，禁止硬编码（CLAUDE.md 4.1节）。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 演示模块
 * @related REQ-MES-AI-20260412-005（S2.5 演示MVP）
 */
@Slf4j
@Configuration
public class ItsmDataSourceConfig {

    @Value("${itsm.datasource.url:}")
    private String url;

    @Value("${itsm.datasource.username:}")
    private String username;

    @Value("${itsm.datasource.password:}")
    private String password;

    @Value("${itsm.datasource.driver-class-name:org.postgresql.Driver}")
    private String driverClassName;

    /**
     * ITSM 测试数据源 Bean
     *
     * <p>当 ITSM_DB_URL 已配置且非空时创建真实连接池；
     * 未配置时不创建（演示接口将返回"未配置数据源"提示）。
     * 使用 ConditionalOnExpression 明确过滤空字符串，避免 ConditionalOnProperty
     * 将空值视为"属性存在"而错误激活 Bean 的歧义行为。
     */
    @Bean("itsmDataSource")
    @ConditionalOnExpression("!'${itsm.datasource.url:}'.isEmpty()")
    public DataSource itsmDataSource() {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl(url);
        ds.setUsername(username);
        ds.setPassword(password);
        ds.setDriverClassName(driverClassName);
        ds.setPoolName("HikariPool-ITSM-Demo");
        ds.setMaximumPoolSize(5);
        ds.setMinimumIdle(1);
        ds.setConnectionTimeout(10_000);
        log.info("ITSM 测试数据源已初始化：{}", maskUrl(url));
        return ds;
    }

    /**
     * ITSM JdbcTemplate Bean（依赖 itsmDataSource）
     */
    @Bean("itsmJdbcTemplate")
    @ConditionalOnExpression("!'${itsm.datasource.url:}'.isEmpty()")
    public JdbcTemplate itsmJdbcTemplate() {
        return new JdbcTemplate(itsmDataSource());
    }

    /**
     * 对 JDBC URL 中的密码部分进行遮蔽，安全地输出到日志
     */
    private String maskUrl(String jdbcUrl) {
        // 只保留协议和主机端口部分，隐藏库名以防误操作
        if (jdbcUrl == null) {
            return "[null]";
        }
        int atIdx = jdbcUrl.indexOf("@");
        if (atIdx > 0) {
            return jdbcUrl.substring(0, jdbcUrl.indexOf("//") + 2) + "[MASKED]" + jdbcUrl.substring(atIdx);
        }
        return jdbcUrl.replaceAll("password=[^&;]+", "password=***");
    }
}
