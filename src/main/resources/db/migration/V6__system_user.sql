-- ============================================================
-- 文件：V6__system_user.sql
-- 用途：系统用户表（sys_user）初始化
-- 模块：系统管理模块（S2-3）
-- 作者：AI（芯智云匠）
-- 日期：2026-04-13
-- 关联需求：REQ-MES-AI-20260412-005
-- ============================================================

USE mesai_app;

-- 系统用户表
CREATE TABLE IF NOT EXISTS sys_user (
    id          BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键',
    username    VARCHAR(64)  NOT NULL                COMMENT '登录账号（唯一）',
    real_name   VARCHAR(64)  NOT NULL                COMMENT '真实姓名',
    password    VARCHAR(128) NOT NULL                COMMENT '密码（BCrypt 加密存储）',
    role        VARCHAR(32)  NOT NULL                COMMENT '角色代码：BUSINESS_USER/IT_REVIEWER/IT_MANAGER/TECH_LEAD/AI_AGENT/MANAGER',
    dept        VARCHAR(64)  DEFAULT NULL            COMMENT '所属部门',
    email       VARCHAR(128) DEFAULT NULL            COMMENT '邮箱',
    is_active   TINYINT(1)   NOT NULL DEFAULT 1      COMMENT '是否启用：1启用 0禁用',
    is_deleted  TINYINT(1)   NOT NULL DEFAULT 0      COMMENT '逻辑删除：0未删除 1已删除',
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (id),
    UNIQUE KEY uk_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统用户表';

-- 初始管理员账号（密码：Xingtong@2026，BCrypt 加密）
INSERT INTO sys_user (username, real_name, password, role, dept, email, is_active)
VALUES (
    'admin',
    '系统管理员',
    '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iAt6yV9C',
    'TECH_LEAD',
    'IT部',
    'admin@xingtong.com',
    1
);
