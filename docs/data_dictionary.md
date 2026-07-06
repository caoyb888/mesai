# MES 数据字典（第一版：静态证据先行）

依据 CLAUDE.md 任务 1 生成，回填自任务 6 映射表 `docs/ui_field_mapping.md`。

## 证据源与标注约定

| 标注 | 含义 |
|---|---|
| `[界面确认]` | 实机截图上可见的界面标签/内容 |
| `[推断]` | 按 glue_sql 别名、JS 字段 ID 或语义对应推断 |
| `[设计文档]` | 设计说明书文字/表格定义（设计意图，可能与实际库结构有出入） |

**当前限制**：`snapshot/` 数据库导出尚未执行，因此——
① 全库表/字段清单与真实字段注释（含乱码判定）缺席，本版只覆盖静态证据可达的部分；
② 「字段注释为空或乱码」的目标字段清单待 `run_export.sh` 产出后，与本文档按
`表.字段` 合并（届时本文档条目升级为该字段的修复建议来源，联动任务 5）；
③ 系统内建字典表 `SCO_DATA_DIC`（约 20266 条，SCOA0020 界面）是最大的一手来源，
待快照导出后整体并入。

---

## 1. 通用审计字段（MESAPUSER 模式全库通用）

出现在几乎所有业务表与接口表中（glue_sql、接口表定义均反复出现）。[界面确认]+[设计文档]

| 字段 | 类型（典型） | 含义 |
|---|---|---|
| CRT_USER_ID | VARCHAR2(20) | 创建用户 ID |
| CRT_OBJ_ID | VARCHAR2(30) | 创建对象 ID（程序 ID，如 JSP 程序号） |
| CRT_TM | TIMESTAMP | 创建时间 |
| UPD_USER_ID | VARCHAR2(20) | 最后修改用户 ID |
| UPD_OBJ_ID | VARCHAR2(30) | 最后修改对象 ID（程序 ID） |
| UPD_TM | TIMESTAMP | 最后修改时间 |
| ARCHIVE_FL | VARCHAR2(1) | 归档标记 |
| USE_YN | VARCHAR2(1) | 是否使用（Y/N，界面经 FC_YN_TO_BOOLEAN 转布尔） |

接口表通用字段（DB link 轮询模式）：FLAG=使用标记(0-未处理/1-已处理)、
FLAG_DATE=使用时间、TRAN_DATE=传输时间。[设计文档]

---

## 2. SCO 系统管理域（字段级，证据最完整）

来源：`src/SCO/src/query/*.glue_sql` SQL + 截图标签（映射表模块 1，image4~29）。

### SCO_USER 用户主表
| 字段 | 含义 | 来源 |
|---|---|---|
| USER_ID | 用户 ID | [界面确认] |
| USER_NM | 用户名称 | [界面确认] |
| USER_TY | 用户类型 | [界面确认] |
| USE_YN | 是否使用 | [界面确认] |
| VALID_PERIOD_STA_DT | 有效期开始日（新增默认当日） | [界面确认] |
| VALID_PERIOD_END_DT | 有效期结束日（默认 2999-12-31） | [界面确认] |
| EMP_NO | 员工号（联动 SCO_EMP） | [界面确认] |

### SCO_PASSWD 用户口令表
| 字段 | 含义 | 来源 |
|---|---|---|
| USER_ID | 用户 ID（=SCO_USER.USER_ID） | [界面确认] |
| PASSWD | 口令（前端 xtea+base64 加密存储；初始化=按 USER_ID 生成） | [界面确认] |
| PASSWD_EXPIRE_DT | 密码到期日 | [界面确认] |

### SCO_EMP 员工表
| 字段 | 含义 | 来源 |
|---|---|---|
| EMP_NO | 员工号 | [界面确认] |
| DEPT_CD | 部门代码（登录查询联取） | [推断] |

### SCO_LOGIN_HIST 登录履历
| 字段 | 含义 | 来源 |
|---|---|---|
| LOGIN_TM | 登录时间 | [推断] user.insert_login_hist |
| USER_ID | 用户 ID | [推断] |
| IP_ADDR | 客户端 IP | [推断] |

### SCO_CODE_MASTER 主代码表
| 字段 | 含义 | 来源 |
|---|---|---|
| BIZ_CHAIN_CD | 业务部门代码（SPR:厚板 等） | [界面确认] |
| MASTER_CD | 主代码 | [界面确认] |
| MASTER_NM | 主代码名 | [界面确认] |
| MASTER_DESC | 说明 | [推断] |
| CD_VALUE_LTH | 代码值长度 | [推断] |
| USE_MULTILANG_YN | 是否使用多语种 | [界面确认] |
| ATTR_NM1~5 | 属性名 1~5（详细代码扩展属性的列头） | [界面确认] |
| REMARKS | 备注 | [推断] |

### SCO_CODE_DETAIL 代码值表
| 字段 | 含义 | 来源 |
|---|---|---|
| MASTER_CD | 主代码 | [界面确认] |
| CD_VAL | 代码值 | [界面确认] |
| CD_NM | 代码名 | [界面确认] |
| DISP_SEQ | 显示顺序号 | [界面确认] |
| CD_DESC | 说明 | [推断] |
| TAGS | 区分 | [推断] |
| REF_CD / ERP_CD | 参照代码 / ERP 代码 | [推断] SQL 有列，截图未及 |

### SCO_CODE_DETAIL_HIST 代码变更履历
CHANGE_TM=变更时间、CHANGE_TY=变更形式(Update/Insert)、CHANGE_USER_NM=变更者，
对象=程序ID。[界面确认]+[推断]（SCOG0040）

### SCO_SCREEN 界面定义表（Glue 元数据驱动 UI 的核心）
| 字段 | 含义 | 来源 |
|---|---|---|
| SCR_ID | 界面 ID（=程序号=JSP 名） | [界面确认] |
| SCR_NM | 界面名 | [界面确认] |
| BIZ_CHAIN_CD | 业务部门代码 | [界面确认] |
| SCR_TY | 界面类型（界面/弹出） | [界面确认] |
| SEARCH_YN / SAVE_YN / DELETE_YN / CONF_YN | 查询/保存/删除/确认按钮启用 | [界面确认] |
| CUST1_YN~CUST5_YN / CUST1_NM~CUST5_NM | 自定义按钮 1~5 启用/名称（如"下发PDI/删除倍尺/取消装炉"） | [界面确认] |

### SCO_MENU 菜单表
| 字段 | 含义 | 来源 |
|---|---|---|
| MNU_ID | 菜单 ID（M000xxxxxx） | [界面确认] |
| MNU_CD | 菜单代码 | [界面确认] |
| MNU_NM | 菜单名 | [界面确认] |
| MNU_GRP_YN | 是否菜单组（目录节点） | [界面确认] |
| DISP_SEQ | 显示顺序 | [界面确认] |
| PGM_ID | 程序 ID（挂接 JSP/界面） | [界面确认] |
| MNU_PARAM1~3 | 菜单因子 1~3（调用参数） | [界面确认] |

### SCO_MENU_MAPPING（用户/角色-菜单授权）
权限列与 SCO_SCREEN 的 *_YN 同构（查询/保存/删除/确认/按钮1~5）。[界面确认]+[推断]

### SCO_ROLE / SCO_USER_ROLE_MAPPING
ROLE_CD=角色代码、ROLE_NM=角色名、REMARKS=备注；映射表含 USER_ID、
VALID_PERIOD_STA_DT/END_DT=授权有效期。[界面确认]

### SCO_DATA_DIC 数据字典表（系统内建，约 20266 条）
| 字段 | 含义 | 来源 |
|---|---|---|
| ITEM_FL | 项目标志（Database 等） | [界面确认] |
| ITEM_CD | 字段编码（字段英文名，如 SPEC_CD） | [界面确认] |
| ITEM_NM | 字段名称（含义，如 SPEC_CD=Order Specification） | [界面确认] |
| DATA_TY / DATA_LTH / DATA_SCALE | 数据类型/长度/小数位 | [界面确认] |
| MOM_ITEM_CD / MOM_REF_VAL | 上位代码/上位顺序号 | [推断] |

> 注意：SCOA0020 界面标签写「物料编码/物料名称」，是通用翻译误导，
> 实际内容是数据字典条目——已在映射表中说明，界面标签在此表不作命名依据。

### SCO_MSG_MASTER 消息表
MSG_ID=信息ID(MSGxxxxx)、MSG_TY=类型(E:ERROR/C:CONFIRM…)、MESSAGE=信息文本、
REMARKS=备注。[界面确认]

### SCO_MULTILANG_MASTER 多语种表
LANG_CD=语言代码、CONTENTS=内容（标签键 CAP_*，缺失时界面显示 @@/@_ 原始键）。
[界面确认]+[推断]；ALT_CONTENTS1~3 列名待快照确认。

### SCO_BIZ_RULE_MASTER / _DATA / _ATTR 业务规则
RULE_ID/RULE_NM=规则 ID/名（如 SQMB0001 编制组批试样基准）、SEQ=顺序、
BIZ_RULE_COND1~20=条件列（列头由 _ATTR 的 ATTR_SEQ/ATTR_NM 动态定义）、
BIZ_RULE_RSLT1~=结果列。[界面确认]+[推断]

### SCO_SYS_ENV 系统环境
ENV_CD/ENV_VAL/ENV_TY/ENV_CAT/ENV_TAGS/USE_YN/REMARKS；示例条目：多语种缺失前缀
(@@)、班次开始时间(0800/2000)、日期/数字格式。[界面确认]+[推断]

### SCO_PKG_LOG 程序包日志
PKG_ID=包名、LOG_DTM=日时、LOG_TY=类型、LOG_TEXT/LOG_SEQ=日志文本/序号。[界面确认]+[推断]

### 其余 SCO 表（glue_sql 中出现，字段待快照）
SCO_QUERY_MASTER（查询定义，SCOB0040）、SCO_INF_TC / SCO_INF_TC_SIMU（接口 TC：
TC_ID/TC_NM/TC_OWNER）、SCO_INF_FORMAT / SCO_INF_FORMAT_ATTR（接口报文格式）、
SCO_INF_LOG 及分域日志 SCO_INF_LOG_SCH/SCO/SPR/SQM/SMS/SSD/SYD/SHR/SIM/SIT/SMP/SPG/SRS/SCR
（14 张同构接口日志表）、SCO_REPORT（报表）、SCO_FILE_MASTER（附件）、
SCO_FUNCTION_MASTER / SCO_FUNCTION_PARAMS（标准 API 字典，SCOZ0050）、
SCO_MENU_MAPPING_EXT、SCO_MENU_FAVORITES、SCO_GLOSSARY（术语）、SCO_BULLETIN（公告）、
SCO_BATCH_JOB、SCO_REQUEST、SCO_DATA_UPLOAD_MASTER/_DETAIL、SCO_GRID_LAYOUT、
SCO_SOURCE_GEN、SCO_OBJ_MASTER、SCO_BIZ_ENV、SCO_ACCESS。[推断]（表名自 glue_sql FROM/INSERT）

---

## 3. 业务域表（表级，字段待 PL/SQL 快照回填）

### SPR 厚板域（SCOZ0070 表包生成界面直接可见，拥有人 MESAPUSER）[界面确认]

| 表名 | 中文含义 |
|---|---|
| SPR_ACC_RSLT_BK | 快冷(ACC)实绩表 |
| SPR_APPR_FIN_RSLT | 外观精整实绩 |
| SPR_BRG_MASTER | Bearing Master（轴承主数据） |
| SPR_BUND_RSLT | 组吊操作实绩 |
| SPR_CCK_MASTER | Chock Master（轴承座主数据） |
| SPR_CHG_LINE_LIST | 两线交接操作记录表 |
| SPR_COMPLEX_SLAB | 复合板坯 |
| SPR_COOL_BED_RSLT | 冷床实绩 |
| SPR_CPL_RSLT | 冷矫实绩（Cold Plate Leveller，注 TB_FRB070） |
| SPR_CUTTING_RSLT | 剪切实绩 |
| SPR_CUT_CS_DTL_RSLT | 横剪 DETAIL 实绩 |
| SPR_CUT_CS_RSLT | 横剪实绩 |
| SPR_CUT_CS_SUB_RSLT | 横剪 SUB 实绩 |
| SPR_CUT_DSTS_RSLT | 双边剪实绩 |

### SIS_DYNM_CONF_FIELD 动态配置字段表（SCOZ0080 截图，字段注释可见）[界面确认]
IS_SHOW=是否显示、IS_SUM=是否累计、AREA_CODE=工序、IS_PK=是否为主键、
IS_SEARCH=是否为查询条件。

### PL/SQL 包（间接表线索，SCOZ0090 截图 + service.xml 锚点）[界面确认]
BSIM_BIZ_COMMON（炼钢业务公共）、BSMS_*（炼钢实绩）、BSCH_*（计划）、BSPG_*（订单进程）、
BSQM_*（质量）、BSPR_*（厚板：HEAT_FCE 加热炉/ROLL_RSLT 轧制/CUTTING_* 剪切/
APPR_JUDGE_RSLT 外观判定/UST_RSLT 探伤/BUND_OBOUT 组吊出库/MARK_INFO 喷印）——
包名前缀 B+域，各包涉及表待 snapshot/03_src 解析后逐表回填。

---

## 4. 代码字典（主代码含义 + 值域，任务 1 直接条目）

### 4.1 主代码中文名（SCOB0010/0020、SCOE0020/0030 截图可见）[界面确认]

| 主代码 | 含义（域） |
|---|---|
| APPR_FIN_MTH_CD | 外观精整方法代码 (SPR) |
| APPR_JDG_YN | 外观检查是否完成 (SPR) |
| BUND_RSN | 钢板去向：H=热处理原料库 / S=精整成品库 (SPR) |
| BUND_TY | 热/精整组吊区分 (SPR) |
| CH_DISCH_FL | 装/出炉区分 (SPR) |
| CPL_STS_CD | CPL 状态代码 (SPR) |
| CS_CUT_TP / DS_CUT_TP / FC_CUT_TP | 横剪/双边剪/框架剪切类型 (SPR) |
| GRING_YN | 研磨与否 (SPR) |
| HTM_CH_DISCH_FL | 热处理装/出炉区分 (SPR) |
| HTM_NO | 热处理炉号 (SPR) |
| MARK_YN | 喷印与否 (SPR) |
| PLT_DIR_CD | 钢板去向 (SPR) |
| PLT_OPER_TRK_CD | 钢板作业跟踪代码 (SPR) |
| PLT_TY | 钢板类型 (SPR) |
| APPRD_GRD | 外观等级 (SMS) |
| APPR_JDG_GRD | 外观判定等级 (SQM) |
| BIZ_CHAIN_CD | 业务链（部门）代码 (SCO) |
| CCM_CD_W | 连铸机代码 (SCH) |
| CHEM_BIZ_CD / CHEM_JDG_GRD / CHEM_LVL2_CD / CHEM_LVL3_CD | 化验业务/成分判定等级/化验层级 (SQM) |
| CITY_CD / COUNTRY_CD / CURRENCY_CD | 城市/国家/币种 (SSD/SMP) |
| CUST_GRD / CUST_KIND | 客户等级/客户种类 (SSD) |
| DORD_STS | 提货单状态 (SYD) |
| ABNR_REASON_GRP | 异常原因组（1=Steel Making … 7=Planning） |
| ABNR_INFO / ABNR_OCR_CAU_CD | 异常信息 / 异常发生原因代码 |
| ACCEPT_YN | 已接收/未接收 |
| ALLOC_CHK_TY | 分配检查类型（Mandatory/Optional） |

### 4.2 值域（截图数据可见）[界面确认]

- **厚度组代码**（SCHA0040）：A:10~12 B:12~14 C:14~16 D:16~18 E:18~20 F:20~22 …至 M
  （步进 2mm 区间）。
- **UST 判定**（SPRC0021）：合格 / 不合格Y1 / 不合格Y2；UST等级值「合订单」。
- **外观等级变更值**（SPRB0730）：合格、订单外1级（另有订单外2级(外观)/(物理)，见改判率查询）。
- **改判原因**（改判率查询）：探伤不合、裂纹、结疤、夹杂、尺寸不合、瓢曲、氧化铁皮压入、
  异物压入、麻点、划伤、压痕、性能不合、卷轧头尾钢板。
- **非计划原因**（SPRB0030）：轧废 等。
- **定尺类型**（组吊及起吊）：长宽定尺；**非稳态级别**：-正常铸坯；**水冷方式**：N:None。
- **交货状态**（SPRC0021）：正火轧、热轧A…。
- **取样地点**（钢水检验成分接口）：Q=炉前、H=炉后、JL=精炼（另转炉炉前/炉后/CCM）。
- **能源名称**（能源数据收集，[原型]）：煤、高炉煤气、压缩空气、电、软化水、生产水、
  脱硫水、蒸汽；分类=投入/产出。
- **轧辊代码**（轧辊管理，[原型]）：轧辊类型 WR:工作辊、轧机类型 F:精轧、机架 F1:精轧机架1、
  轧辊位置 TOP:上辊。
- **消息类型**（SCOA0030）：E=ERROR、C=CONFIRM…。
- **接铁厂**（铁水轨道衡接口）：S=南厂、N=北厂。

### 4.3 编码规则（media/13_编码设计 + 截图实例）[界面确认]

- **LOT_NO 批号**：13 位 `YY P NNNNNN - SS`（年2+工厂1[厚板=P]+序号6+子序号2）；
  复验不合格时从属试样以「原批号+序列号」赋新号。
- **SMP_NO 试样编号**：12 位（工厂1[P]+连铸1+年2+SeqNo7+次数1：1=初验、2/3=复验）。
- **MTC_NO 质量保证书编号**：11 位（公司代码2+年月日6+顺序3）；定义='HB'，实例
  HB/RZ 并存（两套前缀并行，[疑似文档过时]）。
- **钢板号** [推断]：P+年尾数+线别+C/B+7位序+子板后缀（T/N/G+2位），如 P523C0320700T01；
  后缀含义待 PL/SQL 确认。
- **程序号**：S+域(CO/QM/CH/SD/YD/MS/PR/HR/DA…)+功能字母+4位数字；PL/SQL 业务包=B+程序域。
- **投料物料代码 RR***（炼钢投料界面）：详见映射表模块 5。

---

## 5. 接口表字段字典（设计文档「数据结构」章节机器解析）[设计文档]

> 来源：design.md 系统集成及接口章（章起 L20779）。**注意**：这是设计定义，实际
> DB 表名未在文档中给出（待快照按字段组合匹配）；类型/注释可能与实库有出入。
> 注释列已清理文档导出造成的「X_X」重复。原文缺注释的字段保留空值——这些正是
> 任务 1 后续要结合 PL/SQL 用法补注的目标。


### 铁水轨道衡计量接口表（14 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| ID | NUMBER(9) | 主键ID |
| LD_NO | VARCHAR2(30) | 钢包号 |
| PI_LD_NO | VARCHAR2(30) | 铁包号 |
| PI_NO | VARCHAR2(30) | 铁次号 |
| TS_TARE_WGT | NUMBER(9) | 接铁前轨道衡皮重 |
| IRON_CON_NO1 | VARCHAR2(2) | 接铁厂，S-南厂,N-北厂 |
| IRON_CON_TARE_WGT | NUMBER(12) | 接铁皮重 |
| IRON_CON_DTM | DATE | 接铁时间 |
| GROSS_WGT | NUMBER(9) | 毛重 |
| IRON_CON_END_DTM | DATE | 接铁完成时间 |
| NET_WGT | NUMBER(9) | 净重 |
| FLAG | NUMBER(1) | 使用标记, 0-未处理，1-已处理 |
| FLAG_DATE | DATE | 使用时间 |
| CREATE_TIME | DATE | 创建时间 |

