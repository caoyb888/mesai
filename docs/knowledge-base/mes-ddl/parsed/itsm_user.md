## 表：itsm_user（用户表，存储系统登录账号、员工信息及认证数据）

**模块**：用户与权限  |  **Schema**：itsm  |  **来源文件**：01_用户与权限.sql

### 字段明细

| 字段名 | 数据类型 | 可空 | 默认值 | 说明 |
|--------|--------|------|------|------|
| `id` | `BIGINT` | 否 | `` | 雪花算法生成的主键ID |
| `account_no` | `VARCHAR(64)` | 否 | `` | 登录账号/工号，仅允许字母数字下划线，全局唯一 |
| `employee_name` | `VARCHAR(64)` | 否 | `` | 员工姓名，长度2-64字符 |
| `password_hash` | `VARCHAR(128)` | 否 | `` | BCrypt加盐哈希，禁止存储明文密码 |
| `phone` | `VARCHAR(20)` | 是 | `` | 手机号，用于MFA多因素认证及短信推送 |
| `email` | `VARCHAR(128)` | 是 | `` | 邮箱地址，用于MFA及邮件通知 |
| `avatar_url` | `VARCHAR(512)` | 是 | `` | 头像文件在MinIO中的存储路径 |
| `dept_id` | `BIGINT` | 是 | `` | 所属部门ID，外键关联itsm_dept |
| `status` | `SMALLINT` | 否 | `1` | 账号状态：0禁用 1启用 2待管理员审核 |
| `last_login_at` | `TIMESTAMPTZ` | 是 | `` | 最后登录时间，用于审计和活跃度分析 |
| `last_login_ip` | `VARCHAR(64)` | 是 | `` | 最后登录IP地址，安全审计使用 |
| `created_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 记录创建时间 |
| `updated_at` | `TIMESTAMPTZ` | 否 | `NOW()` | 记录最后更新时间 |
| `created_by` | `BIGINT` | 否 | `0` | 记录创建人ID，0表示系统创建 |
| `is_deleted` | `SMALLINT` | 否 | `0` | 逻辑删除标记：0正常 1已删除 |

> *chunk_type: table_card | chunk_id: 用户与权限_itsm_user_table_card*
