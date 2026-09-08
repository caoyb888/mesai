# S3-1 表/字段 SQL 场景验证报告（真实 MES）

| 项 | 内容 |
|----|----|
| 文件编号 | AI-MES-REPORT-S3-1-SQLVAL-2026 |
| 需求单 | REQ-MES-AI-20260715-001（T3-1-4/5）|
| 日期 | 2026-07-15 |
| 题量 | 30（6 模块×5）|
| RAG 上下文 | mes_s3_understanding 表卡片 Top-5 |
| Token 消耗 | 66,771 |
| 自动初评均分 | 69.9/100 |
| 自动初评 ≥60 占比 | 76.7% |
| 验收目标 | 人工评分正确率 **≥85%** |

> ⚠️ 自动初评仅规则检查（表命中/禁 SELECT */参数化/完整性），**不代表 SQL 语义正确**；
> 语义正确率须 TL/BIZ 人工终评（下方每题「人工评分」列），<85% 的模块补训（T3-1-2）。

## 模块自动初评汇总

| 模块 | 题数 | 自动均分 | 最低 | 最高 | 人工均分（待填）|
|----|----|----|----|----|----|
| 订单管理 | 5 | 74.0 | 60 | 80 | ___ |
| 炼钢板坯 | 5 | 67.0 | 60 | 95 | ___ |
| 卷材 | 5 | 61.0 | 55 | 80 | ___ |
| 质量 | 5 | 75.0 | 55 | 100 | ___ |
| 调度 | 5 | 70.0 | 55 | 100 | ___ |
| 提货发货 | 5 | 72.4 | 55 | 100 | ___ |

---

## 逐题明细（含 AI 生成 SQL + 人工评分列）

### 1. MES-ORD-01　（订单管理）

**业务场景**：查询某客户（客户号已知）的所有订单头，显示订单号、下单日期、订单状态和客户名称。

**期望表**：SSD_ORDER_HEAD, SSD_CUSTOMER　**检查点**：JOIN客户表, 按客户过滤

**AI 生成 SQL 与说明**：

```sql
SELECT 
    SOH.ORD_NO,
    SOH.ORD_RCV_DTM AS "下单日期",
    SOH.ORD_STS AS "订单状态",
    CUST.CUST_NM AS "客户名称"
FROM 
    SSD_ORDER_HEAD SOH
JOIN 
    -- 假设存在一个客户信息表 CUST，其中 CUST_CD 为外键关联客户信息
    CUST ON SOH.CUST_CD = CUST.CUST_CD
WHERE 
    SOH.CUST_CD = :paramCustCd -- 参数化客户号
    AND SOH.ARCHIVE_FL = 'N'; -- 未归档的订单
```

说明：此 SQL 查询了 `SSD_ORDER_HEAD` 表中与特定客户相关的所有订单头信息，包括订单号、下单日期、订单状态和客户名称，其中客户名称通过假设存在的客户信息表 `CUST` 进行关联查询。使用了参数化查询 `:paramCustCd` 来防止 SQL 注入攻击，并过滤出未归档的订单。

