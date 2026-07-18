package com.xingtong.mesai.module.messql.dto;

import lombok.Data;

import javax.validation.constraints.Max;
import javax.validation.constraints.Min;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;

/**
 * MES 取数请求 DTO
 *
 * <p>面向真实 MES 库（钢板/卷材钢厂，Oracle）的自然语言取数：
 * 前端提交业务取数需求，后端转发至 AI 网关 /v1/ai/mes-sql 生成 Oracle 只读 SELECT，
 * 再经 SQL 安全校验后在 MES 只读数据源执行并返回结果。
 *
 * @author AI（芯智云匠）
 * @date 2026-07-18
 * @module MES取数
 * @related REQ-MES-AI-20260716-001（NL → Oracle 只读 SELECT 生成与执行）
 */
@Data
public class MesSqlRequest {

    /** 自然语言取数需求 */
    @NotBlank(message = "取数需求不能为空")
    @Size(min = 5, max = 500, message = "取数需求长度须在 5~500 字之间")
    private String question;

    /**
     * RAG 检索条数（1~10），不传则由网关按配置默认值处理（预算降级时自动缩减）
     */
    @Min(value = 1, message = "topN 最小为 1")
    @Max(value = 10, message = "topN 最大为 10")
    private Integer topN;

    /**
     * 是否在 MES 只读数据源上执行生成的 SELECT。
     * 默认 true（取数场景默认执行并返回结果）；
     * 未配置只读数据源时自动降级为“仅生成不执行”。
     */
    private boolean executeSql = true;
}
