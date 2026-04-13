-- V1__create_user_permission_tables.sql
-- 模块一：用户与权限
-- 包含表：itsm_user, itsm_dept, itsm_user_group, itsm_user_group_member, itsm_role, itsm_permission, itsm_user_role, itsm_role_permission

CREATE TABLE IF NOT EXISTS itsm.itsm_user (
    id              BIGINT          NOT NULL,
    account_no      VARCHAR(64)     NOT NULL,
    employee_name   VARCHAR(64)     NOT NULL,
    password_hash   VARCHAR(128)    NOT NULL,
    phone           VARCHAR(20),
    email           VARCHAR(128),
    avatar_url      VARCHAR(512),
    dept_id         BIGINT,
    status          SMALLINT        NOT NULL DEFAULT 1,
    last_login_at   TIMESTAMPTZ,
    last_login_ip   VARCHAR(64),
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    created_by      BIGINT          NOT NULL DEFAULT 0,
    is_deleted      SMALLINT        NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_user PRIMARY KEY (id),
    CONSTRAINT chk_itsm_user_account_length CHECK (LENGTH(TRIM(account_no)) BETWEEN 1 AND 64),
    CONSTRAINT chk_itsm_user_account_format CHECK (account_no ~ '^[A-Za-z0-9_]+$'),
    CONSTRAINT chk_itsm_user_name_length CHECK (LENGTH(TRIM(employee_name)) BETWEEN 2 AND 64),
    CONSTRAINT chk_itsm_user_status CHECK (status IN (0, 1, 2))
);

COMMENT ON TABLE itsm.itsm_user IS '用户表，存储系统登录账号、员工信息及认证数据';
COMMENT ON COLUMN itsm.itsm_user.id IS '雪花算法生成的主键ID';
COMMENT ON COLUMN itsm.itsm_user.account_no IS '登录账号/工号，仅允许字母数字下划线，全局唯一';
COMMENT ON COLUMN itsm.itsm_user.employee_name IS '员工姓名，长度2-64字符';
COMMENT ON COLUMN itsm.itsm_user.password_hash IS 'BCrypt加盐哈希，禁止存储明文密码';
COMMENT ON COLUMN itsm.itsm_user.phone IS '手机号，用于MFA多因素认证及短信推送';
COMMENT ON COLUMN itsm.itsm_user.email IS '邮箱地址，用于MFA及邮件通知';
COMMENT ON COLUMN itsm.itsm_user.avatar_url IS '头像文件在MinIO中的存储路径';
COMMENT ON COLUMN itsm.itsm_user.dept_id IS '所属部门ID，外键关联itsm_dept';
COMMENT ON COLUMN itsm.itsm_user.status IS '账号状态：0禁用 1启用 2待管理员审核';
COMMENT ON COLUMN itsm.itsm_user.last_login_at IS '最后登录时间，用于审计和活跃度分析';
COMMENT ON COLUMN itsm.itsm_user.last_login_ip IS '最后登录IP地址，安全审计使用';
COMMENT ON COLUMN itsm.itsm_user.created_at IS '记录创建时间';
COMMENT ON COLUMN itsm.itsm_user.updated_at IS '记录最后更新时间';
COMMENT ON COLUMN itsm.itsm_user.created_by IS '记录创建人ID，0表示系统创建';
COMMENT ON COLUMN itsm.itsm_user.is_deleted IS '逻辑删除标记：0正常 1已删除';

CREATE UNIQUE INDEX uq_itsm_user_account_no ON itsm.itsm_user(account_no) WHERE is_deleted = 0;
CREATE INDEX idx_itsm_user_dept_id ON itsm.itsm_user(dept_id);
CREATE INDEX idx_itsm_user_status ON itsm.itsm_user(status) WHERE is_deleted = 0;
CREATE INDEX idx_itsm_user_email ON itsm.itsm_user(email) WHERE is_deleted = 0;

CREATE TABLE IF NOT EXISTS itsm.itsm_dept (
    id          BIGINT      NOT NULL,
    name        VARCHAR(64) NOT NULL,
    parent_id   BIGINT      NOT NULL DEFAULT 0,
    sort_order  INTEGER     NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by  BIGINT      NOT NULL DEFAULT 0,
    is_deleted  SMALLINT    NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_dept PRIMARY KEY (id)
);

