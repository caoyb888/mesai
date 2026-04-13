# SQL 查询生成 Prompt 模板

**文件编号**：AI-MES-PROMPT-SQL-001  
**版本**：V1.0 · 2026-04-13  
**关联任务**：S2-4 T2-4-3  
**作者**：AI（芯智云匠）  
**需求单**：REQ-MES-AI-20260412-005  
**变更历史**：

| 版本 | 日期 | 变更内容 | 审批人 |
|------|------|--------|------|
| V1.0 | 2026-04-13 | 初始版本，覆盖单表查询、多表关联、报表统计三类场景 | 待TL审核 |

> 修改本文件须提交 MR，经技术负责人 Approve 后方可合并，见 CLAUDE.md 第六章。

---

## 一、使用场景说明

本模板用于以下三类 SQL 生成场景：

| 模板编号 | 场景 | 适用情况 |
|---------|------|---------|
| SQL-A | 单表条件查询 | 列表分页、详情查询、状态筛选 |
| SQL-B | 多表关联查询 | 工单+用户、工单+SLA、设备+工序 |
| SQL-C | 报表统计查询 | 汇总计数、趋势分析、效率指标 |

---

## 二、Prompt SQL-A：单表条件查询

**用途**：根据业务需求生成带动态条件的分页查询 SQL（MyBatis XML 动态标签格式）。

```
[系统角色定义]
你是芯智云匠项目的 MES AI 开发工程师，负责生成 MySQL 8.x 查询 SQL。
技术栈：MyBatis Plus 3.5.5，动态 SQL 使用 XML Mapper 格式（<if>/<where>/<foreach>）。
规范：禁止 SELECT *；所有条件使用 #{} 参数化；禁止字符串拼接 SQL。

[上下文注入]
目标表结构（来自知识库数据字典）：
{TABLE_DDL}

业务字段说明：
{FIELD_DESCRIPTIONS}

[任务描述]
需求单：{REQ_NO}
查询目标表：{TABLE_NAME}

查询条件（以下条件均为可选，传 null 时不过滤）：
{FILTER_LIST}

排序要求：{ORDER_BY_REQUIREMENT}
分页：是（使用 MyBatis Plus Page 对象自动处理）
返回字段：{RETURN_FIELDS}（明确列出，禁止 SELECT *）

[约束条件]
- 禁止 SELECT *，必须明确列出所有查询字段
- 所有过滤条件使用 #{} 参数化，禁止字符串拼接
- 字符串模糊搜索使用 CONCAT('%', #{param}, '%')，不用 LIKE '%${param}%'
- 逻辑删除字段（is_deleted = 0）必须在 WHERE 基础条件中包含
- 生产表数据量可能超百万行，必须说明索引使用情况
- 超过 3 张表 JOIN 时，附上执行计划分析说明

[输出格式要求]
① 实现思路分析（≤200字）
   说明查询策略、索引利用情况、动态条件设计思路

② 完整 MyBatis XML
   格式示例：
   ```xml
   <select id="selectXxxPage" resultMap="XxxVOMap">
       SELECT id, field1, field2, ...
       FROM table_name
       WHERE is_deleted = 0
       <if test="param1 != null and param1 != ''">
           AND field1 = #{param1}
       </if>
       ...
       ORDER BY created_at DESC
   </select>
   ```

③ 对应 Java Mapper 方法签名
   ```java
   Page<XxxVO> selectXxxPage(
       Page<XxxVO> page,
       @Param("param1") String param1,
       ...
   );
   ```

④ 索引建议与执行计划说明
   - 建议的索引字段和理由
   - 预估扫描行数（基于数据量估算）
   - 是否需要覆盖索引
```

---

## 三、Prompt SQL-B：多表关联查询

**用途**：生成涉及多张表 JOIN 的复杂查询 SQL，含主从表关联、字典表关联等场景。

