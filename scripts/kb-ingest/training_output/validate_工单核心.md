# 验证结果：工单核心

## IT-Ticket-01（⭐）

**题目**：查询今日创建的所有工单，显示工单号、标题、优先级、当前状态和处理人工号，按优先级降序排列。

**检查点**：日期过滤, 字段选择, 排序

**AI 输出**：

1. **分析涉及的表和字段**
   - 表：`itsm_ticket`（工单表）
   - 字段：
     - `id`（工单ID）
     - `title`（工单标题）
     - `priority`（工单优先级）
     - `status`（工单当前状态）
     - `assignee_id`（处理人工号）

2. **写出符合规范的 PostgreSQL SQL**
```sql
-- 你的 SQL
SELECT 
    t.id AS ticket_id,
    t.title AS ticket_title,
    t.priority AS ticket_priority,
    t.status AS ticket_status,
    t.assignee_id AS handler_id
FROM 
    itsm.itsm_ticket t
WHERE 
    t.created_at >= DATE_TRUNC('day', NOW()) AND t.created_at < DATE_TRUNC('day', NOW()) + INTERVAL '1 day'
ORDER BY 
    t.priority DESC;
```

3. **说明 WHERE 条件和 JOIN 逻辑**
   - `WHERE` 条件：
     - `t.created_at >= DATE_TRUNC('day', NOW()) AND t.created_at < DATE_TRUNC('day', NOW()) + INTERVAL '1 day'`：这个条件用于筛选出今日创建的工单。`DATE_TRUNC('day', NOW())` 将当前时间截断到当天的开始，`DATE_TRUNC('day', NOW()) + INTERVAL '1 day'` 则表示第二天的开始，因此这个条件会选择出在今天（00:00:00 到 23:59:59）创建的所有工单。
   - `JOIN` 逻辑：
     - 由于查询只需要从 `itsm_ticket` 表中获取信息，不需要与其他表进行联结，因此没有使用 `JOIN` 语句。所有需要的字段都直接从 `itsm_ticket` 表中选择。

**自动评分**：95/100

- 功能正确性：40/40
- 规范合规性：20/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-Ticket-02（⭐⭐）

**题目**：查询某工单（工单号已知）的完整流转记录，显示每个节点的操作人、操作类型、操作时间和备注，按时间升序。

**检查点**：JOIN flow_log, 按工单号过滤, 时间排序

**AI 输出**：

1. **分析涉及的表和字段**

   涉及到的表有两个：`itsm_ticket` 和 `itsm_ticket_flow_log`。

   - `itsm_ticket` 表：存储工单的基本信息，包括工单ID、创建人等。
     - 字段：`id`（工单ID），`created_by`（创建人ID）。

   - `itsm_ticket_flow_log` 表：存储工单的流转日志，记录每次状态变更的详细信息。
     - 字段：`id`（流转日志ID），`ticket_id`（工单ID），`actor_type`（操作人类型），`actor_id`（操作人ID），`action`（触发动作），`created_at`（创建时间），`comment`（备注）。

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 查询某工单的完整流转记录
SELECT 
    ftfl.id AS flow_log_id,
    ftfl.ticket_id,
    ftu.user_name AS operator_name, -- 假设有一个用户表 itsm_user 存储用户信息，包括 user_id 和 user_name
    ftfl.action AS operation_type,
    ftfl.created_at AS operation_time,
    ftfl.comment AS remark
FROM 
    itsm_ticket_flow_log ftfl
LEFT JOIN 
    itsm_ticket ft 
ON 
    ftfl.ticket_id = ft.id
LEFT JOIN 
    itsm_user ftu 
ON 
    ftfl.actor_id = ftu.id -- 假设操作人ID与用户表的ID对应
WHERE 
    ftfl.ticket_id = #{ticket_id}::BIGINT -- 工单ID参数化
