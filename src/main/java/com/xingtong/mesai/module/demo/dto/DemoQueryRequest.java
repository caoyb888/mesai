package com.xingtong.mesai.module.demo.dto;

import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;

/**
 * 演示查询请求 DTO
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 演示模块
 * @related REQ-MES-AI-20260412-005（S2.5 演示MVP）
 */
@Data
public class DemoQueryRequest {

    /** 自然语言需求描述 */
    @NotBlank(message = "需求描述不能为空")
    @Size(min = 5, max = 500, message = "需求描述长度须在 5~500 字之间")
    private String question;

    /**
     * 生成模式：
     * - sql：生成 SELECT 查询 SQL
     * - dml：生成 INSERT/UPDATE/DELETE SQL
     * - fe_component：生成 Vue 3 前端组件代码
     */
    @NotBlank(message = "模式不能为空")
    @Pattern(regexp = "sql|dml|fe_component", message = "mode 只能是 sql / dml / fe_component")
    private String mode;

    /**
     * 是否在 ITSM 测试库上执行 SQL（仅 mode=sql/dml 时有效）
     * 默认 false；fe_component 模式强制忽略此字段
     */
    private boolean executeSql = false;
}
