package com.xingtong.mesai.module.system.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * 系统角色枚举
 *
 * <p>对应 AI-MES-API-2026-001 第 2.4 节角色权限矩阵定义的 6 种角色。
 * <p>角色层级：MANAGER < BUSINESS_USER < IT_REVIEWER < IT_MANAGER < TECH_LEAD
 * <p>AI_AGENT 为独立服务账号，拥有执行日志写入权限，不参与层级比较。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-5 RBAC权限控制）
 */
@Getter
@AllArgsConstructor
public enum UserRole {

    /** 业务人员：提交需求、查看自己的任务、参与验收 */
    BUSINESS_USER("BUSINESS_USER", "业务人员"),

    /** IT 评审专员：评审需求、查看全部任务、执行授权 */
    IT_REVIEWER("IT_REVIEWER", "IT评审专员"),

    /** IT 负责人：IT_REVIEWER 全部权限 + 部署审批 + 配置管理 */
    IT_MANAGER("IT_MANAGER", "IT负责人"),

    /** 技术负责人：全部权限，管理断言库、审批 Prompt 变更 */
    TECH_LEAD("TECH_LEAD", "技术负责人"),

    /** AI 智能体：写入执行日志、代码交付物、测试报告（服务账号） */
    AI_AGENT("AI_AGENT", "AI智能体"),

    /** 管理层（只读）：查看报告、成本统计、Excel 导出，无写权限 */
    MANAGER("MANAGER", "管理层");

    /** 角色代码（与数据库 sys_user.role 字段一一对应） */
    private final String code;

    /** 角色中文名称 */
    private final String displayName;

    /**
     * 根据角色代码查找枚举。
     *
     * @param code 角色代码字符串
     * @return 对应枚举；未匹配时抛出 IllegalArgumentException
     */
    public static UserRole fromCode(String code) {
        for (UserRole role : values()) {
            if (role.code.equalsIgnoreCase(code)) {
                return role;
            }
        }
        throw new IllegalArgumentException("未知角色代码：" + code);
    }
}
