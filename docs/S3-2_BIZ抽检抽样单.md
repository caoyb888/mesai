# S3-2 存储过程理解 · BIZ 抽检抽样单

| 项 | 内容 |
|----|----|
| 文件编号 | AI-MES-BIZSAMPLE-S3-2-2026 |
| 需求单 | REQ-MES-AI-20260715-001（T3-2-4）|
| 日期 | 2026-07-15 |
| 抽样规模 | 40 / 1314 张过程卡片（分层随模块占比）|
| 验收目标 | 过程理解正确率 **≥85%**（BIZ 判定）|

## 填写说明（BIZ）

逐条阅读「AI 理解摘要」，对照真实业务，在**判定**列填 `正确` / `部分正确` / `错误`；
`部分正确`/`错误` 请在**问题备注**列写明错在哪。完成后回填下方汇总。

> 计分：正确=1、部分正确=0.5、错误=0；正确率 =(Σ得分)/条数。<85% 触发对应模块补训（T3-2-2）。

## 抽样分布

| 模块前缀 | 抽样数 |
|----|----|
| BSCH | 10 |
| BSCR | 1 |
| BSCT | 4 |
| BSDA | 2 |
| BSIF | 1 |
| BSIM | 2 |
| BSMS | 4 |
| BSPG | 2 |
| BSPR | 6 |
| BSQM | 8 |

## 汇总（BIZ 填）

| 指标 | 值 |
|----|----|
| 正确 | ___ |
| 部分正确 | ___ |
| 错误 | ___ |
| **正确率** | ___%（目标 ≥85%）|
| 是否达标 | ☐ 达标　☐ 未达标（列补训模块）|
| BIZ 签字 / 日期 | ________ |

---

## 抽检明细

### 1. `BSCH_B0025.F_GET_MAX_BATCH_SEQ`　（模块 BSCH）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `F_GET_MAX_BATCH_SEQ` 用于生成一个批次号（`BATCH_CD`）。具体来说，它根据当前日期生成一个以特定格式（'S' + 当前年月日）开始的批次号，并在该日期后附加一个数字序列，该数字序列是当前最大批次号的数字部分加1。

### 2. **业务规则**
- **关键判断**：子程序首先从 `SCH_PLT_PLAN_ROLL` 表中查询符合条件的最大批次号，条件是批次号的前7位为当前日期的年月日（格式为'YYMMDD'），并且规格接收日期（`SPEC_RCV_DTM`）与当前日期相同。
- **分支逻辑**：如果查询结果为空，则 `V_BATCH_CDS` 被设置为0，否则为查询到的最大批次号的数字部分加1。
- **校验逻辑**：没有明显的校验逻辑，子程序假设 `SUBSTR` 和 `TO_NUMBER` 函数能够正确处理输入数据。

### 3. **状态流转**
子程序中没有涉及任何状态字段的更新，因此没有状态流转。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 2. `BSCH_B0025S.PR_UPDATE_HEAD`　（模块 BSCH）

**AI 理解摘要**：

### 1. **用途**
这个子程序`PR_UPDATE_HEAD`用于更新钢厂MES系统中的钢板头部信息。根据输入参数，它检查是否存在拆批后的信息，并根据条件更新或插入新的钢板头部信息。

### 2. **业务规则**
- **关键判断、分支、校验逻辑**：
  - 首先，通过查询`SPR_ROLLING_RLST`表和`SPR_PLATE_HEAD`表来确定是否已经存在拆批后的信息。
  - 根据`P_ROLL_UNITS`是否为`NULL`来判断是否需要修改规格。
  - 如果`P_ROLL_UNITS`为`NULL`，则根据`V_COUNT`的值（表示`SPR_PLATE_HEAD`表中`BATCH_CD`为`P_BATCH_CDS`的记录数）来决定是插入新记录还是更新现有记录。
  - 如果`P_ROLL_UNITS`不为`NULL`，则同样根据`V_COUNT`的值来决定操作，但还会更新`ORD_THK`、`ORD_WTH`和`ORD_LTH`字段为传入的`P_PROD_THK`、`P_PROD_WTH`和`P_PROD_LTH`值。

### 3. **状态流转**
- **字段=值及触发条件**：
  - `SLAB_NUMBER = NVL(GF_SPR_PLATE_HEAD.T_REC.SLAB_NUMBER,0)+1`：当`P_ROLL_UNITS`为`NULL`且`V_COUNT`为`0`时，或当`P_ROLL_UNITS`不为`NULL`时。
  - `COLLECT_SLAB_NUMBER = NVL(GF_SPR_PLATE_HEAD.T_REC.COLLECT_SLAB_NUMBER,0)+1`：同上。
  - `FCE_CH_NUMBER = NVL(GF_SPR_PLATE_HEAD.T_REC.FCE_CH_NUMBER,0)+1`：同上。
  - `SUM_NUMBER = NVL(GF_SPR_PLATE_HEAD.T_REC.SUM_NUMBER,0)+1`：同上。
  - `HTM_MTH_CD = P_DELIVERY…

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 3. `BSCH_BATCHA_PLT_JOB2.PR_SAVE_SLAB_DGN_RSLT`　（模块 BSCH）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `PR_SAVE_SLAB_DGN_RSLT` 用于保存钢坯设计结果。它接收一系列的参数，包括订单号、订单行号、设计数量、设计长度等，然后根据这些参数更新钢坯设计订单的信息，并计算钢坯的重量。

### 2. **业务规则**
- **参数校验**：如果 `P_ORD_NO` 或 `P_ORD_LN` 为空，则设置错误信息。
- **设计数量校验**：如果 `P_DGN_PLT_PCS1` 为0，则设置错误信息。
- **行号和行数校验**：如果 `P_ROW_CNT` 小于 `P_ROW_NO`，则直接返回。
- **设计参数校验**：如果 `P_ORD_SIZE_TY` 为 'C' 或 'D' 且 `P_DGN_PLT_PCS2`、`P_DGN_OVROLL_PCS2`、`P_DGN_PLT_LTH2` 中任一大于0，则设置错误信息。
- **复数设计校验**：如果 `P_DBL_YN` 为 'Y'，则在最后一行执行 `PR_SAVE_MP_PROC` 过程；否则执行 `PR_SAVE_LAST_PROC` 过程。
- **设计订单数限制**：如果设计订单数超过9，则设置错误信息。
- **宽度设计限制**：如果订单长度大于14000且板坯宽度与订单宽度之差小于100mm，则设置错误信息（此规则被注释）。

### 3. **状态流转**
- **字段=值** 及触发条件：
  - `GF_SCH_SLAB_DESIGN_ORD.T_REC.SLAB_DGN_THK` 设置为 `P_N_INPUT_SLAB_THK`。
  - `GF_SCH_SLAB_DESIGN_ORD.T_REC.SLAB_DGN_WTH` 设置为 `P_N_INPUT_SLAB_WTH`。
  - `GF_SCH_SLAB_DESIGN_ORD.T_REC.SLAB_DGN_LTH` 设置为 `P_N_INPUT_SLAB_LTH`。
  - `GF_SCH_SLAB_DESIGN_ORD.T_REC.SLAB_DGN_WGT` 计算为 `P_N_IN…

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 4. `BSCH_BATCH_SELECT2.PR_ADD_ORD_COPY`　（模块 BSCH）

**AI 理解摘要**：

### 1. **用途**
这个子程序`PR_ADD_ORD_COPY`主要用于从不同的订单表中复制符合条件的订单数据到`SCH_SLAB_DESIGN_ORDT`表中。它接收一系列的输入参数，包括产品组、质量完成日期、订单号、规格代码等，然后根据这些参数筛选出符合条件的订单记录，并将这些记录的详细信息复制到目标表中。

### 2. **业务规则**
- **数据筛选**：通过一系列的条件判断，筛选出符合特定标准的订单记录。这些条件包括产品组、质量完成日期、订单号、规格代码、未完成钢号、目标标志等。
- **数据复制**：对于每个筛选出的订单记录，将其详细信息复制到`SCH_SLAB_DESIGN_ORDT`表中。复制过程中，会根据订单记录的某些字段值进行一些计算和转换。
- **异常处理**：在调用另一个过程`PR_SELECT_ORD_COPY`时，如果发生异常，则捕获异常并设置错误信息。

### 3. **状态流转**
- `GF_SCH_SLAB_DESIGN_ORDT.T_REC.TARGET_FL := 'T';`：设置目标标志为'T'，对于所有复制的订单记录。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 5. `BSCH_G0025.PR_SELECT_PLAN`　（模块 BSCH）

**AI 理解摘要**：

