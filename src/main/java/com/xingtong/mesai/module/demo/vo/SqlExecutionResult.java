package com.xingtong.mesai.module.demo.vo;

import lombok.Builder;
import lombok.Data;

import java.util.List;
import java.util.Map;

/**
 * SQL 执行结果 VO
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 演示模块
 * @related REQ-MES-AI-20260412-005（S2.5 演示MVP）
 */
@Data
@Builder
public class SqlExecutionResult {

    /**
     * 执行类型：SELECT / DML_PREVIEW
     * DML_PREVIEW 表示在事务内执行后已回滚（仅展示影响行数，不实际修改数据）
     */
    private String execType;

    /** SELECT 查询结果集（execType=SELECT 时有值）*/
    private List<Map<String, Object>> rows;

    /** 结果集总行数 */
    private int totalRows;

    /** DML 影响行数（execType=DML_PREVIEW 时有值）*/
    private int affectedRows;

    /** 执行耗时（毫秒）*/
    private long elapsedMs;

    /** 执行提示信息（如："DML 在事务内执行并已回滚，实际数据未修改"）*/
    private String notice;

    /** 执行是否成功 */
    private boolean success;

    /** 执行失败时的错误信息 */
    private String errorMessage;
}
