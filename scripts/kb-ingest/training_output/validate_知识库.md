# 验证结果：知识库

## IT-KB-01（⭐）

**题目**：查询某知识库分类（分类名已知）下所有已发布的文章标题、作者工号和发布时间，按发布时间降序。

**检查点**：JOIN category, 状态过滤（已发布）, 排序

**AI 输出**：

1. **分析涉及的表和字段**
   - `itsm_kb_category` 表：存储知识库分类信息，字段包括 `id`（分类ID），`name`（分类名）。
   - `itsm_kb_article` 表：存储知识库文章信息，字段包括 `id`（文章ID），`category_id`（所属分类ID），`title`（知识标题），`published_at`（发布时间），`published_by`（发布人ID）。

2. **写出符合规范的 PostgreSQL SQL**
```sql
SELECT 
    a.title,
    u.employee_id AS author_id,
    a.published_at
FROM 
    itsm_kb_article a
JOIN 
    itsm_kb_category c ON a.category_id = c.id
JOIN 
    (SELECT employee_id, user_id FROM itsm_user) u ON a.published_by = u.user_id
WHERE 
    c.name = #{category_name} AND a.status = 'Published'
ORDER BY 
    a.published_at DESC;
```
**说明**：
- **WHERE 条件**：`c.name = #{category_name}` 用于筛选指定的知识库分类名；`a.status = 'Published'` 用于筛选已发布的文章。
- **JOIN 逻辑**：
  - `JOIN itsm_kb_category c ON a.category_id = c.id`：将文章表 `itsm_kb_article` 与分类表 `itsm_kb_category` 进行内连接，通过 `category_id` 匹配对应的分类。
  - `JOIN (SELECT employee_id, user_id FROM itsm_user) u ON a.published_by = u.user_id`：通过子查询获取用户表 `itsm_user` 中的 `employee_id` 和 `user_id`，然后与文章表 `itsm_kb_article` 进行内连接，通过 `published_by` 匹配对应的发布人工号。这里假设 `itsm_user` 表中包含员工工号 `employee_id` 和用户ID `user_id`。

这个查询首先筛选出指定分类下所有已发布的文章，然后通过连接用户表获取发布人的工号，并按发布时间降序排列结果。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-KB-02（⭐⭐）

**题目**：查询阅读量最高的 10 篇知识库文章，显示标题、分类名、阅读数、点赞数。

**检查点**：JOIN category, TOP N, 排序字段

**AI 输出**：

1. **分析涉及的表和字段**

   - `itsm_kb_article`：知识条目主表，包含文章的基本信息，如标题、阅读数、点赞数等。
     - `title`：文章标题。
     - `view_count`：阅读数。
     - `useful_count`：点赞数。
     - `category_id`：所属分类ID，用于关联分类表。
   
   - `itsm_kb_category`：知识库分类表，包含分类的名称。
     - `name`：分类名称。

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 查询阅读量最高的 10 篇知识库文章，显示标题、分类名、阅读数、点赞数
SELECT 
    a.title,
    c.name AS category_name,
    a.view_count,
    a.useful_count
FROM 
    itsm_kb_article a
JOIN 
    itsm_kb_category c ON a.category_id = c.id
WHERE 
    a.is_deleted = 0 AND a.status = 'Published'
ORDER BY 
    a.view_count DESC
LIMIT 10;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - `WHERE` 条件：
     - `a.is_deleted = 0`：确保查询的知识库文章没有被逻辑删除。
     - `a.status = 'Published'`：确保查询的知识库文章是已发布状态，即用户可以阅读的文章。
   
   - `JOIN` 逻辑：
     - 使用 `JOIN` 将 `itsm_kb_article` 表和 `itsm_kb_category` 表连接起来，通过 `a.category_id = c.id` 条件关联，这样可以获取每篇文章对应的分类名称。
     - 连接类型为内连接（`INNER JOIN`），只有当两个表中都有匹配的行时才会返回结果，确保每篇文章都能正确显示其分类名称。

**说明**：（简要解释逻辑）
该查询首先通过内连接将知识库文章表和分类表关联起来，然后通过 `WHERE` 条件过滤出未被删除且已发布的文章。接着，按照阅读数降序排序，并限制结果数量为前10篇，以获取阅读量最高的10篇文章。最后，选择需要显示的字段：标题、分类名、阅读数和点赞数。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-KB-03（⭐⭐）

**题目**：查询某篇文章（文章ID已知）的所有历史版本，显示版本号、变更摘要、创建人和创建时间。

**检查点**：按文章ID过滤, 版本排序

**AI 输出**：

1. **分析涉及的表和字段**

   涉及的表为 `itsm_kb_article_version`，需要查询的字段包括：
   - `version`：版本号
   - `change_note`：变更摘要
   - `created_at`：创建时间
   - `created_by`：创建人

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 查询某篇文章的所有历史版本
SELECT 
    a.id AS article_id,
    v.version,
    v.change_note,
    v.created_at,
    v.created_by
FROM 
    itsm.itsm_kb_article_version v
WHERE 
    v.article_id = #{article_id} -- 文章ID参数化