### 钢水检验成分数据接口表（21 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| HEAT_NO | VARCHAR2(20) | 炉次号 |
| GRADE | VARCHAR2(60) | 钢种 |
| DEV_CODE | VARCHAR2(20) | 设备代码 |
| STEEL_LADLE_NAME | VARCHAR2(20) | 钢包号 |
| CHEM_NAME | VARCHAR2(20) | 检验项目 |
| CHEM_VALUE | NUMBER | 检验结果 |
| REMARK | VARCHAR2(90) | 备注 |
| FLAG | VARCHAR2(1) | 使用标记 |
| FLAG_DATE | DATE | 使用时间 |
| TRAN_DATE | DATE | 传输时间 |
| ID | VARCHAR2(40) | 主键 |
| SAMPLE_PLACE | VARCHAR2(20) | 取样地点 Q炉前，H炉后，JL精炼 |
| SAMPLE_CNT | VARCHAR2(20) | 复验次数 |
| CRT_USER_ID | VARCHAR2(20) | BOTTOM_STAT |
| CRT_OBJ_ID | VARCHAR2(30) | Created Object ID |
| CRT_TM | TIMESTAMP(7) | Created Time |
| UPD_USER_ID | VARCHAR2(20) | Last Updated User ID |
| UPD_OBJ_ID | VARCHAR2(30) | Last Updated Object ID |
| UPD_TM | TIMESTAMP(7) | Last Updated Time |
| ARCHIVE_FL | VARCHAR2(1) | Record Archive Flag |
| JL_FLAG | VARCHAR2(1) | 精炼读取标志 |

### 板材取样指示接口表（68 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| CRT_USER_ID | VARCHAR2(20) | Created User ID |
| CRT_OBJ_ID | VARCHAR2(30) | Created Object ID |
| CRT_TM | TIMESTAMP(7) | Created Time |
| UPD_USER_ID | VARCHAR2(20) |  |
| UPD_OBJ_ID | VARCHAR2(30) | Last Updated Object ID |
| UPD_TM | TIMESTAMP(7) |  |
| ARCHIVE_FL | VARCHAR2(1) | Record Archive Flag |
| QLT_STD_SEQ | NUMBER(8) | 质量标准序列号 |
| QLT_DSN_STD_TY | VARCHAR2(1) | 质量设计标准区分 |
| PROD_GRP | VARCHAR2(2) | 品种代码 |
| QLT_REMARKS | VARCHAR2(300) | 质量备注 |
| SMP_NO | VARCHAR2(30) | 试样编号 |
| BATCH_NO | VARCHAR2(30) | 批号 |
| TEST_CNT | NUMBER | 试验次数 |
| HEAT_NO | NUMBER | 炉号 |
| PRO_LINE | VARCHAR2(30) | 产线 |
| NATL_SPEC_NO | VARCHAR2(130) | 国际标准编号 |
| GANGZHONG | VARCHAR2(130) | 钢种 |
| SPEC | VARCHAR2(30) | 规格 |
| MATERIAL | VARCHAR2(230) | 物料名称 |
| MATERIALBM | VARCHAR2(30) | 物料名称编码 |
| BATCH_WEIGHT | NUMBER | 批次重量 |
| SMP_DATE | DATE | 委托时间 |
| IS_ZHIYANG | VARCHAR2(10) | 是否制样 |
| SMP_PROG_CD | VARCHAR2(10) | 试样进程状态 |
| STAND_MC | VARCHAR2(30) | 标准名称 |
| CHEM_JDG_GRD | VARCHAR2(1) | 成分等级 |
| MECH_JDG_GRD | VARCHAR2(1) | 性能等级 |
| APPR_JDG_GRD | VARCHAR2(1) | 外观等级 |
| PROD_TOT_JDG_GRD | VARCHAR2(1) | 综合等级 |
| JDG_DTM | TIMESTAMP(7) | 试样判定时间 |
| JDG_USER_ID | VARCHAR2(20) | 判定人员 |
| QY_DTM | TIMESTAMP(7) | 取样时间 |
| JY_DTM | TIMESTAMP(7) | 检验时间 |
| GP_DTM | TIMESTAMP(7) | 改判时间 |
| GP_USER_ID | VARCHAR2(20) | 改判人员 |
| TS_NUM | NUMBER | TS组数 |
| BN_NUM | NUMBER | BN组数 |
| IM_NUM | NUMBER | IM组数 |
| RB_NUM | NUMBER | RB组数 |
| ORD_NO | VARCHAR2(20) | 订单号 |
| ORD_LN | VARCHAR2(3) | 订单行号 |
| PROD_CD | VARCHAR2(3) | 产品品名 |
| SMP_LTH_LOC | VARCHAR2(1) | 试样采取位置 |
| NM_NUM | NUMBER |  |
| AV_NUM | NUMBER |  |
| GS_NUM | NUMBER |  |
| DE_NUM | NUMBER |  |
| WE_NUM | NUMBER |  |
| CHENGFEN_FLAG | VARCHAR2(50) | lims成分备注 |
| MECH_FLAG | VARCHAR2(1) | 是否保性能 |
| PLT_NO | VARCHAR2(50) | 复验的钢板号 |
| ZT_NUM | NUMBER | Z向拉伸 |
| HT_NUM | NUMBER | 高温拉伸 |
| AT_NUM | NUMBER | 时效冲击 |
| UP_NUM | NUMBER | 顶锻 |
| HD_NUM | NUMBER | 布氏硬度 |
| HD1_NUM | NUMBER | 洛氏硬度 |
| HD2_NUM | NUMBER | 维 氏硬度 |
| DW_NUM | NUMBER | 落锤试验 |
| NP_NUM | NUMBER | 末端淬透性 |
| CS_NUM | NUMBER | 碳化物偏析 |
| CD_NUM | NUMBER | 成分偏析 |
| ND_NUM | NUMBER | 无损检测 |
| JU_NUM | NUMBER | 判定范围 |
| MA_NUM | NUMBER | 低倍组织缺陷 |
| GA_NUM | NUMBER | 气体 |
| HH_NUM | NUMBER | 热处理 |

### 板材物性检验结果接口表（17 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| ID | VARCHAR2(20) | GUID |
| DOCUMENTNO | VARCHAR2(100) | 批号 |
| ITEMCODE | VARCHAR2(100) | 检测项目编码 |
| ITEMAB | VARCHAR2(100) | 检测项目缩写 |
| ITEMNAME | VARCHAR2(100) | 检测项目名称 |
| COLLECTDATE | DATE | 采集时间 |
| INSERTDATE | DATE | 写入时间 |
| ITEMVALUE | VARCHAR2(100) | 检测值 |
| EQUIPMENTNAME | VARCHAR2(100) | 设备名称 |
| OLDCOLLECTDATE | VARCHAR2(100) | 采集时间非日期格式 |
| TESTNO | VARCHAR2(100) | 设备TextNo编号 |
| MATERIALNAME | VARCHAR2(100) | 物料名称（无用） |
| STATE | NUMBER | 状态（无用） |
| PROCESS_FLAG | VARCHAR2(20) | 接口数据使用状态 |
| PROCESS_TIME | VARCHAR2(50) | 接口数据使用时间 |
| DQ_FLAG | VARCHAR2(10) |  |
| TO_MES_FLAG | VARCHAR2(10) | 标志位(成功：1,失败：0) |

### 炉次作业计划接口表（13 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| ORD_FLAG | CHAR | 标记 |
| PLAN_HEAT_NO | CHAR | 计划炉号 |
| ORD_CAST_NO | CHAR | 计划浇次号 |
| HEAT_PRI_IN_CAST | NUMBER | 浇次内序号 |
| HEAT_CNT_IN_CAST | NUMBER | 浇次炉数 |
| INCMP_STEEL_GRD | CHAR | 钢种编号 |
| BOF_MC_NO | NUMBER | 计划转炉设备号 |
| LF_MC_NO | NUMBER | 计划LF设备号 |
| CC_MC_NO | NUMBER | 计划连铸设备号 |
| TAP_STA_DTM | DATE | 计划出钢开始时间 |
| TAP_END_DTM | DATE | 计划出钢结束时间 |
| FLAG | CHAR | 使用标记 |
| FLAG_DATE | DATE | 使用时间 |

### 板坯计划接口表（15 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| id | String | 主键 |
| PONO | String | 计划号 |
| SLAB_NO | String | 计划铸坯号 |
| SLAB_POS | int | 计划铸坯序号 |
| PLAN_GRADE | String | 计划钢种 |
| PLAN_SLAB_LENGTH_MAX | String | 计划铸坯长度最大值 |
| PLAN_SLAB_LENGTH_MIN | Date | 计划铸坯长度最小值 |
| PLAN_SLAB_LENGTH | int | 计划铸坯长度 |
| PLAN_SLAB_WIDTH | int | 计划铸坯宽度 |
| PLAN_SLAB_THICKNESS | int | 计划铸坯厚度 |
| PLAN_STEEL_WEIGHT | int | 计划钢水重量 |
| HOT_FLAG | String | 热送标志（C下线，H热送） |
| INSTERT_TIME | Date | 插入时间 |
| ACTION | String | 操作标志(U：添加或者更新，D：删除) |
| READ_FLAG | int | 读取标志位（0：未读，1：已读） |

### 转炉作业实绩接口表（36 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| ID | NUMBER(9) | 主键 |
| HEAT_NO | VARCHAR2(20) | 实际炉号 |
| PLAN_HEAT_NO | VARCHAR2(20) | 计划炉号 |
| SPEC_CD | VARCHAR2(50) | 钢种 |
| BOF_LIFE_CNT | NUMBER(22) | 炉龄 |
| LN_DE_SLAG_AFT_FST_HEAT_YN | VARCHAR2(1) | 是否1倒 |
| OXG_LN_NO | NUMBER(22) | 氧枪号 |
| OXG_LN_USED_CNT | NUMBER(22) | 枪龄 |
| LANCE_POSIT_START | NUMBER | 开吹枪位 |
| LANCE_POSIT_PROGRESS | NUMBER | 过程枪位 |
| LANCE_POSIT_END | NUMBER | 终点枪位 |
| PI_LD_NO | NUMBER(22) | 铁次号/罐号 |
| PI_CHARG_ACT_TEMP | NUMBER(22) | 铁水温度 |
| PI_WGT | NUMBER(22,3) | 铁水量 |
| SCRAP_TOT_WGT | NUMBER(22,3) | 废钢总量 |
| OXG_PRS | NUMBER | 总管氧压 |
| PROD_OXG_PRS | NUMBER | 工作氧压 |
| OXG_FLOW | NUMBER | 氧气流量 |
| EP_TEMP | NUMBER(22) | 终点温度 |
| TAP_TEMP | NUMBER(22) | 出钢温度 |
| BEF_AR_TEMP | NUMBER | 氩前温度 |
| AFTER_AR_TEMP | NUMBER(22) | 氩后温度 |
| OXG_USED_TOT_VOL | NUMBER(22) | 氧气消耗 |
| BLW_IN_N2_USE_VOL | NUMBER(22) | 氮气消耗 |
| BOTTOM_STAT | VARCHAR2(2) | 底吹情况 |
| SHIFT_NO | VARCHAR2(2) | 班次 |
| SHIFT_GRP | VARCHAR2(2) | 班组 |
| CAPTAIN_NM | VARCHAR2(30) | 炉长 |
| LD_NO | VARCHAR2(10) | 钢包号 |
| HEAT_TOT_WGT | NUMBER(22,3) | 钢水重量 |
| EP_EST_OXG_DEN | NUMBER(22) | 钢水定氧 |
| LADLE_COVER | VARCHAR2(2) | 钢包加盖 |
| SLAG_CUT_METHOD | VARCHAR2(3) | 挡渣 |
| TAPHOLE_USED_CNT | NUMBER(22) | 出钢口使用次数 |
| FLAG | VARCHAR2(1) | 使用标记 |
| FLAG_DATE | DATE | 使用时间 |

### 精炼作业实绩接口表（27 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| ID | NUMBER(9) | 主键 |
| HEAT_NO | VARCHAR2(20) | 实际炉号 |
| LF_NO | VARCHAR2(1) | lf设备号 |
| PLAN_HEAT_NO | VARCHAR2(20) | 计划炉号 |
| LD_NO | VARCHAR2(20) | 包号 |
| SPEC_CD | VARCHAR2(50) | 钢种 |
| PI_NO | VARCHAR2(20) | 铁次号 |
| PI_LD_NO | VARCHAR2(20) | 铁包号 |
| LF_ARR_DTM | DATE | 到站时间 |
| LF_DEP_DTM | DATE | 出站时间 |
| LIFT_DTM | DATE | 吊包时间 |
| ARR_TEMP | NUMBER(7) | 到站温度 |
| DEP_TEMP | NUMBER(7) | 离站温度 |
| SOFT_BLOW_TIME | NUMBER(9) | 软吹时间 |
| START_ELE_TIME | DATE | 送电时间 |
| LADLE_STAT | VARCHAR2(50) | 钢包情况 |
| BOTTOM_BLOW_STAT | VARCHAR2(50) | 底吹情况 |
| DETER_OXY | NUMBER(20) | 定氧ppm |
| ELE_CONSMP | NUMBER(20) | 电耗 |
| SHIFT_NO | VARCHAR2(20) | 班次 |
| SHIFT_GRP | VARCHAR2(20) | 班组 |
| ARR_WGT | NUMBER(7) | 到站重量 |
| DEP_WGT | NUMBER(7) | 离站重量 |
| CREATE_TIME | DATE | 创建时间 |
| PROC_ROUTE | VARCHAR2(50) | 冶炼周期 |
| FLAG | VARCHAR2(1) | 使用标记 |
| FLAG_DATE | DATE | 使用时间 |

### 炼钢投料实绩接口表（12 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| ID | NUMBER(9) | 主键ID |
| HEAT_NO | VARCHAR2(50) | 实际炉号 |
| SUB_MTRL_CD | VARCHAR2(50) | 物料代码 |
| MTRL_NM | VARCHAR2(50) | 物料名称 |
| MTRL_IN_AREA_CD | VARCHAR2(50) | 加料时区分代码（转炉BOF,LF：LF） |
| MTRL_IN_WGT | NUMBER(9) | 加料数量 |
| MTRL_IN_UNIT | VARCHAR2(50) | 加料单位 |
| MTRL_IN_DTM | DATE | 加料时刻 |
| FLAG | NUMBER(1) | 使用标记, 0-未处理，1-已处理 |
| FLAG_DATE | DATE | 使用时间 |
| CREATE_TIME | DATE | 创建时间 |
| AUTO_TYPE | NUMBER(1) | 投料方式：0自动，1手动; |

### 炉次连铸实绩接口表（29 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| HEAT_ID | VARCHAR2(12) | 炉号 |
| PONO | VARCHAR2(12) | 计划号 |
| SEQU_ID | VARCHAR2(12) | 浇次号 |
| HEAT_POS | NUMBER(3) | 顺序号 |
| GRADE_ID | VARCHAR2(20) | 钢种 |
| STEEL_WEIGHT | NUMBER(7,3) | 钢水浇注重量 |
| TIME_IN_TURRET | DATE | 大包到台时间 |
| STEEL_WEIGHT_LADLE_ARRI | NUMBER(7,3) | 大包到台重量 |
| TIME_LADLE_OPEN | DATE |  |
| STEEL_WEIGHT_LADLE_CLOSE | NUMBER(7,3) |  |
| TIME_LADLE_CLOSE | DATE |  |
| REMAIN_MINUTES | NUMBER(5) |  |
| TIME_CUT_BEGIN | DATE | 炉次开始切割时间 |
| TIME_CUT_END | DATE |  |
| TIME_CREATE | DATE |  |
| NUM_SLAB | NUMBER(2) | 铸坯数目 |
| S1_SPEED_AVG | NUMBER(3,2) | 1流平均拉速 |
| S2_SPEED_AVG | NUMBER(3,2) |  |
| GROUP_SEQUENCE_CODE | NUMBER(1) | 班次 |
| GROUP_CODE | NUMBER(1) | 班组 |
| HEAD_WEIGHT | NUMBER(6) | 切头总重 |
| TAIL_WEGIHT | NUMBER(6) | 切尾总重 |
| READ_FLAG | VARCHAR2(1) | 读取标志 |
| SLAB_WEIGHT | NUMBER(7) | 铸坯总重量 |
| SLAB_YIELD | NUMBER(5) |  |
| CAST_LENGTH | NUMBER(7) | 总长度 |
| HEAT_FLAG | VARCHAR2(5) | 是否尾炉 |
| TEMP_WATER_IN | NUMBER(7,3) | 入侧水温 |
| TEMP_WATER_OUT | NUMBER(7,3) | 出侧水温 |

### 铸坯切割实绩接口表（32 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| SLAB_ID | VARCHAR2(20) | 铸坯号 |
| SLAB_NO | VARCHAR2(20) | 计划铸坯号 |
| HEAT_ID | VARCHAR2(12) | 炉次号 |
| STRAND_NO | NUMBER(1) | 流号 |
| PIECE_WEIGHT | NUMBER(5) | 理论重量 |
| PIECE_WEIGHT_ACT | NUMBER(5) | 实际重量 |
| PIECE_WEIGHT_ACT_TIME | DATE | 称重时间 |
| SLAB_LENGTH | NUMBER(5) | 长度 |
| SLAB_WIDTH | NUMBER(4) | 宽度 |
| SLAB_THICKNESS | NUMBER(9,3) | 厚度 |
| HOT_SEND_FLAG | VARCHAR2(1) | 去向1热送0下线 |
| TIME_CUT_START | DATE | 切割开始时间 |
| TIME_CUT_END | DATE | 切割结束时间 |
| SLAB_CUT_POS | VARCHAR2(20) | 铸坯切割位置 |
| SLAB_CODE | VARCHAR2(1) | 1: 头坯;2: 尾坯; 0-正常坯 |
| SLAB_QUALITY_CODE | NUMBER(1) | 表面质量预测代码1合格2检查3缺陷 |
| CUT_CONTROL | NUMBER(1) |  |
| TIME_CREATE | DATE |  |
| READ_FLAG | NUMBER(1) | 0、默认状态； |
| PLAN_LENGTH | NUMBER(5) | 计划长度 |
| PLAN_WIDTH | NUMBER(5) | 计划宽度 |
| PLAN_THICKNESS | NUMBER(5) | 计划厚度 |
| WEDGE_CODE | NUMBER(1) | 楔形标志0、1头宽、2尾宽 |
| START_WIDTH | NUMBER(4) | 开始宽度 |
| END_WIDTH | NUMBER(4) | 结束宽度 |
| TEMP_TUNDISH_AVG | NUMBER(4) | 中包平均温度 |
| CAST_SPEED_MAX | NUMBER(3,2) | 最大拉速 |
| CAST_SPEED_MIN | NUMBER(3,2) | 最小拉速 |
| CAST_SPEED_AVG | NUMBER(3,2) | 平均拉速 |
| SURPLUS_CODE | NUMBER(1) | 是否余材1是0否 |
| PROD_CUT_CODE | NUMBER(1) | 切割实际类型1切割2喷号3称重 |
| CAST_NO | VARCHAR2(5) | 铸机号 |

### 中间包温度实绩接口表（4 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| CAST_NO | VARCHAR2(5) | 铸机号 |
| HEAT_NO | VARCHAR2(20) | 炉号 |
| STEEL_WEIGHT | NUMBER(5) | 钢包剩余重量 |
| TUNDISH_TEMP | NUMBER(5) | 中包温度 |

### 加热炉PDI接口表（31 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| MES_NO | NUMBER | 消息序列号 |
| SEND_TIME | VARCHAR2(14) | 消息发送时间，发送方填写 |
| MES_TYPE | NUMBER | 0:新增，1:删除，2：修改 |
| HANDLE_TIME | VARCHAR2(14) | 消息处理时间 |
| HANDLE_REMARK | VARCHAR2(200) | 接收方填写消息处理备注 |
| HANDLE_FLAG | VARCHAR2(1) | 已处理标志位（N:未接受,P接收成功:,E:处理失败） |
| PLAN_NO | VARCHAR2(10) | 轧制计划号 |
| SLAB_NO | VARCHAR2(14) | 钢坯号 |
| SLABNUM | NUMBER(5) | 计划钢坯数量 |
| SLABWET_ALL | NUMBER(8,3) | 计划轧制重量\[ton\] |
| Material_STEELGRADE | VARCHAR2(24) | 原料钢种 |
| PRODUCT_STEELGRADE | VARCHAR2(24) | 产品钢种 |
| SLABTHK | NUMBER(6,2) | 钢坯厚度\[mm\] |
| SLABWID | NUMBER(7,2) | 钢坯宽度\[mm\] |
| SLABLEN | NUMBER(8,2) | 钢坯长度\[mm\] |
| PRODUCT_LEN | NUMBER(7,2) | 产品长度\[mm\] |
| PRODUCT_DIAM | NUMBER(7,2) | 产品直径\[mm\] |
| PRODUCT_CODE | VARCHAR2(24) | 产品规范 |
| Metal_CODE | VARCHAR2(24) | 冶金规范 |
| PRODUCT_STD | VARCHAR2(24), | 执行标准 |
| PLAN_TYPE | NUMBER(1) | 0－冷装, 1－热装 |
| ISSIMULATION | NUMBER(1) | 0－正式，1－试车 |
| PRE_TARGET_TEMP_MAX | INTEGER | 预热段目标温度上限 |
| PRE_TARGET_TEMP_MIN | INTEGER | 预热段目标温度下限 |
| HEAT1_TARGET_TEMPM_MAX | INTEGER | 加热一段目标温度上限 |
| HEAT1_TARGET_TEMPM_MIN | INTEGER | 加热一段目标温度下限 |
| HEAT2_TARGET_TEMP_MAX | INTEGER | 加热二段目标温度上限 |
| HEAT2_TARGET_TEMP_MIN | INTEGER | 加热二段目标温度下限 |
| SOAK_TARGET_TEMP_MAX | INTEGER | 均热段目标温度上限 |
| SOAK_TARGET_TEMP_MIN | INTEGER | 均热段目标温度下限 |
| STR_memo | VARCHAR2(500) | 备注 |