1. **用途**：
   这个子程序`PR_SELECT_PLAN`用于查询指定年月`P_YEAR_MONTH`在`SCH_PLAN_SINTER_BURDENING_ZXH`表中记录的数量，并将查询结果通过游标`P_CUR`输出。

2. **业务规则**：
   - 关键判断：检查输入参数`P_YEAR_MONTH`是否为`NULL`。
   - 分支逻辑：
     - 如果`P_YEAR_MONTH`为`NULL`，则调用`PE.PR_SET_ERROR`过程，设置错误信息为“请选择月份！”。
     - 如果`P_YEAR_MONTH`不为`NULL`，则打开游标`P_CUR`，执行查询统计指定年月的记录数。

3. **状态流转**：
   - 无状态流转操作，子程序中没有对任何表的状态字段进行赋值。

4. **读写副作用**：
   - 读取表：`SCH_PLAN_SINTER_BURDENING_ZXH`。
   - 写入表：无写入操作，子程序中没有执行任何DML操作。

5. **调用依赖**：
   - 调用了`PE.PR_SET_ERROR`过程，用于设置错误信息。

6. **风险与不确定点**：
   - 动态SQL盲区：无动态SQL语句，整个查询是静态的。
   - 语义不明处：
     - `PE.PR_SET_ERROR`过程的具体实现未知，需要进一步补充其功能和行为。
     - 游标`P_CUR`的具体使用方式和后续处理逻辑未在代码中体现，需要进一步补充。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 6. `BSCH_PLAN_SEARCH.PR_SEARCH_CAST_NO_LIST3`　（模块 BSCH）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `PR_SEARCH_CAST_NO_LIST3` 用于查询特定工厂代码（`P_FAC_CD`）下的铸坯编号（`CAST_NO`）列表，以及与之相关的一系列统计信息，包括不同状态的加热次数、重量、钢种、规格等级等。

### 2. **业务规则**
- **工厂代码匹配**：通过 `DECODE(SUBSTR(PROD_CD, 1, 2), 'GP', '2', '1') LIKE P_FAC_CD || '%'` 判断 `PROD_CD` 的前两位是否符合工厂代码，符合则进行后续查询。
- **日期范围筛选**：`SPEC_RCV_DTM` 字段的值必须在 `P_WORK_SPEC_RCP_DTM_S` 和 `P_WORK_SPEC_RCP_DTM_D` 之间。
- **完成类型判断**：`P_FINISH_TY` 参数用于确定计划完成状态，如果为 'P' 且 `PLAN_HEAT_STS` 在特定状态内，则结果为 'P'，否则为 'A'。

### 3. **状态流转**
- 此子程序中没有直接的 `UPDATE`、`SET` 语句对状态字段进行赋值，因此没有状态流转。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 7. `BSCH_PLAN_SEARCH.PR_SEARCH_ROLL_LIST`　（模块 BSCH）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `PR_SEARCH_ROLL_LIST` 用于查询钢厂的生产计划中的钢卷列表。它根据提供的参数，如接收日期、物料编号、订单信息等，从数据库中检索相关的钢卷信息，并将其结果集返回给调用者。

### 2. **业务规则**
- **关键判断、分支、校验逻辑**：
  - 子程序首先检查 `P_FAC_CD` 参数是否等于2或者 `P_ORD_PLT_CD` 是否非空。这个条件决定了使用哪个查询逻辑。
  - 如果条件成立，使用第一个查询逻辑，从 `SCH_PLT_PLAN_ROLL` 和 `SQM_ORD_COM` 表中查询数据。
  - 如果条件不成立，使用第二个查询逻辑，从 `SCH_PLAN_ROLL` 和 `SQM_ORD_COM` 表中查询数据。
  - 在两个查询逻辑中，都会根据提供的参数（如 `P_WORK_SPEC_RCP_DTM_S`, `P_WORK_SPEC_RCP_DTM_D`, `P_MTL_NO` 等）进行过滤和匹配。

### 3. **状态流转**
- 这个子程序没有直接对任何表的状态字段进行更新或赋值操作。它仅负责查询数据，并将结果集返回给调用者。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 8. `BSCH_PLAN_TIME_SCHEDULE.PR_INIT_TIME_SCHEDULE`　（模块 BSCH）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `PR_INIT_TIME_SCHEDULE` 用于初始化和计算钢厂的生产计划时间表。具体来说，它通过接收一个浇次编号数组 `P_CAST_NO_ARRAY`，来确定哪些浇次需要被计算时间，并据此更新相关的计划时间表。

### 2. **业务规则**
- **输入校验**：首先检查输入的浇次编号数组 `P_CAST_NO_ARRAY` 是否为空，如果为空，则通过 `PE.PR_SET_ERROR` 抛出错误信息。
- **浇次编号处理**：从输入的浇次编号数组中提取最大编号 `V_CAST_NO_MAX`，用于后续的数据过滤和处理。
- **数据初始化**：调用 `PR_INIT_TIME_STD_DATA` 过程来初始化标准时间数据。
- **临时表清空与数据插入**：清空 `SCH_TEMP_HEAT_SCHEDULE` 临时表，并根据 `V_CAST_NO_MAX` 往该表中插入数据，通过 `PR_SET_TEMP_HEAT_SCHEDULE` 过程实现。
- **浇次排序与时间设置**：根据生产指令的有无（`PROD_INST_YN`），对浇次进行排序，并分别为每个浇次设置实际结果和结束时间（`PR_SET_TIME_RESULT`），以及处理时间（`PR_HEAT_TIME_SCHEDULE`）。
- **主表更新**：将临时表 `SCH_TEMP_HEAT_SCHEDULE` 的数据更新到主表中，通过 `PR_SET_TEMP_TO_MAIN_TABLE` 过程实现。

### 3. **状态流转**
- **字段=值** 及触发条件：
  - `PROD_INST_YN = 'Y'` 或 `PROD_INST_YN = 'N'`：根据这个字段的值，对 `SCH_TEMP_HEAT_SCHEDULE` 表中的浇次进行分组和排序。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 9. `BSCH_PLAN_TIME_SCHEDULE2.FC_GET_PROC_WORK_TM`　（模块 BSCH）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `FC_GET_PROC_WORK_TM` 用于根据给定的参数计算或检索特定工艺（`P_PROC_CD`）的工作时间（`V_WORK_TM`）。具体来说，如果工艺代码是 'LC'，则调用另一个函数 `FC_GET_CC_WORK_TM` 来获取工作时间；否则，从 `SCH_TIME_SCHEDULE_STD` 表中查询并返回工作时间。

### 2. **业务规则**
- **关键判断**：子程序首先检查 `P_PROC_CD` 参数是否等于 'LC'。
  - 如果等于 'LC'，则调用 `FC_GET_CC_WORK_TM` 函数，传入钢种等级（`P_STEEL_GRD`）、板坯厚度（`P_SLAB_THK`）、板坯宽度（`P_SLAB_WTH`）和板坯总长度（`P_SLAB_TOT_LTH`）。
  - 如果不等于 'LC'，则从 `SCH_TIME_SCHEDULE_STD` 表中查询工作时间，根据 `P_WORK_TM_FLAG` 参数选择不同的时间字段（`WORK_AIM_TM`、`WORK_MIN_TM` 或 `WORK_MAX_TM`）。
- **分支逻辑**：根据 `P_PROC_CD` 的值决定是调用另一个函数还是从数据库表中查询数据。

### 3. **状态流转**
- 子程序中没有直接的状态流转语句，因为它不涉及更新数据库表的状态字段。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 10. `BSCH_PROD_INST.FC_GET_COIL_STRAP_PTRN2`　（模块 BSCH）

**AI 理解摘要**：

1. **用途**：
这个子程序`FC_GET_COIL_STRAP_PTRN2`的作用是根据输入的参数（包括钢带类型`P_STRAP_TY`、订单类型`P_ORD_TY`、包装方法代码`P_PACK_MTH_CD`、屈服强度`P_YIELD_STRENGTH`、钢卷厚度`P_COIL_THK`和宽度`P_COIL_WTH`），来确定一个特定的钢带图案（`V_PTRN`）。这个函数返回一个`VARCHAR`类型的值，代表确定的钢带图案。

2. **业务规则**：
- 首先，根据屈服强度`P_YIELD_STRENGTH`的值，确定`V_YIELD_RELA`的值，如果屈服强度大于等于345，则`V_YIELD_RELA`为2，否则为0。
- 根据订单类型`P_ORD_TY`，如果不等于'L'，则从`SCH_HCOIL_STRAP_STD2`表中查询对应的钢带图案；如果等于'L'，则除了上述条件外，还要求查询结果只有一条记录（`ROWNUM = 1`）。
- 如果查询失败（即`V_PTRN`为NULL），则根据钢带类型`P_STRAP_TY`调用`FC_BIZ_RULE_RSLT`函数来获取钢带图案。

