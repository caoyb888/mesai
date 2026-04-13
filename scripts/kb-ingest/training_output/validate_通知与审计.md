# 验证结果：通知与审计

## IT-Notify-01（⭐）

**题目**：查询所有启用的通知渠道，显示渠道名称、渠道类型（邮件/短信/企业微信等）和创建时间。

**检查点**：状态过滤, 渠道类型字段

**AI 输出**：

1. **分析涉及的表和字段**
   - 表：`itsm_notify_channel`
   - 字段：
     - `id`：主键
     - `channel_type`：渠道类型（EMAIL邮件 SMS短信 LARK飞书 DINGDING钉钉）
     - `name`：渠道显示名
     - `is_enabled`：强管控开关：0禁用 1启用
     - `created_at`：创建时间（假设存在此字段，因为题目中没有提到，但通常这类表会有创建时间字段）

2. **写出符合规范的 PostgreSQL SQL**
   ```sql
   SELECT
     nc.name AS channel_name,
     nc.channel_type AS channel_type,
     nc.created_at AS created_at
   FROM
     itsm.notify_channel nc
   WHERE
     nc.is_enabled = 1;
   ```

3. **说明 WHERE 条件和 JOIN 逻辑**
   - **WHERE 条件**：`nc.is_enabled = 1`，这个条件用于筛选出所有启用的通知渠道。因为题目要求查询所有启用的渠道，所以我们只选择`is_enabled`字段值为1的记录。
   - **JOIN 逻辑**：在这个查询中，我们没有使用JOIN，因为只涉及到一个表`itsm_notify_channel`。我们直接从这个表中选择需要的字段，即渠道名称、渠道类型和创建时间。

**说明**：
- 这个查询直接从`itsm_notify_channel`表中选择所有启用的（`is_enabled = 1`）通知渠道，显示其名称、类型和创建时间。
- 由于题目中没有提到具体的创建时间字段，我假设存在一个`created_at`字段。如果实际表结构中使用的是不同的字段名，需要相应地替换。

**自动评分**：95/100

- 功能正确性：40/40
- 规范合规性：20/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-Notify-02（⭐⭐）

**题目**：统计近7天各通知渠道的发送成功数和失败数，计算成功率，按成功率升序排列。

**检查点**：日期过滤, GROUP BY, 成功/失败状态, 成功率计算

**AI 输出**：

1. **分析涉及的表和字段**

   - `itsm_notify_log`：存储通知发送的日志信息，包括发送结果和相关渠道信息。
     - `channel_id`：通知渠道ID，关联`itsm_notify_channel`表。
     - `result`：发送结果，值为`SUCCESS`或`FAIL`。
     - `sent_at`：发送时间。
   
   - `itsm_notify_channel`：存储通知渠道的配置信息。
     - `id`：渠道ID，作为外键关联`itsm_notify_log`表。
     - `channel_type`：渠道类型，如`EMAIL`、`SMS`等。

2. **写出符合规范的 PostgreSQL SQL**