### 加热炉入炉实绩接口表（17 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| Mes_No | NUMBER | 消息序列号 |
| Send_Time | VARCHAR2(14) | 消息发送时间；消息发送时间，发送方填写 |
| Mes_Type | NUMBER | 消息类型；0:新增，1:删除，2修改 |
| Handle_Time | VARCHAR2(14) | 消息处理时间 |
| Handle_Remark | VARCHAR2(200) | 消息处理备注；接收方填写消息处理备注 |
| Handle_Flag | VARCHAR2(1) | 处理标志位；已处理标志位（N:未接受,P接收成功:,E:处理失败） |
| Plan_no | VARCHAR2(10) | 轧制计划号 |
| Heat_No | VARCHAR2(10) | 炉号 |
| Slab_No | VARCHAR2(14) | 钢坯号 |
| Fur_No | VARCHAR2(1) | 加热炉炉座号 |
| Group_No | VARCHAR2(1) | 班组；甲: 班组 = "1" 乙: 班组 = "2" 丙: 班组 = "3" 丁: 班组 = "4" |
| Shift_No | VARCHAR2(1) | 班次；夜: 班次 = "1" 白: 班次 = "2" 中: 班次 = "3" |
| Entry_Time | VARCHAR2(14) | 装炉时间 |
| Entry_Temp | NUMBER(4) | 装炉温度 |
| Act_Weight | NUMBER(6,3) | 实重；实重(t) |
| Entry_Type | VARCHAR2(1) | 装炉方式；装炉方式（0:冷装；1:热装） |
| SLAB_SEQ | NUMBER(4) | 钢坯顺序号；轧号内第几支 |

### 加热炉出炉实绩接口表（33 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| Mes_No | NUMBER | 消息序列号 |
| Send_Time | VARCHAR2(14) | 消息发送时间；消息发送时间，发送方填写 |
| Mes_Type | NUMBER | 消息类型；0:新增，1:删除，2修改 |
| Handle_Time | VARCHAR2(14) | 消息处理时间 |
| Handle_Remark | VARCHAR2(200) | 消息处理备注；接收方填写消息处理备注 |
| Handle_Flag | VARCHAR2(1) | 处理标志位；已处理标志位（N:未接受,P接收成功:,E:处理失败） |
| Plan_no | VARCHAR2(10) | 轧制计划号 |
| Heat_No | VARCHAR2(10) | 炉号 |
| Slab_No | VARCHAR2(14) | 钢坯号 |
| Fur_No | VARCHAR2(1) | 加热炉炉座号 |
| Group_No | VARCHAR2(1) | 班组；甲: 班组 = "1" 乙: 班组 = "2" 丙: 班组 = "3" 丁: 班组 = "4" |
| Shift_No | VARCHAR2(1) | 班次；夜: 班次 = "1" 白: 班次 = "2" 中: 班次 = "3" |
| Exit_Time | VARCHAR2(14) | 出炉时间 |
| Exit_Temp | NUMBER(4) | 出炉温度 |
| During_Time | NUMBER(3) | 在炉时长；在炉时长(min) |
| PRE_FUR_TEMP_MAX | INTEGER | 预热段温度最大值 |
| PRE_FUR_TEMP_MIN | INTEGER | 预热段温度最业值 |
| IN_H1_TIME | DATE | 进入一加时间 |
| H1_FUR_TEMP_MAX | INTEGER | 一加温度最大值 |
| H1_FUR_TEMP_MIN | INTEGER | 一加温度最小值 |
| IN_H2_TIME | DATE | 进入二加时间 |
| H2_FUR_TEMP_MAX | INTEGER | 二加温度最大值 |
| H2_FUR_TEMP_MIN | INTEGER | 二加温度最小值 |
| IN_SOAK_TIME | DATE | 进入均热段时间 |
| SOAK_FUR_TEMP_MAX | INTEGER | 均热段温度最大值 |
| SOAK_FUR_TEMP_MIN | INTEGER | 均热段温度最小值 |
| CHECK_TIME | DATE | 核对时间 |
| CHARGE_TIME | DATE | 装炉时间 |
| CHARGE_TEMP | NUMBER | 装炉温度 |
| TOP_FACE_TEMP | INTEGER | 上表面温度 |
| CORE_TEMP | INTEGER | 中心温度 |
| BOT_FACE_TEMP | INTEGER | 下表面温度 |
| SLAB_SEQ | NUMBER(4) | 钢坯顺序号；轧号内第几支 |

### 加热炉加热实绩接口表（32 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| Mes_No | NUMBER | 消息序列号 |
| Send_Time | VARCHAR2(14) | 消息发送时间；消息发送时间，发送方填写 |
| Mes_Type | NUMBER | 消息类型；0:新增，1:删除，2修改 |
| Handle_Time | VARCHAR2(14) | 消息处理时间 |
| Handle_Remark | VARCHAR2(200) | 消息处理备注；接收方填写消息处理备注 |
| Handle_Flag | VARCHAR2(1) | 处理标志位；已处理标志位（N:未接受,P接收成功:,E:处理失败） |
| Plan_no | VARCHAR2(10) | 轧制计划号 |
| Heat_No | VARCHAR2(10) | 炉号 |
| Slab_No | VARCHAR2(14) | 钢坯号 |
| Fur_No | VARCHAR2(1) | 加热炉炉座号 |
| Group_No | VARCHAR2(1) | 班组；甲: 班组 = "1" 乙: 班组 = "2" 丙: 班组 = "3" 丁: 班组 = "4" |
| Shift_No | VARCHAR2(1) | 班次；夜: 班次 = "1" 白: 班次 = "2" 中: 班次 = "3" |
| Heat_Time | NUMBER(3) | 加热时间；加热时间(min) |
| AIR_PRE_TEMP | NUMBER(4) | 空气预热温度 |
| GAS_PRE_TEMP | NUMBER(4) | 煤气预热温度 |
| Pre_Temp1 | NUMBER(4) | 轧侧预热段温度 |
| Pre_Temp2 | NUMBER(4) | 非轧侧预热段温度 |
| Heat1_Temp1 | NUMBER(4) | 一加上部轧侧加热温度；一加段上部轧侧加热温度 |
| Heat1_Temp2 | NUMBER(4) | 一加上部非轧侧加热温度；一加段上部非轧侧加热温度 |
| Heat1_Temp3 | NUMBER(4) | 一加下部轧侧加热温度；一加段下部轧侧加热温度 |
| Heat1_Temp4 | NUMBER(4) | 一加下部非轧侧加热温度；一加段下部非轧侧加热温度 |
| Heat2_Temp1 | NUMBER(4) | 二加段上部轧侧加热温度 |
| Heat2_Temp2 | NUMBER(4) | 二加段上部非轧侧加热温度 |
| Heat2_Temp3 | NUMBER(4) | 二加段下部轧侧加热温度 |
| Heat2_Temp4 | NUMBER(4) | 二加段下部非轧侧加热温度 |
| SOAK_TEMP1 | NUMBER(4) | 均热段上部轧侧加热温度 |
| SOAK_TEMP2 | NUMBER(4) | 均热段上部非轧侧加热温度 |
| SOAK_TEMP3 | NUMBER(4) | 均热段下部轧侧加热温度 |
| SOAK_TEMP4 | NUMBER(4) | 均热段下部非轧侧加热温度 |
| GAS_PRESURE | NUMBER(7,3) | 煤气压力；煤气压力(kPa) |
| GAS_CAL | NUMBER(7,3) | 煤气热值；煤气热值(KJ) |
| SLAB_SEQ | NUMBER(4) | 钢坯顺序号；轧号内第几支 |

### 吊销实绩接口表（16 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| Mes_No | NUMBER | 消息序列号 |
| Send_Time | VARCHAR2(14) | 消息发送时间；消息发送时间，发送方填写 |
| Mes_Type | NUMBER | 消息类型；0:新增，1:删除，2修改 |
| Handle_Time | VARCHAR2(14) | 消息处理时间 |
| Handle_Remark | VARCHAR2(200) | 消息处理备注；接收方填写消息处理备注 |
| Handle_Flag | VARCHAR2(1) | 处理标志位；已处理标志位（N:未接受,P接收成功:,E:处理失败） |
| Plan_no | VARCHAR2(10) | 轧制计划号 |
| Heat_No | VARCHAR2(10) | 炉号 |
| Slab_No | VARCHAR2(14) | 钢坯号 |
| Fur_No | VARCHAR2(1) | 加热炉炉座号 |
| Dispose_Time | VARCHAR2(14) | 吊销时间 |
| Group_No | VARCHAR2(1) | 班组；甲: 班组 = "1" 乙: 班组 = "2" 丙: 班组 = "3" 丁: 班组 = "4" |
| Shift_No | VARCHAR2(1) | 班次；夜: 班次 = "1" 白: 班次 = "2" 中: 班次 = "3" |
| Error_Type | NUMBER | 异常种类；固定为0 |
| Error_Reason | VARCHAR2(200) | 异常原因；吊销原因 |
| SLAB_SEQ | NUMBER(4) | 钢坯顺序号；轧号内第几支 |