3. **状态流转**：
这个子程序没有对任何状态字段进行赋值操作，因此没有状态流转。

4. **读写副作用**：
- **读取**：从`SCH_HCOIL_STRAP_STD2`表中读取数据。
- **写入**：没有写入任何表。

5. **调用依赖**：
- 调用了`FC_BIZ_RULE_RSLT`函数，用于在查询失败时获取钢带图案。

6. **风险与不确定点**：
- 动态SQL盲区：`FC_BIZ_RULE_RSLT`函数的具体实现和逻辑未在代码中给出，因此无法确定其具体行为和可能的副作用。
- 语义不明处：代码中的注释`/* PKG_LOG.PR_ADD_LOG...`可能表示日志记录功能，但由于被注释掉，其实际作用和影响未知，标为「待补充」。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 11. `BSCR_INDICATOR_ALL.CHECK_IH_MATCH_INDICATOR`　（模块 BSCR）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `check_ih_match_indicator` 用于检查给定的点位号（`p_ih_no`）和指标ID（`p_indicator_id`）是否匹配，并确定是否需要进行新增、修改关联或给出提示让用户做判断。

### 2. **业务规则**
- **点位参数为空**：首先检查点位参数是否为空。
  - 如果为空，再检查指标是否之前关联过点位。
    - 如果没有关联过，返回标志为`N`，表示无操作。
    - 如果关联过，返回标志为`E`，提示用户是否解除关联。
- **点位号不为空**：检查点位号是否包含非法字符（汉字、'+'、',“）。
  - 如果包含非法字符，返回标志为`N`，表示无操作。
  - 如果不包含非法字符，再检查点位号是否已在基表存在。
    - 如果点位号不存在，返回标志为`Y`，表示执行新增+关联。
    - 如果点位号存在，再判断是否有关联指标ID。
      - 如果没有关联任何指标，返回标志为`Y`，表示执行关联。
      - 如果有关联指标，再判断关联的指标是否为本指标。
        - 如果是本指标，返回标志为`Y`，表示无操作。
        - 如果不是本指标，返回标志为`E`，提示用户是否解除点位原有关联，再关联本指标。

### 3. **状态流转**
- 无直接的 UPDATE 或 SET 语句对状态字段赋值。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 12. `BSCT_COST_LA.BATCH_DEL`　（模块 BSCT）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `BATCH_DEL` 用于删除指定用户和批次号的 `sct_day_report_batch` 表中的记录。

### 2. **业务规则**
- 关键判断逻辑：子程序接收两个参数 `p_user_id` 和 `p_batch_id`，使用这两个参数作为条件来删除 `sct_day_report_batch` 表中的记录。
- 分支逻辑：没有明显的分支逻辑，子程序直接执行 DELETE 语句。
- 校验逻辑：没有显式的校验逻辑，直接根据传入的参数进行删除操作。

### 3. **状态流转**
- 此子程序中没有涉及到状态字段的赋值操作，因此没有状态流转。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 13. `BSCT_COST_LA.INV_TRANS_SAVE`　（模块 BSCT）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `INV_TRANS_SAVE` 用于保存或更新库存交易记录。具体来说，它根据传入的参数，如果 `p_trans_id` 为 `NULL`，则创建一条新的库存交易记录；如果 `p_trans_id` 非 `NULL`，则更新指定的库存交易记录。

### 2. **业务规则**
- **新建记录**：如果 `p_trans_id` 为 `NULL`，则执行以下操作：
  - 清空 `gf_sct_inv_transaction` 的记录。
  - 为新记录生成 `trans_id`。
  - 设置交易日期、库存代码、物料代码、物料来源、对象 ID、项目 ID、物料名称、规格代码、钢种和交易数量。
  - 插入新记录。
- **更新记录**：如果 `p_trans_id` 非 `NULL`，则执行以下操作：
  - 检查指定 `trans_id` 的记录是否存在且状态为“已发布成本”。
  - 如果状态为“已发布成本”，则设置错误信息，不允许修改。
  - 如果状态允许修改，则更新记录的交易日期、库存代码、物料代码、对象 ID、项目 ID、物料名称、规格代码、钢种和交易数量。
  - 检查更新后的成本表与成本项是否匹配。
  - 如果不匹配，则设置错误信息。

### 3. **状态流转**
- **字段=值**：
  - `gf_sct_inv_transaction.t_rec.status`：未直接设置，但注释中提到可能设置为“已处理”。
  - `l_status`：从数据库查询获取，可能值为“已发布成本”或“NODATA”。
- **触发条件**：
  - `l_status = '已发布成本'`：不允许修改记录。
  - `l_status = 'NODATA'`：允许修改记录。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 14. `BSCT_COST_LA.UNIT_COST_AUTO`　（模块 BSCT）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `unit_cost_auto` 用于自动更新或插入单位成本信息。根据提供的月份、对象ID、项目ID、单位成本和用户ID，该过程会检查是否已存在对应的单位成本记录。如果不存在，则插入一条新记录；如果存在，则更新该记录的单位成本、更新时间和更新用户。

### 2. **业务规则**
- **关键判断**：通过查询 `sct_unit_cost_auto` 表，检查是否存在与输入参数匹配的记录（即相同的成本月份和项目ID）。
- **分支逻辑**：
  - 如果 `l_counts = 0`（即没有找到匹配的记录），则执行插入操作，将新的单位成本信息插入到 `sct_unit_cost_auto` 表中。
  - 如果 `l_counts ≠ 0`（即找到匹配的记录），则执行更新操作，更新该记录的单位成本、更新时间和更新用户。

### 3. **状态流转**
- **字段=值及触发条件**：
  - `unit_cost = p_unit_cost`：当找到匹配的记录时，更新单位成本。
  - `upd_user = p_user_id`：无论是插入还是更新操作，都会设置更新用户为 `p_user_id`。
  - `upd_tm = to_char(sysdate, 'yyyy-mm-dd HH24:Mi:SS')`：无论是插入还是更新操作，都会将更新时间设置为当前系统时间。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 15. `BSCT_COST_PUBLIC.MATERIAL_DEL_SINGLE`　（模块 BSCT）

**AI 理解摘要**：

## 1. **用途**
这个子程序 `BSCT_COST_PUBLIC.MATERIAL_DEL_SINGLE` 用于删除特定的物料信息。具体来说，它通过传递的 `p_object_id`、`p_item_id` 和 `p_material_code` 参数来指定要删除的物料条目。

## 2. **业务规则**
- 关键判断、分支、校验逻辑：此子程序中没有明显的业务规则判断或分支逻辑。它直接调用了两个过程：`gf_sct_item_material.pr_select` 和 `gf_sct_item_material.pr_delete`，具体的选择和删除逻辑可能在这两个过程中实现。

## 3. **状态流转**
- 此子程序中没有直接的状态流转语句，如 `UPDATE ... SET x_st='..'`。状态流转可能在被调用的过程 `gf_sct_item_material.pr_delete` 中实现。

## 4. **读写副作用**
- **读取表**：`sct_item_material` 表，通过 `gf_sct_item_material.pr_select` 过程读取。
- **写入表及DML类型**：`sct_item_material` 表，通过 `gf_sct_item_material.pr_delete` 过程执行 `DELETE` 操作。

## 5. **调用依赖**
- `gf_sct_item_material.pr_select`：用于选择特定的物料条目。
- `gf_sct_item_material.pr_delete`：用于删除特定的物料条目。

