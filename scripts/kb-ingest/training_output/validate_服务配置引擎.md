# 验证结果：服务配置引擎

## IT-SVC-01（⭐）

**题目**：查询所有启用的服务目录，显示服务名称、描述和图标，按排序号升序。

**检查点**：状态过滤, 排序字段

**AI 输出**：

1. **分析涉及的表和字段**

   涉及的表是 `itsm_service_catalog`，需要查询的字段包括：
   - `name`：服务目录名称
   - `description`：服务目录描述（虽然题目中没有提到描述字段，但根据业务场景，假设存在该字段）
   - `icon_url`：服务目录图标路径
   - `sort_order`：服务目录排序号

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 你的 SQL
SELECT
  c.name,
  c.description,
  c.icon_url,
  c.sort_order
FROM
  itsm_service_catalog c
WHERE
  c.is_deleted = 0
ORDER BY
  c.sort_order ASC;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - **WHERE 条件**：`c.is_deleted = 0` 用于筛选出启用的服务目录。因为 `is_deleted` 字段用于标记逻辑删除，值为0表示记录未被删除，即服务目录处于启用状态。
   - **JOIN 逻辑**：本查询只涉及单个表 `itsm_service_catalog`，无需进行 JOIN 操作。直接从该表中筛选出符合条件的记录即可。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-SVC-02（⭐⭐）

**题目**：查询某服务目录下所有有效的服务模型，显示模型名称、关联的工作流定义名称和表单字段数量。

**检查点**：JOIN workflow, 子查询统计字段数, 状态过滤

**AI 输出**：

1. **分析涉及的表和字段**

   - `itsm_service_model`：服务模型表，包含服务模型的基本信息。
     - 字段：`id`（服务模型ID），`name`（服务模型名称）。
   - `itsm_workflow_def`：工作流定义表，包含工作流的基本信息。
     - 字段：`id`（工作流定义ID），`name`（工作流定义名称）。
   - `itsm_form_field`：动态表单字段定义表，包含服务模型的表单字段信息。
     - 字段：`model_id`（所属服务模型ID），`field_key`（字段唯一键）。

2. **写出符合规范的 PostgreSQL SQL**

```sql
SELECT 
    sm.name AS "服务模型名称",
    wd.name AS "工作流定义名称",
    COUNT(ff.field_key) AS "表单字段数量"
FROM 
    itsm_service_model sm
JOIN 
    itsm_workflow_def wd ON sm.workflow_def_id = wd.id
LEFT JOIN 
    itsm_form_field ff ON sm.id = ff.model_id
WHERE 
    sm.is_deleted = 0 AND wd.is_deleted = 0 AND ff.is_deleted = 0
GROUP BY 
    sm.name, wd.name
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - `WHERE` 条件：
     - `sm.is_deleted = 0`：确保查询的服务模型是有效的，即没有被逻辑删除。
     - `wd.is_deleted = 0`：确保查询的工作流定义是有效的，即没有被逻辑删除。
     - `ff.is_deleted = 0`：确保查询的表单字段是有效的，即没有被逻辑删除。
   - `JOIN` 逻辑：
     - `JOIN itsm_workflow_def wd ON sm.workflow_def_id = wd.id`：通过服务模型表的`workflow_def_id`字段与工作流定义表的`id`字段进行内连接，以获取每个服务模型关联的工作流定义名称。
     - `LEFT JOIN itsm_form_field ff ON sm.id = ff.model_id`：通过服务模型表的`id`字段与表单字段定义表的`model_id`字段进行左连接，以统计每个服务模型的表单字段数量。左连接确保即使某些服务模型没有表单字段，也能在结果中显示，表单字段数量为0。

**说明**：
- 该查询旨在查询某服务目录下所有有效的服务模型，并显示模型名称、关联的工作流定义名称和表单字段数量。
- 通过内连接和左连接，实现了对服务模型、工作流定义和表单字段的有效关联和统计。
- `GROUP BY` 子句用于对结果进行分组，确保每个服务模型和工作流定义的组合只出现一次，并计算相应的表单字段数量。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-SVC-03（⭐⭐）

**题目**：查询某服务模型（模型ID已知）的所有表单字段，按字段顺序排列，显示字段名、字段类型、是否必填。

**检查点**：按模型ID过滤, 顺序排序, 必填字段

**AI 输出**：

1. **分析涉及的表和字段**
   - 涉及的表：`itsm_form_field`
   - 字段：`field_key`（字段名），`field_type`（字段类型），`required`（是否必填）

2. **写出符合规范的 PostgreSQL SQL**
   ```sql
   SELECT
     ff.field_key AS "字段名",
     ff.field_type AS "字段类型",
     CASE WHEN ff.required THEN '是' ELSE '否' END AS "是否必填"
   FROM
     itsm_form_field ff
   WHERE
     ff.model_id = #{model_id}::BIGINT
   ORDER BY
     ff.sort_order ASC;
   ```
   **说明**：
   - `#{model_id}` 是参数化查询的占位符，用于防止 SQL 注入。
   - `WHERE` 条件 `ff.model_id = #{model_id}` 用于筛选出特定服务模型的所有表单字段。
   - 由于没有涉及到多表连接，所以不需要 JOIN 逻辑。
   - `ORDER BY ff.sort_order ASC` 用于按字段顺序排列结果。
   - `CASE WHEN ff.required THEN '是' ELSE '否' END` 用于将布尔值转换为中文的“是”或“否”，以符合输出要求。

