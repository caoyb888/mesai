# 验证结果：运维日历与排班

## IT-Cal-01（⭐）

**题目**：查询本月所有节假日记录，显示日期、假期名称和假期类型。

**检查点**：月份过滤, 事件类型区分

**AI 输出**：

1. **分析涉及的表和字段**
   - 表：`itsm_calendar_event`
   - 字段：
     - `id`：事件ID
     - `title`：事件标题（假期名称）
     - `event_type`：事件类型（假期类型）
     - `start_time`：事件开始时间（日期）

2. **写出符合规范的 PostgreSQL SQL**
```sql
SELECT
    date_trunc('day', start_time) AS event_date,
    title AS holiday_name,
    event_type AS holiday_type
FROM
    itsm.calendar_event
WHERE
    event_type = 'HOLIDAY' -- 假设HOLIDAY是节假日的事件类型
    AND start_time >= current_date
    AND start_time < current_date + interval '1 month' -- 查询本月的记录
    AND is_deleted = 0; -- 确保查询未被逻辑删除的记录
```

3. **说明 WHERE 条件和 JOIN 逻辑**
   - `event_type = 'HOLIDAY'`：筛选出事件类型为节假日的记录。
   - `start_time >= current_date AND start_time < current_date + interval '1 month'`：筛选出开始时间在本月内的记录。
   - `is_deleted = 0`：确保查询的记录没有被逻辑删除。
   - 由于查询只涉及一个表，所以没有 JOIN 逻辑。

**说明**：
- 此查询专注于从`itsm_calendar_event`表中提取本月所有节假日的记录。
- 使用`date_trunc('day', start_time)`来获取`start_time`字段的日期部分，确保日期的精确度。
- 通过`event_type`字段筛选出节假日类型的事件。
- 通过`current_date`和`interval '1 month'`来限定查询范围为本月。
- 最后，通过`is_deleted`字段确保查询结果中不包含被逻辑删除的记录。

**自动评分**：95/100

- 功能正确性：40/40
- 规范合规性：20/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-Cal-02（⭐⭐）

**题目**：查询本周负责值班的团队成员信息，显示团队名称、成员工号和值班日期段。

**检查点**：日期范围过滤, JOIN 成员, JOIN 排班

**AI 输出**：

1. **分析涉及的表和字段**

   - `itsm_roster_team`：值班团队表，包含团队名称和团队ID。
     - 字段：`id`（团队ID），`name`（团队名称）。

   - `itsm_roster_team_member`：值班团队成员表，定义团队成员及轮班顺序。
     - 字段：`id`（成员ID），`team_id`（团队ID），`user_id`（成员工号）。

   - `itsm_roster_schedule`：排班记录表，记录工单分配时查询当日值班人作为默认处理人。
     - 字段：`id`（排班ID），`team_id`（团队ID），`user_id`（值班人ID），`schedule_date`（值班日期），`start_time`（班次开始时间），`end_time`（班次结束时间）。

2. **写出符合规范的 PostgreSQL SQL**