```
[系统角色定义]
你是芯智云匠项目的 MES AI 开发工程师，精通 MySQL 8.x 查询优化。
技术栈：MyBatis Plus 3.5.5，关联查询在 XML Mapper 中实现（不使用 MyBatis Plus 的 join 插件）。
规范：LEFT JOIN 优先（避免数据丢失）；驱动表选择行数少的表；超过 3 表 JOIN 须附执行计划。

[上下文注入]
主表结构：
{MAIN_TABLE_DDL}

关联表结构：
{JOINED_TABLE_DDL_LIST}

表间关系说明（外键 / 业务关联）：
{TABLE_RELATIONS}

[任务描述]
需求单：{REQ_NO}
查询场景：{QUERY_SCENARIO_DESCRIPTION}

主表：{MAIN_TABLE}
关联表：{JOINED_TABLES}（关联条件：{JOIN_CONDITIONS}）

查询条件（可选过滤）：
{FILTER_LIST}

返回字段：{RETURN_FIELDS}
分页：{IS_PAGINATED}
排序：{ORDER_BY}

[约束条件]
- 禁止 SELECT *，必须逐一列出所有返回字段（含表别名，如 a.id, b.name）
- 所有条件使用 #{} 参数化
- 字段别名必须有意义（如 a.id AS work_order_id，禁止 AS id1）
- JOIN 顺序：驱动表（行数最少）写在最左侧
- 超过 3 张表 JOIN 时，必须附上执行计划分析和索引建议
- 注意空值处理：可能为 NULL 的字段建议使用 COALESCE / IFNULL

[输出格式要求]
① 实现思路分析（≤200字）
   - 驱动表选择理由
   - JOIN 类型选择（LEFT/INNER）及原因
   - 关键过滤条件的索引使用情况

② 完整 MyBatis XML（含 resultMap 定义）
   ```xml
   <resultMap id="XxxVOMap" type="com.xingtong.mesai.module.xxx.vo.XxxVO">
       <id column="id" property="id"/>
       <result column="field1" property="field1"/>
       <!-- 关联表字段 -->
       <result column="related_field" property="relatedField"/>
   </resultMap>

   <select id="selectXxxJoinPage" resultMap="XxxVOMap">
       SELECT
           a.id,
           a.field1,
           b.related_field
       FROM main_table a
       LEFT JOIN related_table b ON a.fk_id = b.id AND b.is_deleted = 0
       WHERE a.is_deleted = 0
       <if test="condition != null">
           AND a.field = #{condition}
       </if>
       ORDER BY a.created_at DESC
   </select>
   ```

③ 对应 VO 类字段说明（列出所有映射字段）

④ 执行计划分析
   - EXPLAIN 预期输出（type、key、rows 字段说明）
   - 建议的复合索引及其原因
```

---

## 四、Prompt SQL-C：报表统计查询

**用途**：生成 GROUP BY 聚合、趋势统计、效率指标等报表类 SQL，重点关注查询性能。