COMMENT ON TABLE itsm.itsm_dept IS '部门表，支持无限层级树形组织结构';
COMMENT ON COLUMN itsm.itsm_dept.id IS '雪花算法主键';
COMMENT ON COLUMN itsm.itsm_dept.name IS '部门名称';
COMMENT ON COLUMN itsm.itsm_dept.parent_id IS '父部门ID，0表示顶级部门';
COMMENT ON COLUMN itsm.itsm_dept.sort_order IS '同级部门排序序号';
COMMENT ON COLUMN itsm.itsm_dept.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_dept.updated_at IS '更新时间';
COMMENT ON COLUMN itsm.itsm_dept.created_by IS '创建人ID';
COMMENT ON COLUMN itsm.itsm_dept.is_deleted IS '逻辑删除标记';

CREATE INDEX idx_itsm_dept_parent_id ON itsm.itsm_dept(parent_id) WHERE is_deleted = 0;

CREATE TABLE IF NOT EXISTS itsm.itsm_user_group (
    id          BIGINT          NOT NULL,
    name        VARCHAR(64)     NOT NULL,
    dept_id     BIGINT,
    description VARCHAR(256),
    created_at  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    created_by  BIGINT          NOT NULL DEFAULT 0,
    is_deleted  SMALLINT        NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_user_group PRIMARY KEY (id)
);

COMMENT ON TABLE itsm.itsm_user_group IS '用户组表，工单分配与权限控制的基本单元，如一线支持组、二线运维组';
COMMENT ON COLUMN itsm.itsm_user_group.id IS '主键ID';
COMMENT ON COLUMN itsm.itsm_user_group.name IS '用户组名称，如"应用运维一组"';
COMMENT ON COLUMN itsm.itsm_user_group.dept_id IS '所属部门ID，可选';
COMMENT ON COLUMN itsm.itsm_user_group.description IS '组描述说明';
COMMENT ON COLUMN itsm.itsm_user_group.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_user_group.updated_at IS '更新时间';
COMMENT ON COLUMN itsm.itsm_user_group.created_by IS '创建人';
COMMENT ON COLUMN itsm.itsm_user_group.is_deleted IS '逻辑删除标记';

CREATE INDEX idx_itsm_user_group_dept_id ON itsm.itsm_user_group(dept_id) WHERE is_deleted = 0;

CREATE TABLE IF NOT EXISTS itsm.itsm_user_group_member (
    group_id        BIGINT      NOT NULL,
    user_id         BIGINT      NOT NULL,
    role_in_group   VARCHAR(32) NOT NULL DEFAULT 'MEMBER',
    joined_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT pk_itsm_user_group_member PRIMARY KEY (group_id, user_id),
    CONSTRAINT chk_role_in_group CHECK (role_in_group IN ('MEMBER', 'LEADER'))
);

COMMENT ON TABLE itsm.itsm_user_group_member IS '用户组成员关联表，多对多关系';
COMMENT ON COLUMN itsm.itsm_user_group_member.group_id IS '用户组ID';
COMMENT ON COLUMN itsm.itsm_user_group_member.user_id IS '用户ID';
COMMENT ON COLUMN itsm.itsm_user_group_member.role_in_group IS '组内角色：MEMBER普通成员 LEADER组长';
COMMENT ON COLUMN itsm.itsm_user_group_member.joined_at IS '加入时间';

CREATE INDEX idx_itsm_group_member_user_id ON itsm.itsm_user_group_member(user_id);

CREATE TABLE IF NOT EXISTS itsm.itsm_role (
    id          BIGINT          NOT NULL,
    code        VARCHAR(64)     NOT NULL,
    name        VARCHAR(64)     NOT NULL,
    description VARCHAR(256),
    is_system   SMALLINT        NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    created_by  BIGINT          NOT NULL DEFAULT 0,
    is_deleted  SMALLINT        NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_role PRIMARY KEY (id)
);

COMMENT ON TABLE itsm.itsm_role IS '角色表，定义系统角色如超级管理员、运维工程师、服务台人员';
COMMENT ON COLUMN itsm.itsm_role.id IS '主键';
COMMENT ON COLUMN itsm.itsm_role.code IS '角色编码，如ROLE_ADMIN，用于代码层权限判断';
COMMENT ON COLUMN itsm.itsm_role.name IS '角色显示名称';
COMMENT ON COLUMN itsm.itsm_role.description IS '角色描述';
COMMENT ON COLUMN itsm.itsm_role.is_system IS '系统内置角色标记，1表示内置，禁止删除和修改code';
COMMENT ON COLUMN itsm.itsm_role.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_role.updated_at IS '更新时间';
COMMENT ON COLUMN itsm.itsm_role.created_by IS '创建人';
COMMENT ON COLUMN itsm.itsm_role.is_deleted IS '逻辑删除标记';