ORDER BY 
    ftfl.created_at ASC; -- 按时间升序
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - `WHERE` 条件：`ftfl.ticket_id = #{ticket_id}::BIGINT`，这个条件用于筛选出特定工单ID的流转记录。这里使用了参数化查询，以防止SQL注入攻击。

   - `JOIN` 逻辑：
     - 第一个 `LEFT JOIN` 是将 `itsm_ticket_flow_log` 表与 `itsm_ticket` 表连接，通过 `ticket_id` 字段关联，以便获取工单的基本信息。
     - 第二个 `LEFT JOIN` 是将 `itsm_ticket_flow_log` 表与 `itsm_user` 表连接，通过 `actor_id` 字段关联，以便获取操作人的用户名。这里假设存在一个用户表 `itsm_user`，存储用户ID和用户名信息。

   - `ORDER BY` 子句：`ftfl.created_at ASC`，按照流转日志的创建时间升序排列，以显示工单的流转记录顺序。

**说明**：这个查询首先通过工单ID筛选出相关的流转记录，然后通过左连接获取操作人的用户名，最后按照时间顺序排列结果。这样的查询可以清晰地展示出工单的完整流转过程，包括每个节点的操作人、操作类型、操作时间和备注。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-Ticket-03（⭐⭐）

**题目**：统计本月各处理人处理的工单数量和平均解决时长（分钟），只统计已关闭工单，按工单数降序。

**检查点**：GROUP BY 处理人, 时间差计算, 状态过滤, 月份过滤

**AI 输出**：

1. **分析涉及的表和字段**

   - **itsm_ticket**：工单表，包含工单的基本信息，如工单状态、创建时间、更新时间、处理人ID等。
     - `id`：工单ID
     - `status`：工单状态
     - `resolved_at`：工单解决时间
     - `closed_at`：工单关闭时间
     - `created_at`：工单创建时间
     - `updated_at`：工单更新时间
     - `assignee_id`：处理人ID

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 统计本月各处理人处理的工单数量和平均解决时长（分钟），只统计已关闭工单，按工单数降序
SELECT 
    t.assignee_id,
    COUNT(t.id) AS ticket_count,
    AVG(DATE_PART('epoch', COALESCE(t.resolved_at, t.closed_at) - t.created_at)) / 60 AS avg_resolution_time_minutes
FROM 
    itsm.itsm_ticket t
WHERE 
    t.status = 'CLOSED' AND
    t.closed_at >= DATE_TRUNC('month', CURRENT_DATE) AND
    t.closed_at < DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'
GROUP BY 
    t.assignee_id
ORDER BY 
    ticket_count DESC;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - **WHERE 条件**：
     - `t.status = 'CLOSED'`：只统计已关闭的工单。
     - `t.closed_at >= DATE_TRUNC('month', CURRENT_DATE) AND t.closed_at < DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'`：筛选本月内关闭的工单。`DATE_TRUNC('month', CURRENT_DATE)` 获取本月的第一天，`DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'` 获取下个月的第一天，确保只统计本月的数据。

   - **JOIN 逻辑**：
     - 由于只需要统计处理人处理的工单数量和平均解决时长，因此直接从 `itsm_ticket` 表中筛选数据，不需要与其他表进行 JOIN 操作。

**说明**：
- 该查询统计了本月各处理人处理的工单数量和平均解决时长（分钟），只统计已关闭的工单。
- 使用 `DATE_TRUNC` 函数来获取本月的第一天和下个月的第一天，确保只统计本月的数据。
- 使用 `COALESCE` 函数来处理工单解决时间可能为空的情况，如果 `resolved_at` 为空，则使用 `closed_at` 作为解决时间。
- 使用 `AVG` 和 `DATE_PART` 函数来计算平均解决时长（分钟），并按工单数降序排列结果。

**自动评分**：95/100

- 功能正确性：40/40
- 规范合规性：20/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-Ticket-04（⭐⭐⭐）