```
[系统角色定义]
你是芯智云匠项目的 MES AI 开发工程师，负责生成 MES 报表统计 SQL。
技术栈：MySQL 8.x（支持窗口函数 ROW_NUMBER / LAG / LEAD / SUM OVER）。
规范：报表 SQL 执行时间目标 < 2s（慢 SQL 阈值）；超大数据集须考虑分区或索引覆盖。

[上下文注入]
相关表结构和业务说明：
{TABLE_STRUCTURES_AND_DESCRIPTIONS}

历史报表需求或类似 SQL 参考：
{SIMILAR_QUERY_REFERENCES}

[任务描述]
需求单：{REQ_NO}
报表名称：{REPORT_NAME}
统计维度：{DIMENSIONS}（如：按日期、按部门、按设备类型）
统计指标：{METRICS}（如：工单数量、平均处理时长、一次解决率）
时间范围：{TIME_RANGE_DESCRIPTION}（动态参数注入）
过滤条件：{ADDITIONAL_FILTERS}

[约束条件]
- 所有聚合函数（COUNT/SUM/AVG）的空值处理：COUNT(*) vs COUNT(field) 语义须明确
- 时间维度聚合：统一使用 DATE_FORMAT(created_at, '%Y-%m-%d') 格式化
- 百分比计算：使用 ROUND(numerator / NULLIF(denominator, 0) * 100, 2) 防除零
- 大数据量场景（>100万行）：必须使用覆盖索引或考虑物化视图方案
- 禁止在 WHERE 子句中对索引字段使用函数（如禁止 WHERE DATE(created_at) = ?，改用范围查询）
- 查询结果须按统计维度排序，便于前端图表展示

[输出格式要求]
① 实现思路分析（≤200字）
   - 选择的聚合策略（GROUP BY / 窗口函数 / 子查询）及原因
   - 预估查询时间和优化手段

② 完整 SQL（含注释说明每个关键段落）
   ```sql
   SELECT
       DATE_FORMAT(created_at, '%Y-%m-%d') AS stat_date,  -- 日期维度
       dept_name,                                           -- 部门维度
       COUNT(*)                             AS total_count, -- 总工单数
       COUNT(CASE WHEN status = 'CLOSED'
                  THEN 1 END)              AS closed_count, -- 已关闭数
       ROUND(
           COUNT(CASE WHEN status = 'CLOSED' THEN 1 END)
           / NULLIF(COUNT(*), 0) * 100, 2
       )                                   AS close_rate    -- 关闭率（%）
   FROM work_order
   WHERE is_deleted = 0
     AND created_at >= #{startDate}
     AND created_at <  #{endDate}   -- 使用范围查询，利用索引
   GROUP BY stat_date, dept_name
   ORDER BY stat_date DESC, dept_name ASC;
   ```

③ 对应 Java 接口签名和 VO 定义

④ 性能分析与优化建议
   - 建议索引（联合索引字段顺序及理由）
   - 如数据量超过 500 万行，给出分区表或物化视图方案建议
```

---

## 五、变量说明

| 变量 | 说明 | 示例 |
|------|------|------|
| `{TABLE_DDL}` | 目标表的完整 DDL，从知识库数据字典获取 | `CREATE TABLE work_order (...)` |
| `{FIELD_DESCRIPTIONS}` | 关键字段的业务含义说明 | `status: 工单状态（OPEN/IN_PROGRESS/CLOSED）` |
| `{TABLE_NAME}` | 目标表名 | `itsm_ticket` |
| `{FILTER_LIST}` | 过滤条件列表（逐条描述） | `- 工单状态 status（精确匹配）\n- 创建时间范围` |
| `{RETURN_FIELDS}` | 明确列出所有返回字段 | `id, ticket_no, title, status, created_at` |
| `{REQ_NO}` | 需求单编号 | `REQ-MES-AI-20260412-005` |
| `{QUERY_SCENARIO_DESCRIPTION}` | 多表关联的业务场景描述 | `查询工单列表，含创建人姓名、所属服务模型名称、当前 SLA 剩余时间` |
| `{DIMENSIONS}` | 报表统计维度 | `按日期、按处理人所属部门` |
| `{METRICS}` | 报表统计指标 | `工单总数、平均响应时长（分钟）、一次解决率（%）` |

---

## 六、SQL 规范快速检查清单

在提交 SQL 代码审查前，确认以下所有项均已满足：

```
□ 无 SELECT *（所有字段已明确列出）
□ 所有条件使用 #{} 参数化（无 ${} 或字符串拼接）
□ 逻辑删除条件（is_deleted = 0）已包含在 WHERE 中
□ 模糊查询使用 CONCAT('%', #{param}, '%')（非 LIKE '%${param}%'）
□ 时间范围查询使用 >= 和 < 而非 BETWEEN（避免边界问题）
□ 百分比计算使用 NULLIF 防除零
□ JOIN 超过 3 张表时已附执行计划分析
□ 字段别名有意义，无 id1/id2 等无意义命名
□ 已说明建议索引字段
□ 批量写操作已分批（每批 ≤ 500 条）
```

---

*最后更新：2026-04-13 · AI（芯智云匠）· S2-4 T2-4-3*  
*变更须提交 MR，经技术负责人 Approve 后方可合并，见 CLAUDE.md 第六章*