**自动初评**：80/100（{'表命中': 20, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 2. MES-ORD-02　（订单管理）

**业务场景**：查询某订单（订单号已知）的所有订单明细行，显示行号、物料/产品、数量和规格。

**期望表**：SSD_ORDER_LINE　**检查点**：按订单号过滤, 明细字段

**AI 生成 SQL 与说明**：

```sql
SELECT 
    SPG_ORD_PROG.ORD_LN AS "订单行号",
    SPG_ORD_PROG.PROD_CD AS "物料/产品",
    SPG_ORD_PROG.ORD_QTY AS "数量",
    SQM_ORD_COM.SPEC_CD AS "规格"
FROM 
    SPG_ORD_PROG
JOIN 
    SQM_ORD_COM ON SPG_ORD_PROG.ORD_NO = SQM_ORD_COM.ORD_NO AND SPG_ORD_PROG.ORD_LN = SQM_ORD_COM.ORD_LN
WHERE 
    SPG_ORD_PROG.ORD_NO = :paramOrderNo;
```

说明：根据业务场景，查询特定订单号的所有订单明细行，通过JOIN操作将SPG_ORD_PROG表和SQM_ORD_COM表关联起来，以获取订单行号、物料/产品、数量和规格信息。参数化查询使用`:paramOrderNo`表示订单号。

**自动初评**：60/100（{'表命中': 0, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 3. MES-ORD-03　（订单管理）

**业务场景**：统计各客户的订单数量，按订单数降序取前 10。

**期望表**：SSD_ORDER_HEAD, SSD_CUSTOMER　**检查点**：GROUP BY, COUNT, TOP N

**AI 生成 SQL 与说明**：

```sql
SELECT CUST_CD, COUNT(*) AS ORD_QTY
FROM SSD_ORDER_HEAD
GROUP BY CUST_CD
ORDER BY COUNT(*) DESC
FETCH FIRST 10 ROWS ONLY;
```

说明：此 SQL 查询统计了 `SSD_ORDER_HEAD` 表中每个客户（`CUST_CD`）的订单数量，并按订单数量降序排列，仅获取前 10 个客户。使用 `FETCH FIRST 10 ROWS ONLY` 来限制结果集只返回前 10 行。

**自动初评**：75/100（{'表命中': 20, '规范': 25, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 4. MES-ORD-04　（订单管理）

**业务场景**：查询某订单的订单头及其所有明细行（一对多联查），显示订单号、客户、每行数量。

**期望表**：SSD_ORDER_HEAD, SSD_ORDER_LINE　**检查点**：头-行JOIN, 一对多

**AI 生成 SQL 与说明**：

```sql
SELECT 
    H.ORD_NO AS 订单号,
    H.CUST_CD AS 客户代码,
    H.ORD_QTY AS 订单总量,
    D.ORD_LN AS 明细行号,
    D.ORD_QTY AS 明细行数量
FROM 
    SSD_ORDER_HEAD H
JOIN 
    SQM_ORD_COM D ON H.ORD_NO = D.ORD_NO
WHERE 
    H.ORD_NO = :param_order_no;
```

说明：此 SQL 查询根据提供的订单号 `:param_order_no` 联查订单头表 `SSD_ORDER_HEAD` 和订单明细表 `SQM_ORD_COM`，显示订单号、客户代码、订单总量以及每条明细行的行号和数量。

**自动初评**：80/100（{'表命中': 20, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 5. MES-ORD-05　（订单管理）

**业务场景**：查询本月新增的订单明细行及其所属订单头信息。

**期望表**：SSD_ORDER_HEAD, SSD_ORDER_LINE　**检查点**：月份过滤, JOIN

**AI 生成 SQL 与说明**：

```sql
SELECT 
    OH.ORD_NO,
    OH.ES_EMP_ID,
    OH.ORD_RCV_DT,
    OH.ORD_REG_DTM,
    OH.ORD_STS,
    OH.ARCHIVE_FL,
    OH.URGENT_FL,
    OH.ERROR_FL,
    OH.EXP_TAX_FL,
    OH.MACHINE_YN,
    OH.IMPORTANT_YN,
    OC.ORD_LN,
    OC.PROD_CD,
    OC.CUST_CD,
    OC.SPEC_CD,
    OC.ORD_DELV_DT,
    OC.ORD_RCV_DTM,
    OC.ORD_OVERDUE_FL,
    OC.ORD_IMP_FL
FROM 
    SSD_ORDER_HEAD OH
JOIN 
    SPG_ORD_PROG OC ON OH.ORD_NO = OC.ORD_NO
WHERE 
    TRUNC(OH.ORD_REG_DTM) >= TRUNC(SYSDATE) - 30
    AND TRUNC(OH.ORD_REG_DTM) < TRUNC(SYSDATE + 1)
    AND OH.ARCHIVE_FL = 'N';
```

一句话说明：以上 SQL 查询本月新增的订单明细行及其所属订单头信息，确保订单未归档，并且只考虑订单注册日期在本月内的记录。

**自动初评**：75/100（{'表命中': 20, '规范': 25, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 6. MES-SMS-01　（炼钢板坯）

**业务场景**：查询某热号（HEAT_NO）下生产的所有板坯，显示板坯号、重量、钢种和生产日期。

**期望表**：SMS_SLAB　**检查点**：按热号过滤, 字段选择

**AI 生成 SQL 与说明**：

```sql
SELECT 
    INST.HEAT_NO,
    INST.PLAN_HEAT_NO,
    INST.HEAT_WGT,
    INST.P_STEEL_GRD,
    INST.PROD_INST_DTM
FROM 
    SCH_INST_HEAT INST
WHERE 
    INST.HEAT_NO = :paramHeatNo;
```

说明：根据业务场景，查询指定热号（HEAT_NO）下的所有板坯信息，包括板坯号（PLAN_HEAT_NO）、重量（HEAT_WGT）、钢种（P_STEEL_GRD）和生产日期（PROD_INST_DTM）。使用参数化查询，避免SQL注入风险。

**自动初评**：60/100（{'表命中': 0, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 7. MES-SMS-02　（炼钢板坯）

**业务场景**：查询指定订单（ORD_NO）关联的板坯清单及其状态（SLAB_STS）。

**期望表**：SMS_SLAB　**检查点**：按订单过滤, 状态字段

**AI 生成 SQL 与说明**：

```sql
SELECT 
    S.ORD_NO,
    S.ORD_LN,
    S.PROD_CD,
    S.CUST_CD,
    S.SPEC_CD,
    S.SLAB_STS
FROM 
    SPG_ORD_PROG S
WHERE 
    S.ORD_NO = :param1;
```

说明：根据给定的业务场景和表结构，查询指定订单编号（ORD_NO）关联的板坯清单及其状态（SLAB_STS）。这里假设`SLAB_STS`字段存在于`SPG_ORD_PROG`表中，如果该字段实际存在于其他表中，则需要进行相应的JOIN操作。由于表结构中没有明确`SLAB_STS`字段，这里将其作为一个示例字段进行查询。实际应用中需要根据实际表结构进行调整。

**自动初评**：60/100（{'表命中': 0, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 8. MES-SMS-03　（炼钢板坯）

**业务场景**：统计某日各钢种的板坯数量与总重量。

**期望表**：SMS_SLAB　**检查点**：GROUP BY钢种, SUM重量, 日期过滤

**AI 生成 SQL 与说明**：

```sql
SELECT 
    S.STEEL_GRD_GRP AS 钢种组,
    COUNT(S.PROD_PCS) AS 板坯数量,
    SUM(S.HEAT_WGT) AS 总重量
FROM 
    SCH_PLAN_HEAT S
WHERE 
    S.PLAN_HEAT_STS IN ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9') -- 只统计计划生成到作业结束的炉次
    AND S.HEAT_DTM = TO_DATE(:param_date, 'YYYY-MM-DD') -- 根据参数化输入的日期筛选
GROUP BY 
    S.STEEL_GRD_GRP
ORDER BY 
    S.STEEL_GRD_GRP;
```
一句话说明：该SQL查询统计了指定日期内各钢种组的板坯数量和总重量，其中`:param_date`为参数化输入的日期。

**自动初评**：60/100（{'表命中': 0, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 9. MES-SMS-04　（炼钢板坯）

**业务场景**：查询已发送 ERP（ERP_POSTING_YN='Y'）但尚未冷却完成（COOLING_COMP_YN='N'）的板坯。

**期望表**：SMS_SLAB　**检查点**：多标志位组合, Y/N过滤

**AI 生成 SQL 与说明**：

```sql
SELECT SLAB_NO, HEAT_NO, ORD_NO, PROD_CD, LOC_CD, ERP_POSTING_YN, COOLING_COMP_YN
FROM SMS_SLAB
WHERE ERP_POSTING_YN = 'Y' AND COOLING_COMP_YN = 'N';
```

说明：此查询语句根据给定的表结构和业务场景，选择了已发送至ERP系统但尚未冷却完成的板坯记录，明确列出了所需字段，并使用了参数化命名规范。

**自动初评**：95/100（{'表命中': 40, '规范': 25, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 10. MES-SMS-05　（炼钢板坯）

**业务场景**：查询某热号的炼钢结果及其下属板坯（热号→板坯联查）。

**期望表**：SMS_RSLT_HEAT, SMS_SLAB　**检查点**：热号JOIN板坯

**AI 生成 SQL 与说明**：

```sql
SELECT 
    s.STEEL_GRD_GRP,
    s.HEAT_WGT,
    s.SLAB_TOT_LTH,
    s.PROD_PCS,
    s.PLAN_HEAT_STS,
    s.ORD_FL,
    s.RTN_YN,
    s.STEEL_GRD_DIVERT_YN,
    s.TUNDISH_CHG_FL,
    s.WTH_CHANGE_YN,
    s.X_STR_SLAB_WTH_CHG_YN,
    s.Y_SLAB_WTH_CHG_YN,
    h.FCE_STAY_DUR,
    h.FCE_DISCH_TEMP,
    h.ARCHIVE_FL,
    h.FCE_CH_DISCH_FL,
    h.FCE_DISCH_FL,
    h.RJT_CAUSE_CD,
    h.SLAB_NO,
    h.FCE_CH_SEQ,
    h.PLT_NO,
    h.FAC_CD,
    h.PROC_CD,
    i.P_STEEL_GRD,
    i.HEAT_WGT AS INST_HEAT_WGT,
    i.SLAB_THK,
    i.PROD_INST_DTM,
    i.PLAN_HEAT_STS AS INST_PLAN_HEAT_STS,
    i.ORD_FL AS INST_ORD_FL,
    i.RTN_YN AS INST_RTN_YN,
    i.STEEL_GRD_DIVERT_YN AS INST_STEEL_GRD_DIVERT_YN,
    i.TUNDISH_CHG_FL AS INST_TUNDISH_CHG_FL,
    i.SEND_FL,
    b.HEAT_TOT_WGT,
    b.EP_TGT_TEMP,
    b.OXG_PRS,
    b.ARCHIVE_FL AS BOF_ARCHIVE_FL,
    b.OPER_ABNR_REASON_CD,
    b.N2_COAT_RSLT_PTRN,
    b.SLAG_COAT_METHOD,
    b.IS_END,
    d.HEAT_LAB_WGT,
    d.HEAT_INST_YN,
    d.HEAT_DGN_COMP_FL
FROM 
    SCH_PLAN_HEAT s
JOIN 
    SPR_HEAT_FCE_RSLT h ON s.HEAT_NO = h.HEAT_NO
JOIN 
    SCH_INST_HEAT i ON s.HEAT_NO = i.PLAN_HEAT_NO
JOIN 
    SMS_RSLT_BOF b ON s.HEAT_NO = b.HEAT_NO
JOIN 
    SCH_HEAT_DESIGN_RESULT d ON s.HEAT_NO = d.HEAT_NO
WHERE 
    s.HEAT_NO = :heat_no;
```

说明：此查询联查了五个表，以获取特定热号的炼钢结果及其下属板坯信息。使用了参数化查询，以确保安全性。由于涉及多个表的联查，执行计划可能依赖于各个表的索引和数据分布，具体执行计划需要根据实际数据库环境进行分析。

**自动初评**：60/100（{'表命中': 0, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 11. MES-SCR-01　（卷材）

**业务场景**：查询某订单的所有钢卷，显示卷号、净重和最终判定等级（FINAL_JDG_CD）。

**期望表**：SCR_COIL_MASTER　**检查点**：按订单过滤, 判定等级字段

**AI 生成 SQL 与说明**：

```sql
SELECT 
    H.COIL_NO AS 卷号,
    H.NET_WGT AS 净重,
    P.FINAL_JDG_PASS_FL AS 最终判定等级
FROM 
    MESAPUSER.SYD_PROD_MASTER P
JOIN 
    MESAPUSER.SYD_HOT_COIL H ON P.HEAT_NO = H.HEAT_NO
WHERE 
    P.ORD_NO = :param -- 假设:param为订单编号参数
    AND P.FINAL_JDG_PASS_FL IN ('Y', 'N'); -- 根据业务需求，只选择已判定的产品
```

说明：此查询通过连接产品主表（SYD_PROD_MASTER）和热卷表（SYD_HOT_COIL），根据订单编号（ORD_NO）筛选出所有相关钢卷，并显示卷号、净重和最终判定等级。使用了参数化查询以避免SQL注入风险。

**自动初评**：60/100（{'表命中': 0, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 12. MES-SCR-02　（卷材）

**业务场景**：查询处于 Hold 状态（HOLD_YN='Y'）的钢卷清单。

**期望表**：SCR_COIL_MASTER　**检查点**：Hold标志过滤

**AI 生成 SQL 与说明**：

```sql
SELECT 
    HOLD_SEQ,
    PLT_NO,
    HOLD_REQ_DTM,
    HOLD_RSN_CD,
    HOLD_RSN_DESC
FROM 
    SPR_HOLD
WHERE 
    HOLD_YN = 'Y';
```
一句话说明：查询 `SPR_HOLD` 表中所有处于 Hold 状态（`HOLD_YN='Y'`）的钢卷记录，包括保留序号、生产批次号、保留请求时间、保留原因代码和保留原因描述。

**自动初评**：55/100（{'表命中': 0, '规范': 25, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 13. MES-SCR-03　（卷材）

**业务场景**：查询某钢卷（COIL_NO）的缺陷记录。

**期望表**：SCR_COIL_MASTER, SCR_DEFECT　**检查点**：卷-缺陷JOIN

**AI 生成 SQL 与说明**：

```sql
SELECT 
    D.PROC_CD,
    D.COIL_NO,
    D.DEF_CD,
    D.COIL_THK AS stripThick,
    D.COIL_WTH AS stripWidth,
    D.EMP_CD,
    D.DEF_LOC AS DefectSurfaceCodeT,
    D.DEF_LINE,
    D.DEF_SURF_CD AS DefectSurfaceCode,
    D.ARCHIVE_FL,
    D.REP_YN,
    D.PROD_TOT_JDG_FL,
    D.DEF_CMT_CD AS DefectCommentsCode,
    D.DEF_TYPE AS DefectTypePLTCM
FROM 
    MESAPUSER.SCR_DEFECT D
WHERE 
    D.COIL_NO = :paramCoilNo;
```

说明：以上 SQL 查询指定钢卷编号（COIL_NO）的缺陷记录，使用了参数化查询来防止 SQL 注入，并且明确列出了所有需要查询的字段。

**自动初评**：80/100（{'表命中': 20, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 14. MES-SCR-04　（卷材）

**业务场景**：统计各最终判定等级的钢卷数量与总净重。

**期望表**：SCR_COIL_MASTER　**检查点**：GROUP BY判定, COUNT+SUM

**AI 生成 SQL 与说明**：

```sql
SELECT 
    JDG.`PROD_TOT_JDG_RSLT_TY` AS `最终判定等级`,
    COUNT(DISTINCT MTC.`PROD_NO`) AS `钢卷数量`,
    SUM(MTC.`PROD_WGT`) AS `总净重`
FROM 
    SQM_TOT_JDG_RSLT JDG
JOIN 
    SQM_MTC_PROD MTC ON JDG.`PROD_NO` = MTC.`PROD_NO`
GROUP BY 
    JDG.`PROD_TOT_JDG_RSLT_TY`;
```
说明：此查询统计了每个最终判定等级对应的钢卷数量和总净重，通过连接`SQM_TOT_JDG_RSLT`和`SQM_MTC_PROD`表来实现。

**自动初评**：55/100（{'表命中': 0, '规范': 25, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 15. MES-SCR-05　（卷材）

**业务场景**：查询尚未发送 ERP（SEND_ERP_YN='N'）的钢卷。

**期望表**：SCR_COIL_MASTER　**检查点**：ERP标志过滤

**AI 生成 SQL 与说明**：

```sql
SELECT 
    S.SLAB_NO,
    S.ERP_POSTING_YN,
    S.DEFECT_CD,
    S.SLAB_STS,
    S.ORD_FL,
    S.COOLING_COMP_YN,
    S.MIXED_SLAB_TY,
    S.ERP_SEND_FL,
    S.SLAB_FG,
    S.IS_ABOLISH,
    S.HEAT_NO,
    S.ORD_NO,
    S.PROD_CD,
    S.LOC_CD
FROM 
    SMS_SLAB S
WHERE 
    S.ERP_POSTING_YN = 'N';
```

说明：此查询列出了所有尚未发送至ERP系统的钢坯信息，根据字段`ERP_POSTING_YN`筛选出值为'N'的记录。

**自动初评**：55/100（{'表命中': 0, '规范': 25, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 16. MES-QM-01　（质量）

**业务场景**：查询某订单（订单号+行号）的质量综合信息。

**期望表**：SQM_ORD_COM　**检查点**：复合主键过滤

**AI 生成 SQL 与说明**：

```sql
SELECT 
  S.ORD_NO,
  S.ORD_LN,
  S.PROD_CD,
  S.CUST_CD,
  S.ORD_TY,
  S.ORD_QTY,
  S.ORD_WTH,
  S.ORD_LTH,
  S.ORD_THK,
  S.QLT_DSN_REQ_TY,
  S.ORD_PROG_STS,
  S.URGENT_FL,
  S.AUTO_CONF_YN,
  S.ORD_PLT_YN
FROM 
  SQM_ORD_COM S
WHERE 
  S.ORD_NO = :ord_no AND S.ORD_LN = :ord_ln;
```
一句话说明：此查询语句用于获取指定订单编号和行号的质量综合信息，符合规范要求，使用了参数化查询以防止SQL注入。

**自动初评**：100/100（{'表命中': 40, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 17. MES-QM-02　（质量）

**业务场景**：查询某材料/产品的化学成分检验结果及其判定。

**期望表**：SQM_CHEM_RSLT, SQM_CHEM_JDG　**检查点**：结果JOIN判定

**AI 生成 SQL 与说明**：

```sql
SELECT 
    S.CHEM_SMP_CD,
    S.CHEM_SMP_SEQ,
    S.NON_ANAL_RSN,
    S.SMP_ANAL_END_DTM,
    S.SMP_SEND_DTM,
    S.SMP_RECEIPT_DTM,
    S.INSP_EMP_NO,
    S.INSP_EMP_NM,
    S.TREAT_CNT,
    S.CHEM_JUDG,
    S.CHEM_FLAG,
    S.CHEM_REQ_NO,
    M.MN_RSLT,
    M.P_RSLT,
    M.S_RSLT,
    M.CEQ_RSLT
FROM 
    SQM_SMP_STS S
JOIN 
    SQM_WSP_MTC_CHEM_INF M ON S.CHEM_SMP_CD = M.MTC_NO
WHERE 
    S.CHEM_SMP_CD = :param1 AND
    S.CHEM_SMP_SEQ = :param2;
```
一句话说明：该查询用于检索特定材料/产品的化学成分检验结果及其判定，通过连接`SQM_SMP_STS`和`SQM_WSP_MTC_CHEM_INF`表来获取完整的化学成分数据。

**自动初评**：60/100（{'表命中': 0, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 18. MES-QM-03　（质量）

**业务场景**：查询综合判定结果为不合格的记录。

**期望表**：SQM_TOT_JDG_RSLT　**检查点**：判定值过滤

**AI 生成 SQL 与说明**：

```sql
SELECT 
  ORD_NO, 
  ORD_LN, 
  QLT_DSN_STD_TY, 
  QLT_REMARKS
FROM 
  SQM_ORD_MECH_PRL
WHERE 
  ARCHIVE_FL = 'N' AND
  (IMPACT_SMP_STATUS = '不合格' OR 
  TSL_SMP_STATUS = '不合格' OR 
  HARD_SMP_STATUS = '不合格');
```

说明：此查询针对`SQM_ORD_MECH_PRL`表，选择未归档（`ARCHIVE_FL = 'N'`）且至少有一个测试状态为不合格的记录。字段`IMPACT_SMP_STATUS`、`TSL_SMP_STATUS`和`HARD_SMP_STATUS`的具体取值含义需根据字典解码来确定“不合格”对应的值。

**自动初评**：55/100（{'表命中': 0, '规范': 25, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 19. MES-QM-04　（质量）

**业务场景**：查询某质保书（MTC）的综合信息。

**期望表**：SQM_MTC_COM　**检查点**：按MTC过滤

**AI 生成 SQL 与说明**：

```sql
SELECT 
    MTC_NO,
    MTC_CHG_CNT,
    ORD_NO,
    PROD_CD,
    INSP_AGENCY_CD,
    SPEC_ORG_CD,
    CUST_PO_NO,
    MTC_SPEC_NM,
    MTC_STS_CD,
    MTC_REQ_CD,
    ATND_TEST_YN,
    SALE_PTH_TY,
    MTC_CFM_TY,
    TSL_GRT_CD,
    BEND_GRT_CD,
    IMPACT_GRT_CD,
    HARD_GRT_CD,
    MGRPHY_GRT_CD
FROM 
    SQM_MTC_COM
WHERE 
    MTC_NO = :param_MTC_NO AND
    MTC_CHG_CNT = :param_MTC_CHG_CNT;
```

说明：根据提供的表结构和业务场景，此 SQL 查询语句用于检索特定质量保证书（MTC）的综合信息，包括订单编号、产品代码、检查机构代码等关键字段，同时使用参数化查询以提高安全性。

**自动初评**：100/100（{'表命中': 40, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 20. MES-QM-05　（质量）

**业务场景**：统计某期间各综合判定结果的数量分布。

**期望表**：SQM_TOT_JDG_RSLT　**检查点**：GROUP BY判定, 期间过滤

**AI 生成 SQL 与说明**：

```sql
SELECT 
    CHEM_JUDG AS 综合判定结果,
    COUNT(*) AS 数量
FROM 
    SQM_SMP_STS
WHERE 
    SMP_ANAL_END_DTM BETWEEN :start_date AND :end_date
GROUP BY 
    CHEM_JUDG
ORDER BY 
    数量 DESC;
```
说明：该SQL查询统计了在指定期间内，SQM_SMP_STS表中各综合判定结果的数量分布。使用了参数化查询，其中`:start_date`和`:end_date`为查询的起始和结束日期参数。

**自动初评**：60/100（{'表命中': 0, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 21. MES-SCH-01　（调度）

**业务场景**：查询某计划的板坯设计结果，显示计划号、板坯设计信息。

**期望表**：SCH_SLAB_DESIGN_RESULT, SCH_PLAN_SLAB　**检查点**：计划-设计关联

**AI 生成 SQL 与说明**：

```sql
SELECT 
    SCH_PLAN_ROLL.MTL_NO AS 计划号,
    SCH_HSM_ROLL_DESIGN_RESULT.ROLL_DGN_MGT_NO AS 板坯设计信息
FROM 
    SCH_PLAN_ROLL
JOIN 
    SCH_HSM_ROLL_DESIGN_RESULT
ON 
    SCH_PLAN_ROLL.SLAB_NO = SCH_HSM_ROLL_DESIGN_RESULT.CAST_DGN_MGT_NO
WHERE 
    SCH_PLAN_ROLL.MTL_NO = :param;
```

说明：此 SQL 查询根据提供的表结构卡片，通过 `SCH_PLAN_ROLL` 表的 `MTL_NO` 字段和 `SCH_HSM_ROLL_DESIGN_RESULT` 表的 `CAST_DGN_MGT_NO` 字段进行关联，查询指定计划号的板坯设计信息。使用了参数化查询，以防止 SQL 注入攻击。

**自动初评**：60/100（{'表命中': 0, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 22. MES-SCH-02　（调度）

**业务场景**：查询某热次计划及其加热设计结果（热号→设计联查）。

**期望表**：SCH_PLAN_HEAT, SCH_HEAT_DESIGN_RESULT　**检查点**：计划JOIN设计

**AI 生成 SQL 与说明**：

```sql
SELECT 
    SCH_PLAN_HEAT.PLAN_HEAT_NO,
    SCH_PLAN_HEAT.SPEC_HEAT_NO,
    SCH_PLAN_HEAT.HEAT_WGT,
    SCH_PLAN_HEAT.SLAB_THK,
    SCH_INST_HEAT.PROD_INST_DTM,
    SMS_RSLT_BOF.BOF_NO,
    SMS_RSLT_BOF.SCRAP_CHARG_DTM,
    SQM_TOT_JDG_RSLT.UST_GRD
FROM 
    SCH_PLAN_HEAT
JOIN 
    SCH_INST_HEAT ON SCH_PLAN_HEAT.PLAN_HEAT_NO = SCH_INST_HEAT.PLAN_HEAT_NO
JOIN 
    SMS_RSLT_BOF ON SCH_PLAN_HEAT.PLAN_HEAT_NO = SMS_RSLT_BOF.HEAT_NO
JOIN 
    SQM_TOT_JDG_RSLT ON SCH_PLAN_HEAT.SPEC_HEAT_NO = SQM_TOT_JDG_RSLT.SPEC_CD
WHERE 
    SCH_PLAN_HEAT.PLAN_HEAT_NO = :paramHeatNo;
```

说明：该查询通过连接四个表（SCH_PLAN_HEAT、SCH_INST_HEAT、SMS_RSLT_BOF、SQM_TOT_JDG_RSLT）来获取特定热次计划及其加热设计结果。使用了参数化查询，其中`:paramHeatNo`代表查询参数热次编号。由于表结构中存在多个疑似关联键，所以此处假设了它们之间的关联关系，并进行了表连接。由于缺乏具体的索引信息，无法提供执行计划或索引使用的详细说明。

**自动初评**：80/100（{'表命中': 20, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 23. MES-SCH-03　（调度）

**业务场景**：查询某轧制批次（SCH_ROLL_BATCH）包含的计划。

**期望表**：SCH_ROLL_BATCH　**检查点**：按批次过滤

**AI 生成 SQL 与说明**：

```sql
SELECT 
    SCH_ROLL_BATCH.BATCH_CD,
    SCH_ROLL_BATCH.ROLL_UNIT,
    SCH_PLAN_ROLL.MTL_NO,
    SCH_PLAN_ROLL.PLAN_PROC_SEQ,
    SCH_PLAN_ROLL.PROD_INST_DTM,
    SCH_PLAN_ROLL.WK_STA_SCH_DTM,
    SCH_PLAN_ROLL.WK_END_SCH_DTM,
    SCH_PLAN_ROLL.PLAN_ROLL_STS,
    SCH_PLAN_ROLL.SLAB_NO
FROM 
    SCH_ROLL_BATCH
JOIN 
    SCH_PLAN_ROLL ON SCH_ROLL_BATCH.ROLL_UNIT = SCH_PLAN_ROLL.ROLL_UNIT
WHERE 
    SCH_ROLL_BATCH.BATCH_CD = :paramBatchCd;
```

说明：以上 SQL 查询了指定批次号（:paramBatchCd）的轧制批次（SCH_ROLL_BATCH）包含的计划信息，通过内连接 SCH_PLAN_ROLL 表获取了相关的轧制计划细节。

**自动初评**：100/100（{'表命中': 40, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 24. MES-SCH-04　（调度）

**业务场景**：统计某日各计划的板坯设计数量。

**期望表**：SCH_PLAN_SLAB　**检查点**：GROUP BY, 日期过滤

**AI 生成 SQL 与说明**：

```sql
SELECT
  PLAN_ROLL_STS,
  COUNT(SLAB_NO) AS DESIGN_SLABS_COUNT
FROM
  SCH_PLAN_ROLL
WHERE
  WK_STA_SCH_DTM = TO_DATE('2026-07-14', 'YYYY-MM-DD')
GROUP BY
  PLAN_ROLL_STS;
```

说明：此查询统计了2026年7月14日各计划轧制状态（PLAN_ROLL_STS）对应的板坯设计数量（SLAB_NO），使用`COUNT`函数对每个状态的板坯编号进行计数，并按计划轧制状态分组。

**自动初评**：55/100（{'表命中': 0, '规范': 25, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 25. MES-SCH-05　（调度）

**业务场景**：查询待执行的热次设计计划。

**期望表**：SCH_PLAN_HEAT　**检查点**：状态过滤

**AI 生成 SQL 与说明**：

```sql
SELECT 
    ROLL_UNIT,
    MTL_NO,
    SPEC_ROLL_UNIT,
    SPEC_MTL_NO,
    PLAN_PROC_SEQ,
    PROD_INST_DTM,
    WK_STA_SCH_DTM
FROM 
    SCH_PLT_PLAN_ROLL
WHERE 
    PROD_INST_DTM IS NOT NULL AND
    WK_STA_SCH_DTM >= SYSDATE
```

说明：查询`SCH_PLT_PLAN_ROLL`表中所有待执行的热次设计计划，其中`PROD_INST_DTM`字段不为空表示生产指令已发送，`WK_STA_SCH_DTM`字段大于或等于当前日期表示计划的预计作业开始时刻尚未开始。

**自动初评**：55/100（{'表命中': 0, '规范': 25, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 26. MES-SYD-01　（提货发货）

**业务场景**：查询某提货单（SYD_DISP_ORD）的明细。

**期望表**：SYD_DISP_ORD, SYD_DISP_ORD_DETAIL　**检查点**：单-明细JOIN

**AI 生成 SQL 与说明**：

```sql
SELECT 
    DORD_NO,
    ORD_NO,
    DORD_LN_NO,
    SALES_PROD_ITEM_CD,
    PROD_IN_DIA,
    PROD_LTH,
    DORD_TOT_P,
    DORD_WGT
FROM 
    SYD_DISP_ORD_DETAIL
WHERE 
    DORD_NO = :paramDORD_NO;
```

说明：根据提供的表结构和业务场景，上述 SQL 查询了指定提货单号（DORD_NO）的明细信息，使用了参数化查询以避免 SQL 注入攻击，并明确列出了需要查询的字段。

**自动初评**：100/100（{'表命中': 40, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 27. MES-SYD-02　（提货发货）

**业务场景**：查询某提货单明细关联的物料信息。

**期望表**：SYD_DISP_ORD_DETAIL, SYD_DISP_ORD_DETAIL_MTL　**检查点**：明细-物料JOIN

**AI 生成 SQL 与说明**：

```sql
SELECT 
    SIM_RM_PUR_RELEASE.SUPPLIER_ITEM_CD,
    MD_MATERIAL.ID AS MATERIAL_ID,
    MD_MATERIAL.U8_CODE,
    MD_MATERIAL.IS_BATCH,
    MD_MATERIAL.THK_RANGE,
    MD_MATERIAL.WTH_RANGE
FROM 
    SIM_RM_PUR_RELEASE
JOIN 
    SIM_RM_SUPP_ITEM ON SIM_RM_PUR_RELEASE.SUPPLIER_ITEM_CD = SIM_RM_SUPP_ITEM.SUPPLIER_ITEM_CD
JOIN 
    MD_MATERIAL ON SIM_RM_SUPP_ITEM.ITEM_CD = MD_MATERIAL.ID
WHERE 
    SIM_RM_PUR_RELEASE.SUPPLIER_ITEM_CD = :param_supplier_item_cd;
```

说明：此查询根据提供的表结构和业务场景，通过供应商项目代码（SUPPLIER_ITEM_CD）关联SIM_RM_PUR_RELEASE和SIM_RM_SUPP_ITEM表，再通过ITEM_CD关联MD_MATERIAL表，以获取与提货单明细关联的物料信息。参数化使用了`:param_supplier_item_cd`来代替直接的字符串拼接，以提高SQL的安全性。

**自动初评**：60/100（{'表命中': 0, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 28. MES-SYD-03　（提货发货）

**业务场景**：统计某期间各提货单的物料数量。

**期望表**：SYD_DISP_ORD, SYD_DISP_ORD_DETAIL_MTL　**检查点**：GROUP BY, 期间过滤

**AI 生成 SQL 与说明**：

```sql
SELECT 
    a.SUPPLIER_ITEM_CD,
    b.SALES_PROD_ITEM_CD,
    SUM(a.RM_ORD_QTY) AS TOTAL_MATERIAL_QTY
FROM 
    SIM_RM_PUR_RELEASE a
JOIN 
    SYM_DISP_ORD_DETAIL b ON a.SUPPLIER_ITEM_CD = b.SALES_PROD_ITEM_CD
WHERE 
    a.IR_CHE_OP_AC_DTM BETWEEN :start_date AND :end_date
GROUP BY 
    a.SUPPLIER_ITEM_CD, 
    b.SALES_PROD_ITEM_CD
```

说明：此 SQL 查询统计了指定期间内，每个提货单（根据供应商项目代码和卷材产品 ERP 项目编号关联）的物料总数量。使用了参数化查询以防止 SQL 注入，并根据业务场景需求，通过 `IR_CHE_OP_AC_DTM` 字段限定了统计的时间范围。

**自动初评**：60/100（{'表命中': 0, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 29. MES-SYD-04　（提货发货）

**业务场景**：查询今日的提货单列表。

**期望表**：SYD_DISP_ORD　**检查点**：日期过滤

**AI 生成 SQL 与说明**：

```sql
SELECT 
    ORD_NO AS "订单编号",
    CUST_CD AS "客户代码",
    PROD_CD AS "产品代码",
    SALES_EMP_ID AS "销售员工ID",
    ORD_RCV_DT AS "订单接收日期",
    ORD_REG_DTM AS "订单注册日期",
    ORD_STS AS "订单状态",
    ARCHIVE_FL AS "归档标志",
    URGENT_FL AS "是否紧急",
    ERROR_FL AS "是否错误",
    EXP_TAX_FL AS "是否退税",
    MACHINE_YN AS "自用材订单委外加工与否",
    IMPORTANT_YN AS "重点客户与否"
FROM 
    SSD_ORDER_HEAD
WHERE 
    ORD_RCV_DT = TRUNC(SYSDATE);
```

说明：此查询用于检索今日接收的提货单列表，通过`ORD_RCV_DT`字段与当前日期的比较来筛选今日的订单。`TRUNC(SYSDATE)`函数用于获取当前日期的整数部分，即今日日期，不包含时间。

**自动初评**：55/100（{'表命中': 0, '规范': 25, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

### 30. MES-SYD-05　（提货发货）

**业务场景**：查询某提货单的完整信息（单头 + 明细 + 物料三层联查）。

**期望表**：SYD_DISP_ORD, SYD_DISP_ORD_DETAIL, SYD_DISP_ORD_DETAIL_MTL　**检查点**：三表JOIN

**AI 生成 SQL 与说明**：

```sql
SELECT 
    s.DORD_NO,
    s.DORD_STS,
    s.DORD_WGT AS "提货单重量",
    s.CUST_CD,
    s.SITE_CD,
    s.ARCHIVE_FL,
    d.SALES_PROD_ITEM_CD,
    d.PROD_IN_DIA,
    d.PROD_LTH,
    d.DORD_TOT_PCS,
    d.DORD_TOT_WGT,
    m.CODE AS "物料编码",
    m.NAME AS "物料名称",
    m.MATERIAL_SPEC,
    m.MATERIAL_TYPE
FROM 
    SYD_DISP_ORD s
JOIN 
    SYD_DISP_ORD_DETAIL d ON s.DORD_NO = d.DORD_NO AND s.DORD_LN_NO = d.DORD_LN_NO
JOIN 
    MD_MATERIAL m ON d.SALES_PROD_ITEM_CD = m.CODE
WHERE 
    s.DORD_NO = :param_dord_no;
```

说明：此 SQL 语句实现了对某提货单的完整信息（单头 + 明细 + 物料三层联查）的查询。参数化用 `:param_dord_no` 替换了直接的字符串拼接，确保了 SQL 注入的安全性。由于表结构中没有提供具体的索引信息，所以没有包含执行计划或索引使用的说明。

**自动初评**：87/100（{'表命中': 27, '规范': 30, '完整性': 20, '说明': 10}）

| 人工评分（0-100）| 语义是否正确 | 问题备注 |
|----|----|----|
|  |  |  |