## 6. **风险与不确定点**
- **动态 SQL 盲区**：`gf_sct_item_material.pr_select` 和 `gf_sct_item_material.pr_delete` 过程的具体实现未在源码中给出，因此无法确定是否存在动态 SQL 或其他潜在的风险点。标为「待补充」。
- **语义不明处**：由于缺少对 `gf_sct_item_materi…

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 16. `BSDA_M0001.PR_SAVE_LCWL`　（模块 BSDA）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `PR_SAVE_LCWL` 用于更新 `SIF_BOF_ITEM_CONF` 表中的记录。它接收多个参数，这些参数对应于表中的字段，并将这些参数的值更新到表中对应的记录。

### 2. **业务规则**
- 关键判断、分支、校验逻辑：
  - 子程序首先调用 `GF_SIF_BOF_ITEM_CONF.PR_SELECT` 过程，这可能用于检查 `P_ID` 参数指定的记录是否存在。
  - 然后，它将传入的参数值赋给 `GF_SIF_BOF_ITEM_CONF.T_REC` 记录类型的相应字段。
  - 最后，调用 `GF_SIF_BOF_ITEM_CONF.PR_UPDATE` 过程，这可能用于将更新后的记录保存到数据库中。

### 3. **状态流转**
- 形如 `UPDATE ... SET x_st='..'` / 对状态字段赋值的语句：
  - 由于源码中没有直接的 `UPDATE` 语句，状态流转的具体字段和值无法从代码中直接得出。状态流转依赖于 `GF_SIF_BOF_ITEM_CONF.PR_UPDATE` 过程的实现，这部分代码未给出，因此具体的状态流转「字段=值」及触发条件无法确定。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 17. `BSDA_M0001.PR_SEARCH_PILE_PDI`　（模块 BSDA）

**AI 理解摘要**：

1. **用途**：
这个子程序 `PR_SEARCH_PILE_PDI` 用于查询 `SIF_PILE_DATA` 表中与特定钢板ID（`P_PIECEID`）相关的堆叠数据（pile data），并且这些数据的创建时间（`CRT_TM`）在指定的时间范围（`P_RLG_DTM_FR` 到 `P_RLG_DTM_TO`）内，以及消息ID（`MSGID`）为4131。查询结果通过游标 `P_CUR` 输出。

2. **业务规则**：
- 关键判断：查询 `SIF_PILE_DATA` 表中的数据，其中创建时间在 `P_RLG_DTM_FR` 和 `P_RLG_DTM_TO` 之间，钢板ID包含 `P_PIECEID`，且消息ID为4131。
- 分支、校验逻辑：无明显的分支或校验逻辑，子程序直接执行查询操作。

3. **状态流转**：
- 无状态流转，子程序中没有对任何表的状态字段进行更新。

4. **读写副作用**：
- 读取：`SIF_PILE_DATA` 表。
- 写入：无写入操作，子程序仅进行查询。

5. **调用依赖**：
- 子程序中没有直接调用其他过程或函数，但使用了 `TO_DATE` 函数将字符串转换为日期格式。

6. **风险与不确定点**：
- 动态 SQL 盲区：无动态 SQL 使用。
- 语义不明处：
  - `P_PIECEID` 参数的具体含义和来源待补充。
  - `P_RLG_DTM_FR` 和 `P_RLG_DTM_TO` 参数的具体含义和格式待补充。
  - `MSGID` 为4131的具体业务含义待补充。
  - `SIF_PILE_DATA` 表的结构和字段含义待补充。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 18. `BSIF_MES_TO_ERP_RET.PR_CONFIRM_SMM_TRANSMISSION_ERP_SUM`　（模块 BSIF）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `PR_CONFIRM_SMM_TRANSMISSION_ERP_SUM` 用于处理 `SMM_TRANSMISSION_ERP_SUM` 表中的记录。具体来说，它根据输入参数 `P_INF_DEAL` 的值来决定是否更新记录的状态。

### 2. **业务规则**
- **关键判断**：子程序首先检查输入参数 `P_INF_DEAL` 的值。
  - 如果 `P_INF_DEAL` 等于 `'N'`，则执行更新操作。
  - 如果 `P_INF_DEAL` 等于其他值，则调用 `PE.PR_SET_ERROR` 函数显示错误信息，表示该记录已处理，不能修改。
- **分支逻辑**：
  - **更新操作**：如果 `P_INF_DEAL` 为 `'N'`，则将 `SMM_TRANSMISSION_ERP_SUM` 表中对应 `REPORT_ID` 的记录的 `INF_DEAL` 字段设置为 `'0'`，`CANCEL_DT` 设置为当前日期，`CANCEL_USER` 设置为当前用户 ID。
  - **错误处理**：如果 `P_INF_DEAL` 不为 `'N'`，则显示错误信息。

### 3. **状态流转**
- **字段=值** 及触发条件：
  - `INF_DEAL = '0'`：当 `P_INF_DEAL = 'N'` 时。
  - `CANCEL_DT = SYSDATE`：当 `P_INF_DEAL = 'N'` 时。
  - `CANCEL_USER = fc_user_id()`：当 `P_INF_DEAL = 'N'` 时。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 19. `BSIM_BF_INFO.PR_CALC_FINE_CK_USE_QTY`　（模块 BSIM）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `PR_CALC_FINE_CK_USE_QTY` 用于计算细焦炭的使用量，并进行相关的业务处理。

### 2. **业务规则**
- 子程序接受一个参数 `P_IR_CHE_OP_AC_DT`，表示操作日期。
- 使用常量 `C_DATA_CYCLE_1_DAY` 和 `C_PROC_CD_ST1` 分别表示数据周期和处理代码。
- 调用 `BSIM_BIZ_COMMON.PR_CALC_FINE_CK_USE_QTY` 过程，传入处理后的日期 `FC_OPER_DT(P_IR_CHE_OP_AC_DT)` 来计算细焦炭的使用量。
- 调用 `BSIM_BIZ_COMMON.PR_CALC_CO_PUR_ITEM` 过程，传入数据周期、操作日期、处理代码和输入类型，进行材料采购项的计算。
- 调用 `BSIM_BIZ_COMMON.PR_SAVE_CO_PUR_MTRL_ITEM` 过程，保存材料采购项信息。

### 3. **状态流转**
- 源码中没有直接体现对状态字段的赋值操作，因此无法列出具体的字段和值。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 20. `BSIM_BIZ_COMMON.PR_ST_USE_PUR_BRAND_ITEM`　（模块 BSIM）

**AI 理解摘要**：

### 1. **用途**
这个子程序`PR_ST_USE_PUR_BRAND_ITEM`主要用于处理和更新与采购品牌物料相关的数据。它涉及到检查操作结果、混合物料使用情况，并据此更新采购品牌物料的相关信息。

### 2. **业务规则**
- **关键判断、分支、校验逻辑**：
  - 首先检查`SIM_ST_BLD_OPER_RSLT`表中是否存在对应`DATA_CYCLE`、`IR_CHE_OP_AC_DTM`和`PROC_CD`的记录，如果不存在，则记录日志并返回。
  - 接着检查`SIM_ST_MIX_MTRL_USED_LINE`表中是否存在对应`DATA_CYCLE`、`IR_CHE_OP_AC_DTM`和`PROC_CD`的记录，如果不存在，同样记录日志并返回。
  - 删除`SIM_CO_PUR_BRAND_ITEM`表中特定条件下的记录。
  - 通过`FC_BIZ_RULE_RSLT_BY_CD`函数获取混合矿石和自烧矿石的品牌代码。
  - 遍历`SIM_ST_MIX_MTRL_USED_LINE`和`SIM_RM_SUPP_ITEM`表，对于不在混合矿石和自烧矿石品牌代码中的物料，创建或更新`SIM_CO_PUR_BRAND_ITEM`表中的记录。
  - 对于混合矿石，计算每日使用量，并据此更新`SIM_CO_PUR_BRAND_ITEM`表中的记录。

### 3. **状态流转**
- **字段=值及触发条件**：
  - 无直接的状态字段更新语句，但通过DML操作间接影响状态。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 21. `BSMS_A5310.F_GEN_SLAB_NO`　（模块 BSMS）

**AI 理解摘要**：

1. **用途**：
   这个子程序 `F_GEN_SLAB_NO` 用于生成钢厂中的板坯编号（SLAB_NO）。它接收一个热处理编号（HEAT_NO）作为输入，并根据该编号生成对应的板坯编号。

2. **业务规则**：
   - 首先，子程序通过查询 `SMS_SLAB_BY_HEAT` 表来获取与输入的 `P_HEAT_NO` 相关联的最大板坯编号（MAX(T.SLAB_NO)）。
   - 如果查询结果为空（即 `NVL` 函数返回 'XXXXXXXXXXX'），则生成的板坯编号为输入的热处理编号后接 '1'。
   - 如果查询结果不为空，则提取最大板坯编号的最后一个字符（代表序列），将其转换为数字并加 1，生成新的序列编号。
   - 如果新的序列编号大于 9，则调用 `PE.PR_SET_ERROR` 过程设置错误信息，提示“一炉不能录入9次剪切实绩”。
   - 最终，生成的板坯编号由热处理编号和新的序列编号组成。

3. **状态流转**：
   - 子程序中没有直接的 `UPDATE`、`SET` 语句对状态字段进行赋值，因此没有状态流转。

4. **读写副作用**：
   - **读取**：子程序读取了 `SMS_SLAB_BY_HEAT` 表来获取最大板坯编号。
   - **写入**：子程序没有写入任何表，它仅返回生成的板坯编号。

5. **调用依赖**：
   - 子程序调用了 `PE.PR_SET_ERROR` 过程来设置错误信息。

6. **风险与不确定点**：
   - 动态 SQL 盲区：无。
   - 语义不明处：
     - `PE.PR_SET_ERROR` 过程的具体实现和行为未知，需要进一步的信息来确定其行为。
     - `SMS_SLAB_BY_HEAT` 表的结构和 `SLAB_NO` 字段的具体格式未知，特别是如何确定板坯编号的序列部分。
     - 子程序中的 'XXXXXXXXXXX' 值的具体含义和使用场景需要进一步的业务背景信息。
     - 子程序如何处理 `PE.PR_SET_ERROR`…

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 22. `BSMS_COMMON.GET_RSLT_SEQ`　（模块 BSMS）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `GET_RSLT_SEQ` 的用途是根据输入参数 `P_TYPE`、`P_PRP_HEAT_NO`、`P_HEAT_NO`、`P_PROC_PASS_CNT` 和 `P_PROC_CD` 来获取或生成一个结果序列编号 `N_RSLT_SEQ`。这个编号用于不同的结果记录表中，以确保每个结果记录都有一个唯一的序列编号。

### 2. **业务规则**
- **关键判断、分支、校验逻辑**：
  - 首先，根据 `P_PROC_CD` 的值决定使用 `P_PRP_HEAT_NO` 还是 `P_HEAT_NO` 作为热号。
  - 然后，根据 `P_TYPE` 的值，选择不同的表和条件来查询最大 `RSLT_SEQ` 值，并在此基础上加1来生成新的 `RSLT_SEQ`。
  - 如果 `P_TYPE` 的值不在预定义的范围内，将调用错误处理函数 `PE.PR_SET_ERROR` 来设置错误信息。

### 3. **状态流转**
- 这个子程序没有直接对任何状态字段进行赋值，因此没有状态流转的语句。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 23. `BSMS_OPER_BOF.PR_SAVE_BOF_DEP`　（模块 BSMS）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `PR_SAVE_BOF_DEP` 主要用于保存与锅炉（BOF）相关的操作数据。它接收一系列与锅炉操作相关的参数，并进行数据验证、处理后，更新或插入锅炉操作结果数据。

### 2. **业务规则**
- **参数验证**：对输入参数进行非空、日期范围、温度和重量的校验。
- **日期范围校验**：确保操作日期在合理范围内，例如充电开始日期和结束日期、吹扫开始和结束日期等。
- **温度和重量校验**：对实际温度和废料总重量进行校验。
- **处理时间校验**：检查处理时间是否符合预期。
- **数据更新或插入**：根据传入的 `P_JQX_RS` 参数决定是更新还是插入数据。

### 3. **状态流转**
- **字段=值** 及触发条件：
  - `GF_SMS_RSLT_BOF.T_REC.SCRAP_TOT_WGT` = `P_SCRAP_TOT_WGT * N_UNIT`：当 `P_SCRAP_TOT_WGT` 不为空时。
  - `GF_SMS_RSLT_BOF.T_REC.SURF_MSU_CHARG_WGT` = `P_SURF_MSU_CHARG_WGT * N_UNIT`：当 `P_SURF_MSU_CHARG_WGT` 不为空时。
  - `GF_SMS_RSLT_BOF.T_REC.TAP_STA_DTM` = `NVL(P_TAP_STA_DTM, TO_CHAR(SYSDATE, 'YYYYMMDDHH24MISS'))`：当 `P_TAP_STA_DTM` 为空时，使用系统当前时间。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 24. `BSMS_OPER_HEAT.PR_STD_HEAT_RSLT`　（模块 BSMS）

**AI 理解摘要**：

### 1. **用途**
这个子程序`PR_STD_HEAT_RSLT`主要用于处理钢厂MES系统中关于“加热”（Heat）的标准结果数据。它根据提供的事件代码（`P_EVENT_CD`）和加热编号（`P_HEAT_NO`），进行一系列的数据查询、计算和更新操作，最终将处理结果同步到ERP系统中。

### 2. **业务规则**
- **加热重量计算**：通过查询`SMS_RSLT_CUT`表，计算给定加热编号的总切割重量，并乘以1.02得到`V_HEAT_WGT`。
- **坯料重量（PI_WGT）调整**：根据`SMS_KR_LD_WEIGHT`表中的记录，调整坯料重量，确保其在一定范围内。
- **事件类型判断**：如果`P_EVENT_CD`为'P'，执行一系列ERP数据同步操作。
- **材料消耗处理**：根据`SMS_MAT_CONSUM`表中的数据，处理材料消耗信息，并更新到ERP临时表中。
- **资源使用记录**：根据`SMS_RSLT_KR`、`SMS_RSLT_BOF`、`SMS_RSLT_LF`和`SMS_RSLT_RH`表中的数据，记录资源使用情况。

### 3. **状态流转**
- **字段=值及触发条件**：
  - `GF_SMS_HEAT_ERP_TEMP.T_REC.ERP_TRANSACTION_TY := '02'`：当`P_EVENT_CD`为'P'时。
  - `GF_SMS_HEAT_ERP_TEMP.T_REC.PROC_TY := 'C'`：当`P_EVENT_CD`为'P'时。
  - `GF_SMS_HEAT_ERP_TEMP.T_REC.ERP_TRANSACTION_TY := '22'`：当`P_EVENT_CD`不为'P'且记录已存在时。
  - `GF_SMS_HEAT_ERP_TEMP.T_REC.PROC_TY := 'D'`：当`P_EVENT_CD`不为'P'且记录已存在时。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 25. `BSPG_MTRL_WISE_ALLOC.F_GET_WTH_CUT_LTH`　（模块 BSPG）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `F_GET_WTH_CUT_LTH` 是一个函数，用于根据给定的板材厚度、宽度、规格代码、目标生产厚度和宽度以及工厂代码，查询并返回板材的切割长度。

### 2. **业务规则**
- **关键判断、分支、校验逻辑**：
  - 首先，函数接收六个参数：板材厚度（`P_SLAB_THK`）、板材宽度（`P_SLAB_WTH`）、规格代码（`P_SPEC_CD`）、目标生产厚度（`P_PLT_PROD_THK_AIM`）、目标生产宽度（`P_PLT_PROD_WTH_AIM`）和工厂代码（`P_FAC_CD`）。
  - 使用这些参数，函数在 `SCH_WTHCUT_LTHCUT_STD` 表中查询符合条件的 `MPLATE_WTH_CUT_LTH` 值。
  - 查询条件包括：
    - 工厂代码（`K.FAC_CD = P_FAC_CD`）
    - 工艺代码（`K.PROC_CD = 'PH' || P_FAC_CD`）
    - 规格代码（`K.SPEC_CD IN (P_SPEC_CD, '*')`）
    - 板材厚度（`K.SLAB_THK = P_SLAB_THK`）
    - 板材宽度（`K.SLAB_WTH = P_SLAB_WTH`）
    - 板材厚度代码（通过子查询从 `SCH_PLATE_THK_GRP_CODE_STD` 表中获取）
    - 板材宽度代码（通过子查询从 `SCH_PLATE_WTH_GRP_CODE_STD` 表中获取）
  - 如果查询结果不为空，返回第一个符合条件的 `MPLATE_WTH_CUT_LTH` 值；如果查询结果为空或发生异常，返回 `-1`。

### 3. **状态流转**
- 这个函数不涉及任何状态字段的更新，因此没有状态流转。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 26. `BSPG_ORD_WISE_ALLOC.PR_CHECK_SLAB_LOC`　（模块 BSPG）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `PR_CHECK_SLAB_LOC` 主要用于检查板坯（SLAB）的位置是否符合特定的业务规则，以确定是否可以进行充当（即分配到某个订单）。它通过检查板坯的当前状态、产品代码、以及库房和垛位信息来决定是否允许进行充当操作。

### 2. **业务规则**
- **SLAB MASTER CHECK**：检查板坯主数据是否存在且状态为'2'。
- **GET PROD_CD**：获取订单的产品代码。
- **SYD MAP MASTER CHECK**：检查板坯是否在材料库房映射中。
  - 如果板坯在热轧坯库（`YD_GR_TP = 'H'`）并且产品代码符合特定条件，且垛位代码符合特定模式，则不允许充当，并设置错误信息。
  - 如果板坯在请求移送热轧中，则不允许充当，并设置错误信息。
  - 如果板坯在厚板坯库（`YD_GR_TP IN ('M', 'N', 'O')`）并且产品代码符合特定条件，则不允许充当，并设置错误信息。
  - 如果板坯在请求移送厚板中，则不允许充当，并设置错误信息。
- **其他情况**：如果板坯不在材料库房映射中，则允许充当。

### 3. **状态流转**
- 没有明确的 UPDATE 语句或对状态字段的赋值操作。所有的状态判断和错误设置都是通过变量 `V_LOC_JDG` 和调用 `PE.PR_SET_ERROR` 函数来实现的。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 27. `BSPR_APPR_JUDGE_RSLT.PR_CHANGE_SCRAP`　（模块 BSPR）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `PR_CHANGE_SCRAP` 用于处理钢板（PLATE）的状态变更，具体来说，当一个钢板的状态（PLT_STS_CD）为3且审批判断等级（APPR_JDG_GRD）为9时，即钢板被判定为不合格（判废），则执行一系列的更新操作，包括取消发送到ERP系统、更新钢板的状态、审批判断等级等，并记录审批判断变更。

### 2. **业务规则**
- **关键判断**：首先通过查询 `SPRS_PLATE` 表获取钢板的状态码（PLT_STS_CD）、审批判断等级（APPR_JDG_GRD）和是否被挂起（HOLD_YN）。
- **分支逻辑**：如果钢板的状态码为3且审批判断等级为9，则执行以下操作：
  - 调用 `BSPR_INF_ERP.PR_CANCLE_SEND_ERP` 取消发送到ERP。
  - 调用 `GF_SPR_PLATE.PR_SELECT` 选择钢板。
  - 调用 `GF_SPR_APPR_JDG_CHG_LIST.PR_CLEAR` 清除审批判断变更列表。
  - 更新 `GF_SPR_APPR_JDG_CHG_LIST` 记录审批判断变更。
  - 更新 `GF_SPR_PLATE` 记录钢板的状态和其他相关字段。
- **校验逻辑**：如果钢板的状态码不为3或审批判断等级不为9，则通过 `PE.PR_SET_ERROR` 设置错误信息。

### 3. **状态流转**
- **字段=值** 及触发条件：
  - `PLT_STS_CD = '2'`：当钢板的状态码为3且审批判断等级为9时。
  - `SIZE_GRD = ''`：同上。
  - `SHAPE_GRD = ''`：同上。
  - `SURF_GRD = '1'`：同上。
  - `WGT_GRD = ''`：同上。
  - `APPR_JDG_GRD = '1'`：同上。
  - `APPR_JDG_DTM = ''`：同上。
  - `APPR_JDG_USER_ID = ''`：同上。
  - `APPR_JDG_YN = ''`：…

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 28. `BSPR_BUND_OBOUT.PR_SAVE_BUND_NO`　（模块 BSPR）

**AI 理解摘要**：

### 1. **用途**
这个子程序`PR_SAVE_BUND_NO`用于处理钢板的组吊操作，包括验证钢板是否可以组吊、更新钢板信息、记录组吊操作等。

### 2. **业务规则**
- **层数校验**：注释掉的代码中提到如果`P_CENG_SHU`（层数）为空，则设置错误信息，提示用户输入层数。
- **外观判定**：如果指定钢板的外观判定等级为空，则设置错误信息，提示需要判定后再组吊。
- **钢板重量**：如果指定钢板的重量为0，则不能组吊。
- **吊内重量限制**：吊内钢板总重量必须小于等于31吨。
- **外观等级一致性**：吊内钢板的外观等级必须一致。
- **订单号一致性**：吊内钢板的订单号必须一致。
- **探伤要求**：对于低倍钢板，需要进行探伤。
- **状态检查**：钢板必须处于可组吊状态。
- **落地原因检查**：非已组吊落地原因无法组吊。
- **订单准入量检查**：如果订单准入量小于钢板重量，则不能组吊。
- **热处理状态检查**：对于外观合格的热处理板，不能由精整入成品库。

### 3. **状态流转**
- **字段=值**及触发条件：
  - `GF_SPR_PLATE.T_REC.BUND_NO_YN := 'Q';`：当`P_D_FL = 1`时，表示吊状态去热处理。
  - `GF_SPR_PLATE.T_REC.BUND_NO_YN := 'N';`：当`P_D_FL = 0`时，表示组吊完成等待预设垛位。
  - `GF_SPR_PLATE.T_REC.OVER_ORD_FL := 'Y';`：当订单准入量小于钢板重量时，设置为'Y'。
  - `GF_SPR_PLATE.T_REC.HTM_INST_REQ_YN := '';`：当`P_D_FL = 0`时，清除热处理要求。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 29. `BSPR_CUTTING_RSLT.PR_SAVE_DS_CUT_MANUAL`　（模块 BSPR）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `PR_SAVE_DS_CUT_MANUAL` 用于处理和保存钢板切割的结果信息。它接收一系列参数，包括工厂代码、轧制线编号、序列号、钢板编号、切割开始和结束时间、钢板的宽度和长度等，以及与订单相关的数量和尺寸信息。子程序的主要作用是将这些信息保存到数据库中，用于记录和管理切割操作的结果。

### 2. **业务规则**
- **参数校验**：如果输入的 `P_PLT_NO`（轧制线编号）为 `NULL`，则会通过 `PE.PR_SET_ERROR` 抛出错误，提示“此母板没有轧制信息”。
- **状态检查**：通过查询 `SPR_PLATE` 表获取 `V_PLT_STS_CD`（钢板状态代码），并根据其值进行不同的处理：
  - 如果 `V_PLT_STS_CD` 为 '1'，则表示钢板尚未进行切割，可以继续处理。
  - 如果 `V_PLT_STS_CD` 为 '2'，则表示钢板已在处理中，可以继续进行切割操作。
  - 如果 `V_PLT_STS_CD` 为 '3'，则表示钢板已经完成切割，此时会抛出错误，提示“该计划已经火切”。
- **切割操作**：对于每个订单行（`P_ORD_LN1` 到 `P_ORD_LN9`），如果对应的 `P_PLATE_QTY`（钢板数量）大于0，则进行循环，为每个钢板生成一个新的 `FC_PLT_NO`（切割编号），并调用 `PR_SAVE_OUT_DSCUT_RSLT` 子程序保存切割结果。
- **异常处理**：如果 `P_PLATE_OR_QTY`（其他数量）大于0，也会进行类似的循环处理，但不会关联到具体的订单行。

### 3. **状态流转**
- **字段=值**：
  - `V_PLT_STS_CD` = '1' 或 '2' 或 '3'：根据 `SPR_PLATE` 表中查询到的值。
  - `V_ORD_FL` = '1' 或 '2'：根据循环索引和 `V_ORD_CNT` 的比较结果设置。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 30. `BSPR_CUTTING_SEARCH.PR_SEARCH_FRAME_CUT_SUM_LIST`　（模块 BSPR）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `PR_SEARCH_FRAME_CUT_SUM_LIST` 用于查询特定工厂代码（`FAC_CD`）和生产线编号（`PLT_NO`）下的切割框架结果的汇总信息。它将返回一个游标 `P_CUR`，包含每个切割框架的宽度、长度、订单数量、非订单数量、以及起始框架编号的汇总数据。

### 2. **业务规则**
- **关键判断**：子程序接受两个输入参数 `P_FAC_CD` 和 `P_PLT_NO`，用于筛选 `SPR_CUT_FRAME_RSLT` 表中符合条件的记录。
- **分支逻辑**：无明显的分支逻辑，子程序直接执行一个查询并返回结果。
- **校验逻辑**：没有显式的参数校验逻辑，假设调用者会提供有效的参数。

### 3. **状态流转**
- 子程序没有直接对任何状态字段进行赋值操作，因此没有状态流转。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 31. `BSPR_HEAT_FCE.PR_SEND_PDI`　（模块 BSPR）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `BSPR_HEAT_FCE.PR_SEND_PDI` 用于发送生产数据接口（PDI）信息。具体来说，它根据提供的 `P_MOM_PLT_NO`（钢板编号）和 `P_PRODUCTION_LINE`（生产线）参数，决定是否发送PDI信息，并更新相关数据。

### 2. **业务规则**
- **关键判断**：程序首先检查 `P_PRODUCTION_LINE` 是否等于 '2'。如果是，则执行以下操作：
  - 调用 `BSPR_OPER_PS1.PR_SEND_PS1_PDI` 过程，发送PDI信息。
  - 调用 `GF_SPR_PLATE.PR_SELECT` 过程选择钢板信息，并将 `PRODUCTION_LINE` 字段更新为 `P_PRODUCTION_LINE` 的值。
  - 调用 `GF_SPR_PLATE.PR_UPDATE` 过程更新钢板信息。
- **分支逻辑**：如果 `P_PRODUCTION_LINE` 不等于 '2'，则不执行任何操作。

### 3. **状态流转**
- **字段=值** 及触发条件：
  - `GF_SPR_PLATE.T_REC.PRODUCTION_LINE := P_PRODUCTION_LINE`：当 `P_PRODUCTION_LINE` 等于 '2' 时，更新 `PRODUCTION_LINE` 字段为 `P_PRODUCTION_LINE` 的值。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 32. `BSPR_HEAT_FCE_TEST.SPR_ORDDESC`　（模块 BSPR）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `BSPR_HEAT_FCE_TEST.SPR_ORDDESC` 用于根据给定的订单编号 `P_ORD_NO` 和订单行号 `P_ORD_LN` 查询特定订单行的销售特殊描述 `SALES_SPCL_DESC`。

### 2. **业务规则**
- **关键判断、分支、校验逻辑**：
  - 子程序接收两个参数 `P_ORD_NO` 和 `P_ORD_LN`，分别代表订单编号和订单行号。
  - 使用 `SELECT INTO` 语句从 `SSD_ORDER_LINE` 表中查询与给定订单编号和行号匹配的销售特殊描述 `SALES_SPCL_DESC`。
  - 如果查询成功，将查询结果赋值给变量 `V_SALES_SPCL_DESC` 并返回。
  - 如果查询过程中发生任何异常（如未找到匹配记录或数据库错误），则捕获异常并返回空字符串 `''`。

### 3. **状态流转**
- 该子程序没有涉及任何状态字段的更新或赋值操作。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 33. `BSQM_INF_LIMS_MEC_TEST.FC_GET_MECH_JDG_RSLT`　（模块 BSQM）

**AI 理解摘要**：

1. **用途**：
这个子程序 `FC_GET_MECH_JDG_RSLT` 的用途是根据提供的参数从指定的表中查询机械判断结果。它接收五个参数：表名（`P_TABLE_NM`）、样品编号（`P_SMP_NO`）、样品长度位置（`P_SMP_LTH_LOC`）、测试次数（`P_TEST_CNT`）和列标识符（`P_COL_ID`），并返回查询结果。

2. **业务规则**：
- 关键判断、分支、校验逻辑：
  - 首先检查 `P_COL_ID` 是否为空，如果为空，则直接返回空字符串。
  - 然后检查 `P_TABLE_NM` 是否为特定的三个表名之一（`SQM_HC_MECH_RSLT`、`SQM_CC_MECH_RSLT`、`SQM_PC_MECH_RSLT`）。如果是，则构建 SQL 查询语句；如果不是，则不执行任何操作。

3. **状态流转**：
- 该子程序没有对任何状态字段进行赋值，因此没有状态流转。

4. **读写副作用**：
- 读取的表：根据 `P_TABLE_NM` 参数的值，可能读取的表包括 `SQM_HC_MECH_RSLT`、`SQM_CC_MECH_RSLT`、`SQM_PC_MECH_RSLT`。
- 写入的表及 DML 类型：该子程序没有写入任何表，因此没有 DML 操作。

5. **调用依赖**：
- 该子程序没有调用任何其他过程或函数。

6. **风险与不确定点**：
- 动态 SQL 盲区：构建的 SQL 语句 `V_STR_SQL` 依赖于输入参数，可能导致 SQL 注入风险，特别是如果参数没有经过适当的验证和清理。
- 语义不明处：
  - `P_SMP_NO`、`P_SMP_LTH_LOC`、`P_TEST_CNT` 和 `P_COL_ID` 参数的具体含义和格式没有在代码中明确说明，需要进一步的信息来理解它们的具体作用和预期值。
  - `P_TABLE_NM` 参数的值决定了查询的表，但代码中没有对这些表的结构和内容进行说明，因此不清楚这些表的具体结构和它们如何与子程序的逻辑相匹配。
  - 异常处理：当发生…

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 34. `BSQM_MTC_ISSUE_HB.PR_SAVE_MTC_SMS_CHEM`　（模块 BSQM）

**AI 理解摘要**：

### 1. **用途**
这个子程序`PR_SAVE_MTC_SMS_CHEM`用于保存材料化学分析结果到`SQM_MTC_CHEM`表中。它接收四个参数：`P_MTC_NO`（材料编号）、`P_HEAT_NO`（炉号）、`P_ORD_NO`（订单编号）、`P_ORD_LN`（订单行号），并根据这些参数从`SQM_CHEM_JDG`表中获取化学分析结果，然后更新`SQM_MTC_CHEM`表。

### 2. **业务规则**
- **关键判断、分支、校验逻辑**：
  - 检查`SQM_CHEM_JDG`表中是否存在对应的化学判断结果（`N_CC_JDG`）。如果不存在且`P_HEAT_NO`不等于'203670800'，则调用`PE.PR_SET_ERROR`设置错误并返回。
  - 根据订单类型（`V_ORD_TY`），选择不同的化学分析结果更新逻辑。如果`V_ORD_TY`为'2'，则从`SQM_CHEM_JDG`表中获取化学分析结果；否则，从`SQM_ORD_CHEM`和`SQM_CHEM_JDG`表的连接查询中获取结果。
  - 对于每个化学分析结果，尝试从`SCO_CODE_DETAIL`表中获取属性`ATTR1`。如果查询失败，则调用`PE.PR_SET_ERROR`设置错误。
  - 使用动态SQL更新`SQM_MTC_CHEM`表中的化学分析结果。如果动态SQL执行失败，则不进行任何操作。

### 3. **状态流转**
- **字段=值及触发条件**：
  - `GF_SQM_MTC_CHEM.T_REC.MTC_NO` = `P_MTC_NO`：初始化时设置。
  - `GF_SQM_MTC_CHEM.T_REC.MTC_CHG_CNT` = `'1'`：初始化时设置。
  - `GF_SQM_MTC_CHEM.T_REC.SMS_PROD_CHEM_TY` = `'G'`：初始化时设置。
  - `GF_SQM_MTC_CHEM.T_REC.CHEM_TEST_NO` = `P_HEAT_NO`：初始化时设置。
  - `SQM_MTC_C…

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 35. `BSQM_SMP_LOTFORM_RSLT.PR_SEARCH_LOTFORM_SCR`　（模块 BSQM）

