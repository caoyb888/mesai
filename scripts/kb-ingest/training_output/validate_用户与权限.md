# 验证结果：用户与权限

## IT-UPerm-01（⭐）

**题目**：查询所有有效用户（未删除、状态正常）的工号、姓名和所属部门名称，按部门排序。

**检查点**：JOIN dept, 过滤逻辑删除, 过滤状态

**AI 输出**：

1. **分析涉及的表和字段**

   - 表 `itsm_user`：存储用户信息，包括工号、姓名、所属部门ID等。
     - 字段：
       - `work_number`：工号
       - `name`：姓名
       - `dept_id`：所属部门ID
       - `is_deleted`：逻辑删除标记，有效用户为0
       - `status`：用户状态，正常状态的值需要根据业务定义，这里假设正常状态为1

   - 表 `itsm_dept`：存储部门信息，包括部门名称等。
     - 字段：
       - `name`：部门名称
       - `id`：部门ID

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 有效用户的工号、姓名和所属部门名称，按部门排序
SELECT u.work_number, u.name, d.name AS dept_name
FROM itsm_user u
JOIN itsm_dept d ON u.dept_id = d.id
WHERE u.is_deleted = 0 AND u.status = 1
ORDER BY d.sort_order, u.dept_id;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - `WHERE` 条件：
     - `u.is_deleted = 0`：筛选出未被逻辑删除的用户。
     - `u.status = 1`：筛选出状态正常的用户，这里假设正常状态为1，具体值需要根据实际业务定义。

   - `JOIN` 逻辑：
     - 使用 `INNER JOIN` 将 `itsm_user` 表和 `itsm_dept` 表连接起来，通过 `u.dept_id = d.id` 条件匹配用户和其所属部门。
     - 这样，每个用户记录都会关联到其对应的部门名称。

   - `ORDER BY` 逻辑：
     - 首先按照部门的 `sort_order` 排序，确保部门顺序正确。
     - 然后按照用户的 `dept_id` 排序，确保同一部门内的用户按照部门ID排序。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-UPerm-02（⭐⭐）

**题目**：查询某用户（工号已知）拥有的所有角色名称及其对应的权限编码列表。

**检查点**：多表 JOIN, 通过中间表关联, 权限去重

**AI 输出**：

1. **分析涉及的表和字段**

   - `itsm_user`：用户表，包含用户信息，字段包括`id`（用户ID）。
   - `itsm_user_role`：用户角色关联表，字段包括`user_id`（用户ID）和`role_id`（角色ID）。
   - `itsm_role`：角色表，字段包括`id`（角色ID）和`name`（角色名称）。
   - `itsm_role_permission`：角色权限关联表，字段包括`role_id`（角色ID）和`permission_id`（权限ID）。
   - `itsm_permission`：权限资源表，字段包括`id`（权限ID）和`code`（权限编码）。

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 根据用户工号查询用户拥有的所有角色名称及其对应的权限编码列表
SELECT 
    r.name AS role_name,
    p.code AS permission_code
FROM 
    itsm_user u
JOIN 
    itsm_user_role ur ON u.id = ur.user_id
JOIN 
    itsm_role r ON ur.role_id = r.id
JOIN 
    itsm_role_permission rp ON r.id = rp.role_id
JOIN 
    itsm_permission p ON rp.permission_id = p.id
WHERE 
    u.id = #{user_id} -- 假设 #{user_id} 是参数化的用户工号
    AND u.is_deleted = 0 -- 确保查询的是非删除的用户
    AND r.is_deleted = 0 -- 确保查询的是非删除的角色
    AND p.is_deleted = 0 -- 确保查询的是非删除的权限
ORDER BY 
    r.name, 
    p.sort_order; -- 按角色名称和权限排序
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - `WHERE u.id = #{user_id}`：这个条件用于筛选出特定工号的用户。
   - `AND u.is_deleted = 0`：确保查询的是非删除的用户。
   - `AND r.is_deleted = 0`：确保查询的是非删除的角色。
   - `AND p.is_deleted = 0`：确保查询的是非删除的权限。

   - `JOIN itsm_user_role ur ON u.id = ur.user_id`：将用户表与其对应的角色关联表进行连接，以获取用户的角色信息。
   - `JOIN itsm_role r ON ur.role_id = r.id`：将用户角色关联表与角色表进行连接，以获取角色的详细信息。
   - `JOIN itsm_role_permission rp ON r.id = rp.role_id`：将角色表与角色权限关联表进行连接，以获取角色对应的权限信息。
   - `JOIN itsm_permission p ON rp.permission_id = p.id`：将角色权限关联表与权限表进行连接，以获取权限的详细信息。

   - `ORDER BY r.name, p.sort_order`：对结果进行排序，首先按角色名称排序，其次按权限的排序序号排序。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-UPerm-03（⭐⭐）

**题目**：统计各部门的用户数量，只统计有效用户，按用户数降序排列。

**检查点**：GROUP BY, COUNT, 过滤条件

**AI 输出**：

```sql
-- 你的 SQL
SELECT 
    d.name AS department_name,
    COUNT(u.id) AS user_count
FROM 
    itsm_dept d
JOIN 
    itsm_user u ON d.id = u.dept_id
WHERE 
    u.is_deleted = 0 AND u.status = 'active' -- 假设用户表有一个status字段表示用户状态，有效用户为'active'
GROUP BY 
    d.name
ORDER BY 
    user_count DESC;
```

