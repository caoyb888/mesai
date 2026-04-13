# 验证结果：SLA引擎

## IT-SLA-01（⭐⭐）

**题目**：查询所有有效的 SLA 策略，显示策略名称、适用的工单类型、响应时限（分钟）和解决时限（分钟）。

**检查点**：状态过滤, 时限字段

**AI 输出**：

1. **分析涉及的表和字段**
   - 表：`itsm_sla_policy`（SLA策略表）
   - 字段：
     - `id`：策略ID
     - `name`：策略名称
     - `service_time_type`：服务时间类型
     - `response_minutes_low`：低优先级响应时限（分钟）
     - `response_minutes_medium`：中优先级响应时限（分钟）
     - `response_minutes_high`：高优先级响应时限（分钟）
     - `response_minutes_critical`：紧急优先级响应时限（分钟）
     - `resolve_minutes_low`：低优先级解决时限（分钟）
     - `resolve_minutes_medium`：中优先级解决时限（分钟）
     - `resolve_minutes_high`：高优先级解决时限（分钟）
     - `resolve_minutes_critical`：紧急优先级解决时限（分钟）
     - `is_deleted`：逻辑删除标记

2. **写出符合规范的 PostgreSQL SQL**
   ```sql
   SELECT
     p.name AS "策略名称",
     '工单类型' AS "适用的工单类型", -- 假设工单类型为固定值，实际应用中可能需要根据业务逻辑调整
     p.response_minutes_low AS "响应时限（分钟）",
     p.resolve_minutes_low AS "解决时限（分钟）"
   FROM
     itsm.itsm_sla_policy p
   WHERE
     p.is_deleted = 0;
   ```

3. **说明 WHERE 条件和 JOIN 逻辑**
   - **WHERE 条件**：`p.is_deleted = 0` 用于过滤出有效的 SLA 策略，即未被逻辑删除的策略。
   - **JOIN 逻辑**：本查询只涉及一个表 `itsm_sla_policy`，因此不需要进行 JOIN 操作。如果需要根据工单类型进行筛选，可能需要与工单类型表进行 JOIN，但根据题目描述，这里假设工单类型为固定值，因此省略了 JOIN 操作。

**说明**：
- 此查询假设“适用的工单类型”为固定值，实际应用中可能需要根据业务逻辑调整，可能需要与工单类型表进行 JOIN 操作。
- 响应时限和解决时限分别选择了低优先级作为示例，实际应用中可以根据需要选择不同优先级的时限。

**自动评分**：95/100

- 功能正确性：40/40
- 规范合规性：20/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-SLA-02（⭐⭐⭐）

**题目**：统计上月各 SLA 策略的达成情况：策略名称、适用工单总数、响应达标数、解决达标数、响应达标率、解决达标率。

**检查点**：JOIN policy, 月份过滤, 达标率计算, GROUP BY

**AI 输出**：

1. **分析涉及的表和字段**

   - `itsm_sla_policy` 表：存储 SLA 策略信息。
     - `id`：策略ID。
     - `name`：策略名称。
   - `itsm_sla_record` 表：存储 SLA 记录信息。
     - `policy_id`：关联的 SLA 策略ID。
     - `incident_id`：工单ID。
     - `response_time_minutes`：响应时间（分钟）。
     - `resolve_time_minutes`：解决时间（分钟）。
     - `response_achieved`：响应是否达标（0或1）。
     - `resolve_achieved`：解决是否达标（0或1）。

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 统计上月各 SLA 策略的达成情况
SELECT
  sp.name AS "策略名称",
  COUNT(DISTINCT sr.incident_id) AS "适用工单总数",
  SUM(sr.response_achieved) AS "响应达标数",
  SUM(sr.resolve_achieved) AS "解决达标数",
  ROUND(SUM(sr.response_achieved)::NUMERIC / NULLIF(COUNT(DISTINCT sr.incident_id), 0) * 100, 2) AS "响应达标率",
  ROUND(SUM(sr.resolve_achieved)::NUMERIC / NULLIF(COUNT(DISTINCT sr.incident_id), 0) * 100, 2) AS "解决达标率"
FROM
  itsm_sla_policy sp
LEFT JOIN
  itsm_sla_record sr ON sp.id = sr.policy_id
  AND sr.incident_id IS NOT NULL