```sql
SELECT
  rt.name AS team_name,
  rtm.user_id AS employee_id,
  rs.schedule_date AS duty_date,
  rs.start_time AS start_time,
  rs.end_time AS end_time
FROM
  itsm_roster_schedule rs
JOIN
  itsm_roster_team_member rtm ON rs.team_id = rtm.team_id AND rs.user_id = rtm.user_id
JOIN
  itsm_roster_team rt ON rtm.team_id = rt.id
WHERE
  rs.schedule_date >= CURRENT_DATE - INTERVAL '6 days' AND
  rs.schedule_date < CURRENT_DATE + INTERVAL '1 day' AND
  rs.is_deleted = 0 AND
  rtm.is_deleted = 0;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

- **WHERE 条件**：
  - `rs.schedule_date >= CURRENT_DATE - INTERVAL '6 days' AND rs.schedule_date < CURRENT_DATE + INTERVAL '1 day'`：查询本周的值班记录，即从本周一开始到本周日结束（假设今天是周日）。
  - `rs.is_deleted = 0 AND rtm.is_deleted = 0`：排除已删除的排班记录和团队成员记录。

- **JOIN 逻辑**：
  - `JOIN itsm_roster_team_member rtm ON rs.team_id = rtm.team_id AND rs.user_id = rtm.user_id`：通过团队ID和值班人ID将排班记录表与值班团队成员表关联，以获取值班人的详细信息。
  - `JOIN itsm_roster_team rt ON rtm.team_id = rt.id`：通过团队ID将值班团队成员表与值班团队表关联，以获取团队名称。

**说明**：
- 该查询首先通过内连接（JOIN）将排班记录表、值班团队成员表和值班团队表关联起来，以获取本周负责值班的团队成员信息。
- 通过WHERE条件筛选出本周的值班记录，并排除已删除的记录。
- 最后，选择需要显示的字段，包括团队名称、成员工号、值班日期段等。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-Cal-03（⭐⭐）

**题目**：查询某运维团队（团队名已知）本月的排班情况，显示每个排班周期的开始、结束时间和值班人员工号。

**检查点**：按团队过滤, 月份过滤, 时间字段

**AI 输出**：

1. **分析涉及的表和字段**

   - `itsm_roster_team`：存储团队信息的表，我们需要通过团队名来查询团队ID。
     - 字段：`name`（团队名），`id`（团队ID）。

   - `itsm_roster_schedule`：存储排班信息的表，我们需要查询本月的排班情况。
     - 字段：`team_id`（团队ID），`schedule_date`（值班日期），`user_id`（值班人ID），`start_time`（班次开始时间），`end_time`（班次结束时间）。

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 查询某运维团队本月的排班情况
SELECT
    rs.schedule_date,
    rs.start_time,
    rt.name AS team_name,
    u.user_id
FROM
    itsm_roster_schedule rs
JOIN
    itsm_roster_team rt ON rs.team_id = rt.id
JOIN
    itsm_user u ON rs.user_id = u.id
WHERE
    rt.name = #{team_name} -- 团队名参数化
    AND EXTRACT(MONTH FROM rs.schedule_date) = EXTRACT(MONTH FROM CURRENT_DATE)
    AND EXTRACT(YEAR FROM rs.schedule_date) = EXTRACT(YEAR FROM CURRENT_DATE)
ORDER BY
    rs.schedule_date;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - `WHERE` 条件：
     - `rt.name = #{team_name}`：根据团队名过滤团队，这里使用参数化查询以防止SQL注入。
     - `EXTRACT(MONTH FROM rs.schedule_date) = EXTRACT(MONTH FROM CURRENT_DATE)` 和 `EXTRACT(YEAR FROM rs.schedule_date) = EXTRACT(YEAR FROM CURRENT_DATE)`：这两个条件用于过滤出当前月份的排班记录。

   - `JOIN` 逻辑：
     - `JOIN itsm_roster_team rt ON rs.team_id = rt.id`：通过`team_id`将排班表和团队表连接起来，以便能够根据团队ID查询到团队名。
     - `JOIN itsm_user u ON rs.user_id = u.id`：通过`user_id`将排班表和用户表连接起来，以便能够查询到值班人的工号。

**说明**：（简要解释逻辑）
这个查询首先通过团队名来确定需要查询的团队ID，然后查询该团队在当前月份的所有排班记录。通过连接团队表和用户表，我们能够获取到每个排班周期的开始、结束时间和值班人的工号。最后，结果按照排班日期排序，以便于查看。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-Cal-04（⭐⭐）

**题目**：统计各运维团队的成员人数，显示团队名称、成员数量，按成员数降序。

**检查点**：GROUP BY, COUNT, JOIN

**AI 输出**：