**说明**：
1. **涉及的表和字段**：
   - `itsm_dept` 表：存储部门信息，字段包括 `id`（部门ID）和 `name`（部门名称）。
   - `itsm_user` 表：存储用户信息，字段包括 `id`（用户ID），`dept_id`（部门ID），`is_deleted`（逻辑删除标记），以及 `status`（用户状态）。

2. **SQL 逻辑**：
   - 使用 `JOIN` 将 `itsm_dept` 表和 `itsm_user` 表连接，通过 `dept_id` 和 `id` 字段关联。
   - `WHERE` 条件过滤出未被逻辑删除且状态为 'active' 的有效用户。
   - 使用 `GROUP BY` 按部门名称分组，计算每个部门的有效用户数量。
   - `ORDER BY` 按用户数量降序排列结果。

3. **WHERE 条件和 JOIN 逻辑**：
   - `WHERE` 条件 `u.is_deleted = 0 AND u.status = 'active'` 确保只统计未被逻辑删除且状态为 'active' 的有效用户。
   - `JOIN` 逻辑通过 `d.id = u.dept_id` 将用户表和部门表关联，确保每个用户都与其所属部门匹配。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-UPerm-04（⭐⭐⭐）

**题目**：查询某用户组（组名已知）的所有成员信息（工号、姓名），以及该组的描述。

**检查点**：用户组关联, 成员关联, 用户信息获取

**AI 输出**：

1. **分析涉及的表和字段**

   - `itsm_user_group`：存储用户组信息的表，字段包括`id`（用户组ID）、`name`（用户组名称）、`description`（用户组描述）等。
   - `itsm_user_group_member`：存储用户组与用户之间关系的表，字段包括`user_group_id`（用户组ID）、`user_id`（用户ID）等。
   - `itsm_user`：存储用户信息的表，字段包括`id`（用户ID）、`employee_id`（工号）、`name`（姓名）等。

2. **写出符合规范的 PostgreSQL SQL**

```sql
SELECT 
    u.employee_id, 
    u.name, 
    ug.description
FROM 
    itsm_user_group ug
JOIN 
    itsm_user_group_member ugm ON ug.id = ugm.user_group_id
JOIN 
    itsm_user u ON ugm.user_id = u.id
WHERE 
    ug.name = #{groupName}
    AND ug.is_deleted = 0
    AND u.is_deleted = 0;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

- **WHERE 条件**：
  - `ug.name = #{groupName}`：筛选出特定名称的用户组。
  - `ug.is_deleted = 0` 和 `u.is_deleted = 0`：排除已逻辑删除的用户组和用户。

- **JOIN 逻辑**：
  - 首先，通过`itsm_user_group`表（别名`ug`）和`itsm_user_group_member`表（别名`ugm`）进行内连接（`JOIN`），连接条件是`ug.id = ugm.user_group_id`，即用户组ID匹配，以获取属于特定用户组的用户ID。
  - 然后，将上一步的结果与`itsm_user`表（别名`u`）进行内连接，连接条件是`ugm.user_id = u.id`，即用户ID匹配，以获取用户的详细信息（工号和姓名）。
  - 最终，通过这些连接和筛选条件，查询出特定用户组的所有成员信息（工号和姓名）以及该组的描述。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-UPerm-05（⭐⭐）

**题目**：查询拥有某权限编码的所有角色名称，以及持有这些角色的用户工号。

**检查点**：从权限反查用户, 多层 JOIN

**AI 输出**：

1. **分析涉及的表和字段**

   - `itsm_permission`：存储权限资源信息，关键字段包括`id`（权限ID）和`code`（权限编码）。
   - `itsm_role_permission`：存储角色和权限的关联关系，关键字段包括`role_id`（角色ID）和`permission_id`（权限ID）。
   - `itsm_role`：存储角色信息，关键字段包括`id`（角色ID）和`name`（角色名称）。
   - `itsm_user_role`：存储用户和角色的关联关系，关键字段包括`user_id`（用户ID）和`role_id`（角色ID）。
   - `itsm_user`：存储用户信息，关键字段包括`id`（用户ID）和`employee_number`（用户工号）。

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 查询拥有某权限编码的所有角色名称，以及持有这些角色的用户工号
SELECT 
    r.name AS role_name,
    u.employee_number AS user_employee_number
FROM 
    itsm_permission p
JOIN 
    itsm_role_permission rp ON p.id = rp.permission_id
JOIN 
    itsm_role r ON rp.role_id = r.id
JOIN 
    itsm_user_role ur ON r.id = ur.role_id
JOIN 
    itsm_user u ON ur.user_id = u.id
WHERE 
    p.code = #{permission_code}
    AND u.is_deleted = 0
    AND r.is_deleted = 0;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - `WHERE p.code = #{permission_code}`：筛选出具有特定权限编码的权限记录。
   - `JOIN itsm_role_permission rp ON p.id = rp.permission_id`：将权限表与角色权限关联表连接，通过权限ID匹配。
   - `JOIN itsm_role r ON rp.role_id = r.id`：将角色权限关联表与角色表连接，通过角色ID匹配，获取角色名称。
   - `JOIN itsm_user_role ur ON r.id = ur.role_id`：将角色表与用户角色关联表连接，通过角色ID匹配，获取用户ID。
   - `JOIN itsm_user u ON ur.user_id = u.id`：将用户角色关联表与用户表连接，通过用户ID匹配，获取用户工号。
   - `AND u.is_deleted = 0 AND r.is_deleted = 0`：确保查询结果中不包含已逻辑删除的用户和角色。

这个查询通过多层连接，从权限编码开始，逐步关联到角色和用户，最终获取拥有特定权限编码的所有角色名称以及持有这些角色的用户工号。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