```sql
SELECT 
    nc.channel_type,
    COUNT(CASE WHEN nl.result = 'SUCCESS' THEN 1 END) AS success_count,
    COUNT(CASE WHEN nl.result = 'FAIL' THEN 1 END) AS fail_count,
    CASE 
        WHEN COUNT(nl.id) = 0 THEN 0
        ELSE CAST(COUNT(CASE WHEN nl.result = 'SUCCESS' THEN 1 END) * 100 AS FLOAT) / COUNT(nl.id)
    END AS success_rate
FROM 
    itsm_notify_log nl
JOIN 
    itsm_notify_channel nc ON nl.channel_id = nc.id
WHERE 
    nl.sent_at >= NOW() - INTERVAL '7 days'
GROUP BY 
    nc.channel_type
ORDER BY 
    success_rate ASC;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - **WHERE 条件**：`nl.sent_at >= NOW() - INTERVAL '7 days'` 用于筛选出近7天内发送的通知日志记录。
   
   - **JOIN 逻辑**：通过`JOIN itsm_notify_channel nc ON nl.channel_id = nc.id`将`itsm_notify_log`表和`itsm_notify_channel`表进行连接，以获取每个通知渠道的类型信息。这样，我们可以在结果中显示每个渠道的类型，并根据渠道类型进行分组和排序。

**说明**：（简要解释逻辑）
- 首先，我们通过`JOIN`操作将通知日志表和通知渠道表连接起来，以便能够访问每个通知日志条目的渠道类型。
- 然后，我们使用`WHERE`子句来限制查询的时间范围，只考虑近7天内的日志。
- 使用`GROUP BY`对渠道类型进行分组，以便我们可以为每种渠道类型计算成功和失败的数量。
- 通过`COUNT`函数和`CASE`语句，我们分别计算每种渠道类型的成功数和失败数。
- 计算成功率时，我们使用`CAST`将成功数除以总条目数，并乘以100得到百分比。
- 最后，我们使用`ORDER BY`对结果按照成功率进行升序排列。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-Notify-03（⭐⭐）

**题目**：查询某用户（工号已知）今日的所有操作审计日志，显示操作时间、操作类型、资源类型和变更内容摘要。

**检查点**：按用户过滤, 日期过滤, 字段选择

**AI 输出**：

1. **分析涉及的表和字段**
   - 表：`itsm_audit_log`
   - 字段：
     - `operated_at`：操作时间
     - `action`：操作类型
     - `resource_type`：资源类型
     - `before_json`：变更前数据快照（JSON）
     - `after_json`：变更后数据快照（JSON）

2. **写出符合规范的 PostgreSQL SQL**
```sql
-- 查询某用户今日的所有操作审计日志
SELECT 
    a.operated_at AS "操作时间",
    a.action AS "操作类型",
    a.resource_type AS "资源类型",
    a.before_json AS "变更前数据",
    a.after_json AS "变更后数据"
FROM 
    itsm.itsm_audit_log a
WHERE 
    a.account_no = #{account_no} -- 工号参数化
    AND a.operated_at >= DATE_TRUNC('day', NOW()) -- 今日时间
    AND a.operated_at < DATE_TRUNC('day', NOW()) + INTERVAL '1 day' -- 今日时间
ORDER BY 
    a.operated_at DESC; -- 按操作时间降序排列
```

3. **说明 WHERE 条件和 JOIN 逻辑**
   - `WHERE` 条件：
     - `a.account_no = #{account_no}`：根据提供的工号筛选对应的操作日志。
     - `a.operated_at >= DATE_TRUNC('day', NOW())`：筛选出今日开始时间（00:00:00）之后的操作日志。
     - `a.operated_at < DATE_TRUNC('day', NOW()) + INTERVAL '1 day'`：筛选出今日结束时间（23:59:59）之前的操作日志。
   - `JOIN` 逻辑：由于查询只涉及单表`itsm_audit_log`，无需进行表连接。

**说明**：
- 该查询针对特定用户（工号已知）今日的所有操作审计日志进行筛选，显示操作时间、操作类型、资源类型和变更内容摘要。
- 使用参数化查询（`#{account_no}`）确保SQL注入安全。
- 使用`DATE_TRUNC`函数精确到天筛选今日的操作日志。
- 按操作时间降序排列，方便查看最新的操作记录。

**自动评分**：95/100

- 功能正确性：40/40
- 规范合规性：20/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-Notify-04（⭐⭐⭐）

**题目**：查询近30天内最频繁触发的审计操作（操作类型+资源类型组合），取前10名，显示组合描述和触发次数。

**检查点**：时间范围, 多字段 GROUP BY, COUNT DESC, LIMIT

**AI 输出**：

1. **分析涉及的表和字段**

   涉及的表是 `itsm_audit_log`，需要关注的字段包括：
   - `action`：操作动作，如CREATE/UPDATE/DELETE/LOGIN等。
   - `resource_type`：操作资源类型，如TICKET/USER/KB_ARTICLE等。
   - `operated_at`：操作时间，用于筛选近30天内的数据。

