package com.xingtong.mesai.module.system.vo;

import lombok.Data;

import java.time.LocalDateTime;

/**
 * 用户视图对象（响应体）
 *
 * <p>用于用户列表查询接口返回，明确排除 password 等敏感字段。
 * <p>字段命名与数据库 resultMap（SysUserMapper.xml）保持一致。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-6）
 */
@Data
public class UserVO {

    /** 用户 ID */
    private Long userId;

    /** 登录账号 */
    private String username;

    /** 真实姓名 */
    private String realName;

    /** 角色代码（如 IT_MANAGER） */
    private String role;

    /** 所属部门 */
    private String dept;

    /** 邮箱 */
    private String email;

    /** 账号是否启用：1-启用，0-禁用 */
    private Integer isActive;

    /** 创建时间 */
    private LocalDateTime createdAt;
}