WHERE
  EXTRACT(MONTH FROM sr.created_at) = EXTRACT(MONTH FROM CURRENT_DATE) - 1
  AND EXTRACT(YEAR FROM sr.created_at) = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP BY
  sp.name
ORDER BY
  "适用工单总数" DESC;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

- **WHERE 条件**：
  - `EXTRACT(MONTH FROM sr.created_at) = EXTRACT(MONTH FROM CURRENT_DATE) - 1`：筛选上个月的数据。
  - `EXTRACT(YEAR FROM sr.created_at) = EXTRACT(YEAR FROM CURRENT_DATE)`：确保是当前年份的数据，避免跨年统计。
  - `sr.incident_id IS NOT NULL`：确保工单ID不为空。

- **JOIN 逻辑**：
  - 使用 `LEFT JOIN` 将 `itsm_sla_policy` 表和 `itsm_sla_record` 表连接，通过 `sp.id = sr.policy_id` 关联。
  - 这样可以确保统计每个 SLA 策略下的所有工单记录。

- **GROUP BY**：
  - 按 `sp.name` 分组，以便为每个策略计算统计数据。

- **ORDER BY**：
  - 按 `"适用工单总数"` 降序排列，以便优先显示工单数量较多的策略。

这个查询统计了上个月每个 SLA 策略的适用工单总数、响应达标数、解决达标数以及响应和解决的达标率。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-SLA-03（⭐⭐）

**题目**：查询今日是否为工作日（考虑节假日表），以及今日的工作开始时间和结束时间。

**检查点**：日期匹配, 工作日判断

**AI 输出**：

1. **分析涉及的表和字段**

   涉及的表是 `itsm_holiday`，需要关注的字段包括：
   - `holiday_date`：节假日日期，用于判断今日是否为节假日。
   - `is_workday`：标识是否为工作日，0表示法定休息日，1表示法定调休工作日。

   由于查询今日的工作开始和结束时间，我们还需要知道工作日的时间段，这通常需要一个服务时间配置表或者字段。但根据题目给出的信息，我们假设服务时间类型为 `5x8` 工作制，即周一至周五，每天8小时。因此，我们假设工作日开始时间为早上9点，结束时间为下午5点。

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 你的 SQL
SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM itsm_holiday WHERE holiday_date = CURRENT_DATE AND is_workday = 0) THEN '否'
        ELSE '是'
    END AS is_workday,
    CASE 
        WHEN EXISTS (SELECT 1 FROM itsm_holiday WHERE holiday_date = CURRENT_DATE AND is_workday = 0) THEN NULL
        ELSE '09:00:00'::TIME
    END AS work_start_time,
    CASE 
        WHEN EXISTS (SELECT 1 FROM itsm_holiday WHERE holiday_date = CURRENT_DATE AND is_workday = 0) THEN NULL
        ELSE '17:00:00'::TIME
    END AS work_end_time;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - `WHERE holiday_date = CURRENT_DATE`：这个条件用于筛选出今日的节假日记录。
   - `AND is_workday = 0`：进一步筛选出今日为休息日的记录。
   - `EXISTS`：使用 `EXISTS` 子查询来检查今日是否存在为休息日的节假日记录。如果存在，则今日不是工作日；如果不存在，则今日是工作日。
   - `CASE` 语句：根据是否存在休息日的节假日记录，返回今日是否为工作日，以及工作开始和结束时间。如果今日为休息日，则工作开始和结束时间返回 `NULL`；如果今日为工作日，则返回预设的 `09:00:00` 和 `17:00:00`。

**说明**：（简要解释逻辑）
这个查询首先检查今日是否为节假日，如果是节假日且为休息日，则今日不是工作日，工作开始和结束时间返回 `NULL`。如果不是休息日的节假日或者今日不是节假日，则今日是工作日，返回预设的工作开始和结束时间。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-SLA-04（⭐⭐⭐）

**题目**：查询当前所有 SLA 即将违约（距 due_at 不足 30 分钟且未关闭）的工单，关联 SLA 记录显示剩余时间（分钟）。

**检查点**：时间窗口计算, 关联 SLA 记录, 状态过滤

**AI 输出**：

1. **分析涉及的表和字段**

   - `itsm_ticket` 表：存储工单信息，包括工单状态、创建时间、预计解决时间（due_at）等字段。
     - `id`：工单ID
     - `status`：工单状态
     - `due_at`：预计解决时间
   - `itsm_sla_record` 表：存储SLA记录信息，包括工单ID、剩余时间等字段。
     - `ticket_id`：工单ID
     - `remaining_time`：剩余时间（分钟）

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 查询当前所有 SLA 即将违约（距 due_at 不足 30 分钟且未关闭）的工单，关联 SLA 记录显示剩余时间（分钟）
SELECT
    t.id,
    t.status,
    t.due_at,
    sr.remaining_time
