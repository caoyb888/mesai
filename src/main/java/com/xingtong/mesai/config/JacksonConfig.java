package com.xingtong.mesai.config;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.fasterxml.jackson.datatype.jsr310.deser.LocalDateDeserializer;
import com.fasterxml.jackson.datatype.jsr310.deser.LocalDateTimeDeserializer;
import com.fasterxml.jackson.datatype.jsr310.ser.LocalDateSerializer;
import com.fasterxml.jackson.datatype.jsr310.ser.LocalDateTimeSerializer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.converter.json.Jackson2ObjectMapperBuilder;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * 全局 Jackson 序列化配置
 *
 * <p>统一项目中所有 JSON 序列化/反序列化行为：
 * <ul>
 *   <li>LocalDateTime 格式：{@code yyyy-MM-dd HH:mm:ss}</li>
 *   <li>LocalDate 格式：{@code yyyy-MM-dd}</li>
 *   <li>忽略未知字段（前后端版本不一致时不报错）</li>
 *   <li>禁用将时间序列化为时间戳（使用字符串格式，可读性好）</li>
 * </ul>
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 * @module 全局配置
 * @related REQ-MES-AI-20260412-005（S1-5 后端项目骨架）
 */
@Configuration
public class JacksonConfig {

    /** 标准日期时间格式 */
    public static final String DATE_TIME_FORMAT = "yyyy-MM-dd HH:mm:ss";

    /** 标准日期格式 */
    public static final String DATE_FORMAT = "yyyy-MM-dd";

    @Bean
    public Jackson2ObjectMapperBuilder jackson2ObjectMapperBuilder() {
        JavaTimeModule javaTimeModule = new JavaTimeModule();

        // LocalDateTime：序列化与反序列化均使用 "yyyy-MM-dd HH:mm:ss"
        DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern(DATE_TIME_FORMAT);
        javaTimeModule.addSerializer(LocalDateTime.class,
                new LocalDateTimeSerializer(dateTimeFormatter));
        javaTimeModule.addDeserializer(LocalDateTime.class,
                new LocalDateTimeDeserializer(dateTimeFormatter));

        // LocalDate：序列化与反序列化均使用 "yyyy-MM-dd"
        DateTimeFormatter dateFormatter = DateTimeFormatter.ofPattern(DATE_FORMAT);
        javaTimeModule.addSerializer(LocalDate.class,
                new LocalDateSerializer(dateFormatter));
        javaTimeModule.addDeserializer(LocalDate.class,
                new LocalDateDeserializer(dateFormatter));

        return new Jackson2ObjectMapperBuilder()
                .modules(javaTimeModule)
                // 禁止将 LocalDateTime 序列化为时间戳数字
                .featuresToDisable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)
                // 忽略 JSON 中存在但 Java 对象中不存在的字段，防止版本兼容问题
                .featuresToDisable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
    }
}