**题目**：查询所有超时未解决的工单（当前时间已超过 due_at 且状态不是已关闭），显示工单号、标题、超时时长（小时）、处理人，按超时时长降序取前10条。

**检查点**：时间比较, 状态排除, 计算超时时长, LIMIT

**AI 输出**：

1. **分析涉及的表和字段**

   涉及的表是 `itsm_ticket`，我们需要以下字段：
   - `id`：工单ID
   - `title`：工单标题
   - `due_at`：工单截止时间
   - `status`：工单状态
   - `assignee_id`：处理人ID

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 超时未解决的工单查询
SELECT
    t.id AS ticket_id,
    t.title AS ticket_title,
    (NOW() - t.due_at) * 24 AS overdue_hours,
    u.name AS handler_name
FROM
    itsm.itsm_ticket t
JOIN
    itsm.itsm_user u ON t.assignee_id = u.id
WHERE
    t.status <> 'CLOSED' AND
    t.due_at < NOW()
ORDER BY
    overdue_hours DESC
LIMIT 10;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

- `WHERE` 条件：
  - `t.status <> 'CLOSED'`：确保工单状态不是已关闭。
  - `t.due_at < NOW()`：确保工单的截止时间已经过去，即当前时间已经超过了工单的截止时间。

- `JOIN` 逻辑：
  - 使用 `JOIN` 将 `itsm_ticket` 表和 `itsm_user` 表连接起来，通过 `assignee_id` 和 `id` 字段匹配，以便获取处理人的名称。

**说明**：
- 我们首先从 `itsm_ticket` 表中选择所有未关闭且已超时的工单。
- 通过计算 `NOW() - t.due_at` 得到超时时长，并乘以 24 转换为小时。
- 使用 `JOIN` 将 `itsm_ticket` 表和 `itsm_user` 表连接，以便获取处理人的名称。
- 最后，按照超时时长降序排序，并限制结果为前 10 条记录。

**自动评分**：95/100

- 功能正确性：40/40
- 规范合规性：20/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-Ticket-05（⭐⭐）

**题目**：查询某工单的所有评论，包括评论人工号、评论内容、是否内部评论、评论时间，按时间升序。

**检查点**：按工单过滤, 包含内部评论字段, 时间排序

**AI 输出**：

1. **分析涉及的表和字段**

   涉及的表是 `itsm_ticket_comment`，字段包括：
   - `id`：评论ID
   - `ticket_id`：工单ID
   - `user_id`：评论人ID
   - `content`：评论内容
   - `is_internal`：是否内部评论（0=公开，1=内部）
   - `created_at`：评论时间

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 你的 SQL
SELECT 
    c.user_id AS 评论人工号,
    c.content AS 评论内容,
    CASE WHEN c.is_internal = 0 THEN '公开' ELSE '内部' END AS 是否内部评论,
    c.created_at AS 评论时间
FROM 
    itsm.itsm_ticket_comment c
WHERE 
    c.ticket_id = #{ticket_id} -- 假设ticket_id是参数化变量
ORDER BY 
    c.created_at ASC;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - **WHERE 条件**：`c.ticket_id = #{ticket_id}` 这个条件用于筛选出特定工单的所有评论。这里使用了参数化查询，以防止SQL注入攻击，并且使查询更加灵活。
   - **JOIN 逻辑**：在这个查询中，没有使用JOIN操作，因为只需要从 `itsm_ticket_comment` 表中获取数据。如果需要获取更多信息，比如评论人的姓名等，可能需要与其他表进行JOIN操作，但根据题目要求，这里只涉及一个表。

**说明**：这个查询直接从 `itsm_ticket_comment` 表中选择所需的字段，并通过 `WHERE` 条件筛选出特定工单的评论。使用 `CASE` 语句将 `is_internal` 字段的值转换为更易读的文本（"公开" 或 "内部"），最后按照 `created_at` 字段升序排列结果，以满足按时间升序的要求。

**自动评分**：95/100

- 功能正确性：40/40
- 规范合规性：20/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