**AI 理解摘要**：

### 1. **用途**：
这个子程序 `PR_SEARCH_LOTFORM_SCR` 用于在 `SQM_SMP_LOTFORM_RSLT` 表中搜索符合条件的批次（LOT）信息。它接收多个参数，包括材料编号、规格代码、炉号、批次重量、订单厚度、产品代码和样本条件，然后根据这些参数在表中查找匹配的记录。

### 2. **业务规则**：
- **材料编号匹配**：子程序通过比较输入的材料编号 `P_INST_MTRL_NO` 的前8位和第11至13位与 `SQM_SMP_LOTFORM_RSLT` 表中 `MTRL_NO` 字段的相应部分来匹配记录。
- **产品代码匹配**：只有当 `PROD_CD` 字段与输入的 `P_PROD_CD` 相匹配时，记录才会被考虑。
- **重复样本标记**：只有标记为 `REP_YN = 'Y'` 的记录才会被考虑。
- **独立样本标记**：只有当 `ALONE_FLAG` 为 `NULL` 或 `'N'` 时，记录才会被考虑。
- **行数限制**：通过 `ROWNUM = 1` 限制只选择一个记录。

### 3. **状态流转**：
- `V_SCR_SMP_EXIST` 字段被设置为 `'U'`，当找到符合条件的记录时触发。
- `V_SCR_SMP_EXIST` 字段被设置为 `'I'`，当循环结束没有找到符合条件的记录时触发。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 36. `BSQM_SMP_LOTFORM_RSLT_GH1.PR_SEARCH_LOTFORM_MTL`　（模块 BSQM）

