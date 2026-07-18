package com.xingtong.mesai.module.messql.config;

import com.zaxxer.hikari.HikariDataSource;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnExpression;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;

import javax.sql.DataSource;

/**
 * MES 系统只读数据源配置（真实 MES 库，Oracle）
 *
 * <p>仅在 spring.mes.datasource.url 非空时激活，用于 MES 取数接口执行 AI 生成的 SELECT。
 * 连接信息通过环境变量注入，禁止硬编码（CLAUDE.md §4.1）。
 *
 * <p>安全约束（CLAUDE.md §4.3 生产环境保护）：
 * <ul>
 *   <li>Hikari read-only=true：驱动层声明只读，配合只读账号（如 mes_readonly）双重保障；</li>
 *   <li>未配置 MES_DB_URL 时不创建 Bean，取数接口自动降级为“只生成不执行”；</li>
 *   <li>连接池规模受限（最大 5），避免对生产 MES 库造成压力。</li>
 * </ul>
 *
 * <p>治理提示：Oracle 驱动 ojdbc8 的引入、真实只读账号的接入，均属“新中间件首次接入 /
 * 安全配置变更”，需技术负责人与 IT 审核专员授权后方可在环境中配置 MES_DB_URL 开启执行。
 *
 * @author AI（芯智云匠）
 * @date 2026-07-18
 * @module MES取数
 * @related REQ-MES-AI-20260716-001（NL → Oracle 只读 SELECT 生成与执行）
 */
@Slf4j
@Configuration
public class MesReadOnlyDataSourceConfig {

    @Value("${spring.mes.datasource.url:}")
    private String url;

    @Value("${spring.mes.datasource.username:}")
    private String username;

    @Value("${spring.mes.datasource.password:}")
    private String password;

    @Value("${spring.mes.datasource.driver-class-name:oracle.jdbc.OracleDriver}")
    private String driverClassName;

    /**
     * MES 只读数据源 Bean
     *
     * <p>当 MES_DB_URL 已配置且非空时创建只读连接池；未配置时不创建
     * （取数接口将返回“未配置只读数据源、仅生成 SQL 未执行”提示）。
     */
    @Bean("mesDataSource")
    @ConditionalOnExpression("!'${spring.mes.datasource.url:}'.isEmpty()")
    public DataSource mesDataSource() {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl(url);
        ds.setUsername(username);
        ds.setPassword(password);
        ds.setDriverClassName(driverClassName);
        ds.setPoolName("HikariPool-MesDB-ReadOnly");
        ds.setMaximumPoolSize(5);
        ds.setMinimumIdle(1);
        ds.setConnectionTimeout(10_000);
        // 只读声明：驱动/连接层拒绝任何写操作，是应用层 SQL 校验之外的第二道防线
        ds.setReadOnly(true);
        log.info("MES 只读数据源已初始化（read-only）：{}", maskUrl(url));
        return ds;
    }

    /**
     * MES 只读 JdbcTemplate Bean（依赖 mesDataSource）
     */
    @Bean("mesJdbcTemplate")
    @ConditionalOnExpression("!'${spring.mes.datasource.url:}'.isEmpty()")
    public JdbcTemplate mesJdbcTemplate() {
        return new JdbcTemplate(mesDataSource());
    }

    /**
     * 对 JDBC URL 中的敏感部分进行遮蔽，安全地输出到日志
     */
    private String maskUrl(String jdbcUrl) {
        if (jdbcUrl == null) {
            return "[null]";
        }
        int atIdx = jdbcUrl.indexOf('@');
        if (atIdx > 0) {
            // Oracle thin URL 形如 jdbc:oracle:thin:user/pwd@host:port/service，遮蔽 @ 之前的账密
            return jdbcUrl.substring(0, jdbcUrl.indexOf("thin:") + 5) + "[MASKED]" + jdbcUrl.substring(atIdx);
        }
        return jdbcUrl.replaceAll("password=[^&;]+", "password=***");
    }
}