1. **分析涉及的表和字段**

   - `itsm_roster_team`：存储运维团队的信息。
     - 字段：`id`（团队ID），`name`（团队名称）。

   - `itsm_roster_team_member`：存储团队成员的信息。
     - 字段：`team_id`（团队ID），`user_id`（成员ID）。

2. **写出符合规范的 PostgreSQL SQL**

```sql
SELECT rt.name AS team_name, COUNT(rtm.user_id) AS member_count
FROM itsm_roster_team rt
LEFT JOIN itsm_roster_team_member rtm ON rt.id = rtm.team_id
GROUP BY rt.name
ORDER BY member_count DESC;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

- **JOIN 逻辑**：使用 `LEFT JOIN` 将 `itsm_roster_team` 表和 `itsm_roster_team_member` 表连接起来。连接条件是两个表中的 `team_id` 字段相等，即 `rt.id = rtm.team_id`。这样，我们可以获取每个团队及其成员的信息。

- **WHERE 条件**：在这个查询中，我们没有使用 `WHERE` 子句来过滤特定的记录，因为我们想要统计所有团队的成员数量。

- **GROUP BY**：使用 `GROUP BY rt.name` 将结果按团队名称分组，这样我们可以为每个团队计算成员数量。

- **ORDER BY**：使用 `ORDER BY member_count DESC` 将结果按成员数量降序排列，这样成员数量最多的团队会排在最前面。

**说明**：这个查询首先通过左连接将团队和成员信息关联起来，然后按团队名称分组并计算每个团队的成员数量，最后按成员数量降序排列结果。这样，我们可以得到每个团队的名称和成员数量，并且按成员数量从多到少排序。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-Cal-05（⭐⭐⭐）

**题目**：查询下周有排班且同时在假期表中有节假日记录的日期，这些日期可能需要调整排班。

**检查点**：日期交叉查询, 下周日期范围, 节假日匹配

**AI 输出**：

1. **分析涉及的表和字段**

   - `itsm_roster_schedule` 表：存储排班记录，关键字段包括 `schedule_date`（值班日期）。
   - `itsm_calendar_event` 表：存储运维日历事件，关键字段包括 `start_time` 和 `end_time`（事件的开始和结束时间），以及 `event_type`（事件类型，例如节假日）。

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 查询下周有排班且同时在假期表中有节假日记录的日期
SELECT DISTINCT rs.schedule_date
FROM itsm_roster_schedule rs
JOIN itsm_calendar_event ce ON rs.schedule_date >= ce.start_time AND rs.schedule_date <= ce.end_time
WHERE rs.schedule_date >= CURRENT_DATE + INTERVAL '7 days' AND rs.schedule_date < CURRENT_DATE + INTERVAL '14 days'
AND ce.event_type = 'HOLIDAY';
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - `WHERE` 条件：
     - `rs.schedule_date >= CURRENT_DATE + INTERVAL '7 days' AND rs.schedule_date < CURRENT_DATE + INTERVAL '14 days'`：筛选下周的日期，即从今天开始的下一周。
     - `ce.event_type = 'HOLIDAY'`：筛选出事件类型为节假日的记录。
   
   - `JOIN` 逻辑：
     - 使用 `JOIN` 将 `itsm_roster_schedule` 表和 `itsm_calendar_event` 表连接起来，条件是排班日期 `rs.schedule_date` 落在假期事件的开始时间 `ce.start_time` 和结束时间 `ce.end_time` 之间。这意味着如果一个日期在排班表中有记录，并且在假期表中也有对应的节假日事件，那么这个日期就会被选中。

**说明**：（简要解释逻辑）
这个查询的目的是找出下周内，哪些日期既有排班记录，又被标记为节假日。这对于需要调整排班的情况非常有用，因为节假日可能需要特别的排班安排。通过筛选出这些日期，我们可以进一步决定是否需要调整这些日期的排班计划。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

