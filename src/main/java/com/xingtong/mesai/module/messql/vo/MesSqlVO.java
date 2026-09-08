package com.xingtong.mesai.module.messql.vo;

import com.xingtong.mesai.module.demo.vo.ContextDocVO;
import com.xingtong.mesai.module.demo.vo.SqlExecutionResult;
import lombok.Data;

import java.util.List;

/**
 * MES 取数响应 VO
 *
 * <p>复用演示模块的 {@link ContextDocVO}（RAG 上下文片段）与 {@link SqlExecutionResult}
 * （SQL 执行结果），避免重复定义结构一致的载体。
 *
 * @author AI（芯智云匠）
 * @date 2026-07-18
 * @module MES取数
 * @related REQ-MES-AI-20260716-001（NL → Oracle 只读 SELECT 生成与执行）
 */
@Data
public class MesSqlVO {

    /** 原始取数需求 */
    private String question;

    /** 是否成功生成 SQL（false 表示知识库依据不足，见 unanswerableReason）*/
    private boolean generated;

    /** AI 生成的 Oracle 只读 SELECT（未生成时为空串）*/
    private String sql;

    /** 对查询逻辑、涉及表/字段、关键条件的中文说明 */
    private String explanation;

    /** SQL 引用的表名（英文，来自知识库上下文）*/
    private List<String> referencedTables;

    /** SQL 引用的关键字段名（英文）*/
    private List<String> referencedColumns;

    /** 未能生成 SQL 的原因（知识库无对应表/字段时有值）*/
    private String unanswerableReason;

    /** RAG 检索到的知识库上下文片段列表（含相关度）*/
    private List<ContextDocVO> contextDocs;

    /**
     * SQL 执行结果（executeSql=true 且校验通过、只读数据源已配置时有值）。
     * 校验拦截 / 未配置数据源 / 未生成 SQL 时，execType 分别为 BLOCKED / SKIPPED。
     */
    private SqlExecutionResult executionResult;

    /** 实际使用的 AI 提供商 */
    private String provider;

    /** 实际使用的模型名称 */
    private String model;

    /** Token 消耗数量 */
    private int tokensUsed;

    /** AI 接口响应耗时（毫秒）*/
    private int aiResponseTimeMs;

    /**
     * 自纠错重试次数（REQ-MES-AI-20260730-002 B2.1）。
     * 0 = 首轮即通过/未重试；>0 = 实际发生的重试轮数（上限由 mes.sql.retry.max-rounds 控制）。
     */
    private int retryCount;
}