FROM
    itsm_ticket t
JOIN
    itsm_sla_record sr ON t.id = sr.ticket_id
WHERE
    t.status <> 'closed' -- 工单未关闭
    AND t.due_at - NOW() <= INTERVAL '30 minutes' -- 距 due_at 不足 30 分钟
    AND sr.remaining_time < 30; -- SLA 记录显示剩余时间不足 30 分钟
```

3. **说明 WHERE 条件和 JOIN 逻辑**

- **WHERE 条件**：
  - `t.status <> 'closed'`：筛选工单状态不为“closed”（未关闭）的工单。
  - `t.due_at - NOW() <= INTERVAL '30 minutes'`：筛选预计解决时间（due_at）距当前时间不足30分钟的工单。
  - `sr.remaining_time < 30`：筛选SLA记录中剩余时间不足30分钟的记录。

- **JOIN 逻辑**：
  - 使用 `JOIN` 关联 `itsm_ticket` 表和 `itsm_sla_record` 表，通过工单ID（`t.id = sr.ticket_id`）进行关联，以便同时获取工单信息和SLA记录信息。

这个查询将返回所有即将违约的工单（距due_at不足30分钟且未关闭），并显示它们的剩余时间（分钟）。通过关联两个表，我们可以同时获取工单的详细信息和SLA记录的剩余时间。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-SLA-05（⭐⭐）

**题目**：查询某 SLA 策略下所有响应超时的工单记录，显示工单号、超时时长（分钟）、是否最终解决。

**检查点**：响应超时标志, 关联工单, 超时时长

**AI 输出**：

1. **分析涉及的表和字段**

   - `itsm_sla_record` 表：存储工单的 SLA 记录，包括响应和解决时间等信息。
     - 字段：`id`（主键），`ticket_id`（关联工单ID），`sla_policy_id`（关联SLA策略ID），`response_time`（响应时间），`resolve_time`（解决时间），`created_at`（记录创建时间）。

   - `itsm_ticket` 表：存储工单的基本信息。
     - 字段：`id`（主键），`number`（工单号），`status`（工单状态），`resolved`（是否最终解决）。

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 查询某 SLA 策略下所有响应超时的工单记录
SELECT 
    t.number AS "工单号",
    (COALESCE(r.response_time, EXTRACT(EPOCH FROM (NOW() - t.created_at))) / 60) AS "超时时长（分钟）",
    t.resolved AS "是否最终解决"
FROM 
    itsm_ticket t
LEFT JOIN 
    itsm_sla_record r ON t.id = r.ticket_id
WHERE 
    r.sla_policy_id = #{sla_policy_id} -- 假设通过参数传入SLA策略ID
    AND (r.response_time < t.created_at + INTERVAL '1 minute' * COALESCE(r.response_minutes, 0) OR r.response_time IS NULL)
    AND t.status NOT IN ('Resolved', 'Closed') -- 假设已解决或已关闭的工单不计入超时
ORDER BY 
    t.created_at DESC;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - `LEFT JOIN itsm_sla_record r ON t.id = r.ticket_id`：左连接 `itsm_sla_record` 表和 `itsm_ticket` 表，通过工单ID进行关联，以确保即使某些工单没有SLA记录也能被查询到。

   - `WHERE r.sla_policy_id = #{sla_policy_id}`：筛选出特定SLA策略ID的记录。

   - `AND (r.response_time < t.created_at + INTERVAL '1 minute' * COALESCE(r.response_minutes, 0) OR r.response_time IS NULL)`：检查响应时间是否超时。如果 `response_time` 小于工单创建时间加上响应时限（分钟），或者 `response_time` 为空（表示尚未响应），则认为响应超时。

   - `AND t.status NOT IN ('Resolved', 'Closed')`：排除已经解决或关闭的工单，因为这些工单不计入响应超时。

   - `ORDER BY t.created_at DESC`：按工单创建时间降序排列，最新的工单排在前面。

这个查询将返回所有在指定SLA策略下响应超时的工单记录，包括工单号、超时时长（分钟）和是否最终解决。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