3. **说明 WHERE 条件和 JOIN 逻辑**
   - `WHERE` 条件用于筛选出特定服务模型的所有表单字段。这里使用参数化查询，通过 `#{model_id}` 传递模型ID，确保查询的安全性。
   - 由于查询只涉及 `itsm_form_field` 表，不需要进行表连接（JOIN），因此没有 JOIN 逻辑。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-SVC-04（⭐⭐）

**题目**：统计各工作流定义被多少个服务模型引用，显示工作流名称和引用次数，按引用次数降序。

**检查点**：GROUP BY, COUNT, JOIN

**AI 输出**：

1. **分析涉及的表和字段**

   - `itsm_workflow_def`：工作流定义表，包含工作流的名称等信息。
     - 字段：`name`（工作流名称）

   - `itsm_service_model`：服务模型表，定义每类服务的表单结构、处理流程与SLA策略。
     - 字段：`workflow_def_id`（关联的工作流定义ID）

2. **写出符合规范的 PostgreSQL SQL**

```sql
SELECT 
    w.name AS workflow_name,
    COUNT(sm.id) AS reference_count
FROM 
    itsm.workflow_def w
LEFT JOIN 
    itsm.service_model sm ON w.id = sm.workflow_def_id
WHERE 
    sm.is_deleted = 0
GROUP BY 
    w.name
ORDER BY 
    reference_count DESC;
```

3. **说明 WHERE 条件和 JOIN 逻辑**

- **WHERE 条件**：`sm.is_deleted = 0` 用于过滤掉逻辑删除的服务模型，确保统计的是有效的服务模型引用。

- **JOIN 逻辑**：
  - 使用 `LEFT JOIN` 将 `itsm.workflow_def` 表（工作流定义表）与 `itsm.service_model` 表（服务模型表）连接。
  - 连接条件是 `w.id = sm.workflow_def_id`，即工作流定义ID等于服务模型中的工作流定义ID。
  - 这样，每个工作流定义可以关联到引用它的服务模型，通过统计每个工作流定义关联的服务模型数量，得到每个工作流定义的引用次数。

**说明**：
- 该查询首先通过左连接将工作流定义和引用它的服务模型关联起来。
- 然后，通过分组（`GROUP BY w.name`）和计数（`COUNT(sm.id)`）统计每个工作流定义被引用的次数。
- 最后，通过 `ORDER BY reference_count DESC` 按引用次数降序排列结果，得到每个工作流定义的引用次数和名称。

**自动评分**：95/100

- 功能正确性：40/40
- 规范合规性：20/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

## IT-SVC-05（⭐⭐⭐）

**题目**：查询所有服务模型及其表单字段中包含某关键字（如'电话'）的字段信息。

**检查点**：LIKE 搜索, JOIN, 字段名匹配

**AI 输出**：

1. **分析涉及的表和字段**

   - `itsm_service_model`：服务模型表，包含服务模型的基本信息。
     - `id`：服务模型ID。
   - `itsm_form_field`：动态表单字段定义表，包含服务模型的表单字段信息。
     - `model_id`：所属服务模型ID。
     - `field_key`：字段唯一键。
     - `label`：前端显示标签。

2. **写出符合规范的 PostgreSQL SQL**

```sql
-- 查询所有服务模型及其表单字段中包含某关键字（如'电话'）的字段信息
SELECT sm.id AS service_model_id,
       sm.name AS service_model_name,
       ff.field_key,
       ff.label
FROM itsm_service_model sm
JOIN itsm_form_field ff ON sm.id = ff.model_id
WHERE ff.field_key ILIKE '%电话%' OR ff.label ILIKE '%电话%';
```

3. **说明 WHERE 条件和 JOIN 逻辑**

   - **JOIN 逻辑**：通过`itsm_service_model`表的`id`字段与`itsm_form_field`表的`model_id`字段进行连接，以关联服务模型与其对应的表单字段。
   - **WHERE 条件**：使用`ILIKE`进行不区分大小写的模糊匹配，筛选出`itsm_form_field`表中`field_key`或`label`字段包含关键字“电话”的记录。这样可以确保查询结果中包含所有与关键字相关的字段信息。

**自动评分**：90/100

- 功能正确性：40/40
- 规范合规性：15/20
- 完整性：20/20
- 可维护性：15/20

**人工评分**（待填写）：___/100

---