**AI 理解摘要**：

### 1. **用途**：
这个子程序 `PR_SEARCH_LOTFORM_MTL` 用于在 `SQM_SMP_LOTFORM_RSLT` 表中搜索符合条件的材料批次信息。它根据输入的规格编号（`P_SPEC_CD`）、热处理编号（`P_HEAT_NO`）、批次重量（`P_LOT_WGT`）、订单厚度（`P_ORD_THK`）和样品条件（`P_SMP_CND`）来筛选数据，并返回符合条件的第一条记录。

### 2. **业务规则**：
- **规格匹配**：通过 `SPEC_CD` 字段匹配输入的规格编号 `P_SPEC_CD`。
- **热处理编号匹配**：通过 `HEAT_NO` 字段匹配输入的热处理编号 `P_HEAT_NO`。
- **样品条件匹配**：通过 `SMP_CND` 字段匹配输入的样品条件 `P_SMP_CND`。
- **厚度忽略**：注释掉了 `ORD_THK` 字段的匹配，意味着不根据订单厚度筛选。
- **程序代码匹配**：筛选 `SMP_PROG_CD` 字段为 'A' 的记录。
- **GB标志匹配**：筛选 `GB_FLAG` 字段为 'N' 的记录。
- **重复标志匹配**：筛选 `REP_YN` 字段为 'Y' 的记录。
- **重量累加**：计算累计的测试重量 `V_TEST_ACC_WGT` 和累计的测试线圈数量 `V_TEST_ACC_COIL_CNT`。
- **长度检查**：如果 `LOT_NO` 字段的长度超过10个字符，则跳过当前记录。
- **重量和线圈数量的校验**：注释掉了对 `V_SMP_MAX_WGT` 和 `V_TEST_ACC_WGT` 的比较，以及对 `V_SMP_MIX_COIL_CNT` 和 `V_TEST_ACC_COIL_CNT` 的比较。