CREATE UNIQUE INDEX uq_itsm_role_code ON itsm.itsm_role(code) WHERE is_deleted = 0;

CREATE TABLE IF NOT EXISTS itsm.itsm_permission (
    id            BIGINT      NOT NULL,
    code          VARCHAR(128) NOT NULL,
    name          VARCHAR(64) NOT NULL,
    type          VARCHAR(16) NOT NULL,
    resource_path VARCHAR(256),
    parent_id     BIGINT      NOT NULL DEFAULT 0,
    sort_order    INTEGER     NOT NULL DEFAULT 0,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by    BIGINT      NOT NULL DEFAULT 0,
    is_deleted    SMALLINT    NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_permission PRIMARY KEY (id),
    CONSTRAINT chk_itsm_permission_type CHECK (type IN ('MENU', 'BUTTON', 'API'))
);

COMMENT ON TABLE itsm.itsm_permission IS '权限资源表，存储菜单、按钮、API接口级权限定义';
COMMENT ON COLUMN itsm.itsm_permission.id IS '主键';
COMMENT ON COLUMN itsm.itsm_permission.code IS '权限编码，如ticket:create，用于前端按钮显隐控制';
COMMENT ON COLUMN itsm.itsm_permission.name IS '权限显示名称';
COMMENT ON COLUMN itsm.itsm_permission.type IS '权限类型：MENU菜单项 BUTTON页面按钮 API后端接口';
COMMENT ON COLUMN itsm.itsm_permission.resource_path IS '前端路由路径或后端接口路径';
COMMENT ON COLUMN itsm.itsm_permission.parent_id IS '父权限ID，构建权限树结构';
COMMENT ON COLUMN itsm.itsm_permission.sort_order IS '同级排序';
COMMENT ON COLUMN itsm.itsm_permission.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_permission.updated_at IS '更新时间';
COMMENT ON COLUMN itsm.itsm_permission.created_by IS '创建人';
COMMENT ON COLUMN itsm.itsm_permission.is_deleted IS '逻辑删除标记';

CREATE UNIQUE INDEX uq_itsm_permission_code ON itsm.itsm_permission(code) WHERE is_deleted = 0;
CREATE INDEX idx_itsm_permission_parent ON itsm.itsm_permission(parent_id);

CREATE TABLE IF NOT EXISTS itsm.itsm_user_role (
    user_id     BIGINT      NOT NULL,
    role_id     BIGINT      NOT NULL,
    granted_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    granted_by  BIGINT      NOT NULL,
    
    CONSTRAINT pk_itsm_user_role PRIMARY KEY (user_id, role_id)
);

COMMENT ON TABLE itsm.itsm_user_role IS '用户角色关联表，多对多关系';
COMMENT ON COLUMN itsm.itsm_user_role.user_id IS '用户ID';
COMMENT ON COLUMN itsm.itsm_user_role.role_id IS '角色ID';
COMMENT ON COLUMN itsm.itsm_user_role.granted_at IS '授权时间';
COMMENT ON COLUMN itsm.itsm_user_role.granted_by IS '授权人ID';

CREATE INDEX idx_itsm_user_role_role_id ON itsm.itsm_user_role(role_id);

CREATE TABLE IF NOT EXISTS itsm.itsm_role_permission (
    role_id         BIGINT      NOT NULL,
    permission_id   BIGINT      NOT NULL,
    
    CONSTRAINT pk_itsm_role_permission PRIMARY KEY (role_id, permission_id)
);

COMMENT ON TABLE itsm.itsm_role_permission IS '角色权限关联表，定义角色拥有的权限集合';
COMMENT ON COLUMN itsm.itsm_role_permission.role_id IS '角色ID';
COMMENT ON COLUMN itsm.itsm_role_permission.permission_id IS '权限ID';

CREATE INDEX idx_itsm_role_perm_perm_id ON itsm.itsm_role_permission(permission_id);