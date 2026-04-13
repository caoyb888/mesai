package com.xingtong.mesai.module.system.entity;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableLogic;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 系统用户实体
 *
 * <p>对应数据库表 sys_user，存储登录账号、角色、部门等基本信息。
 * <p>密码字段使用 BCrypt 加密，禁止以明文形式存储或日志输出。
 * <p>逻辑删除字段 is_deleted 由 MyBatis Plus 全局配置自动处理。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-6）
 */
@Data
@TableName("sys_user")
public class SysUser {

    /** 主键，数据库自增 */
    @TableId(type = IdType.AUTO)
    private Long id;

    /** 登录账号（唯一，全局不可重复） */
    private String username;

    /** 真实姓名 */
    private String realName;

    /**
     * 密码（BCrypt 加密存储）。
     * 注意：禁止在日志、响应体中输出此字段。
     */
    private String password;

    /**
     * 角色代码（与 {@link com.xingtong.mesai.module.system.enums.UserRole} 枚举对应）。
     * 可选值：BUSINESS_USER / IT_REVIEWER / IT_MANAGER / TECH_LEAD / AI_AGENT / MANAGER
     */
    private String role;

    /** 所属部门 */
    private String dept;

    /** 邮箱 */
    private String email;

    /** 账号是否启用：1-启用，0-禁用 */
    private Integer isActive;

    /** 逻辑删除标记，由 MyBatis Plus 自动处理 */
    @TableLogic
    private Integer isDeleted;

    /** 创建时间，由 MetaObjectHandler 自动填充 */
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createdAt;

    /** 更新时间，由 MetaObjectHandler 自动填充 */
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
}