### 3. **状态流转**：
- **字段=值**：`V_SMP_EXIST := 'U'`，触发条件是在循环中找到符合条件的第一条记录。
- **字段=值**：`V_SMP_EXIST := 'I'`，触发条件是循环结束后没有找到符合条件的记…

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 37. `BSQM_SMP_LOTFORM_RSLT_GH2.PR_SEARCH_LOTFORM_45`　（模块 BSQM）

**AI 理解摘要**：

1. **用途**：
这个子程序 `PR_SEARCH_LOTFORM_45` 用于在 `SQM_SMP_LOTFORM_RSLT` 表中搜索符合条件的重卷信息。它接收一系列参数，包括材料编号、规格代码、炉号、卷重、订货厚度、产品代码和样本条件，然后根据这些参数在表中查找匹配的记录。

2. **业务规则**：
- 子程序首先定义了一个游标 `C_LOTFORM_CUR`，该游标根据输入参数 `P_INST_MTRL_NO` 和 `P_PROD_CD` 从 `SQM_SMP_LOTFORM_RSLT` 表中检索记录，同时要求 `REP_YN` 为 'Y'，`ALONE_FLAG` 为 'N'，并且只取第一条记录（`ROWNUM = 1`）。
- 在循环中，子程序通过游标检索记录，并累加 `TEST_ACC_WGT` 和 `TEST_ACC_COIL_CNT` 字段的值。
- 如果找到符合条件的记录，则将 `V_SCR_SMP_EXIST` 设置为 'U' 并返回，否则在循环结束后将 `V_SCR_SMP_EXIST` 设置为 'I' 并返回。

