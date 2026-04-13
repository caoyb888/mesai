-- V9__init_permissions.sql
-- 初始化：内置权限数据（示例）
-- 实际项目中应根据需求填充完整权限数据

-- 系统管理模块权限
INSERT INTO itsm.itsm_permission (id, code, name, type, resource_path, parent_id, sort_order, created_by) VALUES
(1, 'system:manage', '系统管理', 'MENU', '/system', 0, 1, 0),
(2, 'user:manage', '用户管理', 'MENU', '/system/user', 1, 1, 0),
(3, 'user:create', '创建用户', 'BUTTON', NULL, 2, 1, 0),
(4, 'user:update', '编辑用户', 'BUTTON', NULL, 2, 2, 0),
(5, 'user:delete', '删除用户', 'BUTTON', NULL, 2, 3, 0),
(6, 'role:manage', '角色管理', 'MENU', '/system/role', 1, 2, 0);

-- 工单模块权限
INSERT INTO itsm.itsm_permission (id, code, name, type, resource_path, parent_id, sort_order, created_by) VALUES
(100, 'ticket:manage', '工单管理', 'MENU', '/ticket', 0, 2, 0),
(101, 'ticket:create', '创建工单', 'BUTTON', NULL, 100, 1, 0),
(102, 'ticket:claim', '接单处理', 'BUTTON', NULL, 100, 2, 0),
(103, 'ticket:transfer', '转单', 'BUTTON', NULL, 100, 3, 0),
(104, 'ticket:close', '关闭工单', 'BUTTON', NULL, 100, 4, 0);


-- V10__init_roles.sql
-- 初始化：内置角色数据

INSERT INTO itsm.itsm_role (id, code, name, description, is_system, created_by) VALUES
(1, 'ROLE_SUPER_ADMIN', '超级管理员', '系统超级管理员，拥有所有权限', 1, 0),
(2, 'ROLE_SYSTEM_ADMIN', '系统管理员', '负责系统配置、用户和权限管理', 1, 0),
(3, 'ROLE_SERVICE_DESK', '服务台人员', '一线支持，负责工单受理和分派', 1, 0),
(4, 'ROLE_SUPPORT_ENGINEER', '运维工程师', '二线支持，负责工单处理', 1, 0),
(5, 'ROLE_AUDITOR', '审计员', '负责查看审计日志和报表', 1, 0),
(6, 'ROLE_END_USER', '普通用户', '可提交工单和查看自己的工单', 1, 0);

-- 分配权限（超级管理员拥有所有权限）
INSERT INTO itsm.itsm_role_permission (role_id, permission_id) 
SELECT 1, id FROM itsm.itsm_permission WHERE is_deleted = 0;


-- V11__init_workflow_def.sql
-- 初始化：内置工作流定义（标准ITSM流程）

INSERT INTO itsm.itsm_workflow_def (id, code, name, states_json, transitions_json, allow_close_states, created_by) VALUES
(1, 'STANDARD_ITSM', '标准ITSM流程', 
'[
  {"code":"Created","label":"已创建","isInitial":true,"canDelete":true},
  {"code":"Pending","label":"待处理","isInitial":false,"canDelete":false},
  {"code":"Processing","label":"处理中","isInitial":false,"canDelete":false},
  {"code":"Pending_Review","label":"待审核","isInitial":false,"canDelete":false},
  {"code":"Closed","label":"已关闭","isInitial":false,"canDelete":false,"isFinal":true},
  {"code":"Suspended","label":"已挂起","isInitial":false,"canDelete":false}
]',
'[
  {"from":"Created","to":"Pending","action":"AUTO_ROUTE","actor":"SYSTEM","label":"自动分单"},
  {"from":"Pending","to":"Processing","action":"CLAIM","actor":"USER","label":"接单"},
  {"from":"Processing","to":"Pending_Review","action":"SUBMIT_REVIEW","actor":"USER","label":"提交审核"},
  {"from":"Pending_Review","to":"Closed","action":"APPROVE","actor":"USER","label":"审核通过关闭"},
  {"from":"Pending_Review","to":"Processing","action":"REJECT","actor":"USER","label":"驳回重办"},
  {"from":"Processing","to":"Suspended","action":"SUSPEND","actor":"USER","label":"挂起"},
  {"from":"Suspended","to":"Processing","action":"RESUME","actor":"USER","label":"恢复"},
  {"from":"Created","to":"Closed","action":"CLOSE","actor":"USER","label":"直接关闭"},
  {"from":"Processing","to":"Closed","action":"CLOSE","actor":"USER","label":"处理完成关闭"}
]',
'Created,Processing', 0);