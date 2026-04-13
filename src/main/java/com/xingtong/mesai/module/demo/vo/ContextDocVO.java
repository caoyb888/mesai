package com.xingtong.mesai.module.demo.vo;

import lombok.Data;

/**
 * RAG 上下文文档片段 VO
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 演示模块
 * @related REQ-MES-AI-20260412-005（S2.5 演示MVP）
 */
@Data
public class ContextDocVO {
    /** 来源标识 */
    private String source;
    /** 文档类型 */
    private String docType;
    /** 内容摘要（前200字符）*/
    private String contentPreview;
    /** 相关度得分（0~1，越高越相关）*/
    private double relevanceScore;
}