### 轧线PDI接口表（296 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| CRT_USER_ID | VARCHAR2(20) | Created User ID |
| CRT_OBJ_ID | VARCHAR2(30) | Created Object ID |
| CRT_TM | TIMESTAMP(7) | Created Time |
| UPD_USER_ID | VARCHAR2(20) | Last Updated User ID |
| UPD_OBJ_ID | VARCHAR2(30) | Last Updated Object ID |
| UPD_TM | TIMESTAMP(7) | Last Updated Time |
| ARCHIVE_FL | VARCHAR2(1) | Record Archive Flag |
| ID | VARCHAR2(32) | GUID |
| MSGSIZE | NUMBER | integer 报文长度 |
| MSGID | NUMBER | integer 报文ID |
| MGSEQNO | NUMBER | integer 轧制单元内顺序 |
| FLAGS | NUMBER | integer 未使用 |
| YEAR | NUMBER | integer YYYY |
| MONTH | NUMBER | integer MM |
| DAY | NUMBER | integer DD |
| HOUR | NUMBER | integer HH24 |
| MINUTE | NUMBER | integer MM |
| SECOND | NUMBER | integer SS |
| MILLISEC | NUMBER | integer mmm |
| SENDMODE | NUMBER | "integer 0 = Add a New PDI1 = Update the PDI 2 = Delete (Cancel) the PDI""""" |
| PIECEIDL3 | VARCHAR2(32) | 钢板号/板坯号 |
| PIECEID | VARCHAR2(16) | *二级主键/钢板号Piece identification format (ASCII): S YY M NNNNN DFCC |
| SCHEDULEID | VARCHAR2(12) | *轧制计划号 |
| SEQNO | NUMBER | *integer4 轧制计划内顺序 |
| LOTNUMBER | VARCHAR2(20) | *批次号 |
| HEATID | VARCHAR2(20) | 炉号 |
| STEELGRADEID | VARCHAR2(12) | *钢种ID Q235B |
| STEELGRADESIGN | VARCHAR2(50) | *国家标准及牌号 |
| TENSILESTRENGTH | NUMBER | *number4 抗拉强度（国标/质量设计）国标最小值 |
| MATERIALPROP | NUMBER | integer 1 = Slab 2 = Ingot |
| SLABTHICKNESS | NUMBER | 板坯厚度 |
| SLABWIDTH | NUMBER | 板坯宽度 |
| SLABWIDTHHEAD | NUMBER |  |
| SLABWIDTHTAIL | NUMBER |  |
| SLABWIDTHCHGSTART | NUMBER |  |
| SLABWIDTHCHGSTOP | NUMBER |  |
| SLABLENGTH | NUMBER | 板坯长度 |
| SLABWEIGHT | NUMBER | 板坯重量 |
| INGOTTYPE | NUMBER | integer 铸锭 |
| INGOTWIDTHHEAD | NUMBER |  |
| INGOTTHICKHEAD | NUMBER |  |
| INGOTWIDTHTAIL | NUMBER |  |
| INGOTTHICKTAIL | NUMBER |  |
| INGOTLENGTH | NUMBER |  |
| INGOTWEIGHT | NUMBER |  |
| FURNACENO | NUMBER | *integer 加热炉号 1、2、3 |
| FURNACECOL | NUMBER | integer 道次号 |
| HOTCHARGEFLAG | NUMBER | *integer 冷/热送 |
| HOTCHARGETEMP | NUMBER | 装炉温度 没有 |
| CHARGETIME | VARCHAR2(14) | string装炉时间 YYYYMMDDhhmmss |
| DISCHARGETEMP | NUMBER | 出炉温度 |
| DISCHARGETEMPMIN | NUMBER | 出炉温度下限 |
| DISCHARGETEMPMAX | NUMBER | 出炉温度上限 |
| DISCHARGETEMPDIFF | NUMBER | 温度差 L2自己算 |
| LABORATORYFLAG | NUMBER | integer 是否有成分 1 = available, 0 = not |
| MATCOMPC | NUMBER |  |
| MATCOMPMN | NUMBER |  |
| MATCOMPP | NUMBER |  |
| MATCOMPS | NUMBER |  |
| MATCOMPSI | NUMBER |  |
| MATCOMPCU | NUMBER |  |
| MATCOMPV | NUMBER |  |
| MATCOMPNB | NUMBER |  |
| MATCOMPCR | NUMBER |  |
| MATCOMPNI | NUMBER |  |
| MATCOMPMO | NUMBER |  |
| MATCOMPSN | NUMBER |  |
| MATCOMPN | NUMBER |  |
| MATCOMPB | NUMBER |  |
| MATCOMPALTOT | NUMBER |  |
| MATCOMPTI | NUMBER |  |
| MATCOMPCA | NUMBER |  |
| MATCOMPPB | NUMBER |  |
| MATCOMPALSOL | NUMBER |  |
| MATCOMPSB | NUMBER |  |
| MATCOMPZN | NUMBER |  |
| MATCOMPAS | NUMBER |  |
| MATCOMPCO | NUMBER |  |
| MATCOMPMG | NUMBER |  |
| MATCOMPZR | NUMBER |  |
| MATCOMPW | NUMBER |  |
| MATCOMPTA | NUMBER |  |
| MATSPARE1 | NUMBER |  |
| MATSPARE2 | NUMBER |  |
| MATSPARE3 | NUMBER |  |
| MATSPARE4 | NUMBER |  |
| MATSPARE5 | NUMBER |  |
| MATSPARE6 | NUMBER |  |
| MATSPARE7 | NUMBER |  |
| MATSPARE8 | NUMBER |  |
| MATSPARE9 | NUMBER |  |
| MATSPARE10 | NUMBER |  |
| RMEXITTHICKHOT | NUMBER | 中间坯 粗轧目标厚度 PDI基准/一次控轧厚度下限 |
| RMEXITTEMP | NUMBER | 中间坯 粗轧结束目标温度/一次控轧目标温度 |
| PRODUCTTHICKNESS | NUMBER | *目标轧制厚度 |
| PRODUCTTHICKNESSMIN | NUMBER | 下限 -1 |
| PRODUCTTHICKNESSMAX | NUMBER | 上限 +1 |
| PRODUCTWIDTH | NUMBER | *目标轧制宽度 |
| PRODUCTWIDTHMIN | NUMBER | -5 |
| PRODUCTWIDTHMAX | NUMBER | 5 |
| PRODUCTFLATNESS | NUMBER | 平整度 日照没有 |
| PRODUCTFLATNESSMIN | NUMBER |  |
| PRODUCTFLATNESSMAX | NUMBER |  |
| PRODUCTPROFILE | NUMBER | 凸度 没有 |
| PRODUCTPROFILEMIN | NUMBER |  |
| PRODUCTPROFILEMAX | NUMBER |  |
| PRODUCTTEMP | NUMBER | *终轧温度 |
| PRODUCTTEMPMIN | NUMBER | -50 |
| PRODUCTTEMPMAX | NUMBER | 50 |
| PRODUCTLENGTH | NUMBER | *母板长度/目标轧制长度 |
| PRODUCTLENGTHMIN | NUMBER | 计算 |
| PRODUCTLENGTHMAX | NUMBER | 计算 |
| QUENCHMODE | NUMBER | integer板坯淬火模式 1：不淬火 2 :淬火 加热炉二级 |
| REDAGAINTEMPAIM | NUMBER | 目标返红温度 |
| REDAGAINTEMPUPPERTOL | NUMBER | 目标返红温度上限 |
| REDAGAINTEMPLOWERTOL | NUMBER | 目标返红温度下限 |
| ACCMODE | NUMBER | 快冷ACC 默认投用：2 mode: 1 = transport piece through device 2 = operate piece in device |
| FINISHCOOLTEMPAIM | NUMBER | 快冷目标温度 |
| FINISHCOOLTEMPUPPERTOL | NUMBER | 快冷温度上限 |
| FINISHCOOLTEMPLOWERTOL | NUMBER | 快冷温度下限 |
| DESCMODE | NUMBER | integer除鳞模式 1：不除鳞 2 :除鳞 默认：2 |
| DESCSPEED | NUMBER | 除鳞速率 默认：1 |
| DESCPATTERN | NUMBER | integer除鳞位置.默认：1（1：入口、2：出口、3：出入口） |
| FINISHSIDE | NUMBER | integer轧制完成侧 默认：1（0：入口、1：出口） |
| ROLLDIRECT | NUMBER | integer轧制方向 默认：0（0 = 不限制 1 = 纵向 2 = 90°） |
| MILLMODE_RM | NUMBER | integer 粗轧机轧制模式 默认：2 （1 = 不使用，2 = 粗轧，3 = 粗轧+立辊） |
| MILLMODE_FM | NUMBER | integer 精轧机轧制模式 默认：2 （1 = 不使用，2 = 精轧，3 = 精轧+立辊） |
| TURNMODE_RM | NUMBER | integer 粗轧转钢模式 默认：2 （1：upstream；2：downstream 3：both） |
| TURNMODE_FM | NUMBER | integer 精轧转钢模式 默认：2 （1：upstream；2：downstream 3：both） |
| ROLLMODE | NUMBER | integer是否控轧 PDI（1 = AR普通轧制 2 = CR 控轧） |
| CTRLROLLMODE | NUMBER | integer控轧模式 PDI 1 = 正常控轧 2 = 2阶段控轧 3 = 3阶段控轧 |
| CTRLPHASETEMPSTART1 | NUMBER | 控轧开始温度 PDI |
| CTRLPHASETEMPSTART2 | NUMBER | 二阶段控轧开始温度 |
| CTRLPHASETEMPSTART3 | NUMBER | 三阶段控轧开始温度 |
| CTRLPHASETEMPEND1 | NUMBER | 控轧结束温度 |
| CTRLPHASETEMPEND2 | NUMBER | 二阶段控轧结束温度 |
| CTRLPHASETEMPEND3 | NUMBER | 三阶段控轧结束温度 |
| CTRLPHASETHICKEND1 | NUMBER | 一阶段后控轧厚度 |
| CTRLPHASETHICKEND2 | NUMBER | 二阶段后控轧厚度 PDI |
| BATCHMODE | NUMBER | integer 批轧模式 默认：0（0=single 1=static；2=dual；3=conti mode） |
| BATCHSIZE | NUMBER | integer 批轧尺寸 默认：0 |
| BATCHPOS | NUMBER | integer 批轧批内计数 默认：0 1 不批轧 n 给定批轧数 |
| PPLMODE | NUMBER | integer 预矫模式 （默认 2：1：不预矫） 2 ：预矫 |
| HPLMODE | NUMBER | integer 热矫模式 1：不热矫 （默认 2 ：热矫） |
| MARKMODE | NUMBER | integer 默认：1 喷号模式 0 = no top painting，1 = 0°纵向，2 = 180° |
| MARKNUM | NUMBER | integer 喷号次数 PDI |
| MARKSTARTDIS | NUMBER | 喷号开始位置 |
| MARKINTERDIS | NUMBER | 喷号间隔 |
| MARKINTERDIS2 | NUMBER | 喷号间隔2 |
| MARKINTERDIS3 | NUMBER | 喷号间隔3 |
| MARKINTERDIS4 | NUMBER | 喷号间隔4 |
| MARKINTERDIS5 | NUMBER | 喷号间隔5 |
| MARKINTERDIS6 | NUMBER | 喷号间隔6 |
| MARKINTERDIS7 | NUMBER | 喷号间隔7 |
| MARKINTERDIS8 | NUMBER | 喷号间隔8 |
| MARKINTERDIS9 | NUMBER | 喷号间隔9 PDI |
| MARKLOGO | NUMBER | integer PDI 喷号logo 0 = no LOGO n = LOGO number |
| MARKTEXT | VARCHAR2(70) | 喷号内容 PDI |
| NROFSUBS | NUMBER | integer 热分段剪子板数量 默认：1 |
| PRODUCTID1 | VARCHAR2(16) | 热分段板号1 / 钢板号 |
| PRODUCTNO1 | NUMBER | integer 序列号第几块 1 |
| ROUTESETNO1 | NUMBER | integer 剪切线去向默认：1 .1 = first route set；2 = second route set |
| PRODUCTLENGTHAIM1 | NUMBER | 热分段剪目标长度 目标长度 |
| PRODUCTWIDTHAIM1 | NUMBER | 目标宽度 |
| CBDESTINFLAG1 | NUMBER | integer 默认：3 冷床去向 1 = via CB1 2 = via CB2 3 = via CB3 |
| CBDESTINCOL1 | NUMBER | integer 默认：1 冷床列 0 = auto ；1：列1； 2：列2 |
| PRODUCTID2 | VARCHAR2(16) | 热分段板号2 |
| PRODUCTNO2 | NUMBER | integer 序列号 |
| ROUTESETNO2 | NUMBER | integer 剪切线去向 1 = first route set；2 = second route set |
| PRODUCTLENGTHAIM2 | NUMBER | 热分段剪目标长度 |
| PRODUCTWIDTHAIM2 | NUMBER | 目标宽度 |
| CBDESTINFLAG2 | NUMBER | integer 冷床去向 1 = via CB1 2 = via CB2 3 = via CB3 |
| CBDESTINCOL2 | NUMBER | integer 冷床列 0 = auto ；1：列1； 2：列2 |
| CUTMODE | NUMBER | integer热分段剪切模式 1；不分段剪 2：分段 |
| NROFCUTS | NUMBER | integer剪切数 |
| CUTNO1 | NUMBER | integer剪切序列号 1 |
| CUTNO2 | NUMBER | 2 |
| CUTNO3 | NUMBER | 3 |
| CUTNO4 | NUMBER | 4 |
| CUTNO5 | NUMBER | 5 |
| CUTNO6 | NUMBER |  |
| CUTNO7 | NUMBER |  |
| CUTNO8 | NUMBER |  |
| CUTNO9 | NUMBER |  |
| CUTNO10 | NUMBER |  |
| CUTNO11 | NUMBER |  |
| CUTNO12 | NUMBER |  |
| CUTNO13 | NUMBER |  |
| CUTNO14 | NUMBER |  |
| CUTNO15 | NUMBER |  |
| CUTNO16 | NUMBER |  |
| CUTNO17 | NUMBER |  |
| CUTNO18 | NUMBER |  |
| CUTNO19 | NUMBER |  |
| CUTNO20 | NUMBER |  |
| CUTTYPE1 | NUMBER | integer切割模式 1 = Hot Deviding cut ；2 = Production piece ；3 = Head crop ；4 = Inter crop；5 = Tail crop ；6 = Test piece cut |
| CUTTYPE2 | NUMBER | 1、热分切 |
| CUTTYPE3 | NUMBER |  |
| CUTTYPE4 | NUMBER |  |
| CUTTYPE5 | NUMBER |  |
| CUTTYPE6 | NUMBER |  |
| CUTTYPE7 | NUMBER |  |
| CUTTYPE8 | NUMBER |  |
| CUTTYPE9 | NUMBER |  |
| CUTTYPE10 | NUMBER |  |
| CUTTYPE11 | NUMBER |  |
| CUTTYPE12 | NUMBER |  |
| CUTTYPE13 | NUMBER |  |
| CUTTYPE14 | NUMBER |  |
| CUTTYPE15 | NUMBER |  |
| CUTTYPE16 | NUMBER |  |
| CUTTYPE17 | NUMBER |  |
| CUTTYPE18 | NUMBER |  |
| CUTTYPE19 | NUMBER |  |
| CUTTYPE20 | NUMBER |  |
| CUTLENAIM1 | NUMBER | 目标长度，切的每一刀的长度 |
| CUTLENAIM2 | NUMBER |  |
| CUTLENAIM3 | NUMBER |  |
| CUTLENAIM4 | NUMBER |  |
| CUTLENAIM5 | NUMBER |  |
| CUTLENAIM6 | NUMBER |  |
| CUTLENAIM7 | NUMBER |  |
| CUTLENAIM8 | NUMBER |  |
| CUTLENAIM9 | NUMBER |  |
| CUTLENAIM10 | NUMBER |  |
| CUTLENAIM11 | NUMBER |  |
| CUTLENAIM12 | NUMBER |  |
| CUTLENAIM13 | NUMBER |  |
| CUTLENAIM14 | NUMBER |  |
| CUTLENAIM15 | NUMBER |  |
| CUTLENAIM16 | NUMBER |  |
| CUTLENAIM17 | NUMBER |  |
| CUTLENAIM18 | NUMBER |  |
| CUTLENAIM19 | NUMBER |  |
| CUTLENAIM20 | NUMBER |  |
| PLANTDESTIN1 | NUMBER | integer 0 = undefined / scrap；1 = to piler 1；2 = to piler 2 |
| PLANTDESTIN2 | NUMBER | 默认 0 去向 |
| PLANTDESTIN3 | NUMBER |  |
| PLANTDESTIN4 | NUMBER |  |
| PLANTDESTIN5 | NUMBER |  |
| PLANTDESTIN6 | NUMBER |  |
| PLANTDESTIN7 | NUMBER |  |
| PLANTDESTIN8 | NUMBER |  |
| PLANTDESTIN9 | NUMBER |  |
| PLANTDESTIN10 | NUMBER |  |
| PLANTDESTIN11 | NUMBER |  |
| PLANTDESTIN12 | NUMBER |  |
| PLANTDESTIN13 | NUMBER |  |
| PLANTDESTIN14 | NUMBER |  |
| PLANTDESTIN15 | NUMBER |  |
| PLANTDESTIN16 | NUMBER |  |
| PLANTDESTIN17 | NUMBER |  |
| PLANTDESTIN18 | NUMBER |  |
| PLANTDESTIN19 | NUMBER |  |
| PLANTDESTIN20 | NUMBER |  |
| CUSTOMERCODE | VARCHAR2(40) | 客户编码 |
| SPAREINT1 | NUMBER | integer4 备用1 |
| SPAREINT2 | NUMBER | integer4 备用2 |
| SPAREINT3 | NUMBER | integer4 备用3 |
| SPAREINT4 | NUMBER | integer4 备用4 |
| SPAREINT5 | NUMBER | integer4 备用5 |
| SPAREINT6 | NUMBER | integer4 备用6 |
| SPAREINT7 | NUMBER | integer4 备用7 |
| SPAREINT8 | NUMBER | integer4 备用8 |
| SPAREINT9 | NUMBER | integer4 备用9 |
| SPAREINT10 | NUMBER | integer4 备用10 |
| READ_FLAG | VARCHAR2(1) | 0 未读 1 已读 |
| READ_DATE | DATE | 读取时间 |
| PRODUCTID3 | VARCHAR2(16) | 热分段板号2 |
| PRODUCTNO3 | NUMBER | integer 序列号 |
| ROUTESETNO3 | NUMBER | integer 剪切线去向 1 = first route set；2 = second route set |
| PRODUCTLENGTHAIM3 | NUMBER | 热分段剪目标长度 |
| PRODUCTWIDTHAIM3 | NUMBER | 目标宽度 |
| CBDESTINFLAG3 | NUMBER | integer 冷床去向 1 = via CB1 2 = via CB2 3 = via CB3 |
| CBDESTINCOL3 | NUMBER | integer 冷床列 0 = auto ；1：列1； 2：列2 |
| PRODUCTID4 | VARCHAR2(16) | 热分段板号2 |
| PRODUCTNO4 | NUMBER | integer 序列号 |
| ROUTESETNO4 | NUMBER | integer 剪切线去向 1 = first route set；2 = second route set |
| PRODUCTLENGTHAIM4 | NUMBER | 热分段剪目标长度 |
| PRODUCTWIDTHAIM4 | NUMBER | 目标宽度 |
| CBDESTINFLAG4 | NUMBER | integer 冷床去向 1 = via CB1 2 = via CB2 3 = via CB3 |
| CBDESTINCOL4 | NUMBER | integer 冷床列 0 = auto ；1：列1； 2：列2 |
| PRODUCTID5 | VARCHAR2(16) | 热分段板号2 |
| PRODUCTNO5 | NUMBER | integer 序列号 |
| ROUTESETNO5 | NUMBER | integer 剪切线去向 1 = first route set；2 = second route set |
| PRODUCTLENGTHAIM5 | NUMBER | 热分段剪目标长度 |
| PRODUCTWIDTHAIM5 | NUMBER | 目标宽度 |
| CBDESTINFLAG5 | NUMBER | integer 冷床去向 1 = via CB1 2 = via CB2 3 = via CB3 |
| CBDESTINCOL5 | NUMBER | integer 冷床列 0 = auto ；1：列1； 2：列2 |
| PRODUCTID6 | VARCHAR2(16) | 热分段板号2 |
| PRODUCTNO6 | NUMBER | integer 序列号 |
| ROUTESETNO6 | NUMBER | integer 剪切线去向 1 = first route set；2 = second route set |
| PRODUCTLENGTHAIM6 | NUMBER | 热分段剪目标长度 |
| PRODUCTWIDTHAIM6 | NUMBER | 目标宽度 |
| CBDESTINFLAG6 | NUMBER | integer 冷床去向 1 = via CB1 2 = via CB2 3 = via CB3 |
| CBDESTINCOL6 | NUMBER | integer 冷床列 0 = auto ；1：列1； 2：列2 |

### 剪切PDI接口表（744 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| CRT_USER_ID | VARCHAR2(20) | Created User ID |
| CRT_OBJ_ID | VARCHAR2(30) | Created Object ID |
| CRT_TM | TIMESTAMP(7) | Created Time |
| UPD_USER_ID | VARCHAR2(20) | Last Updated User ID |
| UPD_OBJ_ID | VARCHAR2(30) | Last Updated Object ID |
| UPD_TM | TIMESTAMP(7) | Last Updated Time |
| ID | VARCHAR2(32) | GUID |
| MSGSIZE | NUMBER | integer 报文长度 |
| MSGID | NUMBER | integer 报文ID |
| MSGSEQNO | NUMBER | integer 轧制单元内顺序 |
| FLAGS | NUMBER | integer 备用 |
| YEAR | NUMBER | integer YYYY |
| MONTH | NUMBER | integer MM |
| DAY | NUMBER | integer DD |
| HOUR | NUMBER | integer HH24 |
| MINUTE | NUMBER | integer MM |
| SECOND | NUMBER | integer SS |
| MILLISEC | NUMBER | integer mmm |
| SENDMODE | NUMBER | """"integer 0 = Add a New PDI名称 1 = Update the PDI 2 = Delete (Cancel) the PDI""""" |
| PIECEIDL3 | VARCHAR2(32) | 母板号，生产管控 |
| PIECEID | VARCHAR2(16) | 二级主键 Piece identification format (ASCII): S YY M NNNNN DFCC |
| STEELGRADEID | VARCHAR2(12) | 钢种ID |
| STEELGRADESIGN | VARCHAR2(50) | 国家标准及牌号 |
| TENSILESTRENGTH | NUMBER | number4 抗拉强度（国标/质量设计） |
| PRODUCTTHICKNESS | NUMBER | 母板目标轧制厚度 |
| PRODUCTWIDTH | NUMBER | 母板未切边宽度 |
| PRODUCTLENGTH | NUMBER | 母板长度 |
| PRODUCTWEIGHT | NUMBER | 母板重量 |
| NROFSUBS | NUMBER | integer 剪切子板数量 最大值 6 |
| PRODUCTID1 | VARCHAR2(16) | 子板号1 |
| PRODUCTNO1 | NUMBER | integer 序列号 |
| ROUTESETNO1 | NUMBER | integer 剪切线去向 1 = first route set；2 = second route set |
| PRODUCTLENGTHAIM1 | NUMBER | 子板目标长度 |
| PRODUCTWIDTHAIM1 | NUMBER | 目标宽度（切边之后的宽度） |
| CBDESTINFLAG1 | NUMBER | integer 冷床去向 1 = via CB1 2 = via CB2 3 = via CB3 |
| CBDESTINCOL1 | NUMBER | integer 冷床列 0 = auto ；1：列1； 2：列2 |
| PRODUCTID2 | VARCHAR2(16) | 子板号2 |
| PRODUCTNO2 | NUMBER | integer 序列号 |
| ROUTESETNO2 | NUMBER | integer 剪切线去向 1 = first route set；2 = second route set |
| PRODUCTLENGTHAIM2 | NUMBER | 子板目标长度 |
| PRODUCTWIDTHAIM2 | NUMBER | 目标宽度（切边之后的宽度） |
| CBDESTINFLAG2 | NUMBER | integer 冷床去向 1 = via CB1 2 = via CB2 3 = via CB3 |
| CBDESTINCOL2 | NUMBER | integer 冷床列 0 = auto ；1：列1； 2：列2 |
| TURNOVERFLAG | NUMBER | integer翻板 0：不翻板 1：翻板 默认：0 |
| COLDLEVELFLAG | NUMBER | integer冷矫 0：不冷矫 1：冷矫 默认：0 |
| USTMODE | NUMBER | integer探伤 1：不探伤 2：探伤 默认：1 |
| USTQUALITY1 | VARCHAR2(8) | 一级探伤标准 |
| USTQUALITY2 | VARCHAR2(8) | 二级探伤标准 |
| TRIMREQ | NUMBER | integer是否切边 0：不剪切 1：剪切 |
| TRIMTYPE | NUMBER | integer剪切模式 1 = 圆盘剪 2 = 双边剪 =剪切线去向 |
| CUTMODE | NUMBER | integer剪切模式 1；不剪 2：剪切 定尺剪 |
| NROFCUTS | NUMBER | integer剪切数 |
| CUTNO1 | NUMBER | integer剪切序列号 |
| CUTNO2 | NUMBER |  |
| CUTNO3 | NUMBER |  |
| CUTNO4 | NUMBER |  |
| CUTNO5 | NUMBER |  |
| CUTNO6 | NUMBER |  |
| CUTNO7 | NUMBER |  |
| CUTNO8 | NUMBER |  |
| CUTNO9 | NUMBER |  |
| CUTNO10 | NUMBER |  |
| CUTNO11 | NUMBER |  |
| CUTNO12 | NUMBER |  |
| CUTNO13 | NUMBER |  |
| CUTNO14 | NUMBER |  |
| CUTNO15 | NUMBER |  |
| CUTNO16 | NUMBER |  |
| CUTNO17 | NUMBER |  |
| CUTNO18 | NUMBER |  |
| CUTNO19 | NUMBER |  |
| CUTNO20 | NUMBER |  |
| CUTTYPE1 | NUMBER | integer切割模式 1 = Hot Deviding cut ；2 = Production piece ；3 = Head crop ；4 = Inter crop；5 = Tail crop ；6 = Test piece cut |
| CUTTYPE2 | NUMBER |  |
| CUTTYPE3 | NUMBER |  |
| CUTTYPE4 | NUMBER |  |
| CUTTYPE5 | NUMBER |  |
| CUTTYPE6 | NUMBER |  |
| CUTTYPE7 | NUMBER |  |
| CUTTYPE8 | NUMBER |  |
| CUTTYPE9 | NUMBER |  |
| CUTTYPE10 | NUMBER |  |
| CUTTYPE11 | NUMBER |  |
| CUTTYPE12 | NUMBER |  |
| CUTTYPE13 | NUMBER |  |
| CUTTYPE14 | NUMBER |  |
| CUTTYPE15 | NUMBER |  |
| CUTTYPE16 | NUMBER |  |
| CUTTYPE17 | NUMBER |  |
| CUTTYPE18 | NUMBER |  |
| CUTTYPE19 | NUMBER |  |
| CUTTYPE20 | NUMBER |  |
| CUTLENAIM1 | NUMBER | 目标长度 |
| CUTLENAIM2 | NUMBER |  |
| CUTLENAIM3 | NUMBER |  |
| CUTLENAIM4 | NUMBER |  |
| CUTLENAIM5 | NUMBER |  |
| CUTLENAIM6 | NUMBER |  |
| CUTLENAIM7 | NUMBER |  |
| CUTLENAIM8 | NUMBER |  |
| CUTLENAIM9 | NUMBER |  |
| CUTLENAIM10 | NUMBER |  |
| CUTLENAIM11 | NUMBER |  |
| CUTLENAIM12 | NUMBER |  |
| CUTLENAIM13 | NUMBER |  |
| CUTLENAIM14 | NUMBER |  |
| CUTLENAIM15 | NUMBER |  |
| CUTLENAIM16 | NUMBER |  |
| CUTLENAIM17 | NUMBER |  |
| CUTLENAIM18 | NUMBER |  |
| CUTLENAIM19 | NUMBER |  |
| CUTLENAIM20 | NUMBER |  |
| PLANTDESTIN1 | NUMBER | integer 0 = undefined / scrap；1 = to piler 1；2 = to piler 2 |
| PLANTDESTIN2 | NUMBER | 0：不堆垛 1：1号堆垛机 2：2号堆垛 = 剪切模式 |
| PLANTDESTIN3 | NUMBER |  |
| PLANTDESTIN4 | NUMBER |  |
| PLANTDESTIN5 | NUMBER |  |
| PLANTDESTIN6 | NUMBER |  |
| PLANTDESTIN7 | NUMBER |  |
| PLANTDESTIN8 | NUMBER |  |
| PLANTDESTIN9 | NUMBER |  |
| PLANTDESTIN10 | NUMBER |  |
| PLANTDESTIN11 | NUMBER |  |
| PLANTDESTIN12 | NUMBER |  |
| PLANTDESTIN13 | NUMBER |  |
| PLANTDESTIN14 | NUMBER |  |
| PLANTDESTIN15 | NUMBER |  |
| PLANTDESTIN16 | NUMBER |  |
| PLANTDESTIN17 | NUMBER |  |
| PLANTDESTIN18 | NUMBER |  |
| PLANTDESTIN19 | NUMBER |  |
| PLANTDESTIN20 | NUMBER |  |
| SURFMODE | NUMBER | *integer 面喷模式 默认：1喷号 0 = no top painting；1 = 0° Longitudinal；2 = 180° Longitudinal |
| SURFPAINTNUM | NUMBER | *integer 面喷数 |
| SURFPAINTSTARTDIS | NUMBER | *number 开始位置 |
| SURFPAINTINTERDIS | NUMBER | *number 开始到结束位置间隔 |
| SURFLOGO | NUMBER | integer LOGO number;0 = no LOGO;n = LOGO number |
| SURFTEXT1 | VARCHAR2(70) | string 面喷喷印内容1 |
| SURFTEXT2 | VARCHAR2(70) | string 面喷喷印内容2 |
| SURFTEXT3 | VARCHAR2(70) | string 面喷喷印内容3 |
| SURFTEXT4 | VARCHAR2(70) | string 面喷喷印内容4 |
| SURFTEXT5 | VARCHAR2(70) | string 面喷喷印内容5 |
| SURFTEXT6 | VARCHAR2(70) | string 面喷喷印内容6 |
| SURFTEXT7 | VARCHAR2(70) | string 面喷喷印内容7 |
| SURFTEXT8 | VARCHAR2(70) | string 面喷喷印内容8 |
| SIDEMODE | NUMBER | *integer 默认：1 侧喷模式Edge painting mode.0 = no Edge painting 1 = longitudinal edge downstream right 2 = longitudinal edge downstream left 3 = longitudinal edge downstream right and left |
| SIDETEXT | VARCHAR2(60) | string 侧喷内容 |
| SIDEBARMODE | NUMBER | integer Barcode mode 默认：0 0 = do no paint a barcode; 1 = paint a barcode |
| SIDEBARCODE | VARCHAR2(60) | String of ASCII 空 characters default = string of "space" means empty line |
| SEALMODE | NUMBER | integer 是否打钢印，默认：1 .0 = no top punching;1 = 0° Longitudinal ;2 = 180° Longitudinal |
| SEALLOGO | NUMBER | integer LOGO 默认：1 number.0 = no LOGO;n = LOGO number |
| SEALTEXT1 | VARCHAR2(30) | String of ASCII 默认：空 characters default = string of "space" means empty line |
| SEALTEXT2 | VARCHAR2(30) | String of ASCII 默认：空 characters default = string of "space" means empty line |
| TURNOVERFLAG2 | NUMBER | integer翻板 0：不翻板 1：翻板 |
| COLDLEVELFLAG2 | NUMBER | integer冷矫 0：不冷矫 1：冷矫 |
| USTMODE2 | NUMBER | integer探伤 1：不探伤 2：探伤 |
| USTQUALITY1_2 | VARCHAR2(8) | 一级探伤标准 |
| USTQUALITY2_2 | VARCHAR2(8) | 二级探伤标准 |
| TRIMREQ2 | NUMBER | integer是否切边 0：不剪切 1：剪切 |
| TRIMTYPE2 | NUMBER | integer剪切模式 1 = 圆盘剪 2 = 双边剪 |
| CUTMODE2 | NUMBER | integer剪切模式 1；不剪 2：剪切 |
| NROFCUTS2 | NUMBER | integer剪切数 |
| CUTNO1_2 | NUMBER | integer剪切序列号 |
| CUTNO2_2 | NUMBER |  |
| CUTNO3_2 | NUMBER |  |
| CUTNO4_2 | NUMBER |  |
| CUTNO5_2 | NUMBER |  |
| CUTNO6_2 | NUMBER |  |
| CUTNO7_2 | NUMBER |  |
| CUTNO8_2 | NUMBER |  |
| CUTNO9_2 | NUMBER |  |
| CUTNO10_2 | NUMBER |  |
| CUTNO11_2 | NUMBER |  |
| CUTNO12_2 | NUMBER |  |
| CUTNO13_2 | NUMBER |  |
| CUTNO14_2 | NUMBER |  |
| CUTNO15_2 | NUMBER |  |
| CUTNO16_2 | NUMBER |  |
| CUTNO17_2 | NUMBER |  |
| CUTNO18_2 | NUMBER |  |
| CUTNO19_2 | NUMBER |  |
| CUTNO20_2 | NUMBER |  |
| CUTTYPE1_2 | NUMBER | integer切割模式 1 = Hot Deviding cut ；2 = Production piece ；3 = Head crop ；4 = Inter crop；5 = Tail crop ；6 = Test piece cut |
| CUTTYPE2_2 | NUMBER |  |
| CUTTYPE3_2 | NUMBER |  |
| CUTTYPE4_2 | NUMBER |  |
| CUTTYPE5_2 | NUMBER |  |
| CUTTYPE6_2 | NUMBER |  |
| CUTTYPE7_2 | NUMBER |  |
| CUTTYPE8_2 | NUMBER |  |
| CUTTYPE9_2 | NUMBER |  |
| CUTTYPE10_2 | NUMBER |  |
| CUTTYPE11_2 | NUMBER |  |
| CUTTYPE12_2 | NUMBER |  |
| CUTTYPE13_2 | NUMBER |  |
| CUTTYPE14_2 | NUMBER |  |
| CUTTYPE15_2 | NUMBER |  |
| CUTTYPE16_2 | NUMBER |  |
| CUTTYPE17_2 | NUMBER |  |
| CUTTYPE18_2 | NUMBER |  |
| CUTTYPE19_2 | NUMBER |  |
| CUTTYPE20_2 | NUMBER |  |
| CUTLENAIM1_2 | NUMBER | 目标长度 |
| CUTLENAIM2_2 | NUMBER |  |
| CUTLENAIM3_2 | NUMBER |  |
| CUTLENAIM4_2 | NUMBER |  |
| CUTLENAIM5_2 | NUMBER |  |
| CUTLENAIM6_2 | NUMBER |  |
| CUTLENAIM7_2 | NUMBER |  |
| CUTLENAIM8_2 | NUMBER |  |
| CUTLENAIM9_2 | NUMBER |  |
| CUTLENAIM10_2 | NUMBER |  |
| CUTLENAIM11_2 | NUMBER |  |
| CUTLENAIM12_2 | NUMBER |  |
| CUTLENAIM13_2 | NUMBER |  |
| CUTLENAIM14_2 | NUMBER |  |
| CUTLENAIM15_2 | NUMBER |  |
| CUTLENAIM16_2 | NUMBER |  |
| CUTLENAIM17_2 | NUMBER |  |
| CUTLENAIM18_2 | NUMBER |  |
| CUTLENAIM19_2 | NUMBER |  |
| CUTLENAIM20_2 | NUMBER |  |
| PLANTDESTIN1_2 | NUMBER | integer 0 = undefined / scrap；1 = to piler 1；2 = to piler 2 |
| PLANTDESTIN2_2 | NUMBER |  |
| PLANTDESTIN3_2 | NUMBER |  |
| PLANTDESTIN4_2 | NUMBER |  |
| PLANTDESTIN5_2 | NUMBER |  |
| PLANTDESTIN6_2 | NUMBER |  |
| PLANTDESTIN7_2 | NUMBER |  |
| PLANTDESTIN8_2 | NUMBER |  |
| PLANTDESTIN9_2 | NUMBER |  |
| PLANTDESTIN10_2 | NUMBER |  |
| PLANTDESTIN11_2 | NUMBER |  |
| PLANTDESTIN12_2 | NUMBER |  |
| PLANTDESTIN13_2 | NUMBER |  |
| PLANTDESTIN14_2 | NUMBER |  |
| PLANTDESTIN15_2 | NUMBER |  |
| PLANTDESTIN16_2 | NUMBER |  |
| PLANTDESTIN17_2 | NUMBER |  |
| PLANTDESTIN18_2 | NUMBER |  |
| PLANTDESTIN19_2 | NUMBER |  |
| PLANTDESTIN20_2 | NUMBER |  |
| SURFMODE_2 | NUMBER | integer 面喷模式 0 = no top painting；1 = 0° Longitudinal；2 = 180° Longitudinal |
| SURFPAINTNUM_2 | NUMBER | integer 面喷数 |
| SURFPAINTSTARTDIS_2 | NUMBER | number 开始位置 |
| SURFPAINTINTERDIS_2 | NUMBER | number 开始到结束位置间隔 |
| SURFLOGO_2 | NUMBER | integer LOGO number;0 = no LOGO;n = LOGO number |
| SURFTEXT1_2 | VARCHAR2(70) | string 面喷喷印内容1 |
| SURFTEXT2_2 | VARCHAR2(70) | string 面喷喷印内容2 |
| SURFTEXT3_2 | VARCHAR2(70) | string 面喷喷印内容3 |
| SURFTEXT4_2 | VARCHAR2(70) | string 面喷喷印内容4 |
| SURFTEXT5_2 | VARCHAR2(70) | string 面喷喷印内容5 |
| SURFTEXT6_2 | VARCHAR2(70) | string 面喷喷印内容6 |
| SURFTEXT7_2 | VARCHAR2(70) | string 面喷喷印内容7 |
| SURFTEXT8_2 | VARCHAR2(70) | string 面喷喷印内容8 |
| SIDEMODE_2 | NUMBER | integer 侧喷模式Edge painting mode.0 = no Edge painting 1 = longitudinal edge downstream right 2 = longitudinal edge downstream left 3 = longitudinal edge downstream right and left |
| SIDETEXT_2 | VARCHAR2(60) | string 侧喷内容 |
| SIDEBARMODE_2 | NUMBER | integer Barcode mode 0 = do no paint a barcode; 1 = paint a barcode |
| SIDEBARCODE_2 | VARCHAR2(60) | String of ASCII characters default = string of "space" means empty line |
| SEALMODE_2 | NUMBER | integer 是否打钢印 .0 = no top punching;1 = 0° Longitudinal ;2 = 180° Longitudinal |
| SEALLOGO_2 | NUMBER | integer LOGO number.0 = no LOGO;n = LOGO number |
| SEALTEXT1_2 | VARCHAR2(30) | String of ASCII characters default = string of "space" means empty line |
| SEALTEXT2_2 | VARCHAR2(30) | String of ASCII characters default = string of "space" means empty line |
| CUSTOMERCODE | VARCHAR2(40) | 客户编码 |
| SPAREINT1 | NUMBER | integer4 备用1 |
| SPAREINT2 | NUMBER | integer4 备用2 |
| SPAREINT3 | NUMBER | integer4 备用3 |
| SPAREINT4 | NUMBER | integer4 备用4 |
| SPAREINT5 | NUMBER | integer4 备用5 |
| SPAREINT6 | NUMBER | integer4 备用6 |
| SPAREINT7 | NUMBER | integer4 备用7 |
| SPAREINT8 | NUMBER | integer4 备用8 |
| SPAREINT9 | NUMBER | integer4 备用9 |
| SPAREINT10 | NUMBER | integer4 备用10 |
| READ_FLAG | VARCHAR2(1) | 0 未读 1 已读 |
| READ_DATE | DATE | 读取时间 |
| PRODUCTID3 | VARCHAR2(16) | 子板号3 |
| PRODUCTNO3 | NUMBER | integer 序列号 |
| ROUTESETNO3 | NUMBER | integer 剪切线去向 1 = first route set；2 = second route set |
| PRODUCTLENGTHAIM3 | NUMBER | 子板目标长度 |
| PRODUCTWIDTHAIM3 | NUMBER | 目标宽度 |
| CBDESTINFLAG3 | NUMBER | integer 冷床去向 1 = via CB1 2 = via CB2 3 = via CB3 |
| CBDESTINCOL3 | NUMBER | integer 冷床列 0 = auto ；1：列1； 2：列2 |
| PRODUCTID4 | VARCHAR2(16) | 子板号4 |
| PRODUCTNO4 | NUMBER | integer 序列号 |
| ROUTESETNO4 | NUMBER | integer 剪切线去向 1 = first route set；2 = second route set |
| PRODUCTLENGTHAIM4 | NUMBER | 子板目标长度 |
| PRODUCTWIDTHAIM4 | NUMBER | 目标宽度 |
| CBDESTINFLAG4 | NUMBER | integer 冷床去向 1 = via CB1 2 = via CB2 3 = via CB3 |
| CBDESTINCOL4 | NUMBER | integer 冷床列 0 = auto ；1：列1； 2：列2 |
| PRODUCTID5 | VARCHAR2(16) | 子板号5 |
| PRODUCTNO5 | NUMBER | integer 序列号 |
| ROUTESETNO5 | NUMBER | integer 剪切线去向 1 = first route set；2 = second route set |
| PRODUCTLENGTHAIM5 | NUMBER | 子板目标长度 |
| PRODUCTWIDTHAIM5 | NUMBER | 目标宽度 |
| CBDESTINFLAG5 | NUMBER | integer 冷床去向 1 = via CB1 2 = via CB2 3 = via CB3 |
| CBDESTINCOL5 | NUMBER | integer 冷床列 0 = auto ；1：列1； 2：列2 |
| PRODUCTID6 | VARCHAR2(16) | 子板号6 |
| PRODUCTNO6 | NUMBER | integer 序列号 |
| ROUTESETNO6 | NUMBER | integer 剪切线去向 1 = first route set；2 = second route set |
| PRODUCTLENGTHAIM6 | NUMBER | 子板目标长度 |
| PRODUCTWIDTHAIM6 | NUMBER | 目标宽度 |
| CBDESTINFLAG6 | NUMBER | integer 冷床去向 1 = via CB1 2 = via CB2 3 = via CB3 |
| CBDESTINCOL6 | NUMBER | integer 冷床列 0 = auto ；1：列1； 2：列2 |
| TURNOVERFLAG3 | NUMBER | integer翻板 0：不翻板 1：翻板 |
| COLDLEVELFLAG3 | NUMBER | integer冷矫 0：不冷矫 1：冷矫 |
| USTMODE3 | NUMBER | integer探伤 1：不探伤 2：探伤 |
| USTQUALITY1_3 | VARCHAR2(8) | 一级探伤标准 |
| USTQUALITY2_3 | VARCHAR2(8) | 二级探伤标准 |
| TRIMREQ3 | NUMBER | integer是否切边 0：不剪切 1：剪切 |
| TRIMTYPE3 | NUMBER | integer剪切模式 1 = 圆盘剪 2 = 双边剪 |
| CUTMODE3 | NUMBER | integer剪切模式 1；不剪 2：剪切 |
| NROFCUTS3 | NUMBER | integer剪切数 |
| CUTNO1_3 | NUMBER | integer剪切序列号 |
| CUTNO2_3 | NUMBER |  |
| CUTNO3_3 | NUMBER |  |
| CUTNO4_3 | NUMBER |  |
| CUTNO5_3 | NUMBER |  |
| CUTNO6_3 | NUMBER |  |
| CUTNO7_3 | NUMBER |  |
| CUTNO8_3 | NUMBER |  |
| CUTNO9_3 | NUMBER |  |
| CUTNO10_3 | NUMBER |  |
| CUTNO11_3 | NUMBER |  |
| CUTNO12_3 | NUMBER |  |
| CUTNO13_3 | NUMBER |  |
| CUTNO14_3 | NUMBER |  |
| CUTNO15_3 | NUMBER |  |
| CUTNO16_3 | NUMBER |  |
| CUTNO17_3 | NUMBER |  |
| CUTNO18_3 | NUMBER |  |
| CUTNO19_3 | NUMBER |  |
| CUTNO20_3 | NUMBER |  |
| CUTTYPE1_3 | NUMBER | integer切割模式 1 = Hot Deviding cut ；2 = Production piece ；3 = Head crop ；4 = Inter crop；5 = Tail crop ；6 = Test piece cut |
| CUTTYPE2_3 | NUMBER | 1、热分切 2、定尺 3、切头 |
| CUTTYPE3_3 | NUMBER |  |
| CUTTYPE4_3 | NUMBER |  |
| CUTTYPE5_3 | NUMBER |  |
| CUTTYPE6_3 | NUMBER |  |
| CUTTYPE7_3 | NUMBER |  |
| CUTTYPE8_3 | NUMBER |  |
| CUTTYPE9_3 | NUMBER |  |
| CUTTYPE10_3 | NUMBER |  |
| CUTTYPE11_3 | NUMBER |  |
| CUTTYPE12_3 | NUMBER |  |
| CUTTYPE13_3 | NUMBER |  |
| CUTTYPE14_3 | NUMBER |  |
| CUTTYPE15_3 | NUMBER |  |
| CUTTYPE16_3 | NUMBER |  |
| CUTTYPE17_3 | NUMBER |  |
| CUTTYPE18_3 | NUMBER |  |
| CUTTYPE19_3 | NUMBER |  |
| CUTTYPE20_3 | NUMBER |  |
| CUTLENAIM1_3 | NUMBER | 目标长度、切头 |
| CUTLENAIM2_3 | NUMBER | 定尺 |
| CUTLENAIM3_3 | NUMBER | 定尺 |
| CUTLENAIM4_3 | NUMBER | 最后一个计算 |
| CUTLENAIM5_3 | NUMBER |  |
| CUTLENAIM6_3 | NUMBER |  |
| CUTLENAIM7_3 | NUMBER |  |
| CUTLENAIM8_3 | NUMBER |  |
| CUTLENAIM9_3 | NUMBER |  |
| CUTLENAIM10_3 | NUMBER |  |
| CUTLENAIM11_3 | NUMBER |  |
| CUTLENAIM12_3 | NUMBER |  |
| CUTLENAIM13_3 | NUMBER |  |
| CUTLENAIM14_3 | NUMBER |  |
| CUTLENAIM15_3 | NUMBER |  |
| CUTLENAIM16_3 | NUMBER |  |
| CUTLENAIM17_3 | NUMBER |  |
| CUTLENAIM18_3 | NUMBER |  |
| CUTLENAIM19_3 | NUMBER |  |
| CUTLENAIM20_3 | NUMBER |  |
| PLANTDESTIN1_3 | NUMBER | integer 0 = undefined / scrap；1 = to piler 1；2 = to piler 2 |
| PLANTDESTIN2_3 | NUMBER |  |
| PLANTDESTIN3_3 | NUMBER |  |
| PLANTDESTIN4_3 | NUMBER |  |
| PLANTDESTIN5_3 | NUMBER |  |
| PLANTDESTIN6_3 | NUMBER |  |
| PLANTDESTIN7_3 | NUMBER |  |
| PLANTDESTIN8_3 | NUMBER |  |
| PLANTDESTIN9_3 | NUMBER |  |
| PLANTDESTIN10_3 | NUMBER |  |
| PLANTDESTIN11_3 | NUMBER |  |
| PLANTDESTIN12_3 | NUMBER |  |
| PLANTDESTIN13_3 | NUMBER |  |
| PLANTDESTIN14_3 | NUMBER |  |
| PLANTDESTIN15_3 | NUMBER |  |
| PLANTDESTIN16_3 | NUMBER |  |
| PLANTDESTIN17_3 | NUMBER |  |
| PLANTDESTIN18_3 | NUMBER |  |
| PLANTDESTIN19_3 | NUMBER |  |
| PLANTDESTIN20_3 | NUMBER |  |
| SURFMODE_3 | NUMBER | integer 面喷模式 0 = no top painting；1 = 0° Longitudinal；2 = 180° Longitudinal |
| SURFPAINTNUM_3 | NUMBER | integer 面喷数 |
| SURFPAINTSTARTDIS_3 | NUMBER | number 开始位置 |
| SURFPAINTINTERDIS_3 | NUMBER | number 开始到结束位置间隔 |
| SURFLOGO_3 | NUMBER | integer LOGO number;0 = no LOGO;n = LOGO number |
| SURFTEXT1_3 | VARCHAR2(70) | string 面喷喷印内容1 |
| SURFTEXT2_3 | VARCHAR2(70) | string 面喷喷印内容2 |
| SURFTEXT3_3 | VARCHAR2(70) | string 面喷喷印内容3 |
| SURFTEXT4_3 | VARCHAR2(70) | string 面喷喷印内容4 |
| SURFTEXT5_3 | VARCHAR2(70) | string 面喷喷印内容5 |
| SURFTEXT6_3 | VARCHAR2(70) | string 面喷喷印内容6 |
| SURFTEXT7_3 | VARCHAR2(70) | string 面喷喷印内容7 |
| SURFTEXT8_3 | VARCHAR2(70) | string 面喷喷印内容8 |
| SIDEMODE_3 | NUMBER | integer 侧喷模式Edge painting mode.0 = no Edge painting 1 = longitudinal edge downstream right 2 = longitudinal edge downstream left 3 = longitudinal edge downstream right and left |
| SIDETEXT_3 | VARCHAR2(60) | string 侧喷内容 |
| SIDEBARMODE_3 | NUMBER | integer Barcode mode 0 = do no paint a barcode; 1 = paint a barcode |
| SIDEBARCODE_3 | VARCHAR2(60) | String of ASCII characters default = string of "space" means empty line |
| SEALMODE_3 | NUMBER | integer 是否打钢印 .0 = no top punching;1 = 0° Longitudinal ;2 = 180° Longitudinal |
| SEALLOGO_3 | NUMBER | integer LOGO number.0 = no LOGO;n = LOGO number |
| SEALTEXT1_3 | VARCHAR2(30) | String of ASCII characters default = string of "space" means empty line |
| SEALTEXT2_3 | VARCHAR2(30) | String of ASCII characters default = string of "space" means empty line |
| TURNOVERFLAG4 | NUMBER | integer翻板 0：不翻板 1：翻板 |
| COLDLEVELFLAG4 | NUMBER | integer冷矫 0：不冷矫 1：冷矫 |
| USTMODE4 | NUMBER | integer探伤 1：不探伤 2：探伤 |
| USTQUALITY1_4 | VARCHAR2(8) | 一级探伤标准 |
| USTQUALITY2_4 | VARCHAR2(8) | 二级探伤标准 |
| TRIMREQ4 | NUMBER | integer是否切边 0：不剪切 1：剪切 |
| TRIMTYPE4 | NUMBER | integer剪切模式 1 = 圆盘剪 2 = 双边剪 |
| CUTMODE4 | NUMBER | integer剪切模式 1；不剪 2：剪切 |
| NROFCUTS4 | NUMBER | integer剪切数 |
| CUTNO1_4 | NUMBER | integer剪切序列号 |
| CUTNO2_4 | NUMBER |  |
| CUTNO3_4 | NUMBER |  |
| CUTNO4_4 | NUMBER |  |
| CUTNO5_4 | NUMBER |  |
| CUTNO6_4 | NUMBER |  |
| CUTNO7_4 | NUMBER |  |
| CUTNO8_4 | NUMBER |  |
| CUTNO9_4 | NUMBER |  |
| CUTNO10_4 | NUMBER |  |
| CUTNO11_4 | NUMBER |  |
| CUTNO12_4 | NUMBER |  |
| CUTNO13_4 | NUMBER |  |
| CUTNO14_4 | NUMBER |  |
| CUTNO15_4 | NUMBER |  |
| CUTNO16_4 | NUMBER |  |
| CUTNO17_4 | NUMBER |  |
| CUTNO18_4 | NUMBER |  |
| CUTNO19_4 | NUMBER |  |
| CUTNO20_4 | NUMBER |  |
| CUTTYPE1_4 | NUMBER | integer切割模式 1 = Hot Deviding cut ；2 = Production piece ；3 = Head crop ；4 = Inter crop；5 = Tail crop ；6 = Test piece cut |
| CUTTYPE2_4 | NUMBER |  |
| CUTTYPE3_4 | NUMBER |  |
| CUTTYPE4_4 | NUMBER |  |
| CUTTYPE5_4 | NUMBER |  |
| CUTTYPE6_4 | NUMBER |  |
| CUTTYPE7_4 | NUMBER |  |
| CUTTYPE8_4 | NUMBER |  |
| CUTTYPE9_4 | NUMBER |  |
| CUTTYPE10_4 | NUMBER |  |
| CUTTYPE11_4 | NUMBER |  |
| CUTTYPE12_4 | NUMBER |  |
| CUTTYPE13_4 | NUMBER |  |
| CUTTYPE14_4 | NUMBER |  |
| CUTTYPE15_4 | NUMBER |  |
| CUTTYPE16_4 | NUMBER |  |
| CUTTYPE17_4 | NUMBER |  |
| CUTTYPE18_4 | NUMBER |  |
| CUTTYPE19_4 | NUMBER |  |
| CUTTYPE20_4 | NUMBER |  |
| CUTLENAIM1_4 | NUMBER | 目标长度 |
| CUTLENAIM2_4 | NUMBER |  |
| CUTLENAIM3_4 | NUMBER |  |
| CUTLENAIM4_4 | NUMBER |  |
| CUTLENAIM5_4 | NUMBER |  |
| CUTLENAIM6_4 | NUMBER |  |
| CUTLENAIM7_4 | NUMBER |  |
| CUTLENAIM8_4 | NUMBER |  |
| CUTLENAIM9_4 | NUMBER |  |
| CUTLENAIM10_4 | NUMBER |  |
| CUTLENAIM11_4 | NUMBER |  |
| CUTLENAIM12_4 | NUMBER |  |
| CUTLENAIM13_4 | NUMBER |  |
| CUTLENAIM14_4 | NUMBER |  |
| CUTLENAIM15_4 | NUMBER |  |
| CUTLENAIM16_4 | NUMBER |  |
| CUTLENAIM17_4 | NUMBER |  |
| CUTLENAIM18_4 | NUMBER |  |
| CUTLENAIM19_4 | NUMBER |  |
| CUTLENAIM20_4 | NUMBER |  |
| PLANTDESTIN1_4 | NUMBER | integer 0 = undefined / scrap；1 = to piler 1；2 = to piler 2 |
| PLANTDESTIN2_4 | NUMBER |  |
| PLANTDESTIN3_4 | NUMBER |  |
| PLANTDESTIN4_4 | NUMBER |  |
| PLANTDESTIN5_4 | NUMBER |  |
| PLANTDESTIN6_4 | NUMBER |  |
| PLANTDESTIN7_4 | NUMBER |  |
| PLANTDESTIN8_4 | NUMBER |  |
| PLANTDESTIN9_4 | NUMBER |  |
| PLANTDESTIN10_4 | NUMBER |  |
| PLANTDESTIN11_4 | NUMBER |  |
| PLANTDESTIN12_4 | NUMBER |  |
| PLANTDESTIN13_4 | NUMBER |  |
| PLANTDESTIN14_4 | NUMBER |  |
| PLANTDESTIN15_4 | NUMBER |  |
| PLANTDESTIN16_4 | NUMBER |  |
| PLANTDESTIN17_4 | NUMBER |  |
| PLANTDESTIN18_4 | NUMBER |  |
| PLANTDESTIN19_4 | NUMBER |  |
| PLANTDESTIN20_4 | NUMBER |  |
| SURFMODE_4 | NUMBER | integer 面喷模式 0 = no top painting；1 = 0° Longitudinal；2 = 180° Longitudinal |
| SURFPAINTNUM_4 | NUMBER | integer 面喷数 |
| SURFPAINTSTARTDIS_4 | NUMBER | number 开始位置 |
| SURFPAINTINTERDIS_4 | NUMBER | number 开始到结束位置间隔 |
| SURFLOGO_4 | NUMBER | integer LOGO number;0 = no LOGO;n = LOGO number |
| SURFTEXT1_4 | VARCHAR2(70) | string 面喷喷印内容1 |
| SURFTEXT2_4 | VARCHAR2(70) | string 面喷喷印内容2 |
| SURFTEXT3_4 | VARCHAR2(70) | string 面喷喷印内容3 |
| SURFTEXT4_4 | VARCHAR2(70) | string 面喷喷印内容4 |
| SURFTEXT5_4 | VARCHAR2(70) | string 面喷喷印内容5 |
| SURFTEXT6_4 | VARCHAR2(70) | string 面喷喷印内容6 |
| SURFTEXT7_4 | VARCHAR2(70) | string 面喷喷印内容7 |
| SURFTEXT8_4 | VARCHAR2(70) | string 面喷喷印内容8 |
| SIDEMODE_4 | NUMBER | integer 侧喷模式Edge painting mode.0 = no Edge painting 1 = longitudinal edge downstream right 2 = longitudinal edge downstream left 3 = longitudinal edge downstream right and left |
| SIDETEXT_4 | VARCHAR2(60) | string 侧喷内容 |
| SIDEBARMODE_4 | NUMBER | integer Barcode mode 0 = do no paint a barcode; 1 = paint a barcode |
| SIDEBARCODE_4 | VARCHAR2(60) | String of ASCII characters default = string of "space" means empty line |
| SEALMODE_4 | NUMBER | integer 是否打钢印 .0 = no top punching;1 = 0° Longitudinal ;2 = 180° Longitudinal |
| SEALLOGO_4 | NUMBER | integer LOGO number.0 = no LOGO;n = LOGO number |
| SEALTEXT1_4 | VARCHAR2(30) | String of ASCII characters default = string of "space" means empty line |
| SEALTEXT2_4 | VARCHAR2(30) | String of ASCII characters default = string of "space" means empty line |
| TURNOVERFLAG5 | NUMBER | integer翻板 0：不翻板 1：翻板 |
| COLDLEVELFLAG5 | NUMBER | integer冷矫 0：不冷矫 1：冷矫 |
| USTMODE5 | NUMBER | integer探伤 1：不探伤 2：探伤 |
| USTQUALITY1_5 | VARCHAR2(8) | 一级探伤标准 |
| USTQUALITY2_5 | VARCHAR2(8) | 二级探伤标准 |
| TRIMREQ5 | NUMBER | integer是否切边 0：不剪切 1：剪切 |
| TRIMTYPE5 | NUMBER | integer剪切模式 1 = 圆盘剪 2 = 双边剪 |
| CUTMODE5 | NUMBER | integer剪切模式 1；不剪 2：剪切 |
| NROFCUTS5 | NUMBER | integer剪切数 |
| CUTNO1_5 | NUMBER | integer剪切序列号 |
| CUTNO2_5 | NUMBER |  |
| CUTNO3_5 | NUMBER |  |
| CUTNO4_5 | NUMBER |  |
| CUTNO5_5 | NUMBER |  |
| CUTNO6_5 | NUMBER |  |
| CUTNO7_5 | NUMBER |  |
| CUTNO8_5 | NUMBER |  |
| CUTNO9_5 | NUMBER |  |
| CUTNO10_5 | NUMBER |  |
| CUTNO11_5 | NUMBER |  |
| CUTNO12_5 | NUMBER |  |
| CUTNO13_5 | NUMBER |  |
| CUTNO14_5 | NUMBER |  |
| CUTNO15_5 | NUMBER |  |
| CUTNO16_5 | NUMBER |  |
| CUTNO17_5 | NUMBER |  |
| CUTNO18_5 | NUMBER |  |
| CUTNO19_5 | NUMBER |  |
| CUTNO20_5 | NUMBER |  |
| CUTTYPE1_5 | NUMBER | integer切割模式 1 = Hot Deviding cut ；2 = Production piece ；3 = Head crop ；4 = Inter crop；5 = Tail crop ；6 = Test piece cut |
| CUTTYPE2_5 | NUMBER |  |
| CUTTYPE3_5 | NUMBER |  |
| CUTTYPE4_5 | NUMBER |  |
| CUTTYPE5_5 | NUMBER |  |
| CUTTYPE6_5 | NUMBER |  |
| CUTTYPE7_5 | NUMBER |  |
| CUTTYPE8_5 | NUMBER |  |
| CUTTYPE9_5 | NUMBER |  |
| CUTTYPE10_5 | NUMBER |  |
| CUTTYPE11_5 | NUMBER |  |
| CUTTYPE12_5 | NUMBER |  |
| CUTTYPE13_5 | NUMBER |  |
| CUTTYPE14_5 | NUMBER |  |
| CUTTYPE15_5 | NUMBER |  |
| CUTTYPE16_5 | NUMBER |  |
| CUTTYPE17_5 | NUMBER |  |
| CUTTYPE18_5 | NUMBER |  |
| CUTTYPE19_5 | NUMBER |  |
| CUTTYPE20_5 | NUMBER |  |
| CUTLENAIM1_5 | NUMBER | 目标长度 |
| CUTLENAIM2_5 | NUMBER |  |
| CUTLENAIM3_5 | NUMBER |  |
| CUTLENAIM4_5 | NUMBER |  |
| CUTLENAIM5_5 | NUMBER |  |
| CUTLENAIM6_5 | NUMBER |  |
| CUTLENAIM7_5 | NUMBER |  |
| CUTLENAIM8_5 | NUMBER |  |
| CUTLENAIM9_5 | NUMBER |  |
| CUTLENAIM10_5 | NUMBER |  |
| CUTLENAIM11_5 | NUMBER |  |
| CUTLENAIM12_5 | NUMBER |  |
| CUTLENAIM13_5 | NUMBER |  |
| CUTLENAIM14_5 | NUMBER |  |
| CUTLENAIM15_5 | NUMBER |  |
| CUTLENAIM16_5 | NUMBER |  |
| CUTLENAIM17_5 | NUMBER |  |
| CUTLENAIM18_5 | NUMBER |  |
| CUTLENAIM19_5 | NUMBER |  |
| CUTLENAIM20_5 | NUMBER |  |
| PLANTDESTIN1_5 | NUMBER | integer 0 = undefined / scrap；1 = to piler 1；2 = to piler 2 |
| PLANTDESTIN2_5 | NUMBER |  |
| PLANTDESTIN3_5 | NUMBER |  |
| PLANTDESTIN4_5 | NUMBER |  |
| PLANTDESTIN5_5 | NUMBER |  |
| PLANTDESTIN6_5 | NUMBER |  |
| PLANTDESTIN7_5 | NUMBER |  |
| PLANTDESTIN8_5 | NUMBER |  |
| PLANTDESTIN9_5 | NUMBER |  |
| PLANTDESTIN10_5 | NUMBER |  |
| PLANTDESTIN11_5 | NUMBER |  |
| PLANTDESTIN12_5 | NUMBER |  |
| PLANTDESTIN13_5 | NUMBER |  |
| PLANTDESTIN14_5 | NUMBER |  |
| PLANTDESTIN15_5 | NUMBER |  |
| PLANTDESTIN16_5 | NUMBER |  |
| PLANTDESTIN17_5 | NUMBER |  |
| PLANTDESTIN18_5 | NUMBER |  |
| PLANTDESTIN19_5 | NUMBER |  |
| PLANTDESTIN20_5 | NUMBER |  |
| SURFMODE_5 | NUMBER | integer 面喷模式 0 = no top painting；1 = 0° Longitudinal；2 = 180° Longitudinal |
| SURFPAINTNUM_5 | NUMBER | integer 面喷数 |
| SURFPAINTSTARTDIS_5 | NUMBER | number 开始位置 |
| SURFPAINTINTERDIS_5 | NUMBER | number 开始到结束位置间隔 |
| SURFLOGO_5 | NUMBER | integer LOGO number;0 = no LOGO;n = LOGO number |
| SURFTEXT1_5 | VARCHAR2(70) | string 面喷喷印内容1 |
| SURFTEXT2_5 | VARCHAR2(70) | string 面喷喷印内容2 |
| SURFTEXT3_5 | VARCHAR2(70) | string 面喷喷印内容3 |
| SURFTEXT4_5 | VARCHAR2(70) | string 面喷喷印内容4 |
| SURFTEXT5_5 | VARCHAR2(70) | string 面喷喷印内容5 |
| SURFTEXT6_5 | VARCHAR2(70) | string 面喷喷印内容6 |
| SURFTEXT7_5 | VARCHAR2(70) | string 面喷喷印内容7 |
| SURFTEXT8_5 | VARCHAR2(70) | string 面喷喷印内容8 |
| SIDEMODE_5 | NUMBER | integer 侧喷模式Edge painting mode.0 = no Edge painting 1 = longitudinal edge downstream right 2 = longitudinal edge downstream left 3 = longitudinal edge downstream right and left |
| SIDETEXT_5 | VARCHAR2(60) | string 侧喷内容 |
| SIDEBARMODE_5 | NUMBER | integer Barcode mode 0 = do no paint a barcode; 1 = paint a barcode |
| SIDEBARCODE_5 | VARCHAR2(60) | String of ASCII characters default = string of "space" means empty line |
| SEALMODE_5 | NUMBER | integer 是否打钢印 .0 = no top punching;1 = 0° Longitudinal ;2 = 180° Longitudinal |
| SEALLOGO_5 | NUMBER | integer LOGO number.0 = no LOGO;n = LOGO number |
| SEALTEXT1_5 | VARCHAR2(30) | String of ASCII characters default = string of "space" means empty line |
| SEALTEXT2_5 | VARCHAR2(30) | String of ASCII characters default = string of "space" means empty line |
| TURNOVERFLAG6 | NUMBER | integer翻板 0：不翻板 1：翻板 |
| COLDLEVELFLAG6 | NUMBER | integer冷矫 0：不冷矫 1：冷矫 |
| USTMODE6 | NUMBER | integer探伤 1：不探伤 2：探伤 |
| USTQUALITY1_6 | VARCHAR2(8) | 一级探伤标准 |
| USTQUALITY2_6 | VARCHAR2(8) | 二级探伤标准 |
| TRIMREQ6 | NUMBER | integer是否切边 0：不剪切 1：剪切 |
| TRIMTYPE6 | NUMBER | integer剪切模式 1 = 圆盘剪 2 = 双边剪 |
| CUTMODE6 | NUMBER | integer剪切模式 1；不剪 2：剪切 |
| NROFCUTS6 | NUMBER | integer剪切数 |
| CUTNO1_6 | NUMBER | integer剪切序列号 |
| CUTNO2_6 | NUMBER |  |
| CUTNO3_6 | NUMBER |  |
| CUTNO4_6 | NUMBER |  |
| CUTNO5_6 | NUMBER |  |
| CUTNO6_6 | NUMBER |  |
| CUTNO7_6 | NUMBER |  |
| CUTNO8_6 | NUMBER |  |
| CUTNO9_6 | NUMBER |  |
| CUTNO10_6 | NUMBER |  |
| CUTNO11_6 | NUMBER |  |
| CUTNO12_6 | NUMBER |  |
| CUTNO13_6 | NUMBER |  |
| CUTNO14_6 | NUMBER |  |
| CUTNO15_6 | NUMBER |  |
| CUTNO16_6 | NUMBER |  |
| CUTNO17_6 | NUMBER |  |
| CUTNO18_6 | NUMBER |  |
| CUTNO19_6 | NUMBER |  |
| CUTNO20_6 | NUMBER |  |
| CUTTYPE1_6 | NUMBER | integer切割模式 1 = Hot Deviding cut ；2 = Production piece ；3 = Head crop ；4 = Inter crop；5 = Tail crop ；6 = Test piece cut |
| CUTTYPE2_6 | NUMBER |  |
| CUTTYPE3_6 | NUMBER |  |
| CUTTYPE4_6 | NUMBER |  |
| CUTTYPE5_6 | NUMBER |  |
| CUTTYPE6_6 | NUMBER |  |
| CUTTYPE7_6 | NUMBER |  |
| CUTTYPE8_6 | NUMBER |  |
| CUTTYPE9_6 | NUMBER |  |
| CUTTYPE10_6 | NUMBER |  |
| CUTTYPE11_6 | NUMBER |  |
| CUTTYPE12_6 | NUMBER |  |
| CUTTYPE13_6 | NUMBER |  |
| CUTTYPE14_6 | NUMBER |  |
| CUTTYPE15_6 | NUMBER |  |
| CUTTYPE16_6 | NUMBER |  |
| CUTTYPE17_6 | NUMBER |  |
| CUTTYPE18_6 | NUMBER |  |
| CUTTYPE19_6 | NUMBER |  |
| CUTTYPE20_6 | NUMBER |  |
| CUTLENAIM1_6 | NUMBER | 目标长度 |
| CUTLENAIM2_6 | NUMBER |  |
| CUTLENAIM3_6 | NUMBER |  |
| CUTLENAIM4_6 | NUMBER |  |
| CUTLENAIM5_6 | NUMBER |  |
| CUTLENAIM6_6 | NUMBER |  |
| CUTLENAIM7_6 | NUMBER |  |
| CUTLENAIM8_6 | NUMBER |  |
| CUTLENAIM9_6 | NUMBER |  |
| CUTLENAIM10_6 | NUMBER |  |
| CUTLENAIM11_6 | NUMBER |  |
| CUTLENAIM12_6 | NUMBER |  |
| CUTLENAIM13_6 | NUMBER |  |
| CUTLENAIM14_6 | NUMBER |  |
| CUTLENAIM15_6 | NUMBER |  |
| CUTLENAIM16_6 | NUMBER |  |
| CUTLENAIM17_6 | NUMBER |  |
| CUTLENAIM18_6 | NUMBER |  |
| CUTLENAIM19_6 | NUMBER |  |
| CUTLENAIM20_6 | NUMBER |  |
| PLANTDESTIN1_6 | NUMBER | integer 0 = undefined / scrap；1 = to piler 1；2 = to piler 2 |
| PLANTDESTIN2_6 | NUMBER |  |
| PLANTDESTIN3_6 | NUMBER |  |
| PLANTDESTIN4_6 | NUMBER |  |
| PLANTDESTIN5_6 | NUMBER |  |
| PLANTDESTIN6_6 | NUMBER |  |
| PLANTDESTIN7_6 | NUMBER |  |
| PLANTDESTIN8_6 | NUMBER |  |
| PLANTDESTIN9_6 | NUMBER |  |
| PLANTDESTIN10_6 | NUMBER |  |
| PLANTDESTIN11_6 | NUMBER |  |
| PLANTDESTIN12_6 | NUMBER |  |
| PLANTDESTIN13_6 | NUMBER |  |
| PLANTDESTIN14_6 | NUMBER |  |
| PLANTDESTIN15_6 | NUMBER |  |
| PLANTDESTIN16_6 | NUMBER |  |
| PLANTDESTIN17_6 | NUMBER |  |
| PLANTDESTIN18_6 | NUMBER |  |
| PLANTDESTIN19_6 | NUMBER |  |
| PLANTDESTIN20_6 | NUMBER |  |
| SURFMODE_6 | NUMBER | integer 面喷模式 0 = no top painting；1 = 0° Longitudinal；2 = 180° Longitudinal |
| SURFPAINTNUM_6 | NUMBER | integer 面喷数 |
| SURFPAINTSTARTDIS_6 | NUMBER | number 开始位置 |
| SURFPAINTINTERDIS_6 | NUMBER | number 开始到结束位置间隔 |
| SURFLOGO_6 | NUMBER | integer LOGO number;0 = no LOGO;n = LOGO number |
| SURFTEXT1_6 | VARCHAR2(70) | string 面喷喷印内容1 |
| SURFTEXT2_6 | VARCHAR2(70) | string 面喷喷印内容2 |
| SURFTEXT3_6 | VARCHAR2(70) | string 面喷喷印内容3 |
| SURFTEXT4_6 | VARCHAR2(70) | string 面喷喷印内容4 |
| SURFTEXT5_6 | VARCHAR2(70) | string 面喷喷印内容5 |
| SURFTEXT6_6 | VARCHAR2(70) | string 面喷喷印内容6 |
| SURFTEXT7_6 | VARCHAR2(70) | string 面喷喷印内容7 |
| SURFTEXT8_6 | VARCHAR2(70) | string 面喷喷印内容8 |
| SIDEMODE_6 | NUMBER | integer 侧喷模式Edge painting mode.0 = no Edge painting 1 = longitudinal edge downstream right 2 = longitudinal edge downstream left 3 = longitudinal edge downstream right and left |
| SIDETEXT_6 | VARCHAR2(60) | string 侧喷内容 |
| SIDEBARMODE_6 | NUMBER | integer Barcode mode 0 = do no paint a barcode; 1 = paint a barcode |
| SIDEBARCODE_6 | VARCHAR2(60) | String of ASCII characters default = string of "space" means empty line |
| SEALMODE_6 | NUMBER | integer 是否打钢印 .0 = no top punching;1 = 0° Longitudinal ;2 = 180° Longitudinal |
| SEALLOGO_6 | NUMBER | integer LOGO number.0 = no LOGO;n = LOGO number |
| SEALTEXT1_6 | VARCHAR2(30) | String of ASCII characters default = string of "space" means empty line |
| SEALTEXT2_6 | VARCHAR2(30) | String of ASCII characters default = string of "space" means empty line |

### 轧机作业实绩接口表（91 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| MSGSIZE | NUMBER |  |
| MSGID | NUMBER |  |
| SEQNO | NUMBER |  |
| FLAGS | NUMBER |  |
| YEAR | NUMBER |  |
| MONTH | NUMBER |  |
| DAY | NUMBER |  |
| HOUR | NUMBER |  |
| MINUTE | NUMBER |  |
| SECOND | NUMBER |  |
| MILLISECOND | NUMBER |  |
| PIECEIDL3 | VARCHAR2(32) | 板坯号 |
| PIECEID | VARCHAR2(16) | 母板号 |
| STEELGRADEID | VARCHAR2(12) | 钢种 |
| STEELGRADESIGN | VARCHAR2(50) | 执行标准 |
| HEATID | VARCHAR2(20) | 炉号 |
| LOTNUMBER | VARCHAR2(20) | 批号 |
| SCHEDULEID | VARCHAR2(12) | 计划号 |
| SEQNO2 | NUMBER | 批次内顺序 |
| PRODUCTTHICKENTRY | NUMBER | 轧机入口侧厚度 |
| PRODUCTTHICKEXIT | NUMBER | 轧机出口侧厚度 |
| PRODUCTWIDTH | NUMBER | 轧制宽度 |
| PRODUCTLENGTH | NUMBER | 轧制长度 |
| PRODUCTWEIGHT | NUMBER | 轧制重量 |
| PRODUCTTEMP | NUMBER | 轧制温度 |
| FURNACENO | NUMBER |  |
| FURNACEPOS | NUMBER |  |
| CHARGETEMP | NUMBER |  |
| DISCHARGETEMP | NUMBER |  |
| CHARGETIME | VARCHAR2(14) |  |
| DISCHARGETIME | VARCHAR2(14) |  |
| ROLLINGSTARTTIME | VARCHAR2(14) |  |
| ROLLINGENDTIME | VARCHAR2(14) |  |
| PLANTLEFTTIME | VARCHAR2(14) |  |
| ROLLINGTIME | NUMBER |  |
| TOTALTIME | NUMBER |  |
| ROLLMODE | NUMBER |  |
| CTRLROLLMODE | NUMBER |  |
| CTRLTEMPSTART1 | NUMBER |  |
| CTRLTEMPSTART2 | NUMBER |  |
| CTRLTEMPSTART3 | NUMBER |  |
| CTRLTEMPEND1 | NUMBER |  |
| CTRLTEMPEND2 | NUMBER |  |
| CTRLTEMPEND3 | NUMBER |  |
| PHASENROFPASSES1 | NUMBER |  |
| PHASENROFPASSES2 | NUMBER |  |
| PHASENROFPASSES3 | NUMBER |  |
| NROFPASSES | NUMBER |  |
| MILLUSAGE | NUMBER |  |
| MILLTOPWRID | VARCHAR2(12) |  |
| MILLBOTWRID | VARCHAR2(12) |  |
| MILLTOPBRID | VARCHAR2(12) |  |
| MILLBOTBRID | VARCHAR2(12) |  |
| MILLDSERID | VARCHAR2(12) |  |
| MILLOSERID | VARCHAR2(12) |  |
| COMPLETEROLLED | NUMBER |  |
| MILLUSAGE2 | NUMBER |  |
| MILLTOPWRID2 | VARCHAR2(12) |  |
| MILLBOTWRID2 | VARCHAR2(12) |  |
| MILLTOPBRID2 | VARCHAR2(12) |  |
| MILLBOTBRID2 | VARCHAR2(12) |  |
| MILLDSERID2 | VARCHAR2(12) |  |
| MILLOSERID2 | VARCHAR2(12) |  |
| COMPLETEROLLED2 | NUMBER |  |
| BATCHMODE | NUMBER |  |
| BATCHSIZE | NUMBER |  |
| BATCHPOS | NUMBER |  |
| BATCHNO | NUMBER |  |
| MEASTHICKOPER1 | NUMBER |  |
| MEASTHICKOPER2 | NUMBER |  |
| MEASTHICKOPER3 | NUMBER |  |
| MEASTHICKCENTER1 | NUMBER |  |
| MEASTHICKCENTER2 | NUMBER |  |
| MEASTHICKCENTER3 | NUMBER |  |
| MEASTHICKDRIVE1 | NUMBER |  |
| MEASTHICKDRIVE2 | NUMBER |  |
| MEASTHICKDRIVE3 | NUMBER |  |
| MEASPROFILE | NUMBER |  |
| MEASFLATNESS | NUMBER |  |
| DISPOSITIONCODE | VARCHAR2(2) |  |
| SHIFTID | VARCHAR2(1) |  |
| OPERATORID | VARCHAR2(7) |  |
| INSERTDATE | DATE |  |
| PROCESS_FLAG | NUMBER |  |
| PROCESS_CODE | VARCHAR2(180) |  |
| PROCESS_TIME | VARCHAR2(14) |  |
| FMROLLINGSTARTTIME | VARCHAR2(14) |  |
| FMROLLINGENDTIME | VARCHAR2(14) |  |
| END_FLAG | NUMBER |  |
| REVERT_YN | VARCHAR2(14) | 撤销回炉轧废与否 |
| BROADENINGWIDTHPASSS | NUMBER | 展宽道次 |

### 双边剪作业实绩接口表（29 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| MSGSIZE | NUMBER |  |
| MSGID | NUMBER |  |
| SEQNO | NUMBER |  |
| FLAGS | NUMBER |  |
| YEAR | NUMBER |  |
| MONTH | NUMBER |  |
| DAY | NUMBER |  |
| HOUR | NUMBER |  |
| MINUTE | NUMBER |  |
| SECOND | NUMBER |  |
| MILLISECOND | NUMBER |  |
| PIECEIDL3 | VARCHAR2(32) | Piece identification of PPS (Production Planning System) |
| PIECEID | VARCHAR2(16) | Piece Id format (ASCII): SYYMNNNNNDFCC S=Strand, YY=Year, M=Month (Hex), NNNNN=Number (ascending), D=Dividing(0..2), F=Forward (Hex), CC=Cutting label(00..99) |
| PRODUCTID | VARCHAR2(20) | Daughter plate ID after HDS cut |
| CUTWIDTH | NUMBER | Cut width |
| SHEARNO | NUMBER | Number of used shear 1 = Rotary side trimming shear 2 = Double side trimming shear |
| TRIMMODE | NUMBER | Actual trim shear mode 1-no trim 2=trimmed |
| PRODUCTENTRYTEMP | NUMBER | Product entry temperature |
| STARTTIME | VARCHAR2(14) | Point in time of trim shear start; Format: YYYYMMDDHHMMSS |
| FINISHTIME | VARCHAR2(14) | Point in time of trim shear Finish; Format: YYYYMMDDHHMMSS |
| SHIFTID | VARCHAR2(1) | Shift ID |
| OPERATORID | VARCHAR2(7) | Operator ID |
| CRT_USER_ID | VARCHAR2(20) | Created User ID |
| CRT_OBJ_ID | VARCHAR2(30) | Created Object ID |
| CRT_TM | TIMESTAMP(7) | Created Time |
| UPD_USER_ID | VARCHAR2(20) | Last Updated User ID |
| UPD_OBJ_ID | VARCHAR2(30) | Last Updated Object ID |
| UPD_TM | TIMESTAMP(7) | Last Updated Time |
| ARCHIVE_FL | VARCHAR2(1) | Record Archive Flag |

### 定尺剪作业实绩接口表（92 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| MSGSIZE | NUMBER |  |
| MSGID | NUMBER |  |
| SEQNO | NUMBER |  |
| FLAGS | NUMBER |  |
| YEAR | NUMBER |  |
| MONTH | NUMBER |  |
| DAY | NUMBER |  |
| HOUR | NUMBER |  |
| MINUTE | NUMBER |  |
| SECOND | NUMBER |  |
| MILLISECOND | NUMBER |  |
| PIECEIDL3 | VARCHAR2(32) | Piece identification of PPS (Production Planning System) |
| PIECEID | VARCHAR2(16) | Piece Id format (ASCII): SYYMNNNNNDFCC S=Strand, YY=Year, M=Month (Hex), NNNNN=Number (ascending), D=Dividing(0..2), F=Forward (Hex), CC=Cutting label(00..99) |
| PRODUCTID | VARCHAR2(16) | Daughter plate ID after HDS cut |
| USED_LEN_MEAS_FLAG | NUMBER | Used Measured length Flag 1=size car 2= laser speed 3=pinch roll |
| SHEARNO | NUMBER | Number of used shear 1 = DS line 1 2 = DS line 2 |
| DSMODE | NUMBER | Divide Shear Mode 1=no divide cut 2=used divide cut |
| NROFCUTS | NUMBER | Number of Cuts |
| CUTTYPE1 | NUMBER | Type of Cut made 1=head crop cut 2=divide cut 3=scrap cut 4=tail crop cut 5=sample cut |
| CUTTYPE2 | NUMBER |  |
| CUTTYPE3 | NUMBER |  |
| CUTTYPE4 | NUMBER |  |
| CUTTYPE5 | NUMBER |  |
| CUTTYPE6 | NUMBER |  |
| CUTTYPE7 | NUMBER |  |
| CUTTYPE8 | NUMBER |  |
| CUTTYPE9 | NUMBER |  |
| CUTTYPE10 | NUMBER |  |
| CUTTYPE11 | NUMBER |  |
| CUTTYPE12 | NUMBER |  |
| CUTTYPE13 | NUMBER |  |
| CUTTYPE14 | NUMBER |  |
| CUTTYPE15 | NUMBER |  |
| CUTTYPE16 | NUMBER |  |
| CUTTYPE17 | NUMBER |  |
| CUTTYPE18 | NUMBER |  |
| CUTTYPE19 | NUMBER |  |
| CUTTYPE20 | NUMBER |  |
| CUTLENGTH1 | NUMBER | X coordinate of tail left corner of defect area |
| CUTLENGTH2 | NUMBER | Y coordinate of tail left corner of defect area |
| CUTLENGTH3 | NUMBER | Defect detection location 1 = at inspection bed 2 = at grinding bed |
| CUTLENGTH4 | NUMBER | Shift ID |
| CUTLENGTH5 | NUMBER | Operator ID |
| CUTLENGTH6 | NUMBER |  |
| CUTLENGTH7 | NUMBER |  |
| CUTLENGTH8 | NUMBER |  |
| CUTLENGTH9 | NUMBER |  |
| CUTLENGTH10 | NUMBER |  |
| CUTLENGTH11 | NUMBER |  |
| CUTLENGTH12 | NUMBER |  |
| CUTLENGTH13 | NUMBER |  |
| CUTLENGTH14 | NUMBER |  |
| CUTLENGTH15 | NUMBER |  |
| CUTLENGTH16 | NUMBER |  |
| CUTLENGTH17 | NUMBER |  |
| CUTLENGTH18 | NUMBER |  |
| CUTLENGTH19 | NUMBER |  |
| CUTLENGTH20 | NUMBER |  |
| PLATEID1 | VARCHAR2(16) |  |
| PLATEID2 | VARCHAR2(16) |  |
| PLATEID3 | VARCHAR2(16) |  |
| PLATEID4 | VARCHAR2(16) |  |
| PLATEID5 | VARCHAR2(16) |  |
| PLATEID6 | VARCHAR2(16) |  |
| PLATEID7 | VARCHAR2(16) |  |
| PLATEID8 | VARCHAR2(16) |  |
| PLATEID9 | VARCHAR2(16) |  |
| PLATEID10 | VARCHAR2(16) |  |
| PLATEID11 | VARCHAR2(16) |  |
| PLATEID12 | VARCHAR2(16) |  |
| PLATEID13 | VARCHAR2(16) |  |
| PLATEID14 | VARCHAR2(16) |  |
| PLATEID15 | VARCHAR2(16) |  |
| PLATEID16 | VARCHAR2(16) |  |
| PLATEID17 | VARCHAR2(16) |  |
| PLATEID18 | VARCHAR2(16) |  |
| PLATEID19 | VARCHAR2(16) |  |
| PLATEID20 | VARCHAR2(16) |  |
| PRODUCTENTRYTEMP | NUMBER | Product entry temperature |
| REMAINLENGTH | NUMBER | Remaining length of mother piece. |
| STARTTIME | VARCHAR2(14) | Point in time of divide shear start; Format: YYYYMMDDHHMMSS |
| FINISHTIME | VARCHAR2(14) | Point in time of divide shear finish; Format: YYYYMMDDHHMMSS |
| SHIFTID | VARCHAR2(1) | Shift ID |
| OPERATORID | VARCHAR2(7) | Operator ID |
| CRT_USER_ID | VARCHAR2(20) | Created User ID |
| CRT_OBJ_ID | VARCHAR2(30) | Created Object ID |
| CRT_TM | TIMESTAMP(7) | Created Time |
| UPD_USER_ID | VARCHAR2(20) | Last Updated User ID |
| UPD_OBJ_ID | VARCHAR2(30) | Last Updated Object ID |
| UPD_TM | TIMESTAMP(7) | Last Updated Time |
| ARCHIVE_FL | VARCHAR2(1) | Record Archive Flag1 |
| PROCESS_FLAG | NUMBER |  |

### 能源消耗实绩接口表（10 字段）

| 字段 | 类型 | 注释 |
|---|---|---|
| ID | NUMBER(9) | 主键ID |
| LINE_NO | VARCHAR2(50) | 产线区分 |
| SUB_MTRL_CD | VARCHAR2(50) | 物料代码 |
| MTRL_NM | VARCHAR2(50) | 物料名称 |
| MTRL_IN_WGT | NUMBER(9) | 能耗量 |
| MTRL_IN_UNIT | VARCHAR2(50) | 能耗单位 |
| MTRL_IN_DTM | DATE | 能耗时间 |
| FLAG | NUMBER(1) | 使用标记, 0-未处理，1-已处理 |
| FLAG_DATE | DATE | 使用时间 |
| CREATE_TIME | DATE | 创建时间 |


### 计量系统 API 参数（非 DB 表，webservice 报文）[设计文档]

- **提货单**（MES→计量）：matchid=物流号、carno=车号、planid=发货单号、targetcode/name=
  客户编码/名称、motorcadename=运输单位、sourceplace=供货地点、status=状态标志
  (1-新增修改/0-作废)；明细 details：materialcode/name=物料编码/名称、specno=规格、
  steelno=牌号、count=件数、lineno=发货单行号、ordLine=订单行号、memo=备注。
- **皮重计量**（计量→MES）：matchid、tare=皮重、taretime=皮重时间、tareweigh=皮重衡器、status。
- **成品销售计量**（计量→MES）：matchid、gross/grosstime=毛重/时间、tare/taretime、
  suttle/suttletime=净重/时间、data=List<oncesuttle>（lotno=件次号、suttle=单件净重、
  amount=金额2位小数）、status。
- **成品出库装车**（MES→计量）：matchid、planid、targetcode/name、carno、
  sourceplacecode/name=发货库房编码/名称(ERP)、sourcetime=发货时间、allweigh=总重量、
  allcount=总件数、status(1-新增/2-修改/0-作废)、details（lotno、materialcode/name、
  specno、steelno、count、weight=理重、lineno）。

### 5.x 设计文档中即无注释的字段（任务 1 待补注目标，共 742 个）

- **板材取样指示接口表**：UPD_USER_ID、UPD_TM、NM_NUM、AV_NUM、GS_NUM、DE_NUM、WE_NUM
- **板材物性检验结果接口表**：DQ_FLAG
- **炉次连铸实绩接口表**：TIME_LADLE_OPEN、STEEL_WEIGHT_LADLE_CLOSE、TIME_LADLE_CLOSE、REMAIN_MINUTES、TIME_CUT_END、TIME_CREATE、S2_SPEED_AVG、SLAB_YIELD
- **铸坯切割实绩接口表**：CUT_CONTROL、TIME_CREATE
- **轧线PDI接口表**：SLABWIDTHHEAD、SLABWIDTHTAIL、SLABWIDTHCHGSTART、SLABWIDTHCHGSTOP、INGOTWIDTHHEAD、INGOTTHICKHEAD、INGOTWIDTHTAIL、INGOTTHICKTAIL、INGOTLENGTH、INGOTWEIGHT、MATCOMPC、MATCOMPMN、MATCOMPP、MATCOMPS、MATCOMPSI、MATCOMPCU、MATCOMPV、MATCOMPNB、MATCOMPCR、MATCOMPNI、MATCOMPMO、MATCOMPSN、MATCOMPN、MATCOMPB、MATCOMPALTOT、MATCOMPTI、MATCOMPCA、MATCOMPPB、MATCOMPALSOL、MATCOMPSB、MATCOMPZN、MATCOMPAS、MATCOMPCO、MATCOMPMG、MATCOMPZR、MATCOMPW、MATCOMPTA、MATSPARE1、MATSPARE2、MATSPARE3、MATSPARE4、MATSPARE5、MATSPARE6、MATSPARE7、MATSPARE8、MATSPARE9、MATSPARE10、PRODUCTFLATNESSMIN、PRODUCTFLATNESSMAX、PRODUCTPROFILEMIN、PRODUCTPROFILEMAX、CUTNO6、CUTNO7、CUTNO8、CUTNO9、CUTNO10、CUTNO11、CUTNO12、CUTNO13、CUTNO14、CUTNO15、CUTNO16、CUTNO17、CUTNO18、CUTNO19、CUTNO20、CUTTYPE3、CUTTYPE4、CUTTYPE5、CUTTYPE6、CUTTYPE7、CUTTYPE8、CUTTYPE9、CUTTYPE10、CUTTYPE11、CUTTYPE12、CUTTYPE13、CUTTYPE14、CUTTYPE15、CUTTYPE16、CUTTYPE17、CUTTYPE18、CUTTYPE19、CUTTYPE20、CUTLENAIM2、CUTLENAIM3、CUTLENAIM4、CUTLENAIM5、CUTLENAIM6、CUTLENAIM7、CUTLENAIM8、CUTLENAIM9、CUTLENAIM10、CUTLENAIM11、CUTLENAIM12、CUTLENAIM13、CUTLENAIM14、CUTLENAIM15、CUTLENAIM16、CUTLENAIM17、CUTLENAIM18、CUTLENAIM19、CUTLENAIM20、PLANTDESTIN3、PLANTDESTIN4、PLANTDESTIN5、PLANTDESTIN6、PLANTDESTIN7、PLANTDESTIN8、PLANTDESTIN9、PLANTDESTIN10、PLANTDESTIN11、PLANTDESTIN12、PLANTDESTIN13、PLANTDESTIN14、PLANTDESTIN15、PLANTDESTIN16、PLANTDESTIN17、PLANTDESTIN18、PLANTDESTIN19、PLANTDESTIN20
- **剪切PDI接口表**：CUTNO2、CUTNO3、CUTNO4、CUTNO5、CUTNO6、CUTNO7、CUTNO8、CUTNO9、CUTNO10、CUTNO11、CUTNO12、CUTNO13、CUTNO14、CUTNO15、CUTNO16、CUTNO17、CUTNO18、CUTNO19、CUTNO20、CUTTYPE2、CUTTYPE3、CUTTYPE4、CUTTYPE5、CUTTYPE6、CUTTYPE7、CUTTYPE8、CUTTYPE9、CUTTYPE10、CUTTYPE11、CUTTYPE12、CUTTYPE13、CUTTYPE14、CUTTYPE15、CUTTYPE16、CUTTYPE17、CUTTYPE18、CUTTYPE19、CUTTYPE20、CUTLENAIM2、CUTLENAIM3、CUTLENAIM4、CUTLENAIM5、CUTLENAIM6、CUTLENAIM7、CUTLENAIM8、CUTLENAIM9、CUTLENAIM10、CUTLENAIM11、CUTLENAIM12、CUTLENAIM13、CUTLENAIM14、CUTLENAIM15、CUTLENAIM16、CUTLENAIM17、CUTLENAIM18、CUTLENAIM19、CUTLENAIM20、PLANTDESTIN3、PLANTDESTIN4、PLANTDESTIN5、PLANTDESTIN6、PLANTDESTIN7、PLANTDESTIN8、PLANTDESTIN9、PLANTDESTIN10、PLANTDESTIN11、PLANTDESTIN12、PLANTDESTIN13、PLANTDESTIN14、PLANTDESTIN15、PLANTDESTIN16、PLANTDESTIN17、PLANTDESTIN18、PLANTDESTIN19、PLANTDESTIN20、CUTNO2_2、CUTNO3_2、CUTNO4_2、CUTNO5_2、CUTNO6_2、CUTNO7_2、CUTNO8_2、CUTNO9_2、CUTNO10_2、CUTNO11_2、CUTNO12_2、CUTNO13_2、CUTNO14_2、CUTNO15_2、CUTNO16_2、CUTNO17_2、CUTNO18_2、CUTNO19_2、CUTNO20_2、CUTTYPE2_2、CUTTYPE3_2、CUTTYPE4_2、CUTTYPE5_2、CUTTYPE6_2、CUTTYPE7_2、CUTTYPE8_2、CUTTYPE9_2、CUTTYPE10_2、CUTTYPE11_2、CUTTYPE12_2、CUTTYPE13_2、CUTTYPE14_2、CUTTYPE15_2、CUTTYPE16_2、CUTTYPE17_2、CUTTYPE18_2、CUTTYPE19_2、CUTTYPE20_2、CUTLENAIM2_2、CUTLENAIM3_2、CUTLENAIM4_2、CUTLENAIM5_2、CUTLENAIM6_2、CUTLENAIM7_2、CUTLENAIM8_2、CUTLENAIM9_2、CUTLENAIM10_2、CUTLENAIM11_2、CUTLENAIM12_2、CUTLENAIM13_2、CUTLENAIM14_2、CUTLENAIM15_2、CUTLENAIM16_2、CUTLENAIM17_2、CUTLENAIM18_2、CUTLENAIM19_2、CUTLENAIM20_2、PLANTDESTIN2_2、PLANTDESTIN3_2、PLANTDESTIN4_2、PLANTDESTIN5_2、PLANTDESTIN6_2、PLANTDESTIN7_2、PLANTDESTIN8_2、PLANTDESTIN9_2、PLANTDESTIN10_2、PLANTDESTIN11_2、PLANTDESTIN12_2、PLANTDESTIN13_2、PLANTDESTIN14_2、PLANTDESTIN15_2、PLANTDESTIN16_2、PLANTDESTIN17_2、PLANTDESTIN18_2、PLANTDESTIN19_2、PLANTDESTIN20_2、CUTNO2_3、CUTNO3_3、CUTNO4_3、CUTNO5_3、CUTNO6_3、CUTNO7_3、CUTNO8_3、CUTNO9_3、CUTNO10_3、CUTNO11_3、CUTNO12_3、CUTNO13_3、CUTNO14_3、CUTNO15_3、CUTNO16_3、CUTNO17_3、CUTNO18_3、CUTNO19_3、CUTNO20_3、CUTTYPE3_3、CUTTYPE4_3、CUTTYPE5_3、CUTTYPE6_3、CUTTYPE7_3、CUTTYPE8_3、CUTTYPE9_3、CUTTYPE10_3、CUTTYPE11_3、CUTTYPE12_3、CUTTYPE13_3、CUTTYPE14_3、CUTTYPE15_3、CUTTYPE16_3、CUTTYPE17_3、CUTTYPE18_3、CUTTYPE19_3、CUTTYPE20_3、CUTLENAIM5_3、CUTLENAIM6_3、CUTLENAIM7_3、CUTLENAIM8_3、CUTLENAIM9_3、CUTLENAIM10_3、CUTLENAIM11_3、CUTLENAIM12_3、CUTLENAIM13_3、CUTLENAIM14_3、CUTLENAIM15_3、CUTLENAIM16_3、CUTLENAIM17_3、CUTLENAIM18_3、CUTLENAIM19_3、CUTLENAIM20_3、PLANTDESTIN2_3、PLANTDESTIN3_3、PLANTDESTIN4_3、PLANTDESTIN5_3、PLANTDESTIN6_3、PLANTDESTIN7_3、PLANTDESTIN8_3、PLANTDESTIN9_3、PLANTDESTIN10_3、PLANTDESTIN11_3、PLANTDESTIN12_3、PLANTDESTIN13_3、PLANTDESTIN14_3、PLANTDESTIN15_3、PLANTDESTIN16_3、PLANTDESTIN17_3、PLANTDESTIN18_3、PLANTDESTIN19_3、PLANTDESTIN20_3、CUTNO2_4、CUTNO3_4、CUTNO4_4、CUTNO5_4、CUTNO6_4、CUTNO7_4、CUTNO8_4、CUTNO9_4、CUTNO10_4、CUTNO11_4、CUTNO12_4、CUTNO13_4、CUTNO14_4、CUTNO15_4、CUTNO16_4、CUTNO17_4、CUTNO18_4、CUTNO19_4、CUTNO20_4、CUTTYPE2_4、CUTTYPE3_4、CUTTYPE4_4、CUTTYPE5_4、CUTTYPE6_4、CUTTYPE7_4、CUTTYPE8_4、CUTTYPE9_4、CUTTYPE10_4、CUTTYPE11_4、CUTTYPE12_4、CUTTYPE13_4、CUTTYPE14_4、CUTTYPE15_4、CUTTYPE16_4、CUTTYPE17_4、CUTTYPE18_4、CUTTYPE19_4、CUTTYPE20_4、CUTLENAIM2_4、CUTLENAIM3_4、CUTLENAIM4_4、CUTLENAIM5_4、CUTLENAIM6_4、CUTLENAIM7_4、CUTLENAIM8_4、CUTLENAIM9_4、CUTLENAIM10_4、CUTLENAIM11_4、CUTLENAIM12_4、CUTLENAIM13_4、CUTLENAIM14_4、CUTLENAIM15_4、CUTLENAIM16_4、CUTLENAIM17_4、CUTLENAIM18_4、CUTLENAIM19_4、CUTLENAIM20_4、PLANTDESTIN2_4、PLANTDESTIN3_4、PLANTDESTIN4_4、PLANTDESTIN5_4、PLANTDESTIN6_4、PLANTDESTIN7_4、PLANTDESTIN8_4、PLANTDESTIN9_4、PLANTDESTIN10_4、PLANTDESTIN11_4、PLANTDESTIN12_4、PLANTDESTIN13_4、PLANTDESTIN14_4、PLANTDESTIN15_4、PLANTDESTIN16_4、PLANTDESTIN17_4、PLANTDESTIN18_4、PLANTDESTIN19_4、PLANTDESTIN20_4、CUTNO2_5、CUTNO3_5、CUTNO4_5、CUTNO5_5、CUTNO6_5、CUTNO7_5、CUTNO8_5、CUTNO9_5、CUTNO10_5、CUTNO11_5、CUTNO12_5、CUTNO13_5、CUTNO14_5、CUTNO15_5、CUTNO16_5、CUTNO17_5、CUTNO18_5、CUTNO19_5、CUTNO20_5、CUTTYPE2_5、CUTTYPE3_5、CUTTYPE4_5、CUTTYPE5_5、CUTTYPE6_5、CUTTYPE7_5、CUTTYPE8_5、CUTTYPE9_5、CUTTYPE10_5、CUTTYPE11_5、CUTTYPE12_5、CUTTYPE13_5、CUTTYPE14_5、CUTTYPE15_5、CUTTYPE16_5、CUTTYPE17_5、CUTTYPE18_5、CUTTYPE19_5、CUTTYPE20_5、CUTLENAIM2_5、CUTLENAIM3_5、CUTLENAIM4_5、CUTLENAIM5_5、CUTLENAIM6_5、CUTLENAIM7_5、CUTLENAIM8_5、CUTLENAIM9_5、CUTLENAIM10_5、CUTLENAIM11_5、CUTLENAIM12_5、CUTLENAIM13_5、CUTLENAIM14_5、CUTLENAIM15_5、CUTLENAIM16_5、CUTLENAIM17_5、CUTLENAIM18_5、CUTLENAIM19_5、CUTLENAIM20_5、PLANTDESTIN2_5、PLANTDESTIN3_5、PLANTDESTIN4_5、PLANTDESTIN5_5、PLANTDESTIN6_5、PLANTDESTIN7_5、PLANTDESTIN8_5、PLANTDESTIN9_5、PLANTDESTIN10_5、PLANTDESTIN11_5、PLANTDESTIN12_5、PLANTDESTIN13_5、PLANTDESTIN14_5、PLANTDESTIN15_5、PLANTDESTIN16_5、PLANTDESTIN17_5、PLANTDESTIN18_5、PLANTDESTIN19_5、PLANTDESTIN20_5、CUTNO2_6、CUTNO3_6、CUTNO4_6、CUTNO5_6、CUTNO6_6、CUTNO7_6、CUTNO8_6、CUTNO9_6、CUTNO10_6、CUTNO11_6、CUTNO12_6、CUTNO13_6、CUTNO14_6、CUTNO15_6、CUTNO16_6、CUTNO17_6、CUTNO18_6、CUTNO19_6、CUTNO20_6、CUTTYPE2_6、CUTTYPE3_6、CUTTYPE4_6、CUTTYPE5_6、CUTTYPE6_6、CUTTYPE7_6、CUTTYPE8_6、CUTTYPE9_6、CUTTYPE10_6、CUTTYPE11_6、CUTTYPE12_6、CUTTYPE13_6、CUTTYPE14_6、CUTTYPE15_6、CUTTYPE16_6、CUTTYPE17_6、CUTTYPE18_6、CUTTYPE19_6、CUTTYPE20_6、CUTLENAIM2_6、CUTLENAIM3_6、CUTLENAIM4_6、CUTLENAIM5_6、CUTLENAIM6_6、CUTLENAIM7_6、CUTLENAIM8_6、CUTLENAIM9_6、CUTLENAIM10_6、CUTLENAIM11_6、CUTLENAIM12_6、CUTLENAIM13_6、CUTLENAIM14_6、CUTLENAIM15_6、CUTLENAIM16_6、CUTLENAIM17_6、CUTLENAIM18_6、CUTLENAIM19_6、CUTLENAIM20_6、PLANTDESTIN2_6、PLANTDESTIN3_6、PLANTDESTIN4_6、PLANTDESTIN5_6、PLANTDESTIN6_6、PLANTDESTIN7_6、PLANTDESTIN8_6、PLANTDESTIN9_6、PLANTDESTIN10_6、PLANTDESTIN11_6、PLANTDESTIN12_6、PLANTDESTIN13_6、PLANTDESTIN14_6、PLANTDESTIN15_6、PLANTDESTIN16_6、PLANTDESTIN17_6、PLANTDESTIN18_6、PLANTDESTIN19_6、PLANTDESTIN20_6
- **轧机作业实绩接口表**：MSGSIZE、MSGID、SEQNO、FLAGS、YEAR、MONTH、DAY、HOUR、MINUTE、SECOND、MILLISECOND、FURNACENO、FURNACEPOS、CHARGETEMP、DISCHARGETEMP、CHARGETIME、DISCHARGETIME、ROLLINGSTARTTIME、ROLLINGENDTIME、PLANTLEFTTIME、ROLLINGTIME、TOTALTIME、ROLLMODE、CTRLROLLMODE、CTRLTEMPSTART1、CTRLTEMPSTART2、CTRLTEMPSTART3、CTRLTEMPEND1、CTRLTEMPEND2、CTRLTEMPEND3、PHASENROFPASSES1、PHASENROFPASSES2、PHASENROFPASSES3、NROFPASSES、MILLUSAGE、MILLTOPWRID、MILLBOTWRID、MILLTOPBRID、MILLBOTBRID、MILLDSERID、MILLOSERID、COMPLETEROLLED、MILLUSAGE2、MILLTOPWRID2、MILLBOTWRID2、MILLTOPBRID2、MILLBOTBRID2、MILLDSERID2、MILLOSERID2、COMPLETEROLLED2、BATCHMODE、BATCHSIZE、BATCHPOS、BATCHNO、MEASTHICKOPER1、MEASTHICKOPER2、MEASTHICKOPER3、MEASTHICKCENTER1、MEASTHICKCENTER2、MEASTHICKCENTER3、MEASTHICKDRIVE1、MEASTHICKDRIVE2、MEASTHICKDRIVE3、MEASPROFILE、MEASFLATNESS、DISPOSITIONCODE、SHIFTID、OPERATORID、INSERTDATE、PROCESS_FLAG、PROCESS_CODE、PROCESS_TIME、FMROLLINGSTARTTIME、FMROLLINGENDTIME、END_FLAG
- **双边剪作业实绩接口表**：MSGSIZE、MSGID、SEQNO、FLAGS、YEAR、MONTH、DAY、HOUR、MINUTE、SECOND、MILLISECOND
- **定尺剪作业实绩接口表**：MSGSIZE、MSGID、SEQNO、FLAGS、YEAR、MONTH、DAY、HOUR、MINUTE、SECOND、MILLISECOND、CUTTYPE2、CUTTYPE3、CUTTYPE4、CUTTYPE5、CUTTYPE6、CUTTYPE7、CUTTYPE8、CUTTYPE9、CUTTYPE10、CUTTYPE11、CUTTYPE12、CUTTYPE13、CUTTYPE14、CUTTYPE15、CUTTYPE16、CUTTYPE17、CUTTYPE18、CUTTYPE19、CUTTYPE20、CUTLENGTH6、CUTLENGTH7、CUTLENGTH8、CUTLENGTH9、CUTLENGTH10、CUTLENGTH11、CUTLENGTH12、CUTLENGTH13、CUTLENGTH14、CUTLENGTH15、CUTLENGTH16、CUTLENGTH17、CUTLENGTH18、CUTLENGTH19、CUTLENGTH20、PLATEID1、PLATEID2、PLATEID3、PLATEID4、PLATEID5、PLATEID6、PLATEID7、PLATEID8、PLATEID9、PLATEID10、PLATEID11、PLATEID12、PLATEID13、PLATEID14、PLATEID15、PLATEID16、PLATEID17、PLATEID18、PLATEID19、PLATEID20、PROCESS_FLAG

> 处理方式：待 PL/SQL 源码导出后按字段名用法推断补注，或与 SCO_DATA_DIC 的 ITEM_CD 匹配取 ITEM_NM。


---

## 6. 数据库快照回填（2026-07-04 已完成第一轮）

快照已导出（`snapshot/` = MESAPUSER，`snapshot/sco/` = SCOAPUSER，见 `snapshot/README.md`）。
**重要更正**：本文档 §2 所述 SCO_* 表实际属于独立 schema **SCOAPUSER**（74 表），
不在 MESAPUSER 中；§2 的字段含义已由 `snapshot/sco/02_columns_comments.csv` 的
真实注释证实（原厂英文注释，如 CRT_USER_ID = Created User ID）。

### 6.1 全量字段字典（机器合并产出）

**`docs/data_dictionary_full.csv`**（81,360 字段）= 02 快照注释 ⊕ SCO_DATA_DIC 语义回填：

| 来源（SOURCE 列） | MESAPUSER | SCOAPUSER |
|---|---|---|
| DB注释(中文) | 30,142 | 9 |
| DB注释(非中文/英文) | 17,750 | 632 |
| SCO_DATA_DIC 回填（原注释为空，按字段名匹配 ITEM_NM） | 12,161 | 268 |
| 仍为空 | 20,217 | 181 |

- SCO_DATA_DIC 可用条目 19,441（全量 22,687，剔除 ITEM_NM=ITEM_CD 的自指条目）；
  内容中英混合，部分 CD_DESC 含韩文（POSCO 血统）。
- 剩余 2 万空注释字段的补注途径：PL/SQL 用法推断（任务 2 顺带）+ 界面映射表回填，
  标注 `[推断]`。
- 字典内容数据已本地化：`snapshot/sco/data_sco_data_dic.csv`、`data_sco_code_master.csv`
  （1,335 主代码）、`data_sco_code_detail.csv`（13,620 代码值，§4 的完整版）、
  `data_sco_multilang_master.csv`（93,781 条，含 CAP_* 界面标签键——任务 6 的 @@/@_
  缺失键可在此核对）。

### 6.2 乱码字段（任务 5 已分型）

7,347 条候选分型完毕（详见 `docs/garbled_fix_proposal.md` 与 `docs/garbled_classified.csv`）：
**可字符集还原 = 0**（丢失发生在写入时，字节即 3f），A 类全问号 2,978 条中 2,416 条
可按 SCO_DATA_DIC 语义重建，建议 SQL 在 `docs/garbled_fix_suggested.sql`（未执行）。
误报 567 条（UTF-8 连续字节命中检测正则）勿改。

### 6.3 仍待办

1. §5 接口表的真实 DB 表名按字段组合匹配（对 MESAPUSER 02 快照做列集合比对）。
2. 业务域表字段级中文化：结合 `snapshot/03_src/` PL/SQL 用法逐域推进（任务 2 联动）。
3. 本文档 §2/§3 的 [推断] 条目与 02 快照真实注释逐项核对升级为 [DB注释]。

> 与 `docs/ui_field_mapping.md` 的关系：映射表是「界面标签→JS字段→表.字段」的过程证据，
> 本文档是以表.字段为主键的最终字典；两文档同步维护。
