package com.xingtong.mesai.module.mesqa.dto;

import lombok.Data;

import javax.validation.constraints.Max;
import javax.validation.constraints.Min;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;

/**
 * MES 数据问答请求 DTO
 *
 * <p>面向真实 MES 库（钢板/卷材钢厂）的表结构与存储过程自然语言问答。
 * 前端提交后由本层转发至 AI 网关 /v1/ai/mes-qa，网关侧完成 RAG 检索 + LLM 接地作答。
 *
 * @author AI（芯智云匠）
 * @date 2026-07-17
 * @module MES数据问答
 * @related REQ-MES-AI-20260716-001（真实 MES 库理解与问答）
 */
@Data
public class MesQaRequest {

    /** 自然语言业务问题 */
    @NotBlank(message = "问题不能为空")
    @Size(min = 5, max = 500, message = "问题长度须在 5~500 字之间")
    private String question;

    /**
     * 检索范围：
     * - auto：表 + 存储过程混合（默认）
     * - table：仅表卡片
     * - proc：仅存储过程卡片
     */
    @Pattern(regexp = "auto|table|proc", message = "kind 只能是 auto / table / proc")
    private String kind = "auto";

    /**
     * RAG 检索条数（1~10），不传则由网关按配置默认值处理（预算降级时自动缩减）
     */
    @Min(value = 1, message = "topN 最小为 1")
    @Max(value = 10, message = "topN 最大为 10")
    private Integer topN;
}
