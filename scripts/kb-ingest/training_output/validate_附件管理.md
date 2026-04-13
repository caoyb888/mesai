# 验证结果：附件管理

## IT-Attach-01（⭐）

**题目**：查询某工单（工单ID已知）的所有附件，显示文件名、文件大小（KB）、上传人工号和上传时间。

**检查点**：按 ref_type 和 ref_id 过滤, 文件大小字段

**AI 输出**：

1. **分析涉及的表和字段**
   - 表：`itsm_attachment`
   - 字段：
     - `file_name`：原始文件名
     - `file_size`：文件大小（字节）
     - `created_by`：上传人ID
     - `created_at`：上传时间
     - `ref_type`：关联业务类型，对于工单是`TICKET`
     - `ref_id`：关联业务ID，即工单ID

2. **写出符合规范的 PostgreSQL SQL**
```sql
SELECT 
    a.file_name,
    (a.file_size / 1024) AS file_size_kb, -- 将字节转换为KB
    a.created_by,
    a.created_at
FROM 
    itsm_attachment a
WHERE 
    a.ref_type = 'TICKET' AND 
    a.ref_id = #{工单ID} AND 
    a.is_deleted = 0;
```

3. **说明 WHERE 条件和 JOIN 逻辑**
   - `WHERE` 条件：
     - `a.ref_type = 'TICKET'`：筛选出与工单（TICKET）相关的附件。
     - `a.ref_id = #{工单ID}`：筛选出与特定工单ID相关的附件。
     - `a.is_deleted = 0`：筛选出未被逻辑删除的附件。
   - `JOIN` 逻辑：此查询没有涉及到多表JOIN，因为所有需要的信息都在`itsm_attachment`表中。我们直接从这个表中选择相关的字段。

**说明**：（简要解释逻辑）
- 此查询针对`itsm_attachment`表，筛选出与特定工单ID相关的附件。
- 通过`ref_type`和`ref_id`字段确保只查询到与指定工单相关的附件。
- 通过`is_deleted`字段过滤掉已经被逻辑删除的附件。
- 将文件大小从字节转换为KB，方便阅读。
- 选择文件名、文件大小（KB）、上传人工号和上传时间作为输出字段。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-Attach-02（⭐⭐）

**题目**：统计各引用类型（工单/知识库文章等）的附件数量和总占用存储空间（MB），按空间降序。

**检查点**：GROUP BY ref_type, SUM 存储大小, 单位换算

**AI 输出**：

1. **分析涉及的表和字段**

   涉及的表是 `itsm_attachment`，字段包括：
   - `ref_type`：关联业务类型，如工单、知识库文章等。
   - `file_size`：文件大小（字节）。
   - `is_deleted`：逻辑删除标记，用于过滤未被删除的记录。

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 统计各引用类型的附件数量和总占用存储空间（MB），按空间降序
SELECT 
    ref_type,
    COUNT(*) AS attachment_count,
    SUM(file_size) / 1024 / 1024 AS total_storage_mb
FROM 
    itsm.itsm_attachment
WHERE 
    is_deleted = 0
GROUP BY 
    ref_type
ORDER BY 
    total_storage_mb DESC;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - **WHERE 条件**：`is_deleted = 0` 用于过滤出未被逻辑删除的附件记录，确保统计的数据是当前有效的附件。
   - **JOIN 逻辑**：本查询只涉及单一表 `itsm_attachment`，无需进行 JOIN 操作。通过聚合函数 `COUNT(*)` 和 `SUM(file_size)` 分别计算每种引用类型的附件数量和总文件大小，然后将文件大小从字节转换为兆字节（MB），以便更直观地表示存储空间占用。最后，通过 `GROUP BY ref_type` 对结果按引用类型进行分组，并使用 `ORDER BY total_storage_mb DESC` 按总存储空间降序排列结果。

**自动评分**：95/100

- 功能正确性：40/40
- 规范合规性：20/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-Attach-03（⭐⭐）

**题目**：查询过去30天内上传的、文件大小超过10MB的附件列表，显示文件名、大小、上传人和所属业务对象类型。

**检查点**：日期过滤, 大小过滤, ref_type

**AI 输出**：

1. **分析涉及的表和字段**

   涉及的表为 `itsm_attachment`，字段包括：
   - `file_name`：原始文件名
   - `file_size`：文件大小（字节）
   - `created_at`：上传时间
   - `created_by`：上传人ID
   - `ref_type`：关联业务类型

2. **写出符合规范的 PostgreSQL SQL**

```sql
SELECT 
    a.file_name,
    a.file_size,
    a.created_by,
    a.ref_type
FROM 
    itsm_attachment a
WHERE 
    a.file_size > 10485760 -- 10MB in bytes
    AND a.created_at > NOW() - INTERVAL '30 days'
    AND a.is_deleted = 0;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

- `a.file_size > 10485760`：这个条件筛选出文件大小超过10MB的附件。10MB等于10485760字节。
- `a.created_at > NOW() - INTERVAL '30 days'`：这个条件筛选出过去30天内上传的附件。`NOW()` 返回当前时间，`INTERVAL '30 days'` 表示30天的时间间隔。
- `a.is_deleted = 0`：这个条件确保查询结果中不包含逻辑删除的记录。

由于查询只涉及 `itsm_attachment` 一个表，所以没有 JOIN 逻辑。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