3. **状态流转**：
- 子程序中没有直接的 UPDATE、SET 语句对状态字段进行赋值，`V_SCR_SMP_EXIST` 变量的值在找到记录时被设置为 'U'，在未找到记录时被设置为 'I'。

4. **读写副作用**：
- **读取**：子程序读取了 `SQM_SMP_LOTFORM_RSLT` 表。
- **写入**：子程序没有写入任何表，没有进行 INSERT、UPDATE 或 DELETE 操作。

5. **调用依赖**：
- 子程序中没有直接调用其他过程或函数，但是注释中提到了 `FC_SMP_CND_CHK` 函数和 `PE.PR_SET_ERROR` 过程，这些可能是在其他代码部分被调用的。

6. **风险与不确定点**：
- 动态 SQL 盲区：子程序中没有使用动态 SQL，因此不存在动态 SQL 盲区。
- 语义不明处：
  - 注释中提到的 `FC_SMP_CND_CHK` 函数和 `PE.P…

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 38. `BSQM_SMP_LOTFORM_RSLT_GK.PR_SAVE_SQM_MECH_HEAD`　（模块 BSQM）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `PR_SAVE_SQM_MECH_HEAD` 用于保存机械性能测试头信息到 `SQM_MECH_HEAD` 表中。它接收一系列的参数，包括材料编号、热号、板坯号、样品类型、样品条件、常规数量、样品常规尺寸和日期等，然后根据这些参数构建一条记录，并执行插入或更新操作。

### 2. **业务规则**
- **主样品编号判断**：通过调用 `FC_GET_MAIN_SMP_NO` 函数获取主样品编号，如果获取到的主样品编号与传入的样品编号相同，则 `V_BATCH_FLAG` 设置为 'Y'，否则为 'N'。
- **样品厚度确定**：根据样品类型 `P_SMP_TP` 和其他条件确定样品的厚度。
- **产品组别确定**：根据样品类型 `P_SMP_TP` 和订单请求记录 `ORD_REQ_REC` 的产品组别 `PROD_GRP` 和机械样品长度位置 `PPL_MECH_FL` 来确定最终的产品组别。
- **批次标志和主样品编号设置**：如果产品组别为 'GB' 或 'GC'，则批次标志设置为 `V_BATCH_FLAG`，主样品编号设置为 `V_MAIN_SMP_NO`；否则批次标志设置为 'Y'，主样品编号设置为传入的样品编号 `V_SMP_NO`。

### 3. **状态流转**
- **字段=值 及触发条件**：
  - `BATCH_FLAG` = `V_BATCH_FLAG`：当 `P_SMP_TP` 为 '9' 时，根据 `FC_GET_MAIN_SMP_NO` 函数返回的结果决定。
  - `MAIN_SMP_NO` = `V_MAIN_SMP_NO`：当产品组别为 'GB' 或 'GC' 时，使用 `V_MAIN_SMP_NO`；否则使用 `V_SMP_NO`。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 39. `BSQM_SMP_LOTFORM_RSLT_HC.PR_ONE_PLT_LOT_FORM`　（模块 BSQM）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `PR_ONE_PLT_LOT_FORM` 主要用于处理钢厂的单卷组批（Single Plate Lot Forming）业务。它接收一个钢卷编号（`P_COIL_NO`），然后根据这个编号进行一系列的数据查询和更新操作，包括生成试样编号、更新试样信息、保存试样跟踪记录等。

### 2. **业务规则**
- **输入校验**：如果输入的钢卷编号 `P_COIL_NO` 为空，则直接返回，不进行任何操作。
- **试样类型默认值**：将试样类型 `V_SMP_TP` 设置为 'A'。
- **订单号校验**：如果订单号 `PC_REQ_REC.ORD_NO` 为空，则设置错误并返回。
- **试样编号生成**：通过 `FC_SMP_NO_CREATE` 函数生成试样编号，如果生成失败，则设置错误并返回。
- **批次编号生成**：如果存在前一个批次编号 `V_BEF_LOT_NO`，则基于此生成新的批次编号 `V_LOT_NO`。
- **试样条件和尺寸**：根据试样宽度位置 `V_SMP_WTH_LOC` 确定试样数量 `SPCMN_CNT`。
- **数据更新**：更新 `SQM_SMP_LOTFORM_RSLT` 表中的试样信息，并插入试样跟踪记录到 `SQM_SMP_TRK` 表。

### 3. **状态流转**
- **字段=值**：
  - `GF_SQM_SMP_LOTFORM_RSLT.T_REC.REP_YN` 设置为 'Y'。
  - `GF_SQM_SMP_LOTFORM_RSLT.T_REC.SMP_LOT_SEQ` 设置为 '1'。
  - `GF_SPR_PLATE.T_REC.SMP_NO` 设置为 `V_SMP_NO`。
  - `GF_SPR_PLATE.T_REC.LOT_NO` 设置为 `V_LOT_NO`。
  - `GF_SPR_PLATE.T_REC.L2_PLT_NO` 设置为 `V_LOT_NO || '-01'`。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

### 40. `BSQM_STD_MECH_TEST.PR_SELECT_MECH_COMMON`　（模块 BSQM）

**AI 理解摘要**：

### 1. **用途**
这个子程序 `PR_SELECT_MECH_COMMON` 用于根据不同的筛选条件（`P_SCR_TY` 参数）从数据库中检索机械测试相关的标准信息，并将结果集返回给调用者。子程序通过参数接收筛选条件，如产品组、规格代码、国家规格年份等，并根据这些条件查询相关的标准数据。

### 2. **业务规则**
- **关键判断、分支、校验逻辑**：
  - 子程序首先根据 `P_SCR_TY` 参数的值（'NATL'、'CUST' 或其他）来决定执行哪个查询分支。
  - 对于每个分支，子程序使用 `WITH GRP_TBL` 子句来构建一个临时表，该表包含产品组和对应的机械项目列表。
  - 在每个分支中，子程序使用 `OPEN P_CUR FOR` 语句打开一个游标，该游标用于返回查询结果。
  - 查询条件包括对产品组、规格代码、国家规格年份等的匹配，以及对客户代码、客户质量证书编号等的模糊匹配。

### 3. **状态流转**
- **字段=值及触发条件**：
  - 子程序不直接更新任何数据库表的状态字段，而是通过游标 `P_CUR` 返回查询结果。

| 判定（正确/部分正确/错误）| 问题备注 |
|----|----|
|  |  |

