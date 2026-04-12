package com.xingtong.mesai.config;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import com.fasterxml.jackson.annotation.PropertyAccessor;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.jsontype.impl.LaissezFaireSubTypeValidator;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.serializer.Jackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;

/**
 * Redis 连接与序列化配置
 *
 * <p>主要用途：
 * <ul>
 *   <li>任务编号（task_no）分布式序列号生成（see TaskNoGenerator）</li>
 *   <li>JWT Token 黑名单存储</li>
 *   <li>Token 预算计数器</li>
 * </ul>
 *
 * <p>连接参数通过 application.yml → 环境变量注入，禁止硬编码。
 * <p>连接配置项：REDIS_HOST / REDIS_PORT / REDIS_PASSWORD（见 application.yml）
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 * @module 全局配置
 * @related REQ-MES-AI-20260412-005（S1-5 后端项目骨架）
 */
@Configuration
public class RedisConfig {

    /**
     * 通用 RedisTemplate（Key=String，Value=JSON）
     *
     * <p>Value 使用 Jackson2JsonRedisSerializer 序列化，支持 Java 8 时间类型。
     * <p>对象类型信息嵌入 JSON，反序列化时无需显式指定类型。
     */
    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory factory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(factory);

        // Key 序列化：String（可读性好，便于 Redis CLI 查看）
        StringRedisSerializer stringSerializer = new StringRedisSerializer();
        template.setKeySerializer(stringSerializer);
        template.setHashKeySerializer(stringSerializer);

        // Value 序列化：Jackson JSON（支持复杂对象和 Java 8 时间类型）
        Jackson2JsonRedisSerializer<Object> jsonSerializer = buildJsonSerializer();
        template.setValueSerializer(jsonSerializer);
        template.setHashValueSerializer(jsonSerializer);

        template.afterPropertiesSet();
        return template;
    }

    /**
     * StringRedisTemplate（Key=String，Value=String）
     *
     * <p>用于 TaskNoGenerator 的序列号 INCR 操作，保证原子性。
     * <p>Spring Boot 自动配置已提供默认 bean，此处显式声明以明确依赖关系。
     */
    @Bean
    public StringRedisTemplate stringRedisTemplate(RedisConnectionFactory factory) {
        return new StringRedisTemplate(factory);
    }

    // ── 私有方法 ─────────────────────────────────────────────────

    private Jackson2JsonRedisSerializer<Object> buildJsonSerializer() {
        ObjectMapper objectMapper = new ObjectMapper();
        // 序列化所有字段（包括私有字段）
        objectMapper.setVisibility(PropertyAccessor.ALL, JsonAutoDetect.Visibility.ANY);
        // 序列化时嵌入类型信息（反序列化时可还原为原始类型）
        objectMapper.activateDefaultTyping(
                LaissezFaireSubTypeValidator.instance,
                ObjectMapper.DefaultTyping.NON_FINAL,
                JsonTypeInfo.As.PROPERTY
        );
        // 支持 Java 8 LocalDateTime 等时间类型
        objectMapper.registerModule(new JavaTimeModule());

        Jackson2JsonRedisSerializer<Object> serializer = new Jackson2JsonRedisSerializer<>(Object.class);
        serializer.setObjectMapper(objectMapper);
        return serializer;
    }
}
