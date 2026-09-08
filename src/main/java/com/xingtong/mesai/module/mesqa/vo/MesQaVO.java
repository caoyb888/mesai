package com.xingtong.mesai.module.mesqa.vo;

import com.xingtong.mesai.module.demo.vo.ContextDocVO;
import lombok.Data;

import java.util.List;

/**
 * MES 数据问答响应 VO
 *
 * <p>RAG 上下文片段复用演示模块的 {@link ContextDocVO}（结构完全一致：
 * source / docType / contentPreview / relevanceScore），避免重复定义。
 *
 * @author AI（芯智云匠）
 * @date 2026-07-17
 * @module MES数据问答
 * @related REQ-MES-AI-20260716-001（真实 MES 库理解与问答）
 */
@Data
public class MesQaVO {

    /** 原始业务问题 */
    private String question;

    /** 实际生效的检索范围（auto / table / proc）*/
    private String kind;

    /** AI 基于知识库上下文生成的回答 */
    private String answer;

    /** RAG 检索到的知识库上下文片段列表（含相关度）*/
    private List<ContextDocVO> contextDocs;

    /** 实际使用的 AI 提供商 */
    private String provider;

    /** 实际使用的模型名称 */
    private String model;

    /** Token 消耗数量 */
    private int tokensUsed;

    /** AI 接口响应耗时（毫秒）*/
    private int aiResponseTimeMs;
}
