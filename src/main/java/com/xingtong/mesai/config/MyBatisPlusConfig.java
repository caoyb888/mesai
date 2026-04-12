package com.xingtong.mesai.config;

import com.baomidou.mybatisplus.annotation.DbType;
import com.baomidou.mybatisplus.core.handlers.MetaObjectHandler;
import com.baomidou.mybatisplus.extension.plugins.MybatisPlusInterceptor;
import com.baomidou.mybatisplus.extension.plugins.inner.PaginationInnerInterceptor;
import lombok.extern.slf4j.Slf4j;
import org.apache.ibatis.reflection.MetaObject;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.LocalDateTime;

/**
 * MyBatis Plus 全局配置
 *
 * <p>配置内容：
 * <ul>
 *   <li>分页插件（MySQL 方言）</li>
 *   <li>字段自动填充（created_at / updated_at）</li>
 * </ul>
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 * @module 全局配置
 * @related REQ-MES-AI-20260412-005（S1-5 后端项目骨架）
 */
@Slf4j
@Configuration
public class MyBatisPlusConfig {

    /**
     * MyBatis Plus 拦截器（含分页插件）
     *
     * <p>分页插件配置 MySQL 方言，与 AI 平台主数据源（MySQL 8.x）对应。
     * <p>注意：overflow=false，页码超出总页数时不返回第一页，而是返回空列表。
     */
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
        PaginationInnerInterceptor paginationInterceptor = new PaginationInnerInterceptor(DbType.MYSQL);
        // 超出总页数时返回空列表，不自动跳转到第一页
        paginationInterceptor.setOverflow(false);
        // 单页最大查询条数限制（防止恶意超大查询）
        paginationInterceptor.setMaxLimit(500L);
        interceptor.addInnerInterceptor(paginationInterceptor);
        return interceptor;
    }

    /**
     * 自动填充处理器
     *
     * <p>对 created_at 和 updated_at 字段实现自动时间注入，
     * 业务代码无需手动赋值，避免遗漏。
     * <p>对应 Entity 中的注解：
     * <pre>
     * {@literal @}TableField(fill = FieldFill.INSERT)
     * private LocalDateTime createdAt;
     *
     * {@literal @}TableField(fill = FieldFill.INSERT_UPDATE)
     * private LocalDateTime updatedAt;
     * </pre>
     */
    @Bean
    public MetaObjectHandler metaObjectHandler() {
        return new MetaObjectHandler() {

            @Override
            public void insertFill(MetaObject metaObject) {
                LocalDateTime now = LocalDateTime.now();
                this.strictInsertFill(metaObject, "createdAt", LocalDateTime.class, now);
                this.strictInsertFill(metaObject, "updatedAt", LocalDateTime.class, now);
            }

            @Override
            public void updateFill(MetaObject metaObject) {
                this.strictUpdateFill(metaObject, "updatedAt", LocalDateTime.class, LocalDateTime.now());
            }
        };
    }
}