ORDER BY 
    v.version DESC; -- 按版本号降序排列
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - **WHERE 条件**：`v.article_id = #{article_id}` 这个条件用于筛选出特定文章的所有历史版本。这里使用参数化查询，以防止SQL注入攻击，并确保查询的灵活性。
   - **JOIN 逻辑**：在这个查询中，我们没有使用 JOIN，因为只涉及到一个表 `itsm_kb_article_version`。我们直接从这个表中选择所需的字段，并通过 `WHERE` 子句过滤出特定文章的版本记录。

**说明**：这个查询直接从 `itsm_kb_article_version` 表中选择文章的所有版本信息，包括版本号、变更摘要、创建时间和创建人。通过指定 `article_id` 参数，我们可以灵活地查询任何文章的历史版本。查询结果按版本号降序排列，以便最新版本显示在最前面。

**自动评分**：95/100

- 功能正确性：40/40
- 规范合规性：20/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-KB-04（⭐⭐）

**题目**：统计各知识库分类的文章数量，只统计已发布文章，按数量降序。

**检查点**：GROUP BY category, 状态过滤, COUNT

**AI 输出**：

1. **分析涉及的表和字段**

   - `itsm_kb_article`：知识条目主表，包含文章的生命周期状态、分类ID等字段。
     - `status`：生命周期状态字段，用于筛选已发布的文章。
     - `category_id`：所属分类ID，用于与分类表进行关联。
   - `itsm_kb_category`：知识库分类表，包含分类的详细信息。
     - `id`：分类ID，用于与文章表进行关联。

2. **写出符合规范的 PostgreSQL SQL**

```sql
SELECT 
    c.id AS category_id,
    c.name AS category_name,
    COUNT(a.id) AS article_count
FROM 
    itsm.itsm_kb_article a
JOIN 
    itsm.itsm_kb_category c ON a.category_id = c.id
WHERE 
    a.status = 'Published'
    AND a.is_deleted = 0
GROUP BY 
    c.id, c.name
ORDER BY 
    article_count DESC;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - **WHERE 条件**：
     - `a.status = 'Published'`：筛选出状态为已发布的知识库文章。
     - `a.is_deleted = 0`：确保筛选的文章没有被逻辑删除。
   - **JOIN 逻辑**：
     - 使用内连接（INNER JOIN）将 `itsm_kb_article` 表与 `itsm_kb_category` 表连接起来，通过 `a.category_id = c.id` 条件关联，这样可以获取每个分类下的文章数量。
   - **GROUP BY**：
     - 按照分类ID和分类名称进行分组，以确保每个分类的文章数量被正确统计。
   - **ORDER BY**：
     - 按照文章数量降序排列，以便于查看文章数量最多的分类。

**自动评分**：95/100

- 功能正确性：40/40
- 规范合规性：20/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-KB-05（⭐⭐⭐）

**题目**：查询本月新增或更新过的知识库文章，显示标题、操作类型（新增/更新）、操作人和操作时间。

**检查点**：月份过滤, created_at vs updated_at 区分, 操作类型判断

**AI 输出**：

1. **分析涉及的表和字段**

   涉及的表是`itsm_kb_article`，需要关注的字段包括：
   - `id`：知识库文章的唯一标识。
   - `title`：知识库文章的标题。
   - `created_at`：知识库文章的创建时间。
   - `updated_at`：知识库文章的更新时间。
   - `created_by`：创建人ID。
   - `is_deleted`：逻辑删除标记，用于确保不包括已删除的文章。

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 查询本月新增或更新过的知识库文章
SELECT 
    a.title AS "标题",
    CASE 
        WHEN a.created_at >= date_trunc('month', CURRENT_DATE) AND a.updated_at >= date_trunc('month', CURRENT_DATE) THEN '新增'
        WHEN a.updated_at >= date_trunc('month', CURRENT_DATE) THEN '更新'
    END AS "操作类型",
    u.name AS "操作人",
    a.updated_at AS "操作时间"
FROM 
    itsm_kb_article a
JOIN 
    itsm_user u ON a.created_by = u.id
WHERE 
    a.is_deleted = 0
    AND (a.created_at >= date_trunc('month', CURRENT_DATE) OR a.updated_at >= date_trunc('month', CURRENT_DATE))
ORDER BY 
    a.updated_at DESC;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

- **WHERE 条件**：
  - `a.is_deleted = 0`：确保查询的知识库文章没有被逻辑删除。
  - `a.created_at >= date_trunc('month', CURRENT_DATE) OR a.updated_at >= date_trunc('month', CURRENT_DATE)`：确保文章是在本月创建或更新的。这里使用`date_trunc('month', CURRENT_DATE)`来获取本月的第一天，然后检查`created_at`和`updated_at`字段是否在这个时间之后。

- **JOIN 逻辑**：
  - 使用`JOIN`将`itsm_kb_article`表与`itsm_user`表连接起来，通过`created_by`字段将文章的创建人ID与用户表的ID匹配，以便获取操作人的名称。这里假设`itsm_user`表有一个`name`字段存储用户名称。

这个查询将返回本月新增或更新的知识库文章的标题、操作类型（新增/更新）、操作人和操作时间。通过`CASE`语句区分是新增还是更新操作，并使用`ORDER BY`对结果进行排序，以确保最新的操作显示在最前面。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