2. **写出符合规范的 PostgreSQL SQL**

```sql
SELECT 
    CONCAT(action, '+', resource_type) AS operation_combination,
    COUNT(*) AS trigger_count
FROM 
    itsm.itsm_audit_log
WHERE 
    operated_at >= CURRENT_TIMESTAMP - INTERVAL '30 days'
GROUP BY 
    operation_combination
ORDER BY 
    trigger_count DESC
LIMIT 10;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - **WHERE 条件**：`operated_at >= CURRENT_TIMESTAMP - INTERVAL '30 days'` 用于筛选出近30天内的记录。`CURRENT_TIMESTAMP` 是 PostgreSQL 中的当前时间戳函数，`INTERVAL '30 days'` 表示30天的时间间隔，通过减去这个时间间隔，我们可以得到30天前的日期，从而筛选出近30天内的记录。
   
   - **JOIN 逻辑**：本查询中没有使用 JOIN，因为所需的所有信息都存储在 `itsm_audit_log` 表中，无需与其他表进行连接。

**说明**：
这个查询首先从 `itsm_audit_log` 表中选择所有近30天内的记录。然后，使用 `CONCAT` 函数将 `action` 和 `resource_type` 字段组合成一个描述（例如 "CREATE+TICKET"）。接着，通过 `GROUP BY` 对这些组合进行分组，并使用 `COUNT(*)` 计算每个组合的出现次数。最后，通过 `ORDER BY` 对触发次数进行降序排序，并使用 `LIMIT 10` 限制结果只显示前10条记录。

**自动评分**：95/100

- 功能正确性：40/40
- 规范合规性：20/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-Notify-05（⭐⭐）

**题目**：查询发送失败次数最多的 5 个通知渠道，显示渠道名称、总发送次数和失败次数。

**检查点**：JOIN channel, GROUP BY, 失败过滤, TOP N

**AI 输出**：

1. **分析涉及的表和字段**

   - 表 `itsm_notify_log`：记录了通知发送的日志，包括发送状态、发送次数等信息。
     - 字段 `channel_id`：通知渠道ID，关联 `itsm_notify_channel` 表。
     - 字段 `send_status`：发送状态，区分成功或失败。
     - 字段 `send_count`：该通知尝试发送的次数。
     - 字段 `fail_count`：该通知失败的次数。
   
   - 表 `itsm_notify_channel`：记录了通知渠道的配置信息。
     - 字段 `id`：渠道ID，作为外键与 `itsm_notify_log` 表关联。
     - 字段 `name`：渠道名称。

2. **写出符合规范的 PostgreSQL SQL**

```sql
SELECT 
    nc.name AS channel_name,
    SUM(nl.send_count) AS total_send_count,
    SUM(nl.fail_count) AS total_fail_count
FROM 
    itsm_notify_log nl
JOIN 
    itsm_notify_channel nc ON nl.channel_id = nc.id
WHERE 
    nl.send_status = 'FAIL'
GROUP BY 
    nc.name
ORDER BY 
    total_fail_count DESC
LIMIT 5;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

- **WHERE 条件**：`nl.send_status = 'FAIL'` 这个条件用于筛选出所有发送失败的通知日志记录。因为我们需要查询的是失败次数最多的通知渠道，所以只关注发送状态为失败的记录。

- **JOIN 逻辑**：通过 `JOIN` 将 `itsm_notify_log` 表和 `itsm_notify_channel` 表连接起来，连接条件是 `nl.channel_id = nc.id`。这样，我们可以将每个通知日志记录与其对应的渠道名称关联起来，从而能够按渠道名称分组和统计。

- **GROUP BY**：使用 `GROUP BY nc.name` 将结果按渠道名称分组，以便对每个渠道的发送次数和失败次数进行聚合计算。

- **ORDER BY**：通过 `ORDER BY total_fail_count DESC` 对结果按失败次数降序排序，确保失败次数最多的渠道排在前面。

- **LIMIT**：使用 `LIMIT 5` 限制结果只显示前5个渠道，即失败次数最多的5个通知渠道。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

