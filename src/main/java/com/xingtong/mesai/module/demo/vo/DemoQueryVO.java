package com.xingtong.mesai.module.demo.vo;

import lombok.Data;

import java.util.List;

/**
 * 演示查询响应 VO
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 演示模块
 * @related REQ-MES-AI-20260412-005（S2.5 演示MVP）
 */
@Data
public class DemoQueryVO {

    /** 生成模式（sql / dml / fe_component）*/
    private String mode;

    /** 原始需求描述 */
    private String question;

    /** AI 生成的代码（SQL 或 Vue 组件）*/
    private String generatedCode;

    /** AI 对生成代码的解释说明 */
    private String explanation;

    /** RAG 使用的知识库上下文片段列表 */
    private List<ContextDocVO> contextDocs;

    /** Token 消耗数量 */
    private int tokensUsed;

    /** AI 接口响应耗时（毫秒）*/
    private int aiResponseTimeMs;

    /**
     * SQL 执行结果（仅 mode=sql/dml 且请求了执行时有值）
     * null 表示未执行（fe_component 模式或 executeSql=false）
     */
    private SqlExecutionResult executionResult;
}
