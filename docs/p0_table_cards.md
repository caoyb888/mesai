# P0 核心表卡片（Sprint 3 · S3-0 素材）

> 关联需求单：REQ-MES-AI-20260706-001 ｜ 生成脚本：`scripts/kb-ingest/build_table_cards.py`
> 结构源：`db_introspect` 盘点 JSON ｜ 语义源：字典 CSV（`data_dictionary_full.csv`）｜ 热度源：依赖图 `tables.csv`
> 纯本地拼装，**未调用外部 AI**。每张卡片 = 一个「表字段理解」训练/RAG 单元。

## 使用须知（务必先读）

1. **Owner/Schema**：本库为 Oracle，所有 P0 表属 `MESAPUSER`。SQL 中若以 `MESAPUSER` 用户连接则**直接写表名**；跨 schema 访问才加 `MESAPUSER.` 前缀。**切勿把 owner 当作表名的一部分**。
2. **列语义来源于字典 CSV**：克隆库列注释全空，语义（中文/英文）由生产库导出的字典反哺；
   `来源` 列标注该语义出处（DB注释(中文)/DB注释(非中文)/SCO_DATA_DIC/空）。`空` = 该列暂无语义，属缺口。
3. **画像**中「被读/被写过程数」来自 PL/SQL 静态依赖图，反映该表在业务中的热度与读写角色。

## 覆盖统计

- 卡片数（P0 表）：**95**
- 字段总数：**13072**　有语义：**11430（87%）**　语义缺口：**1642**
- ⚠️ 未在盘点中找到结构（可能为视图/已删）：5 张 → SCO_CODE_DETAIL, VW_SIM_ITEM_MAST, BIND, VW_CODE_MASTER, SCOAPUSER.SCO_CODE_DETAIL

---

### SMS_SLAB

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=187｜被读 149 过程 / 被写 19 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：147569　**主键**：SLAB_NO　**语义覆盖**：238/264

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | SLAB_NO | VARCHAR2(20) | N | ✓ | Slab No | DB注释(非中文) |
| 9 | MOM_SLAB_NO | VARCHAR2(20) | Y |  | Mother Slab No | DB注释(非中文) |
| 10 | PLAN_SLAB_NO | VARCHAR2(20) | Y |  | Plan Slab No | DB注释(非中文) |
| 11 | SLAB_STS | VARCHAR2(8) | Y |  | Slab Status | DB注释(非中文) |
| 12 | MTRL_SHP_TY | VARCHAR2(1) | Y |  | Matrial Shape Type | DB注释(非中文) |
| 13 | HEAT_NO | VARCHAR2(20) | Y |  | Heat No | DB注释(非中文) |
| 14 | SLAB_CUT_DTM | VARCHAR2(14) | Y |  | Slab Cutting Date | DB注释(非中文) |
| 15 | SLAB_PROD_DTM | VARCHAR2(14) | Y |  | Slab Production Date | DB注释(非中文) |
| 16 | PLAN_SLAB_THK | NUMBER | Y |  | Plan Slab Thickness | DB注释(非中文) |
| 17 | PLAN_SLAB_WTH | NUMBER | Y |  | Plan Slab Width | DB注释(非中文) |
| 18 | PLAN_SLAB_LTH | NUMBER | Y |  | Plan Slab Length | DB注释(非中文) |
| 19 | PLAN_SLAB_WGT | NUMBER | Y |  | Plan Slab Weight | DB注释(非中文) |
| 20 | PLAN_SLAB_STA_WTH | NUMBER | Y |  | Plan Slab Start Width | DB注释(非中文) |
| 21 | PLAN_SLAB_END_WTH | NUMBER | Y |  | Plan Slab End Width | DB注释(非中文) |
| 22 | SLAB_THK | NUMBER | Y |  | Slab Thickness | DB注释(非中文) |
| 23 | SLAB_WTH | NUMBER | Y |  | Slab Width | DB注释(非中文) |
| 24 | SLAB_LTH | NUMBER | Y |  | Slab Length | DB注释(非中文) |
| 25 | SLAB_WGT | NUMBER | Y |  | 重量Slab Weight | DB注释(中文) |
| 26 | SLAB_STA_WTH | NUMBER | Y |  | Slab Start Width | DB注释(非中文) |
| 27 | SLAB_END_WTH | NUMBER | Y |  | Slab End Width | DB注释(非中文) |
| 28 | INCMP_STEEL_GRD | VARCHAR2(20) | Y |  | 钢种Steel Grade | DB注释(中文) |
| 29 | DIVERT_STEEL_GRD1 | VARCHAR2(20) | Y |  | Diverted Steel grade 1 | DB注释(非中文) |
| 30 | DIVERT_STEEL_GRD2 | VARCHAR2(20) | Y |  | Diverted Steel grade 2 | DB注释(非中文) |
| 31 | DIVERT_STEEL_GRD3 | VARCHAR2(20) | Y |  | Diverted Steel grade 3 | DB注释(非中文) |
| 32 | DIVERT_STEEL_GRD4 | VARCHAR2(20) | Y |  | Diverted Steel grade 4 | DB注释(非中文) |
| 33 | DIVERT_STEEL_GRD5 | VARCHAR2(20) | Y |  | Diverted Steel grade 5 | DB注释(非中文) |
| 34 | DIVERT_STEEL_GRD6 | VARCHAR2(20) | Y |  | Diverted Steel grade 6 | DB注释(非中文) |
| 35 | DIVERT_STEEL_GRD7 | VARCHAR2(20) | Y |  | Diverted Steel grade 7 | DB注释(非中文) |
| 36 | DIVERT_STEEL_GRD8 | VARCHAR2(20) | Y |  | Diverted Steel grade 8 | DB注释(非中文) |
| 37 | DIVERT_STEEL_GRD9 | VARCHAR2(20) | Y |  | Diverted Steel grade 9 | DB注释(非中文) |
| 38 | DIVERT_STEEL_GRD10 | VARCHAR2(20) | Y |  | Diverted Steel grade 10 | DB注释(非中文) |
| 39 | ORD_FL | VARCHAR2(1) | Y |  | Order Flag | DB注释(非中文) |
| 40 | ORD_FL_CHANGE_DTM | VARCHAR2(14) | Y |  | Order Flag Change Date | DB注释(非中文) |
| 41 | ORD_FL_CHANGE_REASON_CD | VARCHAR2(3) | Y |  | Order Flag Change Reason Code | DB注释(非中文) |
| 42 | ORD_NO | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 43 | ORD_LN | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 44 | SPEC_CD | VARCHAR2(50) | Y |  | 规格Specification Code | DB注释(中文) |
| 45 | ORD_USAGE | VARCHAR2(4) | Y |  | Usage Code | DB注释(非中文) |
| 46 | SMPING_TY | VARCHAR2(1) | Y |  | Sampling Y/N | DB注释(非中文) |
| 47 | PLAN_SCARF_YN | VARCHAR2(1) | Y |  | Scarfing Y/N | DB注释(非中文) |
| 48 | SCARF_DTM | VARCHAR2(14) | Y |  | Scarfing Date | DB注释(非中文) |
| 49 | SLAB_END_REASON_CD | VARCHAR2(2) | Y |  | Slab End Reason Code | DB注释(非中文) |
| 50 | YD_MTRL_TY | VARCHAR2(2) | Y |  | Yard Material Type | DB注释(非中文) |
| 51 | LOC_CD | VARCHAR2(9) | Y |  | 垛位Slab Location | DB注释(中文) |
| 52 | SLAB_INSP_RSLT | VARCHAR2(1) | Y |  | 板坯检查结果 | DB注释(中文) |
| 53 | SLAB_INSP_RSN | VARCHAR2(10) | Y |  | 板坯检查结果原因 | DB注释(中文) |
| 54 | SLAB_INSP_DTM | VARCHAR2(14) | Y |  | 表检结果记录人 | DB注释(中文) |
| 55 | APPRD_GRD | NUMBER | Y |  | Mechanical Grade | DB注释(非中文) |
| 56 | RTN_TY | VARCHAR2(1) | Y |  | Return Type(C: claim, N: Nota) | DB注释(非中文) |
| 57 | RTN_DTM | VARCHAR2(14) | Y |  | Return Date Time | DB注释(非中文) |
| 58 | RTN_REASON_CD | VARCHAR2(2) | Y |  | Return Reason Code | DB注释(非中文) |
| 59 | CUT_DTM | VARCHAR2(14) | Y |  | Cutting(Scrap) date | DB注释(非中文) |
| 60 | PROD_DT | VARCHAR2(8) | Y |  | Production date | DB注释(非中文) |
| 61 | PLAN_CUT_YN | VARCHAR2(1) | Y |  | Plan Cut  Y/N | DB注释(非中文) |
| 62 | SLAB_END_DTM | VARCHAR2(14) | Y |  | Slab end date | DB注释(非中文) |
| 63 | SCARF_INST_SEQ | NUMBER | Y |  | Scarfing instruction seq | DB注释(非中文) |
| 64 | FCUT_INST_SEQ | NUMBER | Y |  | Cutting(Scrap) instruction seq | DB注释(非中文) |
| 65 | COOLING_METHOD | VARCHAR2(1) | Y |  | Cooling Method Type(Air, Water) | DB注释(非中文) |
| 66 | COOLING_COMP_YN | VARCHAR2(1) | Y |  | Cooling Complete Y/N | DB注释(非中文) |
| 67 | MIXED_SLAB_TY | VARCHAR2(1) | Y |  | Mixed Slab Type | DB注释(非中文) |
| 68 | MARK_YN | VARCHAR2(1) | Y |  | Marked Y/N | DB注释(非中文) |
| 69 | MARK_DTM | VARCHAR2(14) | Y |  | Marked Datetime | DB注释(非中文) |
| 70 | PROG_CD | VARCHAR2(4) | Y |  | 材料状态Progress Code | DB注释(中文) |
| 71 | SMP_NO | VARCHAR2(11) | Y |  | Sampling Code | DB注释(非中文) |
| 72 | PROD_CD | VARCHAR2(3) | Y |  | Production Code | DB注释(非中文) |
| 73 | HR_PROD_THK_AIM | NUMBER | Y |  | HR Production Thick Aim | DB注释(非中文) |
| 74 | HR_PROD_WTH_AIM | NUMBER | Y |  | HR Production Width Aim | DB注释(非中文) |
| 75 | CONF_PASS_PLANT_CD | VARCHAR2(30) | Y |  | Confirm Pass Plant Code | DB注释(非中文) |
| 76 | HR_PLAN_OP_CD | VARCHAR2(60) | Y |  | HR Plan Operation Code | DB注释(非中文) |
| 77 | ORD_DLV_DT | VARCHAR2(8) | Y |  | Order Delivery | DB注释(非中文) |
| 78 | SLAB_DIR_DEST_FL | VARCHAR2(2) | Y |  | Slab Direction Destination Flag | DB注释(非中文) |
| 79 | URGENT_TY | VARCHAR2(1) | Y |  | Urgent Type | DB注释(非中文) |
| 80 | ORD_TY | VARCHAR2(2) | Y |  | Order Type | DB注释(非中文) |
| 81 | HRL_MFC_STD_NO | VARCHAR2(11) | Y |  | HR manufacturing Standard No | DB注释(非中文) |
| 82 | TAPER_FL | VARCHAR2(1) | Y |  | Tapered Flag | DB注释(非中文) |
| 83 | SPL_REASON_CD | VARCHAR2(2) | Y |  | Surplus Production Direction Code | DB注释(非中文) |
| 84 | SPECIFIC_GRAVITY | NUMBER | Y |  | Specific Gravity | DB注释(非中文) |
| 85 | ORD_NO1 | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 86 | ORD_LN1 | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 87 | SLAB_DGN_WGT1 | NUMBER | Y |  | Slab Design Weight | DB注释(非中文) |
| 88 | ORD_NO2 | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 89 | ORD_LN2 | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 90 | SLAB_DGN_WGT2 | NUMBER | Y |  | Slab Design Weight | DB注释(非中文) |
| 91 | ORD_NO3 | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 92 | ORD_LN3 | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 93 | SLAB_DGN_WGT3 | NUMBER | Y |  | Slab Design Weight | DB注释(非中文) |
| 94 | PROC_CD | VARCHAR2(3) | Y |  | Process Code | DB注释(非中文) |
| 95 | SLAB_PLAN_DEST | NUMBER | Y |  | Slab Planned destination | DB注释(非中文) |
| 96 | HCR_FL | VARCHAR2(1) | Y |  | Classification of Hot Coil Work Pattern | DB注释(非中文) |
| 97 | SEMI_PROD_ITEM_CD | VARCHAR2(30) | Y |  | SEMI Production Item code | DB注释(非中文) |
| 98 | SALES_PROD_ITEM_CD | VARCHAR2(30) | Y |  | SALES Production Item code | DB注释(非中文) |
| 99 | PREV_ORD_FL | VARCHAR2(1) | Y |  | Previouse Order Flag | DB注释(非中文) |
| 100 | ORD_FL_CHANGE_REASON_CD2 | VARCHAR2(3) | Y |  | Order Flag Change Reason Code | DB注释(非中文) |
| 101 | ORD_FL_CHANGE_REASON_CD3 | VARCHAR2(3) | Y |  | Order Flag Change Reason Code | DB注释(非中文) |
| 102 | ORD_FL_CHANGE_REASON_CD4 | VARCHAR2(3) | Y |  | Order Flag Change Reason Code | DB注释(非中文) |
| 103 | ORD_FL_CHANGE_REASON_CD5 | VARCHAR2(3) | Y |  | Order Flag Change Reason Code | DB注释(非中文) |
| 104 | PREV_ORD_NO | VARCHAR2(10) | Y |  | Previouse Order NO | DB注释(非中文) |
| 105 | PREV_ORD_LN | VARCHAR2(3) | Y |  | Previouse Order Line | DB注释(非中文) |
| 106 | PREV_PROG_CD | VARCHAR2(4) | Y |  | Previouse Progress Code | DB注释(非中文) |
| 107 | PREV_HCR_FL | VARCHAR2(1) | Y |  | Previouse HCR Flag | DB注释(非中文) |
| 108 | HEAT_JUDG | VARCHAR2(1) | Y |  | Heat Judgment Result | DB注释(非中文) |
| 109 | SLAB_SCRAF_END_TY | VARCHAR2(1) | Y |  | Slab Scarfing ended Type | DB注释(非中文) |
| 110 | SLAB_CHARG_PROG_TY | VARCHAR2(1) | Y |  | Reheating Furnace Slab Charging Progress Type | DB注释(非中文) |
| 111 | COIL_NO | VARCHAR2(14) | Y |  | HotCoil No | DB注释(非中文) |
| 112 | FCE_CHARGE_DTM | VARCHAR2(14) | Y |  | Furnance Charge Date | DB注释(非中文) |
| 113 | RLG_END_DTM | VARCHAR2(14) | Y |  | The Rolling End Date | DB注释(非中文) |
| 114 | RJT_NO_DTM | VARCHAR2(14) | Y |  | Date of Reject | DB注释(非中文) |
| 115 | RJT_CAUSE_CD | VARCHAR2(2) | Y |  | Reject Cause Code | DB注释(非中文) |
| 116 | RJT_CAUSE_CD2 | VARCHAR2(2) | Y |  | Reject Cause Code | DB注释(非中文) |
| 117 | RJT_CAUSE_CD3 | VARCHAR2(2) | Y |  | Reject Cause Code | DB注释(非中文) |
| 118 | RJT_CAUSE_CD4 | VARCHAR2(2) | Y |  | Reject Cause Code | DB注释(非中文) |
| 119 | RJT_CAUSE_CD5 | VARCHAR2(2) | Y |  | Reject Cause Code | DB注释(非中文) |
| 120 | ERP_POSTING_YN | VARCHAR2(1) | Y |  | Slab Result Send To ERP Y/N | DB注释(非中文) |
| 121 | ERP_POSTING_DTM | VARCHAR2(14) | Y |  | Slab Result Send To ERP Datetime | DB注释(非中文) |
| 122 | STEEL_GRD | VARCHAR2(10) | Y |  | Steel Grade | DB注释(非中文) |
| 123 | SCARF_TY | VARCHAR2(6) | Y |  | Scarfing Type | DB注释(非中文) |
| 124 | RJT_SLAB_RLS_TY | NUMBER | Y |  | Reject Slab Release Type | DB注释(非中文) |
| 125 | STA_POS_WID_CHG | NUMBER | Y |  | Start Point of Width Change | DB注释(非中文) |
| 126 | END_POS_WID_CHG | NUMBER | Y |  | End Point of Width Change | DB注释(非中文) |
| 127 | WDG_LNDSCP_VAL | NUMBER | Y |  | Slab wedge | DB注释(非中文) |
| 128 | WDG_PORTR_VAL | NUMBER | Y |  | length slab wedge | DB注释(非中文) |
| 129 | WDG_PORTR_POS | NUMBER | Y |  | length slab wedge change | DB注释(非中文) |
| 130 | PROD_ITEM_CD | VARCHAR2(30) | Y |  | Production Item Code | DB注释(非中文) |
| 131 | ERP_TRANSACTION_TY | VARCHAR2(2) | Y |  | ERP Transaction Type | DB注释(非中文) |
| 132 | ERP_SUMUP_DT | VARCHAR2(14) | Y |  | Sumup Date | DB注释(非中文) |
| 133 | ERP_ORD_NO | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 134 | ERP_ORD_LN | VARCHAR2(3) | Y |  | Order Line No | DB注释(非中文) |
| 135 | ERP_ITEM_CD_PLAN | VARCHAR2(30) | Y |  | Item Code Plan | DB注释(非中文) |
| 136 | ERP_ITEM_CD | VARCHAR2(30) | Y |  | Item Code | DB注释(非中文) |
| 137 | ERP_PROD_QTY | NUMBER | Y |  | Product Quantity | DB注释(非中文) |
| 138 | ERP_PROD_SUB_INV_CD | VARCHAR2(2) | Y |  | Product Sub Inventory Code | DB注释(非中文) |
| 139 | ERP_MTRL_INPUT_ITEM_CD_01 | VARCHAR2(30) | Y |  | Input Item Code 01 | DB注释(非中文) |
| 140 | ERP_MTRL_INPUT_QTY_01 | NUMBER | Y |  | Input Quantity 01 | DB注释(非中文) |
| 141 | ERP_MTRL_INPUT_MTRL_NO_01 | VARCHAR2(20) | Y |  | Input Material No 01 | DB注释(非中文) |
| 142 | ERP_MTRL_INPUT_BYPROD_FL_01 | VARCHAR2(1) | Y |  | Input By-Product Flag 01 | DB注释(非中文) |
| 143 | ERP_MTRL_INPUT_SUB_INV_CD_01 | VARCHAR2(2) | Y |  | Input Sub Inventory Code 01 | DB注释(非中文) |
| 144 | ERP_MTRL_INPUT_PROC_CD_01 | VARCHAR2(4) | Y |  | Input Process Code 01 | DB注释(非中文) |
| 145 | ERP_PROC_CD_01 | VARCHAR2(4) | Y |  | Process Code 01 | DB注释(非中文) |
| 146 | ERP_RSC_USAGE_01 | NUMBER | Y |  | Resource Usage 01 | DB注释(非中文) |
| 147 | ERP_OLD_ITEM_CD | VARCHAR2(30) | Y |  |  | 空 |
| 148 | ERP_OLD_PROD_QTY | NUMBER | Y |  |  | 空 |
| 149 | DEFECT_CD | VARCHAR2(60) | Y |  | 缺陷代码 | DB注释(中文) |
| 150 | PLAN_ORD_FL | VARCHAR2(1) | Y |  | Plan Order Flag | DB注释(非中文) |
| 151 | PREV_ORD_NO1 | VARCHAR2(10) | Y |  | Previouse Order NO1 | DB注释(非中文) |
| 152 | PREV_ORD_LN1 | VARCHAR2(3) | Y |  | Previouse Order Line1 | DB注释(非中文) |
| 153 | PREV_ORD_NO2 | VARCHAR2(10) | Y |  | Previouse Order NO2 | DB注释(非中文) |
| 154 | PREV_ORD_LN2 | VARCHAR2(3) | Y |  | Previouse Order Line2 | DB注释(非中文) |
| 155 | PREV_ORD_NO3 | VARCHAR2(10) | Y |  | Previouse Order NO3 | DB注释(非中文) |
| 156 | PREV_ORD_LN3 | VARCHAR2(3) | Y |  | Previouse Order Line3 | DB注释(非中文) |
| 157 | PO_FLAG | VARCHAR2(1) | Y |  | Purchase slab flag | SCO_DATA_DIC(L) |
| 158 | PO_NO | VARCHAR2(20) | Y |  | Purchase Order Number | SCO_DATA_DIC(D) |
| 159 | PO_LINE_NO | VARCHAR2(5) | Y |  | Purchase Line Number | SCO_DATA_DIC(D) |
| 160 | PO_DLV_NO | VARCHAR2(5) | Y |  | Purchase Delivery No | SCO_DATA_DIC(D) |
| 161 | HEAT_NO_PO | VARCHAR2(20) | Y |  | po heat no | SCO_DATA_DIC(L) |
| 162 | SLAB_NO_PO | VARCHAR2(20) | Y |  | PO SLAB NO | SCO_DATA_DIC(L) |
| 163 | SURF_GRD | VARCHAR2(2) | Y |  | 表面等级 | DB注释(中文) |
| 164 | CHECK_FL | VARCHAR2(1) | Y |  |  | 空 |
| 165 | CHECK_TM | VARCHAR2(14) | Y |  |  | 空 |
| 166 | CHECK_USER_ID | VARCHAR2(20) | Y |  |  | 空 |
| 167 | ERP_SEND_YN | VARCHAR2(1) | Y |  | Slab Transfer Send To ERP Y/N | DB注释(非中文) |
| 168 | ERP_SEND_DTM | VARCHAR2(14) | Y |  | Slab Transfer Send To ERP Datetime | DB注释(非中文) |
| 169 | TRANS_FL | VARCHAR2(2) | Y |  |  | 空 |
| 170 | TRANS_EMP | VARCHAR2(20) | Y |  |  | 空 |
| 171 | TRANS_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 172 | TRANSFER_FG | VARCHAR2(2) | Y |  |  | 空 |
| 173 | ERP_SEND_FL | VARCHAR2(1) | Y |  | ?ERP???0-CCM;1-HR;2-Plate;3-Steckel | DB注释(非中文) |
| 174 | SLAB_TY | VARCHAR2(1) | Y |  | ??SLAB??_?????? | DB注释(非中文) |
| 175 | ORD_NO4 | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 176 | ORD_LN4 | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 177 | SLAB_DGN_WGT4 | NUMBER | Y |  | Slab Design Weight | DB注释(非中文) |
| 178 | PREV_ORD_NO4 | VARCHAR2(10) | Y |  | Previouse Order NO3 | DB注释(非中文) |
| 179 | PREV_ORD_LN4 | VARCHAR2(3) | Y |  | Previouse Order Line3 | DB注释(非中文) |
| 180 | ORD_NO5 | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 181 | ORD_LN5 | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 182 | SLAB_DGN_WGT5 | NUMBER | Y |  | Slab Design Weight | DB注释(非中文) |
| 183 | PREV_ORD_NO5 | VARCHAR2(10) | Y |  | Previouse Order NO3 | DB注释(非中文) |
| 184 | PREV_ORD_LN5 | VARCHAR2(3) | Y |  | Previouse Order Line3 | DB注释(非中文) |
| 185 | ORD_NO6 | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 186 | ORD_LN6 | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 187 | SLAB_DGN_WGT6 | NUMBER | Y |  | Slab Design Weight | DB注释(非中文) |
| 188 | PREV_ORD_NO6 | VARCHAR2(10) | Y |  | Previouse Order NO3 | DB注释(非中文) |
| 189 | PREV_ORD_LN6 | VARCHAR2(3) | Y |  | Previouse Order Line3 | DB注释(非中文) |
| 190 | SLAB_FG | VARCHAR2(1) | Y |  | ??SLAB??_?????? | DB注释(非中文) |
| 191 | NATL_SPEC_YEAR | VARCHAR2(4) | Y |  | ?????? | DB注释(非中文) |
| 192 | PROD_CD_FL | VARCHAR2(1) | Y |  | ?????? | DB注释(非中文) |
| 193 | SLAB_REC_DTM | VARCHAR2(14) | Y |  | ???????????? | DB注释(非中文) |
| 194 | BEF_SPEC_CD | VARCHAR2(50) | Y |  | ????? | DB注释(非中文) |
| 195 | BEF_NATL_SPEC_YEAR | VARCHAR2(4) | Y |  | ?????? | DB注释(非中文) |
| 196 | SPEC_CHG_FLAG | VARCHAR2(1) | Y |  | ?????? | DB注释(非中文) |
| 197 | SLAB_HEAT_NO | VARCHAR2(9) | Y |  | ??????? | DB注释(非中文) |
| 198 | TRANS_CCM_REQ_DTM | VARCHAR2(20) | Y |  | Transfer Request Datetime(炼钢请求出库热轧/4300/3500出库时间) | DB注释(中文) |
| 199 | TRANS_CCM_REQ_USER_ID | VARCHAR2(20) | Y |  | Transfer Request User ID(炼钢请求出库热轧/4300/3500出库者) | DB注释(中文) |
| 200 | TRANS_CCM_ACCT_DTM | VARCHAR2(14) | Y |  | Transfer Accept Datetime(炼钢接收热轧/4300/3500退库时间) | DB注释(中文) |
| 201 | TRANS_CCM_ACCT_USER_ID | VARCHAR2(20) | Y |  | Transfer Accept User ID(炼钢接收热轧/4300/3500退库接收者) | DB注释(中文) |
| 202 | TRANS_HPS_RTN_REQ_DTM | VARCHAR2(14) | Y |  | Transfer Request Datetime(热轧/4300/3500退库到炼钢请求时间) | DB注释(中文) |
| 203 | TRANS_HPS_RTN_REQ_USER_ID | VARCHAR2(20) | Y |  | Transfer Accept User ID(热轧/4300/3500退库到炼钢请求者) | DB注释(中文) |
| 204 | TRANS_HPS_ACCT_DTM | VARCHAR2(14) | Y |  | Transfer Accept Datetime(热轧/4300/3500接收炼钢退库接收时间) | DB注释(中文) |
| 205 | TRANS_HPS_ACCT_USER_ID | VARCHAR2(20) | Y |  | Transfer Accept User ID(热轧/4300/3500接收炼钢退库接接收者) | DB注释(中文) |
| 206 | TRANS_SLAB_WGT | NUMBER | Y |  | Transfer Slab Weight | DB注释(非中文) |
| 207 | COM_BLANK_PROCESS | VARCHAR2(2) | Y |  | 复合坯工序 | DB注释(中文) |
| 208 | COM_SLAB_NO | VARCHAR2(13) | Y |  | 复合板坯号 | DB注释(中文) |
| 209 | WASH_CUT_FL | VARCHAR2(1) | Y |  | 是否洗削 | DB注释(中文) |
| 210 | ALTERNATIVE_SPEC_CD | VARCHAR2(100) | Y |  | 可改判国家标准及牌号 | DB注释(中文) |
| 211 | ALTERNATIVE_NOTE | VARCHAR2(100) | Y |  | 可改判备注 | DB注释(中文) |
| 212 | DEF_MTRL_NOTE | VARCHAR2(100) | Y |  | 缺陷料备注 | DB注释(中文) |
| 213 | CAR_NO | VARCHAR2(10) | Y |  | 车号 | DB注释(中文) |
| 214 | CAR_SEQ | VARCHAR2(20) | Y |  | Car Sequence | SCO_DATA_DIC(D) |
| 215 | SLAB_FINAL_DEST | VARCHAR2(10) | Y |  | 去向 | DB注释(中文) |
| 216 | CAST_RULE | NUMBER | Y |  |  | 空 |
| 217 | SLAB_CUT_POSIT_CD_DES | VARCHAR2(10) | Y |  | 板坯切割位置 | SCO_DATA_DIC(D) |
| 218 | MIX_CAST_SLAB | VARCHAR2(1) | Y |  |  | 空 |
| 219 | IS_ABOLISH | VARCHAR2(1) | Y |  | 0:正常，1：作废 | DB注释(中文) |
| 220 | HEAT_SLAB_NO | VARCHAR2(13) | Y |  |  | 空 |
| 221 | CUT_SLAB_PROG_CD | VARCHAR2(10) | Y |  | 주편진행코드 | SCO_DATA_DIC(D) |
| 222 | INSP_EMP_NO | VARCHAR2(20) | Y |  | Inspector | SCO_DATA_DIC(D) |
| 223 | POS_IN_CAR | VARCHAR2(32) | Y |  | 车上的位置号 2020-11-02 | DB注释(中文) |
| 224 | LAYER_IN_CAR | NUMBER | Y |  | 车上的层号 2020-11-02 | DB注释(中文) |
| 225 | FORECAST_ORD_USER | VARCHAR2(10) | Y |  | 预挂单人员 | DB注释(中文) |
| 226 | FORECAST_ORD_DTM | VARCHAR2(14) | Y |  | 预挂单时间 | DB注释(中文) |
| 227 | FORECAST_ORD_REASON | VARCHAR2(100) | Y |  | 预挂单原因 | DB注释(中文) |
| 228 | ORD_NO7 | VARCHAR2(10) | Y |  |  | 空 |
| 229 | ORD_LN7 | VARCHAR2(3) | Y |  |  | 空 |
| 230 | SLAB_DGN_WGT7 | NUMBER | Y |  | Slab Design Weight | DB注释(非中文) |
| 231 | PREV_ORD_NO7 | VARCHAR2(10) | Y |  | Previouse Order NO3 | DB注释(非中文) |
| 232 | PREV_ORD_LN7 | VARCHAR2(3) | Y |  |  | 空 |
| 233 | ORD_NO8 | VARCHAR2(10) | Y |  | ORD_NO9 | SCO_DATA_DIC(D) |
| 234 | ORD_LN8 | VARCHAR2(3) | Y |  |  | 空 |
| 235 | SLAB_DGN_WGT8 | NUMBER | Y |  |  | 空 |
| 236 | PREV_ORD_NO8 | VARCHAR2(10) | Y |  |  | 空 |
| 237 | PREV_ORD_LN8 | VARCHAR2(3) | Y |  |  | 空 |
| 238 | ORD_NO9 | VARCHAR2(10) | Y |  |  | 空 |
| 239 | ORD_LN9 | VARCHAR2(3) | Y |  |  | 空 |
| 240 | SLAB_DGN_WGT9 | NUMBER | Y |  |  | 空 |
| 241 | PREV_ORD_NO9 | VARCHAR2(10) | Y |  |  | 空 |
| 242 | PREV_ORD_LN9 | VARCHAR2(3) | Y |  |  | 空 |
| 243 | REC_IN_DTM | VARCHAR2(14) | Y |  | 钢坯入库时间 | DB注释(中文) |
| 244 | YD_GR_TP | VARCHAR2(1) | Y |  | 库区 | DB注释(中文) |
| 245 | YD_LAYER_NO | NUMBER | Y |  | 层号 | DB注释(中文) |
| 246 | SHIFT_CD | VARCHAR2(1) | Y |  | 班次 | DB注释(中文) |
| 247 | SHIFT_GRP | VARCHAR2(1) | Y |  | 班组 | DB注释(中文) |
| 248 | IS_BAD | VARCHAR2(1) | Y |  |  | 空 |
| 249 | SLAB_YD_STS | VARCHAR2(2) | Y |  | 0炼钢库内1出库2轧钢库内3拒绝入库4投料出库 | DB注释(中文) |
| 250 | STR_NO | VARCHAR2(1) | Y |  | 流数 | DB注释(中文) |
| 251 | REC_IN_USER | VARCHAR2(14) | Y |  | 钢坯入库人 | DB注释(中文) |
| 252 | SWR_STATE | NUMBER | Y |  | 线材状态：1接收入库/移库入库，2退回炼钢，3入炉出库 | DB注释(中文) |
| 253 | SLAB_SECTION | VARCHAR2(20) | Y |  | 断面 | DB注释(中文) |
| 254 | BATCH_CD | VARCHAR2(20) | Y |  | 批次号 | DB注释(中文) |
| 255 | COMP_GRD | VARCHAR2(2) | Y |  | 成分等级 | DB注释(中文) |
| 256 | CPH_JDG_GRD | VARCHAR2(2) | Y |  | 综判等级 | DB注释(中文) |
| 257 | YD_LAYER_NO_SWR | VARCHAR2(50) | Y |  | 层号 | DB注释(中文) |
| 258 | PLAN_ROLL_FL | VARCHAR2(1) | Y |  |  | 空 |
| 259 | SLAB_ACT_LTH | NUMBER | Y |  | 实绩切割长度 | DB注释(中文) |
| 260 | UST_YN | VARCHAR2(1) | Y |  | 是否探伤 | DB注释(中文) |
| 261 | REMARK_GRD | VARCHAR2(20) | Y |  | 钢种备注 | DB注释(中文) |
| 262 | GBH_USER_ID | VARCHAR2(20) | Y |  | 钢板号识别系统操作用户id | DB注释(中文) |
| 263 | GBH_DTM | VARCHAR2(14) | Y |  | 钢板号识别系统操作时间 | DB注释(中文) |
| 264 | PNOTES | VARCHAR2(50) | Y |  | 原料库板坯备注 | DB注释(中文) |

### SQM_ORD_COM

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=180｜被读 170 过程 / 被写 5 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：8405　**主键**：ORD_NO、ORD_LN　**语义覆盖**：194/196

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 修改人 | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | 修改时间 | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | ORD_NO | VARCHAR2(10) | N | ✓ | 订单编号 | DB注释(中文) |
| 9 | ORD_LN | VARCHAR2(3) | N | ✓ | 订单行号 | DB注释(中文) |
| 10 | QLT_DSN_REQ_TY | VARCHAR2(3) | Y |  | 质量设计要求分类 | DB注释(中文) |
| 11 | ORD_PROG_STS | VARCHAR2(2) | N |  | 订单行号状态 | DB注释(中文) |
| 12 | ORD_MDF_TY | VARCHAR2(2) | Y |  | 订单修改分类 | DB注释(中文) |
| 13 | PROD_GRP | VARCHAR2(2) | Y |  | 品种代码 | DB注释(中文) |
| 14 | PROD_CD | VARCHAR2(3) | Y |  | 品名代码 | DB注释(中文) |
| 15 | ORD_TY | VARCHAR2(2) | Y |  | 订单类型 | DB注释(中文) |
| 16 | CUST_NM | VARCHAR2(100) | Y |  | 客户名称 | DB注释(中文) |
| 17 | CUST_CD | VARCHAR2(20) | Y |  | 客户代码 | DB注释(中文) |
| 18 | CONTRACT_NM | VARCHAR2(100) | Y |  | 订单者名称 | DB注释(中文) |
| 19 | CONTRACT_CD | VARCHAR2(9) | Y |  | 订单者代码 | DB注释(中文) |
| 20 | FINAL_CUST_NM | VARCHAR2(100) | Y |  | 最终客户名称 | DB注释(中文) |
| 21 | FINAL_CUST_CD | VARCHAR2(9) | Y |  | 最终客户代码 | DB注释(中文) |
| 22 | CUST_PO_NO | VARCHAR2(50) | Y |  | 客户PO编号 | DB注释(中文) |
| 23 | CUST_PO_LN | VARCHAR2(5) | Y |  | 客户PO行号编号 | DB注释(中文) |
| 24 | SALES_EMP_ID | VARCHAR2(20) | Y |  | 营业职员编号 | DB注释(中文) |
| 25 | DEPT_CD | VARCHAR2(15) | Y |  | 部门代码 | DB注释(中文) |
| 26 | STOC_SALES_TY | VARCHAR2(1) | Y |  | 库存销售分类 | DB注释(中文) |
| 27 | ORD_WGT_CNT_TY | VARCHAR2(1) | Y |  | 订单重量张数分类 | DB注释(中文) |
| 28 | ORD_LN_PCS | NUMBER | Y |  | 订单张数 | DB注释(中文) |
| 29 | ORD_LN_QTY | NUMBER | Y |  | 订单量 | DB注释(中文) |
| 30 | ORD_THK | NUMBER | Y |  | 订单厚度 | DB注释(中文) |
| 31 | ORD_WTH | NUMBER | Y |  | 订单宽度 | DB注释(中文) |
| 32 | ORD_LTH | NUMBER | Y |  | 订单长度 | DB注释(中文) |
| 33 | PROD_UNIT_WGT | NUMBER | Y |  | 产品计算单重 | DB注释(中文) |
| 34 | ORD_THK_TOL_CD | VARCHAR2(3) | Y |  | 订单厚度允许偏差代码 | DB注释(中文) |
| 35 | ORD_THK_TOL_MIN | NUMBER | Y |  | 订单厚度允许偏差下限 | DB注释(中文) |
| 36 | ORD_THK_TOL_MAX | NUMBER | Y |  | 订单厚度允许偏差上限 | DB注释(中文) |
| 37 | SALES_SPCL_DESC | VARCHAR2(600) | Y |  | 销售重要事项 | DB注释(中文) |
| 38 | INSP_AGENCY_CD | VARCHAR2(3) | Y |  | 检查机构代码 | DB注释(中文) |
| 39 | CLAIM_NO | VARCHAR2(18) | Y |  | 订单异议编号 | DB注释(中文) |
| 40 | BYPROD_UOM_CD | VARCHAR2(3) | Y |  | 副产品单位代码 | DB注释(中文) |
| 41 | URGENT_FL | VARCHAR2(1) | Y |  | 紧急材料 | DB注释(中文) |
| 42 | SPEC_CD | VARCHAR2(50) | Y |  | 国家标准牌号 | DB注释(中文) |
| 43 | NATL_SPEC_NO | VARCHAR2(40) | Y |  | 国家标准编号 | DB注释(中文) |
| 44 | NATL_SPEC_YEAR | VARCHAR2(4) | Y |  | 国家标准年度 | DB注释(中文) |
| 45 | STD_STLGRD | VARCHAR2(20) | Y |  | 牌号 | DB注释(中文) |
| 46 | ORD_USAGE | VARCHAR2(4) | Y |  | 订单用途代码 | DB注释(中文) |
| 47 | ORD_INSZ_THK | VARCHAR2(10) | Y |  | 订单尺寸厚度 | DB注释(中文) |
| 48 | ORD_INSZ_WTH | VARCHAR2(10) | Y |  | 订单尺寸宽度 | DB注释(中文) |
| 49 | ORD_INSZ_LTH | VARCHAR2(10) | Y |  | 订单尺寸长度 | DB注释(中文) |
| 50 | PACK_PROD_WGT_CNT_TY | VARCHAR2(1) | Y |  | 包装单重及张数分类 | DB注释(中文) |
| 51 | PACK_PROD_WGT_CNT_MAX | NUMBER | Y |  | 包装单重及张数上限 | DB注释(中文) |
| 52 | PACK_PROD_WGT_CNT_MIN | NUMBER | Y |  | 包装单重及张数下限 | DB注释(中文) |
| 53 | PACK_MTH_CD | VARCHAR2(5) | Y |  | 包装方法代码 | DB注释(中文) |
| 54 | DEST_CD | VARCHAR2(9) | Y |  | 目的地代码 | DB注释(中文) |
| 55 | DTL_DEST_NM | VARCHAR2(300) | Y |  | 详细到达地名 | DB注释(中文) |
| 56 | DELV_COND_CD | VARCHAR2(2) | Y |  | 交接条件代码 | DB注释(中文) |
| 57 | SHIP_ASGN_NO | VARCHAR2(10) | Y |  | 出口产品配船编号 | DB注释(中文) |
| 58 | ORD_EDGE_TY | VARCHAR2(1) | Y |  | 订单Edge分类 | DB注释(中文) |
| 59 | ORD_IN_DIA | NUMBER | Y |  | 订单内径 | DB注释(中文) |
| 60 | ORD_OUT_DIA | NUMBER | Y |  | 订单外径 | DB注释(中文) |
| 61 | SKINPASS_TY | VARCHAR2(1) | Y |  | 平整分类(SkinPass) | DB注释(中文) |
| 62 | CUST_QCERT_NO | VARCHAR2(15) | Y |  | 客户保证编号 | DB注释(中文) |
| 63 | STEEL_GRVT | NUMBER | Y |  | 比重 | DB注释(中文) |
| 64 | WGT_DCN_MTH_CD | VARCHAR2(2) | Y |  | 决定重量法代码 | DB注释(中文) |
| 65 | ORD_QTY_TOL_TY | VARCHAR2(1) | Y |  | 交接允许偏差分类 | DB注释(中文) |
| 66 | ORD_QTY_TOL_MAX | NUMBER | Y |  | 交接允许偏差上限 | DB注释(中文) |
| 67 | ORD_QTY_TOL_MIN | NUMBER | Y |  | 交接允许偏差下限 | DB注释(中文) |
| 68 | FISH_TAIL_CD | VARCHAR2(1) | Y |  | FishTail代码 | DB注释(中文) |
| 69 | ORG_ORD_NO | VARCHAR2(10) | Y |  | 原订单编号 | DB注释(中文) |
| 70 | ORG_ORD_LN | VARCHAR2(3) | Y |  | 原订单行号 | DB注释(中文) |
| 71 | OIL_MTH_CD | VARCHAR2(2) | Y |  | 涂油方法代码 | DB注释(中文) |
| 72 | RVRS_COIL_YN | VARCHAR2(1) | Y |  | 反转与否 | DB注释(中文) |
| 73 | PCKL_WELD_CD | VARCHAR2(3) | Y |  | 酸洗焊接代码 | DB注释(中文) |
| 74 | PROD_WELD_CD | VARCHAR2(3) | Y |  | 产品焊接代码 | DB注释(中文) |
| 75 | ORD_COAT_WGT_CD | VARCHAR2(7) | Y |  | 订单镀锌量代码 | DB注释(中文) |
| 76 | SURF_TREAT_CD | VARCHAR2(3) | Y |  | 表面处理代码 | DB注释(中文) |
| 77 | PSTREAT_CD | VARCHAR2(3) | Y |  | 后处理方法代码 | DB注释(中文) |
| 78 | SLEEVE_YN | VARCHAR2(1) | Y |  | Sleeve与否 | DB注释(中文) |
| 79 | UST_MTH_CD | VARCHAR2(2) | Y |  | 无损探伤代码(UST) | DB注释(中文) |
| 80 | DIFF_TEMP_GRD_CD | VARCHAR2(2) | Y |  | 调制分类 | DB注释(中文) |
| 81 | HTM_MTH_CD | VARCHAR2(1) | Y |  | 热处理方法代码 | DB注释(中文) |
| 82 | COAT_PROD_THK_TY | VARCHAR2(1) | Y |  | 镀锌产品厚度分类 | DB注释(中文) |
| 83 | MARK_WGT_MSU_CD | VARCHAR2(1) | Y |  | 标记重量单位 | DB注释(中文) |
| 84 | MARK_CUST_NM | VARCHAR2(80) | Y |  | 标记客户名称 | DB注释(中文) |
| 85 | MARK_PROD_NM | VARCHAR2(60) | Y |  | 标记品名 | DB注释(中文) |
| 86 | MARK_PO_NO | VARCHAR2(20) | Y |  | 标记PO编号 | DB注释(中文) |
| 87 | MARK_SPEC_NM | VARCHAR2(30) | Y |  | 标记规格名 | DB注释(中文) |
| 88 | MARK_DEST_NM | VARCHAR2(60) | Y |  | 标记目的地名 | DB注释(中文) |
| 89 | ADD_LN_MARK_MTH1 | VARCHAR2(10) | Y |  | 标记追加行1 | DB注释(中文) |
| 90 | MARK_ADD_DESC1 | VARCHAR2(100) | Y |  | 标记追加内容1 | DB注释(中文) |
| 91 | MARK_ADD_DESC2 | VARCHAR2(100) | Y |  | 标记追加内容2 | DB注释(中文) |
| 92 | MARK_ADD_DESC3 | VARCHAR2(100) | Y |  | 标记追加内容3 | DB注释(中文) |
| 93 | MARK_ADD_DESC4 | VARCHAR2(100) | Y |  | 标记追加内容4 | DB注释(中文) |
| 94 | ENGRV_MRK_CD | VARCHAR2(1) | Y |  | 刻印代码 | DB注释(中文) |
| 95 | COLOR_STRK_CD | VARCHAR2(10) | Y |  | ColorStroke代码 | DB注释(中文) |
| 96 | MTC_MSU_CD | VARCHAR2(1) | Y |  | 质量保证书标记单位 | DB注释(中文) |
| 97 | MTC_KND_CNT_CD | VARCHAR2(3) | Y |  | 质量保证书种类份数代码 | DB注释(中文) |
| 98 | MTC_SPEC_NM | VARCHAR2(60) | Y |  | 质量保证书国家标准名 | DB注释(中文) |
| 99 | MTC_DEST_NM | VARCHAR2(60) | Y |  | 质量保证书目的地名 | DB注释(中文) |
| 100 | PLT_BLK_LOT_NO | VARCHAR2(20) | Y |  | 厚板BlockLot编号 | DB注释(中文) |
| 101 | INSP_AGENCY_SHORT_NM | VARCHAR2(50) | Y |  | 检查机构简码 | DB注释(中文) |
| 102 | CUST_REQ_DELV_DT | VARCHAR2(8) | Y |  | 客户希望交接期限 | DB注释(中文) |
| 103 | DELV_LMT_DT | VARCHAR2(8) | Y |  | 交接期限 | DB注释(中文) |
| 104 | ORD_DELV_DT | VARCHAR2(8) | Y |  | 订单交货期 | DB注释(中文) |
| 105 | PROD_LMT_DT | VARCHAR2(8) | Y |  | 生产期限 | DB注释(中文) |
| 106 | DISP_LMT_DT | VARCHAR2(8) | Y |  | 出货期限 | DB注释(中文) |
| 107 | STD_WORK_TERM | NUMBER | Y |  | 标准制造工期 | DB注释(中文) |
| 108 | ORD_HOLD_TY | VARCHAR2(2) | Y |  | 订单保留分类 | DB注释(中文) |
| 109 | ORD_HOLD_CAU_CD | VARCHAR2(2) | Y |  | 订单保留原因代码 | DB注释(中文) |
| 110 | ORD_TRNSF_DT | VARCHAR2(8) | Y |  | 订单转交日期 | DB注释(中文) |
| 111 | ORD_USAGE_NM | VARCHAR2(200) | Y |  | 订单用途名 | DB注释(中文) |
| 112 | SPEC_FULL_NM | VARCHAR2(60) | Y |  | 国家标准牌号全体名称 | DB注释(中文) |
| 113 | CONV_UPPER_COAT_QTY | NUMBER | Y |  | 换算前面镀锌量 | DB注释(中文) |
| 114 | CONV_LOWER_COAT_QTY | NUMBER | Y |  | 换算后面镀锌量 | DB注释(中文) |
| 115 | TS_GRD | VARCHAR2(4) | Y |  | TS_Grade | DB注释(非中文) |
| 116 | HR_TS_TGT | NUMBER | Y |  | 热轧TS目标值 | DB注释(中文) |
| 117 | MARK_COAT_WGT_CD | VARCHAR2(7) | Y |  | 标记镀锌量代码 | DB注释(中文) |
| 118 | MARK_ENGRV_SPEC_CD | VARCHAR2(5) | Y |  | 标记刻印规格代码 | DB注释(中文) |
| 119 | PLT_PSTREAT_CD | VARCHAR2(2) | Y |  | 厚板后处理代码 | DB注释(中文) |
| 120 | TRNSF_MTH_CD | VARCHAR2(2) | Y |  | 运送方法代码 | DB注释(中文) |
| 121 | QLT_FAC_PROC_GRP | VARCHAR2(30) | Y |  | 质量工厂工序组 | DB注释(中文) |
| 122 | NATL_TOL_SPEC_SZSHP_NO | VARCHAR2(50) | Y |  | 尺寸形状允许偏差国家标准编号 | DB注释(中文) |
| 123 | NATL_TOL_SPEC_PRDCHEM_NO | VARCHAR2(50) | Y |  | 产品成分国家标准编号 | DB注释(中文) |
| 124 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  | 炼钢内控钢种编号 | DB注释(中文) |
| 125 | SMS_MFC_STD_NO | VARCHAR2(15) | Y |  | 炼钢制造标准编号 | DB注释(中文) |
| 126 | HOT_MFC_STD_NO | VARCHAR2(11) | Y |  | 热间制造标准编号 | DB注释(中文) |
| 127 | CRL_MFC_STD_NO | VARCHAR2(11) | Y |  | 冷轧制造标准编号 | DB注释(中文) |
| 128 | CMP_QCERT_NO | VARCHAR2(11) | Y |  | 公司保证编号 | DB注释(中文) |
| 129 | MTL_CMP_QCERT_NO | VARCHAR2(11) | Y |  | 材料公司保证编号 | DB注释(中文) |
| 130 | QLT_KEY_NO | NUMBER | Y |  | 质量设计Key编号 | DB注释(中文) |
| 131 | PROD_CHEM_APL_TY | VARCHAR2(1) | Y |  | 产品成分适用基准分类 | DB注释(中文) |
| 132 | QLT_DSN_STS | VARCHAR2(1) | Y |  | 质量设计状态 | DB注释(中文) |
| 133 | QLT_DSN_STS_DTM | VARCHAR2(14) | Y |  | 质量设计状态时间 | DB注释(中文) |
| 134 | QLT_DSN_RCV_DTM | VARCHAR2(14) | Y |  | 质量设计接收时间 | DB注释(中文) |
| 135 | QLT_DSN_COMPL_DTM | VARCHAR2(14) | Y |  | 质量设计结束时间 | DB注释(中文) |
| 136 | QLT_DSN_GOOD_YN | VARCHAR2(1) | Y |  | 质量设计结束时间 | DB注释(中文) |
| 137 | METH_SMP_CND | VARCHAR2(2) | Y |  | 物性测试取样条件 | DB注释(中文) |
| 138 | METH_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 物性测试长度方向取样位置 | DB注释(中文) |
| 139 | METH_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 物性测试宽度方向取样位置 | DB注释(中文) |
| 140 | METH_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 物性测试取样试样号数 | DB注释(中文) |
| 141 | MTL_METH_SMP_CND | VARCHAR2(2) | Y |  | 素材物性测试取样条件 | DB注释(中文) |
| 142 | MTL_METH_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 素材物性测试长度方向取样位置 | DB注释(中文) |
| 143 | MTL_METH_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 素材物性测试宽度方向取样位置 | DB注释(中文) |
| 144 | MTL_METH_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 素材物性测试取样试样号数 | DB注释(中文) |
| 145 | SURF_GRD | VARCHAR2(2) | Y |  | 表面等级 | DB注释(中文) |
| 146 | ORD_DSN_REQ_HIST_SEQ | NUMBER | Y |  | 质量设计要求履历列号 | DB注释(中文) |
| 147 | MDM_ITEM_REQ_DTM | VARCHAR2(14) | Y |  | Item请求时间 | DB注释(中文) |
| 148 | MDM_ITEM_RES_DTM | VARCHAR2(14) | Y |  | Item应答时间 | DB注释(中文) |
| 149 | SALES_ITEM_CD | VARCHAR2(20) | Y |  | 成品Item | DB注释(中文) |
| 150 | QLT_REMARKS | VARCHAR2(300) | Y |  | 质量备注 | DB注释(中文) |
| 151 | SHIPTO_SITE_CD | VARCHAR2(7) | Y |  | 交货地代码 | DB注释(中文) |
| 152 | BILLTO_SITE_CD | VARCHAR2(7) | Y |  | 接收地代码 | DB注释(中文) |
| 153 | CONTRACT_CONF_NO | VARCHAR2(30) | Y |  | 批示编号 | DB注释(中文) |
| 154 | ORD_WTH_TOL_CD | VARCHAR2(1) | Y |  | 订单宽度允许偏差代码 | DB注释(中文) |
| 155 | ORD_WTH_TOL_MIN | NUMBER | Y |  | 订单宽度允许偏差下限 | DB注释(中文) |
| 156 | ORD_WTH_TOL_MAX | NUMBER | Y |  | 订单宽度允许偏差上限 | DB注释(中文) |
| 157 | PPL_MECH_FL | VARCHAR2(1) | Y |  | 是否酸洗后性能(A-热轧检验冷轧检验;B-热轧检验冷轧不检验;C-热轧不检验冷轧检验;D-热轧不检验冷轧不检验;空-无指定) | DB注释(中文) |
| 158 | QLT_FPROC_PLT_TY | VARCHAR2(1) | Y |  | 质量厚板工厂工序组 | DB注释(中文) |
| 159 | QLT_FPROC_CACGL_TY | VARCHAR2(1) | Y |  | 质量退火工厂工序组 | DB注释(中文) |
| 160 | AUTO_CONF_YN | VARCHAR2(1) | Y |  | Auto Confirmation Yes or No | SCO_DATA_DIC(D) |
| 161 | ORD_SIZE_TY | VARCHAR2(1) | Y |  | Type of Order size | DB注释(非中文) |
| 162 | ORD_WTH_MAX | NUMBER | Y |  | Minimum of Order width | DB注释(非中文) |
| 163 | ORD_LTH_MAX | NUMBER | Y |  | Minimum of Order length | DB注释(非中文) |
| 164 | ORD_LTH_TOL_CD | VARCHAR2(1) | Y |  | Order length Tolerance Code | DB注释(非中文) |
| 165 | ORD_LTH_TOL_MIN | NUMBER | Y |  | Order length Ninimum Tolerance Value | DB注释(非中文) |
| 166 | ORD_LTH_TOL_MAX | NUMBER | Y |  | Order length Maximum Tolerance Value | DB注释(非中文) |
| 167 | SURF_MARK_MTH_CD | VARCHAR2(2) | Y |  | Surface Marking Method Code | DB注释(非中文) |
| 168 | SIDE_MARK_MTH_CD | VARCHAR2(2) | Y |  | Side Marking Method Code | DB注释(非中文) |
| 169 | ORD_PLT_CD | VARCHAR2(1) | Y |  | Order Plant Code | DB注释(非中文) |
| 170 | UST_STD_CD | VARCHAR2(200) | Y |  | UST Standard Code | DB注释(非中文) |
| 171 | UST_GRD_CD | VARCHAR2(1) | Y |  | UST Grade Code | DB注释(非中文) |
| 172 | HIGH_SURF_FL | VARCHAR2(1) | Y |  |  | 空 |
| 173 | ANTRST_OIL_KIND | VARCHAR2(1) | Y |  | 防锈油种类 | DB注释(中文) |
| 174 | OIL_LEVEL | VARCHAR2(2) | Y |  | 涂油级别 | DB注释(中文) |
| 175 | ORD_THK_TGT | NUMBER | Y |  | Order Target thickness | DB注释(非中文) |
| 176 | PROD_1M_WGT | NUMBER | Y |  | Products weight of 1 Meter(kg) | DB注释(非中文) |
| 177 | ORD_NATL_TOL_SPEC_SZSHP_NO | VARCHAR2(50) | Y |  | Specification Tolerance NO Of Order | DB注释(非中文) |
| 178 | CUST_SMP_LOT_FL | VARCHAR2(1) | Y |  | Customer Sample Lot Flag | DB注释(非中文) |
| 179 | SPEC_STLGRD_SUFX | VARCHAR2(15) | Y |  | Steel Grade Suffix of Specification | DB注释(非中文) |
| 180 | NATL_SPEC_ORG_CD | VARCHAR2(5) | Y |  | 国家标准机关简称 | SCO_DATA_DIC(D) |
| 181 | ROUGH_MIN | NUMBER | Y |  | 粗糙度下限 | DB注释(中文) |
| 182 | ROUGH_MAX | NUMBER | Y |  | 粗糙度上限 | DB注释(中文) |
| 183 | OIL_WGT_MIN | NUMBER | Y |  | 涂油量下限 | DB注释(中文) |
| 184 | OIL_WGT_MAX | NUMBER | Y |  | 涂油量上限 | DB注释(中文) |
| 185 | COAT_WGT_MIN | NUMBER | Y |  | 镀锌量下限 | DB注释(中文) |
| 186 | COAT_WGT_MAX | NUMBER | Y |  | 镀锌量上限 | DB注释(中文) |
| 187 | SURF_ZN_FL | VARCHAR2(1) | Y |  | 锌花标识 | DB注释(中文) |
| 188 | FLAW_DT_CD | VARCHAR2(1) | Y |  | 探伤 | DB注释(中文) |
| 189 | PROD_BASE | VARCHAR2(200) | Y |  | 生产基地 | DB注释(中文) |
| 190 | CAR_KIND | VARCHAR2(20) | Y |  | 车型 | DB注释(中文) |
| 191 | COATING_AREA | VARCHAR2(10) | Y |  | 涂层数 | DB注释(中文) |
| 192 | BETTER_SIDE | VARCHAR2(10) | Y |  | 优面 | DB注释(中文) |
| 193 | ORD_PLT_YN | VARCHAR2(1) | Y |  | 是否分产线 | DB注释(中文) |
| 194 | PROJECT_NUMBER | VARCHAR2(150) | Y |  | 科研项目代码 | DB注释(中文) |
| 195 | QUAL_DESI_ID | VARCHAR2(20) | Y |  | 质量设计人员 | DB注释(中文) |
| 196 | CR_DESC | VARCHAR2(200) | Y |  |  | 空 |

### SPR_PLATE

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=165｜被读 123 过程 / 被写 21 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：326095　**主键**：PLT_NO　**语义覆盖**：274/344

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | PLT_NO | VARCHAR2(18) | N | ✓ | 钢板号 | DB注释(中文) |
| 9 | MTL_NO | VARCHAR2(15) | Y |  | 材料号 | DB注释(中文) |
| 10 | L2_PLT_NO | VARCHAR2(18) | Y |  | L2钢板号 | DB注释(中文) |
| 11 | PLT_TY | VARCHAR2(1) | Y |  | PLATE区分 | DB注释(中文) |
| 12 | FAC_CD | VARCHAR2(1) | Y |  | 工厂代码 | DB注释(中文) |
| 13 | PLT_STS_CD | VARCHAR2(1) | Y |  | 状态代码 | DB注释(中文) |
| 14 | PLT_OPER_TRK_CD | VARCHAR2(3) | Y |  | 作业Tracking代码 | DB注释(中文) |
| 15 | PROC_CD | VARCHAR2(3) | Y |  | 工序代码 | DB注释(中文) |
| 16 | NXT_PROC_CD | VARCHAR2(3) | Y |  | 下道工序代码 | DB注释(中文) |
| 17 | PROG_CD | VARCHAR2(4) | Y |  | 进程代码 | DB注释(中文) |
| 18 | PREV_PROG_CD | VARCHAR2(4) | Y |  | 前进程代码 | DB注释(中文) |
| 19 | STR_LOC_CD | VARCHAR2(10) | Y |  | Location Code | DB注释(非中文) |
| 20 | STR_LOC_WK_DTM | VARCHAR2(14) | Y |  | Current Location Updated Date | DB注释(非中文) |
| 21 | PLT_THK | NUMBER | Y |  | 钢板厚度 | DB注释(中文) |
| 22 | PLT_WTH | NUMBER | Y |  | 钢板宽度 | DB注释(中文) |
| 23 | PLT_LTH | NUMBER | Y |  | 钢板长度 | DB注释(中文) |
| 24 | PLT_WGT | NUMBER | Y |  | 钢板重量 | DB注释(中文) |
| 25 | MSU_THK | NUMBER | Y |  | 尺寸厚度 | DB注释(中文) |
| 26 | MSU_WTH | NUMBER | Y |  | 尺寸宽度 | DB注释(中文) |
| 27 | MSU_LTH | NUMBER | Y |  | 尺寸长度 | DB注释(中文) |
| 28 | MSU_WGT | NUMBER | Y |  | 尺寸重量 | DB注释(中文) |
| 29 | SLAB_NO | VARCHAR2(20) | Y |  | 板坯号 | DB注释(中文) |
| 30 | HEAT_NO | VARCHAR2(9) | Y |  | MES炉号 | DB注释(中文) |
| 31 | ROLL_UNIT | VARCHAR2(10) | Y |  | 轧制单位 | DB注释(中文) |
| 32 | ROLL_UNIT_PRI | NUMBER | Y |  | 轧制单位内顺序 | DB注释(中文) |
| 33 | PLAN_PASS_PROC | VARCHAR2(60) | Y |  | 计划通过工序 | DB注释(中文) |
| 34 | RSLT_PASS_PROC | VARCHAR2(60) | Y |  | 实际通过工序 | DB注释(中文) |
| 35 | REM_PASS_PROC | VARCHAR2(60) | Y |  | 剩余工序 | DB注释(中文) |
| 36 | PLT_DIR_CD | VARCHAR2(1) | Y |  | 钢板去向 | DB注释(中文) |
| 37 | HOT_MFC_STD_NO | VARCHAR2(11) | Y |  | Hot Manufacture Standard NO | DB注释(非中文) |
| 38 | PLT_COOL_CD | VARCHAR2(5) | Y |  | 厚板冷却模式 | DB注释(中文) |
| 39 | PLT_HEATING_CD | VARCHAR2(1) | Y |  | 热处理方式_质量 | DB注释(中文) |
| 40 | HTM_MTH_CD | VARCHAR2(1) | Y |  | 热处理方式_订单 | DB注释(中文) |
| 41 | UST_MTH_CD | VARCHAR2(2) | Y |  | UST方式 | DB注释(中文) |
| 42 | UST_STD_CD | VARCHAR2(200) | Y |  | 探伤检查标准代码 | DB注释(中文) |
| 43 | CUT_MTH_CD | VARCHAR2(1) | Y |  | 厚板剪切方法 | DB注释(中文) |
| 44 | FCE_CH_DTM | VARCHAR2(14) | Y |  | 加热炉入炉日期时间 | DB注释(中文) |
| 45 | FCE_DISCH_DTM | VARCHAR2(14) | Y |  | 加热炉出炉日期时间 | DB注释(中文) |
| 46 | RLG_STA_DTM | VARCHAR2(14) | Y |  | 轧制开始日期时间 | DB注释(中文) |
| 47 | RLG_END_DTM | VARCHAR2(14) | Y |  | 轧制结束日期时间 | DB注释(中文) |
| 48 | RLG_SUMUP_DT | VARCHAR2(8) | Y |  | 轧制SUMUP日期 | DB注释(中文) |
| 49 | CS_CUT_YN | VARCHAR2(1) | Y |  | CS与否 | DB注释(中文) |
| 50 | DSTS_CUT_YN | VARCHAR2(1) | Y |  | DSTS与否 | DB注释(中文) |
| 51 | DS_CUT_YN | VARCHAR2(1) | Y |  | DS与否 | DB注释(中文) |
| 52 | FC_CUT_YN | VARCHAR2(1) | Y |  | 火切与否 | DB注释(中文) |
| 53 | FIN_STA_DTM | VARCHAR2(14) | Y |  | 精整开始日期时间 | DB注释(中文) |
| 54 | FIN_END_DTM | VARCHAR2(14) | Y |  | 精整结束日期时间 | DB注释(中文) |
| 55 | FIN_SUMUP_DT | VARCHAR2(8) | Y |  | 精整SUMUP日期 | DB注释(中文) |
| 56 | UST_YN | VARCHAR2(1) | Y |  | UST检查与否 | DB注释(中文) |
| 57 | APPR_JDG_YN | VARCHAR2(1) | Y |  | 外观判定与否 | DB注释(中文) |
| 58 | CPL_YN | VARCHAR2(1) | Y |  | 冷矫与否 | DB注释(中文) |
| 59 | HTM_YN | VARCHAR2(1) | Y |  | 是否热处理 | DB注释(中文) |
| 60 | HTM_CH_SEQ | NUMBER | Y |  | 热处理入炉顺序 | DB注释(中文) |
| 61 | HTM_PLAN_ROUTE | VARCHAR2(10) | Y |  | 热处理计划通过工序 | DB注释(中文) |
| 62 | HTM_RSLT_ROUTE | VARCHAR2(100) | Y |  | 热处理实际通过工序 | DB注释(中文) |
| 63 | HTM_REM_ROUTE | VARCHAR2(10) | Y |  | 热处理剩余工序 | DB注释(中文) |
| 64 | HTM_INST_REQ_YN | VARCHAR2(1) | Y |  | 热处理指令请求与否 | DB注释(中文) |
| 65 | HTM_STA_DTM | VARCHAR2(14) | Y |  | 热处理开始日期时间 | DB注释(中文) |
| 66 | HTM_END_DTM | VARCHAR2(14) | Y |  | 热处理结束日期时间 | DB注释(中文) |
| 67 | HTM_SUMUP_DT | VARCHAR2(8) | Y |  | 热处理SUMUP日期 | DB注释(中文) |
| 68 | MARK_YN | VARCHAR2(1) | Y |  | Marking与否 | DB注释(中文) |
| 69 | MARK_DTM | VARCHAR2(14) | Y |  | Marking日期时间 | DB注释(中文) |
| 70 | PLT_COOL_END_YN | VARCHAR2(1) | Y |  | 厚板冷却结束与否 | DB注释(中文) |
| 71 | PLT_COOL_END_DTM | VARCHAR2(14) | Y |  | 厚板冷却结束日期时间 | DB注释(中文) |
| 72 | PROD_WHS_DTM | VARCHAR2(14) | Y |  | 入库日期 | DB注释(中文) |
| 73 | PROD_WHS_SUMUP_DT | VARCHAR2(8) | Y |  | 计入日期 | DB注释(中文) |
| 74 | DLV_DTM | VARCHAR2(14) | Y |  | Shipment Date | DB注释(非中文) |
| 75 | ERP_TRANS_YN | VARCHAR2(1) | Y |  | ERP传送与否 | DB注释(中文) |
| 76 | ERP_TRANS_DTM | VARCHAR2(14) | Y |  | ERP传送日期时间 | DB注释(中文) |
| 77 | WHS_INF_TP | VARCHAR2(1) | Y |  | Return Inbound  Type | DB注释(非中文) |
| 78 | RTN_PROC_TY | VARCHAR2(1) | Y |  | Return Type | DB注释(非中文) |
| 79 | RTN_DTM | VARCHAR2(14) | Y |  | Return Date | DB注释(非中文) |
| 80 | RTN_SUMUP_DT | VARCHAR2(8) | Y |  | Return Work Date | DB注释(非中文) |
| 81 | RTN_PROC_REASON_CD | VARCHAR2(2) | Y |  | Return Code | DB注释(非中文) |
| 82 | RTN_PROC_USER_ID | VARCHAR2(20) | Y |  | Return Charger | DB注释(非中文) |
| 83 | RTN_RLS_DTM | VARCHAR2(14) | Y |  | Return Release Date | DB注释(非中文) |
| 84 | RTN_RLS_CD | VARCHAR2(3) | Y |  | Return Release Code | DB注释(非中文) |
| 85 | RTN_RLS_SFT_TEAM | VARCHAR2(2) | Y |  | Return Release Shift Crew | DB注释(非中文) |
| 86 | RJT_OCR_LOC | VARCHAR2(2) | Y |  | 缺号LOCATION | DB注释(中文) |
| 87 | RJT_DTM | VARCHAR2(14) | Y |  | 缺号日期时间//回炉时间 | DB注释(中文) |
| 88 | HOLD_YN | VARCHAR2(1) | Y |  | PLATE HOLD YN | DB注释(非中文) |
| 89 | WRK_DTM | VARCHAR2(14) | Y |  | 生产日期 | DB注释(中文) |
| 90 | SMP_YN | VARCHAR2(1) | Y |  | 取样与否 | DB注释(中文) |
| 91 | SMP_NO | VARCHAR2(11) | Y |  | 试样号 | DB注释(中文) |
| 92 | SMP_LTH_LOC | VARCHAR2(1) | Y |  | 试样LOCATION | DB注释(中文) |
| 93 | SMP_CUT_CNT | NUMBER | Y |  | 试样COUNT | DB注释(中文) |
| 94 | SMP_CUT_DTM | VARCHAR2(14) | Y |  | 试样日期时间 | DB注释(中文) |
| 95 | PLT_JDG_YN | VARCHAR2(1) | Y |  | 厚板判定与否 | DB注释(中文) |
| 96 | SIZE_CHG_YN | VARCHAR2(1) | Y |  | SIZE Change与否 | DB注释(中文) |
| 97 | SIZE_CHG_DTM | VARCHAR2(14) | Y |  | SIZE Change日期时间 | DB注释(中文) |
| 98 | CHEM_GRD | VARCHAR2(1) | Y |  | 成分等级 | DB注释(中文) |
| 99 | SIZE_GRD | VARCHAR2(1) | Y |  | SIZE等级(Y/N) | DB注释(中文) |
| 100 | SHAPE_GRD | VARCHAR2(1) | Y |  | 形状等级(Y/N) | DB注释(中文) |
| 101 | SURF_GRD | VARCHAR2(2) | Y |  | 表面等级(FA_FD/SC) | DB注释(中文) |
| 102 | WGT_GRD | VARCHAR2(2) | Y |  | 重量等级(Y/N) | DB注释(中文) |
| 103 | UST_GRD | VARCHAR2(1) | Y |  | 探伤实际等级 | DB注释(中文) |
| 104 | APPR_JDG_GRD | VARCHAR2(1) | Y |  | 外观判定等级 | DB注释(中文) |
| 105 | APPR_JDG_DTM | VARCHAR2(14) | Y |  | 外观判定日期时间 | DB注释(中文) |
| 106 | APPR_JDG_CNT | NUMBER | Y |  | 外观判定COUNT | DB注释(中文) |
| 107 | APPR_JDG_USER_ID | VARCHAR2(20) | Y |  | 外观判定USER ID | DB注释(中文) |
| 108 | PROD_TOT_JDG_GRD | VARCHAR2(2) | Y |  | 产品综合判定等级 | DB注释(中文) |
| 109 | ABN_RSN_CD_APPR | VARCHAR2(10) | Y |  | 外观异常原因代码 | DB注释(中文) |
| 110 | ABN_RSN_CD_MEC | VARCHAR2(3) | Y |  | 性能异常原因代码 | DB注释(中文) |
| 111 | ABN_RSN_CD_CHEM | VARCHAR2(3) | Y |  | 成分异常原因代码 | DB注释(中文) |
| 112 | ABN_RSN_CD_SMP | VARCHAR2(3) | Y |  | 试样及其它异常原因代码 | DB注释(中文) |
| 113 | ERP_TRANS_STS_CD | VARCHAR2(1) | Y |  | ERP传送状态代码 | DB注释(中文) |
| 114 | SCRAP_YN | VARCHAR2(1) | Y |  | 退废与否 | DB注释(中文) |
| 115 | SPEC_CD | VARCHAR2(50) | Y |  | 国家标准牌号 | DB注释(中文) |
| 116 | STD_STLGRD | VARCHAR2(20) | Y |  | 牌号 | DB注释(中文) |
| 117 | PROD_CD | VARCHAR2(3) | Y |  | 品名代码 | DB注释(中文) |
| 118 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  | 炼钢内控钢种编号 | DB注释(中文) |
| 119 | NATL_SPEC_YEAR | VARCHAR2(4) | Y |  | 钢种执行标准年份 | DB注释(中文) |
| 120 | NATL_SPEC_NO | VARCHAR2(40) | Y |  | 钢种执行标准号 | DB注释(中文) |
| 121 | SEMI_PROD_ITEM_CD | VARCHAR2(30) | Y |  | SEMI Production Item code | DB注释(非中文) |
| 122 | SALES_PROD_ITEM_CD | VARCHAR2(30) | Y |  | SALES Production Item code | DB注释(非中文) |
| 123 | SPL_REASON_CD | VARCHAR2(3) | Y |  | 余材原因代码 | DB注释(中文) |
| 124 | HCR_FL | VARCHAR2(1) | Y |  | HCR FLAG | DB注释(非中文) |
| 125 | ORD_FL | VARCHAR2(1) | Y |  | 订单材与否 | DB注释(中文) |
| 126 | ORD_TY | VARCHAR2(2) | Y |  | 订单类型 | DB注释(中文) |
| 127 | ORD_EDGE_TY | VARCHAR2(1) | Y |  | 订单Edge分类 | DB注释(中文) |
| 128 | ORD_USAGE | VARCHAR2(4) | Y |  | 订单用途代码 | DB注释(中文) |
| 129 | ORD_NO | VARCHAR2(10) | Y |  | 订单号 | DB注释(中文) |
| 130 | ORD_LN | VARCHAR2(3) | Y |  | 订单行号 | DB注释(中文) |
| 131 | PREV_ORD_FL | VARCHAR2(1) | Y |  | 前订单材与否 | DB注释(中文) |
| 132 | PREV_ORD_TY | VARCHAR2(2) | Y |  | 前订单类型 | DB注释(中文) |
| 133 | PREV_ORD_USAGE | VARCHAR2(4) | Y |  | 前订单用途代码 | DB注释(中文) |
| 134 | PREV_ORD_NO | VARCHAR2(10) | Y |  | 前订单号 | DB注释(中文) |
| 135 | PREV_ORD_LN | VARCHAR2(3) | Y |  | 前订单行号 | DB注释(中文) |
| 136 | PREV_SPEC_CD | VARCHAR2(50) | Y |  | 前国家标准牌号 | DB注释(中文) |
| 137 | ORD_ALLOC_TY | VARCHAR2(1) | Y |  | 订单 ALLCATION TYPE | DB注释(中文) |
| 138 | ORD_ALLOC_DTM | VARCHAR2(14) | Y |  | 订单 ALLCATION 日期时间 | DB注释(中文) |
| 139 | ORD_THK | NUMBER | Y |  | 订单厚度 | DB注释(中文) |
| 140 | ORD_WTH | NUMBER | Y |  | 订单宽度 | DB注释(中文) |
| 141 | ORD_LTH | NUMBER | Y |  | 订单长度 | DB注释(中文) |
| 142 | ORD_WGT | NUMBER | Y |  | 订单重量 | DB注释(中文) |
| 143 | ORD_NO1 | VARCHAR2(10) | Y |  | 订单号1 | DB注释(中文) |
| 144 | ORD_LN1 | VARCHAR2(3) | Y |  | 订单行号1 | DB注释(中文) |
| 145 | ORD_WTH1 | NUMBER | Y |  | 订单宽度1 | DB注释(中文) |
| 146 | ORD_LTH1 | NUMBER | Y |  | 订单长度1 | DB注释(中文) |
| 147 | ORD_WGT1 | NUMBER | Y |  | 订单重量1 | DB注释(中文) |
| 148 | ORD_PLT_PCS1 | NUMBER | Y |  | 订单钢板数1 | DB注释(中文) |
| 149 | ORD_NO2 | VARCHAR2(10) | Y |  | 订单号2 | DB注释(中文) |
| 150 | ORD_LN2 | VARCHAR2(3) | Y |  | 订单行号2 | DB注释(中文) |
| 151 | ORD_WTH2 | NUMBER | Y |  | 订单宽度2 | DB注释(中文) |
| 152 | ORD_LTH2 | NUMBER | Y |  | 订单长度2 | DB注释(中文) |
| 153 | ORD_WGT2 | NUMBER | Y |  | 订单重量2 | DB注释(中文) |
| 154 | ORD_PLT_PCS2 | NUMBER | Y |  | 订单钢板数2 | DB注释(中文) |
| 155 | ORD_NO3 | VARCHAR2(10) | Y |  | 订单号3 | DB注释(中文) |
| 156 | ORD_LN3 | VARCHAR2(3) | Y |  | 订单行号3 | DB注释(中文) |
| 157 | ORD_WTH3 | NUMBER | Y |  | 订单宽度3 | DB注释(中文) |
| 158 | ORD_LTH3 | NUMBER | Y |  | 订单长度3 | DB注释(中文) |
| 159 | ORD_WGT3 | NUMBER | Y |  | 订单重量3 | DB注释(中文) |
| 160 | ORD_PLT_PCS3 | NUMBER | Y |  | 订单钢板数3 | DB注释(中文) |
| 161 | ORD_NO4 | VARCHAR2(10) | Y |  | 订单号4 | DB注释(中文) |
| 162 | ORD_LN4 | VARCHAR2(3) | Y |  | 订单行号4 | DB注释(中文) |
| 163 | ORD_WTH4 | NUMBER | Y |  | 订单宽度4 | DB注释(中文) |
| 164 | ORD_LTH4 | NUMBER | Y |  | 订单长度4 | DB注释(中文) |
| 165 | ORD_WGT4 | NUMBER | Y |  | 订单重量4 | DB注释(中文) |
| 166 | ORD_PLT_PCS4 | NUMBER | Y |  | 订单钢板数4 | DB注释(中文) |
| 167 | ORD_NO5 | VARCHAR2(10) | Y |  | 订单号5 | DB注释(中文) |
| 168 | ORD_LN5 | VARCHAR2(3) | Y |  | 订单行号5 | DB注释(中文) |
| 169 | ORD_WTH5 | NUMBER | Y |  | 订单宽度5 | DB注释(中文) |
| 170 | ORD_LTH5 | NUMBER | Y |  | 订单长度5 | DB注释(中文) |
| 171 | ORD_WGT5 | NUMBER | Y |  | 订单重量5 | DB注释(中文) |
| 172 | ORD_PLT_PCS5 | NUMBER | Y |  | 订单钢板数5 | DB注释(中文) |
| 173 | ORD_NO6 | VARCHAR2(10) | Y |  | 订单号6 | DB注释(中文) |
| 174 | ORD_LN6 | VARCHAR2(3) | Y |  | 订单行号6 | DB注释(中文) |
| 175 | ORD_WTH6 | NUMBER | Y |  | 订单宽度6 | DB注释(中文) |
| 176 | ORD_LTH6 | NUMBER | Y |  | 订单长度6 | DB注释(中文) |
| 177 | ORD_WGT6 | NUMBER | Y |  | 订单重量6 | DB注释(中文) |
| 178 | ORD_PLT_PCS6 | NUMBER | Y |  | 订单钢板数6 | DB注释(中文) |
| 179 | BUND_NO | VARCHAR2(12) | Y |  | 吊号 | DB注释(中文) |
| 180 | BUND_SEQ | VARCHAR2(5) | Y |  | 吊内顺序 | DB注释(中文) |
| 181 | BUND_NO_YN | VARCHAR2(1) | Y |  | 是否起吊 | DB注释(中文) |
| 182 | BEF_BUND_NO | VARCHAR2(12) | Y |  | 前吊号 | DB注释(中文) |
| 183 | SPR_BED_CD | VARCHAR2(9) | Y |  | 预设垛位 | DB注释(中文) |
| 184 | LOT_NO | VARCHAR2(20) | Y |  | 批号 | DB注释(中文) |
| 185 | SLAB_LOC_WK_DTM | VARCHAR2(14) | Y |  | 原料接收时间 | DB注释(中文) |
| 186 | GRP_NO | VARCHAR2(1) | Y |  | 班组 | DB注释(中文) |
| 187 | SFT_NO | VARCHAR2(1) | Y |  | 次 | DB注释(中文) |
| 188 | SIZE_CHG_USER_ID | VARCHAR2(20) | Y |  | 尺寸更改ID | DB注释(中文) |
| 189 | GRIND_YN | VARCHAR2(1) | Y |  | 磨削与否 | DB注释(中文) |
| 190 | AVG_SLAB_WGT | NUMBER | Y |  | 分摊投料量 | DB注释(中文) |
| 191 | TRANS_FG_PLT | VARCHAR2(2) | Y |  |  | 空 |
| 192 | TRANS_REQ_DTM | VARCHAR2(14) | Y |  | Transfer Request Datetime | DB注释(非中文) |
| 193 | TRANS_REQ_USER_ID | VARCHAR2(20) | Y |  | Transfer Request User ID | DB注释(非中文) |
| 194 | TRANS_ACCT_REF_DTM | VARCHAR2(14) | Y |  | Transfer Accept Datetime | DB注释(非中文) |
| 195 | TRANS_ACCT_REF_USER_ID | VARCHAR2(20) | Y |  | Transfer Accept User ID | DB注释(非中文) |
| 196 | L2_PLT_SEQ | VARCHAR2(200) | Y |  | L2钢板号 | DB注释(中文) |
| 197 | BUND_USER_ID | VARCHAR2(20) | Y |  | 组吊ID | DB注释(中文) |
| 198 | HTM_NO | VARCHAR2(8) | Y |  | 热处理号 | DB注释(中文) |
| 199 | PLT_YIELD | VARCHAR2(8) | Y |  |  | 空 |
| 200 | OVER_ORD_FL | VARCHAR2(1) | Y |  |  | 空 |
| 201 | HTM_SAVE_FL | VARCHAR2(1) | Y |  | 是否挽救 | DB注释(中文) |
| 202 | DIV_CUT_YN | VARCHAR2(1) | Y |  | 热分段与否 | DB注释(中文) |
| 203 | SLAB_WGT | NUMBER | Y |  | Slab Weight | SCO_DATA_DIC(D) |
| 204 | ORD_SIZE_TY | VARCHAR2(1) | Y |  |  | 空 |
| 205 | FCE_CH_DIS_FL | VARCHAR2(1) | Y |  |  | 空 |
| 206 | ERP_TRANS_SEQ | VARCHAR2(2) | Y |  |  | 空 |
| 207 | ERP_TRANS_HTM_SEQ | VARCHAR2(2) | Y |  |  | 空 |
| 208 | ERP_TRANS_HTM_YN | VARCHAR2(1) | Y |  |  | 空 |
| 209 | ERP_TRANS_HTM_STS | VARCHAR2(1) | Y |  |  | 空 |
| 210 | HTM_APPR_JDG_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 211 | BUND_DTM | VARCHAR2(14) | Y |  | 组吊时间 | DB注释(中文) |
| 212 | HOLD_NAME | VARCHAR2(10) | Y |  | 落地人员 | DB注释(中文) |
| 213 | HTM_BUND_DTM | VARCHAR2(14) | Y |  | 热处理组吊时间 | DB注释(中文) |
| 214 | PRODUCTION_LINE | VARCHAR2(5) | Y |  | 产线（1：1号产线，2：2号产线） | DB注释(中文) |
| 215 | FL | VARCHAR2(2) | Y |  |  | 空 |
| 216 | UST_GRADE | VARCHAR2(2) | Y |  | UST等级 | DB注释(中文) |
| 217 | SPR_BED_CD2 | VARCHAR2(9) | Y |  | 预设剁位2 | DB注释(中文) |
| 218 | QUALITY_LOCK | VARCHAR2(1) | Y |  | 质量封锁 | DB注释(中文) |
| 219 | QUALITY_LOCK_USER | VARCHAR2(20) | Y |  | 封锁人 | DB注释(中文) |
| 220 | QUALITY_LOCK_DTM | VARCHAR2(14) | Y |  | 封锁时间 | DB注释(中文) |
| 221 | BUND_DTM_ONE | VARCHAR2(14) | Y |  | 第一次组吊时间 | DB注释(中文) |
| 222 | REP_YN | VARCHAR2(1) | Y |  | 代表与否 | DB注释(中文) |
| 223 | HOLD_RSN_CD_LOV | VARCHAR2(50) | Y |  |  | 空 |
| 224 | PLT_POSTSCRIPT | VARCHAR2(100) | Y |  | 非计划备注/倍尺删除备注 | DB注释(中文) |
| 225 | FIR_CUT | VARCHAR2(30) | Y |  | 火切 | DB注释(中文) |
| 226 | ERP_WGT_ONE | NUMBER | Y |  |  | 空 |
| 227 | TWICE_HEATING | VARCHAR2(1) | Y |  |  | 空 |
| 228 | LOC_OUT_DTM | VARCHAR2(14) | Y |  | 精整移送时间 | DB注释(中文) |
| 229 | LOC_REQ_DTM | VARCHAR2(14) | Y |  | 热处理第一次接收时间 | DB注释(中文) |
| 230 | SQM_COMMENTS | VARCHAR2(200) | Y |  | 综判备注 | DB注释(中文) |
| 231 | UST_REP_YN | VARCHAR2(1) | Y |  | UST代表与否 | DB注释(中文) |
| 232 | QUALITY_LOCK_RSN | VARCHAR2(100) | Y |  | 封锁原因 | DB注释(中文) |
| 233 | COOL_CHANGE_USER | VARCHAR2(15) | Y |  | 水冷模式修改人 | DB注释(中文) |
| 234 | COOL_CHANGE_DTM | VARCHAR2(15) | Y |  | 水冷模式修改时间 | DB注释(中文) |
| 235 | APPR_COMMENTS | VARCHAR2(200) | Y |  |  | 空 |
| 236 | ORD_NO7 | VARCHAR2(10) | Y |  |  | 空 |
| 237 | ORD_LN7 | VARCHAR2(3) | Y |  |  | 空 |
| 238 | ORD_WTH7 | NUMBER | Y |  |  | 空 |
| 239 | ORD_LTH7 | NUMBER | Y |  |  | 空 |
| 240 | ORD_WGT7 | NUMBER | Y |  |  | 空 |
| 241 | ORD_PLT_PCS7 | NUMBER | Y |  |  | 空 |
| 242 | ORD_NO8 | VARCHAR2(10) | Y |  | ORD_NO9 | SCO_DATA_DIC(D) |
| 243 | ORD_LN8 | VARCHAR2(3) | Y |  |  | 空 |
| 244 | ORD_WTH8 | NUMBER | Y |  |  | 空 |
| 245 | ORD_LTH8 | NUMBER | Y |  |  | 空 |
| 246 | ORD_WGT8 | NUMBER | Y |  |  | 空 |
| 247 | ORD_PLT_PCS8 | NUMBER | Y |  |  | 空 |
| 248 | ORD_NO9 | VARCHAR2(10) | Y |  |  | 空 |
| 249 | ORD_LN9 | VARCHAR2(3) | Y |  |  | 空 |
| 250 | ORD_WTH9 | NUMBER | Y |  |  | 空 |
| 251 | ORD_LTH9 | NUMBER | Y |  |  | 空 |
| 252 | ORD_WGT9 | NUMBER | Y |  |  | 空 |
| 253 | ORD_PLT_PCS9 | NUMBER | Y |  |  | 空 |
| 254 | AVG_SLAB_WGT2 | NUMBER | Y |  |  | 空 |
| 255 | HTM_PLT_CUT | VARCHAR2(5) | Y |  | 板型控制 | DB注释(中文) |
| 256 | DB_UNLOCK | VARCHAR2(1) | Y |  | 低倍解锁封锁 Y:解锁 | DB注释(中文) |
| 257 | DB_UNLOCK_USER | VARCHAR2(20) | Y |  | 低倍解锁封锁人 | DB注释(中文) |
| 258 | DB_UNLOCK_DTM | VARCHAR2(20) | Y |  | 低倍解锁封锁时间 | DB注释(中文) |
| 259 | HTM_PQDJ_YN | VARCHAR2(200) | Y |  | 热处理瓢曲待矫标志位 | DB注释(中文) |
| 260 | HTM_PQDJ_DTM | VARCHAR2(20) | Y |  | 热处理瓢曲待矫时间 | DB注释(中文) |
| 261 | HTM_PQDJ_USER | VARCHAR2(20) | Y |  | 热处理瓢曲待矫操作人 | DB注释(中文) |
| 262 | BIAODUAN_NO | VARCHAR2(20) | Y |  | 标段号 | DB注释(中文) |
| 263 | PLT_WGT_REAL | VARCHAR2(20) | Y |  | 真实重量 | DB注释(中文) |
| 264 | GP_BELONG | VARCHAR2(1) | Y |  | 当前所属仓库 | DB注释(中文) |
| 265 | GP_STS | VARCHAR2(1) | Y |  | 仓库状态 1请求出库 2取消出库 3接收入库 4拒绝入库 | DB注释(中文) |
| 266 | GP_TARGET | VARCHAR2(1) | Y |  | 目标仓库 | DB注释(中文) |
| 267 | GP_ORIGINA | VARCHAR2(1) | Y |  | 原始仓库 | DB注释(中文) |
| 268 | GP_RTN_WAREHOUSE | VARCHAR2(20) | Y |  | 退库时仓库 | DB注释(中文) |
| 269 | HTM_LUODI | VARCHAR2(1) | Y |  | 热处理待矫直去向 | DB注释(中文) |
| 270 | HTM_PQDJ_LOCA | VARCHAR2(5) | Y |  |  | 空 |
| 271 | ID_PIECE | VARCHAR2(18) | Y |  |  | 空 |
| 272 | ORD_NOW_PCS1 | NUMBER | Y |  |  | 空 |
| 273 | ORD_NOW_PCS2 | NUMBER | Y |  |  | 空 |
| 274 | ORD_NOW_PCS3 | NUMBER | Y |  |  | 空 |
| 275 | ORD_NOW_PCS4 | NUMBER | Y |  |  | 空 |
| 276 | ORD_NOW_PCS5 | NUMBER | Y |  |  | 空 |
| 277 | ORD_NOW_PCS6 | NUMBER | Y |  |  | 空 |
| 278 | ORD_NOW_PCS7 | NUMBER | Y |  |  | 空 |
| 279 | ORD_NOW_PCS8 | NUMBER | Y |  |  | 空 |
| 280 | ORD_NOW_PCS9 | NUMBER | Y |  |  | 空 |
| 281 | PENYIN_GRP_NO | VARCHAR2(3) | Y |  |  | 空 |
| 282 | PENYIN_LINE | VARCHAR2(3) | Y |  |  | 空 |
| 283 | PENYIN_NO | VARCHAR2(3) | Y |  |  | 空 |
| 284 | PREV_PLT_NO | VARCHAR2(15) | Y |  |  | 空 |
| 285 | ROLL_WAY | VARCHAR2(10) | Y |  |  | 空 |
| 286 | SPR_BED_CD1 | VARCHAR2(7) | Y |  |  | 空 |
| 287 | SPR_BED_CD3 | VARCHAR2(7) | Y |  |  | 空 |
| 288 | SPR_BED_CD4 | VARCHAR2(7) | Y |  |  | 空 |
| 289 | SPR_BED_CD5 | VARCHAR2(7) | Y |  |  | 空 |
| 290 | SPR_BED_CD6 | VARCHAR2(7) | Y |  |  | 空 |
| 291 | SPR_BED_CD7 | VARCHAR2(7) | Y |  |  | 空 |
| 292 | CHG_LINE_NOTE | VARCHAR2(500) | Y |  | 交换产线原因or备注 | DB注释(中文) |
| 293 | SHENGCI_1 | VARCHAR2(500) | Y |  | 剩磁强度1 | DB注释(中文) |
| 294 | SHENGCI_2 | VARCHAR2(500) | Y |  |  | 空 |
| 295 | SHENGCI_3 | VARCHAR2(500) | Y |  |  | 空 |
| 296 | SHENGCI_4 | VARCHAR2(500) | Y |  |  | 空 |
| 297 | SHENGCI_5 | VARCHAR2(500) | Y |  |  | 空 |
| 298 | SHENGCI_6 | VARCHAR2(500) | Y |  |  | 空 |
| 299 | SHENGCI_7 | VARCHAR2(500) | Y |  |  | 空 |
| 300 | SHENGCI_8 | VARCHAR2(500) | Y |  |  | 空 |
| 301 | SHENGCI_9 | VARCHAR2(500) | Y |  |  | 空 |
| 302 | SHENGCI_10 | VARCHAR2(500) | Y |  |  | 空 |
| 303 | LOC_REQ_DTM_ONE | VARCHAR2(14) | Y |  |  | 空 |
| 304 | BEFOR_HEAT_WGT | VARCHAR2(10) | Y |  | 炉前称重 | DB注释(中文) |
| 305 | HTM_UST_YN | VARCHAR2(2) | Y |  | 热处理探伤结果 | DB注释(中文) |
| 306 | HTM_UST_NOTE | VARCHAR2(500) | Y |  | 热处理探伤备注 | DB注释(中文) |
| 307 | DUOBANTAI_NO | VARCHAR2(10) | Y |  | 收集岗位保存垛班台编号 | DB注释(中文) |
| 308 | CENG_SHU | VARCHAR2(2) | Y |  | 收集岗位需要填入层数 | DB注释(中文) |
| 309 | SHOUJIKUA_NO | VARCHAR2(2) | Y |  | 收集岗位保存跨编号 | DB注释(中文) |
| 310 | MARK_THK | VARCHAR2(30) | Y |  |  | 空 |
| 311 | MARK_WTH | VARCHAR2(30) | Y |  |  | 空 |
| 312 | MARK_LTH | VARCHAR2(30) | Y |  |  | 空 |
| 313 | MARK_SPEC | VARCHAR2(30) | Y |  |  | 空 |
| 314 | MARK_PLT_NO | VARCHAR2(30) | Y |  |  | 空 |
| 315 | ROLL_LOT_NO | VARCHAR2(30) | Y |  | 线下批次号 | DB注释(中文) |
| 316 | CLEAN_FL | VARCHAR2(2) | Y |  | 清理待入库标记 | DB注释(中文) |
| 317 | SPR_TRANSFER_FLAG | VARCHAR2(10) | Y |  | 精整入库交接标志 | DB注释(中文) |
| 318 | SPR_TRANSFER_USER_ID | VARCHAR2(20) | Y |  | 精整入库交接人员 | DB注释(中文) |
| 319 | SPR_TRANSFER_TM | VARCHAR2(50) | Y |  | 精整入库交接时间 | DB注释(中文) |
| 320 | UST_DEFAULT | VARCHAR2(1) | Y |  | 是否默认 | DB注释(中文) |
| 321 | UST_USER_ID | VARCHAR2(20) | Y |  | 探伤人 | DB注释(中文) |
| 322 | UST_TM | TIMESTAMP(7) | Y |  | 探伤时间 | DB注释(中文) |
| 323 | COOL_BAD_YN | VARCHAR2(1) | Y |  | 冷床标记 | DB注释(中文) |
| 324 | COOL_BAD_NO | VARCHAR2(1) | Y |  | 冷床号 | DB注释(中文) |
| 325 | BAD_UP_USER_ID | VARCHAR2(20) | Y |  | 上冷床人员 | DB注释(中文) |
| 326 | BAD_UP_TM | VARCHAR2(14) | Y |  | 上冷床时间 | DB注释(中文) |
| 327 | BAD_DOWN_USER_ID | VARCHAR2(20) | Y |  | 下冷床人员 | DB注释(中文) |
| 328 | BAD_DOWN_TM | VARCHAR2(14) | Y |  | 下冷床时间 | DB注释(中文) |
| 329 | REVISE_YN | VARCHAR2(1) | Y |  | 精整标记 | DB注释(中文) |
| 330 | REVISE_TYPE | VARCHAR2(1) | Y |  | 精整类型 | DB注释(中文) |
| 331 | REVISE_USER_ID | VARCHAR2(20) | Y |  | 下线操作人员 | DB注释(中文) |
| 332 | REVISE_TM | VARCHAR2(14) | Y |  | 下线操作时间 | DB注释(中文) |
| 333 | REVISE_UP_USER_ID | VARCHAR2(20) | Y |  | 上线操作人员 | DB注释(中文) |
| 334 | REVISE_UP_TM | VARCHAR2(14) | Y |  | 上线操作时间 | DB注释(中文) |
| 335 | REVISE_REMARK | VARCHAR2(500) | Y |  | 精整备注 | DB注释(中文) |
| 336 | UST_LOC | VARCHAR2(10) | Y |  | 探伤位置 | DB注释(中文) |
| 337 | UST_TYPE | VARCHAR2(10) | Y |  | 探伤类型 | DB注释(中文) |
| 338 | SPR_LOC_CD | VARCHAR2(10) | Y |  | 中间库区域代码 | DB注释(中文) |
| 339 | SPR_STACK_NO | VARCHAR2(10) | Y |  | 中间库垛位 | DB注释(中文) |
| 340 | SPR_LAY_NO1 | VARCHAR2(10) | Y |  | 中间库层号 | DB注释(中文) |
| 341 | SPR_STACK_REMARK | VARCHAR2(300) | Y |  | 中间库备注 | DB注释(中文) |
| 342 | SPR_STACK_USER_ID | VARCHAR2(300) | Y |  | 中间库入库操作人 | DB注释(中文) |
| 343 | SPR_STACK_OPER_DTM | VARCHAR2(14) | Y |  | 中间库入库时间 | DB注释(中文) |
| 344 | SPR_LAY_NO | NUMBER | Y |  | 中间库层号 | DB注释(中文) |

### SSD_ORDER_LINE

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=156｜被读 146 过程 / 被写 5 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：11516　**主键**：ORD_NO、ORD_LN　**语义覆盖**：222/241

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | ORD_NO | VARCHAR2(10) | N | ✓ | Order NO | DB注释(非中文) |
| 9 | ORD_LN | VARCHAR2(3) | N | ✓ | Order Line | DB注释(非中文) |
| 10 | ORD_LN_STS | VARCHAR2(1) | N |  | Order Line status | DB注释(非中文) |
| 11 | ORD_WGT_CNT_TY | VARCHAR2(1) | Y |  | Order Line Weigh type | DB注释(非中文) |
| 12 | ORD_LN_PCS | NUMBER | Y |  | Order Line Piece | DB注释(非中文) |
| 13 | ORD_LN_QTY | NUMBER | Y |  | Order Line Quantity | DB注释(非中文) |
| 14 | SPEC_CD | VARCHAR2(50) | Y |  | Specification code | DB注释(非中文) |
| 15 | NATL_SPEC_NO | VARCHAR2(40) | Y |  | Specification  NO | DB注释(非中文) |
| 16 | NATL_SPEC_YEAR | VARCHAR2(4) | Y |  | Specification  Year | DB注释(非中文) |
| 17 | STD_STLGRD | VARCHAR2(20) | Y |  | Specification  Steel Grade | DB注释(非中文) |
| 18 | ORD_USAGE | VARCHAR2(4) | Y |  | Order usage | DB注释(非中文) |
| 19 | ORD_THK | NUMBER | Y |  | Order thickness | DB注释(非中文) |
| 20 | ORD_WTH | NUMBER | Y |  | Order width | DB注释(非中文) |
| 21 | ORD_LTH | NUMBER | Y |  | Order length | DB注释(非中文) |
| 22 | ORD_YTHK | NUMBER | Y |  |  | 空 |
| 23 | ORD_FTHK | NUMBER | Y |  |  | 空 |
| 24 | PROD_UNIT_WGT | NUMBER | Y |  | Unit of order weight | DB注释(非中文) |
| 25 | INSP_AGENCY_CD | VARCHAR2(3) | Y |  | Inspection agency Code | DB注释(非中文) |
| 26 | ORD_INSZ_THK | VARCHAR2(10) | Y |  | Order entry thickness | DB注释(非中文) |
| 27 | ORD_INSZ_WTH | VARCHAR2(10) | Y |  | Order entry width | DB注释(非中文) |
| 28 | ORD_INSZ_LTH | VARCHAR2(10) | Y |  | Order entry length | DB注释(非中文) |
| 29 | PACK_PROD_WGT_CNT_TY | VARCHAR2(1) | Y |  | Packing  quantity or piece Type | DB注释(非中文) |
| 30 | PACK_PROD_WGT_CNT_MIN | NUMBER | Y |  | Minimum of Packing quantity or piece | DB注释(非中文) |
| 31 | PACK_PROD_WGT_CNT_MAX | NUMBER | Y |  | Maximumof Packing quantity or piece | DB注释(非中文) |
| 32 | PACK_MTH_CD | VARCHAR2(5) | Y |  | Packing Method code | DB注释(非中文) |
| 33 | DEST_CD | VARCHAR2(9) | Y |  | Destinarion Code | DB注释(非中文) |
| 34 | DTL_DEST_NM | VARCHAR2(300) | Y |  | Detail Destinarion Nae | DB注释(非中文) |
| 35 | DELV_COND_CD | VARCHAR2(2) | Y |  | Delevery Condition Code | DB注释(非中文) |
| 36 | SHIP_ASGN_NO | VARCHAR2(10) | Y |  | Ship Assign No. | DB注释(非中文) |
| 37 | ORD_EDGE_TY | VARCHAR2(1) | Y |  | Order Edge Code | DB注释(非中文) |
| 38 | ORD_IN_DIA | NUMBER | Y |  | Order india | DB注释(非中文) |
| 39 | ORD_OUT_DIA | NUMBER | Y |  | Order outdia | DB注释(非中文) |
| 40 | SKINPASS_TY | VARCHAR2(1) | Y |  | Skinpass Type | DB注释(非中文) |
| 41 | CUST_QCERT_NO | VARCHAR2(15) | Y |  | Customer quality Assurance NO | DB注释(非中文) |
| 42 | COLOR_STRK_CD | VARCHAR2(10) | Y |  | Color Stroke Code | DB注释(非中文) |
| 43 | STEEL_GRVT | NUMBER | Y |  | Gravity of Steel | DB注释(非中文) |
| 44 | WGT_DCN_MTH_CD | VARCHAR2(2) | Y |  | Weight decision Method Code | DB注释(非中文) |
| 45 | ORD_QTY_TOL_TY | VARCHAR2(1) | Y |  | Tolerance Type of Order Quantity | DB注释(非中文) |
| 46 | ORD_QTY_TOL_MAX | NUMBER | Y |  | Order Quantity Tolerance Maximun Value | DB注释(非中文) |
| 47 | ORD_QTY_TOL_MIN | NUMBER | Y |  | Order Quantity Tolerance Miniimun Value | DB注释(非中文) |
| 48 | ORG_ORD_NO | VARCHAR2(10) | Y |  | Original Order NO | DB注释(非中文) |
| 49 | ORG_ORD_LN | VARCHAR2(3) | Y |  | Original Order Line | DB注释(非中文) |
| 50 | CHG_ORD_NO | VARCHAR2(10) | Y |  |  | 空 |
| 51 | CHG_ORD_LN | VARCHAR2(3) | Y |  |  | 空 |
| 52 | FISH_TAIL_CD | VARCHAR2(1) | Y |  | Fish Tail code of Hot coil | DB注释(非中文) |
| 53 | OIL_MTH_CD | VARCHAR2(2) | Y |  | Oilling Method Code | DB注释(非中文) |
| 54 | RVRS_COIL_YN | VARCHAR2(1) | Y |  | Coil Revering Yes or not | DB注释(非中文) |
| 55 | PCKL_WELD_CD | VARCHAR2(3) | Y |  | Pickling Weldding Code | DB注释(非中文) |
| 56 | PROD_WELD_CD | VARCHAR2(3) | Y |  | Products Weldding Code | DB注释(非中文) |
| 57 | ORD_COAT_WGT_CD | VARCHAR2(7) | Y |  | Order Coating Weight Code | DB注释(非中文) |
| 58 | SURF_TREAT_CD | VARCHAR2(3) | Y |  | Surface Treatment Code | DB注释(非中文) |
| 59 | ORD_SURF_GRD | VARCHAR2(2) | Y |  |  | 空 |
| 60 | PSTREAT_CD | VARCHAR2(2) | Y |  | Post Treatment Code | DB注释(非中文) |
| 61 | SLEEVE_YN | VARCHAR2(1) | Y |  | Sleeve Yes or Not | DB注释(非中文) |
| 62 | UST_MTH_CD | VARCHAR2(2) | Y |  | UST Method Code | DB注释(非中文) |
| 63 | DIFF_TEMP_GRD_CD | VARCHAR2(2) | Y |  | Difference Temperature Grade Code | DB注释(非中文) |
| 64 | HTM_MTH_CD | VARCHAR2(1) | Y |  | Heat Method Code | DB注释(非中文) |
| 65 | COAT_PROD_THK_TY | VARCHAR2(1) | Y |  | Oder Thickness Type of Coating Products | DB注释(非中文) |
| 66 | ORD_THK_TOL_CD | VARCHAR2(3) | Y |  | Order Thickness Tolerance Code | DB注释(非中文) |
| 67 | ORD_THK_TOL_MIN | NUMBER | Y |  | Order Thickness Ninimum Tolerance Value | DB注释(非中文) |
| 68 | ORD_THK_TOL_MAX | NUMBER | Y |  | Order Thickness Maximum Tolerance Value | DB注释(非中文) |
| 69 | ENGRV_MRK_CD | VARCHAR2(1) | Y |  | 타각 | DB注释(非中文) |
| 70 | PLT_PSTREAT_CD | VARCHAR2(2) | Y |  | Post Treatment Code of Plate | DB注释(非中文) |
| 71 | PLT_BLK_LOT_NO | VARCHAR2(20) | Y |  | Plate Block Number | DB注释(非中文) |
| 72 | CUST_REQ_DELV_DT | VARCHAR2(8) | Y |  | Customer Request Delevey Date | DB注释(非中文) |
| 73 | ORD_INPUT_WEEK | VARCHAR2(8) | Y |  | Order input Week | DB注释(非中文) |
| 74 | ORD_WORK_HOUR | NUMBER | Y |  |  | 空 |
| 75 | ORD_INPUT_DT | VARCHAR2(8) | Y |  | Order input Date | DB注释(非中文) |
| 76 | DELV_LMT_DT | VARCHAR2(8) | Y |  | Delevey Limit Date | DB注释(非中文) |
| 77 | ORD_DELV_DT | VARCHAR2(8) | Y |  | Order Delevey Date | DB注释(非中文) |
| 78 | SMS_LMT_DT | VARCHAR2(8) | Y |  |  | 空 |
| 79 | HR_LMT_DT | VARCHAR2(8) | Y |  |  | 空 |
| 80 | PROD_LMT_DT | VARCHAR2(8) | Y |  | Production Limit Date | DB注释(非中文) |
| 81 | DISP_LMT_DT | VARCHAR2(8) | Y |  | Dispatch Limit Date | DB注释(非中文) |
| 82 | STD_WORK_TERM | NUMBER | Y |  | Standard Work Term | DB注释(非中文) |
| 83 | ADD_WORK_TERM | NUMBER | Y |  | Additional Work Term | DB注释(非中文) |
| 84 | TRNSF_TERM | NUMBER | Y |  |  | 空 |
| 85 | TRNSF_MTH_CD | VARCHAR2(2) | Y |  | Transfer Method Code | DB注释(非中文) |
| 86 | STOC_SALES_TY | VARCHAR2(1) | Y |  | Sales type Of Stocs | SCO_DATA_DIC(D) |
| 87 | URGENT_FL | VARCHAR2(1) | Y |  | Urgent Flag | DB注释(非中文) |
| 88 | BASE_PRICE | NUMBER | Y |  | Base Price基价 | DB注释(中文) |
| 89 | EXTRA_PRICE | NUMBER | Y |  | Extra Price其他加价 | DB注释(中文) |
| 90 | DISCNT_PRICE | NUMBER | Y |  | 一口价/折扣或加价 Discount  Charge | DB注释(中文) |
| 91 | BILL_DISCNT_PRICE | NUMBER | Y |  | 免贴息加价 | DB注释(中文) |
| 92 | PROD_PRICE | NUMBER | Y |  | Products Price产品标准价格 | DB注释(中文) |
| 93 | TRNSF_PRICE | NUMBER | Y |  | Transfer Price | DB注释(非中文) |
| 94 | TRNSF_ADD_PRICE | NUMBER | Y |  |  | 空 |
| 95 | BASE_PRICE_CNY | NUMBER | Y |  | Base Price in CNY | DB注释(非中文) |
| 96 | EXTRA_PRICE_CNY | NUMBER | Y |  | Extra Price in CNY | DB注释(非中文) |
| 97 | DISCNT_PRICE_CNY | NUMBER | Y |  | Discount  Charge | DB注释(非中文) |
| 98 | BILL_DISCNT_PRICE_CNY | NUMBER | Y |  |  | 空 |
| 99 | PROD_PRICE_CNY | NUMBER | Y |  | Products Price  in CNY | DB注释(非中文) |
| 100 | TRNSF_PRICE_CNY | NUMBER | Y |  | Transfer Price  in CNY | DB注释(非中文) |
| 101 | TRNSF_ADD_PRICE_CNY | NUMBER | Y |  | 一票结算税差 | DB注释(中文) |
| 102 | PROD_PRICE_APPLY | NUMBER | Y |  | Applied Products Price产品适用单价 | DB注释(中文) |
| 103 | TRNSF_PRICE_APPLY | NUMBER | Y |  | Applied Products Price | DB注释(非中文) |
| 104 | PROD_PRICE_APPLY_CNY | NUMBER | Y |  | Applied Products Price | DB注释(非中文) |
| 105 | TRNSF_PRICE_APPLY_CNY | NUMBER | Y |  | Applied Products Price | DB注释(非中文) |
| 106 | PROD_AMT | NUMBER | Y |  | Products Amount | DB注释(非中文) |
| 107 | TRNSF_AMT | NUMBER | Y |  | Transfer Amount | DB注释(非中文) |
| 108 | TOT_AMT | NUMBER | Y |  | Total Amount | DB注释(非中文) |
| 109 | PROD_AMT_CNY | NUMBER | Y |  | Products Amount in CNY | DB注释(非中文) |
| 110 | TRNSF_AMT_CNY | NUMBER | Y |  | Transfer Amount in CNY | DB注释(非中文) |
| 111 | TOT_AMT_CNY | NUMBER | Y |  | Total Amount in CNY | DB注释(非中文) |
| 112 | PREPAYMENT_ASGN_AMT | NUMBER | Y |  | Prepayment Assign Amount | DB注释(非中文) |
| 113 | ORD_RCV_DT | VARCHAR2(8) | Y |  | Order Receipt Date | DB注释(非中文) |
| 114 | ORD_REG_DTM | VARCHAR2(14) | Y |  | Order Register Date | DB注释(非中文) |
| 115 | ORD_CONF_DTM | VARCHAR2(14) | Y |  | Order Confirm Date | DB注释(非中文) |
| 116 | ORD_REGL_EMP_ID | VARCHAR2(20) | Y |  | Order Register Employee ID | DB注释(非中文) |
| 117 | ORD_CONF_EMP_ID | VARCHAR2(20) | Y |  | Order Confirm Employee ID | DB注释(非中文) |
| 118 | ORD_HOLD_TY | VARCHAR2(2) | Y |  | Order hold Type | DB注释(非中文) |
| 119 | ORD_HOLD_CAU_CD | VARCHAR2(2) | Y |  | Order holding Cause Code | DB注释(非中文) |
| 120 | ORD_HOLD_EMP_ID | VARCHAR2(20) | Y |  | Order hold Employee ID | DB注释(非中文) |
| 121 | ORD_HOLD_DTM | VARCHAR2(14) | Y |  | Order hold Date | DB注释(非中文) |
| 122 | ORD_CANCEL_TY | VARCHAR2(2) | Y |  | Order Cancel Type | DB注释(非中文) |
| 123 | ORD_CANCEL_EMP_ID | VARCHAR2(20) | Y |  | Order Cancel Employee ID | DB注释(非中文) |
| 124 | ORD_CANCEL_DTM | VARCHAR2(14) | Y |  | Order Cancel Date | DB注释(非中文) |
| 125 | ORD_MDF_TY | VARCHAR2(2) | Y |  | Order Modify Type | DB注释(非中文) |
| 126 | ORD_MDF_EMP_ID | VARCHAR2(20) | Y |  | Order Modify Employee ID | DB注释(非中文) |
| 127 | ORD_MDF_DTM | VARCHAR2(14) | Y |  | Order Modify Date | SCO_DATA_DIC(D) |
| 128 | ORD_END_TY | VARCHAR2(2) | Y |  | Order End Type | DB注释(非中文) |
| 129 | ORD_END_EMP_ID | VARCHAR2(20) | Y |  | Order End Employee ID | DB注释(非中文) |
| 130 | ORD_END_DTM | VARCHAR2(14) | Y |  | Order Eed Date | DB注释(非中文) |
| 131 | SALES_SPCL_DESC | VARCHAR2(600) | Y |  | Special Description in Sales Department订单备注 | DB注释(中文) |
| 132 | MARK_WGT_MSU_CD | VARCHAR2(1) | Y |  | Marking Quanty UOM | DB注释(非中文) |
| 133 | MARK_CUST_NM | VARCHAR2(80) | Y |  | Marking Customer Name标记客户 | DB注释(中文) |
| 134 | MARK_PROD_NM | VARCHAR2(60) | Y |  | Marking Oroducts Name标记品名 | DB注释(中文) |
| 135 | MARK_PO_NO | VARCHAR2(20) | Y |  | Marking PO标记合同号 | DB注释(中文) |
| 136 | MARK_SPEC_NM | VARCHAR2(30) | Y |  | Marking Specification Name标记标准 | DB注释(中文) |
| 137 | MARK_DEST_NM | VARCHAR2(60) | Y |  | Marking Destination Name标记目的地 | DB注释(中文) |
| 138 | ADD_LN_MARK_MTH1 | VARCHAR2(10) | Y |  | Additional Marking Method | DB注释(非中文) |
| 139 | MARK_ADD_DESC1 | VARCHAR2(100) | Y |  | Additional Marking Description 1标签备注 | DB注释(中文) |
| 140 | MARK_ADD_DESC2 | VARCHAR2(100) | Y |  | Additional Marking Description 2质保书备注 | DB注释(中文) |
| 141 | MARK_ADD_DESC3 | VARCHAR2(100) | Y |  | Additional Marking Description 3 | DB注释(非中文) |
| 142 | MARK_ADD_DESC4 | VARCHAR2(100) | Y |  | Additional Marking Description 4 | DB注释(非中文) |
| 143 | MTC_MSU_CD | VARCHAR2(1) | Y |  | MTC UOM | DB注释(非中文) |
| 144 | MTC_KND_CNT_CD | VARCHAR2(3) | Y |  | MTC Kind Prinf count | DB注释(非中文) |
| 145 | MTC_TY | VARCHAR2(2) | Y |  | MTC Specification Name | DB注释(非中文) |
| 146 | MTC_SPEC_NM | VARCHAR2(60) | Y |  | MTC Destination Name | DB注释(非中文) |
| 147 | MTC_DEST_NM | VARCHAR2(60) | Y |  |  | 空 |
| 148 | PRICE_CALC_CD | VARCHAR2(1) | Y |  |  | 空 |
| 149 | SPEC_EXTRA_PRICE | NUMBER | Y |  | 品种加价 | DB注释(中文) |
| 150 | SPEC_EXTRA_PRICE_CNY | NUMBER | Y |  |  | 空 |
| 151 | ORD_WTH_TOL_CD | VARCHAR2(1) | Y |  | 폭공차구분 | SCO_DATA_DIC(D) |
| 152 | ORD_WTH_TOL_MIN | NUMBER | Y |  | Order Width Tolernace Max | SCO_DATA_DIC(D) |
| 153 | ORD_WTH_TOL_MAX | NUMBER | Y |  | Order Width Tolernace Min | SCO_DATA_DIC(D) |
| 154 | MTC_DELV_TY | VARCHAR2(1) | Y |  |  | 空 |
| 155 | MTC_DELV_ADDR | VARCHAR2(500) | Y |  |  | 空 |
| 156 | FIN_PROC_DIV_FL | VARCHAR2(1) | Y |  |  | 空 |
| 157 | PPL_MECH_FL | VARCHAR2(1) | Y |  | 性能选项 | DB注释(中文) |
| 158 | ORD_SIZE_TY | VARCHAR2(1) | Y |  | Type of Order size | DB注释(非中文) |
| 159 | ORD_WTH_MAX | NUMBER | Y |  | Maximum of Order width | DB注释(非中文) |
| 160 | ORD_LTH_MAX | NUMBER | Y |  | Maximum of Order length | DB注释(非中文) |
| 161 | ORD_LTH_TOL_CD | VARCHAR2(1) | Y |  | Order length Tolerance Code | DB注释(非中文) |
| 162 | ORD_LTH_TOL_MIN | NUMBER | Y |  | Order length Ninimum Tolerance Value | DB注释(非中文) |
| 163 | ORD_LTH_TOL_MAX | NUMBER | Y |  | Order length Maximum Tolerance Value | DB注释(非中文) |
| 164 | SURF_MARK_MTH_CD | VARCHAR2(2) | Y |  | Surmaface Marking Method Code | DB注释(非中文) |
| 165 | SIDE_MARK_MTH_CD | VARCHAR2(2) | Y |  | Side Marking Method Code | DB注释(非中文) |
| 166 | ORD_PLT_CD | VARCHAR2(1) | Y |  | Order Plant Code | DB注释(非中文) |
| 167 | UST_STD_CD | VARCHAR2(200) | Y |  | UST Standard Code | DB注释(非中文) |
| 168 | UST_GRD_CD | VARCHAR2(1) | Y |  | UST Grade Code | DB注释(非中文) |
| 169 | HIGH_SURF_FL | VARCHAR2(1) | Y |  |  | 空 |
| 170 | WELD_HTM_SIMUL_FL | VARCHAR2(1) | Y |  | HEAT Treatment Simulation Flag After Welding | DB注释(非中文) |
| 171 | OIL_LEVEL | VARCHAR2(2) | Y |  | 涂油级别 | DB注释(中文) |
| 172 | ANTRST_OIL_KIND | VARCHAR2(1) | Y |  | 防锈油种类 | DB注释(中文) |
| 173 | ORD_THK_TGT | NUMBER | Y |  | Order Target thickness | DB注释(非中文) |
| 174 | ORD_THK_ADD | NUMBER | Y |  | Order Add thickness 厚度附加值 | DB注释(中文) |
| 175 | THK_ADD_PRICE | NUMBER | Y |  | 厚度附加值不计重加价Target thickness Add Price | DB注释(中文) |
| 176 | PROD_1M_WGT | NUMBER | Y |  | Products weight of 1 Meter(kg) | DB注释(非中文) |
| 177 | THK_CAL_FL | VARCHAR2(1) | Y |  | Thicknss Calculation Flag OF Plate Products附加值计重 | DB注释(中文) |
| 178 | ORD_NATL_TOL_SPEC_SZSHP_NO | VARCHAR2(50) | Y |  | Specification Tolerance NO Of Order厚度偏差执行标准 | DB注释(中文) |
| 179 | CUST_SMP_LOT_FL | VARCHAR2(1) | Y |  | Customer Sample Lot Flag | DB注释(非中文) |
| 180 | QLT_THK_TOL_MIN | NUMBER | Y |  | Order Thickness Ninimum Tolerance Value | DB注释(非中文) |
| 181 | QLT_THK_TOL_MAX | NUMBER | Y |  | Order Thickness Maximum Tolerance Value | DB注释(非中文) |
| 182 | QLT_DSN_DTM | VARCHAR2(14) | Y |  | Quality Design Completed date | DB注释(非中文) |
| 183 | QLT_DSN_EMP_ID | VARCHAR2(20) | Y |  | Quality Design Completed Employee ID | DB注释(非中文) |
| 184 | TRNSF_DESC | VARCHAR2(600) | Y |  | Description in Transfer（运输备注） | DB注释(中文) |
| 185 | SPEC_STLGRD_SUFX | VARCHAR2(15) | Y |  | 钢种后缀 | DB注释(中文) |
| 186 | ROUGH_MIN | NUMBER | Y |  | 粗糙度下限 | DB注释(中文) |
| 187 | ROUGH_MAX | NUMBER | Y |  | 粗糙度上限 | DB注释(中文) |
| 188 | OIL_WGT_MIN | NUMBER | Y |  | 涂油量下限 | DB注释(中文) |
| 189 | OIL_WGT_MAX | NUMBER | Y |  | 涂油量上限 | DB注释(中文) |
| 190 | COAT_WGT_MIN | NUMBER | Y |  | 镀锌量A面 | DB注释(中文) |
| 191 | COAT_WGT_MAX | NUMBER | Y |  | 镀锌量B面 | DB注释(中文) |
| 192 | SURF_ZN_FL | VARCHAR2(1) | Y |  | 锌花标识 | DB注释(中文) |
| 193 | PROD_BASE | VARCHAR2(200) | Y |  | 生产基地 | DB注释(中文) |
| 194 | CAR_KIND | VARCHAR2(20) | Y |  | 车型 | DB注释(中文) |
| 195 | COATING_AREA | VARCHAR2(10) | Y |  | 图层数 | DB注释(中文) |
| 196 | BETTER_SIDE | VARCHAR2(10) | Y |  | 优面 | DB注释(中文) |
| 197 | SALES_PROD_ITEM_CD | VARCHAR2(20) | Y |  | 产品物料编码 | DB注释(中文) |
| 198 | INVOICE_COMP_DTM | VARCHAR2(14) | Y |  | Invoice Complete Time(结算完成时间W) | DB注释(中文) |
| 199 | INVOICE_COMP_ID | VARCHAR2(20) | Y |  | Invoice Complete Employee ID(结算完成人员W) | DB注释(中文) |
| 200 | CARRIER_COMPANY_FST | VARCHAR2(100) | Y |  | 承运商1 | DB注释(中文) |
| 201 | CARRIER_COMPANY_SED | VARCHAR2(100) | Y |  | 承运商2 | DB注释(中文) |
| 202 | CARRIER_COMPANY_THD | VARCHAR2(100) | Y |  | 承运商3 | DB注释(中文) |
| 203 | SPEC_ADD_PRICE | NUMBER | Y |  | 规格加价 | DB注释(中文) |
| 204 | ACT_PLT_CD | VARCHAR2(1) | Y |  | 实际厚板产线 | DB注释(中文) |
| 205 | DORD_TRNSF_MTH_CD | VARCHAR2(2) | Y |  | 出货指示运输方式 | DB注释(中文) |
| 206 | DORD_DELV_COND_CD | VARCHAR2(2) | Y |  | 出货指示交货方式 | DB注释(中文) |
| 207 | DORD_DEST_CD | VARCHAR2(9) | Y |  | 出货指示目的地代码 | DB注释(中文) |
| 208 | DORD_TRNSF_DOCU_NO | VARCHAR2(20) | Y |  | 出货指示运费价格文件 | DB注释(中文) |
| 209 | DORD_MDF_DTM | VARCHAR2(14) | Y |  | 出货指示修改时间 | DB注释(中文) |
| 210 | DORD_TRNSF_PRICE | NUMBER | Y |  | 出货指示修改后价格 | DB注释(中文) |
| 211 | DORD_TRNSF_ADD_PRICE | NUMBER | Y |  | 出货指示修改后结算税差 | DB注释(中文) |
| 212 | DORD_MDF_YN | VARCHAR2(1) | Y |  | 出货指示修改与否 | DB注释(中文) |
| 213 | DORD_MDF_RSN | VARCHAR2(200) | Y |  | 出货指示修改原因 | DB注释(中文) |
| 214 | DORD_MDF_ID | VARCHAR2(20) | Y |  | 出货指示修改ID | DB注释(中文) |
| 215 | FR_STATION_CD | VARCHAR2(5) | Y |  | 发货港(站) | DB注释(中文) |
| 216 | DORD_UNLOAD_PLACE_INCHARGE | VARCHAR2(80) | Y |  | 卸货地负责人 | DB注释(中文) |
| 217 | DORD_UNLOAD_PLACE_TEL_NO | VARCHAR2(80) | Y |  | 卸车地联系号码 | DB注释(中文) |
| 218 | DORD_UNLOAD_PLACE_ADDR | VARCHAR2(200) | Y |  | 卸货地址 | DB注释(中文) |
| 219 | DORD_SITE_CD | VARCHAR2(7) | Y |  | 收货方代码 | DB注释(中文) |
| 220 | PORT_TRNSF_PRICE | NUMBER | Y |  | 短倒运输费 | DB注释(中文) |
| 221 | PORT_WORK_PRICE | NUMBER | Y |  | 港口作业费 | DB注释(中文) |
| 222 | PORT_BUILD_PRICE | NUMBER | Y |  | 港口建设费 | DB注释(中文) |
| 223 | PORT_AGENT_PRICE | NUMBER | Y |  | 港/站货物代理费 | DB注释(中文) |
| 224 | PROD_FIX_COST | NUMBER | Y |  | 固定成本 | DB注释(中文) |
| 225 | PROD_VAR_COST | NUMBER | Y |  | 变动成本 | DB注释(中文) |
| 226 | PROJECT_NUMBER | VARCHAR2(150) | Y |  | 科研项目代码 | DB注释(中文) |
| 227 | PROJECT_DESC | VARCHAR2(240) | Y |  | 科研项目名称 | DB注释(中文) |
| 228 | FLOAT_RATIO | NUMBER | Y |  | 运费浮动比例 | DB注释(中文) |
| 229 | PORT_TRNSF_PRICE_MOD | NUMBER | Y |  | 短倒运输费(改地址后) | DB注释(中文) |
| 230 | PORT_WORK_PRICE_MOD | NUMBER | Y |  | 港口作业费(改地址后) | DB注释(中文) |
| 231 | PORT_BUILD_PRICE_MOD | NUMBER | Y |  | 港口建设费(改地址后) | DB注释(中文) |
| 232 | PORT_AGENT_PRICE_MOD | NUMBER | Y |  | 港/站货物代理费(改地址后) | DB注释(中文) |
| 233 | ORD_THK_ADD_MANU | NUMBER | Y |  | 人工指定厚度附加值 | DB注释(中文) |
| 234 | CR_DESC | VARCHAR2(150) | Y |  | 冷轧备注 | DB注释(中文) |
| 235 | CC_PROD_ORD_LEVEL | VARCHAR2(1) | Y |  | 冷轧产品订单等级 | DB注释(中文) |
| 236 | PROD_COST | NUMBER | Y |  |  | 空 |
| 237 | CUST_PO_NO | VARCHAR2(50) | Y |  | 电商订单号 | DB注释(中文) |
| 238 | CUST_PO_LN_NO | VARCHAR2(30) | Y |  | 电商订单行号 | DB注释(中文) |
| 239 | ORD_LTH_MIN | NUMBER | Y |  | 下限值(>) | SCO_DATA_DIC(D) |
| 240 | CUST_ROLL | VARCHAR2(10) | Y |  | 中板是否定轧  0-否   1- 是 | DB注释(中文) |
| 241 | SEGMENT_NO | VARCHAR2(20) | Y |  | 分段号 | DB注释(中文) |

### SCR_COIL_MASTER

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=145｜被读 97 过程 / 被写 24 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：71　**主键**：COIL_NO　**语义覆盖**：186/219

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | SCO_DATA_DIC(D) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | SCO_DATA_DIC(D) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | SCO_DATA_DIC(D) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated UserID | SCO_DATA_DIC(D) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated ObjectID | SCO_DATA_DIC(D) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Date Time | SCO_DATA_DIC(D) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | SCO_DATA_DIC(D) |
| 8 | COIL_NO | VARCHAR2(14) | N | ✓ |  | 空 |
| 9 | RCD_STS_ID | VARCHAR2(1) | Y |  | Record Status Flag | SCO_DATA_DIC(D) |
| 10 | PREV_COIL_NO | VARCHAR2(14) | Y |  | 전코일번호 | SCO_DATA_DIC(D) |
| 11 | PROC_CD | VARCHAR2(3) | Y |  | Process Code | SCO_DATA_DIC(D) |
| 12 | PROG_CD | VARCHAR2(4) | Y |  | Progress Code | SCO_DATA_DIC(D) |
| 13 | PREV_PROG_CD | VARCHAR2(4) | Y |  | 전 CR진도코드 | SCO_DATA_DIC(D) |
| 14 | ROLL_UNIT | VARCHAR2(10) | Y |  | Roll단위 | SCO_DATA_DIC(D) |
| 15 | MULTI_ORD_TP | VARCHAR2(1) | Y |  | Represntive Order Type | SCO_DATA_DIC(D) |
| 16 | ORD_NO | VARCHAR2(10) | Y |  | Order No | SCO_DATA_DIC(D) |
| 17 | ORD_LN | VARCHAR2(3) | Y |  |  | 空 |
| 18 | PREV_ORD_NO | VARCHAR2(10) | Y |  | Previous Order No | SCO_DATA_DIC(D) |
| 19 | PREV_ORD_LN | VARCHAR2(3) | Y |  | 전주문행번 | SCO_DATA_DIC(D) |
| 20 | HCOIL_ORD_WGT | NUMBER | Y |  | 복수수요가 중량1 | SCO_DATA_DIC(D) |
| 21 | HCOIL_ORD_LTH | NUMBER | Y |  | Multi order Length | SCO_DATA_DIC(D) |
| 22 | SUB_ORD_NO1 | VARCHAR2(10) | Y |  | Sub Order Head Number1 | SCO_DATA_DIC(D) |
| 23 | SUB_ORD_LN1 | VARCHAR2(3) | Y |  | Sub Order Line Number1 | SCO_DATA_DIC(D) |
| 24 | HCOIL_ORD_WGT1 | NUMBER | Y |  | 복수수요가 중량2 | SCO_DATA_DIC(D) |
| 25 | HCOIL_ORD_LTH1 | NUMBER | Y |  | Multi order2 Length | SCO_DATA_DIC(D) |
| 26 | SUB_ORD_NO2 | VARCHAR2(10) | Y |  | Sub Order Head Number2 | SCO_DATA_DIC(D) |
| 27 | SUB_ORD_LN2 | VARCHAR2(3) | Y |  | Sub Order Line Number2 | SCO_DATA_DIC(D) |
| 28 | HCOIL_ORD_WGT2 | NUMBER | Y |  | 복수수요가 중량3 | SCO_DATA_DIC(D) |
| 29 | HCOIL_ORD_LTH2 | NUMBER | Y |  | Multi order2 Length | SCO_DATA_DIC(D) |
| 30 | ORD_CHG_FG | VARCHAR2(1) | Y |  | 목전충당구분 | SCO_DATA_DIC(D) |
| 31 | ORD_CHG_DTM | VARCHAR2(14) | Y |  | 목전충당일시 | SCO_DATA_DIC(D) |
| 32 | MTL_CD | VARCHAR2(18) | Y |  | MaterialCode | SCO_DATA_DIC(D) |
| 33 | HCOIL_NO | VARCHAR2(14) | Y |  | 재료수 | SCO_DATA_DIC(L) |
| 34 | HCOIL_LTH | NUMBER | Y |  |  | 空 |
| 35 | HCOIL_WGT | NUMBER | Y |  | 중량 | SCO_DATA_DIC(L) |
| 36 | HCOIL_NO1 | VARCHAR2(14) | Y |  | 재료수 | SCO_DATA_DIC(L) |
| 37 | HCOIL_LTH1 | NUMBER | Y |  | 대표원자재길이 | SCO_DATA_DIC(D) |
| 38 | HCOIL_WGT1 | NUMBER | Y |  | 중량 | SCO_DATA_DIC(L) |
| 39 | HCOIL_NO2 | VARCHAR2(14) | Y |  | 재료수 | SCO_DATA_DIC(L) |
| 40 | HCOIL_LTH2 | NUMBER | Y |  | 원자재길이2 | SCO_DATA_DIC(D) |
| 41 | HCOIL_WGT2 | NUMBER | Y |  | 중량 | SCO_DATA_DIC(L) |
| 42 | HCOIL_SLAB_NO | VARCHAR2(12) | Y |  | 원자재SLAB번호 | SCO_DATA_DIC(D) |
| 43 | ORD_PDN_TP | VARCHAR2(1) | Y |  | 주문생산구분 | SCO_DATA_DIC(D) |
| 44 | URG_MTL_TP | VARCHAR2(1) | Y |  | 긴급재구분 | SCO_DATA_DIC(D) |
| 45 | ORD_FL | VARCHAR2(1) | Y |  | APO/NAPO Type | SCO_DATA_DIC(D) |
| 46 | PREV_ORD_FL | VARCHAR2(1) | Y |  | 전 주여구분 | SCO_DATA_DIC(D) |
| 47 | ORD_FL_DTM | VARCHAR2(14) | Y |  | Updated Timestamp for Current NOK Caused Code | SCO_DATA_DIC(D) |
| 48 | ORD_FL_CD | VARCHAR2(2) | Y |  | Current WO Caused Code | SCO_DATA_DIC(D) |
| 49 | ORD_DELV_SUMUP_DT | VARCHAR2(8) | Y |  | Delivery Date | SCO_DATA_DIC(D) |
| 50 | FINAL_CUST_CD | VARCHAR2(5) | Y |  | Final Customer Code | SCO_DATA_DIC(D) |
| 51 | FINAL_CUST_NM | VARCHAR2(100) | Y |  | Final Customer Name | SCO_DATA_DIC(D) |
| 52 | DELV_COND_CD | VARCHAR2(2) | Y |  | Delevery Condition Code | SCO_DATA_DIC(D) |
| 53 | DMY_PTT_PLT_TP | VARCHAR2(1) | Y |  | Dummy보호판구분 | SCO_DATA_DIC(D) |
| 54 | STR_LOC_CD | VARCHAR2(9) | Y |  |  | 空 |
| 55 | LOC_WK_DTM | VARCHAR2(14) | Y |  | 현저장위치작업일시 | SCO_DATA_DIC(D) |
| 56 | CRL_MFC_STD_NO | VARCHAR2(10) | Y |  | 冷轧制造标准编号 | SCO_DATA_DIC(D) |
| 57 | COIL_THK | NUMBER | Y |  |  | 空 |
| 58 | COIL_WTH | NUMBER | Y |  |  | 空 |
| 59 | COIL_LTH | NUMBER | Y |  | Coil Length | SCO_DATA_DIC(D) |
| 60 | PLN_PASS_PROC_CD | VARCHAR2(60) | Y |  | 계획통과공정 | SCO_DATA_DIC(D) |
| 61 | PASS_PROC_CD | VARCHAR2(60) | Y |  | Work Process Line | SCO_DATA_DIC(D) |
| 62 | REM_PROC_CD | VARCHAR2(60) | Y |  | Remain Process Line | SCO_DATA_DIC(D) |
| 63 | NXT_PROC_CD | VARCHAR2(60) | Y |  | Next PROC_CD | SCO_DATA_DIC(D) |
| 64 | DMD_NXT_PROC_CAU_CD | VARCHAR2(2) | Y |  | Worker Required Next Process Reason Code | SCO_DATA_DIC(D) |
| 65 | WGT_DCN_MTH_CD | VARCHAR2(2) | Y |  | Weight_Decision_Method_Code | SCO_DATA_DIC(D) |
| 66 | COIL_NET_WGT | NUMBER | Y |  | The Coil Weight after Recolling | SCO_DATA_DIC(D) |
| 67 | COIL_GROSS_NET_WGT | NUMBER | Y |  | 코일Gross실평중량 | SCO_DATA_DIC(D) |
| 68 | COIL_THY_WGT | NUMBER | Y |  | 이론중량 | SCO_DATA_DIC(D) |
| 69 | COIL_GROSS_THY_WGT | NUMBER | Y |  | 코일Gross이론중량 | SCO_DATA_DIC(D) |
| 70 | COIL_AW | NUMBER | Y |  | 코일안배중량 | SCO_DATA_DIC(D) |
| 71 | COIL_IN_DIA | NUMBER | Y |  | 内径 | SCO_DATA_DIC(D) |
| 72 | COIL_OUT_DIA | NUMBER | Y |  | Coil outer Diameter | SCO_DATA_DIC(D) |
| 73 | COIL_SHP_TP | VARCHAR2(1) | Y |  | Hcoil Shape Type | SCO_DATA_DIC(D) |
| 74 | PREV_COIL_SHP_TP | VARCHAR2(1) | Y |  | 전 재료외형 | SCO_DATA_DIC(D) |
| 75 | PL_WLD_CNT | NUMBER | Y |  | 산세용접수 | SCO_DATA_DIC(D) |
| 76 | PROD_WLD_CNT | NUMBER | Y |  | 제품용접수 | SCO_DATA_DIC(D) |
| 77 | PROD_CD | VARCHAR2(3) | Y |  | Product Code | SCO_DATA_DIC(D) |
| 78 | COIL_WIND_MD | VARCHAR2(1) | Y |  | 코일권취방향구분 | SCO_DATA_DIC(D) |
| 79 | COIL_SLV_USE_YN | VARCHAR2(1) | Y |  | 코일Sleeve사용여부 | SCO_DATA_DIC(D) |
| 80 | SURF_GRD | VARCHAR2(4) | Y |  | Slab Surface Grade | SCO_DATA_DIC(D) |
| 81 | SHP_GRD | VARCHAR2(1) | Y |  | HotCoil Shape Judgement Grade | SCO_DATA_DIC(D) |
| 82 | SIZE_GRD | VARCHAR2(1) | Y |  | HotCoil Size Judgement Grade | SCO_DATA_DIC(D) |
| 83 | UNT_WGT_GRD | VARCHAR2(1) | Y |  | HotCoil Weight Judgement Grade | SCO_DATA_DIC(D) |
| 84 | COIL_APR_JG | VARCHAR2(2) | Y |  | 코일외관판정등급 | SCO_DATA_DIC(D) |
| 85 | OP_JDG_GRD | VARCHAR2(2) | Y |  | Total Surface caused Code | SCO_DATA_DIC(D) |
| 86 | APR_JG_LOGC | VARCHAR2(2) | Y |  | 코일외관판정등급Logic | SCO_DATA_DIC(D) |
| 87 | COIL_APR_GRD_RSN | VARCHAR2(2) | Y |  | 外观改判原因 | SCO_DATA_DIC(D) |
| 88 | COIL_ARP_INS_DTM | VARCHAR2(14) | Y |  | 코일외관검사일시 | SCO_DATA_DIC(D) |
| 89 | COIL_ABNR_AC_WK_DTM | VARCHAR2(14) | Y |  | Release Date of Abnormal HotCoil | SCO_DATA_DIC(D) |
| 90 | PL_ST_YN | VARCHAR2(1) | Y |  | 산세ST여부 | SCO_DATA_DIC(D) |
| 91 | ANN_ST_YN | VARCHAR2(1) | Y |  | 소둔ST여부 | SCO_DATA_DIC(D) |
| 92 | COR_ST_YN | VARCHAR2(1) | Y |  | 정정ST여부 | SCO_DATA_DIC(D) |
| 93 | FINAL_JDG_CD | VARCHAR2(2) | Y |  | 제품종합판정등급 | SCO_DATA_DIC(D) |
| 94 | FINAL_JDG_CAU_CD | VARCHAR2(2) | Y |  | 제품종합등급원인코드 | SCO_DATA_DIC(D) |
| 95 | FINAL_JDG_DTM | VARCHAR2(14) | Y |  | 제품종합판정일자 | SCO_DATA_DIC(D) |
| 96 | COIL_MQL_JG | VARCHAR2(1) | Y |  | 코일재질판정등급 | SCO_DATA_DIC(D) |
| 97 | PROD_MQ_SYN_JG | VARCHAR2(1) | Y |  | 제품재질종합판정등급 | SCO_DATA_DIC(D) |
| 98 | PROD_SYN_JDG_SUMUP_DT | VARCHAR2(8) | Y |  | 제품종합판정계상일 | SCO_DATA_DIC(D) |
| 99 | PROD_SYN_JDG_DTM | VARCHAR2(14) | Y |  | 제품종합판정일시 | SCO_DATA_DIC(D) |
| 100 | SMP_NO | VARCHAR2(14) | Y |  | 시편번호 | SCO_DATA_DIC(D) |
| 101 | SMP_GTH_CNT | NUMBER | Y |  | Sample채취매수 | SCO_DATA_DIC(D) |
| 102 | SPEC_CD | VARCHAR2(50) | Y |  | Order Specification | SCO_DATA_DIC(D) |
| 103 | ORD_COAT_WGT_CD | VARCHAR2(7) | Y |  | Order Coating Weight Code | SCO_DATA_DIC(D) |
| 104 | CONV_UPPER_COAT_QTY | NUMBER | Y |  | 환산도금량전면 | SCO_DATA_DIC(D) |
| 105 | CONV_LOWER_COAT_QTY | NUMBER | Y |  | 환산도금량후면 | SCO_DATA_DIC(D) |
| 106 | PSTREAT_CD | VARCHAR2(2) | Y |  | 后处理方法代码 | SCO_DATA_DIC(D) |
| 107 | SURF_TREAT_CD | VARCHAR2(2) | Y |  | Surface Treatment | SCO_DATA_DIC(D) |
| 108 | COIL_ROU_CD | VARCHAR2(2) | Y |  | 코일조도코드 | SCO_DATA_DIC(D) |
| 109 | ORD_USAGE | VARCHAR2(4) | Y |  | Order Usage | SCO_DATA_DIC(D) |
| 110 | ORD_TP | VARCHAR2(2) | Y |  | Order Type | SCO_DATA_DIC(D) |
| 111 | OIL_MTH_CD | VARCHAR2(2) | Y |  | 涂油方法代码 | SCO_DATA_DIC(D) |
| 112 | CMP_QCERT_NO | VARCHAR2(11) | Y |  | 회사보증번호(재질기호) | SCO_DATA_DIC(D) |
| 113 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  |  | 空 |
| 114 | COAT_PROD_THK_TY | VARCHAR2(1) | Y |  |  | 空 |
| 115 | ORD_EDGE_TY | VARCHAR2(1) | Y |  | 订单Edge分类 | SCO_DATA_DIC(D) |
| 116 | SKINPASS_TY | VARCHAR2(1) | Y |  |  | 空 |
| 117 | DIFF_TEMP_GRD_CD | VARCHAR2(2) | Y |  |  | 空 |
| 118 | RVRS_COIL_YN | VARCHAR2(1) | Y |  | Coil Revering Yes or not | SCO_DATA_DIC(D) |
| 119 | PCKL_WELD_CD | VARCHAR2(3) | Y |  | Pickling Weldding Code | SCO_DATA_DIC(D) |
| 120 | PROD_WELD_CD | VARCHAR2(3) | Y |  | Products Weldding Code | SCO_DATA_DIC(D) |
| 121 | PACK_MTH_CD | VARCHAR2(5) | Y |  | Packing Method code | SCO_DATA_DIC(D) |
| 122 | COIL_PAK_EQUIP_NM | VARCHAR2(6) | Y |  | 코일포장설비명 | SCO_DATA_DIC(D) |
| 123 | COIL_PAK_STA_DTM | VARCHAR2(14) | Y |  | 코일포장개시일시 | SCO_DATA_DIC(D) |
| 124 | COIL_PAK_END_DTM | VARCHAR2(14) | Y |  | 코일포장완료일시 | SCO_DATA_DIC(D) |
| 125 | COIL_PAK_SUMUP_DTM | VARCHAR2(8) | Y |  | 코일포장계상일 | SCO_DATA_DIC(D) |
| 126 | COIL_PAK_SHIFT_CREW | VARCHAR2(2) | Y |  | 포장작업근조 | SCO_DATA_DIC(D) |
| 127 | COIL_PAK_EMP_ID | VARCHAR2(20) | Y |  | 포장작업자 사번 | SCO_DATA_DIC(D) |
| 128 | PROD_WHS_DTM | VARCHAR2(14) | Y |  | The inbound datetime | SCO_DATA_DIC(D) |
| 129 | PROD_WHS_SUMUP_DT | VARCHAR2(8) | Y |  | Date of Shipment Order | SCO_DATA_DIC(D) |
| 130 | PROD_DLV_REQ_TP | VARCHAR2(1) | Y |  | 제품출고유형 | SCO_DATA_DIC(D) |
| 131 | DLV_DTM | VARCHAR2(14) | Y |  | Date of Shipment | SCO_DATA_DIC(D) |
| 132 | DLV_SUMUP_DT | VARCHAR2(8) | Y |  | 출고계상일 | SCO_DATA_DIC(D) |
| 133 | DISP_DTM | VARCHAR2(14) | Y |  | Dispatch Time | SCO_DATA_DIC(D) |
| 134 | DISP_SUMUP_DT | VARCHAR2(8) | Y |  | 출하계상일 | SCO_DATA_DIC(D) |
| 135 | WHS_INF_TP | VARCHAR2(1) | Y |  | Warehouse Production or Information Flag | SCO_DATA_DIC(D) |
| 136 | RTN_INF_TP | VARCHAR2(1) | Y |  | Return Production or Information Flag | SCO_DATA_DIC(D) |
| 137 | PROD_RTN_DTM | VARCHAR2(14) | Y |  | 제품반납일시 | SCO_DATA_DIC(D) |
| 138 | RTN_SUMUP_DT | VARCHAR2(8) | Y |  | Date of Return | SCO_DATA_DIC(D) |
| 139 | RTN_REQ_REA_TP | VARCHAR2(2) | Y |  | Production Return Request Reason Code | SCO_DATA_DIC(D) |
| 140 | RTN_PRG_STS | VARCHAR2(1) | Y |  | 반납진행상태 | SCO_DATA_DIC(D) |
| 141 | RTN_REQ_EMP_NO | VARCHAR2(20) | Y |  | Production Return Requester | SCO_DATA_DIC(D) |
| 142 | RTN_CNL_PRS_ID | VARCHAR2(20) | Y |  | 반납조치자ID | SCO_DATA_DIC(D) |
| 143 | RTN_REQ_PROC_CD | VARCHAR2(3) | Y |  | 반납요구공정코드 | SCO_DATA_DIC(D) |
| 144 | RTN_CNL_DTM | VARCHAR2(14) | Y |  | 반납조치일시 | SCO_DATA_DIC(D) |
| 145 | DISP_HOLD_TP | VARCHAR2(1) | Y |  | 출하보류구분 | SCO_DATA_DIC(D) |
| 146 | DISP_HOLD_DTM | VARCHAR2(14) | Y |  | 출하보류일시 | SCO_DATA_DIC(D) |
| 147 | DISP_HOLD_REA | VARCHAR2(30) | Y |  | 출하보류사유 | SCO_DATA_DIC(D) |
| 148 | DISP_HOLD_UID | VARCHAR2(20) | Y |  | 출하보류자ID | SCO_DATA_DIC(D) |
| 149 | DISP_HOLD_CNL_UID | VARCHAR2(20) | Y |  | 출하보류해제자ID | SCO_DATA_DIC(D) |
| 150 | DISP_HOLD_CNL_DTM | VARCHAR2(14) | Y |  | 출하보류해제일시 | SCO_DATA_DIC(D) |
| 151 | PROD_LONG_STK_REA_TP | VARCHAR2(2) | Y |  | 제품장기재고사유구분 | SCO_DATA_DIC(D) |
| 152 | PROD_LONG_STK_REA_DTM | VARCHAR2(14) | Y |  | 제품장기재고등록일 | SCO_DATA_DIC(D) |
| 153 | PROD_LONG_STK_REA_ID | VARCHAR2(20) | Y |  | 제품장기재고등록자ID | SCO_DATA_DIC(D) |
| 154 | REA_INF_CRYN_TP | VARCHAR2(1) | Y |  | 실물정보반입구분 | SCO_DATA_DIC(D) |
| 155 | PROD_CRYN_REA_TP | VARCHAR2(3) | Y |  | 제품반입사유구분 | SCO_DATA_DIC(D) |
| 156 | PROD_CRYN_DTM | VARCHAR2(14) | Y |  | 제품반입일시 | SCO_DATA_DIC(D) |
| 157 | CRYN_SUMUP_DT | VARCHAR2(8) | Y |  | 반입계상일 | SCO_DATA_DIC(D) |
| 158 | TST_PROD_TP | VARCHAR2(1) | Y |  | Flag of TEST HotCoil | SCO_DATA_DIC(D) |
| 159 | PCOIL_NO | VARCHAR2(14) | Y |  | Flag of SPM PDI(S:Skin,D:Dividing,R:Recoiling) | SCO_DATA_DIC(D) |
| 160 | SEMI_PROD_ITEM_CD | VARCHAR2(30) | Y |  | 코일 반제품 ERP ITEM | SCO_DATA_DIC(D) |
| 161 | SALES_PROD_ITEM_CD | VARCHAR2(30) | Y |  | 코일 제품 ERP ITEM | SCO_DATA_DIC(D) |
| 162 | DMD_NXT_PROC_CD | VARCHAR2(60) | Y |  | Demand next proceed code | SCO_DATA_DIC(D) |
| 163 | MRG_TY | VARCHAR2(2) | Y |  | Merge Type | SCO_DATA_DIC(D) |
| 164 | MRG_COIL_NO1 | VARCHAR2(14) | Y |  | Merged Coil No1 | SCO_DATA_DIC(D) |
| 165 | MRG_COIL_WGT1 | NUMBER | Y |  | Merged Coil Weight1 | SCO_DATA_DIC(D) |
| 166 | MRG_COIL_LTH1 | NUMBER | Y |  | Merged Coil Length1 | SCO_DATA_DIC(D) |
| 167 | MRG_COIL_NO2 | VARCHAR2(14) | Y |  | Merged Coil No2 | SCO_DATA_DIC(D) |
| 168 | MRG_COIL_WGT2 | NUMBER | Y |  | Merged Coil Weight2 | SCO_DATA_DIC(D) |
| 169 | MRG_COIL_LTH2 | NUMBER | Y |  | Merged Coil Length2 | SCO_DATA_DIC(D) |
| 170 | MRG_COIL_NO3 | VARCHAR2(14) | Y |  | Merged Coil No3 | SCO_DATA_DIC(D) |
| 171 | MRG_COIL_WGT3 | NUMBER | Y |  | Merged Coil Weight3 | SCO_DATA_DIC(D) |
| 172 | MRG_COIL_LTH3 | NUMBER | Y |  | Merged Coil Length3 | SCO_DATA_DIC(D) |
| 173 | HEAT_NO | VARCHAR2(9) | Y |  | Heat No | SCO_DATA_DIC(D) |
| 174 | COIL_STS_ID | VARCHAR2(1) | Y |  | Record상태구분 | SCO_DATA_DIC(D) |
| 175 | PDI_RCV_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 176 | WGT_RCV_YN | VARCHAR2(1) | Y |  | DMS SEND WEIGHT TO MES Y/N | SCO_DATA_DIC(D) |
| 177 | HCOIL_JDG_YN | VARCHAR2(1) | Y |  |  | 空 |
| 178 | STD_STLGRD | VARCHAR2(20) | Y |  | 牌号 | SCO_DATA_DIC(D) |
| 179 | REPROC_CNT | NUMBER | Y |  | Re-process Count | SCO_DATA_DIC(D) |
| 180 | BEF_PROC_CD | VARCHAR2(3) | Y |  | Before Process Code | SCO_DATA_DIC(D) |
| 181 | COOL_END_YN | VARCHAR2(1) | Y |  | Cooling End Type | SCO_DATA_DIC(D) |
| 182 | COOL_END_DTM | VARCHAR2(14) | Y |  | HCR Cooling End Date | SCO_DATA_DIC(D) |
| 183 | WK_STA_DTM | VARCHAR2(14) | Y |  | The SFTCrew based on the SPM Work Day | SCO_DATA_DIC(D) |
| 184 | WK_END_DTM | VARCHAR2(14) | Y |  | Flag of SPM Work(1:Normal,2:Abnormal) | SCO_DATA_DIC(D) |
| 185 | ALLOC_DTM | VARCHAR2(14) | Y |  | Allocation Datetime | SCO_DATA_DIC(D) |
| 186 | ALLOC_TY | VARCHAR2(1) | Y |  | Allocation Type | SCO_DATA_DIC(D) |
| 187 | ERP_IF_DTM | VARCHAR2(14) | Y |  | Send ERP Datetime | SCO_DATA_DIC(D) |
| 188 | NATL_SPEC_NO | VARCHAR2(40) | Y |  |  | 空 |
| 189 | NATL_SPEC_YEAR | VARCHAR2(4) | Y |  | 국가표준년도 | SCO_DATA_DIC(D) |
| 190 | HOLD_FG | VARCHAR2(1) | Y |  |  | 空 |
| 191 | MRG_COIL_NO4 | VARCHAR2(14) | Y |  |  | 空 |
| 192 | MRG_COIL_WGT4 | NUMBER | Y |  |  | 空 |
| 193 | MRG_COIL_LTH4 | NUMBER | Y |  |  | 空 |
| 194 | REPRO_FLAG | VARCHAR2(1) | Y |  | reproduction coil flag | SCO_DATA_DIC(L) |
| 195 | WK_SHF_GRP_CD | VARCHAR2(2) | Y |  | 班次班组 | SCO_DATA_DIC(D) |
| 196 | SUMUP_DT | VARCHAR2(8) | Y |  | Operation Sumup date | SCO_DATA_DIC(D) |
| 197 | HOLD_YN | VARCHAR2(1) | Y |  | Hold Yes/No | SCO_DATA_DIC(D) |
| 198 | PACK_MTRL_WGT | NUMBER | Y |  |  | 空 |
| 199 | SHF_GRP_CD | VARCHAR2(2) | Y |  | 班次班组 | SCO_DATA_DIC(D) |
| 200 | DUMMY_COIL_YN | VARCHAR2(1) | Y |  | 过渡卷标识 | SCO_DATA_DIC(L) |
| 201 | COIL_WTH_L2 | NUMBER | Y |  | Coil Width from L2 | SCO_DATA_DIC(D) |
| 202 | COIL_THK_L2 | NUMBER | Y |  | Coil Thickness from L2 | SCO_DATA_DIC(D) |
| 203 | UP_USER_ID | VARCHAR2(20) | Y |  |  | 空 |
| 204 | UP_DTIME | VARCHAR2(14) | Y |  |  | 空 |
| 205 | UP_SHF_GRP | VARCHAR2(2) | Y |  |  | 空 |
| 206 | COIL_FLAG | VARCHAR2(1) | Y |  |  | 空 |
| 207 | DEL_USE_ID | VARCHAR2(20) | Y |  |  | 空 |
| 208 | DEL_DTIME | VARCHAR2(14) | Y |  |  | 空 |
| 209 | DEL_SHF_GRP | VARCHAR2(2) | Y |  |  | 空 |
| 210 | SEND_ERP_YN | VARCHAR2(1) | Y |  | Send ERP Yes/No | SCO_DATA_DIC(D) |
| 211 | PROD_CD_FL | VARCHAR2(1) | Y |  |  | 空 |
| 212 | LOT_NO | VARCHAR2(14) | Y |  | LOT NO(BATCH NO) | SCO_DATA_DIC(D) |
| 213 | TAIL_COIL_YN | VARCHAR2(1) | Y |  |  | 空 |
| 214 | RCL_PLAN_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 215 | PAK_REMARK_CD | VARCHAR2(200) | Y |  |  | 空 |
| 216 | PAK_REMARK_NM | VARCHAR2(20) | Y |  |  | 空 |
| 217 | COIL_APR_NM | VARCHAR2(20) | Y |  |  | 空 |
| 218 | SMP_FL | VARCHAR2(1) | Y |  |  | 空 |
| 219 | RCL_PLAN_ID | VARCHAR2(20) | Y |  |  | 空 |

### SQM_SMP_TRK

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=134｜被读 68 过程 / 被写 33 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：18575　**主键**：SMP_NO、SMP_LTH_LOC、TEST_CNT　**语义覆盖**：50/50

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | SMP_NO | VARCHAR2(14) | N | ✓ | 试样编号 | DB注释(中文) |
| 9 | SMP_LTH_LOC | VARCHAR2(1) | N | ✓ | 试样采取位置 | DB注释(中文) |
| 10 | TEST_CNT | NUMBER | N | ✓ | 试验回数 | DB注释(中文) |
| 11 | SMP_PROG_CD | VARCHAR2(1) | Y |  | 试样进度代码 | DB注释(中文) |
| 12 | SMP_PROG_DTM | VARCHAR2(14) | Y |  | 试样进度时间 | DB注释(中文) |
| 13 | SMP_LOTFORM_DTM | VARCHAR2(14) | Y |  | 编制组批试样时间 | DB注释(中文) |
| 14 | SMP_GTH_INST_FST_DTM | VARCHAR2(14) | Y |  | 试样采取最初指示时间 | DB注释(中文) |
| 15 | SMP_UNGTH_CAU_OCR_DTM | VARCHAR2(14) | Y |  | 试样未采取原因发生时间 | DB注释(中文) |
| 16 | SMP_GTH_DTM | VARCHAR2(14) | Y |  | 试样采取时间 | DB注释(中文) |
| 17 | SMP_GTH_SFT | VARCHAR2(2) | Y |  | 试样采取班组 | DB注释(中文) |
| 18 | SMP_RCPT_DTM | VARCHAR2(14) | Y |  | 试样入库时间 | DB注释(中文) |
| 19 | SMP_RCPT_SFT | VARCHAR2(2) | Y |  | 试样入库班组 | DB注释(中文) |
| 20 | TEST_INST_DTM | VARCHAR2(14) | Y |  | 试验指示时间 | DB注释(中文) |
| 21 | MECH_TEST_END_DTM | VARCHAR2(14) | Y |  | 试验结束时间 | DB注释(中文) |
| 22 | JDG_FINISH_DTM | VARCHAR2(14) | Y |  | 判定结束时间 | DB注释(中文) |
| 23 | SMP_GTH_EMP_ID | VARCHAR2(20) | Y |  | 试样采取人社编 | DB注释(中文) |
| 24 | SMP_DLVRY_EMP_ID | VARCHAR2(20) | Y |  | 试样引渡人社编 | DB注释(中文) |
| 25 | SMP_RCPT_EMP_ID | VARCHAR2(20) | Y |  | 试样入库人社编 | DB注释(中文) |
| 26 | SMP_UNGTH_CAU_TY | VARCHAR2(1) | Y |  | 试样未采取原因分类 | DB注释(中文) |
| 27 | RESMP_GTH_REQ_DTM | VARCHAR2(14) | Y |  | 再采样要求时间 | DB注释(中文) |
| 28 | PROD_JDG_PROD_CD | VARCHAR2(1) | Y |  | 产品判定用产品分类 | DB注释(中文) |
| 29 | INSP_AGENCY_CD | VARCHAR2(3) | Y |  | 检查机构代码 | DB注释(中文) |
| 30 | PROD_CD | VARCHAR2(3) | Y |  | 品名代码 | DB注释(中文) |
| 31 | PROC_CD | VARCHAR2(3) | Y |  | 工序代码 | DB注释(中文) |
| 32 | SMP_GTH_INST_MTRL_NO | VARCHAR2(20) | Y |  | 试样采取指示材料编号 | DB注释(中文) |
| 33 | HEAT_NO | VARCHAR2(10) | Y |  | Heat编号 | DB注释(中文) |
| 34 | SPEC_CD | VARCHAR2(50) | Y |  | 国家标准牌号 | DB注释(中文) |
| 35 | RETEST_INST_YN | VARCHAR2(1) | Y |  | 是否指示再实验 | DB注释(中文) |
| 36 | RETEST_EXEC_YN | VARCHAR2(1) | Y |  | 是否实施再实验 | DB注释(中文) |
| 37 | RESMP_GTH_CAU_TY | VARCHAR2(1) | Y |  | 再采样原因分类 | DB注释(中文) |
| 38 | ORD_NO | VARCHAR2(10) | Y |  | 订单编号 | DB注释(中文) |
| 39 | ORD_LN | VARCHAR2(3) | Y |  | 订单行号 | DB注释(中文) |
| 40 | RESMP_GTH_REQ_EMP_ID | VARCHAR2(20) | Y |  | 再采样要求人社编 | DB注释(中文) |
| 41 | LOT_NO | VARCHAR2(14) | Y |  | 批号 | DB注释(中文) |
| 42 | TEST_INST_EMP_ID | VARCHAR2(20) | Y |  | 试样指示人员 | DB注释(中文) |
| 43 | MECH_RETEST_TY | VARCHAR2(1000) | Y |  | 性能复验原因分类 | DB注释(中文) |
| 44 | SMP_RCV_DTM | VARCHAR2(14) | Y |  | 试样lims接收时间 | DB注释(中文) |
| 45 | SMP_RCV_EMP_ID | VARCHAR2(20) | Y |  | 试样LIMS接收人员 | DB注释(中文) |
| 46 | OFFLINE_FLAG | VARCHAR2(1) | Y |  | 是否离线取样 | DB注释(中文) |
| 47 | INSP_MTC_NO1 | VARCHAR2(50) | Y |  | 认证证书号 | DB注释(中文) |
| 48 | INSP_MTC_NO2 | VARCHAR2(50) | Y |  | 检验证书号 | DB注释(中文) |
| 49 | INSP_NM | VARCHAR2(50) | Y |  | 验船师姓名 | DB注释(中文) |
| 50 | BEF_SMP_GTH_INST_MTRL_NO | VARCHAR2(20) | Y |  | 试样采取指示材料编号 | DB注释(中文) |

### SQM_SMP_LOTFORM_RSLT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=133｜被读 83 过程 / 被写 25 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：202133　**主键**：INST_MTRL_NO　**语义覆盖**：51/51

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | INST_MTRL_NO | VARCHAR2(20) | N | ✓ | 指示材料编号 | DB注释(中文) |
| 9 | SMP_NO | VARCHAR2(14) | Y |  | 试样编号 | DB注释(中文) |
| 10 | PROD_GRP | VARCHAR2(2) | Y |  | 品种代码 | DB注释(中文) |
| 11 | SMP_TP | VARCHAR2(1) | Y |  | 试样分类 | DB注释(中文) |
| 12 | SMP_LOT_SEQ | NUMBER | Y |  | 试样Lot序列号 | DB注释(中文) |
| 13 | PROD_JDG_PROD_CD | VARCHAR2(1) | Y |  | 产品判定用产品分类 | DB注释(中文) |
| 14 | REP_YN | VARCHAR2(1) | Y |  | 是否代表 | DB注释(中文) |
| 15 | ORD_NO | VARCHAR2(10) | Y |  | 订单编号 | DB注释(中文) |
| 16 | ORD_LN | VARCHAR2(3) | Y |  | 订单行号 | DB注释(中文) |
| 17 | SPEC_CD | VARCHAR2(50) | Y |  | 国家标准牌号 | DB注释(中文) |
| 18 | CUST_QCERT_NO | VARCHAR2(15) | Y |  | 客户保证编号 | DB注释(中文) |
| 19 | PLAN_HEAT_NO | VARCHAR2(10) | Y |  | 预期Heat编号 | DB注释(中文) |
| 20 | HEAT_NO | VARCHAR2(10) | Y |  | Heat编号 | DB注释(中文) |
| 21 | PLAN_SLAB_NO | VARCHAR2(13) | Y |  | 预期Slab编号 | DB注释(中文) |
| 22 | SLAB_NO | VARCHAR2(13) | Y |  | Slab编号 | DB注释(中文) |
| 23 | MTRL_NO | VARCHAR2(20) | Y |  | 材料编号 | DB注释(中文) |
| 24 | SMP_PROG_CD | VARCHAR2(1) | Y |  | 试样进度代码 | DB注释(中文) |
| 25 | INSP_AGENCY_CD | VARCHAR2(3) | Y |  | 检查机构代码 | DB注释(中文) |
| 26 | CMP_QCERT_NO | VARCHAR2(11) | Y |  | 公司保证编号(材质记号) | DB注释(中文) |
| 27 | MATR_THK | NUMBER | Y |  | 基材厚度 | DB注释(中文) |
| 28 | ORD_THK | NUMBER | Y |  | 订单厚度 | DB注释(中文) |
| 29 | SMP_CND | VARCHAR2(2) | Y |  | 物性测试取样条件 | DB注释(中文) |
| 30 | SMP_LTH_LOC | VARCHAR2(1) | Y |  | 物性测试长度方向取样位置 | DB注释(中文) |
| 31 | SMP_WTH_LOC | VARCHAR2(1) | Y |  | 物性测试宽度方向取样位置 | DB注释(中文) |
| 32 | SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 物性测试取样试样号数 | DB注释(中文) |
| 33 | SPCMN_CNT | NUMBER | Y |  | 试样数量 | DB注释(中文) |
| 34 | SMP_LOT_INFO_GRP | VARCHAR2(60) | Y |  | 编制组批试样信息捆绑 | DB注释(中文) |
| 35 | SMP_LOT_THK_GRP_CD | VARCHAR2(2) | Y |  | 试样Lot厚度组代码 | DB注释(中文) |
| 36 | TEST_ACC_MAX_WGT | NUMBER | Y |  | 试验累计最大重量 | DB注释(中文) |
| 37 | TEST_ACC_WGT | NUMBER | Y |  | 试验累计重量 | DB注释(中文) |
| 38 | LOT_WGT | NUMBER | Y |  | LOT重量(材料重量) | DB注释(中文) |
| 39 | MECH_TEST_END_YN | VARCHAR2(1) | Y |  | 材质试验是否结束 | DB注释(中文) |
| 40 | ACC_SMP_EXIST_YN | VARCHAR2(1) | Y |  | 累计试样是否存在 | DB注释(中文) |
| 41 | LOT_NO | VARCHAR2(14) | Y |  | LOT NO(BATCH NO) | DB注释(非中文) |
| 42 | TEST_ACC_COIL_CNT | VARCHAR2(2) | Y |  | Test ACC Coil Count | DB注释(非中文) |
| 43 | SCH_NO | VARCHAR2(10) | Y |  | Schedule No | DB注释(非中文) |
| 44 | PROD_CD | VARCHAR2(3) | Y |  | Order  Prod  Code | DB注释(非中文) |
| 45 | GB_FLAG | VARCHAR2(1) | Y |  | 国标检验标记 | DB注释(中文) |
| 46 | FAC_CD | VARCHAR2(1) | Y |  | 工厂代码 | DB注释(中文) |
| 47 | ALONE_FLAG | VARCHAR2(1) | Y |  | 单个组批标记 | DB注释(中文) |
| 48 | BATCH_DTM | VARCHAR2(14) | Y |  | 组批时间 | DB注释(中文) |
| 49 | HTM_YN | VARCHAR2(1) | Y |  | 热处理与否 | DB注释(中文) |
| 50 | HTM_MTH_CD | VARCHAR2(1) | Y |  | 交货状态 | DB注释(中文) |
| 51 | BEF_MTRL_NO | VARCHAR2(20) | Y |  | 材料编号 | DB注释(中文) |

### SHR_HCOIL_MASTER

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=118｜被读 76 过程 / 被写 21 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：1236　**主键**：COIL_NO　**语义覆盖**：173/203

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | SCO_DATA_DIC(D) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | SCO_DATA_DIC(D) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | SCO_DATA_DIC(D) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated UserID | SCO_DATA_DIC(D) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated ObjectID | SCO_DATA_DIC(D) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Date Time | SCO_DATA_DIC(D) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | SCO_DATA_DIC(D) |
| 8 | COIL_NO | VARCHAR2(14) | N | ✓ |  | 空 |
| 9 | RCD_STS_ID | VARCHAR2(1) | Y |  | Record Status Flag | SCO_DATA_DIC(D) |
| 10 | PREV_COIL_NO | VARCHAR2(14) | Y |  | 전코일번호 | SCO_DATA_DIC(D) |
| 11 | RCD_STS_CHG_DTM | VARCHAR2(14) | Y |  | Record Status Changed Timestamp | SCO_DATA_DIC(D) |
| 12 | PROC_CD | VARCHAR2(3) | Y |  | Process Code | SCO_DATA_DIC(D) |
| 13 | PROG_CD | VARCHAR2(4) | Y |  | Progress Code | SCO_DATA_DIC(D) |
| 14 | PREV_PROG_CD | VARCHAR2(4) | Y |  | 전 CR진도코드 | SCO_DATA_DIC(D) |
| 15 | HCR_FL | VARCHAR2(1) | Y |  | Classification of Hot Coil Work Pattern | SCO_DATA_DIC(D) |
| 16 | SLAB_NO | VARCHAR2(12) | Y |  | Slab No | SCO_DATA_DIC(D) |
| 17 | SCH_NO | VARCHAR2(10) | Y |  | Schedule Number | SCO_DATA_DIC(D) |
| 18 | COIL_IN_DIA | NUMBER | Y |  | 内径 | SCO_DATA_DIC(D) |
| 19 | COIL_OUT_DIA | NUMBER | Y |  | Coil outer Diameter | SCO_DATA_DIC(D) |
| 20 | TNST_EL_ACTL_RLS_AMT | NUMBER | Y |  | EL Measuring Actual Value | SCO_DATA_DIC(D) |
| 21 | STR_LOC_CD | VARCHAR2(9) | Y |  |  | 空 |
| 22 | STR_LOC_WK_DTM | VARCHAR2(14) | Y |  | Current Location Updated Timestamp | SCO_DATA_DIC(D) |
| 23 | MULTI_ORD_TP | VARCHAR2(1) | Y |  | Represntive Order Type | SCO_DATA_DIC(D) |
| 24 | ORD_NO | VARCHAR2(10) | Y |  | Order No | SCO_DATA_DIC(D) |
| 25 | ORD_LN | VARCHAR2(3) | Y |  |  | 空 |
| 26 | PREV_ORD_NO | VARCHAR2(10) | Y |  | Previous Order No | SCO_DATA_DIC(D) |
| 27 | PREV_ORD_LN | VARCHAR2(3) | Y |  | 전주문행번 | SCO_DATA_DIC(D) |
| 28 | HCOIL_ORD_WGT | NUMBER | Y |  | 복수수요가 중량1 | SCO_DATA_DIC(D) |
| 29 | HCOIL_ORD_LTH | NUMBER | Y |  | Multi order Length | SCO_DATA_DIC(D) |
| 30 | SUB_ORD_NO1 | VARCHAR2(10) | Y |  | Sub Order Head Number1 | SCO_DATA_DIC(D) |
| 31 | SUB_ORD_LN1 | VARCHAR2(3) | Y |  | Sub Order Line Number1 | SCO_DATA_DIC(D) |
| 32 | HCOIL_ORD_WGT1 | NUMBER | Y |  | 복수수요가 중량2 | SCO_DATA_DIC(D) |
| 33 | HCOIL_ORD_LTH1 | NUMBER | Y |  | Multi order2 Length | SCO_DATA_DIC(D) |
| 34 | SUB_ORD_NO2 | VARCHAR2(10) | Y |  | Sub Order Head Number2 | SCO_DATA_DIC(D) |
| 35 | SUB_ORD_LN2 | VARCHAR2(3) | Y |  | Sub Order Line Number2 | SCO_DATA_DIC(D) |
| 36 | HCOIL_ORD_WGT2 | NUMBER | Y |  | 복수수요가 중량3 | SCO_DATA_DIC(D) |
| 37 | HCOIL_ORD_LTH2 | NUMBER | Y |  | Multi order2 Length | SCO_DATA_DIC(D) |
| 38 | SPEC_CD | VARCHAR2(50) | Y |  | Order Specification | SCO_DATA_DIC(D) |
| 39 | CMP_QCERT_NO | VARCHAR2(11) | Y |  | 회사보증번호(재질기호) | SCO_DATA_DIC(D) |
| 40 | HOT_MFC_STD_NO | VARCHAR2(11) | Y |  | 热间制造标准编号 | SCO_DATA_DIC(D) |
| 41 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  |  | 空 |
| 42 | ORD_TY | VARCHAR2(2) | Y |  | Order Type (normal order, inventory order, plan order, test order, etc,) | SCO_DATA_DIC(D) |
| 43 | PROD_CD | VARCHAR2(3) | Y |  | Product Code | SCO_DATA_DIC(D) |
| 44 | ORD_USAGE | VARCHAR2(4) | Y |  | Order Usage | SCO_DATA_DIC(D) |
| 45 | ORD_THK | NUMBER | Y |  | Order Thickness | SCO_DATA_DIC(L) |
| 46 | ORD_WTH | NUMBER | Y |  | Order Width | SCO_DATA_DIC(D) |
| 47 | ORD_LTH | NUMBER | Y |  | Order Length | SCO_DATA_DIC(D) |
| 48 | COIL_THK | NUMBER | Y |  |  | 空 |
| 49 | COIL_WTH | NUMBER | Y |  |  | 空 |
| 50 | COIL_LTH | NUMBER | Y |  | Coil Length | SCO_DATA_DIC(D) |
| 51 | COIL_NET_WGT | NUMBER | Y |  | The Coil Weight after Recolling | SCO_DATA_DIC(D) |
| 52 | COIL_GROSS_NET_WGT | NUMBER | Y |  | 코일Gross실평중량 | SCO_DATA_DIC(D) |
| 53 | COIL_THY_WGT | NUMBER | Y |  | 이론중량 | SCO_DATA_DIC(D) |
| 54 | COIL_GROSS_THY_WGT | NUMBER | Y |  | 코일Gross이론중량 | SCO_DATA_DIC(D) |
| 55 | COIL_AW | NUMBER | Y |  | 코일안배중량 | SCO_DATA_DIC(D) |
| 56 | PROD_SUMUP_DT | VARCHAR2(8) | Y |  | Limited date of Product | SCO_DATA_DIC(D) |
| 57 | RLG_SUMUP_DT | VARCHAR2(8) | Y |  | Limited date of Rolling Works | SCO_DATA_DIC(D) |
| 58 | SPM_WK_SUMUP_DT | VARCHAR2(8) | Y |  | Limited date of SPM Works | SCO_DATA_DIC(D) |
| 59 | ORD_DELV_SUMUP_DT | VARCHAR2(8) | Y |  | Delivery Date | SCO_DATA_DIC(D) |
| 60 | FINAL_CUST_CD | VARCHAR2(9) | Y |  | Final Customer Code | SCO_DATA_DIC(D) |
| 61 | FINAL_CUST_NM | VARCHAR2(100) | Y |  | Final Customer Name | SCO_DATA_DIC(D) |
| 62 | DELV_COND_CD | VARCHAR2(2) | Y |  | Delevery Condition Code | SCO_DATA_DIC(D) |
| 63 | TS_GRD | VARCHAR2(4) | Y |  | TS-Grade | SCO_DATA_DIC(D) |
| 64 | TLSCP_UPR_LMT_VAL | NUMBER | Y |  | Telescope Upper Value | SCO_DATA_DIC(D) |
| 65 | ALLOT_DTM | VARCHAR2(14) | Y |  | Date of the Customer Changed | SCO_DATA_DIC(D) |
| 66 | ALLOT_MTH_TP | VARCHAR2(2) | Y |  | Flag of the Customer Changed | SCO_DATA_DIC(D) |
| 67 | ORD_FL | VARCHAR2(1) | Y |  | APO/NAPO Type | SCO_DATA_DIC(D) |
| 68 | PREV_ORD_FL | VARCHAR2(1) | Y |  | 전 주여구분 | SCO_DATA_DIC(D) |
| 69 | ORD_FL_CD | VARCHAR2(2) | Y |  | Current WO Caused Code | SCO_DATA_DIC(D) |
| 70 | ORD_FL_DTM | VARCHAR2(14) | Y |  | Updated Timestamp for Current NOK Caused Code | SCO_DATA_DIC(D) |
| 71 | SMP_NO | VARCHAR2(14) | Y |  | 시편번호 | SCO_DATA_DIC(D) |
| 72 | SMP_SMPLNG_CD | VARCHAR2(1) | Y |  | Sampling Order Flag Code | SCO_DATA_DIC(D) |
| 73 | SMP_SMPLNG_INST_TP | VARCHAR2(1) | Y |  | Flag of Sampling Cut PDI | SCO_DATA_DIC(D) |
| 74 | SMP_SMPLNG_FG | VARCHAR2(1) | Y |  | Ok or Nok of Sampling Cut | SCO_DATA_DIC(D) |
| 75 | COIL_TST_EXCTN_FG | VARCHAR2(1) | Y |  | Retest or not | SCO_DATA_DIC(D) |
| 76 | SLCAM_AC_TP | VARCHAR2(1) | Y |  | Action Flag of Abnormal case in Sampling Lot | SCO_DATA_DIC(D) |
| 77 | SLCAM_AC_DTM | VARCHAR2(14) | Y |  | Abnormal Sampling Updated Timestamp | SCO_DATA_DIC(D) |
| 78 | PLN_PASS_PROC | VARCHAR2(60) | Y |  | Planned Process Line | SCO_DATA_DIC(D) |
| 79 | REM_PROC_CD | VARCHAR2(60) | Y |  | Remain Process Line | SCO_DATA_DIC(D) |
| 80 | NXT_PROC_CD | VARCHAR2(4) | Y |  | Next PROC_CD | SCO_DATA_DIC(D) |
| 81 | PASS_PROC_CD | VARCHAR2(60) | Y |  | Work Process Line | SCO_DATA_DIC(D) |
| 82 | COIL_SHP_TP | VARCHAR2(1) | Y |  | Hcoil Shape Type | SCO_DATA_DIC(D) |
| 83 | PREV_COIL_SHP_TP | VARCHAR2(1) | Y |  | 전 재료외형 | SCO_DATA_DIC(D) |
| 84 | APR_SYN_GRD_DTM | VARCHAR2(14) | Y |  | TimeStamp of HotCoil Total Surface Judgement | SCO_DATA_DIC(D) |
| 85 | COIL_APR_JG | VARCHAR2(2) | Y |  | 코일외관판정등급 | SCO_DATA_DIC(D) |
| 86 | COIL_APR_JG_CAU_CD | VARCHAR2(2) | Y |  | Surface Grade Reason Code | SCO_DATA_DIC(D) |
| 87 | UNT_WGT_GRD | VARCHAR2(2) | Y |  | HotCoil Weight Judgement Grade | SCO_DATA_DIC(D) |
| 88 | SIZE_GRD | VARCHAR2(2) | Y |  | HotCoil Size Judgement Grade | SCO_DATA_DIC(D) |
| 89 | SURF_GRD | VARCHAR2(2) | Y |  | Slab Surface Grade | SCO_DATA_DIC(D) |
| 90 | SHP_GRD | VARCHAR2(2) | Y |  | HotCoil Shape Judgement Grade | SCO_DATA_DIC(D) |
| 91 | OP_JDG_GRD | VARCHAR2(2) | Y |  | Total Surface caused Code | SCO_DATA_DIC(D) |
| 92 | ORD_UNIT_WGT_EXCS_FG | VARCHAR2(2) | Y |  | Over Flag of Customer Order Weight Tolerance | SCO_DATA_DIC(D) |
| 93 | COIL_INSPT_REQ_FG | VARCHAR2(2) | Y |  | Flag of Reinspection request | SCO_DATA_DIC(D) |
| 94 | WK_INST_HLD_FG | VARCHAR2(2) | Y |  | The Hold Flag of the work order | SCO_DATA_DIC(D) |
| 95 | WK_INST_ERR_FCTR_CD | VARCHAR2(2) | Y |  | Error Code of Work Order | SCO_DATA_DIC(D) |
| 96 | COIL_CLNG_NXT_CLNG_MTH | VARCHAR2(2) | Y |  | Cooling Type After Rolling Work | SCO_DATA_DIC(D) |
| 97 | COIL_FRC_CLNG_STAT_DTM | VARCHAR2(14) | Y |  | Start Date of Unplanned Cooling | SCO_DATA_DIC(D) |
| 98 | COIL_FRC_CLNG_CMPLT_DTM | VARCHAR2(14) | Y |  | End Date of Unplanned Cooling | SCO_DATA_DIC(D) |
| 99 | COOL_END_YN | VARCHAR2(1) | Y |  | Cooling End Type | SCO_DATA_DIC(D) |
| 100 | COOL_END_DTM | VARCHAR2(14) | Y |  | HCR Cooling End Date | SCO_DATA_DIC(D) |
| 101 | AIR_CLNG_HOUR | NUMBER | Y |  | Total Hours of Air Cooling | SCO_DATA_DIC(D) |
| 102 | HLD_RQST_CD | VARCHAR2(2) | Y |  | The code requested the hold | SCO_DATA_DIC(D) |
| 103 | PCKG_MTH_CD | VARCHAR2(5) | Y |  | Packing Method Code | SCO_DATA_DIC(D) |
| 104 | RJT_NO_FG | VARCHAR2(1) | Y |  | Reject Flag | SCO_DATA_DIC(D) |
| 105 | RJT_NO_DTM | VARCHAR2(14) | Y |  | Date of Reject | SCO_DATA_DIC(D) |
| 106 | COIL_ABNR_AC_WK_DTM | VARCHAR2(14) | Y |  | Release Date of Abnormal HotCoil | SCO_DATA_DIC(D) |
| 107 | ABNR_COIL_ALLOT_DSMT_TP | VARCHAR2(2) | Y |  | Customer Changed In Abnormal HotCoil | SCO_DATA_DIC(D) |
| 108 | PROD_WH_RCPT_DTM | VARCHAR2(14) | Y |  | 产品仓库入库时间 | SCO_DATA_DIC(D) |
| 109 | FNL_RCPT_FG | VARCHAR2(1) | Y |  | The Final Inbound Flag in WareHouse | SCO_DATA_DIC(D) |
| 110 | FCE_CHARGE_DTM | VARCHAR2(14) | Y |  | Furnace Charge Time | SCO_DATA_DIC(D) |
| 111 | FCE_DISCH_DTM | VARCHAR2(14) | Y |  | Furnace Discharge Time | SCO_DATA_DIC(D) |
| 112 | RLG_STA_DTM | VARCHAR2(14) | Y |  | Rolling Start Date | SCO_DATA_DIC(D) |
| 113 | RLG_END_DTM | VARCHAR2(14) | Y |  | Rolling End Date | SCO_DATA_DIC(D) |
| 114 | RLG_WK_SUMUP_DT | VARCHAR2(8) | Y |  | Work Day based on Steel works | SCO_DATA_DIC(D) |
| 115 | SPM_WK_STA_DTM | VARCHAR2(14) | Y |  | The SPM Work start date | SCO_DATA_DIC(D) |
| 116 | SPM_WK_END_DTM | VARCHAR2(14) | Y |  | The SPM Work finish date | SCO_DATA_DIC(D) |
| 117 | PROD_WHS_DTM | VARCHAR2(14) | Y |  | The inbound datetime | SCO_DATA_DIC(D) |
| 118 | PROD_WHS_SUMUP_DT | VARCHAR2(8) | Y |  | Date of Shipment Order | SCO_DATA_DIC(D) |
| 119 | WHS_INF_TP | VARCHAR2(1) | Y |  | Warehouse Production or Information Flag | SCO_DATA_DIC(D) |
| 120 | RTN_INF_TP | VARCHAR2(1) | Y |  | Return Production or Information Flag | SCO_DATA_DIC(D) |
| 121 | DLV_DTM | VARCHAR2(14) | Y |  | Date of Shipment | SCO_DATA_DIC(D) |
| 122 | RTN_DTM | VARCHAR2(14) | Y |  | Return Date Time | SCO_DATA_DIC(D) |
| 123 | RTN_SUMUP_DT | VARCHAR2(8) | Y |  | Date of Return | SCO_DATA_DIC(D) |
| 124 | RTN_REQ_REA_CD | VARCHAR2(2) | Y |  |  | 空 |
| 125 | RTN_REQ_EMP_NO | VARCHAR2(20) | Y |  | Production Return Requester | SCO_DATA_DIC(D) |
| 126 | RTN_CNL_DTM | VARCHAR2(14) | Y |  | 반납조치일시 | SCO_DATA_DIC(D) |
| 127 | RTN_WK_SFT_TEAM | VARCHAR2(2) | Y |  | Production Return Shift and Crew | SCO_DATA_DIC(D) |
| 128 | RTN_JD_EMP_NO | VARCHAR2(20) | Y |  | Return Production Judgement Employee | SCO_DATA_DIC(D) |
| 129 | PAR_COIL_NO | VARCHAR2(14) | Y |  | Parent Coil No | SCO_DATA_DIC(D) |
| 130 | SPM_WK_SPCLY_FCTS_FG | VARCHAR2(300) | Y |  | Work Comment Flag in SPM | SCO_DATA_DIC(D) |
| 131 | SPM_WK_SPCLY_FCTS | VARCHAR2(300) | Y |  | Work Comments in SPM | SCO_DATA_DIC(D) |
| 132 | TST_PROD_TP | VARCHAR2(1) | Y |  | Flag of TEST HotCoil | SCO_DATA_DIC(D) |
| 133 | ENTRY_DIV_CAU_CD | VARCHAR2(2) | Y |  | Entry Division Caused Code | SCO_DATA_DIC(D) |
| 134 | ENTRY_DIV_WK_DTM | VARCHAR2(14) | Y |  | Entry Division Work Time | SCO_DATA_DIC(D) |
| 135 | SEMI_PROD_ITEM_CD | VARCHAR2(30) | Y |  | 코일 반제품 ERP ITEM | SCO_DATA_DIC(D) |
| 136 | SALES_PROD_ITEM_CD | VARCHAR2(30) | Y |  | 코일 제품 ERP ITEM | SCO_DATA_DIC(D) |
| 137 | COIL_DIV_NOS | NUMBER | Y |  | Hot Coil Item code for ERP | SCO_DATA_DIC(D) |
| 138 | MAN_PCKG_END_DTM | VARCHAR2(14) | Y |  | Manual Packing Completed date | SCO_DATA_DIC(D) |
| 139 | DMD_NXT_PROC_CD | VARCHAR2(3) | Y |  | Demand next proceed code | SCO_DATA_DIC(D) |
| 140 | HEAT_NO | VARCHAR2(9) | Y |  | Heat No | SCO_DATA_DIC(D) |
| 141 | REPROC_NOS | NUMBER | Y |  | Number of Reprogressing | SCO_DATA_DIC(D) |
| 142 | PDI_RCV_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 143 | WGT_RCV_YN | VARCHAR2(1) | Y |  | DMS SEND WEIGHT TO MES Y/N | SCO_DATA_DIC(D) |
| 144 | HCOIL_JDG_YN | VARCHAR2(1) | Y |  |  | 空 |
| 145 | PREV_SPEC_CD | VARCHAR2(50) | Y |  | 国标牌号 | SCO_DATA_DIC(D) |
| 146 | PREV_PROD_CD | VARCHAR2(3) | Y |  | 品名代码 | SCO_DATA_DIC(D) |
| 147 | PREV_ORD_USAGE | VARCHAR2(4) | Y |  | 订单用途 | SCO_DATA_DIC(D) |
| 148 | ERP_IF_DTM | VARCHAR2(14) | Y |  | Send ERP Datetime | SCO_DATA_DIC(D) |
| 149 | SEND_ERP_YN | VARCHAR2(1) | Y |  | Send ERP Yes/No | SCO_DATA_DIC(D) |
| 150 | RLG_SFT_NO | VARCHAR2(1) | Y |  | 班次 | SCO_DATA_DIC(D) |
| 151 | RLG_GRP_NO | VARCHAR2(1) | Y |  | 班组 | SCO_DATA_DIC(D) |
| 152 | COIL_THK_L2 | NUMBER | Y |  | Coil Thickness from L2 | SCO_DATA_DIC(D) |
| 153 | COIL_WTH_L2 | NUMBER | Y |  | Coil Width from L2 | SCO_DATA_DIC(D) |
| 154 | HOLD_YN | VARCHAR2(1) | Y |  | Hold Yes/No | SCO_DATA_DIC(D) |
| 155 | IN_YARD_YN | VARCHAR2(1) | Y |  |  | 空 |
| 156 | IN_YARD_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 157 | SIZE_CHG_YN | VARCHAR2(1) | Y |  |  | 空 |
| 158 | WK_PROC_MODE | VARCHAR2(1) | Y |  | SPM  Work Mode | SCO_DATA_DIC(D) |
| 159 | PLAN_HCOIL_WGT | NUMBER | Y |  |  | 空 |
| 160 | WGT_RCV_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 161 | JDG_SFT_NO | VARCHAR2(1) | Y |  | Judgement Shift Number | SCO_DATA_DIC(L) |
| 162 | JDG_GRP_NO | VARCHAR2(1) | Y |  | Judgement Group Number | SCO_DATA_DIC(L) |
| 163 | JDG_USER_ID | VARCHAR2(20) | Y |  | Judgement User ID | SCO_DATA_DIC(D) |
| 164 | WGT_RCV_LOG | VARCHAR2(2000) | Y |  | Weight Receeive Log | SCO_DATA_DIC(D) |
| 165 | SIZE_CHG_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 166 | NATL_SPEC_YEAR | VARCHAR2(4) | Y |  | 국가표준년도 | SCO_DATA_DIC(D) |
| 167 | PROD_THK | NUMBER | Y |  | Product Thickness | SCO_DATA_DIC(D) |
| 168 | PROD_WTH | NUMBER | Y |  | Product Width | SCO_DATA_DIC(D) |
| 169 | WGT_COUNT | NUMBER | Y |  | Weight Count | SCO_DATA_DIC(D) |
| 170 | RTN_FROM_SCR_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 171 | SEND_ERP_TRANS_FG | VARCHAR2(1) | Y |  |  | 空 |
| 172 | SEND_ERP_TRANS_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 173 | PROD_CD_FL | VARCHAR2(1) | Y |  |  | 空 |
| 174 | SLAB_WGT | NUMBER | Y |  | Slab Weight | SCO_DATA_DIC(D) |
| 175 | TRANSFER_FG | VARCHAR2(2) | Y |  |  | 空 |
| 176 | TRANSFER_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 177 | SEND_ERP_TRANS_EMP | VARCHAR2(20) | Y |  |  | 空 |
| 178 | LOT_NO | VARCHAR2(14) | Y |  | LOT NO(BATCH NO) | SCO_DATA_DIC(D) |
| 179 | SPM_RJT_TY | VARCHAR2(2) | Y |  | SPM Reject Type | SCO_DATA_DIC(D) |
| 180 | COIL_WGT_L2 | NUMBER | Y |  | L2 上传的钢卷重量 | SCO_DATA_DIC(D) |
| 181 | RJT_TREAT_CD | VARCHAR2(2) | Y |  | SPM Reject treatmen Code | SCO_DATA_DIC(D) |
| 182 | LOC_WGT | VARCHAR2(12) | Y |  |  | 空 |
| 183 | PDO_REQ_CNT | NUMBER | Y |  |  | 空 |
| 184 | PDO_REQ_LOG | VARCHAR2(1000) | Y |  |  | 空 |
| 185 | WGT_REQ_CNT | NUMBER | Y |  |  | 空 |
| 186 | WGT_REQ_LOG | VARCHAR2(1000) | Y |  |  | 空 |
| 187 | FINAL_DIV_FLAG | VARCHAR2(1) | Y |  | Finish Division Flag | SCO_DATA_DIC(D) |
| 188 | OLD_COIL_NET_WGT | NUMBER | Y |  |  | 空 |
| 189 | TRANS_REQ_DTM | VARCHAR2(14) | Y |  | 运送申请时间 | SCO_DATA_DIC(D) |
| 190 | TRANS_REQ_USER_ID | VARCHAR2(20) | Y |  | Transfer Request User Id | SCO_DATA_DIC(D) |
| 191 | TRANS_ACCT_REF_DTM | VARCHAR2(14) | Y |  | Transfer Accept/Refuse Datetime | SCO_DATA_DIC(D) |
| 192 | TRANS_ACCT_REF_USER_ID | VARCHAR2(20) | Y |  | Transfer Accept/Refuse User Id | SCO_DATA_DIC(D) |
| 193 | TRANS_HR_REQ_DTM | VARCHAR2(14) | Y |  | HR To CR Request Datetime | SCO_DATA_DIC(D) |
| 194 | TRANS_HR_REQ_USER_ID | VARCHAR2(20) | Y |  | HR To CR Request User ID | SCO_DATA_DIC(D) |
| 195 | TRANS_CR_RTN_REQ_DTM | VARCHAR2(14) | Y |  | CR Return To HR Request Datetime | SCO_DATA_DIC(D) |
| 196 | TRANS_CR_RTN_REQ_USER_ID | VARCHAR2(20) | Y |  | CR Return To HR Request User ID | SCO_DATA_DIC(D) |
| 197 | TRANS_HR_ACCT_DTM | VARCHAR2(14) | Y |  | HR Accept CR Return Datetime | SCO_DATA_DIC(D) |
| 198 | TRANS_HR_ACCT_USER_ID | VARCHAR2(20) | Y |  | HR Accept CR Return User ID | SCO_DATA_DIC(D) |
| 199 | TRANS_CR_ACCT_DTM | VARCHAR2(14) | Y |  | CR Accept HR Return Datetime | SCO_DATA_DIC(D) |
| 200 | TRANS_CR_ACCT_USER_ID | VARCHAR2(20) | Y |  | CR Accept HR Return User ID | SCO_DATA_DIC(D) |
| 201 | C_COIL_NO | VARCHAR2(14) | Y |  |  | 空 |
| 202 | PROD_CD_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 203 | SCH_NO_SPM | VARCHAR2(10) | Y |  | SPM Schedule No | SCO_DATA_DIC(D) |

### SYD_PROD_MASTER

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=109｜被读 91 过程 / 被写 9 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：136　**主键**：PROD_NO　**语义覆盖**：118/143

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | 创建用户 ID | DB注释(中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | 创建对象 ID | DB注释(中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | 创建时间 | DB注释(中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 最后更新用户 ID | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | 最后更新对象 ID | DB注释(中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | 最后更新时间 | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | 记录归档标志 | DB注释(中文) |
| 8 | PROD_NO | VARCHAR2(20) | N | ✓ | 产品编号 | DB注释(中文) |
| 9 | PROD_STS | VARCHAR2(1) | N |  | 产品状态 | DB注释(中文) |
| 10 | PROG_CD | VARCHAR2(4) | N |  | 进度代码 | DB注释(中文) |
| 11 | PROD_GRP | VARCHAR2(2) | Y |  | 品种代码 | DB注释(中文) |
| 12 | PROD_CD | VARCHAR2(10) | Y |  | 品名代码 | DB注释(中文) |
| 13 | ORD_THK | NUMBER | Y |  | 订单厚度 | DB注释(中文) |
| 14 | ORD_WTH | NUMBER | Y |  | 订单宽度 | DB注释(中文) |
| 15 | ORD_LTH | NUMBER | Y |  | 订单长度 | DB注释(中文) |
| 16 | PROD_THK | NUMBER | Y |  | 产品厚度 | DB注释(中文) |
| 17 | PROD_WTH | NUMBER | Y |  | 产品宽度 | DB注释(中文) |
| 18 | PROD_LTH | NUMBER | Y |  | 产品长度 | DB注释(中文) |
| 19 | PROD_NET_RMW_WGT | NUMBER | Y |  | 实际重量 | DB注释(中文) |
| 20 | PROD_NET_THY_WGT | NUMBER | Y |  | 理论重量 | DB注释(中文) |
| 21 | PROD_GRS_RMW_WGT | NUMBER | Y |  | Product Gross Actual Weight | DB注释(非中文) |
| 22 | PROD_GRS_THY_WGT | NUMBER | Y |  | Product Gross Calculated Weight | DB注释(非中文) |
| 23 | COIL_IN_DIA | NUMBER | Y |  | 内径 | DB注释(中文) |
| 24 | COIL_OUT_DIA | NUMBER | Y |  | 外径 | DB注释(中文) |
| 25 | HEAT_NO | VARCHAR2(10) | Y |  | MES炉号 | DB注释(中文) |
| 26 | SLAB_NO | VARCHAR2(50) | Y |  | 板坯号 | DB注释(中文) |
| 27 | HCOIL_NO | VARCHAR2(15) | Y |  | 热卷号 | DB注释(中文) |
| 28 | INCMP_STEEL_GRD | VARCHAR2(15) | Y |  | 替代炼钢内控钢种编号 | DB注释(中文) |
| 29 | CMP_QCERT_NO | VARCHAR2(17) | Y |  | 公司保证编号(材质记号) | DB注释(中文) |
| 30 | ORD_USAGE | VARCHAR2(4) | Y |  | 订单用途代码 | DB注释(中文) |
| 31 | SMP_NO | VARCHAR2(14) | Y |  | 试样编号 | DB注释(中文) |
| 32 | ORD_COAT_WGT_CD | VARCHAR2(7) | Y |  | 订单镀锌量代码 | DB注释(中文) |
| 33 | PACK_MTH_CD | VARCHAR2(5) | Y |  | 包装方式 | DB注释(中文) |
| 34 | ORD_EDGE_TY | VARCHAR2(1) | Y |  | 订单切边分类 | DB注释(中文) |
| 35 | OIL_MTH_CD | VARCHAR2(2) | Y |  | 涂油方法代码 | DB注释(中文) |
| 36 | PSTREAT_CD | VARCHAR2(3) | Y |  | 后处理方法 | DB注释(中文) |
| 37 | SURF_TREAT_CD | VARCHAR2(3) | Y |  | 表面处理代码 | DB注释(中文) |
| 38 | SLEEVE_YN | VARCHAR2(1) | Y |  | 套筒标识 | DB注释(中文) |
| 39 | SKINPASS_TY | VARCHAR2(1) | Y |  | 平整分类 | DB注释(中文) |
| 40 | DIFF_TEMP_GRD | VARCHAR2(2) | Y |  | 调质度 | DB注释(中文) |
| 41 | UST_MTH_CD | VARCHAR2(2) | Y |  | 热处理/探伤 | DB注释(中文) |
| 42 | HTM_MTH_CD | VARCHAR2(1) | Y |  | 热处理方法 | DB注释(中文) |
| 43 | PLT_PSTREAT_CD | VARCHAR2(2) | Y |  | 厚板后处理代码 | DB注释(中文) |
| 44 | ORD_FL | VARCHAR2(1) | Y |  | 订单材/余材区分 | DB注释(中文) |
| 45 | ORD_FL_CHANGE_DTM | VARCHAR2(14) | Y |  | 订单材/余材分类变更时间 | DB注释(中文) |
| 46 | ORD_FL_CHANGE_REASON_CD | VARCHAR2(2) | Y |  | 订单材/余材分类变更事由 | DB注释(中文) |
| 47 | ORD_NO | VARCHAR2(20) | Y |  | 订单号 | DB注释(中文) |
| 48 | ORD_LN | VARCHAR2(20) | Y |  | 订单行号 | DB注释(中文) |
| 49 | CUST_CD | VARCHAR2(9) | Y |  | 客户 | DB注释(中文) |
| 50 | CONTRACT_CD | VARCHAR2(9) | Y |  | 订单客户 | DB注释(中文) |
| 51 | SALE_REQ_FL | VARCHAR2(1) | Y |  | Sales Request Flag | DB注释(非中文) |
| 52 | SALE_REQ_USER_ID | VARCHAR2(20) | Y |  | Sales Request Employee ID | DB注释(非中文) |
| 53 | SALE_REQ_DTM | VARCHAR2(14) | Y |  | Sales Request Datetime | DB注释(非中文) |
| 54 | SPEC_CD | VARCHAR2(50) | Y |  | 国家标准及牌号 | DB注释(中文) |
| 55 | LOC_CD | VARCHAR2(10) | Y |  | 库房垛位 | DB注释(中文) |
| 56 | INWH_PROD_DTM | VARCHAR2(14) | Y |  | 入库日期 | DB注释(中文) |
| 57 | PROD_GRD | VARCHAR2(2) | Y |  | 产品等级 | DB注释(中文) |
| 58 | FINAL_JDG_REQ_DTM | VARCHAR2(14) | Y |  | 综合判定申请日期 | DB注释(中文) |
| 59 | FINAL_JDG_PASS_FL | VARCHAR2(1) | Y |  | 综判是否合格 | DB注释(中文) |
| 60 | FINAL_JDG_DTM | VARCHAR2(14) | Y |  | 综合判定日期 | DB注释(中文) |
| 61 | DORD_NO | VARCHAR2(30) | Y |  | 出货指示号 | DB注释(中文) |
| 62 | DORD_DTM | VARCHAR2(14) | Y |  | 提货单日期 | DB注释(中文) |
| 63 | CAR_ENTRY_ID | NUMBER | Y |  | 入门编号 | DB注释(中文) |
| 64 | OUTWH_DISP_DTM | VARCHAR2(14) | Y |  | 出货日期 | DB注释(中文) |
| 65 | RTN_REQ_DTM | VARCHAR2(14) | Y |  | 退库申请日期 | DB注释(中文) |
| 66 | OUTWH_RTNPROC_DTM | VARCHAR2(14) | Y |  | 退货日期 | DB注释(中文) |
| 67 | RORD_NO | VARCHAR2(10) | Y |  | 退货指令编号 | DB注释(中文) |
| 68 | INWH_RTNPROD_DTM | VARCHAR2(14) | Y |  | 入库日期 | DB注释(中文) |
| 69 | RORD_REASON_CD | VARCHAR2(2) | Y |  | 退货原因 | DB注释(中文) |
| 70 | PROD_END_REASON_CD | VARCHAR2(2) | Y |  |  | 空 |
| 71 | ORGN_PROD_NO | VARCHAR2(20) | Y |  |  | 空 |
| 72 | SALES_PROD_ITEM_CD | VARCHAR2(40) | Y |  | 钢卷成品 ERP ITEM | DB注释(中文) |
| 73 | SEMI_PROD_ITEM_CD | VARCHAR2(40) | Y |  | 钢卷半成品 ERP ITEM | DB注释(中文) |
| 74 | PROD_DTM | VARCHAR2(14) | Y |  | 生产日期 | SCO_DATA_DIC(L) |
| 75 | OP_JDG_GRD | VARCHAR2(2) | Y |  | 外观综判 | DB注释(中文) |
| 76 | PROC_CD | VARCHAR2(3) | Y |  | 工序代码 | DB注释(中文) |
| 77 | ORGN_ORD_NO | VARCHAR2(10) | Y |  |  | 空 |
| 78 | ORGN_ORD_LN | VARCHAR2(20) | Y |  |  | 空 |
| 79 | ORD_TY | VARCHAR2(2) | Y |  | 订单类型 | DB注释(中文) |
| 80 | SURF_GRD | VARCHAR2(10) | Y |  | 表面等级 | DB注释(中文) |
| 81 | ACT_WGT_FL | VARCHAR2(1) | Y |  |  | 空 |
| 82 | UST_STD_CD | VARCHAR2(200) | Y |  | 探伤执行标准及等级 | DB注释(中文) |
| 83 | HIGH_SURF_FL | VARCHAR2(1) | Y |  | 高表面区分 | DB注释(中文) |
| 84 | OIL_LEVEL | VARCHAR2(2) | Y |  | 涂油级别 | DB注释(中文) |
| 85 | ANTRST_OIL_KIND | VARCHAR2(1) | Y |  | 防锈油种类 | DB注释(中文) |
| 86 | NATL_SPEC_YEAR | VARCHAR2(4) | Y |  | 国家标准年度 | DB注释(中文) |
| 87 | PROD_CD_FL | VARCHAR2(1) | Y |  |  | 空 |
| 88 | INWH_USER_ID | VARCHAR2(20) | Y |  |  | 空 |
| 89 | ERP_FL | VARCHAR2(10) | Y |  |  | 空 |
| 90 | OUTWH_DISP_CANCEL_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 91 | SELF_YN | VARCHAR2(1) | Y |  | 自用材与否 | SCO_DATA_DIC(D) |
| 92 | RCV_GOODS_CONF | VARCHAR2(1) | Y |  |  | 空 |
| 93 | CHG_WGT_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 94 | CHG_WGT_USER | VARCHAR2(20) | Y |  |  | 空 |
| 95 | CHG_WGT_BEF | VARCHAR2(14) | Y |  |  | 空 |
| 96 | SQM_HAND_OPEN | VARCHAR2(500) | Y |  |  | 空 |
| 97 | VIRTUAL_SHIPMENT | VARCHAR2(1) | Y |  |  | 空 |
| 98 | STD_STLGRD | VARCHAR2(20) | Y |  | 牌号 | DB注释(中文) |
| 99 | BATCH_CD | VARCHAR2(30) | Y |  | 批次号 | DB注释(中文) |
| 100 | ORD_DIA | NUMBER | Y |  |  | 空 |
| 101 | PROD_DIA | NUMBER | Y |  |  | 空 |
| 102 | HOOK_NO | NUMBER | Y |  | 吊钩号 | DB注释(中文) |
| 103 | YD_LAYER_NO | NUMBER | Y |  | 层号 | DB注释(中文) |
| 104 | BUNDLE_CNT | NUMBER | Y |  | 每捆型材支数 | DB注释(中文) |
| 105 | PROD_FTHK | NUMBER | Y |  | 产品腹板厚度 | DB注释(中文) |
| 106 | PROD_YTHK | NUMBER | Y |  | 产品翼缘厚度 | DB注释(中文) |
| 107 | ORD_FTHK | NUMBER | Y |  | 订单腹板厚度 | DB注释(中文) |
| 108 | ORD_YTHK | NUMBER | Y |  | 订单翼缘厚度 | DB注释(中文) |
| 109 | DORD_FL | VARCHAR2(150) | Y |  |  | 空 |
| 110 | SEC_SCALE_DTM | VARCHAR2(14) | Y |  | 二次计量时间 | DB注释(中文) |
| 111 | OUT_TYPE | VARCHAR2(10) | Y |  | 出库类型 1=销售 2=自用材 | DB注释(中文) |
| 112 | ORD_SIZE_TY | VARCHAR2(1) | Y |  | 定尺类型 | DB注释(中文) |
| 113 | RTNPROC_REASON | VARCHAR2(200) | Y |  | 退货原因 | DB注释(中文) |
| 114 | ORG_ORD_LN | VARCHAR2(20) | Y |  | 原订单行编号 | DB注释(中文) |
| 115 | ORG_ORD_NO | VARCHAR2(20) | Y |  | 原订单编号 | DB注释(中文) |
| 116 | BUNDLE_TP | VARCHAR2(10) | Y |  | 捆类型10-定尺，11-短尺 | DB注释(中文) |
| 117 | ORG_BUNDLE_CNT | NUMBER | Y |  | 每捆型材支数(拆捆前) | DB注释(中文) |
| 118 | IN_SFT_GRP | VARCHAR2(30) | Y |  | 入库班组 | DB注释(中文) |
| 119 | IN_SFT_NO | VARCHAR2(30) | Y |  | 入库班次 | DB注释(中文) |
| 120 | ERP_IN_DATE | VARCHAR2(8) | Y |  | ERP入库时间 | DB注释(中文) |
| 121 | WK_SFT_GRP | VARCHAR2(30) | Y |  | 班组 | DB注释(中文) |
| 122 | CUST_PO_NO | VARCHAR2(30) | Y |  | 电商订单号 | DB注释(中文) |
| 123 | CUST_PO_LN_NO | VARCHAR2(30) | Y |  | 电商订单行号 | DB注释(中文) |
| 124 | YD_GR_TP | VARCHAR2(1) | Y |  | 库区代码 | DB注释(中文) |
| 125 | ERP_RTN_DATE | VARCHAR2(8) | Y |  | ERP退库时间 | DB注释(中文) |
| 126 | ATTRIBUTE4 | VARCHAR2(150) | Y |  |  | 空 |
| 127 | ATTRIBUTE5 | VARCHAR2(150) | Y |  |  | 空 |
| 128 | ATTRIBUTE6 | VARCHAR2(150) | Y |  |  | 空 |
| 129 | ATTRIBUTE7 | VARCHAR2(150) | Y |  |  | 空 |
| 130 | ATTRIBUTE8 | VARCHAR2(150) | Y |  |  | 空 |
| 131 | ATTRIBUTE9 | VARCHAR2(150) | Y |  |  | 空 |
| 132 | ATTRIBUTE10 | VARCHAR2(150) | Y |  |  | 空 |
| 133 | SALES_PROD_ITEM_CD_NM | VARCHAR2(50) | Y |  | 物料名称 | DB注释(中文) |
| 134 | CAR_ASGN_NO | VARCHAR2(50) | Y |  | 提货单号 | DB注释(中文) |
| 135 | CAR_ASGN_LN | VARCHAR2(50) | Y |  | 提货单行号 | DB注释(中文) |
| 136 | IF_OUT | VARCHAR2(10) | Y |  | 是否外卖 | DB注释(中文) |
| 137 | BACK1 | VARCHAR2(3000) | Y |  | 产品库存画面备注 | DB注释(中文) |
| 138 | CUST_CD_NM | VARCHAR2(500) | Y |  | 客户名称 | DB注释(中文) |
| 139 | WORK_DATE | VARCHAR2(20) | Y |  | 作业日期 | DB注释(中文) |
| 140 | WORK_SHIFT | VARCHAR2(20) | Y |  | 作业班次 | DB注释(中文) |
| 141 | IF_CHULI | VARCHAR2(2) | Y |  | 是否待处理 | DB注释(中文) |
| 142 | YD_BED_CD | VARCHAR2(7) | Y |  | 垛位号 | DB注释(中文) |
| 143 | NUM | NUMBER | Y |  | 数量 | DB注释(中文) |

### SSD_ORDER_HEAD

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=100｜被读 94 过程 / 被写 3 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：1303　**主键**：ORD_NO　**语义覆盖**：97/98

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | ORD_NO | VARCHAR2(10) | N | ✓ | 订单号 | DB注释(中文) |
| 9 | ORD_STS | VARCHAR2(1) | N |  | 订单状态 | DB注释(中文) |
| 10 | PROD_GRP | VARCHAR2(2) | Y |  | 品种 | DB注释(中文) |
| 11 | PROD_CD | VARCHAR2(3) | Y |  | 品名 | DB注释(中文) |
| 12 | ORD_TY | VARCHAR2(2) | Y |  | 订单类型 | DB注释(中文) |
| 13 | ORD_RCV_TY | VARCHAR2(1) | Y |  | 内贸国贸区分 | DB注释(中文) |
| 14 | STOC_SALES_TY | VARCHAR2(1) | Y |  | 库存销售分类 | DB注释(中文) |
| 15 | SALES_CHNL_CD | VARCHAR2(2) | Y |  | 渠道类别 | DB注释(中文) |
| 16 | CUST_CD | VARCHAR2(40) | Y |  | 客户 | DB注释(中文) |
| 17 | CONTRACT_CD | VARCHAR2(20) | Y |  | 订单客户 | DB注释(中文) |
| 18 | BILLTO_SITE_CD | VARCHAR2(20) | Y |  | 收单方 | DB注释(中文) |
| 19 | BILLTO_SITE_ADDR | VARCHAR2(500) | Y |  | 收单方地址 | DB注释(中文) |
| 20 | BILLTO_SITE_INCHARGE | VARCHAR2(20) | Y |  | 收单方联系人 | DB注释(中文) |
| 21 | BILLTO_SITE_TEL_NO | VARCHAR2(20) | Y |  | 收单方联系电话 | DB注释(中文) |
| 22 | SHIPTO_SITE_CD | VARCHAR2(20) | Y |  | 收货方 | DB注释(中文) |
| 23 | SHIPTO_SITE_ADDR | VARCHAR2(500) | Y |  | 收货方地址 | DB注释(中文) |
| 24 | SHIPTO_SITE_INCHARGE | VARCHAR2(20) | Y |  | 收货方联系人 | DB注释(中文) |
| 25 | SHIPTO_SITE_TEL_NO | VARCHAR2(20) | Y |  | 收货方联系电话 | DB注释(中文) |
| 26 | FINAL_CUST_CD | VARCHAR2(9) | Y |  | 最终用户（空） | DB注释(中文) |
| 27 | DEST_CD | VARCHAR2(9) | Y |  | 收货目的地 | DB注释(中文) |
| 28 | PAY_TERMS | VARCHAR2(2) | Y |  | 付款约定 | DB注释(中文) |
| 29 | PAY_MTH_CD | VARCHAR2(2) | Y |  | 付款方式 | DB注释(中文) |
| 30 | PREPAYMENT_RATE | NUMBER | Y |  | 预收款比例 | DB注释(中文) |
| 31 | PRICE_DCN_CD | VARCHAR2(1) | Y |  | 定价方式 | DB注释(中文) |
| 32 | INVOICE_MODE | VARCHAR2(1) | Y |  | 运费结算方式 | DB注释(中文) |
| 33 | DELV_COND_CD | VARCHAR2(2) | Y |  | 交货方式 | DB注释(中文) |
| 34 | TRNSF_MTH_CD | VARCHAR2(2) | Y |  | 运输方式 | DB注释(中文) |
| 35 | CURRENCY_CD | VARCHAR2(3) | Y |  | 币种 | DB注释(中文) |
| 36 | PROD_TAX_CD | VARCHAR2(3) | Y |  | 产品税率代码 | DB注释(中文) |
| 37 | PROD_TAX_RATE | NUMBER | Y |  | 产品税率 | DB注释(中文) |
| 38 | TRNSF_TAX_CD | VARCHAR2(3) | Y |  | 运费税率代码 | DB注释(中文) |
| 39 | TRNSF_TAX_RATE | NUMBER | Y |  | 运费税率 | DB注释(中文) |
| 40 | EXCHANGE_RATE | NUMBER | Y |  | 汇率（空） | DB注释(中文) |
| 41 | EXCHANGE_TY | VARCHAR2(1) | Y |  | 汇率类型（空） | DB注释(中文) |
| 42 | EXCHANGE_DT | VARCHAR2(8) | Y |  | 汇率日期（空） | DB注释(中文) |
| 43 | URGENT_FL | VARCHAR2(1) | Y |  | 是否紧急（空） | DB注释(中文) |
| 44 | BYPROD_UOM_CD | VARCHAR2(3) | Y |  | 副产品计量单位（空） | DB注释(中文) |
| 45 | CLAIM_NO | VARCHAR2(10) | Y |  | 异议编号（空） | DB注释(中文) |
| 46 | CUST_PO_NO | VARCHAR2(50) | Y |  | 合同号 | DB注释(中文) |
| 47 | SHIP_ASGN_NO | VARCHAR2(10) | Y |  | 空 | DB注释(中文) |
| 48 | SALES_EMP_ID | VARCHAR2(20) | Y |  | 业务人员ID | DB注释(中文) |
| 49 | DEPT_CD | VARCHAR2(15) | Y |  | 部门代码 | DB注释(中文) |
| 50 | FR_STATION_CD | VARCHAR2(5) | Y |  | 发货港 | DB注释(中文) |
| 51 | TO_STATION_CD | VARCHAR2(5) | Y |  | 到货港（空） | DB注释(中文) |
| 52 | ORD_RCV_DT | VARCHAR2(8) | Y |  | Order Receipt Date | DB注释(非中文) |
| 53 | ORD_REG_DTM | VARCHAR2(14) | Y |  | Order Register Date | DB注释(非中文) |
| 54 | ORD_CONF_DTM | VARCHAR2(14) | Y |  | Order Confirm Date | DB注释(非中文) |
| 55 | ORD_REGL_EMP_ID | VARCHAR2(20) | Y |  | Order Register Employee ID | DB注释(非中文) |
| 56 | ORD_CONF_EMP_ID | VARCHAR2(20) | Y |  | Order Confirm Employee ID | DB注释(非中文) |
| 57 | ORD_HOLD_TY | VARCHAR2(2) | Y |  | Order hold Type | DB注释(非中文) |
| 58 | ORD_HOLD_EMP_ID | VARCHAR2(20) | Y |  | Order hold Employee ID | DB注释(非中文) |
| 59 | ORD_HOLD_DTM | VARCHAR2(14) | Y |  | Order hold Date | DB注释(非中文) |
| 60 | ORD_CANCEL_TY | VARCHAR2(2) | Y |  | Order Cancel Type | DB注释(非中文) |
| 61 | ORD_CANCEL_EMP_ID | VARCHAR2(20) | Y |  | Order Cancel Employee ID | DB注释(非中文) |
| 62 | ORD_CANCEL_DTM | VARCHAR2(14) | Y |  | Order Cancel Date | DB注释(非中文) |
| 63 | ORD_MDF_TY | VARCHAR2(2) | Y |  | Order Modify Type | DB注释(非中文) |
| 64 | ORD_MDF_EMP_ID | VARCHAR2(20) | Y |  | Order Modify Employee ID | DB注释(非中文) |
| 65 | ORD_MDF_DTM | VARCHAR2(14) | Y |  | Order Modify Date | DB注释(非中文) |
| 66 | CONTRACT_DT | VARCHAR2(8) | Y |  | 合同日期 | DB注释(中文) |
| 67 | CONTRACT_CONF_NO | VARCHAR2(30) | Y |  | 批示号 | DB注释(中文) |
| 68 | PRICE_DOCU_NO | VARCHAR2(30) | Y |  | 价格文件 | DB注释(中文) |
| 69 | INSP_AGENCY_CD | VARCHAR2(3) | Y |  | 检查机构 | DB注释(中文) |
| 70 | ADD_LN_MARK_MTH1 | VARCHAR2(10) | Y |  | 标记追加行1 | SCO_DATA_DIC(D) |
| 71 | MARK_ADD_DESC1 | VARCHAR2(100) | Y |  | Marking Description 1 | SCO_DATA_DIC(D) |
| 72 | MARK_ADD_DESC2 | VARCHAR2(100) | Y |  | Marking Description 2 | SCO_DATA_DIC(D) |
| 73 | MARK_ADD_DESC3 | VARCHAR2(100) | Y |  | Marking Description 3 | SCO_DATA_DIC(D) |
| 74 | MARK_ADD_DESC4 | VARCHAR2(100) | Y |  | Marking Description 4 | SCO_DATA_DIC(D) |
| 75 | MARK_PROD_NM | VARCHAR2(30) | Y |  | 标记品名 | DB注释(中文) |
| 76 | MARK_CUST_NM | VARCHAR2(80) | Y |  | 标记客户 | DB注释(中文) |
| 77 | CONSIGN_PRCS_TY | VARCHAR2(2) | Y |  | Consignment Process Type | DB注释(非中文) |
| 78 | CONSIGN_INVOICE_MODE | VARCHAR2(2) | Y |  | Consignment Process Invoice Mode | DB注释(非中文) |
| 79 | SITE_CLF | VARCHAR2(3) | Y |  | Site Classify | SCO_DATA_DIC(D) |
| 80 | COUNTRY_CD | VARCHAR2(3) | Y |  | 出口国家 | DB注释(中文) |
| 81 | EXP_TAX_RATE | NUMBER | Y |  | 出口退税率 | DB注释(中文) |
| 82 | ORD_END_TY | VARCHAR2(2) | Y |  | 订单结束类型 | DB注释(中文) |
| 83 | ORD_END_EMP_ID | VARCHAR2(20) | Y |  | 订单结束人员 | DB注释(中文) |
| 84 | ORD_END_DTM | VARCHAR2(14) | Y |  | 订单结束时间 | DB注释(中文) |
| 85 | ERROR_FL | VARCHAR2(1) | Y |  | 是否错误 | DB注释(中文) |
| 86 | ORD_LMT_DT | VARCHAR2(8) | Y |  | 有效日期 | DB注释(中文) |
| 87 | EXP_TAX_FL | VARCHAR2(1) | Y |  | 是否退税 | DB注释(中文) |
| 88 | MTC_PRT_FL | VARCHAR2(1) | Y |  |  | 空 |
| 89 | SALES_SPCL_DESC | VARCHAR2(600) | Y |  | 备注 | DB注释(中文) |
| 90 | ORD_CANC_CONF_DTM | VARCHAR2(14) | Y |  | 订单取消确认日期 | DB注释(中文) |
| 91 | ORD_CANC_CONF_EMP_ID | VARCHAR2(20) | Y |  | 订单取消确认人员 | DB注释(中文) |
| 92 | MACHINE_YN | VARCHAR2(1) | Y |  | 自用材订单委外加工与否，Y/N | DB注释(中文) |
| 93 | ITEM_MTY | VARCHAR2(5) | Y |  | 自用材订单物料中类 | DB注释(中文) |
| 94 | ITEM_LTY | VARCHAR2(3) | Y |  | 自用材订单物料小类 | DB注释(中文) |
| 95 | MACHINE_TY | VARCHAR2(3) | Y |  | 自用材订单委外加工工艺 | DB注释(中文) |
| 96 | TRNSF_DOCU_NO | VARCHAR2(20) | Y |  | 运费价格文件 | DB注释(中文) |
| 97 | IMPORTANT_YN | VARCHAR2(1) | Y |  | 重点客户与否 | DB注释(中文) |
| 98 | ORD_NO_IMP | VARCHAR2(50) | Y |  | 导入订单号 | DB注释(中文) |

### SMS_HEAT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=99｜被读 91 过程 / 被写 4 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：25978　**主键**：HEAT_NO　**语义覆盖**：82/87

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | HEAT_NO | VARCHAR2(10) | N | ✓ | Heat No | DB注释(非中文) |
| 9 | PRP_HEAT_NO | VARCHAR2(9) | Y |  | Prepared Heat No | DB注释(非中文) |
| 10 | PLAN_HEAT_NO | VARCHAR2(8) | Y |  | Plan Heat No | DB注释(非中文) |
| 11 | HEAT_STS | VARCHAR2(1) | Y |  | Heat Status | DB注释(非中文) |
| 12 | MTRL_SHP_TY | VARCHAR2(1) | Y |  | Matrial Shape Type | DB注释(非中文) |
| 13 | HEAT_WGT | NUMBER | Y |  | Heat Weight | DB注释(非中文) |
| 14 | CAST_NO | VARCHAR2(8) | Y |  | Plan Cast No | DB注释(非中文) |
| 15 | HEAT_CNT | NUMBER | Y |  | Nos of Heat | DB注释(非中文) |
| 16 | HEAT_PRI | NUMBER | Y |  | Heat Priority | DB注释(非中文) |
| 17 | SLAB_CNT | NUMBER | Y |  | Nos of Slab | DB注释(非中文) |
| 18 | ORD_NO | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 19 | ORD_LN | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 20 | SPEC_CD | VARCHAR2(50) | Y |  | Specification Code | DB注释(非中文) |
| 21 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  | Steel Grade | DB注释(非中文) |
| 22 | DE_P_YN | VARCHAR2(1) | Y |  | Dephosphorization Y/N | DB注释(非中文) |
| 23 | SECOND_RFN_CD | VARCHAR2(3) | Y |  | 2nd Refining code | DB注释(非中文) |
| 24 | OPER_TRK_CD | VARCHAR2(3) | Y |  | Operation Tracking Code | DB注释(非中文) |
| 25 | HEAT_PROG_CD | VARCHAR2(3) | Y |  | Progress code | DB注释(非中文) |
| 26 | PASS_PROC_ROUTE | VARCHAR2(40) | Y |  | Pass route | DB注释(非中文) |
| 27 | PLAN_PROC_ROUTE | VARCHAR2(20) | Y |  | Plan route | DB注释(非中文) |
| 28 | REM_PROC_ROUTE | VARCHAR2(20) | Y |  | Remain route | DB注释(非中文) |
| 29 | KR_NO | VARCHAR2(1) | Y |  | KR No | DB注释(非中文) |
| 30 | KR_ARR_DTM | VARCHAR2(14) | Y |  | KR Arrival date | DB注释(非中文) |
| 31 | KR_STA_DTM | VARCHAR2(14) | Y |  | KR Start Date | DB注释(非中文) |
| 32 | KR_END_DTM | VARCHAR2(14) | Y |  | KR End Date | DB注释(非中文) |
| 33 | KR_DEP_DTM | VARCHAR2(14) | Y |  | KR Departure date | DB注释(非中文) |
| 34 | DE_P_MC_NO | VARCHAR2(1) | Y |  | BOF(De-P) No | DB注释(非中文) |
| 35 | DE_P_CHARG_STA_DTM | VARCHAR2(14) | Y |  | BOF(DE-P) Charging start date | DB注释(非中文) |
| 36 | DE_P_CHARG_END_DTM | VARCHAR2(14) | Y |  | BOF(DE-P) Charging end date | DB注释(非中文) |
| 37 | DE_P_BLW_STA_DTM | VARCHAR2(14) | Y |  | BOF(De-P) Blowing Start Date | DB注释(非中文) |
| 38 | DE_P_BLW_END_DTM | VARCHAR2(14) | Y |  | BOF(De-P) Blowing End Date | DB注释(非中文) |
| 39 | DE_P_TAP_STA_DTM | VARCHAR2(14) | Y |  | BOF(De-P) Tapping Start Date | DB注释(非中文) |
| 40 | DE_P_TAP_END_DTM | VARCHAR2(14) | Y |  | BOF(De-P) Tapping End Date | DB注释(非中文) |
| 41 | DE_C_MC_NO | VARCHAR2(1) | Y |  | BOF(De-C) No | DB注释(非中文) |
| 42 | DE_C_CHARG_STA_DTM | VARCHAR2(14) | Y |  | BOF(DE-C) Charging start date | DB注释(非中文) |
| 43 | DE_C_CHARG_END_DTM | VARCHAR2(14) | Y |  | BOF(DE-C) Charging end date | DB注释(非中文) |
| 44 | DE_C_BLW_STA_DTM | VARCHAR2(14) | Y |  | BOF(De-C) Blowing Start Date | DB注释(非中文) |
| 45 | DE_C_BLW_END_DTM | VARCHAR2(14) | Y |  | BOF(De-C) Blowing End Date | DB注释(非中文) |
| 46 | DE_C_TAP_STA_DTM | VARCHAR2(14) | Y |  | BOF(De-C) Tapping Start Date | DB注释(非中文) |
| 47 | DE_C_TAP_END_DTM | VARCHAR2(14) | Y |  | BOF(De-C) Tapping End Date | DB注释(非中文) |
| 48 | WF_NO | VARCHAR2(1) | Y |  | WF No | DB注释(非中文) |
| 49 | WF_ARR_DTM | VARCHAR2(14) | Y |  | WF Arrival date | DB注释(非中文) |
| 50 | WF_STA_DTM | VARCHAR2(14) | Y |  | WF Start Date | DB注释(非中文) |
| 51 | WF_END_DTM | VARCHAR2(14) | Y |  | WF End Date | DB注释(非中文) |
| 52 | WF_DEP_DTM | VARCHAR2(14) | Y |  | WF Departure date | DB注释(非中文) |
| 53 | LF_NO | VARCHAR2(1) | Y |  | LF No | DB注释(非中文) |
| 54 | LF_ARR_DTM | VARCHAR2(14) | Y |  | LF Arrival date | DB注释(非中文) |
| 55 | LF_STA_DTM | VARCHAR2(14) | Y |  | LF Start Date | DB注释(非中文) |
| 56 | LF_END_DTM | VARCHAR2(14) | Y |  | LF End Date | DB注释(非中文) |
| 57 | LF_DEP_DTM | VARCHAR2(14) | Y |  | LF Departure date | DB注释(非中文) |
| 58 | RH_NO | VARCHAR2(1) | Y |  | RH No | DB注释(非中文) |
| 59 | RH_ARR_DTM | VARCHAR2(14) | Y |  | RH Arrival date | DB注释(非中文) |
| 60 | RH_STA_DTM | VARCHAR2(14) | Y |  | RH Start Date | DB注释(非中文) |
| 61 | RH_END_DTM | VARCHAR2(14) | Y |  | RH End Date | DB注释(非中文) |
| 62 | RH_DEP_DTM | VARCHAR2(14) | Y |  | RH Departure date | DB注释(非中文) |
| 63 | CC_NO | VARCHAR2(1) | Y |  | C. Caster No | DB注释(非中文) |
| 64 | CC_ARR_DTM | VARCHAR2(14) | Y |  | CC Arrival date | DB注释(非中文) |
| 65 | CC_STA_DTM | VARCHAR2(14) | Y |  | C. Caster Casting Start Date | DB注释(非中文) |
| 66 | CC_END_DTM | VARCHAR2(14) | Y |  | C. Caster Casting End Date | DB注释(非中文) |
| 67 | CC_DEP_DTM | VARCHAR2(14) | Y |  | CC Departure date | DB注释(非中文) |
| 68 | ERP_HEAT_CHEM_POST_DT | VARCHAR2(8) | Y |  | ERP Heat Chem Post Date | DB注释(非中文) |
| 69 | LST_CUT_YN | VARCHAR2(1) | Y |  | Last cut Y/N | DB注释(非中文) |
| 70 | DIVERT_STEEL_GRD | VARCHAR2(10) | Y |  | Diverted Steel grade | DB注释(非中文) |
| 71 | HEAT_JUDG | VARCHAR2(1) | Y |  | Heat Judgment Result | DB注释(非中文) |
| 72 | RTN_PROC_CD | VARCHAR2(2) | Y |  | Return Process Code | DB注释(非中文) |
| 73 | ERP_POSTING_DTM | VARCHAR2(14) | Y |  | ERP Posting Date | DB注释(非中文) |
| 74 | CC_PLAN_NO | VARCHAR2(10) | Y |  | Casting Plan Number | DB注释(非中文) |
| 75 | SEMI_PROD_ITEM_CD | VARCHAR2(30) | Y |  | SEMI Production Item code | DB注释(非中文) |
| 76 | ERP_POSTING_YN | VARCHAR2(1) | Y |  | ERP Posting Y/N | DB注释(非中文) |
| 77 | ERP_TRANSACTION_TY | VARCHAR2(2) | Y |  | ERP Transaction Type | DB注释(非中文) |
| 78 | HEAT_CONF_YN | VARCHAR2(1) | Y |  | Heat Conf. Yes/No | DB注释(非中文) |
| 79 | HEAT_CONF_DTM | VARCHAR2(14) | Y |  | Heat Conf. Datetime | DB注释(非中文) |
| 80 | HEAT_NO_PO | VARCHAR2(20) | Y |  | po heat no | SCO_DATA_DIC(L) |
| 81 | STD_STLGRD | VARCHAR2(20) | Y |  | 钢种 | DB注释(中文) |
| 82 | CC_HEAT_NO | VARCHAR2(12) | Y |  | 铸机炉次号 | DB注释(中文) |
| 83 | VD_NO | VARCHAR2(1) | Y |  |  | 空 |
| 84 | VD_ARR_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 85 | VD_STA_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 86 | VD_END_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 87 | VD_DEP_DTM | VARCHAR2(14) | Y |  |  | 空 |

### SCH_PLT_INST_ROLL

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=85｜被读 65 过程 / 被写 10 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：119165　**主键**：ROLL_UNIT、MTL_NO　**语义覆盖**：202/202

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID_Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID_Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time_Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID_Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID_Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time_Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag_Record Archive Flag | DB注释(非中文) |
| 8 | ROLL_UNIT | VARCHAR2(20) | N | ✓ | Roll Unit_Roll单位 | DB注释(中文) |
| 9 | MTL_NO | VARCHAR2(14) | N | ✓ | Material No_材料编号 | DB注释(中文) |
| 10 | INST_MPLATE_NO | VARCHAR2(15) | Y |  | Instruction??No_指令母板号 | DB注释(中文) |
| 11 | ROLL_UNIT_PRI | NUMBER | Y |  | Roll Unit Priority_热轧Roll单位内顺序 | DB注释(中文) |
| 12 | PLAN_PROC_SEQ | NUMBER | Y |  | Plan Process Sequence_计划工序顺序 | DB注释(中文) |
| 13 | SPEC_RCV_DTM | VARCHAR2(14) | Y |  | Spec Receive DateTime_作业计划接收时刻 | DB注释(中文) |
| 14 | PROD_INST_DTM | VARCHAR2(14) | Y |  | Production Order Send(L2) Datetime_生产指令时刻 | DB注释(中文) |
| 15 | ROLL_UNIT_FCE_PRI | NUMBER | Y |  | Roll Unit Furnance Priority_Roll单位内加热炉装炉顺序 | DB注释(中文) |
| 16 | FCE_STA_SCH_DTM | VARCHAR2(14) | Y |  | Furnance Start Schedule Datetime_加热炉开始时刻 | DB注释(中文) |
| 17 | FCE_END_SCH_DTM | VARCHAR2(14) | Y |  | Furnance End Schedule Datetime_加热炉结束时刻 | DB注释(中文) |
| 18 | RLG_STA_SCH_DTM | VARCHAR2(14) | Y |  | Rolling Start Schedule Datetime_热间轧制开始时刻 | DB注释(中文) |
| 19 | RLG_END_SCH_DTM | VARCHAR2(14) | Y |  | Rolling End Schedule Datetime_热间轧制结束时刻 | DB注释(中文) |
| 20 | PLAN_ROLL_STS | VARCHAR2(3) | Y |  | PLAN Roll Staus_计划Roll状态 | DB注释(中文) |
| 21 | MPLATE_DGN_THK | NUMBER | Y |  | ??????_母板设计厚度 | DB注释(中文) |
| 22 | MPLATE_DGN_WTH | NUMBER | Y |  | ?????_母板设计宽度 | DB注释(中文) |
| 23 | MPLATE_DGN_LTH | NUMBER | Y |  | ??????_母板设计长度 | DB注释(中文) |
| 24 | MPLATE_DGN_WGT | NUMBER | Y |  | ??????_母板指示重量 | DB注释(中文) |
| 25 | MPLATE_PLATE_QTY | NUMBER | Y |  | ???Plate??_母板內产品买入 | DB注释(中文) |
| 26 | DGN_OVROLL_QTY | NUMBER | Y |  | ??OverRoll??_设计OverRoll支数 | DB注释(中文) |
| 27 | DGN_OVROLL_WGT | NUMBER | Y |  | ??OverRoll?_设计OverRoll重量 | DB注释(中文) |
| 28 | PROD_CD | VARCHAR2(3) | Y |  | ????_品名代码 | DB注释(中文) |
| 29 | ORD_NO | VARCHAR2(10) | Y |  | ??????_代表订单编号 | DB注释(中文) |
| 30 | ORD_LN | VARCHAR2(3) | Y |  | ??????_代表订单行号 | DB注释(中文) |
| 31 | DESIGN_CONTENT | VARCHAR2(1) | Y |  | ????_设计內容 | DB注释(中文) |
| 32 | MPLATE_HTTRT_MIX_DS_GP | VARCHAR2(1) | Y |  | ???????????_母板热处理混合设计分类 | DB注释(中文) |
| 33 | UST_ULTRASONIC_DGN_TY | VARCHAR2(1) | Y |  | ?????????????_母板UST混合设计分类 | DB注释(中文) |
| 34 | CMBN_ORD_LN_CNT | NUMBER | Y |  | ?????????_组合订单行号数 | DB注释(中文) |
| 35 | ORD_NO1 | VARCHAR2(10) | Y |  | ????1_订单编号1 | DB注释(中文) |
| 36 | ORD_LN1 | VARCHAR2(3) | Y |  | ????1_订单行号1 | DB注释(中文) |
| 37 | PLATE_DGN_QTY1 | NUMBER | Y |  | PLATE????1_PLATE设计支数1 | DB注释(中文) |
| 38 | PLATE_OR_QTY1 | NUMBER | Y |  | ??OverRoll??1_设计OverRoll支数1 | DB注释(中文) |
| 39 | PLATE_DGN_WTH1 | NUMBER | Y |  | PLATE???1_PLATE设计宽度1 | DB注释(中文) |
| 40 | PLATE_DGN_LTH1 | NUMBER | Y |  | PLATE????1_PLATE设计长度1 | DB注释(中文) |
| 41 | PLATE_DGN_WGT1 | NUMBER | Y |  | PLATE????1_PLATE设计重量1 | DB注释(中文) |
| 42 | ORD_NO2 | VARCHAR2(10) | Y |  | ????2_订单编号2 | DB注释(中文) |
| 43 | ORD_LN2 | VARCHAR2(3) | Y |  | ????2_订单行号2 | DB注释(中文) |
| 44 | PLATE_DGN_QTY2 | NUMBER | Y |  | PLATE????2_PLATE设计支数2 | DB注释(中文) |
| 45 | PLATE_OR_QTY2 | NUMBER | Y |  | ??OverRoll??2_设计OverRoll支数2 | DB注释(中文) |
| 46 | PLATE_DGN_WTH2 | NUMBER | Y |  | PLATE???2_PLATE设计宽度2 | DB注释(中文) |
| 47 | PLATE_DGN_LTH2 | NUMBER | Y |  | PLATE????2_PLATE设计长度2 | DB注释(中文) |
| 48 | PLATE_DGN_WGT2 | NUMBER | Y |  | PLATE????2_PLATE设计重量2 | DB注释(中文) |
| 49 | ORD_NO3 | VARCHAR2(10) | Y |  | ????3_订单编号3 | DB注释(中文) |
| 50 | ORD_LN3 | VARCHAR2(3) | Y |  | ????3_订单行号3 | DB注释(中文) |
| 51 | PLATE_DGN_QTY3 | NUMBER | Y |  | PLATE????3_PLATE设计支数3 | DB注释(中文) |
| 52 | PLATE_OR_QTY3 | NUMBER | Y |  | ??OverRoll??3_设计OverRoll支数3 | DB注释(中文) |
| 53 | PLATE_DGN_WTH3 | NUMBER | Y |  | PLATE???3_PLATE设计宽度3 | DB注释(中文) |
| 54 | PLATE_DGN_LTH3 | NUMBER | Y |  | PLATE????3_PLATE设计长度3 | DB注释(中文) |
| 55 | PLATE_DGN_WGT3 | NUMBER | Y |  | PLATE????3_PLATE设计重量3 | DB注释(中文) |
| 56 | ORD_NO4 | VARCHAR2(10) | Y |  | ????4_订单编号4 | DB注释(中文) |
| 57 | ORD_LN4 | VARCHAR2(3) | Y |  | ????4_订单行号4 | DB注释(中文) |
| 58 | PLATE_DGN_QTY4 | NUMBER | Y |  | PLATE????4_PLATE设计支数4 | DB注释(中文) |
| 59 | PLATE_OR_QTY4 | NUMBER | Y |  | ??OverRoll??4_设计OverRoll支数4 | DB注释(中文) |
| 60 | PLATE_DGN_WTH4 | NUMBER | Y |  | PLATE???4_PLATE设计宽度4 | DB注释(中文) |
| 61 | PLATE_DGN_LTH4 | NUMBER | Y |  | PLATE????4_PLATE设计长度4 | DB注释(中文) |
| 62 | PLATE_DGN_WGT4 | NUMBER | Y |  | PLATE????4_PLATE设计重量4 | DB注释(中文) |
| 63 | ORD_NO5 | VARCHAR2(10) | Y |  | ????5_订单编号5 | DB注释(中文) |
| 64 | ORD_LN5 | VARCHAR2(3) | Y |  | ????5_订单行号5 | DB注释(中文) |
| 65 | PLATE_DGN_QTY5 | NUMBER | Y |  | PLATE????5_PLATE设计支数5 | DB注释(中文) |
| 66 | PLATE_OR_QTY5 | NUMBER | Y |  | ??OverRoll??5_设计OverRoll支数5 | DB注释(中文) |
| 67 | PLATE_DGN_WTH5 | NUMBER | Y |  | PLATE???5_PLATE设计宽度5 | DB注释(中文) |
| 68 | PLATE_DGN_LTH5 | NUMBER | Y |  | PLATE????5_PLATE设计长度5 | DB注释(中文) |
| 69 | PLATE_DGN_WGT5 | NUMBER | Y |  | PLATE????5_PLATE设计重量5 | DB注释(中文) |
| 70 | ORD_NO6 | VARCHAR2(10) | Y |  | ????6_订单编号6 | DB注释(中文) |
| 71 | ORD_LN6 | VARCHAR2(3) | Y |  | ????6_订单行号6 | DB注释(中文) |
| 72 | PLATE_DGN_QTY6 | NUMBER | Y |  | PLATE????6_PLATE设计支数6 | DB注释(中文) |
| 73 | PLATE_OR_QTY6 | NUMBER | Y |  | ??OverRoll??6_设计OverRoll支数6 | DB注释(中文) |
| 74 | PLATE_DGN_WTH6 | NUMBER | Y |  | PLATE???6_PLATE设计宽度6 | DB注释(中文) |
| 75 | PLATE_DGN_LTH6 | NUMBER | Y |  | PLATE????6_PLATE设计长度6 | DB注释(中文) |
| 76 | PLATE_DGN_WGT6 | NUMBER | Y |  | PLATE????6_PLATE设计重量6 | DB注释(中文) |
| 77 | SMP_NO | VARCHAR2(14) | Y |  | Sampling No_试样编号 | DB注释(中文) |
| 78 | SMP_LTH_LOC | VARCHAR2(1) | Y |  | Test Item LengthDirSampling Loc(Sampling Gather  Loc)_试样采取位置 | DB注释(中文) |
| 79 | TEST_CNT | NUMBER | Y |  | Test CNT_试验回数 | DB注释(中文) |
| 80 | HRL_MFC_STD_NO | VARCHAR2(11) | Y |  | Manufacturing standard marks of HR_热间制造标准编号 | DB注释(中文) |
| 81 | PLT_RF_HOLDING_TIME_MAX | NUMBER | Y |  | ????????_铸坯在炉时间上限 | DB注释(中文) |
| 82 | PLT_RF_HOLDING_TIME_MIN | NUMBER | Y |  | ????????_铸坯在炉时间下限 | DB注释(中文) |
| 83 | PLT_RF_HOLDING_TIME_AIM | NUMBER | Y |  | ????????_铸坯在炉时间目标 | DB注释(中文) |
| 84 | PLT_RF_EXT_TEMP_MAX | NUMBER | Y |  | ?? ??????_铸坯出炉温度上限 | DB注释(中文) |
| 85 | PLT_RF_EXT_TEMP_MIN | NUMBER | Y |  | ?? ??????_铸坯出炉温度下限 | DB注释(中文) |
| 86 | PLT_RF_EXT_TEMP_AIM | NUMBER | Y |  | ?? ??????_铸坯出炉温度目标 | DB注释(中文) |
| 87 | PLT_THK_AIM | NUMBER | Y |  | Thick Plate Aimming Thickness_厚板热轧目标厚度 | DB注释(中文) |
| 88 | PLT_WTH_AIM | NUMBER | Y |  | Thick Plate Aimming Width_厚板热轧目标宽度 | DB注释(中文) |
| 89 | PLT_WTH_TOL_MIN | NUMBER | Y |  | Width Tolerance Min_厚板热轧宽度公差下限值 | DB注释(中文) |
| 90 | PLT_WTH_TOL_MAX | NUMBER | Y |  | Width Tolerance  Max_厚板热轧宽度公差上限值 | DB注释(中文) |
| 91 | PLT_THK_TOL_MIN | NUMBER | Y |  | Thickness Tolerance Min_厚板热轧厚度公差下限值 | DB注释(中文) |
| 92 | PLT_THK_TOL_MAX | NUMBER | Y |  | Thickness Tolerance  Max_厚板热轧厚度公差上限值 | DB注释(中文) |
| 93 | ORD_SIZE_TY | VARCHAR2(1) | Y |  | Type of Order size_订单尺寸类型 | DB注释(中文) |
| 94 | ORD_WTH_MAX | NUMBER | Y |  | Maximum of Order width_订单宽度上限 | DB注释(中文) |
| 95 | ORD_LTH_MAX | NUMBER | Y |  | Maximumof Order length _订单长度上限 | DB注释(中文) |
| 96 | ORD_LTH_TOL_CD | VARCHAR2(1) | Y |  | Order length Tolerance Code_订单长度允许偏差代码 | DB注释(中文) |
| 97 | ORD_LTH_TOL_MIN | NUMBER | Y |  | Order length Ninimum Tolerance Value_订单长度允许偏差下限 | DB注释(中文) |
| 98 | ORD_LTH_TOL_MAX | NUMBER | Y |  | Order length Maximum Tolerance Value_订单长度允许偏差上限 | DB注释(中文) |
| 99 | ORD_PLT_CD | VARCHAR2(1) | Y |  | Order Plant Code_生产工厂分类 | DB注释(中文) |
| 100 | ORD_EDGE_TY | VARCHAR2(1) | Y |  | Order Edge Type_订单Edge区分 | DB注释(中文) |
| 101 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  | Steel Grade_炼钢内控钢种编号 | DB注释(中文) |
| 102 | SPEC_CD | VARCHAR2(50) | Y |  | Specification Code_国家标准牌号 | DB注释(中文) |
| 103 | SLAB_NO | VARCHAR2(50) | Y |  | Slab No_Slab号 | DB注释(中文) |
| 104 | CAST_STR_NO | VARCHAR2(1) | Y |  | Caster Strand No_铸造Strand号 | DB注释(中文) |
| 105 | SLAB_STS | VARCHAR2(1) | Y |  | Slab Status_Slab状态 | DB注释(中文) |
| 106 | SLAB_THK | NUMBER | Y |  | Slab Thickness_Slab厚度 | DB注释(中文) |
| 107 | SLAB_WTH | NUMBER | Y |  | Slab Width_Slab宽度 | DB注释(中文) |
| 108 | SLAB_LTH | NUMBER | Y |  | Slab Length_Slab长度 | DB注释(中文) |
| 109 | SLAB_WGT | NUMBER | Y |  | Slab Weight_Slab重量 | DB注释(中文) |
| 110 | CONF_PASS_PLANT_OP_CD | VARCHAR2(60) | Y |  | ??????????_确定通过工厂工序代码 | DB注释(中文) |
| 111 | QLT_HCR_FL | VARCHAR2(1) | Y |  | ????HCR??_质量设计HCR分类 | DB注释(中文) |
| 112 | PLT_HEATING_CD | VARCHAR2(1) | Y |  | ?????????_热处理方法代码 | DB注释(中文) |
| 113 | UST_MTH_CD | VARCHAR2(2) | Y |  | UST Method Code_UST方法代码 | DB注释(中文) |
| 114 | GAS_CUT_FL | VARCHAR2(1) | Y |  | GAS????_GAS切斷分类 | DB注释(中文) |
| 115 | PLT_1COOL_CD | VARCHAR2(1) | Y |  | M43_????_M43_冷却模式 | DB注释(中文) |
| 116 | HIGH_SURF_FL | VARCHAR2(1) | Y |  | Hight Surface Flag_厚板高表面与否 | DB注释(中文) |
| 117 | PLT_FLAT_AIM | NUMBER | Y |  | Symmetric Flatness Target (Cold Value)_厚板高平直度 | DB注释(中文) |
| 118 | RJT_CAUSE_CD | VARCHAR2(2) | Y |  | Reject Cause Code_缺号原因代码 | DB注释(中文) |
| 119 | SPEC_RTN_CD | VARCHAR2(2) | Y |  | Spec Return Code_计划返送代码 | DB注释(中文) |
| 120 | FAC_CD | VARCHAR2(1) | Y |  | Factory Code_工厂代码 | DB注释(中文) |
| 121 | ROLL_UNIT_INST_SEQ | NUMBER | Y |  | Roll Unit Instruction SEQ_热轧计划工序代码 | DB注释(中文) |
| 122 | TE_PRD_FL | VARCHAR2(1) | Y |  | Test Production Flag_Test Production Flag | DB注释(非中文) |
| 123 | SAVE_FL | VARCHAR2(1) | Y |  | ????_储藏区分 | DB注释(中文) |
| 124 | HEAT_NO | VARCHAR2(50) | Y |  | Heat No_Heat号 | DB注释(中文) |
| 125 | CUT_POINT1 | NUMBER | Y |  | ??CUTTING POINT1_突发CUTTING POINT1 | DB注释(中文) |
| 126 | CUT_POINT2 | NUMBER | Y |  | ??CUTTING POINT2_突发CUTTING POINT2 | DB注释(中文) |
| 127 | CUT_POINT3 | NUMBER | Y |  | ??CUTTING POINT3_突发CUTTING POINT3 | DB注释(中文) |
| 128 | CUT_POINT4 | NUMBER | Y |  | ??CUTTING POINT4_突发CUTTING POINT4 | DB注释(中文) |
| 129 | CUT_POINT5 | NUMBER | Y |  | ??CUTTING POINT5_突发CUTTING POINT5 | DB注释(中文) |
| 130 | CUT_POINT6 | NUMBER | Y |  | ??CUTTING POINT6_突发CUTTING POINT6 | DB注释(中文) |
| 131 | CUT_POINT7 | NUMBER | Y |  | ??CUTTING POINT7_突发CUTTING POINT7 | DB注释(中文) |
| 132 | CUT_POINT8 | NUMBER | Y |  | ??CUTTING POINT8_突发CUTTING POINT8 | DB注释(中文) |
| 133 | CUT_POINT9 | NUMBER | Y |  | ??CUTTING POINT9_突发CUTTING POINT9 | DB注释(中文) |
| 134 | CUT_POINT10 | NUMBER | Y |  | ??CUTTING POINT10_突发CUTTING POINT10 | DB注释(中文) |
| 135 | CUT_POINT11 | NUMBER | Y |  | ??CUTTING POINT11_突发CUTTING POINT11 | DB注释(中文) |
| 136 | CUT_POINT12 | NUMBER | Y |  | ??CUTTING POINT12_突发CUTTING POINT12 | DB注释(中文) |
| 137 | CUT_POINT13 | NUMBER | Y |  | ??CUTTING POINT13_突发CUTTING POINT13 | DB注释(中文) |
| 138 | CUT_POINT14 | NUMBER | Y |  | ??CUTTING POINT14_突发CUTTING POINT14 | DB注释(中文) |
| 139 | CUT_POINT15 | NUMBER | Y |  | ??CUTTING POINT15_突发CUTTING POINT15 | DB注释(中文) |
| 140 | CUT_POINT16 | NUMBER | Y |  | ??CUTTING POINT16_突发CUTTING POINT16 | DB注释(中文) |
| 141 | CUT_POINT17 | NUMBER | Y |  | ??CUTTING POINT17_突发CUTTING POINT17 | DB注释(中文) |
| 142 | CUT_POINT18 | NUMBER | Y |  | ??CUTTING POINT18_突发CUTTING POINT18 | DB注释(中文) |
| 143 | CUT_POINT19 | NUMBER | Y |  | ??CUTTING POINT19_突发CUTTING POINT19 | DB注释(中文) |
| 144 | CUT_POINT20 | NUMBER | Y |  | ??CUTTING POINT20_突发CUTTING POINT20 | DB注释(中文) |
| 145 | CUT_POINT21 | NUMBER | Y |  | ??CUTTING POINT21_突发CUTTING POINT21 | DB注释(中文) |
| 146 | CUT_POINT22 | NUMBER | Y |  | ??CUTTING POINT22_突发CUTTING POINT22 | DB注释(中文) |
| 147 | CUT_POINT23 | NUMBER | Y |  | ??CUTTING POINT23_突发CUTTING POINT23 | DB注释(中文) |
| 148 | CUT_POINT24 | NUMBER | Y |  | ??CUTTING POINT24_突发CUTTING POINT24 | DB注释(中文) |
| 149 | CUT_POINT25 | NUMBER | Y |  | ??CUTTING POINT25_突发CUTTING POINT25 | DB注释(中文) |
| 150 | NPLATE_CUTTING_CNT | NUMBER | Y |  | ?????_原板分割支数 | DB注释(中文) |
| 151 | NPLATE_CUTTING_LTH1 | NUMBER | Y |  | ??????1_原板分割长度1 | DB注释(中文) |
| 152 | NPLATE_CUTTING_LTH2 | NUMBER | Y |  | ??????2_原板分割长度2 | DB注释(中文) |
| 153 | NPLATE_CUTTING_LTH3 | NUMBER | Y |  | ??????3_原板分割长度3 | DB注释(中文) |
| 154 | NPLATE_CUTTING_LTH4 | NUMBER | Y |  | ??????4_原板分割长度4 | DB注释(中文) |
| 155 | NPLATE_CUTTING_LTH5 | NUMBER | Y |  | ??????5_原板分割长度5 | DB注释(中文) |
| 156 | NPLATE_CUTTING_LTH6 | NUMBER | Y |  | ??????6_原板分割长度6 | DB注释(中文) |
| 157 | NPLATE_CUTTING_LTH7 | NUMBER | Y |  | ??????7_原板分割长度7 | DB注释(中文) |
| 158 | NPLATE_CUTTING_LTH8 | NUMBER | Y |  | ??????8_原板分割长度8 | DB注释(中文) |
| 159 | NPLATE_CUTTING_LTH9 | NUMBER | Y |  | ??????9_原板分割长度9 | DB注释(中文) |
| 160 | NPLATE_CUTTING_LTH10 | NUMBER | Y |  | ??????10_原板分割长度10 | DB注释(中文) |
| 161 | NPLATE_CUTTING_LTH11 | NUMBER | Y |  | ??????11_原板分割长度11 | DB注释(中文) |
| 162 | PLT_YIELD | NUMBER | Y |  | 成材率% | DB注释(中文) |
| 163 | ROLL_MOD | VARCHAR2(1) | Y |  | 轧制模式(1、平轧+卷轧，2、平轧，3、预留卷取机卷曲) | DB注释(中文) |
| 164 | ID_PIECE | VARCHAR2(18) | Y |  | 二级主键YYYYMMDDHHHHFFCCCC | DB注释(中文) |
| 165 | PLAN_DESC | VARCHAR2(300) | Y |  | 计划备注 | DB注释(中文) |
| 166 | PDI_COOL_CD | VARCHAR2(1) | Y |  | PDI水冷模式 | DB注释(中文) |
| 167 | PQA_SEND_FLAG | VARCHAR2(1) | Y |  | 发送PQA标记 | DB注释(中文) |
| 168 | SPC_DESC | VARCHAR2(300) | Y |  | 特殊质量要求 | DB注释(中文) |
| 169 | ORD_NO7 | VARCHAR2(10) | Y |  | ????6_订单编号6 | DB注释(中文) |
| 170 | ORD_LN7 | VARCHAR2(3) | Y |  | ????6_订单行号6 | DB注释(中文) |
| 171 | PLATE_DGN_QTY7 | NUMBER | Y |  | PLATE????6_PLATE设计支数6 | DB注释(中文) |
| 172 | PLATE_OR_QTY7 | NUMBER | Y |  | ??OverRoll??6_设计OverRoll支数6 | DB注释(中文) |
| 173 | PLATE_DGN_WTH7 | NUMBER | Y |  | PLATE???6_PLATE设计宽度6 | DB注释(中文) |
| 174 | PLATE_DGN_LTH7 | NUMBER | Y |  | PLATE????6_PLATE设计长度6 | DB注释(中文) |
| 175 | PLATE_DGN_WGT7 | NUMBER | Y |  | PLATE????6_PLATE设计重量6 | DB注释(中文) |
| 176 | ORD_NO8 | VARCHAR2(10) | Y |  | ????6_订单编号6 | DB注释(中文) |
| 177 | ORD_LN8 | VARCHAR2(3) | Y |  | ????6_订单行号6 | DB注释(中文) |
| 178 | PLATE_DGN_QTY8 | NUMBER | Y |  | PLATE????6_PLATE设计支数6 | DB注释(中文) |
| 179 | PLATE_OR_QTY8 | NUMBER | Y |  | ??OverRoll??6_设计OverRoll支数6 | DB注释(中文) |
| 180 | PLATE_DGN_WTH8 | NUMBER | Y |  | PLATE???6_PLATE设计宽度6 | DB注释(中文) |
| 181 | PLATE_DGN_LTH8 | NUMBER | Y |  | PLATE????6_PLATE设计长度6 | DB注释(中文) |
| 182 | PLATE_DGN_WGT8 | NUMBER | Y |  | PLATE????6_PLATE设计重量6 | DB注释(中文) |
| 183 | ORD_NO9 | VARCHAR2(10) | Y |  | ????6_订单编号6 | DB注释(中文) |
| 184 | ORD_LN9 | VARCHAR2(3) | Y |  | ????6_订单行号6 | DB注释(中文) |
| 185 | PLATE_DGN_QTY9 | NUMBER | Y |  | PLATE????6_PLATE设计支数6 | DB注释(中文) |
| 186 | PLATE_OR_QTY9 | NUMBER | Y |  | ??OverRoll??6_设计OverRoll支数6 | DB注释(中文) |
| 187 | PLATE_DGN_WTH9 | NUMBER | Y |  | PLATE???6_PLATE设计宽度6 | DB注释(中文) |
| 188 | PLATE_DGN_LTH9 | NUMBER | Y |  | PLATE????6_PLATE设计长度6 | DB注释(中文) |
| 189 | PLATE_DGN_WGT9 | NUMBER | Y |  | PLATE????6_PLATE设计重量6 | DB注释(中文) |
| 190 | PLT_COOL_FSH_TEMP_AIM | NUMBER | Y |  | 终冷温度目标 | DB注释(中文) |
| 191 | PLT_COOL_ST_TEMP_AIM | NUMBER | Y |  | 开冷温度目标 | DB注释(中文) |
| 192 | BATCH_CD | VARCHAR2(20) | Y |  | 批次 | DB注释(中文) |
| 193 | IS_MAIN_BATCH | NUMBER | Y |  | 是否是代表批次信息0 代表批次，1非代表批次 | DB注释(中文) |
| 194 | BATCH_ROLL_PRI | NUMBER | Y |  | 批次轧制顺序 | DB注释(中文) |
| 195 | PLAN_SEND_FL | VARCHAR2(1) | Y |  | 发送计划标记 | DB注释(中文) |
| 196 | CANCEL_YN | VARCHAR2(1) | Y |  | 是否可取消 | DB注释(中文) |
| 197 | DELIVERY_STATE | VARCHAR2(100) | Y |  | 交货状态 | DB注释(中文) |
| 198 | STEEL_GRD | VARCHAR2(100) | Y |  | 钢种 | DB注释(中文) |
| 199 | DC_LTH | VARCHAR2(100) | Y |  | 定尺长度 | DB注释(中文) |
| 200 | DAN_HAO | NUMBER | Y |  | 单号 | DB注释(中文) |
| 201 | FCE_NO | VARCHAR2(100) | Y |  | 上料炉号 | DB注释(中文) |
| 202 | MPLATE_NO_L2 | VARCHAR2(100) | Y |  | 二级模板号 | DB注释(中文) |

### SSM_STECKEL

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=81｜被读 67 过程 / 被写 7 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：60　**主键**：PLT_NO　**语义覆盖**：212/241

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | PLT_NO | VARCHAR2(15) | N | ✓ | ??? | DB注释(非中文) |
| 9 | MTL_NO | VARCHAR2(15) | Y |  | ??? | DB注释(非中文) |
| 10 | L2_PLT_NO | VARCHAR2(18) | Y |  | L2??? | DB注释(非中文) |
| 11 | PLT_TY | VARCHAR2(1) | Y |  | PLATE?? | DB注释(非中文) |
| 12 | FAC_CD | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 13 | PLT_STS_CD | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 14 | PLT_OPER_TRK_CD | VARCHAR2(3) | Y |  | ??Tracking?? | DB注释(非中文) |
| 15 | PROC_CD | VARCHAR2(3) | Y |  | ???? | DB注释(非中文) |
| 16 | NXT_PROC_CD | VARCHAR2(3) | Y |  | ?????? | DB注释(非中文) |
| 17 | PROG_CD | VARCHAR2(4) | Y |  | ???? | DB注释(非中文) |
| 18 | PREV_PROG_CD | VARCHAR2(4) | Y |  | ????? | DB注释(非中文) |
| 19 | STR_LOC_CD | VARCHAR2(9) | Y |  | Location Code | DB注释(非中文) |
| 20 | STR_LOC_WK_DTM | VARCHAR2(14) | Y |  | Current Location Updated Date | DB注释(非中文) |
| 21 | PLT_THK | NUMBER | Y |  | ???? | DB注释(非中文) |
| 22 | PLT_WTH | NUMBER | Y |  | ???? | DB注释(非中文) |
| 23 | PLT_LTH | NUMBER | Y |  | ???? | DB注释(非中文) |
| 24 | PLT_WGT | NUMBER | Y |  | ???? | DB注释(非中文) |
| 25 | MSU_THK | NUMBER | Y |  | ???? | DB注释(非中文) |
| 26 | MSU_WTH | NUMBER | Y |  | ???? | DB注释(非中文) |
| 27 | MSU_LTH | NUMBER | Y |  | ???? | DB注释(非中文) |
| 28 | MSU_WGT | NUMBER | Y |  | ???? | DB注释(非中文) |
| 29 | SLAB_NO | VARCHAR2(12) | Y |  | ??? | DB注释(非中文) |
| 30 | HEAT_NO | VARCHAR2(9) | Y |  | MES?? | DB注释(非中文) |
| 31 | ROLL_UNIT | VARCHAR2(10) | Y |  | ???? | DB注释(非中文) |
| 32 | ROLL_UNIT_PRI | NUMBER | Y |  | ??????? | DB注释(非中文) |
| 33 | PLAN_PASS_PROC | VARCHAR2(60) | Y |  | ?????? | DB注释(非中文) |
| 34 | RSLT_PASS_PROC | VARCHAR2(60) | Y |  | ?????? | DB注释(非中文) |
| 35 | REM_PASS_PROC | VARCHAR2(60) | Y |  | ???? | DB注释(非中文) |
| 36 | PLT_DIR_CD | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 37 | HOT_MFC_STD_NO | VARCHAR2(11) | Y |  | Hot Manufacture Standard NO | DB注释(非中文) |
| 38 | PLT_COOL_CD | VARCHAR2(1) | Y |  | ?????? | DB注释(非中文) |
| 39 | PLT_HEATING_CD | VARCHAR2(1) | Y |  | ?????_?? | DB注释(非中文) |
| 40 | HTM_MTH_CD | VARCHAR2(1) | Y |  | ?????_?? | DB注释(非中文) |
| 41 | UST_MTH_CD | VARCHAR2(2) | Y |  | UST?? | DB注释(非中文) |
| 42 | UST_STD_CD | VARCHAR2(200) | Y |  | ???????? | DB注释(非中文) |
| 43 | CUT_MTH_CD | VARCHAR2(1) | Y |  | ?????? | DB注释(非中文) |
| 44 | FCE_CH_DTM | VARCHAR2(14) | Y |  | ????????? | DB注释(非中文) |
| 45 | FCE_DISCH_DTM | VARCHAR2(14) | Y |  | ????????? | DB注释(非中文) |
| 46 | RLG_STA_DTM | VARCHAR2(14) | Y |  | ???????? | DB注释(非中文) |
| 47 | RLG_END_DTM | VARCHAR2(14) | Y |  | ???????? | DB注释(非中文) |
| 48 | RLG_SUMUP_DT | VARCHAR2(8) | Y |  | ??SUMUP?? | DB注释(非中文) |
| 49 | CS_CUT_YN | VARCHAR2(1) | Y |  | CS?? | DB注释(非中文) |
| 50 | DSTS_CUT_YN | VARCHAR2(1) | Y |  | DSTS?? | DB注释(非中文) |
| 51 | DS_CUT_YN | VARCHAR2(1) | Y |  | DS?? | DB注释(非中文) |
| 52 | FC_CUT_YN | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 53 | FIN_STA_DTM | VARCHAR2(14) | Y |  | ???????? | DB注释(非中文) |
| 54 | FIN_END_DTM | VARCHAR2(14) | Y |  | ???????? | DB注释(非中文) |
| 55 | FIN_SUMUP_DT | VARCHAR2(8) | Y |  | ??SUMUP?? | DB注释(非中文) |
| 56 | UST_YN | VARCHAR2(1) | Y |  | UST???? | DB注释(非中文) |
| 57 | APPR_JDG_YN | VARCHAR2(1) | Y |  | ?????? | DB注释(非中文) |
| 58 | CPL_YN | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 59 | HTM_YN | VARCHAR2(1) | Y |  |  | 空 |
| 60 | HTM_CH_SEQ | NUMBER | Y |  | ??????? | DB注释(非中文) |
| 61 | HTM_PLAN_ROUTE | VARCHAR2(10) | Y |  | ????????? | DB注释(非中文) |
| 62 | HTM_RSLT_ROUTE | VARCHAR2(10) | Y |  | ????????? | DB注释(非中文) |
| 63 | HTM_REM_ROUTE | VARCHAR2(10) | Y |  | ??????? | DB注释(非中文) |
| 64 | HTM_INST_REQ_YN | VARCHAR2(1) | Y |  | ????????? | DB注释(非中文) |
| 65 | HTM_STA_DTM | VARCHAR2(14) | Y |  | ????????? | DB注释(非中文) |
| 66 | HTM_END_DTM | VARCHAR2(14) | Y |  | ????????? | DB注释(非中文) |
| 67 | HTM_SUMUP_DT | VARCHAR2(8) | Y |  | ???SUMUP?? | DB注释(非中文) |
| 68 | MARK_YN | VARCHAR2(1) | Y |  | Marking?? | DB注释(非中文) |
| 69 | MARK_DTM | VARCHAR2(14) | Y |  | Marking???? | DB注释(非中文) |
| 70 | PLT_COOL_END_YN | VARCHAR2(1) | Y |  | ???????? | DB注释(非中文) |
| 71 | PLT_COOL_END_DTM | VARCHAR2(14) | Y |  | ?????????? | DB注释(非中文) |
| 72 | PROD_WHS_DTM | VARCHAR2(14) | Y |  | ???? | DB注释(非中文) |
| 73 | PROD_WHS_SUMUP_DT | VARCHAR2(8) | Y |  | ???? | DB注释(非中文) |
| 74 | DLV_DTM | VARCHAR2(14) | Y |  | Shipment Date | DB注释(非中文) |
| 75 | ERP_TRANS_YN | VARCHAR2(1) | Y |  | ERP???? | DB注释(非中文) |
| 76 | ERP_TRANS_DTM | VARCHAR2(14) | Y |  | ERP?????? | DB注释(非中文) |
| 77 | WHS_INF_TP | VARCHAR2(1) | Y |  | Return Inbound  Type | DB注释(非中文) |
| 78 | RTN_PROC_TY | VARCHAR2(1) | Y |  | Return Type | DB注释(非中文) |
| 79 | RTN_DTM | VARCHAR2(14) | Y |  | Return Date | DB注释(非中文) |
| 80 | RTN_SUMUP_DT | VARCHAR2(8) | Y |  | Return Work Date | DB注释(非中文) |
| 81 | RTN_PROC_REASON_CD | VARCHAR2(2) | Y |  | Return Code | DB注释(非中文) |
| 82 | RTN_PROC_USER_ID | VARCHAR2(20) | Y |  | Return Charger | DB注释(非中文) |
| 83 | RTN_RLS_DTM | VARCHAR2(14) | Y |  | Return Release Date | DB注释(非中文) |
| 84 | RTN_RLS_CD | VARCHAR2(3) | Y |  | Return Release Code | DB注释(非中文) |
| 85 | RTN_RLS_SFT_TEAM | VARCHAR2(2) | Y |  | Return Release Shift Crew | DB注释(非中文) |
| 86 | RJT_OCR_LOC | VARCHAR2(2) | Y |  | ??LOCATION | DB注释(非中文) |
| 87 | RJT_DTM | VARCHAR2(14) | Y |  | ?????? | DB注释(非中文) |
| 88 | HOLD_YN | VARCHAR2(1) | Y |  | PLATE HOLD YN | DB注释(非中文) |
| 89 | WRK_DTM | VARCHAR2(14) | Y |  | ???? | DB注释(非中文) |
| 90 | SMP_YN | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 91 | SMP_NO | VARCHAR2(11) | Y |  | ??? | DB注释(非中文) |
| 92 | SMP_LTH_LOC | VARCHAR2(1) | Y |  | ??LOCATION | DB注释(非中文) |
| 93 | SMP_CUT_CNT | NUMBER | Y |  | ??COUNT | DB注释(非中文) |
| 94 | SMP_CUT_DTM | VARCHAR2(14) | Y |  | ?????? | DB注释(非中文) |
| 95 | PLT_JDG_YN | VARCHAR2(1) | Y |  | ?????? | DB注释(非中文) |
| 96 | SIZE_CHG_YN | VARCHAR2(1) | Y |  | SIZE Change?? | DB注释(非中文) |
| 97 | SIZE_CHG_DTM | VARCHAR2(14) | Y |  | SIZE Change???? | DB注释(非中文) |
| 98 | CHEM_GRD | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 99 | SIZE_GRD | VARCHAR2(1) | Y |  | SIZE??(Y/N) | DB注释(非中文) |
| 100 | SHAPE_GRD | VARCHAR2(1) | Y |  | ????(Y/N) | DB注释(非中文) |
| 101 | SURF_GRD | VARCHAR2(2) | Y |  | ????(FA_FD/SC) | DB注释(非中文) |
| 102 | WGT_GRD | VARCHAR2(2) | Y |  | ????(Y/N) | DB注释(非中文) |
| 103 | UST_GRD | VARCHAR2(1) | Y |  | ?????? | DB注释(非中文) |
| 104 | APPR_JDG_GRD | VARCHAR2(1) | Y |  | ?????? | DB注释(非中文) |
| 105 | APPR_JDG_DTM | VARCHAR2(14) | Y |  | ???????? | DB注释(非中文) |
| 106 | APPR_JDG_CNT | NUMBER | Y |  | ????COUNT | DB注释(非中文) |
| 107 | APPR_JDG_USER_ID | VARCHAR2(20) | Y |  | ????USER ID | DB注释(非中文) |
| 108 | PROD_TOT_JDG_GRD | VARCHAR2(2) | Y |  | ???????? | DB注释(非中文) |
| 109 | ABN_RSN_CD_APPR | VARCHAR2(3) | Y |  | ???????? | DB注释(非中文) |
| 110 | ABN_RSN_CD_MEC | VARCHAR2(3) | Y |  | ???????? | DB注释(非中文) |
| 111 | ABN_RSN_CD_CHEM | VARCHAR2(3) | Y |  | ???????? | DB注释(非中文) |
| 112 | ABN_RSN_CD_SMP | VARCHAR2(3) | Y |  | ??????????? | DB注释(非中文) |
| 113 | ERP_TRANS_STS_CD | VARCHAR2(1) | Y |  | ERP?????? | DB注释(非中文) |
| 114 | SCRAP_YN | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 115 | SPEC_CD | VARCHAR2(50) | Y |  | ?????? | DB注释(非中文) |
| 116 | STD_STLGRD | VARCHAR2(20) | Y |  | ?? | DB注释(非中文) |
| 117 | PROD_CD | VARCHAR2(3) | Y |  | ???? | DB注释(非中文) |
| 118 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  | ???????? | DB注释(非中文) |
| 119 | NATL_SPEC_YEAR | VARCHAR2(4) | Y |  | ???????? | DB注释(非中文) |
| 120 | NATL_SPEC_NO | VARCHAR2(40) | Y |  | ??????? | DB注释(非中文) |
| 121 | SEMI_PROD_ITEM_CD | VARCHAR2(30) | Y |  | SEMI Production Item code | DB注释(非中文) |
| 122 | SALES_PROD_ITEM_CD | VARCHAR2(30) | Y |  | SALES Production Item code | DB注释(非中文) |
| 123 | SPL_REASON_CD | VARCHAR2(3) | Y |  | ?????? | DB注释(非中文) |
| 124 | HCR_FL | VARCHAR2(1) | Y |  | HCR FLAG | DB注释(非中文) |
| 125 | ORD_FL | VARCHAR2(1) | Y |  | ????? | DB注释(非中文) |
| 126 | ORD_TY | VARCHAR2(2) | Y |  | ???? | DB注释(非中文) |
| 127 | ORD_EDGE_TY | VARCHAR2(1) | Y |  | ??Edge?? | DB注释(非中文) |
| 128 | ORD_USAGE | VARCHAR2(4) | Y |  | ?????? | DB注释(非中文) |
| 129 | ORD_NO | VARCHAR2(10) | Y |  | ??? | DB注释(非中文) |
| 130 | ORD_LN | VARCHAR2(3) | Y |  | ???? | DB注释(非中文) |
| 131 | PREV_ORD_FL | VARCHAR2(1) | Y |  | ?????? | DB注释(非中文) |
| 132 | PREV_ORD_TY | VARCHAR2(2) | Y |  | ????? | DB注释(非中文) |
| 133 | PREV_ORD_USAGE | VARCHAR2(4) | Y |  | ??????? | DB注释(非中文) |
| 134 | PREV_ORD_NO | VARCHAR2(10) | Y |  | ???? | DB注释(非中文) |
| 135 | PREV_ORD_LN | VARCHAR2(3) | Y |  | ????? | DB注释(非中文) |
| 136 | PREV_SPEC_CD | VARCHAR2(50) | Y |  | ??????? | DB注释(非中文) |
| 137 | ORD_ALLOC_TY | VARCHAR2(1) | Y |  | ?? ALLCATION TYPE | DB注释(非中文) |
| 138 | ORD_ALLOC_DTM | VARCHAR2(14) | Y |  | ?? ALLCATION ???? | DB注释(非中文) |
| 139 | ORD_THK | NUMBER | Y |  | ???? | DB注释(非中文) |
| 140 | ORD_WTH | NUMBER | Y |  | ???? | DB注释(非中文) |
| 141 | ORD_LTH | NUMBER | Y |  | ???? | DB注释(非中文) |
| 142 | ORD_WGT | NUMBER | Y |  | ???? | DB注释(非中文) |
| 143 | ORD_NO1 | VARCHAR2(10) | Y |  | ???1 | DB注释(非中文) |
| 144 | ORD_LN1 | VARCHAR2(3) | Y |  | ????1 | DB注释(非中文) |
| 145 | ORD_WTH1 | NUMBER | Y |  | ????1 | DB注释(非中文) |
| 146 | ORD_LTH1 | NUMBER | Y |  | ????1 | DB注释(非中文) |
| 147 | ORD_WGT1 | NUMBER | Y |  | ????1 | DB注释(非中文) |
| 148 | ORD_PLT_PCS1 | NUMBER | Y |  | ?????1 | DB注释(非中文) |
| 149 | ORD_NO2 | VARCHAR2(10) | Y |  | ???2 | DB注释(非中文) |
| 150 | ORD_LN2 | VARCHAR2(3) | Y |  | ????2 | DB注释(非中文) |
| 151 | ORD_WTH2 | NUMBER | Y |  | ????2 | DB注释(非中文) |
| 152 | ORD_LTH2 | NUMBER | Y |  | ????2 | DB注释(非中文) |
| 153 | ORD_WGT2 | NUMBER | Y |  | ????2 | DB注释(非中文) |
| 154 | ORD_PLT_PCS2 | NUMBER | Y |  | ?????2 | DB注释(非中文) |
| 155 | ORD_NO3 | VARCHAR2(10) | Y |  | ???3 | DB注释(非中文) |
| 156 | ORD_LN3 | VARCHAR2(3) | Y |  | ????3 | DB注释(非中文) |
| 157 | ORD_WTH3 | NUMBER | Y |  | ????3 | DB注释(非中文) |
| 158 | ORD_LTH3 | NUMBER | Y |  | ????3 | DB注释(非中文) |
| 159 | ORD_WGT3 | NUMBER | Y |  | ????3 | DB注释(非中文) |
| 160 | ORD_PLT_PCS3 | NUMBER | Y |  | ?????3 | DB注释(非中文) |
| 161 | ORD_NO4 | VARCHAR2(10) | Y |  | ???4 | DB注释(非中文) |
| 162 | ORD_LN4 | VARCHAR2(3) | Y |  | ????4 | DB注释(非中文) |
| 163 | ORD_WTH4 | NUMBER | Y |  | ????4 | DB注释(非中文) |
| 164 | ORD_LTH4 | NUMBER | Y |  | ????4 | DB注释(非中文) |
| 165 | ORD_WGT4 | NUMBER | Y |  | ????4 | DB注释(非中文) |
| 166 | ORD_PLT_PCS4 | NUMBER | Y |  | ?????4 | DB注释(非中文) |
| 167 | ORD_NO5 | VARCHAR2(10) | Y |  | ???5 | DB注释(非中文) |
| 168 | ORD_LN5 | VARCHAR2(3) | Y |  | ????5 | DB注释(非中文) |
| 169 | ORD_WTH5 | NUMBER | Y |  | ????5 | DB注释(非中文) |
| 170 | ORD_LTH5 | NUMBER | Y |  | ????5 | DB注释(非中文) |
| 171 | ORD_WGT5 | NUMBER | Y |  | ????5 | DB注释(非中文) |
| 172 | ORD_PLT_PCS5 | NUMBER | Y |  | ?????5 | DB注释(非中文) |
| 173 | ORD_NO6 | VARCHAR2(10) | Y |  | ???6 | DB注释(非中文) |
| 174 | ORD_LN6 | VARCHAR2(3) | Y |  | ????6 | DB注释(非中文) |
| 175 | ORD_WTH6 | NUMBER | Y |  | ????6 | DB注释(非中文) |
| 176 | ORD_LTH6 | NUMBER | Y |  | ????6 | DB注释(非中文) |
| 177 | ORD_WGT6 | NUMBER | Y |  | ????6 | DB注释(非中文) |
| 178 | ORD_PLT_PCS6 | NUMBER | Y |  | ?????6 | DB注释(非中文) |
| 179 | BUND_NO | VARCHAR2(12) | Y |  | ?? | DB注释(非中文) |
| 180 | BUND_SEQ | VARCHAR2(2) | Y |  | ???? | DB注释(非中文) |
| 181 | BUND_NO_YN | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 182 | BEF_BUND_NO | VARCHAR2(12) | Y |  | ??? | DB注释(非中文) |
| 183 | SPR_BED_CD | VARCHAR2(9) | Y |  | ???? | DB注释(非中文) |
| 184 | LOT_NO | VARCHAR2(20) | Y |  | ?? | DB注释(非中文) |
| 185 | SLAB_LOC_WK_DTM | VARCHAR2(14) | Y |  | ?????? | DB注释(非中文) |
| 186 | GRP_NO | VARCHAR2(1) | Y |  | ?? | DB注释(非中文) |
| 187 | SFT_NO | VARCHAR2(1) | Y |  | ? | DB注释(非中文) |
| 188 | SIZE_CHG_USER_ID | VARCHAR2(20) | Y |  | ????ID | DB注释(非中文) |
| 189 | GRIND_YN | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 190 | AVG_SLAB_WGT | NUMBER | Y |  | ????? | DB注释(非中文) |
| 191 | TRANS_FG_PLT | VARCHAR2(2) | Y |  |  | 空 |
| 192 | TRANS_REQ_DTM | VARCHAR2(14) | Y |  | Transfer Request Datetime | DB注释(非中文) |
| 193 | TRANS_REQ_USER_ID | VARCHAR2(20) | Y |  | Transfer Request User ID | DB注释(非中文) |
| 194 | TRANS_ACCT_REF_DTM | VARCHAR2(14) | Y |  | Transfer Accept Datetime | DB注释(非中文) |
| 195 | TRANS_ACCT_REF_USER_ID | VARCHAR2(20) | Y |  | Transfer Accept User ID | DB注释(非中文) |
| 196 | L2_PLT_SEQ | VARCHAR2(200) | Y |  | L2??? | DB注释(非中文) |
| 197 | BUND_USER_ID | VARCHAR2(20) | Y |  | ??ID | DB注释(非中文) |
| 198 | HTM_NO | VARCHAR2(8) | Y |  | ???? | DB注释(非中文) |
| 199 | PLT_YIELD | VARCHAR2(8) | Y |  |  | 空 |
| 200 | OVER_ORD_FL | VARCHAR2(1) | Y |  |  | 空 |
| 201 | HTM_SAVE_FL | VARCHAR2(1) | Y |  | 挽救标识 | SCO_DATA_DIC(L) |
| 202 | ROLL_WAY | VARCHAR2(10) | Y |  | ???? | DB注释(非中文) |
| 203 | HTM_BUND_DTM | VARCHAR2(14) | Y |  | ??????? | DB注释(非中文) |
| 204 | FCE_CH_DIS_FL | VARCHAR2(1) | Y |  |  | 空 |
| 205 | ORD_SIZE_TY | VARCHAR2(1) | Y |  |  | 空 |
| 206 | ID_PIECE | VARCHAR2(18) | Y |  | ID PIECE | DB注释(非中文) |
| 207 | BUND_DTM | VARCHAR2(14) | Y |  | ???? | DB注释(非中文) |
| 208 | SPR_BED_CD2 | VARCHAR2(9) | Y |  | ????2 | DB注释(非中文) |
| 209 | PRODUCTION_LINE | VARCHAR2(2) | Y |  | ?? ?1.1????2.2??? | DB注释(非中文) |
| 210 | ORD_NOW_PCS1 | NUMBER | Y |  | ??1?? | DB注释(非中文) |
| 211 | ORD_NOW_PCS2 | NUMBER | Y |  |  | 空 |
| 212 | ORD_NOW_PCS3 | NUMBER | Y |  |  | 空 |
| 213 | ORD_NOW_PCS4 | NUMBER | Y |  |  | 空 |
| 214 | ORD_NOW_PCS5 | NUMBER | Y |  |  | 空 |
| 215 | ORD_NOW_PCS6 | NUMBER | Y |  |  | 空 |
| 216 | PREV_PLT_NO | VARCHAR2(15) | Y |  | ???? | DB注释(非中文) |
| 217 | ERP_TRANS_SEQ | VARCHAR2(2) | Y |  |  | 空 |
| 218 | ERP_TRANS_HTM_SEQ | VARCHAR2(2) | Y |  |  | 空 |
| 219 | ERP_TRANS_HTM_YN | VARCHAR2(1) | Y |  |  | 空 |
| 220 | ERP_TRANS_HTM_STS | VARCHAR2(1) | Y |  |  | 空 |
| 221 | FL | VARCHAR2(2) | Y |  |  | 空 |
| 222 | HTM_APPR_JDG_DTM | VARCHAR2(14) | Y |  | ??????? | DB注释(非中文) |
| 223 | QUALITY_LOCK | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 224 | HOLD_NAME | VARCHAR2(10) | Y |  | ???? | DB注释(非中文) |
| 225 | BUND_DTM_ONE | VARCHAR2(14) | Y |  |  | 空 |
| 226 | REP_YN | VARCHAR2(1) | Y |  | 대표여부 | SCO_DATA_DIC(D) |
| 227 | HOLD_RSN_CD_LOV | VARCHAR2(14) | Y |  | ???? | DB注释(非中文) |
| 228 | SPR_BED_CD4 | VARCHAR2(7) | Y |  |  | 空 |
| 229 | SPR_BED_CD3 | VARCHAR2(7) | Y |  |  | 空 |
| 230 | SPR_BED_CD1 | VARCHAR2(7) | Y |  |  | 空 |
| 231 | SPR_BED_CD5 | VARCHAR2(7) | Y |  |  | 空 |
| 232 | SPR_BED_CD6 | VARCHAR2(7) | Y |  |  | 空 |
| 233 | SPR_BED_CD7 | VARCHAR2(7) | Y |  |  | 空 |
| 234 | UST_REP_YN | VARCHAR2(1) | Y |  | US???? | DB注释(非中文) |
| 235 | ERP_WGT_ONE | NUMBER | Y |  |  | 空 |
| 236 | SQM_COMMENTS | VARCHAR2(200) | Y |  | 质量备注 | SCO_DATA_DIC(D) |
| 237 | QUALITY_LOCK_RSN | VARCHAR2(100) | Y |  |  | 空 |
| 238 | LOC_OUT_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 239 | LOC_REQ_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 240 | QUALITY_LOCK_USER | VARCHAR2(20) | Y |  |  | 空 |
| 241 | QUALITY_LOCK_DTM | VARCHAR2(14) | Y |  |  | 空 |

### SMS_RSLT_CUT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=81｜被读 61 过程 / 被写 10 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：52677　**主键**：CUT_SLAB_NO　**语义覆盖**：112/116

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | CUT_SLAB_NO | VARCHAR2(20) | N | ✓ | Uncond Slab No | DB注释(非中文) |
| 9 | PLAN_CUT_SLAB_NO | VARCHAR2(13) | Y |  | Plan uncond Slab No | DB注释(非中文) |
| 10 | PROC_MC_NO | VARCHAR2(1) | Y |  | Process Machine No | DB注释(非中文) |
| 11 | STR_NO | VARCHAR2(1) | Y |  | Strand No | DB注释(非中文) |
| 12 | HEAT_NO | VARCHAR2(10) | Y |  | Heat No | DB注释(非中文) |
| 13 | MOM_HEAT_NO | VARCHAR2(9) | Y |  | Include Heat No | DB注释(非中文) |
| 14 | MIXD_SLAB_HEAT_NO | VARCHAR2(9) | Y |  | Mixed Slab Heat No | DB注释(非中文) |
| 15 | CUT_SLAB_MIX_GRD_TY | VARCHAR2(1) | Y |  | Mixed Uncond Slab Y/N | DB注释(非中文) |
| 16 | CAST_IN_LD_STEEL_WGT | NUMBER | Y |  | Ladle Steel Weight in Casting | DB注释(非中文) |
| 17 | CUT_SLAB_THK | NUMBER | Y |  | Uncond Slab Thickness | DB注释(非中文) |
| 18 | CUT_SLAB_WTH | NUMBER | Y |  | Uncond Slab Width | DB注释(非中文) |
| 19 | CUT_SLAB_LTH | NUMBER | Y |  | Uncond slab Length | DB注释(非中文) |
| 20 | CUT_SLAB_WGT | NUMBER | Y |  | Uncond Slab Weight | DB注释(非中文) |
| 21 | CUT_END_DTM | VARCHAR2(14) | Y |  | Uncond Slab Cutting End Date | DB注释(非中文) |
| 22 | PROD_DT | VARCHAR2(8) | Y |  | Production date | DB注释(非中文) |
| 23 | CUT_SLAB_CONN_LTH | NUMBER | Y |  | Uncond Slab Connection Part Length | DB注释(非中文) |
| 24 | SLAB_CUT_POSIT_CD | VARCHAR2(1) | Y |  | slab assign type | DB注释(非中文) |
| 25 | ORD_FL | VARCHAR2(1) | Y |  | Order flag | DB注释(非中文) |
| 26 | ORD_NO | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 27 | ORD_LN | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 28 | SCARF_TY | VARCHAR2(1) | Y |  | Scarfing type | DB注释(非中文) |
| 29 | SMPING_TY | VARCHAR2(1) | Y |  | Sampling Type | DB注释(非中文) |
| 30 | TAPER_TY | VARCHAR2(1) | Y |  | Tapered Flag | DB注释(非中文) |
| 31 | CUT_SLAB_END_WTH | NUMBER | Y |  | Uncond Slab End Width | DB注释(非中文) |
| 32 | TD_AVG_TEMP | NUMBER | Y |  | Tundish Average Temperature | DB注释(非中文) |
| 33 | TD_STEEL_WGT | NUMBER | Y |  | Tundish Steel Weight | DB注释(非中文) |
| 34 | TD_SLID_NZ_MAX_OPEN | NUMBER | Y |  | Tundish Sliding Nozzle Maximum Open | DB注释(非中文) |
| 35 | TD_SLID_NZ_MIN_OPEN | NUMBER | Y |  | Tundish Sliding Nozzle Minimum Open | DB注释(非中文) |
| 36 | TD_SLID_GATE_OPEN_QTY | NUMBER | Y |  | ???SlidingGate??? | DB注释(非中文) |
| 37 | MLD_LEVEL_GAP_MAX | NUMBER | Y |  | Mold Surface Max Variable Value | DB注释(非中文) |
| 38 | MLD_WIDE_IS_CW_QTY | NUMBER | Y |  | Mold Long Side Inside Cooling Water Quantity | DB注释(非中文) |
| 39 | MLD_WIDE_OS_CW_QTY | NUMBER | Y |  | Mold Long Side OutSide Cooling Water Quantity | DB注释(非中文) |
| 40 | MLD_NARW_LFT_CW_QTY | NUMBER | Y |  | Mold Short Side Left Cooling Water Quantity | DB注释(非中文) |
| 41 | MLD_NARW_RGT_CW_QTY | NUMBER | Y |  | Mold Short Side Right Cooling Water Quantity | DB注释(非中文) |
| 42 | MLD_WIDE_IS_CW_TEMP_DIFF | NUMBER | Y |  | Mold Long Side Insied Cooling Water Temperature Different | DB注释(非中文) |
| 43 | MLD_WIDE_OS_CW_TEMP_DIFF | NUMBER | Y |  | Mold Long Side Outside Cooling Water Temperature Different | DB注释(非中文) |
| 44 | MLD_NARW_LFT_CW_TEMP_DIFF | NUMBER | Y |  | Mold Short Side Left Cooling Water Temperature Different | DB注释(非中文) |
| 45 | MLD_NARW_RGT_CW_TEMP_DIFF | NUMBER | Y |  | Mold Short Side Right Cooling Water Temperature Different | DB注释(非中文) |
| 46 | CAST_MIN_SPD | NUMBER | Y |  | Casting Minimum Speed | DB注释(非中文) |
| 47 | CAST_MAX_SPD | NUMBER | Y |  | Casting Maximum Speed | DB注释(非中文) |
| 48 | CAST_AVG_SPD | NUMBER | Y |  | Casting Average Speed | DB注释(非中文) |
| 49 | CAST_IN_CAST_SPD_CHG_VAL | NUMBER | Y |  | Casting Speed Change value in Casting | DB注释(非中文) |
| 50 | LD_OPEN_PUR_YN | VARCHAR2(1) | Y |  | Ladle Open Puring Y/N | DB注释(非中文) |
| 51 | TD_DAM_BREAK_YN | VARCHAR2(1) | Y |  | Tundish Dam Break Y/N | DB注释(非中文) |
| 52 | SN_TORR_BTM_FAIL_YN | VARCHAR2(1) | Y |  | SEN Nozzle discharge holes Fail Yes/No | DB注释(非中文) |
| 53 | SN_OX_WASH_YN | VARCHAR2(1) | Y |  | Settled Nozzle Oxygen Wash Y/N | DB注释(非中文) |
| 54 | MLD_SURF_VORTEX_YN | VARCHAR2(1) | Y |  | Mold Surface Vortex Y/N | DB注释(非中文) |
| 55 | SH_NZ_AR_FLW_MAX | NUMBER | Y |  | Shroud Nozzle Ar Max Flow | DB注释(非中文) |
| 56 | SH_NZ_AR_PRS_MAX | NUMBER | Y |  | Shroud Nozzle Ar Max Pressure | DB注释(非中文) |
| 57 | TD_SN_AR_AVG_FLW | NUMBER | Y |  | Tundish SN Avg Ar Flow | DB注释(非中文) |
| 58 | TD_UP_NZ_AR_FLW_AVG | NUMBER | Y |  | Tundish Upper Nozzle Average Ar Flow | DB注释(非中文) |
| 59 | TD_UP_NZ_AR_PRS_AVG | NUMBER | Y |  | Tundish Upper Nozzle Ar Average flow Pressure | DB注释(非中文) |
| 60 | ENTRY_CW_TEMP | NUMBER | Y |  | Entry side 2nd Cooling water Temperature | DB注释(非中文) |
| 61 | CUT_SLAB_CALC_SUFR_TEMP | NUMBER | Y |  | Calculated Uncond Slab Surface Temperature | DB注释(非中文) |
| 62 | LST_SLAB_YN | VARCHAR2(1) | Y |  | Last Slab Y/N in a Heat | DB注释(非中文) |
| 63 | CUT_SLAB_LTH_CONT_RATE | NUMBER | Y |  | Uncond Slab Length Contraction Rate | DB注释(非中文) |
| 64 | CUT_SLAB_WTH_CONT_RATE | NUMBER | Y |  | Uncond Slab Length Contraction Rate Standard | DB注释(非中文) |
| 65 | ERP_POSTING_DTM | VARCHAR2(14) | Y |  | ERP Posting date | DB注释(非中文) |
| 66 | BY_PLAN_YN | VARCHAR2(1) | Y |  | Plan Y/N | DB注释(非中文) |
| 67 | CUT_SLAB_STA_WTH | NUMBER | Y |  | Uncond Slab Start Width | SCO_DATA_DIC(D) |
| 68 | CC_PLAN_NO | VARCHAR2(10) | Y |  | Production plan number | DB注释(非中文) |
| 69 | SLAB_CENTER_TEMP | NUMBER | Y |  | Calculated slab center temperature | DB注释(非中文) |
| 70 | SAMPLE_LTH | NUMBER | Y |  | Sample length | DB注释(非中文) |
| 71 | WEIGHT_ACT | NUMBER | Y |  | Actual weight from the weighing table | DB注释(非中文) |
| 72 | SLAB_SURF_QE_CD | NUMBER | Y |  | QE quality result - Surface | DB注释(非中文) |
| 73 | SLAB_IN_QE_CD | NUMBER | Y |  | QE quality result ? Internal | DB注释(非中文) |
| 74 | SLAB_PLAN_DEST | VARCHAR2(10) | Y |  | Planned destination from production plan | DB注释(非中文) |
| 75 | SLAB_FINAL_DEST | VARCHAR2(10) | Y |  | Reported from Discharge PLC | DB注释(非中文) |
| 76 | SLAB_RESULT_TY | VARCHAR2(1) | Y |  | Uncond Slab Result Type | DB注释(非中文) |
| 77 | CUT_SLAB_PROG_CD | VARCHAR2(1) | Y |  | Uncond Slab Progress code | DB注释(非中文) |
| 78 | STA_POS_WID_CHG | NUMBER | Y |  | Start Point of Width Change | DB注释(非中文) |
| 79 | END_POS_WID_CHG | NUMBER | Y |  | End Point of Width Change | DB注释(非中文) |
| 80 | PROD_ITEM_CD | VARCHAR2(30) | Y |  | Production Item Code | DB注释(非中文) |
| 81 | ERP_POSTING_YN | VARCHAR2(1) | Y |  | ERP Posting Y/N | DB注释(非中文) |
| 82 | ERP_TRANSACTION_TY | VARCHAR2(2) | Y |  | ERP Transaction Type | DB注释(非中文) |
| 83 | ERP_SUMUP_DT | VARCHAR2(14) | Y |  | Sumup Date | DB注释(非中文) |
| 84 | ERP_ORD_NO | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 85 | ERP_ORD_LN | VARCHAR2(3) | Y |  | Order Line No | DB注释(非中文) |
| 86 | ERP_ITEM_CD_PLAN | VARCHAR2(30) | Y |  | Item Code Plan | DB注释(非中文) |
| 87 | ERP_ITEM_CD | VARCHAR2(30) | Y |  | Item Code | DB注释(非中文) |
| 88 | ERP_PROD_QTY | NUMBER | Y |  | Product Quantity | DB注释(非中文) |
| 89 | ERP_PROD_SUB_INV_CD | VARCHAR2(2) | Y |  | Product Sub Inventory Code | DB注释(非中文) |
| 90 | ERP_MTRL_INPUT_ITEM_CD_01 | VARCHAR2(30) | Y |  | Input Item Code 01 | DB注释(非中文) |
| 91 | ERP_MTRL_INPUT_QTY_01 | NUMBER | Y |  | Input Quantity 01 | DB注释(非中文) |
| 92 | ERP_MTRL_INPUT_MTRL_NO_01 | VARCHAR2(22) | Y |  | Input Material No 01 | DB注释(非中文) |
| 93 | ERP_MTRL_INPUT_BYPROD_FL_01 | VARCHAR2(1) | Y |  | Input By-Product Flag 01 | DB注释(非中文) |
| 94 | ERP_MTRL_INPUT_SUB_INV_CD_01 | VARCHAR2(2) | Y |  | Input Sub Inventory Code 01 | DB注释(非中文) |
| 95 | ERP_MTRL_INPUT_PROC_CD_01 | VARCHAR2(3) | Y |  | Input Process Code 01 | DB注释(非中文) |
| 96 | ERP_PROC_CD_01 | VARCHAR2(3) | Y |  | Process Code 01 | DB注释(非中文) |
| 97 | ERP_RSC_USAGE_01 | NUMBER | Y |  | Resource Usage 01 | DB注释(非中文) |
| 98 | DMS_POSTING_YN | VARCHAR2(1) | Y |  |  | 空 |
| 99 | DMS_POSTING_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 100 | DMS_POSTING_TY | VARCHAR2(1) | Y |  |  | 空 |
| 101 | SLAB_CUT_POSIT_CD_DES | VARCHAR2(10) | Y |  | ?????? | DB注释(非中文) |
| 102 | UNSTEADY_GRD | VARCHAR2(10) | Y |  | ????? | DB注释(非中文) |
| 103 | PROJECT_NUMBER | VARCHAR2(150) | Y |  | ?????? | DB注释(非中文) |
| 104 | IS_BAD | VARCHAR2(1) | Y |  | 0:正常，1：作废 | DB注释(中文) |
| 105 | HEAT_SLAB_NO | VARCHAR2(13) | Y |  |  | 空 |
| 106 | CAST_RULE | NUMBER | Y |  | 定尺 | DB注释(中文) |
| 107 | MIX_CAST_SLAB | VARCHAR2(1) | Y |  | 混浇坯 | DB注释(中文) |
| 108 | HCR_FL | VARCHAR2(1) | Y |  | 热送 | DB注释(中文) |
| 109 | SLAB_INSP_RSLT | VARCHAR2(1) | Y |  | 板坯检查结果 | DB注释(中文) |
| 110 | SLAB_INSP_RSN | VARCHAR2(10) | Y |  | 板坯检查结果原因 | DB注释(中文) |
| 111 | SLAB_INSP_DTM | VARCHAR2(14) | Y |  | 表检结果记录人 | DB注释(中文) |
| 112 | DEFECT_CD | VARCHAR2(60) | Y |  | 缺陷代码 | DB注释(中文) |
| 113 | INSP_EMP_NO | VARCHAR2(20) | Y |  | Slab Inspection Employee No | DB注释(非中文) |
| 114 | IS_ABOLISH | VARCHAR2(1) | Y |  | 0:正常，1：作废 | DB注释(中文) |
| 115 | SLAB_SECTION | VARCHAR2(20) | Y |  | 断面 | DB注释(中文) |
| 116 | SLAB_ACT_LTH | NUMBER | Y |  | 实绩切割长度 | DB注释(中文) |

### SYD_MAP_LAYER

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=78｜被读 50 过程 / 被写 14 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：54658　**主键**：（无显式主键）　**语义覆盖**：14/14

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | 记录存档标志 | DB注释(中文) |
| 8 | YD_GR_TP | VARCHAR2(1) | Y |  | YD_GR_TP | DB注释(非中文) |
| 9 | YD_BED_CD | VARCHAR2(7) | Y |  | YD_BED_CD | DB注释(非中文) |
| 10 | YD_LAYER_NO | NUMBER | Y |  | YD_LAYER_NO | DB注释(非中文) |
| 11 | YD_LAYER_STS | VARCHAR2(1) | Y |  | YD_LAYER_STS | DB注释(非中文) |
| 12 | MTRL_NO | VARCHAR2(20) | Y |  | MTRL_NO | DB注释(非中文) |
| 13 | YD_BED_CD_BAK | VARCHAR2(1) | Y |  | 暂存垛位号 | DB注释(中文) |
| 14 | YD_LAYER_NO_BAK | VARCHAR2(7) | Y |  | 暂存层号 | DB注释(中文) |

### SQM_MECH_HEAD

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=78｜被读 62 过程 / 被写 8 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：18301　**主键**：SMP_NO　**语义覆盖**：45/45

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | SMP_NO | VARCHAR2(14) | N | ✓ | 试样编号 | DB注释(中文) |
| 9 | ORD_NO | VARCHAR2(10) | Y |  | 订单编号 | DB注释(中文) |
| 10 | ORD_LN | VARCHAR2(3) | Y |  | 订单行号 | DB注释(中文) |
| 11 | HEAT_NO | VARCHAR2(10) | Y |  | Heat编号 | DB注释(中文) |
| 12 | PLAN_HEAT_NO | VARCHAR2(10) | Y |  | 预期Heat编号 | DB注释(中文) |
| 13 | SLAB_NO | VARCHAR2(13) | Y |  | Slab编号 | DB注释(中文) |
| 14 | SMP_GTH_INST_MTRL_NO | VARCHAR2(20) | Y |  | 试样采取指示材料编号 | DB注释(中文) |
| 15 | ORD_THK | NUMBER | Y |  | 订单厚度 | DB注释(中文) |
| 16 | PROD_GRP | VARCHAR2(2) | Y |  | 品种代码 | DB注释(中文) |
| 17 | PROD_CD | VARCHAR2(3) | Y |  | 品名代码 | DB注释(中文) |
| 18 | LOT_NO | VARCHAR2(14) | Y |  | 批号 | DB注释(中文) |
| 19 | SMP_GTH_INST_TY | VARCHAR2(1) | Y |  | 试样采取指令分类 | DB注释(中文) |
| 20 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  | 炼钢内控钢种编号(出钢目标) | DB注释(中文) |
| 21 | ORD_USAGE | VARCHAR2(4) | Y |  | 订单用途代码 | DB注释(中文) |
| 22 | CMP_QCERT_NO | VARCHAR2(11) | Y |  | 公司保证编号(材质记号) | DB注释(中文) |
| 23 | SPEC_CD | VARCHAR2(50) | Y |  | 国家标准牌号 | DB注释(中文) |
| 24 | NATL_SPEC_YEAR | VARCHAR2(4) | Y |  | 国家标准年度 | DB注释(中文) |
| 25 | CUST_QCERT_NO | VARCHAR2(15) | Y |  | 客户保证编号 | DB注释(中文) |
| 26 | INSP_AGENCY_CD | VARCHAR2(3) | Y |  | 检查机构代码 | DB注释(中文) |
| 27 | SMP_LTH_LOC | VARCHAR2(1) | Y |  | 试样采取位置 | DB注释(中文) |
| 28 | SMP_TP | VARCHAR2(1) | Y |  | 试样分类(9-材料试验,A-产品试验) | DB注释(中文) |
| 29 | SMP_CND | VARCHAR2(2) | Y |  | Sampling条件 | DB注释(中文) |
| 30 | SPCMN_CNT | NUMBER | Y |  | 试样数量 | DB注释(中文) |
| 31 | SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 物性测试取样试样号数 | DB注释(中文) |
| 32 | MECH_JDG_GRD | VARCHAR2(1) | Y |  | 物性判定等级 | DB注释(中文) |
| 33 | RETEST_INST_YN | VARCHAR2(1) | Y |  | 是否指示再实验 | DB注释(中文) |
| 34 | RETEST_EXEC_YN | VARCHAR2(1) | Y |  | 是否实施再实验 | DB注释(中文) |
| 35 | MECH_TEST_ITEM_SEQ | NUMBER | Y |  | 材质试验项目个数 | DB注释(中文) |
| 36 | MECH_JDG_FINISH_YN | VARCHAR2(1) | Y |  | 物性判定结束是否 | DB注释(中文) |
| 37 | MECH_JDG_FINISH_DTM | VARCHAR2(14) | Y |  | 物性判定结束时间 | DB注释(中文) |
| 38 | SMP_PROG_CD | VARCHAR2(1) | Y |  | 检验进度代码 | DB注释(中文) |
| 39 | BATCH_FLAG | VARCHAR2(1) | Y |  | 主副批标志 | DB注释(中文) |
| 40 | MAIN_SMP_NO | VARCHAR2(14) | Y |  | 主批试样号 | DB注释(中文) |
| 41 | SCH_NO | VARCHAR2(10) | Y |  | Schedule No | DB注释(非中文) |
| 42 | GB_FLAG | VARCHAR2(1) | Y |  | 国标检验标记 | DB注释(中文) |
| 43 | FAC_CD | VARCHAR2(1) | Y |  | 工厂代码 | DB注释(中文) |
| 44 | MECH_FINISH_USER_ID | VARCHAR2(20) | Y |  | 性能人工判定结束人 | DB注释(中文) |
| 45 | BEF_SMP_GTH_INST_MTRL_NO | VARCHAR2(20) | Y |  | 试样采取指示材料编号 | DB注释(中文) |

### SQM_CHEM_RSLT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=76｜被读 56 过程 / 被写 10 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：1046292　**主键**：CHEM_SMP_CD、CHEM_SMP_SEQ、CHEM_CD　**语义覆盖**：25/25

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | 生成UserID_??UserID | DB注释(中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | 生成ObjectID_??ObjectID | DB注释(中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | 生成时间_???? | DB注释(中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 变更UserID_??UserID | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | 变更ObjectID_??ObjectID | DB注释(中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | 变更时间_???? | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Archive情况_Archive?? | DB注释(中文) |
| 8 | CHEM_SMP_CD | VARCHAR2(12) | N | ✓ | 试验试料编码_???? | DB注释(中文) |
| 9 | CHEM_SMP_SEQ | VARCHAR2(16) | N | ✓ | 试验试料序列号_?????? | DB注释(中文) |
| 10 | CHEM_CD | VARCHAR2(3) | N | ✓ | 试验项目编码_???? | DB注释(中文) |
| 11 | CHEM_MIN2 | NUMBER | Y |  | 试验上限值_??????? | DB注释(中文) |
| 12 | CHEM_MAX2 | NUMBER | Y |  | 试验下限值_??????? | DB注释(中文) |
| 13 | CHEM_TGT2 | NUMBER | Y |  | 试验目標值_??????? | DB注释(中文) |
| 14 | CHEM_RSLT2 | NUMBER | Y |  | 试验实绩值_??????? | DB注释(中文) |
| 15 | CHEM_SPEC_NM | VARCHAR2(30) | Y |  | 试验项目摘要_???????? | DB注释(中文) |
| 16 | CHEM_JUDG | VARCHAR2(10) | Y |  | 试验项目判定结果_?????????? | DB注释(中文) |
| 17 | CHEM_METHOD | VARCHAR2(30) | Y |  | 试验方法_?????? | DB注释(中文) |
| 18 | CHEM_JUDG_DTM | VARCHAR2(14) | Y |  | 试验项目判定时间_?????????? | DB注释(中文) |
| 19 | ERP_SEND_YN | VARCHAR2(1) | Y |  | ERP传送情况_ERP???? | DB注释(中文) |
| 20 | CHEM_MIN | VARCHAR2(20) | Y |  | 最小值 | DB注释(中文) |
| 21 | CHEM_MAX | VARCHAR2(20) | Y |  | 最大值 | DB注释(中文) |
| 22 | CHEM_TGT | VARCHAR2(20) | Y |  | 目标值 | DB注释(中文) |
| 23 | CHEM_RSLT | VARCHAR2(20) | Y |  | 结果值 | DB注释(中文) |
| 24 | ITEM_CD | VARCHAR2(20) | Y |  | Item编码 | DB注释(中文) |
| 25 | SUPPLY_ITEM_CD | VARCHAR2(20) | Y |  | 供应商Item编码 | DB注释(中文) |

### SIM_RM_SUPP_ITEM

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=67｜被读 65 过程 / 被写 1 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：429　**主键**：SUPPLIER_ITEM_CD　**语义覆盖**：28/28

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | ??UserID_??UserID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | ??ObjectID_??ObjectID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | ????_???? | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | ??UserID_??UserID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | ??ObjectID_??ObjectID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | ????_???? | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Archive??_Archive?? | DB注释(非中文) |
| 8 | SUPPLIER_ITEM_CD | VARCHAR2(15) | N | ✓ | ???Item??_???Item?? | DB注释(非中文) |
| 9 | ITEM_CD | VARCHAR2(20) | Y |  | Item??_??Item?? | DB注释(非中文) |
| 10 | SUPPLIER_ITEM_DESC | VARCHAR2(200) | Y |  | ?????Item??_?????Item?? | DB注释(非中文) |
| 11 | REMARK | VARCHAR2(1000) | Y |  | ?? | DB注释(非中文) |
| 12 | RM_MAN_ITEM_DESC_TY | VARCHAR2(1) | Y |  | ????????_???????? | DB注释(非中文) |
| 13 | RM_MAN_ITEM_DESC_CD | VARCHAR2(20) | Y |  | ????????_???????? | DB注释(非中文) |
| 14 | RM_USAGE_TY | VARCHAR2(3) | Y |  | ??????_?????? | DB注释(非中文) |
| 15 | RM_PAK_TY | VARCHAR2(1) | Y |  | ??????_?????? | DB注释(非中文) |
| 16 | STA_ACTIVE_DTM | VARCHAR2(14) | Y |  | ?????_????? | DB注释(非中文) |
| 17 | END_ACTIVE_DTM | VARCHAR2(14) | Y |  | ?????_????? | DB注释(非中文) |
| 18 | COUNTRY_OF_ORGN_CD | VARCHAR2(2) | Y |  | ?????Code_??????? | DB注释(非中文) |
| 19 | MADE_TY | VARCHAR2(1) | Y |  | ????????_???????? | DB注释(非中文) |
| 20 | RM_SHIP_DIS_ITEM_TP_TY | VARCHAR2(1) | Y |  | ????????_???????? | DB注释(非中文) |
| 21 | RM_KIND_TY | VARCHAR2(1) | Y |  | ??????_?????? | DB注释(非中文) |
| 22 | RM_GRAVITY | NUMBER | Y |  | ????????_???????? | DB注释(非中文) |
| 23 | IR_CHE_FRMAT_TY | VARCHAR2(2) | Y |  | ???????????_????????? | DB注释(非中文) |
| 24 | USABLE_PROC_CD | VARCHAR2(50) | Y |  | ????_???? | DB注释(非中文) |
| 25 | IR_CHE_DEC_RT | NUMBER | Y |  | ??????????_?????????? | DB注释(非中文) |
| 26 | ENABLED_FLAG | VARCHAR2(1) | Y |  | ????_???? | DB注释(非中文) |
| 27 | SUB_INVENT_CD | VARCHAR2(10) | Y |  | SubInventoryCode_SubInventoryCode | DB注释(非中文) |
| 28 | SEND_DTM | VARCHAR2(14) | Y |  | ???? | DB注释(非中文) |

### SIM_CO_PUR_BRAND_ITEM

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=60｜被读 26 过程 / 被写 17 过程｜操作 DELETE/INSERT/MERGE/UPDATE
- **行数(克隆库)**：363　**主键**：DATA_CYCLE、IR_CHE_OP_AC_DTM、PROC_CD、IR_CHE_IO_TY、SUPPLIER_ITEM_CD　**语义覆盖**：26/26

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | ??UserID_??UserID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | ??ObjectID_??ObjectID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | ????_???? | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | ??UserID_??UserID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | ??ObjectID_??ObjectID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | ????_???? | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Archive??_Archive?? | DB注释(非中文) |
| 8 | DATA_CYCLE | VARCHAR2(1) | N | ✓ | ??????_?????? | DB注释(非中文) |
| 9 | IR_CHE_OP_AC_DTM | VARCHAR2(14) | N | ✓ | ??????_?????? | DB注释(非中文) |
| 10 | PROC_CD | VARCHAR2(3) | N | ✓ | ??????_?????? | DB注释(非中文) |
| 11 | IR_CHE_IO_TY | VARCHAR2(1) | N | ✓ | ??IO????_????IO???? | DB注释(非中文) |
| 12 | SUPPLIER_ITEM_CD | VARCHAR2(15) | N | ✓ | ???Item??_???Item?? | DB注释(非中文) |
| 13 | IR_CHE_FRMAT_TY | VARCHAR2(5) | Y |  | ???????_????????? | DB注释(非中文) |
| 14 | IR_CHE_PROD_USE_QTY | NUMBER | Y |  | ???????_????????? | DB注释(非中文) |
| 15 | IR_SINGLE_USE_QTY | NUMBER | Y |  | ??????????Brend???_??????????Brend??? | DB注释(非中文) |
| 16 | SIN_PILE_USE_QTY | NUMBER | Y |  | ??BlendingPile???_??BlendingPile??? | DB注释(非中文) |
| 17 | IR_CHE_CMB_RATE | NUMBER | Y |  | ????????_?????????? | DB注释(非中文) |
| 18 | IR_CHE_DEC_RTO | NUMBER | Y |  | ?????_??????? | DB注释(非中文) |
| 19 | IR_CHE_DEC_QTY | NUMBER | Y |  | ????????_?????????? | DB注释(非中文) |
| 20 | IR_APPLY_RATIO | NUMBER | Y |  | ??????_?????? | DB注释(非中文) |
| 21 | IR_BAS_UT_CSUM | NUMBER | Y |  | ???????_??????? | DB注释(非中文) |
| 22 | IR_USE_RATE | NUMBER | Y |  | ????????_???????? | DB注释(非中文) |
| 23 | TRS_F | VARCHAR2(1) | Y |  | InterfaceData????_InterfaceData???? | DB注释(非中文) |
| 24 | BF_REVISE_QTY | NUMBER | Y |  | ?????_????? | DB注释(非中文) |
| 25 | COMPONENT_QTY | NUMBER | Y |  | Item???_Item??? | DB注释(非中文) |
| 26 | IR_CHE_FORM_NM | VARCHAR2(250) | Y |  | ?????_??????? | DB注释(非中文) |

### SCH_PLT_PLAN_ROLL

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=53｜被读 39 过程 / 被写 7 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：122210　**主键**：ROLL_UNIT、MTL_NO　**语义覆盖**：164/177

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID_Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID_Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time_Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID_Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID_Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time_Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag_Record Archive Flag | DB注释(非中文) |
| 8 | ROLL_UNIT | VARCHAR2(20) | N | ✓ | Roll Unit_Roll单位 | DB注释(中文) |
| 9 | MTL_NO | VARCHAR2(14) | N | ✓ | Matrial No_Matrial No | DB注释(非中文) |
| 10 | INST_MPLATE_NO | VARCHAR2(15) | Y |  | Instruction Mother Plate No_指令母板号 | DB注释(中文) |
| 11 | SPEC_ROLL_UNIT | VARCHAR2(20) | N |  | SPEC Roll Unit_SPEC Roll单位 | DB注释(中文) |
| 12 | SPEC_MTL_NO | VARCHAR2(14) | Y |  | SPEC Matrial No_作业计划Matrial No | DB注释(中文) |
| 13 | ROLL_UNIT_PRI | NUMBER | Y |  | Roll Unit Priority_热轧Roll单位内顺序 | DB注释(中文) |
| 14 | PLAN_PROC_SEQ | NUMBER | Y |  | Plan Process Sequence_计划工序顺序 | DB注释(中文) |
| 15 | SPEC_RCV_DTM | VARCHAR2(14) | Y |  | Spec Receive DateTime_作业计划接收时刻 | DB注释(中文) |
| 16 | PROD_INST_DTM | VARCHAR2(14) | Y |  | Production Order Send(L2) Datetime_生产质量时刻 | DB注释(中文) |
| 17 | WK_STA_SCH_DTM | VARCHAR2(14) | Y |  | Work Start Schedule Datetime_预计作业开始时刻 | DB注释(中文) |
| 18 | WK_END_SCH_DTM | VARCHAR2(14) | Y |  | Work End Schedule Datetime_预计作业结束时刻 | DB注释(中文) |
| 19 | PLAN_ROLL_STS | VARCHAR2(3) | Y |  | PLAN Roll Staus_计划Roll状态 | DB注释(中文) |
| 20 | MPLATE_DGN_THK | NUMBER | Y |  | 날판설계두께_母板设计厚度 | DB注释(中文) |
| 21 | MPLATE_DGN_WTH | NUMBER | Y |  | 날판설계폭_母板设计宽度 | DB注释(中文) |
| 22 | MPLATE_DGN_LTH | NUMBER | Y |  | 날판설계길이_母板设计长度 | DB注释(中文) |
| 23 | MPLATE_DGN_WGT | NUMBER | Y |  | 날판지시중량_母板指示重量 | DB注释(中文) |
| 24 | MPLATE_PLATE_QTY | NUMBER | Y |  | 날판내Plate매수_母板內产品买入 | DB注释(中文) |
| 25 | DGN_OVROLL_QTY | NUMBER | Y |  | 설계OverRoll매수_设计OverRoll支数 | DB注释(中文) |
| 26 | DGN_OVROLL_WGT | NUMBER | Y |  | 설계OverRoll량_设计OverRoll重量 | DB注释(中文) |
| 27 | PROD_CD | VARCHAR2(3) | Y |  | 품명코드_品名代码 | DB注释(中文) |
| 28 | ORD_NO | VARCHAR2(10) | Y |  | 대표주문번호_代表订单编号 | DB注释(中文) |
| 29 | ORD_LN | VARCHAR2(3) | Y |  | 대표주문행번_代表订单行号 | DB注释(中文) |
| 30 | DESIGN_CONTENT | VARCHAR2(1) | Y |  | 설계내용_设计內容 | DB注释(中文) |
| 31 | MPLATE_HTTRT_MIX_DS_GP | VARCHAR2(1) | Y |  | 날판열처리혼합설계구분_母板热处理混合设计分类 | DB注释(中文) |
| 32 | UST_ULTRASONIC_DGN_TY | VARCHAR2(1) | Y |  | 날판초음파탐상혼합설계구분_母板UST混合设计分类 | DB注释(中文) |
| 33 | CMBN_ORD_LN_CNT | NUMBER | Y |  | 조합주문번호행번수_组合订单行号数 | DB注释(中文) |
| 34 | ORD_NO1 | VARCHAR2(10) | Y |  | 주문번호1_订单编号1 | DB注释(中文) |
| 35 | ORD_LN1 | VARCHAR2(3) | Y |  | 주문행번1_订单行号1 | DB注释(中文) |
| 36 | PLATE_DGN_QTY1 | NUMBER | Y |  | PLATE설계매수1_PLATE设计支数1 | DB注释(中文) |
| 37 | PLATE_OR_QTY1 | NUMBER | Y |  | 설계OverRoll매수1_设计OverRoll支数1 | DB注释(中文) |
| 38 | PLATE_DGN_WTH1 | NUMBER | Y |  | PLATE설계폭1_PLATE设计宽度1 | DB注释(中文) |
| 39 | PLATE_DGN_LTH1 | NUMBER | Y |  | PLATE설계길이1_PLATE设计长度1 | DB注释(中文) |
| 40 | PLATE_DGN_WGT1 | NUMBER | Y |  | PLATE설계중량1_PLATE设计重量1 | DB注释(中文) |
| 41 | ORD_NO2 | VARCHAR2(10) | Y |  | 주문번호2_订单编号2 | DB注释(中文) |
| 42 | ORD_LN2 | VARCHAR2(3) | Y |  | 주문행번2_订单行号2 | DB注释(中文) |
| 43 | PLATE_DGN_QTY2 | NUMBER | Y |  | PLATE설계매수2_PLATE设计支数2 | DB注释(中文) |
| 44 | PLATE_OR_QTY2 | NUMBER | Y |  | 설계OverRoll매수2_设计OverRoll支数2 | DB注释(中文) |
| 45 | PLATE_DGN_WTH2 | NUMBER | Y |  | PLATE설계폭2_PLATE设计宽度2 | DB注释(中文) |
| 46 | PLATE_DGN_LTH2 | NUMBER | Y |  | PLATE설계길이2_PLATE设计长度2 | DB注释(中文) |
| 47 | PLATE_DGN_WGT2 | NUMBER | Y |  | PLATE설계중량2_PLATE设计重量2 | DB注释(中文) |
| 48 | ORD_NO3 | VARCHAR2(10) | Y |  | 주문번호3_订单编号3 | DB注释(中文) |
| 49 | ORD_LN3 | VARCHAR2(3) | Y |  | 주문행번3_订单行号3 | DB注释(中文) |
| 50 | PLATE_DGN_QTY3 | NUMBER | Y |  | PLATE설계매수3_PLATE设计支数3 | DB注释(中文) |
| 51 | PLATE_OR_QTY3 | NUMBER | Y |  | 설계OverRoll매수3_设计OverRoll支数3 | DB注释(中文) |
| 52 | PLATE_DGN_WTH3 | NUMBER | Y |  | PLATE설계폭3_PLATE设计宽度3 | DB注释(中文) |
| 53 | PLATE_DGN_LTH3 | NUMBER | Y |  | PLATE설계길이3_PLATE设计长度3 | DB注释(中文) |
| 54 | PLATE_DGN_WGT3 | NUMBER | Y |  | PLATE설계중량3_PLATE设计重量3 | DB注释(中文) |
| 55 | ORD_NO4 | VARCHAR2(10) | Y |  | 주문번호4_订单编号4 | DB注释(中文) |
| 56 | ORD_LN4 | VARCHAR2(3) | Y |  | 주문행번4_订单行号4 | DB注释(中文) |
| 57 | PLATE_DGN_QTY4 | NUMBER | Y |  | PLATE설계매수4_PLATE设计支数4 | DB注释(中文) |
| 58 | PLATE_OR_QTY4 | NUMBER | Y |  | 설계OverRoll매수4_设计OverRoll支数4 | DB注释(中文) |
| 59 | PLATE_DGN_WTH4 | NUMBER | Y |  | PLATE설계폭4_PLATE设计宽度4 | DB注释(中文) |
| 60 | PLATE_DGN_LTH4 | NUMBER | Y |  | PLATE설계길이4_PLATE设计长度4 | DB注释(中文) |
| 61 | PLATE_DGN_WGT4 | NUMBER | Y |  | PLATE설계중량4_PLATE设计重量4 | DB注释(中文) |
| 62 | ORD_NO5 | VARCHAR2(10) | Y |  | 주문번호5_订单编号5 | DB注释(中文) |
| 63 | ORD_LN5 | VARCHAR2(3) | Y |  | 주문행번5_订单行号5 | DB注释(中文) |
| 64 | PLATE_DGN_QTY5 | NUMBER | Y |  | PLATE설계매수5_PLATE设计支数5 | DB注释(中文) |
| 65 | PLATE_OR_QTY5 | NUMBER | Y |  | 설계OverRoll매수5_设计OverRoll支数5 | DB注释(中文) |
| 66 | PLATE_DGN_WTH5 | NUMBER | Y |  | PLATE설계폭5_PLATE设计宽度5 | DB注释(中文) |
| 67 | PLATE_DGN_LTH5 | NUMBER | Y |  | PLATE설계길이5_PLATE设计长度5 | DB注释(中文) |
| 68 | PLATE_DGN_WGT5 | NUMBER | Y |  | PLATE설계중량5_PLATE设计重量5 | DB注释(中文) |
| 69 | ORD_NO6 | VARCHAR2(10) | Y |  | 주문번호6_订单编号6 | DB注释(中文) |
| 70 | ORD_LN6 | VARCHAR2(3) | Y |  | 주문행번6_订单行号6 | DB注释(中文) |
| 71 | PLATE_DGN_QTY6 | NUMBER | Y |  | PLATE설계매수6_PLATE设计支数6 | DB注释(中文) |
| 72 | PLATE_OR_QTY6 | NUMBER | Y |  | 설계OverRoll매수6_设计OverRoll支数6 | DB注释(中文) |
| 73 | PLATE_DGN_WTH6 | NUMBER | Y |  | PLATE설계폭6_PLATE设计宽度6 | DB注释(中文) |
| 74 | PLATE_DGN_LTH6 | NUMBER | Y |  | PLATE설계길이6_PLATE设计长度6 | DB注释(中文) |
| 75 | PLATE_DGN_WGT6 | NUMBER | Y |  | PLATE설계중량6_PLATE设计重量6 | DB注释(中文) |
| 76 | SMP_NO | VARCHAR2(14) | Y |  | Sampling No_试样编号 | DB注释(中文) |
| 77 | SMP_LTH_LOC | VARCHAR2(1) | Y |  | Test Item LengthDirSampling Loc(Sampling Gather  Loc)_试样采取位置 | DB注释(中文) |
| 78 | TEST_CNT | NUMBER | Y |  | Test CNT_试验回数 | DB注释(中文) |
| 79 | HRL_MFC_STD_NO | VARCHAR2(11) | Y |  | Manufacturing standard marks of HR_热间制造标准编号 | DB注释(中文) |
| 80 | PLT_RF_HOLDING_TIME_MAX | NUMBER | Y |  | 주편재로시간상한_铸坯在炉时间上限 | DB注释(中文) |
| 81 | PLT_RF_HOLDING_TIME_MIN | NUMBER | Y |  | 주편재로시간하한_铸坯在炉时间下限 | DB注释(中文) |
| 82 | PLT_RF_HOLDING_TIME_AIM | NUMBER | Y |  | 주편재로시간목표_铸坯在炉时间目标 | DB注释(中文) |
| 83 | PLT_RF_EXT_TEMP_MAX | NUMBER | Y |  | 주편 출로온도상한_铸坯出炉温度上限 | DB注释(中文) |
| 84 | PLT_RF_EXT_TEMP_MIN | NUMBER | Y |  | 주편 출로온도하한_铸坯出炉温度下限 | DB注释(中文) |
| 85 | PLT_RF_EXT_TEMP_AIM | NUMBER | Y |  | 주편 출로온도목표_铸坯出炉温度目标 | DB注释(中文) |
| 86 | PLT_THK_AIM | NUMBER | Y |  | Thick Plate Aimming Thickness_厚板热轧目标厚度 | DB注释(中文) |
| 87 | PLT_WTH_AIM | NUMBER | Y |  | Thick Plate Aimming Width_厚板热轧目标宽度 | DB注释(中文) |
| 88 | PLT_WTH_TOL_MIN | NUMBER | Y |  | Width Tolerance Min_厚板热轧宽度公差下限值 | DB注释(中文) |
| 89 | PLT_WTH_TOL_MAX | NUMBER | Y |  | Width Tolerance  Max_厚板热轧宽度公差上限值 | DB注释(中文) |
| 90 | PLT_THK_TOL_MIN | NUMBER | Y |  | Thickness Tolerance Min_厚板热轧厚度公差下限值 | DB注释(中文) |
| 91 | PLT_THK_TOL_MAX | NUMBER | Y |  | Thickness Tolerance  Max_厚板热轧厚度公差上限值 | DB注释(中文) |
| 92 | PLT_FLAT_AIM | NUMBER | Y |  | Symmetric Flatness Target (Cold Value)_对称平直度目标 | DB注释(中文) |
| 93 | HIGH_SURF_FL | VARCHAR2(1) | Y |  | Hight Surface Flag_厚板高表面与否 | DB注释(中文) |
| 94 | ORD_SIZE_TY | VARCHAR2(1) | Y |  | Type of Order size_订单尺寸类型 | DB注释(中文) |
| 95 | ORD_WTH_MAX | NUMBER | Y |  | Maximum of Order width_订单宽度上限 | DB注释(中文) |
| 96 | ORD_LTH_MAX | NUMBER | Y |  | Maximumof Order length _订单长度上限 | DB注释(中文) |
| 97 | ORD_LTH_TOL_CD | VARCHAR2(1) | Y |  | Order length Tolerance Code_订单长度允许偏差代码 | DB注释(中文) |
| 98 | ORD_LTH_TOL_MIN | NUMBER | Y |  | Order length Ninimum Tolerance Value_订单长度允许偏差下限 | DB注释(中文) |
| 99 | ORD_LTH_TOL_MAX | NUMBER | Y |  | Order length Maximum Tolerance Value_订单长度允许偏差上限 | DB注释(中文) |
| 100 | ORD_PLT_CD | VARCHAR2(1) | Y |  | Order Plant Code_生产工厂分类 | DB注释(中文) |
| 101 | ORD_EDGE_TY | VARCHAR2(1) | Y |  | Order Edge Type_订单Edge区分 | DB注释(中文) |
| 102 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  | Steel Grade_炼钢内控钢种编号 | DB注释(中文) |
| 103 | SPEC_CD | VARCHAR2(50) | Y |  | Specification Code_国家标准牌号 | DB注释(中文) |
| 104 | SLAB_NO | VARCHAR2(40) | Y |  | Slab No_Slab号 | DB注释(中文) |
| 105 | CAST_STR_NO | VARCHAR2(1) | Y |  | Caster Strand No_铸造Strand号 | DB注释(中文) |
| 106 | SLAB_STS | VARCHAR2(1) | Y |  | Slab Status_Slab状态 | DB注释(中文) |
| 107 | SLAB_THK | NUMBER | Y |  | Slab Thickness_Slab厚度 | DB注释(中文) |
| 108 | SLAB_WTH | NUMBER | Y |  | Slab Width_Slab宽度 | DB注释(中文) |
| 109 | SLAB_LTH | NUMBER | Y |  | Slab Length_Slab长度 | DB注释(中文) |
| 110 | SLAB_WGT | NUMBER | Y |  | Slab Weight_Slab重量 | DB注释(中文) |
| 111 | CONF_PASS_PLANT_OP_CD | VARCHAR2(60) | Y |  | 확정통과공장공정코드_确定通过工厂工序代码 | DB注释(中文) |
| 112 | QLT_HCR_FL | VARCHAR2(1) | Y |  | 품질설계HCR구분_质量设计HCR分类 | DB注释(中文) |
| 113 | PLT_HEATING_CD | VARCHAR2(1) | Y |  | 품질설계열처리방법_热处理方法代码 | DB注释(中文) |
| 114 | UST_MTH_CD | VARCHAR2(2) | Y |  | UST Method Code_UST方法代码 | DB注释(中文) |
| 115 | GAS_CUT_FL | VARCHAR2(1) | Y |  | GAS절단구분_GAS切斷分类 | DB注释(中文) |
| 116 | PLT_1COOL_CD | VARCHAR2(1) | Y |  | M43_냉각방식_M43_冷却模式 | DB注释(中文) |
| 117 | RJT_CAUSE_CD | VARCHAR2(2) | Y |  | Reject Cause Code_缺号原因代码 | DB注释(中文) |
| 118 | SPEC_RTN_CD | VARCHAR2(2) | Y |  | Spec Return Code_计划返送代码 | DB注释(中文) |
| 119 | FAC_CD | VARCHAR2(1) | Y |  | Factory Code_工厂代码 | DB注释(中文) |
| 120 | ROLL_UNIT_INST_SEQ | NUMBER | Y |  | Roll Unit Instruction SEQ_热轧计划工序代码 | DB注释(中文) |
| 121 | TE_PRD_FL | VARCHAR2(1) | Y |  | Test Production Flag_Test Production Flag | DB注释(非中文) |
| 122 | SPEC_RTN_USER_ID | VARCHAR2(20) | Y |  | Spec Return User ID_计划返送 User ID | DB注释(中文) |
| 123 | SPEC_RTN_DTM | VARCHAR2(14) | Y |  | Spec Return DateTime_计划返送 DateTime | DB注释(中文) |
| 124 | HEAT_NO | VARCHAR2(50) | Y |  | Heat No_Heat号 | DB注释(中文) |
| 125 | WK_STA_DTM | VARCHAR2(14) | Y |  | The SFTCrew based on the SPM Work Day | SCO_DATA_DIC(D) |
| 126 | WK_END_DTM | VARCHAR2(14) | Y |  | Flag of SPM Work(1:Normal,2:Abnormal) | SCO_DATA_DIC(D) |
| 127 | L2_SEND_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 128 | HR_PLAN_OP_CD | VARCHAR2(60) | Y |  | Hot Rolling Plan Progress | SCO_DATA_DIC(D) |
| 129 | NPLATE_CUTTING_CNT | NUMBER | Y |  |  | 空 |
| 130 | NPLATE_CUTTING_LTH1 | NUMBER | Y |  |  | 空 |
| 131 | NPLATE_CUTTING_LTH2 | NUMBER | Y |  |  | 空 |
| 132 | NPLATE_CUTTING_LTH3 | NUMBER | Y |  |  | 空 |
| 133 | NPLATE_CUTTING_LTH4 | NUMBER | Y |  |  | 空 |
| 134 | NPLATE_CUTTING_LTH5 | NUMBER | Y |  |  | 空 |
| 135 | NPLATE_CUTTING_LTH6 | NUMBER | Y |  |  | 空 |
| 136 | NPLATE_CUTTING_LTH7 | NUMBER | Y |  |  | 空 |
| 137 | NPLATE_CUTTING_LTH8 | NUMBER | Y |  |  | 空 |
| 138 | NPLATE_CUTTING_LTH9 | NUMBER | Y |  |  | 空 |
| 139 | NPLATE_CUTTING_LTH10 | NUMBER | Y |  |  | 空 |
| 140 | NPLATE_CUTTING_LTH11 | NUMBER | Y |  |  | 空 |
| 141 | ROLL_MOD | VARCHAR2(1) | Y |  | 1 平轧 ，2 卷轧 | DB注释(中文) |
| 142 | ORD_NO7 | VARCHAR2(10) | Y |  | ????6_订单编号6 | DB注释(中文) |
| 143 | ORD_LN7 | VARCHAR2(3) | Y |  | ????6_订单行号6 | DB注释(中文) |
| 144 | PLATE_DGN_QTY7 | NUMBER | Y |  | PLATE????6_PLATE设计支数6 | DB注释(中文) |
| 145 | PLATE_OR_QTY7 | NUMBER | Y |  | ??OverRoll??6_设计OverRoll支数6 | DB注释(中文) |
| 146 | PLATE_DGN_WTH7 | NUMBER | Y |  | PLATE???6_PLATE设计宽度6 | DB注释(中文) |
| 147 | PLATE_DGN_LTH7 | NUMBER | Y |  | PLATE????6_PLATE设计长度6 | DB注释(中文) |
| 148 | PLATE_DGN_WGT7 | NUMBER | Y |  | PLATE????6_PLATE设计重量6 | DB注释(中文) |
| 149 | ORD_NO8 | VARCHAR2(10) | Y |  | ????6_订单编号6 | DB注释(中文) |
| 150 | ORD_LN8 | VARCHAR2(3) | Y |  | ????6_订单行号6 | DB注释(中文) |
| 151 | PLATE_DGN_QTY8 | NUMBER | Y |  | PLATE????6_PLATE设计支数6 | DB注释(中文) |
| 152 | PLATE_OR_QTY8 | NUMBER | Y |  | ??OverRoll??6_设计OverRoll支数6 | DB注释(中文) |
| 153 | PLATE_DGN_WTH8 | NUMBER | Y |  | PLATE???6_PLATE设计宽度6 | DB注释(中文) |
| 154 | PLATE_DGN_LTH8 | NUMBER | Y |  | PLATE????6_PLATE设计长度6 | DB注释(中文) |
| 155 | PLATE_DGN_WGT8 | NUMBER | Y |  | PLATE????6_PLATE设计重量6 | DB注释(中文) |
| 156 | ORD_NO9 | VARCHAR2(10) | Y |  | ????6_订单编号6 | DB注释(中文) |
| 157 | ORD_LN9 | VARCHAR2(3) | Y |  | ????6_订单行号6 | DB注释(中文) |
| 158 | PLATE_DGN_QTY9 | NUMBER | Y |  | PLATE????6_PLATE设计支数6 | DB注释(中文) |
| 159 | PLATE_OR_QTY9 | NUMBER | Y |  | ??OverRoll??6_设计OverRoll支数6 | DB注释(中文) |
| 160 | PLATE_DGN_WTH9 | NUMBER | Y |  | PLATE???6_PLATE设计宽度6 | DB注释(中文) |
| 161 | PLATE_DGN_LTH9 | NUMBER | Y |  | PLATE????6_PLATE设计长度6 | DB注释(中文) |
| 162 | PLATE_DGN_WGT9 | NUMBER | Y |  | PLATE????6_PLATE设计重量6 | DB注释(中文) |
| 163 | BATCH_CD | VARCHAR2(20) | Y |  | 批次 | DB注释(中文) |
| 164 | IS_MAIN_BATCH | NUMBER | Y |  | 是否是代表批次信息0 代表批次，1非代表批次 | DB注释(中文) |
| 165 | BATCH_ROLL_PRI | NUMBER | Y |  | 批次轧制顺序 | DB注释(中文) |
| 166 | IS_INST | NUMBER | Y |  | 是否下达，0未下达，1 已下达 | DB注释(中文) |
| 167 | PLT_LTH_AIM | NUMBER | Y |  | 子板长度 | DB注释(中文) |
| 168 | BATCH_CONF_SFT_NO | VARCHAR2(20) | Y |  | 班次 | DB注释(中文) |
| 169 | BATCH_CONF_SFT_GRP | VARCHAR2(20) | Y |  | 班组 | DB注释(中文) |
| 170 | DELIVERY_STATE | VARCHAR2(100) | Y |  | 交货状态 | DB注释(中文) |
| 171 | STEEL_GRD | VARCHAR2(100) | Y |  | 钢种 | DB注释(中文) |
| 172 | DC_LTH | VARCHAR2(100) | Y |  | 定尺长度 | DB注释(中文) |
| 173 | DAN_HAO | NUMBER | Y |  | 单号 | DB注释(中文) |
| 174 | FCE_NO | VARCHAR2(100) | Y |  | 上料炉号 | DB注释(中文) |
| 175 | REMARK1 | VARCHAR2(1000) | Y |  | 备注1 | DB注释(中文) |
| 176 | ROLL_LOT_NO | VARCHAR2(100) | Y |  | 线下批号 | DB注释(中文) |
| 177 | UST_YN | VARCHAR2(10) | Y |  | 是否探伤 | DB注释(中文) |

### SQM_CHEM_JDG

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=53｜被读 45 过程 / 被写 4 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：492425　**主键**：MTRL_NO、JDG_SEQ、CHEM_CD　**语义覆盖**：24/24

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | MTRL_NO | VARCHAR2(14) | N | ✓ | 材料编号 | DB注释(中文) |
| 9 | JDG_SEQ | NUMBER | N | ✓ | Sequence | DB注释(非中文) |
| 10 | CHEM_CD | VARCHAR2(4) | N | ✓ | Chemical Code | DB注释(非中文) |
| 11 | CHEM_MIN2 | NUMBER | Y |  | 化学试验下限值 | DB注释(中文) |
| 12 | CHEM_MAX2 | NUMBER | Y |  | 化学试验上限值 | DB注释(中文) |
| 13 | CHEM_TGT2 | NUMBER | Y |  | 化学试验目标值 | DB注释(中文) |
| 14 | CHEM_CHAR | VARCHAR2(10) | Y |  | Chemical Characteristic Value | DB注释(非中文) |
| 15 | CHEM_RSLT2 | NUMBER | Y |  | 化学试验实绩 | DB注释(中文) |
| 16 | CHEM_RSLT_DEC_POINT | NUMBER | Y |  | Chemical Result with assurance decimal point | DB注释(非中文) |
| 17 | CHEM_JUDG | VARCHAR2(10) | Y |  | 化学试验项目判定结果 | DB注释(中文) |
| 18 | CHEM_JUDG_DTM | VARCHAR2(14) | Y |  | 化学试验项目判定时刻 | DB注释(中文) |
| 19 | NUM_FORM | VARCHAR2(15) | Y |  | Decimal Point | DB注释(非中文) |
| 20 | CONF_YN | VARCHAR2(1) | Y |  | 最终成分是否 | DB注释(中文) |
| 21 | CHEM_MIN | VARCHAR2(20) | Y |  | 最小值 | DB注释(中文) |
| 22 | CHEM_MAX | VARCHAR2(20) | Y |  | 最大值 | DB注释(中文) |
| 23 | CHEM_TGT | VARCHAR2(20) | Y |  | 目标值 | DB注释(中文) |
| 24 | CHEM_RSLT | VARCHAR2(20) | Y |  | 结果值 | DB注释(中文) |

### SMS_RSLT_BOF

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=50｜被读 44 过程 / 被写 3 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：10508　**主键**：HEAT_NO、SMS_PROC_CD　**语义覆盖**：222/226

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | BOTTOM_STAT | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | HEAT_NO | VARCHAR2(10) | N | ✓ | Heat No | DB注释(非中文) |
| 9 | SMS_PROC_CD | VARCHAR2(2) | N | ✓ | SMS Process Code | DB注释(非中文) |
| 10 | BOF_NO | VARCHAR2(1) | Y |  | BOF No  ���� | DB注释(非中文) |
| 11 | PLAN_HEAT_NO | VARCHAR2(8) | Y |  | Plan Heat No | DB注释(非中文) |
| 12 | PRP_HEAT_NO | VARCHAR2(9) | Y |  | Prepared Heat No | DB注释(非中文) |
| 13 | BEF_HEAT_NO | VARCHAR2(9) | Y |  | Before Heat No | DB注释(非中文) |
| 14 | RTN_HEAT_NO | VARCHAR2(9) | Y |  | Return Heat No | DB注释(非中文) |
| 15 | RTN_RE_CHARG_WGT | NUMBER | Y |  | Return Re-Charging Weight | DB注释(非中文) |
| 16 | PI_LD_NO | VARCHAR2(15) | Y |  | PI Ladle No 铁次-铁包号 | DB注释(中文) |
| 17 | LD_NO | VARCHAR2(10) | Y |  | Ladle No 钢包号 | DB注释(中文) |
| 18 | SUMUP_DT | VARCHAR2(8) | Y |  | Operation Sumup date | DB注释(非中文) |
| 19 | OPER_DT | VARCHAR2(8) | Y |  | Operation Date | DB注释(非中文) |
| 20 | OPER_SHIFT | VARCHAR2(2) | Y |  | Operation Shift | DB注释(非中文) |
| 21 | OPER_EMP_NO | VARCHAR2(20) | Y |  | Operator Employee No | DB注释(非中文) |
| 22 | PREV_BOF_LIFE_CNT | NUMBER | Y |  | Previous BOF Life Times | DB注释(非中文) |
| 23 | BOF_LIFE_CNT | NUMBER | Y |  | BOF Life Times 转炉炉龄 | DB注释(中文) |
| 24 | BOF_USED_CNT | NUMBER | Y |  | BOF Used Times 转炉使用次数 | DB注释(中文) |
| 25 | OXG_LN_NO | NUMBER | Y |  | Oxygen Lance No 氧枪号 | DB注释(中文) |
| 26 | OXG_LN_MAN_CNT | NUMBER | Y |  | Oxygen Lance Nozzle Hole Times | DB注释(非中文) |
| 27 | OXG_LN_EW12_TY | VARCHAR2(1) | Y |  | Oxygen Lance East-West12 Type | DB注释(非中文) |
| 28 | OXG_LN_USED_CNT | NUMBER | Y |  | Oxygen Lance Used Times 枪龄 | DB注释(中文) |
| 29 | NZ_CHG_AFT_LN_USED_CNT | NUMBER | Y |  | Lance Used Times Afterr Nozzle change | DB注释(非中文) |
| 30 | LN_DE_SLAG_AFT_FST_HEAT_YN | VARCHAR2(10) | Y |  | First heat Y/N After Lance Skimming | DB注释(非中文) |
| 31 | TAPHOLE_CHANGE_CNT | NUMBER | Y |  | Taphole Change Times  出铁口更换次数 | DB注释(中文) |
| 32 | TAPHOLE_USED_CNT | NUMBER | Y |  | Taphole Used Times出铁口使用次数 | DB注释(中文) |
| 33 | PI_HMR | NUMBER | Y |  | Pig Iron Rate 生铁率 | DB注释(中文) |
| 34 | HEAT_TOT_WGT | NUMBER | Y |  | Total Heat Weight 炉次重量 | DB注释(中文) |
| 35 | PI_WGT | NUMBER | Y |  | Pig Iron Weight 生铁重量 | DB注释(中文) |
| 36 | SCRAP_TOT_WGT | NUMBER | Y |  | 废钢总量 | DB注释(中文) |
| 37 | SCRAP_LD_NO | VARCHAR2(3) | Y |  |  | 空 |
| 38 | IRONBLOCK_WGT | NUMBER | Y |  | 铁块重量 | DB注释(中文) |
| 39 | CALC_STEEL_WGT | NUMBER | Y |  | Calculated Heat Weight | DB注释(非中文) |
| 40 | BB_AFT_UNMELT_WGT | NUMBER | Y |  | After BB, Un-Melt Occure Weight | DB注释(非中文) |
| 41 | BEF_FINE_PI_USED_WGT | NUMBER | Y |  | Before Heat, Fine PI Used Weight | DB注释(非中文) |
| 42 | BEF_DE_SLAG_COAT_STA_DTM | VARCHAR2(14) | Y |  | Coating Start Date Before Skimming in before heat | DB注释(非中文) |
| 43 | BEF_DE_SLAG_COAT_END_DTM | VARCHAR2(14) | Y |  | Coating End Date Before Skimming in before heat | DB注释(非中文) |
| 44 | BEF_DE_SLAG_COAT_DUR | NUMBER | Y |  | Coating Time Before Skimming in before heat | DB注释(非中文) |
| 45 | LST_DE_SLAG_END_DTM | VARCHAR2(14) | Y |  | Last Skimming End Date | DB注释(非中文) |
| 46 | COAT_METHOD | VARCHAR2(1) | Y |  | Coating Method | DB注释(非中文) |
| 47 | DE_SLAG_BEF_COAT_STA_DTM | VARCHAR2(14) | Y |  | Coating Start Date Before Skimming | DB注释(非中文) |
| 48 | DE_SLAG_BEF_COAT_END_DTM | VARCHAR2(14) | Y |  | Coating End Date Before Skimming | DB注释(非中文) |
| 49 | DE_SLAG_BEF_COAT_DUR | NUMBER | Y |  | Coating Time Before Skimming | DB注释(非中文) |
| 50 | DE_SLAG_AFT_COAT_STA_DTM | VARCHAR2(14) | Y |  | Coating Start Date After Skimming | DB注释(非中文) |
| 51 | DE_SLAG_AFT_COAT_END_DTM | VARCHAR2(14) | Y |  | Coating End Date After Skimming | DB注释(非中文) |
| 52 | DE_SLAG_AFT_COAT_DUR | NUMBER | Y |  | Coating Time After Skimming | DB注释(非中文) |
| 53 | DE_SLAG_END_DTM | VARCHAR2(14) | Y |  | BOF Skimming End Date | DB注释(非中文) |
| 54 | SCRAP_CHARG_DTM | VARCHAR2(14) | Y |  | Scrap Charging Date 废钢装入开始时间 | DB注释(中文) |
| 55 | CHARG_STA_DTM | VARCHAR2(14) | Y |  | Charging Start Date 装入开始时间 | DB注释(中文) |
| 56 | CHARG_END_DTM | VARCHAR2(14) | Y |  | PI Charging End Date 装入结束时间 | DB注释(中文) |
| 57 | POSLEAD_CLT_STEEL_WGT | NUMBER | Y |  | POSLEAD Collect Steel Weight | DB注释(非中文) |
| 58 | BLW_METHOD | VARCHAR2(2) | Y |  | Blowing Method 吹方式 | DB注释(中文) |
| 59 | DBL_SLAG_DE_SLAG_DUR | NUMBER | Y |  | Double Slag Skimming Time | DB注释(非中文) |
| 60 | DBL_SLAG_OXG_FLW | NUMBER | Y |  | Double Slag Blowing Oxygen Flow | DB注释(非中文) |
| 61 | DBL_SLAG_BLW_DUR | NUMBER | Y |  | Double Slag Blowing Time | DB注释(非中文) |
| 62 | BLW_PURPOSE_TY1 | VARCHAR2(1) | Y |  | Blowing Purpose Type1 | DB注释(非中文) |
| 63 | BLW_STA_DTM1 | VARCHAR2(14) | Y |  | Blowing start date 1 | DB注释(非中文) |
| 64 | BLW_END_DTM1 | VARCHAR2(14) | Y |  | Blowing end date 1 | DB注释(非中文) |
| 65 | BLW_DUR1 | NUMBER | Y |  | Blowing duration 1 | DB注释(非中文) |
| 66 | BLW_PURPOSE_TY2 | VARCHAR2(1) | Y |  | Blowing Purpose Type2 | DB注释(非中文) |
| 67 | BLW_STA_DTM2 | VARCHAR2(14) | Y |  | Blowing start date 2 | DB注释(非中文) |
| 68 | BLW_END_DTM2 | VARCHAR2(14) | Y |  | Blowing end date 2 | DB注释(非中文) |
| 69 | BLW_DUR2 | NUMBER | Y |  | Blowing duration 2 | DB注释(非中文) |
| 70 | BLW_PURPOSE_TY3 | VARCHAR2(1) | Y |  | Blowing Purpose Type3 | DB注释(非中文) |
| 71 | BLW_STA_DTM3 | VARCHAR2(14) | Y |  | Blowing start date 3 | DB注释(非中文) |
| 72 | BLW_END_DTM3 | VARCHAR2(14) | Y |  | Blowing end date 3 | DB注释(非中文) |
| 73 | BLW_DUR3 | NUMBER | Y |  | Blowing duration 3 | DB注释(非中文) |
| 74 | BLW_PURPOSE_TY4 | VARCHAR2(1) | Y |  | Blowing Purpose Type4 | DB注释(非中文) |
| 75 | BLW_STA_DTM4 | VARCHAR2(14) | Y |  | Blowing start date 4 开吹时间 | DB注释(中文) |
| 76 | BLW_END_DTM4 | VARCHAR2(14) | Y |  | Blowing end date 4 终吹时间 | DB注释(中文) |
| 77 | BLW_DUR4 | NUMBER | Y |  | Blowing duration 4 开吹时长 | DB注释(中文) |
| 78 | RINS_STA_DTM | VARCHAR2(14) | Y |  | Rinsing Start date | DB注释(非中文) |
| 79 | RINS_END_DTM | VARCHAR2(14) | Y |  | Rinsing End Date | DB注释(非中文) |
| 80 | RINS_PROC_DUR | NUMBER | Y |  | Rinsing Time | DB注释(非中文) |
| 81 | RINS_AR_USED_VOL | NUMBER | Y |  | Rinsing Ar Used Volume | DB注释(非中文) |
| 82 | RINS_N2_USED_VOL | NUMBER | Y |  | Rinsing N2 Used Volume | DB注释(非中文) |
| 83 | BEF_TAP_STA_DTM | VARCHAR2(14) | Y |  | Before Heat Tapping Start Date | DB注释(非中文) |
| 84 | BEF_TAP_END_DTM | VARCHAR2(14) | Y |  | Before Heat Tapping End Date | DB注释(非中文) |
| 85 | BEF_TAP_DUR | NUMBER | Y |  | Before Heat Tapping Time | DB注释(非中文) |
| 86 | TAP_STA_DTM | VARCHAR2(14) | Y |  | 出钢开始时间 | DB注释(中文) |
| 87 | TAP_END_DTM | VARCHAR2(14) | Y |  | 出钢结束时间 | DB注释(中文) |
| 88 | TAP_DUR | NUMBER | Y |  | 出钢时长 | DB注释(中文) |
| 89 | TAP_TEMP | NUMBER | Y |  | 出钢温度 | DB注释(中文) |
| 90 | AFTER_AR_TEMP | NUMBER | Y |  | 吹氩后温度 | DB注释(中文) |
| 91 | TT_DUR | NUMBER | Y |  | Tap to Tap Time | DB注释(非中文) |
| 92 | SMS_PROC_DUR | NUMBER | Y |  | Steel Making Time | DB注释(非中文) |
| 93 | SMS_NOT_PROC_DUR | NUMBER | Y |  | Not Steel Making Time | DB注释(非中文) |
| 94 | PROC_TGT_DUR | NUMBER | Y |  | Target process time | DB注释(非中文) |
| 95 | TOP_BLW_PTRN | VARCHAR2(3) | Y |  | Top Blowing Pattern  顶吹样？ | DB注释(中文) |
| 96 | BTM_BLW_PTRN | VARCHAR2(3) | Y |  | Bottom Blowing Pattern底吹样？ | DB注释(中文) |
| 97 | AIR_BLW_STA_DTM | VARCHAR2(14) | Y |  | Air Blowing Start Date 吹空气开始时间 | DB注释(中文) |
| 98 | AIR_BLW_END_DTM | VARCHAR2(14) | Y |  | Air Blowing End Date 吹空气结束时间？ | DB注释(中文) |
| 99 | AIR_BLW_DUR | NUMBER | Y |  | Air Blowing Time 吹空气时长 | DB注释(中文) |
| 100 | EP_TGT_TEMP | NUMBER | Y |  | End Point Target Temperature 终点目标温度 | DB注释(中文) |
| 101 | EP_REV_TGT_TEMP | NUMBER | Y |  | End Point Revised Target Temperature 终点修正目标温度 | DB注释(中文) |
| 102 | EP_TGT_C | NUMBER | Y |  | End Point Target Chem-C 终点目标C | DB注释(中文) |
| 103 | EP_REV_TGT_C | NUMBER | Y |  | End Point Revised Target Chem-C | DB注释(非中文) |
| 104 | EP_TGT_P | NUMBER | Y |  | End Point Target Chem-P终点目标P | DB注释(中文) |
| 105 | EP_TGT_S | NUMBER | Y |  | End Point Target Chem-S终点目标S | DB注释(中文) |
| 106 | EP_EST_C | NUMBER | Y |  | End Point Estimate C 终点预估C | DB注释(中文) |
| 107 | EP_EST_P | NUMBER | Y |  | End Point Estimate P终点预估P | DB注释(中文) |
| 108 | EP_EST_S | NUMBER | Y |  | End Point Estimate S终点预估S | DB注释(中文) |
| 109 | EP_EST_TEMP | NUMBER | Y |  | End Point Estimate Temperature终点预测温度 | DB注释(中文) |
| 110 | EP_EST_OXG_DEN | NUMBER | Y |  | End Point Estimate Oxygen Denstity 定氧 | DB注释(中文) |
| 111 | EP_CALC_C | NUMBER | Y |  | End Point Calculate Chem-C | DB注释(非中文) |
| 112 | EP_CALC_MN | NUMBER | Y |  | End Point Calculate Chem-Mn | DB注释(非中文) |
| 113 | EP_CALC_P | NUMBER | Y |  | End Point Calculate Chem-P | DB注释(非中文) |
| 114 | EP_CALC_S | NUMBER | Y |  | End Point Calculate Chem-S | DB注释(非中文) |
| 115 | EP_CALC_TOT_FE | NUMBER | Y |  | End Point Calculate Chem-Total Fe | DB注释(非中文) |
| 116 | EP_TEMP | NUMBER | Y |  | End Point Temperature | DB注释(非中文) |
| 117 | EP_OXG | NUMBER | Y |  | End Point Oxygen 终点氧 | DB注释(中文) |
| 118 | EP_CD_C_DEN | NUMBER | Y |  | End Point CD C Desntity | DB注释(非中文) |
| 119 | BLW_IN_AR_USE_VOL | NUMBER | Y |  | Bottom Blowing Ar Used Volume in Blowing 底吹氩气在清扫使用量 | DB注释(中文) |
| 120 | BLW_IN_N2_USE_VOL | NUMBER | Y |  | Bottom Blowing N2 Used Volume in Blowing 底吹氮气使用量 | DB注释(中文) |
| 121 | BLW_NOTIN_AR_USE_VOL | NUMBER | Y |  | Bottom Blowing Ar Used Volume not in Blowing | DB注释(非中文) |
| 122 | BLW_NOTIN_N2_USE_VOL | NUMBER | Y |  | Bottom Blowing N2 Used Volume not in Blowing | DB注释(非中文) |
| 123 | BTM_BB_AR_USED_TOT_VOL | NUMBER | Y |  | Bottom Blowing Total Ar Used Volume 底吹氩气总使用量 | DB注释(中文) |
| 124 | BTM_BB_N2_USED_TOT_VOL | NUMBER | Y |  | Bottom Blowing Total N2 Used Volume | DB注释(非中文) |
| 125 | OPER_ABNR_REASON_CD | VARCHAR2(1) | Y |  | Operation Abnormal Reason Code  操作异常原因代码 | DB注释(中文) |
| 126 | RE_BLW_CNT | VARCHAR2(1) | Y |  | Re-Blowing Times | DB注释(非中文) |
| 127 | RE_BLW_REASON_TY | VARCHAR2(1) | Y |  | Re-Blowing Reason Type | DB注释(非中文) |
| 128 | SLAG_CUT_METHOD | VARCHAR2(3) | Y |  | Slag Coating Y/N | DB注释(非中文) |
| 129 | COOLANT_IN_YN | VARCHAR2(1) | Y |  | Coolant Input Y/N | DB注释(非中文) |
| 130 | TAP_BEF_BOF_TILT_YN | VARCHAR2(1) | Y |  | Before Tapping, BOF Tilting Y/N | DB注释(非中文) |
| 131 | LDG_CLT_CNT | NUMBER | Y |  | LDG Collect Count | DB注释(非中文) |
| 132 | LDG_CLT_VOL | NUMBER | Y |  | LDG Collect Volume | DB注释(非中文) |
| 133 | LDG_CLT_DUR | NUMBER | Y |  | LDG Collect Time | DB注释(非中文) |
| 134 | LDG_CLT_ABNR_CD | VARCHAR2(1) | Y |  | LDG Collect Abnromal Code | DB注释(非中文) |
| 135 | UPD_SURF_HGT | NUMBER | Y |  | Updated Surface Height | DB注释(非中文) |
| 136 | ACT_SURF_HGT | NUMBER | Y |  | Actual Measure Surface Height | DB注释(非中文) |
| 137 | CALC_SURF_HGT | NUMBER | Y |  | Calculated Surface Height | DB注释(非中文) |
| 138 | SURF_MSU_BOF_LIFE_CNT | NUMBER | Y |  | BOF Life Times at Surface Measuring | DB注释(非中文) |
| 139 | SURF_MSU_CHARG_WGT | NUMBER | Y |  | Charging Weight at Surface Measuring | DB注释(非中文) |
| 140 | NCF_OXG_USED_VOL | NUMBER | Y |  | Not Catch Fire Oxygen Used Volume | DB注释(非中文) |
| 141 | BLW_OXG_USED_TOT_VOL | NUMBER | Y |  | Blowing Oxygen Used Total Vloume | DB注释(非中文) |
| 142 | BLW_OXG_PRESS | NUMBER | Y |  |  | 空 |
| 143 | AIR_BLW_OXG_VOL | NUMBER | Y |  | Air Blowing Oxygen Used Volume | DB注释(非中文) |
| 144 | OXG_USED_TOT_VOL | NUMBER | Y |  | Total Oxygen Used Volume | DB注释(非中文) |
| 145 | BLW_SUB_LN_OXG_USED_VOL | NUMBER | Y |  | Sub-Lance Oxygen Used Volume in Blowing | DB注释(非中文) |
| 146 | DLD_SLAG_THK | NUMBER | Y |  | Deck Ladle Slag Measure Thickness | DB注释(非中文) |
| 147 | DLD_FREEBRD_HGT | NUMBER | Y |  | Deck Ladle Free Board Measure Height | DB注释(非中文) |
| 148 | DLD_CALC_SLAG_WGT | NUMBER | Y |  | Deck Ladle Calculated Slag Weight | DB注释(非中文) |
| 149 | DLD_CALC_HEAT_WGT | NUMBER | Y |  | Deck Ladle Calcultaed Heat Weight | DB注释(非中文) |
| 150 | STEAM_VOL | NUMBER | Y |  | Steam Occuring Volume | DB注释(非中文) |
| 151 | LIFE_OPER_COND_MIN_HMR | NUMBER | Y |  | Minimun Pig Iron Rate at BOF Operation Condition | DB注释(非中文) |
| 152 | TAP_ACT_QTY | NUMBER | Y |  | Actual Tapping Quantity | DB注释(非中文) |
| 153 | SLAG_FREE_RATE | NUMBER | Y |  | Slag Free Rate | DB注释(非中文) |
| 154 | CONS_P_QTY | NUMBER | Y |  | P Contents Quantity | DB注释(非中文) |
| 155 | CONS_S_QTY | NUMBER | Y |  | S Contents Quantity | DB注释(非中文) |
| 156 | PI_CHARG_ACT_TEMP | NUMBER | Y |  | PI Charging Actual Temperature 铁水装炉实绩温度 | DB注释(中文) |
| 157 | PI_CALC_TI | NUMBER | Y |  | PI Calculated Chemical Value Ti | DB注释(非中文) |
| 158 | LIM_DIV_IN_CNT | NUMBER | Y |  | Lime Divde Times | DB注释(非中文) |
| 159 | BLW_LIM_IN_QTY | NUMBER | Y |  | Blowing Lime Input Quantity | DB注释(非中文) |
| 160 | BLW_CAO_IN_TOT_QTY | NUMBER | Y |  | Before Blowing, total CaO Input Quantity | DB注释(非中文) |
| 161 | LOW_BLW_PTRN | VARCHAR2(3) | Y |  | Lower Blowing Pattern | DB注释(非中文) |
| 162 | LOW_BLW_GAS_TY | VARCHAR2(2) | Y |  | Lower Blowing Gas Type | DB注释(非中文) |
| 163 | TAP_LIM_IN_QTY | NUMBER | Y |  | During Tapping, Lime Input Quantity | DB注释(非中文) |
| 164 | TAP_FLUR_IN_QTY | NUMBER | Y |  | During Tapping, Florite Input Quantity | DB注释(非中文) |
| 165 | AL_MPZX_IN_QTY | NUMBER | Y |  | Al Mini Pellet Input Quantity | DB注释(非中文) |
| 166 | SLAG_COAT_BDOL_IN_QTY | NUMBER | Y |  | Slag Coating Burned Dolomite Input Quantity | DB注释(非中文) |
| 167 | SLAG_COAT_DOL_IN_QTY | NUMBER | Y |  | Slag Coating Dolomite Input Quantity | DB注释(非中文) |
| 168 | SLAG_COAT_LIM_IN_QTY | NUMBER | Y |  | Slag Coating Lime Input Quantity | DB注释(非中文) |
| 169 | N2_COAT_RSLT_PTRN | VARCHAR2(1) | Y |  | N2 Coating Result Pattern | DB注释(非中文) |
| 170 | SLAG_COAT_METHOD | VARCHAR2(1) | Y |  | Slag Coating Method | DB注释(非中文) |
| 171 | BTM_BB_TOT_CNT | NUMBER | Y |  | Bottom Bubbling Total Times | DB注释(非中文) |
| 172 | BTM_BB_TOT_DUR | NUMBER | Y |  | Bottom Bubbling Total Time 底部冒泡总时间 | DB注释(中文) |
| 173 | DE_P_AFT_FESI_IN_QTY | NUMBER | Y |  | FeSi Input Quantity after BOF De-P Process | DB注释(非中文) |
| 174 | DE_P_TOP_BLW_OXG_FLW | NUMBER | Y |  | Oxygen Flow in BOF De-P | DB注释(非中文) |
| 175 | CAO_IN_TOT_QTY | NUMBER | Y |  | Total CaO Input Weight(De-P) | DB注释(非中文) |
| 176 | BLW_OXG_USED_VOL1 | NUMBER | Y |  | Blwoing Oxygen Used Volume1 | DB注释(非中文) |
| 177 | BLW_OXG_1_TEMP | NUMBER | Y |  |  | 空 |
| 178 | BLW_OXG_USED_VOL2 | NUMBER | Y |  | Blwoing Oxygen Used Volume2 | DB注释(非中文) |
| 179 | BLW_OXG_2_TEMP | NUMBER | Y |  |  | 空 |
| 180 | BLW_OXG_USED_VOL3 | NUMBER | Y |  | Blwoing Oxygen Used Volume3 | DB注释(非中文) |
| 181 | BLW_OXG_USED_VOL4 | NUMBER | Y |  | Blwoing Oxygen Used Volume4 | DB注释(非中文) |
| 182 | CALC_SLAG_WGT | NUMBER | Y |  | Calculated Slag Weight | DB注释(非中文) |
| 183 | BOF_UNST_DES | VARCHAR2(150) | Y |  | BOF非稳态说明 | DB注释(中文) |
| 184 | WF_UNST_DES | VARCHAR2(150) | Y |  | WF非稳态说明 | DB注释(中文) |
| 185 | LF_UNST_DES | VARCHAR2(150) | Y |  | LF非稳态说明 | DB注释(中文) |
| 186 | RH_UNST_DES | VARCHAR2(150) | Y |  | RH非稳态说明 | DB注释(中文) |
| 187 | DB_GRADE | VARCHAR2(150) | Y |  | 低倍铸坯质量等级 | DB注释(中文) |
| 188 | DB_INFO | VARCHAR2(150) | Y |  | 低倍结果信息 | DB注释(中文) |
| 189 | RES_ORG | VARCHAR2(150) | Y |  | 责任单位 | DB注释(中文) |
| 190 | STD_STLGRD | VARCHAR2(20) | Y |  | 钢种 | DB注释(中文) |
| 191 | OXG_PRS | NUMBER | Y |  | 总管氧压 | DB注释(中文) |
| 192 | PROD_OXG_PRS | NUMBER | Y |  | 工作氧压 | DB注释(中文) |
| 193 | OXG_FLOW | NUMBER | Y |  | 氧气流量 | DB注释(中文) |
| 194 | LANCE_POSIT_START | NUMBER | Y |  | 开始枪位 | DB注释(中文) |
| 195 | LANCE_POSIT_PROGRESS | NUMBER | Y |  | 过程枪位 | DB注释(中文) |
| 196 | LANCE_POSIT_END | NUMBER | Y |  | 终点枪位 | DB注释(中文) |
| 197 | BEF_AR_TEMP | NUMBER | Y |  | 吹氩前温度 | DB注释(中文) |
| 198 | BOTTOM_STAT | VARCHAR2(2) | Y |  | 底吹情况 | DB注释(中文) |
| 199 | SHIFT_NO | VARCHAR2(2) | Y |  | 班次 | DB注释(中文) |
| 200 | SHIFT_GRP | VARCHAR2(2) | Y |  | 班组 | DB注释(中文) |
| 201 | CAPTAIN_NM | VARCHAR2(30) | Y |  | 机长 | DB注释(中文) |
| 202 | LADLE_COVER | VARCHAR2(2) | Y |  | 钢包加盖 | DB注释(中文) |
| 203 | SCRAP_CHARG_DUR | NUMBER | Y |  | 废钢装入时间 | DB注释(中文) |
| 204 | MIX_IRON_TIME | VARCHAR2(14) | Y |  | 兑铁水开始时间 | DB注释(中文) |
| 205 | MIX_IRON_DUR | NUMBER | Y |  | 兑铁水时间 | DB注释(中文) |
| 206 | PUT_SLAG_TIME | VARCHAR2(14) | Y |  | 倒渣时间 | DB注释(中文) |
| 207 | PUT_SLAG_DUR | NUMBER | Y |  | 倒渣时长 | DB注释(中文) |
| 208 | SLAG_SPLASH_DTM | VARCHAR2(14) | Y |  | 溅渣护炉 | DB注释(中文) |
| 209 | SLAG_SPLASH_DUR | NUMBER | Y |  | 溅渣护炉时长 | DB注释(中文) |
| 210 | IS_END | VARCHAR2(1) | Y |  | 炉次结束 | DB注释(中文) |
| 211 | SCRAP_CHARG_END_DTM | VARCHAR2(14) | Y |  | 废钢装入结束时间 | DB注释(中文) |
| 212 | MIX_IRON_END_TIME | VARCHAR2(14) | Y |  | 兑铁水结束时间 | DB注释(中文) |
| 213 | SLAG_SPLASH_END_DTM | VARCHAR2(14) | Y |  | 溅渣护炉结束 | DB注释(中文) |
| 214 | PUT_SLAG_END_TIME | VARCHAR2(14) | Y |  | 倒渣结束时间 | DB注释(中文) |
| 215 | LD_ARR_TIME | VARCHAR2(14) | Y |  | 钢包到达时间 | DB注释(中文) |
| 216 | LD_LV_TIME | VARCHAR2(14) | Y |  | 钢包离开时间 | DB注释(中文) |
| 217 | LD_HDL_DURA | NUMBER | Y |  | 转炉处理时间 | DB注释(中文) |
| 218 | BLOW_AR_DTM | NUMBER | Y |  | 吹氩时间 | DB注释(中文) |
| 219 | TURN_DOWN_CNT | NUMBER | Y |  | 倒炉次数 | DB注释(中文) |
| 220 | SLAG_SPLASH_PRS | NUMBER | Y |  | 溅渣压力 | DB注释(中文) |
| 221 | LADLE_COND | VARCHAR2(60) | Y |  | 钢包状况 | DB注释(中文) |
| 222 | FIRST_TURN_DOWN_TEMP | NUMBER | Y |  | 一次倒炉温度 | DB注释(中文) |
| 223 | SLAG_SPLASH_TIME | NUMBER | Y |  | 溅渣时间 | DB注释(中文) |
| 224 | POINT_BLOW_TIME | NUMBER | Y |  | 点吹时间 | DB注释(中文) |
| 225 | OXG_STA_DTM | DATE | Y |  | 吹氧开始时间 | DB注释(中文) |
| 226 | OXG_END_DTM | DATE | Y |  | 吹氧结束时间 | DB注释(中文) |

### SRS_ROLL_MASTER

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=47｜被读 21 过程 / 被写 13 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：2　**主键**：ROLL_NO　**语义覆盖**：63/64

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | ROLL_NO | VARCHAR2(8) | N | ✓ | ??? | DB注释(非中文) |
| 9 | PROC_CD | VARCHAR2(3) | Y |  | ????(EH1) | DB注释(非中文) |
| 10 | ROLL_STS | VARCHAR2(1) | Y |  | ????(0,1,2) | DB注释(非中文) |
| 11 | ROLL_PROG_CD | VARCHAR2(1) | Y |  | ????(A-Z) | DB注释(非中文) |
| 12 | ROLL_TY | VARCHAR2(10) | Y |  | ????(01-13) | DB注释(非中文) |
| 13 | RLG_MILL_TY | VARCHAR2(2) | Y |  |  | 空 |
| 14 | ROLL_MTRL | VARCHAR2(50) | Y |  | ?? | DB注释(非中文) |
| 15 | ROLL_INBND_DTM | VARCHAR2(14) | Y |  | ?????? | DB注释(非中文) |
| 16 | ROLL_INBND_SUMUP_DT | VARCHAR2(8) | Y |  | ???? | DB注释(非中文) |
| 17 | ROLL_INBND_EMP_ID | VARCHAR2(20) | Y |  | ???? | DB注释(非中文) |
| 18 | ROLL_INBND_SFT | VARCHAR2(2) | Y |  | ???? | DB注释(非中文) |
| 19 | ROLL_PO_NO | VARCHAR2(20) | Y |  | ??? | DB注释(非中文) |
| 20 | ROLL_MAK_CD | VARCHAR2(50) | Y |  | ??? | DB注释(非中文) |
| 21 | ROLL_WGT | NUMBER | Y |  | ???? | DB注释(非中文) |
| 22 | ROLL_BRL_LTH | VARCHAR2(20) | Y |  | ????? | DB注释(非中文) |
| 23 | ROLL_HARD_INIT | VARCHAR2(20) | Y |  | ???? | DB注释(非中文) |
| 24 | ROLL_HARD_DISCARD | VARCHAR2(20) | Y |  | ???? | DB注释(非中文) |
| 25 | ROLL_HARD_CURR | NUMBER | Y |  | Roll Hardness Current | SCO_DATA_DIC(D) |
| 26 | ROLL_DIA_INIT | VARCHAR2(20) | Y |  | ???? | DB注释(非中文) |
| 27 | ROLL_DIA_DISCARD | VARCHAR2(20) | Y |  | ???? | DB注释(非中文) |
| 28 | ROLL_DIA_CURR | NUMBER | Y |  | ???? | DB注释(非中文) |
| 29 | ROLL_DIA_EFFECTIVE | NUMBER | Y |  | Roll Diameter Effective | SCO_DATA_DIC(D) |
| 30 | ROLL_ROUGH | NUMBER | Y |  | ????mpa | DB注释(非中文) |
| 31 | ROLL_DISCARD_DTM | VARCHAR2(14) | Y |  | ?????? | DB注释(非中文) |
| 32 | ROLL_DISCARD_SUMUP_DT | VARCHAR2(8) | Y |  | ???? | DB注释(非中文) |
| 33 | ROLL_DISCARD_EMP_ID | VARCHAR2(20) | Y |  | ???? | DB注释(非中文) |
| 34 | ROLL_DISCARD_SFT | VARCHAR2(2) | Y |  | ???? | DB注释(非中文) |
| 35 | ROLL_DISCARD_RSN_TY | VARCHAR2(20) | Y |  | ???? | DB注释(非中文) |
| 36 | ROLL_LOC_TY | VARCHAR2(3) | Y |  | ??/???T/B? | DB注释(非中文) |
| 37 | ROLL_STAND_TY | VARCHAR2(20) | Y |  | ?????? | DB注释(非中文) |
| 38 | ROLL_INST_SEQ | NUMBER | Y |  | ??? | DB注释(非中文) |
| 39 | ROLL_NO_REL | VARCHAR2(8) | Y |  | ??? | DB注释(非中文) |
| 40 | CCK_NO_WS | VARCHAR2(8) | Y |  | ??????WS | DB注释(非中文) |
| 41 | CCK_NO_DS | VARCHAR2(8) | Y |  | ??????DS | DB注释(非中文) |
| 42 | BRG_NO_WS | VARCHAR2(8) | Y |  | ???????WS | DB注释(非中文) |
| 43 | BRG_NO_DS | VARCHAR2(8) | Y |  | ???????DS | DB注释(非中文) |
| 44 | BRG_NO_WT | VARCHAR2(8) | Y |  | Bearing No WT | SCO_DATA_DIC(L) |
| 45 | ASSEMBLY_YN | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 46 | REMARKS | VARCHAR2(1000) | Y |  | ?? | DB注释(非中文) |
| 47 | CHEM_C | VARCHAR2(20) | Y |  | CHEM_C | DB注释(非中文) |
| 48 | CHEM_SI | VARCHAR2(20) | Y |  | CHEM_SI | DB注释(非中文) |
| 49 | CHEM_MN | VARCHAR2(20) | Y |  | CHEM_MN | DB注释(非中文) |
| 50 | CHEM_P | VARCHAR2(20) | Y |  | CHEM_P | DB注释(非中文) |
| 51 | CHEM_S | VARCHAR2(20) | Y |  | CHEM_S | DB注释(非中文) |
| 52 | CHEM_NI | VARCHAR2(20) | Y |  | CHEM_NI | DB注释(非中文) |
| 53 | CHEM_CR | VARCHAR2(20) | Y |  | CHEM_CR | DB注释(非中文) |
| 54 | CHEM_MO | VARCHAR2(20) | Y |  | CHEM_MO | DB注释(非中文) |
| 55 | CHEM_MG | VARCHAR2(20) | Y |  | CHEM_MG | DB注释(非中文) |
| 56 | REV_DTIME | VARCHAR2(14) | Y |  | ???? | DB注释(非中文) |
| 57 | ASSEMBLY_DTIME | VARCHAR2(14) | Y |  | ???? | DB注释(非中文) |
| 58 | ASSEMBLY_EMP_ID | VARCHAR2(20) | Y |  | ???? | DB注释(非中文) |
| 59 | ON_DTIME | VARCHAR2(14) | Y |  | ???? | DB注释(非中文) |
| 60 | ON_EMP_ID | VARCHAR2(20) | Y |  | ???? | DB注释(非中文) |
| 61 | OFF_DTIME | VARCHAR2(14) | Y |  | ???? | DB注释(非中文) |
| 62 | OFF_EMP_ID | VARCHAR2(20) | Y |  | ???? | DB注释(非中文) |
| 63 | DME_DTIME | VARCHAR2(14) | Y |  | ?????disassemble time? | DB注释(非中文) |
| 64 | DME_EMP_ID | VARCHAR2(20) | Y |  | ?????disassemble person? | DB注释(非中文) |

### SPG_ORD_PROG

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=46｜被读 38 过程 / 被写 4 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：8401　**主键**：ORD_NO、ORD_LN　**语义覆盖**：78/93

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | ORD_NO | VARCHAR2(30) | N | ✓ | Order no | DB注释(非中文) |
| 9 | ORD_LN | VARCHAR2(3) | N | ✓ | Order line | DB注释(非中文) |
| 10 | ORD_PROG_STS | VARCHAR2(1) | N |  | Order Modification | DB注释(非中文) |
| 11 | ORD_LN_QTY | NUMBER | N |  | Order Line quantity | DB注释(非中文) |
| 12 | BFHM | NUMBER | N |  | BFHM(Balance for Heat Making) | DB注释(非中文) |
| 13 | ORD_TY | VARCHAR2(2) | N |  | Order Type | DB注释(非中文) |
| 14 | PROD_CD | VARCHAR2(3) | N |  | Products code | DB注释(非中文) |
| 15 | CUST_CD | VARCHAR2(20) | N |  | customer code | DB注释(非中文) |
| 16 | SPEC_CD | VARCHAR2(50) | N |  | specification code | DB注释(非中文) |
| 17 | ORD_USAGE | VARCHAR2(4) | Y |  | Order usage | DB注释(非中文) |
| 18 | ORD_THK | NUMBER | Y |  | Order Thickness | DB注释(非中文) |
| 19 | ORD_WTH | NUMBER | Y |  | Order width | DB注释(非中文) |
| 20 | ORD_LTH | NUMBER | Y |  | Order length | DB注释(非中文) |
| 21 | ORD_QTY_TOL_TY | VARCHAR2(1) | Y |  | Tolerance Type of Order Quantity | DB注释(非中文) |
| 22 | ORD_QTY_TOL_MAX | NUMBER | Y |  | Order Quantity Tolerance Maximun Value | DB注释(非中文) |
| 23 | ORD_QTY_TOL_MIN | NUMBER | Y |  | Order Quantity Tolerance Miniimun Value | DB注释(非中文) |
| 24 | PACK_PROD_WGT_MIN | NUMBER | Y |  | Minimum  quantity of Products Packing | DB注释(非中文) |
| 25 | PACK_PROD_WGT_MAX | NUMBER | Y |  | Maximum quantity of Products Packing | DB注释(非中文) |
| 26 | ORD_DELV_DT | VARCHAR2(8) | Y |  | Order Dellevery Date | DB注释(非中文) |
| 27 | ORD_RCV_DTM | VARCHAR2(14) | Y |  | Order Receive Date | DB注释(非中文) |
| 28 | URGENT_FL | VARCHAR2(1) | Y |  | Urgent Flag | DB注释(非中文) |
| 29 | INWH_QTY | NUMBER | Y |  | Quantity of In Warehousing | DB注释(非中文) |
| 30 | ORD_CHG_QTY | NUMBER | Y |  | Quantity of Order Change quantity | DB注释(非中文) |
| 31 | DISPATCHED_QTY | NUMBER | Y |  | Quantity of Dispatched | DB注释(非中文) |
| 32 | POSS_PASS_PLANT_CD | VARCHAR2(30) | Y |  | Possible Pass Plant Code | DB注释(非中文) |
| 33 | CONF_PASS_PLANT_CD | VARCHAR2(30) | Y |  | Confirm Pass Plant Code | DB注释(非中文) |
| 34 | CONF_PASS_PLANT_OP_CD | VARCHAR2(60) | Y |  | Confirm Pass Plant Process Code | DB注释(非中文) |
| 35 | FAC_DCN_CONF_YN | VARCHAR2(1) | Y |  | Factory Dececion Yes or No | DB注释(非中文) |
| 36 | FAC_DCN_CONF_DT | VARCHAR2(8) | Y |  | Factory Dececion Date | DB注释(非中文) |
| 37 | QLTY_LMT_DT | VARCHAR2(8) | Y |  |  | 空 |
| 38 | SMS_LMT_DT | VARCHAR2(8) | Y |  | Steel Making Limit Date | DB注释(非中文) |
| 39 | HR_LMT_DT | VARCHAR2(8) | Y |  | Hot rolling Limit Date | DB注释(非中文) |
| 40 | PROD_LMT_DT | VARCHAR2(8) | Y |  | Products Limit Date | DB注释(非中文) |
| 41 | DISP_LMT_DT | VARCHAR2(8) | Y |  | Dispatch Limit Date | DB注释(非中文) |
| 42 | PROD_END_FL | VARCHAR2(2) | Y |  | Production End Type | DB注释(非中文) |
| 43 | PROD_END_EMP_ID | VARCHAR2(20) | Y |  | Production End Employ ID | DB注释(非中文) |
| 44 | PROD_END_DTM | VARCHAR2(14) | Y |  | Production End Date | DB注释(非中文) |
| 45 | DISP_END_FL | VARCHAR2(2) | Y |  | Dispatch End Type | DB注释(非中文) |
| 46 | DISP_END_EMP_ID | VARCHAR2(20) | Y |  | Dispatch End Employ ID | DB注释(非中文) |
| 47 | DISP_END_DTM | VARCHAR2(14) | Y |  | Dispatch End Date | DB注释(非中文) |
| 48 | CHG_ORD_NO | VARCHAR2(10) | Y |  |  | 空 |
| 49 | CHG_ORD_LN | VARCHAR2(3) | Y |  |  | 空 |
| 50 | SLAB_DGN_THK_RNG_MIN | NUMBER | Y |  | Slab Design Thckness minimun | DB注释(非中文) |
| 51 | SLAB_DGN_THK_RNG_MAX | NUMBER | Y |  | Slab Design Thckness maximun | DB注释(非中文) |
| 52 | SLAB_DGN_WTH_RNG_MIN | NUMBER | Y |  | Slab Design Width minimun | DB注释(非中文) |
| 53 | SLAB_DGN_WTH_RNG_MAX | NUMBER | Y |  | Slab Design Width maximun | DB注释(非中文) |
| 54 | SLAB_DGN_LTH_RNG_MIN | NUMBER | Y |  | Slab Design Length minimun | DB注释(非中文) |
| 55 | SLAB_DGN_LTH_RNG_MAX | NUMBER | Y |  | Slab Design Length maximun | DB注释(非中文) |
| 56 | SLAB_DGN_AIM_WGT | NUMBER | Y |  | Slab Design Quantity Target | DB注释(非中文) |
| 57 | SLAB_DGN_WGT_RNG_MIN | NUMBER | Y |  | Slab Design Quantity minimun | DB注释(非中文) |
| 58 | SLAB_DGN_WGT_RNG_MAX | NUMBER | Y |  | Slab Design Quantity maximun | DB注释(非中文) |
| 59 | PROD_RATE | NUMBER | Y |  | Rate of Products | DB注释(非中文) |
| 60 | ADD_QTY | NUMBER | Y |  | Additional Quantity | DB注释(非中文) |
| 61 | ADD_QTY_REG_EMP_ID | VARCHAR2(20) | Y |  | Additional Quantity Register Employee | DB注释(非中文) |
| 62 | ADD_QTY_REG_DT | VARCHAR2(14) | Y |  | Additional Quantity Register | DB注释(非中文) |
| 63 | PROD_BAD_QTY | NUMBER | Y |  |  | 空 |
| 64 | PROD_BAD_CNT | NUMBER | Y |  |  | 空 |
| 65 | CC_YIELD | NUMBER | Y |  |  | 空 |
| 66 | HR_YIELD | NUMBER | Y |  |  | 空 |
| 67 | HR_CRCTN_YIELD | NUMBER | Y |  |  | 空 |
| 68 | PPL_YIELD | NUMBER | Y |  |  | 空 |
| 69 | PCM_YIELD | NUMBER | Y |  |  | 空 |
| 70 | CAL_YIELD | NUMBER | Y |  |  | 空 |
| 71 | CGL_YIELD | NUMBER | Y |  |  | 空 |
| 72 | RCL_YIELD | NUMBER | Y |  |  | 空 |
| 73 | TOT_YIELD | NUMBER | Y |  |  | 空 |
| 74 | PROD_HOLD_FL | VARCHAR2(2) | Y |  | Order Hold Flag | SCO_DATA_DIC(D) |
| 75 | PROD_HOLD_EMP_ID | VARCHAR2(20) | Y |  | Order Hold EMP ID | SCO_DATA_DIC(D) |
| 76 | PROD_HOLD_DTM | VARCHAR2(14) | Y |  | Order Hold DateTime | SCO_DATA_DIC(D) |
| 77 | PROD_HOLD_BEF_STS | VARCHAR2(1) | Y |  | Order Hold Before Status | SCO_DATA_DIC(D) |
| 78 | ORD_INPUT_DT | VARCHAR2(8) | Y |  | Order input Date | SCO_DATA_DIC(D) |
| 79 | SCH_PLAN_DTM | VARCHAR2(14) | Y |  | Schedule Plan Date | DB注释(非中文) |
| 80 | ORD_LN_PCS | NUMBER | Y |  | Order Line Piece | DB注释(非中文) |
| 81 | BFHM_PCS | NUMBER | Y |  | BFHM(Balance for Heat Making) Piece | DB注释(非中文) |
| 82 | FINISH_REASON | VARCHAR2(200) | Y |  |  | 空 |
| 83 | ORD_OVERDUE_FL | VARCHAR2(2) | Y |  | 订单逾期交付标记，N:未超期 | DB注释(中文) |
| 84 | ORD_OVERDUE_EMP_ID | VARCHAR2(20) | Y |  | 标记人员 | DB注释(中文) |
| 85 | ORD_OVERDUE_DTM | VARCHAR2(14) | Y |  | 标记时间 | DB注释(中文) |
| 86 | ORD_IMP_FL | VARCHAR2(1) | Y |  | 重点订单标记,Y:重点 | DB注释(中文) |
| 87 | ORD_IMP_EMP_ID | VARCHAR2(20) | Y |  | 标记人员 | DB注释(中文) |
| 88 | ORD_IMP_DTM | VARCHAR2(14) | Y |  | 标记时间 | DB注释(中文) |
| 89 | ACT_PLT_CD | VARCHAR2(1) | Y |  | 实际产线 | DB注释(中文) |
| 90 | ORD_SEL_DTM | VARCHAR2(14) | Y |  | 订单选定时间 | DB注释(中文) |
| 91 | ORD_DSN_DTM | VARCHAR2(14) | Y |  | 钢坯设计时间 | DB注释(中文) |
| 92 | ORD_HEAT_DTM | VARCHAR2(14) | Y |  | 组炉组浇时间 | DB注释(中文) |
| 93 | ORD_BATCH_DTM | VARCHAR2(14) | Y |  | 轧制计划编制时间 | DB注释(中文) |

### SSD_CUSTOMER

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=46｜被读 44 过程 / 被写 1 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：128　**主键**：CUST_CD　**语义覆盖**：34/34

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | CUST_CD | VARCHAR2(20) | N | ✓ | 客户编码 | DB注释(中文) |
| 9 | CUST_NM | VARCHAR2(100) | N |  | 客户名称 | DB注释(中文) |
| 10 | CUST_NM_ENG | VARCHAR2(100) | Y |  | 英文名 | DB注释(中文) |
| 11 | COUNTRY_CD | VARCHAR2(3) | Y |  | 国家 | DB注释(中文) |
| 12 | SITE_CLF | VARCHAR2(3) | Y |  | 区域 | DB注释(中文) |
| 13 | PROVINCE_CD | VARCHAR2(2) | Y |  | 省份 | DB注释(中文) |
| 14 | CITY_CD | VARCHAR2(10) | Y |  | 城市 | DB注释(中文) |
| 15 | ADDR | VARCHAR2(200) | Y |  | 地址 | DB注释(中文) |
| 16 | REP_NM | VARCHAR2(20) | Y |  | 负责人 | DB注释(中文) |
| 17 | CORP_NM | VARCHAR2(100) | Y |  | 法人 | DB注释(中文) |
| 18 | TEL_NO | VARCHAR2(20) | Y |  | 电话 | DB注释(中文) |
| 19 | BIZ_REG_NO | VARCHAR2(20) | Y |  | 营业执照号 | DB注释(中文) |
| 20 | ZIP_CD | VARCHAR2(10) | Y |  | 邮政编码 | DB注释(中文) |
| 21 | E_MAIL_ADDR | VARCHAR2(50) | Y |  | 电子邮件 | DB注释(中文) |
| 22 | CUST_GRD | VARCHAR2(2) | Y |  | 客户等级 | DB注释(中文) |
| 23 | CUST_KIND | VARCHAR2(2) | Y |  | 客户分类 | DB注释(中文) |
| 24 | SALES_CHNL_CD | VARCHAR2(2) | Y |  | 销售渠道 | DB注释(中文) |
| 25 | BANK_CD | VARCHAR2(10) | Y |  | 银行名称 | DB注释(中文) |
| 26 | ACCOUNT_NO | VARCHAR2(30) | Y |  | 银行账户 | DB注释(中文) |
| 27 | USE_YN | VARCHAR2(1) | Y |  | 是否使用 | DB注释(中文) |
| 28 | MDM_CRT_DTM | VARCHAR2(14) | Y |  | Creation Datetime | DB注释(非中文) |
| 29 | MDM_CRT_USER_ID | VARCHAR2(20) | Y |  | Creation User ID | DB注释(非中文) |
| 30 | MDM_UPD_DTM | VARCHAR2(14) | Y |  | Update Datetime | DB注释(非中文) |
| 31 | MDM_UPD_USER_ID | VARCHAR2(20) | Y |  | Update User ID | DB注释(非中文) |
| 32 | IMPORTANT_YN | VARCHAR2(1) | Y |  | 重点客户与否 | DB注释(中文) |
| 33 | IMPORTANT_DTM | VARCHAR2(14) | Y |  | 重点客户标记时间 | DB注释(中文) |
| 34 | TAX_REF_NO | VARCHAR2(50) | Y |  | 纳税登记号 | DB注释(中文) |

### SPR_DEFECT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=44｜被读 30 过程 / 被写 7 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：1695　**主键**：PROC_CD、PLT_NO、DEF_CD、DEF_SURF_CD　**语义覆盖**：23/23

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | PROC_CD | VARCHAR2(3) | N | ✓ | 工序代码 | DB注释(中文) |
| 9 | PLT_NO | VARCHAR2(18) | N | ✓ | PLT NO | DB注释(非中文) |
| 10 | DEF_CD | VARCHAR2(4) | N | ✓ | Defect Code | DB注释(非中文) |
| 11 | DEF_GRD | VARCHAR2(4) | Y |  | Defect Grade | DB注释(非中文) |
| 12 | DEF_SURF_CD | VARCHAR2(4) | N | ✓ | Defect Surface Code | DB注释(非中文) |
| 13 | DEF_LTH_DIR | NUMBER | Y |  | Defect length Direction | DB注释(非中文) |
| 14 | DEF_WTH_DIR | NUMBER | Y |  | Defect width Direction | DB注释(非中文) |
| 15 | DEF_LTH | NUMBER | Y |  | Defect length | DB注释(非中文) |
| 16 | DEF_CMT | VARCHAR2(500) | Y |  | Defect Comments | DB注释(非中文) |
| 17 | DEF_CMT_CD | VARCHAR2(2) | Y |  | Defect Comments Code | DB注释(非中文) |
| 18 | DEF_WK_DTM | VARCHAR2(14) | Y |  | Defect Work Date | DB注释(非中文) |
| 19 | DEF_WK_EMP_ID | VARCHAR2(20) | Y |  | Defect Worker Employee ID | DB注释(非中文) |
| 20 | REP_YN | VARCHAR2(1) | Y |  | 是否代表缺陷 | DB注释(中文) |
| 21 | LSN_CD | VARCHAR2(2) | Y |  | Liaison Code | DB注释(非中文) |
| 22 | FAC_CD | VARCHAR2(1) | Y |  | 工厂代码 | DB注释(中文) |
| 23 | APP_DEF_PROC | VARCHAR2(10) | Y |  | Surface Defect Process | SCO_DATA_DIC(D) |

### SMS_RSLT_HEAT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=43｜被读 39 过程 / 被写 2 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：10589　**主键**：HEAT_NO、PROC_PASS_CNT　**语义覆盖**：184/185

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | HEAT_NO | VARCHAR2(10) | N | ✓ | 炉次号 | DB注释(中文) |
| 9 | PROC_PASS_CNT | NUMBER | N | ✓ | Process pass times | DB注释(非中文) |
| 10 | PLAN_HEAT_NO | VARCHAR2(8) | Y |  | Plan Heat No | DB注释(非中文) |
| 11 | PROC_MC_NO | VARCHAR2(1) | Y |  | 铸机号 | DB注释(中文) |
| 12 | CAST_NO | VARCHAR2(8) | Y |  | 浇次号 | DB注释(中文) |
| 13 | HEAT_CNT | NUMBER | Y |  | 浇次内炉数 | DB注释(中文) |
| 14 | HEAT_PRI | NUMBER | Y |  | 浇内顺序 | DB注释(中文) |
| 15 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  | 内控钢种 | DB注释(中文) |
| 16 | TD_CHANGE_TY | VARCHAR2(1) | Y |  | Tundish Change Type | DB注释(非中文) |
| 17 | CAST_COMP_TY | VARCHAR2(1) | Y |  | Casting Completion Type | DB注释(非中文) |
| 18 | ARR_DTM | VARCHAR2(14) | Y |  | Ladle arrival date | DB注释(非中文) |
| 19 | TUR_WAIT_ARR_DTM | VARCHAR2(14) | Y |  | Turret  Waiting Arrival Date | DB注释(非中文) |
| 20 | LD_OPEN_TY | VARCHAR2(1) | Y |  | Ladle Open Type | DB注释(非中文) |
| 21 | LD_OPEN_PUR_YN | VARCHAR2(1) | Y |  | Ladle Open Y/N | DB注释(非中文) |
| 22 | LD_PUR_STA_DTM | VARCHAR2(14) | Y |  | Ladle Puring Start Date | DB注释(非中文) |
| 23 | LD_PUR_END_DTM | VARCHAR2(14) | Y |  | Ladle Puring End Date | DB注释(非中文) |
| 24 | LD_PUR_DUR | NUMBER | Y |  | Ladle Puring Time | DB注释(非中文) |
| 25 | DB_INS_STA_DTM | VARCHAR2(14) | Y |  | DummyBar Insert Start Date | DB注释(非中文) |
| 26 | DB_INS_END_DTM | VARCHAR2(14) | Y |  | DummyBar Insert End Date | DB注释(非中文) |
| 27 | DB_INS_DUR | NUMBER | Y |  | Dummy Bar Insert Time | DB注释(非中文) |
| 28 | CUT_STA_DTM | VARCHAR2(14) | Y |  | Uncond Slab Cutting Start Date | DB注释(非中文) |
| 29 | CUT_END_DTM | VARCHAR2(14) | Y |  | Uncond Slab Cutting End Date | DB注释(非中文) |
| 30 | CAST_STA_DTM | VARCHAR2(14) | Y |  | 开浇时间 | DB注释(中文) |
| 31 | CAST_END_DTM | VARCHAR2(14) | Y |  | 终浇时间 | DB注释(中文) |
| 32 | CAST_PROC_DUR | NUMBER | Y |  | 浇铸时间 | DB注释(中文) |
| 33 | TUR_LD_DEP_DTM | VARCHAR2(14) | Y |  | Ladle turrent departure date | DB注释(非中文) |
| 34 | SUMUP_DT | VARCHAR2(8) | Y |  | Operation Sumup date | DB注释(非中文) |
| 35 | OPER_SHIFT | VARCHAR2(2) | Y |  | Operation Shift | DB注释(非中文) |
| 36 | CAST_AVG_SPD | NUMBER | Y |  | Casting Average Speed | DB注释(非中文) |
| 37 | ARR_STEEL_WGT | NUMBER | Y |  | Arrival Heat Weight at Ladle Turret | DB注释(非中文) |
| 38 | RCP_STEEL_WGT | NUMBER | Y |  | Receipt Heat Weight | DB注释(非中文) |
| 39 | LD_REM_WGT | NUMBER | Y |  | Ladle Remain Weight | DB注释(非中文) |
| 40 | HCROP_WGT | NUMBER | Y |  | Head Crop Weight | DB注释(非中文) |
| 41 | TCROP_WGT | NUMBER | Y |  | Tail Crop Weight | DB注释(非中文) |
| 42 | SMPING_WGT | NUMBER | Y |  | Sampling Weight | DB注释(非中文) |
| 43 | CAST_SKULL_WGT | NUMBER | Y |  | ?????? | DB注释(非中文) |
| 44 | SLAB_PROD_TOT_WGT | NUMBER | Y |  | Heat Total Slab Production Weight | DB注释(非中文) |
| 45 | CUT_SLAB_CNT | NUMBER | Y |  | Nos of Uncond Slab | DB注释(非中文) |
| 46 | CUT_SLAB_YIELD | NUMBER | Y |  | Uncond Slab Yield | DB注释(非中文) |
| 47 | CAST_TOT_LEN | NUMBER | Y |  | Casting Total Length | DB注释(非中文) |
| 48 | MLD_ENTRY_CW_TEMP | NUMBER | Y |  | Mold Entry Side Cooling water Temperature | DB注释(非中文) |
| 49 | MLD_EXIT_CW_TEMP | NUMBER | Y |  | Mold Exit Side Cooling Water Temperature | DB注释(非中文) |
| 50 | TD_TGT_TEMP | NUMBER | Y |  | ??????? | DB注释(非中文) |
| 51 | LD_NO | VARCHAR2(20) | Y |  | 钢包 | DB注释(中文) |
| 52 | LD_TUR_ARM_NO | VARCHAR2(1) | Y |  | Ladle Turret Arm No | DB注释(非中文) |
| 53 | CAST_COMP_FL | VARCHAR2(1) | Y |  | C. Casting Complete Y/N | DB注释(非中文) |
| 54 | TD_MOVE_STA_DTM | VARCHAR2(14) | Y |  | Tundish Move Start Date | DB注释(非中文) |
| 55 | TD_MOVE_END_DTM | VARCHAR2(14) | Y |  | Tundish Move End Date | DB注释(非中文) |
| 56 | TD_MOVE_DUR | NUMBER | Y |  | Tundish Move Time | DB注释(非中文) |
| 57 | SURF_AUTO_MSU_STA_TM | NUMBER | Y |  | ?????????? | DB注释(非中文) |
| 58 | SURF_AUTO_MSU_END_TM | NUMBER | Y |  | ?????????? | DB注释(非中文) |
| 59 | MLAC_SQT_HIT_RATE | NUMBER | Y |  | MLAC SQT Hit Rate | DB注释(非中文) |
| 60 | RTN_REASON_CD | VARCHAR2(2) | Y |  | Return Reason Code | DB注释(非中文) |
| 61 | TD_CAR_NO | VARCHAR2(1) | Y |  | Tundish Car No | DB注释(非中文) |
| 62 | CUT_SLAB_DIR_WTH | NUMBER | Y |  | Uncond Slab instruction width | DB注释(非中文) |
| 63 | CUT_SLAB_LTH_CONT_RATE | NUMBER | Y |  | Uncond Slab Length Contraction Rate | DB注释(非中文) |
| 64 | CUT_SLAB_WTH_CONT_RATE | NUMBER | Y |  | Uncond Slab Length Contraction Rate Standard | DB注释(非中文) |
| 65 | X_STR_HCROP_WGT | NUMBER | Y |  | X Strand Head Crop Weight | DB注释(非中文) |
| 66 | X_STR_TCROP_WGT | NUMBER | Y |  | X Strand Tail Crop Weight | DB注释(非中文) |
| 67 | Y_STR_HCROP_WGT | NUMBER | Y |  | Y Strand Head Crop Weight | DB注释(非中文) |
| 68 | Y_STR_TCROP_WGT | NUMBER | Y |  | Y Strand Tail Crop Weight | DB注释(非中文) |
| 69 | COOLING_CTRL_PTRN1 | VARCHAR2(32) | Y |  | Cooling Control Pattern1 | DB注释(非中文) |
| 70 | COOLING_CTRL_PTRN2 | VARCHAR2(32) | Y |  | Cooling Control Pattern2 | DB注释(非中文) |
| 71 | SOFT_REDUCT_PTRN1 | VARCHAR2(32) | Y |  | ???Pattern1 | DB注释(非中文) |
| 72 | SOFT_REDUCT_PTRN2 | VARCHAR2(32) | Y |  | ???Pattern2 | DB注释(非中文) |
| 73 | MLD_EMS_PTRN1 | VARCHAR2(2) | Y |  | ???EMS_Pattern?? 1 | DB注释(非中文) |
| 74 | MLD_EMS_PTRN2 | VARCHAR2(2) | Y |  | ???EMS_Pattern?? 2 | DB注释(非中文) |
| 75 | EMLA_LS_APPLY_PTRN1 | NUMBER | Y |  | EMLA_LS??Pattern1 | DB注释(非中文) |
| 76 | EMLA_LS_APPLY_PTRN2 | NUMBER | Y |  | EMLA_LS??Pattern2 | DB注释(非中文) |
| 77 | TD_INSUL_TY | VARCHAR2(20) | Y |  | Tundish Insulator Type | DB注释(非中文) |
| 78 | TD_INSUL_USED_WGT | NUMBER | Y |  | Tundish Insulator Used Weight | DB注释(非中文) |
| 79 | TD_FLUX_IN_HEAT_WGT | NUMBER | Y |  | ???Flux?????? | DB注释(非中文) |
| 80 | STOP_OCC_EQUIP_LOC_CD | VARCHAR2(6) | Y |  | ?????????? | DB注释(非中文) |
| 81 | TD_NO | VARCHAR2(4) | Y |  | 中包号 | DB注释(中文) |
| 82 | TD_OVF_WGT | NUMBER | Y |  | Tundish Over Flow Weight | DB注释(非中文) |
| 83 | TD_SKULL_WGT | NUMBER | Y |  | Tundish Skull Weight | DB注释(非中文) |
| 84 | CAST_STA_TD_STEEL_WGT | NUMBER | Y |  | Tundish Steel Weight when Casting Start Time | DB注释(非中文) |
| 85 | LD_EXCHG_TD_STEEL_WGT | NUMBER | Y |  | Steel Weight in Tundish | DB注释(非中文) |
| 86 | TD_PRE_HEATING_STA_DTM | VARCHAR2(14) | Y |  | TD Pre-Heating Start Date | DB注释(非中文) |
| 87 | TD_PRE_HEATING_END_DTM | VARCHAR2(14) | Y |  | TD Pre-Heating End Date | DB注释(非中文) |
| 88 | TD_PRE_HEATING_DUR | NUMBER | Y |  | Tundish Heating Time | DB注释(非中文) |
| 89 | TD_AVG_TEMP | NUMBER | Y |  | ??????? | DB注释(非中文) |
| 90 | SAME_TD_IN_HEAT_PRI | NUMBER | Y |  | In Same Tundish, Heat priority | DB注释(非中文) |
| 91 | SH_NZ_TY | VARCHAR2(20) | Y |  | Shroud Nozzle Type | DB注释(非中文) |
| 92 | SLAG_DETECT_STS | VARCHAR2(1) | Y |  | Slag Detector Status | DB注释(非中文) |
| 93 | SH_NZ_SEAL_GAS_FLW | NUMBER | Y |  | Shroud Nozzle Sealing Gas Flow | DB注释(非中文) |
| 94 | SH_NZ_SEAL_GAS_PRS | NUMBER | Y |  | Shroud Nozzle Sealing Gas Pressure | DB注释(非中文) |
| 95 | ERP_POSTING_CNT | NUMBER | Y |  | ERP Posting times | DB注释(非中文) |
| 96 | ERP_POSTING_DTM | VARCHAR2(14) | Y |  | ERP Posting Date | DB注释(非中文) |
| 97 | OPER_EMP_NO | VARCHAR2(20) | Y |  | Operator Employee No | DB注释(非中文) |
| 98 | HEAT_TREATMENT | VARCHAR2(2) | Y |  |  | 空 |
| 99 | MD_POWDER_TY1 | VARCHAR2(20) | Y |  | Mold powder type strand 1 | DB注释(非中文) |
| 100 | MD_POWDER_TY2 | VARCHAR2(20) | Y |  | Mold powder type strand 2 | DB注释(非中文) |
| 101 | OPER_COMMENT | VARCHAR2(500) | Y |  | Operator comment | DB注释(非中文) |
| 102 | CC_PLAN_NO | VARCHAR2(10) | Y |  | C.Casting Plan No | SCO_DATA_DIC(D) |
| 103 | CAST_START_WGT | NUMBER | Y |  | 开浇重量 | DB注释(中文) |
| 104 | CAST_END_WGT | NUMBER | Y |  | 停浇重量 | DB注释(中文) |
| 105 | NET_WGT | NUMBER | Y |  | 净重 | DB注释(中文) |
| 106 | REQ_STEEL_TMP | NUMBER | Y |  | 要钢温度 | DB注释(中文) |
| 107 | ARR_TEMP | NUMBER | Y |  | 到站温度 | DB注释(中文) |
| 108 | FLOW_STS | VARCHAR2(10) | Y |  | 自流情况 | DB注释(中文) |
| 109 | LD_COVER | VARCHAR2(10) | Y |  | 钢包加盖 | DB注释(中文) |
| 110 | RTN_WGT | NUMBER | Y |  | 回炉重量 | DB注释(中文) |
| 111 | PROTECT_SLAG | VARCHAR2(10) | Y |  | 保护渣 | DB注释(中文) |
| 112 | LD_ARR_TIME | VARCHAR2(14) | Y |  | 包到时间 | DB注释(中文) |
| 113 | PROD_DATE | VARCHAR2(8) | Y |  | 生产日期 | DB注释(中文) |
| 114 | SHIFT_NO | VARCHAR2(2) | Y |  | 班次 | DB注释(中文) |
| 115 | SHIFT_CD | VARCHAR2(20) | Y |  | 班组 | DB注释(中文) |
| 116 | COLD_WATER_PRES | NUMBER | Y |  | 二冷水压 | DB注释(中文) |
| 117 | FLOW_AMT | NUMBER | Y |  | 设备水流量 | DB注释(中文) |
| 118 | END_WATER_PRES | NUMBER | Y |  | 闭环水压力 | DB注释(中文) |
| 119 | FAC_NAME | VARCHAR2(8) | Y |  | 厂家 | DB注释(中文) |
| 120 | CRYS_WATER_PRES | NUMBER | Y |  | 结晶器水压 | DB注释(中文) |
| 121 | AFTER_STRAIT_TEMP | NUMBER | Y |  | 矫直后温度 | DB注释(中文) |
| 122 | BEFORE_STRAIT_TEMP | NUMBER | Y |  | 矫直前温度 | DB注释(中文) |
| 123 | TD_A | NUMBER | Y |  | 中包A | DB注释(中文) |
| 124 | TD_B | NUMBER | Y |  | 中包B | DB注释(中文) |
| 125 | FINISH_TYPE | VARCHAR2(1) | Y |  | 完成区分 | DB注释(中文) |
| 126 | QLD_SLAB_AMT | NUMBER | Y |  | 合格只数 | DB注释(中文) |
| 127 | CAST_RULE | NUMBER | Y |  | 定尺 | DB注释(中文) |
| 128 | SLAB_PROD_AMT | NUMBER | Y |  | 铸坯产量 | DB注释(中文) |
| 129 | UNQLD_SLAB_AMT | NUMBER | Y |  | 不合格只数 | DB注释(中文) |
| 130 | WORK_LEADER | VARCHAR2(1) | Y |  | 机长 | DB注释(中文) |
| 131 | REMARK | VARCHAR2(200) | Y |  | 备注 | DB注释(中文) |
| 132 | PROC_CD | VARCHAR2(20) | Y |  | 工序 | DB注释(中文) |
| 133 | GROSS_WGT | NUMBER | Y |  | 毛重 | DB注释(中文) |
| 134 | TARE_WGT | NUMBER | Y |  | 皮重 | DB注释(中文) |
| 135 | CAST_COMMENT | VARCHAR2(200) | Y |  | 开浇情况 | DB注释(中文) |
| 136 | WANT_TEMP | NUMBER | Y |  | 要钢温度 | DB注释(中文) |
| 137 | CRY_PRESSURE | NUMBER | Y |  | 结晶器压力 | DB注释(中文) |
| 138 | BRANCH | NUMBER | Y |  | 支数 | DB注释(中文) |
| 139 | FIX_LEN | NUMBER | Y |  | 定尺 | DB注释(中文) |
| 140 | CAPTAIN_NM | VARCHAR2(50) | Y |  | 机长 | DB注释(中文) |
| 141 | SECTION_SPEC | VARCHAR2(50) | Y |  | 断面规格 | DB注释(中文) |
| 142 | MOULD_POWDER_MILL | VARCHAR2(50) | Y |  | 保护渣厂家 | DB注释(中文) |
| 143 | MOULD_POWDER_DT | VARCHAR2(8) | Y |  | 保护渣日期 | DB注释(中文) |
| 144 | SLAB_TYPE | VARCHAR2(50) | Y |  | 铸坯类型    板坯、方坯、矩形坯 | DB注释(中文) |
| 145 | CAST_TIME | NUMBER | Y |  | 浇铸时长 | DB注释(中文) |
| 146 | MOULD_POWDER_TYPE | VARCHAR2(50) | Y |  | 保护渣型号 | DB注释(中文) |
| 147 | OIL_STAT_WATER_PRES | NUMBER | Y |  | 主油站水压力 | DB注释(中文) |
| 148 | CAST_WTH | NUMBER | Y |  | 规格（宽） | DB注释(中文) |
| 149 | CAST_THK | NUMBER | Y |  | 规格（厚） | DB注释(中文) |
| 150 | HEAT_CNT_T | NUMBER | Y |  | 真实浇次炉数 | DB注释(中文) |
| 151 | HEAT_PRI_T | NUMBER | Y |  | 真实浇次内顺序 | DB注释(中文) |
| 152 | CC_HEAT_NO | VARCHAR2(12) | Y |  | 铸机炉次号 | DB注释(中文) |
| 153 | CAST_SIZE | VARCHAR2(30) | Y |  | 浇铸尺寸 | DB注释(中文) |
| 154 | STD_STLGRD | VARCHAR2(20) | Y |  | 钢种 | DB注释(中文) |
| 155 | HEAT_CNT_NO | VARCHAR2(20) | Y |  | 中包连浇炉次 | DB注释(中文) |
| 156 | PACK_NO_REAL | VARCHAR2(20) | Y |  | 实包数 | DB注释(中文) |
| 157 | PACK_NO_EMPTY | VARCHAR2(20) | Y |  | 空包数 | DB注释(中文) |
| 158 | CRYSTALLIZER_N0 | VARCHAR2(20) | Y |  | 结晶器编号 | DB注释(中文) |
| 159 | CRYSTALLIZER_PRES | VARCHAR2(20) | Y |  | 结晶器流速 | DB注释(中文) |
| 160 | ON_OFF | VARCHAR2(6) | Y |  | 自开否 | DB注释(中文) |
| 161 | CAST_LTH | VARCHAR2(20) | Y |  | 浇铸长度 | DB注释(中文) |
| 162 | CUT_LTH | VARCHAR2(20) | Y |  | 切割长度 | DB注释(中文) |
| 163 | CUT_NUM | VARCHAR2(20) | Y |  | 切割块数 | DB注释(中文) |
| 164 | PRD_CNT | VARCHAR2(20) | Y |  | 坯产量 | DB注释(中文) |
| 165 | CRY_NO | VARCHAR2(20) | Y |  | 结晶器号 | DB注释(中文) |
| 166 | CRY_WATER_PRE | VARCHAR2(20) | Y |  | 进水压力 | DB注释(中文) |
| 167 | CRY_WATER_TEMP | VARCHAR2(20) | Y |  | 进水温度 | DB注释(中文) |
| 168 | IN_FLOW | VARCHAR2(20) | Y |  | 内弧流量 | DB注释(中文) |
| 169 | OUT_FLOW | VARCHAR2(20) | Y |  | 外弧流量 | DB注释(中文) |
| 170 | LEFT_FLOW | VARCHAR2(20) | Y |  | 左窄流量 | DB注释(中文) |
| 171 | RIGHT_FLOW | VARCHAR2(20) | Y |  | 右窄流量 | DB注释(中文) |
| 172 | IN_WATER_TEMP | VARCHAR2(20) | Y |  | 内弧水温差 | DB注释(中文) |
| 173 | OUT_WATER_TEMP | VARCHAR2(20) | Y |  | 外弧水温差 | DB注释(中文) |
| 174 | LEFT_WATER_TEMP | VARCHAR2(20) | Y |  | 左窄水温差 | DB注释(中文) |
| 175 | RIGHT_WATER_TEMP | VARCHAR2(20) | Y |  | 右窄水温差 | DB注释(中文) |
| 176 | UP_SIZE | VARCHAR2(20) | Y |  | 上口尺寸 | DB注释(中文) |
| 177 | DOWN_SIZE | VARCHAR2(20) | Y |  | 下口尺寸 | DB注释(中文) |
| 178 | LEFT_TAPER | VARCHAR2(20) | Y |  | 左侧锥度 | DB注释(中文) |
| 179 | RIGHT_TAPER | VARCHAR2(20) | Y |  | 右侧锥度 | DB注释(中文) |
| 180 | CRY_USE_HEAT_CNT | VARCHAR2(20) | Y |  | 结晶器铜管使用炉数 | DB注释(中文) |
| 181 | COOL_PRE | VARCHAR2(20) | Y |  | 二冷水-总管压力 | DB注释(中文) |
| 182 | COOL_IN_TEMP | VARCHAR2(20) | Y |  | 二冷水-进水温度 | DB注释(中文) |
| 183 | COOL_NO | VARCHAR2(20) | Y |  | 二冷水-表号 | DB注释(中文) |
| 184 | STRAIGHT_TEMP | VARCHAR2(20) | Y |  | 矫直温度 | DB注释(中文) |
| 185 | COMPRESSION_AMOUNT | VARCHAR2(20) | Y |  | 压下量 | DB注释(中文) |

### SQM_MTC_PROD

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=42｜被读 28 过程 / 被写 7 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：3362　**主键**：MTC_NO、MTC_CHG_CNT、PROD_NO　**语义覆盖**：31/31

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | MTC_NO | VARCHAR2(11) | N | ✓ | 质量保证书编号 | DB注释(中文) |
| 9 | MTC_CHG_CNT | NUMBER | N | ✓ | 质量保证书变更回数 | DB注释(中文) |
| 10 | PROD_NO | VARCHAR2(18) | N | ✓ | 产品编号 | DB注释(中文) |
| 11 | ORD_NO | VARCHAR2(10) | Y |  | 订单编号 | DB注释(中文) |
| 12 | ORD_LN | VARCHAR2(3) | Y |  | 订单行号 | DB注释(中文) |
| 13 | SMP_NO | VARCHAR2(14) | Y |  | 试样编号 | DB注释(中文) |
| 14 | HEAT_NO | VARCHAR2(10) | Y |  | Heat编号 | DB注释(中文) |
| 15 | PROD_CONV_WGT | NUMBER | Y |  | 产品换算前重量 | DB注释(中文) |
| 16 | PROD_TOT_JDG_GRD | VARCHAR2(2) | Y |  | 产品综合判定等级 | DB注释(中文) |
| 17 | CHEM_JDG_GRD | VARCHAR2(1) | Y |  | 成分判定等级 | DB注释(中文) |
| 18 | MECH_JDG_GRD | VARCHAR2(1) | Y |  | 物性判定等级 | DB注释(中文) |
| 19 | APPR_JDG_GRD | VARCHAR2(1) | Y |  | 外观判定等级 | DB注释(中文) |
| 20 | ORD_PCS | NUMBER | Y |  | 订单张数 | DB注释(中文) |
| 21 | ORD_THK | NUMBER | Y |  | 订单厚度 | DB注释(中文) |
| 22 | ORD_WTH | NUMBER | Y |  | 订单宽度 | DB注释(中文) |
| 23 | ORD_LTH | NUMBER | Y |  | 订单长度 | DB注释(中文) |
| 24 | PROD_THK | NUMBER | Y |  | 产品厚度 | DB注释(中文) |
| 25 | PROD_WTH | NUMBER | Y |  | 产品宽度 | DB注释(中文) |
| 26 | PROD_LTH | NUMBER | Y |  | 产品长度 | DB注释(中文) |
| 27 | PROD_WGT | NUMBER | Y |  | 产品重量 | DB注释(中文) |
| 28 | PROD_CONV_LTH | NUMBER | Y |  | 产品换算前长度 | DB注释(中文) |
| 29 | LOT_NO | VARCHAR2(14) | Y |  | 批号 | DB注释(中文) |
| 30 | PROD_DTM | VARCHAR2(14) | Y |  | Product Datetime | DB注释(非中文) |
| 31 | UST_GRD | VARCHAR2(1) | Y |  | 探伤实际等级 | DB注释(中文) |

### SQM_ORD_CHEM

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=41｜被读 35 过程 / 被写 3 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：175942　**主键**：ORD_NO、ORD_LN、SMS_PROD_CHEM_TY、QLT_DSN_STD_TY、QLT_CHEM_CD　**语义覆盖**：22/22

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 修改人 | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | 修改时间 | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | ORD_NO | VARCHAR2(10) | N | ✓ | 订单编号 | DB注释(中文) |
| 9 | ORD_LN | VARCHAR2(3) | N | ✓ | 订单行号 | DB注释(中文) |
| 10 | SMS_PROD_CHEM_TY | VARCHAR2(1) | N | ✓ | 炼钢产品成分分类（G-保证炼钢成分,P-产品成分） | DB注释(中文) |
| 11 | QLT_DSN_STD_TY | VARCHAR2(1) | N | ✓ | 质量设计标准区分 | DB注释(中文) |
| 12 | QLT_CHEM_CD | VARCHAR2(5) | N | ✓ | 质量成分代码 | DB注释(中文) |
| 13 | QLT_CHEM_DISP_FORM | VARCHAR2(10) | Y |  | 质量成分标识 | DB注释(中文) |
| 14 | QLT_CHEM_FOMULA | VARCHAR2(2) | Y |  | 质量成分公式 | DB注释(中文) |
| 15 | QLT_CHEM_MIN_TMP | NUMBER | Y |  | 质量成分下限值 | DB注释(中文) |
| 16 | QLT_CHEM_MAX_TMP | NUMBER | Y |  | 质量成分上限值 | DB注释(中文) |
| 17 | QLT_CHEM_AIM_TMP | NUMBER | Y |  | 质量成分目标值 | DB注释(中文) |
| 18 | QLT_CHEM_GRT_CD | VARCHAR2(1) | Y |  | 质量成分保证代号 | DB注释(中文) |
| 19 | QLT_CHEM_MIN | VARCHAR2(20) | Y |  | 质量成分下限值 | DB注释(中文) |
| 20 | QLT_CHEM_MAX | VARCHAR2(20) | Y |  | 质量成分上限值 | DB注释(中文) |
| 21 | QLT_CHEM_AIM | VARCHAR2(20) | Y |  | 质量成分目标值 | DB注释(中文) |
| 22 | MTC_YN | VARCHAR2(1) | Y |  | 是否出具质保书 | DB注释(中文) |

### SIM_RM_IO_WORK_RSLT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=40｜被读 20 过程 / 被写 10 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：2680　**主键**：TRACT_ID　**语义覆盖**：61/61

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | ??UserID_??UserID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | ??ObjectID_??ObjectID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | ????_???? | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | ??UserID_??UserID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | ??ObjectID_??ObjectID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | ????_???? | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Archive??_Archive?? | DB注释(非中文) |
| 8 | TRACT_ID | VARCHAR2(30) | N | ✓ | TransactionID_TransactionID | DB注释(非中文) |
| 9 | DLV_PLAN_ID | VARCHAR2(20) | Y |  | ????ID_????ID | DB注释(非中文) |
| 10 | ANAL_LOT_ID | VARCHAR2(4) | Y |  | ??LOT??_??LOT?? | DB注释(非中文) |
| 11 | PO_NO | VARCHAR2(20) | Y |  | ??????_?????? | DB注释(非中文) |
| 12 | PO_LINE_NO | VARCHAR2(5) | Y |  | ??????_??????? | DB注释(非中文) |
| 13 | PO_DLV_NO | VARCHAR2(5) | Y |  | ????LineNo_????LineNo | DB注释(非中文) |
| 14 | MOVE_TRANS_NO | VARCHAR2(15) | Y |  | ??Trans?_?????? | DB注释(非中文) |
| 15 | TRS_VEHC_DTM | VARCHAR2(14) | Y |  | ????_???? | DB注释(非中文) |
| 16 | TRS_VEHICLE_NO | VARCHAR2(20) | Y |  | ?????_?????? | DB注释(非中文) |
| 17 | ITEM_CD | VARCHAR2(20) | Y |  | Item??_??Item?? | DB注释(非中文) |
| 18 | SUPPLIER_ITEM_CD | VARCHAR2(15) | Y |  | ???Item??_???Item?? | DB注释(非中文) |
| 19 | RM_ISS_PKG_CNT | NUMBER | Y |  | ???????_???????? | DB注释(非中文) |
| 20 | LANSHAN_NET_WGT | NUMBER | Y |  | ??????_???????? | DB注释(非中文) |
| 21 | VEHC_GRS_WGT | NUMBER | Y |  | ???????_??????? | DB注释(非中文) |
| 22 | VEHC_NET_WGT | NUMBER | Y |  | ????????_??????? | DB注释(非中文) |
| 23 | VEHC_PAK_WGT | NUMBER | Y |  | ??????_???????? | DB注释(非中文) |
| 24 | RM_MOIST_RATIO | NUMBER | Y |  | ?????_????? | DB注释(非中文) |
| 25 | RM_REDUCT_QTY | NUMBER | Y |  | ?????_????? | DB注释(非中文) |
| 26 | RM_NET_QTY | NUMBER | Y |  | ????Net??_????Net?? | DB注释(非中文) |
| 27 | SUPPLY_NO | VARCHAR2(10) | Y |  | ???ID_????? | DB注释(非中文) |
| 28 | RM_PAK_TY | VARCHAR2(1) | Y |  | ??????_?????? | DB注释(非中文) |
| 29 | RM_WGT_TY | VARCHAR2(1) | Y |  | ??????_?????? | DB注释(非中文) |
| 30 | RM_WH_TY | VARCHAR2(5) | Y |  | ??????_?????? | DB注释(非中文) |
| 31 | TRK_PROG_STS | VARCHAR2(1) | Y |  | ??????_?????? | DB注释(非中文) |
| 32 | CC_CD | VARCHAR2(5) | Y |  | CostCenter_CostCenter | DB注释(非中文) |
| 33 | DEPT_CD | VARCHAR2(10) | Y |  | ???????_?????? | DB注释(非中文) |
| 34 | DEST_CD | VARCHAR2(10) | Y |  | ?????_?????? | DB注释(非中文) |
| 35 | DELV_FL | VARCHAR2(1) | Y |  | ????????_???????? | DB注释(非中文) |
| 36 | RM_ISS_DELV_TY | VARCHAR2(1) | Y |  | ???????_??????? | DB注释(非中文) |
| 37 | RM_ISS_DELV_TP_TY | VARCHAR2(1) | Y |  | ?????????_????????? | DB注释(非中文) |
| 38 | RM_INV_ADJ_DESC_TY | VARCHAR2(1) | Y |  | ??????????_?????????? | DB注释(非中文) |
| 39 | RM_RTN_FL | VARCHAR2(1) | Y |  | ??????_?????? | DB注释(非中文) |
| 40 | RM_STK_DT | VARCHAR2(8) | Y |  | ??????_?????? | DB注释(非中文) |
| 41 | ERP_SEND_DTM | VARCHAR2(14) | Y |  | ERP????_ERP???? | DB注释(非中文) |
| 42 | IC_ISS_DTM | VARCHAR2(14) | Y |  | ?IC???_IC???? | DB注释(非中文) |
| 43 | PHONE_NO | VARCHAR2(20) | Y |  | ???_???? | DB注释(非中文) |
| 44 | INFO_REG_DTM | VARCHAR2(14) | Y |  | ??????_?????? | DB注释(非中文) |
| 45 | REMARKS | VARCHAR2(100) | Y |  | ??_?? | DB注释(非中文) |
| 46 | LOT_VEHICLE_NO | VARCHAR2(20) | Y |  | ?????lot | DB注释(非中文) |
| 47 | LOT_TRANS_NO | VARCHAR2(15) | Y |  | ?????lot | DB注释(非中文) |
| 48 | FROMWEIGHT | NUMBER | Y |  | ???? | DB注释(非中文) |
| 49 | DELETE_FL | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 50 | DMS_VEHICLE_NO | VARCHAR2(20) | Y |  | ?????DMS | DB注释(非中文) |
| 51 | DMS_TRANS_NO | VARCHAR2(15) | Y |  | ?????DMS | DB注释(非中文) |
| 52 | B1 | VARCHAR2(20) | Y |  | ??1 | DB注释(非中文) |
| 53 | B2 | VARCHAR2(20) | Y |  | ??2 | DB注释(非中文) |
| 54 | B3 | VARCHAR2(20) | Y |  | ??3 | DB注释(非中文) |
| 55 | B4 | VARCHAR2(20) | Y |  | ??4 | DB注释(非中文) |
| 56 | B5 | VARCHAR2(100) | Y |  | ??5 | DB注释(非中文) |
| 57 | LOT_NO | VARCHAR2(28) | Y |  | ??? | DB注释(非中文) |
| 58 | UPDATE_FL | VARCHAR2(10) | Y |  | ???????? | DB注释(非中文) |
| 59 | UOM | VARCHAR2(3) | Y |  | ?? | DB注释(非中文) |
| 60 | CAR_ASSIGN_NO | VARCHAR2(30) | Y |  | ???? | DB注释(非中文) |
| 61 | LOT_YN | VARCHAR2(3) | Y |  | ?????? | DB注释(非中文) |

### SQM_MTC_COM

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=40｜被读 26 过程 / 被写 7 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：334　**主键**：MTC_NO、MTC_CHG_CNT　**语义覆盖**：78/78

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | MTC_NO | VARCHAR2(11) | N | ✓ | 质量保证书编号 | DB注释(中文) |
| 9 | MTC_CHG_CNT | NUMBER | N | ✓ | 质量保证书变更回数 | DB注释(中文) |
| 10 | ORD_NO | VARCHAR2(10) | Y |  | 订单编号 | DB注释(中文) |
| 11 | ORD_LN | VARCHAR2(3) | Y |  | 订单行号 | DB注释(中文) |
| 12 | MTC_STS_CD | VARCHAR2(1) | Y |  | 质量保证书状态代码(1-申请，2-编制，9-取消) | DB注释(中文) |
| 13 | MTC_ISS_CNT | NUMBER | Y |  | 质量保证书发行回数 | DB注释(中文) |
| 14 | MTC_ISS_DT | VARCHAR2(8) | Y |  | 质量保证书发行日期 | DB注释(中文) |
| 15 | MTC_UPD_DT | VARCHAR2(8) | Y |  | 质量保证书修改日期 | DB注释(中文) |
| 16 | PROD_GRP | VARCHAR2(2) | Y |  | 品种代码 | DB注释(中文) |
| 17 | PROD_CD | VARCHAR2(3) | Y |  | 品名代码 | DB注释(中文) |
| 18 | MTC_REQ_CD | VARCHAR2(1) | Y |  | 质量保证书申请代码 | DB注释(中文) |
| 19 | MTC_REQ_NO | VARCHAR2(10) | Y |  | 质量保证书申请编号 | DB注释(中文) |
| 20 | MTC_REQ_DT | VARCHAR2(8) | Y |  | 质量保证书申请日期 | DB注释(中文) |
| 21 | MTC_ORG_DT | VARCHAR2(8) | Y |  | 质量保证书编制日期 | DB注释(中文) |
| 22 | MTC_CNL_CAU_CD | VARCHAR2(1) | Y |  | 质量保证书取消事由代码 | DB注释(中文) |
| 23 | MTC_CNL_DT | VARCHAR2(8) | Y |  | 质量保证书取消日期 | DB注释(中文) |
| 24 | MTC_CNL_PRS_ID | VARCHAR2(20) | Y |  | 质量保证书取消人ID | DB注释(中文) |
| 25 | CUST_PO_NO | VARCHAR2(30) | Y |  | 客户PO编号 | DB注释(中文) |
| 26 | CUST_PO_LN | VARCHAR2(5) | Y |  | 客户Item代码 | DB注释(中文) |
| 27 | CUST_ITEM_CD | VARCHAR2(30) | Y |  | 客户司Item代码 | DB注释(中文) |
| 28 | ATND_TEST_YN | VARCHAR2(1) | Y |  | 入会检查与否 | DB注释(中文) |
| 29 | SALE_PTH_TY | VARCHAR2(1) | Y |  | 销售路径分类 | DB注释(中文) |
| 30 | MTC_CFM_TY | VARCHAR2(1) | Y |  | 质量保证书确定分类 | DB注释(中文) |
| 31 | MTC_CFM_DTM | VARCHAR2(14) | Y |  | 质量保证书确定时间 | DB注释(中文) |
| 32 | ORD_TY | VARCHAR2(2) | Y |  | 订单类型 | DB注释(中文) |
| 33 | INSP_AGENCY_CD | VARCHAR2(3) | Y |  | 检查机构代码 | DB注释(中文) |
| 34 | INSP_AGENCY_NM | VARCHAR2(50) | Y |  | 检查机构名 | DB注释(中文) |
| 35 | SPEC_ORG_CD | VARCHAR2(10) | Y |  | 规格机构代码 | DB注释(中文) |
| 36 | NATL_SPEC_YEAR | VARCHAR2(4) | Y |  | 国家标准年度 | DB注释(中文) |
| 37 | MTC_SPEC_NM | VARCHAR2(50) | Y |  | 质量保证书规格名 | DB注释(中文) |
| 38 | PROD_DIMS_CD | VARCHAR2(7) | Y |  | 产品尺寸代码 | DB注释(中文) |
| 39 | PROD_DIMS_NM | VARCHAR2(30) | Y |  | 产品尺寸名 | DB注释(中文) |
| 40 | ORD_LTH | NUMBER | Y |  | 订单长度 | DB注释(中文) |
| 41 | ORD_CONV_LTH | NUMBER | Y |  | 订单换算前长度 | DB注释(中文) |
| 42 | ORD_PROD_WGT | NUMBER | Y |  | 订单产品重量 | DB注释(中文) |
| 43 | ORD_CONV_PROD_WGT | NUMBER | Y |  | 订单换算前产品重量 | DB注释(中文) |
| 44 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  | 炼钢内控钢种编号(出钢目标) | DB注释(中文) |
| 45 | SPEC_CD | VARCHAR2(50) | Y |  | 国家标准牌号 | DB注释(中文) |
| 46 | TSL_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验保证代码 | DB注释(中文) |
| 47 | TSL_UNIT_CD | VARCHAR2(1) | Y |  | 拉伸试验单位代码 | DB注释(中文) |
| 48 | BEND_GRT_CD | VARCHAR2(1) | Y |  | 弯曲试验保证代码 | DB注释(中文) |
| 49 | BEND_ANGLE_CD | VARCHAR2(1) | Y |  | 弯曲试验角度代码 | DB注释(中文) |
| 50 | IMPACT_GRT_CD | VARCHAR2(1) | Y |  | 冲击试验保证代码 | DB注释(中文) |
| 51 | IMPACT_TEMP_UNIT_CD | VARCHAR2(1) | Y |  | 冲击试验温度单位代码 | DB注释(中文) |
| 52 | IMPACT_TEMP | NUMBER | Y |  | 冲击试验温度 | DB注释(中文) |
| 53 | IMPACT_UNIT_CD | VARCHAR2(1) | Y |  | 冲击试验单位代码 | DB注释(中文) |
| 54 | HARD_GRT_CD | VARCHAR2(1) | Y |  | 硬度试验保证代码 | DB注释(中文) |
| 55 | HARD_UNIT_CD | VARCHAR2(1) | Y |  | 硬度试验单位代码 | DB注释(中文) |
| 56 | MGRPHY_GRT_CD | VARCHAR2(1) | Y |  | 金相试验粒度试验保证代码 | DB注释(中文) |
| 57 | MACRO_GRT_CD | VARCHAR2(1) | Y |  | Macro试验保证代码 | DB注释(中文) |
| 58 | MTC_CNTR_NM | VARCHAR2(50) | Y |  | 质量保证书合约人名 | DB注释(中文) |
| 59 | CNTR_CD | VARCHAR2(30) | Y |  | 合约代码 | DB注释(中文) |
| 60 | MTC_CUST_NM | VARCHAR2(100) | Y |  | 质量保证书客户司名 | DB注释(中文) |
| 61 | CUST_CD | VARCHAR2(20) | Y |  | 客户司代码 | DB注释(中文) |
| 62 | CUST_QCERT_NO | VARCHAR2(15) | Y |  | 客户保证编号 | DB注释(中文) |
| 63 | MTC_TY | VARCHAR2(2) | Y |  | 质量保证书分类 | DB注释(中文) |
| 64 | MTC_REF_DESC1 | VARCHAR2(300) | Y |  | 质量保证书Remark_1 | DB注释(中文) |
| 65 | MTC_REF_DESC2 | VARCHAR2(300) | Y |  | 质量保证书Remark_2 | DB注释(中文) |
| 66 | MTC_REF_DESC3 | VARCHAR2(300) | Y |  | 质量保证书Remark_3 | DB注释(中文) |
| 67 | MTC_REF_DESC4 | VARCHAR2(300) | Y |  | 质量保证书Remark_4 | DB注释(中文) |
| 68 | MTC_REF_DESC5 | VARCHAR2(300) | Y |  | 质量保证书Remark_5 | DB注释(中文) |
| 69 | MTC_REF_DESC6 | VARCHAR2(300) | Y |  | 质量保证书Remark_6 | DB注释(中文) |
| 70 | INSP_MTC_NO1 | VARCHAR2(50) | Y |  | 认证证书编号 | DB注释(中文) |
| 71 | INSP_MTC_NO2 | VARCHAR2(50) | Y |  | 检验证书编号 | DB注释(中文) |
| 72 | ORD_USAGE | VARCHAR2(4) | Y |  | 订单用途代码 | DB注释(中文) |
| 73 | DEST_CD | VARCHAR2(9) | Y |  | 目的地代码 | DB注释(中文) |
| 74 | ORD_DELV_DT | VARCHAR2(8) | Y |  | 订单交货期日 | DB注释(中文) |
| 75 | SURF_TREAT_CD | VARCHAR2(3) | Y |  | 表面处理代码 | DB注释(中文) |
| 76 | SURF_GRD | VARCHAR2(2) | Y |  | 表面等级 | DB注释(中文) |
| 77 | MARK_PROD_NM | VARCHAR2(60) | Y |  | 标记品名 | DB注释(中文) |
| 78 | GK_TREAT_NM | VARCHAR2(100) | Y |  | 热镀锌后处理名称 | DB注释(中文) |

### SIM_RM_PUR_RELEASE

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=39｜被读 37 过程 / 被写 1 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：240　**主键**：PO_NO、PO_LINE_NO、PO_DLV_NO　**语义覆盖**：37/37

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | ??UserID_??UserID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | ??ObjectID_??ObjectID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | ????_???? | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | ??UserID_??UserID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | ??ObjectID_??ObjectID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | ????_???? | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Archive??_Archive?? | DB注释(非中文) |
| 8 | PO_NO | VARCHAR2(20) | N | ✓ | ??????_?????? | DB注释(非中文) |
| 9 | PO_LINE_NO | VARCHAR2(5) | N | ✓ | ??????_??????? | DB注释(非中文) |
| 10 | PO_DLV_NO | VARCHAR2(5) | N | ✓ | ????LineNo_????LineNo | DB注释(非中文) |
| 11 | CURRENCY_CD | VARCHAR2(3) | Y |  | ????_???? | DB注释(非中文) |
| 12 | ORD_PRICE | NUMBER | Y |  | ????_???? | DB注释(非中文) |
| 13 | RM_ORD_QTY | NUMBER | Y |  | ?????_????? | DB注释(非中文) |
| 14 | NEED_BY_DT | VARCHAR2(8) | Y |  | ??????_?????? | DB注释(非中文) |
| 15 | ITEM_CD | VARCHAR2(20) | Y |  | Item??_??Item?? | DB注释(非中文) |
| 16 | SUPPLIER_ITEM_CD | VARCHAR2(15) | Y |  | ???Item??_???Item?? | DB注释(非中文) |
| 17 | ORD_AMT | NUMBER | Y |  | ??????????_?????????? | DB注释(非中文) |
| 18 | SUPPLY_NO | VARCHAR2(10) | Y |  | ?????_???No | DB注释(非中文) |
| 19 | SUPPLY_NM | VARCHAR2(200) | Y |  | ?????_???? | DB注释(非中文) |
| 20 | UOM | VARCHAR2(10) | Y |  | ??_?? | DB注释(非中文) |
| 21 | DEST_CD | VARCHAR2(10) | Y |  | ?????_????? | DB注释(非中文) |
| 22 | DEST_NM | VARCHAR2(40) | Y |  | ????_???? | DB注释(非中文) |
| 23 | ACC_REJ_ANAL | VARCHAR2(1) | Y |  | ????????_???? | DB注释(非中文) |
| 24 | WEIGHT_USE_YN | VARCHAR2(1) | Y |  | ????_???? | DB注释(非中文) |
| 25 | DRY_CAL_YN | VARCHAR2(1) | Y |  | ??????_?????? | DB注释(非中文) |
| 26 | PREPARE_NAME | VARCHAR2(20) | Y |  | ??? | DB注释(非中文) |
| 27 | ORGANIZATION_NAME | VARCHAR2(100) | Y |  | ???? | DB注释(非中文) |
| 28 | CLOSED_CODE | VARCHAR2(30) | Y |  | ???? | DB注释(非中文) |
| 29 | SEND_DTM | VARCHAR2(14) | Y |  | ????TC0008 | DB注释(非中文) |
| 30 | PO_DISTRIBUTION_ID | VARCHAR2(10) | Y |  | ???ID | DB注释(非中文) |
| 31 | CLOSED_DTM | VARCHAR2(14) | Y |  | ???????? | DB注释(非中文) |
| 32 | BOO_FLAG | VARCHAR2(3) | Y |  | boo/bot???? | DB注释(非中文) |
| 33 | B1 | VARCHAR2(100) | Y |  | ??1 | DB注释(非中文) |
| 34 | B2 | VARCHAR2(100) | Y |  | ??2 | DB注释(非中文) |
| 35 | B3 | VARCHAR2(100) | Y |  | ??3 | DB注释(非中文) |
| 36 | B4 | VARCHAR2(100) | Y |  | ??4 | DB注释(非中文) |
| 37 | B5 | VARCHAR2(100) | Y |  | ??5 | DB注释(非中文) |

### SHR_DEFECT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=37｜被读 25 过程 / 被写 6 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：10　**主键**：PROC_CD、COIL_NO、DEF_CD　**语义覆盖**：21/21

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | PROC_CD | VARCHAR2(3) | N | ✓ | Process Code | DB注释(非中文) |
| 9 | COIL_NO | VARCHAR2(14) | N | ✓ | Coil Number | DB注释(非中文) |
| 10 | DEF_CD | VARCHAR2(4) | N | ✓ | Defect Code | DB注释(非中文) |
| 11 | DEF_GRD | VARCHAR2(1) | Y |  | Defect Grade | DB注释(非中文) |
| 12 | DEF_SURF_CD | VARCHAR2(1) | Y |  | Defect Surface Code | DB注释(非中文) |
| 13 | DEF_LTH_DIR | NUMBER | Y |  | Defect length Direction | DB注释(非中文) |
| 14 | DEF_WTH_DIR | NUMBER | Y |  | Defect width Direction | DB注释(非中文) |
| 15 | DEF_LTH | NUMBER | Y |  | Defect length | DB注释(非中文) |
| 16 | DEF_CMT | VARCHAR2(330) | Y |  | Defect Comments | DB注释(非中文) |
| 17 | DEF_CMT_CD | VARCHAR2(2) | Y |  | Defect Comments Code | DB注释(非中文) |
| 18 | DEF_WK_DTM | VARCHAR2(14) | Y |  | Defect Work Date | DB注释(非中文) |
| 19 | DEF_WK_EMP_ID | VARCHAR2(20) | Y |  | Defect Worker Employee ID | DB注释(非中文) |
| 20 | REP_YN | VARCHAR2(1) | Y |  | ?????? | DB注释(非中文) |
| 21 | APP_DEF_PROC | VARCHAR2(10) | Y |  | Surface Defect Process | SCO_DATA_DIC(D) |

### SCR_LN_RSLT_CMM

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=37｜被读 31 过程 / 被写 3 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：13　**主键**：PROC_CD、COIL_NO、RPROC_CNT　**语义覆盖**：87/89

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | PROC_CD | VARCHAR2(3) | N | ✓ | Process Code | DB注释(非中文) |
| 9 | COIL_NO | VARCHAR2(14) | N | ✓ | Coil Number | DB注释(非中文) |
| 10 | RPROC_CNT | NUMBER | N | ✓ | The Number of Work at the same line | DB注释(非中文) |
| 11 | RCD_STS_ID | VARCHAR2(1) | Y |  | Record Status Flag | DB注释(非中文) |
| 12 | PCOIL_NO | VARCHAR2(14) | Y |  | The Number of Coil No at the Entry side | DB注释(非中文) |
| 13 | ROLL_UNIT | VARCHAR2(10) | Y |  | Roll Unit | DB注释(非中文) |
| 14 | WK_STA_DTM | VARCHAR2(14) | Y |  | Date of Work Start | DB注释(非中文) |
| 15 | WK_END_DTM | VARCHAR2(14) | Y |  | Date of Work End | DB注释(非中文) |
| 16 | COIL_WK_TM | NUMBER | Y |  | Duration Time | DB注释(非中文) |
| 17 | SUMUP_DT | VARCHAR2(8) | Y |  | The Work Date | DB注释(非中文) |
| 18 | WK_SHF_GRP | VARCHAR2(2) | Y |  | The Shift and Crew | DB注释(非中文) |
| 19 | WORK_TP | VARCHAR2(1) | Y |  | The Flag of PDI | DB注释(非中文) |
| 20 | ORD_FL | VARCHAR2(1) | Y |  | The Flag of OK or NOK | DB注释(非中文) |
| 21 | HCOIL_NO1 | VARCHAR2(10) | Y |  | HCOIL No_1 | DB注释(非中文) |
| 22 | HCOIL_LTH1 | NUMBER | Y |  | HCOIL Length_1 | DB注释(非中文) |
| 23 | HCOIL_WGT1 | NUMBER | Y |  | HCOIL Weight_1 | DB注释(非中文) |
| 24 | HCOIL_NO2 | VARCHAR2(10) | Y |  | HCOIL No_2 | DB注释(非中文) |
| 25 | HCOIL_LTH2 | NUMBER | Y |  | HCOIL Length_2 | DB注释(非中文) |
| 26 | HCOIL_WGT2 | NUMBER | Y |  | HCOIL Weight_2 | DB注释(非中文) |
| 27 | HCOIL_NO3 | VARCHAR2(10) | Y |  | HCOIL No_3 | DB注释(非中文) |
| 28 | HCOIL_LTH3 | NUMBER | Y |  | HCOIL Length_3 | DB注释(非中文) |
| 29 | HCOIL_WGT3 | NUMBER | Y |  | HCOIL Weight_3 | DB注释(非中文) |
| 30 | ORD_NO | VARCHAR2(10) | Y |  | Order Head No | DB注释(非中文) |
| 31 | ORD_LN | NUMBER | Y |  | Order Line No | DB注释(非中文) |
| 32 | COIL_THK | NUMBER | Y |  | Coil Thickness | DB注释(非中文) |
| 33 | COIL_WTH | NUMBER | Y |  | Coil Width | DB注释(非中文) |
| 34 | COIL_LTH | NUMBER | Y |  | Coil Length | DB注释(非中文) |
| 35 | COIL_IN_DIA | NUMBER | Y |  | Coil InDia | DB注释(非中文) |
| 36 | COIL_OUT_DIA | NUMBER | Y |  | Coil OutDia | DB注释(非中文) |
| 37 | COIL_NET_WGT | NUMBER | Y |  | Coil Actual Weight | DB注释(非中文) |
| 38 | COIL_THY_WGT | NUMBER | Y |  | Coil Calculated Weight | DB注释(非中文) |
| 39 | COIL_GRS_NET_WGT | NUMBER | Y |  | Coil Actual Weight+Packing Weight | DB注释(非中文) |
| 40 | COIL_GRS_THY_WGT | NUMBER | Y |  | Coil Calculated Weight+Packing Weight | DB注释(非中文) |
| 41 | COIL_AW | NUMBER | Y |  | The Exit division weight | DB注释(非中文) |
| 42 | ENT_PTL_YN | VARCHAR2(1) | Y |  | The Flag of Coil Division at the Entry side. | DB注释(非中文) |
| 43 | ACT_EDG_TP | VARCHAR2(1) | Y |  | The Actual Edge from L.2 or MES Input | DB注释(非中文) |
| 44 | TST_ORD_YN | VARCHAR2(1) | Y |  | ??????? | DB注释(非中文) |
| 45 | BEF_PROC_CD | VARCHAR2(3) | Y |  | The just before process code | DB注释(非中文) |
| 46 | CMP_QCERT_NO | VARCHAR2(8) | Y |  | The Abbreviated Code of Material Design | DB注释(非中文) |
| 47 | SUR_TP | VARCHAR2(2) | Y |  | The Surface Spangle Code | DB注释(非中文) |
| 48 | COIL_PTR_CD | VARCHAR2(2) | Y |  | Post Treatment Code | DB注释(非中文) |
| 49 | COIL_WK_GW_CD | VARCHAR2(1) | Y |  | Code of Galvanized Quantity on the STAip | DB注释(非中文) |
| 50 | GAL_ONE_MODE | VARCHAR2(2) | Y |  | ????MODE | DB注释(非中文) |
| 51 | OIL_MODE | VARCHAR2(1) | Y |  | Oiling Mode | DB注释(非中文) |
| 52 | OIL_TYPE | VARCHAR2(3) | Y |  | Oiling Code | DB注释(非中文) |
| 53 | OIL_WGT_TOP | NUMBER | Y |  | Top Oil Quanity() | DB注释(非中文) |
| 54 | OIL_WGT_BOT | NUMBER | Y |  | Bot Oil Quanity | DB注释(非中文) |
| 55 | SPM_USE_YN | VARCHAR2(1) | Y |  | Used or Not SPM | DB注释(非中文) |
| 56 | LN_SPD | VARCHAR2(3) | Y |  | line_Speed | DB注释(非中文) |
| 57 | SIDE_TRIMMER_MD | VARCHAR2(1) | Y |  | SideTrimmer_mode | DB注释(非中文) |
| 58 | TRIM_WTH_QTY | VARCHAR2(4) | Y |  | Trimming Width Quantity | DB注释(非中文) |
| 59 | PL_WLD_CNT | NUMBER | Y |  | A Number of welding points of PLTCM | DB注释(非中文) |
| 60 | COIL_WIND_MD | VARCHAR2(1) | Y |  | Recoiling Direction of PLTCM | DB注释(非中文) |
| 61 | INSR_EMP_ID | NUMBER | Y |  | Employer Number of inspector | DB注释(非中文) |
| 62 | SIZE_GRD | VARCHAR2(1) | Y |  | Sizing Grade (add to SCR_COIL_MASTER?) | DB注释(非中文) |
| 63 | UNT_WGT_GRD | VARCHAR2(1) | Y |  | Weighing Grade  (add to SCR_COIL_MASTER?) | DB注释(非中文) |
| 64 | SUR_GRD | VARCHAR2(1) | Y |  | Surface Grade  (add to SCR_COIL_MASTER?) | DB注释(非中文) |
| 65 | SHP_GRD | VARCHAR2(1) | Y |  | Shape Grade  (add to SCR_COIL_MASTER?) | DB注释(非中文) |
| 66 | APR_SYN_GRD | VARCHAR2(2) | Y |  | Surface Decision Grade  (add to SCR_COIL_MASTER?) | DB注释(非中文) |
| 67 | OP_JDG_GRD | VARCHAR2(2) | Y |  | Operator Input Grade  (add to SCR_COIL_MASTER?) | DB注释(非中文) |
| 68 | COIL_APR_GRD_TP | VARCHAR2(2) | Y |  | The Reason Code for Grade Down  (add to SCR_COIL_MASTER?) | DB注释(非中文) |
| 69 | NXT_PROC_CD | VARCHAR2(20) | Y |  | Next Process based on Planning | DB注释(非中文) |
| 70 | DMD_NXT_PROC | VARCHAR2(3) | Y |  | Next process  requested by The Operator | DB注释(非中文) |
| 71 | DMD_NXT_PROC_REA_TP | VARCHAR2(2) | Y |  | ????????? | DB注释(非中文) |
| 72 | HOLD_OCC_YN | VARCHAR2(1) | Y |  | ?????? | DB注释(非中文) |
| 73 | QUALITY_FLAG | VARCHAR2(1) | Y |  | quality flag : Is surface quality qualified flag? 0, qualified;1,Unqualified | DB注释(非中文) |
| 74 | STD_STLGRD | VARCHAR2(20) | Y |  | Steel grade name | DB注释(非中文) |
| 75 | FINAL_CUT_FL | VARCHAR2(1) | Y |  |  | 空 |
| 76 | COIL_WGT_L2 | NUMBER | Y |  | L2 上传的钢卷重量 | SCO_DATA_DIC(D) |
| 77 | NATL_SPEC_NO | VARCHAR2(40) | Y |  | National standard desc | DB注释(非中文) |
| 78 | NATL_SPEC_YEAR | VARCHAR2(4) | Y |  | National standard year | DB注释(非中文) |
| 79 | WEIGHT_DTM | VARCHAR2(14) | Y |  | metering system weight datetime | DB注释(非中文) |
| 80 | USER_ID | VARCHAR2(20) | Y |  | User ID | SCO_DATA_DIC(D) |
| 81 | CREATE_DTIME | VARCHAR2(14) | Y |  |  | 空 |
| 82 | DUMMY_COIL_YN | VARCHAR2(1) | Y |  | IndDummyCoil | DB注释(非中文) |
| 83 | COIL_WTH_L2 | NUMBER | Y |  | Coil width  L2 | DB注释(非中文) |
| 84 | COIL_THK_L2 | NUMBER | Y |  | Coil thick  L2 | DB注释(非中文) |
| 85 | SLEEVE_YN | VARCHAR2(1) | Y |  | IndSleeveUsage | DB注释(非中文) |
| 86 | UP_USER_ID | VARCHAR2(20) | Y |  | update coil data user id | DB注释(非中文) |
| 87 | UP_DTIME | VARCHAR2(14) | Y |  | update coil data datetime | DB注释(非中文) |
| 88 | UP_SHF_GRP | VARCHAR2(2) | Y |  | update coil data shift and group | DB注释(非中文) |
| 89 | OIL_FLAG | VARCHAR2(1) | Y |  | Oiling Flag | DB注释(非中文) |

### SQM_TOT_JDG_RSLT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=37｜被读 35 过程 / 被写 1 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：90888　**主键**：PROD_NO　**语义覆盖**：43/43

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | PROD_NO | VARCHAR2(18) | N | ✓ | 产品编号 | DB注释(中文) |
| 9 | SMP_NO | VARCHAR2(14) | Y |  | 试样编号 | DB注释(中文) |
| 10 | MTRL_PROG_CD | VARCHAR2(4) | Y |  | 材料进度代码 | DB注释(中文) |
| 11 | PROD_CD | VARCHAR2(3) | Y |  | 品名代码 | DB注释(中文) |
| 12 | ORD_FL | VARCHAR2(1) | Y |  | 订单分类 | DB注释(中文) |
| 13 | HEAT_NO | VARCHAR2(10) | Y |  | Heat编号 | DB注释(中文) |
| 14 | ORD_NO | VARCHAR2(10) | Y |  | 订单编号 | DB注释(中文) |
| 15 | ORD_LN | VARCHAR2(3) | Y |  | 订单行号 | DB注释(中文) |
| 16 | CMP_QCERT_NO | VARCHAR2(11) | Y |  | 公司保证编号(材质记号) | DB注释(中文) |
| 17 | SPEC_CD | VARCHAR2(50) | Y |  | 国家标准牌号 | DB注释(中文) |
| 18 | ORD_THK | NUMBER | Y |  | 订单厚度 | DB注释(中文) |
| 19 | INSP_AGENCY_CD | VARCHAR2(3) | Y |  | 检查机构代码 | DB注释(中文) |
| 20 | CHEM_JDG_GRD | VARCHAR2(1) | Y |  | 成分判定等级 | DB注释(中文) |
| 21 | MECH_JDG_GRD | VARCHAR2(1) | Y |  | 物性判定等级 | DB注释(中文) |
| 22 | APPR_JDG_GRD | VARCHAR2(1) | Y |  | 外观判定等级 | DB注释(中文) |
| 23 | PROD_TOT_JDG_GRD | VARCHAR2(2) | Y |  | 产品综合判定等级 | DB注释(中文) |
| 24 | PROD_TOT_JDG_RSLT_TY | VARCHAR2(1) | Y |  | 产品综合判定结果分类 | DB注释(中文) |
| 25 | SPL_CAU_CD | VARCHAR2(2) | Y |  | 余材原因代码 | DB注释(中文) |
| 26 | PROD_WH_RCPT_DTM | VARCHAR2(14) | Y |  | 产品仓库入库时间 | DB注释(中文) |
| 27 | PROD_DUE_DT | VARCHAR2(8) | Y |  | 生产期限日 | DB注释(中文) |
| 28 | PROD_WGT | NUMBER | Y |  | 产品重量 | DB注释(中文) |
| 29 | YARD_BLKH_TY | VARCHAR2(1) | Y |  | 仓库Bay分类 | DB注释(中文) |
| 30 | PROD_TOT_JDG_DTM | VARCHAR2(14) | Y |  | 产品综合判定时间 | DB注释(中文) |
| 31 | LOT_NO | VARCHAR2(14) | Y |  | 批号 | DB注释(中文) |
| 32 | PROD_GRP | VARCHAR2(2) | Y |  | 品种代码 | DB注释(中文) |
| 33 | JDG_REQ_GRD | VARCHAR2(1) | Y |  | 判定要求分类 | DB注释(中文) |
| 34 | PROD_THK | NUMBER | Y |  | 产品厚度 | DB注释(中文) |
| 35 | PROD_WTH | NUMBER | Y |  | 产品宽 | DB注释(中文) |
| 36 | PROD_LTH | NUMBER | Y |  | 产品长度 | DB注释(中文) |
| 37 | BEF_SPEC_CD | VARCHAR2(50) | Y |  | 国家标准牌号 | DB注释(中文) |
| 38 | BEF_NATL_SPEC_YEAR | VARCHAR2(4) | Y |  | 国家标准年度 | DB注释(中文) |
| 39 | NATL_SPEC_YEAR | VARCHAR2(4) | Y |  | 国家标准年度 | DB注释(中文) |
| 40 | FAC_CD | VARCHAR2(1) | Y |  | 工厂代码 | DB注释(中文) |
| 41 | DEF_PROC | VARCHAR2(30) | Y |  | 缺陷产生工序 | DB注释(中文) |
| 42 | UST_YN | VARCHAR2(10) | Y |  | 是否探伤 | DB注释(中文) |
| 43 | UST_GRD | VARCHAR2(10) | Y |  | 探伤结果 | DB注释(中文) |

### SCH_SLAB_DESIGN_RESULT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=36｜被读 14 过程 / 被写 11 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：7　**主键**：SLAB_DGN_MGT_NO　**语义覆盖**：93/119

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID_ | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(100) | Y |  | Created Object ID_ | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Datetime_Created Object ID | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Updated User ID_Created Datetime | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Updated Object ID_Updated User ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Updated Datetime_Updated Object ID | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Archive Flag_Updated Datetime | DB注释(非中文) |
| 8 | SLAB_DGN_MGT_NO | VARCHAR2(13) | N | ✓ | 材料号 | DB注释(中文) |
| 9 | HEAT_DGN_MGT_NO | VARCHAR2(8) | Y |  | 炉号 | DB注释(中文) |
| 10 | HEAT_INNER_SLAB_SEQ | NUMBER | Y |  | 炉内铸坯顺序号 | DB注释(中文) |
| 11 | HEAT_DGN_YN | VARCHAR2(1) | Y |  | 炉次设计标记 | DB注释(中文) |
| 12 | STR_FL | VARCHAR2(1) | Y |  | Strand구분_Strand分类 | DB注释(中文) |
| 13 | STR_NO | NUMBER | Y |  | 流号 | DB注释(中文) |
| 14 | ORD_NO | VARCHAR2(10) | Y |  | 订单号 | DB注释(中文) |
| 15 | ORD_LN | VARCHAR2(3) | Y |  | 订单行号 | DB注释(中文) |
| 16 | CC_FAC_FL | VARCHAR2(1) | Y |  | 连铸工厂分类 | DB注释(中文) |
| 17 | HR_FAC_FL | VARCHAR2(1) | Y |  | 热轧工厂分类 | DB注释(中文) |
| 18 | POSS_PASS_PLANT_CD | VARCHAR2(30) | Y |  | 可通过工厂代码 | DB注释(中文) |
| 19 | CONF_PASS_PLANT_CD | VARCHAR2(30) | Y |  | 确定通过工厂代码 | DB注释(中文) |
| 20 | SPEC_CD | VARCHAR2(50) | Y |  | 国家标准牌号 | DB注释(中文) |
| 21 | ORD_TY | VARCHAR2(2) | Y |  | 订单类型 | DB注释(中文) |
| 22 | URGENT_TY | VARCHAR2(1) | Y |  | 是否紧急订单 | DB注释(中文) |
| 23 | PROD_CD | VARCHAR2(3) | Y |  | 品名代码 | DB注释(中文) |
| 24 | ORD_USAGE | VARCHAR2(4) | Y |  | 订单用途代码 | DB注释(中文) |
| 25 | ORD_DLV_DT | VARCHAR2(8) | Y |  | 订单交货期 | DB注释(中文) |
| 26 | INCMP_STEEL_NO | VARCHAR2(10) | Y |  | 内控钢种 | DB注释(中文) |
| 27 | ORD_FL | VARCHAR2(1) | Y |  | 订单/余材分类 | DB注释(中文) |
| 28 | ORD_FL_CHANGE_REASON_CD | VARCHAR2(3) | Y |  | 余材原因代码 | DB注释(中文) |
| 29 | HR_PROD_THK_AIM | NUMBER | Y |  | 热轧目标厚度 | DB注释(中文) |
| 30 | HR_PROD_WTH_AIM | NUMBER | Y |  | 热轧目标宽度 | DB注释(中文) |
| 31 | STEEL_GRVT | NUMBER | Y |  | 密度 | DB注释(中文) |
| 32 | QLT_HCR_FL | VARCHAR2(1) | Y |  | 冷热送标记 | DB注释(中文) |
| 33 | PPC_HCR_FL | VARCHAR2(1) | Y |  | 공정계획HCR구분_HCR分类 | DB注释(中文) |
| 34 | HR_ROLL_UNIT_CD | VARCHAR2(1) | Y |  | 热轧Roll单位代码 | DB注释(中文) |
| 35 | HRL_EDGEHEATER_TY | VARCHAR2(1) | Y |  | 热轧EdgeHeater指定分类 | DB注释(中文) |
| 36 | RLG_POSS_WGT_MAX | NUMBER | Y |  | 可轧制单重上限 | DB注释(中文) |
| 37 | TOT_YIELD | NUMBER | Y |  | 综合成材率 | DB注释(中文) |
| 38 | SLAB_DIV_PCS | NUMBER | Y |  | 铸坯内Slab指示支数 | DB注释(中文) |
| 39 | CC_CSTP_RESTRIC_CD | VARCHAR2(8) | Y |  | 连铸铸片使用限制代码 | DB注释(中文) |
| 40 | SLAB_DGN_WTH_RNG_MIN | NUMBER | Y |  | Slab设计宽度下限 | DB注释(中文) |
| 41 | SLAB_DGN_WTH_RNG_MAX | NUMBER | Y |  | Slab设计宽度上限 | DB注释(中文) |
| 42 | SLAB_DGN_LTH_RNG_MIN | NUMBER | Y |  | Slab设计长度下限 | DB注释(中文) |
| 43 | SLAB_DGN_LTH_RNG_MAX | NUMBER | Y |  | Slab设计长度上限 | DB注释(中文) |
| 44 | SLAB_DGN_WGT_RNG_MIN | NUMBER | Y |  | Slab设计重量下限 | DB注释(中文) |
| 45 | SLAB_DGN_WGT_RNG_MAX | NUMBER | Y |  | Slab设计重量上限 | DB注释(中文) |
| 46 | SLAB_DGN_THK | NUMBER | Y |  | Slab设计厚度 | DB注释(中文) |
| 47 | SLAB_DGN_WTH | NUMBER | Y |  | Slab设计宽度 | DB注释(中文) |
| 48 | SLAB_DGN_LTH | NUMBER | Y |  | Slab设计长度 | DB注释(中文) |
| 49 | SLAB_DGN_WGT | NUMBER | Y |  | Slab设计重量 | DB注释(中文) |
| 50 | SLAB_DGN_DIV_PCS | NUMBER | Y |  | Slab设计分割数 | DB注释(中文) |
| 51 | ORD_NO1 | VARCHAR2(10) | Y |  | 订单号1 | DB注释(中文) |
| 52 | ORD_LN1 | VARCHAR2(3) | Y |  | 订单行号1 | DB注释(中文) |
| 53 | SLAB_DGN_WGT1 | NUMBER | Y |  | Slab设计重量1 | DB注释(中文) |
| 54 | SLAB_DGN_LTH1 | NUMBER | Y |  | Slab设计长度1 | DB注释(中文) |
| 55 | ORD_NO2 | VARCHAR2(10) | Y |  | 订单号2 | DB注释(中文) |
| 56 | ORD_LN2 | VARCHAR2(3) | Y |  | 订单行号2 | DB注释(中文) |
| 57 | SLAB_DGN_WGT2 | NUMBER | Y |  | Slab设计重量2 | DB注释(中文) |
| 58 | SLAB_DGN_LTH2 | NUMBER | Y |  | Slab设计长度2 | DB注释(中文) |
| 59 | ORD_NO3 | VARCHAR2(10) | Y |  | 订单号3 | DB注释(中文) |
| 60 | ORD_LN3 | VARCHAR2(3) | Y |  | 订单行号3 | DB注释(中文) |
| 61 | SLAB_DGN_WGT3 | NUMBER | Y |  | Slab设计重量3 | DB注释(中文) |
| 62 | SLAB_DGN_LTH3 | NUMBER | Y |  | Slab设计长度3 | DB注释(中文) |
| 63 | PRI_WO_FL | VARCHAR2(1) | Y |  | 订单/余材分类 | DB注释(中文) |
| 64 | SAME_WTH_CD | NUMBER | Y |  | 동일폭코드_ | DB注释(非中文) |
| 65 | SAME_WTH_LIMIT_CNT | NUMBER | Y |  | 동일폭 제한매수_ | DB注释(非中文) |
| 66 | SAME_THK_CD | NUMBER | Y |  | 동일두께코드_ | DB注释(非中文) |
| 67 | SAME_THK_LIMIT_CNT | NUMBER | Y |  | 동일두께제한매수_ | DB注释(非中文) |
| 68 | ROLL_THK_ALLOW_MIN | NUMBER | Y |  | 轧制厚度最小值 | DB注释(中文) |
| 69 | ROLL_THK_ALLOW_MAX | NUMBER | Y |  | 轧制厚度最大值 | DB注释(中文) |
| 70 | HOT_COIL_CALC_LTH | NUMBER | Y |  | 열연Coil계산길이_ | DB注释(非中文) |
| 71 | SAME_HEAT_CD | VARCHAR2(30) | Y |  | 동일Heat조건_ | DB注释(非中文) |
| 72 | WORK_FLAG1 | VARCHAR2(1) | Y |  |  | 空 |
| 73 | WORK_FLAG2 | VARCHAR2(1) | Y |  |  | 空 |
| 74 | HTM_MTH_CD | VARCHAR2(1) | Y |  | 交货状态(厚板) | DB注释(中文) |
| 75 | SMS_2ND_RFN_CD | VARCHAR2(3) | Y |  | 炼钢2次精炼代码 | DB注释(中文) |
| 76 | TARGET_FL | VARCHAR2(1) | Y |  | 对象区分 | DB注释(中文) |
| 77 | TAPER_FL | VARCHAR2(1) | Y |  | Taper¿¿_Taper¿¿ | SCO_DATA_DIC(D) |
| 78 | SLAB_DGN_STR_WTH | NUMBER | Y |  |  | 空 |
| 79 | SLAB_DGN_END_WTH | NUMBER | Y |  |  | 空 |
| 80 | DGN_MANUAL_FL | VARCHAR2(1) | Y |  | 铸坯设计是否自动 | DB注释(中文) |
| 81 | DE_P_YN | VARCHAR2(1) | Y |  | 脱磷类型。 | DB注释(中文) |
| 82 | ORD_NO4 | VARCHAR2(10) | Y |  | Order No4 | SCO_DATA_DIC(D) |
| 83 | ORD_LN4 | VARCHAR2(3) | Y |  | Order Line4 | SCO_DATA_DIC(D) |
| 84 | SLAB_DGN_WGT4 | NUMBER | Y |  |  | 空 |
| 85 | SLAB_DGN_LTH4 | NUMBER | Y |  |  | 空 |
| 86 | ORD_NO5 | VARCHAR2(10) | Y |  | Order No5 | SCO_DATA_DIC(D) |
| 87 | ORD_LN5 | VARCHAR2(3) | Y |  | Order Line5 | SCO_DATA_DIC(D) |
| 88 | SLAB_DGN_WGT5 | NUMBER | Y |  |  | 空 |
| 89 | SLAB_DGN_LTH5 | NUMBER | Y |  |  | 空 |
| 90 | ORD_NO6 | VARCHAR2(10) | Y |  |  | 空 |
| 91 | ORD_LN6 | VARCHAR2(3) | Y |  |  | 空 |
| 92 | SLAB_DGN_WGT6 | NUMBER | Y |  |  | 空 |
| 93 | SLAB_DGN_LTH6 | NUMBER | Y |  |  | 空 |
| 94 | ORD_EDGE_TY | VARCHAR2(1) | Y |  | 订单Edge分类 | SCO_DATA_DIC(D) |
| 95 | PLT_HEATING_CD | VARCHAR2(1) | Y |  | 热处理方式 | DB注释(中文) |
| 96 | UST_MTH_CD | VARCHAR2(2) | Y |  | 方法代码。 | DB注释(中文) |
| 97 | GAS_CUT_FL | VARCHAR2(1) | Y |  | GAS절단구분 | SCO_DATA_DIC(D) |
| 98 | DGN_OVROLL_QTY | NUMBER | Y |  |  | 空 |
| 99 | DGN_OVROLL_WGT | NUMBER | Y |  |  | 空 |
| 100 | CCM_NO | VARCHAR2(1) | Y |  | 连铸机号 | DB注释(中文) |
| 101 | SLAB_TY | VARCHAR2(1) | Y |  | Slab Type | SCO_DATA_DIC(D) |
| 102 | MOM_SLAB_DGN_MGT_NO | VARCHAR2(13) | Y |  |  | 空 |
| 103 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  | 钢种 | DB注释(中文) |
| 104 | ORD_NO7 | VARCHAR2(10) | Y |  |  | 空 |
| 105 | ORD_LN7 | VARCHAR2(3) | Y |  |  | 空 |
| 106 | SLAB_DGN_WGT7 | NUMBER | Y |  |  | 空 |
| 107 | SLAB_DGN_LTH7 | NUMBER | Y |  |  | 空 |
| 108 | ORD_NO8 | VARCHAR2(10) | Y |  | ORD_NO9 | SCO_DATA_DIC(D) |
| 109 | ORD_LN8 | VARCHAR2(3) | Y |  |  | 空 |
| 110 | SLAB_DGN_WGT8 | NUMBER | Y |  |  | 空 |
| 111 | SLAB_DGN_LTH8 | NUMBER | Y |  |  | 空 |
| 112 | ORD_NO9 | VARCHAR2(10) | Y |  |  | 空 |
| 113 | ORD_LN9 | VARCHAR2(3) | Y |  |  | 空 |
| 114 | SLAB_DGN_WGT9 | NUMBER | Y |  |  | 空 |
| 115 | SLAB_DGN_LTH9 | NUMBER | Y |  |  | 空 |
| 116 | PROD_GRP | VARCHAR2(2) | Y |  | Product Group | SCO_DATA_DIC(D) |
| 117 | HR_PROD_LTH_AIM | NUMBER | Y |  | 轧制目标长度 | DB注释(中文) |
| 118 | HR_PROD_FTHK_AIM | NUMBER | Y |  | 腹板厚度 | DB注释(中文) |
| 119 | HR_PROD_YTHK_AIM | NUMBER | Y |  | 翼缘厚度 | DB注释(中文) |

### SYD_DISP_ORD

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=35｜被读 23 过程 / 被写 6 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：1748　**主键**：DORD_NO　**语义覆盖**：41/41

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | SCO_DATA_DIC(D) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | SCO_DATA_DIC(D) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | SCO_DATA_DIC(D) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated UserID | SCO_DATA_DIC(D) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated ObjectID | SCO_DATA_DIC(D) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Date Time | SCO_DATA_DIC(D) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | SCO_DATA_DIC(D) |
| 8 | DORD_NO | VARCHAR2(50) | N | ✓ | 提货单号 | DB注释(中文) |
| 9 | CAR_NO | VARCHAR2(20) | Y |  | 车号 | DB注释(中文) |
| 10 | TRNSF_MTH_CD | VARCHAR2(2) | Y |  | 运输方式 | DB注释(中文) |
| 11 | DORD_COMMENT | VARCHAR2(2000) | Y |  | 备注 | DB注释(中文) |
| 12 | CUST_CD | VARCHAR2(40) | Y |  | 客户编码 | DB注释(中文) |
| 13 | CUST_NM | VARCHAR2(100) | N |  | 客户名称 | DB注释(中文) |
| 14 | WGT_DCN_MTH_CD | VARCHAR2(20) | Y |  | 计重方式 | DB注释(中文) |
| 15 | DORD_CANCEL_DTM | VARCHAR2(14) | Y |  | 取消时间 | DB注释(中文) |
| 16 | DORD_CANCEL_USER_ID | VARCHAR2(20) | Y |  | 取消人 | DB注释(中文) |
| 17 | DORD_COMPL_DTM | VARCHAR2(14) | Y |  | 发货时间 | DB注释(中文) |
| 18 | DORD_COMPL_USER_ID | VARCHAR2(20) | Y |  | 装车人 | DB注释(中文) |
| 19 | FIRST_SCALE | VARCHAR2(1) | Y |  | 是否第一次计量 | DB注释(中文) |
| 20 | DORD_STS | VARCHAR2(1) | Y |  | 1、新建 2、保存、3完成  9取消 | DB注释(中文) |
| 21 | DORD_TY | VARCHAR2(20) | Y |  | 提货单类型 0-销售；1-退货 | DB注释(中文) |
| 22 | PROD_GRP | VARCHAR2(20) | Y |  | 品种 GA:钢坯  GP:中板 | DB注释(中文) |
| 23 | DORD_CONF_DTM | VARCHAR2(14) | Y |  | 确认时间 | DB注释(中文) |
| 24 | DORD_CONF_USER_ID | VARCHAR2(20) | Y |  | 确认人 | DB注释(中文) |
| 25 | DORD_LOAD_DTM | VARCHAR2(14) | Y |  | 装车时间 | DB注释(中文) |
| 26 | RCV_UNIT_NM | VARCHAR2(200) | Y |  | 收货单位 | DB注释(中文) |
| 27 | SEC_SCALE_DTM | VARCHAR2(14) | Y |  | 二次计量时间 | DB注释(中文) |
| 28 | FIRST_SCALE_DTM | VARCHAR2(14) | Y |  | 一次计量时间 | DB注释(中文) |
| 29 | TAKE_TY | VARCHAR2(10) | Y |  | 提货方式(0-自提；1-配送) | DB注释(中文) |
| 30 | SITE_CD | VARCHAR2(20) | N |  | 收货方代码 | DB注释(中文) |
| 31 | SHIP_NO | VARCHAR2(20) | Y |  | 船号 | DB注释(中文) |
| 32 | SITE_ADDR | VARCHAR2(500) | Y |  | 收货方地址 | DB注释(中文) |
| 33 | SITE_NM | VARCHAR2(100) | Y |  | 收货方名称 | DB注释(中文) |
| 34 | DORD_CRT_DTM | VARCHAR2(14) | Y |  | 提货单时间 | DB注释(中文) |
| 35 | DORD_NO_SHIP | VARCHAR2(50) | Y |  | 配船号 | DB注释(中文) |
| 36 | DORD_EXA_YN | VARCHAR2(10) | Y |  | 财务审核(确认) | DB注释(中文) |
| 37 | PRT_PCS | NUMBER | Y |  | 打印次数 | DB注释(中文) |
| 38 | DORD_EXA_CANCL_YN | VARCHAR2(10) | Y |  | 财务审核(作废) | DB注释(中文) |
| 39 | APPLY_YN | VARCHAR2(10) | Y |  | 确认申请 | DB注释(中文) |
| 40 | CANCEL_YN | VARCHAR2(10) | Y |  | 作废申请 | DB注释(中文) |
| 41 | DORD_WGT | NUMBER | Y |  | 提货单重量 | DB注释(中文) |

### SQM_CC_MECH_RSLT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=35｜被读 23 过程 / 被写 6 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：0　**主键**：SMP_NO、SMP_LTH_LOC、TEST_CNT　**语义覆盖**：420/421

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | SMP_NO | VARCHAR2(14) | N | ✓ | 试样编号 | DB注释(中文) |
| 9 | SMP_LTH_LOC | VARCHAR2(1) | N | ✓ | 试样采取位置 | DB注释(中文) |
| 10 | TEST_CNT | NUMBER | N | ✓ | 试验回数 | DB注释(中文) |
| 11 | MECH_RSLT_REG_FST_DTM | VARCHAR2(14) | Y |  | 材质实绩录入最初时间 | DB注释(中文) |
| 12 | MECH_RSLT_REG_LST_DTM | VARCHAR2(14) | Y |  | 材质实绩录入最终时间 | DB注释(中文) |
| 13 | PROD_CHEM_RSLT_REG_DTM | VARCHAR2(14) | Y |  | 产品成分实绩登记时间 | DB注释(中文) |
| 14 | COAT_TEST_RSLT_REG_DTM | VARCHAR2(14) | Y |  | 镀锌试验实绩登记时间 | DB注释(中文) |
| 15 | SMP_GTH_INST_MTRL_NO | VARCHAR2(20) | Y |  | 试样采取指示材料编号 | DB注释(中文) |
| 16 | SMP_HTM_ASGN_TY | VARCHAR2(1) | Y |  | 试样热处理指定分类 | DB注释(中文) |
| 17 | MECH_JDG_GRD | VARCHAR2(1) | Y |  | 物性判定等级 | DB注释(中文) |
| 18 | TSL_YP_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度类型 | DB注释(中文) |
| 19 | TSL_YP_RSLT | NUMBER | Y |  | 拉伸测试屈服强度实绩 | DB注释(中文) |
| 20 | TSL_YP_JDG | VARCHAR2(1) | Y |  | 拉伸测试屈服强度判定 | DB注释(中文) |
| 21 | TSL_TS_RSLT | NUMBER | Y |  | 拉伸测试抗拉强度实绩 | DB注释(中文) |
| 22 | TSL_TS_JDG | VARCHAR2(1) | Y |  | 拉伸测试抗拉强度判定 | DB注释(中文) |
| 23 | TSL_EL_CD | VARCHAR2(1) | Y |  | 拉伸测试伸长率类型 | DB注释(中文) |
| 24 | TSL_EL_RSLT | NUMBER | Y |  | 拉伸测试伸长率实绩 | DB注释(中文) |
| 25 | TSL_EL_JDG | VARCHAR2(1) | Y |  | 拉伸测试伸长率判定 | DB注释(中文) |
| 26 | TSL_YR_RSLT | NUMBER | Y |  | 拉伸测试屈强比实绩 | DB注释(中文) |
| 27 | TSL_YR_JDG | VARCHAR2(1) | Y |  | 拉伸测试屈强比判定 | DB注释(中文) |
| 28 | TSL_RA_RSLT | NUMBER | Y |  | 拉伸测试断面收缩率实绩 | DB注释(中文) |
| 29 | TSL_RA_JDG | VARCHAR2(1) | Y |  | 拉伸测试断面收缩率判定 | DB注释(中文) |
| 30 | TSL_R_RSLT | NUMBER | Y |  | 拉抻测试塑性应变比r平均实绩 | DB注释(中文) |
| 31 | TSL_R_JDG | VARCHAR2(1) | Y |  | 拉抻测试塑性应变比r平均判定 | DB注释(中文) |
| 32 | TSL_R0_RSLT | NUMBER | Y |  | 拉抻测试r0实绩 | DB注释(中文) |
| 33 | TSL_R0_JDG | VARCHAR2(1) | Y |  | 拉抻测试r0判定 | DB注释(中文) |
| 34 | TSL_R45_RSLT | NUMBER | Y |  | 拉抻测试r45实绩 | DB注释(中文) |
| 35 | TSL_R45_JDG | VARCHAR2(1) | Y |  | 拉抻测试r45判定 | DB注释(中文) |
| 36 | TSL_R90_RSLT | NUMBER | Y |  | 拉抻测试r90实绩 | DB注释(中文) |
| 37 | TSL_R90_JDG | VARCHAR2(1) | Y |  | 拉抻测试r90判定 | DB注释(中文) |
| 38 | TSL_RDELTA_RSLT | NUMBER | Y |  | 拉伸测试\|Δr\|上限值实绩 | DB注释(中文) |
| 39 | TSL_RDELTA_JDG | VARCHAR2(1) | Y |  | 拉伸测试\|Δr\|上限值判定 | DB注释(中文) |
| 40 | TSL_N_RSLT | NUMBER | Y |  | 拉伸测试加工硬化指数n平均实绩 | DB注释(中文) |
| 41 | TSL_N_JDG | VARCHAR2(1) | Y |  | 拉抻测试N判定 | DB注释(中文) |
| 42 | TSL_N0_RSLT | NUMBER | Y |  | 拉抻测试N0实绩 | DB注释(中文) |
| 43 | TSL_N0_JDG | VARCHAR2(1) | Y |  | 拉抻测试N0判定 | DB注释(中文) |
| 44 | TSL_N45_RSLT | NUMBER | Y |  | 拉抻测试N45实绩 | DB注释(中文) |
| 45 | TSL_N45_JDG | VARCHAR2(1) | Y |  | 拉抻测试N45判定 | DB注释(中文) |
| 46 | TSL_N90_RSLT | NUMBER | Y |  | 拉抻测试N90实绩 | DB注释(中文) |
| 47 | TSL_N90_JDG | VARCHAR2(1) | Y |  | 拉抻测试N90判定 | DB注释(中文) |
| 48 | TSL_TESTER_CD | VARCHAR2(20) | Y |  | 拉伸试验机代码 | DB注释(中文) |
| 49 | TSL_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 拉伸试验人ID | DB注释(中文) |
| 50 | BEND_CD | VARCHAR2(1) | Y |  | 弯曲测试角度 | DB注释(中文) |
| 51 | BEND_UNIT | VARCHAR2(1) | Y |  | 弯曲压头直径 | DB注释(中文) |
| 52 | BEND_ANGLE | NUMBER | Y |  | 弯曲测试弯曲角度 | DB注释(中文) |
| 53 | BEND_DIA | NUMBER | Y |  | 弯曲测试弯心直径 | DB注释(中文) |
| 54 | BEND_RSLT | VARCHAR2(1) | Y |  | 弯曲测试实绩 | DB注释(中文) |
| 55 | BEND_JDG | VARCHAR2(1) | Y |  | 弯曲测试判定 | DB注释(中文) |
| 56 | BEND_TESTER_CD | VARCHAR2(20) | Y |  | 弯曲试验机代码 | DB注释(中文) |
| 57 | BEND_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 弯曲试验人ID | DB注释(中文) |
| 58 | HARD_KIND | VARCHAR2(1) | Y |  | 硬度测试种类 | DB注释(中文) |
| 59 | HARD_RSLT | NUMBER | Y |  | 硬度测试实绩 | DB注释(中文) |
| 60 | HARD_JDG | VARCHAR2(1) | Y |  | 硬度测试判定 | DB注释(中文) |
| 61 | HARD_RSLT1 | NUMBER | Y |  | 硬度试验实绩1 | DB注释(中文) |
| 62 | HARD_RSLT2 | NUMBER | Y |  | 硬度试验实绩2 | DB注释(中文) |
| 63 | HARD_RSLT3 | NUMBER | Y |  | 硬度试验实绩3 | DB注释(中文) |
| 64 | HARD_TESTER_CD | VARCHAR2(20) | Y |  | 硬度试验机代码 | DB注释(中文) |
| 65 | HARD_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 硬度试验人ID | DB注释(中文) |
| 66 | IMPACT_SPCMN_CNT | NUMBER | Y |  | 冲击测试试样数量 | DB注释(中文) |
| 67 | IMPACT_TEMP | NUMBER | Y |  | 冲击测试温度 | DB注释(中文) |
| 68 | IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 冲击测试缺口类型 | DB注释(中文) |
| 69 | IMPACT_AVG_RSLT | NUMBER | Y |  | 冲击测试吸收能量实绩 | DB注释(中文) |
| 70 | IMPACT_IND_RSLT1 | NUMBER | Y |  | 冲击功单个实绩1 | DB注释(中文) |
| 71 | IMPACT_IND_JDG | VARCHAR2(1) | Y |  | 冲击功单个判定 | DB注释(中文) |
| 72 | IMPACT_IND_RSLT2 | NUMBER | Y |  | 冲击功单个实绩2 | DB注释(中文) |
| 73 | IMPACT_IND_RSLT3 | NUMBER | Y |  | 冲击功单个实绩3 | DB注释(中文) |
| 74 | IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 冲击测试纤维断面率平均实绩 | DB注释(中文) |
| 75 | IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩1 | DB注释(中文) |
| 76 | IMPACT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 冲击测试纤维断面率单个判定 | DB注释(中文) |
| 77 | IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩2 | DB注释(中文) |
| 78 | IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩3 | DB注释(中文) |
| 79 | IMPACT_TESTER_CD | VARCHAR2(20) | Y |  | 冲击试验机代码 | DB注释(中文) |
| 80 | IMPACT_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 冲击试验人ID | DB注释(中文) |
| 81 | MGRPHY_GRNSZ_LEVEL | NUMBER | Y |  | 金相测试晶粒度级别 | DB注释(中文) |
| 82 | MGRPHY_GRNSZ_OCCP | NUMBER | Y |  | 金相测试基相晶粒的体积分数 | DB注释(中文) |
| 83 | MGRPHY_FGS_MIXED_RATIO_RSLT | NUMBER | Y |  | 铁素体晶粒混晶占有率实绩 | DB注释(中文) |
| 84 | MGRPHY_FGS_MIXED_RATIO_JDG | VARCHAR2(1) | Y |  | 铁素体晶粒混晶占有率判定 | DB注释(中文) |
| 85 | MGRPHY_FGS_DEVT_MAX_RSLT | NUMBER | Y |  | 铁素体混晶晶粒度差实绩 | DB注释(中文) |
| 86 | MGRPHY_FGS_DEVT_MAX_JDG | VARCHAR2(1) | Y |  | 铁素体混晶晶粒度差判定 | DB注释(中文) |
| 87 | MGRPHY_FGS_RSLT | NUMBER | Y |  | 铁素体晶粒尺寸实绩 | DB注释(中文) |
| 88 | MGRPHY_FGS_JDG | VARCHAR2(1) | Y |  | 铁素体晶粒尺寸判定 | DB注释(中文) |
| 89 | MGRPHY_AGS_RSLT | NUMBER | Y |  | 奥氏体晶粒尺寸实绩 | DB注释(中文) |
| 90 | MGRPHY_AGS_JDG | VARCHAR2(1) | Y |  | 奥氏体晶粒尺寸判定 | DB注释(中文) |
| 91 | MGRPHY_INCLD_TY | VARCHAR2(1) | Y |  | 夹杂物类别 | DB注释(中文) |
| 92 | MGRPHY_INCLD_GRD_MAX_RSLT | NUMBER | Y |  | 夹杂物等级上限实绩 | DB注释(中文) |
| 93 | MGRPHY_INCLD_GRD_MAX_JDG | VARCHAR2(1) | Y |  | 夹杂物等级上限实绩 | DB注释(中文) |
| 94 | MGRPHY_DECARBON_MAX_RSLT | NUMBER | Y |  | 脱碳层上限实绩 | DB注释(中文) |
| 95 | MGRPHY_DECARBON_MAX_JDG | VARCHAR2(1) | Y |  | 脱碳层上限实绩 | DB注释(中文) |
| 96 | MGRPHY_WILD_STRC_GRD | NUMBER | Y |  | 魏氏组织等级 | DB注释(中文) |
| 97 | MGRPHY_WILD_STRC_JDG | VARCHAR2(1) | Y |  | 魏氏组织判定 | DB注释(中文) |
| 98 | MGRPHY_MTLGRP_TY | VARCHAR2(2) | Y |  | 组织类型 | DB注释(中文) |
| 99 | MGRPHY_BAND_STRC_GRD_MAX_RSLT | NUMBER | Y |  | 带状组织等级上限实绩 | DB注释(中文) |
| 100 | MGRPHY_BAND_STRC_GRD_MAX_JDG | VARCHAR2(1) | Y |  | 带状组织等级上限判定 | DB注释(中文) |
| 101 | MGRPHY_RAT_TESTER_CD | VARCHAR2(20) | Y |  | 金相试验粒度组织分类试验机代码 | DB注释(中文) |
| 102 | MGRPHY_RAT_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 金相试验粒度组织分类试验人ID | DB注释(中文) |
| 103 | NON_METAL_GRD_KIND_CD | VARCHAR2(2) | Y |  | 非金属夹杂物级别 | DB注释(中文) |
| 104 | NON_METAL_A_RSLT | NUMBER | Y |  | 非金属夹杂物A类实绩(粗) | DB注释(中文) |
| 105 | NON_METAL_A_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物A类判定(粗) | DB注释(中文) |
| 106 | NON_METAL_B_RSLT | NUMBER | Y |  | 非金属夹杂物B类实绩(粗) | DB注释(中文) |
| 107 | NON_METAL_B_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物B类判定(粗) | DB注释(中文) |
| 108 | NON_METAL_C_RSLT | NUMBER | Y |  | 非金属夹杂物C类实绩(粗) | DB注释(中文) |
| 109 | NON_METAL_C_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物C类判定(粗) | DB注释(中文) |
| 110 | NON_METAL_D_RSLT | NUMBER | Y |  | 非金属夹杂物D类实绩(粗) | DB注释(中文) |
| 111 | NON_METAL_D_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物D类判定(粗) | DB注释(中文) |
| 112 | NON_METAL_DS_RSLT | NUMBER | Y |  | 非金属夹杂物Ds实绩 | DB注释(中文) |
| 113 | NON_METAL_DS_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物Ds判定 | DB注释(中文) |
| 114 | NON_METAL_A1_RSLT | NUMBER | Y |  | 非金属夹杂物A1类实绩(细) | DB注释(中文) |
| 115 | NON_METAL_A1_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物A1类判定(细) | DB注释(中文) |
| 116 | NON_METAL_B1_RSLT | NUMBER | Y |  | 非金属夹杂物B1类实绩(细) | DB注释(中文) |
| 117 | NON_METAL_B1_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物B1类判定(细) | DB注释(中文) |
| 118 | NON_METAL_C1_RSLT | NUMBER | Y |  | 非金属夹杂物C1类实绩(细) | DB注释(中文) |
| 119 | NON_METAL_C1_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物C1类判定(细) | DB注释(中文) |
| 120 | NON_METAL_D1_RSLT | NUMBER | Y |  | 非金属夹杂物D1类实绩(细) | DB注释(中文) |
| 121 | NON_METAL_D1_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物D1类判定(细) | DB注释(中文) |
| 122 | NON_METAL_DS1_RSLT | NUMBER | Y |  | 非金属夹杂物Ds1实绩 | DB注释(中文) |
| 123 | NON_METAL_DS1_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物Ds1判定 | DB注释(中文) |
| 124 | NON_METAL_ABCD_RSLT | NUMBER | Y |  | 非金属夹杂物A+B+C+D实绩(粗) | DB注释(中文) |
| 125 | NON_METAL_ABCD_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物ABCD判定(粗) | DB注释(中文) |
| 126 | NON_METAL_MAX_WTH_RSLT | NUMBER | Y |  | 非金属夹杂物测试最大宽度实绩 | DB注释(中文) |
| 127 | NON_METAL_MAX_LTH_RSLT | NUMBER | Y |  | 非金属夹杂物测试最大长度实绩 | DB注释(中文) |
| 128 | NON_METAL_TESTER_CD | VARCHAR2(20) | Y |  | 非金属夹杂物试验机代码 | DB注释(中文) |
| 129 | NON_METAL_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 非金属夹杂物试验人ID | DB注释(中文) |
| 130 | HIGH_TEMP_TSL_TEMP | NUMBER | Y |  | 高温拉伸测试温度 | DB注释(中文) |
| 131 | HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  | 高温拉伸测试屈服强度类型 | DB注释(中文) |
| 132 | HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  | 高温拉伸测试屈服强度实绩 | DB注释(中文) |
| 133 | HIGH_TEMP_TSL_YP_JDG | VARCHAR2(1) | Y |  | 高温拉伸测试屈服强度判定 | DB注释(中文) |
| 134 | HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  | 高温拉伸测试抗拉强度实绩 | DB注释(中文) |
| 135 | HIGH_TEMP_TSL_TS_JDG | VARCHAR2(1) | Y |  | 高温拉伸测试抗拉强度判定 | DB注释(中文) |
| 136 | HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  | 高温拉伸测试伸长率类型 | DB注释(中文) |
| 137 | HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  | 高温拉伸测试伸长率实绩 | DB注释(中文) |
| 138 | HIGH_TEMP_TSL_EL_JDG | VARCHAR2(1) | Y |  | 高温拉伸测试伸长率判定 | DB注释(中文) |
| 139 | HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  | 高温拉伸测试断面收缩率实绩 | DB注释(中文) |
| 140 | HIGH_TEMP_TSL_RA_JDG | VARCHAR2(1) | Y |  | 高温拉伸测试断面收缩率判定 | DB注释(中文) |
| 141 | HIGH_TSL_TESTER_CD | VARCHAR2(20) | Y |  | 高温拉伸试验机代码 | DB注释(中文) |
| 142 | HIGH_TSL_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 高温拉伸试验人ID | DB注释(中文) |
| 143 | CLEAN1_KIND | VARCHAR2(1) | Y |  | 清净度测试1种类 | DB注释(中文) |
| 144 | CLEAN1_RSLT | NUMBER | Y |  | 清净度测试1实绩 | DB注释(中文) |
| 145 | CLEAN1_JDG | VARCHAR2(1) | Y |  | 清净度测试1判定 | DB注释(中文) |
| 146 | CLEAN2_KIND | VARCHAR2(1) | Y |  | 清净度测试2种类 | DB注释(中文) |
| 147 | CLEAN2_RSLT | NUMBER | Y |  | 清净度测试2实绩 | DB注释(中文) |
| 148 | CLEAN2_JDG | VARCHAR2(1) | Y |  | 清净度测试2判定 | DB注释(中文) |
| 149 | CLEAN3_KIND | VARCHAR2(1) | Y |  | 清净度测试3种类 | DB注释(中文) |
| 150 | CLEAN3_RSLT | NUMBER | Y |  | 清净度测试3实绩 | DB注释(中文) |
| 151 | CLEAN3_JDG | VARCHAR2(1) | Y |  | 清净度测试3判定 | DB注释(中文) |
| 152 | CLEAN_TESTER_CD | VARCHAR2(20) | Y |  | 洁净度试验机代码 | DB注释(中文) |
| 153 | CLEAN_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 洁净度试验人ID | DB注释(中文) |
| 154 | ROUGH_KIND | VARCHAR2(1) | Y |  | 粗糙度测试种类 | DB注释(中文) |
| 155 | ROUGH_DIR | VARCHAR2(1) | Y |  | 粗度测试方向 | DB注释(中文) |
| 156 | ROUGH_RA_RSLT | NUMBER | Y |  | 表面平均粗糙度实绩(Ra) | DB注释(中文) |
| 157 | ROUGH_RA_JDG | VARCHAR2(1) | Y |  | 表面平均粗糙度判定(Ra) | DB注释(中文) |
| 158 | ROUGH_RPC_RSLT | NUMBER | Y |  | 单位长度内峰值个数实绩(Rpc) | DB注释(中文) |
| 159 | ROUGH_RPC_JDG | VARCHAR2(1) | Y |  | 单位长度内峰值个数判定(Rpc) | DB注释(中文) |
| 160 | ROUGH_RMAX_RSLT | NUMBER | Y |  | 表面粗糙度最大值实绩(Rmax) | DB注释(中文) |
| 161 | ROUGH_RMAX_JDG | VARCHAR2(1) | Y |  | 表面粗糙度最大值判定(Rmax) | DB注释(中文) |
| 162 | ROUGH_TESTER_CD | VARCHAR2(20) | Y |  | 粗糙度测试机代码 | DB注释(中文) |
| 163 | ROUGH_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 粗糙度测试试验人ID | DB注释(中文) |
| 164 | FATIG_SPCMN_CNT | NUMBER | Y |  | 疲劳测试试样数量 | DB注释(中文) |
| 165 | FATIG_TEMP_RSLT | NUMBER | Y |  | 疲劳测试温度实绩 | DB注释(中文) |
| 166 | FATIG_TEMP_JDG | VARCHAR2(1) | Y |  | 疲劳测试温度判定 | DB注释(中文) |
| 167 | FATIG_FREQ_RSLT | NUMBER | Y |  | 疲劳测试频率实绩 | DB注释(中文) |
| 168 | FATIG_FREQ_JDG | VARCHAR2(1) | Y |  | 疲劳测试频率判定 | DB注释(中文) |
| 169 | FATIG_SERV_LIFE_RSLT | NUMBER | Y |  | 疲劳寿命实绩 | DB注释(中文) |
| 170 | FATIG_SERV_LIFE_JDG | VARCHAR2(1) | Y |  | 疲劳寿命判定 | DB注释(中文) |
| 171 | FATIG_CND_STRTH_RSLT | NUMBER | Y |  | 条件疲劳强度实绩 | DB注释(中文) |
| 172 | FATIG_CND_STRTH_JDG | VARCHAR2(1) | Y |  | 条件疲劳强度判定 | DB注释(中文) |
| 173 | COAT_WGT_SPCMN_CNT | NUMBER | Y |  | 镀锌层质量测试取样数量 | DB注释(中文) |
| 174 | ORD_COAT_WGT_CD | VARCHAR2(7) | Y |  | 订单镀锌量代码 | DB注释(中文) |
| 175 | TST_COAT_WGT_UPPER2_RSLT | NUMBER | Y |  | 镀锌层质量测试上表面镀层实绩2 | DB注释(中文) |
| 176 | TST_COAT_WGT_UPPER3_RSLT | NUMBER | Y |  | 镀锌层质量测试上表面镀层实绩3 | DB注释(中文) |
| 177 | TST_COAT_WGT_LOWER2_RSLT | NUMBER | Y |  | 镀锌层质量测试下表面镀层实绩2 | DB注释(中文) |
| 178 | TST_COAT_WGT_LOWER3_RSLT | NUMBER | Y |  | 镀锌层质量测试下表面镀层实绩3 | DB注释(中文) |
| 179 | TST_COAT_WGT_SUM1_RSLT | NUMBER | Y |  | 镀锌层质量测试上下表面和1 | DB注释(中文) |
| 180 | TST_COAT_WGT_UPPER1_RSLT | NUMBER | Y |  | 镀锌层质量测试上表面镀层实绩1 | DB注释(中文) |
| 181 | TST_COAT_WGT_UPPER_AVG_RSLT | NUMBER | Y |  | 镀锌层质量测试上表面平均实绩 | DB注释(中文) |
| 182 | TST_COAT_WGT_LOWER1_RSLT | NUMBER | Y |  | 镀锌层质量测试下表面镀层实绩1 | DB注释(中文) |
| 183 | TST_COAT_WGT_JDG | VARCHAR2(1) | Y |  | 镀锌层质量测试镀层判定结果 | DB注释(中文) |
| 184 | TST_COAT_WGT_TESTER_CD | VARCHAR2(20) | Y |  | 镀锌量试验机代码 | DB注释(中文) |
| 185 | TST_COAT_WGT_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 镀锌量试验人ID | DB注释(中文) |
| 186 | PSTREAT_CD | VARCHAR2(3) | Y |  | 后处理方法代码 | DB注释(中文) |
| 187 | PHOSP_ADHE_UPPER_RSLT | NUMBER | Y |  | 磷化膜重量上表面实绩 | DB注释(中文) |
| 188 | PHOSP_ADHE_UPPER_JDG | VARCHAR2(1) | Y |  | 磷化膜重量上表面等级 | DB注释(中文) |
| 189 | PHOSP_ADHE_LOWER_RSLT | NUMBER | Y |  | 磷化膜重量下表面实绩 | DB注释(中文) |
| 190 | PHOSP_ADHE_LOWER_JDG | VARCHAR2(1) | Y |  | 磷化膜重量下表面等级 | DB注释(中文) |
| 191 | CHROMATE_ADHE_UPPER_RSLT | NUMBER | Y |  | 无铬钝化膜上表面实绩 | DB注释(中文) |
| 192 | CHROMATE_ADHE_UPPER_JDG | VARCHAR2(1) | Y |  | 无铬钝化膜上表面等级 | DB注释(中文) |
| 193 | CHROMATE_ADHE_LOWER_RSLT | NUMBER | Y |  | 无铬钝化膜下表面实绩 | DB注释(中文) |
| 194 | CHROMATE_ADHE_LOWER_JDG | VARCHAR2(1) | Y |  | 无铬钝化膜下表面等级 | DB注释(中文) |
| 195 | ANTIFNG_WGT_UPPER_RSLT | NUMBER | Y |  | 无铬耐指纹钝化膜上表面重量实绩 | DB注释(中文) |
| 196 | ANTIFNG_WGT_UPPER_JDG | VARCHAR2(1) | Y |  | 无铬耐指纹钝化膜上表面重量等级 | DB注释(中文) |
| 197 | ANTIFNG_WGT_LOWER_RSLT | NUMBER | Y |  | 无铬耐指纹钝化膜下表面重量实绩 | DB注释(中文) |
| 198 | ANTIFNG_WGT_LOWER_JDG | VARCHAR2(1) | Y |  | 无铬耐指纹钝化膜下表面重量等级 | DB注释(中文) |
| 199 | CHROMFRE_ADHE_UPPER_RSLT | NUMBER | Y |  | 无铬自润滑膜上表面实绩 | DB注释(中文) |
| 200 | CHROMFRE_ADHE_UPPER_JDG | VARCHAR2(1) | Y |  | 无铬自润滑膜上表面等级 | DB注释(中文) |
| 201 | CHROMFRE_ADHE_LOWER_RSLT | NUMBER | Y |  | 无铬自润滑膜下表面实绩 | DB注释(中文) |
| 202 | CHROMFRE_ADHE_LOWER_JDG | VARCHAR2(1) | Y |  | 无铬自润滑膜下表面等级 | DB注释(中文) |
| 203 | OIL_MTH_CD | VARCHAR2(2) | Y |  | 涂油方法代码 | DB注释(中文) |
| 204 | OIL_WGT_RSLT | NUMBER | Y |  | 涂油量测试双面涂油量实绩 | DB注释(中文) |
| 205 | OIL_WGT_JDG | VARCHAR2(1) | Y |  | 涂油量测试双面涂油量判定 | DB注释(中文) |
| 206 | OIL_WGT_UPPER_RSLT | NUMBER | Y |  | 涂油量测试上表面涂油量实绩 | DB注释(中文) |
| 207 | OIL_WGT_UPPER_JDG | VARCHAR2(1) | Y |  | 涂油量测试上表面涂油量判定 | DB注释(中文) |
| 208 | OIL_WGT_LOWER_RSLT | NUMBER | Y |  | 涂油量测试下表面涂油量实绩 | DB注释(中文) |
| 209 | OIL_WGT_LOWER_JDG | VARCHAR2(1) | Y |  | 涂油量测试下表面涂油量判定 | DB注释(中文) |
| 210 | OIL_WGT_TESTER_CD | VARCHAR2(20) | Y |  | 涂油量试验机代码 | DB注释(中文) |
| 211 | OIL_WGT_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 涂油量试验人ID | DB注释(中文) |
| 212 | ERICHSEN_RSLT | NUMBER | Y |  | 杯突测试 | DB注释(中文) |
| 213 | ERICHSEN_JDG | VARCHAR2(1) | Y |  | 杯突测试判定 | DB注释(中文) |
| 214 | ERICHSEN_TESTER_CD | VARCHAR2(20) | Y |  | Erichsen试验机代码 | DB注释(中文) |
| 215 | ERICHSEN_DUTY_EMP_ID | VARCHAR2(20) | Y |  | Erichsen试验人ID | DB注释(中文) |
| 216 | WAVIN_TY | VARCHAR2(1) | Y |  | 波纹度测试种类 | DB注释(中文) |
| 217 | WAVIN_WA_RSLT | NUMBER | Y |  | 波纹度检测实绩(Wa) | DB注释(中文) |
| 218 | WAVIN_WA_JDG | VARCHAR2(1) | Y |  | 波纹度检测判定(Wa) | DB注释(中文) |
| 219 | WAVIN_WMAX_RSLT | NUMBER | Y |  | 波纹度检测最大值实绩(Wmax) | DB注释(中文) |
| 220 | WAVIN_WMAX_JDG | VARCHAR2(1) | Y |  | 波纹度检测最大值判定(Wmax) | DB注释(中文) |
| 221 | WAVIN_TESTER_CD | VARCHAR2(20) | Y |  | 波纹度检测 | DB注释(中文) |
| 222 | WAVIN_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 波纹度检测 | DB注释(中文) |
| 223 | COAT_ATTH_CD | VARCHAR2(1) | Y |  | 锌层附着性测试方法 | DB注释(中文) |
| 224 | COAT_ATTH_UPPER_REFLCT_RSLT | NUMBER | Y |  | 锌层附着性测试上表面光反射浓度实绩 | DB注释(中文) |
| 225 | COAT_ATTH_UPPER_REFLCT_JDG | VARCHAR2(1) | Y |  | 锌层附着性测试上表面光反射浓度判定 | DB注释(中文) |
| 226 | COAT_ATTH_LOWER_REFLCT_RSLT | NUMBER | Y |  | 锌层附着性测试下表面光反射浓度实绩 | DB注释(中文) |
| 227 | COAT_ATTH_LOWER_REFLCT_JDG | VARCHAR2(1) | Y |  | 锌层附着性测试下表面光反射浓度判定 | DB注释(中文) |
| 228 | COAT_ATTH_DEWTH_RSLT | NUMBER | Y |  | 锌层附着性测试表面锌层脱落宽度实绩 | DB注释(中文) |
| 229 | COAT_ATTH_DEWTH_JDG | VARCHAR2(1) | Y |  | 锌层附着性测试表面锌层脱落宽度判定 | DB注释(中文) |
| 230 | COAT_ATTH_DERATIO_RSLT | NUMBER | Y |  | 锌层附着性测试表面锌层脱落率实绩 | DB注释(中文) |
| 231 | COAT_ATTH_DERATIO_JDG | VARCHAR2(1) | Y |  | 锌层附着性测试表面锌层脱落率判定 | DB注释(中文) |
| 232 | SPRBCK_CD | VARCHAR2(1) | Y |  | 回弹测试方法 | DB注释(中文) |
| 233 | SPRBCK_DEGR_RSLT | NUMBER | Y |  | 回弹角实绩 | DB注释(中文) |
| 234 | SPRBCK_DEGR_JDG | VARCHAR2(1) | Y |  | 回弹角判定 | DB注释(中文) |
| 235 | SPRBCK_RSLT | NUMBER | Y |  | 回弹测试实绩 | DB注释(中文) |
| 236 | SPRBCK_JDG | VARCHAR2(1) | Y |  | 回弹测试判定 | DB注释(中文) |
| 237 | SPROC_WEAK_RSLT | NUMBER | Y |  | 二次加工脆性测试实绩 | DB注释(中文) |
| 238 | SPROC_WEAK_JDG | VARCHAR2(1) | Y |  | 二次加工脆性测试判定 | DB注释(中文) |
| 239 | BH_RSLT | NUMBER | Y |  | 烘烤硬化值测试实绩 | DB注释(中文) |
| 240 | BH_JDG | VARCHAR2(1) | Y |  | 烘烤硬化值测试判定 | DB注释(中文) |
| 241 | BH_TESTER_CD | VARCHAR2(20) | Y |  | 烘烤硬化试验机代码 | DB注释(中文) |
| 242 | BH_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 烘烤硬化试验人ID | DB注释(中文) |
| 243 | HPT_ADMI_TIME_RSLT | NUMBER | Y |  | 氢扩散达到稳定所需时间实绩 | DB注释(中文) |
| 244 | HPT_ADMI_TIME_JDG | VARCHAR2(1) | Y |  | 氢扩散达到稳定所需时间判定 | DB注释(中文) |
| 245 | HPT_TESTER_CD | VARCHAR2(20) | Y |  | 氢渗透试验机代码 | DB注释(中文) |
| 246 | HPT_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 氢渗透试验人ID | DB注释(中文) |
| 247 | EXT_HOLE_SPCMN_CNT | NUMBER | Y |  | 扩孔测试试样数量 | DB注释(中文) |
| 248 | EXT_HOLE_RATIO_AVG_RSLT | NUMBER | Y |  | 扩孔测试极限扩孔率平均实绩 | DB注释(中文) |
| 249 | EXT_HOLE_RATIO_AVG_JDG | VARCHAR2(1) | Y |  | 扩孔测试极限扩孔率平均判定 | DB注释(中文) |
| 250 | EXT_HOLE_RATIO_EACH_RSLT1 | NUMBER | Y |  | 扩孔测试极限扩孔率单个实绩1 | DB注释(中文) |
| 251 | EXT_HOLE_RATIO_EACH_RSLT2 | NUMBER | Y |  | 扩孔测试极限扩孔率单个实绩2 | DB注释(中文) |
| 252 | EXT_HOLE_RATIO_EACH_RSLT3 | NUMBER | Y |  | 扩孔测试极限扩孔率单个实绩3 | DB注释(中文) |
| 253 | SALT_GRD_MIN_RSLT | NUMBER | Y |  | 缺陷面积实绩 | DB注释(中文) |
| 254 | SALT_GRD_MIN_JDG | VARCHAR2(1) | Y |  | 缺陷面积等级 | DB注释(中文) |
| 255 | QLT_REMARKS | VARCHAR2(300) | Y |  | 质量备注 | DB注释(中文) |
| 256 | PROD_CHEM_ANAL_TY | VARCHAR2(1) | Y |  | 产品成分分析区分 | DB注释(中文) |
| 257 | C_RSLT | VARCHAR2(20) | Y |  | 产品成分C实绩 | DB注释(中文) |
| 258 | SI_RSLT | VARCHAR2(20) | Y |  | 产品成分Si实绩 | DB注释(中文) |
| 259 | MN_RSLT | VARCHAR2(20) | Y |  | 产品成分Mn实绩 | DB注释(中文) |
| 260 | P_RSLT | VARCHAR2(20) | Y |  | 产品成分P实绩 | DB注释(中文) |
| 261 | S_RSLT | VARCHAR2(20) | Y |  | 产品成分S实绩 | DB注释(中文) |
| 262 | SAL_RSLT | VARCHAR2(20) | Y |  | 产品成分Sol_Al实绩 | DB注释(中文) |
| 263 | TAL_RSLT | VARCHAR2(20) | Y |  | 产品成分Tot_Al实绩 | DB注释(中文) |
| 264 | AS_RSLT | VARCHAR2(20) | Y |  | 产品成分As实绩 | DB注释(中文) |
| 265 | BI_RSLT | VARCHAR2(20) | Y |  | 产品成分Bi实绩 | DB注释(中文) |
| 266 | B_RSLT | VARCHAR2(20) | Y |  | 产品成分B实绩 | DB注释(中文) |
| 267 | CA_RSLT | VARCHAR2(20) | Y |  | 产品成分Ca实绩 | DB注释(中文) |
| 268 | CO_RSLT | VARCHAR2(20) | Y |  | 产品成分Co实绩 | DB注释(中文) |
| 269 | CR_RSLT | VARCHAR2(20) | Y |  | 产品成分Cr实绩 | DB注释(中文) |
| 270 | CU_RSLT | VARCHAR2(20) | Y |  | 产品成分Cu实绩 | DB注释(中文) |
| 271 | H_RSLT | VARCHAR2(20) | Y |  | 产品成分H实绩 | DB注释(中文) |
| 272 | MG_RSLT | VARCHAR2(20) | Y |  | 产品成分Mg实绩 | DB注释(中文) |
| 273 | MO_RSLT | VARCHAR2(20) | Y |  | 产品成分Mo实绩 | DB注释(中文) |
| 274 | NB_RSLT | VARCHAR2(20) | Y |  | 产品成分Nb实绩 | DB注释(中文) |
| 275 | NI_RSLT | VARCHAR2(20) | Y |  | 产品成分Ni实绩 | DB注释(中文) |
| 276 | N_RSLT | VARCHAR2(20) | Y |  | 产品成分N实绩 | DB注释(中文) |
| 277 | O_RSLT | VARCHAR2(20) | Y |  | 产品成分O实绩 | DB注释(中文) |
| 278 | PB_RSLT | VARCHAR2(20) | Y |  | 产品成分Pb实绩 | DB注释(中文) |
| 279 | SB_RSLT | VARCHAR2(20) | Y |  | 产品成分Sb实绩 | DB注释(中文) |
| 280 | SN_RSLT | VARCHAR2(20) | Y |  | 产品成分Sn实绩 | DB注释(中文) |
| 281 | TE_RSLT | VARCHAR2(20) | Y |  | 产品成分Te实绩 | DB注释(中文) |
| 282 | TI_RSLT | VARCHAR2(20) | Y |  | 产品成分Ti实绩 | DB注释(中文) |
| 283 | V_RSLT | VARCHAR2(20) | Y |  | 产品成分V实绩 | DB注释(中文) |
| 284 | W_RSLT | VARCHAR2(20) | Y |  | 产品成分W实绩 | DB注释(中文) |
| 285 | ZN_RSLT | VARCHAR2(20) | Y |  | 产品成分Zn实绩 | DB注释(中文) |
| 286 | ZR_RSLT | VARCHAR2(20) | Y |  | 产品成分Zr实绩 | DB注释(中文) |
| 287 | CEQ_RSLT | VARCHAR2(20) | Y |  | 产品成分CEQ计算值 | DB注释(中文) |
| 288 | PCM_RSLT | VARCHAR2(20) | Y |  | 产品成分PCM计算值 | DB注释(中文) |
| 289 | CREQ_RSLT | VARCHAR2(20) | Y |  | 产品成分CrEq计算值 | DB注释(中文) |
| 290 | PROD_CHEM_TESTER_CD | VARCHAR2(20) | Y |  | 产品成分试验机代码 | DB注释(中文) |
| 291 | PROD_CHEM_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 产品成分试验人ID | DB注释(中文) |
| 292 | SPL_OCR_DTM | VARCHAR2(14) | Y |  | 余材发生时间 | DB注释(中文) |
| 293 | TST_COAT_WGT_LOWER_AVG_RSLT | NUMBER | Y |  | 镀锌层质量测试下表面平均实绩 | DB注释(中文) |
| 294 | TST_COAT_WGT_TOT_AVG_RSLT | NUMBER | Y |  | 镀锌层质量测试上下平均 | DB注释(中文) |
| 295 | TST_COAT_WGT_SUM2_RSLT | NUMBER | Y |  | 镀锌层质量测试上下表面和2 | DB注释(中文) |
| 296 | TST_COAT_WGT_SUM3_RSLT | NUMBER | Y |  | 镀锌层质量测试上下表面和3 | DB注释(中文) |
| 297 | COAT_ATTH_RSLT | VARCHAR2(1) | Y |  | 锌层附着性测试表面锌层目视检测结果 | DB注释(中文) |
| 298 | COAT_ATTH_JDG | VARCHAR2(1) | Y |  | 锌层附着性测试表面锌层目视检测结果判定 | DB注释(中文) |
| 299 | NON_METAL_ABCD1_RSLT | NUMBER | Y |  | 非金属夹杂物A+B+C+D1实绩(细) | DB注释(中文) |
| 300 | NON_METAL_ABCD1_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物ABCD1判定(细) | DB注释(中文) |
| 301 | ANTIFNG_WGT_JDG | VARCHAR2(1) | Y |  | 耐指纹膜测试表面重量判定 | DB注释(中文) |
| 302 | PHOSP_ADHE_JDG | VARCHAR2(1) | Y |  | 磷酸盐附着量表面等级 | DB注释(中文) |
| 303 | CHROMATE_ADHE_JDG | VARCHAR2(1) | Y |  | 铬酸盐附着量表面等级 | DB注释(中文) |
| 304 | CHROMFRE_ADHE_JDG | VARCHAR2(1) | Y |  | 无铬附着量表面等级 | DB注释(中文) |
| 305 | ROUGH_RY_RSLT | NUMBER | Y |  | 轮廓最大高度实绩(Ry) | DB注释(中文) |
| 306 | ROUGH_RY_JDG | VARCHAR2(1) | Y |  | 轮廓最大高度判定(Ry) | DB注释(中文) |
| 307 | ROUGH_RZ_RSLT | NUMBER | Y |  | 微观不平度十点高度实绩(Rz) | DB注释(中文) |
| 308 | ROUGH_RZ_JDG | VARCHAR2(1) | Y |  | 微观不平度十点高度判定(Rz) | DB注释(中文) |
| 309 | COAT_ATTH_V_RSLT | VARCHAR2(1) | Y |  | 锌层附着性测试表面锌层目视检测结果 | DB注释(中文) |
| 310 | COAT_ATTH_V_JDG | VARCHAR2(1) | Y |  | 锌层附着性测试表面锌层目视检测结果判定 | DB注释(中文) |
| 311 | COAT_ATTH_T_RSLT | VARCHAR2(1) | Y |  | 锌层附着性测试表面锌层目视检测结果 | DB注释(中文) |
| 312 | COAT_ATTH_T_JDG | VARCHAR2(1) | Y |  | 锌层附着性测试表面锌层目视检测结果判定 | DB注释(中文) |
| 313 | COAT_ATTH_Q_RSLT | VARCHAR2(1) | Y |  | 锌层附着性测试表面锌层目视检测结果 | DB注释(中文) |
| 314 | COAT_ATTH_Q_JDG | VARCHAR2(1) | Y |  | 锌层附着性测试表面锌层目视检测结果判定 | DB注释(中文) |
| 315 | WAVIN_WSA_RSLT | NUMBER | Y |  | 波纹度检测实绩(Wsa) | DB注释(中文) |
| 316 | WAVIN_WSA_JDG | VARCHAR2(1) | Y |  | 波纹度检测判定(Wsa) | DB注释(中文) |
| 317 | WAVIN_WSAMAX_RSLT | NUMBER | Y |  | 波纹度检测最大值实绩(Wsamax) | DB注释(中文) |
| 318 | WAVIN_WSAMAX_JDG | VARCHAR2(1) | Y |  | 波纹度检测最大值判定(Wsamax) | DB注释(中文) |
| 319 | WAVIN_WCA_RSLT | NUMBER | Y |  | 波纹度检测实绩(Wca) | DB注释(中文) |
| 320 | WAVIN_WCA_JDG | VARCHAR2(1) | Y |  | 波纹度检测判定(Wca) | DB注释(中文) |
| 321 | WAVIN_WCAMAX_RSLT | NUMBER | Y |  | 波纹度检测最大值实绩(Wcamax) | DB注释(中文) |
| 322 | WAVIN_WCAMAX_JDG | VARCHAR2(1) | Y |  | 波纹度检测最大值判定(Wcamax) | DB注释(中文) |
| 323 | WAVIN_WA08_RSLT | NUMBER | Y |  | 波纹度检测实绩(Wa08) | DB注释(中文) |
| 324 | WAVIN_WA08_JDG | VARCHAR2(1) | Y |  | 波纹度检测判定(Wa08) | DB注释(中文) |
| 325 | WAVIN_WA08MAX_RSLT | NUMBER | Y |  | 波纹度检测最大值实绩(Wa08max) | DB注释(中文) |
| 326 | WAVIN_WA08MAX_JDG | VARCHAR2(1) | Y |  | 波纹度检测最大值判定(Wa08max) | DB注释(中文) |
| 327 | MGRPHY_GRNSZ_LEVEL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 328 | COAT_ATTH_GRD_MAX_RSLT | VARCHAR2(5) | Y |  | 锌层附着性等级 | SCO_DATA_DIC(D) |
| 329 | COAT_ATTH_GRD_MAX_JDG | VARCHAR2(1) | Y |  | 锌层附着性判定结果 | SCO_DATA_DIC(D) |
| 330 | HARD_RSLT4 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 331 | HARD_RSLT5 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 332 | HARD_RSLT6 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 333 | HARD_RSLT7 | NUMBER | Y |  | 硬度测试实绩7 | DB注释(中文) |
| 334 | HARD_RSLT8 | NUMBER | Y |  | 硬度测试实绩8 | DB注释(中文) |
| 335 | HARD_RSLT9 | NUMBER | Y |  | 硬度测试实绩9 | DB注释(中文) |
| 336 | TSL_YP_REH_RSLT | VARCHAR2(10) | Y |  | 拉伸测试屈服强度平台标志 | DB注释(中文) |
| 337 | C3_WGT_UPPER_RSLT | NUMBER | Y |  | 三价铬钝化膜重量上表面实绩 | DB注释(中文) |
| 338 | C3_WGT_UPPER_JDG | VARCHAR2(1) | Y |  | 三价铬钝化膜重量上表面等级 | DB注释(中文) |
| 339 | C3_WGT_LOWER_RSLT | NUMBER | Y |  | 三价铬钝化膜重量下表面实绩 | DB注释(中文) |
| 340 | C3_WGT_LOWER_JDG | VARCHAR2(1) | Y |  | 三价铬钝化膜重量下表面等级 | DB注释(中文) |
| 341 | C6_WGT_UPPER_RSLT | NUMBER | Y |  | 六价铬钝化膜重量上表面实绩 | DB注释(中文) |
| 342 | C6_WGT_UPPER_JDG | VARCHAR2(1) | Y |  | 六价铬钝化膜重量上表面等级 | DB注释(中文) |
| 343 | C6_WGT_LOWER_RSLT | NUMBER | Y |  | 六价铬钝化膜重量下表面实绩 | DB注释(中文) |
| 344 | C6_WGT_LOWER_JDG | VARCHAR2(1) | Y |  | 六价铬钝化膜重量下表面等级 | DB注释(中文) |
| 345 | AF3_WGT_UPPER_RSLT | NUMBER | Y |  | 有铬耐指纹钝化膜重量上表面实绩 | DB注释(中文) |
| 346 | AF3_WGT_UPPER_JDG | VARCHAR2(1) | Y |  | 有铬耐指纹钝化膜重量上表面等级 | DB注释(中文) |
| 347 | AF3_WGT_LOWER_RSLT | NUMBER | Y |  | 有铬耐指纹钝化膜重量下表面实绩 | DB注释(中文) |
| 348 | AF3_WGT_LOWER_JDG | VARCHAR2(1) | Y |  | 有铬耐指纹钝化膜重量下表面等级 | DB注释(中文) |
| 349 | SL6_WGT_UPPER_RSLT | NUMBER | Y |  | 自润滑膜重量上表面实绩 | DB注释(中文) |
| 350 | SL6_WGT_UPPER_JDG | VARCHAR2(1) | Y |  | 自润滑膜重量上表面等级 | DB注释(中文) |
| 351 | SL6_WGT_LOWER_RSLT | NUMBER | Y |  | 自润滑膜重量下表面实绩 | DB注释(中文) |
| 352 | SL6_WGT_LOWER_JDG | VARCHAR2(1) | Y |  | 自润滑膜重量下表面等级 | DB注释(中文) |
| 353 | HCR_WGT_UPPER_RSLT | NUMBER | Y |  | 高耐蚀膜重量上表面实绩 | DB注释(中文) |
| 354 | HCR_WGT_UPPER_JDG | VARCHAR2(1) | Y |  | 高耐蚀膜重量上表面等级 | DB注释(中文) |
| 355 | HCR_WGT_LOWER_RSLT | NUMBER | Y |  | 高耐蚀膜重量下表面实绩 | DB注释(中文) |
| 356 | HCR_WGT_LOWER_JDG | VARCHAR2(1) | Y |  | 高耐蚀膜重量下表面等级 | DB注释(中文) |
| 357 | HSL_WGT_UPPER_RSLT | NUMBER | Y |  | 高润滑膜重量上表面实绩 | DB注释(中文) |
| 358 | HSL_WGT_UPPER_JDG | VARCHAR2(1) | Y |  | 高润滑膜重量上表面等级 | DB注释(中文) |
| 359 | HSL_WGT_LOWER_RSLT | NUMBER | Y |  | 高润滑膜重量下表面实绩 | DB注释(中文) |
| 360 | HSL_WGT_LOWER_JDG | VARCHAR2(1) | Y |  | 高润滑膜重量下表面等级 | DB注释(中文) |
| 361 | PHOSP_ADHE_UPPER_RSLT1 | NUMBER | Y |  | 磷化膜重量上表面实绩1 | DB注释(中文) |
| 362 | PHOSP_ADHE_UPPER_RSLT2 | NUMBER | Y |  | 磷化膜重量上表面实绩2 | DB注释(中文) |
| 363 | PHOSP_ADHE_UPPER_RSLT3 | NUMBER | Y |  | 磷化膜重量上表面实绩3 | DB注释(中文) |
| 364 | PHOSP_ADHE_LOWER_RSLT1 | NUMBER | Y |  | 磷化膜重量下表面实绩1 | DB注释(中文) |
| 365 | PHOSP_ADHE_LOWER_RSLT2 | NUMBER | Y |  | 磷化膜重量下表面实绩2 | DB注释(中文) |
| 366 | PHOSP_ADHE_LOWER_RSLT3 | NUMBER | Y |  | 磷化膜重量下表面实绩3 | DB注释(中文) |
| 367 | CHROMATE_ADHE_UPPER_RSLT1 | NUMBER | Y |  | 无铬钝化膜上表面实绩1 | DB注释(中文) |
| 368 | CHROMATE_ADHE_UPPER_RSLT2 | NUMBER | Y |  | 无铬钝化膜上表面实绩2 | DB注释(中文) |
| 369 | CHROMATE_ADHE_UPPER_RSLT3 | NUMBER | Y |  | 无铬钝化膜上表面实绩3 | DB注释(中文) |
| 370 | CHROMATE_ADHE_LOWER_RSLT1 | NUMBER | Y |  | 无铬钝化膜下表面实绩1 | DB注释(中文) |
| 371 | CHROMATE_ADHE_LOWER_RSLT2 | NUMBER | Y |  | 无铬钝化膜下表面实绩2 | DB注释(中文) |
| 372 | CHROMATE_ADHE_LOWER_RSLT3 | NUMBER | Y |  | 无铬钝化膜下表面实绩3 | DB注释(中文) |
| 373 | ANTIFNG_WGT_UPPER_RSLT1 | NUMBER | Y |  | 无铬耐指纹钝化膜上表面重量实绩1 | DB注释(中文) |
| 374 | ANTIFNG_WGT_UPPER_RSLT2 | NUMBER | Y |  | 无铬耐指纹钝化膜上表面重量实绩2 | DB注释(中文) |
| 375 | ANTIFNG_WGT_UPPER_RSLT3 | NUMBER | Y |  | 无铬耐指纹钝化膜上表面重量实绩3 | DB注释(中文) |
| 376 | ANTIFNG_WGT_LOWER_RSLT1 | NUMBER | Y |  | 无铬耐指纹钝化膜下表面重量实绩1 | DB注释(中文) |
| 377 | ANTIFNG_WGT_LOWER_RSLT2 | NUMBER | Y |  | 无铬耐指纹钝化膜下表面重量实绩2 | DB注释(中文) |
| 378 | ANTIFNG_WGT_LOWER_RSLT3 | NUMBER | Y |  | 无铬耐指纹钝化膜下表面重量实绩3 | DB注释(中文) |
| 379 | CHROMFRE_ADHE_UPPER_RSLT1 | NUMBER | Y |  | 无铬自润滑膜上表面实绩1 | DB注释(中文) |
| 380 | CHROMFRE_ADHE_UPPER_RSLT2 | NUMBER | Y |  | 无铬自润滑膜上表面实绩2 | DB注释(中文) |
| 381 | CHROMFRE_ADHE_UPPER_RSLT3 | NUMBER | Y |  | 无铬自润滑膜上表面实绩3 | DB注释(中文) |
| 382 | CHROMFRE_ADHE_LOWER_RSLT1 | NUMBER | Y |  | 无铬自润滑膜下表面实绩1 | DB注释(中文) |
| 383 | CHROMFRE_ADHE_LOWER_RSLT2 | NUMBER | Y |  | 无铬自润滑膜下表面实绩2 | DB注释(中文) |
| 384 | CHROMFRE_ADHE_LOWER_RSLT3 | NUMBER | Y |  | 无铬自润滑膜下表面实绩3 | DB注释(中文) |
| 385 | C3_WGT_UPPER_RSLT1 | NUMBER | Y |  | 三价铬钝化膜重量上表面实绩1 | DB注释(中文) |
| 386 | C3_WGT_UPPER_RSLT2 | NUMBER | Y |  | 三价铬钝化膜重量上表面实绩2 | DB注释(中文) |
| 387 | C3_WGT_UPPER_RSLT3 | NUMBER | Y |  | 三价铬钝化膜重量上表面实绩3 | DB注释(中文) |
| 388 | C3_WGT_LOWER_RSLT1 | NUMBER | Y |  | 三价铬钝化膜重量下表面实绩1 | DB注释(中文) |
| 389 | C3_WGT_LOWER_RSLT2 | NUMBER | Y |  | 三价铬钝化膜重量下表面实绩2 | DB注释(中文) |
| 390 | C3_WGT_LOWER_RSLT3 | NUMBER | Y |  | 三价铬钝化膜重量下表面实绩3 | DB注释(中文) |
| 391 | C6_WGT_UPPER_RSLT1 | NUMBER | Y |  | 六价铬钝化膜重量上表面实绩1 | DB注释(中文) |
| 392 | C6_WGT_UPPER_RSLT2 | NUMBER | Y |  | 六价铬钝化膜重量上表面实绩2 | DB注释(中文) |
| 393 | C6_WGT_UPPER_RSLT3 | NUMBER | Y |  | 六价铬钝化膜重量上表面实绩3 | DB注释(中文) |
| 394 | C6_WGT_LOWER_RSLT1 | NUMBER | Y |  | 六价铬钝化膜重量下表面实绩1 | DB注释(中文) |
| 395 | C6_WGT_LOWER_RSLT2 | NUMBER | Y |  | 六价铬钝化膜重量下表面实绩2 | DB注释(中文) |
| 396 | C6_WGT_LOWER_RSLT3 | NUMBER | Y |  | 六价铬钝化膜重量下表面实绩3 | DB注释(中文) |
| 397 | AF3_WGT_UPPER_RSLT1 | NUMBER | Y |  | 有铬耐指纹钝化膜重量上表面实绩1 | DB注释(中文) |
| 398 | AF3_WGT_UPPER_RSLT2 | NUMBER | Y |  | 有铬耐指纹钝化膜重量上表面实绩2 | DB注释(中文) |
| 399 | AF3_WGT_UPPER_RSLT3 | NUMBER | Y |  | 有铬耐指纹钝化膜重量上表面实绩3 | DB注释(中文) |
| 400 | AF3_WGT_LOWER_RSLT1 | NUMBER | Y |  | 有铬耐指纹钝化膜重量下表面实绩1 | DB注释(中文) |
| 401 | AF3_WGT_LOWER_RSLT2 | NUMBER | Y |  | 有铬耐指纹钝化膜重量下表面实绩2 | DB注释(中文) |
| 402 | AF3_WGT_LOWER_RSLT3 | NUMBER | Y |  | 有铬耐指纹钝化膜重量下表面实绩3 | DB注释(中文) |
| 403 | SL6_WGT_UPPER_RSLT1 | NUMBER | Y |  | 自润滑膜重量上表面实绩1 | DB注释(中文) |
| 404 | SL6_WGT_UPPER_RSLT2 | NUMBER | Y |  | 自润滑膜重量上表面实绩2 | DB注释(中文) |
| 405 | SL6_WGT_UPPER_RSLT3 | NUMBER | Y |  | 自润滑膜重量上表面实绩3 | DB注释(中文) |
| 406 | SL6_WGT_LOWER_RSLT1 | NUMBER | Y |  | 自润滑膜重量下表面实绩1 | DB注释(中文) |
| 407 | SL6_WGT_LOWER_RSLT2 | NUMBER | Y |  | 自润滑膜重量下表面实绩2 | DB注释(中文) |
| 408 | SL6_WGT_LOWER_RSLT3 | NUMBER | Y |  | 自润滑膜重量下表面实绩3 | DB注释(中文) |
| 409 | HCR_WGT_UPPER_RSLT1 | NUMBER | Y |  | 高耐蚀膜重量上表面实绩1 | DB注释(中文) |
| 410 | HCR_WGT_UPPER_RSLT2 | NUMBER | Y |  | 高耐蚀膜重量上表面实绩2 | DB注释(中文) |
| 411 | HCR_WGT_UPPER_RSLT3 | NUMBER | Y |  | 高耐蚀膜重量上表面实绩3 | DB注释(中文) |
| 412 | HCR_WGT_LOWER_RSLT1 | NUMBER | Y |  | 高耐蚀膜重量下表面实绩1 | DB注释(中文) |
| 413 | HCR_WGT_LOWER_RSLT2 | NUMBER | Y |  | 高耐蚀膜重量下表面实绩2 | DB注释(中文) |
| 414 | HCR_WGT_LOWER_RSLT3 | NUMBER | Y |  | 高耐蚀膜重量下表面实绩3 | DB注释(中文) |
| 415 | HSL_WGT_UPPER_RSLT1 | NUMBER | Y |  | 高润滑膜重量上表面实绩1 | DB注释(中文) |
| 416 | HSL_WGT_UPPER_RSLT2 | NUMBER | Y |  | 高润滑膜重量上表面实绩2 | DB注释(中文) |
| 417 | HSL_WGT_UPPER_RSLT3 | NUMBER | Y |  | 高润滑膜重量上表面实绩3 | DB注释(中文) |
| 418 | HSL_WGT_LOWER_RSLT1 | NUMBER | Y |  | 高润滑膜重量下表面实绩1 | DB注释(中文) |
| 419 | HSL_WGT_LOWER_RSLT2 | NUMBER | Y |  | 高润滑膜重量下表面实绩2 | DB注释(中文) |
| 420 | HSL_WGT_LOWER_RSLT3 | NUMBER | Y |  | 高润滑膜重量下表面实绩3 | DB注释(中文) |
| 421 | TSL_YP_REH_JDG | VARCHAR2(1) | Y |  | 拉伸测试屈服强度平台标志判定 | DB注释(中文) |

### SQM_MTC_CHEM

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=35｜被读 21 过程 / 被写 7 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：570　**主键**：MTC_NO、MTC_CHG_CNT、SMS_PROD_CHEM_TY、CHEM_TEST_NO　**语义覆盖**：163/163

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | MTC_NO | VARCHAR2(11) | N | ✓ | 质量保证书编号 | DB注释(中文) |
| 9 | MTC_CHG_CNT | NUMBER | N | ✓ | 质量保证书变更回数 | DB注释(中文) |
| 10 | SMS_PROD_CHEM_TY | VARCHAR2(1) | N | ✓ | 炼钢产品成分分类 | DB注释(中文) |
| 11 | CHEM_TEST_NO | VARCHAR2(14) | N | ✓ | 成分试验编号 | DB注释(中文) |
| 12 | C_GRT_CD | VARCHAR2(1) | Y |  | C保证代码 | DB注释(中文) |
| 13 | SI_GRT_CD | VARCHAR2(1) | Y |  | SI保证代码 | DB注释(中文) |
| 14 | SI_RSLT2 | NUMBER | Y |  | 实绩Si | DB注释(中文) |
| 15 | MN_GRT_CD | VARCHAR2(1) | Y |  | MN保证代码 | DB注释(中文) |
| 16 | MN_RSLT2 | NUMBER | Y |  | 实绩Mn | DB注释(中文) |
| 17 | P_GRT_CD | VARCHAR2(1) | Y |  | P保证代码 | DB注释(中文) |
| 18 | P_RSLT2 | NUMBER | Y |  | 实绩P | DB注释(中文) |
| 19 | S_GRT_CD | VARCHAR2(1) | Y |  | S保证代码 | DB注释(中文) |
| 20 | S_RSLT2 | NUMBER | Y |  | 实绩S | DB注释(中文) |
| 21 | TOT_AL_GRT_CD | VARCHAR2(1) | Y |  | TOT_AL保证代码 | DB注释(中文) |
| 22 | TOT_AL_RSLT2 | NUMBER | Y |  | 实绩Tot_Al | DB注释(中文) |
| 23 | SOL_AL_GRT_CD | VARCHAR2(1) | Y |  | SOL_AL保证代码 | DB注释(中文) |
| 24 | SOL_AL_RSLT2 | NUMBER | Y |  | 实绩Sol_Al | DB注释(中文) |
| 25 | V_GRT_CD | VARCHAR2(1) | Y |  | V保证代码 | DB注释(中文) |
| 26 | V_RSLT2 | NUMBER | Y |  | 实绩V | DB注释(中文) |
| 27 | N_GRT_CD | VARCHAR2(1) | Y |  | N保证代码 | DB注释(中文) |
| 28 | N_RSLT2 | NUMBER | Y |  | 实绩N | DB注释(中文) |
| 29 | CU_GRT_CD | VARCHAR2(1) | Y |  | CU保证代码 | DB注释(中文) |
| 30 | CU_RSLT2 | NUMBER | Y |  | 实绩Cu | DB注释(中文) |
| 31 | TI_GRT_CD | VARCHAR2(1) | Y |  | TI保证代码 | DB注释(中文) |
| 32 | TI_RSLT2 | NUMBER | Y |  | 实绩Ti | DB注释(中文) |
| 33 | NI_GRT_CD | VARCHAR2(1) | Y |  | NI保证代码 | DB注释(中文) |
| 34 | NI_RSLT2 | NUMBER | Y |  | 实绩Ni | DB注释(中文) |
| 35 | NB_GRT_CD | VARCHAR2(1) | Y |  | NB保证代码 | DB注释(中文) |
| 36 | NB_RSLT2 | NUMBER | Y |  | 实绩Nb | DB注释(中文) |
| 37 | SN_GRT_CD | VARCHAR2(1) | Y |  | SN保证代码 | DB注释(中文) |
| 38 | SN_RSLT | VARCHAR2(20) | Y |  | 实绩SN | DB注释(中文) |
| 39 | MO_GRT_CD | VARCHAR2(1) | Y |  | MO保证代码 | DB注释(中文) |
| 40 | MO_RSLT2 | NUMBER | Y |  | 实绩Mo | DB注释(中文) |
| 41 | CR_GRT_CD | VARCHAR2(1) | Y |  | CR保证代码 | DB注释(中文) |
| 42 | CR_RSLT2 | NUMBER | Y |  | 实绩Cr | DB注释(中文) |
| 43 | H_GRT_CD | VARCHAR2(1) | Y |  | H保证代码 | DB注释(中文) |
| 44 | H_RSLT | VARCHAR2(20) | Y |  | 实绩H | DB注释(中文) |
| 45 | O_GRT_CD | VARCHAR2(1) | Y |  | O保证代码 | DB注释(中文) |
| 46 | O_RSLT2 | NUMBER | Y |  | 实绩O | DB注释(中文) |
| 47 | CEQ_GRT_CD | VARCHAR2(1) | Y |  | CEQ保证代码 | DB注释(中文) |
| 48 | CEQ_TYPE | VARCHAR2(1) | Y |  | CEQ式 | DB注释(中文) |
| 49 | CEQ_RSLT2 | NUMBER | Y |  | 实绩CEQ | DB注释(中文) |
| 50 | PCM_GRT_CD | VARCHAR2(1) | Y |  | PCM保证代码 | DB注释(中文) |
| 51 | PCM_FML | VARCHAR2(2) | Y |  | PCM式 | DB注释(中文) |
| 52 | PCM_RSLT2 | NUMBER | Y |  | 实绩PCM | DB注释(中文) |
| 53 | CHEMI1_GRT_CD | VARCHAR2(1) | Y |  | 复合元素1保证代码 | DB注释(中文) |
| 54 | CHEMI1_CD | VARCHAR2(2) | Y |  | 复合元素1代码 | DB注释(中文) |
| 55 | CHEMI1_FML | VARCHAR2(2) | Y |  | 复合元素1式 | DB注释(中文) |
| 56 | CHEMI1_RSLT | VARCHAR2(20) | Y |  | 实绩复合元素1值 | DB注释(中文) |
| 57 | CHEMI2_GRT_CD | VARCHAR2(1) | Y |  | 复合元素2保证代码 | DB注释(中文) |
| 58 | CHEMI2_CD | VARCHAR2(2) | Y |  | 复合元素2代码 | DB注释(中文) |
| 59 | CHEMI2_FML | VARCHAR2(2) | Y |  | 复合元素2式 | DB注释(中文) |
| 60 | CHEMI2_RSLT | VARCHAR2(20) | Y |  | 实绩复合元素2值 | DB注释(中文) |
| 61 | QLT_REMARK | VARCHAR2(600) | Y |  | 质量Remarks | DB注释(中文) |
| 62 | B_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 63 | B_RSLT2 | NUMBER | Y |  | 实绩B | DB注释(中文) |
| 64 | RE_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 65 | RE_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 66 | W_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 67 | W_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 68 | ZR_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 69 | ZR_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 70 | PB_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 71 | PB_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 72 | AS_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 73 | AS_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 74 | CO_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 75 | CO_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 76 | CA_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 77 | CA_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 78 | MG_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 79 | MG_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 80 | TE_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 81 | TE_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 82 | BI_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 83 | BI_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 84 | SB_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 85 | SB_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 86 | ZN_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 87 | ZN_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 88 | CFI_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 89 | CFI_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 90 | CFJ_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 91 | CFJ_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 92 | CFX_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 93 | CFX_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 94 | PSR_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 95 | PSR_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 96 | YSB1_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 97 | YSB1_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 98 | YSB2_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 99 | YSB2_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 100 | YSB3_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 101 | YSB3_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 102 | YSB4_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 103 | YSB4_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 104 | YSB5_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 105 | YSB5_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 106 | YSB6_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 107 | YSB6_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 108 | YSB7_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 109 | YSB7_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 110 | CSOL_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 111 | CSOL_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 112 | WLYS1_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 113 | WLYS1_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 114 | WLYS2_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 115 | WLYS2_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 116 | WLYS3_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 117 | WLYS3_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 118 | WLYS4_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 119 | WLYS4_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 120 | WLYS5_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 121 | WLYS5_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 122 | WLYS6_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 123 | WLYS6_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 124 | CEQ1_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 125 | CEQ1_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 126 | CEQEXP_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 127 | CEQEXP_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 128 | CEVIIW_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 129 | CEVIIW_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 130 | CET_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 131 | CET_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 132 | CEQAWS_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 133 | CEQAWS_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 134 | CEQJIS_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 135 | CEQJIS_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 136 | WLYS7_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 137 | WLYS7_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 138 | WLYS8_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 139 | WLYS8_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 140 | WLYS9_GRT_CD | VARCHAR2(1) | Y |  | B保证代码 | DB注释(中文) |
| 141 | WLYS9_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 142 | C_RSLT2 | NUMBER | Y |  | 实绩C | DB注释(中文) |
| 143 | C_RSLT | VARCHAR2(20) | Y |  | 实绩C | DB注释(中文) |
| 144 | SI_RSLT | VARCHAR2(20) | Y |  | 实绩Si | DB注释(中文) |
| 145 | MN_RSLT | VARCHAR2(20) | Y |  | 实绩Mn | DB注释(中文) |
| 146 | P_RSLT | VARCHAR2(20) | Y |  | 实绩P | DB注释(中文) |
| 147 | S_RSLT | VARCHAR2(20) | Y |  | 实绩S | DB注释(中文) |
| 148 | TOT_AL_RSLT | VARCHAR2(20) | Y |  | 实绩TOT | DB注释(中文) |
| 149 | SOL_AL_RSLT | VARCHAR2(20) | Y |  | 实绩SOL | DB注释(中文) |
| 150 | V_RSLT | VARCHAR2(20) | Y |  | 实绩V | DB注释(中文) |
| 151 | N_RSLT | VARCHAR2(20) | Y |  | 实绩N | DB注释(中文) |
| 152 | CU_RSLT | VARCHAR2(20) | Y |  | 实绩CU | DB注释(中文) |
| 153 | TI_RSLT | VARCHAR2(20) | Y |  | 实绩TI | DB注释(中文) |
| 154 | NI_RSLT | VARCHAR2(20) | Y |  | 实绩NI | DB注释(中文) |
| 155 | NB_RSLT | VARCHAR2(20) | Y |  | 实绩NB | DB注释(中文) |
| 156 | MO_RSLT | VARCHAR2(20) | Y |  | 实绩MO | DB注释(中文) |
| 157 | CR_RSLT | VARCHAR2(20) | Y |  | 实绩CR | DB注释(中文) |
| 158 | O_RSLT | VARCHAR2(20) | Y |  | 实绩O | DB注释(中文) |
| 159 | CEQ_RSLT | VARCHAR2(20) | Y |  | 实绩CEQ | DB注释(中文) |
| 160 | PCM_RSLT | VARCHAR2(20) | Y |  | 实绩PCM | DB注释(中文) |
| 161 | B_RSLT | VARCHAR2(20) | Y |  | 实绩B | DB注释(中文) |
| 162 | WLYS10_RSLT | VARCHAR2(20) | Y |  | 实绩WLYS10 | DB注释(中文) |
| 163 | TFE_RSLT | VARCHAR2(20) | Y |  | 实绩Tfe | DB注释(中文) |

### SYD_DISP_ORD_DETAIL

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=34｜被读 20 过程 / 被写 7 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：14922　**主键**：DORD_NO、ORD_NO、ORD_LN、DORD_LN_NO　**语义覆盖**：21/26

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | SCO_DATA_DIC(D) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | SCO_DATA_DIC(D) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | SCO_DATA_DIC(D) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated UserID | SCO_DATA_DIC(D) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated ObjectID | SCO_DATA_DIC(D) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Date Time | SCO_DATA_DIC(D) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | SCO_DATA_DIC(D) |
| 8 | DORD_NO | VARCHAR2(50) | N | ✓ | Dispatch Order No | SCO_DATA_DIC(D) |
| 9 | ORD_NO | VARCHAR2(50) | N | ✓ | Order No | SCO_DATA_DIC(D) |
| 10 | ORD_LN | VARCHAR2(50) | N | ✓ |  | 空 |
| 11 | SALES_PROD_ITEM_CD | VARCHAR2(40) | Y |  | 코일 제품 ERP ITEM | SCO_DATA_DIC(D) |
| 12 | SPEC_CD | VARCHAR2(50) | Y |  | Order Specification | SCO_DATA_DIC(D) |
| 13 | PROD_IN_DIA | NUMBER | Y |  | 直径 | DB注释(中文) |
| 14 | PROD_THK | NUMBER | Y |  | 厚度 /高度 | DB注释(中文) |
| 15 | PROD_WTH | NUMBER | Y |  | 宽度 | DB注释(中文) |
| 16 | PROD_LTH | NUMBER | Y |  | Product Length | SCO_DATA_DIC(D) |
| 17 | PROD_FTHK | NUMBER | Y |  | 腹板厚度 | DB注释(中文) |
| 18 | PROD_YTHK | NUMBER | Y |  | 翼缘厚度 | DB注释(中文) |
| 19 | PROD_NET_WGT | NUMBER | Y |  |  | 空 |
| 20 | DORD_TOT_PCS | NUMBER | Y |  | Dispatch Total Pieces | SCO_DATA_DIC(D) |
| 21 | DORD_TOT_WGT | NUMBER | Y |  | Dispatch Total Weight | SCO_DATA_DIC(D) |
| 22 | DORD_SIZE | VARCHAR2(50) | Y |  |  | 空 |
| 23 | DORD_LN_NO | VARCHAR2(50) | N | ✓ | 提单明细号 | DB注释(中文) |
| 24 | PROD_LTH_MIN | NUMBER | Y |  |  | 空 |
| 25 | PROD_LTH_MAX | NUMBER | Y |  |  | 空 |
| 26 | WGT_DCN_MTH_CD | VARCHAR2(20) | Y |  | 计重方式 | DB注释(中文) |

### SQM_STDB_NATL_COM

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=33｜被读 31 过程 / 被写 1 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：29　**主键**：QLT_STD_SEQ　**语义覆盖**：32/32

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 修改人 | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | 修改时间 | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | QLT_STD_SEQ | NUMBER | N | ✓ | 质量标准序列号 | DB注释(中文) |
| 9 | PROD_GRP | VARCHAR2(2) | N |  | 品种代码 | DB注释(中文) |
| 10 | SPEC_CD | VARCHAR2(50) | N |  | 国家标准牌号 | DB注释(中文) |
| 11 | NATL_SPEC_YEAR | VARCHAR2(4) | N |  | 国家标准年度 | DB注释(中文) |
| 12 | NATL_SPEC_ORG_CD | VARCHAR2(5) | N |  | 国家标准机关简称 | DB注释(中文) |
| 13 | NATL_SPEC_NO | VARCHAR2(40) | N |  | 国家标准编号 | DB注释(中文) |
| 14 | STD_STLGRD | VARCHAR2(20) | N |  | 牌号 | DB注释(中文) |
| 15 | NATL_SPEC_FULL_NM | VARCHAR2(60) | N |  | 国家标准牌号全体名称 | DB注释(中文) |
| 16 | NATL_TOL_SPEC_SZSHP_NO | VARCHAR2(50) | N |  | 尺寸形状允许偏差国家标准编号 | DB注释(中文) |
| 17 | NATL_TOL_SPEC_PRDCHEM_NO | VARCHAR2(50) | Y |  | 产品成分国家标准编号 | DB注释(中文) |
| 18 | TSL_AIM | VARCHAR2(4) | Y |  | TS_目标值 | DB注释(中文) |
| 19 | TEMP_GRADE_CD | VARCHAR2(2) | Y |  | 调制分类 | DB注释(中文) |
| 20 | COAT_PROD_THK_TY | VARCHAR2(1) | Y |  | 镀锌产品厚度分类 | DB注释(中文) |
| 21 | SPECIFIC_GRAVITY | NUMBER | N |  | 比重 | DB注释(中文) |
| 22 | SPEC_CD_DESC | VARCHAR2(300) | Y |  | 国家标准牌号说明 | DB注释(中文) |
| 23 | SPEC_CD_ENG_DESC | VARCHAR2(300) | Y |  | 国家标准牌号英文说明 | DB注释(中文) |
| 24 | USE_YN | VARCHAR2(1) | Y |  | 是否使用 | DB注释(中文) |
| 25 | QLT_REMARKS | VARCHAR2(300) | Y |  | 质量备注 | DB注释(中文) |
| 26 | SPEC_CD_INTER | VARCHAR2(50) | Y |  | 内部牌号 | DB注释(中文) |
| 27 | STEEL_TYPE | VARCHAR2(100) | Y |  | 钢种大类 | DB注释(中文) |
| 28 | VARIETY_TYPE | VARCHAR2(100) | Y |  | 品种大类 | DB注释(中文) |
| 29 | SPEC_CD_NM | VARCHAR2(300) | Y |  | 标准名称 | DB注释(中文) |
| 30 | SLAB_GRAVITY | NUMBER | Y |  | 比重 | DB注释(中文) |
| 31 | PROD_NM_CN | VARCHAR2(100) | Y |  | 产品名称中文 | DB注释(中文) |
| 32 | PROD_NM_EN | VARCHAR2(100) | Y |  | 产品名称英文 | DB注释(中文) |

### SCH_PLAN_SLAB

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=33｜被读 25 过程 / 被写 4 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：119743　**主键**：PLAN_SLAB_NO　**语义覆盖**：97/100

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | PLAN_SLAB_NO | VARCHAR2(13) | N | ✓ | Plan Slab No | DB注释(非中文) |
| 9 | PLAN_HEAT_NO | VARCHAR2(8) | Y |  | Spec Heat No | DB注释(非中文) |
| 10 | SPEC_SLAB_NO | VARCHAR2(13) | Y |  | SPEC Slab NO | DB注释(非中文) |
| 11 | SPEC_HEAT_NO | VARCHAR2(8) | Y |  | SPEC Heat NO | DB注释(非中文) |
| 12 | INST_HEAT_NO | VARCHAR2(9) | Y |  | Instruction Heat No | DB注释(非中文) |
| 13 | INST_SLAB_NO | VARCHAR2(12) | Y |  | Instruction Slab NO | DB注释(非中文) |
| 14 | PLAN_SLAB_STS | VARCHAR2(3) | Y |  | Plan Slab Status | DB注释(非中文) |
| 15 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  | Steel Grade | DB注释(非中文) |
| 16 | SPEC_CD | VARCHAR2(50) | Y |  | Specification Code | DB注释(非中文) |
| 17 | PLAN_SLAB_THK | NUMBER | Y |  | Plan Slab Thickness | DB注释(非中文) |
| 18 | PLAN_SLAB_WTH | NUMBER | Y |  | Plan Slab Width | DB注释(非中文) |
| 19 | PLAN_SLAB_STA_WTH | NUMBER | Y |  | Plan Slab Start Width | DB注释(非中文) |
| 20 | PLAN_SLAB_END_WTH | NUMBER | Y |  | Plan Slab End Width | DB注释(非中文) |
| 21 | PLAN_SLAB_LTH | NUMBER | Y |  | Plan Slab Length | DB注释(非中文) |
| 22 | PLAN_SLAB_LTH_MAX | NUMBER | Y |  | Plan Slab Length Max. | DB注释(非中文) |
| 23 | PLAN_SLAB_LTH_MIN | NUMBER | Y |  | Plan Slab Length MIn. | DB注释(非中文) |
| 24 | PLAN_SLAB_WGT | NUMBER | Y |  | Plan Slab Weight | DB注释(非中文) |
| 25 | PLAN_SLAB_WGT_MAX | NUMBER | Y |  | Plan Slab Weight Max. | DB注释(非中文) |
| 26 | PLAN_SLAB_WGT_MIN | NUMBER | Y |  | Plan Slab Weight Min. | DB注释(非中文) |
| 27 | SUBDIV_TY | VARCHAR2(1) | Y |  | SubDivide Type | DB注释(非中文) |
| 28 | PROD_THK | NUMBER | Y |  | Product Thickness | DB注释(非中文) |
| 29 | PROD_WTH | NUMBER | Y |  | Product Width | DB注释(非中文) |
| 30 | PROD_LTH | NUMBER | Y |  | Product Length | DB注释(非中文) |
| 31 | PROD_WGT | NUMBER | Y |  | Product Weight | DB注释(非中文) |
| 32 | PROD_PCS | NUMBER | Y |  | Product Pieces | DB注释(非中文) |
| 33 | PLAN_ORD_FL | VARCHAR2(1) | Y |  | Plan Order Flag | DB注释(非中文) |
| 34 | ORD_USAGE | VARCHAR2(4) | Y |  | Order usage | DB注释(非中文) |
| 35 | ORD_NO | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 36 | ORD_LN | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 37 | ORD_NO1 | VARCHAR2(10) | Y |  | Order No1 | DB注释(非中文) |
| 38 | ORD_LN1 | VARCHAR2(3) | Y |  | Order Line1 | DB注释(非中文) |
| 39 | SLAB_DGN_WGT1 | NUMBER | Y |  | Slab Design Weight1 | DB注释(非中文) |
| 40 | SLAB_DGN_LTH1 | NUMBER | Y |  | SlabDesign Length1 | DB注释(非中文) |
| 41 | ORD_NO2 | VARCHAR2(10) | Y |  | Order No2 | DB注释(非中文) |
| 42 | ORD_LN2 | VARCHAR2(3) | Y |  | Order Line2 | DB注释(非中文) |
| 43 | SLAB_DGN_WGT2 | NUMBER | Y |  | Slab Design Weight2 | DB注释(非中文) |
| 44 | SLAB_DGN_LTH2 | NUMBER | Y |  | SlabDesign Length2 | DB注释(非中文) |
| 45 | ORD_NO3 | VARCHAR2(10) | Y |  | Order No3 | DB注释(非中文) |
| 46 | ORD_LN3 | VARCHAR2(3) | Y |  | Order Line3 | DB注释(非中文) |
| 47 | SLAB_DGN_WGT3 | NUMBER | Y |  | Slab Design Weight3 | DB注释(非中文) |
| 48 | SLAB_DGN_LTH3 | NUMBER | Y |  | SlabDesign Length3 | DB注释(非中文) |
| 49 | SCARF_TY | VARCHAR2(6) | Y |  | Scarfing Type | DB注释(非中文) |
| 50 | UST_YN | VARCHAR2(1) | Y |  | UST Y/N | DB注释(非中文) |
| 51 | SMPING_TY | VARCHAR2(1) | Y |  | Simpling Type | DB注释(非中文) |
| 52 | TAPER_TY | VARCHAR2(1) | Y |  | Taper Type | DB注释(非中文) |
| 53 | STR_NO | VARCHAR2(1) | Y |  | Strand No | DB注释(非中文) |
| 54 | MIXED_TY | VARCHAR2(1) | Y |  | Mixed Type | DB注释(非中文) |
| 55 | COOLING_TY | VARCHAR2(1) | Y |  | Cooling Type | DB注释(非中文) |
| 56 | HCR_FL | VARCHAR2(1) | Y |  | HCR Flag | DB注释(非中文) |
| 57 | RF_SML_CH_LOT_NO | VARCHAR2(13) | Y |  | Furnance Small Charge Lot No | DB注释(非中文) |
| 58 | RL_INDI_F_CD | VARCHAR2(1) | Y |  | Rolling Instruction Y/N | DB注释(非中文) |
| 59 | HRL_MFC_STD_NO | VARCHAR2(11) | Y |  | Manufacturing standard marks of HR | DB注释(非中文) |
| 60 | SMP_NO | VARCHAR2(11) | Y |  | Sampling No | DB注释(非中文) |
| 61 | SPL_REASON_CD | VARCHAR2(2) | Y |  | Surplus Reason Code | DB注释(非中文) |
| 62 | SLAB_DIRT_ROUTE_CD | VARCHAR2(2) | Y |  | Slab Direction Route Code | DB注释(非中文) |
| 63 | SPEC_RCV_DTM | VARCHAR2(14) | Y |  | Spec Receive DateTime | DB注释(非中文) |
| 64 | PROD_INST_DTM | VARCHAR2(14) | Y |  | Production Order Send(L2) Datetime | DB注释(非中文) |
| 65 | HR_PLAN_OP_CD | VARCHAR2(6) | Y |  | Hot Rolling Operation Code | DB注释(非中文) |
| 66 | ROLL_UNIT | VARCHAR2(20) | Y |  | Roll Unit | DB注释(非中文) |
| 67 | ORD_TY | VARCHAR2(2) | Y |  | OrderType | DB注释(非中文) |
| 68 | CONF_PASS_PLANT_CD | VARCHAR2(30) | Y |  | Confirm Pass Plant Code | DB注释(非中文) |
| 69 | URGENT_TY | VARCHAR2(1) | Y |  | Urgent Type | DB注释(非中文) |
| 70 | SPEC_RTN_USER_ID | VARCHAR2(20) | Y |  | Spec Return User ID | DB注释(非中文) |
| 71 | SPEC_RTN_DTM | VARCHAR2(14) | Y |  | Spec Return Datetime | DB注释(非中文) |
| 72 | MOM_SLAB_DGN_MGT_NO | VARCHAR2(13) | Y |  |  | 空 |
| 73 | ORD_NO4 | VARCHAR2(10) | Y |  | Order No4_订单号4 | DB注释(中文) |
| 74 | ORD_LN4 | VARCHAR2(3) | Y |  | Order Line4_订单行号4 | DB注释(中文) |
| 75 | SLAB_DGN_WGT4 | NUMBER | Y |  | Slab Design Weight4_工序计划Slab设计重量4 | DB注释(中文) |
| 76 | SLAB_DGN_LTH4 | NUMBER | Y |  | SlabDesign Length4_工序计划Slab设计长度4 | DB注释(中文) |
| 77 | ORD_NO5 | VARCHAR2(10) | Y |  | Order No5_订单号5 | DB注释(中文) |
| 78 | ORD_LN5 | VARCHAR2(3) | Y |  | Order Line5_订单行号5 | DB注释(中文) |
| 79 | SLAB_DGN_WGT5 | NUMBER | Y |  | Slab Design Weight5_工序计划Slab设计重量5 | DB注释(中文) |
| 80 | SLAB_DGN_LTH5 | NUMBER | Y |  | SlabDesign Length5_工序计划Slab设计长度5 | DB注释(中文) |
| 81 | ORD_NO6 | VARCHAR2(10) | Y |  | Order No6_订单号6 | DB注释(中文) |
| 82 | ORD_LN6 | VARCHAR2(3) | Y |  | Order Line6_订单行号6 | DB注释(中文) |
| 83 | SLAB_DGN_WGT6 | NUMBER | Y |  | Slab Design Weight6_工序计划Slab设计重量6 | DB注释(中文) |
| 84 | SLAB_DGN_LTH6 | NUMBER | Y |  | SlabDesign Length6_工序计划Slab设计长度6 | DB注释(中文) |
| 85 | PROD_CD | VARCHAR2(3) | Y |  | ????_品名代码 | DB注释(中文) |
| 86 | SLAB_TY | VARCHAR2(1) | Y |  | ??SLAB??_铸坯板坯状态 | DB注释(中文) |
| 87 | PQA_SEND_FLAG | VARCHAR2(1) | Y |  | 1-SEND | DB注释(非中文) |
| 88 | ORD_NO7 | VARCHAR2(10) | Y |  | Order No7_订单号7 | DB注释(中文) |
| 89 | ORD_LN7 | VARCHAR2(3) | Y |  | Order Line7_订单行号7 | DB注释(中文) |
| 90 | SLAB_DGN_WGT7 | NUMBER | Y |  | Slab Design Weight7_工序计划Slab设计重量7 | DB注释(中文) |
| 91 | SLAB_DGN_LTH7 | NUMBER | Y |  | SlabDesign Length7_工序计划Slab设计长度7 | DB注释(中文) |
| 92 | ORD_NO8 | VARCHAR2(10) | Y |  | Order No6_订单号6 | DB注释(中文) |
| 93 | ORD_LN8 | VARCHAR2(3) | Y |  | Order Line6_订单行号6 | DB注释(中文) |
| 94 | SLAB_DGN_WGT8 | NUMBER | Y |  | Slab Design Weight6_工序计划Slab设计重量6 | DB注释(中文) |
| 95 | SLAB_DGN_LTH8 | NUMBER | Y |  | SlabDesign Length6_工序计划Slab设计长度6 | DB注释(中文) |
| 96 | ORD_NO9 | VARCHAR2(10) | Y |  | Order No6_订单号6 | DB注释(中文) |
| 97 | SLAB_DGN_WGT9 | NUMBER | Y |  | Slab Design Weight6_工序计划Slab设计重量6 | DB注释(中文) |
| 98 | SLAB_DGN_LTH9 | NUMBER | Y |  | SlabDesign Length6_工序计划Slab设计长度6 | DB注释(中文) |
| 99 | ORD_LN9 | VARCHAR2(3) | Y |  |  | 空 |
| 100 | PLAN_ROLL_FL | VARCHAR2(1) | Y |  |  | 空 |

### SCH_INST_HEAT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=33｜被读 29 过程 / 被写 2 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：13354　**主键**：PLAN_HEAT_NO　**语义覆盖**：113/119

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | PLAN_HEAT_NO | VARCHAR2(50) | N | ✓ | Plan Heat No | DB注释(非中文) |
| 9 | SPEC_HEAT_NO | VARCHAR2(50) | Y |  | Spec Heat No | DB注释(非中文) |
| 10 | INST_HEAT_NO | VARCHAR2(9) | Y |  | Instruction Heat No | DB注释(非中文) |
| 11 | CAST_NO | VARCHAR2(8) | Y |  | Cast No | DB注释(非中文) |
| 12 | PLAN_HEAT_CNT | NUMBER | Y |  | Plan Heat Count | DB注释(非中文) |
| 13 | PLAN_HEAT_PRI | NUMBER | Y |  | Plan Heat Priority | DB注释(非中文) |
| 14 | PLAN_HEAT_STS | VARCHAR2(3) | Y |  | Plan Heat Status | DB注释(非中文) |
| 15 | SPEC_CD | VARCHAR2(50) | Y |  | Specification Code | DB注释(非中文) |
| 16 | STEEL_GRD_GRP | VARCHAR2(14) | Y |  | Steel Grade Group | DB注释(非中文) |
| 17 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  | Steel Grade | DB注释(非中文) |
| 18 | SECOND_RFN_CD | VARCHAR2(3) | Y |  | 2nd Refining | DB注释(非中文) |
| 19 | DE_P_YN | VARCHAR2(1) | Y |  | Dephosphorization Y/N | DB注释(非中文) |
| 20 | HEAT_WGT | NUMBER | Y |  | Heat Weight | DB注释(非中文) |
| 21 | SLAB_THK | NUMBER | Y |  | Slab Thickness | DB注释(非中文) |
| 22 | WTH_CHANGE_YN | VARCHAR2(1) | Y |  | Width Change Y/N | DB注释(非中文) |
| 23 | X_STR_SLAB_WTH_CHG_YN | VARCHAR2(1) | Y |  | X Strand Slab Width Change Y/N | DB注释(非中文) |
| 24 | X_STR_STA_WTH | NUMBER | Y |  | X Strand Start Width | DB注释(非中文) |
| 25 | X_STR_END_WTH | NUMBER | Y |  | X Strand End Width | DB注释(非中文) |
| 26 | Y_STR_SLAB_WTH_CHG_YN | VARCHAR2(1) | Y |  | Y Strand Slab Width Change Y/N | DB注释(非中文) |
| 27 | Y_STR_STA_WTH | NUMBER | Y |  | Y Strand Start Width | DB注释(非中文) |
| 28 | Y_STR_END_WTH | NUMBER | Y |  | Y Strand End Width | DB注释(非中文) |
| 29 | SLAB_TOT_LTH | NUMBER | Y |  | Slab Total Length | DB注释(非中文) |
| 30 | SLAB_PCS | NUMBER | Y |  | Slab Pieces | DB注释(非中文) |
| 31 | PROD_PCS | NUMBER | Y |  | Product Pieces | DB注释(非中文) |
| 32 | ORD_FL | VARCHAR2(1) | Y |  | APO/Surplus Type | DB注释(非中文) |
| 33 | ORD_NO | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 34 | ORD_LN | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 35 | PLAN_DTM | VARCHAR2(14) | Y |  | Plan DateTime | DB注释(非中文) |
| 36 | PROD_INST_DTM | VARCHAR2(14) | Y |  | Production Order Send(L2) Datetime | DB注释(非中文) |
| 37 | TIME_SCH_DTM | VARCHAR2(14) | Y |  | Time Schedule Datetime | DB注释(非中文) |
| 38 | RTN_YN | VARCHAR2(1) | Y |  | Return Y/N | DB注释(非中文) |
| 39 | STEEL_GRD_DIVERT_YN | VARCHAR2(1) | Y |  | Steel Grade Diversion Y/N | DB注释(非中文) |
| 40 | PLAN_PROC_ROUTE | VARCHAR2(30) | Y |  | Plan Route | DB注释(非中文) |
| 41 | PI_PR_END_DTM | VARCHAR2(14) | Y |  | Pig Iron Prepare End Datetime | DB注释(非中文) |
| 42 | SCRAP_CHARGE_STA_DTM | VARCHAR2(14) | Y |  | Scrap Charge Start Datetime | DB注释(非中文) |
| 43 | MELT_STA_DTM | VARCHAR2(14) | Y |  | Melting Start Datetime | DB注释(非中文) |
| 44 | KR_NO | VARCHAR2(1) | Y |  | KR No | DB注释(非中文) |
| 45 | KR_STA_DTM | VARCHAR2(14) | Y |  | KR Start Date | DB注释(非中文) |
| 46 | KR_END_DTM | VARCHAR2(14) | Y |  | KR End Date | DB注释(非中文) |
| 47 | DE_P_MC_NO | VARCHAR2(1) | Y |  | BOF(De-P) No | DB注释(非中文) |
| 48 | DE_P_BLW_STA_DTM | VARCHAR2(14) | Y |  | BOF(De-P) Blowing Start Date | DB注释(非中文) |
| 49 | DE_P_BLW_END_DTM | VARCHAR2(14) | Y |  | BOF(De-P) Blowing End Date | DB注释(非中文) |
| 50 | DE_P_TAP_STA_DTM | VARCHAR2(14) | Y |  | BOF(De-P) Tapping Start Date | DB注释(非中文) |
| 51 | DE_P_TAP_END_DTM | VARCHAR2(14) | Y |  | BOF(De-P) Tapping End Date | DB注释(非中文) |
| 52 | DE_C_MC_NO | VARCHAR2(1) | Y |  | BOF(De-C) No | DB注释(非中文) |
| 53 | DE_C_BLW_STA_DTM | VARCHAR2(14) | Y |  | BOF(De-C) Blowing Start Date | DB注释(非中文) |
| 54 | DE_C_BLW_END_DTM | VARCHAR2(14) | Y |  | BOF(De-C) Blowing End Date | DB注释(非中文) |
| 55 | DE_C_TAP_STA_DTM | VARCHAR2(14) | Y |  | BOF(De-C) Tapping Start Date | DB注释(非中文) |
| 56 | DE_C_TAP_END_DTM | VARCHAR2(14) | Y |  | BOF(De-C) Tapping End Date | DB注释(非中文) |
| 57 | WF_NO | VARCHAR2(1) | Y |  | WF No | DB注释(非中文) |
| 58 | WF_STA_DTM | VARCHAR2(14) | Y |  | WF Start Date | DB注释(非中文) |
| 59 | WF_END_DTM | VARCHAR2(14) | Y |  | WF End Date | DB注释(非中文) |
| 60 | LF_NO | VARCHAR2(1) | Y |  | LF No | DB注释(非中文) |
| 61 | LF_STA_DTM | VARCHAR2(14) | Y |  | LF Start Date | DB注释(非中文) |
| 62 | LF_END_DTM | VARCHAR2(14) | Y |  | LF End Date | DB注释(非中文) |
| 63 | RH_NO | VARCHAR2(1) | Y |  | RH No | DB注释(非中文) |
| 64 | RH_STA_DTM | VARCHAR2(14) | Y |  | RH Start Date | DB注释(非中文) |
| 65 | RH_END_DTM | VARCHAR2(14) | Y |  | RH  End Date | DB注释(非中文) |
| 66 | CC_NO | VARCHAR2(1) | Y |  | C. Caster No | DB注释(非中文) |
| 67 | CC_ARR_DTM | VARCHAR2(14) | Y |  | C. Caster Arrival date | DB注释(非中文) |
| 68 | CC_STA_DTM | VARCHAR2(14) | Y |  | C. Caster Casting Start Date | DB注释(非中文) |
| 69 | CC_END_DTM | VARCHAR2(14) | Y |  | C. Caster Casting End Date | DB注释(非中文) |
| 70 | TUNDISH_CHG_FL | VARCHAR2(1) | Y |  | Tundish Change Flag(Manaul) | DB注释(非中文) |
| 71 | STA_SLAB_CUT_LTH | NUMBER | Y |  | Start Slab Cutting Length | DB注释(非中文) |
| 72 | END_SLAB_CUT_LTH | NUMBER | Y |  | End Slab Cutting Length | DB注释(非中文) |
| 73 | STA_SLAB_TD_CHG_CUT_LTH | NUMBER | Y |  | After Tundish Change, Start Slab Cutting Length in Cast no | DB注释(非中文) |
| 74 | END_SLAB_TD_CHG_CUT_LTH | NUMBER | Y |  | Before Tundish Change, End Slab Cutting Length in Cast No | DB注释(非中文) |
| 75 | CUT_SLAB_WGT | NUMBER | Y |  | Slab Cutting(Scrap) Weight | DB注释(非中文) |
| 76 | TAP_TEMP_AIM | NUMBER | Y |  | Tapping Aim Temp. | DB注释(非中文) |
| 77 | LF_DEP_TEMP_AIM | NUMBER | Y |  | LF Departure Aim Temp. | DB注释(非中文) |
| 78 | RH_DEP_TEMP_AIM | NUMBER | Y |  | RH Departure Aim Temp. | DB注释(非中文) |
| 79 | TD_STE_TEMP_AIM | NUMBER | Y |  | Turndish  Steel Aim Temp. | DB注释(非中文) |
| 80 | TD_STE_TEMP_MIN | NUMBER | Y |  | Turndish  Steel Min Temp. | DB注释(非中文) |
| 81 | TD_STE_TEMP_MAX | NUMBER | Y |  | Turndish  Steel Max Temp. | DB注释(非中文) |
| 82 | RTN_HEAT_NO | VARCHAR2(8) | Y |  | Retuen Heat No | DB注释(非中文) |
| 83 | BEF_CHG_PLAN_HEAT_NO | VARCHAR2(8) | Y |  | Before Change Plan Heat No | DB注释(非中文) |
| 84 | BEF_CHG_STEEL_GRD | VARCHAR2(10) | Y |  | Before Change Plan Steel Grade | DB注释(非中文) |
| 85 | INCMP_STEEL_GRD1 | VARCHAR2(10) | Y |  | Steel Grade1 | DB注释(非中文) |
| 86 | SLAB_DIRT_WGT1 | NUMBER | Y |  | Slab Direction Weight 1 | DB注释(非中文) |
| 87 | INCMP_STEEL_GRD2 | VARCHAR2(10) | Y |  | Steel Grade2 | DB注释(非中文) |
| 88 | SLAB_DIRT_WGT2 | NUMBER | Y |  | Slab Direction Weight 2 | DB注释(非中文) |
| 89 | INCMP_STEEL_GRD3 | VARCHAR2(10) | Y |  | Steel Grade3 | DB注释(非中文) |
| 90 | SLAB_DIRT_WGT3 | NUMBER | Y |  | Slab Direction Weight 3 | DB注释(非中文) |
| 91 | INCMP_STEEL_GRD4 | VARCHAR2(10) | Y |  | Steel Grade4 | DB注释(非中文) |
| 92 | SLAB_DIRT_WGT4 | NUMBER | Y |  | Slab Direction Weight 4 | DB注释(非中文) |
| 93 | INCMP_STEEL_GRD5 | VARCHAR2(10) | Y |  | Steel Grade5 | DB注释(非中文) |
| 94 | SLAB_DIRT_WGT5 | NUMBER | Y |  | Slab Direction Weight 5 | DB注释(非中文) |
| 95 | BOF_WORK_AIM_TM | NUMBER | Y |  | BOF Aim WorkingTime | DB注释(非中文) |
| 96 | WF_WORK_AIM_TM | NUMBER | Y |  | 2nd Refining WF Aim Working Time | DB注释(非中文) |
| 97 | LF_WORK_AIM_TM | NUMBER | Y |  | 2nd Refining LF Aim Working Time | DB注释(非中文) |
| 98 | RH_WORK_AIM_TM | NUMBER | Y |  | 2nd Refining RH Aim Working Time | DB注释(非中文) |
| 99 | RH_WORK_AIM_TM1 | NUMBER | Y |  | 2nd Refining RH Aim Working Time 1 | DB注释(非中文) |
| 100 | TOT_WORK_AIM_TM | NUMBER | Y |  | Total Work Aim Time | DB注释(非中文) |
| 101 | WF_MOV_AIM_TM | NUMBER | Y |  | 2nd Refining WF Aim Moving Time | DB注释(非中文) |
| 102 | LF_MOV_AIM_TM | NUMBER | Y |  | 2nd Refining LF Aim Moving Time | DB注释(非中文) |
| 103 | RH_MOV_AIM_TM | NUMBER | Y |  | 2nd Refining RH Aim Moving Time | DB注释(非中文) |
| 104 | RH_MOV_AIM_TM1 | NUMBER | Y |  | 2nd Refining RH Aim Working Time 1 | DB注释(非中文) |
| 105 | CC_MOV_AIM_TM | NUMBER | Y |  | C.Casting Aim Moving Time | DB注释(非中文) |
| 106 | TOT_MOV_AIM_TM | NUMBER | Y |  | Total Aim Moving Time | DB注释(非中文) |
| 107 | CC_SPD_AIM | NUMBER | Y |  | C.Casting Aim Speed | DB注释(非中文) |
| 108 | CC_SPD_MIN | NUMBER | Y |  | C.Casting Minimum Speed | DB注释(非中文) |
| 109 | CC_SPD_MAX | NUMBER | Y |  | C.Casting Maximum Speed | DB注释(非中文) |
| 110 | CC_PLAN_NO | VARCHAR2(10) | Y |  | C.Casting Plan No | DB注释(非中文) |
| 111 | SEND_FL | VARCHAR2(1) | Y |  | Send Flag | DB注释(非中文) |
| 112 | PI_REQ_WGT | NUMBER | Y |  | Pig Iron Request Weight | DB注释(非中文) |
| 113 | PROD_CD | VARCHAR2(3) | Y |  | Product Code | SCO_DATA_DIC(D) |
| 114 | VD_NO | VARCHAR2(1) | Y |  |  | 空 |
| 115 | VD_STA_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 116 | VD_END_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 117 | VD_DEP_TEMP_AIM | NUMBER | Y |  |  | 空 |
| 118 | VD_WORK_AIM_TM | NUMBER | Y |  |  | 空 |
| 119 | VD_MOV_AIM_TM | NUMBER | Y |  |  | 空 |

### SQM_SMP_STS

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=33｜被读 25 过程 / 被写 4 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：54538　**主键**：CHEM_SMP_CD、CHEM_SMP_SEQ　**语义覆盖**：19/19

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | 生成UserID_??UserID | DB注释(中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | 生成ObjectID_??ObjectID | DB注释(中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | 生成时间_???? | DB注释(中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 变更UserID_??UserID | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | 变更ObjectID_??ObjectID | DB注释(中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | 变更时间_???? | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Archive情况_Archive?? | DB注释(中文) |
| 8 | CHEM_SMP_CD | VARCHAR2(12) | N | ✓ | 试验试料编码 | DB注释(中文) |
| 9 | CHEM_SMP_SEQ | VARCHAR2(16) | N | ✓ | 试验试料序列号 | DB注释(中文) |
| 10 | NON_ANAL_RSN | VARCHAR2(1) | Y |  | 试验验未分析原因编码 | DB注释(中文) |
| 11 | SMP_ANAL_END_DTM | VARCHAR2(14) | Y |  | 试料分析完成时间 | DB注释(中文) |
| 12 | SMP_SEND_DTM | VARCHAR2(14) | Y |  | 结果发送时间 | DB注释(中文) |
| 13 | SMP_RECEIPT_DTM | VARCHAR2(14) | Y |  | 试料到达时间 | DB注释(中文) |
| 14 | INSP_EMP_NO | VARCHAR2(10) | Y |  | 职员NO | DB注释(中文) |
| 15 | INSP_EMP_NM | VARCHAR2(50) | Y |  | 职员名 | DB注释(中文) |
| 16 | TREAT_CNT | NUMBER | Y |  | 试验处理件数 | DB注释(中文) |
| 17 | CHEM_JUDG | VARCHAR2(1) | Y |  | 试验项目判定结果 | DB注释(中文) |
| 18 | CHEM_FLAG | VARCHAR2(1) | Y |  | 最终结果标记 | DB注释(中文) |
| 19 | CHEM_REQ_NO | VARCHAR2(20) | Y |  | 试验委托号 | DB注释(中文) |

### SQM_SMP_DETAIL

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=33｜被读 25 过程 / 被写 4 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：0　**主键**：CHEM_SMP_CD、ANAL_TY、CHEM_CD　**语义覆盖**：21/33

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | 生成UserID_??UserID | DB注释(中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | 生成ObjectID_??ObjectID | DB注释(中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | 生成时间_???? | DB注释(中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 变更UserID_??UserID | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | 变更ObjectID_??ObjectID | DB注释(中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | 变更时间_???? | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Archive情况_Archive?? | DB注释(中文) |
| 8 | CHEM_SMP_CD | VARCHAR2(12) | N | ✓ | 试验试料编码_???? | DB注释(中文) |
| 9 | ANAL_TY | VARCHAR2(1) | N | ✓ | 分析类型区分_?????? | DB注释(中文) |
| 10 | CHEM_CD | VARCHAR2(3) | N | ✓ | 试验项目编码_???? | DB注释(中文) |
| 11 | CHEM_NM | VARCHAR2(50) | Y |  | 试验项目名称_??? | DB注释(中文) |
| 12 | CHEM_MIN | NUMBER | Y |  | 试验上限值_??? | DB注释(中文) |
| 13 | CHEM_MAX | NUMBER | Y |  | 试验下限值_??? | DB注释(中文) |
| 14 | DISP_SEQ | NUMBER | Y |  | 界面输出顺序_?????? | DB注释(中文) |
| 15 | UOM | VARCHAR2(10) | Y |  | 单位_?? | DB注释(中文) |
| 16 | NUM_FMT | VARCHAR2(50) | Y |  | 单位输出型态_?????? | DB注释(中文) |
| 17 | DECIMAL_POINT | VARCHAR2(50) | Y |  | DATA格式_DATA????? | DB注释(中文) |
| 18 | STAND_GRADE1 | VARCHAR2(1) | Y |  | 标准等级1 | DB注释(中文) |
| 19 | CHEM_MIN1 | NUMBER | Y |  | 下限值1 | DB注释(中文) |
| 20 | CHEM_MAX1 | NUMBER | Y |  | 上限值1 | DB注释(中文) |
| 21 | STAND_GRADE2 | VARCHAR2(1) | Y |  |  | 空 |
| 22 | CHEM_MIN2 | NUMBER | Y |  |  | 空 |
| 23 | CHEM_MAX2 | NUMBER | Y |  |  | 空 |
| 24 | STAND_GRADE3 | VARCHAR2(1) | Y |  |  | 空 |
| 25 | CHEM_MIN3 | NUMBER | Y |  |  | 空 |
| 26 | CHEM_MAX3 | NUMBER | Y |  |  | 空 |
| 27 | STAND_GRADE4 | VARCHAR2(1) | Y |  |  | 空 |
| 28 | CHEM_MIN4 | NUMBER | Y |  |  | 空 |
| 29 | CHEM_MAX4 | NUMBER | Y |  |  | 空 |
| 30 | STAND_GRADE5 | VARCHAR2(1) | Y |  |  | 空 |
| 31 | CHEM_MIN5 | NUMBER | Y |  |  | 空 |
| 32 | CHEM_MAX5 | NUMBER | Y |  |  | 空 |
| 33 | TIME_STAND | NUMBER | Y |  | 时效标准 | DB注释(中文) |

### SQM_MTC_MECH

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=33｜被读 19 过程 / 被写 7 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：487　**主键**：MTC_NO、MTC_CHG_CNT、SMP_NO　**语义覆盖**：507/762

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | MTC_NO | VARCHAR2(11) | N | ✓ | 质量保证书编号 | DB注释(中文) |
| 9 | MTC_CHG_CNT | NUMBER | N | ✓ | 质量保证书变更回数 | DB注释(中文) |
| 10 | SMP_NO | VARCHAR2(14) | N | ✓ | 试样编号 | DB注释(中文) |
| 11 | TEST_CNT | NUMBER | Y |  | 试验回数 | DB注释(中文) |
| 12 | TSL_YP_RSLT | NUMBER | Y |  | 拉伸测试屈服强度实绩 | DB注释(中文) |
| 13 | TSL_TS_RSLT | NUMBER | Y |  | 拉伸测试抗拉强度实绩 | DB注释(中文) |
| 14 | TSL_EL_RSLT | NUMBER | Y |  | 拉伸测试伸长率实绩 | DB注释(中文) |
| 15 | TSL_YR_RSLT | NUMBER | Y |  | 拉伸测试屈强比实绩 | DB注释(中文) |
| 16 | TSL_RA_RSLT | NUMBER | Y |  | 拉伸测试断面收缩率实绩 | DB注释(中文) |
| 17 | TSL_R_RSLT | NUMBER | Y |  | 拉抻测试塑性应变比r平均实绩 | DB注释(中文) |
| 18 | TSL_R0_RSLT | NUMBER | Y |  | 拉抻测试r0实绩 | DB注释(中文) |
| 19 | TSL_R45_RSLT | NUMBER | Y |  | 拉抻测试r45实绩 | DB注释(中文) |
| 20 | TSL_R90_RSLT | NUMBER | Y |  | 拉抻测试r90实绩 | DB注释(中文) |
| 21 | TSL_N_RSLT | NUMBER | Y |  | 拉伸测试加工硬化指数n平均实绩 | DB注释(中文) |
| 22 | TSL_N0_RSLT | NUMBER | Y |  | 拉抻测试N0实绩 | DB注释(中文) |
| 23 | TSL_N45_RSLT | NUMBER | Y |  | 拉抻测试N45实绩 | DB注释(中文) |
| 24 | TSL_N90_RSLT | NUMBER | Y |  | 拉抻测试N90实绩 | DB注释(中文) |
| 25 | BEND_RSLT | VARCHAR2(1) | Y |  | 弯曲测试实绩 | DB注释(中文) |
| 26 | EXT_HOLE_RATIO_AVG_RSLT | NUMBER | Y |  | 扩孔测试极限扩孔率平均实绩 | DB注释(中文) |
| 27 | IMPACT_AVG_RSLT | NUMBER | Y |  | 冲击测试吸收能量实绩 | DB注释(中文) |
| 28 | IMPACT_IND_RSLT1 | NUMBER | Y |  | 冲击功单个实绩1 | DB注释(中文) |
| 29 | IMPACT_IND_RSLT2 | NUMBER | Y |  | 冲击功单个实绩2 | DB注释(中文) |
| 30 | IMPACT_IND_RSLT3 | NUMBER | Y |  | 冲击功单个实绩3 | DB注释(中文) |
| 31 | IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 冲击测试纤维断面率平均实绩 | DB注释(中文) |
| 32 | IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩1 | DB注释(中文) |
| 33 | IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩2 | DB注释(中文) |
| 34 | IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩3 | DB注释(中文) |
| 35 | HARD_RSLT | NUMBER | Y |  | 硬度测试实绩 | DB注释(中文) |
| 36 | NON_METAL_A_RSLT | NUMBER | Y |  | 非金属夹杂物A类实绩(细) | DB注释(中文) |
| 37 | NON_METAL_A1_RSLT | NUMBER | Y |  | 非金属夹杂物A1类实绩(粗) | DB注释(中文) |
| 38 | NON_METAL_B_RSLT | NUMBER | Y |  | 非金属夹杂物B类实绩(细) | DB注释(中文) |
| 39 | NON_METAL_B1_RSLT | NUMBER | Y |  | 非金属夹杂物B1类实绩(粗) | DB注释(中文) |
| 40 | NON_METAL_C_RSLT | NUMBER | Y |  | 非金属夹杂物C类实绩(细) | DB注释(中文) |
| 41 | NON_METAL_C1_RSLT | NUMBER | Y |  | 非金属夹杂物C1类实绩(粗) | DB注释(中文) |
| 42 | NON_METAL_D_RSLT | NUMBER | Y |  | 非金属夹杂物D类实绩(细) | DB注释(中文) |
| 43 | NON_METAL_D1_RSLT | NUMBER | Y |  | 非金属夹杂物D1类实绩(粗) | DB注释(中文) |
| 44 | NON_METAL_DS_RSLT | NUMBER | Y |  | 非金属夹杂物Ds实绩 | DB注释(中文) |
| 45 | NON_METAL_ABCD_RSLT | NUMBER | Y |  | 非金属夹杂物A+B+C+D实绩 | DB注释(中文) |
| 46 | S_PRINT_GRD_RSLT | VARCHAR2(1) | Y |  | 硫印测试等级实绩 | DB注释(中文) |
| 47 | DWTT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | DWTT测试最小剪切面积平均实绩 | DB注释(中文) |
| 48 | DWTT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | DWTT测试最小剪切面积单个实绩1 | DB注释(中文) |
| 49 | DWTT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | DWTT测试最小剪切面积单个实绩2 | DB注释(中文) |
| 50 | HIC_CLR_TOT_AVG_RSLT | NUMBER | Y |  | HIC测试CLR全体平均实绩 | DB注释(中文) |
| 51 | HIC_CSR_TOT_AVG_RSLT | NUMBER | Y |  | HIC测试CSR全体平均实绩 | DB注释(中文) |
| 52 | HIC_CTR_TOT_AVG_RSLT | NUMBER | Y |  | HIC测试CTR全体平均实绩 | DB注释(中文) |
| 53 | HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  | 高温拉伸测试屈服强度实绩 | DB注释(中文) |
| 54 | HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  | 高温拉伸测试抗拉强度实绩 | DB注释(中文) |
| 55 | HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  | 高温拉伸测试伸长率实绩 | DB注释(中文) |
| 56 | HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  | 高温拉伸测试断面收缩率实绩 | DB注释(中文) |
| 57 | BH_RSLT | NUMBER | Y |  | 烘烤硬化值测试实绩 | DB注释(中文) |
| 58 | ERICHSEN_RSLT | NUMBER | Y |  | 杯突测试 | DB注释(中文) |
| 59 | TST_COAT_WGT_UPPER_RSLT | NUMBER | Y |  | 镀锌层重量测试上表面镀层实绩 | DB注释(中文) |
| 60 | TST_COAT_WGT_LOWER_RSLT | NUMBER | Y |  | 镀锌层重量测试下表面镀层实绩 | DB注释(中文) |
| 61 | TST_COAT_WGT_TOT_RSLT | NUMBER | Y |  | 镀锌层重量测试双面镀层实绩 | DB注释(中文) |
| 62 | ROUGH_RA_RSLT | NUMBER | Y |  | 表面平均粗糙度实绩(Ra) | DB注释(中文) |
| 63 | MGRPHY_FGS_RSLT | NUMBER | Y |  | 铁素体晶粒尺寸实绩 | DB注释(中文) |
| 64 | MGRPHY_AGS_RSLT | NUMBER | Y |  | 奥氏体晶粒尺寸实绩 | DB注释(中文) |
| 65 | MGRPHY_INCLD_GRD_MAX_RSLT | NUMBER | Y |  | 夹杂物等级上限实绩 | DB注释(中文) |
| 66 | MGRPHY_DECARBON_MAX_RSLT | NUMBER | Y |  | 脱碳层上限实绩 | DB注释(中文) |
| 67 | MGRPHY_BAND_STRC_GRD_MAX_RSLT | NUMBER | Y |  | 带状组织等级上限实绩 | DB注释(中文) |
| 68 | LOT_NO | VARCHAR2(14) | Y |  | 批号 | DB注释(中文) |
| 69 | QLT_REMARK | VARCHAR2(600) | Y |  | 质量Remarks | DB注释(中文) |
| 70 | WAVIN_WA_RSLT | NUMBER | Y |  | 波纹度检测实绩(Wa) | DB注释(中文) |
| 71 | SURFACE_RESIS_RSLT | NUMBER | Y |  | 表面电阻 | DB注释(中文) |
| 72 | ROUGH_RY_RSLT | NUMBER | Y |  | 轮廓最大高度实绩(Ry) | DB注释(中文) |
| 73 | ROUGH_RZ_RSLT | NUMBER | Y |  | 微观不平度十点高度实绩(Rz) | DB注释(中文) |
| 74 | WAVIN_WSA_RSLT | NUMBER | Y |  | 波纹度检测实绩(Wsa) | DB注释(中文) |
| 75 | WAVIN_WSAMAX_RSLT | NUMBER | Y |  | 波纹度检测最大值实绩(Wsamax) | DB注释(中文) |
| 76 | WAVIN_WCA_RSLT | NUMBER | Y |  | 波纹度检测实绩(Wca) | DB注释(中文) |
| 77 | WAVIN_WCAMAX_RSLT | NUMBER | Y |  | 波纹度检测最大值实绩(Wcamax) | DB注释(中文) |
| 78 | WAVIN_WA08_RSLT | NUMBER | Y |  | 波纹度检测实绩(Wa08) | DB注释(中文) |
| 79 | WAVIN_WA08MAX_RSLT | NUMBER | Y |  | 波纹度检测最大值实绩(Wa08max) | DB注释(中文) |
| 80 | ROUGH_RPC_RSLT | NUMBER | Y |  | 表面平均粗糙度实绩(RPC) | DB注释(中文) |
| 81 | ROUGH_RMAX_RSLT | NUMBER | Y |  | 表面平均粗糙度实绩(RMAX) | DB注释(中文) |
| 82 | MGRPHY_GRNSZ_LEVEL | NUMBER | Y |  | 金相测试晶粒度级别 | DB注释(中文) |
| 83 | TSL_YP_TS_RSLT | VARCHAR2(10) | Y |  | 拉伸试验屈强比YP/TS实绩 | DB注释(中文) |
| 84 | TSL_RT05_RM_RSLT | VARCHAR2(10) | Y |  | 拉伸试验屈强比Rt0.5/Rm实绩 | DB注释(中文) |
| 85 | TSL_RT15_RT05_RSLT | VARCHAR2(10) | Y |  | 拉伸试验屈强比Rt1.5/Rt0.5实绩 | DB注释(中文) |
| 86 | TSL_RT20_RT10_RSLT | VARCHAR2(10) | Y |  | 拉伸试验屈强比Rt2.0/Rt1.0实绩 | DB注释(中文) |
| 87 | TSL_RT50_RT10_RSLT | VARCHAR2(10) | Y |  | 拉伸试验屈强比Rt5.0/Rt1.0实绩 | DB注释(中文) |
| 88 | TSL_CT_EX_RA_RSLT | VARCHAR2(10) | Y |  | 拉抻测试断后伸长率实绩 | DB注释(中文) |
| 89 | TSL_CT_RA_RSLT | VARCHAR2(10) | Y |  | 拉伸试验均匀伸长率实绩 | DB注释(中文) |
| 90 | IMPACT_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试样侧膨胀值平均值实绩 | DB注释(中文) |
| 91 | IMPACT_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试样侧膨胀值单值实绩1 | DB注释(中文) |
| 92 | IMPACT_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试样侧膨胀值单值实绩2 | DB注释(中文) |
| 93 | IMPACT_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试样侧膨胀值单值实绩3 | DB注释(中文) |
| 94 | Z_TSL_CUT_IND_RSLT1 | VARCHAR2(10) | Y |  | Z向拉伸断面收缩率单值实绩1 | DB注释(中文) |
| 95 | Z_TSL_CUT_IND_RSLT2 | VARCHAR2(10) | Y |  | Z向拉伸断面收缩率单值实绩2 | DB注释(中文) |
| 96 | Z_TSL_CUT_IND_RSLT3 | VARCHAR2(10) | Y |  | Z向拉伸断面收缩率单值实绩3 | DB注释(中文) |
| 97 | Z_TSL_CUT_AVG_RSLT | VARCHAR2(10) | Y |  | Z向拉伸断面收缩率平均值实绩 | DB注释(中文) |
| 98 | Z_TSL_YP_RSLT | VARCHAR2(10) | Y |  | Z向拉伸试验屈服强度实绩 | DB注释(中文) |
| 99 | Z_TSL_TS_RSLT | VARCHAR2(10) | Y |  | Z向拉伸试验抗拉强度实绩 | DB注释(中文) |
| 100 | Z_TSL_CT_EX_RA_RSLT | VARCHAR2(10) | Y |  | Z向拉伸试验断后伸长率实绩 | DB注释(中文) |
| 101 | HIGH_TEMP_TSL_TEMP_RSLT | VARCHAR2(10) | Y |  | 高温拉伸测试温度实绩 | DB注释(中文) |
| 102 | DWTT1_SA_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | DWTT1纤维断面率SA平均值实绩 | DB注释(中文) |
| 103 | DWTT1_SA_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | DWTT1纤维断面率SA单值实绩1 | DB注释(中文) |
| 104 | DWTT1_SA_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | DWTT1纤维断面率SA单值实绩2 | DB注释(中文) |
| 105 | DWTT2_SA_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | DWTT2纤维断面率SA平均值实绩 | DB注释(中文) |
| 106 | DWTT2_SA_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | DWTT2纤维断面率SA单值实绩1 | DB注释(中文) |
| 107 | DWTT2_SA_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | DWTT2纤维断面率SA单值实绩2 | DB注释(中文) |
| 108 | DWTT3_SA_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | DWTT3纤维断面率SA平均值实绩 | DB注释(中文) |
| 109 | DWTT3_SA_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | DWTT3纤维断面率SA单值实绩1 | DB注释(中文) |
| 110 | DWTT3_SA_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | DWTT3纤维断面率SA单值实绩2 | DB注释(中文) |
| 111 | DWTT4_SA_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | DWTT4纤维断面率SA平均值实绩 | DB注释(中文) |
| 112 | DWTT4_SA_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | DWTT4纤维断面率SA单值实绩1 | DB注释(中文) |
| 113 | DWTT4_SA_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | DWTT4纤维断面率SA单值实绩2 | DB注释(中文) |
| 114 | DWTT5_SA_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | DWTT5纤维断面率SA平均值实绩 | DB注释(中文) |
| 115 | DWTT5_SA_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | DWTT5纤维断面率SA单值实绩1 | DB注释(中文) |
| 116 | DWTT5_SA_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | DWTT5纤维断面率SA单值实绩2 | DB注释(中文) |
| 117 | SSCC_STRESS_TST_VAL_RSLT | VARCHAR2(10) | Y |  | SSCC测试应力实绩 | DB注释(中文) |
| 118 | HIC_CLR_SPCMN_AVG1_RSLT | VARCHAR2(10) | Y |  | HIC测试CLR试样平均1实绩 | DB注释(中文) |
| 119 | HIC_CLR_SPCMN_AVG2_RSLT | VARCHAR2(10) | Y |  | HIC测试CLR试样平均2实绩 | DB注释(中文) |
| 120 | HIC_CLR_SPCMN_AVG3_RSLT | VARCHAR2(10) | Y |  | HIC测试CLR试样平均3实绩 | DB注释(中文) |
| 121 | HIC_CSR_SPCMN_AVG1_RSLT | VARCHAR2(10) | Y |  | HIC测试CSR试样平均1实绩 | DB注释(中文) |
| 122 | HIC_CSR_SPCMN_AVG2_RSLT | VARCHAR2(10) | Y |  | HIC测试CSR试样平均2实绩 | DB注释(中文) |
| 123 | HIC_CSR_SPCMN_AVG3_RSLT | VARCHAR2(10) | Y |  | HIC测试CSR试样平均3实绩 | DB注释(中文) |
| 124 | HIC_CTR_SPCMN_AVG1_RSLT | VARCHAR2(10) | Y |  | HIC测试CTR试样平均1实绩 | DB注释(中文) |
| 125 | HIC_CTR_SPCMN_AVG2_RSLT | VARCHAR2(10) | Y |  | HIC测试CTR试样平均2实绩 | DB注释(中文) |
| 126 | HIC_CTR_SPCMN_AVG3_RSLT | VARCHAR2(10) | Y |  | HIC测试CTR试样平均3实绩 | DB注释(中文) |
| 127 | MGRPHY_GRNSZ_OCCP_RSLT | VARCHAR2(10) | Y |  | 金相测试基相的体积分数实绩 | DB注释(中文) |
| 128 | NON_METAL_A_GRP_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_A类（粗系）上限实绩 | DB注释(中文) |
| 129 | NON_METAL_A_DETAIL_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_A类（细系）上限实绩 | DB注释(中文) |
| 130 | NON_METAL_B_GRP_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_B类（粗系）上限实绩 | DB注释(中文) |
| 131 | NON_METAL_B_DETAIL_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_B类（细系）上限实绩 | DB注释(中文) |
| 132 | NON_METAL_C_GRP_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_C类（粗系）上限实绩 | DB注释(中文) |
| 133 | NON_METAL_C_DETAIL_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_C类（细系）上限实绩 | DB注释(中文) |
| 134 | NON_METAL_D_GRP_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_D类（粗系）上限实绩 | DB注释(中文) |
| 135 | NON_METAL_D_DETAIL_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_D类（细系）上限实绩 | DB注释(中文) |
| 136 | NON_METAL_AC_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_A+C上限实绩 | DB注释(中文) |
| 137 | NON_METAL_BDDS_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_B+D+Ds上限实绩 | DB注释(中文) |
| 138 | CPLATE_CUT_STRESS_RSLT | VARCHAR2(10) | Y |  | 抗剪强度τ实绩 | DB注释(中文) |
| 139 | CPLATE_THK_RSLT | VARCHAR2(10) | Y |  | 复层厚度实绩 | DB注释(中文) |
| 140 | CPLATE_ER_IE_RSLT | VARCHAR2(10) | Y |  | 杯突IE实绩 | DB注释(中文) |
| 141 | CPLATE_IN_BD_RSLT | VARCHAR2(10) | Y |  | 复层弯曲内弯结果 | DB注释(中文) |
| 142 | CPLATE_OT_BD_RSLT | VARCHAR2(10) | Y |  | 复层弯曲外弯结果 | DB注释(中文) |
| 143 | CPLATE_SIDE_BD_RSLT | VARCHAR2(10) | Y |  | 复层弯曲侧弯结果 | DB注释(中文) |
| 144 | HARD_AVG_RSLT | VARCHAR2(10) | Y |  | 硬度平均值实绩 | DB注释(中文) |
| 145 | HARD_IND_RSLT1 | VARCHAR2(10) | Y |  | 硬度平均值实绩1 | DB注释(中文) |
| 146 | HARD_IND_RSLT2 | VARCHAR2(10) | Y |  | 硬度平均值实绩2 | DB注释(中文) |
| 147 | HARD_IND_RSLT3 | VARCHAR2(10) | Y |  | 硬度平均值实绩3 | DB注释(中文) |
| 148 | S_PRINT_RSLT | VARCHAR2(10) | Y |  | 硫印测试实绩 | DB注释(中文) |
| 149 | AGE_TST_STRESS_RSLT | VARCHAR2(10) | Y |  | 时效应变量实绩 | DB注释(中文) |
| 150 | AGE_TST_AGE_TIME_RSLT | VARCHAR2(10) | Y |  | 时效温度实绩 | DB注释(中文) |
| 151 | AGE_TST_AGE_TEMP_RSLT | VARCHAR2(10) | Y |  | 保温时间实绩 | DB注释(中文) |
| 152 | AGE_TST_YP_RSLT | VARCHAR2(10) | Y |  | 时效拉伸测试屈服强度实绩 | DB注释(中文) |
| 153 | AGE_TST_TS_RSLT | VARCHAR2(10) | Y |  | 时效拉伸测试抗拉强度实绩 | DB注释(中文) |
| 154 | AGE_TST_YP_TS_RSLT | VARCHAR2(10) | Y |  | 时效拉伸试验屈强比YP/TS实绩 | DB注释(中文) |
| 155 | AGE_TST_RT05_RM_RSLT | VARCHAR2(10) | Y |  | 时效拉伸试验屈强比Rt0.5/Rm实绩 | DB注释(中文) |
| 156 | AGE_TST_RT15_RT05_RSLT | VARCHAR2(10) | Y |  | 时效拉伸试验屈强比Rt1.5/Rt0.5实绩 | DB注释(中文) |
| 157 | AGE_TST_RT20_RT10_RSLT | VARCHAR2(10) | Y |  | 时效拉伸试验屈强比Rt2.0/Rt1.0实绩 | DB注释(中文) |
| 158 | AGE_TST_RT50_RT10_RSLT | VARCHAR2(10) | Y |  | 时效拉伸试验屈强比Rt5.0/Rt1.0实绩 | DB注释(中文) |
| 159 | AGE_TST_CT_EX_RA_RSLT | VARCHAR2(10) | Y |  | 拉抻测试断后伸长率实绩 | DB注释(中文) |
| 160 | AGE_TST_CT_RA_RSLT | VARCHAR2(10) | Y |  | 时效拉伸试验均匀伸长率实绩 | DB注释(中文) |
| 161 | AGE_TST_RA_RSLT | VARCHAR2(10) | Y |  | 时效拉伸试验断面收缩率实绩 | DB注释(中文) |
| 162 | AGE_TST1_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击1测试平均值实绩 | DB注释(中文) |
| 163 | AGE_TST1_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击1测试单值实绩1 | DB注释(中文) |
| 164 | AGE_TST1_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击1测试单值实绩2 | DB注释(中文) |
| 165 | AGE_TST1_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击1测试单值实绩3 | DB注释(中文) |
| 166 | AGE_TST1_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 纤维断面率1平均值实绩 | DB注释(中文) |
| 167 | AGE_TST1_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 纤维断面率1单值实绩1 | DB注释(中文) |
| 168 | AGE_TST1_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 纤维断面率1单值实绩2 | DB注释(中文) |
| 169 | AGE_TST1_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 纤维断面率1单值实绩3 | DB注释(中文) |
| 170 | AGE_TST1_SIDE_EXP_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击1试样侧膨胀值平均值实绩 | DB注释(中文) |
| 171 | AGE_TST1_SIDE_EXP_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击1试样侧膨胀值单值实绩1 | DB注释(中文) |
| 172 | AGE_TST1_SIDE_EXP_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击1试样侧膨胀值单值实绩2 | DB注释(中文) |
| 173 | AGE_TST1_SIDE_EXP_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击1试样侧膨胀值单值实绩3 | DB注释(中文) |
| 174 | AGE_TST2_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击2测试平均值实绩 | DB注释(中文) |
| 175 | AGE_TST2_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击2测试单值实绩1 | DB注释(中文) |
| 176 | AGE_TST2_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击2测试单值实绩2 | DB注释(中文) |
| 177 | AGE_TST2_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击2测试单值实绩3 | DB注释(中文) |
| 178 | AGE_TST2_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 纤维断面率2平均值实绩 | DB注释(中文) |
| 179 | AGE_TST2_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 纤维断面率2单值实绩1 | DB注释(中文) |
| 180 | AGE_TST2_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 纤维断面率2单值实绩2 | DB注释(中文) |
| 181 | AGE_TST2_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 纤维断面率2单值实绩3 | DB注释(中文) |
| 182 | AGE_TST2_SIDE_EXP_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击2试样侧膨胀值平均值实绩 | DB注释(中文) |
| 183 | AGE_TST2_SIDE_EXP_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击2试样侧膨胀值单值实绩1 | DB注释(中文) |
| 184 | AGE_TST2_SIDE_EXP_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击2试样侧膨胀值单值实绩2 | DB注释(中文) |
| 185 | AGE_TST2_SIDE_EXP_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击2试样侧膨胀值单值实绩3 | DB注释(中文) |
| 186 | AGE_TST3_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击3测试平均值实绩 | DB注释(中文) |
| 187 | AGE_TST3_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击3测试单值实绩1 | DB注释(中文) |
| 188 | AGE_TST3_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击3测试单值实绩2 | DB注释(中文) |
| 189 | AGE_TST3_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击3测试单值实绩3 | DB注释(中文) |
| 190 | AGE_TST3_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 纤维断面率3平均值实绩 | DB注释(中文) |
| 191 | AGE_TST3_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 纤维断面率3单值实绩1 | DB注释(中文) |
| 192 | AGE_TST3_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 纤维断面率3单值实绩2 | DB注释(中文) |
| 193 | AGE_TST3_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 纤维断面率3单值实绩3 | DB注释(中文) |
| 194 | AGE_TST3_SIDE_EXP_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击3试样侧膨胀值平均值实绩1 | DB注释(中文) |
| 195 | AGE_TST3_SIDE_EXP_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击3试样侧膨胀值单值实绩 | DB注释(中文) |
| 196 | AGE_TST3_SIDE_EXP_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击3试样侧膨胀值单值实绩2 | DB注释(中文) |
| 197 | AGE_TST3_SIDE_EXP_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击3试样侧膨胀值单值实绩3 | DB注释(中文) |
| 198 | AGE_TST4_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击4测试平均值实绩 | DB注释(中文) |
| 199 | AGE_TST4_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击4测试单值实绩1 | DB注释(中文) |
| 200 | AGE_TST4_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击4测试单值实绩2 | DB注释(中文) |
| 201 | AGE_TST4_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击4测试单值实绩3 | DB注释(中文) |
| 202 | AGE_TST4_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 纤维断面率4平均值实绩 | DB注释(中文) |
| 203 | AGE_TST4_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 纤维断面率4单值实绩1 | DB注释(中文) |
| 204 | AGE_TST4_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 纤维断面率4单值实绩2 | DB注释(中文) |
| 205 | AGE_TST4_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 纤维断面率4单值实绩3 | DB注释(中文) |
| 206 | AGE_TST4_SIDE_EXP_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击4试样侧膨胀值平均值实绩1 | DB注释(中文) |
| 207 | AGE_TST4_SIDE_EXP_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击4试样侧膨胀值单值实绩 | DB注释(中文) |
| 208 | AGE_TST4_SIDE_EXP_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击4试样侧膨胀值单值实绩2 | DB注释(中文) |
| 209 | AGE_TST4_SIDE_EXP_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击4试样侧膨胀值单值实绩3 | DB注释(中文) |
| 210 | AGE_TST5_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击5测试平均值实绩 | DB注释(中文) |
| 211 | AGE_TST5_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击5测试单值实绩1 | DB注释(中文) |
| 212 | AGE_TST5_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击5测试单值实绩2 | DB注释(中文) |
| 213 | AGE_TST5_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击5测试单值实绩3 | DB注释(中文) |
| 214 | AGE_TST5_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 纤维断面率5平均值实绩 | DB注释(中文) |
| 215 | AGE_TST5_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 纤维断面率5单值实绩1 | DB注释(中文) |
| 216 | AGE_TST5_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 纤维断面率5单值实绩2 | DB注释(中文) |
| 217 | AGE_TST5_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 纤维断面率5单值实绩3 | DB注释(中文) |
| 218 | AGE_TST5_SIDE_EXP_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击5试样侧膨胀值平均值实绩1 | DB注释(中文) |
| 219 | AGE_TST5_SIDE_EXP_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击5试样侧膨胀值单值实绩 | DB注释(中文) |
| 220 | AGE_TST5_SIDE_EXP_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击5试样侧膨胀值单值实绩2 | DB注释(中文) |
| 221 | AGE_TST5_SIDE_EXP_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击5试样侧膨胀值单值实绩3 | DB注释(中文) |
| 222 | NDT_TEMP_RSLT | VARCHAR2(10) | Y |  | NDT温度实绩 | DB注释(中文) |
| 223 | CTOD_VAL_RSLT | VARCHAR2(10) | Y |  | CTOD值实绩 | DB注释(中文) |
| 224 | NP_JHRC_HARD_RSLT | VARCHAR2(10) | Y |  | 淬透性指数_JHRC硬度实绩 | DB注释(中文) |
| 225 | NP_JHRC_DIST_RSLT | VARCHAR2(10) | Y |  | 淬透性指数_JHRC距离实绩 | DB注释(中文) |
| 226 | NP_JHV_HARD_RSLT | VARCHAR2(10) | Y |  | 淬透性指数_JHV硬度实绩 | DB注释(中文) |
| 227 | NP_JHV_DIST_RSLT | VARCHAR2(10) | Y |  | 淬透性指数_JHV距离实绩 | DB注释(中文) |
| 228 | TSL1_YP_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1屈服强度实绩 | DB注释(中文) |
| 229 | TSL1_TS_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1抗拉强度实绩 | DB注释(中文) |
| 230 | TSL1_YP_TS_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1屈强比YP/TS实绩 | DB注释(中文) |
| 231 | TSL1_RT05_RM_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1屈强比Rt0.5/Rm实绩 | DB注释(中文) |
| 232 | TSL1_RT15_RT05_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1屈强比Rt1.5/Rt0.5实绩 | DB注释(中文) |
| 233 | TSL1_RT20_RT10_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1屈强比Rt2.0/Rt1.0实绩 | DB注释(中文) |
| 234 | TSL1_RT50_RT10_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1屈强比Rt5.0/Rt1.0实绩 | DB注释(中文) |
| 235 | TSL1_CT_EX_RA_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1断后伸长率实绩 | DB注释(中文) |
| 236 | TSL1_CT_RA_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1均匀伸长率实绩 | DB注释(中文) |
| 237 | TSL1_RA_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1断面收缩率实绩 | DB注释(中文) |
| 238 | TSL2_YP_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2屈服强度实绩 | DB注释(中文) |
| 239 | TSL2_TS_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2抗拉强度实绩 | DB注释(中文) |
| 240 | TSL2_YP_TS_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2屈强比YP/TS实绩 | DB注释(中文) |
| 241 | TSL2_RT05_RM_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2屈强比Rt0.5/Rm实绩 | DB注释(中文) |
| 242 | TSL2_RT15_RT05_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2屈强比Rt1.5/Rt0.5实绩 | DB注释(中文) |
| 243 | TSL2_RT20_RT10_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2屈强比Rt2.0/Rt1.0实绩 | DB注释(中文) |
| 244 | TSL2_RT50_RT10_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2屈强比Rt5.0/Rt1.0实绩 | DB注释(中文) |
| 245 | TSL2_CT_EX_RA_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2断后伸长率实绩 | DB注释(中文) |
| 246 | TSL2_CT_RA_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2均匀伸长率实绩 | DB注释(中文) |
| 247 | TSL2_RA_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2断面收缩率实绩 | DB注释(中文) |
| 248 | IMPACT1_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验1平均值实绩 | DB注释(中文) |
| 249 | IMPACT1_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验1单值实绩1 | DB注释(中文) |
| 250 | IMPACT1_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验1单值实绩2 | DB注释(中文) |
| 251 | IMPACT1_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验1单值实绩3 | DB注释(中文) |
| 252 | IMPACT1_SF_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验1纤维断面率平均值实绩 | DB注释(中文) |
| 253 | IMPACT1_SF_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验1纤维断面率单值实绩1 | DB注释(中文) |
| 254 | IMPACT1_SF_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验1纤维断面率单值实绩2 | DB注释(中文) |
| 255 | IMPACT1_SF_RATIO_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验1纤维断面率单值实绩3 | DB注释(中文) |
| 256 | IMPACT1_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验1试样侧膨胀值平均值实绩 | DB注释(中文) |
| 257 | IMPACT1_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验1试样侧膨胀值单值实绩1 | DB注释(中文) |
| 258 | IMPACT1_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验1试样侧膨胀值单值实绩2 | DB注释(中文) |
| 259 | IMPACT1_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验1试样侧膨胀值单值实绩3 | DB注释(中文) |
| 260 | IMPACT2_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验2平均值实绩 | DB注释(中文) |
| 261 | IMPACT2_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验2单值实绩1 | DB注释(中文) |
| 262 | IMPACT2_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验2单值实绩2 | DB注释(中文) |
| 263 | IMPACT2_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验2单值实绩3 | DB注释(中文) |
| 264 | IMPACT2_SF_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验2纤维断面率平均值实绩 | DB注释(中文) |
| 265 | IMPACT2_SF_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验2纤维断面率单值实绩1 | DB注释(中文) |
| 266 | IMPACT2_SF_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验2纤维断面率单值实绩2 | DB注释(中文) |
| 267 | IMPACT2_SF_RATIO_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验2纤维断面率单值实绩3 | DB注释(中文) |
| 268 | IMPACT2_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验2试样侧膨胀值平均值实绩 | DB注释(中文) |
| 269 | IMPACT2_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验2试样侧膨胀值单值实绩1 | DB注释(中文) |
| 270 | IMPACT2_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验2试样侧膨胀值单值实绩2 | DB注释(中文) |
| 271 | IMPACT2_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验2试样侧膨胀值单值实绩3 | DB注释(中文) |
| 272 | IMPACT3_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验3平均值实绩 | DB注释(中文) |
| 273 | IMPACT3_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验3单值实绩1 | DB注释(中文) |
| 274 | IMPACT3_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验3单值实绩2 | DB注释(中文) |
| 275 | IMPACT3_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验3单值实绩3 | DB注释(中文) |
| 276 | IMPACT3_SF_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验3纤维断面率平均值实绩 | DB注释(中文) |
| 277 | IMPACT3_SF_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验3纤维断面率单值实绩1 | DB注释(中文) |
| 278 | IMPACT3_SF_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验3纤维断面率单值实绩2 | DB注释(中文) |
| 279 | IMPACT3_SF_RATIO_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验3纤维断面率单值实绩3 | DB注释(中文) |
| 280 | IMPACT3_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验3试样侧膨胀值平均值实绩 | DB注释(中文) |
| 281 | IMPACT3_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验3试样侧膨胀值单值实绩1 | DB注释(中文) |
| 282 | IMPACT3_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验3试样侧膨胀值单值实绩2 | DB注释(中文) |
| 283 | IMPACT3_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验3试样侧膨胀值单值实绩3 | DB注释(中文) |
| 284 | IMPACT4_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验4平均值实绩 | DB注释(中文) |
| 285 | IMPACT4_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验4单值实绩1 | DB注释(中文) |
| 286 | IMPACT4_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验4单值实绩2 | DB注释(中文) |
| 287 | IMPACT4_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验4单值实绩3 | DB注释(中文) |
| 288 | IMPACT4_SF_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验4纤维断面率平均值实绩 | DB注释(中文) |
| 289 | IMPACT4_SF_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验4纤维断面率单值实绩1 | DB注释(中文) |
| 290 | IMPACT4_SF_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验4纤维断面率单值实绩2 | DB注释(中文) |
| 291 | IMPACT4_SF_RATIO_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验4纤维断面率单值实绩3 | DB注释(中文) |
| 292 | IMPACT4_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验4试样侧膨胀值平均值实绩 | DB注释(中文) |
| 293 | IMPACT4_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验4试样侧膨胀值单值实绩1 | DB注释(中文) |
| 294 | IMPACT4_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验4试样侧膨胀值单值实绩2 | DB注释(中文) |
| 295 | IMPACT4_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验4试样侧膨胀值单值实绩3 | DB注释(中文) |
| 296 | TST_COAT_WGT_TOT_AVG_RSLT | VARCHAR2(10) | Y |  | 镀锌层质量测试上下平均 | DB注释(中文) |
| 297 | TST_COAT_WGT_UPPER_AVG_RSLT | VARCHAR2(10) | Y |  | 镀锌层质量测试上表面平均实绩 | DB注释(中文) |
| 298 | TST_COAT_WGT_LOWER_AVG_RSLT | VARCHAR2(10) | Y |  | 镀锌层质量测试下表面平均实绩 | DB注释(中文) |
| 299 | TSL1_EL_RSLT | VARCHAR2(10) | Y |  | 拉伸测试1伸长率实绩 | DB注释(中文) |
| 300 | PW_TSL_YP_CD | VARCHAR2(1) | Y |  | 模拟焊后 拉伸测试屈服强度类型 | DB注释(中文) |
| 301 | PW_TSL_YP_RSLT | NUMBER | Y |  | 模拟焊后 拉伸测试屈服强度实绩 | DB注释(中文) |
| 302 | PW_TSL_YP_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸测试屈服强度判定 | DB注释(中文) |
| 303 | PW_TSL_TS_RSLT | NUMBER | Y |  | 模拟焊后 拉伸测试抗拉强度实绩 | DB注释(中文) |
| 304 | PW_TSL_TS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸测试抗拉强度判定 | DB注释(中文) |
| 305 | PW_TSL_YP_TS_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比YP/TS实绩 | DB注释(中文) |
| 306 | PW_TSL_YP_TS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比YP/TS判定 | DB注释(中文) |
| 307 | PW_TSL_RT05_RM_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比Rt0.5/Rm实绩 | DB注释(中文) |
| 308 | PW_TSL_RT05_RM_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比Rt0.5/Rm判定 | DB注释(中文) |
| 309 | PW_TSL_RT15_RT05_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5实绩 | DB注释(中文) |
| 310 | PW_TSL_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5判定 | DB注释(中文) |
| 311 | PW_TSL_RT20_RT10_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0实绩 | DB注释(中文) |
| 312 | PW_TSL_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0判定 | DB注释(中文) |
| 313 | PW_TSL_RT50_RT10_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0实绩 | DB注释(中文) |
| 314 | PW_TSL_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0判定 | DB注释(中文) |
| 315 | PW_TSL_CT_EX_RA_RSLT | NUMBER | Y |  | 模拟焊后 拉抻测试断后伸长率实绩 | DB注释(中文) |
| 316 | PW_TSL_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 模拟焊后 拉抻测试断后伸长率类型 | DB注释(中文) |
| 317 | PW_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉抻测试断后伸长率判定 | DB注释(中文) |
| 318 | PW_TSL_CT_RA_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验均匀伸长率实绩 | DB注释(中文) |
| 319 | PW_TSL_CT_RA_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验均匀伸长率判定 | DB注释(中文) |
| 320 | PW_TSL_RA_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验断面收缩率实绩 | DB注释(中文) |
| 321 | PW_TSL_RA_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验断面收缩率判定 | DB注释(中文) |
| 322 | PW_TSL_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 模拟焊后 消应力处理_保温温度实绩 | DB注释(中文) |
| 323 | PW_TSL_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 模拟焊后 消应力处理_保温时间实绩 | DB注释(中文) |
| 324 | PW_TSL_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 模拟焊后 消应力处理_冷却方式 | DB注释(中文) |
| 325 | PW_TSL_STRESS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 消应力处理_判定 | DB注释(中文) |
| 326 | PW_IMPACT_TEMP_RSLT | NUMBER | Y |  | 模拟焊后 冲击测试温度实绩 | DB注释(中文) |
| 327 | PW_IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 模拟焊后 冲击测试缺口类型 | DB注释(中文) |
| 328 | PW_IMPACT_ENERGY_CD | VARCHAR2(1) | Y |  | 模拟焊后 冲击试样能量值类型 | DB注释(中文) |
| 329 | PW_IMPACT_AVG_RSLT | NUMBER | Y |  | 模拟焊后 冲击测试平均值实绩 | DB注释(中文) |
| 330 | PW_IMPACT_IND_RSLT1 | NUMBER | Y |  | 模拟焊后 冲击测试单值实绩1 | DB注释(中文) |
| 331 | PW_IMPACT_IND_RSLT2 | NUMBER | Y |  | 模拟焊后 冲击测试单值实绩2 | DB注释(中文) |
| 332 | PW_IMPACT_IND_RSLT3 | NUMBER | Y |  | 模拟焊后 冲击测试单值实绩3 | DB注释(中文) |
| 333 | PW_IMPACT_IND_JDG | VARCHAR2(1) | Y |  | 模拟焊后 冲击测试单值判定 | DB注释(中文) |
| 334 | PW_IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 模拟焊后 纤维断面率平均值实绩 | DB注释(中文) |
| 335 | PW_IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 模拟焊后 纤维断面率单值实绩1 | DB注释(中文) |
| 336 | PW_IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 模拟焊后 纤维断面率单值实绩2 | DB注释(中文) |
| 337 | PW_IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 模拟焊后 纤维断面率单值实绩3 | DB注释(中文) |
| 338 | PW_IMPACT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 模拟焊后 纤维断面率单值判定 | DB注释(中文) |
| 339 | PW_IMPACT_SMP_AVG_RSLT | NUMBER | Y |  | 模拟焊后 冲击试样侧膨胀值平均值实绩 | DB注释(中文) |
| 340 | PW_IMPACT_SMP_IND_RSLT1 | NUMBER | Y |  | 模拟焊后 冲击试样侧膨胀值单值实绩1 | DB注释(中文) |
| 341 | PW_IMPACT_SMP_IND_RSLT2 | NUMBER | Y |  | 模拟焊后 冲击试样侧膨胀值单值实绩2 | DB注释(中文) |
| 342 | PW_IMPACT_SMP_IND_RSLT3 | NUMBER | Y |  | 模拟焊后 冲击试样侧膨胀值单值实绩3 | DB注释(中文) |
| 343 | PW_IMPACT_SMP_IND_JDG | VARCHAR2(1) | Y |  | 模拟焊后 冲击试样侧膨胀值单值判定 | DB注释(中文) |
| 344 | PW_MGRPHY_MTLGRP_TY | VARCHAR2(20) | Y |  | 模拟焊后 组织类型 | DB注释(中文) |
| 345 | PW_MGRPHY_MTLGRP_TY_PROVIDE | VARCHAR2(1) | Y |  | 模拟焊后 组织类型是否提供 | DB注释(中文) |
| 346 | PW_MGRPHY_BAND_STRC_MAX_RSLT | NUMBER | Y |  | 模拟焊后 带状组织等级上限实绩 | DB注释(中文) |
| 347 | PW_MGRPHY_BAND_STRC_MAX_JDG | VARCHAR2(1) | Y |  | 模拟焊后 带状组织等级上限判定 | DB注释(中文) |
| 348 | PW_MGRPHY_RSLT | NUMBER | Y |  |  | 空 |
| 349 | PW_MGRPHY_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 350 | PW_MGRPHY_FGS_RSLT | NUMBER | Y |  | 模拟焊后 铁素体晶粒度实绩 | DB注释(中文) |
| 351 | PW_MGRPHY_FGS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 铁素体晶粒度判定 | DB注释(中文) |
| 352 | PW_MGRPHY_AGS_RSLT | NUMBER | Y |  | 模拟焊后 奥氏体晶粒度实绩 | DB注释(中文) |
| 353 | PW_MGRPHY_AGS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 奥氏体晶粒度判定 | DB注释(中文) |
| 354 | PW_MGRPHY_GRNSZ_OCCP_RSLT | NUMBER | Y |  | 模拟焊后 金相测试基相的体积分数实绩 | DB注释(中文) |
| 355 | PW_MGRPHY_GRNSZ_OCCP_JDG | VARCHAR2(1) | Y |  | 模拟焊后 金相测试基相的体积分数判定 | DB注释(中文) |
| 356 | PW_BEND_DIA | NUMBER | Y |  | 模拟焊后 弯曲测试弯心直径 | DB注释(中文) |
| 357 | PW_BEND_ANGLE | NUMBER | Y |  | 模拟焊后 弯曲测试弯曲角度 | DB注释(中文) |
| 358 | PW_BEND_RSLT | VARCHAR2(1) | Y |  | 模拟焊后 弯曲测试实绩 | DB注释(中文) |
| 359 | PW_BEND_JDG | VARCHAR2(1) | Y |  | 模拟焊后 弯曲测试判定 | DB注释(中文) |
| 360 | PW_Z_TSL_CUT_IND_RSLT1 | NUMBER | Y |  |  | 空 |
| 361 | PW_Z_TSL_CUT_IND_RSLT2 | NUMBER | Y |  |  | 空 |
| 362 | PW_Z_TSL_CUT_IND_RSLT3 | NUMBER | Y |  |  | 空 |
| 363 | PW_Z_TSL_CUT_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 364 | PW_Z_TSL_CUT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 365 | PW_Z_TSL_CUT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 366 | PW_Z_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 367 | PW_Z_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 368 | PW_Z_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 369 | PW_Z_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 370 | PW_Z_TSL_CT_EX_RA_RSLT | NUMBER | Y |  |  | 空 |
| 371 | PW_Z_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 372 | PW_HIGH_TEMP_TSL_STAND_CD | VARCHAR2(20) | Y |  |  | 空 |
| 373 | PW_HIGH_TEMP_TSL_TEMP_RSLT | NUMBER | Y |  |  | 空 |
| 374 | PW_HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 375 | PW_HIGH_TEMP_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 376 | PW_HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  |  | 空 |
| 377 | PW_HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 378 | PW_HIGH_TEMP_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 379 | PW_HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  |  | 空 |
| 380 | PW_HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  |  | 空 |
| 381 | PW_HIGH_TEMP_TSL_EL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 382 | PW_HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  |  | 空 |
| 383 | PW_HIGH_TEMP_TSL_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 384 | PW_SSCC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 385 | PW_SSCC_STRESS_TY | VARCHAR2(1) | Y |  |  | 空 |
| 386 | PW_SSCC_STRESS_TST_VAL_RSLT | NUMBER | Y |  |  | 空 |
| 387 | PW_SSCC_STRESS_TST_VAL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 388 | PW_SSCC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 389 | PW_HIC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 390 | PW_HIC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 391 | PW_HIC_CLR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 392 | PW_HIC_CLR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 393 | PW_HIC_CLR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 394 | PW_HIC_CLR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 395 | PW_HIC_CLR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 396 | PW_HIC_CLR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 397 | PW_HIC_CLR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 398 | PW_HIC_CLR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 399 | PW_HIC_CLR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 400 | PW_HIC_CLR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 401 | PW_HIC_CLR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 402 | PW_HIC_CLR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 403 | PW_HIC_CLR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 404 | PW_HIC_CLR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 405 | PW_HIC_CLR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 406 | PW_HIC_CLR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 407 | PW_HIC_CSR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 408 | PW_HIC_CSR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 409 | PW_HIC_CSR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 410 | PW_HIC_CSR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 411 | PW_HIC_CSR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 412 | PW_HIC_CSR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 413 | PW_HIC_CSR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 414 | PW_HIC_CSR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 415 | PW_HIC_CSR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 416 | PW_HIC_CSR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 417 | PW_HIC_CSR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 418 | PW_HIC_CSR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 419 | PW_HIC_CSR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 420 | PW_HIC_CSR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 421 | PW_HIC_CSR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 422 | PW_HIC_CSR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 423 | PW_HIC_CTR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 424 | PW_HIC_CTR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 425 | PW_HIC_CTR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 426 | PW_HIC_CTR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 427 | PW_HIC_CTR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 428 | PW_HIC_CTR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 429 | PW_HIC_CTR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 430 | PW_HIC_CTR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 431 | PW_HIC_CTR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 432 | PW_HIC_CTR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 433 | PW_HIC_CTR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 434 | PW_HIC_CTR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 435 | PW_HIC_CTR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 436 | PW_HIC_CTR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 437 | PW_HIC_CTR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 438 | PW_HIC_CTR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 439 | PW_HARD_KIND | VARCHAR2(1) | Y |  |  | 空 |
| 440 | PW_HARD_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 441 | PW_HARD_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 442 | PW_HARD_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 443 | MXPW_TSL_YP_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸测试屈服强度类型 | DB注释(中文) |
| 444 | MXPW_TSL_YP_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸测试屈服强度实绩 | DB注释(中文) |
| 445 | MXPW_TSL_YP_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸测试屈服强度判定 | DB注释(中文) |
| 446 | MXPW_TSL_TS_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸测试抗拉强度实绩 | DB注释(中文) |
| 447 | MXPW_TSL_TS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸测试抗拉强度判定 | DB注释(中文) |
| 448 | MXPW_TSL_YP_TS_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比YP/TS实绩 | DB注释(中文) |
| 449 | MXPW_TSL_YP_TS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比YP/TS判定 | DB注释(中文) |
| 450 | MXPW_TSL_RT05_RM_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比Rt0.5/Rm实绩 | DB注释(中文) |
| 451 | MXPW_TSL_RT05_RM_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比Rt0.5/Rm判定 | DB注释(中文) |
| 452 | MXPW_TSL_RT15_RT05_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5实绩 | DB注释(中文) |
| 453 | MXPW_TSL_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5判定 | DB注释(中文) |
| 454 | MXPW_TSL_RT20_RT10_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0实绩 | DB注释(中文) |
| 455 | MXPW_TSL_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0判定 | DB注释(中文) |
| 456 | MXPW_TSL_RT50_RT10_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0实绩 | DB注释(中文) |
| 457 | MXPW_TSL_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0判定 | DB注释(中文) |
| 458 | MXPW_TSL_CT_EX_RA_RSLT | NUMBER | Y |  | 最大模拟焊后 拉抻测试断后伸长率实绩 | DB注释(中文) |
| 459 | MXPW_TSL_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 拉抻测试断后伸长率类型 | DB注释(中文) |
| 460 | MXPW_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉抻测试断后伸长率判定 | DB注释(中文) |
| 461 | MXPW_TSL_CT_RA_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验均匀伸长率实绩 | DB注释(中文) |
| 462 | MXPW_TSL_CT_RA_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验均匀伸长率判定 | DB注释(中文) |
| 463 | MXPW_TSL_RA_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验断面收缩率实绩 | DB注释(中文) |
| 464 | MXPW_TSL_RA_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验断面收缩率判定 | DB注释(中文) |
| 465 | MXPW_TSL_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 最大模拟焊后 消应力处理_保温温度实绩 | DB注释(中文) |
| 466 | MXPW_TSL_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 最大模拟焊后 消应力处理_保温时间实绩 | DB注释(中文) |
| 467 | MXPW_TSL_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 消应力处理_冷却方式 | DB注释(中文) |
| 468 | MXPW_TSL_STRESS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 消应力处理_判定 | DB注释(中文) |
| 469 | MXPW_IMPACT_TEMP_RSLT | NUMBER | Y |  | 最大模拟焊后 冲击测试温度实绩 | DB注释(中文) |
| 470 | MXPW_IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 冲击测试缺口类型 | DB注释(中文) |
| 471 | MXPW_IMPACT_ENERGY_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 冲击试样能量值类型 | DB注释(中文) |
| 472 | MXPW_IMPACT_AVG_RSLT | NUMBER | Y |  | 最大模拟焊后 冲击测试平均值实绩 | DB注释(中文) |
| 473 | MXPW_IMPACT_IND_RSLT1 | NUMBER | Y |  | 最大模拟焊后 冲击测试单值实绩1 | DB注释(中文) |
| 474 | MXPW_IMPACT_IND_RSLT2 | NUMBER | Y |  | 最大模拟焊后 冲击测试单值实绩2 | DB注释(中文) |
| 475 | MXPW_IMPACT_IND_RSLT3 | NUMBER | Y |  | 最大模拟焊后 冲击测试单值实绩3 | DB注释(中文) |
| 476 | MXPW_IMPACT_IND_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 冲击测试单值判定 | DB注释(中文) |
| 477 | MXPW_IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 最大模拟焊后 纤维断面率平均值实绩 | DB注释(中文) |
| 478 | MXPW_IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 最大模拟焊后 纤维断面率单值实绩1 | DB注释(中文) |
| 479 | MXPW_IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 最大模拟焊后 纤维断面率单值实绩2 | DB注释(中文) |
| 480 | MXPW_IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 最大模拟焊后 纤维断面率单值实绩3 | DB注释(中文) |
| 481 | MXPW_IMPACT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 纤维断面率单值判定 | DB注释(中文) |
| 482 | MXPW_IMPACT_SMP_AVG_RSLT | NUMBER | Y |  | 最大模拟焊后 冲击试样侧膨胀值平均值实绩 | DB注释(中文) |
| 483 | MXPW_IMPACT_SMP_IND_RSLT1 | NUMBER | Y |  | 最大模拟焊后 冲击试样侧膨胀值单值实绩1 | DB注释(中文) |
| 484 | MXPW_IMPACT_SMP_IND_RSLT2 | NUMBER | Y |  | 最大模拟焊后 冲击试样侧膨胀值单值实绩2 | DB注释(中文) |
| 485 | MXPW_IMPACT_SMP_IND_RSLT3 | NUMBER | Y |  | 最大模拟焊后 冲击试样侧膨胀值单值实绩3 | DB注释(中文) |
| 486 | MXPW_IMPACT_SMP_IND_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 冲击试样侧膨胀值单值判定 | DB注释(中文) |
| 487 | MXPW_MGRPHY_MTLGRP_TY | VARCHAR2(20) | Y |  | 最大模拟焊后 组织类型 | DB注释(中文) |
| 488 | MXPW_MGRPHY_MTLGRP_TY_PROVIDE | VARCHAR2(1) | Y |  | 最大模拟焊后 组织类型是否提供 | DB注释(中文) |
| 489 | MXPW_MGRPHY_BAND_STRC_MAX_RSLT | NUMBER | Y |  | 最大模拟焊后 带状组织等级上限实绩 | DB注释(中文) |
| 490 | MXPW_MGRPHY_BAND_STRC_MAX_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 带状组织等级上限判定 | DB注释(中文) |
| 491 | MXPW_MGRPHY_RSLT | NUMBER | Y |  |  | 空 |
| 492 | MXPW_MGRPHY_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 493 | MXPW_MGRPHY_FGS_RSLT | NUMBER | Y |  | 最大模拟焊后 铁素体晶粒度实绩 | DB注释(中文) |
| 494 | MXPW_MGRPHY_FGS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 铁素体晶粒度判定 | DB注释(中文) |
| 495 | MXPW_MGRPHY_AGS_RSLT | NUMBER | Y |  | 最大模拟焊后 奥氏体晶粒度实绩 | DB注释(中文) |
| 496 | MXPW_MGRPHY_AGS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 奥氏体晶粒度判定 | DB注释(中文) |
| 497 | MXPW_MGRPHY_GRNSZ_OCCP_RSLT | NUMBER | Y |  | 最大模拟焊后 金相测试基相的体积分数实绩 | DB注释(中文) |
| 498 | MXPW_MGRPHY_GRNSZ_OCCP_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 金相测试基相的体积分数判定 | DB注释(中文) |
| 499 | MXPW_BEND_DIA | NUMBER | Y |  | 最大模拟焊后 弯曲测试弯心直径 | DB注释(中文) |
| 500 | MXPW_BEND_ANGLE | NUMBER | Y |  | 最大模拟焊后 弯曲测试弯曲角度 | DB注释(中文) |
| 501 | MXPW_BEND_RSLT | VARCHAR2(1) | Y |  | 最大模拟焊后 弯曲测试实绩 | DB注释(中文) |
| 502 | MXPW_BEND_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 弯曲测试判定 | DB注释(中文) |
| 503 | MXPW_Z_TSL_CUT_IND_RSLT1 | NUMBER | Y |  |  | 空 |
| 504 | MXPW_Z_TSL_CUT_IND_RSLT2 | NUMBER | Y |  |  | 空 |
| 505 | MXPW_Z_TSL_CUT_IND_RSLT3 | NUMBER | Y |  |  | 空 |
| 506 | MXPW_Z_TSL_CUT_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 507 | MXPW_Z_TSL_CUT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 508 | MXPW_Z_TSL_CUT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 509 | MXPW_Z_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 510 | MXPW_Z_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 511 | MXPW_Z_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 512 | MXPW_Z_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 513 | MXPW_Z_TSL_CT_EX_RA_RSLT | NUMBER | Y |  |  | 空 |
| 514 | MXPW_Z_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 515 | MXPW_HIGH_TEMP_TSL_STAND_CD | VARCHAR2(20) | Y |  |  | 空 |
| 516 | MXPW_HIGH_TEMP_TSL_TEMP_RSLT | NUMBER | Y |  |  | 空 |
| 517 | MXPW_HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 518 | MXPW_HIGH_TEMP_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 519 | MXPW_HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  |  | 空 |
| 520 | MXPW_HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 521 | MXPW_HIGH_TEMP_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 522 | MXPW_HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  |  | 空 |
| 523 | MXPW_HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  |  | 空 |
| 524 | MXPW_HIGH_TEMP_TSL_EL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 525 | MXPW_HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  |  | 空 |
| 526 | MXPW_HIGH_TEMP_TSL_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 527 | MXPW_SSCC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 528 | MXPW_SSCC_STRESS_TY | VARCHAR2(1) | Y |  |  | 空 |
| 529 | MXPW_SSCC_STRESS_TST_VAL_RSLT | NUMBER | Y |  |  | 空 |
| 530 | MXPW_SSCC_STRESS_TST_VAL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 531 | MXPW_SSCC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 532 | MXPW_HIC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 533 | MXPW_HIC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 534 | MXPW_HIC_CLR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 535 | MXPW_HIC_CLR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 536 | MXPW_HIC_CLR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 537 | MXPW_HIC_CLR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 538 | MXPW_HIC_CLR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 539 | MXPW_HIC_CLR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 540 | MXPW_HIC_CLR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 541 | MXPW_HIC_CLR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 542 | MXPW_HIC_CLR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 543 | MXPW_HIC_CLR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 544 | MXPW_HIC_CLR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 545 | MXPW_HIC_CLR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 546 | MXPW_HIC_CLR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 547 | MXPW_HIC_CLR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 548 | MXPW_HIC_CLR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 549 | MXPW_HIC_CLR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 550 | MXPW_HIC_CSR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 551 | MXPW_HIC_CSR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 552 | MXPW_HIC_CSR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 553 | MXPW_HIC_CSR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 554 | MXPW_HIC_CSR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 555 | MXPW_HIC_CSR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 556 | MXPW_HIC_CSR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 557 | MXPW_HIC_CSR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 558 | MXPW_HIC_CSR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 559 | MXPW_HIC_CSR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 560 | MXPW_HIC_CSR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 561 | MXPW_HIC_CSR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 562 | MXPW_HIC_CSR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 563 | MXPW_HIC_CSR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 564 | MXPW_HIC_CSR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 565 | MXPW_HIC_CSR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 566 | MXPW_HIC_CTR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 567 | MXPW_HIC_CTR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 568 | MXPW_HIC_CTR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 569 | MXPW_HIC_CTR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 570 | MXPW_HIC_CTR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 571 | MXPW_HIC_CTR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 572 | MXPW_HIC_CTR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 573 | MXPW_HIC_CTR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 574 | MXPW_HIC_CTR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 575 | MXPW_HIC_CTR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 576 | MXPW_HIC_CTR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 577 | MXPW_HIC_CTR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 578 | MXPW_HIC_CTR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 579 | MXPW_HIC_CTR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 580 | MXPW_HIC_CTR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 581 | MXPW_HIC_CTR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 582 | MXPW_HARD_KIND | VARCHAR2(1) | Y |  |  | 空 |
| 583 | MXPW_HARD_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 584 | MXPW_HARD_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 585 | MXPW_HARD_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 586 | MNPW_TSL_YP_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸测试屈服强度类型 | DB注释(中文) |
| 587 | MNPW_TSL_YP_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸测试屈服强度实绩 | DB注释(中文) |
| 588 | MNPW_TSL_YP_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸测试屈服强度判定 | DB注释(中文) |
| 589 | MNPW_TSL_TS_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸测试抗拉强度实绩 | DB注释(中文) |
| 590 | MNPW_TSL_TS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸测试抗拉强度判定 | DB注释(中文) |
| 591 | MNPW_TSL_YP_TS_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比YP/TS实绩 | DB注释(中文) |
| 592 | MNPW_TSL_YP_TS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比YP/TS判定 | DB注释(中文) |
| 593 | MNPW_TSL_RT05_RM_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比Rt0.5/Rm实绩 | DB注释(中文) |
| 594 | MNPW_TSL_RT05_RM_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比Rt0.5/Rm判定 | DB注释(中文) |
| 595 | MNPW_TSL_RT15_RT05_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5实绩 | DB注释(中文) |
| 596 | MNPW_TSL_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5判定 | DB注释(中文) |
| 597 | MNPW_TSL_RT20_RT10_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0实绩 | DB注释(中文) |
| 598 | MNPW_TSL_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0判定 | DB注释(中文) |
| 599 | MNPW_TSL_RT50_RT10_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0实绩 | DB注释(中文) |
| 600 | MNPW_TSL_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0判定 | DB注释(中文) |
| 601 | MNPW_TSL_CT_EX_RA_RSLT | NUMBER | Y |  | 最小模拟焊后 拉抻测试断后伸长率实绩 | DB注释(中文) |
| 602 | MNPW_TSL_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 拉抻测试断后伸长率类型 | DB注释(中文) |
| 603 | MNPW_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉抻测试断后伸长率判定 | DB注释(中文) |
| 604 | MNPW_TSL_CT_RA_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验均匀伸长率实绩 | DB注释(中文) |
| 605 | MNPW_TSL_CT_RA_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验均匀伸长率判定 | DB注释(中文) |
| 606 | MNPW_TSL_RA_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验断面收缩率实绩 | DB注释(中文) |
| 607 | MNPW_TSL_RA_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验断面收缩率判定 | DB注释(中文) |
| 608 | MNPW_TSL_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 最小模拟焊后 消应力处理_保温温度实绩 | DB注释(中文) |
| 609 | MNPW_TSL_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 最小模拟焊后 消应力处理_保温时间实绩 | DB注释(中文) |
| 610 | MNPW_TSL_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 消应力处理_冷却方式 | DB注释(中文) |
| 611 | MNPW_TSL_STRESS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 消应力处理_判定 | DB注释(中文) |
| 612 | MNPW_IMPACT_TEMP_RSLT | NUMBER | Y |  | 最小模拟焊后 冲击测试温度实绩 | DB注释(中文) |
| 613 | MNPW_IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 冲击测试缺口类型 | DB注释(中文) |
| 614 | MNPW_IMPACT_ENERGY_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 冲击试样能量值类型 | DB注释(中文) |
| 615 | MNPW_IMPACT_AVG_RSLT | NUMBER | Y |  | 最小模拟焊后 冲击测试平均值实绩 | DB注释(中文) |
| 616 | MNPW_IMPACT_IND_RSLT1 | NUMBER | Y |  | 最小模拟焊后 冲击测试单值实绩1 | DB注释(中文) |
| 617 | MNPW_IMPACT_IND_RSLT2 | NUMBER | Y |  | 最小模拟焊后 冲击测试单值实绩2 | DB注释(中文) |
| 618 | MNPW_IMPACT_IND_RSLT3 | NUMBER | Y |  | 最小模拟焊后 冲击测试单值实绩3 | DB注释(中文) |
| 619 | MNPW_IMPACT_IND_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 冲击测试单值判定 | DB注释(中文) |
| 620 | MNPW_IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 最小模拟焊后 纤维断面率平均值实绩 | DB注释(中文) |
| 621 | MNPW_IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 最小模拟焊后 纤维断面率单值实绩1 | DB注释(中文) |
| 622 | MNPW_IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 最小模拟焊后 纤维断面率单值实绩2 | DB注释(中文) |
| 623 | MNPW_IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 最小模拟焊后 纤维断面率单值实绩3 | DB注释(中文) |
| 624 | MNPW_IMPACT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 纤维断面率单值判定 | DB注释(中文) |
| 625 | MNPW_IMPACT_SMP_AVG_RSLT | NUMBER | Y |  | 最小模拟焊后 冲击试样侧膨胀值平均值实绩 | DB注释(中文) |
| 626 | MNPW_IMPACT_SMP_IND_RSLT1 | NUMBER | Y |  | 最小模拟焊后 冲击试样侧膨胀值单值实绩1 | DB注释(中文) |
| 627 | MNPW_IMPACT_SMP_IND_RSLT2 | NUMBER | Y |  | 最小模拟焊后 冲击试样侧膨胀值单值实绩2 | DB注释(中文) |
| 628 | MNPW_IMPACT_SMP_IND_RSLT3 | NUMBER | Y |  | 最小模拟焊后 冲击试样侧膨胀值单值实绩3 | DB注释(中文) |
| 629 | MNPW_IMPACT_SMP_IND_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 冲击试样侧膨胀值单值判定 | DB注释(中文) |
| 630 | MNPW_MGRPHY_MTLGRP_TY | VARCHAR2(20) | Y |  | 最小模拟焊后 组织类型 | DB注释(中文) |
| 631 | MNPW_MGRPHY_MTLGRP_TY_PROVIDE | VARCHAR2(1) | Y |  | 最小模拟焊后 组织类型是否提供 | DB注释(中文) |
| 632 | MNPW_MGRPHY_BAND_STRC_MAX_RSLT | NUMBER | Y |  | 最小模拟焊后 带状组织等级上限实绩 | DB注释(中文) |
| 633 | MNPW_MGRPHY_BAND_STRC_MAX_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 带状组织等级上限判定 | DB注释(中文) |
| 634 | MNPW_MGRPHY_RSLT | NUMBER | Y |  |  | 空 |
| 635 | MNPW_MGRPHY_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 636 | MNPW_MGRPHY_FGS_RSLT | NUMBER | Y |  | 最小模拟焊后 铁素体晶粒度实绩 | DB注释(中文) |
| 637 | MNPW_MGRPHY_FGS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 铁素体晶粒度判定 | DB注释(中文) |
| 638 | MNPW_MGRPHY_AGS_RSLT | NUMBER | Y |  | 最小模拟焊后 奥氏体晶粒度实绩 | DB注释(中文) |
| 639 | MNPW_MGRPHY_AGS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 奥氏体晶粒度判定 | DB注释(中文) |
| 640 | MNPW_MGRPHY_GRNSZ_OCCP_RSLT | NUMBER | Y |  | 最小模拟焊后 金相测试基相的体积分数实绩 | DB注释(中文) |
| 641 | MNPW_MGRPHY_GRNSZ_OCCP_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 金相测试基相的体积分数判定 | DB注释(中文) |
| 642 | MNPW_BEND_DIA | NUMBER | Y |  | 最小模拟焊后 弯曲测试弯心直径 | DB注释(中文) |
| 643 | MNPW_BEND_ANGLE | NUMBER | Y |  | 最小模拟焊后 弯曲测试弯曲角度 | DB注释(中文) |
| 644 | MNPW_BEND_RSLT | VARCHAR2(1) | Y |  | 最小模拟焊后 弯曲测试实绩 | DB注释(中文) |
| 645 | MNPW_BEND_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 弯曲测试判定 | DB注释(中文) |
| 646 | MNPW_Z_TSL_CUT_IND_RSLT1 | NUMBER | Y |  |  | 空 |
| 647 | MNPW_Z_TSL_CUT_IND_RSLT2 | NUMBER | Y |  |  | 空 |
| 648 | MNPW_Z_TSL_CUT_IND_RSLT3 | NUMBER | Y |  |  | 空 |
| 649 | MNPW_Z_TSL_CUT_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 650 | MNPW_Z_TSL_CUT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 651 | MNPW_Z_TSL_CUT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 652 | MNPW_Z_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 653 | MNPW_Z_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 654 | MNPW_Z_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 655 | MNPW_Z_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 656 | MNPW_Z_TSL_CT_EX_RA_RSLT | NUMBER | Y |  |  | 空 |
| 657 | MNPW_Z_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 658 | MNPW_HIGH_TEMP_TSL_STAND_CD | VARCHAR2(20) | Y |  |  | 空 |
| 659 | MNPW_HIGH_TEMP_TSL_TEMP_RSLT | NUMBER | Y |  |  | 空 |
| 660 | MNPW_HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 661 | MNPW_HIGH_TEMP_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 662 | MNPW_HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  |  | 空 |
| 663 | MNPW_HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 664 | MNPW_HIGH_TEMP_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 665 | MNPW_HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  |  | 空 |
| 666 | MNPW_HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  |  | 空 |
| 667 | MNPW_HIGH_TEMP_TSL_EL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 668 | MNPW_HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  |  | 空 |
| 669 | MNPW_HIGH_TEMP_TSL_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 670 | MNPW_SSCC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 671 | MNPW_SSCC_STRESS_TY | VARCHAR2(1) | Y |  |  | 空 |
| 672 | MNPW_SSCC_STRESS_TST_VAL_RSLT | NUMBER | Y |  |  | 空 |
| 673 | MNPW_SSCC_STRESS_TST_VAL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 674 | MNPW_SSCC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 675 | MNPW_HIC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 676 | MNPW_HIC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 677 | MNPW_HIC_CLR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 678 | MNPW_HIC_CLR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 679 | MNPW_HIC_CLR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 680 | MNPW_HIC_CLR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 681 | MNPW_HIC_CLR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 682 | MNPW_HIC_CLR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 683 | MNPW_HIC_CLR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 684 | MNPW_HIC_CLR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 685 | MNPW_HIC_CLR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 686 | MNPW_HIC_CLR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 687 | MNPW_HIC_CLR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 688 | MNPW_HIC_CLR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 689 | MNPW_HIC_CLR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 690 | MNPW_HIC_CLR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 691 | MNPW_HIC_CLR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 692 | MNPW_HIC_CLR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 693 | MNPW_HIC_CSR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 694 | MNPW_HIC_CSR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 695 | MNPW_HIC_CSR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 696 | MNPW_HIC_CSR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 697 | MNPW_HIC_CSR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 698 | MNPW_HIC_CSR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 699 | MNPW_HIC_CSR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 700 | MNPW_HIC_CSR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 701 | MNPW_HIC_CSR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 702 | MNPW_HIC_CSR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 703 | MNPW_HIC_CSR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 704 | MNPW_HIC_CSR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 705 | MNPW_HIC_CSR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 706 | MNPW_HIC_CSR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 707 | MNPW_HIC_CSR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 708 | MNPW_HIC_CSR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 709 | MNPW_HIC_CTR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 710 | MNPW_HIC_CTR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 711 | MNPW_HIC_CTR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 712 | MNPW_HIC_CTR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 713 | MNPW_HIC_CTR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 714 | MNPW_HIC_CTR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 715 | MNPW_HIC_CTR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 716 | MNPW_HIC_CTR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 717 | MNPW_HIC_CTR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 718 | MNPW_HIC_CTR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 719 | MNPW_HIC_CTR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 720 | MNPW_HIC_CTR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 721 | MNPW_HIC_CTR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 722 | MNPW_HIC_CTR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 723 | MNPW_HIC_CTR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 724 | MNPW_HIC_CTR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 725 | MNPW_HARD_KIND | VARCHAR2(1) | Y |  |  | 空 |
| 726 | MNPW_HARD_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 727 | MNPW_HARD_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 728 | MNPW_HARD_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 729 | MNPW_HARD_RSLT1 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 730 | MNPW_HARD_RSLT2 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 731 | MNPW_HARD_RSLT3 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 732 | MNPW_HARD_RSLT4 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 733 | MNPW_HARD_RSLT5 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 734 | MNPW_HARD_RSLT6 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 735 | MNPW_HARD_RSLT7 | NUMBER | Y |  | 硬度测试实绩7 | DB注释(中文) |
| 736 | MNPW_HARD_RSLT8 | NUMBER | Y |  | 硬度测试实绩8 | DB注释(中文) |
| 737 | MNPW_HARD_RSLT9 | NUMBER | Y |  | 硬度测试实绩9 | DB注释(中文) |
| 738 | MXPW_HARD_RSLT1 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 739 | MXPW_HARD_RSLT2 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 740 | MXPW_HARD_RSLT3 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 741 | MXPW_HARD_RSLT4 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 742 | MXPW_HARD_RSLT5 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 743 | MXPW_HARD_RSLT6 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 744 | MXPW_HARD_RSLT7 | NUMBER | Y |  | 硬度测试实绩7 | DB注释(中文) |
| 745 | MXPW_HARD_RSLT8 | NUMBER | Y |  | 硬度测试实绩8 | DB注释(中文) |
| 746 | MXPW_HARD_RSLT9 | NUMBER | Y |  | 硬度测试实绩9 | DB注释(中文) |
| 747 | PW_HARD_RSLT1 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 748 | PW_HARD_RSLT2 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 749 | PW_HARD_RSLT3 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 750 | PW_HARD_RSLT4 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 751 | PW_HARD_RSLT5 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 752 | PW_HARD_RSLT6 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 753 | PW_HARD_RSLT7 | NUMBER | Y |  | 硬度测试实绩7 | DB注释(中文) |
| 754 | PW_HARD_RSLT8 | NUMBER | Y |  | 硬度测试实绩8 | DB注释(中文) |
| 755 | PW_HARD_RSLT9 | NUMBER | Y |  | 硬度测试实绩9 | DB注释(中文) |
| 756 | Z1_TSL_CUT_IND_RSLT1 | VARCHAR2(10) | Y |  | Z向拉伸断面收缩率单值实绩1-1 | DB注释(中文) |
| 757 | Z1_TSL_CUT_IND_RSLT2 | VARCHAR2(10) | Y |  | Z向拉伸断面收缩率单值实绩2-1 | DB注释(中文) |
| 758 | Z1_TSL_CUT_IND_RSLT3 | VARCHAR2(10) | Y |  | Z向拉伸断面收缩率单值实绩3-1 | DB注释(中文) |
| 759 | Z1_TSL_CUT_AVG_RSLT | VARCHAR2(10) | Y |  | Z向拉伸断面收缩率平均值实绩-1 | DB注释(中文) |
| 760 | Z1_TSL_YP_RSLT | VARCHAR2(10) | Y |  | Z向拉伸试验屈服强度实绩-1 | DB注释(中文) |
| 761 | Z1_TSL_TS_RSLT | VARCHAR2(10) | Y |  | Z向拉伸试验抗拉强度实绩-1 | DB注释(中文) |
| 762 | Z1_TSL_CT_EX_RA_RSLT | VARCHAR2(10) | Y |  | Z向拉伸试验断后伸长率实绩-1 | DB注释(中文) |

### SCH_SCH_CRL

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=32｜被读 28 过程 / 被写 2 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：0　**主键**：PROC_CD、ROLL_UNIT、COIL_NO　**语义覆盖**：95/96

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | PROC_CD | VARCHAR2(3) | N | ✓ | Process Code | DB注释(非中文) |
| 9 | ROLL_UNIT | VARCHAR2(10) | N | ✓ | Roll Unit | DB注释(非中文) |
| 10 | COIL_NO | VARCHAR2(15) | N | ✓ | Coil No | DB注释(非中文) |
| 11 | PLAN_PROC_SEQ | NUMBER | Y |  | Plan Process Sequence | DB注释(非中文) |
| 12 | INST_COIL_NO | VARCHAR2(14) | Y |  | Instruction Coil No | DB注释(非中文) |
| 13 | CTL_SCH_SEQ | NUMBER | Y |  | Control Schedule Sequence | DB注释(非中文) |
| 14 | PLAN_COIL_STS_CD | VARCHAR2(2) | Y |  | Plan Coil Status Code | DB注释(非中文) |
| 15 | ROLL_UNIT_PRI | NUMBER | Y |  | Roll Unit Priority | DB注释(非中文) |
| 16 | INST_TY | VARCHAR2(1) | Y |  | Instruction Type | DB注释(非中文) |
| 17 | L2_SEND_YN | VARCHAR2(1) | Y |  | L2 Send YN | DB注释(非中文) |
| 18 | SCH_CHG_FOB_YN | VARCHAR2(1) | Y |  | Schedule Change Forbid YN | DB注释(非中文) |
| 19 | WK_PLAN_DT | VARCHAR2(14) | Y |  | Work Plan Date | DB注释(非中文) |
| 20 | COIL_WTH | NUMBER | Y |  | Coil Width | DB注释(非中文) |
| 21 | COIL_THK | NUMBER | Y |  | Coil Thick | DB注释(非中文) |
| 22 | COIL_LTH | NUMBER | Y |  | Coil Length | DB注释(非中文) |
| 23 | COIL_WGT | NUMBER | Y |  | Coil Weight | DB注释(非中文) |
| 24 | STEEL_GRD | VARCHAR2(10) | Y |  | Steel Grade | DB注释(非中文) |
| 25 | CRL_MFC_STD_NO | VARCHAR2(11) | Y |  | CRL Manufacturing Standard No | DB注释(非中文) |
| 26 | COIL_OUT_DIA | NUMBER | Y |  | Coil Outer Diameter | DB注释(非中文) |
| 27 | COIL_IN_DIA | NUMBER | Y |  | Coil Inner Diameter | DB注释(非中文) |
| 28 | SPEC_CD | VARCHAR2(50) | Y |  | Specification Code | DB注释(非中文) |
| 29 | HEAT_NO | VARCHAR2(9) | Y |  | Heat No | DB注释(非中文) |
| 30 | HCOIL_NO | VARCHAR2(15) | Y |  | Hot Coil No | DB注释(非中文) |
| 31 | ORD_NO | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 32 | ORD_LN | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 33 | PROD_GRP | VARCHAR2(2) | Y |  | Production Group | DB注释(非中文) |
| 34 | PROD_CD | VARCHAR2(3) | Y |  | Production Code | DB注释(非中文) |
| 35 | COIL_LOC | VARCHAR2(10) | Y |  | Coil Location | DB注释(非中文) |
| 36 | PL_ORD_YN | VARCHAR2(1) | Y |  | Plural Order YN | DB注释(非中文) |
| 37 | URGENT_MTL_YN | VARCHAR2(1) | Y |  | Urgent Material YN | DB注释(非中文) |
| 38 | LNK_MTL_YN | VARCHAR2(1) | Y |  | Link Material YN | DB注释(非中文) |
| 39 | DMY_MTL_YN | VARCHAR2(1) | Y |  | Dummy Material YN | DB注释(非中文) |
| 40 | ORD_FL | VARCHAR2(1) | Y |  | Order Flag | DB注释(非中文) |
| 41 | PLAN_ROUTE | VARCHAR2(60) | Y |  | Plan Route | DB注释(非中文) |
| 42 | WK_STA_SCH_DTM | VARCHAR2(14) | Y |  | Work Start Schedule Datetime | DB注释(非中文) |
| 43 | WK_END_SCH_DTM | VARCHAR2(14) | Y |  | Work End Schedule Datetime | DB注释(非中文) |
| 44 | WK_SCH_DUR | NUMBER | Y |  | Work Schedule Duration | DB注释(非中文) |
| 45 | WK_STA_DTM | VARCHAR2(14) | Y |  | Work Start Datetime | DB注释(非中文) |
| 46 | WK_END_DTM | VARCHAR2(14) | Y |  | Work End Datetime | DB注释(非中文) |
| 47 | LINE_SPD | NUMBER | Y |  | Line Speed | DB注释(非中文) |
| 48 | ANN_CYL | VARCHAR2(5) | Y |  | Annealing Cycle | DB注释(非中文) |
| 49 | MRG_TY | VARCHAR2(2) | Y |  | Merge Type | DB注释(非中文) |
| 50 | MRG_GRP_SEQ_NO | NUMBER | Y |  | Merge Group Sequence No | DB注释(非中文) |
| 51 | MRG_MTL_INPUT_SEQ | NUMBER | Y |  | Merge Material Input Sequence | DB注释(非中文) |
| 52 | ORD_DELV_DT | VARCHAR2(8) | Y |  | Order Delivery Date | DB注释(非中文) |
| 53 | PROD_UNIT_WGT_MIN | NUMBER | Y |  | Production Unit Weight Min | DB注释(非中文) |
| 54 | PROD_UNIT_WGT_MAX | NUMBER | Y |  | Production Unit Weight Max | DB注释(非中文) |
| 55 | WELD_POINT_ALOW_YN | VARCHAR2(1) | Y |  | Welding Point Allow YN | DB注释(非中文) |
| 56 | TCM_THK_SET_VAL | NUMBER | Y |  | TCM Thick Set Value | DB注释(非中文) |
| 57 | ST_YN | VARCHAR2(1) | Y |  | Side Trim YN | DB注释(非中文) |
| 58 | ST_WTH | NUMBER | Y |  | Side Trim Width | DB注释(非中文) |
| 59 | SLEEVE_YN | VARCHAR2(1) | Y |  | Sleeve YN | DB注释(非中文) |
| 60 | REPROC_CNT | NUMBER | Y |  | Re-process Count | DB注释(非中文) |
| 61 | BEF_PROC_CD | VARCHAR2(3) | Y |  | Before Process Code | DB注释(非中文) |
| 62 | NXT_PROC_CD | VARCHAR2(3) | Y |  | Next Process Code | DB注释(非中文) |
| 63 | REM_ROUTE | VARCHAR2(60) | Y |  | Remain Route | DB注释(非中文) |
| 64 | ABNR_OCR_CAU_CD | VARCHAR2(2) | Y |  | Abnormal Occurrence Cause Code | DB注释(非中文) |
| 65 | SMP_NO | VARCHAR2(11) | Y |  | Sample No | DB注释(非中文) |
| 66 | SMP_CUT_TY | VARCHAR2(1) | Y |  | Sample Cut Type | DB注释(非中文) |
| 67 | SMP_CUT_LOC | VARCHAR2(1) | Y |  | Sample Cut Location | DB注释(非中文) |
| 68 | SMP_CUT_LTH | NUMBER | Y |  | Sample Cut Length | DB注释(非中文) |
| 69 | COIL_DIV_FL | VARCHAR2(1) | Y |  | Coil Divide Flag | DB注释(非中文) |
| 70 | COIL_DIV_CNT | NUMBER | Y |  | Coil Divide Count | DB注释(非中文) |
| 71 | ORD_NO1 | VARCHAR2(10) | Y |  | Order No1 | DB注释(非中文) |
| 72 | ORD_LN1 | VARCHAR2(3) | Y |  | Order Line1 | DB注释(非中文) |
| 73 | COIL_DIV_WGT1 | NUMBER | Y |  | Coil Divide Weight1 | DB注释(非中文) |
| 74 | ORD_NO2 | VARCHAR2(10) | Y |  | Order No2 | DB注释(非中文) |
| 75 | ORD_LN2 | VARCHAR2(3) | Y |  | Order Line2 | DB注释(非中文) |
| 76 | COIL_DIV_WGT2 | NUMBER | Y |  | Coil Divide Weight2 | DB注释(非中文) |
| 77 | ORD_NO3 | VARCHAR2(10) | Y |  | Order No3 | DB注释(非中文) |
| 78 | ORD_LN3 | VARCHAR2(3) | Y |  | Order Line3 | DB注释(非中文) |
| 79 | COIL_DIV_WGT3 | NUMBER | Y |  | Coil Divide Weight3 | DB注释(非中文) |
| 80 | ORD_NO4 | VARCHAR2(10) | Y |  | Order No4 | DB注释(非中文) |
| 81 | ORD_LN4 | VARCHAR2(3) | Y |  | Order Line4 | DB注释(非中文) |
| 82 | COIL_DIV_WGT4 | NUMBER | Y |  | Coil Divide Weight4 | DB注释(非中文) |
| 83 | ORD_NO5 | VARCHAR2(10) | Y |  | Order No5 | DB注释(非中文) |
| 84 | ORD_LN5 | VARCHAR2(3) | Y |  | Order Line5 | DB注释(非中文) |
| 85 | COIL_DIV_WGT5 | NUMBER | Y |  | Coil Divide Weight5 | DB注释(非中文) |
| 86 | EXIT_WTH | NUMBER | Y |  | Exit Width | DB注释(非中文) |
| 87 | PCKL_DEN | NUMBER | Y |  | Pickling Density | DB注释(非中文) |
| 88 | OIL_TY | VARCHAR2(2) | Y |  | Oil Type | DB注释(非中文) |
| 89 | OIL_TANK | VARCHAR2(2) | Y |  | Oil Tank | DB注释(非中文) |
| 90 | OIL_WGT_TOP | NUMBER | Y |  | Oil Weight Top | DB注释(非中文) |
| 91 | OIL_WGT_BOT | NUMBER | Y |  | Oil Weight Bottom | DB注释(非中文) |
| 92 | SPM_FL | VARCHAR2(1) | Y |  | SPM Flag | DB注释(非中文) |
| 93 | SPM_EL | NUMBER | Y |  | SPM Elongation | DB注释(非中文) |
| 94 | L2_SEND_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 95 | PLAN_DESC | VARCHAR2(300) | Y |  | 计划备注 | DB注释(中文) |
| 96 | PQA_SEND_FLAG | VARCHAR2(1) | Y |  | SEND TO PQA:  1-SEND A2;  2-SEND A9 | DB注释(非中文) |

### SQM_HC_MECH_RSLT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=32｜被读 24 过程 / 被写 4 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：0　**主键**：SMP_NO、SMP_LTH_LOC、TEST_CNT　**语义覆盖**：426/435

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | SMP_NO | VARCHAR2(14) | N | ✓ | 试样编号 | DB注释(中文) |
| 9 | SMP_LTH_LOC | VARCHAR2(1) | N | ✓ | 试样采取位置 | DB注释(中文) |
| 10 | TEST_CNT | NUMBER | N | ✓ | 试验回数 | DB注释(中文) |
| 11 | MECH_RSLT_REG_FST_DTM | VARCHAR2(14) | Y |  | 材质实绩录入最初时间 | DB注释(中文) |
| 12 | MECH_RSLT_REG_LST_DTM | VARCHAR2(14) | Y |  | 材质实绩录入最终时间 | DB注释(中文) |
| 13 | PROD_CHEM_RSLT_REG_DTM | VARCHAR2(14) | Y |  | 产品成分实绩登记时间 | DB注释(中文) |
| 14 | SMP_GTH_INST_MTRL_NO | VARCHAR2(14) | Y |  | 试样采取指示材料编号 | DB注释(中文) |
| 15 | SMP_HTM_ASGN_TY | VARCHAR2(1) | Y |  | 试样热处理指定分类 | DB注释(中文) |
| 16 | MECH_JDG_GRD | VARCHAR2(1) | Y |  | 物性判定等级 | DB注释(中文) |
| 17 | TSL_YP_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度类型 | DB注释(中文) |
| 18 | TSL_YP_RSLT | NUMBER | Y |  | 拉伸测试屈服强度实绩 | DB注释(中文) |
| 19 | TSL_YP_JDG | VARCHAR2(1) | Y |  | 拉伸测试屈服强度判定 | DB注释(中文) |
| 20 | TSL_TS_RSLT | NUMBER | Y |  | 拉伸测试抗拉强度实绩 | DB注释(中文) |
| 21 | TSL_TS_JDG | VARCHAR2(1) | Y |  | 拉伸测试抗拉强度判定 | DB注释(中文) |
| 22 | TSL_EL_CD | VARCHAR2(1) | Y |  | 拉伸测试伸长率类型 | DB注释(中文) |
| 23 | TSL_EL_RSLT | NUMBER | Y |  | 拉伸测试伸长率实绩 | DB注释(中文) |
| 24 | TSL_EL_JDG | VARCHAR2(1) | Y |  | 拉伸测试伸长率判定 | DB注释(中文) |
| 25 | TSL_EL_UNF_RSLT | NUMBER | Y |  | 拉抻测试均匀延伸率(uEL)实绩 | DB注释(中文) |
| 26 | TSL_EL_UNF_JDG | VARCHAR2(1) | Y |  | 拉抻测试均匀延伸率(uEL)判定 | DB注释(中文) |
| 27 | TSL_YR_RSLT | NUMBER | Y |  | 拉伸测试屈强比实绩 | DB注释(中文) |
| 28 | TSL_YR_JDG | VARCHAR2(1) | Y |  | 拉伸测试屈强比判定 | DB注释(中文) |
| 29 | TSL_RA_RSLT | NUMBER | Y |  | 拉伸测试断面收缩率实绩 | DB注释(中文) |
| 30 | TSL_RA_JDG | VARCHAR2(1) | Y |  | 拉伸测试断面收缩率判定 | DB注释(中文) |
| 31 | TSL_R_RSLT | NUMBER | Y |  | 拉抻测试塑性应变比r平均实绩 | DB注释(中文) |
| 32 | TSL_R_JDG | VARCHAR2(1) | Y |  | 拉抻测试塑性应变比r平均判定 | DB注释(中文) |
| 33 | TSL_R0_RSLT | NUMBER | Y |  | 拉抻测试r0实绩 | DB注释(中文) |
| 34 | TSL_R0_JDG | VARCHAR2(1) | Y |  | 拉抻测试r0判定 | DB注释(中文) |
| 35 | TSL_R45_RSLT | NUMBER | Y |  | 拉抻测试r45实绩 | DB注释(中文) |
| 36 | TSL_R45_JDG | VARCHAR2(1) | Y |  | 拉抻测试r45判定 | DB注释(中文) |
| 37 | TSL_R90_RSLT | NUMBER | Y |  | 拉抻测试r90实绩 | DB注释(中文) |
| 38 | TSL_R90_JDG | VARCHAR2(1) | Y |  | 拉抻测试r90判定 | DB注释(中文) |
| 39 | TSL_RDELTA_RSLT | NUMBER | Y |  | 拉伸测试\|Δr\|实绩 | DB注释(中文) |
| 40 | TSL_RDELTA_JDG | VARCHAR2(1) | Y |  | 拉伸测试\|Δr\|判定 | DB注释(中文) |
| 41 | TSL_N_RSLT | NUMBER | Y |  | 拉伸测试加工硬化指数n平均实绩 | DB注释(中文) |
| 42 | TSL_N_JDG | VARCHAR2(1) | Y |  | 拉伸测试加工硬化指数n平均判定 | DB注释(中文) |
| 43 | TSL_N0_RSLT | NUMBER | Y |  | 拉抻测试N0实绩 | DB注释(中文) |
| 44 | TSL_N0_JDG | VARCHAR2(1) | Y |  | 拉抻测试n0判定 | DB注释(中文) |
| 45 | TSL_N45_RSLT | NUMBER | Y |  | 拉抻测试N45实绩 | DB注释(中文) |
| 46 | TSL_N45_JDG | VARCHAR2(1) | Y |  | 拉抻测试n45判定 | DB注释(中文) |
| 47 | TSL_N90_RSLT | NUMBER | Y |  | 拉抻测试N90实绩 | DB注释(中文) |
| 48 | TSL_N90_JDG | VARCHAR2(1) | Y |  | 拉抻测试n90判定 | DB注释(中文) |
| 49 | TSL_TESTER_CD | VARCHAR2(20) | Y |  | 拉伸试验机代码 | DB注释(中文) |
| 50 | TSL_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 拉伸试验人ID | DB注释(中文) |
| 51 | BEND_CD | VARCHAR2(1) | Y |  | 弯曲测试角度 | DB注释(中文) |
| 52 | BEND_UNIT | VARCHAR2(1) | Y |  | 弯曲压头直径 | DB注释(中文) |
| 53 | BEND_ANGLE | NUMBER | Y |  | 弯曲测试弯曲角度 | DB注释(中文) |
| 54 | BEND_DIA | NUMBER | Y |  | 弯曲测试弯心直径 | DB注释(中文) |
| 55 | BEND_RSLT | VARCHAR2(1) | Y |  | 弯曲测试实绩 | DB注释(中文) |
| 56 | BEND_JDG | VARCHAR2(1) | Y |  | 弯曲测试判定 | DB注释(中文) |
| 57 | BEND_TESTER_CD | VARCHAR2(20) | Y |  | 弯曲试验机代码 | DB注释(中文) |
| 58 | BEND_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 弯曲试验人ID | DB注释(中文) |
| 59 | IMPACT_SPCMN_CNT | NUMBER | Y |  | 冲击测试试样数量 | DB注释(中文) |
| 60 | IMPACT_TEMP | NUMBER | Y |  | 冲击测试温度 | DB注释(中文) |
| 61 | IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 冲击测试缺口类型 | DB注释(中文) |
| 62 | IMPACT_AVG_RSLT | NUMBER | Y |  | 冲击测试吸收能量实绩 | DB注释(中文) |
| 63 | IMPACT_IND_RSLT1 | NUMBER | Y |  | 冲击功单个实绩1 | DB注释(中文) |
| 64 | IMPACT_IND_JDG | VARCHAR2(1) | Y |  | 冲击功单个判定 | DB注释(中文) |
| 65 | IMPACT_IND_RSLT2 | NUMBER | Y |  | 冲击功单个实绩2 | DB注释(中文) |
| 66 | IMPACT_IND_RSLT3 | NUMBER | Y |  | 冲击功单个实绩3 | DB注释(中文) |
| 67 | IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 冲击测试纤维断面率平均实绩 | DB注释(中文) |
| 68 | IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩1 | DB注释(中文) |
| 69 | IMPACT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 冲击测试纤维断面率单个判定 | DB注释(中文) |
| 70 | IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩2 | DB注释(中文) |
| 71 | IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩3 | DB注释(中文) |
| 72 | IMPACT_TESTER_CD | VARCHAR2(20) | Y |  | 冲击试验机代码 | DB注释(中文) |
| 73 | IMPACT_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 冲击试验人ID | DB注释(中文) |
| 74 | DWTT_SPCMN_CNT | NUMBER | Y |  | DWTT试验试样数量 | DB注释(中文) |
| 75 | DWTT_TEMP_SIGN | VARCHAR2(1) | Y |  | DWTT试验温度符号 | DB注释(中文) |
| 76 | DWTT_TEMP | NUMBER | Y |  | DWTT试验温度 | DB注释(中文) |
| 77 | DWTT_CREAK_CD | VARCHAR2(1) | Y |  | DWTT测试缺口类型 | DB注释(中文) |
| 78 | DWTT_ABSP_RSLT | NUMBER | Y |  | DWTT测试吸收能量实绩 | DB注释(中文) |
| 79 | DWTT_ABSP_JDG | VARCHAR2(1) | Y |  | DWTT测试吸收能量判定 | DB注释(中文) |
| 80 | DWTT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | DWTT测试最小剪切面积平均实绩 | DB注释(中文) |
| 81 | DWTT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | DWTT测试最小剪切面积单个实绩1 | DB注释(中文) |
| 82 | DWTT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | DWTT测试最小剪切面积单个判定 | DB注释(中文) |
| 83 | DWTT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | DWTT测试最小剪切面积单个实绩2 | DB注释(中文) |
| 84 | DWTT_TESTER_CD | VARCHAR2(20) | Y |  | DWTT试验机代码 | DB注释(中文) |
| 85 | DWTT_DUTY_EMP_ID | VARCHAR2(20) | Y |  | DWTT试验人ID | DB注释(中文) |
| 86 | HARD_KIND | VARCHAR2(1) | Y |  | 硬度试验种类 | DB注释(中文) |
| 87 | HARD_RSLT | NUMBER | Y |  | 硬度测试实绩 | DB注释(中文) |
| 88 | HARD_JDG | VARCHAR2(1) | Y |  | 硬度测试判定 | DB注释(中文) |
| 89 | HARD_RSLT1 | NUMBER | Y |  | 硬度测试实绩1 | DB注释(中文) |
| 90 | HARD_RSLT2 | NUMBER | Y |  | 硬度测试实绩2 | DB注释(中文) |
| 91 | HARD_RSLT3 | NUMBER | Y |  | 硬度测试实绩3 | DB注释(中文) |
| 92 | HARD_TESTER_CD | VARCHAR2(20) | Y |  | 硬度试验机代码 | DB注释(中文) |
| 93 | HARD_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 硬度试验人ID | DB注释(中文) |
| 94 | MGRPHY_GRNSZ_LEVEL | NUMBER | Y |  | 金相测试晶粒度级别 | DB注释(中文) |
| 95 | MGRPHY_GRNSZ_OCCP | NUMBER | Y |  | 金相测试基相晶粒的体积分数 | DB注释(中文) |
| 96 | MGRPHY_FGS_MIXED_RATIO_RSLT | NUMBER | Y |  | 铁素体晶粒混晶占有率实绩 | DB注释(中文) |
| 97 | MGRPHY_FGS_MIXED_RATIO_JDG | VARCHAR2(1) | Y |  | 铁素体晶粒混晶占有率判定 | DB注释(中文) |
| 98 | MGRPHY_FGS_DEVT_MAX_RSLT | NUMBER | Y |  | 铁素体混晶晶粒度差实绩 | DB注释(中文) |
| 99 | MGRPHY_FGS_DEVT_MAX_JDG | VARCHAR2(1) | Y |  | 铁素体混晶晶粒度差判定 | DB注释(中文) |
| 100 | MGRPHY_FGS_RSLT | NUMBER | Y |  | 铁素体晶粒尺寸实绩 | DB注释(中文) |
| 101 | MGRPHY_FGS_JDG | VARCHAR2(1) | Y |  | 铁素体晶粒尺寸判定 | DB注释(中文) |
| 102 | MGRPHY_AGS_RSLT | NUMBER | Y |  | 奥氏体晶粒尺寸实绩 | DB注释(中文) |
| 103 | MGRPHY_AGS_JDG | VARCHAR2(1) | Y |  | 奥氏体晶粒尺寸判定 | DB注释(中文) |
| 104 | MGRPHY_INCLD_TY | VARCHAR2(1) | Y |  | 夹杂物类别 | DB注释(中文) |
| 105 | MGRPHY_INCLD_GRD_MAX_RSLT | NUMBER | Y |  | 夹杂物等级上限实绩 | DB注释(中文) |
| 106 | MGRPHY_INCLD_GRD_MAX_JDG | VARCHAR2(1) | Y |  | 夹杂物等级上限实绩 | DB注释(中文) |
| 107 | MGRPHY_DECARBON_MAX_RSLT | NUMBER | Y |  | 脱碳层上限实绩 | DB注释(中文) |
| 108 | MGRPHY_DECARBON_MAX_JDG | VARCHAR2(1) | Y |  | 脱碳层上限实绩 | DB注释(中文) |
| 109 | MGRPHY_WILD_STRC_GRD | NUMBER | Y |  | 魏氏组织等级 | DB注释(中文) |
| 110 | MGRPHY_WILD_STRC_JDG | VARCHAR2(1) | Y |  | 魏氏组织判定 | DB注释(中文) |
| 111 | MGRPHY_MTLGRP_TY | VARCHAR2(2) | Y |  | 组织类型 | DB注释(中文) |
| 112 | MGRPHY_BAND_STRC_GRD_MAX_RSLT | NUMBER | Y |  | 带状组织等级上限实绩 | DB注释(中文) |
| 113 | MGRPHY_BAND_STRC_GRD_MAX_JDG | VARCHAR2(1) | Y |  | 带状组织等级上限判定 | DB注释(中文) |
| 114 | MGRPHY_RAT_TESTER_CD | VARCHAR2(20) | Y |  | 金相试验粒度组织分类试验机代码 | DB注释(中文) |
| 115 | MGRPHY_RAT_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 金相试验粒度组织分类试验人ID | DB注释(中文) |
| 116 | NON_METAL_GRD_KIND_CD | VARCHAR2(2) | Y |  | 非金属夹杂物级别 | DB注释(中文) |
| 117 | NON_METAL_A_RSLT | NUMBER | Y |  | 非金属夹杂物A类实绩(粗) | DB注释(中文) |
| 118 | NON_METAL_A_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物A类判定(粗) | DB注释(中文) |
| 119 | NON_METAL_B_RSLT | NUMBER | Y |  | 非金属夹杂物B类实绩(粗) | DB注释(中文) |
| 120 | NON_METAL_B_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物B类判定(粗) | DB注释(中文) |
| 121 | NON_METAL_C_RSLT | NUMBER | Y |  | 非金属夹杂物C类实绩(粗) | DB注释(中文) |
| 122 | NON_METAL_C_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物C类判定(粗) | DB注释(中文) |
| 123 | NON_METAL_D_RSLT | NUMBER | Y |  | 非金属夹杂物D类实绩(粗) | DB注释(中文) |
| 124 | NON_METAL_D_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物D类判定(粗) | DB注释(中文) |
| 125 | NON_METAL_DS_RSLT | NUMBER | Y |  | 非金属夹杂物Ds实绩 | DB注释(中文) |
| 126 | NON_METAL_DS_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物Ds判定 | DB注释(中文) |
| 127 | NON_METAL_A1_RSLT | NUMBER | Y |  | 非金属夹杂物A1类实绩(细) | DB注释(中文) |
| 128 | NON_METAL_A1_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物A1类判定(细) | DB注释(中文) |
| 129 | NON_METAL_B1_RSLT | NUMBER | Y |  | 非金属夹杂物B1类实绩(细) | DB注释(中文) |
| 130 | NON_METAL_B1_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物B1类判定(细) | DB注释(中文) |
| 131 | NON_METAL_C1_RSLT | NUMBER | Y |  | 非金属夹杂物C1类实绩(细) | DB注释(中文) |
| 132 | NON_METAL_C1_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物C1类判定(细) | DB注释(中文) |
| 133 | NON_METAL_D1_RSLT | NUMBER | Y |  | 非金属夹杂物D1类实绩(细) | DB注释(中文) |
| 134 | NON_METAL_D1_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物D1类判定(细) | DB注释(中文) |
| 135 | NON_METAL_DS1_RSLT | NUMBER | Y |  | 非金属夹杂物Ds1实绩 | DB注释(中文) |
| 136 | NON_METAL_DS1_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物Ds1判定 | DB注释(中文) |
| 137 | NON_METAL_ABCD_RSLT | NUMBER | Y |  | 非金属夹杂物A+B+C+D实绩(粗) | DB注释(中文) |
| 138 | NON_METAL_ABCD_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物ABCD判定(粗) | DB注释(中文) |
| 139 | NON_METAL_MAX_WTH_RSLT | NUMBER | Y |  | 非金属夹杂物测试最大宽度实绩 | DB注释(中文) |
| 140 | NON_METAL_MAX_LTH_RSLT | NUMBER | Y |  | 非金属夹杂物测试最大长度实绩 | DB注释(中文) |
| 141 | NON_METAL_TESTER_CD | VARCHAR2(20) | Y |  | 非金属夹杂物试验机代码 | DB注释(中文) |
| 142 | NON_METAL_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 非金属夹杂物试验人ID | DB注释(中文) |
| 143 | S_PRINT_KIND | VARCHAR2(1) | Y |  | S_Print试验种类 | DB注释(中文) |
| 144 | S_PRINT_GRD_RSLT | VARCHAR2(1) | Y |  | 硫印测试等级实绩 | DB注释(中文) |
| 145 | S_PRINT_GRD_JDG | VARCHAR2(1) | Y |  | 硫印测试等级判定 | DB注释(中文) |
| 146 | S_PRINT_TESTER_CD | VARCHAR2(20) | Y |  | S_Print试验机代码 | DB注释(中文) |
| 147 | S_PRINT_DUTY_EMP_ID | VARCHAR2(20) | Y |  | S_Print试验人ID | DB注释(中文) |
| 148 | P_PRINT_GRD_RSLT | VARCHAR2(1) | Y |  | 磷印测试等级实绩 | DB注释(中文) |
| 149 | P_PRINT_GRD_JDG | VARCHAR2(1) | Y |  | 磷印测试等级判定 | DB注释(中文) |
| 150 | P_PRINT_TESTER_CD | VARCHAR2(20) | Y |  | P_Print试验机代码 | DB注释(中文) |
| 151 | P_PRINT_DUTY_EMP_ID | VARCHAR2(20) | Y |  | P_Print试验人ID | DB注释(中文) |
| 152 | P_SGRG_GRD_RSLT | VARCHAR2(1) | Y |  | 磷偏析测试等级实绩 | DB注释(中文) |
| 153 | P_SGRG_GRD_JDG | VARCHAR2(1) | Y |  | 磷偏析测试等级判定 | DB注释(中文) |
| 154 | P_SGRG_TESTER_CD | VARCHAR2(20) | Y |  | 磷偏析试验机代码 | DB注释(中文) |
| 155 | P_SGRG_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 磷偏析测试人ID | DB注释(中文) |
| 156 | C_SGRG_KIND | VARCHAR2(1) | Y |  | 碳偏析测试种类 | DB注释(中文) |
| 157 | C_SGRG_SMP_GRD_RSLT | VARCHAR2(1) | Y |  | 碳偏析测试上限等级实绩 | DB注释(中文) |
| 158 | C_SGRG_SMP_GRD_JDG | VARCHAR2(1) | Y |  | 碳偏析测试上限等级判定 | DB注释(中文) |
| 159 | HIC_SOLUTION_KIND | VARCHAR2(1) | Y |  | HIC测试溶液种类 | DB注释(中文) |
| 160 | HIC_CLR_EACH_RSLT | NUMBER | Y |  | HIC测试CLR单个实绩 | DB注释(中文) |
| 161 | HIC_CLR_EACH_JDG | VARCHAR2(1) | Y |  | HIC测试CLR单个判定 | DB注释(中文) |
| 162 | HIC_CLR_SPCMN_AVG1_RSLT | NUMBER | Y |  | HIC测试CLR试样平均1实绩 | DB注释(中文) |
| 163 | HIC_CLR_SPCMN_AVG2_RSLT | NUMBER | Y |  | HIC测试CLR试样平均2实绩 | DB注释(中文) |
| 164 | HIC_CLR_SPCMN_AVG3_RSLT | NUMBER | Y |  | HIC测试CLR试样平均3实绩 | DB注释(中文) |
| 165 | HIC_CLR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CLR试样平均判定 | DB注释(中文) |
| 166 | HIC_CLR_TOT_AVG_RSLT | NUMBER | Y |  | HIC测试CLR全体平均实绩 | DB注释(中文) |
| 167 | HIC_CLR_TOT_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CLR全体平均判定 | DB注释(中文) |
| 168 | HIC_CSR_EACH_RSLT | NUMBER | Y |  | HIC测试CSR单个实绩 | DB注释(中文) |
| 169 | HIC_CSR_EACH_JDG | VARCHAR2(1) | Y |  | HIC测试CSR单个判定 | DB注释(中文) |
| 170 | HIC_CSR_SPCMN_AVG1_RSLT | NUMBER | Y |  | HIC测试CSR试样平均1实绩 | DB注释(中文) |
| 171 | HIC_CSR_SPCMN_AVG2_RSLT | NUMBER | Y |  | HIC测试CSR试样平均2实绩 | DB注释(中文) |
| 172 | HIC_CSR_SPCMN_AVG3_RSLT | NUMBER | Y |  | HIC测试CSR试样平均3实绩 | DB注释(中文) |
| 173 | HIC_CSR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CSR试样平均判定 | DB注释(中文) |
| 174 | HIC_CSR_TOT_AVG_RSLT | NUMBER | Y |  | HIC测试CSR全体平均实绩 | DB注释(中文) |
| 175 | HIC_CSR_TOT_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CSR全体平均判定 | DB注释(中文) |
| 176 | HIC_CTR_EACH_RSLT | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 177 | HIC_CTR_EACH_JDG | VARCHAR2(1) | Y |  | HIC测试CTR单个判定 | DB注释(中文) |
| 178 | HIC_CTR_SPCMN_AVG1_RSLT | NUMBER | Y |  | HIC测试CTR试样平均1实绩 | DB注释(中文) |
| 179 | HIC_CTR_SPCMN_AVG2_RSLT | NUMBER | Y |  | HIC测试CTR试样平均2实绩 | DB注释(中文) |
| 180 | HIC_CTR_SPCMN_AVG3_RSLT | NUMBER | Y |  | HIC测试CTR试样平均3实绩 | DB注释(中文) |
| 181 | HIC_CTR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CTR试样平均判定 | DB注释(中文) |
| 182 | HIC_CTR_TOT_AVG_RSLT | NUMBER | Y |  | HIC测试CTR全体平均实绩 | DB注释(中文) |
| 183 | HIC_CTR_TOT_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CTR全体平均判定 | DB注释(中文) |
| 184 | HIC_TESTER_CD | VARCHAR2(20) | Y |  | HIC试验机代码 | DB注释(中文) |
| 185 | HIC_DUTY_EMP_ID | VARCHAR2(20) | Y |  | HIC试验人ID | DB注释(中文) |
| 186 | SSCC_SOLUTION_KIND | VARCHAR2(1) | Y |  | SSCC测试溶液种类 | DB注释(中文) |
| 187 | SSCC_STRESS_TY | VARCHAR2(1) | Y |  | SSCC测试应力区分 | DB注释(中文) |
| 188 | SSCC_KIND | VARCHAR2(1) | Y |  | SSCC测试种类 | DB注释(中文) |
| 189 | SSCC_STRESS_RATIO_RSLT | NUMBER | Y |  | SSCC测试应力比实绩 | DB注释(中文) |
| 190 | SSCC_STRESS_RATIO_JDG | VARCHAR2(1) | Y |  | SSCC测试应力比判定 | DB注释(中文) |
| 191 | SSCC_TIME | NUMBER | Y |  | SSCC测试时间 | DB注释(中文) |
| 192 | SSCC_TIME_RSLT | NUMBER | Y |  | SSCC测试时间实绩 | DB注释(中文) |
| 193 | SSCC_TIME_JDG | VARCHAR2(1) | Y |  | SSCC测试时间判定 | DB注释(中文) |
| 194 | SSCC_TESTER_CD | VARCHAR2(20) | Y |  | SSCC试验机代码 | DB注释(中文) |
| 195 | SSCC_DUTY_EMP_ID | VARCHAR2(20) | Y |  | SSCC试验人ID | DB注释(中文) |
| 196 | HIGH_TEMP_TSL_TEMP | NUMBER | Y |  | 高温拉伸测试温度 | DB注释(中文) |
| 197 | HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  | 高温拉伸测试屈服强度类型 | DB注释(中文) |
| 198 | HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  | 高温拉伸测试屈服强度实绩 | DB注释(中文) |
| 199 | HIGH_TEMP_TSL_YP_JDG | VARCHAR2(1) | Y |  | 高温拉伸测试屈服强度判定 | DB注释(中文) |
| 200 | HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  | 高温拉伸测试抗拉强度实绩 | DB注释(中文) |
| 201 | HIGH_TEMP_TSL_TS_JDG | VARCHAR2(1) | Y |  | 高温拉伸测试抗拉强度判定 | DB注释(中文) |
| 202 | HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  | 高温拉伸测试伸长率类型 | DB注释(中文) |
| 203 | HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  | 高温拉伸测试伸长率实绩 | DB注释(中文) |
| 204 | HIGH_TEMP_TSL_EL_JDG | VARCHAR2(1) | Y |  | 高温拉伸测试伸长率判定 | DB注释(中文) |
| 205 | HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  | 高温拉伸测试断面收缩率实绩 | DB注释(中文) |
| 206 | HIGH_TEMP_TSL_RA_JDG | VARCHAR2(1) | Y |  | 高温拉伸测试断面收缩率判定 | DB注释(中文) |
| 207 | HIGH_TSL_TESTER_CD | VARCHAR2(20) | Y |  | 高温拉伸试验机代码 | DB注释(中文) |
| 208 | HIGH_TSL_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 高温拉伸试验人ID | DB注释(中文) |
| 209 | EXT_HOLE_SPCMN_CNT | NUMBER | Y |  | 扩孔测试试样数量 | DB注释(中文) |
| 210 | EXT_HOLE_RATIO_AVG_RSLT | NUMBER | Y |  | 扩孔测试极限扩孔率平均实绩 | DB注释(中文) |
| 211 | EXT_HOLE_RATIO_AVG_JDG | VARCHAR2(1) | Y |  | 扩孔测试极限扩孔率平均判定 | DB注释(中文) |
| 212 | EXT_HOLE_RATIO_EACH_RSLT1 | NUMBER | Y |  | 扩孔测试极限扩孔率单个实绩1 | DB注释(中文) |
| 213 | EXT_HOLE_RATIO_EACH_RSLT2 | NUMBER | Y |  | 扩孔测试极限扩孔率单个实绩2 | DB注释(中文) |
| 214 | EXT_HOLE_RATIO_EACH_RSLT3 | NUMBER | Y |  | 扩孔测试极限扩孔率单个实绩3 | DB注释(中文) |
| 215 | BH_RSLT | NUMBER | Y |  | 烘烤硬化值测试实绩 | DB注释(中文) |
| 216 | BH_JDG | VARCHAR2(1) | Y |  | 烘烤硬化值测试判定 | DB注释(中文) |
| 217 | BH_TESTER_CD | VARCHAR2(20) | Y |  | 烘烤硬化试验机代码 | DB注释(中文) |
| 218 | BH_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 烘烤硬化试验人ID | DB注释(中文) |
| 219 | FATIG_SPCMN_CNT | NUMBER | Y |  | 疲劳测试试样数量 | DB注释(中文) |
| 220 | FATIG_TEMP_RSLT | NUMBER | Y |  | 疲劳测试温度实绩 | DB注释(中文) |
| 221 | FATIG_TEMP_JDG | VARCHAR2(1) | Y |  | 疲劳测试温度判定 | DB注释(中文) |
| 222 | FATIG_FREQ_RSLT | NUMBER | Y |  | 疲劳测试频率实绩 | DB注释(中文) |
| 223 | FATIG_FREQ_JDG | VARCHAR2(1) | Y |  | 疲劳测试频率判定 | DB注释(中文) |
| 224 | FATIG_SERV_LIFE_RSLT | NUMBER | Y |  | 疲劳寿命实绩 | DB注释(中文) |
| 225 | FATIG_SERV_LIFE_JDG | VARCHAR2(1) | Y |  | 疲劳寿命判定 | DB注释(中文) |
| 226 | FATIG_CND_STRTH_RSLT | NUMBER | Y |  | 条件疲劳强度实绩 | DB注释(中文) |
| 227 | FATIG_CND_STRTH_JDG | VARCHAR2(1) | Y |  | 条件疲劳强度判定 | DB注释(中文) |
| 228 | CLEAN1_KIND | VARCHAR2(1) | Y |  | 清净度测试1种类 | DB注释(中文) |
| 229 | CLEAN1_RSLT | NUMBER | Y |  | 清净度测试1实绩 | DB注释(中文) |
| 230 | CLEAN1_JDG | VARCHAR2(1) | Y |  | 清净度测试1判定 | DB注释(中文) |
| 231 | CLEAN2_KIND | VARCHAR2(1) | Y |  | 清净度测试2种类 | DB注释(中文) |
| 232 | CLEAN2_RSLT | NUMBER | Y |  | 清净度测试2实绩 | DB注释(中文) |
| 233 | CLEAN2_JDG | VARCHAR2(1) | Y |  | 清净度测试2判定 | DB注释(中文) |
| 234 | CLEAN3_KIND | VARCHAR2(1) | Y |  | 清净度测试3种类 | DB注释(中文) |
| 235 | CLEAN3_RSLT | NUMBER | Y |  | 清净度测试3实绩 | DB注释(中文) |
| 236 | CLEAN3_JDG | VARCHAR2(1) | Y |  | 清净度测试3判定 | DB注释(中文) |
| 237 | CLEAN_TESTER_CD | VARCHAR2(20) | Y |  | 洁净度试验机代码 | DB注释(中文) |
| 238 | CLEAN_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 洁净度试验人ID | DB注释(中文) |
| 239 | ROUGH_KIND | VARCHAR2(1) | Y |  | 粗糙度测试种类 | DB注释(中文) |
| 240 | ROUGH_DIR | VARCHAR2(1) | Y |  | 粗糙度测试方向 | DB注释(中文) |
| 241 | ROUGH_RA_RSLT | NUMBER | Y |  | 表面平均粗糙度实绩(Ra) | DB注释(中文) |
| 242 | ROUGH_RA_JDG | VARCHAR2(1) | Y |  | 表面平均粗糙度判定(Ra) | DB注释(中文) |
| 243 | ROUGH_RPC_RSLT | NUMBER | Y |  | 单位长度内峰值个数实绩(Rpc) | DB注释(中文) |
| 244 | ROUGH_RPC_JDG | VARCHAR2(1) | Y |  | 单位长度内峰值个数判定(Rpc) | DB注释(中文) |
| 245 | ROUGH_RMAX_RSLT | NUMBER | Y |  | 表面粗糙度最大值实绩(Rmax) | DB注释(中文) |
| 246 | ROUGH_RMAX_JDG | VARCHAR2(1) | Y |  | 表面粗糙度最大值判定(Rmax) | DB注释(中文) |
| 247 | ROUGH_TESTER_CD | VARCHAR2(20) | Y |  | 粗糙度测试机代码 | DB注释(中文) |
| 248 | ROUGH_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 粗糙度测试试验人ID | DB注释(中文) |
| 249 | QLT_REMARKS | VARCHAR2(300) | Y |  | 质量备注 | DB注释(中文) |
| 250 | PROD_CHEM_SMP_CND | VARCHAR2(2) | Y |  | 产品成分分析取样条件 | DB注释(中文) |
| 251 | PROD_CHEM_ANAL_TY | VARCHAR2(1) | Y |  | 产品成分分析区分 | DB注释(中文) |
| 252 | C_RSLT | VARCHAR2(20) | Y |  | 产品成分C实绩 | DB注释(中文) |
| 253 | SI_RSLT | VARCHAR2(20) | Y |  | 产品成分Si实绩 | DB注释(中文) |
| 254 | MN_RSLT | VARCHAR2(20) | Y |  | 产品成分Mn实绩 | DB注释(中文) |
| 255 | P_RSLT | VARCHAR2(20) | Y |  | 产品成分P实绩 | DB注释(中文) |
| 256 | S_RSLT | VARCHAR2(20) | Y |  | 产品成分S实绩 | DB注释(中文) |
| 257 | SAL_RSLT | VARCHAR2(20) | Y |  | 产品成分Sol_Al实绩 | DB注释(中文) |
| 258 | TAL_RSLT | VARCHAR2(20) | Y |  | 产品成分Tot_Al实绩 | DB注释(中文) |
| 259 | AS_RSLT | VARCHAR2(20) | Y |  | 产品成分As实绩 | DB注释(中文) |
| 260 | BI_RSLT | VARCHAR2(20) | Y |  | 产品成分Bi实绩 | DB注释(中文) |
| 261 | B_RSLT | VARCHAR2(20) | Y |  | 产品成分B实绩 | DB注释(中文) |
| 262 | CA_RSLT | VARCHAR2(20) | Y |  | 产品成分Ca实绩 | DB注释(中文) |
| 263 | CO_RSLT | VARCHAR2(20) | Y |  | 产品成分Co实绩 | DB注释(中文) |
| 264 | CR_RSLT | VARCHAR2(20) | Y |  | 产品成分Cr实绩 | DB注释(中文) |
| 265 | CU_RSLT | VARCHAR2(20) | Y |  | 产品成分Cu实绩 | DB注释(中文) |
| 266 | H_RSLT | VARCHAR2(20) | Y |  | 产品成分H实绩 | DB注释(中文) |
| 267 | MG_RSLT | VARCHAR2(20) | Y |  | 产品成分Mg实绩 | DB注释(中文) |
| 268 | MO_RSLT | VARCHAR2(20) | Y |  | 产品成分Mo实绩 | DB注释(中文) |
| 269 | NB_RSLT | VARCHAR2(20) | Y |  | 产品成分Nb实绩 | DB注释(中文) |
| 270 | NI_RSLT | VARCHAR2(20) | Y |  | 产品成分Ni实绩 | DB注释(中文) |
| 271 | N_RSLT | VARCHAR2(20) | Y |  | 产品成分N实绩 | DB注释(中文) |
| 272 | O_RSLT | VARCHAR2(20) | Y |  | 产品成分O实绩 | DB注释(中文) |
| 273 | PB_RSLT | VARCHAR2(20) | Y |  | 产品成分Pb实绩 | DB注释(中文) |
| 274 | SB_RSLT | VARCHAR2(20) | Y |  | 产品成分Sb实绩 | DB注释(中文) |
| 275 | SN_RSLT | VARCHAR2(20) | Y |  | 产品成分Sn实绩 | DB注释(中文) |
| 276 | TE_RSLT | VARCHAR2(20) | Y |  | 产品成分Te实绩 | DB注释(中文) |
| 277 | TI_RSLT | VARCHAR2(20) | Y |  | 产品成分Ti实绩 | DB注释(中文) |
| 278 | V_RSLT | VARCHAR2(20) | Y |  | 产品成分V实绩 | DB注释(中文) |
| 279 | W_RSLT | VARCHAR2(20) | Y |  | 产品成分W实绩 | DB注释(中文) |
| 280 | ZN_RSLT | VARCHAR2(20) | Y |  | 产品成分Zn实绩 | DB注释(中文) |
| 281 | ZR_RSLT | VARCHAR2(20) | Y |  | 产品成分Zr实绩 | DB注释(中文) |
| 282 | CEQ_RSLT | VARCHAR2(20) | Y |  | 产品成分CEQ计算值 | DB注释(中文) |
| 283 | PCM_RSLT | VARCHAR2(20) | Y |  | 产品成分PCM计算值 | DB注释(中文) |
| 284 | CREQ_RSLT | VARCHAR2(20) | Y |  | 产品成分CrEq计算值 | DB注释(中文) |
| 285 | PROD_CHEM_TESTER_CD | VARCHAR2(20) | Y |  | 产品成分试验机代码 | DB注释(中文) |
| 286 | PROD_CHEM_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 产品成分试验人ID | DB注释(中文) |
| 287 | SPL_OCR_DTM | VARCHAR2(14) | Y |  | 余材发生时间 | DB注释(中文) |
| 288 | OIL_MTH_CD | VARCHAR2(2) | Y |  | 涂油方法代码 | DB注释(中文) |
| 289 | OIL_WGT_RSLT | NUMBER | Y |  | 涂油量测试双面涂油量实绩 | DB注释(中文) |
| 290 | OIL_WGT_JDG | VARCHAR2(1) | Y |  | 涂油量测试双面涂油量判定 | DB注释(中文) |
| 291 | OIL_WGT_UPPER_RSLT | NUMBER | Y |  | 涂油量测试上表面涂油量实绩 | DB注释(中文) |
| 292 | OIL_WGT_UPPER_JDG | VARCHAR2(1) | Y |  | 涂油量测试上表面涂油量判定 | DB注释(中文) |
| 293 | OIL_WGT_LOWER_RSLT | NUMBER | Y |  | 涂油量测试下表面涂油量实绩 | DB注释(中文) |
| 294 | OIL_WGT_LOWER_JDG | VARCHAR2(1) | Y |  | 涂油量测试下表面涂油量判定 | DB注释(中文) |
| 295 | OIL_WGT_TESTER_CD | VARCHAR2(20) | Y |  | 涂油量试验机代码 | DB注释(中文) |
| 296 | OIL_WGT_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 涂油量试验人ID | DB注释(中文) |
| 297 | ERICHSEN_RSLT | NUMBER | Y |  | 杯突测试 | DB注释(中文) |
| 298 | ERICHSEN_JDG | VARCHAR2(1) | Y |  | 杯突测试判定 | DB注释(中文) |
| 299 | ERICHSEN_TESTER_CD | VARCHAR2(20) | Y |  | Erichsen试验机代码 | DB注释(中文) |
| 300 | ERICHSEN_DUTY_EMP_ID | VARCHAR2(20) | Y |  | Erichsen试验人ID | DB注释(中文) |
| 301 | WAVIN_TY | VARCHAR2(1) | Y |  | 波纹度测试种类 | DB注释(中文) |
| 302 | WAVIN_WA_RSLT | NUMBER | Y |  | 波纹度检测实绩(Wa) | DB注释(中文) |
| 303 | WAVIN_WA_JDG | VARCHAR2(1) | Y |  | 波纹度检测判定(Wa) | DB注释(中文) |
| 304 | WAVIN_WMAX_RSLT | NUMBER | Y |  | 波纹度检测最大值实绩(Wmax) | DB注释(中文) |
| 305 | WAVIN_WMAX_JDG | VARCHAR2(1) | Y |  | 波纹度检测最大值判定(Wmax) | DB注释(中文) |
| 306 | WAVIN_TESTER_CD | VARCHAR2(20) | Y |  | 波纹度检测 | DB注释(中文) |
| 307 | WAVIN_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 波纹度检测 | DB注释(中文) |
| 308 | SPRBCK_CD | VARCHAR2(1) | Y |  | 回弹测试方法 | DB注释(中文) |
| 309 | SPRBCK_DEGR_RSLT | NUMBER | Y |  | 回弹角实绩 | DB注释(中文) |
| 310 | SPRBCK_DEGR_JDG | VARCHAR2(1) | Y |  | 回弹角判定 | DB注释(中文) |
| 311 | SPRBCK_RSLT | NUMBER | Y |  | 回弹测试实绩 | DB注释(中文) |
| 312 | SPRBCK_JDG | VARCHAR2(1) | Y |  | 回弹测试判定 | DB注释(中文) |
| 313 | HPT_ADMI_TIME_RSLT | NUMBER | Y |  | 氢扩散达到稳定所需时间实绩 | DB注释(中文) |
| 314 | HPT_ADMI_TIME_JDG | VARCHAR2(1) | Y |  | 氢扩散达到稳定所需时间判定 | DB注释(中文) |
| 315 | HPT_TESTER_CD | VARCHAR2(20) | Y |  | 氢渗透试验机代码 | DB注释(中文) |
| 316 | HPT_DUTY_EMP_ID | VARCHAR2(20) | Y |  | 氢渗透试验人ID | DB注释(中文) |
| 317 | EXT_HOLE_RATIO_DIAM_MAX_RSLT | NUMBER | Y |  | 扩孔测试极限扩孔直径最大值 | DB注释(中文) |
| 318 | EXT_HOLE_RATIO_DIAM_MIN_RSLT | NUMBER | Y |  | 扩孔测试极限扩孔直径最小值 | DB注释(中文) |
| 319 | EXT_HOLE_RATIO_DIAM_AVG_RSLT | NUMBER | Y |  | 扩孔测试极限扩孔直径平均值 | DB注释(中文) |
| 320 | NON_METAL_ABCD1_RSLT | NUMBER | Y |  | 非金属夹杂物A+B+C+D实绩(细) | DB注释(中文) |
| 321 | NON_METAL_ABCD1_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物ABCD判定(细) | DB注释(中文) |
| 322 | ROUGH_RY_RSLT | NUMBER | Y |  | 轮廓最大高度实绩(Ry) | DB注释(中文) |
| 323 | ROUGH_RY_JDG | VARCHAR2(1) | Y |  | 轮廓最大高度判定(Ry) | DB注释(中文) |
| 324 | ROUGH_RZ_RSLT | NUMBER | Y |  | 微观不平度十点高度实绩(Rz) | DB注释(中文) |
| 325 | ROUGH_RZ_JDG | VARCHAR2(1) | Y |  | 微观不平度十点高度判定(Rz) | DB注释(中文) |
| 326 | WAVIN_WSA_RSLT | NUMBER | Y |  | 波纹度检测实绩(Wsa) | DB注释(中文) |
| 327 | WAVIN_WSA_JDG | VARCHAR2(1) | Y |  | 波纹度检测判定(Wsa) | DB注释(中文) |
| 328 | WAVIN_WSAMAX_RSLT | NUMBER | Y |  | 波纹度检测最大值实绩(Wsamax) | DB注释(中文) |
| 329 | WAVIN_WSAMAX_JDG | VARCHAR2(1) | Y |  | 波纹度检测最大值判定(Wsamax) | DB注释(中文) |
| 330 | WAVIN_WCA_RSLT | NUMBER | Y |  | 波纹度检测实绩(Wca) | DB注释(中文) |
| 331 | WAVIN_WCA_JDG | VARCHAR2(1) | Y |  | 波纹度检测判定(Wca) | DB注释(中文) |
| 332 | WAVIN_WCAMAX_RSLT | NUMBER | Y |  | 波纹度检测最大值实绩(Wcamax) | DB注释(中文) |
| 333 | WAVIN_WCAMAX_JDG | VARCHAR2(1) | Y |  | 波纹度检测最大值判定(Wcamax) | DB注释(中文) |
| 334 | WAVIN_WA08_RSLT | NUMBER | Y |  | 波纹度检测实绩(Wa08) | DB注释(中文) |
| 335 | WAVIN_WA08_JDG | VARCHAR2(1) | Y |  | 波纹度检测判定(Wa08) | DB注释(中文) |
| 336 | WAVIN_WA08MAX_RSLT | NUMBER | Y |  | 波纹度检测最大值实绩(Wa08max) | DB注释(中文) |
| 337 | WAVIN_WA08MAX_JDG | VARCHAR2(1) | Y |  | 波纹度检测最大值判定(Wa08max) | DB注释(中文) |
| 338 | DWTT_ABSP_IND_RSLT1 | NUMBER | Y |  | DWTT测试吸收能量单个实绩1 | DB注释(中文) |
| 339 | DWTT_ABSP_IND_RSLT2 | NUMBER | Y |  | DWTT测试吸收能量单个实绩2 | DB注释(中文) |
| 340 | MGRPHY_GRNSZ_LEVEL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 341 | HARD_RSLT4 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 342 | HARD_RSLT5 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 343 | HARD_RSLT6 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 344 | HARD_RSLT7 | NUMBER | Y |  | 硬度测试实绩7 | DB注释(中文) |
| 345 | HARD_RSLT8 | NUMBER | Y |  | 硬度测试实绩8 | DB注释(中文) |
| 346 | HARD_RSLT9 | NUMBER | Y |  | 硬度测试实绩9 | DB注释(中文) |
| 347 | SR_TSL_YP_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度类型 | DB注释(中文) |
| 348 | SR_TSL_YP_RSLT | NUMBER | Y |  | 拉伸测试屈服强度实绩 | DB注释(中文) |
| 349 | SR_TSL_YP_JDG | VARCHAR2(1) | Y |  | 拉伸测试屈服强度判定 | DB注释(中文) |
| 350 | SR_TSL_TS_RSLT | NUMBER | Y |  | 拉伸测试抗拉强度实绩 | DB注释(中文) |
| 351 | SR_TSL_TS_JDG | VARCHAR2(1) | Y |  | 拉伸测试抗拉强度判定 | DB注释(中文) |
| 352 | SR_TSL_EL_CD | VARCHAR2(1) | Y |  | 拉伸测试伸长率类型 | DB注释(中文) |
| 353 | SR_TSL_EL_RSLT | NUMBER | Y |  | 拉伸测试伸长率实绩 | DB注释(中文) |
| 354 | SR_TSL_EL_JDG | VARCHAR2(1) | Y |  | 拉伸测试伸长率判定 | DB注释(中文) |
| 355 | SR_TSL_EL_UNF_RSLT | NUMBER | Y |  | 拉抻测试均匀延伸率(uEL)实绩 | DB注释(中文) |
| 356 | SR_TSL_EL_UNF_JDG | VARCHAR2(1) | Y |  | 拉抻测试均匀延伸率(uEL)判定 | DB注释(中文) |
| 357 | SR_TSL_YR_RSLT | NUMBER | Y |  | 拉伸测试屈强比实绩 | DB注释(中文) |
| 358 | SR_TSL_YR_JDG | VARCHAR2(1) | Y |  | 拉伸测试屈强比判定 | DB注释(中文) |
| 359 | SR_TSL_RA_RSLT | NUMBER | Y |  | 拉伸测试断面收缩率实绩 | DB注释(中文) |
| 360 | SR_TSL_RA_JDG | VARCHAR2(1) | Y |  | 拉伸测试断面收缩率判定 | DB注释(中文) |
| 361 | SR_TSL_R_RSLT | NUMBER | Y |  | 拉抻测试塑性应变比r平均实绩 | DB注释(中文) |
| 362 | SR_TSL_R_JDG | VARCHAR2(1) | Y |  | 拉抻测试塑性应变比r平均判定 | DB注释(中文) |
| 363 | SR_TSL_R0_RSLT | NUMBER | Y |  | 拉抻测试r0实绩 | DB注释(中文) |
| 364 | SR_TSL_R0_JDG | VARCHAR2(1) | Y |  | 拉抻测试r0判定 | DB注释(中文) |
| 365 | SR_TSL_R45_RSLT | NUMBER | Y |  | 拉抻测试r45实绩 | DB注释(中文) |
| 366 | SR_TSL_R45_JDG | VARCHAR2(1) | Y |  | 拉抻测试r45判定 | DB注释(中文) |
| 367 | SR_TSL_R90_RSLT | NUMBER | Y |  | 拉抻测试r90实绩 | DB注释(中文) |
| 368 | SR_TSL_R90_JDG | VARCHAR2(1) | Y |  | 拉抻测试r90判定 | DB注释(中文) |
| 369 | SR_TSL_RDELTA_RSLT | NUMBER | Y |  | 拉伸测试\|Δr\|实绩 | DB注释(中文) |
| 370 | SR_TSL_RDELTA_JDG | VARCHAR2(1) | Y |  | 拉伸测试\|Δr\|判定 | DB注释(中文) |
| 371 | SR_TSL_N_RSLT | NUMBER | Y |  | 拉伸测试加工硬化指数n平均实绩 | DB注释(中文) |
| 372 | SR_TSL_N_JDG | VARCHAR2(1) | Y |  | 拉伸测试加工硬化指数n平均判定 | DB注释(中文) |
| 373 | SR_TSL_N0_RSLT | NUMBER | Y |  | 拉抻测试N0实绩 | DB注释(中文) |
| 374 | SR_TSL_N0_JDG | VARCHAR2(1) | Y |  | 拉抻测试n0判定 | DB注释(中文) |
| 375 | SR_TSL_N45_RSLT | NUMBER | Y |  | 拉抻测试N45实绩 | DB注释(中文) |
| 376 | SR_TSL_N45_JDG | VARCHAR2(1) | Y |  | 拉抻测试n45判定 | DB注释(中文) |
| 377 | SR_TSL_N90_RSLT | NUMBER | Y |  | 拉抻测试N90实绩 | DB注释(中文) |
| 378 | SR_TSL_N90_JDG | VARCHAR2(1) | Y |  | 拉抻测试n90判定 | DB注释(中文) |
| 379 | SR_BEND_CD | VARCHAR2(1) | Y |  | 弯曲测试角度 | DB注释(中文) |
| 380 | SR_BEND_UNIT | VARCHAR2(1) | Y |  | 弯曲压头直径 | DB注释(中文) |
| 381 | SR_BEND_ANGLE | NUMBER | Y |  | 弯曲测试弯曲角度 | DB注释(中文) |
| 382 | SR_BEND_DIA | NUMBER | Y |  | 弯曲测试弯心直径 | DB注释(中文) |
| 383 | SR_BEND_RSLT | VARCHAR2(1) | Y |  | 弯曲测试实绩 | DB注释(中文) |
| 384 | SR_BEND_JDG | VARCHAR2(1) | Y |  | 弯曲测试判定 | DB注释(中文) |
| 385 | SR_IMPACT_SPCMN_CNT | NUMBER | Y |  | 冲击测试试样数量 | DB注释(中文) |
| 386 | SR_IMPACT_TEMP | NUMBER | Y |  | 冲击测试温度 | DB注释(中文) |
| 387 | SR_IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 冲击测试缺口类型 | DB注释(中文) |
| 388 | SR_IMPACT_AVG_RSLT | NUMBER | Y |  | 冲击测试吸收能量实绩 | DB注释(中文) |
| 389 | SR_IMPACT_IND_RSLT1 | NUMBER | Y |  | 冲击功单个实绩1 | DB注释(中文) |
| 390 | SR_IMPACT_IND_JDG | VARCHAR2(1) | Y |  | 冲击功单个判定 | DB注释(中文) |
| 391 | SR_IMPACT_IND_RSLT2 | NUMBER | Y |  | 冲击功单个实绩2 | DB注释(中文) |
| 392 | SR_IMPACT_IND_RSLT3 | NUMBER | Y |  | 冲击功单个实绩3 | DB注释(中文) |
| 393 | SR_IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 冲击测试纤维断面率平均实绩 | DB注释(中文) |
| 394 | SR_IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩1 | DB注释(中文) |
| 395 | SR_IMPACT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 冲击测试纤维断面率单个判定 | DB注释(中文) |
| 396 | SR_IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩2 | DB注释(中文) |
| 397 | SR_IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩3 | DB注释(中文) |
| 398 | SR_MGRPHY_GRNSZ_OCCP | NUMBER | Y |  | 金相测试基相晶粒的体积分数 | DB注释(中文) |
| 399 | SR_MGRPHY_FGS_MIXED_RATIO_RSLT | NUMBER | Y |  | 铁素体晶粒混晶占有率实绩 | DB注释(中文) |
| 400 | SR_MGRPHY_FGS_MIXED_RATIO_JDG | VARCHAR2(1) | Y |  | 铁素体晶粒混晶占有率判定 | DB注释(中文) |
| 401 | SR_MGRPHY_FGS_DEVT_MAX_RSLT | NUMBER | Y |  | 铁素体混晶晶粒度差实绩 | DB注释(中文) |
| 402 | SR_MGRPHY_FGS_DEVT_MAX_JDG | VARCHAR2(1) | Y |  | 铁素体混晶晶粒度差判定 | DB注释(中文) |
| 403 | SR_MGRPHY_FGS_RSLT | NUMBER | Y |  | 铁素体晶粒尺寸实绩 | DB注释(中文) |
| 404 | SR_MGRPHY_FGS_JDG | VARCHAR2(1) | Y |  | 铁素体晶粒尺寸判定 | DB注释(中文) |
| 405 | SR_MGRPHY_AGS_RSLT | NUMBER | Y |  | 奥氏体晶粒尺寸实绩 | DB注释(中文) |
| 406 | SR_MGRPHY_AGS_JDG | VARCHAR2(1) | Y |  | 奥氏体晶粒尺寸判定 | DB注释(中文) |
| 407 | SR_MGRPHY_INCLD_TY | VARCHAR2(1) | Y |  | 夹杂物类别 | DB注释(中文) |
| 408 | SR_MGRPHY_INCLD_GRD_MAX_RSLT | NUMBER | Y |  | 夹杂物等级上限实绩 | DB注释(中文) |
| 409 | SR_MGRPHY_INCLD_GRD_MAX_JDG | VARCHAR2(1) | Y |  | 夹杂物等级上限实绩 | DB注释(中文) |
| 410 | SR_MGRPHY_DECARBON_MAX_RSLT | NUMBER | Y |  | 脱碳层上限实绩 | DB注释(中文) |
| 411 | SR_MGRPHY_DECARBON_MAX_JDG | VARCHAR2(1) | Y |  | 脱碳层上限实绩 | DB注释(中文) |
| 412 | SR_MGRPHY_WILD_STRC_GRD | NUMBER | Y |  | 魏氏组织等级 | DB注释(中文) |
| 413 | SR_MGRPHY_WILD_STRC_JDG | VARCHAR2(1) | Y |  | 魏氏组织判定 | DB注释(中文) |
| 414 | SR_MGRPHY_MTLGRP_TY | VARCHAR2(2) | Y |  | 组织类型 | DB注释(中文) |
| 415 | SR_MGRPHY_BAND_STRC_GRD_MAX_RSLT | NUMBER | Y |  | 带状组织等级上限实绩 | DB注释(中文) |
| 416 | SR_MGRPHY_BAND_STRC_GRD_MAX_JDG | VARCHAR2(1) | Y |  | 带状组织等级上限判定 | DB注释(中文) |
| 417 | SR_MGRPHY_GRNSZ_LEVEL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 418 | SR_MGRPHY_GRNSZ_LEVEL | NUMBER | Y |  | 金相测试晶粒度级别 | DB注释(中文) |
| 419 | TSL1_YP_RSLT | NUMBER | Y |  | 拉伸测试1屈服强度实绩 | DB注释(中文) |
| 420 | TSL1_YP_JDG | VARCHAR2(1) | Y |  | 拉伸测试1屈服强度判定 | DB注释(中文) |
| 421 | TSL1_TS_RSLT | NUMBER | Y |  | 拉伸测试1抗拉强度实绩 | DB注释(中文) |
| 422 | TSL1_TS_JDG | VARCHAR2(1) | Y |  | 拉伸测试1抗拉强度判定 | DB注释(中文) |
| 423 | TSL1_EL_RSLT | NUMBER | Y |  | 拉伸测试1伸长率实绩 | DB注释(中文) |
| 424 | TSL1_EL_JDG | VARCHAR2(1) | Y |  | 拉伸测试1伸长率判定 | DB注释(中文) |
| 425 | RE_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 426 | CEQ1_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 427 | CEQEXP_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 428 | CSOL_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 429 | CET_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 430 | CEQAWS_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 431 | CEQJIS_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 432 | TOT_AL_RSLT | VARCHAR2(20) | Y |  | 实绩TOT | DB注释(中文) |
| 433 | SOL_AL_RSLT | VARCHAR2(20) | Y |  | 实绩SOL | DB注释(中文) |
| 434 | WLYS1_RSLT | VARCHAR2(20) | Y |  | 产品成分WLYS1实绩 | DB注释(中文) |
| 435 | WLYS3_RSLT | VARCHAR2(20) | Y |  | 产品成分WLYS3实绩 | DB注释(中文) |

### SHR_HCOIL_ROLLING_RSLT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=31｜被读 27 过程 / 被写 2 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：144　**主键**：COIL_NO、REPROC_NOS　**语义覆盖**：265/267

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | COIL_NO | VARCHAR2(14) | N | ✓ | HotCoil No | DB注释(非中文) |
| 9 | REPROC_NOS | NUMBER | N | ✓ | Number of Reprogressing | DB注释(非中文) |
| 10 | RCD_STS_ID | VARCHAR2(1) | Y |  | Record???? | DB注释(非中文) |
| 11 | ROLL_SCH_NO | VARCHAR2(10) | Y |  | Rolling Schedule Number | DB注释(非中文) |
| 12 | ROLL_SEQ_NO | NUMBER | Y |  | Rolling Sequence Number | DB注释(非中文) |
| 13 | RLG_WK_ABNR_FCTR_CD | VARCHAR2(2) | Y |  | The rolling abnormal code | DB注释(非中文) |
| 14 | RLG_STA_DTM | VARCHAR2(14) | Y |  | The Rolling Start Date | DB注释(非中文) |
| 15 | RLG_END_DTM | VARCHAR2(14) | Y |  | The Rolling End Date | DB注释(非中文) |
| 16 | DUR_TM | NUMBER | Y |  | The Duration Time | DB注释(非中文) |
| 17 | RLG_WK_SUMUP_DT | VARCHAR2(8) | Y |  | Work Day based on Steel works | DB注释(非中文) |
| 18 | RLG_WK_SFT_TEAM | VARCHAR2(2) | Y |  | The Rolling SFT  Crew | DB注释(非中文) |
| 19 | RLG_THK | NUMBER | Y |  | The Coil Thickness after rolling | DB注释(非中文) |
| 20 | RLG_WTH | NUMBER | Y |  | The Coil Width after rolling | DB注释(非中文) |
| 21 | RLG_LTH | NUMBER | Y |  | The Coil Length after rolling | DB注释(非中文) |
| 22 | RLG_IN_DIA | NUMBER | Y |  | The Coil India after Recolling | DB注释(非中文) |
| 23 | RLG_OUT_DIA | NUMBER | Y |  | The Coil Outdia after Recolling | DB注释(非中文) |
| 24 | RLG_COIL_WGT | NUMBER | Y |  | The Coil Weight after Recolling | DB注释(非中文) |
| 25 | RLG_PRDIV_WGT | NUMBER | Y |  | The Coil Weight after Recolling | DB注释(非中文) |
| 26 | RLG_SIZE_CHG_THK | NUMBER | Y |  | The Coil Thickness after Size Changing | DB注释(非中文) |
| 27 | RLG_SIZE_CHG_WTH | NUMBER | Y |  | The Coil Width after Size Changing | DB注释(非中文) |
| 28 | HLDG_FCE_EQP_NO_TP | VARCHAR2(1) | Y |  | Flag of Holding Furance | DB注释(非中文) |
| 29 | HLDG_FCE_STY_HOUR | NUMBER | Y |  | Holding Time  in Furance | DB注释(非中文) |
| 30 | HLDG_FCE_ETR_TEMP | NUMBER | Y |  | Temperature on extracting in Furance | DB注释(非中文) |
| 31 | HLDG_FCE_ETR_DTM | VARCHAR2(14) | Y |  | Extracted Date in Furance | DB注释(非中文) |
| 32 | TF_ETR_WK_SFT | VARCHAR2(2) | Y |  | Extracted SFT/Crew in Furance | DB注释(非中文) |
| 33 | FNSHNG_RLG_PTCH | NUMBER | Y |  | Finishing Roll Pitch | DB注释(非中文) |
| 34 | RLG_RJCT_OCR_FCTR_CD | VARCHAR2(4) | Y |  | The Reject caused Code | DB注释(非中文) |
| 35 | RLG_RJCT_CMT | VARCHAR2(330) | Y |  | The Reject Comment | DB注释(非中文) |
| 36 | RLG_RJCT_SFT | VARCHAR2(1) | Y |  | The Reject Shift | DB注释(非中文) |
| 37 | RLG_RJCT_CREW | VARCHAR2(1) | Y |  | The Reject Crew | DB注释(非中文) |
| 38 | RLG_RJCT_DTM | VARCHAR2(14) | Y |  | The Reject Date | DB注释(非中文) |
| 39 | RLG_RJCT_POS | VARCHAR2(1) | Y |  | The Reject Position | DB注释(非中文) |
| 40 | RLG_FNL_QURT_DTM | VARCHAR2(14) | Y |  | Date of leaving on the final W/B at the Delivary Side | DB注释(非中文) |
| 41 | QURT_CNVY_NO | VARCHAR2(2) | Y |  | The Conveyer No on taking over Hr Coil at the Rolling Line | DB注释(非中文) |
| 42 | SMP_SMPLNG_INST_TP | VARCHAR2(1) | Y |  | Flag of Sampling Cut P DI | DB注释(非中文) |
| 43 | SMP_SMPLNG_FG | VARCHAR2(1) | Y |  | Ok or Nok of Sampling Cut | DB注释(非中文) |
| 44 | APR_SYN_GRD | VARCHAR2(1) | Y |  | HotCoil Surface Total Judgement Grade | DB注释(非中文) |
| 45 | UNT_WGT_GRD | VARCHAR2(1) | Y |  | HotCoil Weight Judgement Grade | DB注释(非中文) |
| 46 | SIZE_GRD | VARCHAR2(1) | Y |  | HotCoil Size Judgement Grade | DB注释(非中文) |
| 47 | SUR_GRD | VARCHAR2(1) | Y |  | HotCoil Surface Judgement Grade | DB注释(非中文) |
| 48 | SHP_GRD | VARCHAR2(1) | Y |  | HotCoil Shape Judgement Grade | DB注释(非中文) |
| 49 | MID_INSPT_DTM | VARCHAR2(14) | Y |  | Date of Inspection | DB注释(非中文) |
| 50 | MID_INSPT_FG | VARCHAR2(1) | Y |  | Ok or Nok of Inspection | DB注释(非中文) |
| 51 | MID_INSPTR_EMP_NO | VARCHAR2(20) | Y |  | Inspector Empoly Number | DB注释(非中文) |
| 52 | RLG_INSPTR_OPNN | VARCHAR2(330) | Y |  | Inspector Comment | DB注释(非中文) |
| 53 | RLG_TLSCP_OCR_FG | VARCHAR2(1) | Y |  | Have or not Telescope | DB注释(非中文) |
| 54 | COIL_TLSCP_TP | VARCHAR2(2) | Y |  | Flag of Telescope | DB注释(非中文) |
| 55 | SLAB_NO | VARCHAR2(12) | Y |  | Slab No | DB注释(非中文) |
| 56 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  | Steel Grade | DB注释(非中文) |
| 57 | SLAB_THK | NUMBER | Y |  | Slab Thickness | DB注释(非中文) |
| 58 | SLAB_WTH | NUMBER | Y |  | Slab Width | DB注释(非中文) |
| 59 | SLAB_LTH | NUMBER | Y |  | Slab Length | DB注释(非中文) |
| 60 | SLAB_WGT | NUMBER | Y |  | Slab Weight | DB注释(非中文) |
| 61 | FCE_NO | VARCHAR2(1) | Y |  | Furnace Number | DB注释(非中文) |
| 62 | FCE_CHARGE_TEMP | NUMBER | Y |  | Furnace Charge Temperature | DB注释(非中文) |
| 63 | FCE_DISCHARGE_TEMP | NUMBER | Y |  | Furnace Discharge Temperature | DB注释(非中文) |
| 64 | SLAB_TEMP_MSU_AVG_LTH_PET | NUMBER | Y |  | Slab temperature measured value_AVG in whole length (by PET) | DB注释(非中文) |
| 65 | SLAB_TEMP_MSU_MAX_LTH_PET | NUMBER | Y |  | Slab temperature measured value_MAX in whole length (by PET) | DB注释(非中文) |
| 66 | SLAB_TEMP_MSU_MIN_LTH_PET | NUMBER | Y |  | Slab temperature measured value_MIN in whole length (by PET) | DB注释(非中文) |
| 67 | SLAB_TEMP_MSU_AVE_LTH_R2DT | NUMBER | Y |  | Slab temperature measured value_AVG in whole length (by R2DT) | DB注释(非中文) |
| 68 | SLAB_TEMP_MSU_MAX_LTH_R2DT | NUMBER | Y |  | Slab temperature measured value_MAX in whole length (by R2DT) | DB注释(非中文) |
| 69 | SLAB_TEMP_MSU_MIN_LTH_R2DT | NUMBER | Y |  | Slab temperature measured value_MIN in whole length (by R2DT) | DB注释(非中文) |
| 70 | SLAB_TEMP_MSU_AVE_LTH_CB | NUMBER | Y |  | Slab temperature measured value_AVG in whole length (by CB) | DB注释(非中文) |
| 71 | SLAB_TEMP_MSU_MAX_LTH_CB | NUMBER | Y |  | Slab temperature measured value_MAX in whole length (by CB) | DB注释(非中文) |
| 72 | SLAB_TEMP_MSU_MIN_LTH_CB | NUMBER | Y |  | Slab temperature measured value_MIN in whole length (by CB) | DB注释(非中文) |
| 73 | THK_TGT_MDL_CALU_COLD | NUMBER | Y |  | Thickness target for model calculation (Cold) | DB注释(非中文) |
| 74 | WTH_SET_TGT_CALU_COLD | NUMBER | Y |  | Width set target for model calculation (Cold) | DB注释(非中文) |
| 75 | FM_EXT_TEMP_CALU | NUMBER | Y |  | FM Exit Temperature Calculation | DB注释(非中文) |
| 76 | DC_TEMP_CALU | NUMBER | Y |  | DC Temperature Calculation | DB注释(非中文) |
| 77 | FLAT_TGT | NUMBER | Y |  | Flatness target | DB注释(非中文) |
| 78 | CROWN_TGT | NUMBER | Y |  | Crown target | DB注释(非中文) |
| 79 | FM_ENTRY_TEMP_MSU_AVG1 | NUMBER | Y |  | FM Entry temperature: measured value_AVG | DB注释(非中文) |
| 80 | FM_ENTRY_TEMP_MSU_MAX1 | NUMBER | Y |  | FM Entry temperature: measured value_MAX (excluding head and tail part | DB注释(非中文) |
| 81 | FM_ENTRY_TEMP_MSU_MIN1 | NUMBER | Y |  | FM Entry temperature: measured value_MIN | DB注释(非中文) |
| 82 | THK_MSU_COLD_AVG | NUMBER | Y |  | Thickness: measured Cold value_AVG | DB注释(非中文) |
| 83 | THK_MSU_COLD_MAX | NUMBER | Y |  | Thickness: measured Cold value_MAX | DB注释(非中文) |
| 84 | THK_MSU_COLD_MIN | NUMBER | Y |  | Thickness: measured Cold value_MIN | DB注释(非中文) |
| 85 | THK_MSU_COLD_SD | NUMBER | Y |  | Thickness: measured Cold value_SD | DB注释(非中文) |
| 86 | THK_PER_IN_TOL | NUMBER | Y |  | Thickness: _PEC_TOL | DB注释(非中文) |
| 87 | WTH_MSU_COLD_AVG | NUMBER | Y |  | Width: measured Cold value_AVG | DB注释(非中文) |
| 88 | WTH_MSU_COLD_MAX | NUMBER | Y |  | Width: measured Cold value_MAX | DB注释(非中文) |
| 89 | WTH_MSU_COLD_MIN | NUMBER | Y |  | Width: measured Cold value_MIN | DB注释(非中文) |
| 90 | WTH_MSU_COLD_SD | NUMBER | Y |  | Width: measured Cold value_SD | DB注释(非中文) |
| 91 | WTH_PER_IN_TOL | NUMBER | Y |  | Width: _PEC_TOL | DB注释(非中文) |
| 92 | FM_ENTRY_TGT_TEMP | NUMBER | Y |  | FM Entry target temperature | DB注释(非中文) |
| 93 | FM_ENTRY_TEMP_MSU_AVG2 | NUMBER | Y |  | FM Entry temperature: measured value_AVG | DB注释(非中文) |
| 94 | FM_ENTRY_TEMP_MSU_MAX2 | NUMBER | Y |  | FM Entry temperature: measured value_MAX | DB注释(非中文) |
| 95 | FM_ENTRY_TEMP_MSU_MIN2 | NUMBER | Y |  | FM Entry temperature: measured value_MIN | DB注释(非中文) |
| 96 | FM_ENTRY_TEMP_MSU_SD2 | NUMBER | Y |  | FM Entry temperature: measured value_SD | DB注释(非中文) |
| 97 | FM_ENTRY_TEMP_PER_TOL | NUMBER | Y |  | FM Entry temperature: _PEC_TOL | DB注释(非中文) |
| 98 | FM_EXIT_TEMP_MSU_AVG | NUMBER | Y |  | FM Exit temperature: measured value_AVG | DB注释(非中文) |
| 99 | FM_EXIT_TEMP_MSU_MAX | NUMBER | Y |  | FM Exit temperature: measured value_MAX | DB注释(非中文) |
| 100 | FM_EXIT_TEMP_MSU_MIN | NUMBER | Y |  | FM Exit temperature: measured value_MIN | DB注释(非中文) |
| 101 | FM_EXIT_TEMP_MSU_SD | NUMBER | Y |  | FM Exit temperature: measured value_SD | DB注释(非中文) |
| 102 | FM_EXIT_TEMP_PEC_TOL | NUMBER | Y |  | FM Exit temperature: _PEC_TOL | DB注释(非中文) |
| 103 | COL_TEMP_MSU_AVG | NUMBER | Y |  | Coiling temperature: measured value_AVG | DB注释(非中文) |
| 104 | COL_TEMP_MSU_MAX | NUMBER | Y |  | Coiling temperature: measured value_MAX | DB注释(非中文) |
| 105 | COL_TEMP_MSU_MIN | NUMBER | Y |  | Coiling temperature: measured value_MIN | DB注释(非中文) |
| 106 | COL_TEMP_MSU_SD | NUMBER | Y |  | Coiling temperature: measured value_SD | DB注释(非中文) |
| 107 | COL_TEMP_PEC_TOL | NUMBER | Y |  | Coiling temperature: _PEC_TOL | DB注释(非中文) |
| 108 | FLATL_SYM_MSU_COLD_AVG | NUMBER | Y |  | Flatness (symmetric): measured Cold value_AVG | DB注释(非中文) |
| 109 | FLATL_SYM_MSU_COLD_MAX | NUMBER | Y |  | Flatness (symmetric): measured Cold value_MAX | DB注释(非中文) |
| 110 | FLATL_SYM_MSU_COLD_MIN | NUMBER | Y |  | Flatness (symmetric): measured Cold value_MIN | DB注释(非中文) |
| 111 | FLATL_SYM_MSU_COLD_SD | NUMBER | Y |  | Flatness (symmetric): measured Cold value_SD | DB注释(非中文) |
| 112 | FLATL_SYM_OUT_CLASS_LTH | NUMBER | Y |  | Flatness (symmetric): out of classification range length | DB注释(非中文) |
| 113 | FLATL_ASYM_MSU_COLD_AVG | NUMBER | Y |  | Flatness (asymmetric): measured Cold value_AVG | DB注释(非中文) |
| 114 | FLATL_ASYM_MSU_COLD_MAX | NUMBER | Y |  | Flatness (asymmetric): measured Cold value_MAX | DB注释(非中文) |
| 115 | FLATL_ASYM_MSU_COLD_MIN | NUMBER | Y |  | Flatness (asymmetric): measured Cold value_MIN | DB注释(非中文) |
| 116 | FLATL_ASYM_MSU_COLD_SD | NUMBER | Y |  | Flatness (asymmetric): measured Cold value_SD | DB注释(非中文) |
| 117 | FLATL_ASYM_OUT_CLASS_LTH | NUMBER | Y |  | Flatness (asymmetric): out of classification range length | DB注释(非中文) |
| 118 | CROWN_MSU_COLD_AVG | NUMBER | Y |  | Crown: measured Cold value_AVG | DB注释(非中文) |
| 119 | CROWN_MSU_COLD_MAX | NUMBER | Y |  | Crown: measured Cold value_MAX(excluding head and tail part) | DB注释(非中文) |
| 120 | CROWN_MSU_COLD_MIN | NUMBER | Y |  | Crown: measured Cold value_MIN(excluding head and tail part) | DB注释(非中文) |
| 121 | CROWN_MSU_COLD_SD | NUMBER | Y |  | Crown: measured Cold value_SD(excluding head and tail part) | DB注释(非中文) |
| 122 | CROWN_PEC_TOL | NUMBER | Y |  | Crown: _PEC_TOL | DB注释(非中文) |
| 123 | WEDGE_MSU_COLD_AVG | NUMBER | Y |  | Wedge: measured Cold value_AVG | DB注释(非中文) |
| 124 | WEDGE_MSU_COLD_MAX | NUMBER | Y |  | Wedge: measured Cold value_MAX(excluding head and tail part) | DB注释(非中文) |
| 125 | WEDGE_MSU_COLD_MIN | NUMBER | Y |  | Wedge: measured Cold value_MIN(excluding head and tail part) | DB注释(非中文) |
| 126 | WEDGE_MSU_COLD_SD | NUMBER | Y |  | Wedge: measured Cold value_SD(excluding head and tail part) | DB注释(非中文) |
| 127 | WEDGE_PEC_TOL | NUMBER | Y |  | Wedge: _PEC_TOL | DB注释(非中文) |
| 128 | QNTY_THK_CD | VARCHAR2(4) | Y |  | Coil quality code: Thickness | DB注释(非中文) |
| 129 | QNTY_WTH_CD | VARCHAR2(4) | Y |  | Coil quality code: Width | DB注释(非中文) |
| 130 | QNTY_FM_EXIT_CD | VARCHAR2(4) | Y |  | Coil quality code: FM exit temperature | DB注释(非中文) |
| 131 | QNTY_COILING_CD | VARCHAR2(4) | Y |  | Coil quality code: Coiling temperature | DB注释(非中文) |
| 132 | QNTY_FLAT_CD | VARCHAR2(4) | Y |  | Coil quality code: Flatness | DB注释(非中文) |
| 133 | QNTY_LAT_SYM_CD | VARCHAR2(4) | Y |  | Coil quality code: Flatness (symmetric) | DB注释(非中文) |
| 134 | QNTY_CROWN_CD | VARCHAR2(4) | Y |  | Coil quality code: Crown | DB注释(非中文) |
| 135 | QNTY_WEDGE_CD | VARCHAR2(4) | Y |  | Coil quality code: Wedge | DB注释(非中文) |
| 136 | NMNL_THK_FRM_MARKET | NUMBER | Y |  | Nominal thickness from market | DB注释(非中文) |
| 137 | COL_RECIPE_CD | VARCHAR2(4) | Y |  | Cooling Recipe Code | DB注释(非中文) |
| 138 | FCE_CHARGE_DTM | VARCHAR2(14) | Y |  | Furnace Charge Time | DB注释(非中文) |
| 139 | FCE_DISCHARGE_DTM | VARCHAR2(14) | Y |  | Furnace Discharge Time | DB注释(非中文) |
| 140 | SLAB_FCE_TM | NUMBER | Y |  | Slab in Furnace Time | DB注释(非中文) |
| 141 | RM_ENTRY_TEMP | NUMBER | Y |  | RM Entrance Temperature | DB注释(非中文) |
| 142 | HIGH_PRS_WTR | VARCHAR2(1) | Y |  | high pressure water descaling box service condition | DB注释(非中文) |
| 143 | ROUGH_MILL_DESCL_SVE_COND | VARCHAR2(1) | Y |  | RoughMill descaling service condition | DB注释(非中文) |
| 144 | R1_ROLLING_TM | NUMBER | Y |  | R1 Rolling Times | DB注释(非中文) |
| 145 | R1_EXIT_SLAB_THK | NUMBER | Y |  | R1 Exit Slab Thickness | DB注释(非中文) |
| 146 | R1_EXIT_SLAB_WTH | NUMBER | Y |  | R1 Exit Slab Width | DB注释(非中文) |
| 147 | R1_EXIT_SLAB_LTH | NUMBER | Y |  | R1 Exit Slab Length | DB注释(非中文) |
| 148 | R1_EXIT_TEMP | NUMBER | Y |  | R1 Exit Temperature | DB注释(非中文) |
| 149 | R1_DUMMY_ACT | VARCHAR2(1) | Y |  | R1 Dummy act | DB注释(非中文) |
| 150 | R2_ROLL_TM | NUMBER | Y |  | R2 Rolling Times | DB注释(非中文) |
| 151 | R2_EXIT_SLAB_THK | NUMBER | Y |  | R2 Exit Slab Thickness | DB注释(非中文) |
| 152 | R2_EXIT_SLAB_WTH | NUMBER | Y |  | R2 Exit Slab Width | DB注释(非中文) |
| 153 | R2_EXIT_SLAB_LTH | NUMBER | Y |  | R2 Exit Slab Length | DB注释(非中文) |
| 154 | R2_EXIT_TEMP | NUMBER | Y |  | R2 Exit Temperature | DB注释(非中文) |
| 155 | E2_DUMMY_ACT | VARCHAR2(1) | Y |  | E2_Dummy_act | DB注释(非中文) |
| 156 | R2_DUMMY_ACT | VARCHAR2(1) | Y |  | E2_Dummy_act | DB注释(非中文) |
| 157 | R1_ENTRY_DESCA_COND | VARCHAR2(1) | Y |  | R1 Entrance descaling service condition | DB注释(非中文) |
| 158 | R1_EXIT_DESCA_COND | VARCHAR2(1) | Y |  | R1 Exit descaling service condition | DB注释(非中文) |
| 159 | R2_ENRTY_DESCA_COND | VARCHAR2(1) | Y |  | R2 Entrance descaling service condition | DB注释(非中文) |
| 160 | R2_EXIT_DESCA_COND | VARCHAR2(1) | Y |  | R2 Exit descaling service condition | DB注释(非中文) |
| 161 | DESCA_COND_BEF_FM | VARCHAR2(1) | Y |  | descaling service condition before FM | DB注释(非中文) |
| 162 | EH_COND | VARCHAR2(1) | Y |  | EH service condition | DB注释(非中文) |
| 163 | EH_POWER | VARCHAR2(6) | Y |  | EH power | DB注释(非中文) |
| 164 | F1_ENRTY_TEMP | NUMBER | Y |  | F1 Entrance Temperature | DB注释(非中文) |
| 165 | FM_F1_ON_DTM | VARCHAR2(14) | Y |  | F1 on Time | DB注释(非中文) |
| 166 | FM_FNL_STND_OFF_DTM | VARCHAR2(14) | Y |  | F7 off Time | DB注释(非中文) |
| 167 | FM_ROLL_TM | NUMBER | Y |  | FM Rolling Time | DB注释(非中文) |
| 168 | F7_TEMP_SET_VAL | NUMBER | Y |  | F7 Temperature Set Value | DB注释(非中文) |
| 169 | F7_TEMP_ACT_VAL | NUMBER | Y |  | F7 Temperature Actual Value | DB注释(非中文) |
| 170 | FM_COND_FG | NUMBER | Y |  | FM service condition Flag | DB注释(非中文) |
| 171 | F1_ROLL_FORCE | NUMBER | Y |  | F1 rolling force | DB注释(非中文) |
| 172 | F2_ROLL_FORCE | NUMBER | Y |  | F2 rolling force | DB注释(非中文) |
| 173 | F3_ROLL_FORCE | NUMBER | Y |  | F3 rolling force | DB注释(非中文) |
| 174 | F4_ROLL_FORCE | NUMBER | Y |  | F4 rolling force | DB注释(非中文) |
| 175 | F5_ROLL_FORCE | NUMBER | Y |  | F5 rolling force | DB注释(非中文) |
| 176 | F6_ROLL_FORCE | NUMBER | Y |  | F6 rolling force | DB注释(非中文) |
| 177 | F7_ROLL_FORCE | NUMBER | Y |  | F7 rolling force | DB注释(非中文) |
| 178 | F1_ROLL_GAP | NUMBER | Y |  | F1 roll gap | DB注释(非中文) |
| 179 | F2_ROLL_GAP | NUMBER | Y |  | F2 roll gap | DB注释(非中文) |
| 180 | F3_ROLL_GAP | NUMBER | Y |  | F3 roll gap | DB注释(非中文) |
| 181 | F4_ROLL_GAP | NUMBER | Y |  | F4 roll gap | DB注释(非中文) |
| 182 | F5_ROLL_GAP | NUMBER | Y |  | F5 roll gap | DB注释(非中文) |
| 183 | F6_ROLL_GAP | NUMBER | Y |  | F6 roll gap | DB注释(非中文) |
| 184 | F7_ROLL_GAP | NUMBER | Y |  | F7 roll gap | DB注释(非中文) |
| 185 | F1_F2_INTER_COL_FLW | NUMBER | Y |  | F1-F2 inter cooling flow | DB注释(非中文) |
| 186 | F2_F3_INTER_COL_FLW | NUMBER | Y |  | F2-F3 inter cooling flow | DB注释(非中文) |
| 187 | F3_F4_INTER_COL_FLW | NUMBER | Y |  | F3-F4 inter cooling flow | DB注释(非中文) |
| 188 | F4_F5_INTER_COL_FLW | NUMBER | Y |  | F4-F5 inter cooling flow | DB注释(非中文) |
| 189 | F5_F6_INTER_COL_FLW | NUMBER | Y |  | F5-F6 inter cooling flow | DB注释(非中文) |
| 190 | F6_F7_INTER_COL_FLW | NUMBER | Y |  | F6-F7 inter cooling flow | DB注释(非中文) |
| 191 | F1_ROLL_GAP_LUB_FLW | NUMBER | Y |  | F1 Roll gap lubrication flow | DB注释(非中文) |
| 192 | F2_ROLL_GAP_LUB_FLW | NUMBER | Y |  | F2 Roll gap lubrication flow | DB注释(非中文) |
| 193 | F3_ROLL_GAP_LUB_FLW | NUMBER | Y |  | F3 Roll gap lubrication flow | DB注释(非中文) |
| 194 | F4_ROLL_GAP_LUB_FLW | NUMBER | Y |  | F4 Roll gap lubrication flow | DB注释(非中文) |
| 195 | F5_ROLL_GAP_LUB_FLW | NUMBER | Y |  | F5 Roll gap lubrication flow | DB注释(非中文) |
| 196 | F6_ROLL_GAP_LUB_FLW | NUMBER | Y |  | F6 Roll gap lubrication flow | DB注释(非中文) |
| 197 | F7_ROLL_GAP_LUB_FLW | NUMBER | Y |  | F7 Roll gap lubrication flow | DB注释(非中文) |
| 198 | F1_F2_LPE_TNS | NUMBER | Y |  | F1-F2 Looper tension | DB注释(非中文) |
| 199 | F2_F3_LPE_TNS | NUMBER | Y |  | F2-F3 Looper tension | DB注释(非中文) |
| 200 | F3_F4_LPE_TNS | NUMBER | Y |  | F3-F4 Looper tension | DB注释(非中文) |
| 201 | F4_F5_LPE_TNS | NUMBER | Y |  | F4-F5 Looper tension | DB注释(非中文) |
| 202 | F5_F6_LPE_TNS | NUMBER | Y |  | F5-F6 Looper tension | DB注释(非中文) |
| 203 | F6_F7_LPE_TNS | NUMBER | Y |  | F6-F7 Looper tension | DB注释(非中文) |
| 204 | F1_F2_LPE_ANGLE | NUMBER | Y |  | F1-F2 Looper angle | DB注释(非中文) |
| 205 | F2_F3_LPE_ANGLE | NUMBER | Y |  | F2-F3 Looper angle | DB注释(非中文) |
| 206 | F3_F4_LPE_ANGLE | NUMBER | Y |  | F3-F4 Looper angle | DB注释(非中文) |
| 207 | F4_F5_LPE_ANGLE | NUMBER | Y |  | F4-F5 Looper angle | DB注释(非中文) |
| 208 | F5_F6_LPE_ANGLE | NUMBER | Y |  | F5-F6 Looper angle | DB注释(非中文) |
| 209 | F6_F7_LPE_ANGLE | NUMBER | Y |  | F6-F7 Looper angle | DB注释(非中文) |
| 210 | F7_RUN_SPD | NUMBER | Y |  | F7 Runing speed | DB注释(非中文) |
| 211 | CTC_USED_FLG | VARCHAR2(1) | Y |  | CTC used flag | DB注释(非中文) |
| 212 | UFC_SYS_FLG | VARCHAR2(1) | Y |  | UFC System Flag | DB注释(非中文) |
| 213 | CTC_CTRL_PTRN | VARCHAR2(3) | Y |  | CTC_ctrl_pattern(CTC Cooling pattern) | DB注释(非中文) |
| 214 | UFC_CTRL_PTRN | VARCHAR2(3) | Y |  | UFC_ctrl_pattern(UFC Cooling pattern) | DB注释(非中文) |
| 215 | CTC_COOL_RATE_CTL_SET | NUMBER | Y |  | CTC cooling rate control set value | DB注释(非中文) |
| 216 | CTC_COOL_RATE_CTL_ACTL_SET | NUMBER | Y |  | CTC cooling rate control actual value | DB注释(非中文) |
| 217 | UFC_COOL_RATE_CTL_SET | NUMBER | Y |  | UFC cooling rate control set value | DB注释(非中文) |
| 218 | UFC_COOL_RATE_CTL_ACTL_SET | NUMBER | Y |  | UFC cooling rate control actual value | DB注释(非中文) |
| 219 | COOL_TEMP_CTL_SET_VAL | NUMBER | Y |  | cooling temperature control set value | DB注释(非中文) |
| 220 | COOL_TEMP_CTL_ACT_VAL | NUMBER | Y |  | cooling temperature control actual value | DB注释(非中文) |
| 221 | DC_NO | VARCHAR2(1) | Y |  | DC number | DB注释(非中文) |
| 222 | DC_ON_DTM | VARCHAR2(14) | Y |  | DC on time | DB注释(非中文) |
| 223 | DC_OFF_DTM | VARCHAR2(14) | Y |  | DC off time | DB注释(非中文) |
| 224 | DC_TEMP_SET_VAL | NUMBER | Y |  | DC temperature set value | DB注释(非中文) |
| 225 | DC_TEMP_ACT_VAL | NUMBER | Y |  | DC temperature actual value | DB注释(非中文) |
| 226 | COIL_WGT | NUMBER | Y |  | Coil Weight | DB注释(非中文) |
| 227 | COIL_LTH | NUMBER | Y |  | Coil Length | DB注释(非中文) |
| 228 | COIL_IN_DIA | NUMBER | Y |  | Coil inner Diameter | DB注释(非中文) |
| 229 | COIL_OUT_DIA | NUMBER | Y |  | Coil outer Diameter | DB注释(非中文) |
| 230 | COIL_THK_AVG_VAL | NUMBER | Y |  | Coil thickness_AVG value | DB注释(非中文) |
| 231 | THK_ON_GAG_RATE | NUMBER | Y |  | Coil thickness on gauge rate | DB注释(非中文) |
| 232 | WTH_FW7_AVG_VAL | NUMBER | Y |  | Coil width FW7_AVG value | DB注释(非中文) |
| 233 | WTH_FW7_ON_GAG_RATE | NUMBER | Y |  | Coil width FW7 on gauge rate | DB注释(非中文) |
| 234 | R2DT_AVG_VAL | NUMBER | Y |  | R2DT_AVG value | DB注释(非中文) |
| 235 | R2DT_ON_GAG_VAL | NUMBER | Y |  | R2DT on gauge value | DB注释(非中文) |
| 236 | FET_AVG_VAL | NUMBER | Y |  | FET_AVG value | DB注释(非中文) |
| 237 | FET_ON_GAG_VAL | NUMBER | Y |  | FET on gauge value | DB注释(非中文) |
| 238 | FDT7_AVG_VAL | NUMBER | Y |  | FDT7_AVG value ???? | DB注释(非中文) |
| 239 | FDT7_ON_GAG_VAL | NUMBER | Y |  | FDT7 on gauge value | DB注释(非中文) |
| 240 | CT_AVG_VAL | NUMBER | Y |  | CT_AVG value ???? | DB注释(非中文) |
| 241 | CT_ON_GAG_VAL | NUMBER | Y |  | CT on gauge value | DB注释(非中文) |
| 242 | UFC_TEMP_AVG_VAL | NUMBER | Y |  | UFC temperature_AVG value | DB注释(非中文) |
| 243 | UFC_TEMP_ON_GAG_RATE | NUMBER | Y |  | UFC temperature on gauge rate | DB注释(非中文) |
| 244 | CROWN_AVG_VAL | NUMBER | Y |  | Crown_AVG Value | DB注释(非中文) |
| 245 | CROWN_ON_GAG_RATE | NUMBER | Y |  | Crown on gauge rate | DB注释(非中文) |
| 246 | FLAT_AVG_VAL | NUMBER | Y |  | Flatness_AVG Value | DB注释(非中文) |
| 247 | FLAT_ON_GAG_RATE | NUMBER | Y |  | Flatness on gauge rate | DB注释(非中文) |
| 248 | WDG_AVG_VAL | NUMBER | Y |  | Wedge_AVG value | DB注释(非中文) |
| 249 | WDG_ON_GAG_RATE | NUMBER | Y |  | Wedge on gauge rate | DB注释(非中文) |
| 250 | SFT_NO | VARCHAR2(1) | Y |  | SFT Number | DB注释(非中文) |
| 251 | GRP_NO | VARCHAR2(1) | Y |  | Group Number | DB注释(非中文) |
| 252 | CUST_ORD_NO | VARCHAR2(15) | Y |  | Customer Order Number | DB注释(非中文) |
| 253 | COIL_DIR | VARCHAR2(1) | Y |  | Coil direction | DB注释(非中文) |
| 254 | CUST_CD | VARCHAR2(9) | Y |  | Customer code | DB注释(非中文) |
| 255 | QLT_TRKG_CD1 | VARCHAR2(9) | Y |  | The Quality tracking code_1 | DB注释(非中文) |
| 256 | QLT_TRKG_GRD1 | NUMBER | Y |  | The Quality tracking value_1 | DB注释(非中文) |
| 257 | QLT_TRKG_CD2 | VARCHAR2(9) | Y |  | The Quality tracking code_2 | DB注释(非中文) |
| 258 | QLT_TRKG_GRD2 | NUMBER | Y |  | The Quality tracking value_2 | DB注释(非中文) |
| 259 | QLT_TRKG_CD3 | VARCHAR2(9) | Y |  | The Quality tracking code_3 | DB注释(非中文) |
| 260 | QLT_TRKG_GRD3 | NUMBER | Y |  | The Quality tracking value_3 | DB注释(非中文) |
| 261 | QLT_TRKG_ABNR_AC_CD1 | VARCHAR2(3) | Y |  | The Quality tracking abnormal recorrection code_1 | DB注释(非中文) |
| 262 | QLT_TRKG_ABNR_AC_CD2 | VARCHAR2(3) | Y |  | The Quality tracking abnormal recorrection code_2 | DB注释(非中文) |
| 263 | QLT_TRKG_ABNR_AC_CD3 | VARCHAR2(3) | Y |  | The Quality tracking abnormal recorrection code_3 | DB注释(非中文) |
| 264 | HFR_FNL_STND_ON_DTM | VARCHAR2(14) | Y |  | The Date stood on the final finishing roll | DB注释(非中文) |
| 265 | RM_R2_STND_RLG_PTCH | NUMBER | Y |  | The R2_stand rolling pitch on the roughing roll | DB注释(非中文) |
| 266 | OPER_JDG_TY | VARCHAR2(1) | Y |  |  | 空 |
| 267 | FINAL_DIV_MARK | VARCHAR2(1) | Y |  |  | 空 |

### SCH_ROLL_BATCH

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=30｜被读 22 过程 / 被写 4 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：0　**主键**：BATCH_CD　**语义覆盖**：42/50

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | 创建用户 | DB注释(中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(100) | Y |  | 创建对象 | DB注释(中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | 创建时间 | DB注释(中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 更新用户 | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | 更新对象 | DB注释(中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | 更新时间 | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | 归档标志 | DB注释(中文) |
| 8 | BATCH_CD | VARCHAR2(20) | N | ✓ | 批次号 | DB注释(中文) |
| 9 | BILLET_CNT | NUMBER | Y |  | 钢坯数量 | DB注释(中文) |
| 10 | ROLL_UNIT_PRI | NUMBER | Y |  | 轧制顺序 | DB注释(中文) |
| 11 | FAC_CD | VARCHAR2(20) | Y |  | 产线 | DB注释(中文) |
| 12 | ROLL_UNIT | VARCHAR2(20) | Y |  | 轧制计划号 | DB注释(中文) |
| 13 | MAIN_HEAT_NO | VARCHAR2(20) | Y |  | 炉号 | DB注释(中文) |
| 14 | GRP_BATCH_HEAT | VARCHAR2(20) | Y |  | 组批炉号 | DB注释(中文) |
| 15 | GRP_BATCH_CNT | NUMBER | Y |  | 组批数量 | DB注释(中文) |
| 16 | TOTAL_WGT | NUMBER | Y |  | 总重量 | DB注释(中文) |
| 17 | SPEC_CD | VARCHAR2(20) | Y |  | 国家标准及牌号 | DB注释(中文) |
| 18 | BILLET_THK | NUMBER | Y |  | 钢坯厚度 | DB注释(中文) |
| 19 | BILLET_WTH | NUMBER | Y |  | 钢坯宽度 | DB注释(中文) |
| 20 | BILLET_LEN | NUMBER | Y |  | 钢坯长度 | DB注释(中文) |
| 21 | PROD_GRP | VARCHAR2(20) | Y |  | 产品名称 | DB注释(中文) |
| 22 | PROD_PCS | NUMBER | Y |  | 产品数量 | DB注释(中文) |
| 23 | ORD_TY | VARCHAR2(20) | Y |  | 订单类型 | DB注释(中文) |
| 24 | ORD_USAGE | VARCHAR2(20) | Y |  | 订单用途 | DB注释(中文) |
| 25 | PLAN_PROC_ROUTE | VARCHAR2(20) | Y |  | 计划通过工序 | DB注释(中文) |
| 26 | CUST_NM | VARCHAR2(20) | Y |  | 客户 | DB注释(中文) |
| 27 | ORD_DELV_DT | DATE | Y |  | 订单交货期 | DB注释(中文) |
| 28 | ORD_NO | VARCHAR2(20) | Y |  | 订单号 | DB注释(中文) |
| 29 | ORD_LN | VARCHAR2(20) | Y |  | 订单行号 | DB注释(中文) |
| 30 | ORD_PCS | NUMBER | Y |  | 订单数量 | DB注释(中文) |
| 31 | PLAN_ROLL_STS | VARCHAR2(20) | Y |  | 轧制状态 | DB注释(中文) |
| 32 | HCR_FL | VARCHAR2(20) | Y |  | 冷热送状态 | DB注释(中文) |
| 33 | SPEC_RCV_DTM | DATE | Y |  | 计划接受日期 | DB注释(中文) |
| 34 | PROD_INST_DTM | DATE | Y |  | 作业指令传送日 | DB注释(中文) |
| 35 | PLAN_ISSUE_STA | VARCHAR2(20) | Y |  | 下发状态(1-取消,2-下达) | DB注释(中文) |
| 36 | PLAN_ISSUE_USER | VARCHAR2(20) | Y |  | 下发人 | DB注释(中文) |
| 37 | PLAN_ISSUE_TM | VARCHAR2(20) | Y |  | 下发时间 | DB注释(中文) |
| 38 | PROD_SPEC | VARCHAR2(20) | Y |  | 产品规格 | DB注释(中文) |
| 39 | DELETE_FLAG | NUMBER | Y |  | 删除标志 0正常 1已删除 | DB注释(中文) |
| 40 | ATTRIBUTE1 | VARCHAR2(500) | Y |  | 产线使用装炉备注 | DB注释(中文) |
| 41 | ATTRIBUTE2 | VARCHAR2(500) | Y |  | 产线使用集卷备注 | DB注释(中文) |
| 42 | ATTRIBUTE3 | VARCHAR2(50) | Y |  |  | 空 |
| 43 | ATTRIBUTE4 | VARCHAR2(50) | Y |  |  | 空 |
| 44 | ATTRIBUTE5 | VARCHAR2(50) | Y |  |  | 空 |
| 45 | ATTRIBUTE6 | VARCHAR2(50) | Y |  |  | 空 |
| 46 | ATTRIBUTE7 | VARCHAR2(50) | Y |  |  | 空 |
| 47 | ATTRIBUTE8 | VARCHAR2(50) | Y |  |  | 空 |
| 48 | ATTRIBUTE9 | VARCHAR2(50) | Y |  |  | 空 |
| 49 | ATTRIBUTE10 | VARCHAR2(50) | Y |  |  | 空 |
| 50 | BATCH_FLAG | NUMBER | Y |  | 是否组批 0单独 1追加 | DB注释(中文) |

### SQM_MTC_REQ

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=30｜被读 12 过程 / 被写 9 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：19098　**主键**：PROD_NO、MTC_REQ_NO　**语义覆盖**：18/18

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | PROD_NO | VARCHAR2(18) | N | ✓ | 产品编号 | DB注释(中文) |
| 8 | MTC_REQ_NO | VARCHAR2(10) | N | ✓ | 质量保证书申请编号 | DB注释(中文) |
| 9 | MTC_NO | VARCHAR2(11) | Y |  | 质量保证书编号 | DB注释(中文) |
| 10 | ORD_NO | VARCHAR2(10) | Y |  | 订单编号 | DB注释(中文) |
| 11 | ORD_LN | VARCHAR2(3) | Y |  | 订单行号 | DB注释(中文) |
| 12 | MTC_STS_CD | VARCHAR2(1) | Y |  | 质量保证书状态代码 | DB注释(中文) |
| 13 | MTC_REQ_DTM | VARCHAR2(14) | Y |  | 质量保证书申请时间 | DB注释(中文) |
| 14 | REMARK | VARCHAR2(500) | Y |  | ETC | DB注释(非中文) |
| 15 | MTC_CREATE_DTM | VARCHAR2(14) | Y |  | 生成时间 | DB注释(中文) |
| 16 | INSP_MTC_NO1 | VARCHAR2(50) | Y |  | 认证证书号 | DB注释(中文) |
| 17 | INSP_MTC_NO2 | VARCHAR2(50) | Y |  | 检验证书号 | DB注释(中文) |
| 18 | INSP_NM | VARCHAR2(50) | Y |  | 验船师姓名 | DB注释(中文) |

### SCR_DEFECT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=29｜被读 21 过程 / 被写 4 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：10　**主键**：PROC_CD、COIL_NO、DEF_CD　**语义覆盖**：33/33

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | PROC_CD | VARCHAR2(3) | N | ✓ | Process Code | DB注释(非中文) |
| 9 | COIL_NO | VARCHAR2(14) | N | ✓ | Coil Number | DB注释(非中文) |
| 10 | DEF_CD | VARCHAR2(4) | N | ✓ | Defect Code | DB注释(非中文) |
| 11 | DEF_GRD | VARCHAR2(10) | Y |  | Defect Grade | DB注释(非中文) |
| 12 | DEF_LOC | VARCHAR2(1) | Y |  | Defect Surface Code T, | DB注释(非中文) |
| 13 | DEF_LTH_DIR | NUMBER | Y |  | Defect length Direction | DB注释(非中文) |
| 14 | DEF_WTH_DIR | NUMBER | Y |  | Defect width Direction | DB注释(非中文) |
| 15 | DEF_LTH | NUMBER | Y |  | Defect length | DB注释(非中文) |
| 16 | DEF_CMT | VARCHAR2(330) | Y |  | Defect Comments | DB注释(非中文) |
| 17 | DEF_CMT_CD | VARCHAR2(2) | Y |  | Defect Comments Code | DB注释(非中文) |
| 18 | DEF_WK_DTM | VARCHAR2(14) | Y |  | Defect Work Date | DB注释(非中文) |
| 19 | DEF_WK_EMP_ID | VARCHAR2(20) | Y |  | Defect Worker Employee ID | DB注释(非中文) |
| 20 | REP_YN | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 21 | SAMPLE_NO | VARCHAR2(14) | Y |  | SampleId | DB注释(非中文) |
| 22 | DEF_FRE_OCCUR | VARCHAR2(20) | Y |  | DefectFreqOccur | DB注释(非中文) |
| 23 | COIL_THK | NUMBER | Y |  | stripThick | DB注释(非中文) |
| 24 | COIL_WTH | NUMBER | Y |  | stripWidth | DB注释(非中文) |
| 25 | SMP_COIL_THK | NUMBER | Y |  | sample stripThicknessAvg | DB注释(非中文) |
| 26 | SMP_COIL_WTH | NUMBER | Y |  | sample stripWidthAvg | DB注释(非中文) |
| 27 | DEF_TYPE | VARCHAR2(10) | Y |  | DefectType -PLTCM | DB注释(非中文) |
| 28 | ENTER_USER_ID | VARCHAR2(20) | Y |  | defect enter user id | DB注释(非中文) |
| 29 | ENTER_SHIFT_GROUP | VARCHAR2(2) | Y |  | defect enter shift and group | DB注释(非中文) |
| 30 | ENTER_DTM | VARCHAR2(14) | Y |  | defect enter datatime | DB注释(非中文) |
| 31 | DEF_LINE | VARCHAR2(20) | Y |  | ?????? | DB注释(非中文) |
| 32 | PROD_TOT_JDG_FL | VARCHAR2(1) | Y |  | ?????????????? | DB注释(非中文) |
| 33 | DEF_SURF_CD | VARCHAR2(1) | Y |  | Defect Surface Code | DB注释(非中文) |

### SQM_PC_MECH_RSLT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=29｜被读 25 过程 / 被写 2 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：18588　**主键**：SMP_NO、SMP_LTH_LOC、TEST_CNT　**语义覆盖**：733/1000

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | SMP_NO | VARCHAR2(14) | N | ✓ | 试样编号 | DB注释(中文) |
| 9 | SMP_LTH_LOC | VARCHAR2(1) | N | ✓ | 试样采取位置 | DB注释(中文) |
| 10 | TEST_CNT | NUMBER | N | ✓ | 试验回数 | DB注释(中文) |
| 11 | MECH_RSLT_REG_FST_DTM | VARCHAR2(14) | Y |  | 材质实绩录入最初时间 | DB注释(中文) |
| 12 | MECH_RSLT_REG_LST_DTM | VARCHAR2(14) | Y |  | 材质实绩录入最终时间 | DB注释(中文) |
| 13 | PROD_CHEM_RSLT_REG_DTM | VARCHAR2(14) | Y |  | 产品成分实绩登记时间 | DB注释(中文) |
| 14 | SMP_GTH_INST_MTRL_NO | VARCHAR2(20) | Y |  | 试样采取指示材料编号 | DB注释(中文) |
| 15 | SMP_HTM_ASGN_TY | VARCHAR2(1) | Y |  | 试样热处理指定分类 | DB注释(中文) |
| 16 | MECH_JDG_GRD | VARCHAR2(1) | Y |  | 物性判定等级 | DB注释(中文) |
| 17 | TSL_YP_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度类型 | DB注释(中文) |
| 18 | TSL_YP_RSLT | NUMBER | Y |  | 拉伸测试屈服强度实绩 | DB注释(中文) |
| 19 | TSL_YP_JDG | VARCHAR2(1) | Y |  | 拉伸测试屈服强度判定 | DB注释(中文) |
| 20 | TSL_TS_RSLT | NUMBER | Y |  | 拉伸测试抗拉强度实绩 | DB注释(中文) |
| 21 | TSL_TS_JDG | VARCHAR2(1) | Y |  | 拉伸测试抗拉强度判定 | DB注释(中文) |
| 22 | TSL_YP_TS_RSLT | NUMBER | Y |  | 拉伸试验屈强比YP/TS实绩 | DB注释(中文) |
| 23 | TSL_YP_TS_JDG | VARCHAR2(1) | Y |  | 拉伸试验屈强比YP/TS判定 | DB注释(中文) |
| 24 | TSL_RT05_RM_RSLT | NUMBER | Y |  | 拉伸试验屈强比Rt0.5/Rm实绩 | DB注释(中文) |
| 25 | TSL_RT05_RM_JDG | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt0.5/Rm判定 | DB注释(中文) |
| 26 | TSL_RT15_RT05_RSLT | NUMBER | Y |  | 拉伸试验屈强比Rt1.5/Rt0.5实绩 | DB注释(中文) |
| 27 | TSL_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt1.5/Rt0.5判定 | DB注释(中文) |
| 28 | TSL_RT20_RT10_RSLT | NUMBER | Y |  | 拉伸试验屈强比Rt2.0/Rt1.0实绩 | DB注释(中文) |
| 29 | TSL_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt2.0/Rt1.0判定 | DB注释(中文) |
| 30 | TSL_RT50_RT10_RSLT | NUMBER | Y |  | 拉伸试验屈强比Rt5.0/Rt1.0实绩 | DB注释(中文) |
| 31 | TSL_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt5.0/Rt1.0判定 | DB注释(中文) |
| 32 | TSL_CT_EX_RA_RSLT | NUMBER | Y |  | 拉抻测试断后伸长率实绩 | DB注释(中文) |
| 33 | TSL_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 拉抻测试断后伸长率类型 | DB注释(中文) |
| 34 | TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 拉抻测试断后伸长率判定 | DB注释(中文) |
| 35 | TSL_CT_RA_RSLT | NUMBER | Y |  | 拉伸试验均匀伸长率实绩 | DB注释(中文) |
| 36 | TSL_CT_RA_JDG | VARCHAR2(1) | Y |  | 拉伸试验均匀伸长率判定 | DB注释(中文) |
| 37 | TSL_RA_RSLT | NUMBER | Y |  | 拉伸试验断面收缩率实绩 | DB注释(中文) |
| 38 | TSL_RA_JDG | VARCHAR2(1) | Y |  | 拉伸试验断面收缩率判定 | DB注释(中文) |
| 39 | TSL_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 消应力处理_保温温度实绩 | DB注释(中文) |
| 40 | TSL_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 消应力处理_保温时间实绩 | DB注释(中文) |
| 41 | TSL_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 消应力处理_冷却方式 | DB注释(中文) |
| 42 | TSL_STRESS_JDG | VARCHAR2(1) | Y |  | 消应力处理_判定 | DB注释(中文) |
| 43 | IMPACT_TEMP_RSLT | NUMBER | Y |  | 冲击测试温度实绩 | DB注释(中文) |
| 44 | IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 冲击测试缺口类型 | DB注释(中文) |
| 45 | IMPACT_ENERGY_CD | VARCHAR2(1) | Y |  | 冲击试样能量值类型 | DB注释(中文) |
| 46 | IMPACT_AVG_RSLT | NUMBER | Y |  | 冲击测试平均值实绩 | DB注释(中文) |
| 47 | IMPACT_IND_RSLT1 | NUMBER | Y |  | 冲击测试单值实绩1 | DB注释(中文) |
| 48 | IMPACT_IND_RSLT2 | NUMBER | Y |  | 冲击测试单值实绩2 | DB注释(中文) |
| 49 | IMPACT_IND_RSLT3 | NUMBER | Y |  | 冲击测试单值实绩3 | DB注释(中文) |
| 50 | IMPACT_IND_JDG | VARCHAR2(1) | Y |  | 冲击测试单值判定 | DB注释(中文) |
| 51 | IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 纤维断面率平均值实绩 | DB注释(中文) |
| 52 | IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 纤维断面率单值实绩1 | DB注释(中文) |
| 53 | IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 纤维断面率单值实绩2 | DB注释(中文) |
| 54 | IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 纤维断面率单值实绩3 | DB注释(中文) |
| 55 | IMPACT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 纤维断面率单值判定 | DB注释(中文) |
| 56 | IMPACT_SMP_AVG_RSLT | NUMBER | Y |  | 冲击试样侧膨胀值平均值实绩 | DB注释(中文) |
| 57 | IMPACT_SMP_IND_RSLT1 | NUMBER | Y |  | 冲击试样侧膨胀值单值实绩1 | DB注释(中文) |
| 58 | IMPACT_SMP_IND_RSLT2 | NUMBER | Y |  | 冲击试样侧膨胀值单值实绩2 | DB注释(中文) |
| 59 | IMPACT_SMP_IND_RSLT3 | NUMBER | Y |  | 冲击试样侧膨胀值单值实绩3 | DB注释(中文) |
| 60 | IMPACT_SMP_IND_JDG | VARCHAR2(1) | Y |  | 冲击试样侧膨胀值单值判定 | DB注释(中文) |
| 61 | Z_TSL_CUT_IND_RSLT1 | NUMBER | Y |  | Z向拉伸断面收缩率单值实绩1 | DB注释(中文) |
| 62 | Z_TSL_CUT_IND_RSLT2 | NUMBER | Y |  | Z向拉伸断面收缩率单值实绩2 | DB注释(中文) |
| 63 | Z_TSL_CUT_IND_RSLT3 | NUMBER | Y |  | Z向拉伸断面收缩率单值实绩3 | DB注释(中文) |
| 64 | Z_TSL_CUT_IND_JDG | VARCHAR2(1) | Y |  | Z向拉伸断面收缩率单值判定 | DB注释(中文) |
| 65 | Z_TSL_CUT_AVG_RSLT | NUMBER | Y |  | Z向拉伸断面收缩率平均值实绩 | DB注释(中文) |
| 66 | Z_TSL_CUT_AVG_JDG | VARCHAR2(1) | Y |  | Z向拉伸断面收缩率平均值判定 | DB注释(中文) |
| 67 | Z_TSL_YP_RSLT | NUMBER | Y |  | Z向拉伸试验屈服强度实绩 | DB注释(中文) |
| 68 | Z_TSL_YP_JDG | VARCHAR2(1) | Y |  | Z向拉伸试验屈服强度判定 | DB注释(中文) |
| 69 | Z_TSL_TS_RSLT | NUMBER | Y |  | Z向拉伸试验抗拉强度实绩 | DB注释(中文) |
| 70 | Z_TSL_TS_JDG | VARCHAR2(1) | Y |  | Z向拉伸试验抗拉强度判定 | DB注释(中文) |
| 71 | Z_TSL_CT_EX_RA_RSLT | NUMBER | Y |  | Z向拉伸试验断后伸长率实绩 | DB注释(中文) |
| 72 | Z_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | Z向拉伸试验断后伸长率判定 | DB注释(中文) |
| 73 | HIGH_TEMP_TSL_STAND_CD | VARCHAR2(20) | Y |  | 高温拉伸测试试验标准类型 | DB注释(中文) |
| 74 | HIGH_TEMP_TSL_TEMP_RSLT | NUMBER | Y |  | 高温拉伸测试温度实绩 | DB注释(中文) |
| 75 | HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  | 高温拉伸测试抗拉强度TS实绩 | DB注释(中文) |
| 76 | HIGH_TEMP_TSL_TS_JDG | VARCHAR2(1) | Y |  | 高温拉伸测试抗拉强度TS判定 | DB注释(中文) |
| 77 | HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  | 高温拉伸测试屈服强度类型 | DB注释(中文) |
| 78 | HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  | 高温拉伸测试屈服强度YP实绩 | DB注释(中文) |
| 79 | HIGH_TEMP_TSL_YP_JDG | VARCHAR2(1) | Y |  | 高温拉伸测试屈服强度YP判定 | DB注释(中文) |
| 80 | HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  | 高温拉伸测试伸长率类型 | DB注释(中文) |
| 81 | HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  | 高温拉伸测试伸长率EL实绩 | DB注释(中文) |
| 82 | HIGH_TEMP_TSL_EL_JDG | VARCHAR2(1) | Y |  | 高温拉伸测试伸长率EL判定 | DB注释(中文) |
| 83 | HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  | 高温拉伸断面收缩率实绩 | DB注释(中文) |
| 84 | HIGH_TEMP_TSL_RA_JDG | VARCHAR2(1) | Y |  | 高温拉伸断面收缩率判定 | DB注释(中文) |
| 85 | DWTT_TEMP_SIGN | VARCHAR2(1) | Y |  | DWTT试验温度符号 | DB注释(中文) |
| 86 | DWTT_TEMP_RSLT | NUMBER | Y |  | DWTT试验温度实绩 | DB注释(中文) |
| 87 | DWTT_CREAK_CD | VARCHAR2(1) | Y |  | DWTT测试缺口类型 | DB注释(中文) |
| 88 | DWTT1_SA_RATIO_AVG_RSLT | NUMBER | Y |  | DWTT1纤维断面率SA平均值实绩 | DB注释(中文) |
| 89 | DWTT1_SA_RATIO_IND_RSLT1 | NUMBER | Y |  | DWTT1纤维断面率SA单值实绩1 | DB注释(中文) |
| 90 | DWTT1_SA_RATIO_IND_RSLT2 | NUMBER | Y |  | DWTT1纤维断面率SA单值实绩2 | DB注释(中文) |
| 91 | DWTT1_SA_RATIO_IND_JDG | VARCHAR2(1) | Y |  | DWTT1纤维断面率SA单值判定 | DB注释(中文) |
| 92 | DWTT2_SA_RATIO_AVG_RSLT | NUMBER | Y |  | DWTT2纤维断面率SA平均值实绩 | DB注释(中文) |
| 93 | DWTT2_SA_RATIO_IND_RSLT1 | NUMBER | Y |  | DWTT2纤维断面率SA单值实绩1 | DB注释(中文) |
| 94 | DWTT2_SA_RATIO_IND_RSLT2 | NUMBER | Y |  | DWTT2纤维断面率SA单值实绩2 | DB注释(中文) |
| 95 | DWTT2_SA_RATIO_IND_JDG | VARCHAR2(1) | Y |  | DWTT2纤维断面率SA单值判定 | DB注释(中文) |
| 96 | DWTT3_SA_RATIO_AVG_RSLT | NUMBER | Y |  | DWTT3纤维断面率SA平均值实绩 | DB注释(中文) |
| 97 | DWTT3_SA_RATIO_IND_RSLT1 | NUMBER | Y |  | DWTT3纤维断面率SA单值实绩1 | DB注释(中文) |
| 98 | DWTT3_SA_RATIO_IND_RSLT2 | NUMBER | Y |  | DWTT3纤维断面率SA单值实绩2 | DB注释(中文) |
| 99 | DWTT3_SA_RATIO_IND_JDG | VARCHAR2(1) | Y |  | DWTT3纤维断面率SA单值判定 | DB注释(中文) |
| 100 | DWTT4_SA_RATIO_AVG_RSLT | NUMBER | Y |  | DWTT4纤维断面率SA平均值实绩 | DB注释(中文) |
| 101 | DWTT4_SA_RATIO_IND_RSLT1 | NUMBER | Y |  | DWTT4纤维断面率SA单值实绩1 | DB注释(中文) |
| 102 | DWTT4_SA_RATIO_IND_RSLT2 | NUMBER | Y |  | DWTT4纤维断面率SA单值实绩2 | DB注释(中文) |
| 103 | DWTT4_SA_RATIO_IND_JDG | VARCHAR2(1) | Y |  | DWTT4纤维断面率SA单值判定 | DB注释(中文) |
| 104 | DWTT5_SA_RATIO_AVG_RSLT | NUMBER | Y |  | DWTT5纤维断面率SA平均值实绩 | DB注释(中文) |
| 105 | DWTT5_SA_RATIO_IND_RSLT1 | NUMBER | Y |  | DWTT5纤维断面率SA单值实绩1 | DB注释(中文) |
| 106 | DWTT5_SA_RATIO_IND_RSLT2 | NUMBER | Y |  | DWTT5纤维断面率SA单值实绩2 | DB注释(中文) |
| 107 | DWTT5_SA_RATIO_IND_JDG | VARCHAR2(1) | Y |  | DWTT5纤维断面率SA单值判定 | DB注释(中文) |
| 108 | SSCC_SOLUTION_KIND | VARCHAR2(20) | Y |  | SSCC测试溶液种类 | DB注释(中文) |
| 109 | SSCC_STRESS_TY | VARCHAR2(1) | Y |  | SSCC测试应力区分 | DB注释(中文) |
| 110 | SSCC_STRESS_TST_VAL_RSLT | NUMBER | Y |  | SSCC测试应力实绩 | DB注释(中文) |
| 111 | SSCC_STRESS_TST_VAL_JDG | VARCHAR2(1) | Y |  | SSCC测试应力判定 | DB注释(中文) |
| 112 | SSCC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  | SSCC执行标准 | DB注释(中文) |
| 113 | HIC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  | 执行标准 | DB注释(中文) |
| 114 | HIC_SOLUTION_KIND | VARCHAR2(20) | Y |  | HIC测试溶液种类 | DB注释(中文) |
| 115 | HIC_CLR_EACH1_RSLT1 | NUMBER | Y |  | HIC测试CLR试样1单个实绩1 | DB注释(中文) |
| 116 | HIC_CLR_EACH1_RSLT2 | NUMBER | Y |  | HIC测试CLR试样1单个实绩2 | DB注释(中文) |
| 117 | HIC_CLR_EACH1_RSLT3 | NUMBER | Y |  | HIC测试CLR试样1单个实绩3 | DB注释(中文) |
| 118 | HIC_CLR_EACH2_RSLT1 | NUMBER | Y |  | HIC测试CLR试样2单个实绩1 | DB注释(中文) |
| 119 | HIC_CLR_EACH2_RSLT2 | NUMBER | Y |  | HIC测试CLR试样2单个实绩2 | DB注释(中文) |
| 120 | HIC_CLR_EACH2_RSLT3 | NUMBER | Y |  | HIC测试CLR试样2单个实绩3 | DB注释(中文) |
| 121 | HIC_CLR_EACH3_RSLT1 | NUMBER | Y |  | HIC测试CLR试样3单个实绩1 | DB注释(中文) |
| 122 | HIC_CLR_EACH3_RSLT2 | NUMBER | Y |  | HIC测试CLR试样3单个实绩2 | DB注释(中文) |
| 123 | HIC_CLR_EACH3_RSLT3 | NUMBER | Y |  | HIC测试CLR试样3单个实绩3 | DB注释(中文) |
| 124 | HIC_CLR_EACH_JDG | VARCHAR2(1) | Y |  | HIC测试CLR单个判定 | DB注释(中文) |
| 125 | HIC_CLR_SPCMN_AVG1_RSLT | NUMBER | Y |  | HIC测试CLR试样平均1实绩 | DB注释(中文) |
| 126 | HIC_CLR_SPCMN_AVG2_RSLT | NUMBER | Y |  | HIC测试CLR试样平均2实绩 | DB注释(中文) |
| 127 | HIC_CLR_SPCMN_AVG3_RSLT | NUMBER | Y |  | HIC测试CLR试样平均3实绩 | DB注释(中文) |
| 128 | HIC_CLR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CLR试样平均判定 | DB注释(中文) |
| 129 | HIC_CLR_TOT_AVG_RSLT | NUMBER | Y |  | HIC测试CLR全体平均实绩 | DB注释(中文) |
| 130 | HIC_CLR_TOT_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CLR全体平均判定 | DB注释(中文) |
| 131 | HIC_CSR_EACH1_RSLT1 | NUMBER | Y |  | HIC测试CSR1单个实绩1 | DB注释(中文) |
| 132 | HIC_CSR_EACH1_RSLT2 | NUMBER | Y |  | HIC测试CSR1单个实绩2 | DB注释(中文) |
| 133 | HIC_CSR_EACH1_RSLT3 | NUMBER | Y |  | HIC测试CSR1单个实绩3 | DB注释(中文) |
| 134 | HIC_CSR_EACH2_RSLT1 | NUMBER | Y |  | HIC测试CSR2单个实绩1 | DB注释(中文) |
| 135 | HIC_CSR_EACH2_RSLT2 | NUMBER | Y |  | HIC测试CSR2单个实绩2 | DB注释(中文) |
| 136 | HIC_CSR_EACH2_RSLT3 | NUMBER | Y |  | HIC测试CSR2单个实绩3 | DB注释(中文) |
| 137 | HIC_CSR_EACH3_RSLT1 | NUMBER | Y |  | HIC测试CSR3单个实绩1 | DB注释(中文) |
| 138 | HIC_CSR_EACH3_RSLT2 | NUMBER | Y |  | HIC测试CSR3单个实绩2 | DB注释(中文) |
| 139 | HIC_CSR_EACH3_RSLT3 | NUMBER | Y |  | HIC测试CSR3单个实绩3 | DB注释(中文) |
| 140 | HIC_CSR_EACH_JDG | VARCHAR2(1) | Y |  | HIC测试CSR单个判定 | DB注释(中文) |
| 141 | HIC_CSR_SPCMN_AVG1_RSLT | NUMBER | Y |  | HIC测试CSR试样平均1实绩 | DB注释(中文) |
| 142 | HIC_CSR_SPCMN_AVG2_RSLT | NUMBER | Y |  | HIC测试CSR试样平均2实绩 | DB注释(中文) |
| 143 | HIC_CSR_SPCMN_AVG3_RSLT | NUMBER | Y |  | HIC测试CSR试样平均3实绩 | DB注释(中文) |
| 144 | HIC_CSR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CSR试样平均判定 | DB注释(中文) |
| 145 | HIC_CSR_TOT_AVG_RSLT | NUMBER | Y |  | HIC测试CSR全体平均实绩 | DB注释(中文) |
| 146 | HIC_CSR_TOT_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CSR全体平均判定 | DB注释(中文) |
| 147 | HIC_CTR_EACH1_RSLT1 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 148 | HIC_CTR_EACH1_RSLT2 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 149 | HIC_CTR_EACH1_RSLT3 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 150 | HIC_CTR_EACH2_RSLT1 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 151 | HIC_CTR_EACH2_RSLT2 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 152 | HIC_CTR_EACH2_RSLT3 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 153 | HIC_CTR_EACH3_RSLT1 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 154 | HIC_CTR_EACH3_RSLT2 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 155 | HIC_CTR_EACH3_RSLT3 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 156 | HIC_CTR_EACH_JDG | VARCHAR2(1) | Y |  | HIC测试CTR单个判定 | DB注释(中文) |
| 157 | HIC_CTR_SPCMN_AVG1_RSLT | NUMBER | Y |  | HIC测试CTR试样平均1实绩 | DB注释(中文) |
| 158 | HIC_CTR_SPCMN_AVG2_RSLT | NUMBER | Y |  | HIC测试CTR试样平均2实绩 | DB注释(中文) |
| 159 | HIC_CTR_SPCMN_AVG3_RSLT | NUMBER | Y |  | HIC测试CTR试样平均3实绩 | DB注释(中文) |
| 160 | HIC_CTR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CTR试样平均判定 | DB注释(中文) |
| 161 | HIC_CTR_TOT_AVG_RSLT | NUMBER | Y |  | HIC测试CTR全体平均实绩 | DB注释(中文) |
| 162 | HIC_CTR_TOT_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CTR全体平均判定 | DB注释(中文) |
| 163 | MGRPHY_MTLGRP_TY | VARCHAR2(20) | Y |  | 组织类型 | DB注释(中文) |
| 164 | MGRPHY_MTLGRP_TY_PROVIDE | VARCHAR2(1) | Y |  | 组织类型是否提供 | DB注释(中文) |
| 165 | MGRPHY_BAND_STRC_GRD_MAX_RSLT | NUMBER | Y |  | 带状组织等级上限实绩 | DB注释(中文) |
| 166 | MGRPHY_BAND_STRC_GRD_MAX_JDG | VARCHAR2(1) | Y |  | 带状组织等级上限判定 | DB注释(中文) |
| 167 | MGRPHY_RSLT | NUMBER | Y |  |  | 空 |
| 168 | MGRPHY_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 169 | MGRPHY_FGS_RSLT | NUMBER | Y |  | 铁素体晶粒度实绩 | DB注释(中文) |
| 170 | MGRPHY_FGS_JDG | VARCHAR2(1) | Y |  | 铁素体晶粒度判定 | DB注释(中文) |
| 171 | MGRPHY_AGS_RSLT | NUMBER | Y |  | 奥氏体晶粒度实绩 | DB注释(中文) |
| 172 | MGRPHY_AGS_JDG | VARCHAR2(1) | Y |  | 奥氏体晶粒度判定 | DB注释(中文) |
| 173 | MGRPHY_GRNSZ_OCCP_RSLT | NUMBER | Y |  | 金相测试基相的体积分数实绩 | DB注释(中文) |
| 174 | MGRPHY_GRNSZ_OCCP_JDG | VARCHAR2(1) | Y |  | 金相测试基相的体积分数判定 | DB注释(中文) |
| 175 | NON_METAL_KIND_CD | VARCHAR2(1) | Y |  | 非金属夹杂物类别 | DB注释(中文) |
| 176 | NON_METAL_A_GRP_RSLT | NUMBER | Y |  | 夹杂物类别_A类（粗系）上限实绩 | DB注释(中文) |
| 177 | NON_METAL_A_DETAIL_RSLT | NUMBER | Y |  | 夹杂物类别_A类（细系）上限实绩 | DB注释(中文) |
| 178 | NON_METAL_A_GRP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 179 | NON_METAL_A_RSLT | NUMBER | Y |  | 夹杂物类别_A类上限实绩 | DB注释(中文) |
| 180 | NON_METAL_A_JDG | VARCHAR2(1) | Y |  | 夹杂物类别_A类判定 | DB注释(中文) |
| 181 | NON_METAL_B_GRP_RSLT | NUMBER | Y |  | 夹杂物类别_B类（粗系）上限实绩 | DB注释(中文) |
| 182 | NON_METAL_B_DETAIL_RSLT | NUMBER | Y |  | 夹杂物类别_B类（细系）上限实绩 | DB注释(中文) |
| 183 | NON_METAL_B_GRP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 184 | NON_METAL_B_RSLT | NUMBER | Y |  | 夹杂物类别_B类上限实绩 | DB注释(中文) |
| 185 | NON_METAL_B_JDG | VARCHAR2(1) | Y |  | 夹杂物类别_B类判定 | DB注释(中文) |
| 186 | NON_METAL_C_GRP_RSLT | NUMBER | Y |  | 夹杂物类别_C类（粗系）上限实绩 | DB注释(中文) |
| 187 | NON_METAL_C_DETAIL_RSLT | NUMBER | Y |  | 夹杂物类别_C类（细系）上限实绩 | DB注释(中文) |
| 188 | NON_METAL_C_GRP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 189 | NON_METAL_C_RSLT | NUMBER | Y |  | 夹杂物类别_C类上限实绩 | DB注释(中文) |
| 190 | NON_METAL_C_JDG | VARCHAR2(1) | Y |  | 夹杂物类别_C类判定 | DB注释(中文) |
| 191 | NON_METAL_D_GRP_RSLT | NUMBER | Y |  | 夹杂物类别_D类（粗系）上限实绩 | DB注释(中文) |
| 192 | NON_METAL_D_DETAIL_RSLT | NUMBER | Y |  | 夹杂物类别_D类（细系）上限实绩 | DB注释(中文) |
| 193 | NON_METAL_D_GRP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 194 | NON_METAL_D_RSLT | NUMBER | Y |  | 夹杂物类别_D类上限实绩 | DB注释(中文) |
| 195 | NON_METAL_D_JDG | VARCHAR2(1) | Y |  | 夹杂物类别_D类判定 | DB注释(中文) |
| 196 | NON_METAL_DS_RSLT | NUMBER | Y |  | 夹杂物类别_DS类上限实绩 | DB注释(中文) |
| 197 | NON_METAL_DS_JDG | VARCHAR2(1) | Y |  | 夹杂物类别_DSDs判定 | DB注释(中文) |
| 198 | NON_METAL_ABCD_RSLT | NUMBER | Y |  | 夹杂物类别_DSA+B+C+D上限实绩 | DB注释(中文) |
| 199 | NON_METAL_ABCD_JDG | VARCHAR2(1) | Y |  | 夹杂物类别_DSA+B+C+D判定 | DB注释(中文) |
| 200 | NON_METAL_AC_RSLT | NUMBER | Y |  | 夹杂物类别_A+C上限实绩 | DB注释(中文) |
| 201 | NON_METAL_AC_JDG | VARCHAR2(1) | Y |  | 夹杂物类别_A+C判定 | DB注释(中文) |
| 202 | NON_METAL_BDDS_RSLT | NUMBER | Y |  | 夹杂物类别_B+D+Ds上限实绩 | DB注释(中文) |
| 203 | NON_METAL_BDDS_JDG | VARCHAR2(1) | Y |  | 夹杂物类别_B+D+Ds判定 | DB注释(中文) |
| 204 | BEND_DIA | NUMBER | Y |  | 弯曲测试弯心直径 | DB注释(中文) |
| 205 | BEND_ANGLE | NUMBER | Y |  | 弯曲测试弯曲角度 | DB注释(中文) |
| 206 | BEND_RSLT | VARCHAR2(1) | Y |  | 弯曲测试实绩 | DB注释(中文) |
| 207 | BEND_JDG | VARCHAR2(1) | Y |  | 弯曲测试判定 | DB注释(中文) |
| 208 | CPLATE_CUT_STRESS_RSLT | NUMBER | Y |  | 抗剪强度τ实绩 | DB注释(中文) |
| 209 | CPLATE_CUT_STRESS_JDG | VARCHAR2(1) | Y |  | 抗剪强度τ判定 | DB注释(中文) |
| 210 | CPLATE_THK_RSLT | NUMBER | Y |  | 复层厚度实绩 | DB注释(中文) |
| 211 | CPLATE_THK_JDG | VARCHAR2(1) | Y |  | 复层厚度判定 | DB注释(中文) |
| 212 | CPLATE_ER_IE_RSLT | NUMBER | Y |  | 杯突IE实绩 | DB注释(中文) |
| 213 | CPLATE_ER_IE_JDG | VARCHAR2(1) | Y |  | 杯突IE判定 | DB注释(中文) |
| 214 | CPLATE_IN_BD_DIA_D_RSLT | NUMBER | Y |  | 内弯弯曲压头直径D | DB注释(中文) |
| 215 | CPLATE_IN_BD_ANGLE_RSLT | NUMBER | Y |  | 内弯弯曲角度 | DB注释(中文) |
| 216 | CPLATE_IN_BD_WTH_RSLT | VARCHAR2(7) | Y |  | 内弯试样宽度 | DB注释(中文) |
| 217 | CPLATE_IN_BD_RSLT | VARCHAR2(1) | Y |  | 复层弯曲内弯结果 | DB注释(中文) |
| 218 | CPLATE_IN_BD_JDG | VARCHAR2(1) | Y |  | 复层弯曲内弯判定 | DB注释(中文) |
| 219 | CPLATE_OT_BD_DIA_D_RSLT | NUMBER | Y |  | 外弯弯曲压头直径D | DB注释(中文) |
| 220 | CPLATE_OT_BD_ANGLE_RSLT | NUMBER | Y |  | 外弯弯曲角度 | DB注释(中文) |
| 221 | CPLATE_OT_BD_WTH_RSLT | VARCHAR2(7) | Y |  | 外弯试样宽度 | DB注释(中文) |
| 222 | CPLATE_OT_BD_RSLT | VARCHAR2(1) | Y |  | 复层弯曲外弯结果 | DB注释(中文) |
| 223 | CPLATE_OT_BD_JDG | VARCHAR2(1) | Y |  | 复层弯曲外弯判定 | DB注释(中文) |
| 224 | CPLATE_SIDE_BD_DIA_D_RSLT | NUMBER | Y |  | 侧弯弯曲压头直径D | DB注释(中文) |
| 225 | CPLATE_SIDE_BD_ANGLE_RSLT | NUMBER | Y |  | 侧弯弯曲角度 | DB注释(中文) |
| 226 | CPLATE_SIDE_BD_WTH_RSLT | VARCHAR2(7) | Y |  | 侧弯试样宽度 | DB注释(中文) |
| 227 | CPLATE_SIDE_BD_RSLT | VARCHAR2(1) | Y |  | 复层弯曲侧弯结果 | DB注释(中文) |
| 228 | CPLATE_SIDE_BD_JDG | VARCHAR2(1) | Y |  | 复层弯曲侧弯判定 | DB注释(中文) |
| 229 | HARD_KIND | VARCHAR2(1) | Y |  | 硬度试验种类 | DB注释(中文) |
| 230 | HARD_AVG_RSLT | NUMBER | Y |  | 硬度平均值实绩 | DB注释(中文) |
| 231 | HARD_IND_JDG | VARCHAR2(1) | Y |  | 硬度单值判定 | DB注释(中文) |
| 232 | HARD_AVG_JDG | VARCHAR2(1) | Y |  | 硬度平均值判定 | DB注释(中文) |
| 233 | S_PRINT_KIND | VARCHAR2(1) | Y |  | S_Print试验种类 | DB注释(中文) |
| 234 | S_PRINT_RSLT | NUMBER | Y |  | 硫印测试实绩 | DB注释(中文) |
| 235 | S_PRINT_JDG | VARCHAR2(1) | Y |  | 硫印测试判定 | DB注释(中文) |
| 236 | AGE_TST_STRESS_RSLT | NUMBER | Y |  | 时效应变量实绩 | DB注释(中文) |
| 237 | AGE_TST_STRESS_JDG | VARCHAR2(1) | Y |  | 时效应变量判定 | DB注释(中文) |
| 238 | AGE_TST_AGE_TIME_RSLT | NUMBER | Y |  | 时效温度实绩 | DB注释(中文) |
| 239 | AGE_TST_AGE_TIME_JDG | VARCHAR2(1) | Y |  | 时效温度判定 | DB注释(中文) |
| 240 | AGE_TST_AGE_TEMP_RSLT | NUMBER | Y |  | 保温时间实绩 | DB注释(中文) |
| 241 | AGE_TST_AGE_TEMP_JDG | VARCHAR2(1) | Y |  | 保温时间判定 | DB注释(中文) |
| 242 | AGE_TST_YP_CD | VARCHAR2(1) | Y |  | 时效拉伸测试屈服强度类型 | DB注释(中文) |
| 243 | AGE_TST_YP_RSLT | NUMBER | Y |  | 时效拉伸测试屈服强度实绩 | DB注释(中文) |
| 244 | AGE_TST_YP_JDG | VARCHAR2(1) | Y |  | 时效拉伸测试屈服强度判定 | DB注释(中文) |
| 245 | AGE_TST_TS_RSLT | NUMBER | Y |  | 时效拉伸测试抗拉强度实绩 | DB注释(中文) |
| 246 | AGE_TST_TS_JDG | VARCHAR2(1) | Y |  | 时效拉伸测试抗拉强度判定 | DB注释(中文) |
| 247 | AGE_TST_YP_TS_RSLT | NUMBER | Y |  | 时效拉伸试验屈强比YP/TS实绩 | DB注释(中文) |
| 248 | AGE_TST_YP_TS_JDG | VARCHAR2(1) | Y |  | 时效拉伸试验屈强比YP/TS判定 | DB注释(中文) |
| 249 | AGE_TST_RT05_RM_RSLT | NUMBER | Y |  | 时效拉伸试验屈强比Rt0.5/Rm实绩 | DB注释(中文) |
| 250 | AGE_TST_RT05_RM_JDG | VARCHAR2(1) | Y |  | 时效拉伸试验屈强比Rt0.5/Rm判定 | DB注释(中文) |
| 251 | AGE_TST_RT15_RT05_RSLT | NUMBER | Y |  | 时效拉伸试验屈强比Rt1.5/Rt0.5实绩 | DB注释(中文) |
| 252 | AGE_TST_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 时效拉伸试验屈强比Rt1.5/Rt0.5判定 | DB注释(中文) |
| 253 | AGE_TST_RT20_RT10_RSLT | NUMBER | Y |  | 时效拉伸试验屈强比Rt2.0/Rt1.0实绩 | DB注释(中文) |
| 254 | AGE_TST_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 时效拉伸试验屈强比Rt2.0/Rt1.0判定 | DB注释(中文) |
| 255 | AGE_TST_RT50_RT10_RSLT | NUMBER | Y |  | 时效拉伸试验屈强比Rt5.0/Rt1.0实绩 | DB注释(中文) |
| 256 | AGE_TST_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 时效拉伸试验屈强比Rt5.0/Rt1.0判定 | DB注释(中文) |
| 257 | AGE_TST_CT_EX_RA_RSLT | NUMBER | Y |  | 拉抻测试断后伸长率实绩 | DB注释(中文) |
| 258 | AGE_TST_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 拉抻测试断后伸长率类型 | DB注释(中文) |
| 259 | AGE_TST_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 拉抻测试断后伸长率判定 | DB注释(中文) |
| 260 | AGE_TST_CT_RA_RSLT | NUMBER | Y |  | 时效拉伸试验均匀伸长率实绩 | DB注释(中文) |
| 261 | AGE_TST_CT_RA_JDG | VARCHAR2(1) | Y |  | 时效拉伸试验均匀伸长率判定 | DB注释(中文) |
| 262 | AGE_TST_RA_RSLT | NUMBER | Y |  | 时效拉伸试验断面收缩率实绩 | DB注释(中文) |
| 263 | AGE_TST_RA_JDG | VARCHAR2(1) | Y |  | 时效拉伸试验断面收缩率判定 | DB注释(中文) |
| 264 | AGE_TST1_TEMP_RSLT | NUMBER | Y |  | 时效冲击1测试温度实绩 | DB注释(中文) |
| 265 | AGE_TST1_CREAK_CD | VARCHAR2(1) | Y |  | 时效冲击1测试缺口类型 | DB注释(中文) |
| 266 | AGE_TST1_AVG_RSLT | NUMBER | Y |  | 时效冲击1测试平均值实绩 | DB注释(中文) |
| 267 | AGE_TST1_IND_RSLT1 | NUMBER | Y |  | 时效冲击1测试单值实绩1 | DB注释(中文) |
| 268 | AGE_TST1_IND_RSLT2 | NUMBER | Y |  | 时效冲击1测试单值实绩2 | DB注释(中文) |
| 269 | AGE_TST1_IND_RSLT3 | NUMBER | Y |  | 时效冲击1测试单值实绩3 | DB注释(中文) |
| 270 | AGE_TST1_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击1测试单值判定 | DB注释(中文) |
| 271 | AGE_TST1_SMP_AVG_RSLT | NUMBER | Y |  | 纤维断面率1平均值实绩 | DB注释(中文) |
| 272 | AGE_TST1_SMP_IND_RSLT1 | NUMBER | Y |  | 纤维断面率1单值实绩1 | DB注释(中文) |
| 273 | AGE_TST1_SMP_IND_RSLT2 | NUMBER | Y |  | 纤维断面率1单值实绩2 | DB注释(中文) |
| 274 | AGE_TST1_SMP_IND_RSLT3 | NUMBER | Y |  | 纤维断面率1单值实绩3 | DB注释(中文) |
| 275 | AGE_TST1_SMP_IND_JDG | VARCHAR2(1) | Y |  | 纤维断面率1单值判定 | DB注释(中文) |
| 276 | AGE_TST1_SIDE_EXP_AVG_RSLT | NUMBER | Y |  | 时效冲击1试样侧膨胀值平均值实绩 | DB注释(中文) |
| 277 | AGE_TST1_SIDE_EXP_IND_RSLT1 | NUMBER | Y |  | 时效冲击1试样侧膨胀值单值实绩1 | DB注释(中文) |
| 278 | AGE_TST1_SIDE_EXP_IND_RSLT2 | NUMBER | Y |  | 时效冲击1试样侧膨胀值单值实绩2 | DB注释(中文) |
| 279 | AGE_TST1_SIDE_EXP_IND_RSLT3 | NUMBER | Y |  | 时效冲击1试样侧膨胀值单值实绩3 | DB注释(中文) |
| 280 | AGE_TST1_SIDE_EXP_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击1试样侧膨胀值单值判定 | DB注释(中文) |
| 281 | AGE_TST2_TEMP_RSLT | NUMBER | Y |  | 时效冲击2测试温度实绩 | DB注释(中文) |
| 282 | AGE_TST2_CREAK_CD | VARCHAR2(1) | Y |  | 时效冲击2测试缺口类型 | DB注释(中文) |
| 283 | AGE_TST2_AVG_RSLT | NUMBER | Y |  | 时效冲击2测试平均值实绩 | DB注释(中文) |
| 284 | AGE_TST2_IND_RSLT1 | NUMBER | Y |  | 时效冲击2测试单值实绩1 | DB注释(中文) |
| 285 | AGE_TST2_IND_RSLT2 | NUMBER | Y |  | 时效冲击2测试单值实绩2 | DB注释(中文) |
| 286 | AGE_TST2_IND_RSLT3 | NUMBER | Y |  | 时效冲击2测试单值实绩3 | DB注释(中文) |
| 287 | AGE_TST2_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击2测试单值判定 | DB注释(中文) |
| 288 | AGE_TST2_SMP_AVG_RSLT | NUMBER | Y |  | 纤维断面率2平均值实绩 | DB注释(中文) |
| 289 | AGE_TST2_SMP_IND_RSLT1 | NUMBER | Y |  | 纤维断面率2单值实绩1 | DB注释(中文) |
| 290 | AGE_TST2_SMP_IND_RSLT2 | NUMBER | Y |  | 纤维断面率2单值实绩2 | DB注释(中文) |
| 291 | AGE_TST2_SMP_IND_RSLT3 | NUMBER | Y |  | 纤维断面率2单值实绩3 | DB注释(中文) |
| 292 | AGE_TST2_SMP_IND_JDG | VARCHAR2(1) | Y |  | 纤维断面率2单值判定 | DB注释(中文) |
| 293 | AGE_TST2_SIDE_EXP_AVG_RSLT | NUMBER | Y |  | 时效冲击2试样侧膨胀值平均值实绩 | DB注释(中文) |
| 294 | AGE_TST2_SIDE_EXP_IND_RSLT1 | NUMBER | Y |  | 时效冲击2试样侧膨胀值单值实绩1 | DB注释(中文) |
| 295 | AGE_TST2_SIDE_EXP_IND_RSLT2 | NUMBER | Y |  | 时效冲击2试样侧膨胀值单值实绩2 | DB注释(中文) |
| 296 | AGE_TST2_SIDE_EXP_IND_RSLT3 | NUMBER | Y |  | 时效冲击2试样侧膨胀值单值实绩3 | DB注释(中文) |
| 297 | AGE_TST2_SIDE_EXP_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击2试样侧膨胀值单值判定 | DB注释(中文) |
| 298 | AGE_TST3_TEMP_RSLT | NUMBER | Y |  | 时效冲击3测试温度实绩 | DB注释(中文) |
| 299 | AGE_TST3_CREAK_CD | VARCHAR2(1) | Y |  | 时效冲击3测试缺口类型 | DB注释(中文) |
| 300 | AGE_TST3_AVG_RSLT | NUMBER | Y |  | 时效冲击3测试平均值实绩 | DB注释(中文) |
| 301 | AGE_TST3_IND_RSLT1 | NUMBER | Y |  | 时效冲击3测试单值实绩1 | DB注释(中文) |
| 302 | AGE_TST3_IND_RSLT2 | NUMBER | Y |  | 时效冲击3测试单值实绩2 | DB注释(中文) |
| 303 | AGE_TST3_IND_RSLT3 | NUMBER | Y |  | 时效冲击3测试单值实绩3 | DB注释(中文) |
| 304 | AGE_TST3_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击3测试单值判定 | DB注释(中文) |
| 305 | AGE_TST3_SMP_AVG_RSLT | NUMBER | Y |  | 纤维断面率3平均值实绩 | DB注释(中文) |
| 306 | AGE_TST3_SMP_IND_RSLT1 | NUMBER | Y |  | 纤维断面率3单值实绩1 | DB注释(中文) |
| 307 | AGE_TST3_SMP_IND_RSLT2 | NUMBER | Y |  | 纤维断面率3单值实绩2 | DB注释(中文) |
| 308 | AGE_TST3_SMP_IND_RSLT3 | NUMBER | Y |  | 纤维断面率3单值实绩3 | DB注释(中文) |
| 309 | AGE_TST3_SMP_IND_JDG | VARCHAR2(1) | Y |  | 纤维断面率3单值判定 | DB注释(中文) |
| 310 | AGE_TST3_SIDE_EXP_AVG_RSLT | NUMBER | Y |  | 时效冲击3试样侧膨胀值平均值实绩1 | DB注释(中文) |
| 311 | AGE_TST3_SIDE_EXP_IND_RSLT1 | NUMBER | Y |  | 时效冲击3试样侧膨胀值单值实绩 | DB注释(中文) |
| 312 | AGE_TST3_SIDE_EXP_IND_RSLT2 | NUMBER | Y |  | 时效冲击3试样侧膨胀值单值实绩2 | DB注释(中文) |
| 313 | AGE_TST3_SIDE_EXP_IND_RSLT3 | NUMBER | Y |  | 时效冲击3试样侧膨胀值单值实绩3 | DB注释(中文) |
| 314 | AGE_TST3_SIDE_EXP_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击3试样侧膨胀值单值判定 | DB注释(中文) |
| 315 | AGE_TST4_TEMP_RSLT | NUMBER | Y |  | 时效冲击4测试温度实绩 | DB注释(中文) |
| 316 | AGE_TST4_CREAK_CD | VARCHAR2(1) | Y |  | 时效冲击4测试缺口类型 | DB注释(中文) |
| 317 | AGE_TST4_AVG_RSLT | NUMBER | Y |  | 时效冲击4测试平均值实绩 | DB注释(中文) |
| 318 | AGE_TST4_IND_RSLT1 | NUMBER | Y |  | 时效冲击4测试单值实绩1 | DB注释(中文) |
| 319 | AGE_TST4_IND_RSLT2 | NUMBER | Y |  | 时效冲击4测试单值实绩2 | DB注释(中文) |
| 320 | AGE_TST4_IND_RSLT3 | NUMBER | Y |  | 时效冲击4测试单值实绩3 | DB注释(中文) |
| 321 | AGE_TST4_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击4测试单值判定 | DB注释(中文) |
| 322 | AGE_TST4_SMP_AVG_RSLT | NUMBER | Y |  | 纤维断面率4平均值实绩 | DB注释(中文) |
| 323 | AGE_TST4_SMP_IND_RSLT1 | NUMBER | Y |  | 纤维断面率4单值实绩1 | DB注释(中文) |
| 324 | AGE_TST4_SMP_IND_RSLT2 | NUMBER | Y |  | 纤维断面率4单值实绩2 | DB注释(中文) |
| 325 | AGE_TST4_SMP_IND_RSLT3 | NUMBER | Y |  | 纤维断面率4单值实绩3 | DB注释(中文) |
| 326 | AGE_TST4_SMP_IND_JDG | VARCHAR2(1) | Y |  | 纤维断面率4单值判定 | DB注释(中文) |
| 327 | AGE_TST4_SIDE_EXP_AVG_RSLT | NUMBER | Y |  | 时效冲击4试样侧膨胀值平均值实绩1 | DB注释(中文) |
| 328 | AGE_TST4_SIDE_EXP_IND_RSLT1 | NUMBER | Y |  | 时效冲击4试样侧膨胀值单值实绩 | DB注释(中文) |
| 329 | AGE_TST4_SIDE_EXP_IND_RSLT2 | NUMBER | Y |  | 时效冲击4试样侧膨胀值单值实绩2 | DB注释(中文) |
| 330 | AGE_TST4_SIDE_EXP_IND_RSLT3 | NUMBER | Y |  | 时效冲击4试样侧膨胀值单值实绩3 | DB注释(中文) |
| 331 | AGE_TST4_SIDE_EXP_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击4试样侧膨胀值单值判定 | DB注释(中文) |
| 332 | AGE_TST5_TEMP_RSLT | NUMBER | Y |  | 时效冲击5测试温度实绩 | DB注释(中文) |
| 333 | AGE_TST5_CREAK_CD | VARCHAR2(1) | Y |  | 时效冲击5测试缺口类型 | DB注释(中文) |
| 334 | AGE_TST5_AVG_RSLT | NUMBER | Y |  | 时效冲击5测试平均值实绩 | DB注释(中文) |
| 335 | AGE_TST5_IND_RSLT1 | NUMBER | Y |  | 时效冲击5测试单值实绩1 | DB注释(中文) |
| 336 | AGE_TST5_IND_RSLT2 | NUMBER | Y |  | 时效冲击5测试单值实绩2 | DB注释(中文) |
| 337 | AGE_TST5_IND_RSLT3 | NUMBER | Y |  | 时效冲击5测试单值实绩3 | DB注释(中文) |
| 338 | AGE_TST5_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击5测试单值判定 | DB注释(中文) |
| 339 | AGE_TST5_SMP_AVG_RSLT | NUMBER | Y |  | 纤维断面率5平均值实绩 | DB注释(中文) |
| 340 | AGE_TST5_SMP_IND_RSLT1 | NUMBER | Y |  | 纤维断面率5单值实绩1 | DB注释(中文) |
| 341 | AGE_TST5_SMP_IND_RSLT2 | NUMBER | Y |  | 纤维断面率5单值实绩2 | DB注释(中文) |
| 342 | AGE_TST5_SMP_IND_RSLT3 | NUMBER | Y |  | 纤维断面率5单值实绩3 | DB注释(中文) |
| 343 | AGE_TST5_SMP_IND_JDG | VARCHAR2(1) | Y |  | 纤维断面率5单值判定 | DB注释(中文) |
| 344 | AGE_TST5_SIDE_EXP_AVG_RSLT | NUMBER | Y |  | 时效冲击5试样侧膨胀值平均值实绩1 | DB注释(中文) |
| 345 | AGE_TST5_SIDE_EXP_IND_RSLT1 | NUMBER | Y |  | 时效冲击5试样侧膨胀值单值实绩 | DB注释(中文) |
| 346 | AGE_TST5_SIDE_EXP_IND_RSLT2 | NUMBER | Y |  | 时效冲击5试样侧膨胀值单值实绩2 | DB注释(中文) |
| 347 | AGE_TST5_SIDE_EXP_IND_RSLT3 | NUMBER | Y |  | 时效冲击5试样侧膨胀值单值实绩3 | DB注释(中文) |
| 348 | AGE_TST5_SIDE_EXP_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击5试样侧膨胀值单值判定 | DB注释(中文) |
| 349 | NDT_TEMP_RSLT | NUMBER | Y |  | NDT温度实绩 | DB注释(中文) |
| 350 | NDT_TEMP_JDG | VARCHAR2(1) | Y |  | NDT温度判定 | DB注释(中文) |
| 351 | CTOD_VAL_RSLT | NUMBER | Y |  | CTOD值实绩 | DB注释(中文) |
| 352 | CTOD_VAL_JDG | VARCHAR2(1) | Y |  | CTOD值判定 | DB注释(中文) |
| 353 | NP_JHRC_HARD_RSLT | NUMBER | Y |  | 淬透性指数_JHRC硬度实绩 | DB注释(中文) |
| 354 | NP_JHRC_HARD_JDG | VARCHAR2(1) | Y |  | 淬透性指数_JHRC硬度判定 | DB注释(中文) |
| 355 | NP_JHRC_DIST_RSLT | NUMBER | Y |  | 淬透性指数_JHRC距离实绩 | DB注释(中文) |
| 356 | NP_JHRC_DIST_JDG | VARCHAR2(1) | Y |  | 淬透性指数_JHRC距离判定 | DB注释(中文) |
| 357 | NP_JHV_HARD_RSLT | NUMBER | Y |  | 淬透性指数_JHV硬度实绩 | DB注释(中文) |
| 358 | NP_JHV_HARD_JDG | VARCHAR2(1) | Y |  | 淬透性指数_JHV硬度判定 | DB注释(中文) |
| 359 | NP_JHV_DIST_RSLT | NUMBER | Y |  | 淬透性指数_JHV距离实绩 | DB注释(中文) |
| 360 | NP_JHV_DIST_JDG | VARCHAR2(1) | Y |  | 淬透性指数_JHV距离判定 | DB注释(中文) |
| 361 | TSL1_YP_CD | VARCHAR2(1) | Y |  | 拉伸试验1屈服强度类型 | DB注释(中文) |
| 362 | TSL1_YP_RSLT | NUMBER | Y |  | 拉伸试验1屈服强度实绩 | DB注释(中文) |
| 363 | TSL1_YP_JDG | VARCHAR2(1) | Y |  | 拉伸试验1屈服强度判定 | DB注释(中文) |
| 364 | TSL1_TS_RSLT | NUMBER | Y |  | 拉伸试验1抗拉强度实绩 | DB注释(中文) |
| 365 | TSL1_TS_JDG | VARCHAR2(1) | Y |  | 拉伸试验1抗拉强度判定 | DB注释(中文) |
| 366 | TSL1_YP_TS_RSLT | NUMBER | Y |  | 拉伸试验1屈强比YP/TS实绩 | DB注释(中文) |
| 367 | TSL1_YP_TS_JDG | VARCHAR2(1) | Y |  | 拉伸试验1屈强比YP/TS判定 | DB注释(中文) |
| 368 | TSL1_RT05_RM_RSLT | NUMBER | Y |  | 拉伸试验1屈强比Rt0.5/Rm实绩 | DB注释(中文) |
| 369 | TSL1_RT05_RM_JDG | VARCHAR2(1) | Y |  | 拉伸试验1屈强比Rt0.5/Rm判定 | DB注释(中文) |
| 370 | TSL1_RT15_RT05_RSLT | NUMBER | Y |  | 拉伸试验1屈强比Rt1.5/Rt0.5实绩 | DB注释(中文) |
| 371 | TSL1_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 拉伸试验1屈强比Rt1.5/Rt0.5判定 | DB注释(中文) |
| 372 | TSL1_RT20_RT10_RSLT | NUMBER | Y |  | 拉伸试验1屈强比Rt2.0/Rt1.0实绩 | DB注释(中文) |
| 373 | TSL1_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 拉伸试验1屈强比Rt2.0/Rt1.0判定 | DB注释(中文) |
| 374 | TSL1_RT50_RT10_RSLT | NUMBER | Y |  | 拉伸试验1屈强比Rt5.0/Rt1.0实绩 | DB注释(中文) |
| 375 | TSL1_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 拉伸试验1屈强比Rt5.0/Rt1.0判定 | DB注释(中文) |
| 376 | TSL1_CT_EX_RA_RSLT | NUMBER | Y |  | 拉伸试验1断后伸长率实绩 | DB注释(中文) |
| 377 | TSL1_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 拉伸试验1断后伸长率类型 | DB注释(中文) |
| 378 | TSL1_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 拉伸试验1断后伸长率判定 | DB注释(中文) |
| 379 | TSL1_CT_RA_RSLT | NUMBER | Y |  | 拉伸试验1均匀伸长率实绩 | DB注释(中文) |
| 380 | TSL1_CT_RA_JDG | VARCHAR2(1) | Y |  | 拉伸试验1均匀伸长率判定 | DB注释(中文) |
| 381 | TSL1_RA_RSLT | NUMBER | Y |  | 拉伸试验1断面收缩率实绩 | DB注释(中文) |
| 382 | TSL1_RA_JDG | VARCHAR2(1) | Y |  | 拉伸试验1断面收缩率判定 | DB注释(中文) |
| 383 | TSL1_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 消应力处理1_保温温度实绩 | DB注释(中文) |
| 384 | TSL1_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 消应力处理1_保温时间实绩 | DB注释(中文) |
| 385 | TSL1_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 消应力处理1_冷却方式 | DB注释(中文) |
| 386 | TSL1_STRESS_JDG | VARCHAR2(1) | Y |  | 消应力处理1_判定 | DB注释(中文) |
| 387 | TSL2_YP_CD | VARCHAR2(1) | Y |  | 拉伸试验2屈服强度类型 | DB注释(中文) |
| 388 | TSL2_YP_RSLT | NUMBER | Y |  | 拉伸试验2屈服强度实绩 | DB注释(中文) |
| 389 | TSL2_YP_JDG | VARCHAR2(1) | Y |  | 拉伸试验2屈服强度判定 | DB注释(中文) |
| 390 | TSL2_TS_RSLT | NUMBER | Y |  | 拉伸试验2抗拉强度实绩 | DB注释(中文) |
| 391 | TSL2_TS_JDG | VARCHAR2(1) | Y |  | 拉伸试验2抗拉强度判定 | DB注释(中文) |
| 392 | TSL2_YP_TS_RSLT | NUMBER | Y |  | 拉伸试验2屈强比YP/TS实绩 | DB注释(中文) |
| 393 | TSL2_YP_TS_JDG | VARCHAR2(1) | Y |  | 拉伸试验2屈强比YP/TS判定 | DB注释(中文) |
| 394 | TSL2_RT05_RM_RSLT | NUMBER | Y |  | 拉伸试验2屈强比Rt0.5/Rm实绩 | DB注释(中文) |
| 395 | TSL2_RT05_RM_JDG | VARCHAR2(1) | Y |  | 拉伸试验2屈强比Rt0.5/Rm判定 | DB注释(中文) |
| 396 | TSL2_RT15_RT05_RSLT | NUMBER | Y |  | 拉伸试验2屈强比Rt1.5/Rt0.5实绩 | DB注释(中文) |
| 397 | TSL2_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 拉伸试验2屈强比Rt1.5/Rt0.5判定 | DB注释(中文) |
| 398 | TSL2_RT20_RT10_RSLT | NUMBER | Y |  | 拉伸试验2屈强比Rt2.0/Rt1.0实绩 | DB注释(中文) |
| 399 | TSL2_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 拉伸试验2屈强比Rt2.0/Rt1.0判定 | DB注释(中文) |
| 400 | TSL2_RT50_RT10_RSLT | NUMBER | Y |  | 拉伸试验2屈强比Rt5.0/Rt1.0实绩 | DB注释(中文) |
| 401 | TSL2_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 拉伸试验2屈强比Rt5.0/Rt1.0判定 | DB注释(中文) |
| 402 | TSL2_CT_EX_RA_RSLT | NUMBER | Y |  | 拉伸试验2断后伸长率实绩 | DB注释(中文) |
| 403 | TSL2_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 拉伸试验2断后伸长率类型 | DB注释(中文) |
| 404 | TSL2_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 拉伸试验2断后伸长率判定 | DB注释(中文) |
| 405 | TSL2_CT_RA_RSLT | NUMBER | Y |  | 拉伸试验2均匀伸长率实绩 | DB注释(中文) |
| 406 | TSL2_CT_RA_JDG | VARCHAR2(1) | Y |  | 拉伸试验2均匀伸长率判定 | DB注释(中文) |
| 407 | TSL2_RA_RSLT | NUMBER | Y |  | 拉伸试验2断面收缩率实绩 | DB注释(中文) |
| 408 | TSL2_RA_JDG | VARCHAR2(1) | Y |  | 拉伸试验2断面收缩率判定 | DB注释(中文) |
| 409 | TSL2_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 消应力处理2_保温温度实绩 | DB注释(中文) |
| 410 | TSL2_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 消应力处理2_保温时间实绩 | DB注释(中文) |
| 411 | TSL2_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 消应力处理2_冷却方式 | DB注释(中文) |
| 412 | TSL2_STRESS_JDG | VARCHAR2(1) | Y |  | 消应力处理2_判定 | DB注释(中文) |
| 413 | IMPACT1_TEMP_RSLT | NUMBER | Y |  | 冲击试验1温度实绩 | DB注释(中文) |
| 414 | IMPACT1_CREAK_CD | VARCHAR2(1) | Y |  | 冲击试验1缺口类型 | DB注释(中文) |
| 415 | IMPACT1_ENERGY_CD | VARCHAR2(1) | Y |  | 冲击试验1试样能量值类型 | DB注释(中文) |
| 416 | IMPACT1_AVG_RSLT | NUMBER | Y |  | 冲击试验1平均值实绩 | DB注释(中文) |
| 417 | IMPACT1_IND_RSLT1 | NUMBER | Y |  | 冲击试验1单值实绩1 | DB注释(中文) |
| 418 | IMPACT1_IND_RSLT2 | NUMBER | Y |  | 冲击试验1单值实绩2 | DB注释(中文) |
| 419 | IMPACT1_IND_RSLT3 | NUMBER | Y |  | 冲击试验1单值实绩3 | DB注释(中文) |
| 420 | IMPACT1_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验1单值判定 | DB注释(中文) |
| 421 | IMPACT1_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 冲击试验1纤维断面率平均值实绩 | DB注释(中文) |
| 422 | IMPACT1_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 冲击试验1纤维断面率单值实绩1 | DB注释(中文) |
| 423 | IMPACT1_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 冲击试验1纤维断面率单值实绩2 | DB注释(中文) |
| 424 | IMPACT1_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 冲击试验1纤维断面率单值实绩3 | DB注释(中文) |
| 425 | IMPACT1_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验1纤维断面率单值判定 | DB注释(中文) |
| 426 | IMPACT1_SMP_AVG_RSLT | NUMBER | Y |  | 冲击试验1试样侧膨胀值平均值实绩 | DB注释(中文) |
| 427 | IMPACT1_SMP_IND_RSLT1 | NUMBER | Y |  | 冲击试验1试样侧膨胀值单值实绩1 | DB注释(中文) |
| 428 | IMPACT1_SMP_IND_RSLT2 | NUMBER | Y |  | 冲击试验1试样侧膨胀值单值实绩2 | DB注释(中文) |
| 429 | IMPACT1_SMP_IND_RSLT3 | NUMBER | Y |  | 冲击试验1试样侧膨胀值单值实绩3 | DB注释(中文) |
| 430 | IMPACT1_SMP_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验1试样侧膨胀值单值判定 | DB注释(中文) |
| 431 | IMPACT2_TEMP_RSLT | NUMBER | Y |  | 冲击试验2温度实绩 | DB注释(中文) |
| 432 | IMPACT2_CREAK_CD | VARCHAR2(1) | Y |  | 冲击试验2缺口类型 | DB注释(中文) |
| 433 | IMPACT2_ENERGY_CD | VARCHAR2(1) | Y |  | 冲击试验2试样能量值类型 | DB注释(中文) |
| 434 | IMPACT2_AVG_RSLT | NUMBER | Y |  | 冲击试验2平均值实绩 | DB注释(中文) |
| 435 | IMPACT2_IND_RSLT1 | NUMBER | Y |  | 冲击试验2单值实绩1 | DB注释(中文) |
| 436 | IMPACT2_IND_RSLT2 | NUMBER | Y |  | 冲击试验2单值实绩2 | DB注释(中文) |
| 437 | IMPACT2_IND_RSLT3 | NUMBER | Y |  | 冲击试验2单值实绩3 | DB注释(中文) |
| 438 | IMPACT2_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验2单值判定 | DB注释(中文) |
| 439 | IMPACT2_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 冲击试验2纤维断面率平均值实绩 | DB注释(中文) |
| 440 | IMPACT2_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 冲击试验2纤维断面率单值实绩1 | DB注释(中文) |
| 441 | IMPACT2_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 冲击试验2纤维断面率单值实绩2 | DB注释(中文) |
| 442 | IMPACT2_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 冲击试验2纤维断面率单值实绩3 | DB注释(中文) |
| 443 | IMPACT2_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验2纤维断面率单值判定 | DB注释(中文) |
| 444 | IMPACT2_SMP_AVG_RSLT | NUMBER | Y |  | 冲击试验2试样侧膨胀值平均值实绩 | DB注释(中文) |
| 445 | IMPACT2_SMP_IND_RSLT1 | NUMBER | Y |  | 冲击试验2试样侧膨胀值单值实绩1 | DB注释(中文) |
| 446 | IMPACT2_SMP_IND_RSLT2 | NUMBER | Y |  | 冲击试验2试样侧膨胀值单值实绩2 | DB注释(中文) |
| 447 | IMPACT2_SMP_IND_RSLT3 | NUMBER | Y |  | 冲击试验2试样侧膨胀值单值实绩3 | DB注释(中文) |
| 448 | IMPACT2_SMP_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验2试样侧膨胀值单值判定 | DB注释(中文) |
| 449 | IMPACT3_TEMP_RSLT | NUMBER | Y |  | 冲击试验3温度实绩 | DB注释(中文) |
| 450 | IMPACT3_CREAK_CD | VARCHAR2(1) | Y |  | 冲击试验3缺口类型 | DB注释(中文) |
| 451 | IMPACT3_ENERGY_CD | VARCHAR2(1) | Y |  | 冲击试验3试样能量值类型 | DB注释(中文) |
| 452 | IMPACT3_AVG_RSLT | NUMBER | Y |  | 冲击试验3平均值实绩 | DB注释(中文) |
| 453 | IMPACT3_IND_RSLT1 | NUMBER | Y |  | 冲击试验3单值实绩1 | DB注释(中文) |
| 454 | IMPACT3_IND_RSLT2 | NUMBER | Y |  | 冲击试验3单值实绩2 | DB注释(中文) |
| 455 | IMPACT3_IND_RSLT3 | NUMBER | Y |  | 冲击试验3单值实绩3 | DB注释(中文) |
| 456 | IMPACT3_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验3单值判定 | DB注释(中文) |
| 457 | IMPACT3_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 冲击试验3纤维断面率平均值实绩 | DB注释(中文) |
| 458 | IMPACT3_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 冲击试验3纤维断面率单值实绩1 | DB注释(中文) |
| 459 | IMPACT3_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 冲击试验3纤维断面率单值实绩2 | DB注释(中文) |
| 460 | IMPACT3_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 冲击试验3纤维断面率单值实绩3 | DB注释(中文) |
| 461 | IMPACT3_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验3纤维断面率单值判定 | DB注释(中文) |
| 462 | IMPACT3_SMP_AVG_RSLT | NUMBER | Y |  | 冲击试验3试样侧膨胀值平均值实绩 | DB注释(中文) |
| 463 | IMPACT3_SMP_IND_RSLT1 | NUMBER | Y |  | 冲击试验3试样侧膨胀值单值实绩1 | DB注释(中文) |
| 464 | IMPACT3_SMP_IND_RSLT2 | NUMBER | Y |  | 冲击试验3试样侧膨胀值单值实绩2 | DB注释(中文) |
| 465 | IMPACT3_SMP_IND_RSLT3 | NUMBER | Y |  | 冲击试验3试样侧膨胀值单值实绩3 | DB注释(中文) |
| 466 | IMPACT3_SMP_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验3试样侧膨胀值单值判定 | DB注释(中文) |
| 467 | IMPACT4_TEMP_RSLT | NUMBER | Y |  | 冲击试验4温度实绩 | DB注释(中文) |
| 468 | IMPACT4_CREAK_CD | VARCHAR2(1) | Y |  | 冲击试验4缺口类型 | DB注释(中文) |
| 469 | IMPACT4_ENERGY_CD | VARCHAR2(1) | Y |  | 冲击试验4试样能量值类型 | DB注释(中文) |
| 470 | IMPACT4_AVG_RSLT | NUMBER | Y |  | 冲击试验4平均值实绩 | DB注释(中文) |
| 471 | IMPACT4_IND_RSLT1 | NUMBER | Y |  | 冲击试验4单值实绩1 | DB注释(中文) |
| 472 | IMPACT4_IND_RSLT2 | NUMBER | Y |  | 冲击试验4单值实绩2 | DB注释(中文) |
| 473 | IMPACT4_IND_RSLT3 | NUMBER | Y |  | 冲击试验4单值实绩3 | DB注释(中文) |
| 474 | IMPACT4_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验4单值判定 | DB注释(中文) |
| 475 | IMPACT4_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 冲击试验4纤维断面率平均值实绩 | DB注释(中文) |
| 476 | IMPACT4_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 冲击试验4纤维断面率单值实绩1 | DB注释(中文) |
| 477 | IMPACT4_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 冲击试验4纤维断面率单值实绩2 | DB注释(中文) |
| 478 | IMPACT4_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 冲击试验4纤维断面率单值实绩3 | DB注释(中文) |
| 479 | IMPACT4_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验4纤维断面率单值判定 | DB注释(中文) |
| 480 | IMPACT4_SMP_AVG_RSLT | NUMBER | Y |  | 冲击试验4试样侧膨胀值平均值实绩 | DB注释(中文) |
| 481 | IMPACT4_SMP_IND_RSLT1 | NUMBER | Y |  | 冲击试验4试样侧膨胀值单值实绩1 | DB注释(中文) |
| 482 | IMPACT4_SMP_IND_RSLT2 | NUMBER | Y |  | 冲击试验4试样侧膨胀值单值实绩2 | DB注释(中文) |
| 483 | IMPACT4_SMP_IND_RSLT3 | NUMBER | Y |  | 冲击试验4试样侧膨胀值单值实绩3 | DB注释(中文) |
| 484 | IMPACT4_SMP_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验4试样侧膨胀值单值判定 | DB注释(中文) |
| 485 | PW_TSL_YP_CD | VARCHAR2(1) | Y |  | 模拟焊后 拉伸测试屈服强度类型 | DB注释(中文) |
| 486 | PW_TSL_YP_RSLT | NUMBER | Y |  | 模拟焊后 拉伸测试屈服强度实绩 | DB注释(中文) |
| 487 | PW_TSL_YP_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸测试屈服强度判定 | DB注释(中文) |
| 488 | PW_TSL_TS_RSLT | NUMBER | Y |  | 模拟焊后 拉伸测试抗拉强度实绩 | DB注释(中文) |
| 489 | PW_TSL_TS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸测试抗拉强度判定 | DB注释(中文) |
| 490 | PW_TSL_YP_TS_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比YP/TS实绩 | DB注释(中文) |
| 491 | PW_TSL_YP_TS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比YP/TS判定 | DB注释(中文) |
| 492 | PW_TSL_RT05_RM_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比Rt0.5/Rm实绩 | DB注释(中文) |
| 493 | PW_TSL_RT05_RM_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比Rt0.5/Rm判定 | DB注释(中文) |
| 494 | PW_TSL_RT15_RT05_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5实绩 | DB注释(中文) |
| 495 | PW_TSL_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5判定 | DB注释(中文) |
| 496 | PW_TSL_RT20_RT10_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0实绩 | DB注释(中文) |
| 497 | PW_TSL_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0判定 | DB注释(中文) |
| 498 | PW_TSL_RT50_RT10_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0实绩 | DB注释(中文) |
| 499 | PW_TSL_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0判定 | DB注释(中文) |
| 500 | PW_TSL_CT_EX_RA_RSLT | NUMBER | Y |  | 模拟焊后 拉抻测试断后伸长率实绩 | DB注释(中文) |
| 501 | PW_TSL_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 模拟焊后 拉抻测试断后伸长率类型 | DB注释(中文) |
| 502 | PW_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉抻测试断后伸长率判定 | DB注释(中文) |
| 503 | PW_TSL_CT_RA_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验均匀伸长率实绩 | DB注释(中文) |
| 504 | PW_TSL_CT_RA_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验均匀伸长率判定 | DB注释(中文) |
| 505 | PW_TSL_RA_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验断面收缩率实绩 | DB注释(中文) |
| 506 | PW_TSL_RA_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验断面收缩率判定 | DB注释(中文) |
| 507 | PW_TSL_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 模拟焊后 消应力处理_保温温度实绩 | DB注释(中文) |
| 508 | PW_TSL_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 模拟焊后 消应力处理_保温时间实绩 | DB注释(中文) |
| 509 | PW_TSL_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 模拟焊后 消应力处理_冷却方式 | DB注释(中文) |
| 510 | PW_TSL_STRESS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 消应力处理_判定 | DB注释(中文) |
| 511 | PW_IMPACT_TEMP_RSLT | NUMBER | Y |  | 模拟焊后 冲击测试温度实绩 | DB注释(中文) |
| 512 | PW_IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 模拟焊后 冲击测试缺口类型 | DB注释(中文) |
| 513 | PW_IMPACT_ENERGY_CD | VARCHAR2(1) | Y |  | 模拟焊后 冲击试样能量值类型 | DB注释(中文) |
| 514 | PW_IMPACT_AVG_RSLT | NUMBER | Y |  | 模拟焊后 冲击测试平均值实绩 | DB注释(中文) |
| 515 | PW_IMPACT_IND_RSLT1 | NUMBER | Y |  | 模拟焊后 冲击测试单值实绩1 | DB注释(中文) |
| 516 | PW_IMPACT_IND_RSLT2 | NUMBER | Y |  | 模拟焊后 冲击测试单值实绩2 | DB注释(中文) |
| 517 | PW_IMPACT_IND_RSLT3 | NUMBER | Y |  | 模拟焊后 冲击测试单值实绩3 | DB注释(中文) |
| 518 | PW_IMPACT_IND_JDG | VARCHAR2(1) | Y |  | 模拟焊后 冲击测试单值判定 | DB注释(中文) |
| 519 | PW_IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 模拟焊后 纤维断面率平均值实绩 | DB注释(中文) |
| 520 | PW_IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 模拟焊后 纤维断面率单值实绩1 | DB注释(中文) |
| 521 | PW_IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 模拟焊后 纤维断面率单值实绩2 | DB注释(中文) |
| 522 | PW_IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 模拟焊后 纤维断面率单值实绩3 | DB注释(中文) |
| 523 | PW_IMPACT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 模拟焊后 纤维断面率单值判定 | DB注释(中文) |
| 524 | PW_IMPACT_SMP_AVG_RSLT | NUMBER | Y |  | 模拟焊后 冲击试样侧膨胀值平均值实绩 | DB注释(中文) |
| 525 | PW_IMPACT_SMP_IND_RSLT1 | NUMBER | Y |  | 模拟焊后 冲击试样侧膨胀值单值实绩1 | DB注释(中文) |
| 526 | PW_IMPACT_SMP_IND_RSLT2 | NUMBER | Y |  | 模拟焊后 冲击试样侧膨胀值单值实绩2 | DB注释(中文) |
| 527 | PW_IMPACT_SMP_IND_RSLT3 | NUMBER | Y |  | 模拟焊后 冲击试样侧膨胀值单值实绩3 | DB注释(中文) |
| 528 | PW_IMPACT_SMP_IND_JDG | VARCHAR2(1) | Y |  | 模拟焊后 冲击试样侧膨胀值单值判定 | DB注释(中文) |
| 529 | PW_MGRPHY_MTLGRP_TY | VARCHAR2(20) | Y |  | 模拟焊后 组织类型 | DB注释(中文) |
| 530 | PW_MGRPHY_MTLGRP_TY_PROVIDE | VARCHAR2(1) | Y |  | 模拟焊后 组织类型是否提供 | DB注释(中文) |
| 531 | PW_MGRPHY_BAND_STRC_MAX_RSLT | NUMBER | Y |  | 模拟焊后 带状组织等级上限实绩 | DB注释(中文) |
| 532 | PW_MGRPHY_BAND_STRC_MAX_JDG | VARCHAR2(1) | Y |  | 模拟焊后 带状组织等级上限判定 | DB注释(中文) |
| 533 | PW_MGRPHY_RSLT | NUMBER | Y |  |  | 空 |
| 534 | PW_MGRPHY_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 535 | PW_MGRPHY_FGS_RSLT | NUMBER | Y |  | 模拟焊后 铁素体晶粒度实绩 | DB注释(中文) |
| 536 | PW_MGRPHY_FGS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 铁素体晶粒度判定 | DB注释(中文) |
| 537 | PW_MGRPHY_AGS_RSLT | NUMBER | Y |  | 模拟焊后 奥氏体晶粒度实绩 | DB注释(中文) |
| 538 | PW_MGRPHY_AGS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 奥氏体晶粒度判定 | DB注释(中文) |
| 539 | PW_MGRPHY_GRNSZ_OCCP_RSLT | NUMBER | Y |  | 模拟焊后 金相测试基相的体积分数实绩 | DB注释(中文) |
| 540 | PW_MGRPHY_GRNSZ_OCCP_JDG | VARCHAR2(1) | Y |  | 模拟焊后 金相测试基相的体积分数判定 | DB注释(中文) |
| 541 | PW_BEND_DIA | NUMBER | Y |  | 模拟焊后 弯曲测试弯心直径 | DB注释(中文) |
| 542 | PW_BEND_ANGLE | NUMBER | Y |  | 模拟焊后 弯曲测试弯曲角度 | DB注释(中文) |
| 543 | PW_BEND_RSLT | VARCHAR2(1) | Y |  | 模拟焊后 弯曲测试实绩 | DB注释(中文) |
| 544 | PW_BEND_JDG | VARCHAR2(1) | Y |  | 模拟焊后 弯曲测试判定 | DB注释(中文) |
| 545 | PW_Z_TSL_CUT_IND_RSLT1 | NUMBER | Y |  |  | 空 |
| 546 | PW_Z_TSL_CUT_IND_RSLT2 | NUMBER | Y |  |  | 空 |
| 547 | PW_Z_TSL_CUT_IND_RSLT3 | NUMBER | Y |  |  | 空 |
| 548 | PW_Z_TSL_CUT_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 549 | PW_Z_TSL_CUT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 550 | PW_Z_TSL_CUT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 551 | PW_Z_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 552 | PW_Z_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 553 | PW_Z_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 554 | PW_Z_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 555 | PW_Z_TSL_CT_EX_RA_RSLT | NUMBER | Y |  |  | 空 |
| 556 | PW_Z_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 557 | PW_HIGH_TEMP_TSL_STAND_CD | VARCHAR2(20) | Y |  |  | 空 |
| 558 | PW_HIGH_TEMP_TSL_TEMP_RSLT | NUMBER | Y |  |  | 空 |
| 559 | PW_HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 560 | PW_HIGH_TEMP_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 561 | PW_HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  |  | 空 |
| 562 | PW_HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 563 | PW_HIGH_TEMP_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 564 | PW_HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  |  | 空 |
| 565 | PW_HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  |  | 空 |
| 566 | PW_HIGH_TEMP_TSL_EL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 567 | PW_HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  |  | 空 |
| 568 | PW_HIGH_TEMP_TSL_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 569 | PW_SSCC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 570 | PW_SSCC_STRESS_TY | VARCHAR2(1) | Y |  |  | 空 |
| 571 | PW_SSCC_STRESS_TST_VAL_RSLT | NUMBER | Y |  |  | 空 |
| 572 | PW_SSCC_STRESS_TST_VAL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 573 | PW_SSCC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 574 | PW_HIC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 575 | PW_HIC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 576 | PW_HIC_CLR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 577 | PW_HIC_CLR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 578 | PW_HIC_CLR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 579 | PW_HIC_CLR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 580 | PW_HIC_CLR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 581 | PW_HIC_CLR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 582 | PW_HIC_CLR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 583 | PW_HIC_CLR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 584 | PW_HIC_CLR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 585 | PW_HIC_CLR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 586 | PW_HIC_CLR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 587 | PW_HIC_CLR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 588 | PW_HIC_CLR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 589 | PW_HIC_CLR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 590 | PW_HIC_CLR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 591 | PW_HIC_CLR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 592 | PW_HIC_CSR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 593 | PW_HIC_CSR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 594 | PW_HIC_CSR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 595 | PW_HIC_CSR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 596 | PW_HIC_CSR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 597 | PW_HIC_CSR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 598 | PW_HIC_CSR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 599 | PW_HIC_CSR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 600 | PW_HIC_CSR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 601 | PW_HIC_CSR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 602 | PW_HIC_CSR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 603 | PW_HIC_CSR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 604 | PW_HIC_CSR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 605 | PW_HIC_CSR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 606 | PW_HIC_CSR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 607 | PW_HIC_CSR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 608 | PW_HIC_CTR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 609 | PW_HIC_CTR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 610 | PW_HIC_CTR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 611 | PW_HIC_CTR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 612 | PW_HIC_CTR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 613 | PW_HIC_CTR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 614 | PW_HIC_CTR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 615 | PW_HIC_CTR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 616 | PW_HIC_CTR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 617 | PW_HIC_CTR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 618 | PW_HIC_CTR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 619 | PW_HIC_CTR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 620 | PW_HIC_CTR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 621 | PW_HIC_CTR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 622 | PW_HIC_CTR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 623 | PW_HIC_CTR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 624 | PW_HARD_KIND | VARCHAR2(1) | Y |  |  | 空 |
| 625 | PW_HARD_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 626 | PW_HARD_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 627 | PW_HARD_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 628 | MXPW_TSL_YP_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸测试屈服强度类型 | DB注释(中文) |
| 629 | MXPW_TSL_YP_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸测试屈服强度实绩 | DB注释(中文) |
| 630 | MXPW_TSL_YP_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸测试屈服强度判定 | DB注释(中文) |
| 631 | MXPW_TSL_TS_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸测试抗拉强度实绩 | DB注释(中文) |
| 632 | MXPW_TSL_TS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸测试抗拉强度判定 | DB注释(中文) |
| 633 | MXPW_TSL_YP_TS_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比YP/TS实绩 | DB注释(中文) |
| 634 | MXPW_TSL_YP_TS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比YP/TS判定 | DB注释(中文) |
| 635 | MXPW_TSL_RT05_RM_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比Rt0.5/Rm实绩 | DB注释(中文) |
| 636 | MXPW_TSL_RT05_RM_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比Rt0.5/Rm判定 | DB注释(中文) |
| 637 | MXPW_TSL_RT15_RT05_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5实绩 | DB注释(中文) |
| 638 | MXPW_TSL_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5判定 | DB注释(中文) |
| 639 | MXPW_TSL_RT20_RT10_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0实绩 | DB注释(中文) |
| 640 | MXPW_TSL_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0判定 | DB注释(中文) |
| 641 | MXPW_TSL_RT50_RT10_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0实绩 | DB注释(中文) |
| 642 | MXPW_TSL_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0判定 | DB注释(中文) |
| 643 | MXPW_TSL_CT_EX_RA_RSLT | NUMBER | Y |  | 最大模拟焊后 拉抻测试断后伸长率实绩 | DB注释(中文) |
| 644 | MXPW_TSL_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 拉抻测试断后伸长率类型 | DB注释(中文) |
| 645 | MXPW_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉抻测试断后伸长率判定 | DB注释(中文) |
| 646 | MXPW_TSL_CT_RA_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验均匀伸长率实绩 | DB注释(中文) |
| 647 | MXPW_TSL_CT_RA_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验均匀伸长率判定 | DB注释(中文) |
| 648 | MXPW_TSL_RA_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验断面收缩率实绩 | DB注释(中文) |
| 649 | MXPW_TSL_RA_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验断面收缩率判定 | DB注释(中文) |
| 650 | MXPW_TSL_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 最大模拟焊后 消应力处理_保温温度实绩 | DB注释(中文) |
| 651 | MXPW_TSL_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 最大模拟焊后 消应力处理_保温时间实绩 | DB注释(中文) |
| 652 | MXPW_TSL_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 消应力处理_冷却方式 | DB注释(中文) |
| 653 | MXPW_TSL_STRESS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 消应力处理_判定 | DB注释(中文) |
| 654 | MXPW_IMPACT_TEMP_RSLT | NUMBER | Y |  | 最大模拟焊后 冲击测试温度实绩 | DB注释(中文) |
| 655 | MXPW_IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 冲击测试缺口类型 | DB注释(中文) |
| 656 | MXPW_IMPACT_ENERGY_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 冲击试样能量值类型 | DB注释(中文) |
| 657 | MXPW_IMPACT_AVG_RSLT | NUMBER | Y |  | 最大模拟焊后 冲击测试平均值实绩 | DB注释(中文) |
| 658 | MXPW_IMPACT_IND_RSLT1 | NUMBER | Y |  | 最大模拟焊后 冲击测试单值实绩1 | DB注释(中文) |
| 659 | MXPW_IMPACT_IND_RSLT2 | NUMBER | Y |  | 最大模拟焊后 冲击测试单值实绩2 | DB注释(中文) |
| 660 | MXPW_IMPACT_IND_RSLT3 | NUMBER | Y |  | 最大模拟焊后 冲击测试单值实绩3 | DB注释(中文) |
| 661 | MXPW_IMPACT_IND_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 冲击测试单值判定 | DB注释(中文) |
| 662 | MXPW_IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 最大模拟焊后 纤维断面率平均值实绩 | DB注释(中文) |
| 663 | MXPW_IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 最大模拟焊后 纤维断面率单值实绩1 | DB注释(中文) |
| 664 | MXPW_IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 最大模拟焊后 纤维断面率单值实绩2 | DB注释(中文) |
| 665 | MXPW_IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 最大模拟焊后 纤维断面率单值实绩3 | DB注释(中文) |
| 666 | MXPW_IMPACT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 纤维断面率单值判定 | DB注释(中文) |
| 667 | MXPW_IMPACT_SMP_AVG_RSLT | NUMBER | Y |  | 最大模拟焊后 冲击试样侧膨胀值平均值实绩 | DB注释(中文) |
| 668 | MXPW_IMPACT_SMP_IND_RSLT1 | NUMBER | Y |  | 最大模拟焊后 冲击试样侧膨胀值单值实绩1 | DB注释(中文) |
| 669 | MXPW_IMPACT_SMP_IND_RSLT2 | NUMBER | Y |  | 最大模拟焊后 冲击试样侧膨胀值单值实绩2 | DB注释(中文) |
| 670 | MXPW_IMPACT_SMP_IND_RSLT3 | NUMBER | Y |  | 最大模拟焊后 冲击试样侧膨胀值单值实绩3 | DB注释(中文) |
| 671 | MXPW_IMPACT_SMP_IND_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 冲击试样侧膨胀值单值判定 | DB注释(中文) |
| 672 | MXPW_MGRPHY_MTLGRP_TY | VARCHAR2(20) | Y |  | 最大模拟焊后 组织类型 | DB注释(中文) |
| 673 | MXPW_MGRPHY_MTLGRP_TY_PROVIDE | VARCHAR2(1) | Y |  | 最大模拟焊后 组织类型是否提供 | DB注释(中文) |
| 674 | MXPW_MGRPHY_BAND_STRC_MAX_RSLT | NUMBER | Y |  | 最大模拟焊后 带状组织等级上限实绩 | DB注释(中文) |
| 675 | MXPW_MGRPHY_BAND_STRC_MAX_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 带状组织等级上限判定 | DB注释(中文) |
| 676 | MXPW_MGRPHY_RSLT | NUMBER | Y |  |  | 空 |
| 677 | MXPW_MGRPHY_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 678 | MXPW_MGRPHY_FGS_RSLT | NUMBER | Y |  | 最大模拟焊后 铁素体晶粒度实绩 | DB注释(中文) |
| 679 | MXPW_MGRPHY_FGS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 铁素体晶粒度判定 | DB注释(中文) |
| 680 | MXPW_MGRPHY_AGS_RSLT | NUMBER | Y |  | 最大模拟焊后 奥氏体晶粒度实绩 | DB注释(中文) |
| 681 | MXPW_MGRPHY_AGS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 奥氏体晶粒度判定 | DB注释(中文) |
| 682 | MXPW_MGRPHY_GRNSZ_OCCP_RSLT | NUMBER | Y |  | 最大模拟焊后 金相测试基相的体积分数实绩 | DB注释(中文) |
| 683 | MXPW_MGRPHY_GRNSZ_OCCP_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 金相测试基相的体积分数判定 | DB注释(中文) |
| 684 | MXPW_BEND_DIA | NUMBER | Y |  | 最大模拟焊后 弯曲测试弯心直径 | DB注释(中文) |
| 685 | MXPW_BEND_ANGLE | NUMBER | Y |  | 最大模拟焊后 弯曲测试弯曲角度 | DB注释(中文) |
| 686 | MXPW_BEND_RSLT | VARCHAR2(1) | Y |  | 最大模拟焊后 弯曲测试实绩 | DB注释(中文) |
| 687 | MXPW_BEND_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 弯曲测试判定 | DB注释(中文) |
| 688 | MXPW_Z_TSL_CUT_IND_RSLT1 | NUMBER | Y |  |  | 空 |
| 689 | MXPW_Z_TSL_CUT_IND_RSLT2 | NUMBER | Y |  |  | 空 |
| 690 | MXPW_Z_TSL_CUT_IND_RSLT3 | NUMBER | Y |  |  | 空 |
| 691 | MXPW_Z_TSL_CUT_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 692 | MXPW_Z_TSL_CUT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 693 | MXPW_Z_TSL_CUT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 694 | MXPW_Z_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 695 | MXPW_Z_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 696 | MXPW_Z_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 697 | MXPW_Z_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 698 | MXPW_Z_TSL_CT_EX_RA_RSLT | NUMBER | Y |  |  | 空 |
| 699 | MXPW_Z_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 700 | MXPW_HIGH_TEMP_TSL_STAND_CD | VARCHAR2(20) | Y |  |  | 空 |
| 701 | MXPW_HIGH_TEMP_TSL_TEMP_RSLT | NUMBER | Y |  |  | 空 |
| 702 | MXPW_HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 703 | MXPW_HIGH_TEMP_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 704 | MXPW_HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  |  | 空 |
| 705 | MXPW_HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 706 | MXPW_HIGH_TEMP_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 707 | MXPW_HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  |  | 空 |
| 708 | MXPW_HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  |  | 空 |
| 709 | MXPW_HIGH_TEMP_TSL_EL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 710 | MXPW_HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  |  | 空 |
| 711 | MXPW_HIGH_TEMP_TSL_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 712 | MXPW_SSCC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 713 | MXPW_SSCC_STRESS_TY | VARCHAR2(1) | Y |  |  | 空 |
| 714 | MXPW_SSCC_STRESS_TST_VAL_RSLT | NUMBER | Y |  |  | 空 |
| 715 | MXPW_SSCC_STRESS_TST_VAL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 716 | MXPW_SSCC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 717 | MXPW_HIC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 718 | MXPW_HIC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 719 | MXPW_HIC_CLR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 720 | MXPW_HIC_CLR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 721 | MXPW_HIC_CLR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 722 | MXPW_HIC_CLR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 723 | MXPW_HIC_CLR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 724 | MXPW_HIC_CLR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 725 | MXPW_HIC_CLR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 726 | MXPW_HIC_CLR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 727 | MXPW_HIC_CLR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 728 | MXPW_HIC_CLR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 729 | MXPW_HIC_CLR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 730 | MXPW_HIC_CLR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 731 | MXPW_HIC_CLR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 732 | MXPW_HIC_CLR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 733 | MXPW_HIC_CLR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 734 | MXPW_HIC_CLR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 735 | MXPW_HIC_CSR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 736 | MXPW_HIC_CSR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 737 | MXPW_HIC_CSR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 738 | MXPW_HIC_CSR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 739 | MXPW_HIC_CSR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 740 | MXPW_HIC_CSR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 741 | MXPW_HIC_CSR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 742 | MXPW_HIC_CSR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 743 | MXPW_HIC_CSR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 744 | MXPW_HIC_CSR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 745 | MXPW_HIC_CSR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 746 | MXPW_HIC_CSR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 747 | MXPW_HIC_CSR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 748 | MXPW_HIC_CSR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 749 | MXPW_HIC_CSR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 750 | MXPW_HIC_CSR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 751 | MXPW_HIC_CTR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 752 | MXPW_HIC_CTR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 753 | MXPW_HIC_CTR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 754 | MXPW_HIC_CTR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 755 | MXPW_HIC_CTR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 756 | MXPW_HIC_CTR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 757 | MXPW_HIC_CTR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 758 | MXPW_HIC_CTR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 759 | MXPW_HIC_CTR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 760 | MXPW_HIC_CTR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 761 | MXPW_HIC_CTR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 762 | MXPW_HIC_CTR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 763 | MXPW_HIC_CTR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 764 | MXPW_HIC_CTR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 765 | MXPW_HIC_CTR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 766 | MXPW_HIC_CTR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 767 | MXPW_HARD_KIND | VARCHAR2(1) | Y |  |  | 空 |
| 768 | MXPW_HARD_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 769 | MXPW_HARD_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 770 | MXPW_HARD_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 771 | MNPW_TSL_YP_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸测试屈服强度类型 | DB注释(中文) |
| 772 | MNPW_TSL_YP_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸测试屈服强度实绩 | DB注释(中文) |
| 773 | MNPW_TSL_YP_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸测试屈服强度判定 | DB注释(中文) |
| 774 | MNPW_TSL_TS_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸测试抗拉强度实绩 | DB注释(中文) |
| 775 | MNPW_TSL_TS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸测试抗拉强度判定 | DB注释(中文) |
| 776 | MNPW_TSL_YP_TS_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比YP/TS实绩 | DB注释(中文) |
| 777 | MNPW_TSL_YP_TS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比YP/TS判定 | DB注释(中文) |
| 778 | MNPW_TSL_RT05_RM_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比Rt0.5/Rm实绩 | DB注释(中文) |
| 779 | MNPW_TSL_RT05_RM_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比Rt0.5/Rm判定 | DB注释(中文) |
| 780 | MNPW_TSL_RT15_RT05_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5实绩 | DB注释(中文) |
| 781 | MNPW_TSL_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5判定 | DB注释(中文) |
| 782 | MNPW_TSL_RT20_RT10_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0实绩 | DB注释(中文) |
| 783 | MNPW_TSL_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0判定 | DB注释(中文) |
| 784 | MNPW_TSL_RT50_RT10_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0实绩 | DB注释(中文) |
| 785 | MNPW_TSL_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0判定 | DB注释(中文) |
| 786 | MNPW_TSL_CT_EX_RA_RSLT | NUMBER | Y |  | 最小模拟焊后 拉抻测试断后伸长率实绩 | DB注释(中文) |
| 787 | MNPW_TSL_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 拉抻测试断后伸长率类型 | DB注释(中文) |
| 788 | MNPW_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉抻测试断后伸长率判定 | DB注释(中文) |
| 789 | MNPW_TSL_CT_RA_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验均匀伸长率实绩 | DB注释(中文) |
| 790 | MNPW_TSL_CT_RA_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验均匀伸长率判定 | DB注释(中文) |
| 791 | MNPW_TSL_RA_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验断面收缩率实绩 | DB注释(中文) |
| 792 | MNPW_TSL_RA_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验断面收缩率判定 | DB注释(中文) |
| 793 | MNPW_TSL_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 最小模拟焊后 消应力处理_保温温度实绩 | DB注释(中文) |
| 794 | MNPW_TSL_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 最小模拟焊后 消应力处理_保温时间实绩 | DB注释(中文) |
| 795 | MNPW_TSL_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 消应力处理_冷却方式 | DB注释(中文) |
| 796 | MNPW_TSL_STRESS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 消应力处理_判定 | DB注释(中文) |
| 797 | MNPW_IMPACT_TEMP_RSLT | NUMBER | Y |  | 最小模拟焊后 冲击测试温度实绩 | DB注释(中文) |
| 798 | MNPW_IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 冲击测试缺口类型 | DB注释(中文) |
| 799 | MNPW_IMPACT_ENERGY_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 冲击试样能量值类型 | DB注释(中文) |
| 800 | MNPW_IMPACT_AVG_RSLT | NUMBER | Y |  | 最小模拟焊后 冲击测试平均值实绩 | DB注释(中文) |
| 801 | MNPW_IMPACT_IND_RSLT1 | NUMBER | Y |  | 最小模拟焊后 冲击测试单值实绩1 | DB注释(中文) |
| 802 | MNPW_IMPACT_IND_RSLT2 | NUMBER | Y |  | 最小模拟焊后 冲击测试单值实绩2 | DB注释(中文) |
| 803 | MNPW_IMPACT_IND_RSLT3 | NUMBER | Y |  | 最小模拟焊后 冲击测试单值实绩3 | DB注释(中文) |
| 804 | MNPW_IMPACT_IND_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 冲击测试单值判定 | DB注释(中文) |
| 805 | MNPW_IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 最小模拟焊后 纤维断面率平均值实绩 | DB注释(中文) |
| 806 | MNPW_IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 最小模拟焊后 纤维断面率单值实绩1 | DB注释(中文) |
| 807 | MNPW_IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 最小模拟焊后 纤维断面率单值实绩2 | DB注释(中文) |
| 808 | MNPW_IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 最小模拟焊后 纤维断面率单值实绩3 | DB注释(中文) |
| 809 | MNPW_IMPACT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 纤维断面率单值判定 | DB注释(中文) |
| 810 | MNPW_IMPACT_SMP_AVG_RSLT | NUMBER | Y |  | 最小模拟焊后 冲击试样侧膨胀值平均值实绩 | DB注释(中文) |
| 811 | MNPW_IMPACT_SMP_IND_RSLT1 | NUMBER | Y |  | 最小模拟焊后 冲击试样侧膨胀值单值实绩1 | DB注释(中文) |
| 812 | MNPW_IMPACT_SMP_IND_RSLT2 | NUMBER | Y |  | 最小模拟焊后 冲击试样侧膨胀值单值实绩2 | DB注释(中文) |
| 813 | MNPW_IMPACT_SMP_IND_RSLT3 | NUMBER | Y |  | 最小模拟焊后 冲击试样侧膨胀值单值实绩3 | DB注释(中文) |
| 814 | MNPW_IMPACT_SMP_IND_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 冲击试样侧膨胀值单值判定 | DB注释(中文) |
| 815 | MNPW_MGRPHY_MTLGRP_TY | VARCHAR2(20) | Y |  | 最小模拟焊后 组织类型 | DB注释(中文) |
| 816 | MNPW_MGRPHY_MTLGRP_TY_PROVIDE | VARCHAR2(1) | Y |  | 最小模拟焊后 组织类型是否提供 | DB注释(中文) |
| 817 | MNPW_MGRPHY_BAND_STRC_MAX_RSLT | NUMBER | Y |  | 最小模拟焊后 带状组织等级上限实绩 | DB注释(中文) |
| 818 | MNPW_MGRPHY_BAND_STRC_MAX_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 带状组织等级上限判定 | DB注释(中文) |
| 819 | MNPW_MGRPHY_RSLT | NUMBER | Y |  |  | 空 |
| 820 | MNPW_MGRPHY_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 821 | MNPW_MGRPHY_FGS_RSLT | NUMBER | Y |  | 最小模拟焊后 铁素体晶粒度实绩 | DB注释(中文) |
| 822 | MNPW_MGRPHY_FGS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 铁素体晶粒度判定 | DB注释(中文) |
| 823 | MNPW_MGRPHY_AGS_RSLT | NUMBER | Y |  | 最小模拟焊后 奥氏体晶粒度实绩 | DB注释(中文) |
| 824 | MNPW_MGRPHY_AGS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 奥氏体晶粒度判定 | DB注释(中文) |
| 825 | MNPW_MGRPHY_GRNSZ_OCCP_RSLT | NUMBER | Y |  | 最小模拟焊后 金相测试基相的体积分数实绩 | DB注释(中文) |
| 826 | MNPW_MGRPHY_GRNSZ_OCCP_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 金相测试基相的体积分数判定 | DB注释(中文) |
| 827 | MNPW_BEND_DIA | NUMBER | Y |  | 最小模拟焊后 弯曲测试弯心直径 | DB注释(中文) |
| 828 | MNPW_BEND_ANGLE | NUMBER | Y |  | 最小模拟焊后 弯曲测试弯曲角度 | DB注释(中文) |
| 829 | MNPW_BEND_RSLT | VARCHAR2(1) | Y |  | 最小模拟焊后 弯曲测试实绩 | DB注释(中文) |
| 830 | MNPW_BEND_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 弯曲测试判定 | DB注释(中文) |
| 831 | MNPW_Z_TSL_CUT_IND_RSLT1 | NUMBER | Y |  |  | 空 |
| 832 | MNPW_Z_TSL_CUT_IND_RSLT2 | NUMBER | Y |  |  | 空 |
| 833 | MNPW_Z_TSL_CUT_IND_RSLT3 | NUMBER | Y |  |  | 空 |
| 834 | MNPW_Z_TSL_CUT_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 835 | MNPW_Z_TSL_CUT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 836 | MNPW_Z_TSL_CUT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 837 | MNPW_Z_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 838 | MNPW_Z_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 839 | MNPW_Z_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 840 | MNPW_Z_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 841 | MNPW_Z_TSL_CT_EX_RA_RSLT | NUMBER | Y |  |  | 空 |
| 842 | MNPW_Z_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 843 | MNPW_HIGH_TEMP_TSL_STAND_CD | VARCHAR2(20) | Y |  |  | 空 |
| 844 | MNPW_HIGH_TEMP_TSL_TEMP_RSLT | NUMBER | Y |  |  | 空 |
| 845 | MNPW_HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 846 | MNPW_HIGH_TEMP_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 847 | MNPW_HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  |  | 空 |
| 848 | MNPW_HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 849 | MNPW_HIGH_TEMP_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 850 | MNPW_HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  |  | 空 |
| 851 | MNPW_HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  |  | 空 |
| 852 | MNPW_HIGH_TEMP_TSL_EL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 853 | MNPW_HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  |  | 空 |
| 854 | MNPW_HIGH_TEMP_TSL_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 855 | MNPW_SSCC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 856 | MNPW_SSCC_STRESS_TY | VARCHAR2(1) | Y |  |  | 空 |
| 857 | MNPW_SSCC_STRESS_TST_VAL_RSLT | NUMBER | Y |  |  | 空 |
| 858 | MNPW_SSCC_STRESS_TST_VAL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 859 | MNPW_SSCC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 860 | MNPW_HIC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 861 | MNPW_HIC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 862 | MNPW_HIC_CLR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 863 | MNPW_HIC_CLR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 864 | MNPW_HIC_CLR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 865 | MNPW_HIC_CLR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 866 | MNPW_HIC_CLR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 867 | MNPW_HIC_CLR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 868 | MNPW_HIC_CLR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 869 | MNPW_HIC_CLR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 870 | MNPW_HIC_CLR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 871 | MNPW_HIC_CLR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 872 | MNPW_HIC_CLR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 873 | MNPW_HIC_CLR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 874 | MNPW_HIC_CLR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 875 | MNPW_HIC_CLR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 876 | MNPW_HIC_CLR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 877 | MNPW_HIC_CLR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 878 | MNPW_HIC_CSR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 879 | MNPW_HIC_CSR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 880 | MNPW_HIC_CSR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 881 | MNPW_HIC_CSR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 882 | MNPW_HIC_CSR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 883 | MNPW_HIC_CSR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 884 | MNPW_HIC_CSR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 885 | MNPW_HIC_CSR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 886 | MNPW_HIC_CSR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 887 | MNPW_HIC_CSR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 888 | MNPW_HIC_CSR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 889 | MNPW_HIC_CSR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 890 | MNPW_HIC_CSR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 891 | MNPW_HIC_CSR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 892 | MNPW_HIC_CSR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 893 | MNPW_HIC_CSR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 894 | MNPW_HIC_CTR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 895 | MNPW_HIC_CTR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 896 | MNPW_HIC_CTR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 897 | MNPW_HIC_CTR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 898 | MNPW_HIC_CTR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 899 | MNPW_HIC_CTR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 900 | MNPW_HIC_CTR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 901 | MNPW_HIC_CTR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 902 | MNPW_HIC_CTR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 903 | MNPW_HIC_CTR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 904 | MNPW_HIC_CTR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 905 | MNPW_HIC_CTR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 906 | MNPW_HIC_CTR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 907 | MNPW_HIC_CTR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 908 | MNPW_HIC_CTR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 909 | MNPW_HIC_CTR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 910 | MNPW_HARD_KIND | VARCHAR2(1) | Y |  |  | 空 |
| 911 | MNPW_HARD_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 912 | MNPW_HARD_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 913 | MNPW_HARD_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 914 | PROD_CHEM_SMP_CND | VARCHAR2(2) | Y |  | 产品成分分析取样条件 | DB注释(中文) |
| 915 | PROD_CHEM_ANAL_TY | VARCHAR2(1) | Y |  | 产品成分分析区分(P-PASS;F-FAIL) | DB注释(中文) |
| 916 | C_RSLT | VARCHAR2(20) | Y |  | 产品成分C实绩 | DB注释(中文) |
| 917 | SI_RSLT | VARCHAR2(20) | Y |  | 产品成分Si实绩 | DB注释(中文) |
| 918 | MN_RSLT | VARCHAR2(20) | Y |  | 产品成分Mn实绩 | DB注释(中文) |
| 919 | P_RSLT | VARCHAR2(20) | Y |  | 产品成分P实绩 | DB注释(中文) |
| 920 | S_RSLT | VARCHAR2(20) | Y |  | 产品成分S实绩 | DB注释(中文) |
| 921 | SAL_RSLT | VARCHAR2(20) | Y |  | 产品成分Sol_Al实绩 | DB注释(中文) |
| 922 | TAL_RSLT | VARCHAR2(20) | Y |  | 产品成分Tot_Al实绩 | DB注释(中文) |
| 923 | AS_RSLT | VARCHAR2(20) | Y |  | 产品成分As实绩 | DB注释(中文) |
| 924 | BI_RSLT | VARCHAR2(20) | Y |  | 产品成分Bi实绩 | DB注释(中文) |
| 925 | B_RSLT | VARCHAR2(20) | Y |  | 产品成分B实绩 | DB注释(中文) |
| 926 | CA_RSLT | VARCHAR2(20) | Y |  | 产品成分Ca实绩 | DB注释(中文) |
| 927 | CO_RSLT | VARCHAR2(20) | Y |  | 产品成分Co实绩 | DB注释(中文) |
| 928 | CR_RSLT | VARCHAR2(20) | Y |  | 产品成分Cr实绩 | DB注释(中文) |
| 929 | CU_RSLT | VARCHAR2(20) | Y |  | 产品成分Cu实绩 | DB注释(中文) |
| 930 | H_RSLT | VARCHAR2(20) | Y |  | 产品成分H实绩 | DB注释(中文) |
| 931 | MG_RSLT | VARCHAR2(20) | Y |  | 产品成分Mg实绩 | DB注释(中文) |
| 932 | MO_RSLT | VARCHAR2(20) | Y |  | 产品成分Mo实绩 | DB注释(中文) |
| 933 | NB_RSLT | VARCHAR2(20) | Y |  | 产品成分Nb实绩 | DB注释(中文) |
| 934 | NI_RSLT | VARCHAR2(20) | Y |  | 产品成分Ni实绩 | DB注释(中文) |
| 935 | N_RSLT | VARCHAR2(20) | Y |  | 产品成分N实绩 | DB注释(中文) |
| 936 | O_RSLT | VARCHAR2(20) | Y |  | 产品成分O实绩 | DB注释(中文) |
| 937 | PB_RSLT | VARCHAR2(20) | Y |  | 产品成分Pb实绩 | DB注释(中文) |
| 938 | SB_RSLT | VARCHAR2(20) | Y |  | 产品成分Sb实绩 | DB注释(中文) |
| 939 | SN_RSLT | VARCHAR2(20) | Y |  | 产品成分Sn实绩 | DB注释(中文) |
| 940 | TE_RSLT | VARCHAR2(20) | Y |  | 产品成分Te实绩 | DB注释(中文) |
| 941 | TI_RSLT | VARCHAR2(20) | Y |  | 产品成分Ti实绩 | DB注释(中文) |
| 942 | V_RSLT | VARCHAR2(20) | Y |  | 产品成分V实绩 | DB注释(中文) |
| 943 | W_RSLT | VARCHAR2(20) | Y |  | 产品成分W实绩 | DB注释(中文) |
| 944 | ZN_RSLT | VARCHAR2(20) | Y |  | 产品成分Zn实绩 | DB注释(中文) |
| 945 | ZR_RSLT | VARCHAR2(20) | Y |  | 产品成分Zr实绩 | DB注释(中文) |
| 946 | CEQ_RSLT | VARCHAR2(20) | Y |  | 产品成分CEQ计算值 | DB注释(中文) |
| 947 | PCM_RSLT | VARCHAR2(20) | Y |  | 产品成分PCM计算值 | DB注释(中文) |
| 948 | PSR_RSLT | VARCHAR2(20) | Y |  | 产品成分PSR计算值 | DB注释(中文) |
| 949 | CFI_RSLT | VARCHAR2(20) | Y |  | 产品成分CFI计算值 | DB注释(中文) |
| 950 | CFJ_RSLT | VARCHAR2(20) | Y |  | 产品成分CFJ计算值 | DB注释(中文) |
| 951 | CFX_RSLT | VARCHAR2(20) | Y |  | 产品成分CFX计算值 | DB注释(中文) |
| 952 | WLYS10_RSLT | VARCHAR2(20) | Y |  | 产品成分WLYS10实绩 | DB注释(中文) |
| 953 | HARD_RSLT1 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 954 | HARD_RSLT2 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 955 | HARD_RSLT3 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 956 | HARD_RSLT4 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 957 | HARD_RSLT5 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 958 | HARD_RSLT6 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 959 | HARD_RSLT7 | NUMBER | Y |  | 硬度测试实绩7 | DB注释(中文) |
| 960 | HARD_RSLT8 | NUMBER | Y |  | 硬度测试实绩8 | DB注释(中文) |
| 961 | HARD_RSLT9 | NUMBER | Y |  | 硬度测试实绩9 | DB注释(中文) |
| 962 | MNPW_HARD_RSLT1 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 963 | MNPW_HARD_RSLT2 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 964 | MNPW_HARD_RSLT3 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 965 | MNPW_HARD_RSLT4 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 966 | MNPW_HARD_RSLT5 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 967 | MNPW_HARD_RSLT6 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 968 | MNPW_HARD_RSLT7 | NUMBER | Y |  | 硬度测试实绩7 | DB注释(中文) |
| 969 | MNPW_HARD_RSLT8 | NUMBER | Y |  | 硬度测试实绩8 | DB注释(中文) |
| 970 | MNPW_HARD_RSLT9 | NUMBER | Y |  | 硬度测试实绩9 | DB注释(中文) |
| 971 | MXPW_HARD_RSLT1 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 972 | MXPW_HARD_RSLT2 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 973 | MXPW_HARD_RSLT3 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 974 | MXPW_HARD_RSLT4 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 975 | MXPW_HARD_RSLT5 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 976 | MXPW_HARD_RSLT6 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 977 | MXPW_HARD_RSLT7 | NUMBER | Y |  | 硬度测试实绩7 | DB注释(中文) |
| 978 | MXPW_HARD_RSLT8 | NUMBER | Y |  | 硬度测试实绩8 | DB注释(中文) |
| 979 | MXPW_HARD_RSLT9 | NUMBER | Y |  | 硬度测试实绩9 | DB注释(中文) |
| 980 | PW_HARD_RSLT1 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 981 | PW_HARD_RSLT2 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 982 | PW_HARD_RSLT3 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 983 | PW_HARD_RSLT4 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 984 | PW_HARD_RSLT5 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 985 | PW_HARD_RSLT6 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 986 | PW_HARD_RSLT7 | NUMBER | Y |  | 硬度测试实绩7 | DB注释(中文) |
| 987 | PW_HARD_RSLT8 | NUMBER | Y |  | 硬度测试实绩8 | DB注释(中文) |
| 988 | PW_HARD_RSLT9 | NUMBER | Y |  | 硬度测试实绩9 | DB注释(中文) |
| 989 | RE_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 990 | CEQ1_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 991 | CEQEXP_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 992 | CSOL_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 993 | CET_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 994 | CEQAWS_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 995 | YSB1_RSLT | VARCHAR2(20) | Y |  | CEQJIS替换为YSB1 | DB注释(中文) |
| 996 | TOT_AL_RSLT | VARCHAR2(20) | Y |  | 实绩TOT | DB注释(中文) |
| 997 | SOL_AL_RSLT | VARCHAR2(20) | Y |  | 实绩SOL | DB注释(中文) |
| 998 | WLYS1_RSLT | VARCHAR2(20) | Y |  | 产品成分WLYS1实绩 | DB注释(中文) |
| 999 | WLYS3_RSLT | VARCHAR2(20) | Y |  | 产品成分WLYS3实绩 | DB注释(中文) |
| 1000 | WLYS5_RSLT | VARCHAR2(20) | Y |  | 产品成分WLYS5实绩 | DB注释(中文) |

### SQM_STDA_MECH_SAMPLE

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=29｜被读 27 过程 / 被写 1 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：27　**主键**：QLT_STD_SEQ　**语义覆盖**：17/17

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 修改人 | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | 修改时间 | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | QLT_STD_SEQ | NUMBER | N | ✓ | 质量标准序列号 | DB注释(中文) |
| 9 | PROD_GRP | VARCHAR2(2) | N |  | 品种代码 | DB注释(中文) |
| 10 | SPEC_CD | VARCHAR2(50) | N |  | 国家标准牌号 | DB注释(中文) |
| 11 | MECH_SMP_CND | VARCHAR2(2) | Y |  | 物性测试取样条件 | DB注释(中文) |
| 12 | MECH_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 物性测试长度方向取样位置 | DB注释(中文) |
| 13 | MECH_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 物性测试宽度方向取样位置 | DB注释(中文) |
| 14 | MECH_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 物性测试取样号数 | DB注释(中文) |
| 15 | MECH_SMP_SPCMN_CNT | NUMBER | Y |  | 物性测试取样数量 | DB注释(中文) |
| 16 | USE_YN | VARCHAR2(1) | Y |  | 是否使用 | DB注释(中文) |
| 17 | QLT_REMARKS | VARCHAR2(300) | Y |  | 质量备注 | DB注释(中文) |

### MD_MATERIAL

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=28｜被读 28 过程 / 被写 0 过程｜操作 —
- **行数(克隆库)**：30　**主键**：（无显式主键）　**语义覆盖**：2/20

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | ID | VARCHAR2(32) | N |  |  | 空 |
| 2 | PK_MATERIAL | CHAR(20) | Y |  |  | 空 |
| 3 | PK_ORG | CHAR(20) | Y |  |  | 空 |
| 4 | CODE | VARCHAR2(40) | Y |  |  | 空 |
| 5 | NAME | VARCHAR2(200) | Y |  |  | 空 |
| 6 | VERSION | NUMBER | Y |  |  | 空 |
| 7 | LATEST | CHAR(1) | Y |  |  | 空 |
| 8 | MATERIAL_SPEC | VARCHAR2(400) | Y |  |  | 空 |
| 9 | MATERIAL_TYPE | VARCHAR2(400) | Y |  |  | 空 |
| 10 | PK_MEAS_DOC | CHAR(20) | Y |  |  | 空 |
| 11 | PK_MATERIAL_CLASS | CHAR(20) | Y |  |  | 空 |
| 12 | PK_MAT_TAXES | VARCHAR2(20) | Y |  |  | 空 |
| 13 | ENABLE_STATE | NUMBER | Y |  |  | 空 |
| 14 | CREATE_TIME | DATE | Y |  |  | 空 |
| 15 | NCC_CREATE_TIME | DATE | Y |  |  | 空 |
| 16 | UPDATE_TIME | DATE | Y |  |  | 空 |
| 17 | U8_CODE | VARCHAR2(32) | Y |  |  | 空 |
| 18 | IS_BATCH | CHAR(1) | Y |  |  | 空 |
| 19 | THK_RANGE | VARCHAR2(60) | Y |  | thk range | SCO_DATA_DIC(L) |
| 20 | WTH_RANGE | VARCHAR2(60) | Y |  | width range | SCO_DATA_DIC(L) |

### SWR_WIRE_MASTER

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=28｜被读 20 过程 / 被写 4 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：26703　**主键**：BATCH_NO　**语义覆盖**：70/72

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | SCO_DATA_DIC(D) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | SCO_DATA_DIC(D) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | SCO_DATA_DIC(D) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated UserID | SCO_DATA_DIC(D) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated ObjectID | SCO_DATA_DIC(D) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Date Time | SCO_DATA_DIC(D) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | SCO_DATA_DIC(D) |
| 8 | BATCH_NO | VARCHAR2(12) | N | ✓ | 批号 | DB注释(中文) |
| 9 | FAC_CD | VARCHAR2(1) | Y |  | 工序 | DB注释(中文) |
| 10 | PLAN_SIZE | NUMBER | Y |  | 计划规格 | DB注释(中文) |
| 11 | ACT_SIZE | NUMBER | Y |  | 实绩规格 | DB注释(中文) |
| 12 | SWR_STS_CD | VARCHAR2(1) | Y |  | 批号状态 | DB注释(中文) |
| 13 | SWR_OPER_TRK_CD | VARCHAR2(3) | Y |  | 作业进程 | DB注释(中文) |
| 14 | PROG_CD | VARCHAR2(4) | Y |  | 订单进程 | DB注释(中文) |
| 15 | PREV_PROG_CD | VARCHAR2(4) | Y |  | 前进程状态 | DB注释(中文) |
| 16 | UNIT_WGT | NUMBER | Y |  | 单重 | DB注释(中文) |
| 17 | TOT_WGT | NUMBER | Y |  | 总重 | DB注释(中文) |
| 18 | ACT_WGT | NUMBER | Y |  | 实际重量 | DB注释(中文) |
| 19 | BORE | NUMBER | Y |  | 内径 | DB注释(中文) |
| 20 | XRIB_HIGHT | NUMBER | Y |  | 横肋高 | DB注释(中文) |
| 21 | YRIB_HIGHT | NUMBER | Y |  | 纵肋高 | DB注释(中文) |
| 22 | WIRE_SPACE | NUMBER | Y |  | 间距 | DB注释(中文) |
| 23 | FCE_CH_NUM | NUMBER | Y |  | 装炉支数 | DB注释(中文) |
| 24 | FCE_DISCH_NUM | NUMBER | Y |  | 出炉支数 | DB注释(中文) |
| 25 | RM_RLG_NUM | NUMBER | Y |  | 粗轧支数 | DB注释(中文) |
| 26 | FM_RLG_NUM | NUMBER | Y |  | 精轧支数 | DB注释(中文) |
| 27 | WGT_NUM | NUMBER | Y |  | 称重支数 | DB注释(中文) |
| 28 | STR_NUM | NUMBER | Y |  | 入库支数 | DB注释(中文) |
| 29 | PROD_SFT_NO | VARCHAR2(1) | Y |  | 生产班次 | DB注释(中文) |
| 30 | PROD_GRP_NO | VARCHAR2(1) | Y |  | 生产班组 | DB注释(中文) |
| 31 | PROD_DATE | VARCHAR2(14) | Y |  | 生产日期 | DB注释(中文) |
| 32 | ERP_TRANS_YN | VARCHAR2(1) | Y |  | ERP传送与否 | DB注释(中文) |
| 33 | ERP_TRANS_DTM | VARCHAR2(14) | Y |  | ERP传送时间 | DB注释(中文) |
| 34 | RTN_NUM | VARCHAR2(1) | Y |  | 退库支数 | DB注释(中文) |
| 35 | RTN_DTM | VARCHAR2(14) | Y |  | 退库时间 | DB注释(中文) |
| 36 | RTN_PROC_REASON_CD | VARCHAR2(2) | Y |  | 退库原因 | DB注释(中文) |
| 37 | RTN_PROC_USER_ID | VARCHAR2(20) | Y |  | 退库操作人 | DB注释(中文) |
| 38 | BACK_NUM | NUMBER | Y |  | 回炉支数 | DB注释(中文) |
| 39 | REJECT_NUM | NUMBER | Y |  | 剔除支数 | DB注释(中文) |
| 40 | SCRAP_NUM | NUMBER | Y |  | 轧废支数 | DB注释(中文) |
| 41 | RJT_CD | VARCHAR2(14) | Y |  | 剔除原因 | DB注释(中文) |
| 42 | COMMENTS | VARCHAR2(100) | Y |  | 备注 | DB注释(中文) |
| 43 | OK_NUM | NUMBER | Y |  | 合格支数 | DB注释(中文) |
| 44 | DEF_CD_1 | VARCHAR2(10) | Y |  | 缺陷1 | DB注释(中文) |
| 45 | DEF_NUM_1 | NUMBER | Y |  | 缺陷1数量 | DB注释(中文) |
| 46 | DEF_CD_2 | VARCHAR2(10) | Y |  | 缺陷2 | DB注释(中文) |
| 47 | DEF_NUM_2 | NUMBER | Y |  | 缺陷2数量 | DB注释(中文) |
| 48 | DEF_CD_3 | VARCHAR2(10) | Y |  | 缺陷3 | DB注释(中文) |
| 49 | DEF_NUM_3 | NUMBER | Y |  | 缺陷3数量 | DB注释(中文) |
| 50 | DEF_CD_4 | VARCHAR2(10) | Y |  | 缺陷4 | DB注释(中文) |
| 51 | DEF_NUM_4 | NUMBER | Y |  | 缺陷4数量 | DB注释(中文) |
| 52 | DEF_CD_5 | VARCHAR2(10) | Y |  | 缺陷5 | DB注释(中文) |
| 53 | DEF_NUM_5 | NUMBER | Y |  | 缺陷5数量 | DB注释(中文) |
| 54 | PLAN_SPEC_CD | VARCHAR2(50) | Y |  | 计划钢种 | DB注释(中文) |
| 55 | SPEC_CD | VARCHAR2(50) | Y |  | 实绩钢种 | DB注释(中文) |
| 56 | STD_STLGRD | VARCHAR2(20) | Y |  | 炼钢内控钢种 | DB注释(中文) |
| 57 | PROD_CD | VARCHAR2(3) | Y |  | 品种 | DB注释(中文) |
| 58 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  |  | 空 |
| 59 | NATL_SPEC_YEAR | VARCHAR2(4) | Y |  | 국가표준년도 | SCO_DATA_DIC(D) |
| 60 | NATL_SPEC_NO | VARCHAR2(40) | Y |  |  | 空 |
| 61 | SEMI_PROD_ITEM_CD | VARCHAR2(30) | Y |  | 코일 반제품 ERP ITEM | SCO_DATA_DIC(D) |
| 62 | SALES_PROD_ITEM_CD | VARCHAR2(30) | Y |  | 코일 제품 ERP ITEM | SCO_DATA_DIC(D) |
| 63 | HCR_FL | VARCHAR2(1) | Y |  | 冷热送区分 | DB注释(中文) |
| 64 | ORD_FL | VARCHAR2(1) | Y |  | 订单材余材区分 | DB注释(中文) |
| 65 | ORD_NO | VARCHAR2(10) | Y |  | 订单号 | DB注释(中文) |
| 66 | ORD_LN | VARCHAR2(3) | Y |  | 订单行号 | DB注释(中文) |
| 67 | WGT_DTM | VARCHAR2(14) | Y |  | 称重时间 | DB注释(中文) |
| 68 | PLAN_COUNT | NUMBER | Y |  | 计划支数 | DB注释(中文) |
| 69 | ACT_LTH | NUMBER | Y |  | 实绩长度 | DB注释(中文) |
| 70 | NO_OK_NUM | NUMBER | Y |  | 不合格支数 | DB注释(中文) |
| 71 | LC_NUM | NUMBER | Y |  | 乱尺支数 | DB注释(中文) |
| 72 | STATE | VARCHAR2(3) | Y |  | 状态 1：已发布；2：未发布 | DB注释(中文) |

### SCH_PLAN_HEAT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=28｜被读 22 过程 / 被写 3 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：17184　**主键**：PLAN_HEAT_NO　**语义覆盖**：77/77

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID_Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID_Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time_Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID_Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID_Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time_Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag_Record Archive Flag | DB注释(非中文) |
| 8 | PLAN_HEAT_NO | VARCHAR2(50) | N | ✓ | 计划炉号 | DB注释(中文) |
| 9 | SPEC_HEAT_NO | VARCHAR2(200) | Y |  | SPEC Heat指令号码 | DB注释(中文) |
| 10 | INST_HEAT_NO | VARCHAR2(50) | Y |  | Heat指令号码 | DB注释(中文) |
| 11 | CAST_NO | VARCHAR2(8) | Y |  | 浇次号 | DB注释(中文) |
| 12 | PLAN_HEAT_CNT | NUMBER | Y |  | 预定Heat数量 | DB注释(中文) |
| 13 | PLAN_HEAT_PRI | NUMBER | Y |  | 炉次顺序 | DB注释(中文) |
| 14 | PLAN_HEAT_STS | VARCHAR2(3) | Y |  | 炉次状态(A1-计划生成,A2-计划下发L2,A3-转炉作业中,A4-转炉作业结束,A5-精炼作业中,A6-连铸作业中,A7-计划返送,A8-结束异常(返送),A9-作业结束) | DB注释(中文) |
| 15 | SPEC_CD | VARCHAR2(50) | Y |  | 国家标组及牌号 | DB注释(中文) |
| 16 | STEEL_GRD_GRP | VARCHAR2(10) | Y |  | 钢种组 | DB注释(中文) |
| 17 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  | 炼钢内控钢种编号 | DB注释(中文) |
| 18 | SECOND_RFN_CD | VARCHAR2(3) | Y |  | 2次精炼代码 | DB注释(中文) |
| 19 | DE_P_YN | VARCHAR2(1) | Y |  | 脱磷作业分类 | DB注释(中文) |
| 20 | HEAT_WGT | NUMBER | Y |  | 钢水重量 | DB注释(中文) |
| 21 | SLAB_TOT_LTH | NUMBER | Y |  | 板坯总长度 | DB注释(中文) |
| 22 | SLAB_PCS | NUMBER | Y |  | 板坯数量 | DB注释(中文) |
| 23 | PROD_PCS | NUMBER | Y |  | 产品数量 | DB注释(中文) |
| 24 | SLAB_THK | NUMBER | Y |  | 板坯厚度 | DB注释(中文) |
| 25 | WTH_CHANGE_YN | VARCHAR2(1) | Y |  | 宽度变更与否(Y/N) | DB注释(中文) |
| 26 | X_STR_SLAB_WTH_CHG_YN | VARCHAR2(1) | Y |  | X Strand Slab Width Change(Y/N) | DB注释(非中文) |
| 27 | X_STR_SLAB_TOT_LTH | NUMBER | Y |  | X Strand Slab Total Length_X(Y/N) | DB注释(非中文) |
| 28 | X_STR_SLAB_TOT_WGT | NUMBER | Y |  | X Strand Slab Total Weight_X(Y/N) | DB注释(非中文) |
| 29 | X_STR_SLAB_PCS | NUMBER | Y |  | X Strand Slab Pieces_X(Y/N) | DB注释(非中文) |
| 30 | X_STR_SLAB_THK | NUMBER | Y |  | X Strand Slab Thickness_X(Y/N) | DB注释(非中文) |
| 31 | X_STR_SLAB_STA_WTH | NUMBER | Y |  | X Strand Slab Start Width_X(Y/N) | DB注释(非中文) |
| 32 | X_STR_SLAB_END_WTH | NUMBER | Y |  | X Strand Slab End Width_X(Y/N) | DB注释(非中文) |
| 33 | Y_STR_SLAB_WTH_CHG_YN | VARCHAR2(1) | Y |  | Y Strand Slab Width Change(Y/N) | DB注释(非中文) |
| 34 | Y_STR_SLAB_TOT_LTH | NUMBER | Y |  | Y Strand Slab Total Length_Y(Y/N) | DB注释(非中文) |
| 35 | Y_STR_SLAB_TOT_WGT | NUMBER | Y |  | Y Strand Slab Total Weight_Y(Y/N) | DB注释(非中文) |
| 36 | Y_STR_SLAB_PCS | NUMBER | Y |  | Y Strand Slab Pieces_Y(Y/N) | DB注释(非中文) |
| 37 | Y_STR_SLAB_THK | NUMBER | Y |  | Y Strand Slab Thickness_Y(Y/N) | DB注释(非中文) |
| 38 | Y_STR_SLAB_STA_WTH | NUMBER | Y |  | Y Strand Slab Start Width(Y/N) | DB注释(非中文) |
| 39 | Y_STR_SLAB_END_WTH | NUMBER | Y |  | Y Strand Slab End Width_Y(Y/N) | DB注释(非中文) |
| 40 | ORD_FL | VARCHAR2(1) | Y |  | 订单材/余材标记 | DB注释(中文) |
| 41 | ORD_NO | VARCHAR2(10) | Y |  | 订单号 | DB注释(中文) |
| 42 | ORD_LN | VARCHAR2(3) | Y |  | 订单行号 | DB注释(中文) |
| 43 | TAP_REQ_DT | VARCHAR2(8) | Y |  | 出钢要求日 | DB注释(中文) |
| 44 | HEAT_TAP_PLAN_DT | VARCHAR2(8) | Y |  | 预计出钢日 | DB注释(中文) |
| 45 | SPEC_RCV_DTM | VARCHAR2(14) | Y |  | 计划接收日期 | DB注释(中文) |
| 46 | PROD_INST_DTM | VARCHAR2(14) | Y |  | 作业指令传送日 | DB注释(中文) |
| 47 | RTN_YN | VARCHAR2(1) | Y |  | 返送与否(Y/N) | DB注释(中文) |
| 48 | STEEL_GRD_DIVERT_YN | VARCHAR2(1) | Y |  | 钢种变更与否(Y/N) | DB注释(中文) |
| 49 | PLAN_PROC_ROUTE | VARCHAR2(30) | Y |  | 计划通过工序 | DB注释(中文) |
| 50 | PLAN_CHANGE_TY | VARCHAR2(1) | Y |  | Plan Change Type | DB注释(非中文) |
| 51 | BOF_BALANCE_TY | VARCHAR2(2) | Y |  | BOF Balance Type(M1-Same Mc DE-P/C,M2-Only BOF#1 DE-P,M3-Only BOF#2 DE-P,M4-Cross Mc DE-P/C) | DB注释(非中文) |
| 52 | TUNDISH_CHG_FL | VARCHAR2(1) | Y |  | Tundish Chage Flag_Tundish Chage Flag | DB注释(非中文) |
| 53 | STA_SLAB_CUT_LTH | NUMBER | Y |  | 坯料长度-头 | DB注释(中文) |
| 54 | END_SLAB_CUT_LTH | NUMBER | Y |  | 坯料长度-尾 | DB注释(中文) |
| 55 | STA_SLAB_TD_CHG_CUT_LTH | NUMBER | Y |  | After Tundish Change, Start Slab Cutting Length in SEQ_Tundish | DB注释(非中文) |
| 56 | END_SLAB_TD_CHG_CUT_LTH | NUMBER | Y |  | Before Tundish Change, End Slab Cutting Length in SEQ_Tundish | DB注释(非中文) |
| 57 | CUT_SLAB_WGT | NUMBER | Y |  | 坯料重量 | DB注释(中文) |
| 58 | PROD_INST_REASON | VARCHAR2(50) | Y |  | Production Instruction Reason | DB注释(非中文) |
| 59 | SPEC_RTN_CD | VARCHAR2(500) | Y |  | 返送原因 | DB注释(中文) |
| 60 | CC_NO | VARCHAR2(1) | Y |  | 铸机号 | DB注释(中文) |
| 61 | UPDATE_KEY | VARCHAR2(18) | Y |  | 浇次号变更Key | DB注释(中文) |
| 62 | SPEC_CAST_NO | VARCHAR2(8) | Y |  | SPEC Cast No | DB注释(非中文) |
| 63 | INST_OBJ_YN | VARCHAR2(1) | Y |  | Instruction Object(Y/N) | DB注释(非中文) |
| 64 | FAC_CD | VARCHAR2(5) | Y |  | Factory Code | DB注释(非中文) |
| 65 | PI_REQ_WGT | NUMBER | Y |  | 铁水需求量 | DB注释(中文) |
| 66 | SPEC_RTN_USER_ID | VARCHAR2(20) | Y |  | 返送人 | DB注释(中文) |
| 67 | SPEC_RTN_DTM | VARCHAR2(14) | Y |  | 返送日期 | DB注释(中文) |
| 68 | PROD_CD | VARCHAR2(3) | Y |  | 品名代码 | DB注释(中文) |
| 69 | DE_P_MC_NO | VARCHAR2(1) | Y |  | 转炉号（脱P） | DB注释(中文) |
| 70 | DE_C_MC_NO | VARCHAR2(1) | Y |  | 转炉号（脱C） | DB注释(中文) |
| 71 | WF_MC_NO | VARCHAR2(1) | Y |  | WF | DB注释(非中文) |
| 72 | LF_MC_NO | VARCHAR2(1) | Y |  | LF | DB注释(非中文) |
| 73 | RH_MC_NO | VARCHAR2(1) | Y |  | RH | DB注释(非中文) |
| 74 | CC_MC_NO | VARCHAR2(1) | Y |  | 连铸 | DB注释(中文) |
| 75 | VD_MC_NO | VARCHAR2(1) | Y |  | VD | DB注释(非中文) |
| 76 | CAST_TYPE | NUMBER | Y |  | 浇次类型(0-正常浇次,1-异常替代浇次) | DB注释(中文) |
| 77 | CAST_START_WORK_TM | VARCHAR2(14) | Y |  | 计划开始生产时间 | DB注释(中文) |

### SHR_HCOIL_FCE_RSLT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=28｜被读 18 过程 / 被写 5 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：152　**主键**：SLAB_NO、NO_FCE_CHARGE、SCH_ID　**语义覆盖**：56/56

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | SLAB_NO | VARCHAR2(12) | N | ✓ | SLAB NO | DB注释(非中文) |
| 9 | NO_FCE_CHARGE | NUMBER | N | ✓ | Charge Count | DB注释(非中文) |
| 10 | SCH_ID | VARCHAR2(10) | N | ✓ | Schedule No | DB注释(非中文) |
| 11 | RCD_STS_ID | VARCHAR2(1) | Y |  | Record Status Flag | DB注释(非中文) |
| 12 | FCE_DISCH_SUMUP_DT | VARCHAR2(8) | Y |  | Discharge Work DATE | DB注释(非中文) |
| 13 | SCH_SEQ | NUMBER | Y |  | Work Sequence | DB注释(非中文) |
| 14 | COIL_NO | VARCHAR2(14) | Y |  | Coil NO | DB注释(非中文) |
| 15 | FCE_NO | VARCHAR2(1) | Y |  | FurnaceNO | DB注释(非中文) |
| 16 | FCE_CHARGE_DTM | VARCHAR2(14) | Y |  | Furnace Charge Date | DB注释(非中文) |
| 17 | FCE_DISCH_DTM | VARCHAR2(14) | Y |  | Furnace Discharge Date | DB注释(非中文) |
| 18 | FCE_STAY_DUR | NUMBER | Y |  | Stay Duration | DB注释(非中文) |
| 19 | FCE_ROWNUM | VARCHAR2(1) | Y |  | Furnace  RowNO | DB注释(非中文) |
| 20 | SLAB_TEMP_MEAS | NUMBER | Y |  | Charge SLAB Temperature | DB注释(非中文) |
| 21 | SLAB_LENGTH_MEAS | NUMBER | Y |  | Charge SLAB Length | DB注释(非中文) |
| 22 | SLAB_WEIGHT_MEAS | NUMBER | Y |  | Charge SLAB Weight | DB注释(非中文) |
| 23 | FCE_CHARGE_FL | VARCHAR2(1) | Y |  | Charge / Recharge Flag | DB注释(非中文) |
| 24 | REJ_RSN | VARCHAR2(30) | Y |  | RejectReason | DB注释(非中文) |
| 25 | REJ_DTM | VARCHAR2(14) | Y |  | Reject Date | DB注释(非中文) |
| 26 | REJ_ROWNUM | VARCHAR2(2) | Y |  | Row NO | DB注释(非中文) |
| 27 | REJ_SHF_ID | VARCHAR2(1) | Y |  | Reject Shift | DB注释(非中文) |
| 28 | REJ_CREW_ID | VARCHAR2(1) | Y |  | Reject Crew | DB注释(非中文) |
| 29 | REJ_CD | VARCHAR2(2) | Y |  | Reject Reason Code | DB注释(非中文) |
| 30 | REJ_EMP_NO | VARCHAR2(20) | Y |  | Reject Charger Employee No | DB注释(非中文) |
| 31 | REJ_POS | VARCHAR2(7) | Y |  | Reject Position | DB注释(非中文) |
| 32 | FCE_CHARGE_TEMP | NUMBER | Y |  | Furnace ChargeTemperature | DB注释(非中文) |
| 33 | RHF_ROWNUM | NUMBER | Y |  | Heating Position | DB注释(非中文) |
| 34 | TM_IN_PREHEAT | NUMBER | Y |  | Preheating Row Work Duration | DB注释(非中文) |
| 35 | TM_IN_HEAT1 | NUMBER | Y |  | Furnace1 Work Duration | DB注释(非中文) |
| 36 | TM_IN_HEAT2 | NUMBER | Y |  | Furnace2 Work Duration | DB注释(非中文) |
| 37 | TM_IN_HEAT3 | NUMBER | Y |  | Furnace3 Work Duration | DB注释(非中文) |
| 38 | TM_IN_SOAK | NUMBER | Y |  | SS Work Duration | DB注释(非中文) |
| 39 | TEMP_IN_SUR_PREHEAT | NUMBER | Y |  | Preheating Surface Temperature | DB注释(非中文) |
| 40 | TEMP_IN_DEEP_PREHEAT | NUMBER | Y |  | Preheating Deep Temperature | DB注释(非中文) |
| 41 | TEMP_IN_SUR_HEAT1 | NUMBER | Y |  | Furnace1 SurfaceTemperature | DB注释(非中文) |
| 42 | TEMP_IN_DEEP_HEAT1 | NUMBER | Y |  | Furnace1 SurfaceTemperature | DB注释(非中文) |
| 43 | TEMP_IN_SUR_HEAT2 | NUMBER | Y |  | Furnace2 SurfaceTemperature | DB注释(非中文) |
| 44 | TEMP_IN_DEEP_HEAT2 | NUMBER | Y |  | Furnace2 SurfaceTemperature | DB注释(非中文) |
| 45 | TEMP_IN_SUR_HEAT3 | NUMBER | Y |  | Furnace3 SurfaceTemperature | DB注释(非中文) |
| 46 | TEMP_IN_DEEP_HEAT3 | NUMBER | Y |  | Furnace3 SurfaceTemperature | DB注释(非中文) |
| 47 | FCE_DISCH_DTM1 | NUMBER | Y |  | Furnace Discharge Duration | DB注释(非中文) |
| 48 | FCE_DISCH_TEMP | NUMBER | Y |  | Furnace Discharge Temperature | DB注释(非中文) |
| 49 | UPPER_TEMP | NUMBER | Y |  | Upper Temperature | DB注释(非中文) |
| 50 | CEN_TEMP | NUMBER | Y |  | Middle Temperature | DB注释(非中文) |
| 51 | BTM_TEMP | NUMBER | Y |  | Bottom Temperature | DB注释(非中文) |
| 52 | TEMP_GAP_BTN_SURF | NUMBER | Y |  | Surface Temperature Gap | DB注释(非中文) |
| 53 | FCE_DISCHARGE_FL | VARCHAR2(4) | Y |  | Discharge Flag | DB注释(非中文) |
| 54 | FUR_SHIFT | VARCHAR2(1) | Y |  | Shift | DB注释(非中文) |
| 55 | FUR_CREW | VARCHAR2(1) | Y |  | Crew | DB注释(非中文) |
| 56 | FUR_EMP_ID | VARCHAR2(20) | Y |  | Worker Employee ID | DB注释(非中文) |

### SIT_TRANS_RSLT_DETAIL

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=28｜被读 26 过程 / 被写 1 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：91　**主键**：TRK_SCALE_PLAN_NO、TASK_ID　**语义覆盖**：45/45

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | TRK_SCALE_PLAN_NO | VARCHAR2(15) | N | ✓ | ??????? | DB注释(非中文) |
| 9 | GROSS_WGT | NUMBER | Y |  | ???? | DB注释(非中文) |
| 10 | TARE_WGT | NUMBER | Y |  | ???? | DB注释(非中文) |
| 11 | NET_WGT | NUMBER | Y |  | ???? | DB注释(非中文) |
| 12 | GROSS_SCALE_NO | VARCHAR2(15) | Y |  | ??????? | DB注释(非中文) |
| 13 | GROSS_SCALE_DTM | VARCHAR2(14) | Y |  | ?????? | DB注释(非中文) |
| 14 | TARE_SCALE_NO | VARCHAR2(15) | Y |  | ??????? | DB注释(非中文) |
| 15 | TARE_SCALE_DTM | VARCHAR2(14) | Y |  | ?????? | DB注释(非中文) |
| 16 | CAR_NO | VARCHAR2(20) | Y |  | ?? | DB注释(非中文) |
| 17 | MATERIAL_CD | VARCHAR2(18) | Y |  | ???? | DB注释(非中文) |
| 18 | TRANS_CD | VARCHAR2(11) | Y |  | ?????? | DB注释(非中文) |
| 19 | SCALE_INVOICE_CD | VARCHAR2(12) | Y |  | ?????? | DB注释(非中文) |
| 20 | SCALE_EMP_NM | VARCHAR2(20) | Y |  | ??? | DB注释(非中文) |
| 21 | TRK_SCALE_TY | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 22 | SCALE_RCV_DTM | VARCHAR2(14) | Y |  | ???? | DB注释(非中文) |
| 23 | TRANS_TY | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 24 | TARE_SCALE_NM | VARCHAR2(30) | Y |  | ??????? | DB注释(非中文) |
| 25 | GROSS_SCALE_NM | VARCHAR2(30) | Y |  | ??????? | DB注释(非中文) |
| 26 | TARE_SCALE_EMP_NM | VARCHAR2(20) | Y |  | ????? | DB注释(非中文) |
| 27 | GROSS_SCALE_EMP_NM | VARCHAR2(20) | Y |  | ????? | DB注释(非中文) |
| 28 | TASK_ID | VARCHAR2(15) | N | ✓ | ????? | DB注释(非中文) |
| 29 | CONF_FL | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 30 | CONF_DTM | VARCHAR2(14) | Y |  | ???? | DB注释(非中文) |
| 31 | ORIGIN_CD | VARCHAR2(11) | Y |  | ????? | DB注释(非中文) |
| 32 | DEST_CD | VARCHAR2(11) | Y |  | ????? | DB注释(非中文) |
| 33 | ORGINAL_NM | VARCHAR2(50) | Y |  | ????? | DB注释(非中文) |
| 34 | DEST_NM | VARCHAR2(50) | Y |  | ????? | DB注释(非中文) |
| 35 | ORGINAL_INVENTORY | VARCHAR2(50) | Y |  | ???? | DB注释(非中文) |
| 36 | DEST_INVENTORY | VARCHAR2(50) | Y |  | ???? | DB注释(非中文) |
| 37 | UPDATE_FL | VARCHAR2(10) | Y |  | ???? | DB注释(非中文) |
| 38 | UOM | VARCHAR2(3) | Y |  | ???? | DB注释(非中文) |
| 39 | ATTRIBUTE1 | VARCHAR2(100) | Y |  | ????1 | DB注释(非中文) |
| 40 | ATTRIBUTE2 | VARCHAR2(100) | Y |  | ????2 | DB注释(非中文) |
| 41 | ATTRIBUTE3 | VARCHAR2(100) | Y |  | ????3 | DB注释(非中文) |
| 42 | ATTRIBUTE4 | VARCHAR2(100) | Y |  | ????4 | DB注释(非中文) |
| 43 | ATTRIBUTE5 | VARCHAR2(100) | Y |  | ????5 | DB注释(非中文) |
| 44 | ATTRIBUTE6 | VARCHAR2(100) | Y |  | ????6 | DB注释(非中文) |
| 45 | TRANSPORT_CODE | VARCHAR2(15) | Y |  | ????SIT_TRANS_CODE | DB注释(非中文) |

### SRS_ROLL_MASTER_HIST

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=28｜被读 2 过程 / 被写 13 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：128　**主键**：ROLL_NO、HIST_DTM　**语义覆盖**：46/46

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | ROLL_NO | VARCHAR2(8) | N | ✓ | Roll Number | DB注释(非中文) |
| 9 | HIST_DTM | VARCHAR2(14) | N | ✓ | History Datetime | DB注释(非中文) |
| 10 | PROC_CD | VARCHAR2(8) | Y |  | Process Code | DB注释(非中文) |
| 11 | ROLL_STS | VARCHAR2(1) | Y |  | Roll Status | DB注释(非中文) |
| 12 | ROLL_PROG_CD | VARCHAR2(1) | Y |  | Roll Progress Code | DB注释(非中文) |
| 13 | ROLL_TY | VARCHAR2(1) | Y |  | Roll Type | DB注释(非中文) |
| 14 | ROLL_MTRL | VARCHAR2(5) | Y |  | Roll Material | DB注释(非中文) |
| 15 | ROLL_INBND_DTM | VARCHAR2(14) | Y |  | Roll Inbound Datetime | DB注释(非中文) |
| 16 | ROLL_INBND_SUMUP_DT | VARCHAR2(8) | Y |  | Roll Inbound Sumup Date | DB注释(非中文) |
| 17 | ROLL_INBND_EMP_ID | VARCHAR2(20) | Y |  | Roll Inbound Employee ID | DB注释(非中文) |
| 18 | ROLL_INBND_SFT | VARCHAR2(2) | Y |  | Roll Inbound Shift | DB注释(非中文) |
| 19 | ROLL_PO_NO | NUMBER | Y |  | Roll PO No | DB注释(非中文) |
| 20 | ROLL_MAK_CD | VARCHAR2(5) | Y |  | Roll Maker Code | DB注释(非中文) |
| 21 | ROLL_WGT | NUMBER | Y |  | Roll Weight | DB注释(非中文) |
| 22 | ROLL_BRL_LTH | NUMBER | Y |  | Roll Barrel Length | DB注释(非中文) |
| 23 | ROLL_HARD_INIT | NUMBER | Y |  | Roll Hardness Init | DB注释(非中文) |
| 24 | ROLL_HARD_DISCARD | NUMBER | Y |  | Roll Hardness Discard | DB注释(非中文) |
| 25 | ROLL_HARD_CURR | NUMBER | Y |  | Roll Hardness Current | DB注释(非中文) |
| 26 | ROLL_DIA_INIT | NUMBER | Y |  | Roll Diameter Init | DB注释(非中文) |
| 27 | ROLL_DIA_DISCARD | NUMBER | Y |  | Roll Diameter Discard | DB注释(非中文) |
| 28 | ROLL_DIA_CURR | NUMBER | Y |  | Roll Diameter Current | DB注释(非中文) |
| 29 | ROLL_DIA_EFFECTIVE | NUMBER | Y |  | Roll Diameter Effective | DB注释(非中文) |
| 30 | ROLL_ROUGH | NUMBER | Y |  | Roll Roughness | DB注释(非中文) |
| 31 | ROLL_DISCARD_DTM | VARCHAR2(14) | Y |  | Roll Discard Datetime | DB注释(非中文) |
| 32 | ROLL_DISCARD_SUMUP_DT | VARCHAR2(8) | Y |  | Roll Discard Sumup Date | DB注释(非中文) |
| 33 | ROLL_DISCARD_EMP_ID | VARCHAR2(20) | Y |  | Roll Discard Employee ID | DB注释(非中文) |
| 34 | ROLL_DISCARD_SFT | VARCHAR2(2) | Y |  | Roll Discard Shift | DB注释(非中文) |
| 35 | ROLL_DISCARD_RSN_TY | VARCHAR2(2) | Y |  | Roll Discard Reason Type | DB注释(非中文) |
| 36 | ROLL_LOC_TY | VARCHAR2(1) | Y |  | Roll Location Type | DB注释(非中文) |
| 37 | ROLL_STAND_TY | VARCHAR2(2) | Y |  | Roll Stand Type | DB注释(非中文) |
| 38 | ROLL_INST_SEQ | NUMBER | Y |  | Roll Instrument Sequence | DB注释(非中文) |
| 39 | ROLL_NO_REL | VARCHAR2(8) | Y |  | Roll No Related | DB注释(非中文) |
| 40 | CCK_NO_WS | VARCHAR2(8) | Y |  | Roll WS Chock No | DB注释(非中文) |
| 41 | CCK_NO_DS | VARCHAR2(8) | Y |  | Roll DS Chock No | DB注释(非中文) |
| 42 | BRG_NO_WS | VARCHAR2(8) | Y |  | Roll WS Bearing No1 | DB注释(非中文) |
| 43 | BRG_NO_DS | VARCHAR2(8) | Y |  | Roll WS Bearing No2 | DB注释(非中文) |
| 44 | BRG_NO_WT | VARCHAR2(8) | Y |  | Roll DS Bearing No1 | DB注释(非中文) |
| 45 | ASSEMBLY_YN | VARCHAR2(1) | Y |  | Assembly YN | DB注释(非中文) |
| 46 | REMARKS | VARCHAR2(1000) | Y |  | Remarks | DB注释(非中文) |

### SCH_PLAN_ROLL

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=27｜被读 23 过程 / 被写 2 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：0　**主键**：ROLL_UNIT、MTL_NO　**语义覆盖**：81/81

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | ROLL_UNIT | VARCHAR2(10) | N | ✓ | Roll Unit | DB注释(非中文) |
| 9 | MTL_NO | VARCHAR2(14) | N | ✓ | Matrial No | DB注释(非中文) |
| 10 | SPEC_ROLL_UNIT | VARCHAR2(10) | Y |  | SPEC Roll Unit | DB注释(非中文) |
| 11 | SPEC_MTL_NO | VARCHAR2(14) | Y |  | SPEC Matrial No | DB注释(非中文) |
| 12 | INST_COIL_NO | VARCHAR2(14) | Y |  | Instruction Coil No | DB注释(非中文) |
| 13 | ROLL_UNIT_PRI | NUMBER | Y |  | Roll Unit Priority | DB注释(非中文) |
| 14 | PLAN_PROC_SEQ | NUMBER | Y |  | Plan Process Sequence | DB注释(非中文) |
| 15 | SPEC_RCV_DTM | VARCHAR2(14) | Y |  | Spec Receive DateTime | DB注释(非中文) |
| 16 | PROD_INST_DTM | VARCHAR2(14) | Y |  | Production Order Send(L2) Datetime | DB注释(非中文) |
| 17 | WK_STA_SCH_DTM | VARCHAR2(14) | Y |  | Work Start Schedule Datetime | DB注释(非中文) |
| 18 | WK_END_SCH_DTM | VARCHAR2(14) | Y |  | Work End Schedule Datetime | DB注释(非中文) |
| 19 | PLAN_ROLL_STS | VARCHAR2(3) | Y |  | PLAN Roll Staus | DB注释(非中文) |
| 20 | RF_CH_LOT_NO | VARCHAR2(10) | Y |  | ¿¿¿¿¿Lot¿¿ | DB注释(非中文) |
| 21 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  | Steel Grade | DB注释(非中文) |
| 22 | SPEC_CD | VARCHAR2(50) | Y |  | Specification Code | DB注释(非中文) |
| 23 | ORD_NO | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 24 | ORD_LN | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 25 | ORD_NO1 | VARCHAR2(10) | Y |  | Order No1 | DB注释(非中文) |
| 26 | ORD_LN1 | VARCHAR2(3) | Y |  | Order Line1 | DB注释(非中文) |
| 27 | SLAB_DGN_WGT1 | NUMBER | Y |  | Slab Design Weight1 | DB注释(非中文) |
| 28 | SLAB_DGN_LTH1 | NUMBER | Y |  | SlabDesign Length1 | DB注释(非中文) |
| 29 | ORD_NO2 | VARCHAR2(10) | Y |  | Order No2 | DB注释(非中文) |
| 30 | ORD_LN2 | VARCHAR2(3) | Y |  | Order Line2 | DB注释(非中文) |
| 31 | SLAB_DGN_WGT2 | NUMBER | Y |  | Slab Design Weight2 | DB注释(非中文) |
| 32 | SLAB_DGN_LTH2 | NUMBER | Y |  | SlabDesign Length2 | DB注释(非中文) |
| 33 | ORD_NO3 | VARCHAR2(10) | Y |  | Order No3 | DB注释(非中文) |
| 34 | ORD_LN3 | VARCHAR2(3) | Y |  | Order Line3 | DB注释(非中文) |
| 35 | SLAB_DGN_WGT3 | NUMBER | Y |  | Slab Design Weight3 | DB注释(非中文) |
| 36 | SLAB_DGN_LTH3 | NUMBER | Y |  | SlabDesign Length3 | DB注释(非中文) |
| 37 | HCR_FL | VARCHAR2(1) | Y |  | HCR Flag | DB注释(非中文) |
| 38 | HCOIL_THK | NUMBER | Y |  | Hot Coil Thickness | DB注释(非中文) |
| 39 | HCOIL_WTH | NUMBER | Y |  | Hot Coil Width | DB注释(非中文) |
| 40 | HCOIL_LTH | NUMBER | Y |  | Hot Coil length | DB注释(非中文) |
| 41 | HCOIL_WGT | NUMBER | Y |  | Hot Coil Weight | DB注释(非中文) |
| 42 | PROD_THK | NUMBER | Y |  | Product Thickness | DB注释(非中文) |
| 43 | PROD_WTH | NUMBER | Y |  | Product Width | DB注释(非中文) |
| 44 | PROD_LTH | NUMBER | Y |  | Product Length | DB注释(非中文) |
| 45 | PROD_WGT | NUMBER | Y |  | Product Weight | DB注释(非中文) |
| 46 | PROD_PCS | NUMBER | Y |  | Product Pieces | DB注释(非中文) |
| 47 | SLAB_NO | VARCHAR2(13) | Y |  | Slab No | DB注释(非中文) |
| 48 | SLAB_STS | VARCHAR2(1) | Y |  | Slab Status | DB注释(非中文) |
| 49 | SLAB_THK | NUMBER | Y |  | Slab Thickness | DB注释(非中文) |
| 50 | SLAB_WTH | NUMBER | Y |  | Slab Width | DB注释(非中文) |
| 51 | SLAB_LTH | NUMBER | Y |  | Slab Length | DB注释(非中文) |
| 52 | SLAB_WGT | NUMBER | Y |  | Slab Weight | DB注释(非中文) |
| 53 | SMP_NO | VARCHAR2(11) | Y |  | Sample No | DB注释(非中文) |
| 54 | SMPING_TY | VARCHAR2(1) | Y |  | Simpling Type | DB注释(非中文) |
| 55 | HRL_MFC_STD_NO | VARCHAR2(11) | Y |  | Manufacturing standard marks of HR | DB注释(非中文) |
| 56 | HR_HR_THK_SET_AIM | NUMBER | Y |  | ¿¿¿¿¿¿Set¿¿¿ | DB注释(非中文) |
| 57 | HR_HR_THK_SET_TOL_MIN | NUMBER | Y |  | ¿¿¿¿¿¿Set¿¿¿¿¿¿ | DB注释(非中文) |
| 58 | HR_HR_THK_SET_TOL_MAX | NUMBER | Y |  | ¿¿¿¿¿¿Set¿¿¿¿¿¿ | DB注释(非中文) |
| 59 | HR_PROD_THK_AIM | NUMBER | Y |  | ¿¿¿¿¿¿ | DB注释(非中文) |
| 60 | HR_PROD_WTH_AIM | NUMBER | Y |  | ¿¿¿¿¿ | DB注释(非中文) |
| 61 | HR_PROD_WTH_TOL_MIN | NUMBER | Y |  | ¿¿¿¿¿¿¿¿¿¿¿ | DB注释(非中文) |
| 62 | HR_PROD_WTH_TOL_MAX | NUMBER | Y |  | ¿¿¿¿¿¿¿¿¿¿¿ | DB注释(非中文) |
| 63 | HR_PLAN_OP_CD | VARCHAR2(60) | Y |  | ¿¿¿¿¿¿¿¿ | DB注释(非中文) |
| 64 | HR_SPT_INDI_F | VARCHAR2(1) | Y |  | ¿¿¿¿¿¿¿¿¿¿ | DB注释(非中文) |
| 65 | HR_EH_FLAG | VARCHAR2(1) | Y |  | ¿¿EdgeHeater¿¿¿¿ | DB注释(非中文) |
| 66 | HRL_SP_COMPOSITE_TY | VARCHAR2(1) | Y |  | ¿¿¿¿SkinPass¿¿ | DB注释(非中文) |
| 67 | HRL_AFTER_COIL_COOL_TY | VARCHAR2(1) | Y |  | ¿¿¿¿¿¿¿¿¿ | DB注释(非中文) |
| 68 | RJT_CAUSE_CD | VARCHAR2(5) | Y |  | Reject Cause Code | DB注释(非中文) |
| 69 | SPEC_RTN_CD | VARCHAR2(2) | Y |  | Spec Return Code | DB注释(非中文) |
| 70 | FAC_CD | VARCHAR2(1) | Y |  | Factory Code | DB注释(非中文) |
| 71 | ROLL_UNIT_INST_SEQ | NUMBER | Y |  | Roll Unit Instruction SEQ | DB注释(非中文) |
| 72 | TE_PRD_FL | VARCHAR2(1) | Y |  | Test Production Flag | DB注释(非中文) |
| 73 | DIV_PCS | NUMBER | Y |  | Dvide PCS | DB注释(非中文) |
| 74 | SPEC_RTN_USER_ID | VARCHAR2(20) | Y |  | Spec Return User ID | DB注释(非中文) |
| 75 | SPEC_RTN_DTM | VARCHAR2(14) | Y |  | Spec Return Datetime | DB注释(非中文) |
| 76 | SPM_YN | VARCHAR2(1) | Y |  | Y-订单没有要求平整，但是工序板坯设计时需要平整或分卷 | DB注释(中文) |
| 77 | PLAN_DESC | VARCHAR2(300) | Y |  | 计划备注 | DB注释(中文) |
| 78 | LOCK_YN | NUMBER | Y |  | 是否锁定 | DB注释(中文) |
| 79 | BATCH_CD | VARCHAR2(20) | Y |  | 批次号 | DB注释(中文) |
| 80 | IS_MAIN_BATCH | NUMBER | Y |  | 是否是代表批次信息0 代表批次，1非代表批次 | DB注释(中文) |
| 81 | BATCH_ROLL_PRI | NUMBER | Y |  | 批次轧制顺序 | DB注释(中文) |

### SQM_ORD_SZSHP_TOL

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=27｜被读 23 过程 / 被写 2 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：61393　**主键**：ORD_NO、ORD_LN、QLT_DSN_STD_TY、QLT_SZSHP_TOL_CD　**语义覆盖**：17/17

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 修改人 | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | 修改时间 | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | ORD_NO | VARCHAR2(10) | N | ✓ | 订单编号 | DB注释(中文) |
| 9 | ORD_LN | VARCHAR2(3) | N | ✓ | 订单行号 | DB注释(中文) |
| 10 | QLT_DSN_STD_TY | VARCHAR2(1) | N | ✓ | 质量设计标准区分 | DB注释(中文) |
| 11 | QLT_SZSHP_TOL_CD | VARCHAR2(3) | N | ✓ | 尺寸形状允许偏差代码 | DB注释(中文) |
| 12 | QLT_TOL_UNT_TY | VARCHAR2(10) | Y |  | 允许偏差单位分类 | DB注释(中文) |
| 13 | QLT_TOL_UNT_CD | VARCHAR2(3) | Y |  | 允许偏差单位代码 | DB注释(中文) |
| 14 | QLT_TOL_MIN_FOMULA | VARCHAR2(1) | Y |  | 允许偏差下限计算公式 | DB注释(中文) |
| 15 | QLT_DSN_TOL_MIN | NUMBER | Y |  | 质量设计允许偏差下限 | DB注释(中文) |
| 16 | QLT_TOL_MAX_FOMULA | VARCHAR2(1) | Y |  | 允许偏差上限计算公式 | DB注释(中文) |
| 17 | QLT_DSN_TOL_MAX | NUMBER | Y |  | 质量设计允许偏差上限 | DB注释(中文) |

### SQM_ORD_MECH_PRL

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=27｜被读 23 过程 / 被写 2 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：16958　**主键**：ORD_NO、ORD_LN、QLT_DSN_STD_TY　**语义覆盖**：605/650

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 修改人 | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | 修改时间 | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | ORD_NO | VARCHAR2(10) | N | ✓ | 订单编号 | DB注释(中文) |
| 9 | ORD_LN | VARCHAR2(3) | N | ✓ | 订单行号 | DB注释(中文) |
| 10 | QLT_DSN_STD_TY | VARCHAR2(1) | N | ✓ | 质量设计标准区分 | DB注释(中文) |
| 11 | TSL_SMP_CND | VARCHAR2(2) | Y |  | 拉伸测试取样条件 | DB注释(中文) |
| 12 | TSL_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 拉伸测试长度方向取样位置 | DB注释(中文) |
| 13 | TSL_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 拉伸测试宽度方向取样位置 | DB注释(中文) |
| 14 | TSL_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 拉伸测试取样试样方向 | DB注释(中文) |
| 15 | TSL_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 拉伸测试取样试样尺寸 | DB注释(中文) |
| 16 | TSL_SMP_THK_LOC | VARCHAR2(1) | Y |  | 拉伸测试板厚度方向取样位置 | DB注释(中文) |
| 17 | TSL_SMP_CD | VARCHAR2(1) | Y |  | 拉伸试样类型 | DB注释(中文) |
| 18 | TSL_SMP_STATUS | VARCHAR2(1) | Y |  | 拉伸测试试样状态 | DB注释(中文) |
| 19 | TSL_STRESS_GRT_CD | VARCHAR2(1) | Y |  | 消应力处理保证代号 | DB注释(中文) |
| 20 | TSL_STRESS_WARM_TEMP | NUMBER | Y |  | 消应力处理_保温温度 | DB注释(中文) |
| 21 | TSL_STRESS_WARM_TIME | NUMBER | Y |  | 消应力处理_保温时间 | DB注释(中文) |
| 22 | TSL_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 消应力处理_冷却方式 | DB注释(中文) |
| 23 | TSL_SMP_CUT_PHOTO | VARCHAR2(1) | Y |  | 拉伸试样断口照片 | DB注释(中文) |
| 24 | TSL_YP_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度保证代号(YP) | DB注释(中文) |
| 25 | TSL_YP_MIN | NUMBER | Y |  | 拉伸测试屈服强度YP下限值 | DB注释(中文) |
| 26 | TSL_YP_MAX | NUMBER | Y |  | 拉伸测试屈服强度YP上限值 | DB注释(中文) |
| 27 | TSL_YP_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度类型 | DB注释(中文) |
| 28 | TSL_TS_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试抗拉强度保证代号(TS) | DB注释(中文) |
| 29 | TSL_TS_MIN | NUMBER | Y |  | 拉伸测试抗拉强度TS下限值 | DB注释(中文) |
| 30 | TSL_TS_MAX | NUMBER | Y |  | 拉伸测试抗拉强度TS上限值 | DB注释(中文) |
| 31 | TSL_YP_TS_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验屈强比YP/TS保证代号 | DB注释(中文) |
| 32 | TSL_YP_TS_MIN | NUMBER | Y |  | 拉伸试验屈强比YP/TS下限值 | DB注释(中文) |
| 33 | TSL_YP_TS_MAX | NUMBER | Y |  | 拉伸试验屈强比YP/TS上限值 | DB注释(中文) |
| 34 | TSL_RT05_RM_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt0.5/Rm保证代号 | DB注释(中文) |
| 35 | TSL_RT05_RM_MIN | NUMBER | Y |  | 拉伸试验屈强比Rt0.5/Rm下限值 | DB注释(中文) |
| 36 | TSL_RT05_RM_MAX | NUMBER | Y |  | 拉伸试验屈强比Rt0.5/Rm上限值 | DB注释(中文) |
| 37 | TSL_RT15_RT05_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt1.5/Rt0.5保证代号 | DB注释(中文) |
| 38 | TSL_RT15_RT05_MIN | NUMBER | Y |  | 拉伸试验屈强比Rt1.5/Rt0.5下限值 | DB注释(中文) |
| 39 | TSL_RT15_RT05_MAX | NUMBER | Y |  | 拉伸试验屈强比Rt1.5/Rt0.5上限值 | DB注释(中文) |
| 40 | TSL_RT20_RT10_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt2.0/Rt1.0保证代号 | DB注释(中文) |
| 41 | TSL_RT20_RT10_MIN | NUMBER | Y |  | 拉伸试验屈强比Rt2.0/Rt1.0下限值 | DB注释(中文) |
| 42 | TSL_RT20_RT10_MAX | NUMBER | Y |  | 拉伸试验屈强比Rt2.0/Rt1.0上限值 | DB注释(中文) |
| 43 | TSL_RT50_RT10_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt5.0/Rt1.0保证代号 | DB注释(中文) |
| 44 | TSL_RT50_RT10_MIN | NUMBER | Y |  | 拉伸试验屈强比Rt5.0/Rt1.0下限值 | DB注释(中文) |
| 45 | TSL_RT50_RT10_MAX | NUMBER | Y |  | 拉伸试验屈强比Rt5.0/Rt1.0上限值 | DB注释(中文) |
| 46 | TSL_CT_EX_RA_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试断后伸长率保证代号 | DB注释(中文) |
| 47 | TSL_CT_EX_RA_MIN | NUMBER | Y |  | 拉抻测试断后伸长率下限值 | DB注释(中文) |
| 48 | TSL_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 拉抻测试断后伸长率类型 | DB注释(中文) |
| 49 | TSL_CT_RA_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验均匀伸长率保证代号 | DB注释(中文) |
| 50 | TSL_CT_RA_MIN | NUMBER | Y |  | 拉伸试验均匀伸长率下限值 | DB注释(中文) |
| 51 | TSL_RA_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验断面收缩率保证代号 | DB注释(中文) |
| 52 | TSL_RA_MIN | NUMBER | Y |  | 拉伸试验断面收缩率下限值 | DB注释(中文) |
| 53 | IMPACT_SMP_CND | VARCHAR2(2) | Y |  | 冲击试验取样条件 | DB注释(中文) |
| 54 | IMPACT_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 冲击试验取样长度方向位置 | DB注释(中文) |
| 55 | IMPACT_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 冲击试验取样宽度方向位置 | DB注释(中文) |
| 56 | IMPACT_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 冲击试验试样方向 | DB注释(中文) |
| 57 | IMPACT_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 冲击试验取样试样尺寸 | DB注释(中文) |
| 58 | IMPACT_SMP_THK_LOC | VARCHAR2(1) | Y |  | 冲击试样厚度取样位置 | DB注释(中文) |
| 59 | IMPACT_TEMP | NUMBER | Y |  | 冲击测试温度 | DB注释(中文) |
| 60 | IMPACT_SMP_SZ | VARCHAR2(1) | Y |  | 冲击试样尺寸 | DB注释(中文) |
| 61 | IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 冲击测试缺口类型 | DB注释(中文) |
| 62 | IMPACT_ENERGY_CD | VARCHAR2(1) | Y |  | 冲击试样能量值类型 | DB注释(中文) |
| 63 | IMPACT_AVG_GRT_CD | VARCHAR2(1) | Y |  | 冲击测试保证代号 | DB注释(中文) |
| 64 | IMPACT_IND_MIN | NUMBER | Y |  | 冲击测试单值下限值 | DB注释(中文) |
| 65 | IMPACT_AVG_MIN | NUMBER | Y |  | 冲击测试平均值下限值 | DB注释(中文) |
| 66 | IMPACT_SF_RATIO_GRT_CD | VARCHAR2(1) | Y |  | 冲击测试纤维断面率保证代号 | DB注释(中文) |
| 67 | IMPACT_SF_RATIO_IND_MIN | NUMBER | Y |  | 纤维断面率单值下限值 | DB注释(中文) |
| 68 | IMPACT_SF_RATIO_AVG_MIN | NUMBER | Y |  | 纤维断面率平均值下限值 | DB注释(中文) |
| 69 | IMPACT_SMP_GRT_CD | VARCHAR2(1) | Y |  | 冲击试样侧膨胀值保证代号 | DB注释(中文) |
| 70 | IMPACT_SMP_IND_MIN | NUMBER | Y |  | 冲击试样侧膨胀值单值下限值 | DB注释(中文) |
| 71 | IMPACT_SMP_AVG_MIN | NUMBER | Y |  | 冲击试样侧膨胀值平均值下限值 | DB注释(中文) |
| 72 | IMPACT_SMP_CUT_PHOTO | VARCHAR2(1) | Y |  | 冲击试样断口照片 | DB注释(中文) |
| 73 | IMPACT_SMP_STATUS | VARCHAR2(1) | Y |  | 冲击测试试样状态 | DB注释(中文) |
| 74 | Z_TSL_SMP_CND | VARCHAR2(2) | Y |  | Z向拉伸试验取样条件 | DB注释(中文) |
| 75 | Z_TSL_SMP_LTH_LOC | VARCHAR2(1) | Y |  | Z向拉伸试验取样长度方向位置 | DB注释(中文) |
| 76 | Z_TSL_SMP_WTH_LOC | VARCHAR2(1) | Y |  | Z向拉伸试验取样宽度方向位置 | DB注释(中文) |
| 77 | Z_TSL_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | Z向拉伸试验取样试样尺寸 | DB注释(中文) |
| 78 | Z_TSL_CUT_GRT_CD | VARCHAR2(1) | Y |  | Z向拉伸断面收缩率保证代号 | DB注释(中文) |
| 79 | Z_TSL_CUT_IND_MIN | NUMBER | Y |  | Z向拉伸断面收缩率单值下限值 | DB注释(中文) |
| 80 | Z_TSL_CUT_AVG_MIN | NUMBER | Y |  | Z向拉伸断面收缩率平均值下限值 | DB注释(中文) |
| 81 | Z_TSL_YP_GRT_CD | VARCHAR2(1) | Y |  | Z向拉伸试验屈服强度保证代号 | DB注释(中文) |
| 82 | Z_TSL_YP_MIN | NUMBER | Y |  | Z向拉伸试验屈服强度下限值 | DB注释(中文) |
| 83 | Z_TSL_YP_MAX | NUMBER | Y |  | Z向拉伸试验屈服强度上限值 | DB注释(中文) |
| 84 | Z_TSL_TS_GRT_CD | VARCHAR2(1) | Y |  | Z向拉伸试验抗拉强度保证代号 | DB注释(中文) |
| 85 | Z_TSL_TS_MIN | NUMBER | Y |  | Z向拉伸试验抗拉强度下限值 | DB注释(中文) |
| 86 | Z_TSL_TS_MAX | NUMBER | Y |  | Z向拉伸试验抗拉强度上限值 | DB注释(中文) |
| 87 | Z_TSL_CT_EX_RA_GRT_CD | VARCHAR2(1) | Y |  | Z向拉伸试验断后伸长率保证代号 | DB注释(中文) |
| 88 | Z_TSL_CT_EX_RA_MIN | NUMBER | Y |  | Z向拉伸试验断后伸长率下限值 | DB注释(中文) |
| 89 | Z_TSL_SMP_CUT_PHOTO | VARCHAR2(1) | Y |  | Z向拉伸断口照片 | DB注释(中文) |
| 90 | Z_TSL_SMP_STATUS | VARCHAR2(1) | Y |  | Z向拉伸试样状态 | DB注释(中文) |
| 91 | HIGH_TEMP_TSL_SMP_CND | VARCHAR2(2) | Y |  | 高温拉伸测试取样条件 | DB注释(中文) |
| 92 | HIGH_TEMP_TSL_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 高温拉伸测试长度方向取样位置 | DB注释(中文) |
| 93 | HIGH_TEMP_TSL_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 高温拉伸测试宽度方向取样位置 | DB注释(中文) |
| 94 | HIGH_TEMP_TSL_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 高温拉伸测试取样试样方向 | DB注释(中文) |
| 95 | HIGH_TEMP_TSL_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 高温拉伸试验取样试样尺寸 | DB注释(中文) |
| 96 | HIGH_TEMP_TSL_STAND_CD | VARCHAR2(20) | Y |  | 高温拉伸测试试验标准类型 | DB注释(中文) |
| 97 | HIGH_TEMP_SMP_CD | VARCHAR2(1) | Y |  | 高温拉伸测试试样类型 | DB注释(中文) |
| 98 | HIGH_TEMP_TSL_TEMP | NUMBER | Y |  | 高温拉伸试验温度 | DB注释(中文) |
| 99 | HIGH_TEMP_TSL_TS_GRT_CD | VARCHAR2(1) | Y |  | 高温拉伸测试抗拉强度保证代号 | DB注释(中文) |
| 100 | HIGH_TEMP_TSL_TS_MIN | NUMBER | Y |  | 高温拉伸测试抗拉强度TS下限值 | DB注释(中文) |
| 101 | HIGH_TEMP_TSL_TS_MAX | NUMBER | Y |  | 高温拉伸测试抗拉强度TS上限值 | DB注释(中文) |
| 102 | HIGH_TEMP_TSL_YP_GRT_CD | VARCHAR2(1) | Y |  | 高温拉伸测试屈服强度保证代号 | DB注释(中文) |
| 103 | HIGH_TEMP_TSL_YP_MIN | NUMBER | Y |  | 高温拉伸测试屈服强度YP下限值 | DB注释(中文) |
| 104 | HIGH_TEMP_TSL_YP_MAX | NUMBER | Y |  | 高温拉伸测试屈服强度YP上限值 | DB注释(中文) |
| 105 | HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  | 高温拉伸测试屈服强度类型 | DB注释(中文) |
| 106 | HIGH_TEMP_TSL_EL_GRT_CD | VARCHAR2(1) | Y |  | 高温拉伸测试伸长率保证代号 | DB注释(中文) |
| 107 | HIGH_TEMP_TSL_EL_MIN | NUMBER | Y |  | 高温拉伸测试伸长率EL下限 | DB注释(中文) |
| 108 | HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  | 高温拉伸测试伸长率类型 | DB注释(中文) |
| 109 | HIGH_TEMP_TSL_RA_GRT_CD | VARCHAR2(1) | Y |  | 高温拉伸断面收缩率保证代号 | DB注释(中文) |
| 110 | HIGH_TEMP_TSL_RA_MIN | NUMBER | Y |  | 高温拉伸断面收缩率Z下限值 | DB注释(中文) |
| 111 | HIGH_TEMP_SMP_STATUS | VARCHAR2(1) | Y |  | 高温拉伸试样状态 | DB注释(中文) |
| 112 | PWHT_WARM_GRT_CD | VARCHAR2(1) | Y |  | 模拟焊后热处理试验保证代号 | DB注释(中文) |
| 113 | PWHT_WARM_TEMP_MIN | NUMBER | Y |  | 模拟焊后热处理试验保温温度下限值 | DB注释(中文) |
| 114 | PWHT_WARM_TEMP_MAX | NUMBER | Y |  | 模拟焊后热处理试验保温温度上限值 | DB注释(中文) |
| 115 | PWHT_WARM_TIME_MIN | NUMBER | Y |  | 模拟焊后热处理试验保温时间下限值 | DB注释(中文) |
| 116 | PWHT_WARM_TIME_MAX | NUMBER | Y |  | 模拟焊后热处理试验保温时间上限值 | DB注释(中文) |
| 117 | PWHT_WARM_HEAT_RATE_MIN | NUMBER | Y |  | 模拟焊后热处理试验升温速率下限值 | DB注释(中文) |
| 118 | PWHT_WARM_HEAT_RATE_MAX | NUMBER | Y |  | 模拟焊后热处理试验升温速率上限值 | DB注释(中文) |
| 119 | PWHT_WARM_DEGR_RATE_MIN | NUMBER | Y |  | 模拟焊后热处理试验降温速率下限值 | DB注释(中文) |
| 120 | PWHT_WARM_DEGR_RATE_MAX | NUMBER | Y |  | 模拟焊后热处理试验降温速率上限值 | DB注释(中文) |
| 121 | MAX_PWHT_WARM_GRT_CD | VARCHAR2(1) | Y |  | 最大模拟焊后热处理试验保证代号 | DB注释(中文) |
| 122 | MAX_PWHT_WARM_TEMP_MIN | NUMBER | Y |  | 最大模拟焊后热处理试验保温温度下限值 | DB注释(中文) |
| 123 | MAX_PWHT_WARM_TEMP_MAX | NUMBER | Y |  | 最大模拟焊后热处理试验保温温度上限值 | DB注释(中文) |
| 124 | MAX_PWHT_WARM_TIME_MIN | NUMBER | Y |  | 最大模拟焊后热处理试验保温时间下限值 | DB注释(中文) |
| 125 | MAX_PWHT_WARM_TIME_MAX | NUMBER | Y |  | 最大模拟焊后热处理试验保温时间上限值 | DB注释(中文) |
| 126 | MAX_PWHT_WARM_HEAT_RATE_MIN | NUMBER | Y |  | 最大模拟焊后热处理试验升温速率下限值 | DB注释(中文) |
| 127 | MAX_PWHT_WARM_HEAT_RATE_MAX | NUMBER | Y |  | 最大模拟焊后热处理试验升温速率上限值 | DB注释(中文) |
| 128 | MAX_PWHT_WARM_DEGR_RATE_MIN | NUMBER | Y |  | 最大模拟焊后热处理试验降温速率下限值 | DB注释(中文) |
| 129 | MAX_PWHT_WARM_DEGR_RATE_MAX | NUMBER | Y |  | 最大模拟焊后热处理试验降温速率上限值 | DB注释(中文) |
| 130 | MIN_PWHT_WARM_GRT_CD | VARCHAR2(1) | Y |  | 最小模拟焊后热处理试验保证代号 | DB注释(中文) |
| 131 | MIN_PWHT_WARM_TEMP_MIN | NUMBER | Y |  | 最小模拟焊后热处理试验保温温度下限值 | DB注释(中文) |
| 132 | MIN_PWHT_WARM_TEMP_MAX | NUMBER | Y |  | 最小模拟焊后热处理试验保温温度上限值 | DB注释(中文) |
| 133 | MIN_PWHT_WARM_TIME_MIN | NUMBER | Y |  | 最小模拟焊后热处理试验保温时间下限值 | DB注释(中文) |
| 134 | MIN_PWHT_WARM_TIME_MAX | NUMBER | Y |  | 最小模拟焊后热处理试验保温时间上限值 | DB注释(中文) |
| 135 | MIN_PWHT_WARM_HEAT_RATE_MIN | NUMBER | Y |  | 最小模拟焊后热处理试验升温速率下限值 | DB注释(中文) |
| 136 | MIN_PWHT_WARM_HEAT_RATE_MAX | NUMBER | Y |  | 最小模拟焊后热处理试验升温速率上限值 | DB注释(中文) |
| 137 | MIN_PWHT_WARM_DEGR_RATE_MIN | NUMBER | Y |  | 最小模拟焊后热处理试验降温速率下限值 | DB注释(中文) |
| 138 | MIN_PWHT_WARM_DEGR_RATE_MAX | NUMBER | Y |  | 最小模拟焊后热处理试验降温速率上限值 | DB注释(中文) |
| 139 | DWTT_SMP_CND | VARCHAR2(2) | Y |  | DWTT测试取样条件 | DB注释(中文) |
| 140 | DWTT_SMP_LTH_LOC | VARCHAR2(1) | Y |  | DWTT测试长度方向取样位置 | DB注释(中文) |
| 141 | DWTT_SMP_WTH_LOC | VARCHAR2(1) | Y |  | DWTT测试宽度方向取样位置 | DB注释(中文) |
| 142 | DWTT_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | DWTT测试取样试样方向 | DB注释(中文) |
| 143 | DWTT_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | DWTT取样试样尺寸 | DB注释(中文) |
| 144 | DWTT_CREAK_CD | VARCHAR2(1) | Y |  | DWTT测试缺口类型 | DB注释(中文) |
| 145 | DWTT_TEMP | NUMBER | Y |  | DWTT测试温度 | DB注释(中文) |
| 146 | DWTT1_SA_RATIO_GRT_CD | VARCHAR2(1) | Y |  | DWTT纤维断面率SA保证代号_1 | DB注释(中文) |
| 147 | DWTT1_SMP_LTH_LOC | VARCHAR2(1) | Y |  | DWTT测试长度方向取样位置_1 | DB注释(中文) |
| 148 | DWTT1_SA_RATIO_IND_MIN | NUMBER | Y |  | DWTT纤维断面率SA单值下限_1 | DB注释(中文) |
| 149 | DWTT1_SA_RATIO_AVG_MIN | NUMBER | Y |  | DWTT纤维断面率SA平均值下限_1 | DB注释(中文) |
| 150 | DWTT2_SA_RATIO_GRT_CD | VARCHAR2(1) | Y |  | DWTT纤维断面率SA保证代号_2 | DB注释(中文) |
| 151 | DWTT2_SMP_LTH_LOC | VARCHAR2(1) | Y |  | DWTT测试长度方向取样位置_2 | DB注释(中文) |
| 152 | DWTT2_SA_RATIO_IND_MIN | NUMBER | Y |  | DWTT纤维断面率SA单值下限_2 | DB注释(中文) |
| 153 | DWTT2_SA_RATIO_AVG_MIN | NUMBER | Y |  | DWTT纤维断面率SA平均值下限_2 | DB注释(中文) |
| 154 | DWTT3_SA_RATIO_GRT_CD | VARCHAR2(1) | Y |  | DWTT纤维断面率SA保证代号_3 | DB注释(中文) |
| 155 | DWTT3_SMP_LTH_LOC | VARCHAR2(1) | Y |  | DWTT测试长度方向取样位置_3 | DB注释(中文) |
| 156 | DWTT3_SA_RATIO_IND_MIN | NUMBER | Y |  | DWTT纤维断面率SA单值下限_3 | DB注释(中文) |
| 157 | DWTT3_SA_RATIO_AVG_MIN | NUMBER | Y |  | DWTT纤维断面率SA平均值下限_3 | DB注释(中文) |
| 158 | SSCC_SMP_CND | VARCHAR2(2) | Y |  | SSCC测试取样条件 | DB注释(中文) |
| 159 | SSCC_SMP_LTH_LOC | VARCHAR2(1) | Y |  | SSCC测试长度方向取样位置 | DB注释(中文) |
| 160 | SSCC_SMP_WTH_LOC | VARCHAR2(1) | Y |  | SSCC测试宽度方向取样位置 | DB注释(中文) |
| 161 | SSCC_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | SSCC测试取样试样方向 | DB注释(中文) |
| 162 | SSCC_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | SSCC检验取样试样尺寸 | DB注释(中文) |
| 163 | SSCC_GRT_CD | VARCHAR2(1) | Y |  | SSCC测试保证代号 | DB注释(中文) |
| 164 | SSCC_STRESS_TY | VARCHAR2(1) | Y |  | SSCC测试应力区分 | DB注释(中文) |
| 165 | SSCC_STRESS_TST_VAL | NUMBER | Y |  | SSCC测试应力 | DB注释(中文) |
| 166 | SSCC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  | SSCC执行标准 | DB注释(中文) |
| 167 | SSCC_SOLUTION_KIND | VARCHAR2(20) | Y |  | SSCC测试溶液种类 | DB注释(中文) |
| 168 | SSCC_SMP_STATUS | VARCHAR2(1) | Y |  | SSCC试验试样状态 | DB注释(中文) |
| 169 | HIC_SMP_CND | VARCHAR2(2) | Y |  | HIC测试取样条件 | DB注释(中文) |
| 170 | HIC_SMP_LTH_LOC | VARCHAR2(1) | Y |  | HIC测试长度方向取样位置 | DB注释(中文) |
| 171 | HIC_SMP_WTH_LOC | VARCHAR2(1) | Y |  | HIC测试宽度方向取样位置 | DB注释(中文) |
| 172 | HIC_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | HIC测试取样测试方向 | DB注释(中文) |
| 173 | HIC_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | HIC检验取样试样尺寸 | DB注释(中文) |
| 174 | HIC_CLR_GRT_CD | VARCHAR2(1) | Y |  | HIC测试CLR保证代号 | DB注释(中文) |
| 175 | HIC_CLR_EACH_MAX | NUMBER | Y |  | HIC裂纹长度率CLR单个上限值 | DB注释(中文) |
| 176 | HIC_CLR_SPCMN_AVG_MAX | NUMBER | Y |  | HIC裂纹长度率CLR平均上限值 | DB注释(中文) |
| 177 | HIC_CLR_TOT_AVG_MAX | NUMBER | Y |  | HIC裂纹长度率CLR全部平均上限值 | DB注释(中文) |
| 178 | HIC_CTR_GRT_CD | VARCHAR2(1) | Y |  | HIC测试CTR保证代号 | DB注释(中文) |
| 179 | HIC_CTR_EACH_MAX | NUMBER | Y |  | HIC裂纹厚度率CTR单个上限值 | DB注释(中文) |
| 180 | HIC_CTR_SPCMN_AVG_MAX | NUMBER | Y |  | HIC裂纹厚度率CTR平均上限值 | DB注释(中文) |
| 181 | HIC_CTR_TOT_AVG_MAX | NUMBER | Y |  | HIC裂纹厚度率CTR全部平均上限值 | DB注释(中文) |
| 182 | HIC_CSR_GRT_CD | VARCHAR2(1) | Y |  | HIC测试CSR保证代号 | DB注释(中文) |
| 183 | HIC_CSR_EACH_MAX | NUMBER | Y |  | HIC裂纹敏感率CSR单个上限值 | DB注释(中文) |
| 184 | HIC_CSR_SPCMN_AVG_MAX | NUMBER | Y |  | HIC裂纹敏感率CSR平均上限值 | DB注释(中文) |
| 185 | HIC_CSR_TOT_AVG_MAX | NUMBER | Y |  | HIC裂纹敏感率CSR全部平均上限值 | DB注释(中文) |
| 186 | HIC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  | 执行标准 | DB注释(中文) |
| 187 | HIC_SOLUTION_KIND | VARCHAR2(20) | Y |  | HIC测试溶液种类 | DB注释(中文) |
| 188 | HIC_SMP_STATUS | VARCHAR2(1) | Y |  | HIC试验试样状态 | DB注释(中文) |
| 189 | MGRPHY_SMP_CND | VARCHAR2(2) | Y |  | 金相测试取样条件 | DB注释(中文) |
| 190 | MGRPHY_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 金相测试长度方向取样位置 | DB注释(中文) |
| 191 | MGRPHY_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 金相测试宽度方向取样位置 | DB注释(中文) |
| 192 | MGRPHY_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 金相测试取样试样方向 | DB注释(中文) |
| 193 | MGRPHY_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 金相显微组织取样试样尺寸 | DB注释(中文) |
| 194 | MGRPHY_SMP_THK_LOC | VARCHAR2(1) | Y |  | 金相厚度位置 | DB注释(中文) |
| 195 | MGRPHY_MTLGRP_TY | VARCHAR2(8) | Y |  | 组织类型 | DB注释(中文) |
| 196 | MGRPHY_BAND_STRC_GRT_CD | VARCHAR2(1) | Y |  | 带状组织级别保证代号 | DB注释(中文) |
| 197 | MGRPHY_BAND_STRC_GRD_MAX | NUMBER | Y |  | 带状组织级别上限值 | DB注释(中文) |
| 198 | MGRPHY_FGS_GRT_CD | VARCHAR2(1) | Y |  | 铁素体晶粒度保证代号 | DB注释(中文) |
| 199 | MGRPHY_FGS_MIN | NUMBER | Y |  | 铁素体晶粒度下限值 | DB注释(中文) |
| 200 | MGRPHY_FGS_MAX | NUMBER | Y |  | 铁素体晶粒度上限值 | DB注释(中文) |
| 201 | MGRPHY_AGS_GRT_CD | VARCHAR2(1) | Y |  | 奥氏体晶粒度保证代号 | DB注释(中文) |
| 202 | MGRPHY_AGS_MIN | NUMBER | Y |  | 奥氏体晶粒度下限值 | DB注释(中文) |
| 203 | MGRPHY_AGS_MAX | NUMBER | Y |  | 奥氏体晶粒度上限值 | DB注释(中文) |
| 204 | MGRPHY_GRNSZ_OCCP_GRT_CD | VARCHAR2(1) | Y |  | 金相测试基相的体积分数保证代号 | DB注释(中文) |
| 205 | MGRPHY_GRNSZ_OCCP_MIN | NUMBER | Y |  | 金相测试基相的体积分数下限值 | DB注释(中文) |
| 206 | MGRPHY_GRNSZ_OCCP_MAX | NUMBER | Y |  | 金相测试基相的体积分数上限值 | DB注释(中文) |
| 207 | MGRPHY_PHOTO_PROVIDE | VARCHAR2(1) | Y |  | 提供照片 | DB注释(中文) |
| 208 | MGRPHY_PHOTO_EXP_RATE | VARCHAR2(1) | Y |  | 照片放大倍数 | DB注释(中文) |
| 209 | MGRPHY_SMP_STATUS | VARCHAR2(1) | Y |  | 金相检验试样状态 | DB注释(中文) |
| 210 | NON_METAL_SMP_CND | VARCHAR2(2) | Y |  | 非金属夹杂物测试取样条件 | DB注释(中文) |
| 211 | NON_METAL_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 非金属夹杂物测试长度方向取样位置 | DB注释(中文) |
| 212 | NON_METAL_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 非金属夹杂物测试宽度方向取样位置 | DB注释(中文) |
| 213 | NON_METAL_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 非金属夹杂物测试取样试样方向 | DB注释(中文) |
| 214 | NON_METAL_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 夹杂物级别取样试样尺寸 | DB注释(中文) |
| 215 | NON_METAL_GRD_SPEC | VARCHAR2(20) | Y |  | 非金属夹杂评级标准 | DB注释(中文) |
| 216 | NON_METAL_KIND_CD | VARCHAR2(1) | Y |  | 非金属夹杂物类别 | DB注释(中文) |
| 217 | NON_METAL_A_GRP_GRT_CD | VARCHAR2(1) | Y |  | 夹杂物类别_A类 保证代号 | DB注释(中文) |
| 218 | NON_METAL_A_GRP_MAX | NUMBER | Y |  | 夹杂物类别_A类（粗系）上限 | DB注释(中文) |
| 219 | NON_METAL_A_DETAIL_MAX | NUMBER | Y |  | 夹杂物类别_A类（细系）上限 | DB注释(中文) |
| 220 | NON_METAL_A_MAX | NUMBER | Y |  | 夹杂物类别_A类上限 | DB注释(中文) |
| 221 | NON_METAL_B_GRP_GRT_CD | VARCHAR2(1) | Y |  | 夹杂物类别_B类 保证代号 | DB注释(中文) |
| 222 | NON_METAL_B_GRP_MAX | NUMBER | Y |  | 夹杂物类别_B类（粗系）上限 | DB注释(中文) |
| 223 | NON_METAL_B_DETAIL_MAX | NUMBER | Y |  | 夹杂物类别_B类（细系）上限 | DB注释(中文) |
| 224 | NON_METAL_B_MAX | NUMBER | Y |  | 夹杂物类别_B类上限 | DB注释(中文) |
| 225 | NON_METAL_C_GRP_GRT_CD | VARCHAR2(1) | Y |  | 夹杂物类别_C类 保证代号 | DB注释(中文) |
| 226 | NON_METAL_C_GRP_MAX | NUMBER | Y |  | 夹杂物类别_C类（粗系）上限 | DB注释(中文) |
| 227 | NON_METAL_C_DETAIL_MAX | NUMBER | Y |  | 夹杂物类别_C类（细系）上限 | DB注释(中文) |
| 228 | NON_METAL_C_MAX | NUMBER | Y |  | 夹杂物类别_C类上限 | DB注释(中文) |
| 229 | NON_METAL_D_GRP_GRT_CD | VARCHAR2(1) | Y |  | 夹杂物类别_D类 保证代号 | DB注释(中文) |
| 230 | NON_METAL_D_GRP_MAX | NUMBER | Y |  | 夹杂物类别_D类（粗系）上限 | DB注释(中文) |
| 231 | NON_METAL_D_DETAIL_MAX | NUMBER | Y |  | 夹杂物类别_D类（细系）上限 | DB注释(中文) |
| 232 | NON_METAL_D_MAX | NUMBER | Y |  | 夹杂物类别_D类上限 | DB注释(中文) |
| 233 | NON_METAL_DS_GRT_CD | VARCHAR2(1) | Y |  | 夹杂物类别_DS类保证代号 | DB注释(中文) |
| 234 | NON_METAL_DS_MAX | NUMBER | Y |  | 夹杂物类别_DS类上限 | DB注释(中文) |
| 235 | NON_METAL_ABCD_GRT_CD | VARCHAR2(1) | Y |  | 夹杂物类别_A+B+C+D保证代号 | DB注释(中文) |
| 236 | NON_METAL_ABCD_MAX | NUMBER | Y |  | 夹杂物类别_A+B+C+D上限 | DB注释(中文) |
| 237 | NON_METAL_AC_GRT_CD | VARCHAR2(1) | Y |  | 夹杂物类别_A+C保证代号 | DB注释(中文) |
| 238 | NON_METAL_AC_MAX | NUMBER | Y |  | 夹杂物类别_A+C上限 | DB注释(中文) |
| 239 | NON_METAL_BDDS_GRT_CD | VARCHAR2(1) | Y |  | 夹杂物类别_B+D+Ds保证代号 | DB注释(中文) |
| 240 | NON_METAL_BDDS_MAX | NUMBER | Y |  | 夹杂物类别_B+D+Ds上限 | DB注释(中文) |
| 241 | BEND_SMP_CND | VARCHAR2(2) | Y |  | 弯曲测试取样条件 | DB注释(中文) |
| 242 | BEND_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 弯曲测试长度方向取样位置 | DB注释(中文) |
| 243 | BEND_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 弯曲测试宽度方向取样位置 | DB注释(中文) |
| 244 | BEND_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 弯曲测试取样试样方向 | DB注释(中文) |
| 245 | BEND_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 弯曲试验取样试样尺寸 | DB注释(中文) |
| 246 | BEND_GRT_CD | VARCHAR2(1) | Y |  | 弯曲测试保证代号 | DB注释(中文) |
| 247 | BEND_DIA | NUMBER | Y |  | 弯曲压头直径D | DB注释(中文) |
| 248 | BEND_ANGLE | NUMBER | Y |  | 弯曲角度 | DB注释(中文) |
| 249 | BEND_SMP_WTH | VARCHAR2(7) | Y |  | 试样宽度 | DB注释(中文) |
| 250 | BEND_SMP_PHOTO | VARCHAR2(1) | Y |  | 弯曲试样照片 | DB注释(中文) |
| 251 | BEND_SMP_STATUS | VARCHAR2(1) | Y |  | 弯曲试验试样状态 | DB注释(中文) |
| 252 | CPLATE_SMP_CND | VARCHAR2(2) | Y |  | 复合板指标试验取样条件 | DB注释(中文) |
| 253 | CPLATE_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 复合板指标试验取样长度方向位置 | DB注释(中文) |
| 254 | CPLATE_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 复合板指标试验取样宽度方向位置 | DB注释(中文) |
| 255 | CPLATE_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 复合板指标试验试样方向 | DB注释(中文) |
| 256 | CPLATE_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 复合板指标试验取样试样尺寸 | DB注释(中文) |
| 257 | CPLATE_CUT_STRESS_GRT_CD | VARCHAR2(1) | Y |  | 抗剪强度τ保证代号 | DB注释(中文) |
| 258 | CPLATE_CUT_STRESS_MIN | NUMBER | Y |  | 抗剪强度τ下限值 | DB注释(中文) |
| 259 | CPLATE_THK_GRT_CD | VARCHAR2(1) | Y |  | 复层厚度保证代号 | DB注释(中文) |
| 260 | CPLATE_THK_MIN | NUMBER | Y |  | 复层厚度下限值 | DB注释(中文) |
| 261 | CPLATE_THK_MAX | NUMBER | Y |  | 复层厚度上限值 | DB注释(中文) |
| 262 | CPLATE_ER_GRT_CD | VARCHAR2(1) | Y |  | 杯突IE保证代号 | DB注释(中文) |
| 263 | CPLATE_ER_IE_MIN | NUMBER | Y |  | 杯突IE下限值 | DB注释(中文) |
| 264 | CPLATE_ER_IE_AIM | NUMBER | Y |  | 杯突IE目标值 | DB注释(中文) |
| 265 | HARD_SMP_CND | VARCHAR2(2) | Y |  | 硬度测试取样条件 | DB注释(中文) |
| 266 | HARD_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 硬度测试长度方向取样位置 | DB注释(中文) |
| 267 | HARD_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 硬度测试宽度方向取样位置 | DB注释(中文) |
| 268 | HARD_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 硬度测试取样试样方向 | DB注释(中文) |
| 269 | HARD_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 硬度测试取样试样尺寸 | DB注释(中文) |
| 270 | HARD_KIND | VARCHAR2(1) | Y |  | 硬度测试种类 | DB注释(中文) |
| 271 | HARD_IND_GRT_CD | VARCHAR2(1) | Y |  | 硬度单值保证代号 | DB注释(中文) |
| 272 | HARD_IND_MIN | NUMBER | Y |  | 硬度单值最小值 | DB注释(中文) |
| 273 | HARD_IND_MAX | NUMBER | Y |  | 硬度单值最大值 | DB注释(中文) |
| 274 | HARD_AVG_GRT_CD | VARCHAR2(1) | Y |  | 硬度平均保证代号 | DB注释(中文) |
| 275 | HARD_AVG_MIN | NUMBER | Y |  | 硬度平均最小值 | DB注释(中文) |
| 276 | HARD_AVG_MAX | NUMBER | Y |  | 硬度平均最大值 | DB注释(中文) |
| 277 | HARD_SMP_STATUS | VARCHAR2(1) | Y |  | 硬度试验试样状态 | DB注释(中文) |
| 278 | S_PRINT_SMP_CND | VARCHAR2(2) | Y |  | 硫印测试取样条件 | DB注释(中文) |
| 279 | S_PRINT_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 硫印测试长度方向取样位置 | DB注释(中文) |
| 280 | S_PRINT_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 硫印测试宽度方向取样位置 | DB注释(中文) |
| 281 | S_PRINT_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 硫印测试取样试样方向 | DB注释(中文) |
| 282 | S_PRINT_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 硫印测试取样试样尺寸 | DB注释(中文) |
| 283 | S_PRINT_GRT_CD | VARCHAR2(1) | Y |  | 硫印测试保证代号 | DB注释(中文) |
| 284 | S_PRINT_KIND | VARCHAR2(10) | Y |  | 硫印测试种类 | DB注释(中文) |
| 285 | S_PRINT_CUT_PHOTO | VARCHAR2(1) | Y |  | 硫印测试上限 | DB注释(中文) |
| 286 | AGE_TST_SMP_CND | VARCHAR2(2) | Y |  | 效检验取样条件 | DB注释(中文) |
| 287 | AGE_TST_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 时效检验取样长度方向位置 | DB注释(中文) |
| 288 | AGE_TST_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 时效检验取样宽度方向位置 | DB注释(中文) |
| 289 | AGE_TST_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 时效检验试样方向 | DB注释(中文) |
| 290 | AGE_TST_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 效检验取样试样尺寸 | DB注释(中文) |
| 291 | AGE_TST_SMP_THK_LOC | VARCHAR2(1) | Y |  | 时效冲击试样厚度取样位置 | DB注释(中文) |
| 292 | AGE_TST_STRESS | NUMBER | Y |  | 时效预应变量 | DB注释(中文) |
| 293 | AGE_TST_AGE_TIME | NUMBER | Y |  | 时效温度 | DB注释(中文) |
| 294 | AGE_TST_AGE_TEMP | NUMBER | Y |  | 保温时间 | DB注释(中文) |
| 295 | AGE_TST_YP_GRT_CD | VARCHAR2(1) | Y |  | 时效拉伸测试屈服强度保证代号(YP) | DB注释(中文) |
| 296 | AGE_TST_YP_MIN | NUMBER | Y |  | 时效拉伸测试屈服强度YP下限 | DB注释(中文) |
| 297 | AGE_TST_YP_MAX | NUMBER | Y |  | 时效拉伸测试屈服强度YP上限 | DB注释(中文) |
| 298 | AGE_TST_YP_CD | VARCHAR2(1) | Y |  | 时效拉伸测试屈服强度类型 | DB注释(中文) |
| 299 | AGE_TST_TS_GRT_CD | VARCHAR2(1) | Y |  | 时效拉伸测试抗拉强度保证代号(TS) | DB注释(中文) |
| 300 | AGE_TST_TS_MIN | NUMBER | Y |  | 时效拉伸测试抗拉强度TS下限 | DB注释(中文) |
| 301 | AGE_TST_TS_MAX | NUMBER | Y |  | 时效拉伸测试抗拉强度TS上限 | DB注释(中文) |
| 302 | AGE_TST_YP_TS_GRT_CD | VARCHAR2(1) | Y |  | 时效检验屈强比YP/TS保证代号 | DB注释(中文) |
| 303 | AGE_TST_YP_TS_MIN | NUMBER | Y |  | 时效检验屈强比YP/TS下限值 | DB注释(中文) |
| 304 | AGE_TST_YP_TS_MAX | NUMBER | Y |  | 时效检验屈强比YP/TS上限值 | DB注释(中文) |
| 305 | AGE_TST_RT05_RM_GRT_CD | VARCHAR2(1) | Y |  | 时效检验屈强比Rt0.5/Rm保证代号 | DB注释(中文) |
| 306 | AGE_TST_RT05_RM_MIN | NUMBER | Y |  | 时效检验屈强比Rt0.5/Rm下限值 | DB注释(中文) |
| 307 | AGE_TST_RT05_RM_MAX | NUMBER | Y |  | 时效检验屈强比Rt0.5/Rm上限值 | DB注释(中文) |
| 308 | AGE_TST_RT15_RT05_GRT_CD | VARCHAR2(1) | Y |  | 时效试验屈强比Rt1.5/Rt0.5保证代号 | DB注释(中文) |
| 309 | AGE_TST_RT15_RT05_MIN | NUMBER | Y |  | 时效检验屈强比Rt1.5/Rt0.5下限值 | DB注释(中文) |
| 310 | AGE_TST_RT15_RT05_MAX | NUMBER | Y |  | 时效检验屈强比Rt1.5/Rt0.5上限值 | DB注释(中文) |
| 311 | AGE_TST_RT20_RT10_GRT_CD | VARCHAR2(1) | Y |  | 时效试验屈强比Rt2.0/Rt1.0保证代号 | DB注释(中文) |
| 312 | AGE_TST_RT20_RT10_MIN | NUMBER | Y |  | 时效检验屈强比Rt2.0/Rt1.0下限值 | DB注释(中文) |
| 313 | AGE_TST_RT20_RT10_MAX | NUMBER | Y |  | 时效检验屈强比Rt2.0/Rt1.0上限值 | DB注释(中文) |
| 314 | AGE_TST_RT50_RT10_GRT_CD | VARCHAR2(1) | Y |  | 时效试验屈强比Rt5.0/Rt1.0保证代号 | DB注释(中文) |
| 315 | AGE_TST_RT50_RT10_MIN | NUMBER | Y |  | 时效检验屈强比Rt5.0/Rt1.0下限值 | DB注释(中文) |
| 316 | AGE_TST_RT50_RT10_MAX | NUMBER | Y |  | 时效检验屈强比Rt5.0/Rt1.0上限值 | DB注释(中文) |
| 317 | AGE_TST_CT_EX_RA_GRT_CD | VARCHAR2(1) | Y |  | 时效拉抻测试断后伸长率保证代号 | DB注释(中文) |
| 318 | AGE_TST_CT_EX_RA_MIN | NUMBER | Y |  | 时效拉伸测试延伸率EL下限 | DB注释(中文) |
| 319 | AGE_TST_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 时效拉抻测试延伸率类型(EL) | DB注释(中文) |
| 320 | AGE_TST_CT_RA_GRT_CD | VARCHAR2(1) | Y |  | 时效拉伸试验均匀伸长率保证代号 | DB注释(中文) |
| 321 | AGE_TST_CT_RA_MIN | NUMBER | Y |  | 时效均匀伸长率下限值 | DB注释(中文) |
| 322 | AGE_TST_RA_GRT_CD | VARCHAR2(1) | Y |  | 时效拉伸试验断面收缩率保证代号 | DB注释(中文) |
| 323 | AGE_TST_RA_MIN | NUMBER | Y |  | 时效拉伸断面收缩率下限值 | DB注释(中文) |
| 324 | AGE_TST_SMP_CD | VARCHAR2(1) | Y |  | 时效拉伸试样类型 | DB注释(中文) |
| 325 | AGE_TST1_TEMP | NUMBER | Y |  | 时效冲击1测试温度 | DB注释(中文) |
| 326 | AGE_TST1_SMP_SZ | VARCHAR2(1) | Y |  | 时效冲击1试样尺寸 | DB注释(中文) |
| 327 | AGE_TST1_CREAK_CD | VARCHAR2(1) | Y |  | 时效冲击1测试缺口类型 | DB注释(中文) |
| 328 | AGE_TST1_SPCMN_DIR | VARCHAR2(1) | Y |  | 时效冲击1试样方向 | DB注释(中文) |
| 329 | AGE_TST1_GRT_CD | VARCHAR2(1) | Y |  | 时效冲击1测试保证代号 | DB注释(中文) |
| 330 | AGE_TST1_IND_MIN | NUMBER | Y |  | 时效冲击1测试单值下限 | DB注释(中文) |
| 331 | AGE_TST1_AVG_MIN | NUMBER | Y |  | 时效冲击1测试平均值下限 | DB注释(中文) |
| 332 | AGE_TST1_SMP_GRT_CD | VARCHAR2(1) | Y |  | 时效冲击1纤维断面率保证代号 | DB注释(中文) |
| 333 | AGE_TST1_SMP_IND_MIN | NUMBER | Y |  | 时效冲击1纤维断面率单值下限 | DB注释(中文) |
| 334 | AGE_TST1_SMP_AVG_MIN | NUMBER | Y |  | 时效冲击1纤维断面率平均值下限 | DB注释(中文) |
| 335 | AGE_TST1_SIDE_EXP_GRT_CD | VARCHAR2(1) | Y |  | 时效冲击1侧膨胀量保证代号 | DB注释(中文) |
| 336 | AGE_TST1_SIDE_EXP_MIN | NUMBER | Y |  | 时效冲击1侧膨胀量下限 | DB注释(中文) |
| 337 | AGE_TST2_TEMP | NUMBER | Y |  | 时效冲击2测试温度 | DB注释(中文) |
| 338 | AGE_TST2_SMP_SZ | VARCHAR2(1) | Y |  | 时效冲击2试样尺寸 | DB注释(中文) |
| 339 | AGE_TST2_CREAK_CD | VARCHAR2(1) | Y |  | 时效冲击2测试缺口类型 | DB注释(中文) |
| 340 | AGE_TST2_SPCMN_DIR | VARCHAR2(1) | Y |  | 时效冲击2试样方向 | DB注释(中文) |
| 341 | AGE_TST2_GRT_CD | VARCHAR2(1) | Y |  | 时效冲击2测试保证代号 | DB注释(中文) |
| 342 | AGE_TST2_IND_MIN | NUMBER | Y |  | 时效冲击2测试单值下限 | DB注释(中文) |
| 343 | AGE_TST2_AVG_MIN | NUMBER | Y |  | 时效冲击2测试平均值下限 | DB注释(中文) |
| 344 | AGE_TST2_SMP_GRT_CD | VARCHAR2(1) | Y |  | 时效冲击2纤维断面率保证代号 | DB注释(中文) |
| 345 | AGE_TST2_SMP_IND_MIN | NUMBER | Y |  | 时效冲击2纤维断面率单值下限 | DB注释(中文) |
| 346 | AGE_TST2_SMP_AVG_MIN | NUMBER | Y |  | 时效冲击2纤维断面率平均值下限 | DB注释(中文) |
| 347 | AGE_TST2_SIDE_EXP_GRT_CD | VARCHAR2(1) | Y |  | 时效冲击2侧膨胀量保证代号 | DB注释(中文) |
| 348 | AGE_TST2_SIDE_EXP_MIN | NUMBER | Y |  | 时效冲击2侧膨胀量下限 | DB注释(中文) |
| 349 | AGE_TST3_TEMP | NUMBER | Y |  | 时效冲击3测试温度 | DB注释(中文) |
| 350 | AGE_TST3_SMP_SZ | VARCHAR2(1) | Y |  | 时效冲击3试样尺寸 | DB注释(中文) |
| 351 | AGE_TST3_CREAK_CD | VARCHAR2(1) | Y |  | 时效冲击3测试缺口类型 | DB注释(中文) |
| 352 | AGE_TST3_SPCMN_DIR | VARCHAR2(1) | Y |  | 时效冲击3试样方向 | DB注释(中文) |
| 353 | AGE_TST3_GRT_CD | VARCHAR2(1) | Y |  | 时效冲击3测试保证代号 | DB注释(中文) |
| 354 | AGE_TST3_IND_MIN | NUMBER | Y |  | 时效冲击3测试单值下限 | DB注释(中文) |
| 355 | AGE_TST3_AVG_MIN | NUMBER | Y |  | 时效冲击3测试平均值下限 | DB注释(中文) |
| 356 | AGE_TST3_SMP_GRT_CD | VARCHAR2(1) | Y |  | 时效冲击3纤维断面率保证代号 | DB注释(中文) |
| 357 | AGE_TST3_SMP_IND_MIN | NUMBER | Y |  | 时效冲击3纤维断面率单值下限 | DB注释(中文) |
| 358 | AGE_TST3_SMP_AVG_MIN | NUMBER | Y |  | 时效冲击3纤维断面率平均值下限 | DB注释(中文) |
| 359 | AGE_TST3_SIDE_EXP_GRT_CD | VARCHAR2(1) | Y |  | 时效冲击3侧膨胀量保证代号 | DB注释(中文) |
| 360 | AGE_TST3_SIDE_EXP_MIN | NUMBER | Y |  | 时效冲击3侧膨胀量下限 | DB注释(中文) |
| 361 | AGE_TST4_TEMP | NUMBER | Y |  | 时效冲击4测试温度 | DB注释(中文) |
| 362 | AGE_TST4_SMP_SZ | VARCHAR2(1) | Y |  | 时效冲击4试样尺寸 | DB注释(中文) |
| 363 | AGE_TST4_CREAK_CD | VARCHAR2(1) | Y |  | 时效冲击4测试缺口类型 | DB注释(中文) |
| 364 | AGE_TST4_SPCMN_DIR | VARCHAR2(1) | Y |  | 时效冲击4试样方向 | DB注释(中文) |
| 365 | AGE_TST4_GRT_CD | VARCHAR2(1) | Y |  | 时效冲击4测试保证代号 | DB注释(中文) |
| 366 | AGE_TST4_IND_MIN | NUMBER | Y |  | 时效冲击4测试单值下限 | DB注释(中文) |
| 367 | AGE_TST4_AVG_MIN | NUMBER | Y |  | 时效冲击4测试平均值下限 | DB注释(中文) |
| 368 | AGE_TST4_SMP_GRT_CD | VARCHAR2(1) | Y |  | 时效冲击4纤维断面率保证代号 | DB注释(中文) |
| 369 | AGE_TST4_SMP_IND_MIN | NUMBER | Y |  | 时效冲击4纤维断面率单值下限 | DB注释(中文) |
| 370 | AGE_TST4_SMP_AVG_MIN | NUMBER | Y |  | 时效冲击4纤维断面率平均值下限 | DB注释(中文) |
| 371 | AGE_TST4_SIDE_EXP_GRT_CD | VARCHAR2(1) | Y |  | 时效冲击4侧膨胀量保证代号 | DB注释(中文) |
| 372 | AGE_TST4_SIDE_EXP_MIN | NUMBER | Y |  | 时效冲击4侧膨胀量下限 | DB注释(中文) |
| 373 | NDT_SMP_CND | VARCHAR2(2) | Y |  | NDT取样条件 | DB注释(中文) |
| 374 | NDT_SMP_LTH_LOC | VARCHAR2(1) | Y |  | NDT取样长度方向位置 | DB注释(中文) |
| 375 | NDT_SMP_WTH_LOC | VARCHAR2(1) | Y |  | NDT取样宽度方向位置 | DB注释(中文) |
| 376 | NDT_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | NDT试样方向 | DB注释(中文) |
| 377 | NDT_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | NDT取样试样尺寸 | DB注释(中文) |
| 378 | NDT_SMP_THK_LOC | VARCHAR2(1) | Y |  | NDT落锤试验厚度方向取样位置 | DB注释(中文) |
| 379 | NDT_SMP_TY | VARCHAR2(1) | Y |  | NDT落锤试验试样型号 | DB注释(中文) |
| 380 | NDT_TEST_GRT_CD | VARCHAR2(1) | Y |  | NDT试验保证代号 | DB注释(中文) |
| 381 | NDT_TEST_TEMP | NUMBER | Y |  | NDT试验测试温度 | DB注释(中文) |
| 382 | NDT_TEMP | NUMBER | Y |  | NDT温度 | DB注释(中文) |
| 383 | CTOD_SMP_CND | VARCHAR2(2) | Y |  | CTOD检验取样条件 | DB注释(中文) |
| 384 | CTOD_SMP_LTH_LOC | VARCHAR2(1) | Y |  | CTOD检验取样长度方向位置 | DB注释(中文) |
| 385 | CTOD_SMP_WTH_LOC | VARCHAR2(1) | Y |  | CTOD检验取样宽度方向位置 | DB注释(中文) |
| 386 | CTOD_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | CTOD检验试样方向 | DB注释(中文) |
| 387 | CTOD_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | CTOD检验取样试样尺寸 | DB注释(中文) |
| 388 | CTOD_TEST_GRT_CD | VARCHAR2(1) | Y |  | CTOD试验保证代号 | DB注释(中文) |
| 389 | CTOD_TEST_STAND | VARCHAR2(20) | Y |  | CTOD试验方法标准 | DB注释(中文) |
| 390 | CTOD_SMP_TY | VARCHAR2(1) | Y |  | CTOD试样类型 | DB注释(中文) |
| 391 | CTOD_TEST_TEMP | NUMBER | Y |  | CTOD试验温度 | DB注释(中文) |
| 392 | CTOD_VAL_TY | VARCHAR2(1) | Y |  | CTOD值类型 | DB注释(中文) |
| 393 | CTOD_VAL | NUMBER | Y |  | CTOD值 | DB注释(中文) |
| 394 | NP_SMP_CND | VARCHAR2(2) | Y |  | 淬透性检验取样条件 | DB注释(中文) |
| 395 | NP_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 淬透性检验取样长度方向位置 | DB注释(中文) |
| 396 | NP_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 淬透性检验取样宽度方向位置 | DB注释(中文) |
| 397 | NP_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 淬透性检验试样方向 | DB注释(中文) |
| 398 | NP_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 淬透性检验取样试样尺寸 | DB注释(中文) |
| 399 | NP_JHRC_HARD_GRT_CD | VARCHAR2(1) | Y |  | 淬透性指数_JHRC硬度保证代号 | DB注释(中文) |
| 400 | NP_JHRC_HARD_MIN | NUMBER | Y |  | 淬透性指数_JHRC硬度下限值 | DB注释(中文) |
| 401 | NP_JHRC_HARD_MAX | NUMBER | Y |  | 淬透性指数_JHRC硬度上限值 | DB注释(中文) |
| 402 | NP_JHRC_DIST_MIN | NUMBER | Y |  | 淬透性指数_JHRC距离下限值 | DB注释(中文) |
| 403 | NP_JHRC_DIST_MAX | NUMBER | Y |  | 淬透性指数_JHRC距离上限值 | DB注释(中文) |
| 404 | NP_JHV_HARD_GRT_CD | VARCHAR2(1) | Y |  | 淬透性指数_JHV硬度保证代号 | DB注释(中文) |
| 405 | NP_JHV_HARD_MIN | NUMBER | Y |  | 淬透性指数_JHV硬度下限值 | DB注释(中文) |
| 406 | NP_JHV_HARD_MAX | NUMBER | Y |  | 淬透性指数_JHV硬度上限值 | DB注释(中文) |
| 407 | NP_JHV_DIST_MIN | NUMBER | Y |  | 淬透性指数_JHV距离下限值 | DB注释(中文) |
| 408 | NP_JHV_DIST_MAX | NUMBER | Y |  | 淬透性指数_JHV距离上限值 | DB注释(中文) |
| 409 | USE_YN | VARCHAR2(1) | Y |  | 是否使用 | DB注释(中文) |
| 410 | QLT_REMARKS | VARCHAR2(300) | Y |  | 质量备注 | DB注释(中文) |
| 411 | TSL1_SMP_CND | VARCHAR2(2) | Y |  | 拉伸测试取样条件_1 | DB注释(中文) |
| 412 | TSL1_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 拉伸测试长度方向取样位置_1 | DB注释(中文) |
| 413 | TSL1_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 拉伸测试宽度方向取样位置_1 | DB注释(中文) |
| 414 | TSL1_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 拉伸测试取样试样方向_1 | DB注释(中文) |
| 415 | TSL1_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 拉伸测试取样试样尺寸_1 | DB注释(中文) |
| 416 | TSL1_SMP_THK_LOC | VARCHAR2(1) | Y |  | 拉伸测试板厚度方向取样位置_1 | DB注释(中文) |
| 417 | TSL1_SMP_CD | VARCHAR2(1) | Y |  | 拉伸试样类型_1 | DB注释(中文) |
| 418 | TSL1_SMP_STATUS | VARCHAR2(1) | Y |  | 拉伸测试试样状态_1 | DB注释(中文) |
| 419 | TSL1_STRESS_GRT_CD | VARCHAR2(1) | Y |  | 消应力处理保证代号_1 | DB注释(中文) |
| 420 | TSL1_STRESS_WARM_TEMP | NUMBER | Y |  | 消应力处理_保温温度_1 | DB注释(中文) |
| 421 | TSL1_STRESS_WARM_TIME | NUMBER | Y |  | 消应力处理_保温时间_1 | DB注释(中文) |
| 422 | TSL1_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 消应力处理_冷却方式_1 | DB注释(中文) |
| 423 | TSL1_SMP_CUT_PHOTO | VARCHAR2(1) | Y |  | 拉伸试样断口照片_1 | DB注释(中文) |
| 424 | TSL1_YP_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度保证代号(YP)_1 | DB注释(中文) |
| 425 | TSL1_YP_MIN | NUMBER | Y |  | 拉伸测试屈服强度YP下限值_1 | DB注释(中文) |
| 426 | TSL1_YP_MAX | NUMBER | Y |  | 拉伸测试屈服强度YP上限值_1 | DB注释(中文) |
| 427 | TSL1_YP_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度类型_1 | DB注释(中文) |
| 428 | TSL1_TS_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试抗拉强度保证代号(TS)_1 | DB注释(中文) |
| 429 | TSL1_TS_MIN | NUMBER | Y |  | 拉伸测试抗拉强度TS下限值_1 | DB注释(中文) |
| 430 | TSL1_TS_MAX | NUMBER | Y |  | 拉伸测试抗拉强度TS上限值_1 | DB注释(中文) |
| 431 | TSL1_YP_TS_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验屈强比YP/TS保证代号_1 | DB注释(中文) |
| 432 | TSL1_YP_TS_MIN | NUMBER | Y |  | 拉伸试验屈强比YP/TS下限值_1 | DB注释(中文) |
| 433 | TSL1_YP_TS_MAX | NUMBER | Y |  | 拉伸试验屈强比YP/TS上限值_1 | DB注释(中文) |
| 434 | TSL1_RT05_RM_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt0.5/Rm保证代号_1 | DB注释(中文) |
| 435 | TSL1_RT05_RM_MIN | NUMBER | Y |  | 拉伸试验屈强比Rt0.5/Rm下限值_1 | DB注释(中文) |
| 436 | TSL1_RT05_RM_MAX | NUMBER | Y |  | 拉伸试验屈强比Rt0.5/Rm上限值_1 | DB注释(中文) |
| 437 | TSL1_RT15_RT05_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt1.5/Rt0.5保证代号_1 | DB注释(中文) |
| 438 | TSL1_RT15_RT05_MIN | NUMBER | Y |  | 拉伸试验屈强比Rt1.5/Rt0.5下限值_1 | DB注释(中文) |
| 439 | TSL1_RT15_RT05_MAX | NUMBER | Y |  | 拉伸试验屈强比Rt1.5/Rt0.5上限值_1 | DB注释(中文) |
| 440 | TSL1_RT20_RT10_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt2.0/Rt1.0保证代号_1 | DB注释(中文) |
| 441 | TSL1_RT20_RT10_MIN | NUMBER | Y |  | 拉伸试验屈强比Rt2.0/Rt1.0下限值_1 | DB注释(中文) |
| 442 | TSL1_RT20_RT10_MAX | NUMBER | Y |  | 拉伸试验屈强比Rt2.0/Rt1.0上限值_1 | DB注释(中文) |
| 443 | TSL1_RT50_RT10_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt5.0/Rt1.0保证代号_1 | DB注释(中文) |
| 444 | TSL1_RT50_RT10_MIN | NUMBER | Y |  | 拉伸试验屈强比Rt5.0/Rt1.0下限值_1 | DB注释(中文) |
| 445 | TSL1_RT50_RT10_MAX | NUMBER | Y |  | 拉伸试验屈强比Rt5.0/Rt1.0上限值_1 | DB注释(中文) |
| 446 | TSL1_CT_EX_RA_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试断后伸长率保证代号_1 | DB注释(中文) |
| 447 | TSL1_CT_EX_RA_MIN | NUMBER | Y |  | 拉抻测试断后伸长率下限值_1 | DB注释(中文) |
| 448 | TSL1_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 拉抻测试断后伸长率类型_1 | DB注释(中文) |
| 449 | TSL1_CT_RA_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验均匀伸长率保证代号_1 | DB注释(中文) |
| 450 | TSL1_CT_RA_MIN | NUMBER | Y |  | 拉伸试验均匀伸长率下限值_1 | DB注释(中文) |
| 451 | TSL1_RA_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验断面收缩率保证代号_1 | DB注释(中文) |
| 452 | TSL1_RA_MIN | NUMBER | Y |  | 拉伸试验断面收缩率下限值_1 | DB注释(中文) |
| 453 | TSL2_SMP_CND | VARCHAR2(2) | Y |  | 拉伸测试取样条件_2 | DB注释(中文) |
| 454 | TSL2_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 拉伸测试长度方向取样位置_2 | DB注释(中文) |
| 455 | TSL2_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 拉伸测试宽度方向取样位置_2 | DB注释(中文) |
| 456 | TSL2_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 拉伸测试取样试样方向_2 | DB注释(中文) |
| 457 | TSL2_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 拉伸测试取样试样尺寸_2 | DB注释(中文) |
| 458 | TSL2_SMP_THK_LOC | VARCHAR2(1) | Y |  | 拉伸测试板厚度方向取样位置_2 | DB注释(中文) |
| 459 | TSL2_SMP_CD | VARCHAR2(1) | Y |  | 拉伸试样类型_2 | DB注释(中文) |
| 460 | TSL2_SMP_STATUS | VARCHAR2(1) | Y |  | 拉伸测试试样状态_2 | DB注释(中文) |
| 461 | TSL2_STRESS_GRT_CD | VARCHAR2(1) | Y |  | 消应力处理保证代号_2 | DB注释(中文) |
| 462 | TSL2_STRESS_WARM_TEMP | NUMBER | Y |  | 消应力处理_保温温度_2 | DB注释(中文) |
| 463 | TSL2_STRESS_WARM_TIME | NUMBER | Y |  | 消应力处理_保温时间_2 | DB注释(中文) |
| 464 | TSL2_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 消应力处理_冷却方式_2 | DB注释(中文) |
| 465 | TSL2_SMP_CUT_PHOTO | VARCHAR2(1) | Y |  | 拉伸试样断口照片_2 | DB注释(中文) |
| 466 | TSL2_YP_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度保证代号(YP)_2 | DB注释(中文) |
| 467 | TSL2_YP_MIN | NUMBER | Y |  | 拉伸测试屈服强度YP下限值_2 | DB注释(中文) |
| 468 | TSL2_YP_MAX | NUMBER | Y |  | 拉伸测试屈服强度YP上限值_2 | DB注释(中文) |
| 469 | TSL2_YP_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度类型_2 | DB注释(中文) |
| 470 | TSL2_TS_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试抗拉强度保证代号(TS)_2 | DB注释(中文) |
| 471 | TSL2_TS_MIN | NUMBER | Y |  | 拉伸测试抗拉强度TS下限值_2 | DB注释(中文) |
| 472 | TSL2_TS_MAX | NUMBER | Y |  | 拉伸测试抗拉强度TS上限值_2 | DB注释(中文) |
| 473 | TSL2_YP_TS_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验屈强比YP/TS保证代号_2 | DB注释(中文) |
| 474 | TSL2_YP_TS_MIN | NUMBER | Y |  | 拉伸试验屈强比YP/TS下限值_2 | DB注释(中文) |
| 475 | TSL2_YP_TS_MAX | NUMBER | Y |  | 拉伸试验屈强比YP/TS上限值_2 | DB注释(中文) |
| 476 | TSL2_RT05_RM_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt0.5/Rm保证代号_2 | DB注释(中文) |
| 477 | TSL2_RT05_RM_MIN | NUMBER | Y |  | 拉伸试验屈强比Rt0.5/Rm下限值_2 | DB注释(中文) |
| 478 | TSL2_RT05_RM_MAX | NUMBER | Y |  | 拉伸试验屈强比Rt0.5/Rm上限值_2 | DB注释(中文) |
| 479 | TSL2_RT15_RT05_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt1.5/Rt0.5保证代号_2 | DB注释(中文) |
| 480 | TSL2_RT15_RT05_MIN | NUMBER | Y |  | 拉伸试验屈强比Rt1.5/Rt0.5下限值_2 | DB注释(中文) |
| 481 | TSL2_RT15_RT05_MAX | NUMBER | Y |  | 拉伸试验屈强比Rt1.5/Rt0.5上限值_2 | DB注释(中文) |
| 482 | TSL2_RT20_RT10_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt2.0/Rt1.0保证代号_2 | DB注释(中文) |
| 483 | TSL2_RT20_RT10_MIN | NUMBER | Y |  | 拉伸试验屈强比Rt2.0/Rt1.0下限值_2 | DB注释(中文) |
| 484 | TSL2_RT20_RT10_MAX | NUMBER | Y |  | 拉伸试验屈强比Rt2.0/Rt1.0上限值_2 | DB注释(中文) |
| 485 | TSL2_RT50_RT10_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt5.0/Rt1.0保证代号_2 | DB注释(中文) |
| 486 | TSL2_RT50_RT10_MIN | NUMBER | Y |  | 拉伸试验屈强比Rt5.0/Rt1.0下限值_2 | DB注释(中文) |
| 487 | TSL2_RT50_RT10_MAX | NUMBER | Y |  | 拉伸试验屈强比Rt5.0/Rt1.0上限值_2 | DB注释(中文) |
| 488 | TSL2_CT_EX_RA_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试断后伸长率保证代号_2 | DB注释(中文) |
| 489 | TSL2_CT_EX_RA_MIN | NUMBER | Y |  | 拉抻测试断后伸长率下限值_2 | DB注释(中文) |
| 490 | TSL2_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 拉抻测试断后伸长率类型_2 | DB注释(中文) |
| 491 | TSL2_CT_RA_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验均匀伸长率保证代号_2 | DB注释(中文) |
| 492 | TSL2_CT_RA_MIN | NUMBER | Y |  | 拉伸试验均匀伸长率下限值_2 | DB注释(中文) |
| 493 | TSL2_RA_GRT_CD | VARCHAR2(1) | Y |  | 拉伸试验断面收缩率保证代号_2 | DB注释(中文) |
| 494 | TSL2_RA_MIN | NUMBER | Y |  | 拉伸试验断面收缩率下限值_2 | DB注释(中文) |
| 495 | IMPACT1_SMP_CND | VARCHAR2(2) | Y |  | 冲击试验取样条件_1 | DB注释(中文) |
| 496 | IMPACT1_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 冲击试验取样长度方向位置_1 | DB注释(中文) |
| 497 | IMPACT1_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 冲击试验取样宽度方向位置_1 | DB注释(中文) |
| 498 | IMPACT1_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 冲击试验试样方向_1 | DB注释(中文) |
| 499 | IMPACT1_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 冲击试验取样试样尺寸_1 | DB注释(中文) |
| 500 | IMPACT1_SMP_THK_LOC | VARCHAR2(1) | Y |  | 冲击试样厚度取样位置_1 | DB注释(中文) |
| 501 | IMPACT1_TEMP | NUMBER | Y |  | 冲击测试温度_1 | DB注释(中文) |
| 502 | IMPACT1_SMP_SZ | VARCHAR2(1) | Y |  | 冲击试样尺寸_1 | DB注释(中文) |
| 503 | IMPACT1_CREAK_CD | VARCHAR2(1) | Y |  | 冲击测试缺口类型_1 | DB注释(中文) |
| 504 | IMPACT1_ENERGY_CD | VARCHAR2(1) | Y |  | 冲击试样能量值类型_1 | DB注释(中文) |
| 505 | IMPACT1_AVG_GRT_CD | VARCHAR2(1) | Y |  | 冲击测试保证代号_1 | DB注释(中文) |
| 506 | IMPACT1_IND_MIN | NUMBER | Y |  | 冲击测试单值下限值_1 | DB注释(中文) |
| 507 | IMPACT1_AVG_MIN | NUMBER | Y |  | 冲击测试平均值下限值_1 | DB注释(中文) |
| 508 | IMPACT1_SF_RATIO_GRT_CD | VARCHAR2(1) | Y |  | 冲击测试纤维断面率保证代号_1 | DB注释(中文) |
| 509 | IMPACT1_SF_RATIO_IND_MIN | NUMBER | Y |  | 纤维断面率单值下限值_1 | DB注释(中文) |
| 510 | IMPACT1_SF_RATIO_AVG_MIN | NUMBER | Y |  | 纤维断面率平均值下限值_1 | DB注释(中文) |
| 511 | IMPACT1_SMP_GRT_CD | VARCHAR2(1) | Y |  | 冲击试样侧膨胀值保证代号_1 | DB注释(中文) |
| 512 | IMPACT1_SMP_IND_MIN | NUMBER | Y |  | 冲击试样侧膨胀值单值下限值_1 | DB注释(中文) |
| 513 | IMPACT1_SMP_AVG_MIN | NUMBER | Y |  | 冲击试样侧膨胀值平均值下限值_1 | DB注释(中文) |
| 514 | IMPACT1_SMP_CUT_PHOTO | VARCHAR2(1) | Y |  | 冲击试样断口照片_1 | DB注释(中文) |
| 515 | IMPACT1_SMP_STATUS | VARCHAR2(1) | Y |  | 冲击测试试样状态_1 | DB注释(中文) |
| 516 | IMPACT2_SMP_CND | VARCHAR2(2) | Y |  | 冲击试验取样条件_2 | DB注释(中文) |
| 517 | IMPACT2_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 冲击试验取样长度方向位置_2 | DB注释(中文) |
| 518 | IMPACT2_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 冲击试验取样宽度方向位置_2 | DB注释(中文) |
| 519 | IMPACT2_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 冲击试验试样方向_2 | DB注释(中文) |
| 520 | IMPACT2_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 冲击试验取样试样尺寸_2 | DB注释(中文) |
| 521 | IMPACT2_SMP_THK_LOC | VARCHAR2(1) | Y |  | 冲击试样厚度取样位置_2 | DB注释(中文) |
| 522 | IMPACT2_TEMP | NUMBER | Y |  | 冲击测试温度_2 | DB注释(中文) |
| 523 | IMPACT2_SMP_SZ | VARCHAR2(1) | Y |  | 冲击试样尺寸_2 | DB注释(中文) |
| 524 | IMPACT2_CREAK_CD | VARCHAR2(1) | Y |  | 冲击测试缺口类型_2 | DB注释(中文) |
| 525 | IMPACT2_ENERGY_CD | VARCHAR2(1) | Y |  | 冲击试样能量值类型_2 | DB注释(中文) |
| 526 | IMPACT2_AVG_GRT_CD | VARCHAR2(1) | Y |  | 冲击测试保证代号_2 | DB注释(中文) |
| 527 | IMPACT2_IND_MIN | NUMBER | Y |  | 冲击测试单值下限值_2 | DB注释(中文) |
| 528 | IMPACT2_AVG_MIN | NUMBER | Y |  | 冲击测试平均值下限值_2 | DB注释(中文) |
| 529 | IMPACT2_SF_RATIO_GRT_CD | VARCHAR2(1) | Y |  | 冲击测试纤维断面率保证代号_2 | DB注释(中文) |
| 530 | IMPACT2_SF_RATIO_IND_MIN | NUMBER | Y |  | 纤维断面率单值下限值_2 | DB注释(中文) |
| 531 | IMPACT2_SF_RATIO_AVG_MIN | NUMBER | Y |  | 纤维断面率平均值下限值_2 | DB注释(中文) |
| 532 | IMPACT2_SMP_GRT_CD | VARCHAR2(1) | Y |  | 冲击试样侧膨胀值保证代号_2 | DB注释(中文) |
| 533 | IMPACT2_SMP_IND_MIN | NUMBER | Y |  | 冲击试样侧膨胀值单值下限值_2 | DB注释(中文) |
| 534 | IMPACT2_SMP_AVG_MIN | NUMBER | Y |  | 冲击试样侧膨胀值平均值下限值_2 | DB注释(中文) |
| 535 | IMPACT2_SMP_CUT_PHOTO | VARCHAR2(1) | Y |  | 冲击试样断口照片_2 | DB注释(中文) |
| 536 | IMPACT2_SMP_STATUS | VARCHAR2(1) | Y |  | 冲击测试试样状态_2 | DB注释(中文) |
| 537 | IMPACT3_SMP_CND | VARCHAR2(2) | Y |  | 冲击试验取样条件_3 | DB注释(中文) |
| 538 | IMPACT3_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 冲击试验取样长度方向位置_3 | DB注释(中文) |
| 539 | IMPACT3_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 冲击试验取样宽度方向位置_3 | DB注释(中文) |
| 540 | IMPACT3_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 冲击试验试样方向_3 | DB注释(中文) |
| 541 | IMPACT3_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 冲击试验取样试样尺寸_3 | DB注释(中文) |
| 542 | IMPACT3_SMP_THK_LOC | VARCHAR2(1) | Y |  | 冲击试样厚度取样位置_3 | DB注释(中文) |
| 543 | IMPACT3_TEMP | NUMBER | Y |  | 冲击测试温度_3 | DB注释(中文) |
| 544 | IMPACT3_SMP_SZ | VARCHAR2(1) | Y |  | 冲击试样尺寸_3 | DB注释(中文) |
| 545 | IMPACT3_CREAK_CD | VARCHAR2(1) | Y |  | 冲击测试缺口类型_3 | DB注释(中文) |
| 546 | IMPACT3_ENERGY_CD | VARCHAR2(1) | Y |  | 冲击试样能量值类型_3 | DB注释(中文) |
| 547 | IMPACT3_AVG_GRT_CD | VARCHAR2(1) | Y |  | 冲击测试保证代号_3 | DB注释(中文) |
| 548 | IMPACT3_IND_MIN | NUMBER | Y |  | 冲击测试单值下限值_3 | DB注释(中文) |
| 549 | IMPACT3_AVG_MIN | NUMBER | Y |  | 冲击测试平均值下限值_3 | DB注释(中文) |
| 550 | IMPACT3_SF_RATIO_GRT_CD | VARCHAR2(1) | Y |  | 冲击测试纤维断面率保证代号_3 | DB注释(中文) |
| 551 | IMPACT3_SF_RATIO_IND_MIN | NUMBER | Y |  | 纤维断面率单值下限值_3 | DB注释(中文) |
| 552 | IMPACT3_SF_RATIO_AVG_MIN | NUMBER | Y |  | 纤维断面率平均值下限值_3 | DB注释(中文) |
| 553 | IMPACT3_SMP_GRT_CD | VARCHAR2(1) | Y |  | 冲击试样侧膨胀值保证代号_3 | DB注释(中文) |
| 554 | IMPACT3_SMP_IND_MIN | NUMBER | Y |  | 冲击试样侧膨胀值单值下限值_3 | DB注释(中文) |
| 555 | IMPACT3_SMP_AVG_MIN | NUMBER | Y |  | 冲击试样侧膨胀值平均值下限值_3 | DB注释(中文) |
| 556 | IMPACT3_SMP_CUT_PHOTO | VARCHAR2(1) | Y |  | 冲击试样断口照片_3 | DB注释(中文) |
| 557 | IMPACT3_SMP_STATUS | VARCHAR2(1) | Y |  | 冲击测试试样状态_3 | DB注释(中文) |
| 558 | IMPACT4_SMP_CND | VARCHAR2(2) | Y |  | 冲击试验取样条件_4 | DB注释(中文) |
| 559 | IMPACT4_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 冲击试验取样长度方向位置_4 | DB注释(中文) |
| 560 | IMPACT4_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 冲击试验取样宽度方向位置_4 | DB注释(中文) |
| 561 | IMPACT4_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 冲击试验试样方向_4 | DB注释(中文) |
| 562 | IMPACT4_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 冲击试验取样试样尺寸_4 | DB注释(中文) |
| 563 | IMPACT4_SMP_THK_LOC | VARCHAR2(1) | Y |  | 冲击试样厚度取样位置_4 | DB注释(中文) |
| 564 | IMPACT4_TEMP | NUMBER | Y |  | 冲击测试温度_4 | DB注释(中文) |
| 565 | IMPACT4_SMP_SZ | VARCHAR2(1) | Y |  | 冲击试样尺寸_4 | DB注释(中文) |
| 566 | IMPACT4_CREAK_CD | VARCHAR2(1) | Y |  | 冲击测试缺口类型_4 | DB注释(中文) |
| 567 | IMPACT4_ENERGY_CD | VARCHAR2(1) | Y |  | 冲击试样能量值类型_4 | DB注释(中文) |
| 568 | IMPACT4_AVG_GRT_CD | VARCHAR2(1) | Y |  | 冲击测试保证代号_4 | DB注释(中文) |
| 569 | IMPACT4_IND_MIN | NUMBER | Y |  | 冲击测试单值下限值_4 | DB注释(中文) |
| 570 | IMPACT4_AVG_MIN | NUMBER | Y |  | 冲击测试平均值下限值_4 | DB注释(中文) |
| 571 | IMPACT4_SF_RATIO_GRT_CD | VARCHAR2(1) | Y |  | 冲击测试纤维断面率保证代号_4 | DB注释(中文) |
| 572 | IMPACT4_SF_RATIO_IND_MIN | NUMBER | Y |  | 纤维断面率单值下限值_4 | DB注释(中文) |
| 573 | IMPACT4_SF_RATIO_AVG_MIN | NUMBER | Y |  | 纤维断面率平均值下限值_4 | DB注释(中文) |
| 574 | IMPACT4_SMP_GRT_CD | VARCHAR2(1) | Y |  | 冲击试样侧膨胀值保证代号_4 | DB注释(中文) |
| 575 | IMPACT4_SMP_IND_MIN | NUMBER | Y |  | 冲击试样侧膨胀值单值下限值_4 | DB注释(中文) |
| 576 | IMPACT4_SMP_AVG_MIN | NUMBER | Y |  | 冲击试样侧膨胀值平均值下限值_4 | DB注释(中文) |
| 577 | IMPACT4_SMP_CUT_PHOTO | VARCHAR2(1) | Y |  | 冲击试样断口照片_4 | DB注释(中文) |
| 578 | IMPACT4_SMP_STATUS | VARCHAR2(1) | Y |  | 冲击测试试样状态_4 | DB注释(中文) |
| 579 | DWTT4_SA_RATIO_GRT_CD | VARCHAR2(1) | Y |  |  | 空 |
| 580 | DWTT4_SMP_LTH_LOC | VARCHAR2(1) | Y |  |  | 空 |
| 581 | DWTT4_SA_RATIO_IND_MIN | NUMBER | Y |  |  | 空 |
| 582 | DWTT4_SA_RATIO_AVG_MIN | NUMBER | Y |  |  | 空 |
| 583 | DWTT5_SA_RATIO_GRT_CD | VARCHAR2(1) | Y |  |  | 空 |
| 584 | DWTT5_SMP_LTH_LOC | VARCHAR2(1) | Y |  |  | 空 |
| 585 | DWTT5_SA_RATIO_IND_MIN | NUMBER | Y |  |  | 空 |
| 586 | DWTT5_SA_RATIO_AVG_MIN | NUMBER | Y |  |  | 空 |
| 587 | MGRPHY_MTLGRP_TY_PROVIDE | VARCHAR2(1) | Y |  |  | 空 |
| 588 | CPLATE_IN_BD_GRT_CD | VARCHAR2(1) | Y |  | 内弯弯曲测试保证代号 | DB注释(中文) |
| 589 | CPLATE_IN_BD_DIA_D | NUMBER | Y |  |  | 空 |
| 590 | CPLATE_IN_BD_ANGLE | NUMBER | Y |  |  | 空 |
| 591 | CPLATE_IN_BD_WTH | VARCHAR2(7) | Y |  |  | 空 |
| 592 | CPLATE_OT_BD_DIA_D | NUMBER | Y |  |  | 空 |
| 593 | CPLATE_OT_BD_ANGLE | NUMBER | Y |  |  | 空 |
| 594 | CPLATE_OT_BD_WTH | VARCHAR2(7) | Y |  |  | 空 |
| 595 | CPLATE_SIDE_BD_DIA_D | NUMBER | Y |  |  | 空 |
| 596 | CPLATE_SIDE_BD_ANGLE | NUMBER | Y |  |  | 空 |
| 597 | CPLATE_SIDE_BD_WTH | VARCHAR2(7) | Y |  |  | 空 |
| 598 | AGE_TST1_SMP_CUT_PHOTO | VARCHAR2(1) | Y |  |  | 空 |
| 599 | AGE_TST2_SMP_CUT_PHOTO | VARCHAR2(1) | Y |  |  | 空 |
| 600 | AGE_TST3_SMP_CUT_PHOTO | VARCHAR2(1) | Y |  |  | 空 |
| 601 | AGE_TST4_SMP_CUT_PHOTO | VARCHAR2(1) | Y |  |  | 空 |
| 602 | AGE_TST5_TEMP | NUMBER | Y |  |  | 空 |
| 603 | AGE_TST5_SMP_SZ | VARCHAR2(1) | Y |  |  | 空 |
| 604 | AGE_TST5_CREAK_CD | VARCHAR2(1) | Y |  | 时效冲击5测试缺口类型 | SCO_DATA_DIC(D) |
| 605 | AGE_TST5_SPCMN_DIR | VARCHAR2(1) | Y |  |  | 空 |
| 606 | AGE_TST5_GRT_CD | VARCHAR2(1) | Y |  |  | 空 |
| 607 | AGE_TST5_IND_MIN | NUMBER | Y |  |  | 空 |
| 608 | AGE_TST5_AVG_MIN | NUMBER | Y |  |  | 空 |
| 609 | AGE_TST5_SMP_GRT_CD | VARCHAR2(1) | Y |  |  | 空 |
| 610 | AGE_TST5_SMP_IND_MIN | NUMBER | Y |  |  | 空 |
| 611 | AGE_TST5_SMP_AVG_MIN | NUMBER | Y |  |  | 空 |
| 612 | AGE_TST5_SIDE_EXP_GRT_CD | VARCHAR2(1) | Y |  |  | 空 |
| 613 | AGE_TST5_SIDE_EXP_MIN | NUMBER | Y |  |  | 空 |
| 614 | AGE_TST5_SMP_CUT_PHOTO | VARCHAR2(1) | Y |  |  | 空 |
| 615 | Z_TSL_SMP_CD | VARCHAR2(1) | Y |  |  | 空 |
| 616 | AGE_TST1_SIDE_AVG_MIN | NUMBER | Y |  |  | 空 |
| 617 | AGE_TST2_SIDE_AVG_MIN | NUMBER | Y |  |  | 空 |
| 618 | AGE_TST3_SIDE_AVG_MIN | NUMBER | Y |  |  | 空 |
| 619 | AGE_TST4_SIDE_AVG_MIN | NUMBER | Y |  |  | 空 |
| 620 | AGE_TST5_SIDE_AVG_MIN | NUMBER | Y |  |  | 空 |
| 621 | CPLATE_OT_BD_GRT_CD | VARCHAR2(1) | Y |  | 外弯弯曲测试保证代号 | DB注释(中文) |
| 622 | CPLATE_SIDE_BD_GRT_CD | VARCHAR2(1) | Y |  | 侧弯弯曲测试保证代号 | DB注释(中文) |
| 623 | NP_JHRC_DIST_GRT_CD | VARCHAR2(1) | Y |  | 淬透性指数_JHRC距离保证代号 | DB注释(中文) |
| 624 | NP_JHV_DIST_GRT_CD | VARCHAR2(1) | Y |  | 淬透性指数_JHV距离保证代号 | DB注释(中文) |
| 625 | MGRPHY_MIN | NUMBER | Y |  | 晶粒度下限值 | DB注释(中文) |
| 626 | MGRPHY_MAX | NUMBER | Y |  | 晶粒度上限值 | DB注释(中文) |
| 627 | MGRPHY_GRT_CD | VARCHAR2(1) | Y |  | 晶粒度保证代号 | DB注释(中文) |
| 628 | NON_METAL_A_MAX_GRT_CD | VARCHAR2(1) | Y |  |  | 空 |
| 629 | NON_METAL_B_MAX_GRT_CD | VARCHAR2(1) | Y |  |  | 空 |
| 630 | NON_METAL_C_MAX_GRT_CD | VARCHAR2(1) | Y |  |  | 空 |
| 631 | NON_METAL_D_MAX_GRT_CD | VARCHAR2(1) | Y |  |  | 空 |
| 632 | BEND_DIA_1 | NUMBER | Y |  | 弯曲测试弯心直径 | DB注释(中文) |
| 633 | Z1_TSL_SMP_CND | VARCHAR2(2) | Y |  | Z向拉伸试验取样条件-1 | DB注释(中文) |
| 634 | Z1_TSL_SMP_LTH_LOC | VARCHAR2(1) | Y |  | Z向拉伸试验取样长度方向位置-1 | DB注释(中文) |
| 635 | Z1_TSL_SMP_WTH_LOC | VARCHAR2(1) | Y |  | Z向拉伸试验取样宽度方向位置-1 | DB注释(中文) |
| 636 | Z1_TSL_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | Z向拉伸试验取样试样尺寸-1 | DB注释(中文) |
| 637 | Z1_TSL_CUT_GRT_CD | VARCHAR2(1) | Y |  | Z向拉伸断面收缩率保证代号-1 | DB注释(中文) |
| 638 | Z1_TSL_CUT_IND_MIN | NUMBER | Y |  | Z向拉伸断面收缩率单值下限值-1 | DB注释(中文) |
| 639 | Z1_TSL_CUT_AVG_MIN | NUMBER | Y |  | Z向拉伸断面收缩率平均值下限值-1 | DB注释(中文) |
| 640 | Z1_TSL_YP_GRT_CD | VARCHAR2(1) | Y |  | Z向拉伸试验屈服强度保证代号-1 | DB注释(中文) |
| 641 | Z1_TSL_YP_MIN | NUMBER | Y |  | Z向拉伸试验屈服强度下限值-1 | DB注释(中文) |
| 642 | Z1_TSL_YP_MAX | NUMBER | Y |  | Z向拉伸试验屈服强度上限值-1 | DB注释(中文) |
| 643 | Z1_TSL_TS_GRT_CD | VARCHAR2(1) | Y |  | Z向拉伸试验抗拉强度保证代号-1 | DB注释(中文) |
| 644 | Z1_TSL_TS_MIN | NUMBER | Y |  | Z向拉伸试验抗拉强度下限值-1 | DB注释(中文) |
| 645 | Z1_TSL_TS_MAX | NUMBER | Y |  | Z向拉伸试验抗拉强度上限值-1 | DB注释(中文) |
| 646 | Z1_TSL_CT_EX_RA_GRT_CD | VARCHAR2(1) | Y |  | Z向拉伸试验断后伸长率保证代号-1 | DB注释(中文) |
| 647 | Z1_TSL_CT_EX_RA_MIN | NUMBER | Y |  | Z向拉伸试验断后伸长率下限值-1 | DB注释(中文) |
| 648 | Z1_TSL_SMP_CUT_PHOTO | VARCHAR2(1) | Y |  | Z向拉伸断口照片-1 | DB注释(中文) |
| 649 | Z1_TSL_SMP_STATUS | VARCHAR2(1) | Y |  | Z向拉伸试样状态-1 | DB注释(中文) |
| 650 | Z1_TSL_SMP_CD | VARCHAR2(1) | Y |  |  | 空 |

### SQM_STDC_COM_MANF

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=26｜被读 24 过程 / 被写 1 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：196　**主键**：QLT_STD_SEQ　**语义覆盖**：13/13

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 修改人 | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | 修改时间 | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | QLT_STD_SEQ | NUMBER | N | ✓ | 质量标准序列号 | DB注释(中文) |
| 9 | MFC_STD_TY | VARCHAR2(1) | Y |  | 制造标准分类 | DB注释(中文) |
| 10 | MFC_STD_COM_NO | VARCHAR2(20) | Y |  | 制造标准共同编号 | DB注释(中文) |
| 11 | MFC_STD_DESC | VARCHAR2(300) | Y |  | 制造标准说明 | DB注释(中文) |
| 12 | USE_YN | VARCHAR2(1) | Y |  | 是否使用 | DB注释(中文) |
| 13 | QLT_REMARKS | VARCHAR2(300) | Y |  | 质量备注 | DB注释(中文) |

### SPR_HEAT_FCE_RSLT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=26｜被读 20 过程 / 被写 3 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：181338　**主键**：SLAB_NO、FCE_CH_SEQ　**语义覆盖**：57/58

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | SLAB_NO | VARCHAR2(20) | N | ✓ | 板坯号 | DB注释(中文) |
| 9 | FCE_CH_SEQ | NUMBER | N | ✓ | 入炉顺序 | DB注释(中文) |
| 10 | PLT_NO | VARCHAR2(15) | Y |  | 钢板号 | DB注释(中文) |
| 11 | FAC_CD | VARCHAR2(1) | Y |  | 工厂代码 | DB注释(中文) |
| 12 | PROC_CD | VARCHAR2(3) | Y |  | 工序代码 | DB注释(中文) |
| 13 | FCE_STS_CD | VARCHAR2(1) | Y |  | 加热炉作业状态代码 | DB注释(中文) |
| 14 | ROLL_UNIT | VARCHAR2(10) | Y |  | 轧制单位 | DB注释(中文) |
| 15 | ROLL_UNIT_PRI | NUMBER | Y |  | 轧制单位内顺序 | DB注释(中文) |
| 16 | FCE_NO | VARCHAR2(10) | Y |  | 加热炉号 | DB注释(中文) |
| 17 | FCE_ROWNUM | VARCHAR2(10) | Y |  | 加热炉RowNum | DB注释(中文) |
| 18 | FCE_CH_DISCH_FL | VARCHAR2(10) | Y |  | 装/出炉区分 | DB注释(中文) |
| 19 | FCE_CH_DTM | VARCHAR2(14) | Y |  | 入炉日期时间 | DB注释(中文) |
| 20 | FCE_DISCH_DTM | VARCHAR2(14) | Y |  | 出炉日期时间 | DB注释(中文) |
| 21 | FCE_STAY_DUR | NUMBER | Y |  | 板坯入炉持续时间 | DB注释(中文) |
| 22 | FCE_DISCH_SUMUP_DT | VARCHAR2(14) | Y |  | 出炉计入日期 | DB注释(中文) |
| 23 | FCE_CH_TEMP | NUMBER | Y |  | 装炉板坯温度 | DB注释(中文) |
| 24 | PREHEAT_DUR | NUMBER | Y |  | 预热站作业时间 | DB注释(中文) |
| 25 | HEAT1_DUR | NUMBER | Y |  | 加热台1 作业时间 | DB注释(中文) |
| 26 | HEAT2_DUR | NUMBER | Y |  | 加热台2 作业时间 | DB注释(中文) |
| 27 | HEAT3_DUR | NUMBER | Y |  | 加热台3 作业时间 | DB注释(中文) |
| 28 | SOAK_DUR | NUMBER | Y |  | 裂痕处作业时间 | DB注释(中文) |
| 29 | PREHEAT_SURF_TEMP | NUMBER | Y |  | 预热站 表面温度 | DB注释(中文) |
| 30 | PREHEAT_DEEP_TEMP | NUMBER | Y |  | 预热站 芯部温度 | DB注释(中文) |
| 31 | HEAT1_SURF_TEMP | NUMBER | Y |  | 加热台1表面温度 | DB注释(中文) |
| 32 | HEAT1_DEEP_TEMP | NUMBER | Y |  | 加热台1芯部温度 | DB注释(中文) |
| 33 | HEAT2_SURF_TEMP | NUMBER | Y |  | 加热台2表面温度 | DB注释(中文) |
| 34 | HEAT2_DEEP_TEMP | NUMBER | Y |  | 加热台2芯部温度 | DB注释(中文) |
| 35 | HEAT3_SURF_TEMP | NUMBER | Y |  | 加热台3表面温度 | DB注释(中文) |
| 36 | HEAT3_DEEP_TEMP | NUMBER | Y |  | 加热台3芯部温度 | DB注释(中文) |
| 37 | FCE_DISCH_FL | VARCHAR2(10) | Y |  | 出炉Type | DB注释(中文) |
| 38 | FCE_DISCH_TEMP_TGT | NUMBER | Y |  | 出炉目标温度 | DB注释(中文) |
| 39 | FCE_DISCH_TEMP | NUMBER | Y |  | 出炉板坯温度 | DB注释(中文) |
| 40 | TOP_TEMP | NUMBER | Y |  | 上表面温度 | DB注释(中文) |
| 41 | CEN_TEMP | NUMBER | Y |  | 中心温度 | DB注释(中文) |
| 42 | BTM_TEMP | NUMBER | Y |  | 下表面温度 | DB注释(中文) |
| 43 | SURF_TEMP_GAP | NUMBER | Y |  | 断面温差 | DB注释(中文) |
| 44 | RLG_TEMP_TGT | NUMBER | Y |  | 目标轧制温度 | DB注释(中文) |
| 45 | CH_SFT_NO | VARCHAR2(1) | Y |  | 装炉班次 | DB注释(中文) |
| 46 | CH_GRP_NO | VARCHAR2(1) | Y |  | 装炉班组 | DB注释(中文) |
| 47 | CH_USER_ID | VARCHAR2(20) | Y |  | 装炉人员ID | DB注释(中文) |
| 48 | DISCH_SFT_NO | VARCHAR2(1) | Y |  | 出炉班次 | DB注释(中文) |
| 49 | DISCH_GRP_NO | VARCHAR2(1) | Y |  | 出炉班组 | DB注释(中文) |
| 50 | DISCH_USER_ID | VARCHAR2(20) | Y |  | 出炉人员ID | DB注释(中文) |
| 51 | RJT_CAUSE_CD | VARCHAR2(2) | Y |  | 缺号原因代码 | DB注释(中文) |
| 52 | RJT_DTM | VARCHAR2(14) | Y |  | 缺号日期时间 | DB注释(中文) |
| 53 | RJT_SFT_NO | VARCHAR2(10) | Y |  | 缺号班次 | DB注释(中文) |
| 54 | RJT_GRP_NO | VARCHAR2(10) | Y |  | 缺号班组 | DB注释(中文) |
| 55 | RJT_USER_ID | VARCHAR2(20) | Y |  | 缺号人员ID | DB注释(中文) |
| 56 | ORD_NO | VARCHAR2(20) | Y |  | 订单号 | DB注释(中文) |
| 57 | ORD_LN | VARCHAR2(10) | Y |  | 订单行号 | DB注释(中文) |
| 58 | FL | NUMBER | Y |  |  | 空 |

### SYD_MAP_BED

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=25｜被读 21 过程 / 被写 2 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：4222　**主键**：YD_GR_TP、YD_BED_CD　**语义覆盖**：36/38

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | YD_GR_TP | VARCHAR2(1) | N | ✓ | 仓库区分 | DB注释(中文) |
| 9 | YD_BED_CD | VARCHAR2(20) | N | ✓ | 垛位号 | DB注释(中文) |
| 10 | YD_BAY_CD | VARCHAR2(1) | Y |  | 库栋代码 | DB注释(中文) |
| 11 | YD_BED_STS | VARCHAR2(1) | Y |  | Bed状态 | DB注释(中文) |
| 12 | YD_BED_ACTIVE_STS | VARCHAR2(1) | Y |  | Bed活性状态 | DB注释(中文) |
| 13 | MTRL_SHP_TP | VARCHAR2(1) | Y |  | ????Type | DB注释(非中文) |
| 14 | YD_BED_TY | VARCHAR2(1) | Y |  | Bed区分 | DB注释(中文) |
| 15 | CAR_NO | VARCHAR2(10) | Y |  | ???? | DB注释(非中文) |
| 16 | YD_MAX_LOAD_PCS | NUMBER | Y |  | 最大装载个数 | DB注释(中文) |
| 17 | YD_MAX_LOAD_HGT | NUMBER | Y |  | 最大装载高度 | DB注释(中文) |
| 18 | YD_MAX_MOVE_PCS | NUMBER | Y |  | 最大移载个数 | DB注释(中文) |
| 19 | YD_MAX_MOVE_HGT | NUMBER | Y |  | 最大移载高度 | DB注释(中文) |
| 20 | YD_BED_WTH | NUMBER | Y |  | Bed宽度 | DB注释(中文) |
| 21 | YD_BED_LTH | NUMBER | Y |  | Bed长度 | DB注释(中文) |
| 22 | YD_BED_POS_X | NUMBER | Y |  | Bed X轴位置 | DB注释(中文) |
| 23 | YD_BED_POS_Y | NUMBER | Y |  | Bed Y轴位置 | DB注释(中文) |
| 24 | YD_BED_TOL_X | NUMBER | Y |  | Bed X轴允许误差 | DB注释(中文) |
| 25 | YD_BED_TOL_Y | NUMBER | Y |  | Bed Y轴允许误差 | DB注释(中文) |
| 26 | YD_BED_SPACE_X | NUMBER | Y |  | Bed间 X轴空余 | DB注释(中文) |
| 27 | YD_BED_SPACE_Y | NUMBER | Y |  | Bed间 Y轴空余 | DB注释(中文) |
| 28 | YD_DISP_POS_X | NUMBER | Y |  | 画面显示位置X | DB注释(中文) |
| 29 | YD_DISP_POS_Y | NUMBER | Y |  | 画面显示位置Y | DB注释(中文) |
| 30 | YD_BED_NM | VARCHAR2(30) | Y |  | Bed名 | DB注释(中文) |
| 31 | YD_BED_CD_INF | VARCHAR2(10) | Y |  | YD_BED_CD_INF | DB注释(非中文) |
| 32 | YD_BED_POS_WTH | NUMBER | Y |  | 画面显示宽度 | DB注释(中文) |
| 33 | YD_BED_SEQ | NUMBER | Y |  |  | 空 |
| 34 | YD_GATE_NO | VARCHAR2(2) | Y |  |  | 空 |
| 35 | MTRL_THK | NUMBER | Y |  | 材料厚度 | DB注释(中文) |
| 36 | MTRL_WTH | NUMBER | Y |  | 材料宽度 | DB注释(中文) |
| 37 | MTRL_LTH | NUMBER | Y |  | 材料长度 | DB注释(中文) |
| 38 | ORD_SIZE_TY | VARCHAR2(2) | Y |  | 定尺类型 | DB注释(中文) |

### SCR_LN_TRK

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=25｜被读 15 过程 / 被写 5 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：75　**主键**：PROC_CD、ENTRY_DELV_TY、TRK_SEQ　**语义覆盖**：22/22

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | PROC_CD | VARCHAR2(3) | N | ✓ | Process Code | DB注释(非中文) |
| 9 | ENTRY_DELV_TY | VARCHAR2(1) | N | ✓ | Entry Delivery Type    E:entry;D:exit | DB注释(非中文) |
| 10 | TRK_SEQ | NUMBER | N | ✓ | Equipment Sequence | DB注释(非中文) |
| 11 | EQUIP_NM | VARCHAR2(10) | Y |  | Equipment Nmae | DB注释(非中文) |
| 12 | RCD_STS_ID | VARCHAR2(1) | Y |  | Record Status Flag | DB注释(非中文) |
| 13 | COIL_NO | VARCHAR2(14) | Y |  | Coil Number | DB注释(非中文) |
| 14 | EVENT_STS | VARCHAR2(1) | Y |  | Event Status | DB注释(非中文) |
| 15 | EQUIP_LOC | VARCHAR2(7) | Y |  | Equipment Location | DB注释(非中文) |
| 16 | WB_STS_TP | VARCHAR2(1) | Y |  | The Flag of W/B Status  ?? | DB注释(非中文) |
| 17 | WB_DRV_MODE | VARCHAR2(1) | Y |  | W/B Operation Mode  ?? | DB注释(非中文) |
| 18 | AUT_IN_TP | VARCHAR2(1) | Y |  | Supply Coil on W/B, Auto or Not   ??? | DB注释(非中文) |
| 19 | STOP_STA_DTM | VARCHAR2(14) | Y |  | Stop Start Date | DB注释(非中文) |
| 20 | STOP_END_DTM | VARCHAR2(14) | Y |  | Stop End Date | DB注释(非中文) |
| 21 | STOP_RSN_CD | VARCHAR2(4) | Y |  | Line Stop Code | DB注释(非中文) |
| 22 | EQUIP_DESCR | VARCHAR2(30) | Y |  | Equipment DESCR | DB注释(非中文) |

### SCH_HSM_ROLL_DESIGN_RESULT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=24｜被读 10 过程 / 被写 7 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：13　**主键**：FAC_CD、ROLL_DGN_MGT_NO　**语义覆盖**：19/19

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID_Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(100) | Y |  | Created Object ID | SCO_DATA_DIC(D) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | SCO_DATA_DIC(D) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated UserID | SCO_DATA_DIC(D) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated ObjectID | SCO_DATA_DIC(D) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Date Time | SCO_DATA_DIC(D) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | SCO_DATA_DIC(D) |
| 8 | FAC_CD | VARCHAR2(1) | N | ✓ | FAC_CD[Factory Code] | SCO_DATA_DIC(D) |
| 9 | ROLL_DGN_MGT_NO | NUMBER | N | ✓ | Roll설계관리번호 | DB注释(非中文) |
| 10 | HR_ROLL_UNIT_CD | VARCHAR2(1) | Y |  | 열연Roll단위코드_？？Roll？位代？ | DB注释(中文) |
| 11 | HR_ROLL_DGN_FL | VARCHAR2(1) | Y |  | 열연Roll설계구분_？？Roll？？分？ | DB注释(中文) |
| 12 | CAST_DGN_MGT_NO | VARCHAR2(6) | Y |  | Cast설계관리번호_Cast？？管理？？ | DB注释(中文) |
| 13 | HR_ROLL_INNER_SLAB_TOT_PCS | NUMBER | Y |  | 열연Roll단위내Slab총개수_？？Roll？位？Slab？？？ | DB注释(中文) |
| 14 | HR_ROLL_INNER_SLAB_TOT_WGT | NUMBER | Y |  | 열연Roll단위Slab총중량_？？Roll？位Slab？重量 | DB注释(中文) |
| 15 | HR_ROLL_WK_SEQ | NUMBER | Y |  | 열연Roll작업순_？？Roll作？？序 | DB注释(中文) |
| 16 | HR_ROLL_UNIT_NM | VARCHAR2(10) | Y |  | 열연Roll작업단위명_？？Roll作？？位名 | DB注释(中文) |
| 17 | WK_INST_YN | VARCHAR2(1) | Y |  | 작업지시여부_作？指示？否 | DB注释(中文) |
| 18 | CTL_RCV_YN | VARCHAR2(1) | Y |  | 관제수신여부_ | DB注释(非中文) |
| 19 | PROD_CD | VARCHAR2(3) | Y |  | Product Code | SCO_DATA_DIC(D) |

### SDA_IH_MAT_MAP

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=24｜被读 16 过程 / 被写 4 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：364　**主键**：ID　**语义覆盖**：17/17

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | 生成者 | DB注释(中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | SCO_DATA_DIC(D) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | 生成时间 | DB注释(中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 修改人id | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated ObjectID | SCO_DATA_DIC(D) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | 修改时间 | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | SCO_DATA_DIC(D) |
| 8 | MATERIAL_CODE_PLC | VARCHAR2(50) | N |  | 现场换料编码 | DB注释(中文) |
| 9 | MATERIAL_NAME_PLC | VARCHAR2(150) | Y |  | 现场换料名称 | DB注释(中文) |
| 10 | MATERIAL_CODE_ERP | VARCHAR2(50) | Y |  | ERP物料编码 | DB注释(中文) |
| 11 | MATERIAL_NAME_ERP | VARCHAR2(150) | Y |  | ERP物料名称 | DB注释(中文) |
| 12 | MATERIAL_CODE_MD | VARCHAR2(50) | Y |  | 主数据物料编码 | DB注释(中文) |
| 13 | MATERIAL_NAME_MD | VARCHAR2(150) | Y |  | 主数据物料名称 | DB注释(中文) |
| 14 | WORK_MODEL | VARCHAR2(50) | Y |  | 产线区分 | DB注释(中文) |
| 15 | ID | NUMBER | N | ✓ | 主键id | DB注释(中文) |
| 16 | MATERIAL_TYPE | VARCHAR2(50) | Y |  | 物料类型 | DB注释(中文) |
| 17 | MATERIAL_NAME_TYPE | VARCHAR2(50) | Y |  | 物料大类 | DB注释(中文) |

### SYD_DISP_ORD_DETAIL_MTL

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=24｜被读 12 过程 / 被写 6 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：17518　**主键**：DORD_NO、PROD_NO　**语义覆盖**：16/27

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | SCO_DATA_DIC(D) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | SCO_DATA_DIC(D) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | SCO_DATA_DIC(D) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated UserID | SCO_DATA_DIC(D) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated ObjectID | SCO_DATA_DIC(D) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Date Time | SCO_DATA_DIC(D) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | SCO_DATA_DIC(D) |
| 8 | DORD_NO | VARCHAR2(50) | N | ✓ | Dispatch Order No | SCO_DATA_DIC(D) |
| 9 | ORD_NO | VARCHAR2(50) | Y |  | Order No | SCO_DATA_DIC(D) |
| 10 | ORD_LN | VARCHAR2(50) | Y |  |  | 空 |
| 11 | PROD_NO | VARCHAR2(20) | N | ✓ | Product No. | SCO_DATA_DIC(D) |
| 12 | PROD_IN_DIA | NUMBER | Y |  |  | 空 |
| 13 | PROD_THK | NUMBER | Y |  | Product Thickness | SCO_DATA_DIC(D) |
| 14 | PROD_YTHK | NUMBER | Y |  |  | 空 |
| 15 | PROD_FTHK | NUMBER | Y |  |  | 空 |
| 16 | PROD_WTH | NUMBER | Y |  | Product Width | SCO_DATA_DIC(D) |
| 17 | PROD_LTH | NUMBER | Y |  | Product Length | SCO_DATA_DIC(D) |
| 18 | PROD_NET_WGT | NUMBER | Y |  |  | 空 |
| 19 | PROD_ACT_WGT | NUMBER | Y |  |  | 空 |
| 20 | OUTWH_DISP_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 21 | DORD_CANCEL_DTM | VARCHAR2(14) | Y |  | Dispatch Order Cancel Time | SCO_DATA_DIC(D) |
| 22 | DORD_CANCEL_USER_ID | VARCHAR2(20) | Y |  | Dispatch Order Cancel User ID | SCO_DATA_DIC(D) |
| 23 | DORD_COMPL_CANCEL_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 24 | DORD_COMPL_CANCEL_USER_ID | VARCHAR2(20) | Y |  |  | 空 |
| 25 | BATCH_CD | VARCHAR2(20) | Y |  | 批次号 | DB注释(中文) |
| 26 | DORD_LN_NO | VARCHAR2(20) | Y |  |  | 空 |
| 27 | RTN_FL | VARCHAR2(10) | Y |  |  | 空 |

### SMS_SLAB_BY_HEAT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=24｜被读 18 过程 / 被写 3 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：13516　**主键**：SLAB_NO　**语义覆盖**：255/265

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | SLAB_NO | VARCHAR2(14) | N | ✓ | Slab No | DB注释(非中文) |
| 9 | MOM_SLAB_NO | VARCHAR2(12) | Y |  | Mother Slab No | DB注释(非中文) |
| 10 | PLAN_SLAB_NO | VARCHAR2(52) | Y |  | Plan Slab No | DB注释(非中文) |
| 11 | SLAB_STS | VARCHAR2(8) | Y |  | Slab Status | DB注释(非中文) |
| 12 | MTRL_SHP_TY | VARCHAR2(1) | Y |  | Matrial Shape Type | DB注释(非中文) |
| 13 | HEAT_NO | VARCHAR2(10) | Y |  | Heat No | DB注释(非中文) |
| 14 | SLAB_CUT_DTM | VARCHAR2(14) | Y |  | Slab Cutting Date | DB注释(非中文) |
| 15 | SLAB_PROD_DTM | VARCHAR2(14) | Y |  | Slab Production Date | DB注释(非中文) |
| 16 | PLAN_SLAB_THK | NUMBER | Y |  | Plan Slab Thickness | DB注释(非中文) |
| 17 | PLAN_SLAB_WTH | NUMBER | Y |  | Plan Slab Width | DB注释(非中文) |
| 18 | PLAN_SLAB_LTH | NUMBER | Y |  | Plan Slab Length | DB注释(非中文) |
| 19 | PLAN_SLAB_WGT | NUMBER | Y |  | Plan Slab Weight | DB注释(非中文) |
| 20 | PLAN_SLAB_STA_WTH | NUMBER | Y |  | Plan Slab Start Width | DB注释(非中文) |
| 21 | PLAN_SLAB_END_WTH | NUMBER | Y |  | Plan Slab End Width | DB注释(非中文) |
| 22 | SLAB_THK | NUMBER | Y |  | Slab Thickness | DB注释(非中文) |
| 23 | SLAB_WTH | NUMBER | Y |  | Slab Width | DB注释(非中文) |
| 24 | SLAB_LTH | NUMBER | Y |  | Slab Length | DB注释(非中文) |
| 25 | SLAB_WGT | NUMBER | Y |  | Slab Weight | DB注释(非中文) |
| 26 | SLAB_STA_WTH | NUMBER | Y |  | Slab Start Width | DB注释(非中文) |
| 27 | SLAB_END_WTH | NUMBER | Y |  | Slab End Width | DB注释(非中文) |
| 28 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  | Steel Grade | DB注释(非中文) |
| 29 | DIVERT_STEEL_GRD1 | VARCHAR2(10) | Y |  | Diverted Steel grade 1 | DB注释(非中文) |
| 30 | DIVERT_STEEL_GRD2 | VARCHAR2(10) | Y |  | Diverted Steel grade 2 | DB注释(非中文) |
| 31 | DIVERT_STEEL_GRD3 | VARCHAR2(10) | Y |  | Diverted Steel grade 3 | DB注释(非中文) |
| 32 | DIVERT_STEEL_GRD4 | VARCHAR2(10) | Y |  | Diverted Steel grade 4 | DB注释(非中文) |
| 33 | DIVERT_STEEL_GRD5 | VARCHAR2(10) | Y |  | Diverted Steel grade 5 | DB注释(非中文) |
| 34 | DIVERT_STEEL_GRD6 | VARCHAR2(10) | Y |  | Diverted Steel grade 6 | DB注释(非中文) |
| 35 | DIVERT_STEEL_GRD7 | VARCHAR2(10) | Y |  | Diverted Steel grade 7 | DB注释(非中文) |
| 36 | DIVERT_STEEL_GRD8 | VARCHAR2(10) | Y |  | Diverted Steel grade 8 | DB注释(非中文) |
| 37 | DIVERT_STEEL_GRD9 | VARCHAR2(10) | Y |  | Diverted Steel grade 9 | DB注释(非中文) |
| 38 | DIVERT_STEEL_GRD10 | VARCHAR2(10) | Y |  | Diverted Steel grade 10 | DB注释(非中文) |
| 39 | ORD_FL | VARCHAR2(1) | Y |  | Order Flag | DB注释(非中文) |
| 40 | ORD_FL_CHANGE_DTM | VARCHAR2(14) | Y |  | Order Flag Change Date | DB注释(非中文) |
| 41 | ORD_FL_CHANGE_REASON_CD | VARCHAR2(3) | Y |  | Order Flag Change Reason Code | DB注释(非中文) |
| 42 | ORD_NO | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 43 | ORD_LN | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 44 | SPEC_CD | VARCHAR2(50) | Y |  | Specification Code | DB注释(非中文) |
| 45 | ORD_USAGE | VARCHAR2(4) | Y |  | Usage Code | DB注释(非中文) |
| 46 | SMPING_TY | VARCHAR2(1) | Y |  | Sampling Y/N | DB注释(非中文) |
| 47 | PLAN_SCARF_YN | VARCHAR2(1) | Y |  | Scarfing Y/N | DB注释(非中文) |
| 48 | SCARF_DTM | VARCHAR2(14) | Y |  | Scarfing Date | DB注释(非中文) |
| 49 | SLAB_END_REASON_CD | VARCHAR2(2) | Y |  | Slab End Reason Code | DB注释(非中文) |
| 50 | YD_MTRL_TY | VARCHAR2(2) | Y |  | Yard Material Type | DB注释(非中文) |
| 51 | LOC_CD | VARCHAR2(9) | Y |  | Slab Location | DB注释(非中文) |
| 52 | SLAB_INSP_RSLT | VARCHAR2(1) | Y |  | Slab Inspection Result | DB注释(非中文) |
| 53 | SLAB_INSP_RSN | VARCHAR2(10) | Y |  | Slab Inspection Result Reason | DB注释(非中文) |
| 54 | SLAB_INSP_DTM | VARCHAR2(14) | Y |  | Slab Inspection Date | DB注释(非中文) |
| 55 | APPRD_GRD | NUMBER | Y |  | Mechanical Grade | DB注释(非中文) |
| 56 | RTN_TY | VARCHAR2(1) | Y |  | Return Type(C: claim, N: Nota) | DB注释(非中文) |
| 57 | RTN_DTM | VARCHAR2(14) | Y |  | Return Date Time | DB注释(非中文) |
| 58 | RTN_REASON_CD | VARCHAR2(2) | Y |  | Return Reason Code | DB注释(非中文) |
| 59 | CUT_DTM | VARCHAR2(14) | Y |  | Cutting(Scrap) date | DB注释(非中文) |
| 60 | PROD_DT | VARCHAR2(8) | Y |  | Production date | DB注释(非中文) |
| 61 | PLAN_CUT_YN | VARCHAR2(1) | Y |  | Plan Cut  Y/N | DB注释(非中文) |
| 62 | SLAB_END_DTM | VARCHAR2(14) | Y |  | Slab end date | DB注释(非中文) |
| 63 | SCARF_INST_SEQ | NUMBER | Y |  | Scarfing instruction seq | DB注释(非中文) |
| 64 | FCUT_INST_SEQ | NUMBER | Y |  | Cutting(Scrap) instruction seq | DB注释(非中文) |
| 65 | COOLING_METHOD | VARCHAR2(1) | Y |  | Cooling Method Type(Air, Water) | DB注释(非中文) |
| 66 | COOLING_COMP_YN | VARCHAR2(1) | Y |  | Cooling Complete Y/N | DB注释(非中文) |
| 67 | MIXED_SLAB_TY | VARCHAR2(1) | Y |  | Mixed Slab Type | DB注释(非中文) |
| 68 | MARK_YN | VARCHAR2(1) | Y |  | Marked Y/N | DB注释(非中文) |
| 69 | MARK_DTM | VARCHAR2(14) | Y |  | Marked Datetime | DB注释(非中文) |
| 70 | PROG_CD | VARCHAR2(4) | Y |  | Progress Code | DB注释(非中文) |
| 71 | SMP_NO | VARCHAR2(11) | Y |  | Sampling Code | DB注释(非中文) |
| 72 | PROD_CD | VARCHAR2(3) | Y |  | Production Code | DB注释(非中文) |
| 73 | HR_PROD_THK_AIM | NUMBER | Y |  | HR Production Thick Aim | DB注释(非中文) |
| 74 | HR_PROD_WTH_AIM | NUMBER | Y |  | HR Production Width Aim | DB注释(非中文) |
| 75 | CONF_PASS_PLANT_CD | VARCHAR2(30) | Y |  | Confirm Pass Plant Code | DB注释(非中文) |
| 76 | HR_PLAN_OP_CD | VARCHAR2(60) | Y |  | HR Plan Operation Code | DB注释(非中文) |
| 77 | ORD_DLV_DT | VARCHAR2(8) | Y |  | Order Delivery | DB注释(非中文) |
| 78 | SLAB_DIR_DEST_FL | VARCHAR2(2) | Y |  | Slab Direction Destination Flag | DB注释(非中文) |
| 79 | URGENT_TY | VARCHAR2(1) | Y |  | Urgent Type | DB注释(非中文) |
| 80 | ORD_TY | VARCHAR2(2) | Y |  | Order Type | DB注释(非中文) |
| 81 | HRL_MFC_STD_NO | VARCHAR2(11) | Y |  | HR manufacturing Standard No | DB注释(非中文) |
| 82 | TAPER_FL | VARCHAR2(1) | Y |  | Tapered Flag | DB注释(非中文) |
| 83 | SPL_REASON_CD | VARCHAR2(2) | Y |  | Surplus Production Direction Code | DB注释(非中文) |
| 84 | SPECIFIC_GRAVITY | NUMBER | Y |  | Specific Gravity | DB注释(非中文) |
| 85 | ORD_NO1 | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 86 | ORD_LN1 | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 87 | SLAB_DGN_WGT1 | NUMBER | Y |  | Slab Design Weight | DB注释(非中文) |
| 88 | ORD_NO2 | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 89 | ORD_LN2 | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 90 | SLAB_DGN_WGT2 | NUMBER | Y |  | Slab Design Weight | DB注释(非中文) |
| 91 | ORD_NO3 | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 92 | ORD_LN3 | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 93 | SLAB_DGN_WGT3 | NUMBER | Y |  | Slab Design Weight | DB注释(非中文) |
| 94 | PROC_CD | VARCHAR2(3) | Y |  | Process Code | DB注释(非中文) |
| 95 | SLAB_PLAN_DEST | NUMBER | Y |  | Slab Planned destination | DB注释(非中文) |
| 96 | HCR_FL | VARCHAR2(1) | Y |  | Classification of Hot Coil Work Pattern | DB注释(非中文) |
| 97 | SEMI_PROD_ITEM_CD | VARCHAR2(30) | Y |  | SEMI Production Item code | DB注释(非中文) |
| 98 | SALES_PROD_ITEM_CD | VARCHAR2(30) | Y |  | SALES Production Item code | DB注释(非中文) |
| 99 | PREV_ORD_FL | VARCHAR2(1) | Y |  | Previouse Order Flag | DB注释(非中文) |
| 100 | ORD_FL_CHANGE_REASON_CD2 | VARCHAR2(3) | Y |  | Order Flag Change Reason Code | DB注释(非中文) |
| 101 | ORD_FL_CHANGE_REASON_CD3 | VARCHAR2(3) | Y |  | Order Flag Change Reason Code | DB注释(非中文) |
| 102 | ORD_FL_CHANGE_REASON_CD4 | VARCHAR2(3) | Y |  | Order Flag Change Reason Code | DB注释(非中文) |
| 103 | ORD_FL_CHANGE_REASON_CD5 | VARCHAR2(3) | Y |  | Order Flag Change Reason Code | DB注释(非中文) |
| 104 | PREV_ORD_NO | VARCHAR2(10) | Y |  | Previouse Order NO | DB注释(非中文) |
| 105 | PREV_ORD_LN | VARCHAR2(3) | Y |  | Previouse Order Line | DB注释(非中文) |
| 106 | PREV_PROG_CD | VARCHAR2(4) | Y |  | Previouse Progress Code | DB注释(非中文) |
| 107 | PREV_HCR_FL | VARCHAR2(1) | Y |  | Previouse HCR Flag | DB注释(非中文) |
| 108 | HEAT_JUDG | VARCHAR2(1) | Y |  | Heat Judgment Result | DB注释(非中文) |
| 109 | SLAB_SCRAF_END_TY | VARCHAR2(1) | Y |  | Slab Scarfing ended Type | DB注释(非中文) |
| 110 | SLAB_CHARG_PROG_TY | VARCHAR2(1) | Y |  | Reheating Furnace Slab Charging Progress Type | DB注释(非中文) |
| 111 | COIL_NO | VARCHAR2(14) | Y |  | HotCoil No | DB注释(非中文) |
| 112 | FCE_CHARGE_DTM | VARCHAR2(14) | Y |  | Furnance Charge Date | DB注释(非中文) |
| 113 | RLG_END_DTM | VARCHAR2(14) | Y |  | The Rolling End Date | DB注释(非中文) |
| 114 | RJT_NO_DTM | VARCHAR2(14) | Y |  | Date of Reject | DB注释(非中文) |
| 115 | RJT_CAUSE_CD | VARCHAR2(2) | Y |  | Reject Cause Code | DB注释(非中文) |
| 116 | RJT_CAUSE_CD2 | VARCHAR2(2) | Y |  | Reject Cause Code | DB注释(非中文) |
| 117 | RJT_CAUSE_CD3 | VARCHAR2(2) | Y |  | Reject Cause Code | DB注释(非中文) |
| 118 | RJT_CAUSE_CD4 | VARCHAR2(2) | Y |  | Reject Cause Code | DB注释(非中文) |
| 119 | RJT_CAUSE_CD5 | VARCHAR2(2) | Y |  | Reject Cause Code | DB注释(非中文) |
| 120 | ERP_POSTING_YN | VARCHAR2(1) | Y |  | Slab Result Send To ERP Y/N | DB注释(非中文) |
| 121 | ERP_POSTING_DTM | VARCHAR2(14) | Y |  | Slab Result Send To ERP Datetime | DB注释(非中文) |
| 122 | STEEL_GRD | VARCHAR2(10) | Y |  | Steel Grade | DB注释(非中文) |
| 123 | SCARF_TY | VARCHAR2(6) | Y |  | Scarfing Type | DB注释(非中文) |
| 124 | RJT_SLAB_RLS_TY | NUMBER | Y |  | Reject Slab Release Type | DB注释(非中文) |
| 125 | STA_POS_WID_CHG | NUMBER | Y |  | Start Point of Width Change | DB注释(非中文) |
| 126 | END_POS_WID_CHG | NUMBER | Y |  | End Point of Width Change | DB注释(非中文) |
| 127 | WDG_LNDSCP_VAL | NUMBER | Y |  | Slab wedge | DB注释(非中文) |
| 128 | WDG_PORTR_VAL | NUMBER | Y |  | length slab wedge | DB注释(非中文) |
| 129 | WDG_PORTR_POS | NUMBER | Y |  | length slab wedge change | DB注释(非中文) |
| 130 | PROD_ITEM_CD | VARCHAR2(30) | Y |  | Production Item Code | DB注释(非中文) |
| 131 | ERP_TRANSACTION_TY | VARCHAR2(2) | Y |  | ERP Transaction Type | DB注释(非中文) |
| 132 | ERP_SUMUP_DT | VARCHAR2(14) | Y |  | Sumup Date | DB注释(非中文) |
| 133 | ERP_ORD_NO | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 134 | ERP_ORD_LN | VARCHAR2(3) | Y |  | Order Line No | DB注释(非中文) |
| 135 | ERP_ITEM_CD_PLAN | VARCHAR2(30) | Y |  | Item Code Plan | DB注释(非中文) |
| 136 | ERP_ITEM_CD | VARCHAR2(30) | Y |  | Item Code | DB注释(非中文) |
| 137 | ERP_PROD_QTY | NUMBER | Y |  | Product Quantity | DB注释(非中文) |
| 138 | ERP_PROD_SUB_INV_CD | VARCHAR2(2) | Y |  | Product Sub Inventory Code | DB注释(非中文) |
| 139 | ERP_MTRL_INPUT_ITEM_CD_01 | VARCHAR2(30) | Y |  | Input Item Code 01 | DB注释(非中文) |
| 140 | ERP_MTRL_INPUT_QTY_01 | NUMBER | Y |  | Input Quantity 01 | DB注释(非中文) |
| 141 | ERP_MTRL_INPUT_MTRL_NO_01 | VARCHAR2(20) | Y |  | Input Material No 01 | DB注释(非中文) |
| 142 | ERP_MTRL_INPUT_BYPROD_FL_01 | VARCHAR2(1) | Y |  | Input By-Product Flag 01 | DB注释(非中文) |
| 143 | ERP_MTRL_INPUT_SUB_INV_CD_01 | VARCHAR2(2) | Y |  | Input Sub Inventory Code 01 | DB注释(非中文) |
| 144 | ERP_MTRL_INPUT_PROC_CD_01 | VARCHAR2(4) | Y |  | Input Process Code 01 | DB注释(非中文) |
| 145 | ERP_PROC_CD_01 | VARCHAR2(4) | Y |  | Process Code 01 | DB注释(非中文) |
| 146 | ERP_RSC_USAGE_01 | NUMBER | Y |  | Resource Usage 01 | DB注释(非中文) |
| 147 | ERP_OLD_ITEM_CD | VARCHAR2(30) | Y |  |  | 空 |
| 148 | ERP_OLD_PROD_QTY | NUMBER | Y |  |  | 空 |
| 149 | DEFECT_CD | VARCHAR2(60) | Y |  | Defect Code | SCO_DATA_DIC(D) |
| 150 | PLAN_ORD_FL | VARCHAR2(1) | Y |  | Plan Order Flag | DB注释(非中文) |
| 151 | PREV_ORD_NO1 | VARCHAR2(10) | Y |  | Previouse Order NO1 | DB注释(非中文) |
| 152 | PREV_ORD_LN1 | VARCHAR2(3) | Y |  | Previouse Order Line1 | DB注释(非中文) |
| 153 | PREV_ORD_NO2 | VARCHAR2(10) | Y |  | Previouse Order NO2 | DB注释(非中文) |
| 154 | PREV_ORD_LN2 | VARCHAR2(3) | Y |  | Previouse Order Line2 | DB注释(非中文) |
| 155 | PREV_ORD_NO3 | VARCHAR2(10) | Y |  | Previouse Order NO3 | DB注释(非中文) |
| 156 | PREV_ORD_LN3 | VARCHAR2(3) | Y |  | Previouse Order Line3 | DB注释(非中文) |
| 157 | PO_FLAG | VARCHAR2(1) | Y |  | Purchase slab flag | SCO_DATA_DIC(L) |
| 158 | PO_NO | VARCHAR2(20) | Y |  | Purchase Order Number | SCO_DATA_DIC(D) |
| 159 | PO_LINE_NO | VARCHAR2(5) | Y |  | Purchase Line Number | SCO_DATA_DIC(D) |
| 160 | PO_DLV_NO | VARCHAR2(5) | Y |  | Purchase Delivery No | SCO_DATA_DIC(D) |
| 161 | HEAT_NO_PO | VARCHAR2(20) | Y |  | po heat no | SCO_DATA_DIC(L) |
| 162 | SLAB_NO_PO | VARCHAR2(20) | Y |  | PO SLAB NO | SCO_DATA_DIC(L) |
| 163 | SURF_GRD | VARCHAR2(2) | Y |  | Slab Surface Grade | SCO_DATA_DIC(D) |
| 164 | CHECK_FL | VARCHAR2(1) | Y |  |  | 空 |
| 165 | CHECK_TM | VARCHAR2(14) | Y |  |  | 空 |
| 166 | CHECK_USER_ID | VARCHAR2(20) | Y |  |  | 空 |
| 167 | ERP_SEND_YN | VARCHAR2(1) | Y |  | Slab Transfer Send To ERP Y/N | DB注释(非中文) |
| 168 | ERP_SEND_DTM | VARCHAR2(14) | Y |  | Slab Transfer Send To ERP Datetime | DB注释(非中文) |
| 169 | TRANS_FL | VARCHAR2(2) | Y |  |  | 空 |
| 170 | TRANS_EMP | VARCHAR2(20) | Y |  |  | 空 |
| 171 | TRANS_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 172 | TRANSFER_FG | VARCHAR2(2) | Y |  |  | 空 |
| 173 | ERP_SEND_FL | VARCHAR2(1) | Y |  | ?ERP???0-CCM;1-HR;2-Plate;3-Steckel | DB注释(非中文) |
| 174 | SLAB_TY | VARCHAR2(1) | Y |  | ??SLAB??_?????? | DB注释(非中文) |
| 175 | ORD_NO4 | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 176 | ORD_LN4 | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 177 | SLAB_DGN_WGT4 | NUMBER | Y |  | Slab Design Weight | DB注释(非中文) |
| 178 | PREV_ORD_NO4 | VARCHAR2(10) | Y |  | Previouse Order NO3 | DB注释(非中文) |
| 179 | PREV_ORD_LN4 | VARCHAR2(3) | Y |  | Previouse Order Line3 | DB注释(非中文) |
| 180 | ORD_NO5 | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 181 | ORD_LN5 | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 182 | SLAB_DGN_WGT5 | NUMBER | Y |  | Slab Design Weight | DB注释(非中文) |
| 183 | PREV_ORD_NO5 | VARCHAR2(10) | Y |  | Previouse Order NO3 | DB注释(非中文) |
| 184 | PREV_ORD_LN5 | VARCHAR2(3) | Y |  | Previouse Order Line3 | DB注释(非中文) |
| 185 | ORD_NO6 | VARCHAR2(10) | Y |  | Order No | DB注释(非中文) |
| 186 | ORD_LN6 | VARCHAR2(3) | Y |  | Order Line | DB注释(非中文) |
| 187 | SLAB_DGN_WGT6 | NUMBER | Y |  | Slab Design Weight | DB注释(非中文) |
| 188 | PREV_ORD_NO6 | VARCHAR2(10) | Y |  | Previouse Order NO3 | DB注释(非中文) |
| 189 | PREV_ORD_LN6 | VARCHAR2(3) | Y |  | Previouse Order Line3 | DB注释(非中文) |
| 190 | SLAB_FG | VARCHAR2(1) | Y |  | ??SLAB??_?????? | DB注释(非中文) |
| 191 | NATL_SPEC_YEAR | VARCHAR2(4) | Y |  | ?????? | DB注释(非中文) |
| 192 | PROD_CD_FL | VARCHAR2(1) | Y |  | ?????? | DB注释(非中文) |
| 193 | SLAB_REC_DTM | VARCHAR2(14) | Y |  | ???????????? | DB注释(非中文) |
| 194 | BEF_SPEC_CD | VARCHAR2(50) | Y |  | ????? | DB注释(非中文) |
| 195 | BEF_NATL_SPEC_YEAR | VARCHAR2(4) | Y |  | ?????? | DB注释(非中文) |
| 196 | SPEC_CHG_FLAG | VARCHAR2(1) | Y |  | ?????? | DB注释(非中文) |
| 197 | SLAB_HEAT_NO | VARCHAR2(9) | Y |  | ??????? | DB注释(非中文) |
| 198 | TRANS_CCM_REQ_DTM | VARCHAR2(14) | Y |  | Transfer Request Datetime(????????/4300/3500????) | DB注释(非中文) |
| 199 | TRANS_CCM_REQ_USER_ID | VARCHAR2(20) | Y |  | Transfer Request User ID(????????/4300/3500???) | DB注释(非中文) |
| 200 | TRANS_CCM_ACCT_DTM | VARCHAR2(14) | Y |  | Transfer Accept Datetime(??????/4300/3500????) | DB注释(非中文) |
| 201 | TRANS_CCM_ACCT_USER_ID | VARCHAR2(20) | Y |  | Transfer Accept User ID(??????/4300/3500?????) | DB注释(非中文) |
| 202 | TRANS_HPS_RTN_REQ_DTM | VARCHAR2(14) | Y |  | Transfer Request Datetime(??/4300/3500?????????) | DB注释(非中文) |
| 203 | TRANS_HPS_RTN_REQ_USER_ID | VARCHAR2(20) | Y |  | Transfer Accept User ID(??/4300/3500????????) | DB注释(非中文) |
| 204 | TRANS_HPS_ACCT_DTM | VARCHAR2(14) | Y |  | Transfer Accept Datetime(??/4300/3500??????????) | DB注释(非中文) |
| 205 | TRANS_HPS_ACCT_USER_ID | VARCHAR2(20) | Y |  | Transfer Accept User ID(??/4300/3500??????????) | DB注释(非中文) |
| 206 | TRANS_SLAB_WGT | NUMBER | Y |  | Transfer Slab Weight | DB注释(非中文) |
| 207 | COM_BLANK_PROCESS | VARCHAR2(2) | Y |  | ????? | DB注释(非中文) |
| 208 | COM_SLAB_NO | VARCHAR2(13) | Y |  | ????? | DB注释(非中文) |
| 209 | WASH_CUT_FL | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 210 | ALTERNATIVE_SPEC_CD | VARCHAR2(100) | Y |  | ?????????? | DB注释(非中文) |
| 211 | ALTERNATIVE_NOTE | VARCHAR2(100) | Y |  | ????? | DB注释(非中文) |
| 212 | DEF_MTRL_NOTE | VARCHAR2(100) | Y |  | ????? | DB注释(非中文) |
| 213 | CAR_NO | VARCHAR2(10) | Y |  | ?? | DB注释(非中文) |
| 214 | CAR_SEQ | VARCHAR2(20) | Y |  | Car Sequence | SCO_DATA_DIC(D) |
| 215 | SLAB_FINAL_DEST | VARCHAR2(10) | Y |  | 板坯去向 | DB注释(中文) |
| 216 | CAST_RULE | NUMBER | Y |  | 定尺 | DB注释(中文) |
| 217 | SLAB_CUT_POSIT_CD_DES | VARCHAR2(10) | Y |  | 切割位置 | DB注释(中文) |
| 218 | MIX_CAST_SLAB | VARCHAR2(1) | Y |  | 混浇坯 | DB注释(中文) |
| 219 | CUT_SLAB_PROG_CD | VARCHAR2(1) | Y |  | 精整进程代码 | DB注释(中文) |
| 220 | HEAT_SLAB_NO | VARCHAR2(13) | Y |  |  | 空 |
| 221 | CSLAB_TOT_NUMS | NUMBER | Y |  | 总支数 | DB注释(中文) |
| 222 | CSLAB_TOT_WGT | NUMBER | Y |  | 总重量（理重） | DB注释(中文) |
| 223 | CSLAB_TOT_REAL_WGT | NUMBER | Y |  | 总重量（实重） | DB注释(中文) |
| 224 | CSLAB_NUMS | NUMBER | Y |  | 合格支数 | DB注释(中文) |
| 225 | CSLAB_WGT | NUMBER | Y |  | 合格重量（理重） | DB注释(中文) |
| 226 | CSLAB_REAL_WGT | NUMBER | Y |  | 合格重量（实重） | DB注释(中文) |
| 227 | CSLAB_BAD_NUMS | NUMBER | Y |  | 作废支数 | DB注释(中文) |
| 228 | CSLAB_BAD_WGT | NUMBER | Y |  | 不合格重量（理重） | DB注释(中文) |
| 229 | CSLAB_BAD_REAL_WGT | NUMBER | Y |  | 不合格重量（实重） | DB注释(中文) |
| 230 | DEFECT_1 | VARCHAR2(4) | Y |  | 缺陷1 | DB注释(中文) |
| 231 | DEFECT_1_NUMS | NUMBER | Y |  | 缺陷1支数 | DB注释(中文) |
| 232 | DEFECT_1_WGT | NUMBER | Y |  | 缺陷1重量（理重） | DB注释(中文) |
| 233 | DEFECT_1_REAL_WGT | NUMBER | Y |  | 缺陷1重量(实重) | DB注释(中文) |
| 234 | DEFECT_2 | VARCHAR2(4) | Y |  | 缺陷2 | DB注释(中文) |
| 235 | DEFECT_2_NUMS | NUMBER | Y |  | 缺陷2支数 | DB注释(中文) |
| 236 | DEFECT_2_WGT | NUMBER | Y |  | 缺陷2重量（理重） | DB注释(中文) |
| 237 | DEFECT_2_REAL_WGT | NUMBER | Y |  | 缺陷2重量(实重) | DB注释(中文) |
| 238 | DEFECT_3 | VARCHAR2(4) | Y |  | 缺陷3 | DB注释(中文) |
| 239 | DEFECT_3_NUMS | NUMBER | Y |  | 缺陷3支数 | DB注释(中文) |
| 240 | DEFECT_3_WGT | NUMBER | Y |  | 缺陷3重量（理重） | DB注释(中文) |
| 241 | DEFECT_3_REAL_WGT | NUMBER | Y |  | 缺陷3重量(实重) | DB注释(中文) |
| 242 | DEFECT_4 | VARCHAR2(4) | Y |  | 缺陷4 | DB注释(中文) |
| 243 | DEFECT_4_NUMS | NUMBER | Y |  | 缺陷4支数 | DB注释(中文) |
| 244 | DEFECT_4_WGT | NUMBER | Y |  | 缺陷4重量（理重） | DB注释(中文) |
| 245 | DEFECT_4_REAL_WGT | NUMBER | Y |  | 缺陷4重量(实重) | DB注释(中文) |
| 246 | DEFECT_5 | VARCHAR2(4) | Y |  | 缺陷5 | DB注释(中文) |
| 247 | DEFECT_5_NUMS | NUMBER | Y |  | 缺陷5支数 | DB注释(中文) |
| 248 | DEFECT_5_WGT | NUMBER | Y |  | 缺陷5重量（理重） | DB注释(中文) |
| 249 | DEFECT_5_REAL_WGT | NUMBER | Y |  | 缺陷5重量(实重) | DB注释(中文) |
| 250 | DEFECT_1_COMPT | VARCHAR2(1) | Y |  | 缺陷精整完成 | DB注释(中文) |
| 251 | DEFECT_2_COMPT | VARCHAR2(1) | Y |  | 缺陷精整完成 | DB注释(中文) |
| 252 | DEFECT_3_COMPT | VARCHAR2(1) | Y |  | 缺陷精整完成 | DB注释(中文) |
| 253 | DEFECT_4_COMPT | VARCHAR2(1) | Y |  | 缺陷精整完成 | DB注释(中文) |
| 254 | DEFECT_5_COMPT | VARCHAR2(1) | Y |  | 缺陷精整完成 | DB注释(中文) |
| 255 | ABOLISH_NUMS | NUMBER | Y |  | 作废数量 | DB注释(中文) |
| 256 | WAREHOUSING_NUMS | NUMBER | Y |  | 入库支数 | DB注释(中文) |
| 257 | STACK_NO | VARCHAR2(10) | Y |  | 入库垛位 | DB注释(中文) |
| 258 | TO_ROLL_NUMS | NUMBER | Y |  | 送轧钢支数 | DB注释(中文) |
| 259 | OUT_RESHIP_NUMS | NUMBER | Y |  | 外倒支数 | DB注释(中文) |
| 260 | SELL_NUMS | NUMBER | Y |  | 外卖支数 | DB注释(中文) |
| 261 | PENDING_NUMS | NUMBER | Y |  | 待处理支数 | DB注释(中文) |
| 262 | DIST_NUMS | NUMBER | Y |  | 可分配支数 | DB注释(中文) |
| 263 | YARD_NO | VARCHAR2(1) | Y |  | 库房 | DB注释(中文) |
| 264 | REC_IN_DTM | VARCHAR2(14) | Y |  | 钢坯入库时间 | DB注释(中文) |
| 265 | SLAB_SECTION | VARCHAR2(24) | Y |  | 断面 | DB注释(中文) |

### SPR_HOLD

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=24｜被读 16 过程 / 被写 4 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：0　**主键**：PLT_NO、HOLD_SEQ　**语义覆盖**：38/38

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | PROC_CD | VARCHAR2(3) | Y |  | 工序代码 | DB注释(中文) |
| 9 | PLT_NO | VARCHAR2(20) | N | ✓ | PLT NO | DB注释(非中文) |
| 10 | HOLD_SEQ | NUMBER | N | ✓ | Hold SEQ | DB注释(非中文) |
| 11 | RCD_STS_ID | VARCHAR2(1) | Y |  | Record Status | DB注释(非中文) |
| 12 | RCD_STS_CHG_DTM | VARCHAR2(14) | Y |  | Record Status Change Date | DB注释(非中文) |
| 13 | ENTRY_DELV_TY | VARCHAR2(1) | Y |  | Entry Delivary Type | DB注释(非中文) |
| 14 | MTRL_SHP_TY | VARCHAR2(1) | Y |  | Material Shape Type | DB注释(非中文) |
| 15 | HOLD_REQ_DTM | VARCHAR2(14) | Y |  | Hold Request Datetime | DB注释(非中文) |
| 16 | HOLD_REQ_SFT | VARCHAR2(1) | Y |  | Hold Request Shift | DB注释(非中文) |
| 17 | HOLD_REQ_USER_ID | VARCHAR2(20) | Y |  | Hold Request User ID | DB注释(非中文) |
| 18 | HOLD_REQ_SUMUP_DT | VARCHAR2(8) | Y |  | Hold Request Sumup Date | DB注释(非中文) |
| 19 | HOLD_RSN_CD | VARCHAR2(200) | Y |  | Hold Reason Code(PROD_TOT_UNJDG_CAU_TY)--落地原因 | DB注释(中文) |
| 20 | HOLD_RSN_DESC | VARCHAR2(1000) | Y |  | Hold Reason Description--保留原因备注 | DB注释(中文) |
| 21 | NXT_PROC_CD | VARCHAR2(3) | Y |  | Next Process Code | DB注释(非中文) |
| 22 | REPROC_CD | VARCHAR2(1) | Y |  | Reprocess Code | DB注释(非中文) |
| 23 | HOLD_DISPOSE_FLAG | VARCHAR2(1) | Y |  | dispose flag  0 : no dispose; 1: dispose | DB注释(非中文) |
| 24 | SND_BACK_YN | VARCHAR2(1) | Y |  | SND_BACK_YN | DB注释(非中文) |
| 25 | SND_BACK_DTM | VARCHAR2(14) | Y |  | SND_BACK_DTM | DB注释(非中文) |
| 26 | SND_BACK_SUMUP_DT | VARCHAR2(8) | Y |  | SND_BACK_SUMUP_DT | DB注释(非中文) |
| 27 | SND_BACK_STS | VARCHAR2(1) | Y |  | SND_BACK_STS | DB注释(非中文) |
| 28 | FAC_CD | VARCHAR2(1) | Y |  | 工厂代码 | DB注释(中文) |
| 29 | HOLD_REQ_END_DTM | VARCHAR2(14) | Y |  | 结束保留时间 | DB注释(中文) |
| 30 | HOLD_REQ_END_USER_ID | VARCHAR2(20) | Y |  | 结束保留人员 | DB注释(中文) |
| 31 | HOLD_REQ_END_REGION | VARCHAR2(10) | Y |  | 结束保留区域 | DB注释(中文) |
| 32 | HOLD_ACTION_END_DTM | VARCHAR2(14) | Y |  | 落地结束时间 | DB注释(中文) |
| 33 | HOLD_RSN_CD_LOV | VARCHAR2(30) | Y |  | 保留原因 | DB注释(中文) |
| 34 | BEFORE_REQ_DTM | VARCHAR2(14) | Y |  | 修改时间 | DB注释(中文) |
| 35 | BEFORE_RSN_CD_LOV | VARCHAR2(30) | Y |  | 修改之前的保留原因 | DB注释(中文) |
| 36 | BEFORE_RSN_CD | VARCHAR2(200) | Y |  | 修改之前的信息 | DB注释(中文) |
| 37 | BEFORE_RSN_DESC | VARCHAR2(1000) | Y |  | 修改之前的信息 | DB注释(中文) |
| 38 | BEFORE_REQ_USER_ID | VARCHAR2(20) | Y |  | 修改人员名称 | DB注释(中文) |

### SQM_WSP_MTC_CHEM_INF

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=24｜被读 8 过程 / 被写 8 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：2　**主键**：PK_ID　**语义覆盖**：43/72

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | MTC_NO | VARCHAR2(11) | N |  | 质量保证书编号 | SCO_DATA_DIC(D) |
| 2 | MTC_STS | VARCHAR2(1) | N |  |  | 空 |
| 3 | MTC_DTM | VARCHAR2(14) | N |  |  | 空 |
| 4 | SMS_PROD_CHEM_TY | VARCHAR2(1) | N |  | 炼钢产品成分分类 | SCO_DATA_DIC(D) |
| 5 | CHEM_TEST_NO | VARCHAR2(14) | N |  | Heat编号 | SCO_DATA_DIC(D) |
| 6 | SN_RSLT | VARCHAR2(20) | Y |  | 产品成分Sn实绩 | SCO_DATA_DIC(D) |
| 7 | H_RSLT | VARCHAR2(20) | Y |  | 产品成分H实绩 | SCO_DATA_DIC(D) |
| 8 | CHEMI1_RSLT | VARCHAR2(20) | Y |  | 实绩复合元素1值 | SCO_DATA_DIC(D) |
| 9 | CHEMI2_RSLT | VARCHAR2(20) | Y |  | 实绩复合元素2值 | SCO_DATA_DIC(D) |
| 10 | RE_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 11 | W_RSLT | VARCHAR2(20) | Y |  | 产品成分W实绩 | SCO_DATA_DIC(D) |
| 12 | ZR_RSLT | VARCHAR2(20) | Y |  | 产品成分Zr实绩 | SCO_DATA_DIC(D) |
| 13 | PB_RSLT | VARCHAR2(20) | Y |  | 产品成分Pb实绩 | SCO_DATA_DIC(D) |
| 14 | AS_RSLT | VARCHAR2(20) | Y |  | 产品成分As实绩 | SCO_DATA_DIC(D) |
| 15 | CO_RSLT | VARCHAR2(20) | Y |  | 产品成分Co实绩 | SCO_DATA_DIC(D) |
| 16 | CA_RSLT | VARCHAR2(20) | Y |  | 产品成分Ca实绩 | SCO_DATA_DIC(D) |
| 17 | MG_RSLT | VARCHAR2(20) | Y |  | 产品成分Mg实绩 | SCO_DATA_DIC(D) |
| 18 | TE_RSLT | VARCHAR2(20) | Y |  | 产品成分Te实绩 | SCO_DATA_DIC(D) |
| 19 | BI_RSLT | VARCHAR2(20) | Y |  | 产品成分Bi实绩 | SCO_DATA_DIC(D) |
| 20 | SB_RSLT | VARCHAR2(20) | Y |  | 产品成分Sb实绩 | SCO_DATA_DIC(D) |
| 21 | ZN_RSLT | VARCHAR2(20) | Y |  | 产品成分Zn实绩 | SCO_DATA_DIC(D) |
| 22 | CFI_RSLT | VARCHAR2(20) | Y |  | 产品成分CFI计算值 | SCO_DATA_DIC(D) |
| 23 | CFJ_RSLT | VARCHAR2(20) | Y |  | 产品成分CFJ计算值 | SCO_DATA_DIC(D) |
| 24 | CFX_RSLT | VARCHAR2(20) | Y |  | 产品成分CFX计算值 | SCO_DATA_DIC(D) |
| 25 | PSR_RSLT | VARCHAR2(20) | Y |  | 产品成分PSR计算值 | SCO_DATA_DIC(D) |
| 26 | YSB1_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 27 | YSB2_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 28 | YSB3_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 29 | YSB4_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 30 | YSB5_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 31 | YSB6_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 32 | YSB7_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 33 | CSOL_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 34 | WLYS1_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 35 | WLYS2_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 36 | WLYS3_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 37 | WLYS4_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 38 | WLYS5_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 39 | WLYS6_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 40 | CEQ1_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 41 | CEQEXP_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 42 | CEVIIW_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 43 | CET_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 44 | CEQAWS_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 45 | CEQJIS_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 46 | WLYS7_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 47 | WLYS8_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 48 | WLYS9_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 49 | C_RSLT | VARCHAR2(20) | Y |  | 产品成分C实绩 | SCO_DATA_DIC(D) |
| 50 | SI_RSLT | VARCHAR2(20) | Y |  | 产品成分Si实绩 | SCO_DATA_DIC(D) |
| 51 | MN_RSLT | VARCHAR2(20) | Y |  | 产品成分Mn实绩 | SCO_DATA_DIC(D) |
| 52 | P_RSLT | VARCHAR2(20) | Y |  | 产品成分P实绩 | SCO_DATA_DIC(D) |
| 53 | S_RSLT | VARCHAR2(20) | Y |  | 产品成分S实绩 | SCO_DATA_DIC(D) |
| 54 | TOT_AL_RSLT | VARCHAR2(20) | Y |  | 实绩Tot_Al | SCO_DATA_DIC(D) |
| 55 | SOL_AL_RSLT | VARCHAR2(20) | Y |  | 实绩Sol_Al | SCO_DATA_DIC(D) |
| 56 | V_RSLT | VARCHAR2(20) | Y |  | 产品成分V实绩 | SCO_DATA_DIC(D) |
| 57 | N_RSLT | VARCHAR2(20) | Y |  | 产品成分N实绩 | SCO_DATA_DIC(D) |
| 58 | CU_RSLT | VARCHAR2(20) | Y |  | 产品成分Cu实绩 | SCO_DATA_DIC(D) |
| 59 | TI_RSLT | VARCHAR2(20) | Y |  | 产品成分Ti实绩 | SCO_DATA_DIC(D) |
| 60 | NI_RSLT | VARCHAR2(20) | Y |  | 产品成分Ni实绩 | SCO_DATA_DIC(D) |
| 61 | NB_RSLT | VARCHAR2(20) | Y |  | 产品成分Nb实绩 | SCO_DATA_DIC(D) |
| 62 | MO_RSLT | VARCHAR2(20) | Y |  | 产品成分Mo实绩 | SCO_DATA_DIC(D) |
| 63 | CR_RSLT | VARCHAR2(20) | Y |  | 产品成分Cr实绩 | SCO_DATA_DIC(D) |
| 64 | O_RSLT | VARCHAR2(20) | Y |  | 产品成分O实绩 | SCO_DATA_DIC(D) |
| 65 | CEQ_RSLT | VARCHAR2(20) | Y |  | 产品成分CEQ计算值 | SCO_DATA_DIC(D) |
| 66 | PCM_RSLT | VARCHAR2(20) | Y |  | 产品成分PCM计算值 | SCO_DATA_DIC(D) |
| 67 | B_RSLT | VARCHAR2(20) | Y |  | 产品成分B实绩 | SCO_DATA_DIC(D) |
| 68 | PCM_FML | VARCHAR2(2) | Y |  | PCM式 | SCO_DATA_DIC(D) |
| 69 | ESB_FLAG | VARCHAR2(1) | Y |  |  | 空 |
| 70 | ESB_DATE | VARCHAR2(14) | Y |  |  | 空 |
| 71 | PK_ID | VARCHAR2(45) | N | ✓ | Interface Primay Key ID | SCO_DATA_DIC(D) |
| 72 | PK_ID_D | VARCHAR2(60) | Y |  |  | 空 |

### SQM_WSP_MTC_COM_INF

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=24｜被读 8 过程 / 被写 8 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：2　**主键**：PK_ID　**语义覆盖**：46/61

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | MTC_NO | VARCHAR2(11) | N |  | 质保书号 | DB注释(中文) |
| 2 | MTC_STS | VARCHAR2(1) | N |  | C-Create，U-Update，D-Delete | DB注释(非中文) |
| 3 | MTC_DTM | VARCHAR2(14) | N |  | MES发送时间 | DB注释(中文) |
| 4 | MTC_TY | VARCHAR2(2) | Y |  | 质保书类型 | DB注释(中文) |
| 5 | PROD_GRP | VARCHAR2(2) | Y |  | 品种 | DB注释(中文) |
| 6 | PROD_CD | VARCHAR2(60) | Y |  | 产品名称 | DB注释(中文) |
| 7 | ORD_NO | VARCHAR2(10) | Y |  | 订单号 | DB注释(中文) |
| 8 | ORD_LN | VARCHAR2(3) | Y |  | 订单行号 | DB注释(中文) |
| 9 | CUST_NM | VARCHAR2(100) | Y |  | 客户 | DB注释(中文) |
| 10 | SPEC_CD | VARCHAR2(50) | Y |  | 技术条件 | DB注释(中文) |
| 11 | SERIAL_NO | VARCHAR2(50) | Y |  | 编码 | DB注释(中文) |
| 12 | DELIVERY | VARCHAR2(100) | Y |  | 交货状态 | DB注释(中文) |
| 13 | CONTRACT_NO | VARCHAR2(40) | Y |  | 合同号 | DB注释(中文) |
| 14 | INSP_MTC_NO1 | VARCHAR2(100) | Y |  | 认证证书号 | DB注释(中文) |
| 15 | INSP_MTC_NO2 | VARCHAR2(50) | Y |  | 检验证书号 | DB注释(中文) |
| 16 | INSP_AGENCY_CD | VARCHAR2(3) | Y |  | 检查机构代码 | DB注释(中文) |
| 17 | INSP_AGENCY_NM | VARCHAR2(50) | Y |  | 检查机构名称 | DB注释(中文) |
| 18 | MTC_REF_DESC1 | VARCHAR2(300) | Y |  | 质保书备注1 | DB注释(中文) |
| 19 | MTC_REF_DESC2 | VARCHAR2(300) | Y |  | 质保书备注2 | DB注释(中文) |
| 20 | MTC_REF_DESC3 | VARCHAR2(300) | Y |  | 质保书备注3 | DB注释(中文) |
| 21 | MARK_PROD_NM | VARCHAR2(60) | Y |  | 标记品名 | DB注释(中文) |
| 22 | CHECKER | VARCHAR2(50) | Y |  | 会验者 | DB注释(中文) |
| 23 | MTC_REMARK | VARCHAR2(300) | Y |  | 备注 | DB注释(中文) |
| 24 | COMMENTS_CHN | VARCHAR2(300) | Y |  | 备注中文 | DB注释(中文) |
| 25 | COMMENTS_ENG | VARCHAR2(300) | Y |  | 备注英文 | DB注释(中文) |
| 26 | LICENSE_UNDER | VARCHAR2(50) | Y |  | 二维码下内容 | DB注释(中文) |
| 27 | UNDER_CE | VARCHAR2(20) | Y |  | 图片下内容 | DB注释(中文) |
| 28 | ESB_FLAG | VARCHAR2(1) | Y |  | ESB使用传输标志(0:未处理1:已处理) | DB注释(中文) |
| 29 | ESB_DATE | VARCHAR2(14) | Y |  | ESB使用,同步时间 | DB注释(中文) |
| 30 | PK_ID | VARCHAR2(30) | N | ✓ | Interface Primay Key ID | SCO_DATA_DIC(D) |
| 31 | GRADE_CD | VARCHAR2(60) | Y |  | 牌号 | DB注释(中文) |
| 32 | TSL_YP_CD | VARCHAR2(60) | Y |  | 拉伸测试屈服强度类型 | SCO_DATA_DIC(D) |
| 33 | TSL_EL_CD | VARCHAR2(60) | Y |  | 拉伸测试伸长率类型 | SCO_DATA_DIC(D) |
| 34 | BEND_CD | VARCHAR2(60) | Y |  | 弯曲测试类型 | SCO_DATA_DIC(D) |
| 35 | BEND_UNIT | VARCHAR2(60) | Y |  | 弯曲测试单位 | SCO_DATA_DIC(D) |
| 36 | IMPACT_TEMP | VARCHAR2(60) | Y |  | 冲击测试温度 | SCO_DATA_DIC(D) |
| 37 | IMPACT_SIZE | VARCHAR2(60) | Y |  |  | 空 |
| 38 | IMPACT_DIRECTION | VARCHAR2(60) | Y |  |  | 空 |
| 39 | HARD_KIND | VARCHAR2(60) | Y |  | 硬度测试种类 | SCO_DATA_DIC(D) |
| 40 | DWTT_TEMP | VARCHAR2(60) | Y |  | DWTT | SCO_DATA_DIC(D) |
| 41 | ROUGH_KIND | VARCHAR2(60) | Y |  | 粗糙度测试种类 | SCO_DATA_DIC(D) |
| 42 | WAVIN_TY | VARCHAR2(60) | Y |  | 波纹度测试种类 | SCO_DATA_DIC(D) |
| 43 | TSL_CT_EX_RA_CD | VARCHAR2(60) | Y |  | 拉抻测试断后伸长率类型 | SCO_DATA_DIC(D) |
| 44 | HIGH_TEMP_TSL_YP_TY | VARCHAR2(60) | Y |  | 高温拉伸测试屈服强度类型 | SCO_DATA_DIC(D) |
| 45 | HIGH_TEMP_TSL_EL_CD | VARCHAR2(60) | Y |  | 高温拉伸测试伸长率类型 | SCO_DATA_DIC(D) |
| 46 | Z_TSL_CUT_GRT_CD | VARCHAR2(60) | Y |  |  | 空 |
| 47 | Z_TSL_YP_GRT_CD | VARCHAR2(60) | Y |  |  | 空 |
| 48 | Z_TSL_TS_GRT_CD | VARCHAR2(60) | Y |  |  | 空 |
| 49 | Z_TSL_CT_EX_RA_GRT_CD | VARCHAR2(60) | Y |  |  | 空 |
| 50 | IMPACT_ENERGY_CD | VARCHAR2(60) | Y |  | 冲击试样能量值类型 | SCO_DATA_DIC(D) |
| 51 | IMPACT1_TEMP | VARCHAR2(60) | Y |  |  | 空 |
| 52 | IMPACT1_SMP_SZ | VARCHAR2(60) | Y |  |  | 空 |
| 53 | IMPACT1_SMP_SPCMN_DIR | VARCHAR2(60) | Y |  |  | 空 |
| 54 | IMPACT1_ENERGY_CD | VARCHAR2(60) | Y |  | 冲击试验1试样能量值类型 | SCO_DATA_DIC(D) |
| 55 | Z1_TSL_CUT_GRT_CD | VARCHAR2(60) | Y |  |  | 空 |
| 56 | Z1_TSL_YP_GRT_CD | VARCHAR2(60) | Y |  |  | 空 |
| 57 | Z1_TSL_TS_GRT_CD | VARCHAR2(60) | Y |  |  | 空 |
| 58 | Z1_TSL_CT_EX_RA_GRT_CD | VARCHAR2(60) | Y |  |  | 空 |
| 59 | UST_STD_CD | VARCHAR2(60) | Y |  |  | 空 |
| 60 | PK_ID_D | VARCHAR2(60) | Y |  |  | 空 |
| 61 | CUST_CD | VARCHAR2(100) | Y |  | Customer No | SCO_DATA_DIC(D) |

### SQM_WSP_MTC_PROD_INF

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=24｜被读 8 过程 / 被写 8 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：4　**主键**：PK_ID　**语义覆盖**：24/26

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | MTC_NO | VARCHAR2(11) | N |  | 质量保证书编号 | DB注释(中文) |
| 2 | MTC_STS | VARCHAR2(1) | N |  | C-Create，U-Update，D-Delete | DB注释(非中文) |
| 3 | MTC_DTM | VARCHAR2(14) | N |  | MES发送时间 | DB注释(中文) |
| 4 | PROD_NO | VARCHAR2(18) | N |  | 产品编号 | DB注释(中文) |
| 5 | ORD_NO | VARCHAR2(10) | Y |  | 订单编号 | DB注释(中文) |
| 6 | ORD_LN | VARCHAR2(3) | Y |  | 订单行号 | DB注释(中文) |
| 7 | SMP_NO | VARCHAR2(14) | Y |  | 试样编号 | DB注释(中文) |
| 8 | LOT_NO | VARCHAR2(14) | Y |  | 批号 | DB注释(中文) |
| 9 | HEAT_NO | VARCHAR2(10) | Y |  | 炉次号 | DB注释(中文) |
| 10 | PROD_TOT_JDG_GRD | VARCHAR2(2) | Y |  | 产品综合判定等级 | DB注释(中文) |
| 11 | CHEM_JDG_GRD | VARCHAR2(1) | Y |  | 成分判定等级 | DB注释(中文) |
| 12 | MECH_JDG_GRD | VARCHAR2(1) | Y |  | 物性判定等级 | DB注释(中文) |
| 13 | APPR_JDG_GRD | VARCHAR2(1) | Y |  | 外观判定等级 | DB注释(中文) |
| 14 | ORD_PCS | NUMBER | Y |  | 订单张数 | DB注释(中文) |
| 15 | ORD_THK | NUMBER | Y |  | 订单厚度 | DB注释(中文) |
| 16 | ORD_WTH | NUMBER | Y |  | 订单宽度 | DB注释(中文) |
| 17 | ORD_LTH | NUMBER | Y |  | 订单长度 | DB注释(中文) |
| 18 | PROD_THK | NUMBER | Y |  | 产品厚度 | DB注释(中文) |
| 19 | PROD_WTH | NUMBER | Y |  | 产品宽度 | DB注释(中文) |
| 20 | PROD_LTH | NUMBER | Y |  | 产品长度 | DB注释(中文) |
| 21 | PROD_WGT | NUMBER | Y |  | 产品重量 | DB注释(中文) |
| 22 | UST_GRD | VARCHAR2(1) | Y |  | 探伤实际等级 | DB注释(中文) |
| 23 | ESB_FLAG | VARCHAR2(1) | Y |  |  | 空 |
| 24 | ESB_DATE | NUMBER | Y |  | 产品数量 | DB注释(中文) |
| 25 | PK_ID | VARCHAR2(50) | N | ✓ | Interface Primay Key ID | SCO_DATA_DIC(D) |
| 26 | PK_ID_D | VARCHAR2(60) | Y |  |  | 空 |

### SQM_ORD_PROS_PLM

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=23｜被读 19 过程 / 被写 2 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：8387　**主键**：ORD_NO、ORD_LN　**语义覆盖**：192/208

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 修改人 | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | 修改时间 | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | ORD_NO | VARCHAR2(10) | N | ✓ | 订单编号 | DB注释(中文) |
| 9 | ORD_LN | VARCHAR2(3) | N | ✓ | 订单行号 | DB注释(中文) |
| 10 | INCMP_STEEL_GRD | VARCHAR2(10) | N |  | 炼钢内控钢种编号 | DB注释(中文) |
| 11 | SMS_2ND_RFN_CD | VARCHAR2(3) | Y |  | 炼钢2次精炼代码 | DB注释(中文) |
| 12 | SECOND_RFN_PROC_TY | VARCHAR2(1) | Y |  | 2次精炼工序分类 | DB注释(中文) |
| 13 | SECOND_RFN_TIME_TY | VARCHAR2(1) | Y |  | 2次精炼时间分类 | DB注释(中文) |
| 14 | TAP_TEMP_AIM | NUMBER | Y |  | 出钢温度目标值 | DB注释(中文) |
| 15 | LF_DEP_TEMP_AIM | NUMBER | Y |  | 炼钢LF出发温度目标值 | DB注释(中文) |
| 16 | RH_DEP_TEMP_AIM | NUMBER | Y |  | 炼钢RH出发温度目标值 | DB注释(中文) |
| 17 | SMS_END_O2_CONT_TY | NUMBER | Y |  | 炼钢终点O2含量分类 | DB注释(中文) |
| 18 | SMS_END_C_CONT_TY | NUMBER | Y |  | 炼钢终点C含量分类 | DB注释(中文) |
| 19 | SMS_SLAG_DBL_TY | VARCHAR2(1) | Y |  | 炼钢是否双渣操作分类 | DB注释(中文) |
| 20 | SMS_END_DEOXI_MTH | VARCHAR2(1) | Y |  | 炼钢终点脱氧方式 | DB注释(中文) |
| 21 | SLAG_STOP_MTH | VARCHAR2(1) | Y |  | 挡渣方式 | DB注释(中文) |
| 22 | SMS_TAP_TIME_TY | VARCHAR2(1) | Y |  | 转炉出钢时间分类 | DB注释(中文) |
| 23 | DE_P_YN | VARCHAR2(1) | Y |  | 脱磷作业分类 | DB注释(中文) |
| 24 | RH_TREAT_TIME_TY | VARCHAR2(1) | Y |  | 真空处理时间分类 | DB注释(中文) |
| 25 | RH_DEGAS_TIME_TY | VARCHAR2(1) | Y |  | 纯脱气时间分类 | DB注释(中文) |
| 26 | RH_VACUM_REQ_TY | VARCHAR2(1) | Y |  | 真空度要求分类 | DB注释(中文) |
| 27 | SECOND_AR_TIME_TY | VARCHAR2(1) | Y |  | 吹氩时间分类 | DB注释(中文) |
| 28 | SECOND_CA_TREAT_TY | VARCHAR2(1) | Y |  | 精炼Ca处理分类 | DB注释(中文) |
| 29 | CC_LADLE_STR_TY | VARCHAR2(1) | Y |  | 大包开始分类 | DB注释(中文) |
| 30 | TD_OPEN_POUR_TY | VARCHAR2(1) | Y |  | 敞浇分类 | DB注释(中文) |
| 31 | CAST_DIFF_STL_MIX_TY | VARCHAR2(1) | Y |  | 混浇分类 | DB注释(中文) |
| 32 | TD_STEEL_TEMP_MIN | NUMBER | Y |  | 中间包钢水温度下限值 | DB注释(中文) |
| 33 | TD_STEEL_TEMP_MAX | NUMBER | Y |  | 中间包钢水温度上限值 | DB注释(中文) |
| 34 | SLAB_CAST_SPD_MIN | NUMBER | Y |  | SlabSpeed下限值 | DB注释(中文) |
| 35 | SLAB_CAST_SPD_MAX | NUMBER | Y |  | SlabSpeed上限值 | DB注释(中文) |
| 36 | MOLD_LVL_FLUCT_TY | VARCHAR2(1) | Y |  | 结晶器液面波动分类 | DB注释(中文) |
| 37 | SLAB_INQLT_REQ_TY | VARCHAR2(1) | Y |  | 铸坯内部质量要求 | DB注释(中文) |
| 38 | TD_MIN_SMS_WGT | NUMBER | Y |  | 中包最低吨位 | DB注释(中文) |
| 39 | TD_SLAG_THK_TY | VARCHAR2(1) | Y |  | 中包渣层厚度分类 | DB注释(中文) |
| 40 | MOLD_POWDER_TY | VARCHAR2(1) | Y |  | 保护渣类型 | DB注释(中文) |
| 41 | MOLD_OSCIL_TY | VARCHAR2(1) | Y |  | 振动类型 | DB注释(中文) |
| 42 | CC_CB_REPAIR_TY | VARCHAR2(1) | Y |  | 铸坯处理方法 | DB注释(中文) |
| 43 | CC_CB_COOL_TY | VARCHAR2(1) | Y |  | 铸坯冷却方式 | DB注释(中文) |
| 44 | CC_CB_COOL_TIME_TY | VARCHAR2(1) | Y |  | 铸坯冷却时间分类 | DB注释(中文) |
| 45 | CC_CB_RESTR_CD | VARCHAR2(1) | Y |  | 铸坯使用限制代码 | DB注释(中文) |
| 46 | TAP_TEMP_MIN | NUMBER | Y |  | 出钢温度下限值 | SCO_DATA_DIC(D) |
| 47 | TAP_TEMP_MAX | NUMBER | Y |  | 出钢温度上限值 | SCO_DATA_DIC(D) |
| 48 | SLAG_THK_TY | VARCHAR2(1) | Y |  | 下渣厚度 | SCO_DATA_DIC(D) |
| 49 | CAS_TREAT_TIME | NUMBER | Y |  | CAS软吹时间 | SCO_DATA_DIC(D) |
| 50 | LF_HEAT_TIME | NUMBER | Y |  | LF加热时间 | SCO_DATA_DIC(D) |
| 51 | LF_TREAT_TIME | NUMBER | Y |  | LF软吹时间 | SCO_DATA_DIC(D) |
| 52 | LF_DEPART_S | NUMBER | Y |  | LF出站S含量 | SCO_DATA_DIC(D) |
| 53 | RH_DE_C_TIME_MIN | NUMBER | Y |  | RH脱碳时间下限 | SCO_DATA_DIC(D) |
| 54 | RH_DE_C_TIME_MAX | NUMBER | Y |  | RH脱碳时间上限 | SCO_DATA_DIC(D) |
| 55 | RH_DEGAS_TIME | NUMBER | Y |  | RH纯脱气时间 | SCO_DATA_DIC(D) |
| 56 | RH_TREAT_TIME | NUMBER | Y |  | RH软吹时间 | SCO_DATA_DIC(D) |
| 57 | RH_VACUM_VAL | NUMBER | Y |  | RH真空度 | SCO_DATA_DIC(D) |
| 58 | WAVE_STATUS_SPD | NUMBER | Y |  | 稳态拉速波动 | SCO_DATA_DIC(D) |
| 59 | CC_CB_SEG | VARCHAR2(1) | Y |  | 铸坯中心偏析 | SCO_DATA_DIC(D) |
| 60 | CC_CB_PRST | VARCHAR2(1) | Y |  | 铸坯中心疏松 | SCO_DATA_DIC(D) |
| 61 | CC_CB_CRACK | NUMBER | Y |  | 铸坯内部裂纹 | SCO_DATA_DIC(D) |
| 62 | CC_CB_QL_OTHER | NUMBER | Y |  | 铸坯内部质量其他 | SCO_DATA_DIC(D) |
| 63 | TD_SLAG_THK | NUMBER | Y |  | 中包渣层厚度 | SCO_DATA_DIC(D) |
| 64 | QLT_HCR_TY | VARCHAR2(1) | Y |  | 质量设计热装分类(HCR) | DB注释(中文) |
| 65 | PLT_PR_HEAT_AIM | NUMBER | Y |  | 预热段目标 | DB注释(中文) |
| 66 | PLT_RF_STR1_AIM | NUMBER | Y |  | 加热一段目标 | DB注释(中文) |
| 67 | PLT_RF_STR2_AIM | NUMBER | Y |  | 加热二段目标 | DB注释(中文) |
| 68 | PLT_RF_PREH_AIM | NUMBER | Y |  | 均热段目标 | DB注释(中文) |
| 69 | PLT_RF_HOLDING_TIME_MAX | NUMBER | Y |  | 铸坯在炉时间上限 | DB注释(中文) |
| 70 | PLT_RF_HOLDING_TIME_MIN | NUMBER | Y |  | 铸坯在炉时间下限 | DB注释(中文) |
| 71 | PLT_RF_HOLDING_TIME_AIM | NUMBER | Y |  | 铸坯在炉时间目标 | DB注释(中文) |
| 72 | PLT_RF_EXT_TEMP_MAX | NUMBER | Y |  | 铸坯出炉温度上限 | DB注释(中文) |
| 73 | PLT_RF_EXT_TEMP_MIN | NUMBER | Y |  | 铸坯出炉温度下限 | DB注释(中文) |
| 74 | PLT_RF_EXT_TEMP_AIM | NUMBER | Y |  | 铸坯出炉温度目标 | DB注释(中文) |
| 75 | PLT_DES_SLAB_TEMP_MAX | NUMBER | Y |  | 除鳞后铸坯表面温度上限 | DB注释(中文) |
| 76 | PLT_DES_SLAB_TEMP_MIN | NUMBER | Y |  | 除鳞后铸坯表面温度下限 | DB注释(中文) |
| 77 | PLT_DES_SLAB_TEMP_AIM | NUMBER | Y |  | 除鳞后铸坯表面温度目标 | DB注释(中文) |
| 78 | PLT_1RM_ST_TEMP_MAX | NUMBER | Y |  | M43_粗轧开轧温度上限 | DB注释(中文) |
| 79 | PLT_1RM_ST_TEMP_MIN | NUMBER | Y |  | M43_粗轧开轧温度下限 | DB注释(中文) |
| 80 | PLT_1RM_ST_TEMP_AIM | NUMBER | Y |  | M43_粗轧开轧温度目标 | DB注释(中文) |
| 81 | PLT_1RM_FSH_TEMP_MAX | NUMBER | Y |  | M43_粗轧终轧温度上限 | DB注释(中文) |
| 82 | PLT_1RM_FSH_TEMP_MIN | NUMBER | Y |  | M43_粗轧终轧温度下限 | DB注释(中文) |
| 83 | PLT_1RM_FSH_TEMP_AIM | NUMBER | Y |  | M43_粗轧终轧温度目标 | DB注释(中文) |
| 84 | PLT_1_SLAB_PROD_RATE | NUMBER | Y |  | M43_中间坯/成品厚度倍数目标值 | DB注释(中文) |
| 85 | PLT_1FM_ST_TEMP_MAX | NUMBER | Y |  | M43_精轧开轧温度上限 | DB注释(中文) |
| 86 | PLT_1FM_ST_TEMP_MIN | NUMBER | Y |  | M43_精轧开轧温度下限 | DB注释(中文) |
| 87 | PLT_1FM_ST_TEMP_AIM | NUMBER | Y |  | M43_精轧开轧温度目标 | DB注释(中文) |
| 88 | PLT_1FM_FSH_TEMP_MAX | NUMBER | Y |  | M43_精轧终轧温度上限 | DB注释(中文) |
| 89 | PLT_1FM_FSH_TEMP_MIN | NUMBER | Y |  | M43_精轧终轧温度下限 | DB注释(中文) |
| 90 | PLT_1FM_FSH_TEMP_AIM | NUMBER | Y |  | M43_精轧终轧温度目标 | DB注释(中文) |
| 91 | PLT_1COOL_CD | VARCHAR2(1) | Y |  | M43_冷却模式 | DB注释(中文) |
| 92 | PLT_1ACC_COOL_ST_TEMP_MAX | NUMBER | Y |  | M43_ACC开冷温度上限 | DB注释(中文) |
| 93 | PLT_1ACC_COOL_ST_TEMP_MIN | NUMBER | Y |  | M43_ACC开冷温度下限 | DB注释(中文) |
| 94 | PLT_1ACC_COOL_ST_TEMP_AIM | NUMBER | Y |  | M43_ACC开冷温度目标 | DB注释(中文) |
| 95 | PLT_1ACC_COOL_FSH_TEMP_MAX | NUMBER | Y |  | M43_ACC终冷温度上限 | DB注释(中文) |
| 96 | PLT_1ACC_COOL_FSH_TEMP_MIN | NUMBER | Y |  | M43_ACC终冷温度下限 | DB注释(中文) |
| 97 | PLT_1ACC_COOL_FSH_TEMP_AIM | NUMBER | Y |  | M43_ACC终冷温度目标 | DB注释(中文) |
| 98 | PLT_1ACC_COOL_SPD_MAX | NUMBER | Y |  | M43_ACC冷却速度上限 | DB注释(中文) |
| 99 | PLT_1ACC_COOL_SPD_MIN | NUMBER | Y |  | M43_ACC冷却速度下限 | DB注释(中文) |
| 100 | PLT_1ACC_COOL_SPD_AIM | NUMBER | Y |  | M43_ACC冷却速度目标 | DB注释(中文) |
| 101 | PLT_1DQ_COOL_ST_TEMP_MAX | NUMBER | Y |  | M43_DQ开冷温度上限 | DB注释(中文) |
| 102 | PLT_1DQ_COOL_ST_TEMP_MIN | NUMBER | Y |  | M43_DQ开冷温度下限 | DB注释(中文) |
| 103 | PLT_1DQ_COOL_ST_TEMP_AIM | NUMBER | Y |  | M43_DQ开冷温度目标 | DB注释(中文) |
| 104 | PLT_1DQ_COOL_FSH_TEMP_MAX | NUMBER | Y |  | M43_DQ终冷温度上限 | DB注释(中文) |
| 105 | PLT_1DQ_COOL_FSH_TEMP_MIN | NUMBER | Y |  | M43_DQ终冷温度下限 | DB注释(中文) |
| 106 | PLT_1DQ_COOL_FSH_TEMP_AIM | NUMBER | Y |  | M43_DQ终冷温度目标 | DB注释(中文) |
| 107 | PLT_1DQ_COOL_SPD_MAX | NUMBER | Y |  | M43_DQ冷却速度上限 | DB注释(中文) |
| 108 | PLT_1DQ_COOL_SPD_MIN | NUMBER | Y |  | M43_DQ冷却速度下限 | DB注释(中文) |
| 109 | PLT_1DQ_COOL_SPD_AIM | NUMBER | Y |  | M43_DQ冷却速度目标 | DB注释(中文) |
| 110 | PLT_1OSC_COOL_ST_TEMP_MAX | NUMBER | Y |  | M43_OSC开冷温度上限 | DB注释(中文) |
| 111 | PLT_1OSC_COOL_ST_TEMP_MIN | NUMBER | Y |  | M43_OSC开冷温度下限 | DB注释(中文) |
| 112 | PLT_1OSC_COOL_ST_TEMP_AIM | NUMBER | Y |  | M43_OSC开冷温度目标 | DB注释(中文) |
| 113 | PLT_1OSC_COOL_FSH_TEMP_MAX | NUMBER | Y |  | M43_OSC终冷温度上限 | DB注释(中文) |
| 114 | PLT_1OSC_COOL_FSH_TEMP_MIN | NUMBER | Y |  | M43_OSC终冷温度下限 | DB注释(中文) |
| 115 | PLT_1OSC_COOL_FSH_TEMP_AIM | NUMBER | Y |  | M43_OSC终冷温度目标 | DB注释(中文) |
| 116 | PLT_1OSC_COOL_SPD_MAX | NUMBER | Y |  | M43_OSC冷却速度上限 | DB注释(中文) |
| 117 | PLT_1OSC_COOL_SPD_MIN | NUMBER | Y |  | M43_OSC冷却速度下限 | DB注释(中文) |
| 118 | PLT_1OSC_COOL_SPD_AIM | NUMBER | Y |  | M43_OSC冷却速度目标 | DB注释(中文) |
| 119 | PLT_STG1_ST_TEMP_MAX | NUMBER | Y |  | M34_第一阶段开轧温度上限 | DB注释(中文) |
| 120 | PLT_STG1_ST_TEMP_MIN | NUMBER | Y |  | M34_第一阶段开轧温度下限 | DB注释(中文) |
| 121 | PLT_STG1_ST_TEMP_AIM | NUMBER | Y |  | M34_第一阶段开轧温度目标 | DB注释(中文) |
| 122 | PLT_STG1_FSH_TEMP_MAX | NUMBER | Y |  | M34_第一阶段终轧温度上限 | DB注释(中文) |
| 123 | PLT_STG1_FSH_TEMP_MIN | NUMBER | Y |  | M34_第一阶段终轧温度下限 | DB注释(中文) |
| 124 | PLT_STG1_FSH_TEMP_AIM | NUMBER | Y |  | M34_第一阶段终轧温度目标 | DB注释(中文) |
| 125 | PLT_2_SLAB_PROD_RATE | NUMBER | Y |  | M34_中间坯/成品厚度倍数值目标值 | DB注释(中文) |
| 126 | PLT_STG2_ST_TEMP_MAX | NUMBER | Y |  | M34_第二阶段开轧温度上限 | DB注释(中文) |
| 127 | PLT_STG2_ST_TEMP_MIN | NUMBER | Y |  | M34_第二阶段开轧温度下限 | DB注释(中文) |
| 128 | PLT_STG2_ST_TEMP_AIM | NUMBER | Y |  | M34_第二阶段开轧温度目标 | DB注释(中文) |
| 129 | PLT_BEF_COIL_TEMP_MAX | NUMBER | Y |  | M34_机前卷曲炉温度上限 | DB注释(中文) |
| 130 | PLT_BEF_COIL_TEMP_MIN | NUMBER | Y |  | M34_机前卷曲炉温度下限 | DB注释(中文) |
| 131 | PLT_BEF_COIL_TEMP_AIM | NUMBER | Y |  | M34_机前卷曲炉温度目标 | DB注释(中文) |
| 132 | PLT_AFT_COIL_TEMP_MAX | NUMBER | Y |  | M34_机后卷曲炉温度上限 | DB注释(中文) |
| 133 | PLT_AFT_COIL_TEMP_MIN | NUMBER | Y |  | M34_机后卷曲炉温度下限 | DB注释(中文) |
| 134 | PLT_AFT_COIL_TEMP_AIM | NUMBER | Y |  | M34_机后卷曲炉温度目标 | DB注释(中文) |
| 135 | PLT_STG2_FSH_TEMP_MAX | NUMBER | Y |  | M34_第二阶段终轧温度上限 | DB注释(中文) |
| 136 | PLT_STG2_FSH_TEMP_MIN | NUMBER | Y |  | M34_第二阶段终轧温度下限 | DB注释(中文) |
| 137 | PLT_STG2_FSH_TEMP_AIM | NUMBER | Y |  | M34_第二阶段终轧温度目标 | DB注释(中文) |
| 138 | PLT_2COOL_CD | VARCHAR2(1) | Y |  | M34_冷却模式 | DB注释(中文) |
| 139 | PLT_2ACC_COOL_ST_TEMP_MAX | NUMBER | Y |  | M34_ACC开冷温度上限 | DB注释(中文) |
| 140 | PLT_2ACC_COOL_ST_TEMP_MIN | NUMBER | Y |  | M34_ACC开冷温度下限 | DB注释(中文) |
| 141 | PLT_2ACC_COOL_ST_TEMP_AIM | NUMBER | Y |  | M34_ACC开冷温度目标 | DB注释(中文) |
| 142 | PLT_2ACC_COOL_FSH_TEMP_MAX | NUMBER | Y |  | M34_ACC终冷温度上限 | DB注释(中文) |
| 143 | PLT_2ACC_COOL_FSH_TEMP_MIN | NUMBER | Y |  | M34_ACC终冷温度下限 | DB注释(中文) |
| 144 | PLT_2ACC_COOL_FSH_TEMP_AIM | NUMBER | Y |  | M34_ACC终冷温度目标 | DB注释(中文) |
| 145 | PLT_2ACC_COOL_SPD_MAX | NUMBER | Y |  | M34_ACC冷却速度上限 | DB注释(中文) |
| 146 | PLT_2ACC_COOL_SPD_MIN | NUMBER | Y |  | M34_ACC冷却速度下限 | DB注释(中文) |
| 147 | PLT_2ACC_COOL_SPD_AIM | NUMBER | Y |  | M34_ACC冷却速度目标 | DB注释(中文) |
| 148 | PLT_2UFC_COOL_ST_TEMP_MAX | NUMBER | Y |  | M34_UFC开冷温度上限 | DB注释(中文) |
| 149 | PLT_2UFC_COOL_ST_TEMP_MIN | NUMBER | Y |  | M34_UFC开冷温度下限 | DB注释(中文) |
| 150 | PLT_2UFC_COOL_ST_TEMP_AIM | NUMBER | Y |  | M34_UFC开冷温度目标 | DB注释(中文) |
| 151 | PLT_2UFC_COOL_FSH_TEMP_MAX | NUMBER | Y |  | M34_UFC终冷温度上限 | DB注释(中文) |
| 152 | PLT_2UFC_COOL_FSH_TEMP_MIN | NUMBER | Y |  | M34_UFC终冷温度下限 | DB注释(中文) |
| 153 | PLT_2UFC_COOL_FSH_TEMP_AIM | NUMBER | Y |  | M34_UFC终冷温度目标 | DB注释(中文) |
| 154 | PLT_2UFC_COOL_SPD_MAX | NUMBER | Y |  | M34_UFC冷却速度上限 | DB注释(中文) |
| 155 | PLT_2UFC_COOL_SPD_MIN | NUMBER | Y |  | M34_UFC冷却速度下限 | DB注释(中文) |
| 156 | PLT_2UFC_COOL_SPD_AIM | NUMBER | Y |  | M34_UFC冷却速度目标 | DB注释(中文) |
| 157 | PLT_2OSC_COOL_ST_TEMP_MAX | NUMBER | Y |  | M34_OSC开冷温度上限 | DB注释(中文) |
| 158 | PLT_2OSC_COOL_ST_TEMP_MIN | NUMBER | Y |  | M34_OSC开冷温度下限 | DB注释(中文) |
| 159 | PLT_2OSC_COOL_ST_TEMP_AIM | NUMBER | Y |  | M34_OSC开冷温度目标 | DB注释(中文) |
| 160 | PLT_2OSC_COOL_FSH_TEMP_MAX | NUMBER | Y |  | M34_OSC终冷温度上限 | DB注释(中文) |
| 161 | PLT_2OSC_COOL_FSH_TEMP_MIN | NUMBER | Y |  | M34_OSC终冷温度下限 | DB注释(中文) |
| 162 | PLT_2OSC_COOL_FSH_TEMP_AIM | NUMBER | Y |  | M34_OSC终冷温度目标 | DB注释(中文) |
| 163 | PLT_2OSC_COOL_SPD_MAX | NUMBER | Y |  | M34_OSC冷却速度上限 | DB注释(中文) |
| 164 | PLT_2OSC_COOL_SPD_MIN | NUMBER | Y |  | M34_OSC冷却速度下限 | DB注释(中文) |
| 165 | PLT_2OSC_COOL_SPD_AIM | NUMBER | Y |  | M34_OSC冷却速度目标 | DB注释(中文) |
| 166 | PLT_HEATING_CD | VARCHAR2(1) | Y |  | 热处理方式 | DB注释(中文) |
| 167 | PLT_HTM_QC_TEMP_MAX | NUMBER | Y |  | 淬火温度上限 | DB注释(中文) |
| 168 | PLT_HTM_QC_TEMP_MIN | NUMBER | Y |  | 淬火温度下限 | DB注释(中文) |
| 169 | PLT_HTM_QC_TEMP_AIM | NUMBER | Y |  | 淬火温度目标 | DB注释(中文) |
| 170 | PLT_HTM_NR_TEMP_MAX | NUMBER | Y |  | 正火温度上限 | DB注释(中文) |
| 171 | PLT_HTM_NR_TEMP_MIN | NUMBER | Y |  | 正火温度下限 | DB注释(中文) |
| 172 | PLT_HTM_NR_TEMP_AIM | NUMBER | Y |  | 正火温度目标 | DB注释(中文) |
| 173 | PLT_HTM_TP_TEMP_MAX | NUMBER | Y |  | 回火温度上限 | DB注释(中文) |
| 174 | PLT_HTM_TP_TEMP_MIN | NUMBER | Y |  | 回火温度下限 | DB注释(中文) |
| 175 | PLT_HTM_TP_TEMP_AIM | NUMBER | Y |  | 回火温度目标 | DB注释(中文) |
| 176 | PLT_HTM_TIME_AIM_RATE | NUMBER | Y |  | 热处理时间目标系数 | DB注释(中文) |
| 177 | PLT_WARM_AIM_TIME | NUMBER | Y |  | 保温目标时间 | DB注释(中文) |
| 178 | PLT_PROD_THK_AIM | NUMBER | Y |  | 产品目标厚度 | DB注释(中文) |
| 179 | PLT_PROD_THK_RNG_MIN | NUMBER | Y |  | 产品厚度范围下限 | DB注释(中文) |
| 180 | PLT_PROD_THK_RNG_MAX | NUMBER | Y |  | 产品厚度范围上限 | DB注释(中文) |
| 181 | PLT_PROD_WTH_AIM | NUMBER | Y |  | 产品目标宽度 | DB注释(中文) |
| 182 | PLT_PROD_WTH_RNG_MIN | NUMBER | Y |  | 产品宽度范围下限 | DB注释(中文) |
| 183 | PLT_PROD_WTH_RNG_MAX | NUMBER | Y |  | 产品宽度范围上限 | DB注释(中文) |
| 184 | PLT_PROD_LTH_AIM | NUMBER | Y |  | 产品目标长度 | DB注释(中文) |
| 185 | PLT_PROD_LTH_RNG_MIN | NUMBER | Y |  | 产品长度范围下限 | DB注释(中文) |
| 186 | PLT_PROD_LTH_RNG_MAX | NUMBER | Y |  | 产品长度范围上限 | DB注释(中文) |
| 187 | PLT_THK_AIM | NUMBER | Y |  | PLT_WTH_AIM | SCO_DATA_DIC(D) |
| 188 | PLT_WTH_AIM | NUMBER | Y |  |  | 空 |
| 189 | PLT_WTH_TOL_MIN | NUMBER | Y |  |  | 空 |
| 190 | PLT_WTH_TOL_MAX | NUMBER | Y |  |  | 空 |
| 191 | PLT_THK_TOL_MIN | NUMBER | Y |  |  | 空 |
| 192 | PLT_THK_TOL_MAX | NUMBER | Y |  |  | 空 |
| 193 | PLT_CROWN_AIM | NUMBER | Y |  | Crown目标 | SCO_DATA_DIC(D) |
| 194 | PLT_CROWN_TOL_MIN | NUMBER | Y |  |  | 空 |
| 195 | PLT_CROWN_TOL_MAX | NUMBER | Y |  |  | 空 |
| 196 | PLT_FLAT_AIM | NUMBER | Y |  |  | 空 |
| 197 | PLT_FLAT_TOL_MIN | NUMBER | Y |  |  | 空 |
| 198 | PLT_FLAT_TOL_MAX | NUMBER | Y |  |  | 空 |
| 199 | PLT_WDG_AIM | NUMBER | Y |  |  | 空 |
| 200 | PLT_WDG_TOL_MIN | NUMBER | Y |  |  | 空 |
| 201 | PLT_WDG_TOL_MAX | NUMBER | Y |  |  | 空 |
| 202 | PLT_ASY_FLAT_TOL_MIN | NUMBER | Y |  |  | 空 |
| 203 | PLT_ASY_FLAT_AIM | NUMBER | Y |  |  | 空 |
| 204 | PLT_ASY_FLAT_TOL_MAX | NUMBER | Y |  |  | 空 |
| 205 | UST_MTH_CD | VARCHAR2(2) | Y |  | UST Method Code | SCO_DATA_DIC(D) |
| 206 | CUT_MTH_CD | VARCHAR2(1) | Y |  | Cutting Method | SCO_DATA_DIC(D) |
| 207 | INTO_SMS_TEMP | NUMBER | Y |  | 钢坯入炉温度要求 | DB注释(中文) |
| 208 | SMS_THREE_COLD_TY | VARCHAR2(1) | Y |  | 铸坯是否三冷 | DB注释(中文) |

### SQM_SC_MECH_RSLT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=23｜被读 19 过程 / 被写 2 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：0　**主键**：SMP_NO、SMP_LTH_LOC、TEST_CNT　**语义覆盖**：730/998

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | SMP_NO | VARCHAR2(14) | N | ✓ | 试样编号 | DB注释(中文) |
| 9 | SMP_LTH_LOC | VARCHAR2(1) | N | ✓ | 试样采取位置 | DB注释(中文) |
| 10 | TEST_CNT | NUMBER | N | ✓ | 试验回数 | DB注释(中文) |
| 11 | MECH_RSLT_REG_FST_DTM | VARCHAR2(14) | Y |  | 材质实绩录入最初时间 | DB注释(中文) |
| 12 | MECH_RSLT_REG_LST_DTM | VARCHAR2(14) | Y |  | 材质实绩录入最终时间 | DB注释(中文) |
| 13 | PROD_CHEM_RSLT_REG_DTM | VARCHAR2(14) | Y |  | 产品成分实绩登记时间 | DB注释(中文) |
| 14 | SMP_GTH_INST_MTRL_NO | VARCHAR2(20) | Y |  | 试样采取指示材料编号 | DB注释(中文) |
| 15 | SMP_HTM_ASGN_TY | VARCHAR2(1) | Y |  | 试样热处理指定分类 | DB注释(中文) |
| 16 | MECH_JDG_GRD | VARCHAR2(1) | Y |  | 物性判定等级 | DB注释(中文) |
| 17 | TSL_YP_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度类型 | DB注释(中文) |
| 18 | TSL_YP_RSLT | NUMBER | Y |  | 拉伸测试屈服强度实绩 | DB注释(中文) |
| 19 | TSL_YP_JDG | VARCHAR2(1) | Y |  | 拉伸测试屈服强度判定 | DB注释(中文) |
| 20 | TSL_TS_RSLT | NUMBER | Y |  | 拉伸测试抗拉强度实绩 | DB注释(中文) |
| 21 | TSL_TS_JDG | VARCHAR2(1) | Y |  | 拉伸测试抗拉强度判定 | DB注释(中文) |
| 22 | TSL_YP_TS_RSLT | NUMBER | Y |  | 拉伸试验屈强比YP/TS实绩 | DB注释(中文) |
| 23 | TSL_YP_TS_JDG | VARCHAR2(1) | Y |  | 拉伸试验屈强比YP/TS判定 | DB注释(中文) |
| 24 | TSL_RT05_RM_RSLT | NUMBER | Y |  | 拉伸试验屈强比Rt0.5/Rm实绩 | DB注释(中文) |
| 25 | TSL_RT05_RM_JDG | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt0.5/Rm判定 | DB注释(中文) |
| 26 | TSL_RT15_RT05_RSLT | NUMBER | Y |  | 拉伸试验屈强比Rt1.5/Rt0.5实绩 | DB注释(中文) |
| 27 | TSL_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt1.5/Rt0.5判定 | DB注释(中文) |
| 28 | TSL_RT20_RT10_RSLT | NUMBER | Y |  | 拉伸试验屈强比Rt2.0/Rt1.0实绩 | DB注释(中文) |
| 29 | TSL_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt2.0/Rt1.0判定 | DB注释(中文) |
| 30 | TSL_RT50_RT10_RSLT | NUMBER | Y |  | 拉伸试验屈强比Rt5.0/Rt1.0实绩 | DB注释(中文) |
| 31 | TSL_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 拉伸试验屈强比Rt5.0/Rt1.0判定 | DB注释(中文) |
| 32 | TSL_CT_EX_RA_RSLT | NUMBER | Y |  | 拉抻测试断后伸长率实绩 | DB注释(中文) |
| 33 | TSL_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 拉抻测试断后伸长率类型 | DB注释(中文) |
| 34 | TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 拉抻测试断后伸长率判定 | DB注释(中文) |
| 35 | TSL_CT_RA_RSLT | NUMBER | Y |  | 拉伸试验均匀伸长率实绩 | DB注释(中文) |
| 36 | TSL_CT_RA_JDG | VARCHAR2(1) | Y |  | 拉伸试验均匀伸长率判定 | DB注释(中文) |
| 37 | TSL_RA_RSLT | NUMBER | Y |  | 拉伸测试断面收缩率实绩 | SCO_DATA_DIC(D) |
| 38 | TSL_RA_JDG | VARCHAR2(1) | Y |  | 拉伸测试断面收缩率判定 | SCO_DATA_DIC(D) |
| 39 | TSL_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 消应力处理_保温温度实绩 | SCO_DATA_DIC(D) |
| 40 | TSL_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 消应力处理_保温时间实绩 | SCO_DATA_DIC(D) |
| 41 | TSL_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 消应力处理_冷却方式 | SCO_DATA_DIC(D) |
| 42 | TSL_STRESS_JDG | VARCHAR2(1) | Y |  | 消应力处理_判定 | SCO_DATA_DIC(D) |
| 43 | IMPACT_TEMP_RSLT | NUMBER | Y |  | 冲击测试温度实绩 | SCO_DATA_DIC(D) |
| 44 | IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 冲击测试缺口类型 | SCO_DATA_DIC(D) |
| 45 | IMPACT_ENERGY_CD | VARCHAR2(1) | Y |  | 冲击试样能量值类型 | SCO_DATA_DIC(D) |
| 46 | IMPACT_AVG_RSLT | NUMBER | Y |  | 冲击试验平均实绩 | SCO_DATA_DIC(D) |
| 47 | IMPACT_IND_RSLT1 | NUMBER | Y |  | 冲击功单个实绩1 | SCO_DATA_DIC(D) |
| 48 | IMPACT_IND_RSLT2 | NUMBER | Y |  | 冲击功单个实绩2 | SCO_DATA_DIC(D) |
| 49 | IMPACT_IND_RSLT3 | NUMBER | Y |  | 冲击功单个实绩3 | SCO_DATA_DIC(D) |
| 50 | IMPACT_IND_JDG | VARCHAR2(1) | Y |  | 冲击功单个判定 | SCO_DATA_DIC(D) |
| 51 | IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 冲击测试纤维断面率平均实绩 | SCO_DATA_DIC(D) |
| 52 | IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩1 | SCO_DATA_DIC(D) |
| 53 | IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩2 | SCO_DATA_DIC(D) |
| 54 | IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩3 | SCO_DATA_DIC(D) |
| 55 | IMPACT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 冲击测试纤维断面率개개判定 | SCO_DATA_DIC(D) |
| 56 | IMPACT_SMP_AVG_RSLT | NUMBER | Y |  | 冲击试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 57 | IMPACT_SMP_IND_RSLT1 | NUMBER | Y |  | 冲击试样侧膨胀值单值实绩1 | SCO_DATA_DIC(D) |
| 58 | IMPACT_SMP_IND_RSLT2 | NUMBER | Y |  | 冲击试样侧膨胀值单值实绩2 | SCO_DATA_DIC(D) |
| 59 | IMPACT_SMP_IND_RSLT3 | NUMBER | Y |  | 冲击试样侧膨胀值单值实绩3 | SCO_DATA_DIC(D) |
| 60 | IMPACT_SMP_IND_JDG | VARCHAR2(1) | Y |  | 冲击试样侧膨胀值单值判定 | SCO_DATA_DIC(D) |
| 61 | Z_TSL_CUT_IND_RSLT1 | NUMBER | Y |  | Z向拉伸断面收缩率单值实绩1 | DB注释(中文) |
| 62 | Z_TSL_CUT_IND_RSLT2 | NUMBER | Y |  | Z向拉伸断面收缩率单值实绩2 | DB注释(中文) |
| 63 | Z_TSL_CUT_IND_RSLT3 | NUMBER | Y |  | Z向拉伸断面收缩率单值实绩3 | DB注释(中文) |
| 64 | Z_TSL_CUT_IND_JDG | VARCHAR2(1) | Y |  | Z向拉伸断面收缩率单值判定 | SCO_DATA_DIC(D) |
| 65 | Z_TSL_CUT_AVG_RSLT | NUMBER | Y |  | Z向拉伸断面收缩率平均值实绩 | SCO_DATA_DIC(D) |
| 66 | Z_TSL_CUT_AVG_JDG | VARCHAR2(1) | Y |  | Z向拉伸断面收缩率平均值判定 | SCO_DATA_DIC(D) |
| 67 | Z_TSL_YP_RSLT | NUMBER | Y |  | Z向拉伸试验屈服强度实绩 | SCO_DATA_DIC(D) |
| 68 | Z_TSL_YP_JDG | VARCHAR2(1) | Y |  | Z向拉伸试验屈服强度判定 | SCO_DATA_DIC(D) |
| 69 | Z_TSL_TS_RSLT | NUMBER | Y |  | Z向拉伸试验抗拉强度实绩 | SCO_DATA_DIC(D) |
| 70 | Z_TSL_TS_JDG | VARCHAR2(1) | Y |  | Z向拉伸试验抗拉强度判定 | SCO_DATA_DIC(D) |
| 71 | Z_TSL_CT_EX_RA_RSLT | NUMBER | Y |  | Z向拉伸试验断后伸长率实绩 | SCO_DATA_DIC(D) |
| 72 | Z_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | Z向拉伸试验断后伸长率判定 | SCO_DATA_DIC(D) |
| 73 | HIGH_TEMP_TSL_STAND_CD | VARCHAR2(20) | Y |  | 高温拉伸测试试验标准类型 | SCO_DATA_DIC(D) |
| 74 | HIGH_TEMP_TSL_TEMP_RSLT | NUMBER | Y |  | 高温拉伸测试温度实绩 | SCO_DATA_DIC(D) |
| 75 | HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  | 高温拉伸测试抗拉强度实绩 | SCO_DATA_DIC(D) |
| 76 | HIGH_TEMP_TSL_TS_JDG | VARCHAR2(1) | Y |  | 高温拉伸测试抗拉强度判定 | SCO_DATA_DIC(D) |
| 77 | HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  | 高温拉伸测试屈服强度类型 | SCO_DATA_DIC(D) |
| 78 | HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  | 高温拉伸测试屈服强度实绩 | SCO_DATA_DIC(D) |
| 79 | HIGH_TEMP_TSL_YP_JDG | VARCHAR2(1) | Y |  | 高温拉伸测试屈服强度判定 | SCO_DATA_DIC(D) |
| 80 | HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  | 高温拉伸测试伸长率类型 | SCO_DATA_DIC(D) |
| 81 | HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  | 高温拉伸测试伸长率EL实绩 | DB注释(中文) |
| 82 | HIGH_TEMP_TSL_EL_JDG | VARCHAR2(1) | Y |  | 高温拉伸测试伸长率EL判定 | DB注释(中文) |
| 83 | HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  | 高温拉伸测试断面收缩率实绩 | SCO_DATA_DIC(D) |
| 84 | HIGH_TEMP_TSL_RA_JDG | VARCHAR2(1) | Y |  | 高温拉伸测试断面收缩率判定 | SCO_DATA_DIC(D) |
| 85 | DWTT_TEMP_SIGN | VARCHAR2(1) | Y |  | DWTT试验温度符号 | DB注释(中文) |
| 86 | DWTT_TEMP_RSLT | NUMBER | Y |  | DWTT试验温度实绩 | DB注释(中文) |
| 87 | DWTT_CREAK_CD | VARCHAR2(1) | Y |  | DWTT测试缺口类型 | DB注释(中文) |
| 88 | DWTT1_SA_RATIO_AVG_RSLT | NUMBER | Y |  | DWTT1纤维断面率SA平均值实绩 | SCO_DATA_DIC(D) |
| 89 | DWTT1_SA_RATIO_IND_RSLT1 | NUMBER | Y |  | DWTT1纤维断面率SA单值实绩1 | SCO_DATA_DIC(D) |
| 90 | DWTT1_SA_RATIO_IND_RSLT2 | NUMBER | Y |  | DWTT1纤维断面率SA单值实绩2 | SCO_DATA_DIC(D) |
| 91 | DWTT1_SA_RATIO_IND_JDG | VARCHAR2(1) | Y |  | DWTT1纤维断面率SA单值判定 | SCO_DATA_DIC(D) |
| 92 | DWTT2_SA_RATIO_AVG_RSLT | NUMBER | Y |  | DWTT2纤维断面率SA平均值实绩 | SCO_DATA_DIC(D) |
| 93 | DWTT2_SA_RATIO_IND_RSLT1 | NUMBER | Y |  | DWTT2纤维断面率SA单值实绩1 | SCO_DATA_DIC(D) |
| 94 | DWTT2_SA_RATIO_IND_RSLT2 | NUMBER | Y |  | DWTT2纤维断面率SA单值实绩2 | SCO_DATA_DIC(D) |
| 95 | DWTT2_SA_RATIO_IND_JDG | VARCHAR2(1) | Y |  | DWTT2纤维断面率SA单值判定 | SCO_DATA_DIC(D) |
| 96 | DWTT3_SA_RATIO_AVG_RSLT | NUMBER | Y |  | DWTT3纤维断面率SA平均值实绩 | SCO_DATA_DIC(D) |
| 97 | DWTT3_SA_RATIO_IND_RSLT1 | NUMBER | Y |  | DWTT3纤维断面率SA单值实绩1 | SCO_DATA_DIC(D) |
| 98 | DWTT3_SA_RATIO_IND_RSLT2 | NUMBER | Y |  | DWTT3纤维断面率SA单值实绩2 | SCO_DATA_DIC(D) |
| 99 | DWTT3_SA_RATIO_IND_JDG | VARCHAR2(1) | Y |  | DWTT3纤维断面率SA单值判定 | SCO_DATA_DIC(D) |
| 100 | DWTT4_SA_RATIO_AVG_RSLT | NUMBER | Y |  | DWTT4纤维断面率SA平均值实绩 | SCO_DATA_DIC(D) |
| 101 | DWTT4_SA_RATIO_IND_RSLT1 | NUMBER | Y |  | DWTT4纤维断面率SA单值实绩1 | SCO_DATA_DIC(D) |
| 102 | DWTT4_SA_RATIO_IND_RSLT2 | NUMBER | Y |  | DWTT4纤维断面率SA单值实绩2 | SCO_DATA_DIC(D) |
| 103 | DWTT4_SA_RATIO_IND_JDG | VARCHAR2(1) | Y |  | DWTT4纤维断面率SA单值判定 | SCO_DATA_DIC(D) |
| 104 | DWTT5_SA_RATIO_AVG_RSLT | NUMBER | Y |  | DWTT5纤维断面率SA平均值实绩 | SCO_DATA_DIC(D) |
| 105 | DWTT5_SA_RATIO_IND_RSLT1 | NUMBER | Y |  | DWTT5纤维断面率SA单值实绩1 | SCO_DATA_DIC(D) |
| 106 | DWTT5_SA_RATIO_IND_RSLT2 | NUMBER | Y |  | DWTT5纤维断面率SA单值实绩2 | SCO_DATA_DIC(D) |
| 107 | DWTT5_SA_RATIO_IND_JDG | VARCHAR2(1) | Y |  | DWTT5纤维断面率SA单值判定 | SCO_DATA_DIC(D) |
| 108 | SSCC_SOLUTION_KIND | VARCHAR2(20) | Y |  | SSCC测试溶液种类 | DB注释(中文) |
| 109 | SSCC_STRESS_TY | VARCHAR2(1) | Y |  | SSCC测试应力区分 | DB注释(中文) |
| 110 | SSCC_STRESS_TST_VAL_RSLT | NUMBER | Y |  | SSCC测试应力实绩 | DB注释(中文) |
| 111 | SSCC_STRESS_TST_VAL_JDG | VARCHAR2(1) | Y |  | SSCC测试应力判定 | DB注释(中文) |
| 112 | SSCC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  | SSCC执行标准 | DB注释(中文) |
| 113 | HIC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  | 执行标准 | DB注释(中文) |
| 114 | HIC_SOLUTION_KIND | VARCHAR2(20) | Y |  | HIC测试溶液种类 | DB注释(中文) |
| 115 | HIC_CLR_EACH1_RSLT1 | NUMBER | Y |  | HIC测试CLR试样1单个实绩1 | DB注释(中文) |
| 116 | HIC_CLR_EACH1_RSLT2 | NUMBER | Y |  | HIC测试CLR试样1单个实绩2 | DB注释(中文) |
| 117 | HIC_CLR_EACH1_RSLT3 | NUMBER | Y |  | HIC测试CLR试样1单个实绩3 | DB注释(中文) |
| 118 | HIC_CLR_EACH2_RSLT1 | NUMBER | Y |  | HIC测试CLR试样2单个实绩1 | DB注释(中文) |
| 119 | HIC_CLR_EACH2_RSLT2 | NUMBER | Y |  | HIC测试CLR试样2单个实绩2 | DB注释(中文) |
| 120 | HIC_CLR_EACH2_RSLT3 | NUMBER | Y |  | HIC测试CLR试样2单个实绩3 | DB注释(中文) |
| 121 | HIC_CLR_EACH3_RSLT1 | NUMBER | Y |  | HIC测试CLR试样3单个实绩1 | DB注释(中文) |
| 122 | HIC_CLR_EACH3_RSLT2 | NUMBER | Y |  | HIC测试CLR试样3单个实绩2 | DB注释(中文) |
| 123 | HIC_CLR_EACH3_RSLT3 | NUMBER | Y |  | HIC测试CLR试样3单个实绩3 | DB注释(中文) |
| 124 | HIC_CLR_EACH_JDG | VARCHAR2(1) | Y |  | HIC测试CLR单个判定 | DB注释(中文) |
| 125 | HIC_CLR_SPCMN_AVG1_RSLT | NUMBER | Y |  | HIC测试CLR试样平均1实绩 | DB注释(中文) |
| 126 | HIC_CLR_SPCMN_AVG2_RSLT | NUMBER | Y |  | HIC测试CLR试样平均2实绩 | DB注释(中文) |
| 127 | HIC_CLR_SPCMN_AVG3_RSLT | NUMBER | Y |  | HIC测试CLR试样平均3实绩 | DB注释(中文) |
| 128 | HIC_CLR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CLR试样平均判定 | DB注释(中文) |
| 129 | HIC_CLR_TOT_AVG_RSLT | NUMBER | Y |  | HIC测试CLR全体平均实绩 | DB注释(中文) |
| 130 | HIC_CLR_TOT_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CLR全体平均判定 | DB注释(中文) |
| 131 | HIC_CSR_EACH1_RSLT1 | NUMBER | Y |  | HIC测试CSR1单个实绩1 | DB注释(中文) |
| 132 | HIC_CSR_EACH1_RSLT2 | NUMBER | Y |  | HIC测试CSR1单个实绩2 | DB注释(中文) |
| 133 | HIC_CSR_EACH1_RSLT3 | NUMBER | Y |  | HIC测试CSR1单个实绩3 | DB注释(中文) |
| 134 | HIC_CSR_EACH2_RSLT1 | NUMBER | Y |  | HIC测试CSR2单个实绩1 | DB注释(中文) |
| 135 | HIC_CSR_EACH2_RSLT2 | NUMBER | Y |  | HIC测试CSR2单个实绩2 | DB注释(中文) |
| 136 | HIC_CSR_EACH2_RSLT3 | NUMBER | Y |  | HIC测试CSR2单个实绩3 | DB注释(中文) |
| 137 | HIC_CSR_EACH3_RSLT1 | NUMBER | Y |  | HIC测试CSR3单个实绩1 | DB注释(中文) |
| 138 | HIC_CSR_EACH3_RSLT2 | NUMBER | Y |  | HIC测试CSR3单个实绩2 | DB注释(中文) |
| 139 | HIC_CSR_EACH3_RSLT3 | NUMBER | Y |  | HIC测试CSR3单个实绩3 | DB注释(中文) |
| 140 | HIC_CSR_EACH_JDG | VARCHAR2(1) | Y |  | HIC测试CSR单个判定 | DB注释(中文) |
| 141 | HIC_CSR_SPCMN_AVG1_RSLT | NUMBER | Y |  | HIC测试CSR试样平均1实绩 | DB注释(中文) |
| 142 | HIC_CSR_SPCMN_AVG2_RSLT | NUMBER | Y |  | HIC测试CSR试样平均2实绩 | DB注释(中文) |
| 143 | HIC_CSR_SPCMN_AVG3_RSLT | NUMBER | Y |  | HIC测试CSR试样平均3实绩 | DB注释(中文) |
| 144 | HIC_CSR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CSR试样平均判定 | DB注释(中文) |
| 145 | HIC_CSR_TOT_AVG_RSLT | NUMBER | Y |  | HIC测试CSR全体平均实绩 | DB注释(中文) |
| 146 | HIC_CSR_TOT_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CSR全体平均判定 | DB注释(中文) |
| 147 | HIC_CTR_EACH1_RSLT1 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 148 | HIC_CTR_EACH1_RSLT2 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 149 | HIC_CTR_EACH1_RSLT3 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 150 | HIC_CTR_EACH2_RSLT1 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 151 | HIC_CTR_EACH2_RSLT2 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 152 | HIC_CTR_EACH2_RSLT3 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 153 | HIC_CTR_EACH3_RSLT1 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 154 | HIC_CTR_EACH3_RSLT2 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 155 | HIC_CTR_EACH3_RSLT3 | NUMBER | Y |  | HIC测试CTR单个实绩 | DB注释(中文) |
| 156 | HIC_CTR_EACH_JDG | VARCHAR2(1) | Y |  | HIC测试CTR单个判定 | DB注释(中文) |
| 157 | HIC_CTR_SPCMN_AVG1_RSLT | NUMBER | Y |  | HIC测试CTR试样平均1实绩 | DB注释(中文) |
| 158 | HIC_CTR_SPCMN_AVG2_RSLT | NUMBER | Y |  | HIC测试CTR试样平均2实绩 | DB注释(中文) |
| 159 | HIC_CTR_SPCMN_AVG3_RSLT | NUMBER | Y |  | HIC测试CTR试样平均3实绩 | DB注释(中文) |
| 160 | HIC_CTR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CTR试样平均判定 | DB注释(中文) |
| 161 | HIC_CTR_TOT_AVG_RSLT | NUMBER | Y |  | HIC测试CTR全体平均实绩 | DB注释(中文) |
| 162 | HIC_CTR_TOT_AVG_JDG | VARCHAR2(1) | Y |  | HIC测试CTR全体平均判定 | DB注释(中文) |
| 163 | MGRPHY_MTLGRP_TY | VARCHAR2(20) | Y |  | 组织类型 | DB注释(中文) |
| 164 | MGRPHY_MTLGRP_TY_PROVIDE | VARCHAR2(1) | Y |  | 组织类型是否提供 | DB注释(中文) |
| 165 | MGRPHY_BAND_STRC_GRD_MAX_RSLT | NUMBER | Y |  | 带状组织等级上限实绩 | DB注释(中文) |
| 166 | MGRPHY_BAND_STRC_GRD_MAX_JDG | VARCHAR2(1) | Y |  | 带状组织等级上限判定 | DB注释(中文) |
| 167 | MGRPHY_RSLT | NUMBER | Y |  |  | 空 |
| 168 | MGRPHY_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 169 | MGRPHY_FGS_RSLT | NUMBER | Y |  | 铁素体晶粒度实绩 | DB注释(中文) |
| 170 | MGRPHY_FGS_JDG | VARCHAR2(1) | Y |  | 铁素体晶粒度判定 | DB注释(中文) |
| 171 | MGRPHY_AGS_RSLT | NUMBER | Y |  | 奥氏体晶粒度实绩 | DB注释(中文) |
| 172 | MGRPHY_AGS_JDG | VARCHAR2(1) | Y |  | 奥氏体晶粒度判定 | DB注释(中文) |
| 173 | MGRPHY_GRNSZ_OCCP_RSLT | NUMBER | Y |  | 金相测试基相的体积分数实绩 | SCO_DATA_DIC(D) |
| 174 | MGRPHY_GRNSZ_OCCP_JDG | VARCHAR2(1) | Y |  | 金相测试基相的体积分数判定 | SCO_DATA_DIC(D) |
| 175 | NON_METAL_KIND_CD | VARCHAR2(1) | Y |  | 非金属夹杂物类别 | DB注释(中文) |
| 176 | NON_METAL_A_GRP_RSLT | NUMBER | Y |  | 夹杂物类别_A类（粗系）上限实绩 | SCO_DATA_DIC(D) |
| 177 | NON_METAL_A_DETAIL_RSLT | NUMBER | Y |  | 夹杂物类别_A类（细系）上限实绩 | SCO_DATA_DIC(D) |
| 178 | NON_METAL_A_GRP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 179 | NON_METAL_A_RSLT | NUMBER | Y |  | 非金属夹杂物A类实绩 | SCO_DATA_DIC(D) |
| 180 | NON_METAL_A_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物A类判定 | SCO_DATA_DIC(D) |
| 181 | NON_METAL_B_GRP_RSLT | NUMBER | Y |  | 夹杂物类别_B类（粗系）上限实绩 | SCO_DATA_DIC(D) |
| 182 | NON_METAL_B_DETAIL_RSLT | NUMBER | Y |  | 夹杂物类别_B类（细系）上限实绩 | SCO_DATA_DIC(D) |
| 183 | NON_METAL_B_GRP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 184 | NON_METAL_B_RSLT | NUMBER | Y |  | 非金属夹杂物B类实绩 | SCO_DATA_DIC(D) |
| 185 | NON_METAL_B_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物B类判定 | SCO_DATA_DIC(D) |
| 186 | NON_METAL_C_GRP_RSLT | NUMBER | Y |  | 夹杂物类别_C类（粗系）上限实绩 | SCO_DATA_DIC(D) |
| 187 | NON_METAL_C_DETAIL_RSLT | NUMBER | Y |  | 夹杂物类别_C类（细系）上限实绩 | SCO_DATA_DIC(D) |
| 188 | NON_METAL_C_GRP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 189 | NON_METAL_C_RSLT | NUMBER | Y |  | 非金属夹杂物C类实绩 | SCO_DATA_DIC(D) |
| 190 | NON_METAL_C_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物C类判定 | SCO_DATA_DIC(D) |
| 191 | NON_METAL_D_GRP_RSLT | NUMBER | Y |  | 夹杂物类别_D类（粗系）上限实绩 | SCO_DATA_DIC(D) |
| 192 | NON_METAL_D_DETAIL_RSLT | NUMBER | Y |  | 夹杂物类别_D类（细系）上限实绩 | SCO_DATA_DIC(D) |
| 193 | NON_METAL_D_GRP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 194 | NON_METAL_D_RSLT | NUMBER | Y |  | 非金属夹杂物D类实绩 | SCO_DATA_DIC(D) |
| 195 | NON_METAL_D_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物D类判定 | SCO_DATA_DIC(D) |
| 196 | NON_METAL_DS_RSLT | NUMBER | Y |  | 非金属夹杂物Ds实绩 | SCO_DATA_DIC(D) |
| 197 | NON_METAL_DS_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物Ds判定 | SCO_DATA_DIC(D) |
| 198 | NON_METAL_ABCD_RSLT | NUMBER | Y |  | 非金属夹杂物A+B+C+D实绩 | SCO_DATA_DIC(D) |
| 199 | NON_METAL_ABCD_JDG | VARCHAR2(1) | Y |  | 非金属夹杂物ABCD判定 | SCO_DATA_DIC(D) |
| 200 | NON_METAL_AC_RSLT | NUMBER | Y |  | 夹杂物类别_A+C上限实绩 | SCO_DATA_DIC(D) |
| 201 | NON_METAL_AC_JDG | VARCHAR2(1) | Y |  | 夹杂物类别_A+C判定 | SCO_DATA_DIC(D) |
| 202 | NON_METAL_BDDS_RSLT | NUMBER | Y |  | 夹杂物类别_B+D+Ds上限实绩 | SCO_DATA_DIC(D) |
| 203 | NON_METAL_BDDS_JDG | VARCHAR2(1) | Y |  | 夹杂物类别_B+D+Ds判定 | SCO_DATA_DIC(D) |
| 204 | BEND_DIA | NUMBER | Y |  | 弯曲测试弯心直径 | SCO_DATA_DIC(D) |
| 205 | BEND_ANGLE | NUMBER | Y |  | 弯曲测试弯曲角度 | SCO_DATA_DIC(D) |
| 206 | BEND_RSLT | VARCHAR2(1) | Y |  | 弯曲测试实绩 | SCO_DATA_DIC(D) |
| 207 | BEND_JDG | VARCHAR2(1) | Y |  | 弯曲测试判定 | SCO_DATA_DIC(D) |
| 208 | CPLATE_CUT_STRESS_RSLT | NUMBER | Y |  | 抗剪强度τ实绩 | SCO_DATA_DIC(D) |
| 209 | CPLATE_CUT_STRESS_JDG | VARCHAR2(1) | Y |  | 抗剪强度τ判定 | SCO_DATA_DIC(D) |
| 210 | CPLATE_THK_RSLT | NUMBER | Y |  | 复层厚度实绩 | SCO_DATA_DIC(D) |
| 211 | CPLATE_THK_JDG | VARCHAR2(1) | Y |  | 复层厚度判定 | SCO_DATA_DIC(D) |
| 212 | CPLATE_ER_IE_RSLT | NUMBER | Y |  | 杯突IE实绩 | SCO_DATA_DIC(D) |
| 213 | CPLATE_ER_IE_JDG | VARCHAR2(1) | Y |  | 杯突IE判定 | SCO_DATA_DIC(D) |
| 214 | CPLATE_IN_BD_DIA_D_RSLT | NUMBER | Y |  | 内弯弯曲压头直径D | SCO_DATA_DIC(D) |
| 215 | CPLATE_IN_BD_ANGLE_RSLT | NUMBER | Y |  | 内弯弯曲角度 | SCO_DATA_DIC(D) |
| 216 | CPLATE_IN_BD_WTH_RSLT | VARCHAR2(7) | Y |  | 内弯试样宽度 | SCO_DATA_DIC(D) |
| 217 | CPLATE_IN_BD_RSLT | VARCHAR2(1) | Y |  | 复层弯曲内弯结果 | SCO_DATA_DIC(D) |
| 218 | CPLATE_IN_BD_JDG | VARCHAR2(1) | Y |  | 复层弯曲内弯判定 | SCO_DATA_DIC(D) |
| 219 | CPLATE_OT_BD_DIA_D_RSLT | NUMBER | Y |  | 外弯弯曲压头直径D | SCO_DATA_DIC(D) |
| 220 | CPLATE_OT_BD_ANGLE_RSLT | NUMBER | Y |  | 外弯弯曲角度 | SCO_DATA_DIC(D) |
| 221 | CPLATE_OT_BD_WTH_RSLT | VARCHAR2(7) | Y |  | 外弯试样宽度 | SCO_DATA_DIC(D) |
| 222 | CPLATE_OT_BD_RSLT | VARCHAR2(1) | Y |  | 复层弯曲外弯结果 | SCO_DATA_DIC(D) |
| 223 | CPLATE_OT_BD_JDG | VARCHAR2(1) | Y |  | 复层弯曲外弯判定 | SCO_DATA_DIC(D) |
| 224 | CPLATE_SIDE_BD_DIA_D_RSLT | NUMBER | Y |  | 侧弯弯曲压头直径D | SCO_DATA_DIC(D) |
| 225 | CPLATE_SIDE_BD_ANGLE_RSLT | NUMBER | Y |  | 侧弯弯曲角度 | SCO_DATA_DIC(D) |
| 226 | CPLATE_SIDE_BD_WTH_RSLT | VARCHAR2(7) | Y |  | 侧弯试样宽度 | SCO_DATA_DIC(D) |
| 227 | CPLATE_SIDE_BD_RSLT | VARCHAR2(1) | Y |  | 复层弯曲侧弯结果 | SCO_DATA_DIC(D) |
| 228 | CPLATE_SIDE_BD_JDG | VARCHAR2(1) | Y |  | 复层弯曲侧弯判定 | SCO_DATA_DIC(D) |
| 229 | HARD_KIND | VARCHAR2(1) | Y |  | 硬度测试种类 | SCO_DATA_DIC(D) |
| 230 | HARD_AVG_RSLT | NUMBER | Y |  | 硬度平均值实绩 | SCO_DATA_DIC(D) |
| 231 | HARD_IND_JDG | VARCHAR2(1) | Y |  | 硬度单值判定 | SCO_DATA_DIC(D) |
| 232 | HARD_AVG_JDG | VARCHAR2(1) | Y |  | 硬度平均值判定 | SCO_DATA_DIC(D) |
| 233 | S_PRINT_KIND | VARCHAR2(1) | Y |  | S_Print试验种类 | DB注释(中文) |
| 234 | S_PRINT_RSLT | NUMBER | Y |  | 硫印测试实绩 | DB注释(中文) |
| 235 | S_PRINT_JDG | VARCHAR2(1) | Y |  | 硫印测试判定 | DB注释(中文) |
| 236 | AGE_TST_STRESS_RSLT | NUMBER | Y |  | 时效应变量实绩 | SCO_DATA_DIC(D) |
| 237 | AGE_TST_STRESS_JDG | VARCHAR2(1) | Y |  | 时效应变量判定 | SCO_DATA_DIC(D) |
| 238 | AGE_TST_AGE_TIME_RSLT | NUMBER | Y |  | 时效温度实绩 | DB注释(中文) |
| 239 | AGE_TST_AGE_TIME_JDG | VARCHAR2(1) | Y |  | 时效温度判定 | DB注释(中文) |
| 240 | AGE_TST_AGE_TEMP_RSLT | NUMBER | Y |  | 保温时间实绩 | DB注释(中文) |
| 241 | AGE_TST_AGE_TEMP_JDG | VARCHAR2(1) | Y |  | 保温时间判定 | DB注释(中文) |
| 242 | AGE_TST_YP_CD | VARCHAR2(1) | Y |  | 时效拉伸测试屈服强度类型 | DB注释(中文) |
| 243 | AGE_TST_YP_RSLT | NUMBER | Y |  | 时效拉伸测试屈服强度实绩 | DB注释(中文) |
| 244 | AGE_TST_YP_JDG | VARCHAR2(1) | Y |  | 时效拉伸测试屈服强度判定 | DB注释(中文) |
| 245 | AGE_TST_TS_RSLT | NUMBER | Y |  | 时效拉伸测试抗拉强度实绩 | DB注释(中文) |
| 246 | AGE_TST_TS_JDG | VARCHAR2(1) | Y |  | 时效拉伸测试抗拉强度判定 | DB注释(中文) |
| 247 | AGE_TST_YP_TS_RSLT | NUMBER | Y |  | 时效拉伸试验屈强比YP/TS实绩 | DB注释(中文) |
| 248 | AGE_TST_YP_TS_JDG | VARCHAR2(1) | Y |  | 时效拉伸试验屈强比YP/TS判定 | DB注释(中文) |
| 249 | AGE_TST_RT05_RM_RSLT | NUMBER | Y |  | 时效拉伸试验屈强比Rt0.5/Rm实绩 | DB注释(中文) |
| 250 | AGE_TST_RT05_RM_JDG | VARCHAR2(1) | Y |  | 时效拉伸试验屈强比Rt0.5/Rm判定 | DB注释(中文) |
| 251 | AGE_TST_RT15_RT05_RSLT | NUMBER | Y |  | 时效拉伸试验屈强比Rt1.5/Rt0.5实绩 | DB注释(中文) |
| 252 | AGE_TST_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 时效拉伸试验屈强比Rt1.5/Rt0.5判定 | DB注释(中文) |
| 253 | AGE_TST_RT20_RT10_RSLT | NUMBER | Y |  | 时效拉伸试验屈强比Rt2.0/Rt1.0实绩 | DB注释(中文) |
| 254 | AGE_TST_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 时效拉伸试验屈强比Rt2.0/Rt1.0判定 | DB注释(中文) |
| 255 | AGE_TST_RT50_RT10_RSLT | NUMBER | Y |  | 时效拉伸试验屈强比Rt5.0/Rt1.0实绩 | DB注释(中文) |
| 256 | AGE_TST_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 时效拉伸试验屈强比Rt5.0/Rt1.0判定 | DB注释(中文) |
| 257 | AGE_TST_CT_EX_RA_RSLT | NUMBER | Y |  | 拉抻测试断后伸长率实绩 | SCO_DATA_DIC(D) |
| 258 | AGE_TST_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 时效拉抻测试延伸率类型(EL) | SCO_DATA_DIC(D) |
| 259 | AGE_TST_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 拉抻测试断后伸长率判定 | SCO_DATA_DIC(D) |
| 260 | AGE_TST_CT_RA_RSLT | NUMBER | Y |  | 时效拉伸试验均匀伸长率实绩 | SCO_DATA_DIC(D) |
| 261 | AGE_TST_CT_RA_JDG | VARCHAR2(1) | Y |  | 时效拉伸试验均匀伸长率判定 | SCO_DATA_DIC(D) |
| 262 | AGE_TST_RA_RSLT | NUMBER | Y |  | 时效拉伸试验断面收缩率实绩 | SCO_DATA_DIC(D) |
| 263 | AGE_TST_RA_JDG | VARCHAR2(1) | Y |  | 时效拉伸试验断面收缩率判定 | SCO_DATA_DIC(D) |
| 264 | AGE_TST1_TEMP_RSLT | NUMBER | Y |  | 时效冲击1测试温度实绩 | SCO_DATA_DIC(D) |
| 265 | AGE_TST1_CREAK_CD | VARCHAR2(1) | Y |  | 时效冲击1测试缺口类型 | SCO_DATA_DIC(D) |
| 266 | AGE_TST1_AVG_RSLT | NUMBER | Y |  | 时效冲击1测试平均值实绩 | SCO_DATA_DIC(D) |
| 267 | AGE_TST1_IND_RSLT1 | NUMBER | Y |  | 时效冲击1测试单值实绩1 | DB注释(中文) |
| 268 | AGE_TST1_IND_RSLT2 | NUMBER | Y |  | 时效冲击1测试单值实绩2 | DB注释(中文) |
| 269 | AGE_TST1_IND_RSLT3 | NUMBER | Y |  | 时效冲击1测试单值实绩3 | DB注释(中文) |
| 270 | AGE_TST1_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击1测试单值判定 | SCO_DATA_DIC(D) |
| 271 | AGE_TST1_SMP_AVG_RSLT | NUMBER | Y |  | 纤维断面率1平均值实绩 | SCO_DATA_DIC(D) |
| 272 | AGE_TST1_SMP_IND_RSLT1 | NUMBER | Y |  | 纤维断面率1单值实绩1 | DB注释(中文) |
| 273 | AGE_TST1_SMP_IND_RSLT2 | NUMBER | Y |  | 纤维断面率1单值实绩2 | DB注释(中文) |
| 274 | AGE_TST1_SMP_IND_RSLT3 | NUMBER | Y |  | 纤维断面率1单值实绩3 | DB注释(中文) |
| 275 | AGE_TST1_SMP_IND_JDG | VARCHAR2(1) | Y |  | 纤维断面率1单值判定 | SCO_DATA_DIC(D) |
| 276 | AGE_TST1_SIDE_EXP_AVG_RSLT | NUMBER | Y |  | 时效冲击1试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 277 | AGE_TST1_SIDE_EXP_IND_RSLT1 | NUMBER | Y |  | 时效冲击1试样侧膨胀值单值实绩1 | DB注释(中文) |
| 278 | AGE_TST1_SIDE_EXP_IND_RSLT2 | NUMBER | Y |  | 时效冲击1试样侧膨胀值单值实绩2 | DB注释(中文) |
| 279 | AGE_TST1_SIDE_EXP_IND_RSLT3 | NUMBER | Y |  | 时效冲击1试样侧膨胀值单值实绩3 | DB注释(中文) |
| 280 | AGE_TST1_SIDE_EXP_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击1试样侧膨胀值单值判定 | SCO_DATA_DIC(D) |
| 281 | AGE_TST2_TEMP_RSLT | NUMBER | Y |  | 时效冲击2测试温度实绩 | SCO_DATA_DIC(D) |
| 282 | AGE_TST2_CREAK_CD | VARCHAR2(1) | Y |  | 时效冲击2测试缺口类型 | SCO_DATA_DIC(D) |
| 283 | AGE_TST2_AVG_RSLT | NUMBER | Y |  | 时效冲击2测试平均值实绩 | SCO_DATA_DIC(D) |
| 284 | AGE_TST2_IND_RSLT1 | NUMBER | Y |  | 时效冲击2测试单值实绩1 | DB注释(中文) |
| 285 | AGE_TST2_IND_RSLT2 | NUMBER | Y |  | 时效冲击2测试单值实绩2 | DB注释(中文) |
| 286 | AGE_TST2_IND_RSLT3 | NUMBER | Y |  | 时效冲击2测试单值实绩3 | DB注释(中文) |
| 287 | AGE_TST2_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击2测试单值判定 | SCO_DATA_DIC(D) |
| 288 | AGE_TST2_SMP_AVG_RSLT | NUMBER | Y |  | 纤维断面率2平均值实绩 | SCO_DATA_DIC(D) |
| 289 | AGE_TST2_SMP_IND_RSLT1 | NUMBER | Y |  | 纤维断面率2单值实绩1 | DB注释(中文) |
| 290 | AGE_TST2_SMP_IND_RSLT2 | NUMBER | Y |  | 纤维断面率2单值实绩2 | DB注释(中文) |
| 291 | AGE_TST2_SMP_IND_RSLT3 | NUMBER | Y |  | 纤维断面率2单值实绩3 | DB注释(中文) |
| 292 | AGE_TST2_SMP_IND_JDG | VARCHAR2(1) | Y |  | 纤维断面率2单值判定 | SCO_DATA_DIC(D) |
| 293 | AGE_TST2_SIDE_EXP_AVG_RSLT | NUMBER | Y |  | 时效冲击2试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 294 | AGE_TST2_SIDE_EXP_IND_RSLT1 | NUMBER | Y |  | 时效冲击2试样侧膨胀值单值实绩1 | DB注释(中文) |
| 295 | AGE_TST2_SIDE_EXP_IND_RSLT2 | NUMBER | Y |  | 时效冲击2试样侧膨胀值单值实绩2 | DB注释(中文) |
| 296 | AGE_TST2_SIDE_EXP_IND_RSLT3 | NUMBER | Y |  | 时效冲击2试样侧膨胀值单值实绩3 | DB注释(中文) |
| 297 | AGE_TST2_SIDE_EXP_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击2试样侧膨胀值单值判定 | SCO_DATA_DIC(D) |
| 298 | AGE_TST3_TEMP_RSLT | NUMBER | Y |  | 时效冲击3测试温度实绩 | SCO_DATA_DIC(D) |
| 299 | AGE_TST3_CREAK_CD | VARCHAR2(1) | Y |  | 时效冲击3测试缺口类型 | SCO_DATA_DIC(D) |
| 300 | AGE_TST3_AVG_RSLT | NUMBER | Y |  | 时效冲击3测试平均值实绩 | SCO_DATA_DIC(D) |
| 301 | AGE_TST3_IND_RSLT1 | NUMBER | Y |  | 时效冲击3测试单值实绩1 | DB注释(中文) |
| 302 | AGE_TST3_IND_RSLT2 | NUMBER | Y |  | 时效冲击3测试单值实绩2 | DB注释(中文) |
| 303 | AGE_TST3_IND_RSLT3 | NUMBER | Y |  | 时效冲击3测试单值实绩3 | DB注释(中文) |
| 304 | AGE_TST3_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击3测试单值判定 | SCO_DATA_DIC(D) |
| 305 | AGE_TST3_SMP_AVG_RSLT | NUMBER | Y |  | 纤维断面率3平均值实绩 | SCO_DATA_DIC(D) |
| 306 | AGE_TST3_SMP_IND_RSLT1 | NUMBER | Y |  | 纤维断面率3单值实绩1 | DB注释(中文) |
| 307 | AGE_TST3_SMP_IND_RSLT2 | NUMBER | Y |  | 纤维断面率3单值实绩2 | DB注释(中文) |
| 308 | AGE_TST3_SMP_IND_RSLT3 | NUMBER | Y |  | 纤维断面率3单值实绩3 | DB注释(中文) |
| 309 | AGE_TST3_SMP_IND_JDG | VARCHAR2(1) | Y |  | 纤维断面率3单值判定 | SCO_DATA_DIC(D) |
| 310 | AGE_TST3_SIDE_EXP_AVG_RSLT | NUMBER | Y |  | 时效冲击3试样侧膨胀值平均值实绩1 | SCO_DATA_DIC(D) |
| 311 | AGE_TST3_SIDE_EXP_IND_RSLT1 | NUMBER | Y |  | 时效冲击3试样侧膨胀值单值实绩 | SCO_DATA_DIC(D) |
| 312 | AGE_TST3_SIDE_EXP_IND_RSLT2 | NUMBER | Y |  | 时效冲击3试样侧膨胀值单值实绩2 | DB注释(中文) |
| 313 | AGE_TST3_SIDE_EXP_IND_RSLT3 | NUMBER | Y |  | 时效冲击3试样侧膨胀值单值实绩3 | DB注释(中文) |
| 314 | AGE_TST3_SIDE_EXP_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击3试样侧膨胀值单值判定 | SCO_DATA_DIC(D) |
| 315 | AGE_TST4_TEMP_RSLT | NUMBER | Y |  | 时效冲击4测试温度实绩 | SCO_DATA_DIC(D) |
| 316 | AGE_TST4_CREAK_CD | VARCHAR2(1) | Y |  | 时效冲击4测试缺口类型 | SCO_DATA_DIC(D) |
| 317 | AGE_TST4_AVG_RSLT | NUMBER | Y |  | 时效冲击4测试平均值实绩 | SCO_DATA_DIC(D) |
| 318 | AGE_TST4_IND_RSLT1 | NUMBER | Y |  | 时效冲击4测试单值实绩1 | DB注释(中文) |
| 319 | AGE_TST4_IND_RSLT2 | NUMBER | Y |  | 时效冲击4测试单值实绩2 | DB注释(中文) |
| 320 | AGE_TST4_IND_RSLT3 | NUMBER | Y |  | 时效冲击4测试单值实绩3 | DB注释(中文) |
| 321 | AGE_TST4_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击4测试单值判定 | SCO_DATA_DIC(D) |
| 322 | AGE_TST4_SMP_AVG_RSLT | NUMBER | Y |  | 纤维断面率4平均值实绩 | SCO_DATA_DIC(D) |
| 323 | AGE_TST4_SMP_IND_RSLT1 | NUMBER | Y |  | 纤维断面率4单值实绩1 | DB注释(中文) |
| 324 | AGE_TST4_SMP_IND_RSLT2 | NUMBER | Y |  | 纤维断面率4单值实绩2 | DB注释(中文) |
| 325 | AGE_TST4_SMP_IND_RSLT3 | NUMBER | Y |  | 纤维断面率4单值实绩3 | DB注释(中文) |
| 326 | AGE_TST4_SMP_IND_JDG | VARCHAR2(1) | Y |  | 纤维断面率4单值判定 | SCO_DATA_DIC(D) |
| 327 | AGE_TST4_SIDE_EXP_AVG_RSLT | NUMBER | Y |  | 时效冲击4试样侧膨胀值平均值实绩1 | SCO_DATA_DIC(D) |
| 328 | AGE_TST4_SIDE_EXP_IND_RSLT1 | NUMBER | Y |  | 时效冲击4试样侧膨胀值单值实绩 | SCO_DATA_DIC(D) |
| 329 | AGE_TST4_SIDE_EXP_IND_RSLT2 | NUMBER | Y |  | 时效冲击4试样侧膨胀值单值实绩2 | DB注释(中文) |
| 330 | AGE_TST4_SIDE_EXP_IND_RSLT3 | NUMBER | Y |  | 时效冲击4试样侧膨胀值单值实绩3 | DB注释(中文) |
| 331 | AGE_TST4_SIDE_EXP_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击4试样侧膨胀值单值判定 | SCO_DATA_DIC(D) |
| 332 | AGE_TST5_TEMP_RSLT | NUMBER | Y |  | 时效冲击5测试温度实绩 | SCO_DATA_DIC(D) |
| 333 | AGE_TST5_CREAK_CD | VARCHAR2(1) | Y |  | 时效冲击5测试缺口类型 | SCO_DATA_DIC(D) |
| 334 | AGE_TST5_AVG_RSLT | NUMBER | Y |  | 时效冲击5测试平均值实绩 | SCO_DATA_DIC(D) |
| 335 | AGE_TST5_IND_RSLT1 | NUMBER | Y |  | 时效冲击5测试单值实绩1 | DB注释(中文) |
| 336 | AGE_TST5_IND_RSLT2 | NUMBER | Y |  | 时效冲击5测试单值实绩2 | DB注释(中文) |
| 337 | AGE_TST5_IND_RSLT3 | NUMBER | Y |  | 时效冲击5测试单值实绩3 | DB注释(中文) |
| 338 | AGE_TST5_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击5测试单值判定 | SCO_DATA_DIC(D) |
| 339 | AGE_TST5_SMP_AVG_RSLT | NUMBER | Y |  | 纤维断面率5平均值实绩 | SCO_DATA_DIC(D) |
| 340 | AGE_TST5_SMP_IND_RSLT1 | NUMBER | Y |  | 纤维断面率5单值实绩1 | DB注释(中文) |
| 341 | AGE_TST5_SMP_IND_RSLT2 | NUMBER | Y |  | 纤维断面率5单值实绩2 | DB注释(中文) |
| 342 | AGE_TST5_SMP_IND_RSLT3 | NUMBER | Y |  | 纤维断面率5单值实绩3 | DB注释(中文) |
| 343 | AGE_TST5_SMP_IND_JDG | VARCHAR2(1) | Y |  | 纤维断面率5单值判定 | SCO_DATA_DIC(D) |
| 344 | AGE_TST5_SIDE_EXP_AVG_RSLT | NUMBER | Y |  | 时效冲击5试样侧膨胀值平均值实绩1 | SCO_DATA_DIC(D) |
| 345 | AGE_TST5_SIDE_EXP_IND_RSLT1 | NUMBER | Y |  | 时效冲击5试样侧膨胀值单值实绩 | SCO_DATA_DIC(D) |
| 346 | AGE_TST5_SIDE_EXP_IND_RSLT2 | NUMBER | Y |  | 时效冲击5试样侧膨胀值单值实绩2 | DB注释(中文) |
| 347 | AGE_TST5_SIDE_EXP_IND_RSLT3 | NUMBER | Y |  | 时效冲击5试样侧膨胀值单值实绩3 | DB注释(中文) |
| 348 | AGE_TST5_SIDE_EXP_IND_JDG | VARCHAR2(1) | Y |  | 时效冲击5试样侧膨胀值单值判定 | SCO_DATA_DIC(D) |
| 349 | NDT_TEMP_RSLT | NUMBER | Y |  | NDT温度实绩 | SCO_DATA_DIC(D) |
| 350 | NDT_TEMP_JDG | VARCHAR2(1) | Y |  | NDT温度判定 | SCO_DATA_DIC(D) |
| 351 | CTOD_VAL_RSLT | NUMBER | Y |  | CTOD值实绩 | SCO_DATA_DIC(D) |
| 352 | CTOD_VAL_JDG | VARCHAR2(1) | Y |  | CTOD值判定 | SCO_DATA_DIC(D) |
| 353 | NP_JHRC_HARD_RSLT | NUMBER | Y |  | 淬透性指数_JHRC硬度实绩 | SCO_DATA_DIC(D) |
| 354 | NP_JHRC_HARD_JDG | VARCHAR2(1) | Y |  | 淬透性指数_JHRC硬度判定 | SCO_DATA_DIC(D) |
| 355 | NP_JHRC_DIST_RSLT | NUMBER | Y |  | 淬透性指数_JHRC距离实绩 | SCO_DATA_DIC(D) |
| 356 | NP_JHRC_DIST_JDG | VARCHAR2(1) | Y |  | 淬透性指数_JHRC距离判定 | SCO_DATA_DIC(D) |
| 357 | NP_JHV_HARD_RSLT | NUMBER | Y |  | 淬透性指数_JHV硬度实绩 | SCO_DATA_DIC(D) |
| 358 | NP_JHV_HARD_JDG | VARCHAR2(1) | Y |  | 淬透性指数_JHV硬度判定 | SCO_DATA_DIC(D) |
| 359 | NP_JHV_DIST_RSLT | NUMBER | Y |  | 淬透性指数_JHV距离实绩 | SCO_DATA_DIC(D) |
| 360 | NP_JHV_DIST_JDG | VARCHAR2(1) | Y |  | 淬透性指数_JHV距离判定 | SCO_DATA_DIC(D) |
| 361 | TSL1_YP_CD | VARCHAR2(1) | Y |  | 拉伸试验1屈服强度类型 | SCO_DATA_DIC(D) |
| 362 | TSL1_YP_RSLT | NUMBER | Y |  | 拉伸试验1屈服强度实绩 | SCO_DATA_DIC(L) |
| 363 | TSL1_YP_JDG | VARCHAR2(1) | Y |  | 拉伸试验1屈服强度判定 | SCO_DATA_DIC(D) |
| 364 | TSL1_TS_RSLT | NUMBER | Y |  | 拉伸试验1抗拉强度实绩 | SCO_DATA_DIC(D) |
| 365 | TSL1_TS_JDG | VARCHAR2(1) | Y |  | 拉伸试验1抗拉强度判定 | SCO_DATA_DIC(D) |
| 366 | TSL1_YP_TS_RSLT | NUMBER | Y |  | 拉伸试验1屈强比YP/TS实绩 | SCO_DATA_DIC(D) |
| 367 | TSL1_YP_TS_JDG | VARCHAR2(1) | Y |  | 拉伸试验1屈强比YP/TS判定 | SCO_DATA_DIC(D) |
| 368 | TSL1_RT05_RM_RSLT | NUMBER | Y |  | 拉伸试验1屈强比Rt0.5/Rm实绩 | SCO_DATA_DIC(D) |
| 369 | TSL1_RT05_RM_JDG | VARCHAR2(1) | Y |  | 拉伸试验1屈强比Rt0.5/Rm判定 | SCO_DATA_DIC(D) |
| 370 | TSL1_RT15_RT05_RSLT | NUMBER | Y |  | 拉伸试验1屈强比Rt1.5/Rt0.5实绩 | SCO_DATA_DIC(D) |
| 371 | TSL1_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 拉伸试验1屈强比Rt1.5/Rt0.5判定 | SCO_DATA_DIC(D) |
| 372 | TSL1_RT20_RT10_RSLT | NUMBER | Y |  | 拉伸试验1屈强比Rt2.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 373 | TSL1_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 拉伸试验1屈强比Rt2.0/Rt1.0判定 | SCO_DATA_DIC(D) |
| 374 | TSL1_RT50_RT10_RSLT | NUMBER | Y |  | 拉伸试验1屈强比Rt5.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 375 | TSL1_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 拉伸试验1屈强比Rt5.0/Rt1.0判定 | SCO_DATA_DIC(D) |
| 376 | TSL1_CT_EX_RA_RSLT | NUMBER | Y |  | 拉伸试验1断后伸长率实绩 | SCO_DATA_DIC(D) |
| 377 | TSL1_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 拉伸试验1断后伸长率类型 | SCO_DATA_DIC(D) |
| 378 | TSL1_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 拉伸试验1断后伸长率判定 | SCO_DATA_DIC(D) |
| 379 | TSL1_CT_RA_RSLT | NUMBER | Y |  | 拉伸试验1均匀伸长率实绩 | SCO_DATA_DIC(D) |
| 380 | TSL1_CT_RA_JDG | VARCHAR2(1) | Y |  | 拉伸试验1均匀伸长率判定 | SCO_DATA_DIC(D) |
| 381 | TSL1_RA_RSLT | NUMBER | Y |  | 拉伸试验1断面收缩率实绩 | SCO_DATA_DIC(D) |
| 382 | TSL1_RA_JDG | VARCHAR2(1) | Y |  | 拉伸试验1断面收缩率判定 | SCO_DATA_DIC(D) |
| 383 | TSL1_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 消应力处理1_保温温度实绩 | DB注释(中文) |
| 384 | TSL1_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 消应力处理1_保温时间实绩 | DB注释(中文) |
| 385 | TSL1_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 消应力处理1_冷却方式 | DB注释(中文) |
| 386 | TSL1_STRESS_JDG | VARCHAR2(1) | Y |  | 消应力处理1_判定 | DB注释(中文) |
| 387 | TSL2_YP_CD | VARCHAR2(1) | Y |  | 拉伸试验2屈服强度类型 | DB注释(中文) |
| 388 | TSL2_YP_RSLT | NUMBER | Y |  | 拉伸试验2屈服强度实绩 | DB注释(中文) |
| 389 | TSL2_YP_JDG | VARCHAR2(1) | Y |  | 拉伸试验2屈服强度判定 | DB注释(中文) |
| 390 | TSL2_TS_RSLT | NUMBER | Y |  | 拉伸试验2抗拉强度实绩 | DB注释(中文) |
| 391 | TSL2_TS_JDG | VARCHAR2(1) | Y |  | 拉伸试验2抗拉强度判定 | DB注释(中文) |
| 392 | TSL2_YP_TS_RSLT | NUMBER | Y |  | 拉伸试验2屈强比YP/TS实绩 | DB注释(中文) |
| 393 | TSL2_YP_TS_JDG | VARCHAR2(1) | Y |  | 拉伸试验2屈强比YP/TS判定 | DB注释(中文) |
| 394 | TSL2_RT05_RM_RSLT | NUMBER | Y |  | 拉伸试验2屈强比Rt0.5/Rm实绩 | DB注释(中文) |
| 395 | TSL2_RT05_RM_JDG | VARCHAR2(1) | Y |  | 拉伸试验2屈强比Rt0.5/Rm判定 | DB注释(中文) |
| 396 | TSL2_RT15_RT05_RSLT | NUMBER | Y |  | 拉伸试验2屈强比Rt1.5/Rt0.5实绩 | DB注释(中文) |
| 397 | TSL2_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 拉伸试验2屈强比Rt1.5/Rt0.5判定 | DB注释(中文) |
| 398 | TSL2_RT20_RT10_RSLT | NUMBER | Y |  | 拉伸试验2屈强比Rt2.0/Rt1.0实绩 | DB注释(中文) |
| 399 | TSL2_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 拉伸试验2屈强比Rt2.0/Rt1.0判定 | DB注释(中文) |
| 400 | TSL2_RT50_RT10_RSLT | NUMBER | Y |  | 拉伸试验2屈强比Rt5.0/Rt1.0实绩 | DB注释(中文) |
| 401 | TSL2_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 拉伸试验2屈强比Rt5.0/Rt1.0判定 | DB注释(中文) |
| 402 | TSL2_CT_EX_RA_RSLT | NUMBER | Y |  | 拉伸试验2断后伸长率实绩 | SCO_DATA_DIC(D) |
| 403 | TSL2_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 拉伸试验2断后伸长率类型 | SCO_DATA_DIC(D) |
| 404 | TSL2_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 拉伸试验2断后伸长率判定 | SCO_DATA_DIC(D) |
| 405 | TSL2_CT_RA_RSLT | NUMBER | Y |  | 拉伸试验2均匀伸长率实绩 | SCO_DATA_DIC(D) |
| 406 | TSL2_CT_RA_JDG | VARCHAR2(1) | Y |  | 拉伸试验2均匀伸长率判定 | SCO_DATA_DIC(D) |
| 407 | TSL2_RA_RSLT | NUMBER | Y |  | 拉伸试验2断面收缩率实绩 | SCO_DATA_DIC(D) |
| 408 | TSL2_RA_JDG | VARCHAR2(1) | Y |  | 拉伸试验2断面收缩率判定 | SCO_DATA_DIC(D) |
| 409 | TSL2_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 消应力处理2_保温温度实绩 | SCO_DATA_DIC(D) |
| 410 | TSL2_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 消应力处理2_保温时间实绩 | SCO_DATA_DIC(D) |
| 411 | TSL2_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 消应力处理2_冷却方式 | SCO_DATA_DIC(D) |
| 412 | TSL2_STRESS_JDG | VARCHAR2(1) | Y |  | 消应力处理2_判定 | SCO_DATA_DIC(D) |
| 413 | IMPACT1_TEMP_RSLT | NUMBER | Y |  | 冲击试验1温度实绩 | SCO_DATA_DIC(D) |
| 414 | IMPACT1_CREAK_CD | VARCHAR2(1) | Y |  | 冲击试验1缺口类型 | SCO_DATA_DIC(D) |
| 415 | IMPACT1_ENERGY_CD | VARCHAR2(1) | Y |  | 冲击试验1试样能量值类型 | SCO_DATA_DIC(D) |
| 416 | IMPACT1_AVG_RSLT | NUMBER | Y |  | 冲击试验1平均值实绩 | SCO_DATA_DIC(D) |
| 417 | IMPACT1_IND_RSLT1 | NUMBER | Y |  | 冲击试验1单值实绩1 | SCO_DATA_DIC(D) |
| 418 | IMPACT1_IND_RSLT2 | NUMBER | Y |  | 冲击试验1单值实绩2 | SCO_DATA_DIC(D) |
| 419 | IMPACT1_IND_RSLT3 | NUMBER | Y |  | 冲击试验1单值实绩3 | SCO_DATA_DIC(D) |
| 420 | IMPACT1_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验1单值判定 | SCO_DATA_DIC(D) |
| 421 | IMPACT1_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 冲击试验1纤维断面率平均值实绩 | SCO_DATA_DIC(D) |
| 422 | IMPACT1_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 冲击试验1纤维断面率单值实绩1 | SCO_DATA_DIC(D) |
| 423 | IMPACT1_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 冲击试验1纤维断面率单值实绩2 | SCO_DATA_DIC(D) |
| 424 | IMPACT1_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 冲击试验1纤维断面率单值实绩3 | SCO_DATA_DIC(D) |
| 425 | IMPACT1_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验1纤维断面率单值判定 | SCO_DATA_DIC(D) |
| 426 | IMPACT1_SMP_AVG_RSLT | NUMBER | Y |  | 冲击试验1试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 427 | IMPACT1_SMP_IND_RSLT1 | NUMBER | Y |  | 冲击试验1试样侧膨胀值单值实绩1 | SCO_DATA_DIC(D) |
| 428 | IMPACT1_SMP_IND_RSLT2 | NUMBER | Y |  | 冲击试验1试样侧膨胀值单值实绩2 | SCO_DATA_DIC(D) |
| 429 | IMPACT1_SMP_IND_RSLT3 | NUMBER | Y |  | 冲击试验1试样侧膨胀值单值实绩3 | SCO_DATA_DIC(D) |
| 430 | IMPACT1_SMP_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验1试样侧膨胀值单值判定 | SCO_DATA_DIC(D) |
| 431 | IMPACT2_TEMP_RSLT | NUMBER | Y |  | 冲击试验2温度实绩 | DB注释(中文) |
| 432 | IMPACT2_CREAK_CD | VARCHAR2(1) | Y |  | 冲击试验2缺口类型 | DB注释(中文) |
| 433 | IMPACT2_ENERGY_CD | VARCHAR2(1) | Y |  | 冲击试验2试样能量值类型 | SCO_DATA_DIC(D) |
| 434 | IMPACT2_AVG_RSLT | NUMBER | Y |  | 冲击试验2平均值实绩 | SCO_DATA_DIC(D) |
| 435 | IMPACT2_IND_RSLT1 | NUMBER | Y |  | 冲击试验2单值实绩1 | DB注释(中文) |
| 436 | IMPACT2_IND_RSLT2 | NUMBER | Y |  | 冲击试验2单值实绩2 | DB注释(中文) |
| 437 | IMPACT2_IND_RSLT3 | NUMBER | Y |  | 冲击试验2单值实绩3 | DB注释(中文) |
| 438 | IMPACT2_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验2单值判定 | SCO_DATA_DIC(D) |
| 439 | IMPACT2_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 冲击试验2纤维断面率平均值实绩 | SCO_DATA_DIC(D) |
| 440 | IMPACT2_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 冲击试验2纤维断面率单值实绩1 | DB注释(中文) |
| 441 | IMPACT2_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 冲击试验2纤维断面率单值实绩2 | DB注释(中文) |
| 442 | IMPACT2_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 冲击试验2纤维断面率单值实绩3 | DB注释(中文) |
| 443 | IMPACT2_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验2纤维断面率单值判定 | SCO_DATA_DIC(D) |
| 444 | IMPACT2_SMP_AVG_RSLT | NUMBER | Y |  | 冲击试验2试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 445 | IMPACT2_SMP_IND_RSLT1 | NUMBER | Y |  | 冲击试验2试样侧膨胀值单值实绩1 | DB注释(中文) |
| 446 | IMPACT2_SMP_IND_RSLT2 | NUMBER | Y |  | 冲击试验2试样侧膨胀值单值实绩2 | DB注释(中文) |
| 447 | IMPACT2_SMP_IND_RSLT3 | NUMBER | Y |  | 冲击试验2试样侧膨胀值单值实绩3 | DB注释(中文) |
| 448 | IMPACT2_SMP_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验2试样侧膨胀值单值判定 | SCO_DATA_DIC(D) |
| 449 | IMPACT3_TEMP_RSLT | NUMBER | Y |  | 冲击试验3温度实绩 | SCO_DATA_DIC(D) |
| 450 | IMPACT3_CREAK_CD | VARCHAR2(1) | Y |  | 冲击试验3缺口类型 | SCO_DATA_DIC(D) |
| 451 | IMPACT3_ENERGY_CD | VARCHAR2(1) | Y |  | 冲击试验3试样能量值类型 | SCO_DATA_DIC(D) |
| 452 | IMPACT3_AVG_RSLT | NUMBER | Y |  | 冲击试验3平均值实绩 | SCO_DATA_DIC(D) |
| 453 | IMPACT3_IND_RSLT1 | NUMBER | Y |  | 冲击试验3单值实绩1 | SCO_DATA_DIC(D) |
| 454 | IMPACT3_IND_RSLT2 | NUMBER | Y |  | 冲击试验3单值实绩2 | SCO_DATA_DIC(D) |
| 455 | IMPACT3_IND_RSLT3 | NUMBER | Y |  | 冲击试验3单值实绩3 | SCO_DATA_DIC(D) |
| 456 | IMPACT3_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验3单值判定 | SCO_DATA_DIC(D) |
| 457 | IMPACT3_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 冲击试验3纤维断面率平均值实绩 | SCO_DATA_DIC(D) |
| 458 | IMPACT3_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 冲击试验3纤维断面率单值实绩1 | SCO_DATA_DIC(D) |
| 459 | IMPACT3_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 冲击试验3纤维断面率单值实绩2 | SCO_DATA_DIC(D) |
| 460 | IMPACT3_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 冲击试验3纤维断面率单值实绩3 | SCO_DATA_DIC(D) |
| 461 | IMPACT3_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验3纤维断面率单值判定 | SCO_DATA_DIC(D) |
| 462 | IMPACT3_SMP_AVG_RSLT | NUMBER | Y |  | 冲击试验3试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 463 | IMPACT3_SMP_IND_RSLT1 | NUMBER | Y |  | 冲击试验3试样侧膨胀值单值实绩1 | SCO_DATA_DIC(D) |
| 464 | IMPACT3_SMP_IND_RSLT2 | NUMBER | Y |  | 冲击试验3试样侧膨胀值单值实绩2 | SCO_DATA_DIC(D) |
| 465 | IMPACT3_SMP_IND_RSLT3 | NUMBER | Y |  | 冲击试验3试样侧膨胀值单值实绩3 | SCO_DATA_DIC(D) |
| 466 | IMPACT3_SMP_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验3试样侧膨胀值单值判定 | SCO_DATA_DIC(D) |
| 467 | IMPACT4_TEMP_RSLT | NUMBER | Y |  | 冲击试验4温度实绩 | DB注释(中文) |
| 468 | IMPACT4_CREAK_CD | VARCHAR2(1) | Y |  | 冲击试验4缺口类型 | DB注释(中文) |
| 469 | IMPACT4_ENERGY_CD | VARCHAR2(1) | Y |  | 冲击试验4试样能量值类型 | SCO_DATA_DIC(D) |
| 470 | IMPACT4_AVG_RSLT | NUMBER | Y |  | 冲击试验4平均值实绩 | SCO_DATA_DIC(D) |
| 471 | IMPACT4_IND_RSLT1 | NUMBER | Y |  | 冲击试验4单值实绩1 | DB注释(中文) |
| 472 | IMPACT4_IND_RSLT2 | NUMBER | Y |  | 冲击试验4单值实绩2 | DB注释(中文) |
| 473 | IMPACT4_IND_RSLT3 | NUMBER | Y |  | 冲击试验4单值实绩3 | DB注释(中文) |
| 474 | IMPACT4_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验4单值判定 | SCO_DATA_DIC(D) |
| 475 | IMPACT4_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 冲击试验4纤维断面率平均值实绩 | SCO_DATA_DIC(D) |
| 476 | IMPACT4_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 冲击试验4纤维断面率单值实绩1 | DB注释(中文) |
| 477 | IMPACT4_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 冲击试验4纤维断面率单值实绩2 | DB注释(中文) |
| 478 | IMPACT4_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 冲击试验4纤维断面率单值实绩3 | DB注释(中文) |
| 479 | IMPACT4_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验4纤维断面率单值判定 | SCO_DATA_DIC(D) |
| 480 | IMPACT4_SMP_AVG_RSLT | NUMBER | Y |  | 冲击试验4试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 481 | IMPACT4_SMP_IND_RSLT1 | NUMBER | Y |  | 冲击试验4试样侧膨胀值单值实绩1 | DB注释(中文) |
| 482 | IMPACT4_SMP_IND_RSLT2 | NUMBER | Y |  | 冲击试验4试样侧膨胀值单值实绩2 | DB注释(中文) |
| 483 | IMPACT4_SMP_IND_RSLT3 | NUMBER | Y |  | 冲击试验4试样侧膨胀值单值实绩3 | DB注释(中文) |
| 484 | IMPACT4_SMP_IND_JDG | VARCHAR2(1) | Y |  | 冲击试验4试样侧膨胀值单值判定 | SCO_DATA_DIC(D) |
| 485 | PW_TSL_YP_CD | VARCHAR2(1) | Y |  | 模拟焊后 拉伸测试屈服强度类型 | SCO_DATA_DIC(D) |
| 486 | PW_TSL_YP_RSLT | NUMBER | Y |  | 模拟焊后 拉伸测试屈服强度实绩 | SCO_DATA_DIC(D) |
| 487 | PW_TSL_YP_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸测试屈服强度判定 | SCO_DATA_DIC(D) |
| 488 | PW_TSL_TS_RSLT | NUMBER | Y |  | 模拟焊后 拉伸测试抗拉强度实绩 | SCO_DATA_DIC(D) |
| 489 | PW_TSL_TS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸测试抗拉强度判定 | SCO_DATA_DIC(D) |
| 490 | PW_TSL_YP_TS_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比YP/TS实绩 | SCO_DATA_DIC(D) |
| 491 | PW_TSL_YP_TS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比YP/TS判定 | SCO_DATA_DIC(D) |
| 492 | PW_TSL_RT05_RM_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比Rt0.5/Rm实绩 | SCO_DATA_DIC(D) |
| 493 | PW_TSL_RT05_RM_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比Rt0.5/Rm判定 | SCO_DATA_DIC(D) |
| 494 | PW_TSL_RT15_RT05_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5实绩 | SCO_DATA_DIC(D) |
| 495 | PW_TSL_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5判定 | SCO_DATA_DIC(D) |
| 496 | PW_TSL_RT20_RT10_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 497 | PW_TSL_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0判定 | SCO_DATA_DIC(D) |
| 498 | PW_TSL_RT50_RT10_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 499 | PW_TSL_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0判定 | SCO_DATA_DIC(D) |
| 500 | PW_TSL_CT_EX_RA_RSLT | NUMBER | Y |  | 模拟焊后 拉抻测试断后伸长率实绩 | SCO_DATA_DIC(D) |
| 501 | PW_TSL_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 模拟焊后 拉抻测试断后伸长率类型 | SCO_DATA_DIC(D) |
| 502 | PW_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉抻测试断后伸长率判定 | SCO_DATA_DIC(D) |
| 503 | PW_TSL_CT_RA_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验均匀伸长率实绩 | SCO_DATA_DIC(D) |
| 504 | PW_TSL_CT_RA_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验均匀伸长率判定 | SCO_DATA_DIC(D) |
| 505 | PW_TSL_RA_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验断面收缩率实绩 | SCO_DATA_DIC(D) |
| 506 | PW_TSL_RA_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验断面收缩率判定 | SCO_DATA_DIC(D) |
| 507 | PW_TSL_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 模拟焊后 消应力处理_保温温度实绩 | DB注释(中文) |
| 508 | PW_TSL_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 模拟焊后 消应力处理_保温时间实绩 | DB注释(中文) |
| 509 | PW_TSL_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 模拟焊后 消应力处理_冷却方式 | DB注释(中文) |
| 510 | PW_TSL_STRESS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 消应力处理_判定 | DB注释(中文) |
| 511 | PW_IMPACT_TEMP_RSLT | NUMBER | Y |  | 模拟焊后 冲击测试温度实绩 | DB注释(中文) |
| 512 | PW_IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 模拟焊后 冲击测试缺口类型 | DB注释(中文) |
| 513 | PW_IMPACT_ENERGY_CD | VARCHAR2(1) | Y |  | 模拟焊后 冲击试样能量值类型 | SCO_DATA_DIC(D) |
| 514 | PW_IMPACT_AVG_RSLT | NUMBER | Y |  | 模拟焊后 冲击测试平均值实绩 | SCO_DATA_DIC(D) |
| 515 | PW_IMPACT_IND_RSLT1 | NUMBER | Y |  | 模拟焊后 冲击测试单值实绩1 | DB注释(中文) |
| 516 | PW_IMPACT_IND_RSLT2 | NUMBER | Y |  | 模拟焊后 冲击测试单值实绩2 | DB注释(中文) |
| 517 | PW_IMPACT_IND_RSLT3 | NUMBER | Y |  | 模拟焊后 冲击测试单值实绩3 | DB注释(中文) |
| 518 | PW_IMPACT_IND_JDG | VARCHAR2(1) | Y |  | 模拟焊后 冲击测试单值判定 | SCO_DATA_DIC(D) |
| 519 | PW_IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 模拟焊后 纤维断面率平均值实绩 | SCO_DATA_DIC(D) |
| 520 | PW_IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 模拟焊后 纤维断面率单值实绩1 | DB注释(中文) |
| 521 | PW_IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 模拟焊后 纤维断面率单值实绩2 | DB注释(中文) |
| 522 | PW_IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 模拟焊后 纤维断面率单值实绩3 | DB注释(中文) |
| 523 | PW_IMPACT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 模拟焊后 纤维断面率单值判定 | SCO_DATA_DIC(D) |
| 524 | PW_IMPACT_SMP_AVG_RSLT | NUMBER | Y |  | 模拟焊后 冲击试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 525 | PW_IMPACT_SMP_IND_RSLT1 | NUMBER | Y |  | 模拟焊后 冲击试样侧膨胀值单值实绩1 | DB注释(中文) |
| 526 | PW_IMPACT_SMP_IND_RSLT2 | NUMBER | Y |  | 模拟焊后 冲击试样侧膨胀值单值实绩2 | DB注释(中文) |
| 527 | PW_IMPACT_SMP_IND_RSLT3 | NUMBER | Y |  | 模拟焊后 冲击试样侧膨胀值单值实绩3 | DB注释(中文) |
| 528 | PW_IMPACT_SMP_IND_JDG | VARCHAR2(1) | Y |  | 模拟焊后 冲击试样侧膨胀值单值判定 | SCO_DATA_DIC(D) |
| 529 | PW_MGRPHY_MTLGRP_TY | VARCHAR2(20) | Y |  | 模拟焊后 组织类型 | SCO_DATA_DIC(D) |
| 530 | PW_MGRPHY_MTLGRP_TY_PROVIDE | VARCHAR2(1) | Y |  | 模拟焊后 组织类型是否提供 | SCO_DATA_DIC(D) |
| 531 | PW_MGRPHY_BAND_STRC_MAX_RSLT | NUMBER | Y |  | 模拟焊后 带状组织等级上限实绩 | SCO_DATA_DIC(D) |
| 532 | PW_MGRPHY_BAND_STRC_MAX_JDG | VARCHAR2(1) | Y |  | 模拟焊后 带状组织等级上限判定 | SCO_DATA_DIC(D) |
| 533 | PW_MGRPHY_RSLT | NUMBER | Y |  |  | 空 |
| 534 | PW_MGRPHY_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 535 | PW_MGRPHY_FGS_RSLT | NUMBER | Y |  | 模拟焊后 铁素体晶粒度实绩 | SCO_DATA_DIC(D) |
| 536 | PW_MGRPHY_FGS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 铁素体晶粒度判定 | SCO_DATA_DIC(D) |
| 537 | PW_MGRPHY_AGS_RSLT | NUMBER | Y |  | 模拟焊后 奥氏体晶粒度实绩 | SCO_DATA_DIC(D) |
| 538 | PW_MGRPHY_AGS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 奥氏体晶粒度判定 | SCO_DATA_DIC(D) |
| 539 | PW_MGRPHY_GRNSZ_OCCP_RSLT | NUMBER | Y |  | 模拟焊后 金相测试基相的体积分数实绩 | SCO_DATA_DIC(D) |
| 540 | PW_MGRPHY_GRNSZ_OCCP_JDG | VARCHAR2(1) | Y |  | 模拟焊后 金相测试基相的体积分数判定 | SCO_DATA_DIC(D) |
| 541 | PW_BEND_DIA | NUMBER | Y |  | 模拟焊后 弯曲测试弯心直径 | SCO_DATA_DIC(D) |
| 542 | PW_BEND_ANGLE | NUMBER | Y |  | 模拟焊后 弯曲测试弯曲角度 | SCO_DATA_DIC(D) |
| 543 | PW_BEND_RSLT | VARCHAR2(1) | Y |  | 模拟焊后 弯曲测试实绩 | SCO_DATA_DIC(D) |
| 544 | PW_BEND_JDG | VARCHAR2(1) | Y |  | 模拟焊后 弯曲测试判定 | SCO_DATA_DIC(D) |
| 545 | PW_Z_TSL_CUT_IND_RSLT1 | NUMBER | Y |  |  | 空 |
| 546 | PW_Z_TSL_CUT_IND_RSLT2 | NUMBER | Y |  |  | 空 |
| 547 | PW_Z_TSL_CUT_IND_RSLT3 | NUMBER | Y |  |  | 空 |
| 548 | PW_Z_TSL_CUT_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 549 | PW_Z_TSL_CUT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 550 | PW_Z_TSL_CUT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 551 | PW_Z_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 552 | PW_Z_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 553 | PW_Z_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 554 | PW_Z_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 555 | PW_Z_TSL_CT_EX_RA_RSLT | NUMBER | Y |  |  | 空 |
| 556 | PW_Z_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 557 | PW_HIGH_TEMP_TSL_STAND_CD | VARCHAR2(20) | Y |  |  | 空 |
| 558 | PW_HIGH_TEMP_TSL_TEMP_RSLT | NUMBER | Y |  |  | 空 |
| 559 | PW_HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 560 | PW_HIGH_TEMP_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 561 | PW_HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  |  | 空 |
| 562 | PW_HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 563 | PW_HIGH_TEMP_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 564 | PW_HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  |  | 空 |
| 565 | PW_HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  |  | 空 |
| 566 | PW_HIGH_TEMP_TSL_EL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 567 | PW_HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  |  | 空 |
| 568 | PW_HIGH_TEMP_TSL_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 569 | PW_SSCC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 570 | PW_SSCC_STRESS_TY | VARCHAR2(1) | Y |  |  | 空 |
| 571 | PW_SSCC_STRESS_TST_VAL_RSLT | NUMBER | Y |  |  | 空 |
| 572 | PW_SSCC_STRESS_TST_VAL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 573 | PW_SSCC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 574 | PW_HIC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 575 | PW_HIC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 576 | PW_HIC_CLR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 577 | PW_HIC_CLR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 578 | PW_HIC_CLR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 579 | PW_HIC_CLR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 580 | PW_HIC_CLR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 581 | PW_HIC_CLR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 582 | PW_HIC_CLR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 583 | PW_HIC_CLR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 584 | PW_HIC_CLR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 585 | PW_HIC_CLR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 586 | PW_HIC_CLR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 587 | PW_HIC_CLR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 588 | PW_HIC_CLR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 589 | PW_HIC_CLR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 590 | PW_HIC_CLR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 591 | PW_HIC_CLR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 592 | PW_HIC_CSR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 593 | PW_HIC_CSR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 594 | PW_HIC_CSR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 595 | PW_HIC_CSR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 596 | PW_HIC_CSR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 597 | PW_HIC_CSR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 598 | PW_HIC_CSR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 599 | PW_HIC_CSR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 600 | PW_HIC_CSR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 601 | PW_HIC_CSR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 602 | PW_HIC_CSR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 603 | PW_HIC_CSR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 604 | PW_HIC_CSR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 605 | PW_HIC_CSR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 606 | PW_HIC_CSR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 607 | PW_HIC_CSR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 608 | PW_HIC_CTR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 609 | PW_HIC_CTR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 610 | PW_HIC_CTR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 611 | PW_HIC_CTR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 612 | PW_HIC_CTR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 613 | PW_HIC_CTR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 614 | PW_HIC_CTR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 615 | PW_HIC_CTR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 616 | PW_HIC_CTR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 617 | PW_HIC_CTR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 618 | PW_HIC_CTR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 619 | PW_HIC_CTR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 620 | PW_HIC_CTR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 621 | PW_HIC_CTR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 622 | PW_HIC_CTR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 623 | PW_HIC_CTR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 624 | PW_HARD_KIND | VARCHAR2(1) | Y |  |  | 空 |
| 625 | PW_HARD_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 626 | PW_HARD_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 627 | PW_HARD_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 628 | MXPW_TSL_YP_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸测试屈服强度类型 | SCO_DATA_DIC(D) |
| 629 | MXPW_TSL_YP_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸测试屈服强度实绩 | SCO_DATA_DIC(D) |
| 630 | MXPW_TSL_YP_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸测试屈服强度判定 | SCO_DATA_DIC(D) |
| 631 | MXPW_TSL_TS_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸测试抗拉强度实绩 | SCO_DATA_DIC(D) |
| 632 | MXPW_TSL_TS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸测试抗拉强度判定 | SCO_DATA_DIC(D) |
| 633 | MXPW_TSL_YP_TS_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比YP/TS实绩 | SCO_DATA_DIC(D) |
| 634 | MXPW_TSL_YP_TS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比YP/TS判定 | SCO_DATA_DIC(D) |
| 635 | MXPW_TSL_RT05_RM_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比Rt0.5/Rm实绩 | SCO_DATA_DIC(D) |
| 636 | MXPW_TSL_RT05_RM_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比Rt0.5/Rm判定 | SCO_DATA_DIC(D) |
| 637 | MXPW_TSL_RT15_RT05_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5实绩 | SCO_DATA_DIC(D) |
| 638 | MXPW_TSL_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5判定 | SCO_DATA_DIC(D) |
| 639 | MXPW_TSL_RT20_RT10_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 640 | MXPW_TSL_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0判定 | SCO_DATA_DIC(D) |
| 641 | MXPW_TSL_RT50_RT10_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 642 | MXPW_TSL_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0判定 | SCO_DATA_DIC(D) |
| 643 | MXPW_TSL_CT_EX_RA_RSLT | NUMBER | Y |  | 最大模拟焊后 拉抻测试断后伸长率实绩 | SCO_DATA_DIC(D) |
| 644 | MXPW_TSL_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 拉抻测试断后伸长率类型 | SCO_DATA_DIC(D) |
| 645 | MXPW_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉抻测试断后伸长率判定 | SCO_DATA_DIC(D) |
| 646 | MXPW_TSL_CT_RA_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验均匀伸长率实绩 | SCO_DATA_DIC(D) |
| 647 | MXPW_TSL_CT_RA_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验均匀伸长率判定 | SCO_DATA_DIC(D) |
| 648 | MXPW_TSL_RA_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验断面收缩率实绩 | SCO_DATA_DIC(D) |
| 649 | MXPW_TSL_RA_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验断面收缩率判定 | SCO_DATA_DIC(D) |
| 650 | MXPW_TSL_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 最大模拟焊后 消应力处理_保温温度实绩 | DB注释(中文) |
| 651 | MXPW_TSL_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 最大模拟焊后 消应力处理_保温时间实绩 | DB注释(中文) |
| 652 | MXPW_TSL_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 消应力处理_冷却方式 | DB注释(中文) |
| 653 | MXPW_TSL_STRESS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 消应力处理_判定 | DB注释(中文) |
| 654 | MXPW_IMPACT_TEMP_RSLT | NUMBER | Y |  | 最大模拟焊后 冲击测试温度实绩 | DB注释(中文) |
| 655 | MXPW_IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 冲击测试缺口类型 | DB注释(中文) |
| 656 | MXPW_IMPACT_ENERGY_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 冲击试样能量值类型 | SCO_DATA_DIC(D) |
| 657 | MXPW_IMPACT_AVG_RSLT | NUMBER | Y |  | 最大模拟焊后 冲击测试平均值实绩 | SCO_DATA_DIC(D) |
| 658 | MXPW_IMPACT_IND_RSLT1 | NUMBER | Y |  | 最大模拟焊后 冲击测试单值实绩1 | DB注释(中文) |
| 659 | MXPW_IMPACT_IND_RSLT2 | NUMBER | Y |  | 最大模拟焊后 冲击测试单值实绩2 | DB注释(中文) |
| 660 | MXPW_IMPACT_IND_RSLT3 | NUMBER | Y |  | 最大模拟焊后 冲击测试单值实绩3 | DB注释(中文) |
| 661 | MXPW_IMPACT_IND_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 冲击测试单值判定 | SCO_DATA_DIC(D) |
| 662 | MXPW_IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 最大模拟焊后 纤维断面率平均值实绩 | SCO_DATA_DIC(D) |
| 663 | MXPW_IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 最大模拟焊后 纤维断面率单值实绩1 | DB注释(中文) |
| 664 | MXPW_IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 最大模拟焊后 纤维断面率单值实绩2 | DB注释(中文) |
| 665 | MXPW_IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 最大模拟焊后 纤维断面率单值实绩3 | DB注释(中文) |
| 666 | MXPW_IMPACT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 纤维断面率单值判定 | SCO_DATA_DIC(D) |
| 667 | MXPW_IMPACT_SMP_AVG_RSLT | NUMBER | Y |  | 最大模拟焊后 冲击试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 668 | MXPW_IMPACT_SMP_IND_RSLT1 | NUMBER | Y |  | 最大模拟焊后 冲击试样侧膨胀值单值实绩1 | DB注释(中文) |
| 669 | MXPW_IMPACT_SMP_IND_RSLT2 | NUMBER | Y |  | 最大模拟焊后 冲击试样侧膨胀值单值实绩2 | DB注释(中文) |
| 670 | MXPW_IMPACT_SMP_IND_RSLT3 | NUMBER | Y |  | 最大模拟焊后 冲击试样侧膨胀值单值实绩3 | DB注释(中文) |
| 671 | MXPW_IMPACT_SMP_IND_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 冲击试样侧膨胀值单值判定 | SCO_DATA_DIC(D) |
| 672 | MXPW_MGRPHY_MTLGRP_TY | VARCHAR2(20) | Y |  | 最大模拟焊后 组织类型 | SCO_DATA_DIC(D) |
| 673 | MXPW_MGRPHY_MTLGRP_TY_PROVIDE | VARCHAR2(1) | Y |  | 最大模拟焊后 组织类型是否提供 | SCO_DATA_DIC(D) |
| 674 | MXPW_MGRPHY_BAND_STRC_MAX_RSLT | NUMBER | Y |  | 最大模拟焊后 带状组织等级上限实绩 | SCO_DATA_DIC(D) |
| 675 | MXPW_MGRPHY_BAND_STRC_MAX_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 带状组织等级上限判定 | SCO_DATA_DIC(D) |
| 676 | MXPW_MGRPHY_RSLT | NUMBER | Y |  |  | 空 |
| 677 | MXPW_MGRPHY_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 678 | MXPW_MGRPHY_FGS_RSLT | NUMBER | Y |  | 最大模拟焊后 铁素体晶粒度实绩 | SCO_DATA_DIC(D) |
| 679 | MXPW_MGRPHY_FGS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 铁素体晶粒度判定 | SCO_DATA_DIC(D) |
| 680 | MXPW_MGRPHY_AGS_RSLT | NUMBER | Y |  | 最大模拟焊后 奥氏体晶粒度实绩 | SCO_DATA_DIC(D) |
| 681 | MXPW_MGRPHY_AGS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 奥氏体晶粒度判定 | SCO_DATA_DIC(D) |
| 682 | MXPW_MGRPHY_GRNSZ_OCCP_RSLT | NUMBER | Y |  | 最大模拟焊后 金相测试基相的体积分数实绩 | SCO_DATA_DIC(D) |
| 683 | MXPW_MGRPHY_GRNSZ_OCCP_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 金相测试基相的体积分数判定 | SCO_DATA_DIC(D) |
| 684 | MXPW_BEND_DIA | NUMBER | Y |  | 最大模拟焊后 弯曲测试弯心直径 | SCO_DATA_DIC(D) |
| 685 | MXPW_BEND_ANGLE | NUMBER | Y |  | 最大模拟焊后 弯曲测试弯曲角度 | SCO_DATA_DIC(D) |
| 686 | MXPW_BEND_RSLT | VARCHAR2(1) | Y |  | 最大模拟焊后 弯曲测试实绩 | SCO_DATA_DIC(D) |
| 687 | MXPW_BEND_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 弯曲测试判定 | SCO_DATA_DIC(D) |
| 688 | MXPW_Z_TSL_CUT_IND_RSLT1 | NUMBER | Y |  |  | 空 |
| 689 | MXPW_Z_TSL_CUT_IND_RSLT2 | NUMBER | Y |  |  | 空 |
| 690 | MXPW_Z_TSL_CUT_IND_RSLT3 | NUMBER | Y |  |  | 空 |
| 691 | MXPW_Z_TSL_CUT_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 692 | MXPW_Z_TSL_CUT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 693 | MXPW_Z_TSL_CUT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 694 | MXPW_Z_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 695 | MXPW_Z_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 696 | MXPW_Z_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 697 | MXPW_Z_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 698 | MXPW_Z_TSL_CT_EX_RA_RSLT | NUMBER | Y |  |  | 空 |
| 699 | MXPW_Z_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 700 | MXPW_HIGH_TEMP_TSL_STAND_CD | VARCHAR2(20) | Y |  |  | 空 |
| 701 | MXPW_HIGH_TEMP_TSL_TEMP_RSLT | NUMBER | Y |  |  | 空 |
| 702 | MXPW_HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 703 | MXPW_HIGH_TEMP_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 704 | MXPW_HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  |  | 空 |
| 705 | MXPW_HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 706 | MXPW_HIGH_TEMP_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 707 | MXPW_HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  |  | 空 |
| 708 | MXPW_HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  |  | 空 |
| 709 | MXPW_HIGH_TEMP_TSL_EL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 710 | MXPW_HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  |  | 空 |
| 711 | MXPW_HIGH_TEMP_TSL_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 712 | MXPW_SSCC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 713 | MXPW_SSCC_STRESS_TY | VARCHAR2(1) | Y |  |  | 空 |
| 714 | MXPW_SSCC_STRESS_TST_VAL_RSLT | NUMBER | Y |  |  | 空 |
| 715 | MXPW_SSCC_STRESS_TST_VAL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 716 | MXPW_SSCC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 717 | MXPW_HIC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 718 | MXPW_HIC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 719 | MXPW_HIC_CLR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 720 | MXPW_HIC_CLR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 721 | MXPW_HIC_CLR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 722 | MXPW_HIC_CLR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 723 | MXPW_HIC_CLR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 724 | MXPW_HIC_CLR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 725 | MXPW_HIC_CLR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 726 | MXPW_HIC_CLR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 727 | MXPW_HIC_CLR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 728 | MXPW_HIC_CLR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 729 | MXPW_HIC_CLR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 730 | MXPW_HIC_CLR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 731 | MXPW_HIC_CLR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 732 | MXPW_HIC_CLR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 733 | MXPW_HIC_CLR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 734 | MXPW_HIC_CLR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 735 | MXPW_HIC_CSR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 736 | MXPW_HIC_CSR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 737 | MXPW_HIC_CSR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 738 | MXPW_HIC_CSR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 739 | MXPW_HIC_CSR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 740 | MXPW_HIC_CSR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 741 | MXPW_HIC_CSR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 742 | MXPW_HIC_CSR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 743 | MXPW_HIC_CSR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 744 | MXPW_HIC_CSR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 745 | MXPW_HIC_CSR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 746 | MXPW_HIC_CSR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 747 | MXPW_HIC_CSR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 748 | MXPW_HIC_CSR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 749 | MXPW_HIC_CSR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 750 | MXPW_HIC_CSR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 751 | MXPW_HIC_CTR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 752 | MXPW_HIC_CTR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 753 | MXPW_HIC_CTR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 754 | MXPW_HIC_CTR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 755 | MXPW_HIC_CTR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 756 | MXPW_HIC_CTR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 757 | MXPW_HIC_CTR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 758 | MXPW_HIC_CTR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 759 | MXPW_HIC_CTR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 760 | MXPW_HIC_CTR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 761 | MXPW_HIC_CTR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 762 | MXPW_HIC_CTR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 763 | MXPW_HIC_CTR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 764 | MXPW_HIC_CTR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 765 | MXPW_HIC_CTR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 766 | MXPW_HIC_CTR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 767 | MXPW_HARD_KIND | VARCHAR2(1) | Y |  |  | 空 |
| 768 | MXPW_HARD_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 769 | MXPW_HARD_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 770 | MXPW_HARD_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 771 | MNPW_TSL_YP_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸测试屈服强度类型 | SCO_DATA_DIC(D) |
| 772 | MNPW_TSL_YP_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸测试屈服强度实绩 | SCO_DATA_DIC(D) |
| 773 | MNPW_TSL_YP_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸测试屈服强度判定 | SCO_DATA_DIC(D) |
| 774 | MNPW_TSL_TS_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸测试抗拉强度实绩 | SCO_DATA_DIC(D) |
| 775 | MNPW_TSL_TS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸测试抗拉强度判定 | SCO_DATA_DIC(D) |
| 776 | MNPW_TSL_YP_TS_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比YP/TS实绩 | SCO_DATA_DIC(D) |
| 777 | MNPW_TSL_YP_TS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比YP/TS判定 | SCO_DATA_DIC(D) |
| 778 | MNPW_TSL_RT05_RM_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比Rt0.5/Rm实绩 | SCO_DATA_DIC(D) |
| 779 | MNPW_TSL_RT05_RM_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比Rt0.5/Rm判定 | SCO_DATA_DIC(D) |
| 780 | MNPW_TSL_RT15_RT05_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5实绩 | SCO_DATA_DIC(D) |
| 781 | MNPW_TSL_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5判定 | SCO_DATA_DIC(D) |
| 782 | MNPW_TSL_RT20_RT10_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 783 | MNPW_TSL_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0判定 | SCO_DATA_DIC(D) |
| 784 | MNPW_TSL_RT50_RT10_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 785 | MNPW_TSL_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0判定 | SCO_DATA_DIC(D) |
| 786 | MNPW_TSL_CT_EX_RA_RSLT | NUMBER | Y |  | 最小模拟焊后 拉抻测试断后伸长率实绩 | SCO_DATA_DIC(D) |
| 787 | MNPW_TSL_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 拉抻测试断后伸长率类型 | SCO_DATA_DIC(D) |
| 788 | MNPW_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉抻测试断后伸长率判定 | SCO_DATA_DIC(D) |
| 789 | MNPW_TSL_CT_RA_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验均匀伸长率实绩 | SCO_DATA_DIC(D) |
| 790 | MNPW_TSL_CT_RA_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验均匀伸长率判定 | SCO_DATA_DIC(D) |
| 791 | MNPW_TSL_RA_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验断面收缩率实绩 | SCO_DATA_DIC(D) |
| 792 | MNPW_TSL_RA_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验断面收缩率判定 | SCO_DATA_DIC(D) |
| 793 | MNPW_TSL_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 最小模拟焊后 消应力处理_保温温度实绩 | DB注释(中文) |
| 794 | MNPW_TSL_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 最小模拟焊后 消应力处理_保温时间实绩 | DB注释(中文) |
| 795 | MNPW_TSL_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 消应力处理_冷却方式 | DB注释(中文) |
| 796 | MNPW_TSL_STRESS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 消应力处理_判定 | DB注释(中文) |
| 797 | MNPW_IMPACT_TEMP_RSLT | NUMBER | Y |  | 最小模拟焊后 冲击测试温度实绩 | DB注释(中文) |
| 798 | MNPW_IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 冲击测试缺口类型 | DB注释(中文) |
| 799 | MNPW_IMPACT_ENERGY_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 冲击试样能量值类型 | SCO_DATA_DIC(D) |
| 800 | MNPW_IMPACT_AVG_RSLT | NUMBER | Y |  | 最小模拟焊后 冲击测试平均值实绩 | SCO_DATA_DIC(D) |
| 801 | MNPW_IMPACT_IND_RSLT1 | NUMBER | Y |  | 最小模拟焊后 冲击测试单值实绩1 | DB注释(中文) |
| 802 | MNPW_IMPACT_IND_RSLT2 | NUMBER | Y |  | 最小模拟焊后 冲击测试单值实绩2 | DB注释(中文) |
| 803 | MNPW_IMPACT_IND_RSLT3 | NUMBER | Y |  | 最小模拟焊后 冲击测试单值实绩3 | DB注释(中文) |
| 804 | MNPW_IMPACT_IND_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 冲击测试单值判定 | SCO_DATA_DIC(D) |
| 805 | MNPW_IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 最小模拟焊后 纤维断面率平均值实绩 | SCO_DATA_DIC(D) |
| 806 | MNPW_IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 最小模拟焊后 纤维断面率单值实绩1 | DB注释(中文) |
| 807 | MNPW_IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 最小模拟焊后 纤维断面率单值实绩2 | DB注释(中文) |
| 808 | MNPW_IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 最小模拟焊后 纤维断面率单值实绩3 | DB注释(中文) |
| 809 | MNPW_IMPACT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 纤维断面率单值判定 | SCO_DATA_DIC(D) |
| 810 | MNPW_IMPACT_SMP_AVG_RSLT | NUMBER | Y |  | 最小模拟焊后 冲击试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 811 | MNPW_IMPACT_SMP_IND_RSLT1 | NUMBER | Y |  | 最小模拟焊后 冲击试样侧膨胀值单值实绩1 | DB注释(中文) |
| 812 | MNPW_IMPACT_SMP_IND_RSLT2 | NUMBER | Y |  | 最小模拟焊后 冲击试样侧膨胀值单值实绩2 | DB注释(中文) |
| 813 | MNPW_IMPACT_SMP_IND_RSLT3 | NUMBER | Y |  | 最小模拟焊后 冲击试样侧膨胀值单值实绩3 | DB注释(中文) |
| 814 | MNPW_IMPACT_SMP_IND_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 冲击试样侧膨胀值单值判定 | SCO_DATA_DIC(D) |
| 815 | MNPW_MGRPHY_MTLGRP_TY | VARCHAR2(20) | Y |  | 最小模拟焊后 组织类型 | SCO_DATA_DIC(D) |
| 816 | MNPW_MGRPHY_MTLGRP_TY_PROVIDE | VARCHAR2(1) | Y |  | 最小模拟焊后 组织类型是否提供 | SCO_DATA_DIC(D) |
| 817 | MNPW_MGRPHY_BAND_STRC_MAX_RSLT | NUMBER | Y |  | 最小模拟焊后 带状组织等级上限实绩 | SCO_DATA_DIC(D) |
| 818 | MNPW_MGRPHY_BAND_STRC_MAX_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 带状组织等级上限判定 | SCO_DATA_DIC(D) |
| 819 | MNPW_MGRPHY_RSLT | NUMBER | Y |  |  | 空 |
| 820 | MNPW_MGRPHY_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 821 | MNPW_MGRPHY_FGS_RSLT | NUMBER | Y |  | 最小模拟焊后 铁素体晶粒度实绩 | SCO_DATA_DIC(D) |
| 822 | MNPW_MGRPHY_FGS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 铁素体晶粒度判定 | SCO_DATA_DIC(D) |
| 823 | MNPW_MGRPHY_AGS_RSLT | NUMBER | Y |  | 最小模拟焊后 奥氏体晶粒度实绩 | SCO_DATA_DIC(D) |
| 824 | MNPW_MGRPHY_AGS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 奥氏体晶粒度判定 | SCO_DATA_DIC(D) |
| 825 | MNPW_MGRPHY_GRNSZ_OCCP_RSLT | NUMBER | Y |  | 最小模拟焊后 金相测试基相的体积分数实绩 | SCO_DATA_DIC(D) |
| 826 | MNPW_MGRPHY_GRNSZ_OCCP_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 金相测试基相的体积分数判定 | SCO_DATA_DIC(D) |
| 827 | MNPW_BEND_DIA | NUMBER | Y |  | 最小模拟焊后 弯曲测试弯心直径 | SCO_DATA_DIC(D) |
| 828 | MNPW_BEND_ANGLE | NUMBER | Y |  | 最小模拟焊后 弯曲测试弯曲角度 | SCO_DATA_DIC(D) |
| 829 | MNPW_BEND_RSLT | VARCHAR2(1) | Y |  | 最小模拟焊后 弯曲测试实绩 | SCO_DATA_DIC(D) |
| 830 | MNPW_BEND_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 弯曲测试判定 | SCO_DATA_DIC(D) |
| 831 | MNPW_Z_TSL_CUT_IND_RSLT1 | NUMBER | Y |  |  | 空 |
| 832 | MNPW_Z_TSL_CUT_IND_RSLT2 | NUMBER | Y |  |  | 空 |
| 833 | MNPW_Z_TSL_CUT_IND_RSLT3 | NUMBER | Y |  |  | 空 |
| 834 | MNPW_Z_TSL_CUT_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 835 | MNPW_Z_TSL_CUT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 836 | MNPW_Z_TSL_CUT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 837 | MNPW_Z_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 838 | MNPW_Z_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 839 | MNPW_Z_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 840 | MNPW_Z_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 841 | MNPW_Z_TSL_CT_EX_RA_RSLT | NUMBER | Y |  |  | 空 |
| 842 | MNPW_Z_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 843 | MNPW_HIGH_TEMP_TSL_STAND_CD | VARCHAR2(20) | Y |  |  | 空 |
| 844 | MNPW_HIGH_TEMP_TSL_TEMP_RSLT | NUMBER | Y |  |  | 空 |
| 845 | MNPW_HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 846 | MNPW_HIGH_TEMP_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 847 | MNPW_HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  |  | 空 |
| 848 | MNPW_HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 849 | MNPW_HIGH_TEMP_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 850 | MNPW_HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  |  | 空 |
| 851 | MNPW_HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  |  | 空 |
| 852 | MNPW_HIGH_TEMP_TSL_EL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 853 | MNPW_HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  |  | 空 |
| 854 | MNPW_HIGH_TEMP_TSL_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 855 | MNPW_SSCC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 856 | MNPW_SSCC_STRESS_TY | VARCHAR2(1) | Y |  |  | 空 |
| 857 | MNPW_SSCC_STRESS_TST_VAL_RSLT | NUMBER | Y |  |  | 空 |
| 858 | MNPW_SSCC_STRESS_TST_VAL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 859 | MNPW_SSCC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 860 | MNPW_HIC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 861 | MNPW_HIC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 862 | MNPW_HIC_CLR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 863 | MNPW_HIC_CLR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 864 | MNPW_HIC_CLR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 865 | MNPW_HIC_CLR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 866 | MNPW_HIC_CLR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 867 | MNPW_HIC_CLR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 868 | MNPW_HIC_CLR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 869 | MNPW_HIC_CLR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 870 | MNPW_HIC_CLR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 871 | MNPW_HIC_CLR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 872 | MNPW_HIC_CLR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 873 | MNPW_HIC_CLR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 874 | MNPW_HIC_CLR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 875 | MNPW_HIC_CLR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 876 | MNPW_HIC_CLR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 877 | MNPW_HIC_CLR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 878 | MNPW_HIC_CSR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 879 | MNPW_HIC_CSR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 880 | MNPW_HIC_CSR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 881 | MNPW_HIC_CSR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 882 | MNPW_HIC_CSR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 883 | MNPW_HIC_CSR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 884 | MNPW_HIC_CSR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 885 | MNPW_HIC_CSR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 886 | MNPW_HIC_CSR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 887 | MNPW_HIC_CSR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 888 | MNPW_HIC_CSR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 889 | MNPW_HIC_CSR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 890 | MNPW_HIC_CSR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 891 | MNPW_HIC_CSR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 892 | MNPW_HIC_CSR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 893 | MNPW_HIC_CSR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 894 | MNPW_HIC_CTR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 895 | MNPW_HIC_CTR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 896 | MNPW_HIC_CTR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 897 | MNPW_HIC_CTR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 898 | MNPW_HIC_CTR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 899 | MNPW_HIC_CTR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 900 | MNPW_HIC_CTR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 901 | MNPW_HIC_CTR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 902 | MNPW_HIC_CTR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 903 | MNPW_HIC_CTR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 904 | MNPW_HIC_CTR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 905 | MNPW_HIC_CTR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 906 | MNPW_HIC_CTR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 907 | MNPW_HIC_CTR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 908 | MNPW_HIC_CTR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 909 | MNPW_HIC_CTR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 910 | MNPW_HARD_KIND | VARCHAR2(1) | Y |  |  | 空 |
| 911 | MNPW_HARD_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 912 | MNPW_HARD_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 913 | MNPW_HARD_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 914 | PROD_CHEM_SMP_CND | VARCHAR2(2) | Y |  | 产品成分分析取样条件 | SCO_DATA_DIC(D) |
| 915 | PROD_CHEM_ANAL_TY | VARCHAR2(1) | Y |  | 제품성분분석구분 | SCO_DATA_DIC(D) |
| 916 | C_RSLT | VARCHAR2(20) | Y |  | 产品成分C实绩 | DB注释(中文) |
| 917 | SI_RSLT | VARCHAR2(20) | Y |  | 产品成分Si实绩 | DB注释(中文) |
| 918 | MN_RSLT | VARCHAR2(20) | Y |  | 产品成分Mn实绩 | DB注释(中文) |
| 919 | P_RSLT | VARCHAR2(20) | Y |  | 产品成分P实绩 | DB注释(中文) |
| 920 | S_RSLT | VARCHAR2(20) | Y |  | 产品成分S实绩 | DB注释(中文) |
| 921 | SAL_RSLT | VARCHAR2(20) | Y |  | 产品成分Sol_Al实绩 | DB注释(中文) |
| 922 | TAL_RSLT | VARCHAR2(20) | Y |  | 产品成分Tot_Al实绩 | DB注释(中文) |
| 923 | AS_RSLT | VARCHAR2(20) | Y |  | 产品成分As实绩 | DB注释(中文) |
| 924 | BI_RSLT | VARCHAR2(20) | Y |  | 产品成分Bi实绩 | DB注释(中文) |
| 925 | B_RSLT | VARCHAR2(20) | Y |  | 产品成分B实绩 | DB注释(中文) |
| 926 | CA_RSLT | VARCHAR2(20) | Y |  | 产品成分Ca实绩 | DB注释(中文) |
| 927 | CO_RSLT | VARCHAR2(20) | Y |  | 产品成分Co实绩 | DB注释(中文) |
| 928 | CR_RSLT | VARCHAR2(20) | Y |  | 产品成分Cr实绩 | DB注释(中文) |
| 929 | CU_RSLT | VARCHAR2(20) | Y |  | 产品成分Cu实绩 | DB注释(中文) |
| 930 | H_RSLT | VARCHAR2(20) | Y |  | 产品成分H实绩 | DB注释(中文) |
| 931 | MG_RSLT | VARCHAR2(20) | Y |  | 产品成分Mg实绩 | DB注释(中文) |
| 932 | MO_RSLT | VARCHAR2(20) | Y |  | 产品成分Mo实绩 | DB注释(中文) |
| 933 | NB_RSLT | VARCHAR2(20) | Y |  | 产品成分Nb实绩 | DB注释(中文) |
| 934 | NI_RSLT | VARCHAR2(20) | Y |  | 产品成分Ni实绩 | DB注释(中文) |
| 935 | N_RSLT | VARCHAR2(20) | Y |  | 产品成分N实绩 | DB注释(中文) |
| 936 | O_RSLT | VARCHAR2(20) | Y |  | 产品成分O实绩 | DB注释(中文) |
| 937 | PB_RSLT | VARCHAR2(20) | Y |  | 产品成分Pb实绩 | DB注释(中文) |
| 938 | SB_RSLT | VARCHAR2(20) | Y |  | 产品成分Sb实绩 | DB注释(中文) |
| 939 | SN_RSLT | VARCHAR2(20) | Y |  | 产品成分Sn实绩 | DB注释(中文) |
| 940 | TE_RSLT | VARCHAR2(20) | Y |  | 产品成分Te实绩 | DB注释(中文) |
| 941 | TI_RSLT | VARCHAR2(20) | Y |  | 产品成分Ti实绩 | DB注释(中文) |
| 942 | V_RSLT | VARCHAR2(20) | Y |  | 产品成分V实绩 | DB注释(中文) |
| 943 | W_RSLT | VARCHAR2(20) | Y |  | 产品成分W实绩 | DB注释(中文) |
| 944 | ZN_RSLT | VARCHAR2(20) | Y |  | 产品成分Zn实绩 | DB注释(中文) |
| 945 | ZR_RSLT | VARCHAR2(20) | Y |  | 产品成分Zr实绩 | DB注释(中文) |
| 946 | CEQ_RSLT | VARCHAR2(20) | Y |  | 产品成分CEQ计算值 | DB注释(中文) |
| 947 | PCM_RSLT | VARCHAR2(20) | Y |  | 产品成分PCM计算值 | DB注释(中文) |
| 948 | PSR_RSLT | VARCHAR2(20) | Y |  | 产品成分PSR计算值 | DB注释(中文) |
| 949 | CFI_RSLT | VARCHAR2(20) | Y |  | 产品成分CFI计算值 | DB注释(中文) |
| 950 | CFJ_RSLT | VARCHAR2(20) | Y |  | 产品成分CFJ计算值 | DB注释(中文) |
| 951 | CFX_RSLT | VARCHAR2(20) | Y |  | 产品成分CFX计算值 | DB注释(中文) |
| 952 | QLT_REMARKS | VARCHAR2(300) | Y |  | 质量备注 | DB注释(中文) |
| 953 | HARD_RSLT1 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 954 | HARD_RSLT2 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 955 | HARD_RSLT3 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 956 | HARD_RSLT4 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 957 | HARD_RSLT5 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 958 | HARD_RSLT6 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 959 | HARD_RSLT7 | NUMBER | Y |  | 硬度测试实绩7 | DB注释(中文) |
| 960 | HARD_RSLT8 | NUMBER | Y |  | 硬度测试实绩8 | DB注释(中文) |
| 961 | HARD_RSLT9 | NUMBER | Y |  | 硬度测试实绩9 | DB注释(中文) |
| 962 | MNPW_HARD_RSLT1 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 963 | MNPW_HARD_RSLT2 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 964 | MNPW_HARD_RSLT3 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 965 | MNPW_HARD_RSLT4 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 966 | MNPW_HARD_RSLT5 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 967 | MNPW_HARD_RSLT6 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 968 | MNPW_HARD_RSLT7 | NUMBER | Y |  | 硬度测试实绩7 | DB注释(中文) |
| 969 | MNPW_HARD_RSLT8 | NUMBER | Y |  | 硬度测试实绩8 | DB注释(中文) |
| 970 | MNPW_HARD_RSLT9 | NUMBER | Y |  | 硬度测试实绩9 | DB注释(中文) |
| 971 | MXPW_HARD_RSLT1 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 972 | MXPW_HARD_RSLT2 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 973 | MXPW_HARD_RSLT3 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 974 | MXPW_HARD_RSLT4 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 975 | MXPW_HARD_RSLT5 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 976 | MXPW_HARD_RSLT6 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 977 | MXPW_HARD_RSLT7 | NUMBER | Y |  | 硬度测试实绩7 | DB注释(中文) |
| 978 | MXPW_HARD_RSLT8 | NUMBER | Y |  | 硬度测试实绩8 | DB注释(中文) |
| 979 | MXPW_HARD_RSLT9 | NUMBER | Y |  | 硬度测试实绩9 | DB注释(中文) |
| 980 | PW_HARD_RSLT1 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 981 | PW_HARD_RSLT2 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 982 | PW_HARD_RSLT3 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 983 | PW_HARD_RSLT4 | NUMBER | Y |  | 硬度测试实绩4 | DB注释(中文) |
| 984 | PW_HARD_RSLT5 | NUMBER | Y |  | 硬度测试实绩5 | DB注释(中文) |
| 985 | PW_HARD_RSLT6 | NUMBER | Y |  | 硬度测试实绩6 | DB注释(中文) |
| 986 | PW_HARD_RSLT7 | NUMBER | Y |  | 硬度测试实绩7 | DB注释(中文) |
| 987 | PW_HARD_RSLT8 | NUMBER | Y |  | 硬度测试实绩8 | DB注释(中文) |
| 988 | PW_HARD_RSLT9 | NUMBER | Y |  | 硬度测试实绩9 | DB注释(中文) |
| 989 | RE_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 990 | CEQ1_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 991 | CEQEXP_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 992 | CSOL_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 993 | CET_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 994 | CEQAWS_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 995 | CEQJIS_RSLT | VARCHAR2(20) | Y |  |  | 空 |
| 996 | TOT_AL_RSLT | VARCHAR2(20) | Y |  | 实绩TOT | DB注释(中文) |
| 997 | SOL_AL_RSLT | VARCHAR2(20) | Y |  | 实绩SOL | DB注释(中文) |
| 998 | WLYS10_RSLT | VARCHAR2(20) | Y |  | 产品成分WLYS10实绩 | DB注释(中文) |

### SQM_ORD_MECH_HRL

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=23｜被读 19 过程 / 被写 2 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：0　**主键**：ORD_NO、ORD_LN、QLT_DSN_STD_TY　**语义覆盖**：459/459

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 修改人 | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | 修改时间 | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | ORD_NO | VARCHAR2(10) | N | ✓ | 订单编号 | DB注释(中文) |
| 9 | ORD_LN | VARCHAR2(3) | N | ✓ | 订单行号 | DB注释(中文) |
| 10 | QLT_DSN_STD_TY | VARCHAR2(1) | N | ✓ | 质量设计标准区分(1-客户保证基准，2-公司保证基准，3-国家标准基准，4-合成) | DB注释(中文) |
| 11 | TSL_SMP_CND | VARCHAR2(2) | Y |  | 拉伸测试取样条件 | DB注释(中文) |
| 12 | TSL_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 拉伸测试长度方向取样位置 | DB注释(中文) |
| 13 | TSL_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 拉伸测试宽度方向取样位置 | DB注释(中文) |
| 14 | TSL_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 拉伸测试取样试样方向 | DB注释(中文) |
| 15 | TSL_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 拉伸测试取样试样号数 | DB注释(中文) |
| 16 | TSL_YP_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度保证代号(YP) | DB注释(中文) |
| 17 | TSL_YP_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度类型(YP) | DB注释(中文) |
| 18 | TSL_YP_MIN | NUMBER | Y |  | 拉伸测试屈服强度下限值(YP) | DB注释(中文) |
| 19 | TSL_YP_MAX | NUMBER | Y |  | 拉伸测试屈服强度上限值(YP) | DB注释(中文) |
| 20 | TSL_YP_AIM | NUMBER | Y |  | 拉伸测试屈服强度目标值(YP) | DB注释(中文) |
| 21 | TSL_TS_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试抗拉强度保证代号(TS) | DB注释(中文) |
| 22 | TSL_TS_MIN | NUMBER | Y |  | 拉伸测试抗拉强度下限值(TS) | DB注释(中文) |
| 23 | TSL_TS_MAX | NUMBER | Y |  | 拉伸测试抗拉强度上限值(TS) | DB注释(中文) |
| 24 | TSL_TS_AIM | NUMBER | Y |  | 拉伸测试抗拉强度目标值(TS) | DB注释(中文) |
| 25 | TSL_EL_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试延伸率保证代号(EL) | DB注释(中文) |
| 26 | TSL_EL_CD | VARCHAR2(1) | Y |  | 拉抻测试延伸率类型(EL) | DB注释(中文) |
| 27 | TSL_EL_MIN | NUMBER | Y |  | 拉抻测试延伸率下限值(EL) | DB注释(中文) |
| 28 | TSL_EL_MAX | NUMBER | Y |  | 拉抻测试延伸率上限值(EL) | DB注释(中文) |
| 29 | TSL_EL_AIM | NUMBER | Y |  | 拉抻测试延伸率目标值(EL) | DB注释(中文) |
| 30 | TSL_EL_UNF_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试均匀延伸率保证代号(uEL) | DB注释(中文) |
| 31 | TSL_EL_UNF_MIN | NUMBER | Y |  | 拉抻测试均匀延伸率下限值(uEL) | DB注释(中文) |
| 32 | TSL_EL_UNF_MAX | NUMBER | Y |  | 拉抻测试均匀延伸率目标值(uEL) | DB注释(中文) |
| 33 | TSL_EL_UNF_AIM | NUMBER | Y |  | 拉抻测试均匀延伸率上限值(uEL) | DB注释(中文) |
| 34 | TSL_YR_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试屈强比保证代号(YR) | DB注释(中文) |
| 35 | TSL_YR_MIN | NUMBER | Y |  | 拉伸测试屈强比下限值(YR) | DB注释(中文) |
| 36 | TSL_YR_MAX | NUMBER | Y |  | 拉伸测试屈强比上限值(YR) | DB注释(中文) |
| 37 | TSL_YR_AIM | NUMBER | Y |  | 拉伸测试屈强比目标值(YR) | DB注释(中文) |
| 38 | TSL_RA_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试断面收缩率保证代号(RA) | DB注释(中文) |
| 39 | TSL_RA_MIN | NUMBER | Y |  | 拉伸测试断面收缩率下限值(RA) | DB注释(中文) |
| 40 | TSL_RA_MAX | NUMBER | Y |  | 拉伸测试断面收缩率上限值(RA) | DB注释(中文) |
| 41 | TSL_RA_AIM | NUMBER | Y |  | 拉伸测试断面收缩率目标值(RA) | DB注释(中文) |
| 42 | TSL_R_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试塑性应变比r保证代号 | DB注释(中文) |
| 43 | TSL_R_MIN | NUMBER | Y |  | 拉抻测试塑性应变比r平均下限值 | DB注释(中文) |
| 44 | TSL_R0_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试r0保证代号 | DB注释(中文) |
| 45 | TSL_R0_MIN | NUMBER | Y |  | 拉抻测试r0下限值 | DB注释(中文) |
| 46 | TSL_R45_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试r45保证代号 | DB注释(中文) |
| 47 | TSL_R45_MIN | NUMBER | Y |  | 拉抻测试r45下限值 | DB注释(中文) |
| 48 | TSL_R90_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试r90保证代号 | DB注释(中文) |
| 49 | TSL_R90_MIN | NUMBER | Y |  | 拉抻测试r90下限值 | DB注释(中文) |
| 50 | TSL_RDELTA_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试\|Δr\|保证代号 | DB注释(中文) |
| 51 | TSL_RDELTA_MAX | NUMBER | Y |  | 拉伸测试\|Δr\|上限值 | DB注释(中文) |
| 52 | TSL_N_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试加工硬化指数n保证代号 | DB注释(中文) |
| 53 | TSL_N_MIN | NUMBER | Y |  | 拉伸测试加工硬化指数n平均下限值 | DB注释(中文) |
| 54 | TSL_N0_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试n0保证代号 | DB注释(中文) |
| 55 | TSL_N0_MIN | NUMBER | Y |  | 拉抻测试n0下限值 | DB注释(中文) |
| 56 | TSL_N45_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试n45保证代号 | DB注释(中文) |
| 57 | TSL_N45_MIN | NUMBER | Y |  | 拉抻测试n45下限值 | DB注释(中文) |
| 58 | TSL_N90_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试n90保证代号 | DB注释(中文) |
| 59 | TSL_N90_MIN | NUMBER | Y |  | 拉抻测试n90下限值 | DB注释(中文) |
| 60 | BEND_SMP_CND | VARCHAR2(2) | Y |  | 弯曲测试取样条件 | DB注释(中文) |
| 61 | BEND_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 弯曲测试长度方向取样位置 | DB注释(中文) |
| 62 | BEND_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 弯曲测试宽度方向取样位置 | DB注释(中文) |
| 63 | BEND_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 弯曲测试取样试样方向 | DB注释(中文) |
| 64 | BEND_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 弯曲测试取样试样号数 | DB注释(中文) |
| 65 | BEND_GRT_CD | VARCHAR2(1) | Y |  | 弯曲测试保证代号 | DB注释(中文) |
| 66 | BEND_CD | VARCHAR2(1) | Y |  | 弯曲测试类型 | DB注释(中文) |
| 67 | BEND_UNIT | VARCHAR2(1) | Y |  | 弯曲测试单位 | DB注释(中文) |
| 68 | BEND_ANGLE | NUMBER | Y |  | 弯曲测试弯曲角度 | DB注释(中文) |
| 69 | BEND_DIA | NUMBER | Y |  | 弯曲测试弯心直径 | DB注释(中文) |
| 70 | HARD_SMP_CND | VARCHAR2(2) | Y |  | 硬度测试取样条件 | DB注释(中文) |
| 71 | HARD_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 硬度测试长度方向取样位置 | DB注释(中文) |
| 72 | HARD_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 硬度测试宽度方向取样位置 | DB注释(中文) |
| 73 | HARD_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 硬度测试取样试样方向 | DB注释(中文) |
| 74 | HARD_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 硬度测试取样试样号数 | DB注释(中文) |
| 75 | HARD_GRT_CD | VARCHAR2(1) | Y |  | 硬度测试保证代号 | DB注释(中文) |
| 76 | HARD_KIND | VARCHAR2(1) | Y |  | 硬度测试种类 | DB注释(中文) |
| 77 | HARD_MIN | NUMBER | Y |  | 硬度测试下限值 | DB注释(中文) |
| 78 | HARD_MAX | NUMBER | Y |  | 硬度测试上限值 | DB注释(中文) |
| 79 | HARD_AIM | NUMBER | Y |  | 硬度测试目标值 | DB注释(中文) |
| 80 | IMPACT_SMP_CND | VARCHAR2(2) | Y |  | 冲击测试取样条件 | DB注释(中文) |
| 81 | IMPACT_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 冲击测试长度方向取样位置 | DB注释(中文) |
| 82 | IMPACT_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 冲击测试宽度方向取样位置 | DB注释(中文) |
| 83 | IMPACT_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 冲击测试取样试样方向 | DB注释(中文) |
| 84 | IMPACT_SMP_SPCMN_NON_SZ | VARCHAR2(2) | Y |  | 冲击测试非标准取样试样号数 | DB注释(中文) |
| 85 | IMPACT_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 冲击测试标准取样试样号数 | DB注释(中文) |
| 86 | IMPACT_SMP_SPCMN_CNT | NUMBER | Y |  | 冲击测试试样数量 | DB注释(中文) |
| 87 | IMPACT_TEMP | NUMBER | Y |  | 冲击测试温度 | DB注释(中文) |
| 88 | IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 冲击测试缺口类型 | DB注释(中文) |
| 89 | IMPACT_AVG_GRT_CD | VARCHAR2(1) | Y |  | 冲击测试吸收能量保证代号 | DB注释(中文) |
| 90 | IMPACT_AVG_MIN | NUMBER | Y |  | 冲击测试吸收能量平均下限值 | DB注释(中文) |
| 91 | IMPACT_AVG_AIM | NUMBER | Y |  | 冲击测试吸收能量平均目标值 | DB注释(中文) |
| 92 | IMPACT_IND_MIN | NUMBER | Y |  | 冲击测试吸收能量单个下限值 | DB注释(中文) |
| 93 | IMPACT_SF_RATIO_GRT_CD | VARCHAR2(1) | Y |  | 冲击测试纤维断面率保证代号 | DB注释(中文) |
| 94 | IMPACT_SF_RATIO_IND_AVG_MIN | NUMBER | Y |  | 冲击测试纤维断面率单个平均下限值 | DB注释(中文) |
| 95 | IMPACT_SF_RATIO_IND_MIN | NUMBER | Y |  | 冲击测试纤维断面率单个下限值 | DB注释(中文) |
| 96 | DWTT_SMP_CND | VARCHAR2(2) | Y |  | DWTT测试取样条件 | DB注释(中文) |
| 97 | DWTT_SMP_LTH_LOC | VARCHAR2(1) | Y |  | DWTT测试长度方向取样位置 | DB注释(中文) |
| 98 | DWTT_SMP_WTH_LOC | VARCHAR2(1) | Y |  | DWTT测试宽度方向取样位置 | DB注释(中文) |
| 99 | DWTT_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | DWTT测试取样试样方向 | DB注释(中文) |
| 100 | DWTT_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | DWTT测试取样试样号数 | DB注释(中文) |
| 101 | DWTT_SPCMN_CNT | NUMBER | Y |  | DWTT测试试样数量 | DB注释(中文) |
| 102 | DWTT_TEMP | NUMBER | Y |  | DWTT测试温度 | DB注释(中文) |
| 103 | DWTT_CREAK_CD | VARCHAR2(1) | Y |  | DWTT测试缺口类型 | DB注释(中文) |
| 104 | DWTT_GRT_CD | VARCHAR2(1) | Y |  | DWTT测试保证代号 | DB注释(中文) |
| 105 | DWTT_ABSP_AVG | NUMBER | Y |  | DWTT测试吸收能量平均值 | DB注释(中文) |
| 106 | DWTT_SF_RATIO_GRT_CD | VARCHAR2(1) | Y |  | DWTT测试最小剪切面保证代号 | DB注释(中文) |
| 107 | DWTT_SF_RATIO_AVG_MIN | NUMBER | Y |  | DWTT测试最小剪切面积平均下限值 | DB注释(中文) |
| 108 | DWTT_SF_RATIO_IND_MIN | NUMBER | Y |  | DWTT测试最小剪切面积单个下限值 | DB注释(中文) |
| 109 | MGRPHY_SMP_CND | VARCHAR2(2) | Y |  | 金相测试取样条件 | DB注释(中文) |
| 110 | MGRPHY_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 金相测试长度方向取样位置 | DB注释(中文) |
| 111 | MGRPHY_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 金相测试宽度方向取样位置 | DB注释(中文) |
| 112 | MGRPHY_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 金相测试取样试样方向 | DB注释(中文) |
| 113 | MGRPHY_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 金相测试取样试样号数 | DB注释(中文) |
| 114 | MGRPHY_GRNSZ_LEVEL | NUMBER | Y |  | 金相测试晶粒度级别 | DB注释(中文) |
| 115 | MGRPHY_GRNSZ_OCCP | NUMBER | Y |  | 金相测试基相晶粒的体积分数 | DB注释(中文) |
| 116 | MGRPHY_FGS_MIXED_GRT_CD | VARCHAR2(1) | Y |  | 铁素体晶粒混晶保证代号 | DB注释(中文) |
| 117 | MGRPHY_FGS_MIXED_RATIO | NUMBER | Y |  | 铁素体晶粒混晶占有率 | DB注释(中文) |
| 118 | MGRPHY_FGS_DEVT_GRT_CD | VARCHAR2(1) | Y |  | 铁素体混晶晶粒度差保证代号 | DB注释(中文) |
| 119 | MGRPHY_FGS_DEVT_MAX | NUMBER | Y |  | 铁素体混晶晶粒度差上限值 | DB注释(中文) |
| 120 | MGRPHY_FGS_GRT_CD | VARCHAR2(1) | Y |  | 铁素体晶粒尺寸保证代号 | DB注释(中文) |
| 121 | MGRPHY_FGS_MIN | NUMBER | Y |  | 铁素体晶粒尺寸下限值 | DB注释(中文) |
| 122 | MGRPHY_FGS_MAX | NUMBER | Y |  | 铁素体晶粒尺寸上限值 | DB注释(中文) |
| 123 | MGRPHY_AGS_GRT_CD | VARCHAR2(1) | Y |  | 奥氏体晶粒尺寸保证代号 | DB注释(中文) |
| 124 | MGRPHY_AGS_MIN | NUMBER | Y |  | 奥氏体晶粒尺寸下限值 | DB注释(中文) |
| 125 | MGRPHY_AGS_MAX | NUMBER | Y |  | 奥氏体晶粒尺寸上限值 | DB注释(中文) |
| 126 | MGRPHY_INCLD_GRT_CD | VARCHAR2(1) | Y |  | 夹杂物保证代号 | DB注释(中文) |
| 127 | MGRPHY_INCLD_TY | VARCHAR2(1) | Y |  | 夹杂物类别 | DB注释(中文) |
| 128 | MGRPHY_INCLD_GRD_MAX | NUMBER | Y |  | 夹杂物等级上限值 | DB注释(中文) |
| 129 | MGRPHY_DECARBON_GRT_CD | VARCHAR2(1) | Y |  | 脱碳层保证代号 | DB注释(中文) |
| 130 | MGRPHY_DECARBON_MAX | NUMBER | Y |  | 脱碳层上限值 | DB注释(中文) |
| 131 | MGRPHY_WILD_STRC_GRT_CD | VARCHAR2(1) | Y |  | 魏氏组织保证代号 | DB注释(中文) |
| 132 | MGRPHY_WILD_STRC_GRD | NUMBER | Y |  | 魏氏组织等级 | DB注释(中文) |
| 133 | MGRPHY_MTLGRP_GRT_CD | VARCHAR2(1) | Y |  | 组织类型保证代号 | DB注释(中文) |
| 134 | MGRPHY_MTLGRP_TY | VARCHAR2(2) | Y |  | 组织类型 | DB注释(中文) |
| 135 | MGRPHY_BAND_STRC_GRT_CD | VARCHAR2(1) | Y |  | 带状组织保证代号 | DB注释(中文) |
| 136 | MGRPHY_BAND_STRC_GRD_MAX | NUMBER | Y |  | 带状组织等级上限值 | DB注释(中文) |
| 137 | NON_METAL_SMP_CND | VARCHAR2(2) | Y |  | 非金属夹杂物测试取样条件 | DB注释(中文) |
| 138 | NON_METAL_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 非金属夹杂物测试长度方向取样位置 | DB注释(中文) |
| 139 | NON_METAL_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 非金属夹杂物测试宽度方向取样位置 | DB注释(中文) |
| 140 | NON_METAL_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 非金属夹杂物测试取样试样方向 | DB注释(中文) |
| 141 | NON_METAL_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 非金属夹杂物测试取样试样号数 | DB注释(中文) |
| 142 | NON_METAL_GRD_KIND_CD | VARCHAR2(2) | Y |  | 非金属夹杂评级图种类代码 | DB注释(中文) |
| 143 | NON_METAL_A_GRT_CD | VARCHAR2(1) | Y |  | 非金属夹杂物A保证代号 | DB注释(中文) |
| 144 | NON_METAL_A_MAX | NUMBER | Y |  | 非金属夹杂物A类上限 | DB注释(中文) |
| 145 | NON_METAL_B_GRT_CD | VARCHAR2(1) | Y |  | 非金属夹杂物B类保证代号 | DB注释(中文) |
| 146 | NON_METAL_B_MAX | NUMBER | Y |  | 非金属夹杂物B类上限 | DB注释(中文) |
| 147 | NON_METAL_C_GRT_CD | VARCHAR2(1) | Y |  | 非金属夹杂物C类保证代号 | DB注释(中文) |
| 148 | NON_METAL_C_MAX | NUMBER | Y |  | 非金属夹杂物C类上限 | DB注释(中文) |
| 149 | NON_METAL_D_GRT_CD | VARCHAR2(1) | Y |  | 非金属夹杂物D类保证代号 | DB注释(中文) |
| 150 | NON_METAL_D_MAX | NUMBER | Y |  | 非金属夹杂物D类上限 | DB注释(中文) |
| 151 | NON_METAL_DS_GRT_CD | VARCHAR2(1) | Y |  | 非金属夹杂物Ds保证代号 | DB注释(中文) |
| 152 | NON_METAL_DS_MAX | NUMBER | Y |  | 非金属夹杂物Ds上限 | DB注释(中文) |
| 153 | NON_METAL_ABCD_GRT_CD | VARCHAR2(1) | Y |  | 非金属夹杂物A+B+C+D保证代号 | DB注释(中文) |
| 154 | NON_METAL_ABCD_MAX | NUMBER | Y |  | 非金属夹杂物A+B+C+D上限 | DB注释(中文) |
| 155 | S_PRINT_SMP_CND | VARCHAR2(2) | Y |  | 硫印测试取样条件 | DB注释(中文) |
| 156 | S_PRINT_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 硫印测试长度方向取样位置 | DB注释(中文) |
| 157 | S_PRINT_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 硫印测试宽度方向取样位置 | DB注释(中文) |
| 158 | S_PRINT_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 硫印测试取样试样方向 | DB注释(中文) |
| 159 | S_PRINT_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 硫印测试取样试样号数 | DB注释(中文) |
| 160 | S_PRINT_GRT_CD | VARCHAR2(1) | Y |  | 硫印测试保证代号 | DB注释(中文) |
| 161 | S_PRINT_KIND | VARCHAR2(1) | Y |  | 硫印测试种类 | DB注释(中文) |
| 162 | S_PRINT_GRD_MAX | VARCHAR2(1) | Y |  | 硫印测试上限等级 | DB注释(中文) |
| 163 | P_PRINT_SMP_CND | VARCHAR2(2) | Y |  | 磷印测试取样条件 | DB注释(中文) |
| 164 | P_PRINT_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 磷印测试长度方向取样位置 | DB注释(中文) |
| 165 | P_PRINT_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 磷印测试宽度方向取样位置 | DB注释(中文) |
| 166 | P_PRINT_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 磷印测试取样试样方向 | DB注释(中文) |
| 167 | P_PRINT_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 磷印测试取样试样号数 | DB注释(中文) |
| 168 | P_PRINT_GRT_CD | VARCHAR2(1) | Y |  | 磷印测试保证代号 | DB注释(中文) |
| 169 | P_PRINT_GRD_MAX | VARCHAR2(1) | Y |  | 磷印测试上限等级 | DB注释(中文) |
| 170 | P_SGRG_SMP_CND | VARCHAR2(2) | Y |  | 磷偏析测试取样条件 | DB注释(中文) |
| 171 | P_SGRG_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 磷偏析测试长度方向取样位置 | DB注释(中文) |
| 172 | P_SGRG_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 磷偏析测试宽度方向取样位置 | DB注释(中文) |
| 173 | P_SGRG_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 磷偏析测试取样试样方向 | DB注释(中文) |
| 174 | P_SGRG_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 磷偏析测试取样试样号数 | DB注释(中文) |
| 175 | P_SGRG_GRT_CD | VARCHAR2(1) | Y |  | 磷偏析测试保证代号 | DB注释(中文) |
| 176 | P_SGRG_GRD_MAX | VARCHAR2(1) | Y |  | 磷偏析测试上限等级 | DB注释(中文) |
| 177 | C_SGRG_SMP_CND | VARCHAR2(2) | Y |  | 碳偏析测试取样条件 | DB注释(中文) |
| 178 | C_SGRG_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 碳偏析测试长度方向取样位置 | DB注释(中文) |
| 179 | C_SGRG_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 碳偏析测试宽度方向取样位置 | DB注释(中文) |
| 180 | C_SGRG_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 碳偏析测试取样试样方向 | DB注释(中文) |
| 181 | C_SGRG_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 碳偏析测试取样试样号数 | DB注释(中文) |
| 182 | C_SGRG_GRT_CD | VARCHAR2(1) | Y |  | 碳偏析测试保证代号 | DB注释(中文) |
| 183 | C_SGRG_KIND | VARCHAR2(1) | Y |  | 碳偏析测试种类 | DB注释(中文) |
| 184 | C_SGRG_SMP_GRD_MAX | VARCHAR2(1) | Y |  | 碳偏析测试上限等级 | DB注释(中文) |
| 185 | HIC_SMP_CND | VARCHAR2(2) | Y |  | HIC测试取样条件 | DB注释(中文) |
| 186 | HIC_SMP_LTH_LOC | VARCHAR2(1) | Y |  | HIC测试长度方向取样位置 | DB注释(中文) |
| 187 | HIC_SMP_WTH_LOC | VARCHAR2(1) | Y |  | HIC测试宽度方向取样位置 | DB注释(中文) |
| 188 | HIC_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | HIC测试取样测试方向 | DB注释(中文) |
| 189 | HIC_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | HIC测试取样试样号数 | DB注释(中文) |
| 190 | HIC_SOLUTION_KIND | VARCHAR2(1) | Y |  | HIC测试溶液种类 | DB注释(中文) |
| 191 | HIC_CLR_GRT_CD | VARCHAR2(1) | Y |  | HIC测试CLR保证代号 | DB注释(中文) |
| 192 | HIC_CLR_EACH_MAX | NUMBER | Y |  | HIC测试CLR单个上限值 | DB注释(中文) |
| 193 | HIC_CLR_SPCMN_AVG_MAX | NUMBER | Y |  | HIC测试CLR试样平均上限值 | DB注释(中文) |
| 194 | HIC_CLR_TOT_AVG_MAX | NUMBER | Y |  | HIC测试CLR全体平均上限值 | DB注释(中文) |
| 195 | HIC_CSR_GRT_CD | VARCHAR2(1) | Y |  | HIC测试CSR保证代号 | DB注释(中文) |
| 196 | HIC_CSR_EACH_MAX | NUMBER | Y |  | HIC测试CSR单个上限值 | DB注释(中文) |
| 197 | HIC_CSR_SPCMN_AVG_MAX | NUMBER | Y |  | HIC测试CSR试样平均上限值 | DB注释(中文) |
| 198 | HIC_CSR_TOT_AVG_MAX | NUMBER | Y |  | HIC测试CSR全体平均上限值 | DB注释(中文) |
| 199 | HIC_CTR_GRT_CD | VARCHAR2(1) | Y |  | HIC测试CTR保证代号 | DB注释(中文) |
| 200 | HIC_CTR_EACH_MAX | NUMBER | Y |  | HIC测试CTR单个上限值 | DB注释(中文) |
| 201 | HIC_CTR_SPCMN_AVG_MAX | NUMBER | Y |  | HIC测试CTR试样平均上限值 | DB注释(中文) |
| 202 | HIC_CTR_TOT_AVG_MAX | NUMBER | Y |  | HIC测试CTR全体平均上限值 | DB注释(中文) |
| 203 | SSCC_SMP_CND | VARCHAR2(2) | Y |  | SSCC测试取样条件 | DB注释(中文) |
| 204 | SSCC_SMP_LTH_LOC | VARCHAR2(1) | Y |  | SSCC测试长度方向取样位置 | DB注释(中文) |
| 205 | SSCC_SMP_WTH_LOC | VARCHAR2(1) | Y |  | SSCC测试宽度方向取样位置 | DB注释(中文) |
| 206 | SSCC_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | SSCC测试取样试样方向 | DB注释(中文) |
| 207 | SSCC_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | SSCC测试取样试样号数 | DB注释(中文) |
| 208 | SSCC_GRT_CD | VARCHAR2(1) | Y |  | SSCC测试保证代号 | DB注释(中文) |
| 209 | SSCC_SOLUTION_KIND | VARCHAR2(1) | Y |  | SSCC测试溶液种类 | DB注释(中文) |
| 210 | SSCC_KIND | VARCHAR2(1) | Y |  | SSCC测试种类 | DB注释(中文) |
| 211 | SSCC_STRESS_TY | VARCHAR2(1) | Y |  | SSCC测试应力区分 | DB注释(中文) |
| 212 | SSCC_STRESS_RATIO | NUMBER | Y |  | SSCC测试应力比率 | DB注释(中文) |
| 213 | SSCC_TIME | NUMBER | Y |  | SSCC测试时间 | DB注释(中文) |
| 214 | HIGH_TEMP_TSL_SMP_CND | VARCHAR2(2) | Y |  | 高温拉伸测试取样条件 | DB注释(中文) |
| 215 | HIGH_TEMP_TSL_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 高温拉伸测试长度方向取样位置 | DB注释(中文) |
| 216 | HIGH_TEMP_TSL_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 高温拉伸测试宽度方向取样位置 | DB注释(中文) |
| 217 | HIGH_TEMP_TSL_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 高温拉伸测试取样试样方向 | DB注释(中文) |
| 218 | HIGH_TEMP_TSL_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 高温拉伸测试取样试样号数 | DB注释(中文) |
| 219 | HIGH_TEMP_TSL_TEMP | NUMBER | Y |  | 高温拉伸测试温度 | DB注释(中文) |
| 220 | HIGH_TEMP_TSL_YP_GRT_CD | VARCHAR2(1) | Y |  | 高温拉伸测试屈服强度保证代号 | DB注释(中文) |
| 221 | HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  | 高温拉伸测试屈服强度类型 | DB注释(中文) |
| 222 | HIGH_TEMP_TSL_YP_MIN | NUMBER | Y |  | 高温拉伸测试屈服强度下限值 | DB注释(中文) |
| 223 | HIGH_TEMP_TSL_YP_MAX | NUMBER | Y |  | 高温拉伸测试屈服强度上限值 | DB注释(中文) |
| 224 | HIGH_TEMP_TSL_YP_AIM | NUMBER | Y |  | 高温拉伸测试屈服强度目标值 | DB注释(中文) |
| 225 | HIGH_TEMP_TSL_TS_GRT_CD | VARCHAR2(1) | Y |  | 高温拉伸测试抗拉强度保证代号 | DB注释(中文) |
| 226 | HIGH_TEMP_TSL_TS_MIN | NUMBER | Y |  | 高温拉伸测试抗拉强度下限值 | DB注释(中文) |
| 227 | HIGH_TEMP_TSL_TS_MAX | NUMBER | Y |  | 高温拉伸测试抗拉强度上限值 | DB注释(中文) |
| 228 | HIGH_TEMP_TSL_TS_AIM | NUMBER | Y |  | 高温拉伸测试抗拉强度目标值 | DB注释(中文) |
| 229 | HIGH_TEMP_TSL_EL_GRT_CD | VARCHAR2(1) | Y |  | 高温拉伸测试伸长率保证代号 | DB注释(中文) |
| 230 | HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  | 高温拉伸测试伸长率类型 | DB注释(中文) |
| 231 | HIGH_TEMP_TSL_EL_MIN | NUMBER | Y |  | 高温拉伸测试伸长率下限值 | DB注释(中文) |
| 232 | HIGH_TEMP_TSL_EL_MAX | NUMBER | Y |  | 高温拉伸测试伸长率上限值 | DB注释(中文) |
| 233 | HIGH_TEMP_TSL_EL_AIM | NUMBER | Y |  | 高温拉伸测试伸长率目标值 | DB注释(中文) |
| 234 | HIGH_TEMP_TSL_RA_GRT_CD | VARCHAR2(1) | Y |  | 高温拉伸测试断面收缩率保证代号 | DB注释(中文) |
| 235 | HIGH_TEMP_TSL_RA_MIN | NUMBER | Y |  | 高温拉伸测试断面收缩率下限值 | DB注释(中文) |
| 236 | HIGH_TEMP_TSL_RA_MAX | NUMBER | Y |  | 高温拉伸测试断面收缩率上限值 | DB注释(中文) |
| 237 | HIGH_TEMP_TSL_RA_AIM | NUMBER | Y |  | 高温拉伸测试断面收缩率目标值 | DB注释(中文) |
| 238 | CLEAN_SMP_CND | VARCHAR2(2) | Y |  | 洁净度测试取样条件 | DB注释(中文) |
| 239 | CLEAN_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 洁净度测试长度方向取样位置 | DB注释(中文) |
| 240 | CLEAN_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 洁净度测试宽度方向取样位置 | DB注释(中文) |
| 241 | CLEAN_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 洁净度测试取样试样方向 | DB注释(中文) |
| 242 | CLEAN_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 洁净度测试取样试样号数 | DB注释(中文) |
| 243 | CLEAN1_GRT_CD | VARCHAR2(1) | Y |  | 洁净度测试1保证代号 | DB注释(中文) |
| 244 | CLEAN1_KIND | VARCHAR2(1) | Y |  | 洁净度测试1种类 | DB注释(中文) |
| 245 | CLEAN1_MAX | NUMBER | Y |  | 洁净度测试1上限值 | DB注释(中文) |
| 246 | CLEAN2_GRT_CD | VARCHAR2(1) | Y |  | 洁净度测试2保证代号 | DB注释(中文) |
| 247 | CLEAN2_KIND | VARCHAR2(1) | Y |  | 洁净度测试2种类 | DB注释(中文) |
| 248 | CLEAN2_MAX | NUMBER | Y |  | 洁净度测试2上限值 | DB注释(中文) |
| 249 | CLEAN3_GRT_CD | VARCHAR2(1) | Y |  | 洁净度测试3保证代号 | DB注释(中文) |
| 250 | CLEAN3_KIND | VARCHAR2(1) | Y |  | 洁净度测试3种类 | DB注释(中文) |
| 251 | CLEAN3_MAX | NUMBER | Y |  | 洁净度测试3上限值 | DB注释(中文) |
| 252 | ROUGH_SMP_CND | VARCHAR2(2) | Y |  | 粗糙度测试取样条件 | DB注释(中文) |
| 253 | ROUGH_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 粗糙度测试长度方向取样位置 | DB注释(中文) |
| 254 | ROUGH_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 粗糙度测试宽度方向取样位置 | DB注释(中文) |
| 255 | ROUGH_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 粗糙度测试取样试样方向 | DB注释(中文) |
| 256 | ROUGH_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 粗糙度测试取样试样号数 | DB注释(中文) |
| 257 | ROUGH_KIND | VARCHAR2(1) | Y |  | 粗糙度测试种类 | DB注释(中文) |
| 258 | ROUGH_DIR | VARCHAR2(1) | Y |  | 粗度测试方向 | DB注释(中文) |
| 259 | ROUGH_RA_GRT_CD | VARCHAR2(1) | Y |  | 表面平均粗糙度保证代号(Ra) | DB注释(中文) |
| 260 | ROUGH_RA_MIN | NUMBER | Y |  | 表面平均粗糙度下限值(Ra) | DB注释(中文) |
| 261 | ROUGH_RA_MAX | NUMBER | Y |  | 表面平均粗糙度上限值(Ra) | DB注释(中文) |
| 262 | ROUGH_RA_AIM | NUMBER | Y |  | 表面平均粗糙度目标值(Ra) | DB注释(中文) |
| 263 | ROUGH_RPC_GRT_CD | VARCHAR2(1) | Y |  | 单位长度内峰值保证代号(Rpc) | DB注释(中文) |
| 264 | ROUGH_RPC_MIN | NUMBER | Y |  | 单位长度内峰值个数下限值(Rpc) | DB注释(中文) |
| 265 | ROUGH_RPC_MAX | NUMBER | Y |  | 单位长度内峰值个数上限值(Rpc) | DB注释(中文) |
| 266 | ROUGH_RMAX_GRT_CD | VARCHAR2(1) | Y |  | 表面粗糙度最大值保证代号(Rmax) | DB注释(中文) |
| 267 | ROUGH_RMAX_MIN | NUMBER | Y |  | 表面粗糙度最大值下限值(Rmax) | DB注释(中文) |
| 268 | ROUGH_RMAX_MAX | NUMBER | Y |  | 表面粗糙度最大值上限值(Rmax) | DB注释(中文) |
| 269 | EXT_HOLE_SMP_CND | VARCHAR2(2) | Y |  | 扩孔测试取样条件 | DB注释(中文) |
| 270 | EXT_HOLE_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 扩孔测试长度方向取样位置 | DB注释(中文) |
| 271 | EXT_HOLE_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 扩孔测试宽度方向取样位置 | DB注释(中文) |
| 272 | EXT_HOLE_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 扩孔测试取样试样方向 | DB注释(中文) |
| 273 | EXT_HOLE_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 扩孔测试取样试样号数 | DB注释(中文) |
| 274 | EXT_HOLE_SPCMN_CNT | NUMBER | Y |  | 扩孔测试试样数量 | DB注释(中文) |
| 275 | EXT_HOLE_RATIO_GRT_CD | VARCHAR2(1) | Y |  | 扩孔测试极限扩孔率保证代号 | DB注释(中文) |
| 276 | EXT_HOLE_RATIO_AVG_MIN | NUMBER | Y |  | 扩孔测试极限扩孔率平均下限值 | DB注释(中文) |
| 277 | EXT_HOLE_RATIO_EACH_MIN | NUMBER | Y |  | 扩孔测试极限扩孔率单个下限值 | DB注释(中文) |
| 278 | EXT_HOLE_RATIO_AVG_AIM | NUMBER | Y |  | 扩孔测试极限扩孔率平均目标值 | DB注释(中文) |
| 279 | FATIG_SMP_CND | VARCHAR2(2) | Y |  | 疲劳测试取样条件 | DB注释(中文) |
| 280 | FATIG_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 疲劳测试长度方向取样位置 | DB注释(中文) |
| 281 | FATIG_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 疲劳测试宽度方向取样位置 | DB注释(中文) |
| 282 | FATIG_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 疲劳测试取样试样方向 | DB注释(中文) |
| 283 | FATIG_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 疲劳测试取样试样号数 | DB注释(中文) |
| 284 | FATIG_SPCMN_CNT | NUMBER | Y |  | 疲劳测试试样数量 | DB注释(中文) |
| 285 | FATIG_GRT_CD | VARCHAR2(1) | Y |  | 疲劳测试保证代号 | DB注释(中文) |
| 286 | FATIG_TEMP | NUMBER | Y |  | 疲劳测试温度 | DB注释(中文) |
| 287 | FATIG_FREQ | NUMBER | Y |  | 疲劳测试频率 | DB注释(中文) |
| 288 | FATIG_SERV_LIFE | NUMBER | Y |  | 疲劳寿命 | DB注释(中文) |
| 289 | FATIG_CND_STRTH | NUMBER | Y |  | 条件疲劳强度 | DB注释(中文) |
| 290 | OIL_SMP_CND | VARCHAR2(2) | Y |  | 涂油测试取样条件 | DB注释(中文) |
| 291 | OIL_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 涂油测试长度方向取样位置 | DB注释(中文) |
| 292 | OIL_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 涂油测试宽度方向取样位置 | DB注释(中文) |
| 293 | OIL_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 涂油测试取样试样方向 | DB注释(中文) |
| 294 | OIL_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 涂油测试取样试样号数 | DB注释(中文) |
| 295 | OIL_WGT_GRT_CD | VARCHAR2(1) | Y |  | 涂油量保证代号 | DB注释(中文) |
| 296 | OIL_MTH_CD | VARCHAR2(2) | Y |  | 涂油方法代码 | DB注释(中文) |
| 297 | OIL_WGT_MIN | NUMBER | Y |  | 涂油量测试双面涂油量下限值 | DB注释(中文) |
| 298 | OIL_WGT_MAX | NUMBER | Y |  | 涂油量测试双面涂油量上限值 | DB注释(中文) |
| 299 | OIL_WGT_UPPER_MIN | NUMBER | Y |  | 涂油量测试上表面涂油量下限值 | DB注释(中文) |
| 300 | OIL_WGT_UPPER_MAX | NUMBER | Y |  | 涂油量测试上表面涂油量上限值 | DB注释(中文) |
| 301 | OIL_WGT_LOWER_MIN | NUMBER | Y |  | 涂油量测试下表面涂油量下限值 | DB注释(中文) |
| 302 | OIL_WGT_LOWER_MAX | NUMBER | Y |  | 涂油量测试下表面涂油量上限值 | DB注释(中文) |
| 303 | ERICHSEN_SMP_CND | VARCHAR2(2) | Y |  | 杯突测试取样条件 | DB注释(中文) |
| 304 | ERICHSEN_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 杯突测试长度方向取样位置 | DB注释(中文) |
| 305 | ERICHSEN_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 杯突测试宽度方向取样位置 | DB注释(中文) |
| 306 | ERICHSEN_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 杯突测试试样取样方向 | DB注释(中文) |
| 307 | ERICHSEN_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 杯突测试试样尺寸 | DB注释(中文) |
| 308 | ERICHSEN_GRT_CD | VARCHAR2(1) | Y |  | 杯突测试保证代号 | DB注释(中文) |
| 309 | ERICHSEN_MIN | NUMBER | Y |  | 杯突测试下限值 | DB注释(中文) |
| 310 | ERICHSEN_AIM | NUMBER | Y |  | 杯突测试目标值 | DB注释(中文) |
| 311 | WAVIN_SMP_CND | VARCHAR2(2) | Y |  | 波纹度测试取样条件 | DB注释(中文) |
| 312 | WAVIN_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 波纹度测试长度方向取样位置 | DB注释(中文) |
| 313 | WAVIN_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 波纹度测试宽度方向取样位置 | DB注释(中文) |
| 314 | WAVIN_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 波纹度测试取样试样方向 | DB注释(中文) |
| 315 | WAVIN_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 波纹度测试取样试样号数 | DB注释(中文) |
| 316 | WAVIN_WA_GRT_CD | VARCHAR2(1) | Y |  | 波纹度检测保证代号 | DB注释(中文) |
| 317 | WAVIN_TY | VARCHAR2(1) | Y |  | 波纹度测试种类 | DB注释(中文) |
| 318 | WAVIN_WA_MAX | NUMBER | Y |  | 波纹度检测上限值(Wa) | DB注释(中文) |
| 319 | WAVIN_WMAX_MAX | NUMBER | Y |  | 波纹度检测最大值上限值(Wmax) | DB注释(中文) |
| 320 | SPRBCK_SMP_CND | VARCHAR2(2) | Y |  | 回弹测试取样条件 | DB注释(中文) |
| 321 | SPRBCK_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 回弹测试长度方向取样位置 | DB注释(中文) |
| 322 | SPRBCK_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 回弹测试宽度方向取样位置 | DB注释(中文) |
| 323 | SPRBCK_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 回弹测试取样试样方向 | DB注释(中文) |
| 324 | SPRBCK_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 回弹测试取样试样号数 | DB注释(中文) |
| 325 | SPRBCK_CD | VARCHAR2(1) | Y |  | 回弹测试方法 | DB注释(中文) |
| 326 | SPRBCK_DEGR_GRT_CD | VARCHAR2(1) | Y |  | 回弹角保证代号 | DB注释(中文) |
| 327 | SPRBCK_DEGR_MIN | NUMBER | Y |  | 回弹角下限值 | DB注释(中文) |
| 328 | SPRBCK_DEGR_MAX | NUMBER | Y |  | 回弹角上限值 | DB注释(中文) |
| 329 | SPRBCK_GRT_CD | VARCHAR2(1) | Y |  | 回弹测试保证代号 | DB注释(中文) |
| 330 | SPRBCK_MIN | NUMBER | Y |  | 回弹测试下限值 | DB注释(中文) |
| 331 | SPRBCK_MAX | NUMBER | Y |  | 回弹测试上限值 | DB注释(中文) |
| 332 | BH_SMP_CND | VARCHAR2(2) | Y |  | 烘烤硬化值测试取样条件 | DB注释(中文) |
| 333 | BH_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 烘烤硬化值测试长度方向取样位置 | DB注释(中文) |
| 334 | BH_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 烘烤硬化值测试宽度方向取样位置 | DB注释(中文) |
| 335 | BH_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 烘烤硬化值测试试样取样方向 | DB注释(中文) |
| 336 | BH_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 烘烤硬化值测试试样尺寸 | DB注释(中文) |
| 337 | BH_GRT_CD | VARCHAR2(1) | Y |  | 烘烤硬化值测试保证代号 | DB注释(中文) |
| 338 | BH_MIN | NUMBER | Y |  | 烘烤硬化值测试下限值 | DB注释(中文) |
| 339 | BH_AIM | NUMBER | Y |  | 烘烤硬化值测试目标值 | DB注释(中文) |
| 340 | HPT_SMP_CND | VARCHAR2(2) | Y |  | 氢渗透性测试取样条件 | DB注释(中文) |
| 341 | HPT_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 氢渗透性测试长度方向取样位置 | DB注释(中文) |
| 342 | HPT_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 氢渗透性测试宽度方向取样位置 | DB注释(中文) |
| 343 | HPT_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 氢渗透性测试取样试样方向 | DB注释(中文) |
| 344 | HPT_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 氢渗透性测试取样试样号数 | DB注释(中文) |
| 345 | HPT_SMP_GRT_CD | VARCHAR2(1) | Y |  | 氢渗透性测试保证代号 | DB注释(中文) |
| 346 | HPT_ADMI_TIME_MIN | NUMBER | Y |  | 氢扩散达到稳定所需时间下限值 | DB注释(中文) |
| 347 | QLT_REMARKS | VARCHAR2(300) | Y |  | 质量备注 | DB注释(中文) |
| 348 | IMPACT_SMP_SZ | VARCHAR2(2) | Y |  | 冲击试样尺寸 | DB注释(中文) |
| 349 | IMPACT_SF_RATIO_IND_AVG | NUMBER | Y |  | 冲击测试纤维断面率单个平均值 | DB注释(中文) |
| 350 | DWTT_ABSP_SING | NUMBER | Y |  | DWTT测试吸收能量单个值 | DB注释(中文) |
| 351 | MGRPHY_GRNSZ_LEVEL_GRT_CD | VARCHAR2(1) | Y |  | 金相测试晶粒度级别代码 | DB注释(中文) |
| 352 | BEND_WTH_LOC_KIND | VARCHAR2(1) | Y |  | 弯曲试样宽度 | DB注释(中文) |
| 353 | SR_TSL_SMP_CND | VARCHAR2(2) | Y |  | 拉伸测试取样条件 | DB注释(中文) |
| 354 | SR_TSL_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 拉伸测试长度方向取样位置 | DB注释(中文) |
| 355 | SR_TSL_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 拉伸测试宽度方向取样位置 | DB注释(中文) |
| 356 | SR_TSL_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 拉伸测试取样试样方向 | DB注释(中文) |
| 357 | SR_TSL_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 拉伸测试取样试样号数 | DB注释(中文) |
| 358 | SR_TSL_YP_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度保证代号(YP) | DB注释(中文) |
| 359 | SR_TSL_YP_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度类型(YP) | DB注释(中文) |
| 360 | SR_TSL_YP_MIN | NUMBER | Y |  | 拉伸测试屈服强度下限值(YP) | DB注释(中文) |
| 361 | SR_TSL_YP_MAX | NUMBER | Y |  | 拉伸测试屈服强度上限值(YP) | DB注释(中文) |
| 362 | SR_TSL_YP_AIM | NUMBER | Y |  | 拉伸测试屈服强度目标值(YP) | DB注释(中文) |
| 363 | SR_TSL_TS_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试抗拉强度保证代号(TS) | DB注释(中文) |
| 364 | SR_TSL_TS_MIN | NUMBER | Y |  | 拉伸测试抗拉强度下限值(TS) | DB注释(中文) |
| 365 | SR_TSL_TS_MAX | NUMBER | Y |  | 拉伸测试抗拉强度上限值(TS) | DB注释(中文) |
| 366 | SR_TSL_TS_AIM | NUMBER | Y |  | 拉伸测试抗拉强度目标值(TS) | DB注释(中文) |
| 367 | SR_TSL_EL_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试延伸率保证代号(EL) | DB注释(中文) |
| 368 | SR_TSL_EL_CD | VARCHAR2(1) | Y |  | 拉抻测试延伸率类型(EL) | DB注释(中文) |
| 369 | SR_TSL_EL_MIN | NUMBER | Y |  | 拉抻测试延伸率下限值(EL) | DB注释(中文) |
| 370 | SR_TSL_EL_MAX | NUMBER | Y |  | 拉抻测试延伸率上限值(EL) | DB注释(中文) |
| 371 | SR_TSL_EL_AIM | NUMBER | Y |  | 拉抻测试延伸率目标值(EL) | DB注释(中文) |
| 372 | SR_TSL_EL_UNF_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试均匀延伸率保证代号(uEL) | DB注释(中文) |
| 373 | SR_TSL_EL_UNF_MIN | NUMBER | Y |  | 拉抻测试均匀延伸率下限值(uEL) | DB注释(中文) |
| 374 | SR_TSL_EL_UNF_MAX | NUMBER | Y |  | 拉抻测试均匀延伸率目标值(uEL) | DB注释(中文) |
| 375 | SR_TSL_EL_UNF_AIM | NUMBER | Y |  | 拉抻测试均匀延伸率上限值(uEL) | DB注释(中文) |
| 376 | SR_TSL_YR_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试屈强比保证代号(YR) | DB注释(中文) |
| 377 | SR_TSL_YR_MIN | NUMBER | Y |  | 拉伸测试屈强比下限值(YR) | DB注释(中文) |
| 378 | SR_TSL_YR_MAX | NUMBER | Y |  | 拉伸测试屈强比上限值(YR) | DB注释(中文) |
| 379 | SR_TSL_YR_AIM | NUMBER | Y |  | 拉伸测试屈强比目标值(YR) | DB注释(中文) |
| 380 | SR_TSL_RA_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试断面收缩率保证代号(RA) | DB注释(中文) |
| 381 | SR_TSL_RA_MIN | NUMBER | Y |  | 拉伸测试断面收缩率下限值(RA) | DB注释(中文) |
| 382 | SR_TSL_RA_MAX | NUMBER | Y |  | 拉伸测试断面收缩率上限值(RA) | DB注释(中文) |
| 383 | SR_TSL_RA_AIM | NUMBER | Y |  | 拉伸测试断面收缩率目标值(RA) | DB注释(中文) |
| 384 | SR_TSL_R_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试塑性应变比r保证代号 | DB注释(中文) |
| 385 | SR_TSL_R_MIN | NUMBER | Y |  | 拉抻测试塑性应变比r平均下限值 | DB注释(中文) |
| 386 | SR_TSL_R0_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试r0保证代号 | DB注释(中文) |
| 387 | SR_TSL_R0_MIN | NUMBER | Y |  | 拉抻测试r0下限值 | DB注释(中文) |
| 388 | SR_TSL_R45_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试r45保证代号 | DB注释(中文) |
| 389 | SR_TSL_R45_MIN | NUMBER | Y |  | 拉抻测试r45下限值 | DB注释(中文) |
| 390 | SR_TSL_R90_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试r90保证代号 | DB注释(中文) |
| 391 | SR_TSL_R90_MIN | NUMBER | Y |  | 拉抻测试r90下限值 | DB注释(中文) |
| 392 | SR_TSL_RDELTA_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试\|Δr\|保证代号 | DB注释(中文) |
| 393 | SR_TSL_RDELTA_MAX | NUMBER | Y |  | 拉伸测试\|Δr\|上限值 | DB注释(中文) |
| 394 | SR_TSL_N_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试加工硬化指数n保证代号 | DB注释(中文) |
| 395 | SR_TSL_N_MIN | NUMBER | Y |  | 拉伸测试加工硬化指数n平均下限值 | DB注释(中文) |
| 396 | SR_TSL_N0_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试n0保证代号 | DB注释(中文) |
| 397 | SR_TSL_N0_MIN | NUMBER | Y |  | 拉抻测试n0下限值 | DB注释(中文) |
| 398 | SR_TSL_N45_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试n45保证代号 | DB注释(中文) |
| 399 | SR_TSL_N45_MIN | NUMBER | Y |  | 拉抻测试n45下限值 | DB注释(中文) |
| 400 | SR_TSL_N90_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试n90保证代号 | DB注释(中文) |
| 401 | SR_TSL_N90_MIN | NUMBER | Y |  | 拉抻测试n90下限值 | DB注释(中文) |
| 402 | SR_BEND_SMP_CND | VARCHAR2(2) | Y |  | 弯曲测试取样条件 | DB注释(中文) |
| 403 | SR_BEND_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 弯曲测试长度方向取样位置 | DB注释(中文) |
| 404 | SR_BEND_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 弯曲测试宽度方向取样位置 | DB注释(中文) |
| 405 | SR_BEND_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 弯曲测试取样试样方向 | DB注释(中文) |
| 406 | SR_BEND_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 弯曲测试取样试样号数 | DB注释(中文) |
| 407 | SR_BEND_GRT_CD | VARCHAR2(1) | Y |  | 弯曲测试保证代号 | DB注释(中文) |
| 408 | SR_BEND_CD | VARCHAR2(1) | Y |  | 弯曲测试类型 | DB注释(中文) |
| 409 | SR_BEND_UNIT | VARCHAR2(1) | Y |  | 弯曲测试单位 | DB注释(中文) |
| 410 | SR_BEND_ANGLE | NUMBER | Y |  | 弯曲测试弯曲角度 | DB注释(中文) |
| 411 | SR_BEND_DIA | NUMBER | Y |  | 弯曲测试弯心直径 | DB注释(中文) |
| 412 | SR_BEND_WTH_LOC_KIND | VARCHAR2(1) | Y |  | 弯曲试样宽度 | DB注释(中文) |
| 413 | SR_IMPACT_SMP_CND | VARCHAR2(2) | Y |  | 冲击测试取样条件 | DB注释(中文) |
| 414 | SR_IMPACT_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 冲击测试长度方向取样位置 | DB注释(中文) |
| 415 | SR_IMPACT_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 冲击测试宽度方向取样位置 | DB注释(中文) |
| 416 | SR_IMPACT_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 冲击测试取样试样方向 | DB注释(中文) |
| 417 | SR_IMPACT_SMP_SPCMN_NON_SZ | VARCHAR2(2) | Y |  | 冲击测试非标准取样试样号数 | DB注释(中文) |
| 418 | SR_IMPACT_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 冲击测试标准取样试样号数 | DB注释(中文) |
| 419 | SR_IMPACT_SMP_SPCMN_CNT | NUMBER | Y |  | 冲击测试试样数量 | DB注释(中文) |
| 420 | SR_IMPACT_TEMP | NUMBER | Y |  | 冲击测试温度 | DB注释(中文) |
| 421 | SR_IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 冲击测试缺口类型 | DB注释(中文) |
| 422 | SR_IMPACT_AVG_GRT_CD | VARCHAR2(1) | Y |  | 冲击测试吸收能量保证代号 | DB注释(中文) |
| 423 | SR_IMPACT_AVG_MIN | NUMBER | Y |  | 冲击测试吸收能量平均下限值 | DB注释(中文) |
| 424 | SR_IMPACT_AVG_AIM | NUMBER | Y |  | 冲击测试吸收能量平均目标值 | DB注释(中文) |
| 425 | SR_IMPACT_IND_MIN | NUMBER | Y |  | 冲击测试吸收能量单个下限值 | DB注释(中文) |
| 426 | SR_IMPACT_SF_RATIO_GRT_CD | VARCHAR2(1) | Y |  | 冲击测试纤维断面率保证代号 | DB注释(中文) |
| 427 | SR_IMPACT_SF_RATIO_IND_AVG_MIN | NUMBER | Y |  | 冲击测试纤维断面率单个平均下限值 | DB注释(中文) |
| 428 | SR_IMPACT_SF_RATIO_IND_MIN | NUMBER | Y |  | 冲击测试纤维断面率单个下限值 | DB注释(中文) |
| 429 | SR_IMPACT_SMP_SZ | VARCHAR2(2) | Y |  | 冲击试样尺寸 | DB注释(中文) |
| 430 | SR_IMPACT_SF_RATIO_IND_AVG | NUMBER | Y |  | 冲击测试纤维断面率单个平均值 | DB注释(中文) |
| 431 | SR_MGRPHY_SMP_CND | VARCHAR2(2) | Y |  | 金相测试取样条件 | DB注释(中文) |
| 432 | SR_MGRPHY_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 金相测试长度方向取样位置 | DB注释(中文) |
| 433 | SR_MGRPHY_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 金相测试宽度方向取样位置 | DB注释(中文) |
| 434 | SR_MGRPHY_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 金相测试取样试样方向 | DB注释(中文) |
| 435 | SR_MGRPHY_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 金相测试取样试样号数 | DB注释(中文) |
| 436 | SR_MGRPHY_GRNSZ_LEVEL | NUMBER | Y |  | 金相测试晶粒度级别 | DB注释(中文) |
| 437 | SR_MGRPHY_GRNSZ_OCCP | NUMBER | Y |  | 金相测试基相晶粒的体积分数 | DB注释(中文) |
| 438 | SR_MGRPHY_FGS_MIXED_GRT_CD | VARCHAR2(1) | Y |  | 铁素体晶粒混晶保证代号 | DB注释(中文) |
| 439 | SR_MGRPHY_FGS_MIXED_RATIO | NUMBER | Y |  | 铁素体晶粒混晶占有率 | DB注释(中文) |
| 440 | SR_MGRPHY_FGS_DEVT_GRT_CD | VARCHAR2(1) | Y |  | 铁素体混晶晶粒度差保证代号 | DB注释(中文) |
| 441 | SR_MGRPHY_FGS_DEVT_MAX | NUMBER | Y |  | 铁素体混晶晶粒度差上限值 | DB注释(中文) |
| 442 | SR_MGRPHY_FGS_GRT_CD | VARCHAR2(1) | Y |  | 铁素体晶粒尺寸保证代号 | DB注释(中文) |
| 443 | SR_MGRPHY_FGS_MIN | NUMBER | Y |  | 铁素体晶粒尺寸下限值 | DB注释(中文) |
| 444 | SR_MGRPHY_FGS_MAX | NUMBER | Y |  | 铁素体晶粒尺寸上限值 | DB注释(中文) |
| 445 | SR_MGRPHY_AGS_GRT_CD | VARCHAR2(1) | Y |  | 奥氏体晶粒尺寸保证代号 | DB注释(中文) |
| 446 | SR_MGRPHY_AGS_MIN | NUMBER | Y |  | 奥氏体晶粒尺寸下限值 | DB注释(中文) |
| 447 | SR_MGRPHY_AGS_MAX | NUMBER | Y |  | 奥氏体晶粒尺寸上限值 | DB注释(中文) |
| 448 | SR_MGRPHY_INCLD_GRT_CD | VARCHAR2(1) | Y |  | 夹杂物保证代号 | DB注释(中文) |
| 449 | SR_MGRPHY_INCLD_TY | VARCHAR2(1) | Y |  | 夹杂物类别 | DB注释(中文) |
| 450 | SR_MGRPHY_INCLD_GRD_MAX | NUMBER | Y |  | 夹杂物等级上限值 | DB注释(中文) |
| 451 | SR_MGRPHY_DECARBON_GRT_CD | VARCHAR2(1) | Y |  | 脱碳层保证代号 | DB注释(中文) |
| 452 | SR_MGRPHY_DECARBON_MAX | NUMBER | Y |  | 脱碳层上限值 | DB注释(中文) |
| 453 | SR_MGRPHY_WILD_STRC_GRT_CD | VARCHAR2(1) | Y |  | 魏氏组织保证代号 | DB注释(中文) |
| 454 | SR_MGRPHY_WILD_STRC_GRD | NUMBER | Y |  | 魏氏组织等级 | DB注释(中文) |
| 455 | SR_MGRPHY_MTLGRP_GRT_CD | VARCHAR2(1) | Y |  | 组织类型保证代号 | DB注释(中文) |
| 456 | SR_MGRPHY_MTLGRP_TY | VARCHAR2(2) | Y |  | 组织类型 | DB注释(中文) |
| 457 | SR_MGRPHY_BAND_STRC_GRT_CD | VARCHAR2(1) | Y |  | 带状组织保证代号 | DB注释(中文) |
| 458 | SR_MGRPHY_BAND_STRC_GRD_MAX | NUMBER | Y |  | 带状组织等级上限值 | DB注释(中文) |
| 459 | SR_MGRPHY_GRNSZ_LEVEL_GRT_CD | VARCHAR2(1) | Y |  | 金相测试晶粒度级别代码 | DB注释(中文) |

### SCH_HSM_ROLL_DESIGN_SLAB

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=22｜被读 8 过程 / 被写 7 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：1　**主键**：FAC_CD、SLAB_NO　**语义覆盖**：65/89

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID_Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(100) | Y |  | Created Object ID_Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Datetime_Created Datetime | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Updated User ID_Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Updated Object ID_Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Updated Datetime_Updated Datetime | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Archive Flag_Archive Flag | DB注释(非中文) |
| 8 | FAC_CD | VARCHAR2(1) | N | ✓ | Factory Classification_???? | DB注释(非中文) |
| 9 | SLAB_NO | VARCHAR2(14) | N | ✓ | Slab??_Slab？？ | DB注释(非中文) |
| 10 | ROLL_DGN_MGT_NO | NUMBER | Y |  | Roll??????_Roll？？管理？？ | DB注释(中文) |
| 11 | ROLL_INNER_SLAB_SEQ | NUMBER | Y |  | ROLL???????_Roll？位？？制？序 | DB注释(中文) |
| 12 | HEAT_NO | VARCHAR2(13) | Y |  | Heat No_Heat?? | DB注释(非中文) |
| 13 | SMP_NO | VARCHAR2(11) | Y |  | ????_???? | DB注释(非中文) |
| 14 | ORD_NO | VARCHAR2(10) | Y |  | ????_???? | DB注释(非中文) |
| 15 | ORD_LN | VARCHAR2(3) | Y |  | ????_???? | DB注释(非中文) |
| 16 | SLAB_THK | NUMBER | Y |  | Slab Thickness_???? | DB注释(非中文) |
| 17 | SLAB_WTH | NUMBER | Y |  | Slab Width_???? | DB注释(非中文) |
| 18 | SLAB_LTH | NUMBER | Y |  | Slab Length_???? | DB注释(非中文) |
| 19 | SLAB_WGT | NUMBER | Y |  | Slab Weight_???? | DB注释(非中文) |
| 20 | RF_SML_CH_LOT_NO | VARCHAR2(16) | Y |  | ?????Lot??_?????Lot?? | DB注释(非中文) |
| 21 | HR_ROLL_UNIT_CD | VARCHAR2(1) | Y |  | ??Roll????_??Roll???? | DB注释(非中文) |
| 22 | ORD_USAGE | VARCHAR2(4) | Y |  | ??????_?????? | DB注释(非中文) |
| 23 | YD_MTRL_TY | VARCHAR2(8) | Y |  | Yard Material Type_Yard???? | DB注释(非中文) |
| 24 | SLAB_LOC | VARCHAR2(9) | Y |  | Slab Location_Slab???? | DB注释(非中文) |
| 25 | PROD_CD | VARCHAR2(3) | Y |  | ????_???? | DB注释(非中文) |
| 26 | HR_PROD_THK_AIM | NUMBER | Y |  | ??????_?????? | DB注释(非中文) |
| 27 | HR_PROD_WTH_AIM | NUMBER | Y |  | ?????_?????? | DB注释(非中文) |
| 28 | CONF_PASS_PLANT_CD | VARCHAR2(30) | Y |  | ????????_???????? | DB注释(非中文) |
| 29 | ORD_DLV_DT | VARCHAR2(8) | Y |  | ????_????? | DB注释(非中文) |
| 30 | SLAB_INST_DEST_CD | VARCHAR2(2) | Y |  | Slab??????_SLAB?????? | DB注释(非中文) |
| 31 | URGENT_TY | VARCHAR2(1) | Y |  | ???_???? | DB注释(非中文) |
| 32 | SPECIFIC_GRAVITY | NUMBER | Y |  | ??_?? | DB注释(非中文) |
| 33 | HR_ROLL_DGN_FL | VARCHAR2(1) | Y |  | ??Roll????_??Roll???? | DB注释(非中文) |
| 34 | ORD_TY | VARCHAR2(2) | Y |  | OrderType_???? | DB注释(非中文) |
| 35 | SPEC_CD | VARCHAR2(50) | Y |  | ??????(????)_?????? | DB注释(非中文) |
| 36 | INCMP_STEEL_NO | VARCHAR2(10) | Y |  | ??????(????)_???????? | DB注释(非中文) |
| 37 | HRL_MFC_STD_NO | VARCHAR2(11) | Y |  | ????????_???????? | DB注释(非中文) |
| 38 | SLAB_STA_WTH | NUMBER | Y |  | Slab Start Width_Slab???? | DB注释(非中文) |
| 39 | SLAB_END_WTH | NUMBER | Y |  | Slab End Width_Slab???? | DB注释(非中文) |
| 40 | DIV_PCS | NUMBER | Y |  | ???_S??? | DB注释(非中文) |
| 41 | ORD_NO1 | VARCHAR2(10) | Y |  | ????1_????1 | DB注释(非中文) |
| 42 | ORD_LN1 | VARCHAR2(3) | Y |  | ????1_????1 | DB注释(非中文) |
| 43 | SLAB_WGT1 | NUMBER | Y |  | Slab Weight1_????1 | DB注释(非中文) |
| 44 | ORD_NO2 | VARCHAR2(10) | Y |  | ????2_????2 | DB注释(非中文) |
| 45 | ORD_LN2 | VARCHAR2(3) | Y |  | ????2_????2 | DB注释(非中文) |
| 46 | SLAB_WGT2 | NUMBER | Y |  | Slab Weight2_????2 | DB注释(非中文) |
| 47 | ORD_NO3 | VARCHAR2(10) | Y |  | ????3_????3 | DB注释(非中文) |
| 48 | ORD_LN3 | VARCHAR2(3) | Y |  | ????3_????3 | DB注释(非中文) |
| 49 | SLAB_WGT3 | NUMBER | Y |  | Slab Weight3_????3 | DB注释(非中文) |
| 50 | TAPER_FL | VARCHAR2(1) | Y |  | Taper??_Taper?? | DB注释(非中文) |
| 51 | SAME_WTH_CD | NUMBER | Y |  | ?????_ | DB注释(非中文) |
| 52 | SAME_WTH_LIMIT_CNT | NUMBER | Y |  | ??? ????_ | DB注释(非中文) |
| 53 | SAME_THK_CD | NUMBER | Y |  | ??????_ | DB注释(非中文) |
| 54 | SAME_THK_LIMIT_CNT | NUMBER | Y |  | ????????_ | DB注释(非中文) |
| 55 | ROLL_THK_ALLOW_MIN | NUMBER | Y |  | ROLL????MIN_ | DB注释(非中文) |
| 56 | ROLL_THK_ALLOW_MAX | NUMBER | Y |  | ROLL????MAX_ | DB注释(非中文) |
| 57 | TARGET_FL | VARCHAR2(1) | Y |  | 대상구분 | SCO_DATA_DIC(D) |
| 58 | ROLL_MAT_TY | VARCHAR2(3) | Y |  | 압연재료구분 | SCO_DATA_DIC(D) |
| 59 | ROLL_MAT_LTH | NUMBER | Y |  |  | 空 |
| 60 | STD_STLGRD | VARCHAR2(20) | Y |  | 牌号 | SCO_DATA_DIC(D) |
| 61 | ROLL_MAT_CAT | VARCHAR2(3) | Y |  |  | 空 |
| 62 | SORT_KEY | VARCHAR2(200) | Y |  | SortKey¿_SortKey¿ | SCO_DATA_DIC(D) |
| 63 | ROLL_ADJ_YN | VARCHAR2(1) | Y |  |  | 空 |
| 64 | ROLL_ADJ_USER_ID | VARCHAR2(20) | Y |  |  | 空 |
| 65 | ROLL_ADJ_DTM | VARCHAR2(14) | Y |  |  | 空 |
| 66 | ORD_NO4 | VARCHAR2(10) | Y |  | Order No4 | SCO_DATA_DIC(D) |
| 67 | ORD_LN4 | VARCHAR2(3) | Y |  | Order Line4 | SCO_DATA_DIC(D) |
| 68 | SLAB_WGT4 | NUMBER | Y |  |  | 空 |
| 69 | ORD_NO5 | VARCHAR2(10) | Y |  | Order No5 | SCO_DATA_DIC(D) |
| 70 | ORD_LN5 | VARCHAR2(3) | Y |  | Order Line5 | SCO_DATA_DIC(D) |
| 71 | SLAB_WGT5 | NUMBER | Y |  |  | 空 |
| 72 | ORD_NO6 | VARCHAR2(10) | Y |  |  | 空 |
| 73 | ORD_LN6 | VARCHAR2(3) | Y |  |  | 空 |
| 74 | SLAB_WGT6 | NUMBER | Y |  |  | 空 |
| 75 | MPLATE_DGN_THK | NUMBER | Y |  |  | 空 |
| 76 | MPLATE_DGN_WTH | NUMBER | Y |  |  | 空 |
| 77 | MPLATE_DGN_LTH | NUMBER | Y |  |  | 空 |
| 78 | MPLATE_DGN_WGT | NUMBER | Y |  |  | 空 |
| 79 | ORD_NO7 | VARCHAR2(10) | Y |  |  | 空 |
| 80 | ORD_LN7 | VARCHAR2(3) | Y |  |  | 空 |
| 81 | SLAB_WGT7 | NUMBER | Y |  |  | 空 |
| 82 | ORD_NO8 | VARCHAR2(10) | Y |  | ORD_NO9 | SCO_DATA_DIC(D) |
| 83 | ORD_LN8 | VARCHAR2(3) | Y |  |  | 空 |
| 84 | SLAB_WGT8 | NUMBER | Y |  |  | 空 |
| 85 | ORD_NO9 | VARCHAR2(10) | Y |  |  | 空 |
| 86 | ORD_LN9 | VARCHAR2(3) | Y |  |  | 空 |
| 87 | SLAB_WGT9 | NUMBER | Y |  |  | 空 |
| 88 | HR_PROD_DIA_AIM | NUMBER | Y |  |  | 空 |
| 89 | HR_PROD_LTH_AIM | NUMBER | Y |  |  | 空 |

### SMS_RSLT_LF

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=22｜被读 18 过程 / 被写 2 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：10694　**主键**：HEAT_NO、PROC_PASS_CNT　**语义覆盖**：108/108

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | SCO_DATA_DIC(D) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID已创建对象ID | DB注释(中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time创建时间 | DB注释(中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID上次更新的用户ID | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID上次更新的对象ID | DB注释(中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time上次更新时间 | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag记录存档标志 | DB注释(中文) |
| 8 | HEAT_NO | VARCHAR2(10) | N | ✓ | Heat No炉号 | DB注释(中文) |
| 9 | PROC_PASS_CNT | NUMBER | N | ✓ | Process Pass Times过程通过时间 | DB注释(中文) |
| 10 | PLAN_HEAT_NO | VARCHAR2(8) | Y |  | Plan Heat No计划炉号 | DB注释(中文) |
| 11 | PROC_SERIAL_NO | NUMBER | Y |  | Process Serial No工艺序列号 | DB注释(中文) |
| 12 | SUMUP_DT | VARCHAR2(8) | Y |  | Operation Sumup date操作总结日期 | DB注释(中文) |
| 13 | OPER_DT | VARCHAR2(8) | Y |  | Operation Date运行日期 | DB注释(中文) |
| 14 | OPER_SHIFT | VARCHAR2(2) | Y |  | Operation Shift操作班次 | DB注释(中文) |
| 15 | OPER_EMP_NO | VARCHAR2(20) | Y |  | Operator Employee No操作员员工编号 | DB注释(中文) |
| 16 | PROC_METHOD | VARCHAR2(4) | Y |  | Process Method工艺方法 | DB注释(中文) |
| 17 | PROC_PTRN | VARCHAR2(3) | Y |  | Process Pattern过程模式 | DB注释(中文) |
| 18 | LF_NO | VARCHAR2(1) | Y |  | LF NoLF编号 | DB注释(中文) |
| 19 | ARR_DTM | VARCHAR2(14) | Y |  | Ladle Arrival Date钢包到达日期 | DB注释(中文) |
| 20 | DEP_DTM | VARCHAR2(14) | Y |  | Ladle Departure Date钢包离开日期 | DB注释(中文) |
| 21 | FST_COVER_DN_DTM | VARCHAR2(14) | Y |  | LF First Cover Down DateLF首次覆盖日期 | DB注释(中文) |
| 22 | LST_COVER_UP_DTM | VARCHAR2(14) | Y |  | LF Last Conver Rise DateLF最后召集人上升日期 | DB注释(中文) |
| 23 | PROC_STA_DTM | VARCHAR2(14) | Y |  | Process Start Date进程开始日期 | DB注释(中文) |
| 24 | PROC_END_DTM | VARCHAR2(14) | Y |  | Process End Date流程结束日期 | DB注释(中文) |
| 25 | PROC_TOT_DUR | NUMBER | Y |  | Total Process Time总处理时间 | DB注释(中文) |
| 26 | BTM_BB_TOT_DUR | NUMBER | Y |  | Bottom Bubbling Total Time底部气泡总时间 | DB注释(中文) |
| 27 | TOP_BB_TOT_DUR | NUMBER | Y |  | Top Bubbling Total Times顶部冒泡总次数 | DB注释(中文) |
| 28 | HEATING_TOT_DUR | NUMBER | Y |  | Total Heating Time总加热时间 | DB注释(中文) |
| 29 | HEATING_TOT_EPOWER | NUMBER | Y |  | LF Total Heating Electronic Used QuantityLF总加热电子使用量 | DB注释(中文) |
| 30 | BTM_BB_GAS_TY | VARCHAR2(1) | Y |  | Bottom Bubbling Gas Type底部气泡气体类型 | DB注释(中文) |
| 31 | AR_USED_TOT_VOL | NUMBER | Y |  | Total Ar Used Volume总Ar使用量 | DB注释(中文) |
| 32 | N2_USED_TOT_VOL | NUMBER | Y |  | Total N2 Used VolumeN2总使用量 | DB注释(中文) |
| 33 | HEATING_FST_SET_TAP | VARCHAR2(2) | Y |  | First Heating setting TAP第一次加热设置TAP | DB注释(中文) |
| 34 | INSUL_IN_WGT | NUMBER | Y |  | Insulator Used Weight绝缘子使用重量 | DB注释(中文) |
| 35 | LD_FREEBRD | NUMBER | Y |  | LD Free BoardLD自由板 | DB注释(中文) |
| 36 | TOP_BB_LN_NO | NUMBER | Y |  | Top Bubbling Lance No顶部气泡喷枪编号 | DB注释(中文) |
| 37 | TOP_BB_LN_USED_CNT | NUMBER | Y |  | Top Bubbling Lance Used Times顶部气泡喷枪使用次数 | DB注释(中文) |
| 38 | COVER_NO | NUMBER | Y |  | Cover No封面编号 | DB注释(中文) |
| 39 | COVER_USED_CNT | NUMBER | Y |  | Cover Used Times覆盖使用时间 | DB注释(中文) |
| 40 | PI_PROC_TOT_DUR | NUMBER | Y |  | Powder Injection Total Process Time粉末注射总工艺时间 | DB注释(中文) |
| 41 | PI_LN_NO | NUMBER | Y |  | Powder Injection Lance No粉末注射枪编号 | DB注释(中文) |
| 42 | PI_LN_USED_CNT | NUMBER | Y |  | Powder Injection Lance Used Times粉末注射枪使用次数 | DB注释(中文) |
| 43 | LST_AL_AFT_BB_DUR | NUMBER | Y |  | After last AL Input, Bubbling Time上次AL输入后，气泡时间 | DB注释(中文) |
| 44 | COOLANT_IN_AFT_BB_DUR | NUMBER | Y |  | After Last Coolant input, Bubbling Time最后一次冷却液输入后，起泡时间 | DB注释(中文) |
| 45 | OPER_MODE_TY | VARCHAR2(1) | Y |  | Operation Mode Type操作模式类型 | DB注释(中文) |
| 46 | ARR_REQ_TEMP | NUMBER | Y |  | Arrival requested Temperature到达要求温度 | DB注释(中文) |
| 47 | ARR_TEMP | NUMBER | Y |  | Arrival Temperature到达温度 | DB注释(中文) |
| 48 | ARR_OXG_DEN | NUMBER | Y |  | Arrival Oxygen Density到达氧气密度 | DB注释(中文) |
| 49 | DEP_TEMP | NUMBER | Y |  | Departure Temperature出发温度 | DB注释(中文) |
| 50 | DEP_OXG_DEN | NUMBER | Y |  | Departure oxygen density起飞氧气密度 | DB注释(中文) |
| 51 | NXT_PROC_REQ_TEMP | NUMBER | Y |  | Next Process requried Arrival Temperature下一个工艺要求的到达温度 | DB注释(中文) |
| 52 | DEP_PLAN_TEMP | NUMBER | Y |  | Plan Departure Temperature计划出发温度 | DB注释(中文) |
| 53 | H_DEN | NUMBER | Y |  | Measured Hydrogen Density测量的氢密度 | DB注释(中文) |
| 54 | PROC_AFT_CALC_STEEL_WGT | NUMBER | Y |  | After process, Calcualte Heat Quantity加工后，计算热量 | DB注释(中文) |
| 55 | ARR_CALC_TEMP | NUMBER | Y |  | Calculated Arrival Temperature计算的到达温度 | DB注释(中文) |
| 56 | STEEL_SURF_CRUSH_CNT | NUMBER | Y |  | Steel Surface Cursh Times钢表面翘曲时间 | DB注释(中文) |
| 57 | SLAG_MSU_THK | NUMBER | Y |  | LD Slag Measured ThicknessLD渣测量厚度 | DB注释(中文) |
| 58 | H_DEN_MSU_DTM | VARCHAR2(14) | Y |  | Hydrogen Density measurement Date氢密度测量日期 | DB注释(中文) |
| 59 | ARR_REQ_DTM | VARCHAR2(14) | Y |  | Required Arrival Date要求到达日期 | DB注释(中文) |
| 60 | UNPLAN_PROC_CD | VARCHAR2(1) | Y |  | Un-Planed Process Reason Code未计划流程原因代码 | DB注释(中文) |
| 61 | OPER_LNG_USED_VOL | NUMBER | Y |  | Operation LNG Used Volume运行LNG使用量 | DB注释(中文) |
| 62 | LD_NO | VARCHAR2(22) | Y |  | Ladle No钢包编号 | DB注释(中文) |
| 63 | SILICA_USED_QTY | NUMBER | Y |  | Silica Used Quantity二氧化硅用量 | DB注释(中文) |
| 64 | LST_LD_DEP_DTM | VARCHAR2(14) | Y |  | Last Ladle Departure Date上次钢包离开日期 | DB注释(中文) |
| 65 | LST_LD_TRANSCAR_MOVE_END_DTM | VARCHAR2(14) | Y |  | Last Transfer Car Moving Date上次转运车移动日期 | DB注释(中文) |
| 66 | FLUX_IN_WGT | NUMBER | Y |  | Flux Input Weight通量输入权重 | DB注释(中文) |
| 67 | WIRE_FEED_TY | VARCHAR2(5) | Y |  | Wire Feed Type送丝类型 | DB注释(中文) |
| 68 | WIRE_FEED_QTY | NUMBER | Y |  | Wire Feed Quantity送丝量 | DB注释(中文) |
| 69 | WIRE_FEED_LTH | NUMBER | Y |  | Wire Feed Length送丝长度 | DB注释(中文) |
| 70 | CA_IN_QTY | NUMBER | Y |  | Ca Input QuantityCa输入数量 | DB注释(中文) |
| 71 | FERRO_AFT_BB_DUR | NUMBER | Y |  | After Ferro Alloy Input, Bubbling Time铁合金输入后，起泡时间 | DB注释(中文) |
| 72 | CA_AFT_BB_DUR | NUMBER | Y |  | After Ca Process, Bubbling TimeCa处理后，起泡时间 | DB注释(中文) |
| 73 | CONS_H_QTY | NUMBER | Y |  | H Contents QuantityH内容数量 | DB注释(中文) |
| 74 | SLAG_BST | NUMBER | Y |  | Slag Basicity矿渣碱性 | DB注释(中文) |
| 75 | LOW_STAY_DUR | NUMBER | Y |  | Steel Lower Stay time钢制下部停留时间 | DB注释(中文) |
| 76 | BEF_PROC_CD | VARCHAR2(2) | Y |  | Before Process Code流程代码之前 | DB注释(中文) |
| 77 | PROC_TGT_DUR | NUMBER | Y |  | Target process time目标处理时间 | DB注释(中文) |
| 78 | MOVE_TGT_DUR | NUMBER | Y |  | Target moving time目标移动时间 | DB注释(中文) |
| 79 | MOVE_ACT_DUR | NUMBER | Y |  | actual moving time实际移动时间 | DB注释(中文) |
| 80 | ARR_TGT_TEMP | NUMBER | Y |  | Arrival Target Temperature到达目标温度 | DB注释(中文) |
| 81 | RE_PROC_REASON_TY | VARCHAR2(2) | Y |  | Re-processing Reason Code重新处理原因代码 | DB注释(中文) |
| 82 | SPEC_CD | VARCHAR2(50) | Y |  | Specification Code 钢种 | DB注释(中文) |
| 83 | LIFTING_LADLE_DTM | VARCHAR2(14) | Y |  | 吊包时间 | DB注释(中文) |
| 84 | REFINING_TIME | NUMBER | Y |  | 冶炼周期 | DB注释(中文) |
| 85 | SOFT_BLOW_TM | NUMBER | Y |  | 软吹时间 | DB注释(中文) |
| 86 | POWER_INPUTING_TM | NUMBER | Y |  | 送电时间 | DB注释(中文) |
| 87 | POWER_CONS | NUMBER | Y |  | 电耗 | DB注释(中文) |
| 88 | LADLE_STAT | VARCHAR2(20) | Y |  | 钢包情况 | DB注释(中文) |
| 89 | BOTTOM_BLOW_STAT | VARCHAR2(20) | Y |  | 底吹时间 | DB注释(中文) |
| 90 | DETER_OXY | NUMBER | Y |  | 定氧PPM | DB注释(中文) |
| 91 | MOLTEN_STEEL_AIM | VARCHAR2(2) | Y |  | 钢水去向 | DB注释(中文) |
| 92 | FURNACE_LEADER | VARCHAR2(20) | Y |  | 炉长 | DB注释(中文) |
| 93 | SHIFT_NO | VARCHAR2(2) | Y |  | 班次 | DB注释(中文) |
| 94 | SHIFT_GRP | VARCHAR2(2) | Y |  | 班组 | DB注释(中文) |
| 95 | REMARK | VARCHAR2(100) | Y |  | 备注 | DB注释(中文) |
| 96 | PI_WGT | VARCHAR2(20) | Y |  | 钢水重量 | DB注释(中文) |
| 97 | STD_STLGRD | VARCHAR2(20) | Y |  | 钢种 | DB注释(中文) |
| 98 | OPER_GRP | VARCHAR2(2) | Y |  | 班组 | DB注释(中文) |
| 99 | ARR_WGT | VARCHAR2(20) | Y |  | 到站重量 | DB注释(中文) |
| 100 | DEP_WGT | VARCHAR2(20) | Y |  | 离站重量 | DB注释(中文) |
| 101 | AR_CONSMP | VARCHAR2(20) | Y |  | 氩气消耗 | DB注释(中文) |
| 102 | SFUR_COVER_NUM | VARCHAR2(20) | Y |  | 小炉盖次数 | DB注释(中文) |
| 103 | BFUR_COVER_NUM | VARCHAR2(20) | Y |  | 大炉盖次数 | DB注释(中文) |
| 104 | SVG_POWER | VARCHAR2(20) | Y |  | SVG电耗 | DB注释(中文) |
| 105 | ABNL_CAUSE | VARCHAR2(100) | Y |  | 异常原因 | DB注释(中文) |
| 106 | HEAT_FEAR | VARCHAR2(10) | Y |  | 加热档位 | DB注释(中文) |
| 107 | LD_AGE | VARCHAR2(20) | Y |  | 钢包包龄 | DB注释(中文) |
| 108 | ELE_CONSUME | VARCHAR2(20) | Y |  | 电极消耗 | DB注释(中文) |

### SCR_RSMS_ROLL_DATA

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=22｜被读 8 过程 / 被写 7 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：0　**主键**：ROLL_ID　**语义覆盖**：40/50

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | CREATED_DATE | DATE | Y |  |  | 空 |
| 9 | UPDATED_DATE | DATE | Y |  |  | 空 |
| 10 | UPDATED_BY | VARCHAR2(80) | Y |  |  | 空 |
| 11 | HANDSHAKE_STATUS | VARCHAR2(1) | Y |  |  | 空 |
| 12 | ERR_1 | NUMBER | Y |  |  | 空 |
| 13 | ERR_2 | NUMBER | Y |  |  | 空 |
| 14 | ERR_3 | NUMBER | Y |  |  | 空 |
| 15 | ERR_4 | NUMBER | Y |  |  | 空 |
| 16 | ERR_5 | NUMBER | Y |  |  | 空 |
| 17 | COMMENTS | VARCHAR2(160) | Y |  |  | 空 |
| 18 | PRIM_INDEX | NUMBER | Y |  | Primary key | DB注释(非中文) |
| 19 | LINE_CODE | VARCHAR2(4) | Y |  | Line code of the process line. | DB注释(非中文) |
| 20 | STAND_NO | NUMBER | Y |  | Stand number | DB注释(非中文) |
| 21 | ROLL_TYPE | VARCHAR2(3) | Y |  | Roll type | DB注释(非中文) |
| 22 | ROLL_ID | VARCHAR2(20) | N | ✓ | Top roll ID | DB注释(非中文) |
| 23 | ROLL_MAKER_CODE | VARCHAR2(4) | Y |  | Maker code of the  roll | DB注释(非中文) |
| 24 | ROLL_MATERIAL_CODE | VARCHAR2(8) | Y |  | Material code of the  roll | DB注释(非中文) |
| 25 | ROLL_SURF_TYPE | VARCHAR2(4) | Y |  | Indicates whether  roll is textured and chrome plated | DB注释(非中文) |
| 26 | ROLL_BUR_TYPE | VARCHAR2(1) | Y |  | Indicates whether the  BUR is of CVC type | DB注释(非中文) |
| 27 | ROLL_DIA | NUMBER | Y |  | roll diameter | DB注释(非中文) |
| 28 | ROLL_CROWN | NUMBER | Y |  | Crown height of  roll | DB注释(非中文) |
| 29 | ROLL_ROUGH_RA | NUMBER | Y |  | Average roughness of roll | DB注释(非中文) |
| 30 | ROLL_ROUGH_RZ | NUMBER | Y |  | Average roughness of roll I Rz | DB注释(非中文) |
| 31 | ROLL_ROUGH_MAX | NUMBER | Y |  | Maximum roughness of roll in Ra | DB注释(非中文) |
| 32 | ROLL_PEAK_COUNT | NUMBER | Y |  | Average peak count of roll | DB注释(非中文) |
| 33 | ROLL_ROLLQUALITY | NUMBER | Y |  | K96080 RiZhao SMS requires WR quality(1=chrome, 2=indefinite chill, 3 =HSS??-1=No Info) | DB注释(非中文) |
| 34 | ROLL_GRINDSTARTTIME | DATE | Y |  | K96080 RiZhao. Starting time by last grinding this top(bottom) roll | DB注释(非中文) |
| 35 | ROLL_GRINDENDTIME | DATE | Y |  | K96080 RiZhao. End Time by grinding this top(bottom) roll | DB注释(非中文) |
| 36 | ROLL_SHAPE_CODE | VARCHAR2(1) | Y |  | The shape code which is used in the RSMS / RSMA data table T_SHAPE to host barrel shape parameters. The shape code is mapped to the curve-ID of a grinding process.                                                                          for RiZhao Curve type: 1=flat, 2=circle, 3 cone, 4=sine, V=individual points, P=interpolation (CVC), Q=CVC+ (for 96080 requirement Instand of standard complete curve type name. Here will only the BasicType referenced. Based no Mill requirement. ) | DB注释(非中文) |
| 37 | ROLL_OS_CHOCK_OUTER | VARCHAR2(20) | Y |  | Outer chock ID of roll at operator | DB注释(非中文) |
| 38 | ROLL_OS_CHOCK_INNER | VARCHAR2(20) | Y |  | Inner chock ID of roll at operator side | DB注释(非中文) |
| 39 | ROLL_DS_CHOCK_OUTER | VARCHAR2(20) | Y |  | Outer chock ID of roll at drive side | DB注释(非中文) |
| 40 | ROLL_DS_CHOCK_INNER | VARCHAR2(20) | Y |  | Inner chock ID of roll at drive side | DB注释(非中文) |
| 41 | ROLL_SHIM_THICKNESS | NUMBER | Y |  | Shim thickness in case of BUR roll | DB注释(非中文) |
| 42 | ROLL_CHAMFERED | NUMBER | Y |  | Indicates whether barrel of roll contains chamfer | DB注释(非中文) |
| 43 | ROLL_CHAMFER_LENGTH | NUMBER | Y |  | Length of the chamfer of roll | DB注释(非中文) |
| 44 | ROLL_CHAMFER_HEIGHT | NUMBER | Y |  | Height of the chamfer of roll | DB注释(非中文) |
| 45 | ROLL_CVC_COEFF_1 | NUMBER | Y |  | CVC coefficient 1 of roll | DB注释(非中文) |
| 46 | ROLL_CVC_COEFF_2 | NUMBER | Y |  | CVC coefficient 2 of roll | DB注释(非中文) |
| 47 | ROLL_CVC_COEFF_3 | NUMBER | Y |  | CVC coefficient 3 of roll | DB注释(非中文) |
| 48 | ROLL_CVC_COEFF_4 | NUMBER | Y |  | CVC coefficient 4 of roll | DB注释(非中文) |
| 49 | ROLL_CVC_COEFF_5 | NUMBER | Y |  | CVC coefficient 5 of roll | DB注释(非中文) |
| 50 | ROLL_HARD_GRIND | NUMBER | Y |  | Average hardness of the roll after grinding | DB注释(非中文) |

### SIM_CO_PUR_MTRL_ITEM

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=22｜被读 8 过程 / 被写 7 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：303　**主键**：DATA_CYCLE、IR_CHE_OP_AC_DT、PROC_CD、IR_CHE_IO_TY、ITEM_CD　**语义覆盖**：17/17

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | ??UserID_??UserID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | ??ObjectID_??ObjectID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | ????_???? | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | ??UserID_??UserID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | ??ObjectID_??ObjectID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | ????_???? | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Archive??_Archive?? | DB注释(非中文) |
| 8 | DATA_CYCLE | VARCHAR2(1) | N | ✓ | ??????_?????? | DB注释(非中文) |
| 9 | IR_CHE_OP_AC_DT | VARCHAR2(8) | N | ✓ | ??????_?????? | DB注释(非中文) |
| 10 | PROC_CD | VARCHAR2(3) | N | ✓ | ??????_?????? | DB注释(非中文) |
| 11 | IR_CHE_IO_TY | VARCHAR2(1) | N | ✓ | ??IO????_????IO???? | DB注释(非中文) |
| 12 | ITEM_CD | VARCHAR2(20) | N | ✓ | Item??_Item?? | DB注释(非中文) |
| 13 | IR_CHE_PROD_USE_QTY | NUMBER | Y |  | ???????_????????? | DB注释(非中文) |
| 14 | IR_CHE_DEC_QTY | NUMBER | Y |  | ????????_?????????? | DB注释(非中文) |
| 15 | IR_BAS_UT_CSUM | NUMBER | Y |  | ???????_??????? | DB注释(非中文) |
| 16 | COMPONENT_QTY | NUMBER | Y |  | Item???_Item??? | DB注释(非中文) |
| 17 | IR_CHE_FORM_NM | VARCHAR2(250) | Y |  | Iron Making FormNm | SCO_DATA_DIC(D) |

### SMS_MAT_CONSUM

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=22｜被读 10 过程 / 被写 6 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：53　**主键**：HEAT_NO、SMS_PROC_CD、PROC_PASS_CNT、RM_REP_MTRL_CD、MTRL_IN_AREA_CD　**语义覆盖**：17/18

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | HEAT_NO | VARCHAR2(9) | N | ✓ | Heat No | DB注释(非中文) |
| 9 | SMS_PROC_CD | VARCHAR2(2) | N | ✓ | SMS Process Code | DB注释(非中文) |
| 10 | PROC_PASS_CNT | NUMBER | N | ✓ | Process Pass Times | DB注释(非中文) |
| 11 | RM_REP_MTRL_CD | VARCHAR2(20) | N | ✓ | R/Mat Representative Material Code | DB注释(非中文) |
| 12 | MTRL_IN_AREA_CD | VARCHAR2(3) | N | ✓ | Input Area Code | DB注释(非中文) |
| 13 | MTRL_IN_STA_DTM | VARCHAR2(14) | Y |  | Input Start Date | DB注释(非中文) |
| 14 | MTRL_IN_END_DTM | VARCHAR2(14) | Y |  | Input End Date | DB注释(非中文) |
| 15 | MTRL_IN_WGT | NUMBER | Y |  | Material Input Weight | DB注释(非中文) |
| 16 | MTRL_TY | VARCHAR2(1) | Y |  | Material Type | DB注释(非中文) |
| 17 | CONF_USER_ID | VARCHAR2(20) | Y |  |  | 空 |
| 18 | CONF_DTM | VARCHAR2(14) | Y |  | Confirmation Date | SCO_DATA_DIC(D) |

### SQM_ORD_MECH_CRL

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=22｜被读 18 过程 / 被写 2 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：0　**主键**：ORD_NO、ORD_LN、QLT_DSN_STD_TY　**语义覆盖**：419/420

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 修改人 | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | 修改时间 | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | ORD_NO | VARCHAR2(10) | N | ✓ | 订单编号 | DB注释(中文) |
| 9 | ORD_LN | VARCHAR2(3) | N | ✓ | 订单行号 | DB注释(中文) |
| 10 | QLT_DSN_STD_TY | VARCHAR2(1) | N | ✓ | 质量设计标准区分 | DB注释(中文) |
| 11 | TSL_SMP_CND | VARCHAR2(2) | Y |  | 拉伸测试取样条件 | DB注释(中文) |
| 12 | TSL_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 拉伸测试长度方向取样位置 | DB注释(中文) |
| 13 | TSL_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 拉伸测试宽度方向取样位置 | DB注释(中文) |
| 14 | TSL_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 拉伸测试取样试样方向 | DB注释(中文) |
| 15 | TSL_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 拉伸测试取样试样号数 | DB注释(中文) |
| 16 | TSL_YP_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度保证代号(YP) | DB注释(中文) |
| 17 | TSL_YP_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度类型(YP) | DB注释(中文) |
| 18 | TSL_YP_MIN | NUMBER | Y |  | 拉伸测试屈服强度下限值(YP) | DB注释(中文) |
| 19 | TSL_YP_MAX | NUMBER | Y |  | 拉伸测试屈服强度上限值(YP) | DB注释(中文) |
| 20 | TSL_YP_AIM | NUMBER | Y |  | 拉伸测试屈服强度目标值(YP) | DB注释(中文) |
| 21 | TSL_TS_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试抗拉强度保证代号(TS) | DB注释(中文) |
| 22 | TSL_TS_MIN | NUMBER | Y |  | 拉伸测试抗拉强度下限值(TS) | DB注释(中文) |
| 23 | TSL_TS_MAX | NUMBER | Y |  | 拉伸测试抗拉强度上限值(TS) | DB注释(中文) |
| 24 | TSL_TS_AIM | NUMBER | Y |  | 拉伸测试抗拉强度目标值(TS) | DB注释(中文) |
| 25 | TSL_EL_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试延伸率保证代号(EL) | DB注释(中文) |
| 26 | TSL_EL_CD | VARCHAR2(1) | Y |  | 拉抻测试延伸率类型(EL) | DB注释(中文) |
| 27 | TSL_EL_MIN | NUMBER | Y |  | 拉抻测试延伸率下限值(EL) | DB注释(中文) |
| 28 | TSL_EL_MAX | NUMBER | Y |  | 拉抻测试延伸率上限值(EL) | DB注释(中文) |
| 29 | TSL_EL_AIM | NUMBER | Y |  | 拉抻测试延伸率目标值(EL) | DB注释(中文) |
| 30 | TSL_EL_UNF_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试均匀延伸率保证代号(uEL) | DB注释(中文) |
| 31 | TSL_EL_UNF_MIN | NUMBER | Y |  | 拉抻测试均匀延伸率下限值(uEL) | DB注释(中文) |
| 32 | TSL_EL_UNF_MAX | NUMBER | Y |  | 拉抻测试均匀延伸率目标值(uEL) | DB注释(中文) |
| 33 | TSL_EL_UNF_AIM | NUMBER | Y |  | 拉抻测试均匀延伸率上限值(uEL) | DB注释(中文) |
| 34 | TSL_YR_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试屈强比保证代号(YR) | DB注释(中文) |
| 35 | TSL_YR_MIN | NUMBER | Y |  | 拉伸测试屈强比下限值(YR) | DB注释(中文) |
| 36 | TSL_YR_MAX | NUMBER | Y |  | 拉伸测试屈强比上限值(YR) | DB注释(中文) |
| 37 | TSL_YR_AIM | NUMBER | Y |  | 拉伸测试屈强比目标值(YR) | DB注释(中文) |
| 38 | TSL_RA_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试断面收缩率保证代号(RA) | DB注释(中文) |
| 39 | TSL_RA_MIN | NUMBER | Y |  | 拉伸测试断面收缩率下限值(RA) | DB注释(中文) |
| 40 | TSL_RA_MAX | NUMBER | Y |  | 拉伸测试断面收缩率上限值(RA) | DB注释(中文) |
| 41 | TSL_RA_AIM | NUMBER | Y |  | 拉伸测试断面收缩率目标值(RA) | DB注释(中文) |
| 42 | TSL_R_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试塑性应变比r保证代号 | DB注释(中文) |
| 43 | TSL_R_MIN | NUMBER | Y |  | 拉抻测试塑性应变比r平均下限值 | DB注释(中文) |
| 44 | TSL_R0_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试r0保证代号 | DB注释(中文) |
| 45 | TSL_R0_MIN | NUMBER | Y |  | 拉抻测试r0下限值 | DB注释(中文) |
| 46 | TSL_R45_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试r45保证代号 | DB注释(中文) |
| 47 | TSL_R45_MIN | NUMBER | Y |  | 拉抻测试r45下限值 | DB注释(中文) |
| 48 | TSL_R90_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试r90保证代号 | DB注释(中文) |
| 49 | TSL_R90_MIN | NUMBER | Y |  | 拉抻测试r90下限值 | DB注释(中文) |
| 50 | TSL_RDELTA_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试\|Δr\|保证代号 | DB注释(中文) |
| 51 | TSL_RDELTA_MAX | NUMBER | Y |  | 拉伸测试\|Δr\|上限值 | DB注释(中文) |
| 52 | TSL_N_GRT_CD | VARCHAR2(1) | Y |  | 拉伸测试加工硬化指数n保证代号 | DB注释(中文) |
| 53 | TSL_N_MIN | NUMBER | Y |  | 拉伸测试加工硬化指数n平均下限值 | DB注释(中文) |
| 54 | TSL_N0_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试n0保证代号 | DB注释(中文) |
| 55 | TSL_N0_MIN | NUMBER | Y |  | 拉抻测试n0下限值 | DB注释(中文) |
| 56 | TSL_N45_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试n45保证代号 | DB注释(中文) |
| 57 | TSL_N45_MIN | NUMBER | Y |  | 拉抻测试n45下限值 | DB注释(中文) |
| 58 | TSL_N90_GRT_CD | VARCHAR2(1) | Y |  | 拉抻测试n90保证代号 | DB注释(中文) |
| 59 | TSL_N90_MIN | NUMBER | Y |  | 拉抻测试n90下限值 | DB注释(中文) |
| 60 | BEND_SMP_CND | VARCHAR2(2) | Y |  | 弯曲测试取样条件 | DB注释(中文) |
| 61 | BEND_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 弯曲测试长度方向取样位置 | DB注释(中文) |
| 62 | BEND_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 弯曲测试宽度方向取样位置 | DB注释(中文) |
| 63 | BEND_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 弯曲测试取样试样方向 | DB注释(中文) |
| 64 | BEND_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 弯曲测试取样试样号数 | DB注释(中文) |
| 65 | BEND_GRT_CD | VARCHAR2(1) | Y |  | 弯曲测试保证代号 | DB注释(中文) |
| 66 | BEND_CD | VARCHAR2(1) | Y |  | 弯曲测试类型 | DB注释(中文) |
| 67 | BEND_UNIT | VARCHAR2(1) | Y |  | 弯曲测试单位 | DB注释(中文) |
| 68 | BEND_ANGLE | NUMBER | Y |  | 弯曲测试弯曲角度 | DB注释(中文) |
| 69 | BEND_DIA | NUMBER | Y |  | 弯曲测试弯心直径 | DB注释(中文) |
| 70 | HARD_SMP_CND | VARCHAR2(2) | Y |  | 硬度测试取样条件 | DB注释(中文) |
| 71 | HARD_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 硬度测试长度方向取样位置 | DB注释(中文) |
| 72 | HARD_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 硬度测试宽度方向取样位置 | DB注释(中文) |
| 73 | HARD_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 硬度测试取样试样方向 | DB注释(中文) |
| 74 | HARD_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 硬度测试取样试样号数 | DB注释(中文) |
| 75 | HARD_GRT_CD | VARCHAR2(1) | Y |  | 硬度测试保证代号 | DB注释(中文) |
| 76 | HARD_KIND | VARCHAR2(1) | Y |  | 硬度测试种类 | DB注释(中文) |
| 77 | HARD_MIN | NUMBER | Y |  | 硬度测试下限值 | DB注释(中文) |
| 78 | HARD_MAX | NUMBER | Y |  | 硬度测试上限值 | DB注释(中文) |
| 79 | HARD_AIM | NUMBER | Y |  | 硬度测试目标值 | DB注释(中文) |
| 80 | IMPACT_SMP_CND | VARCHAR2(2) | Y |  | 冲击测试取样条件 | DB注释(中文) |
| 81 | IMPACT_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 冲击测试长度方向取样位置 | DB注释(中文) |
| 82 | IMPACT_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 冲击测试宽度方向取样位置 | DB注释(中文) |
| 83 | IMPACT_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 冲击测试取样试样方向 | DB注释(中文) |
| 84 | IMPACT_SMP_SPCMN_NON_SZ | VARCHAR2(2) | Y |  | 冲击测试非标准取样试样号数 | DB注释(中文) |
| 85 | IMPACT_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 冲击测试标准取样试样号数 | DB注释(中文) |
| 86 | IMPACT_SMP_SPCMN_CNT | NUMBER | Y |  | 冲击测试试样数量 | DB注释(中文) |
| 87 | IMPACT_TEMP | NUMBER | Y |  | 冲击测试温度 | DB注释(中文) |
| 88 | IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 冲击测试缺口类型 | DB注释(中文) |
| 89 | IMPACT_AVG_GRT_CD | VARCHAR2(1) | Y |  | 冲击测试吸收能量保证代号 | DB注释(中文) |
| 90 | IMPACT_AVG_MIN | NUMBER | Y |  | 冲击测试吸收能量平均下限值 | DB注释(中文) |
| 91 | IMPACT_AVG_AIM | NUMBER | Y |  | 冲击测试吸收能量平均目标值 | DB注释(中文) |
| 92 | IMPACT_IND_MIN | NUMBER | Y |  | 冲击测试吸收能量单个下限值 | DB注释(中文) |
| 93 | IMPACT_SF_RATIO_GRT_CD | VARCHAR2(1) | Y |  | 冲击测试纤维断面率保证代号 | DB注释(中文) |
| 94 | IMPACT_SF_RATIO_IND_AVG_MIN | NUMBER | Y |  | 冲击测试纤维断面率单个平均下限值 | DB注释(中文) |
| 95 | IMPACT_SF_RATIO_IND_MIN | NUMBER | Y |  | 冲击测试纤维断面率单个下限值 | DB注释(中文) |
| 96 | MGRPHY_SMP_CND | VARCHAR2(2) | Y |  | 金相测试取样条件 | DB注释(中文) |
| 97 | MGRPHY_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 金相测试长度方向取样位置 | DB注释(中文) |
| 98 | MGRPHY_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 金相测试宽度方向取样位置 | DB注释(中文) |
| 99 | MGRPHY_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 金相测试取样试样方向 | DB注释(中文) |
| 100 | MGRPHY_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 金相测试取样试样号数 | DB注释(中文) |
| 101 | MGRPHY_GRNSZ_LEVEL | NUMBER | Y |  | 金相测试晶粒度级别 | DB注释(中文) |
| 102 | MGRPHY_GRNSZ_OCCP | NUMBER | Y |  | 金相测试基相晶粒的体积分数 | DB注释(中文) |
| 103 | MGRPHY_FGS_MIXED_GRT_CD | VARCHAR2(1) | Y |  | 铁素体晶粒混晶保证代号 | DB注释(中文) |
| 104 | MGRPHY_FGS_MIXED_RATIO | NUMBER | Y |  | 铁素体晶粒混晶占有率 | DB注释(中文) |
| 105 | MGRPHY_FGS_DEVT_GRT_CD | VARCHAR2(1) | Y |  | 铁素体混晶晶粒度差保证代号 | DB注释(中文) |
| 106 | MGRPHY_FGS_DEVT_MAX | NUMBER | Y |  | 铁素体混晶晶粒度差上限值 | DB注释(中文) |
| 107 | MGRPHY_FGS_GRT_CD | VARCHAR2(1) | Y |  | 铁素体晶粒尺寸保证代号 | DB注释(中文) |
| 108 | MGRPHY_FGS_MIN | NUMBER | Y |  | 铁素体晶粒尺寸下限值 | DB注释(中文) |
| 109 | MGRPHY_FGS_MAX | NUMBER | Y |  | 铁素体晶粒尺寸上限值 | DB注释(中文) |
| 110 | MGRPHY_AGS_GRT_CD | VARCHAR2(1) | Y |  | 奥氏体晶粒尺寸保证代号 | DB注释(中文) |
| 111 | MGRPHY_AGS_MIN | NUMBER | Y |  | 奥氏体晶粒尺寸下限值 | DB注释(中文) |
| 112 | MGRPHY_AGS_MAX | NUMBER | Y |  | 奥氏体晶粒尺寸上限值 | DB注释(中文) |
| 113 | MGRPHY_INCLD_GRT_CD | VARCHAR2(1) | Y |  | 夹杂物保证代号 | DB注释(中文) |
| 114 | MGRPHY_INCLD_TY | VARCHAR2(1) | Y |  | 夹杂物类别 | DB注释(中文) |
| 115 | MGRPHY_INCLD_GRD_MAX | NUMBER | Y |  | 夹杂物等级上限值 | DB注释(中文) |
| 116 | MGRPHY_DECARBON_GRT_CD | VARCHAR2(1) | Y |  | 脱碳层保证代号 | DB注释(中文) |
| 117 | MGRPHY_DECARBON_MAX | NUMBER | Y |  | 脱碳层上限值 | DB注释(中文) |
| 118 | MGRPHY_WILD_STRC_GRT_CD | VARCHAR2(1) | Y |  | 魏氏组织保证代号 | DB注释(中文) |
| 119 | MGRPHY_WILD_STRC_GRD | NUMBER | Y |  | 魏氏组织等级 | DB注释(中文) |
| 120 | MGRPHY_MTLGRP_GRT_CD | VARCHAR2(1) | Y |  | 组织类型保证代号 | DB注释(中文) |
| 121 | MGRPHY_MTLGRP_TY | VARCHAR2(2) | Y |  | 组织类型 | DB注释(中文) |
| 122 | MGRPHY_BAND_STRC_GRT_CD | VARCHAR2(1) | Y |  | 带状组织保证代号 | DB注释(中文) |
| 123 | MGRPHY_BAND_STRC_GRD_MAX | NUMBER | Y |  | 带状组织等级上限值 | DB注释(中文) |
| 124 | NON_METAL_SMP_CND | VARCHAR2(2) | Y |  | 非金属夹杂物测试取样条件 | DB注释(中文) |
| 125 | NON_METAL_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 非金属夹杂物测试长度方向取样位置 | DB注释(中文) |
| 126 | NON_METAL_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 非金属夹杂物测试宽度方向取样位置 | DB注释(中文) |
| 127 | NON_METAL_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 非金属夹杂物测试取样试样方向 | DB注释(中文) |
| 128 | NON_METAL_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 非金属夹杂物测试取样试样号数 | DB注释(中文) |
| 129 | NON_METAL_GRD_KIND_CD | VARCHAR2(2) | Y |  | 非金属夹杂评级图种类代码 | DB注释(中文) |
| 130 | NON_METAL_A_GRT_CD | VARCHAR2(1) | Y |  | 非金属夹杂物A保证代号 | DB注释(中文) |
| 131 | NON_METAL_A_MAX | NUMBER | Y |  | 非金属夹杂物A类上限 | DB注释(中文) |
| 132 | NON_METAL_B_GRT_CD | VARCHAR2(1) | Y |  | 非金属夹杂物B类保证代号 | DB注释(中文) |
| 133 | NON_METAL_B_MAX | NUMBER | Y |  | 非金属夹杂物B类上限 | DB注释(中文) |
| 134 | NON_METAL_C_GRT_CD | VARCHAR2(1) | Y |  | 非金属夹杂物C类保证代号 | DB注释(中文) |
| 135 | NON_METAL_C_MAX | NUMBER | Y |  | 非金属夹杂物C类上限 | DB注释(中文) |
| 136 | NON_METAL_D_GRT_CD | VARCHAR2(1) | Y |  | 非金属夹杂物D类保证代号 | DB注释(中文) |
| 137 | NON_METAL_D_MAX | NUMBER | Y |  | 非金属夹杂物D类上限 | DB注释(中文) |
| 138 | NON_METAL_DS_GRT_CD | VARCHAR2(1) | Y |  | 非金属夹杂物Ds保证代号 | DB注释(中文) |
| 139 | NON_METAL_DS_MAX | NUMBER | Y |  | 非金属夹杂物Ds上限 | DB注释(中文) |
| 140 | NON_METAL_ABCD_GRT_CD | VARCHAR2(1) | Y |  | 非金属夹杂物A+B+C+D保证代号 | DB注释(中文) |
| 141 | NON_METAL_ABCD_MAX | NUMBER | Y |  | 非金属夹杂物A+B+C+D上限 | DB注释(中文) |
| 142 | HIGH_TEMP_TSL_SMP_CND | VARCHAR2(2) | Y |  | 高温拉伸测试取样条件 | DB注释(中文) |
| 143 | HIGH_TEMP_TSL_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 高温拉伸测试长度方向取样位置 | DB注释(中文) |
| 144 | HIGH_TEMP_TSL_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 高温拉伸测试宽度方向取样位置 | DB注释(中文) |
| 145 | HIGH_TEMP_TSL_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 高温拉伸测试取样试样方向 | DB注释(中文) |
| 146 | HIGH_TEMP_TSL_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 高温拉伸测试取样试样号数 | DB注释(中文) |
| 147 | HIGH_TEMP_TSL_TEMP | NUMBER | Y |  | 高温拉伸测试温度 | DB注释(中文) |
| 148 | HIGH_TEMP_TSL_YP_GRT_CD | VARCHAR2(1) | Y |  | 高温拉伸测试屈服强度保证代号 | DB注释(中文) |
| 149 | HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  | 高温拉伸测试屈服强度类型 | DB注释(中文) |
| 150 | HIGH_TEMP_TSL_YP_MIN | NUMBER | Y |  | 高温拉伸测试屈服强度下限值 | DB注释(中文) |
| 151 | HIGH_TEMP_TSL_YP_MAX | NUMBER | Y |  | 高温拉伸测试屈服强度上限值 | DB注释(中文) |
| 152 | HIGH_TEMP_TSL_YP_AIM | NUMBER | Y |  | 高温拉伸测试屈服强度目标值 | DB注释(中文) |
| 153 | HIGH_TEMP_TSL_TS_GRT_CD | VARCHAR2(1) | Y |  | 高温拉伸测试抗拉强度保证代号 | DB注释(中文) |
| 154 | HIGH_TEMP_TSL_TS_MIN | NUMBER | Y |  | 高温拉伸测试抗拉强度下限值 | DB注释(中文) |
| 155 | HIGH_TEMP_TSL_TS_MAX | NUMBER | Y |  | 高温拉伸测试抗拉强度上限值 | DB注释(中文) |
| 156 | HIGH_TEMP_TSL_TS_AIM | NUMBER | Y |  | 高温拉伸测试抗拉强度目标值 | DB注释(中文) |
| 157 | HIGH_TEMP_TSL_EL_GRT_CD | VARCHAR2(1) | Y |  | 高温拉伸测试伸长率保证代号 | DB注释(中文) |
| 158 | HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  | 高温拉伸测试伸长率类型 | DB注释(中文) |
| 159 | HIGH_TEMP_TSL_EL_MIN | NUMBER | Y |  | 高温拉伸测试伸长率下限值 | DB注释(中文) |
| 160 | HIGH_TEMP_TSL_EL_MAX | NUMBER | Y |  | 高温拉伸测试伸长率上限值 | DB注释(中文) |
| 161 | HIGH_TEMP_TSL_EL_AIM | NUMBER | Y |  | 高温拉伸测试伸长率目标值 | DB注释(中文) |
| 162 | HIGH_TEMP_TSL_RA_GRT_CD | VARCHAR2(1) | Y |  | 高温拉伸测试断面收缩率保证代号 | DB注释(中文) |
| 163 | HIGH_TEMP_TSL_RA_MIN | NUMBER | Y |  | 高温拉伸测试断面收缩率下限值 | DB注释(中文) |
| 164 | HIGH_TEMP_TSL_RA_MAX | NUMBER | Y |  | 高温拉伸测试断面收缩率上限值 | DB注释(中文) |
| 165 | HIGH_TEMP_TSL_RA_AIM | NUMBER | Y |  | 高温拉伸测试断面收缩率目标值 | DB注释(中文) |
| 166 | CLEAN_SMP_CND | VARCHAR2(2) | Y |  | 洁净度测试取样条件 | DB注释(中文) |
| 167 | CLEAN_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 洁净度测试长度方向取样位置 | DB注释(中文) |
| 168 | CLEAN_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 洁净度测试宽度方向取样位置 | DB注释(中文) |
| 169 | CLEAN_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 洁净度测试取样试样方向 | DB注释(中文) |
| 170 | CLEAN_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 洁净度测试取样试样号数 | DB注释(中文) |
| 171 | CLEAN1_GRT_CD | VARCHAR2(1) | Y |  | 洁净度测试1保证代号 | DB注释(中文) |
| 172 | CLEAN1_KIND | VARCHAR2(1) | Y |  | 洁净度测试1种类 | DB注释(中文) |
| 173 | CLEAN1_MAX | NUMBER | Y |  | 洁净度测试1上限值 | DB注释(中文) |
| 174 | CLEAN2_GRT_CD | VARCHAR2(1) | Y |  | 洁净度测试2保证代号 | DB注释(中文) |
| 175 | CLEAN2_KIND | VARCHAR2(1) | Y |  | 洁净度测试2种类 | DB注释(中文) |
| 176 | CLEAN2_MAX | NUMBER | Y |  | 洁净度测试2上限值 | DB注释(中文) |
| 177 | CLEAN3_GRT_CD | VARCHAR2(1) | Y |  | 洁净度测试3保证代号 | DB注释(中文) |
| 178 | CLEAN3_KIND | VARCHAR2(1) | Y |  | 洁净度测试3种类 | DB注释(中文) |
| 179 | CLEAN3_MAX | NUMBER | Y |  | 洁净度测试3上限值 | DB注释(中文) |
| 180 | ROUGH_SMP_CND | VARCHAR2(2) | Y |  | 粗糙度测试取样条件 | DB注释(中文) |
| 181 | ROUGH_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 粗糙度测试长度方向取样位置 | DB注释(中文) |
| 182 | ROUGH_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 粗糙度测试宽度方向取样位置 | DB注释(中文) |
| 183 | ROUGH_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 粗糙度测试取样试样方向 | DB注释(中文) |
| 184 | ROUGH_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 粗糙度测试取样试样号数 | DB注释(中文) |
| 185 | ROUGH_KIND | VARCHAR2(1) | Y |  | 粗糙度测试种类 | DB注释(中文) |
| 186 | ROUGH_DIR | VARCHAR2(1) | Y |  | 粗度测试方向 | DB注释(中文) |
| 187 | ROUGH_RA_GRT_CD | VARCHAR2(1) | Y |  | 表面平均粗糙度保证代号(Ra) | DB注释(中文) |
| 188 | ROUGH_RA_MIN | NUMBER | Y |  | 表面平均粗糙度下限值(Ra) | DB注释(中文) |
| 189 | ROUGH_RA_MAX | NUMBER | Y |  | 表面平均粗糙度上限值(Ra) | DB注释(中文) |
| 190 | ROUGH_RA_AIM | NUMBER | Y |  | 表面平均粗糙度目标值(Ra) | DB注释(中文) |
| 191 | ROUGH_RPC_GRT_CD | VARCHAR2(1) | Y |  | 单位长度内峰值保证代号(Rpc) | DB注释(中文) |
| 192 | ROUGH_RPC_MIN | NUMBER | Y |  | 单位长度内峰值个数下限值(Rpc) | DB注释(中文) |
| 193 | ROUGH_RPC_MAX | NUMBER | Y |  | 单位长度内峰值个数上限值(Rpc) | DB注释(中文) |
| 194 | ROUGH_RMAX_GRT_CD | VARCHAR2(1) | Y |  | 表面粗糙度最大值保证代号(Rmax) | DB注释(中文) |
| 195 | ROUGH_RMAX_MIN | NUMBER | Y |  | 表面粗糙度最大值下限值(Rmax) | DB注释(中文) |
| 196 | ROUGH_RMAX_MAX | NUMBER | Y |  | 表面粗糙度最大值上限值(Rmax) | DB注释(中文) |
| 197 | FATIG_SMP_CND | VARCHAR2(2) | Y |  | 疲劳测试取样条件 | DB注释(中文) |
| 198 | FATIG_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 疲劳测试长度方向取样位置 | DB注释(中文) |
| 199 | FATIG_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 疲劳测试宽度方向取样位置 | DB注释(中文) |
| 200 | FATIG_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 疲劳测试取样试样方向 | DB注释(中文) |
| 201 | FATIG_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 疲劳测试取样试样号数 | DB注释(中文) |
| 202 | FATIG_SPCMN_CNT | NUMBER | Y |  | 疲劳测试试样数量 | DB注释(中文) |
| 203 | FATIG_GRT_CD | VARCHAR2(1) | Y |  | 疲劳测试保证代号 | DB注释(中文) |
| 204 | FATIG_TEMP | NUMBER | Y |  | 疲劳测试温度 | DB注释(中文) |
| 205 | FATIG_FREQ | NUMBER | Y |  | 疲劳测试频率 | DB注释(中文) |
| 206 | FATIG_SERV_LIFE | NUMBER | Y |  | 疲劳寿命 | DB注释(中文) |
| 207 | FATIG_CND_STRTH | NUMBER | Y |  | 条件疲劳强度 | DB注释(中文) |
| 208 | COAT_WGT_SMP_CND | VARCHAR2(2) | Y |  | 镀锌层质量测试取样条件 | DB注释(中文) |
| 209 | COAT_WGT_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 镀锌层质量测试长度方向取样位置 | DB注释(中文) |
| 210 | COAT_WGT_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 镀锌层质量测试宽度方向取样位置 | DB注释(中文) |
| 211 | COAT_WGT_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 镀锌层质量测试取样试样方向 | DB注释(中文) |
| 212 | COAT_WGT_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 镀锌层质量测试取样试样号数 | DB注释(中文) |
| 213 | COAT_WGT_SPCMN_CNT | NUMBER | Y |  | 镀锌层质量测试取样数量 | DB注释(中文) |
| 214 | COAT_WGT_GRT_CD | VARCHAR2(1) | Y |  | 镀锌层质量测试保证代号 | DB注释(中文) |
| 215 | TST_COAT_WGT_UPPER_AVG | NUMBER | Y |  | ？？？？量？？上表面？？下限？ | DB注释(中文) |
| 216 | TST_COAT_WGT_LOWER_AVG | NUMBER | Y |  | ？？？？量？？上表面？？上限？ | DB注释(中文) |
| 217 | TST_COAT_WGT_TOT_AVG | NUMBER | Y |  | ？？？？量？？下表面？？下限？ | DB注释(中文) |
| 218 | TST_COAT_WGT_UPPER1_MIN | NUMBER | Y |  | 镀锌层试验上表面1点下限值 | SCO_DATA_DIC(D) |
| 219 | TST_COAT_WGT_LOWER1_MIN | NUMBER | Y |  | 镀锌层试验下表面1点下限值 | SCO_DATA_DIC(D) |
| 220 | TST_COAT_WGT_TOT1_MIN | NUMBER | Y |  | ？？？？量？？？面？？上限？ | DB注释(中文) |
| 221 | PSTREAT_SMP_CND | VARCHAR2(2) | Y |  | 后处理测试取样条件 | DB注释(中文) |
| 222 | PSTREAT_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 后处理测试长度方向取样位置 | DB注释(中文) |
| 223 | PSTREAT_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 后处理测试宽度方向取样位置 | DB注释(中文) |
| 224 | PSTREAT_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 后处理测试取样试样方向 | DB注释(中文) |
| 225 | PSTREAT_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 后处理测试取样试样号数 | DB注释(中文) |
| 226 | PSTREAT_CD | VARCHAR2(3) | Y |  | 后处理方法代码 | DB注释(中文) |
| 227 | PHOSP_ADHE_GRT_CD | VARCHAR2(1) | Y |  | 磷酸盐附着量保证代号 | DB注释(中文) |
| 228 | PHOSP_ADHE_UPPER_MIN | NUMBER | Y |  | 磷酸盐附着量上表面下限值 | DB注释(中文) |
| 229 | PHOSP_ADHE_UPPER_MAX | NUMBER | Y |  | 磷酸盐附着量上表面上限值 | DB注释(中文) |
| 230 | PHOSP_ADHE_LOWER_MIN | NUMBER | Y |  | 磷酸盐附着量下表面下限值 | DB注释(中文) |
| 231 | PHOSP_ADHE_LOWER_MAX | NUMBER | Y |  | 磷酸盐附着量下表面上限值 | DB注释(中文) |
| 232 | CHROMATE_ADHE_GRT_CD | VARCHAR2(1) | Y |  | 铬酸盐捕捉量保证代号 | DB注释(中文) |
| 233 | CHROMATE_ADHE_UPPER_MIN | NUMBER | Y |  | 无铬上表面下限值 | DB注释(中文) |
| 234 | CHROMATE_ADHE_UPPER_MAX | NUMBER | Y |  | 无铬上表面上限值 | DB注释(中文) |
| 235 | CHROMATE_ADHE_LOWER_MIN | NUMBER | Y |  | 无铬下表面下限值 | DB注释(中文) |
| 236 | CHROMATE_ADHE_LOWER_MAX | NUMBER | Y |  | 无铬下表面上限值 | DB注释(中文) |
| 237 | ANTIFNG_WGT_GRT_CD | VARCHAR2(1) | Y |  | 耐指纹膜测试保证代号 | DB注释(中文) |
| 238 | ANTIFNG_WGT_UPPER_MIN | NUMBER | Y |  | 耐指纹膜测试上表面重量下限值 | DB注释(中文) |
| 239 | ANTIFNG_WGT_UPPER_MAX | NUMBER | Y |  | 耐指纹膜测试上表面重量上限值 | DB注释(中文) |
| 240 | ANTIFNG_WGT_LOWER_MIN | NUMBER | Y |  | 耐指纹膜测试下表面重量下限值 | DB注释(中文) |
| 241 | ANTIFNG_WGT_LOWER_MAX | NUMBER | Y |  | 耐指纹膜测试下表面重量上限值 | DB注释(中文) |
| 242 | CHROMFRE_ADHE_GRT_CD | VARCHAR2(1) | Y |  | 无铬附着量保证代号 | DB注释(中文) |
| 243 | CHROMFRE_ADHE_UPPER_MIN | NUMBER | Y |  | 无铬附着量上表面下限值 | DB注释(中文) |
| 244 | CHROMFRE_ADHE_UPPER_MAX | NUMBER | Y |  | 无铬附着量上表面上限值 | DB注释(中文) |
| 245 | CHROMFRE_ADHE_LOWER_MIN | NUMBER | Y |  | 无铬附着量下表面下限值 | DB注释(中文) |
| 246 | CHROMFRE_ADHE_LOWER_MAX | NUMBER | Y |  | 无铬附着量下表面上限值 | DB注释(中文) |
| 247 | OIL_SMP_CND | VARCHAR2(2) | Y |  | 涂油测试取样条件 | DB注释(中文) |
| 248 | OIL_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 涂油测试长度方向取样位置 | DB注释(中文) |
| 249 | OIL_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 涂油测试宽度方向取样位置 | DB注释(中文) |
| 250 | OIL_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 涂油测试取样试样方向 | DB注释(中文) |
| 251 | OIL_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 涂油测试取样试样号数 | DB注释(中文) |
| 252 | OIL_WGT_GRT_CD | VARCHAR2(1) | Y |  | 涂油量保证代号 | DB注释(中文) |
| 253 | OIL_MTH_CD | VARCHAR2(2) | Y |  | 涂油方法代码 | DB注释(中文) |
| 254 | OIL_WGT_MIN | NUMBER | Y |  | 涂油量测试双面涂油量下限值 | DB注释(中文) |
| 255 | OIL_WGT_MAX | NUMBER | Y |  | 涂油量测试双面涂油量上限值 | DB注释(中文) |
| 256 | OIL_WGT_UPPER_MIN | NUMBER | Y |  | 涂油量测试上表面涂油量下限值 | DB注释(中文) |
| 257 | OIL_WGT_UPPER_MAX | NUMBER | Y |  | 涂油量测试上表面涂油量上限值 | DB注释(中文) |
| 258 | OIL_WGT_LOWER_MIN | NUMBER | Y |  | 涂油量测试下表面涂油量下限值 | DB注释(中文) |
| 259 | OIL_WGT_LOWER_MAX | NUMBER | Y |  | 涂油量测试下表面涂油量上限值 | DB注释(中文) |
| 260 | ERICHSEN_SMP_CND | VARCHAR2(2) | Y |  | 杯突测试取样条件 | DB注释(中文) |
| 261 | ERICHSEN_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 杯突测试长度方向取样位置 | DB注释(中文) |
| 262 | ERICHSEN_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 杯突测试宽度方向取样位置 | DB注释(中文) |
| 263 | ERICHSEN_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 杯突测试试样取样方向 | DB注释(中文) |
| 264 | ERICHSEN_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 杯突测试试样尺寸 | DB注释(中文) |
| 265 | ERICHSEN_GRT_CD | VARCHAR2(1) | Y |  | 杯突测试保证代号 | DB注释(中文) |
| 266 | ERICHSEN_MIN | NUMBER | Y |  | 杯突测试下限值 | DB注释(中文) |
| 267 | ERICHSEN_AIM | NUMBER | Y |  | 杯突测试目标值 | DB注释(中文) |
| 268 | WAVIN_SMP_CND | VARCHAR2(2) | Y |  | 波纹度测试取样条件 | DB注释(中文) |
| 269 | WAVIN_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 波纹度测试长度方向取样位置 | DB注释(中文) |
| 270 | WAVIN_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 波纹度测试宽度方向取样位置 | DB注释(中文) |
| 271 | WAVIN_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 波纹度测试取样试样方向 | DB注释(中文) |
| 272 | WAVIN_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 波纹度测试取样试样号数 | DB注释(中文) |
| 273 | WAVIN_WA_GRT_CD | VARCHAR2(1) | Y |  | 波纹度检测保证代号 | DB注释(中文) |
| 274 | WAVIN_TY | VARCHAR2(1) | Y |  | 波纹度测试种类 | DB注释(中文) |
| 275 | WAVIN_WA_MAX | NUMBER | Y |  | 波纹度检测上限值(Wa) | DB注释(中文) |
| 276 | WAVIN_WMAX_MAX | NUMBER | Y |  | 波纹度检测最大值上限值(Wmax) | DB注释(中文) |
| 277 | COAT_ATTH_SMP_CND | VARCHAR2(2) | Y |  | 锌层附着性测试取样条件 | DB注释(中文) |
| 278 | COAT_ATTH_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 锌层附着性测试长度方向取样位置 | DB注释(中文) |
| 279 | COAT_ATTH_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 锌层附着性测试宽度方向取样位置 | DB注释(中文) |
| 280 | COAT_ATTH_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 锌层附着性测试取样试样方向 | DB注释(中文) |
| 281 | COAT_ATTH_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 锌层附着性测试取样试样号数 | DB注释(中文) |
| 282 | COAT_ATTH_CD | VARCHAR2(1) | Y |  | 锌层附着性测试方法 | DB注释(中文) |
| 283 | COAT_ATTH_REFLCT_GRT_CD | VARCHAR2(1) | Y |  | 锌层附着性测试表面光反射浓度保证代号 | DB注释(中文) |
| 284 | COAT_ATTH_UPPER_REFLCT_MIN | NUMBER | Y |  | 锌层附着性测试上表面光反射浓度值下限 | DB注释(中文) |
| 285 | COAT_ATTH_LOWER_REFLCT_MIN | NUMBER | Y |  | 锌层附着性测试下表面光反射浓度值下限 | DB注释(中文) |
| 286 | COAT_ATTH_DEWTH_GRT_CD | VARCHAR2(1) | Y |  | 锌层附着性测试表面锌层脱落宽度保证代号 | DB注释(中文) |
| 287 | COAT_ATTH_DEWTH_MAX | NUMBER | Y |  | 锌层附着性测试表面锌层脱落宽度上限 | DB注释(中文) |
| 288 | COAT_ATTH_DERATIO_GRT_CD | VARCHAR2(1) | Y |  | 锌层附着性测试表面锌层脱落率保证代号 | DB注释(中文) |
| 289 | COAT_ATTH_DERATIO_MAX | NUMBER | Y |  | 锌层附着性测试表面锌层脱落率上限 | DB注释(中文) |
| 290 | SPRBCK_SMP_CND | VARCHAR2(2) | Y |  | 回弹测试取样条件 | DB注释(中文) |
| 291 | SPRBCK_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 回弹测试长度方向取样位置 | DB注释(中文) |
| 292 | SPRBCK_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 回弹测试宽度方向取样位置 | DB注释(中文) |
| 293 | SPRBCK_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 回弹测试取样试样方向 | DB注释(中文) |
| 294 | SPRBCK_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 回弹测试取样试样号数 | DB注释(中文) |
| 295 | SPRBCK_CD | VARCHAR2(1) | Y |  | 回弹测试方法 | DB注释(中文) |
| 296 | SPRBCK_DEGR_GRT_CD | VARCHAR2(1) | Y |  | 回弹角保证代号 | DB注释(中文) |
| 297 | SPRBCK_DEGR_MIN | NUMBER | Y |  | 回弹角下限值 | DB注释(中文) |
| 298 | SPRBCK_DEGR_MAX | NUMBER | Y |  | 回弹角上限值 | DB注释(中文) |
| 299 | SPRBCK_GRT_CD | VARCHAR2(1) | Y |  | 回弹测试保证代号 | DB注释(中文) |
| 300 | SPRBCK_MIN | NUMBER | Y |  | 回弹测试下限值 | DB注释(中文) |
| 301 | SPRBCK_MAX | NUMBER | Y |  | 回弹测试上限值 | DB注释(中文) |
| 302 | SPROC_WEAK_SMP_CND | VARCHAR2(2) | Y |  | 二次加工脆性测试取样条件 | DB注释(中文) |
| 303 | SPROC_WEAK_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 二次加工脆性测试长度方向取样位置 | DB注释(中文) |
| 304 | SPROC_WEAK_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 二次加工脆性测试宽度方向取样位置 | DB注释(中文) |
| 305 | SPROC_WEAK_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 二次加工脆性测试试样取样方向 | DB注释(中文) |
| 306 | SPROC_WEAK_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 二次加工脆性取样试样号数 | DB注释(中文) |
| 307 | SPROC_WEAK_GRT_CD | VARCHAR2(1) | Y |  | 二次加工脆性测试保证代号 | DB注释(中文) |
| 308 | SPROC_WEAK_MIN | NUMBER | Y |  | 二次加工脆性测试最小值 | DB注释(中文) |
| 309 | SPROC_WEAK_AIM | NUMBER | Y |  | 二次加工脆性测试目标值 | DB注释(中文) |
| 310 | BH_SMP_CND | VARCHAR2(2) | Y |  | 烘烤硬化值测试取样条件 | DB注释(中文) |
| 311 | BH_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 烘烤硬化值测试长度方向取样位置 | DB注释(中文) |
| 312 | BH_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 烘烤硬化值测试宽度方向取样位置 | DB注释(中文) |
| 313 | BH_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 烘烤硬化值测试试样取样方向 | DB注释(中文) |
| 314 | BH_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 烘烤硬化值测试试样尺寸 | DB注释(中文) |
| 315 | BH_GRT_CD | VARCHAR2(1) | Y |  | 烘烤硬化值测试保证代号 | DB注释(中文) |
| 316 | BH_MIN | NUMBER | Y |  | 烘烤硬化值测试下限值 | DB注释(中文) |
| 317 | BH_AIM | NUMBER | Y |  | 烘烤硬化值测试目标值 | DB注释(中文) |
| 318 | HPT_SMP_CND | VARCHAR2(2) | Y |  | 氢渗透性测试取样条件 | DB注释(中文) |
| 319 | HPT_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 氢渗透性测试长度方向取样位置 | DB注释(中文) |
| 320 | HPT_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 氢渗透性测试宽度方向取样位置 | DB注释(中文) |
| 321 | HPT_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 氢渗透性测试取样试样方向 | DB注释(中文) |
| 322 | HPT_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 氢渗透性测试取样试样号数 | DB注释(中文) |
| 323 | HPT_SMP_GRT_CD | VARCHAR2(1) | Y |  | 氢渗透性测试保证代号 | DB注释(中文) |
| 324 | HPT_ADMI_TIME_MIN | NUMBER | Y |  | 氢扩散达到稳定所需时间下限值 | DB注释(中文) |
| 325 | SALT_SMP_CND | VARCHAR2(2) | Y |  | 中性盐雾测试取样条件 | DB注释(中文) |
| 326 | SALT_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 中性盐雾测试长度方向取样位置 | DB注释(中文) |
| 327 | SALT_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 中性盐雾测试宽度方向取样位置 | DB注释(中文) |
| 328 | SALT_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 中性盐雾测试取样试样方向 | DB注释(中文) |
| 329 | SALT_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 中性盐雾测试取样试样号数 | DB注释(中文) |
| 330 | SALT_GRD_MIN_GRT_CD | VARCHAR2(1) | Y |  | 中性盐雾测试保证代号 | DB注释(中文) |
| 331 | SALT_GRD10_DEFAR | NUMBER | Y |  | 10级缺陷面积 | DB注释(中文) |
| 332 | SALT_GRD9_DEFAR_MIN | NUMBER | Y |  | 9级缺陷面积下限值 | DB注释(中文) |
| 333 | SALT_GRD9_DEFAR_MAX | NUMBER | Y |  | 9级缺陷面积上限值 | DB注释(中文) |
| 334 | SALT_GRD8_DEFAR_MIN | NUMBER | Y |  | 8级缺陷面积下限值 | DB注释(中文) |
| 335 | SALT_GRD8_DEFAR_MAX | NUMBER | Y |  | 8级缺陷面积上限值 | DB注释(中文) |
| 336 | SALT_GRD7_DEFAR_MIN | NUMBER | Y |  | 7级缺陷面积下限值 | DB注释(中文) |
| 337 | SALT_GRD7_DEFAR_MAX | NUMBER | Y |  | 7级缺陷面积上限值 | DB注释(中文) |
| 338 | SALT_GRD6_DEFAR_MIN | NUMBER | Y |  | 6级缺陷面积下限值 | DB注释(中文) |
| 339 | SALT_GRD6_DEFAR_MAX | NUMBER | Y |  | 6级缺陷面积上限值 | DB注释(中文) |
| 340 | SALT_GRD5_DEFAR_MIN | NUMBER | Y |  | 5级缺陷面积下限值 | DB注释(中文) |
| 341 | SALT_GRD5_DEFAR_MAX | NUMBER | Y |  | 5级缺陷面积上限值 | DB注释(中文) |
| 342 | SALT_GRD4_DEFAR_MIN | NUMBER | Y |  | 4级缺陷面积下限值 | DB注释(中文) |
| 343 | SALT_GRD4_DEFAR_MAX | NUMBER | Y |  | 4级缺陷面积上限值 | DB注释(中文) |
| 344 | SALT_GRD3_DEFAR_MIN | NUMBER | Y |  | 3级缺陷面积下限值 | DB注释(中文) |
| 345 | SALT_GRD3_DEFAR_MAX | NUMBER | Y |  | 3级缺陷面积上限值 | DB注释(中文) |
| 346 | SALT_GRD2_DEFAR_MIN | NUMBER | Y |  | 2级缺陷面积下限值 | DB注释(中文) |
| 347 | SALT_GRD2_DEFAR_MAX | NUMBER | Y |  | 2级缺陷面积上限值 | DB注释(中文) |
| 348 | SALT_GRD1_DEFAR_MIN | NUMBER | Y |  | 1级缺陷面积下限值 | DB注释(中文) |
| 349 | SALT_GRD1_DEFAR_MAX | NUMBER | Y |  | 1级缺陷面积上限值 | DB注释(中文) |
| 350 | SALT_GRD0_DEFAR | NUMBER | Y |  | 0级缺陷面积下限值 | DB注释(中文) |
| 351 | QLT_DSN_GOOD_YN | VARCHAR2(1) | Y |  | 质量设计结束时间 | DB注释(中文) |
| 352 | QLT_REMARKS | VARCHAR2(300) | Y |  | 质量备注 | DB注释(中文) |
| 353 | EXT_HOLE_SMP_CND | VARCHAR2(2) | Y |  | 扩孔测试取样条件 | DB注释(中文) |
| 354 | EXT_HOLE_SMP_LTH_LOC | VARCHAR2(1) | Y |  | 扩孔测试长度方向取样位置 | DB注释(中文) |
| 355 | EXT_HOLE_SMP_WTH_LOC | VARCHAR2(1) | Y |  | 扩孔测试宽度方向取样位置 | DB注释(中文) |
| 356 | EXT_HOLE_SMP_SPCMN_DIR | VARCHAR2(1) | Y |  | 扩孔测试取样试样方向 | DB注释(中文) |
| 357 | EXT_HOLE_SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 扩孔测试取样试样号数 | DB注释(中文) |
| 358 | EXT_HOLE_SPCMN_CNT | NUMBER | Y |  | 扩孔测试试样数量 | DB注释(中文) |
| 359 | EXT_HOLE_RATIO_GRT_CD | VARCHAR2(1) | Y |  | 扩孔测试极限扩孔率保证代号 | DB注释(中文) |
| 360 | EXT_HOLE_RATIO_AVG_MIN | NUMBER | Y |  | 扩孔测试极限扩孔率平均下限值 | DB注释(中文) |
| 361 | EXT_HOLE_RATIO_EACH_MIN | NUMBER | Y |  | 扩孔测试极限扩孔率单个下限值 | DB注释(中文) |
| 362 | EXT_HOLE_RATIO_AVG_AIM | NUMBER | Y |  | 扩孔测试极限扩孔率平均目标值 | DB注释(中文) |
| 363 | MGRPHY_GRNSZ_LEVEL_GRT_CD | VARCHAR2(1) | Y |  |  | 空 |
| 364 | IMPACT_SMP_SZ | VARCHAR2(2) | Y |  | 冲击试样尺寸 | SCO_DATA_DIC(L) |
| 365 | IMPACT_SF_RATIO_IND_AVG | NUMBER | Y |  | 纤维断面率平均值 | SCO_DATA_DIC(L) |
| 366 | TST_COAT_DS_TP_AVG_MAX | NUMBER | Y |  | 双面三点平均上限值 | DB注释(中文) |
| 367 | TST_COAT_DS_TP_AVG_MIN | NUMBER | Y |  | 双面三点平均下限值 | DB注释(中文) |
| 368 | TST_COAT_DS_SP_MAX | NUMBER | Y |  | 双面单点上限值 | DB注释(中文) |
| 369 | TST_COAT_DS_SP_MIN | NUMBER | Y |  | 双面单点下限值 | DB注释(中文) |
| 370 | TST_COAT_SS_SP_MAX | NUMBER | Y |  | 单面单点上限值 | DB注释(中文) |
| 371 | TST_COAT_SS_SP_MIN | NUMBER | Y |  | 单面单点下限值 | DB注释(中文) |
| 372 | TST_COAT_SS_TP_MAX | NUMBER | Y |  | 单面三点平均上限值 | DB注释(中文) |
| 373 | TST_COAT_SS_TP_MIN | NUMBER | Y |  | 单面三点平均下限值 | DB注释(中文) |
| 374 | OIL_LEVEL | VARCHAR2(2) | Y |  | 涂油级别 | DB注释(中文) |
| 375 | ANTRST_OIL_KIND | VARCHAR2(1) | Y |  | 防锈油种类 | DB注释(中文) |
| 376 | BEND_WTH_LOC_KIND | VARCHAR2(1) | Y |  | 弯曲试样宽度 | DB注释(中文) |
| 377 | SALT_GRD_MIN | NUMBER | Y |  | 염무시험하한등급 | SCO_DATA_DIC(D) |
| 378 | COAT_ATTH_GRD_MAX_GRT_CD | VARCHAR2(1) | Y |  | 锌层附着性测试등급상한보증코드 | SCO_DATA_DIC(D) |
| 379 | COAT_ATTH_GRD_MAX | NUMBER | Y |  | 锌层附着性测试등급상한 | SCO_DATA_DIC(D) |
| 380 | C3_WGT_UPPER_MIN | NUMBER | Y |  | 三价铬钝化膜重量上表面下限值 | DB注释(中文) |
| 381 | C3_WGT_UPPER_MAX | NUMBER | Y |  | 三价铬钝化膜重量上表面上限值 | DB注释(中文) |
| 382 | C3_WGT_LOWER_MIN | NUMBER | Y |  | 三价铬钝化膜重量下表面下限值 | DB注释(中文) |
| 383 | C3_WGT_LOWER_MAX | NUMBER | Y |  | 三价铬钝化膜重量下表面上限值 | DB注释(中文) |
| 384 | C6_WGT_UPPER_MIN | NUMBER | Y |  | 六价铬钝化膜重量上表面下限值 | DB注释(中文) |
| 385 | C6_WGT_UPPER_MAX | NUMBER | Y |  | 六价铬钝化膜重量上表面上限值 | DB注释(中文) |
| 386 | C6_WGT_LOWER_MIN | NUMBER | Y |  | 六价铬钝化膜重量下表面下限值 | DB注释(中文) |
| 387 | C6_WGT_LOWER_MAX | NUMBER | Y |  | 六价铬钝化膜重量下表面上限值 | DB注释(中文) |
| 388 | AF3_WGT_UPPER_MIN | NUMBER | Y |  | 有铬耐指纹钝化膜重量上表面下限值 | DB注释(中文) |
| 389 | AF3_WGT_UPPER_MAX | NUMBER | Y |  | 有铬耐指纹钝化膜重量上表面上限值 | DB注释(中文) |
| 390 | AF3_WGT_LOWER_MIN | NUMBER | Y |  | 有铬耐指纹钝化膜重量下表面下限值 | DB注释(中文) |
| 391 | AF3_WGT_LOWER_MAX | NUMBER | Y |  | 有铬耐指纹钝化膜重量下表面上限值 | DB注释(中文) |
| 392 | SL6_WGT_UPPER_MIN | NUMBER | Y |  | 自润滑膜重量上表面下限值 | DB注释(中文) |
| 393 | SL6_WGT_UPPER_MAX | NUMBER | Y |  | 自润滑膜重量上表面上限值 | DB注释(中文) |
| 394 | SL6_WGT_LOWER_MIN | NUMBER | Y |  | 自润滑膜重量下表面下限值 | DB注释(中文) |
| 395 | SL6_WGT_LOWER_MAX | NUMBER | Y |  | 自润滑膜重量下表面上限值 | DB注释(中文) |
| 396 | HCR_WGT_UPPER_MIN | NUMBER | Y |  | 高耐蚀膜重量上表面下限值 | DB注释(中文) |
| 397 | HCR_WGT_UPPER_MAX | NUMBER | Y |  | 高耐蚀膜重量上表面上限值 | DB注释(中文) |
| 398 | HCR_WGT_LOWER_MIN | NUMBER | Y |  | 高耐蚀膜重量下表面下限值 | DB注释(中文) |
| 399 | HCR_WGT_LOWER_MAX | NUMBER | Y |  | 高耐蚀膜重量下表面上限值 | DB注释(中文) |
| 400 | HSL_WGT_UPPER_MIN | NUMBER | Y |  | 高润滑膜重量上表面下限值 | DB注释(中文) |
| 401 | HSL_WGT_UPPER_MAX | NUMBER | Y |  | 高润滑膜重量上表面上限值 | DB注释(中文) |
| 402 | HSL_WGT_LOWER_MIN | NUMBER | Y |  | 高润滑膜重量下表面下限值 | DB注释(中文) |
| 403 | HSL_WGT_LOWER_MAX | NUMBER | Y |  | 高润滑膜重量下表面上限值 | DB注释(中文) |
| 404 | PHOSP_GRT_CD | VARCHAR2(1) | Y |  | 磷化膜保证代号 | DB注释(中文) |
| 405 | CHROMATE_GRT_CD | VARCHAR2(1) | Y |  | 无铬钝化保证代号 | DB注释(中文) |
| 406 | ANTIFNG_GRT_CD | VARCHAR2(1) | Y |  | 无铬耐指纹保证代号 | DB注释(中文) |
| 407 | CHROMFRE_GRT_CD | VARCHAR2(1) | Y |  | 无铬自润滑保证代号 | DB注释(中文) |
| 408 | C3_WGT_GRT_CD | VARCHAR2(1) | Y |  | 三价铬保证代号 | DB注释(中文) |
| 409 | C6_WGT_GRT_CD | VARCHAR2(1) | Y |  | 六价铬保证代号 | DB注释(中文) |
| 410 | AF3_WGT_GRT_CD | VARCHAR2(1) | Y |  | 有铬耐指纹保证代号 | DB注释(中文) |
| 411 | SL6_WGT_GRT_CD | VARCHAR2(1) | Y |  | 自润滑保证代号 | DB注释(中文) |
| 412 | HCR_WGT_GRT_CD | VARCHAR2(1) | Y |  | 高耐蚀保证代号 | DB注释(中文) |
| 413 | HSL_WGT_GRT_CD | VARCHAR2(1) | Y |  | 高润滑保证代号 | DB注释(中文) |
| 414 | ORD_COAT_WGT_CD | VARCHAR2(7) | Y |  | 订单镀锌量代码 | DB注释(中文) |
| 415 | NATL_SPEC_ORG_CD | VARCHAR2(5) | Y |  | 国家标准机关简称 | DB注释(中文) |
| 416 | NATL_SPEC_UPPER_COAT_CD | VARCHAR2(7) | Y |  | 国家标准上表面镀锌量代码 | DB注释(中文) |
| 417 | NATL_SPEC_LOWER_COAT_CD | VARCHAR2(7) | Y |  | 国家标准下表面镀锌量代码 | DB注释(中文) |
| 418 | WORK_COAT_WGT_UPPER_AIM | NUMBER | Y |  | 作业镀锌量上表面目标值 | DB注释(中文) |
| 419 | WORK_COAT_WGT_LOWER_AIM | NUMBER | Y |  | 作业镀锌量下表面目标值 | DB注释(中文) |
| 420 | ROUGH_CD | VARCHAR2(2) | Y |  | 粗糙度代码 | DB注释(中文) |

### SQM_SMP_LOTFORM_RSLT_HIST

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=22｜被读 20 过程 / 被写 1 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：254386　**主键**：INST_MTRL_NO、SEQ_NO　**语义覆盖**：43/43

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | Last Updated Time | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | INST_MTRL_NO | VARCHAR2(20) | N | ✓ | 指示材料编号 | DB注释(中文) |
| 9 | SEQ_NO | NUMBER | N | ✓ | 序号 | DB注释(中文) |
| 10 | SMP_NO | VARCHAR2(14) | Y |  | 试样编号 | DB注释(中文) |
| 11 | PROD_GRP | VARCHAR2(2) | Y |  | 品种代码 | DB注释(中文) |
| 12 | SMP_TP | VARCHAR2(1) | Y |  | 试样分类 | DB注释(中文) |
| 13 | SMP_LOT_SEQ | NUMBER | Y |  | 试样Lot序列号 | DB注释(中文) |
| 14 | PROD_JDG_PROD_CD | VARCHAR2(1) | Y |  | 产品判定用产品分类 | DB注释(中文) |
| 15 | REP_YN | VARCHAR2(1) | Y |  | 是否代表 | DB注释(中文) |
| 16 | ORD_NO | VARCHAR2(10) | Y |  | 订单编号 | DB注释(中文) |
| 17 | ORD_LN | VARCHAR2(3) | Y |  | 订单行号 | DB注释(中文) |
| 18 | SPEC_CD | VARCHAR2(50) | Y |  | 国家标准牌号 | DB注释(中文) |
| 19 | CUST_QCERT_NO | VARCHAR2(15) | Y |  | 客户保证编号 | DB注释(中文) |
| 20 | PLAN_HEAT_NO | VARCHAR2(10) | Y |  | 预期Heat编号 | DB注释(中文) |
| 21 | HEAT_NO | VARCHAR2(10) | Y |  | Heat编号 | DB注释(中文) |
| 22 | PLAN_SLAB_NO | VARCHAR2(13) | Y |  | 预期Slab编号 | DB注释(中文) |
| 23 | SLAB_NO | VARCHAR2(13) | Y |  | Slab编号 | DB注释(中文) |
| 24 | MTRL_NO | VARCHAR2(20) | Y |  | 材料编号 | DB注释(中文) |
| 25 | SMP_PROG_CD | VARCHAR2(1) | Y |  | 试样进度代码 | DB注释(中文) |
| 26 | INSP_AGENCY_CD | VARCHAR2(3) | Y |  | 检查机构代码 | DB注释(中文) |
| 27 | CMP_QCERT_NO | VARCHAR2(11) | Y |  | 公司保证编号(材质记号) | DB注释(中文) |
| 28 | MATR_THK | NUMBER | Y |  | 基材厚度 | DB注释(中文) |
| 29 | ORD_THK | NUMBER | Y |  | 订单厚度 | DB注释(中文) |
| 30 | SMP_CND | VARCHAR2(2) | Y |  | 物性测试取样条件 | DB注释(中文) |
| 31 | SMP_LTH_LOC | VARCHAR2(1) | Y |  | 物性测试长度方向取样位置 | DB注释(中文) |
| 32 | SMP_WTH_LOC | VARCHAR2(1) | Y |  | 物性测试宽度方向取样位置 | DB注释(中文) |
| 33 | SMP_SPCMN_SZ | VARCHAR2(2) | Y |  | 物性测试取样试样号数 | DB注释(中文) |
| 34 | SPCMN_CNT | NUMBER | Y |  | 试样数量 | DB注释(中文) |
| 35 | SMP_LOT_INFO_GRP | VARCHAR2(60) | Y |  | 编制组批试样信息捆绑 | DB注释(中文) |
| 36 | SMP_LOT_THK_GRP_CD | VARCHAR2(2) | Y |  | 试样Lot厚度组代码 | DB注释(中文) |
| 37 | TEST_ACC_MAX_WGT | NUMBER | Y |  | 试验累计最大重量 | DB注释(中文) |
| 38 | TEST_ACC_WGT | NUMBER | Y |  | 试验累计重量 | DB注释(中文) |
| 39 | LOT_WGT | NUMBER | Y |  | LOT重量(材料重量) | DB注释(中文) |
| 40 | MECH_TEST_END_YN | VARCHAR2(1) | Y |  | 材质试验是否结束 | DB注释(中文) |
| 41 | ACC_SMP_EXIST_YN | VARCHAR2(1) | Y |  | 累计试样是否存在 | DB注释(中文) |
| 42 | LOT_NO | VARCHAR2(14) | Y |  | LOT NO(BATCH NO) | DB注释(非中文) |
| 43 | TEST_ACC_COIL_CNT | VARCHAR2(2) | Y |  | Test ACC Coil Count | DB注释(非中文) |

### SQM_ORD_PROS_CRM

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=21｜被读 17 过程 / 被写 2 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：0　**主键**：ORD_NO、ORD_LN　**语义覆盖**：156/165

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 修改人 | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | 修改时间 | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | ORD_NO | VARCHAR2(10) | N | ✓ | 订单编号 | DB注释(中文) |
| 9 | ORD_LN | VARCHAR2(3) | N | ✓ | 订单行号 | DB注释(中文) |
| 10 | CRL_MFC_STD_NO | VARCHAR2(11) | N |  | 冷轧制造标准编号 | DB注释(中文) |
| 11 | CRL_ANN_GRD_CD | VARCHAR2(3) | Y |  | 冷轧退火Grade代码 | DB注释(中文) |
| 12 | QA_CRL_STLGRD_TY | VARCHAR2(3) | Y |  | 质量冷轧钢种分类 | DB注释(中文) |
| 13 | PCM_ROLL_FORCE | NUMBER | Y |  | 总压下率 | DB注释(中文) |
| 14 | PCM_ROLL_FORCE_MIN | NUMBER | Y |  | 总压下率下限值 | DB注释(中文) |
| 15 | PCM_ROLL_FORCE_MAX | NUMBER | Y |  | 总压下率上限值 | DB注释(中文) |
| 16 | PCM_PICKL_TEMP | NUMBER | Y |  | 酸洗温度 | DB注释(中文) |
| 17 | PCM_PICKL_TEMP_MIN | NUMBER | Y |  | 酸洗温度下限值 | DB注释(中文) |
| 18 | PCM_PICKL_TEMP_MAX | NUMBER | Y |  | 酸洗温度上限值 | DB注释(中文) |
| 19 | CRL_BOSH1_PICKL_CNTR_AIM | NUMBER | Y |  | 1#酸槽的酸液浓度 | DB注释(中文) |
| 20 | CRL_BOSH1_PICKL_CNTR_MIN | NUMBER | Y |  | 1#酸槽的酸液浓度下限值 | DB注释(中文) |
| 21 | CRL_BOSH1_PICKL_CNTR_MAX | NUMBER | Y |  | 1#酸槽的酸液浓度上限值 | DB注释(中文) |
| 22 | CRL_BOSH3_PICKL_CNTR_AIM | NUMBER | Y |  | 3#酸槽的酸液浓度 | DB注释(中文) |
| 23 | CRL_BOSH3_PICKL_CNTR_MIN | NUMBER | Y |  | 3#酸槽的酸液浓度下限值 | DB注释(中文) |
| 24 | CRL_BOSH3_PICKL_CNTR_MAX | NUMBER | Y |  | 3#酸槽的酸液浓度上限值 | DB注释(中文) |
| 25 | PCM_CL_CNTR | NUMBER | Y |  | Cl-浓度上限值 | DB注释(中文) |
| 26 | PCM_RINS_TANK_CNTR | NUMBER | Y |  | 漂洗水槽电导率 | DB注释(中文) |
| 27 | CAL1_HEAT_CYCLE_CD | VARCHAR2(10) | Y |  | 加热循环代码 | DB注释(中文) |
| 28 | CAL1_SPM_USE_TY | VARCHAR2(1) | Y |  | 有无使用SPM | DB注释(中文) |
| 29 | CAL1_SPM_EL | NUMBER | Y |  | SPM延伸率 | DB注释(中文) |
| 30 | CAL1_ROLL_FORCE | NUMBER | Y |  | SPM轧制力 | DB注释(中文) |
| 31 | CAL1_SRFC_RFLT_RT | NUMBER | Y |  | 带钢表面反射率 | DB注释(中文) |
| 32 | CAL2_HEAT_CYCLE_CD | VARCHAR2(10) | Y |  | 加热循环代码 | DB注释(中文) |
| 33 | CAL2_SPM_USE_TY | VARCHAR2(1) | Y |  | 有无使用SPM | DB注释(中文) |
| 34 | CAL2_SPM_EL | NUMBER | Y |  | SPM延伸率 | DB注释(中文) |
| 35 | CAL2_ROLL_FORCE | NUMBER | Y |  | SPM轧制力 | DB注释(中文) |
| 36 | CAL2_SRFC_RFLT_RT | NUMBER | Y |  | 带钢表面反射率 | DB注释(中文) |
| 37 | CGL_HEAT_CYCLE_CD | VARCHAR2(10) | Y |  | 热循环代码 | DB注释(中文) |
| 38 | CGL_SPM_USE_TY | VARCHAR2(1) | Y |  | 有无使用SPM | DB注释(中文) |
| 39 | CGL_SPM_EL | NUMBER | Y |  | SPM延伸率 | DB注释(中文) |
| 40 | CGL_TL_USE_TY | VARCHAR2(1) | Y |  | 有无使用Tension Leveller拉矫机 | DB注释(中文) |
| 41 | CGL_TL_EL | NUMBER | Y |  | 拉矫延伸率 | DB注释(中文) |
| 42 | CGL_SRFC_RFLT_RT | NUMBER | Y |  | 带钢表面反射率 | DB注释(中文) |
| 43 | CRL_YP_AIM | NUMBER | Y |  | 屈服点 | DB注释(中文) |
| 44 | CRL_TS_AIM | NUMBER | Y |  | 抗拉强度 | DB注释(中文) |
| 45 | CRL_DSN_EDGE_PICKLE | VARCHAR2(1) | Y |  | 冷轧设计切边(酸洗) | DB注释(中文) |
| 46 | CRL_DSN_EDGE_REFINE | VARCHAR2(1) | Y |  | 冷轧设计切边(精整) | DB注释(中文) |
| 47 | CRL_PROD_AIM_WTH | NUMBER | Y |  | 冷轧产目标度 | DB注释(中文) |
| 48 | CRL_COAT_EXT_DSN_WTH | NUMBER | Y |  | 冷轧镀锌出侧设计宽度 | DB注释(中文) |
| 49 | CRL_ANNL1_EXT_DSN_WTH | NUMBER | Y |  | 冷轧退火1出侧设计宽度 | DB注释(中文) |
| 50 | CRL_ANNL2_EXT_DSN_WTH | NUMBER | Y |  | 冷轧退火2出侧设计宽度 | DB注释(中文) |
| 51 | CRL_ROLL1_EXT_DSN_WTH | NUMBER | Y |  | 冷轧轧钢1出侧设计宽度 | DB注释(中文) |
| 52 | CRL_ROLL2_EXT_DSN_WTH | NUMBER | Y |  | 冷轧轧钢2出侧设计宽度 | DB注释(中文) |
| 53 | CRL_PICKL1_EXT_DSN_WTH | NUMBER | Y |  | 冷轧酸洗1出侧设计宽度 | DB注释(中文) |
| 54 | CRL_PICKL2_EXT_DSN_WTH | NUMBER | Y |  | 冷轧酸洗2出侧设计宽度 | DB注释(中文) |
| 55 | CRL_PICKL1_ENT_DSN_WTH | NUMBER | Y |  | 冷轧酸洗1入侧设计宽度 | DB注释(中文) |
| 56 | CRL_PICKL2_ENT_DSN_WTH | NUMBER | Y |  | 冷轧酸洗2入侧设计宽度 | DB注释(中文) |
| 57 | CRL_PPL_ENT_DSN_WTH | NUMBER | Y |  | 冷轧PPL入侧设计宽度 | DB注释(中文) |
| 58 | CRL_HCOIL_DSN_WTH | NUMBER | Y |  | 热轧基材设计宽度 | DB注释(中文) |
| 59 | CRL_PROD_WTH_RNG_MIN | NUMBER | Y |  | 冷轧产品宽度范围下限 | DB注释(中文) |
| 60 | CRL_PROD_WTH_RNG_MAX | NUMBER | Y |  | 冷轧产品宽度范围上限 | DB注释(中文) |
| 61 | CRL_COAT_EXT_DSN_WTH_MIN | NUMBER | Y |  | 冷轧镀锌出侧设计宽度下限 | DB注释(中文) |
| 62 | CRL_COAT_EXT_DSN_WTH_MAX | NUMBER | Y |  | 冷轧镀锌出侧设计宽度上限 | DB注释(中文) |
| 63 | CRL_ANNL1_EXT_DSN_WTH_MIN | NUMBER | Y |  | 冷轧退火1出侧设计宽度下限 | DB注释(中文) |
| 64 | CRL_ANNL1_EXT_DSN_WTH_MAX | NUMBER | Y |  | 冷轧退火1出侧设计宽度上限 | DB注释(中文) |
| 65 | CRL_ANNL2_EXT_DSN_WTH_MIN | NUMBER | Y |  | 冷轧退火2出侧设计宽度下限 | DB注释(中文) |
| 66 | CRL_ANNL2_EXT_DSN_WTH_MAX | NUMBER | Y |  | 冷轧退火2出侧设计宽度上限 | DB注释(中文) |
| 67 | CRL_ROLL1_EXT_DSN_WTH_MIN | NUMBER | Y |  | 冷轧轧钢1出侧设计宽度下限 | DB注释(中文) |
| 68 | CRL_ROLL1_EXT_DSN_WTH_MAX | NUMBER | Y |  | 冷轧轧钢1出侧设计宽度上限 | DB注释(中文) |
| 69 | CRL_ROLL2_EXT_DSN_WTH_MIN | NUMBER | Y |  | 冷轧轧钢2出侧设计宽度下限 | DB注释(中文) |
| 70 | CRL_ROLL2_EXT_DSN_WTH_MAX | NUMBER | Y |  | 冷轧轧钢2出侧设计宽度上限 | DB注释(中文) |
| 71 | CRL_PICKL1_EXT_DSN_WTH_MIN | NUMBER | Y |  | 冷轧酸洗1出侧设计宽度下限 | DB注释(中文) |
| 72 | CRL_PICKL1_EXT_DSN_WTH_MAX | NUMBER | Y |  | 冷轧酸洗1出侧设计宽度上限 | DB注释(中文) |
| 73 | CRL_PICKL2_EXT_DSN_WTH_MIN | NUMBER | Y |  | 冷轧酸洗2出侧设计宽度下限 | DB注释(中文) |
| 74 | CRL_PICKL2_EXT_DSN_WTH_MAX | NUMBER | Y |  | 冷轧酸洗2出侧设计宽度上限 | DB注释(中文) |
| 75 | CRL_PICKL1_ENT_DSN_WTH_MIN | NUMBER | Y |  | 冷轧酸洗1入侧设计宽度下限 | DB注释(中文) |
| 76 | CRL_PICKL1_ENT_DSN_WTH_MAX | NUMBER | Y |  | 冷轧酸洗1入侧设计宽度上限 | DB注释(中文) |
| 77 | CRL_PICKL2_ENT_DSN_WTH_MIN | NUMBER | Y |  | 冷轧酸洗2入侧设计宽度下限 | DB注释(中文) |
| 78 | CRL_PICKL2_ENT_DSN_WTH_MAX | NUMBER | Y |  | 冷轧酸洗2入侧设计宽度上限 | DB注释(中文) |
| 79 | CRL_PPL_ENT_DSN_WTH_MIN | NUMBER | Y |  | 冷轧PPL入侧设计宽度下限 | DB注释(中文) |
| 80 | CRL_PPL_ENT_DSN_WTH_MAX | NUMBER | Y |  | 冷轧PPL入侧设计宽度上限 | DB注释(中文) |
| 81 | CRL_PROD_AIM_THK | NUMBER | Y |  | 冷轧产品目标厚度 | DB注释(中文) |
| 82 | CRL_RFN1_ENT_DSN_THK | NUMBER | Y |  | 冷轧精整1入侧设计厚度 | DB注释(中文) |
| 83 | CRL_RFN2_ENT_DSN_THK | NUMBER | Y |  | 冷轧精整2入侧设计厚度 | DB注释(中文) |
| 84 | CRL_COAT_ENT_DSN_THK | NUMBER | Y |  | 冷轧镀锌入侧设计厚度 | DB注释(中文) |
| 85 | CRL_ANNL1_ENT_DSN_THK | NUMBER | Y |  | 冷轧退火1入侧设计厚度 | DB注释(中文) |
| 86 | CRL_ANNL2_ENT_DSN_THK | NUMBER | Y |  | 冷轧退火2入侧设计厚度 | DB注释(中文) |
| 87 | CRL_ROLL1_DSN_SET_THK | NUMBER | Y |  | 冷轧1厚度Set | DB注释(中文) |
| 88 | CRL_ROLL2_DSN_SET_THK | NUMBER | Y |  | 冷轧2厚度Set | DB注释(中文) |
| 89 | CRL_PICKL1_ENT_DSN_THK | NUMBER | Y |  | 冷轧酸洗1入侧厚度 | DB注释(中文) |
| 90 | CRL_PICKL2_ENT_DSN_THK | NUMBER | Y |  | 冷轧酸洗2入侧厚度 | DB注释(中文) |
| 91 | CRL_HCOIL_DSN_THK | NUMBER | Y |  | 热轧基材设计厚度 | DB注释(中文) |
| 92 | CRL_PROD_THK_RNG_MIN | NUMBER | Y |  | 冷轧产品厚度范围下限 | DB注释(中文) |
| 93 | CRL_PROD_THK_RNG_MAX | NUMBER | Y |  | 冷轧产品厚度范围上限 | DB注释(中文) |
| 94 | CRL_RFN1_ENT_DSN_THK_MIN | NUMBER | Y |  | 冷轧精整1入侧设计厚度下限 | DB注释(中文) |
| 95 | CRL_RFN1_ENT_DSN_THK_MAX | NUMBER | Y |  | 冷轧精整1入侧设计厚度上限 | DB注释(中文) |
| 96 | CRL_RFN2_ENT_DSN_THK_MIN | NUMBER | Y |  | 冷轧精整2入侧设计厚度下限 | DB注释(中文) |
| 97 | CRL_RFN2_ENT_DSN_THK_MAX | NUMBER | Y |  | 冷轧精整2入侧设计厚度上限 | DB注释(中文) |
| 98 | CRL_COAT_ENT_DSN_THK_MIN | NUMBER | Y |  | 冷轧镀锌入侧设计厚度下限 | DB注释(中文) |
| 99 | CRL_COAT_ENT_DSN_THK_MAX | NUMBER | Y |  | 冷轧镀锌入侧设计厚度上限 | DB注释(中文) |
| 100 | CRL_ANNL1_ENT_DSN_THK_MIN | NUMBER | Y |  | 冷轧退火1入侧设计厚度下限 | DB注释(中文) |
| 101 | CRL_ANNL1_ENT_DSN_THK_MAX | NUMBER | Y |  | 冷轧退火1入侧设计厚度上限 | DB注释(中文) |
| 102 | CRL_ANNL2_ENT_DSN_THK_MIN | NUMBER | Y |  | 冷轧退火2入侧设计厚度下限 | DB注释(中文) |
| 103 | CRL_ANNL2_ENT_DSN_THK_MAX | NUMBER | Y |  | 冷轧退火2入侧设计厚度上限 | DB注释(中文) |
| 104 | CRL_PICKL1_ENT_DSN_THK_MIN | NUMBER | Y |  | 冷轧酸洗1入侧设计厚度下限 | DB注释(中文) |
| 105 | CRL_PICKL1_ENT_DSN_THK_MAX | NUMBER | Y |  | 冷轧酸洗1入侧设计厚度上限 | DB注释(中文) |
| 106 | CRL_PICKL2_ENT_DSN_THK_MIN | NUMBER | Y |  | 冷轧酸洗2入侧设计厚度下限 | DB注释(中文) |
| 107 | CRL_PICKL2_ENT_DSN_THK_MAX | NUMBER | Y |  | 冷轧酸洗2入侧设计厚度上限 | DB注释(中文) |
| 108 | CRL_PPL_ENT_DSN_THK_MIN | NUMBER | Y |  | 冷轧PPL入侧设计厚度下限 | DB注释(中文) |
| 109 | CRL_PPL_ENT_DSN_THK_MAX | NUMBER | Y |  | 冷轧PPL入侧设计厚度上限 | DB注释(中文) |
| 110 | CRL_PPL_ENT_DSN_THK | NUMBER | Y |  | 冷轧PPL入侧设计厚度 | DB注释(中文) |
| 111 | UPPER_COAT_WGT_AIM | NUMBER | Y |  | 前面镀锌量目标值 | DB注释(中文) |
| 112 | LOWER_COAT_WGT_AIM | NUMBER | Y |  | 后面镀锌量目标值 | DB注释(中文) |
| 113 | WORK_COAT_UPPER_AIM_THK | NUMBER | Y |  | 作业镀锌上表面目标值厚度 | DB注释(中文) |
| 114 | WORK_COAT_LOWER_AIM_THK | NUMBER | Y |  | 作业镀锌下表面目标值厚度 | DB注释(中文) |
| 115 | PPL_PICKL_TEMP_AIM | NUMBER | Y |  | 酸液温度 | DB注释(中文) |
| 116 | PPL_PICKL_TEMP_MIN | NUMBER | Y |  | 酸液温度下限值 | DB注释(中文) |
| 117 | PPL_PICKL_TEMP_MAX | NUMBER | Y |  | 酸液温度上限值 | DB注释(中文) |
| 118 | PPL_PICKL_CNTR_AIM | NUMBER | Y |  | 酸液浓度 | DB注释(中文) |
| 119 | PPL_PICKL_CNTR_MIN | NUMBER | Y |  | 酸液浓度下限值 | DB注释(中文) |
| 120 | PPL_PICKL_CNTR_MAX | NUMBER | Y |  | 酸液浓度上限值 | DB注释(中文) |
| 121 | PPL_FERROUS_CNTR_AIM | NUMBER | Y |  | 亚铁浓度 | DB注释(中文) |
| 122 | PPL_FERROUS_CNTR_MIN | NUMBER | Y |  | 亚铁浓度下限值 | DB注释(中文) |
| 123 | PPL_FERROUS_CNTR_MAX | NUMBER | Y |  | 亚铁浓度上限值 | DB注释(中文) |
| 124 | PPL_RINS_TANK_CNTR_AIM | NUMBER | Y |  | 漂洗水电导率 | DB注释(中文) |
| 125 | PPL_RINS_TANK_CNTR_MIN | NUMBER | Y |  | 漂洗水电导率下限值 | DB注释(中文) |
| 126 | PPL_RINS_TANK_CNTR_MAX | NUMBER | Y |  | 漂洗水电导率上限值 | DB注释(中文) |
| 127 | PPL_RINS_TANK_PH1_AIM | NUMBER | Y |  | 漂洗水PH值01 | DB注释(中文) |
| 128 | PPL_RINS_TANK_PH1_MIN | NUMBER | Y |  | 漂洗水PH值01下限值 | DB注释(中文) |
| 129 | PPL_RINS_TANK_PH1_MAX | NUMBER | Y |  | 漂洗水PH值01上限值 | DB注释(中文) |
| 130 | PPL_RINS_TANK_PH2_AIM | NUMBER | Y |  | 漂洗水PH值02 | DB注释(中文) |
| 131 | PPL_RINS_TANK_PH2_MIN | NUMBER | Y |  | 漂洗水PH值02下限值 | DB注释(中文) |
| 132 | PPL_RINS_TANK_PH2_MAX | NUMBER | Y |  | 漂洗水PH值02上限值 | DB注释(中文) |
| 133 | PPL_DRY_TEMP_AIM | NUMBER | Y |  | 烘干温度 | DB注释(中文) |
| 134 | PPL_DRY_TEMP_MIN | NUMBER | Y |  | 烘干温度下限值 | DB注释(中文) |
| 135 | PPL_DRY_TEMP_MAX | NUMBER | Y |  | 烘干温度上限值 | DB注释(中文) |
| 136 | OIL_MTH_CD | VARCHAR2(2) | Y |  | 涂油方法代码 | SCO_DATA_DIC(D) |
| 137 | OIL_LEVEL | VARCHAR2(2) | Y |  | 涂油级别 | SCO_DATA_DIC(L) |
| 138 | ANTRST_OIL_KIND | VARCHAR2(1) | Y |  | 防锈油种类 | SCO_DATA_DIC(D) |
| 139 | OIL_WGT_MIN | NUMBER | Y |  | 涂油量测试双面涂油量下限值 | SCO_DATA_DIC(D) |
| 140 | OIL_WGT_MAX | NUMBER | Y |  | 涂油量测试双面涂油量上限值 | SCO_DATA_DIC(D) |
| 141 | OIL_WGT_UPPER_MIN | NUMBER | Y |  | 涂油量测试上表面涂油量下限值 | SCO_DATA_DIC(D) |
| 142 | OIL_WGT_UPPER_MAX | NUMBER | Y |  | 涂油量测试上表面涂油量上限值 | SCO_DATA_DIC(D) |
| 143 | OIL_WGT_LOWER_MIN | NUMBER | Y |  | 涂油量测试下表面涂油量下限值 | SCO_DATA_DIC(D) |
| 144 | OIL_WGT_LOWER_MAX | NUMBER | Y |  | 涂油量测试下表面涂油量上限值 | SCO_DATA_DIC(D) |
| 145 | CRL_DSN_EDGE_CALCGL | VARCHAR2(1) | Y |  | 冷轧设计切边(CAL/CGL) | SCO_DATA_DIC(D) |
| 146 | CRL_RCL1_EXT_DSN_WTH | NUMBER | Y |  |  | 空 |
| 147 | CRL_RCL1_EXT_DSN_WTH_MIN | NUMBER | Y |  |  | 空 |
| 148 | CRL_RCL1_EXT_DSN_WTH_MAX | NUMBER | Y |  |  | 空 |
| 149 | CRL_RCL2_EXT_DSN_WTH | NUMBER | Y |  |  | 空 |
| 150 | CRL_RCL2_EXT_DSN_WTH_MIN | NUMBER | Y |  |  | 空 |
| 151 | CRL_RCL2_EXT_DSN_WTH_MAX | NUMBER | Y |  |  | 空 |
| 152 | CRL_RCL3_EXT_DSN_WTH | NUMBER | Y |  |  | 空 |
| 153 | CRL_RCL3_EXT_DSN_WTH_MIN | NUMBER | Y |  |  | 空 |
| 154 | CRL_RCL3_EXT_DSN_WTH_MAX | NUMBER | Y |  |  | 空 |
| 155 | CAL1_WD_CD | VARCHAR2(10) | Y |  | 连退1焊接代码 | DB注释(中文) |
| 156 | CAL2_WD_CD | VARCHAR2(10) | Y |  | 连退2焊接代码 | DB注释(中文) |
| 157 | CGL_WD_CD | VARCHAR2(10) | Y |  | 镀锌焊接代码 | DB注释(中文) |
| 158 | PPL_SPM_EL | NUMBER | Y |  | 酸洗SPM延伸率 | DB注释(中文) |
| 159 | WTH_TRIM_QTY | NUMBER | Y |  | 切边量 | DB注释(中文) |
| 160 | CAL1_PROC_SPEED_MIN | NUMBER | Y |  | 工艺速度下限(CAL1) | DB注释(中文) |
| 161 | CAL1_PROC_SPEED_MAX | NUMBER | Y |  | 工艺速度下限(CAL1) | DB注释(中文) |
| 162 | CAL2_PROC_SPEED_MIN | NUMBER | Y |  | 工艺速度下限(CAL2) | DB注释(中文) |
| 163 | CAL2_PROC_SPEED_MAX | NUMBER | Y |  | 工艺速度下限(CAL2) | DB注释(中文) |
| 164 | CGL_PROC_SPEED_MIN | NUMBER | Y |  | 工艺速度下限(CGL) | DB注释(中文) |
| 165 | CGL_PROC_SPEED_MAX | NUMBER | Y |  | 工艺速度下限(CGL) | DB注释(中文) |

### SCH_HEAT_DESIGN_RESULT

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=21｜被读 9 过程 / 被写 6 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：1　**主键**：HEAT_DGN_MGT_NO　**语义覆盖**：38/45

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID_Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(100) | Y |  | Created Object ID_Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Datetime_Created Datetime | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Updated User ID_Updated User ID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Updated Object ID_Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | Updated Datetime_Updated Datetime | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Archive Flag_Archive Flag | DB注释(非中文) |
| 8 | HEAT_DGN_MGT_NO | VARCHAR2(8) | N | ✓ | 공정계획Heat설계관리번호_Heat设计管理编号 | DB注释(中文) |
| 9 | CAST_DGN_YN | VARCHAR2(1) | Y |  | Cast설계여부_Cast设计与否 | DB注释(中文) |
| 10 | CAST_DGN_MGT_NO | VARCHAR2(6) | Y |  | 공정계획Cast설계관리번호_Cast设计管理编号 | DB注释(中文) |
| 11 | CAST_INNER_HEAT_SEQ | NUMBER | Y |  | Cast내Heat순서_Cast内Heat顺序 | DB注释(中文) |
| 12 | INCMP_STEEL_NO | VARCHAR2(10) | Y |  | 사내강종번호(출강목표)_炼钢内控钢种编号 | DB注释(中文) |
| 13 | SM_2ND_RFN_CD | VARCHAR2(3) | Y |  | 제강2차정련코드_炼钢2次精炼代码 | DB注释(中文) |
| 14 | HEAT_INNER_SLAB_PCS | NUMBER | Y |  | Heat내Slab수_Heat内Slab数 | DB注释(中文) |
| 15 | HEAT_STEEL_WGT | NUMBER | Y |  | Heat용강량_Heat钢水量 | DB注释(中文) |
| 16 | CC_FAC_FL | VARCHAR2(1) | Y |  | Casting Classification_连铸工厂分类 | DB注释(中文) |
| 17 | HR_ROLL_UNIT_CD | VARCHAR2(1) | Y |  | 열연Roll단위코드_热轧Rolll单位代码 | DB注释(中文) |
| 18 | HEAT_STR1_SLAB_WGT | NUMBER | Y |  | Heat내Strand1 Slab편성중량_Heat内Strand1编制量 | DB注释(中文) |
| 19 | HEAT_STR1_ORD_SLAB_WGT | NUMBER | Y |  | Heat내Strand1주문재Slab편성중량_Heat内Strand1订单再次编制量 | DB注释(中文) |
| 20 | HEAT_STR1_FST_SLAB_WTH | NUMBER | Y |  | Heat내Strand1최초Slab폭_Heat内Strand1最初Slab宽度 | DB注释(中文) |
| 21 | HEAT_STR1_END_SLAB_WTH | NUMBER | Y |  | Heat내Strand1최종Slab폭_Heat内Strand1最终Slab宽度 | DB注释(中文) |
| 22 | HEAT_STR1_SLAB_WTH_VAR_FL | VARCHAR2(1) | Y |  | Heat내Strand1 Slab폭가변여부_Heat内Strand1宽度可变与否 | DB注释(中文) |
| 23 | HEAT_STR1_SLAB_TOT_LTH | NUMBER | Y |  | Heat내Strand1 Slab총길이_Heat内Strand1铸坯总长度 | DB注释(中文) |
| 24 | HEAT_STR1_SLAB_TOT_PCS | NUMBER | Y |  | Heat내Strand1 Slab편성총매수_Heat内Strand1编制Slab支数 | DB注释(中文) |
| 25 | HEAT_STR2_SLAB_WGT | NUMBER | Y |  | Heat내Strand2 Slab편성중량_Heat内Strand2编制量 | DB注释(中文) |
| 26 | HEAT_STR2_ORD_SLAB_WGT | NUMBER | Y |  | Heat내Strand2주문재Slab편성중량_Heat内Strand2订单再次编制量 | DB注释(中文) |
| 27 | HEAT_STR2_FST_SLAB_WTH | NUMBER | Y |  | Heat내Strand2최초Slab폭_Heat内Strand2最初Slab宽度 | DB注释(中文) |
| 28 | HEAT_STR2_END_SLAB_WTH | NUMBER | Y |  | Heat내Strand2최종Slab폭_Heat内Strand2最终Slab宽度 | DB注释(中文) |
| 29 | HEAT_STR2_SLAB_WTH_VAR_FL | VARCHAR2(1) | Y |  | Heat내Strand2 Slab폭가변여부_Heat内Strand2宽度可变与否 | DB注释(中文) |
| 30 | HEAT_STR2_SLAB_TOT_LTH | NUMBER | Y |  | Heat내Strand2 Slab총길이_Heat内Strand2铸坯总长度 | DB注释(中文) |
| 31 | HEAT_STR2_SLAB_TOT_PCS | NUMBER | Y |  | Heat내Strand2 Slab편성총매수_Heat内Strand2编制Slab支数 | DB注释(中文) |
| 32 | HEAT_INST_YN | VARCHAR2(1) | Y |  | Heat지시여부_Heat指示与否 | DB注释(中文) |
| 33 | HEAT_HR_COIL_FST_WTH | NUMBER | Y |  | Heat열연Coil최초폭_ | DB注释(非中文) |
| 34 | HEAT_HR_COIL_END_WTH | NUMBER | Y |  | Heat열연Coil최종폭_ | DB注释(非中文) |
| 35 | HEAT_HCR_FL | VARCHAR2(1) | Y |  | Heat내HCR여부_ | DB注释(非中文) |
| 36 | SLAB_DGN_WTH_RNG_MIN | NUMBER | Y |  | SLAB_DGN_WTH_RNG MIN | SCO_DATA_DIC(L) |
| 37 | SLAB_DGN_WTH_RNG_MAX | NUMBER | Y |  |  | 空 |
| 38 | HEAT_DGN_COMP_FL | VARCHAR2(1) | Y |  | Heat Design Completion Flag | SCO_DATA_DIC(D) |
| 39 | HEAT_STR1_WTH_RNG_MIN | NUMBER | Y |  |  | 空 |
| 40 | HEAT_STR1_WTH_RNG_MAX | NUMBER | Y |  |  | 空 |
| 41 | HEAT_STR2_WTH_RNG_MIN | NUMBER | Y |  |  | 空 |
| 42 | HEAT_STR2_WTH_RNG_MAX | NUMBER | Y |  |  | 空 |
| 43 | DGN_MANUAL_FL | VARCHAR2(1) | Y |  |  | 空 |
| 44 | INCMP_STEEL_GRD | VARCHAR2(10) | Y |  |  | 空 |
| 45 | CCM_NO | VARCHAR2(1) | Y |  | Strand번호_铸机 | SCO_DATA_DIC(D) |

### CUX_LES_TEMP_CAR

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=21｜被读 17 过程 / 被写 2 过程｜操作 INSERT/UPDATE
- **行数(克隆库)**：914051　**主键**：（无显式主键）　**语义覆盖**：58/69

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | ID1 | NUMBER | Y |  |  | 空 |
| 2 | CARNO | VARCHAR2(32) | Y |  | 车号 | DB注释(中文) |
| 3 | MOTORCADENAME | VARCHAR2(128) | Y |  | 物流公司 | DB注释(中文) |
| 4 | CARTYPE | VARCHAR2(16) | Y |  | C汽车T火车，I铁水车，皮带P，船运 S | DB注释(中文) |
| 5 | MATCHID | VARCHAR2(32) | Y |  | 验配ID clientID+yymmdd+00000  该验配ID是第一个业务点生成 | DB注释(中文) |
| 6 | MATCHIDB | VARCHAR2(32) | Y |  | 原单号（复磅物流号） | DB注释(中文) |
| 7 | OPERATYPE | VARCHAR2(16) | Y |  | 业务类型(90采购业务;80销售业务;81副产品销售;13铁水;10厂内调拨先皮后毛;12厂内调拨先毛后皮) | DB注释(中文) |
| 8 | ORDERNO | VARCHAR2(128) | Y |  | 订单合同号 | DB注释(中文) |
| 9 | PLANID | VARCHAR2(64) | Y |  | 计划号 | DB注释(中文) |
| 10 | PLANIDB | VARCHAR2(64) | Y |  | 供方计划号\疏港计划号\集港计划号 | DB注释(中文) |
| 11 | TASKCODE | VARCHAR2(128) | Y |  | 调拨业务号 | DB注释(中文) |
| 12 | MATERIALID | NUMBER | Y |  | 物料id | DB注释(中文) |
| 13 | MATERIALCODE | VARCHAR2(128) | Y |  | 物料编码 | DB注释(中文) |
| 14 | MATERIALNAME | VARCHAR2(128) | Y |  | 物料名称 | DB注释(中文) |
| 15 | STEELNO | VARCHAR2(128) | Y |  | 材质\钢种 | DB注释(中文) |
| 16 | SPECNO | VARCHAR2(128) | Y |  | 规格 | DB注释(中文) |
| 17 | LOTNO | VARCHAR2(128) | Y |  | 物料批次 | DB注释(中文) |
| 18 | SOURCEID | NUMBER | Y |  | 供货单位ID（供应商、分厂、客户） | DB注释(中文) |
| 19 | SOURCECODE | VARCHAR2(128) | Y |  | 供货单位编码 | DB注释(中文) |
| 20 | SOURCE | VARCHAR2(128) | Y |  | 供货单位名称 | DB注释(中文) |
| 21 | SOURCEPLACEID | NUMBER | Y |  | 供货地点ID（发站、港口、库房） | DB注释(中文) |
| 22 | SOURCEPLACECODE | VARCHAR2(128) | Y |  | 供货地点编码 | DB注释(中文) |
| 23 | SOURCEPLACE | VARCHAR2(128) | Y |  | 供货地点名称 | DB注释(中文) |
| 24 | SOURCEMEMO | VARCHAR2(128) | Y |  | 供货备注（子公司、库位） | DB注释(中文) |
| 25 | SOURCEOPERACODE | VARCHAR2(128) | Y |  | 供货人编码 | DB注释(中文) |
| 26 | SOURCEOPERANAME | VARCHAR2(128) | Y |  | 供货人名称 | DB注释(中文) |
| 27 | SOURCETIME | DATE | Y |  | 供货时间 | DB注释(中文) |
| 28 | TARGETID | NUMBER | Y |  | 收货库房ID（客户、分厂、供应商） | DB注释(中文) |
| 29 | TARGETCODE | VARCHAR2(128) | Y |  | 收货单位编码 | DB注释(中文) |
| 30 | TARGET | VARCHAR2(128) | Y |  | 收货单位名称 | DB注释(中文) |
| 31 | TARGETPLACEID | NUMBER | Y |  | 收货地点ID（港口、车站、库房） | DB注释(中文) |
| 32 | TARGETPLACECODE | VARCHAR2(128) | Y |  | 收货地点编码 | DB注释(中文) |
| 33 | TARGETPLACE | VARCHAR2(128) | Y |  | 收货地点名称 | DB注释(中文) |
| 34 | TARGETMEMO | VARCHAR2(128) | Y |  | 收货备注（子公司、库位） | DB注释(中文) |
| 35 | TARGETOPERACODE | VARCHAR2(64) | Y |  | 收货人编码 | DB注释(中文) |
| 36 | TARGETOPERANAME | VARCHAR2(64) | Y |  | 收货人名称 | DB注释(中文) |
| 37 | TARGETTIME | DATE | Y |  | 收货时间 | DB注释(中文) |
| 38 | GROSS | NUMBER | Y |  | 毛重 | DB注释(中文) |
| 39 | GROSSTIME | DATE | Y |  |  | 空 |
| 40 | GROSSWEIGHID | VARCHAR2(64) | Y |  | 计毛衡器ID | DB注释(中文) |
| 41 | GROSSWEIGH | VARCHAR2(64) | Y |  | 毛重衡器名称 | DB注释(中文) |
| 42 | TARE | NUMBER | Y |  | 皮重 | DB注释(中文) |
| 43 | TARETIME | DATE | Y |  |  | 空 |
| 44 | TAREWEIGHID | VARCHAR2(64) | Y |  |  | 空 |
| 45 | TAREWEIGH | VARCHAR2(64) | Y |  |  | 空 |
| 46 | DEDUCTION | NUMBER | Y |  | 扣重值1（扣重，小于等于1：百分比，大于1：KG ） | DB注释(中文) |
| 47 | DEDUCTION2 | NUMBER | Y |  | 扣重值2（扣水） | DB注释(中文) |
| 48 | DEDUCTION3 | NUMBER | Y |  | 扣重值3（扣杂） | DB注释(中文) |
| 49 | DEDUCTION4 | NUMBER | Y |  | 扣重值4（扣其它） | DB注释(中文) |
| 50 | DEDUCTIONTIME | DATE | Y |  |  | 空 |
| 51 | SUTTLE | NUMBER | Y |  | 净重 | DB注释(中文) |
| 52 | SUTTLETIME | DATE | Y |  |  | 空 |
| 53 | SUTTLEWEIGHID | VARCHAR2(64) | Y |  |  | 空 |
| 54 | SUTTLEWEIGH | VARCHAR2(64) | Y |  |  | 空 |
| 55 | BATCHCODE | VARCHAR2(64) | Y |  | 质检批号 | DB注释(中文) |
| 56 | BFLAG | NUMBER | Y |  | 收货方式 0 全部收货，1部分收货，2整车退货 | DB注释(中文) |
| 57 | MEMO4 | VARCHAR2(64) | Y |  | 入库是否扣重 0是 1 否 | DB注释(中文) |
| 58 | MEMO12 | VARCHAR2(256) | Y |  | 已使用:1已取样；0未取样 | DB注释(中文) |
| 59 | MEMO14 | VARCHAR2(256) | Y |  | 供方净重时间 | DB注释(中文) |
| 60 | MEMO15 | VARCHAR2(256) | Y |  | 修改次数 | DB注释(中文) |
| 61 | MATERIALFLOW | NUMBER | Y |  | 物资流向：0厂内，1进厂，2出厂 | DB注释(中文) |
| 62 | USERMEMO | VARCHAR2(256) | Y |  | 用户备注,扣杂备注 | DB注释(中文) |
| 63 | SYSMEMO | VARCHAR2(256) | Y |  | 系统备注 | DB注释(中文) |
| 64 | CREATEDATE | DATE | Y |  |  | 空 |
| 65 | VALIDFLAG | NUMBER | Y |  | 标记：1有效，0作废，8完成 | DB注释(中文) |
| 66 | RECORDTYPE | VARCHAR2(64) | Y |  | 装卸方式：录入或选择 | DB注释(中文) |
| 67 | LINK | VARCHAR2(64) | Y |  | 环节T只计皮、G只计毛、TS回皮出净，GS计毛出净、IN进厂、OUT出厂、MK制卡、SP取样、SIN入库、SOUT出库、C检验 | DB注释(中文) |
| 68 | ISUPLOAD | NUMBER | Y |  | 1是已上传 ，0是未上传 | DB注释(中文) |
| 69 | PROCESS_FLAG | VARCHAR2(1) | Y |  |  | 空 |

### SQM_STDB_CHEM

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=21｜被读 13 过程 / 被写 4 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：866　**主键**：QLT_STD_SEQ　**语义覆盖**：25/25

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 修改人 | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated Object ID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | 修改时间 | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 8 | QLT_STD_SEQ | NUMBER | N | ✓ | 质量标准序列号 | DB注释(中文) |
| 9 | SMS_PROD_CHEM_TY | VARCHAR2(1) | N |  | 炼钢产品成分分类 | DB注释(中文) |
| 10 | QLT_DSN_STD_TY | VARCHAR2(1) | N |  | 质量设计标准区分 | DB注释(中文) |
| 11 | PROD_GRP | VARCHAR2(2) | N |  | 品种代码 | DB注释(中文) |
| 12 | QLT_GRT_COM_NO | VARCHAR2(50) | N |  | 质量保证共同编号 | DB注释(中文) |
| 13 | NATL_SPEC_YEAR | VARCHAR2(4) | N |  | 国家标准年度 | DB注释(中文) |
| 14 | THK_GRP_ABOVE | NUMBER | N |  | 厚度下限值(>) | DB注释(中文) |
| 15 | THK_GRP_FEWER | NUMBER | N |  | 厚度上限值(≤) | DB注释(中文) |
| 16 | QLT_CHEM_CD | VARCHAR2(5) | N |  | 质量成分代码 | DB注释(中文) |
| 17 | QLT_CHEM_DISP_FORM | VARCHAR2(10) | Y |  | 质量成分标识 | DB注释(中文) |
| 18 | QLT_CHEM_FOMULA | VARCHAR2(2) | Y |  | 质量成分公式 | DB注释(中文) |
| 19 | QLT_CHEM_MIN | VARCHAR2(20) | Y |  | 质量成分下限值 | DB注释(中文) |
| 20 | QLT_CHEM_MAX | VARCHAR2(20) | Y |  | 质量成分上限值 | DB注释(中文) |
| 21 | QLT_CHEM_AIM | VARCHAR2(20) | Y |  | 质量成分目标值 | DB注释(中文) |
| 22 | QLT_CHEM_GRT_CD | VARCHAR2(1) | Y |  | 质量成分保证代号 | DB注释(中文) |
| 23 | USE_YN | VARCHAR2(1) | Y |  | 是否使用 | DB注释(中文) |
| 24 | QLT_REMARKS | VARCHAR2(300) | Y |  | 质量备注 | DB注释(中文) |
| 25 | MTC_YN | VARCHAR2(1) | Y |  | 是否出具质保书 | DB注释(中文) |

### SIM_ST_MIX_MTRL_USED_HEAD

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=21｜被读 17 过程 / 被写 2 过程｜操作 DELETE/INSERT/MERGE/UPDATE
- **行数(克隆库)**：38　**主键**：DATA_CYCLE、IR_CHE_OP_AC_DTM、PROC_CD　**语义覆盖**：108/108

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | ??UserID_??UserID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | ??ObjectID_??ObjectID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(6) | Y |  | ????_???? | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | ??UserID_??UserID | DB注释(非中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | ??ObjectID_??ObjectID | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(6) | Y |  | ????_???? | DB注释(非中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Archive??_Archive?? | DB注释(非中文) |
| 8 | DATA_CYCLE | VARCHAR2(1) | N | ✓ | ??????_?????? | DB注释(非中文) |
| 9 | IR_CHE_OP_AC_DTM | VARCHAR2(14) | N | ✓ | ??????_?????? | DB注释(非中文) |
| 10 | PROC_CD | VARCHAR2(3) | N | ✓ | ??????_?????? | DB注释(非中文) |
| 11 | CMB_DRY_T_QTY | NUMBER | Y |  | ??Dry??_??Dry?? | DB注释(非中文) |
| 12 | SIN_CMBRM_DRY_USE_QTY | NUMBER | Y |  | ??????Dry??_??????Dry?? | DB注释(非中文) |
| 13 | SIN_CMBRM_WET_USE_QTY | NUMBER | Y |  | ??????Wet??_??????Wet?? | DB注释(非中文) |
| 14 | SIN_ORE_DRY_USE_QTY | NUMBER | Y |  | ?????Dry???_?????Dry??? | DB注释(非中文) |
| 15 | SIN_ORE_WET_USE_QTY | NUMBER | Y |  | ?????Wet???_?????Wet??? | DB注释(非中文) |
| 16 | SIN_SELF_REN_FINE_USE_QTY | NUMBER | Y |  | ?????????_????????? | DB注释(非中文) |
| 17 | SIN_BF_REN_FINE_USE_QTY | NUMBER | Y |  | ?????????_????????? | DB注释(非中文) |
| 18 | SIN_T_REN_FINE_USE_QTY | NUMBER | Y |  | ????????_???????? | DB注释(非中文) |
| 19 | SIN_T_REN_FINE_USE_RATE | NUMBER | Y |  | ????????_???????? | DB注释(非中文) |
| 20 | SIN_FUEL_T_USE_QTY | NUMBER | Y |  | ????????_???????? | DB注释(非中文) |
| 21 | SIN_TP_ORE_USE_QTY | NUMBER | Y |  | ????????_???????? | DB注释(非中文) |
| 22 | SIN_TP_ORE_USE_RATE | NUMBER | Y |  | ????????_???????? | DB注释(非中文) |
| 23 | SIN_ROD_MILL_CRUSH_QTY | NUMBER | Y |  | ??RodMill???_??RodMill??? | DB注释(非中文) |
| 24 | MIXER_ADD_QTY1 | NUMBER | Y |  | Mixer????1_Mixer????1 | DB注释(非中文) |
| 25 | MIXER_ADD_QTY2 | NUMBER | Y |  | Mixer????2_Mixer????2 | DB注释(非中文) |
| 26 | SIN_MIXER_RM_DUR_PRC_QTY | NUMBER | Y |  | ??Mixer????????_??Mixer???????? | DB注释(非中文) |
| 27 | SIN_DRUM_FEEDER_TURN_SPD | NUMBER | Y |  | ??DrumFeeder????_??DrumFeeder???? | DB注释(非中文) |
| 28 | SIN_CH_DEN | NUMBER | Y |  | ???????_??????? | DB注释(非中文) |
| 29 | SIN_UP_ORE_L_AF | NUMBER | Y |  | ????????_???????? | DB注释(非中文) |
| 30 | SIN_THK | NUMBER | Y |  | ??????????_?????????? | DB注释(非中文) |
| 31 | SIN_BLW_FCE_TEMP | NUMBER | Y |  | ??????????_?????????? | DB注释(非中文) |
| 32 | SIN_BLW_FCE_PRS | NUMBER | Y |  | ????????_???????? | DB注释(非中文) |
| 33 | SIN_BLW_FCE_VEFFI_RATE | NUMBER | Y |  | ????????_???????? | DB注释(非中文) |
| 34 | SIN_BLW_FCE_COG_FLOW | NUMBER | Y |  | ?????COG??_?????COG?? | DB注释(非中文) |
| 35 | SIN_BLW_FCE_AIR_TEMP | NUMBER | Y |  | ?????Air??_?????Air?? | DB注释(非中文) |
| 36 | SIN_BLW_FCE_AIR_FLOW | NUMBER | Y |  | ?????Air??_?????Air?? | DB注释(非中文) |
| 37 | SIN_BLW_FCE_COG_PRS | NUMBER | Y |  | ?????COG??_?????COG?? | DB注释(非中文) |
| 38 | SIN_BED_FLU | NUMBER | Y |  | ???Bed???_???Bed??? | DB注释(非中文) |
| 39 | SIN_BLW_IN_STRN_QTY | NUMBER | Y |  | ??????????COG???_??????????COG??? | DB注释(非中文) |
| 40 | SIN_PAL_SPD | NUMBER | Y |  | ???PalletSpeed_???PalletSpeed | DB注释(非中文) |
| 41 | SIN_FLAME_PRG_SPD | NUMBER | Y |  | ?????????_????????? | DB注释(非中文) |
| 42 | SIN_BTP_TEMP | NUMBER | Y |  | ???BTP??_???BTP?? | DB注释(非中文) |
| 43 | SIN_BTP_LOC | NUMBER | Y |  | ???BTP??_???BTP?? | DB注释(非中文) |
| 44 | SIN_DGAS_AVG_TEMP | NUMBER | Y |  | ???Gas????_???Gas???? | DB注释(非中文) |
| 45 | SIN_DGAS_AVG_WIND_QTY | NUMBER | Y |  | ???Gas????_???Gas???? | DB注释(非中文) |
| 46 | SIN_DGAS_DST_DEN | NUMBER | Y |  | ??????Dust??_???????Dust?? | DB注释(非中文) |
| 47 | SIN_DGAS_NOX_DEN | NUMBER | Y |  | ??????NOx??_???????NOx?? | DB注释(非中文) |
| 48 | SIN_DGAS_SOX_DEN | NUMBER | Y |  | ??????SOx??_???????SOx?? | DB注释(非中文) |
| 49 | SIN_DGAS_O2_DEN | NUMBER | Y |  | ??????O2??_???????O2?? | DB注释(非中文) |
| 50 | SIN_MBLW_LEFT_E_FRC | NUMBER | Y |  | ??MainBlowerLeft??_??MainBlowerLeft?? | DB注释(非中文) |
| 51 | SIN_MBLW_RGT_E_FRC | NUMBER | Y |  | ??MainBlowerRight???_??MainBlowerRight?? | DB注释(非中文) |
| 52 | SIN_MBLW_LEFT_TEMP | NUMBER | Y |  | ??MainBlowerLeft??_??MainBlowerLeft?? | DB注释(非中文) |
| 53 | SIN_MBLW_RGT_TEMP | NUMBER | Y |  | ??MainBlowerRight??_??MainBlowerRight?? | DB注释(非中文) |
| 54 | SIN_MBLW_LEFT_PRS | NUMBER | Y |  | ??MainBlowerLeft??_??MainBlowerLeft?? | DB注释(非中文) |
| 55 | SIN_MBLW_RGT_PRS | NUMBER | Y |  | ??MainBlowerRight??_??MainBlowerRight?? | DB注释(非中文) |
| 56 | SIN_MBLW_NEGATIVE_PRS | NUMBER | Y |  | ??MainBlower????_??MainBlower???? | DB注释(非中文) |
| 57 | SIN_ROD_MILL_OP_YN | VARCHAR2(1) | Y |  | ??RodMill????_??RodMill???? | DB注释(非中文) |
| 58 | SIN_OP_YN | VARCHAR2(1) | Y |  | ???????_??????? | DB注释(非中文) |
| 59 | SIN_MAN_BLW_LEFT_OP_YN | VARCHAR2(1) | Y |  | ??MainBlowerLeft????_??MainBlowerLeft???? | DB注释(非中文) |
| 60 | SIN_MAN_BLW_RGT_OP_YN | VARCHAR2(1) | Y |  | ??MainBlowerRight????_??MainBlowerRight???? | DB注释(非中文) |
| 61 | SIN_MIXER_OP_YN1 | VARCHAR2(1) | Y |  | ??Mixer????1_??Mixer????1 | DB注释(非中文) |
| 62 | SIN_MIXER_OP_YN2 | VARCHAR2(1) | Y |  | ??Mixer????2_??Mixer????2 | DB注释(非中文) |
| 63 | SIN_CER_OP_YN | VARCHAR2(1) | Y |  | ??Cooler????_??Cooler???? | DB注释(非中文) |
| 64 | SIN_ORE_DUR_PER_PRD_QTY | NUMBER | Y |  | ?????????_????????? | DB注释(非中文) |
| 65 | SIN_SELF_REN_FINE_OCR_QTY | NUMBER | Y |  | ?????????_????????? | DB注释(非中文) |
| 66 | SIN_SELF_REN_FINE_OCR_RATE | NUMBER | Y |  | ?????????_????????? | DB注释(非中文) |
| 67 | SIN_BF_REN_FINE_OCR_QTY | NUMBER | Y |  | ?????????_????????? | DB注释(非中文) |
| 68 | SIN_BF_REN_FINE_OCR_RATE | NUMBER | Y |  | ?????????_????????? | DB注释(非中文) |
| 69 | SIN_ORE_T_PRD_QTY | NUMBER | Y |  | ???????_??????? | DB注释(非中文) |
| 70 | SIN_ORE_NET_PRD_QTY | NUMBER | Y |  | ???????_??????? | DB注释(非中文) |
| 71 | SIN_ORE_SEAT_RATE | NUMBER | Y |  | ?????_????? | DB注释(非中文) |
| 72 | SIN_CAL_ORE_SEAT_RATE | NUMBER | Y |  | ???????_??????? | DB注释(非中文) |
| 73 | SIN_T_PRD_PRD_S | NUMBER | Y |  | ?????_???_?????_??? | DB注释(非中文) |
| 74 | SIN_T_PRD_PRD_EFF | NUMBER | Y |  | ?????_????_?????_???? | DB注释(非中文) |
| 75 | SIN_WK_DUR | NUMBER | Y |  | ?????_????? | DB注释(非中文) |
| 76 | SIN_DRIVE_DUR | NUMBER | Y |  | ???????_??????? | DB注释(非中文) |
| 77 | SIN_STP_DUR | NUMBER | Y |  | ???????_??????? | DB注释(非中文) |
| 78 | EQP_RGR_RPR_DUR | NUMBER | Y |  | ????????_???????? | DB注释(非中文) |
| 79 | EQP_LARGE_RPR_DUR | NUMBER | Y |  | ???????_??????? | DB注释(非中文) |
| 80 | EQP_INTER_RPR_DUR | NUMBER | Y |  | ???????_??????? | DB注释(非中文) |
| 81 | REPAIR_PLAN_DUR | NUMBER | Y |  | ??????????_?????????? | DB注释(非中文) |
| 82 | SIN_STP_CNT | NUMBER | Y |  | ???????_??????? | DB注释(非中文) |
| 83 | SIN_OP_ARC_RTO | NUMBER | Y |  | ???????_??????? | DB注释(非中文) |
| 84 | SIN_OP_RT | NUMBER | Y |  | ??????_?????? | DB注释(非中文) |
| 85 | SIN_OP_WK_RTO | NUMBER | Y |  | ??????_?????? | DB注释(非中文) |
| 86 | SIN_OP_RTO | NUMBER | Y |  | ??????_?????? | DB注释(非中文) |
| 87 | SIN_T_PRD_CHARACER_CLT_RTO | NUMBER | Y |  | ??????????_?????????? | DB注释(非中文) |
| 88 | SIN_T_PRD_PLS_CLT_RTO | NUMBER | Y |  | ??????????_?????????? | DB注释(非中文) |
| 89 | SIN_NET_PRD_PLS_CLT_RTO | NUMBER | Y |  | ??????????_?????????? | DB注释(非中文) |
| 90 | SIN_T_PRD_SIN_CLT_RTO | NUMBER | Y |  | ??????????_?????????? | DB注释(非中文) |
| 91 | SIN_T_PRD_AND_CLT_RTO | NUMBER | Y |  | ?????????_????????? | DB注释(非中文) |
| 92 | SIN_ORE_YRD_IMPT_QTY | NUMBER | Y |  | ???Yard???_???Yard??? | DB注释(非中文) |
| 93 | SIN_ORE_YRD_TOD_INV_QTY | NUMBER | Y |  | ???Yard?????_???Yard????? | DB注释(非中文) |
| 94 | SIN_TP_ORE_UT_CSUM | NUMBER | Y |  | ??????????_?????????? | DB注释(非中文) |
| 95 | SIN_T_CALORIE_UT_CSUM | NUMBER | Y |  | ????????_???????? | DB注释(非中文) |
| 96 | SIN_COOLER_SU_ORG_AVG_TEMP | NUMBER | Y |  | ??Cooler???????_??Cooler??????? | DB注释(非中文) |
| 97 | SIN_COOLER_SU_ORG_HI_TEMP | NUMBER | Y |  | ??Cooler???????_??Cooler??????? | DB注释(非中文) |
| 98 | SIN_COOLER_OVER_BRG_AVG_TEMP | NUMBER | Y |  | ??CoolerOverBridge????_??CoolerOverBridge???? | DB注释(非中文) |
| 99 | SIN_COOLER_OVER_BRG_HI_TEMP | NUMBER | Y |  | ??CoolerOverBridge????_??CoolerOverBridge???? | DB注释(非中文) |
| 100 | SIN_COOLER_OUT_ORG_AVG_TEMP | NUMBER | Y |  | ??Cooler???????_??Cooler??????? | DB注释(非中文) |
| 101 | SIN_COOLER_OUT_ORG_HI_TEMP | NUMBER | Y |  | ??Cooler???????_??Cooler??????? | DB注释(非中文) |
| 102 | SIN_COOLER_SPD | NUMBER | Y |  | ??CoolerSpeed_??CoolerSpeed | DB注释(非中文) |
| 103 | SIN_COOLER_DUCT_PRS | NUMBER | Y |  | ??CoolerDuct??_??CoolerDuct?? | DB注释(非中文) |
| 104 | SIN_COOLER_FAN_WIND_QTY1 | NUMBER | Y |  | ??CoolerFan??1_??CoolerFan??1 | DB注释(非中文) |
| 105 | SIN_COOLER_FAN_WIND_QTY2 | NUMBER | Y |  | ??CoolerFan??2_??CoolerFan??2 | DB注释(非中文) |
| 106 | SIN_ORE_BOOK_TOD_INV_QTY | NUMBER | Y |  | ??SinterOreBookTodInvQt_??SinterOreBookTodInvQt | DB注释(非中文) |
| 107 | SIN_ROOM_EP_DST_DEN | NUMBER | Y |  | ??RoomEP_Dust??_??RoomEP_Dust?? | DB注释(非中文) |
| 108 | SIN_COLR_B_SOZD_TEMP | NUMBER | Y |  | ???Cooler???????_??Cooler??????? | DB注释(非中文) |

### SIT_TRANS_PROG

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=21｜被读 19 过程 / 被写 1 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：120　**主键**：TRK_SCALE_PLAN_NO　**语义覆盖**：42/42

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | Created User ID | DB注释(非中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(30) | Y |  | Created Object ID | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | Created Time | DB注释(非中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | Last Updated User ID | DB注释(非中文) |
| 5 | UPD_TM | TIMESTAMP(7) | Y |  | Last Updated Time | DB注释(非中文) |
| 6 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Record Archive Flag | DB注释(非中文) |
| 7 | TRK_SCALE_PLAN_NO | VARCHAR2(15) | N | ✓ | ?????? | DB注释(非中文) |
| 8 | TRANS_ORD_DTM | VARCHAR2(14) | Y |  | ?????? | DB注释(非中文) |
| 9 | TRANS_PROG_STS | VARCHAR2(1) | Y |  | ???????? | DB注释(非中文) |
| 10 | TRANS_TY | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 11 | SCALE_LOC | VARCHAR2(1) | Y |  | ???? | DB注释(非中文) |
| 12 | CAR_NO | VARCHAR2(10) | Y |  | ???? | DB注释(非中文) |
| 13 | TRANS_CD | VARCHAR2(15) | Y |  | ???? | DB注释(非中文) |
| 14 | TRANS_NM | VARCHAR2(50) | Y |  | ????? | DB注释(非中文) |
| 15 | MATERIAL_CD | VARCHAR2(18) | Y |  | ???? | DB注释(非中文) |
| 16 | MATERIAL_NM | VARCHAR2(50) | Y |  | ???? | DB注释(非中文) |
| 17 | ORIGIN_CD | VARCHAR2(11) | Y |  | ???? | DB注释(非中文) |
| 18 | ORIGIN_NM | VARCHAR2(50) | Y |  | ????? | DB注释(非中文) |
| 19 | DEST_CD | VARCHAR2(11) | Y |  | ???? | DB注释(非中文) |
| 20 | DEST_NM | VARCHAR2(50) | Y |  | ????? | DB注释(非中文) |
| 21 | DRIVER_NM | VARCHAR2(40) | Y |  | ????? | DB注释(非中文) |
| 22 | DRIVER_TEL_NO | VARCHAR2(20) | Y |  | ??????? | DB注释(非中文) |
| 23 | TRANS_REQ_NO | VARCHAR2(12) | Y |  | ?????? | DB注释(非中文) |
| 24 | CAR_ASSIGN_SEQ | NUMBER | Y |  | ???????? | DB注释(非中文) |
| 25 | CAR_ASSIGN_QTY | NUMBER | Y |  | ????? | DB注释(非中文) |
| 26 | TARE_WGT | NUMBER | Y |  | ?? | DB注释(非中文) |
| 27 | ORD_NO | VARCHAR2(10) | Y |  | ORDER NO | DB注释(非中文) |
| 28 | ORD_ITEM | VARCHAR2(3) | Y |  | ORDER ITEM | DB注释(非中文) |
| 29 | ORD_CLASS_CD | VARCHAR2(2) | Y |  | ORDER ???? | DB注释(非中文) |
| 30 | CUST_CD | VARCHAR2(6) | Y |  | ????? | DB注释(非中文) |
| 31 | CUST_NM | VARCHAR2(50) | Y |  | ???? | DB注释(非中文) |
| 32 | VENDER_CD | VARCHAR2(10) | Y |  | ???? | DB注释(非中文) |
| 33 | CONTRACT_NO | VARCHAR2(10) | Y |  | ???? | DB注释(非中文) |
| 34 | CONTRACT_LINE_NO | NUMBER | Y |  | ??LINE?? | DB注释(非中文) |
| 35 | PO_NO | VARCHAR2(10) | Y |  | Po ?? | DB注释(非中文) |
| 36 | PO_LINE_NO | NUMBER | Y |  | Po Line ?? | DB注释(非中文) |
| 37 | PO_PARTIAL_NUM | NUMBER | Y |  | Po Partial ?? | DB注释(非中文) |
| 38 | SUPPLIER_ITEM | VARCHAR2(15) | Y |  | ?? Item ?? | DB注释(非中文) |
| 39 | ARR_PLAN_DT | VARCHAR2(8) | Y |  | ?????? | DB注释(非中文) |
| 40 | SCALE_DTM | VARCHAR2(14) | Y |  | ???? | DB注释(非中文) |
| 41 | CANCEL_DTM | VARCHAR2(14) | Y |  | ???? | DB注释(非中文) |
| 42 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Last Updated ObjectID | SCO_DATA_DIC(D) |

### SQM_WSP_MTC_MECH_INF_1

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=21｜被读 7 过程 / 被写 7 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：2　**主键**：（无显式主键）　**语义覆盖**：194/201

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | MTC_NO | VARCHAR2(11) | N |  | 质量保证书编号 | SCO_DATA_DIC(D) |
| 2 | MTC_STS | VARCHAR2(1) | N |  |  | 空 |
| 3 | MTC_DTM | VARCHAR2(14) | N |  |  | 空 |
| 4 | SMP_NO | VARCHAR2(14) | N |  | 시편번호 | SCO_DATA_DIC(D) |
| 5 | LOT_NO | VARCHAR2(14) | Y |  | LOT NO(BATCH NO) | SCO_DATA_DIC(D) |
| 6 | TEST_CNT | NUMBER | Y |  | 시험회수 | SCO_DATA_DIC(D) |
| 7 | TSL_YP_RSLT | NUMBER | Y |  | 拉伸测试屈服强度实绩 | SCO_DATA_DIC(D) |
| 8 | TSL_TS_RSLT | NUMBER | Y |  | 拉伸测试抗拉强度实绩 | SCO_DATA_DIC(D) |
| 9 | TSL_EL_RSLT | NUMBER | Y |  | 拉伸测试伸长率实绩 | SCO_DATA_DIC(D) |
| 10 | TSL_YR_RSLT | NUMBER | Y |  | 拉伸测试屈强比实绩 | SCO_DATA_DIC(D) |
| 11 | TSL_RA_RSLT | NUMBER | Y |  | 拉伸测试断面收缩率实绩 | SCO_DATA_DIC(D) |
| 12 | TSL_R_RSLT | NUMBER | Y |  | 拉抻测试塑性应变比r平均实绩 | SCO_DATA_DIC(D) |
| 13 | TSL_R0_RSLT | NUMBER | Y |  | 拉抻测试r0实绩 | SCO_DATA_DIC(D) |
| 14 | TSL_R45_RSLT | NUMBER | Y |  | 拉抻测试r45实绩 | SCO_DATA_DIC(D) |
| 15 | TSL_R90_RSLT | NUMBER | Y |  | 拉抻测试r90实绩 | SCO_DATA_DIC(D) |
| 16 | TSL_N_RSLT | NUMBER | Y |  | 拉伸测试加工硬化指数n平均实绩 | SCO_DATA_DIC(D) |
| 17 | TSL_N0_RSLT | NUMBER | Y |  | 拉抻测试N0实绩 | SCO_DATA_DIC(D) |
| 18 | TSL_N45_RSLT | NUMBER | Y |  | 拉抻测试N45实绩 | SCO_DATA_DIC(D) |
| 19 | TSL_N90_RSLT | NUMBER | Y |  | 拉抻测试N90实绩 | SCO_DATA_DIC(D) |
| 20 | BEND_RSLT | VARCHAR2(1) | Y |  | 弯曲测试实绩 | SCO_DATA_DIC(D) |
| 21 | EXT_HOLE_RATIO_AVG_RSLT | NUMBER | Y |  | 扩孔测试极限扩孔率平均 | SCO_DATA_DIC(D) |
| 22 | IMPACT_AVG_RSLT | NUMBER | Y |  | 冲击试验平均实绩 | SCO_DATA_DIC(D) |
| 23 | IMPACT_IND_RSLT1 | NUMBER | Y |  | 冲击功单个实绩1 | SCO_DATA_DIC(D) |
| 24 | IMPACT_IND_RSLT2 | NUMBER | Y |  | 冲击功单个实绩2 | SCO_DATA_DIC(D) |
| 25 | IMPACT_IND_RSLT3 | NUMBER | Y |  | 冲击功单个实绩3 | SCO_DATA_DIC(D) |
| 26 | IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 冲击测试纤维断面率平均实绩 | SCO_DATA_DIC(D) |
| 27 | IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩1 | SCO_DATA_DIC(D) |
| 28 | IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩2 | SCO_DATA_DIC(D) |
| 29 | IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 冲击测试纤维断面率单个实绩3 | SCO_DATA_DIC(D) |
| 30 | HARD_RSLT | NUMBER | Y |  | 硬度测试实绩 | SCO_DATA_DIC(D) |
| 31 | NON_METAL_A_RSLT | NUMBER | Y |  | 非金属夹杂物A类实绩 | SCO_DATA_DIC(D) |
| 32 | NON_METAL_A1_RSLT | NUMBER | Y |  | 非金属夹杂物A1类实绩 | SCO_DATA_DIC(D) |
| 33 | NON_METAL_B_RSLT | NUMBER | Y |  | 非金属夹杂物B类实绩 | SCO_DATA_DIC(D) |
| 34 | NON_METAL_B1_RSLT | NUMBER | Y |  | 非金属夹杂物B1类实绩 | SCO_DATA_DIC(D) |
| 35 | NON_METAL_C_RSLT | NUMBER | Y |  | 非金属夹杂物C类实绩 | SCO_DATA_DIC(D) |
| 36 | NON_METAL_C1_RSLT | NUMBER | Y |  | 非金属夹杂物C1类实绩 | SCO_DATA_DIC(D) |
| 37 | NON_METAL_D_RSLT | NUMBER | Y |  | 非金属夹杂物D类实绩 | SCO_DATA_DIC(D) |
| 38 | NON_METAL_D1_RSLT | NUMBER | Y |  | 非金属夹杂物D1类实绩 | SCO_DATA_DIC(D) |
| 39 | NON_METAL_DS_RSLT | NUMBER | Y |  | 非金属夹杂物Ds实绩 | SCO_DATA_DIC(D) |
| 40 | NON_METAL_ABCD_RSLT | NUMBER | Y |  | 非金属夹杂物A+B+C+D实绩 | SCO_DATA_DIC(D) |
| 41 | S_PRINT_GRD_RSLT | VARCHAR2(1) | Y |  | 硫印测试等级实绩 | SCO_DATA_DIC(D) |
| 42 | DWTT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | DWTT测试最小剪切面积平均实绩 | SCO_DATA_DIC(D) |
| 43 | DWTT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | DWTT测试最小剪切面积单个实绩1 | SCO_DATA_DIC(D) |
| 44 | DWTT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | DWTT测试最小剪切面积单个实绩2 | SCO_DATA_DIC(D) |
| 45 | HIC_CLR_TOT_AVG_RSLT | NUMBER | Y |  | HIC测试CLR全体平均实绩 | SCO_DATA_DIC(D) |
| 46 | HIC_CSR_TOT_AVG_RSLT | NUMBER | Y |  | HIC测试CSR全体平均实绩 | SCO_DATA_DIC(D) |
| 47 | HIC_CTR_TOT_AVG_RSLT | NUMBER | Y |  | HIC测试CTR全体平均实绩 | SCO_DATA_DIC(D) |
| 48 | HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  | 高温拉伸测试屈服强度实绩 | SCO_DATA_DIC(D) |
| 49 | HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  | 高温拉伸测试抗拉强度实绩 | SCO_DATA_DIC(D) |
| 50 | HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  | 高温拉伸测试伸长率实绩 | SCO_DATA_DIC(D) |
| 51 | HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  | 高温拉伸测试断面收缩率实绩 | SCO_DATA_DIC(D) |
| 52 | BH_RSLT | NUMBER | Y |  | 烘烤硬化值测试实绩 | SCO_DATA_DIC(D) |
| 53 | ERICHSEN_RSLT | NUMBER | Y |  | 杯突测试 | SCO_DATA_DIC(D) |
| 54 | TST_COAT_WGT_UPPER_RSLT | NUMBER | Y |  | 镀锌层质量测试上表面镀层实绩 | SCO_DATA_DIC(D) |
| 55 | TST_COAT_WGT_LOWER_RSLT | NUMBER | Y |  | 镀锌层质量测试下表面镀层实绩 | SCO_DATA_DIC(D) |
| 56 | TST_COAT_WGT_TOT_RSLT | NUMBER | Y |  | 镀锌层质量测试双面镀层实绩 | SCO_DATA_DIC(D) |
| 57 | ROUGH_RA_RSLT | NUMBER | Y |  | 表面平均粗糙度(Ra) | SCO_DATA_DIC(D) |
| 58 | MGRPHY_FGS_RSLT | NUMBER | Y |  | 铁素体晶粒度 | SCO_DATA_DIC(D) |
| 59 | MGRPHY_AGS_RSLT | NUMBER | Y |  | 奥氏体晶粒度 | SCO_DATA_DIC(D) |
| 60 | MGRPHY_INCLD_GRD_MAX_RSLT | NUMBER | Y |  | 夹杂物等级上限实绩 | SCO_DATA_DIC(D) |
| 61 | MGRPHY_DECARBON_MAX_RSLT | NUMBER | Y |  | 脱碳层上限实绩 | SCO_DATA_DIC(D) |
| 62 | MGRPHY_BAND_STRC_GRD_MAX_RSLT | NUMBER | Y |  | 带状组织等级上限实绩 | SCO_DATA_DIC(D) |
| 63 | WAVIN_WA_RSLT | NUMBER | Y |  | 波纹度检测实绩(Wa) | SCO_DATA_DIC(D) |
| 64 | SURFACE_RESIS_RSLT | NUMBER | Y |  | 表面电阻 | SCO_DATA_DIC(D) |
| 65 | ROUGH_RY_RSLT | NUMBER | Y |  | 轮廓最大高度实绩(Ry) | SCO_DATA_DIC(D) |
| 66 | ROUGH_RZ_RSLT | NUMBER | Y |  | 微观不平度十点高度实绩(Rz) | SCO_DATA_DIC(D) |
| 67 | WAVIN_WSA_RSLT | NUMBER | Y |  | 波纹度检测实绩(Wsa) | SCO_DATA_DIC(D) |
| 68 | WAVIN_WSAMAX_RSLT | NUMBER | Y |  | 波纹度检测最大值实绩(Wsamax) | SCO_DATA_DIC(D) |
| 69 | WAVIN_WCA_RSLT | NUMBER | Y |  | 波纹度检测实绩(Wca) | SCO_DATA_DIC(D) |
| 70 | WAVIN_WCAMAX_RSLT | NUMBER | Y |  | 波纹度检测最大值实绩(Wcamax) | SCO_DATA_DIC(D) |
| 71 | WAVIN_WA08_RSLT | NUMBER | Y |  | 波纹度检测实绩(Wa08) | SCO_DATA_DIC(D) |
| 72 | WAVIN_WA08MAX_RSLT | NUMBER | Y |  | 波纹度检测最大值实绩(Wa08max) | SCO_DATA_DIC(D) |
| 73 | ROUGH_RPC_RSLT | NUMBER | Y |  | 单位长度内峰值个数实绩(Rpc) | SCO_DATA_DIC(D) |
| 74 | ROUGH_RMAX_RSLT | NUMBER | Y |  | 表面粗糙度最大值实绩(Rmax) | SCO_DATA_DIC(D) |
| 75 | MGRPHY_GRNSZ_LEVEL | NUMBER | Y |  | 金相测试晶粒度级别 | SCO_DATA_DIC(D) |
| 76 | TSL_YP_TS_RSLT | VARCHAR2(10) | Y |  | 拉伸试验屈强比YP/TS实绩 | SCO_DATA_DIC(D) |
| 77 | TSL_RT05_RM_RSLT | VARCHAR2(10) | Y |  | 拉伸试验屈强比Rt0.5/Rm实绩 | SCO_DATA_DIC(D) |
| 78 | TSL_RT15_RT05_RSLT | VARCHAR2(10) | Y |  | 拉伸试验屈强比Rt1.5/Rt0.5实绩 | SCO_DATA_DIC(D) |
| 79 | TSL_RT20_RT10_RSLT | VARCHAR2(10) | Y |  | 拉伸试验屈强比Rt2.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 80 | TSL_RT50_RT10_RSLT | VARCHAR2(10) | Y |  | 拉伸试验屈强比Rt5.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 81 | TSL_CT_EX_RA_RSLT | VARCHAR2(10) | Y |  | 拉抻测试断后伸长率实绩 | SCO_DATA_DIC(D) |
| 82 | TSL_CT_RA_RSLT | VARCHAR2(10) | Y |  | 拉伸试验均匀伸长率实绩 | SCO_DATA_DIC(D) |
| 83 | IMPACT_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 84 | IMPACT_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试样侧膨胀值单值实绩1 | SCO_DATA_DIC(D) |
| 85 | IMPACT_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试样侧膨胀值单值实绩2 | SCO_DATA_DIC(D) |
| 86 | IMPACT_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试样侧膨胀值单值实绩3 | SCO_DATA_DIC(D) |
| 87 | Z_TSL_CUT_IND_RSLT1 | VARCHAR2(10) | Y |  | Z向拉伸断面收缩率单值实绩1 | SCO_DATA_DIC(D) |
| 88 | Z_TSL_CUT_IND_RSLT2 | VARCHAR2(10) | Y |  | Z向拉伸断面收缩率单值实绩2 | SCO_DATA_DIC(D) |
| 89 | Z_TSL_CUT_IND_RSLT3 | VARCHAR2(10) | Y |  | Z向拉伸断面收缩率单值实绩3 | SCO_DATA_DIC(D) |
| 90 | Z_TSL_CUT_AVG_RSLT | VARCHAR2(10) | Y |  | Z向拉伸断面收缩率平均值实绩 | SCO_DATA_DIC(D) |
| 91 | Z_TSL_YP_RSLT | VARCHAR2(10) | Y |  | Z向拉伸试验屈服强度实绩 | SCO_DATA_DIC(D) |
| 92 | Z_TSL_TS_RSLT | VARCHAR2(10) | Y |  | Z向拉伸试验抗拉强度实绩 | SCO_DATA_DIC(D) |
| 93 | Z_TSL_CT_EX_RA_RSLT | VARCHAR2(10) | Y |  | Z向拉伸试验断后伸长率实绩 | SCO_DATA_DIC(D) |
| 94 | HIGH_TEMP_TSL_TEMP_RSLT | VARCHAR2(10) | Y |  | 高温拉伸测试温度实绩 | SCO_DATA_DIC(D) |
| 95 | DWTT1_SA_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | DWTT1纤维断面率SA平均值实绩 | SCO_DATA_DIC(D) |
| 96 | DWTT1_SA_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | DWTT1纤维断面率SA单值实绩1 | SCO_DATA_DIC(D) |
| 97 | DWTT1_SA_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | DWTT1纤维断面率SA单值实绩2 | SCO_DATA_DIC(D) |
| 98 | DWTT2_SA_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | DWTT2纤维断面率SA平均值实绩 | SCO_DATA_DIC(D) |
| 99 | DWTT2_SA_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | DWTT2纤维断面率SA单值实绩1 | SCO_DATA_DIC(D) |
| 100 | DWTT2_SA_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | DWTT2纤维断面率SA单值实绩2 | SCO_DATA_DIC(D) |
| 101 | DWTT3_SA_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | DWTT3纤维断面率SA平均值实绩 | SCO_DATA_DIC(D) |
| 102 | DWTT3_SA_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | DWTT3纤维断面率SA单值实绩1 | SCO_DATA_DIC(D) |
| 103 | DWTT3_SA_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | DWTT3纤维断面率SA单值实绩2 | SCO_DATA_DIC(D) |
| 104 | DWTT4_SA_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | DWTT4纤维断面率SA平均值实绩 | SCO_DATA_DIC(D) |
| 105 | DWTT4_SA_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | DWTT4纤维断面率SA单值实绩1 | SCO_DATA_DIC(D) |
| 106 | DWTT4_SA_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | DWTT4纤维断面率SA单值实绩2 | SCO_DATA_DIC(D) |
| 107 | DWTT5_SA_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | DWTT5纤维断面率SA平均值实绩 | SCO_DATA_DIC(D) |
| 108 | DWTT5_SA_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | DWTT5纤维断面率SA单值实绩1 | SCO_DATA_DIC(D) |
| 109 | DWTT5_SA_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | DWTT5纤维断面率SA单值实绩2 | SCO_DATA_DIC(D) |
| 110 | SSCC_STRESS_TST_VAL_RSLT | VARCHAR2(10) | Y |  | SSCC测试应力实绩 | SCO_DATA_DIC(D) |
| 111 | HIC_CLR_SPCMN_AVG1_RSLT | VARCHAR2(10) | Y |  | HIC测试CLR试样平均1实绩 | SCO_DATA_DIC(D) |
| 112 | HIC_CLR_SPCMN_AVG2_RSLT | VARCHAR2(10) | Y |  | HIC测试CLR试样平均2实绩 | SCO_DATA_DIC(D) |
| 113 | HIC_CLR_SPCMN_AVG3_RSLT | VARCHAR2(10) | Y |  | HIC测试CLR试样平均3实绩 | SCO_DATA_DIC(D) |
| 114 | HIC_CSR_SPCMN_AVG1_RSLT | VARCHAR2(10) | Y |  | HIC测试CSR试样平均1实绩 | SCO_DATA_DIC(D) |
| 115 | HIC_CSR_SPCMN_AVG2_RSLT | VARCHAR2(10) | Y |  | HIC测试CSR试样平均2实绩 | SCO_DATA_DIC(D) |
| 116 | HIC_CSR_SPCMN_AVG3_RSLT | VARCHAR2(10) | Y |  | HIC测试CSR试样平均3实绩 | SCO_DATA_DIC(D) |
| 117 | HIC_CTR_SPCMN_AVG1_RSLT | VARCHAR2(10) | Y |  | HIC测试CTR试样平均1实绩 | SCO_DATA_DIC(D) |
| 118 | HIC_CTR_SPCMN_AVG2_RSLT | VARCHAR2(10) | Y |  | HIC测试CTR试样平均2实绩 | SCO_DATA_DIC(D) |
| 119 | HIC_CTR_SPCMN_AVG3_RSLT | VARCHAR2(10) | Y |  | HIC测试CTR试样平均3实绩 | SCO_DATA_DIC(D) |
| 120 | MGRPHY_GRNSZ_OCCP_RSLT | VARCHAR2(10) | Y |  | 金相测试基相的体积分数实绩 | SCO_DATA_DIC(D) |
| 121 | NON_METAL_A_GRP_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_A类（粗系）上限实绩 | SCO_DATA_DIC(D) |
| 122 | NON_METAL_A_DETAIL_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_A类（细系）上限实绩 | SCO_DATA_DIC(D) |
| 123 | NON_METAL_B_GRP_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_B类（粗系）上限实绩 | SCO_DATA_DIC(D) |
| 124 | NON_METAL_B_DETAIL_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_B类（细系）上限实绩 | SCO_DATA_DIC(D) |
| 125 | NON_METAL_C_GRP_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_C类（粗系）上限实绩 | SCO_DATA_DIC(D) |
| 126 | NON_METAL_C_DETAIL_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_C类（细系）上限实绩 | SCO_DATA_DIC(D) |
| 127 | NON_METAL_D_GRP_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_D类（粗系）上限实绩 | SCO_DATA_DIC(D) |
| 128 | NON_METAL_D_DETAIL_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_D类（细系）上限实绩 | SCO_DATA_DIC(D) |
| 129 | NON_METAL_AC_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_A+C上限实绩 | SCO_DATA_DIC(D) |
| 130 | NON_METAL_BDDS_RSLT | VARCHAR2(10) | Y |  | 夹杂物类别_B+D+Ds上限实绩 | SCO_DATA_DIC(D) |
| 131 | CPLATE_CUT_STRESS_RSLT | VARCHAR2(10) | Y |  | 抗剪强度τ实绩 | SCO_DATA_DIC(D) |
| 132 | CPLATE_THK_RSLT | VARCHAR2(10) | Y |  | 复层厚度实绩 | SCO_DATA_DIC(D) |
| 133 | CPLATE_ER_IE_RSLT | VARCHAR2(10) | Y |  | 杯突IE实绩 | SCO_DATA_DIC(D) |
| 134 | CPLATE_IN_BD_RSLT | VARCHAR2(10) | Y |  | 复层弯曲内弯结果 | SCO_DATA_DIC(D) |
| 135 | CPLATE_OT_BD_RSLT | VARCHAR2(10) | Y |  | 复层弯曲外弯结果 | SCO_DATA_DIC(D) |
| 136 | CPLATE_SIDE_BD_RSLT | VARCHAR2(10) | Y |  | 复层弯曲侧弯结果 | SCO_DATA_DIC(D) |
| 137 | HARD_AVG_RSLT | VARCHAR2(10) | Y |  | 硬度平均值实绩 | SCO_DATA_DIC(D) |
| 138 | HARD_IND_RSLT1 | VARCHAR2(10) | Y |  | 硬度单值实绩1 | SCO_DATA_DIC(D) |
| 139 | HARD_IND_RSLT2 | VARCHAR2(10) | Y |  | 硬度单值实绩2 | SCO_DATA_DIC(D) |
| 140 | HARD_IND_RSLT3 | VARCHAR2(10) | Y |  | 硬度单值实绩3 | SCO_DATA_DIC(D) |
| 141 | S_PRINT_RSLT | VARCHAR2(10) | Y |  | 硫印测试实绩 | SCO_DATA_DIC(D) |
| 142 | AGE_TST_STRESS_RSLT | VARCHAR2(10) | Y |  | 时效应变量实绩 | SCO_DATA_DIC(D) |
| 143 | AGE_TST_AGE_TIME_RSLT | VARCHAR2(10) | Y |  | 时效温度实绩 | SCO_DATA_DIC(D) |
| 144 | AGE_TST_AGE_TEMP_RSLT | VARCHAR2(10) | Y |  | 保温时间实绩 | SCO_DATA_DIC(D) |
| 145 | AGE_TST_YP_RSLT | VARCHAR2(10) | Y |  | 时效拉伸测试屈服强度实绩 | SCO_DATA_DIC(D) |
| 146 | AGE_TST_TS_RSLT | VARCHAR2(10) | Y |  | 时效拉伸测试抗拉强度实绩 | SCO_DATA_DIC(D) |
| 147 | AGE_TST_YP_TS_RSLT | VARCHAR2(10) | Y |  | 时效拉伸试验屈强比YP/TS实绩 | SCO_DATA_DIC(D) |
| 148 | AGE_TST_RT05_RM_RSLT | VARCHAR2(10) | Y |  | 时效拉伸试验屈强比Rt0.5/Rm实绩 | SCO_DATA_DIC(D) |
| 149 | AGE_TST_RT15_RT05_RSLT | VARCHAR2(10) | Y |  | 时效拉伸试验屈强比Rt1.5/Rt0.5实绩 | SCO_DATA_DIC(D) |
| 150 | AGE_TST_RT20_RT10_RSLT | VARCHAR2(10) | Y |  | 时效拉伸试验屈强比Rt2.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 151 | AGE_TST_RT50_RT10_RSLT | VARCHAR2(10) | Y |  | 时效拉伸试验屈强比Rt5.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 152 | AGE_TST_CT_EX_RA_RSLT | VARCHAR2(10) | Y |  | 拉抻测试断后伸长率实绩 | SCO_DATA_DIC(D) |
| 153 | AGE_TST_CT_RA_RSLT | VARCHAR2(10) | Y |  | 时效拉伸试验均匀伸长率实绩 | SCO_DATA_DIC(D) |
| 154 | AGE_TST_RA_RSLT | VARCHAR2(10) | Y |  | 时效拉伸试验断面收缩率实绩 | SCO_DATA_DIC(D) |
| 155 | AGE_TST1_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击1测试平均值实绩 | SCO_DATA_DIC(D) |
| 156 | AGE_TST1_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击1测试单值实绩1 | SCO_DATA_DIC(D) |
| 157 | AGE_TST1_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击1测试单值实绩2 | SCO_DATA_DIC(D) |
| 158 | AGE_TST1_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击1测试单值实绩3 | SCO_DATA_DIC(D) |
| 159 | AGE_TST1_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 纤维断面率1平均值实绩 | SCO_DATA_DIC(D) |
| 160 | AGE_TST1_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 纤维断面率1单值实绩1 | SCO_DATA_DIC(D) |
| 161 | AGE_TST1_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 纤维断面率1单值实绩2 | SCO_DATA_DIC(D) |
| 162 | AGE_TST1_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 纤维断面率1单值实绩3 | SCO_DATA_DIC(D) |
| 163 | AGE_TST1_SIDE_EXP_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击1试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 164 | AGE_TST1_SIDE_EXP_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击1试样侧膨胀值单值实绩1 | SCO_DATA_DIC(D) |
| 165 | AGE_TST1_SIDE_EXP_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击1试样侧膨胀值单值实绩2 | SCO_DATA_DIC(D) |
| 166 | AGE_TST1_SIDE_EXP_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击1试样侧膨胀值单值实绩3 | SCO_DATA_DIC(D) |
| 167 | AGE_TST2_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击2测试平均值实绩 | SCO_DATA_DIC(D) |
| 168 | AGE_TST2_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击2测试单值实绩1 | SCO_DATA_DIC(D) |
| 169 | AGE_TST2_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击2测试单值实绩2 | SCO_DATA_DIC(D) |
| 170 | AGE_TST2_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击2测试单值实绩3 | SCO_DATA_DIC(D) |
| 171 | AGE_TST2_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 纤维断面率2平均值实绩 | SCO_DATA_DIC(D) |
| 172 | AGE_TST2_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 纤维断面率2单值实绩1 | SCO_DATA_DIC(D) |
| 173 | AGE_TST2_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 纤维断面率2单值实绩2 | SCO_DATA_DIC(D) |
| 174 | AGE_TST2_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 纤维断面率2单值实绩3 | SCO_DATA_DIC(D) |
| 175 | AGE_TST2_SIDE_EXP_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击2试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 176 | AGE_TST2_SIDE_EXP_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击2试样侧膨胀值单值实绩1 | SCO_DATA_DIC(D) |
| 177 | AGE_TST2_SIDE_EXP_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击2试样侧膨胀值单值实绩2 | SCO_DATA_DIC(D) |
| 178 | AGE_TST2_SIDE_EXP_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击2试样侧膨胀值单值实绩3 | SCO_DATA_DIC(D) |
| 179 | AGE_TST3_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击3测试平均值实绩 | SCO_DATA_DIC(D) |
| 180 | AGE_TST3_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击3测试单值实绩1 | SCO_DATA_DIC(D) |
| 181 | AGE_TST3_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击3测试单值实绩2 | SCO_DATA_DIC(D) |
| 182 | AGE_TST3_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击3测试单值实绩3 | SCO_DATA_DIC(D) |
| 183 | AGE_TST3_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 纤维断面率3平均值实绩 | SCO_DATA_DIC(D) |
| 184 | AGE_TST3_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 纤维断面率3单值实绩1 | SCO_DATA_DIC(D) |
| 185 | AGE_TST3_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 纤维断面率3单值实绩2 | SCO_DATA_DIC(D) |
| 186 | AGE_TST3_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 纤维断面率3单值实绩3 | SCO_DATA_DIC(D) |
| 187 | ESB_FLAG | VARCHAR2(1) | Y |  |  | 空 |
| 188 | ESB_DATE | VARCHAR2(14) | Y |  |  | 空 |
| 189 | PK_ID | VARCHAR2(45) | N |  | Interface Primay Key ID | SCO_DATA_DIC(D) |
| 190 | TSL_YP_CD | VARCHAR2(1) | Y |  | 拉伸测试屈服强度类型 | SCO_DATA_DIC(D) |
| 191 | TSL_EL_CD | VARCHAR2(1) | Y |  | 拉伸测试伸长率类型 | SCO_DATA_DIC(D) |
| 192 | BEND_CD | VARCHAR2(1) | Y |  | 弯曲测试类型 | SCO_DATA_DIC(D) |
| 193 | BEND_UNIT | VARCHAR2(1) | Y |  | 弯曲测试单位 | SCO_DATA_DIC(D) |
| 194 | IMPACT_TEMP | NUMBER | Y |  | 冲击测试温度 | SCO_DATA_DIC(D) |
| 195 | IMPACT_SIZE | VARCHAR2(2) | Y |  |  | 空 |
| 196 | IMPACT_DIRECTION | VARCHAR2(1) | Y |  |  | 空 |
| 197 | HARD_KIND | VARCHAR2(1) | Y |  | 硬度测试种类 | SCO_DATA_DIC(D) |
| 198 | DWTT_TEMP | NUMBER | Y |  | DWTT | SCO_DATA_DIC(D) |
| 199 | ROUGH_KIND | VARCHAR2(1) | Y |  | 粗糙度测试种类 | SCO_DATA_DIC(D) |
| 200 | WAVIN_TY | VARCHAR2(1) | Y |  | 波纹度测试种类 | SCO_DATA_DIC(D) |
| 201 | PK_ID_D | VARCHAR2(60) | Y |  |  | 空 |

### SQM_WSP_MTC_MECH_INF_2

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=21｜被读 7 过程 / 被写 7 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：2　**主键**：（无显式主键）　**语义覆盖**：199/290

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | MTC_NO | VARCHAR2(11) | N |  | 质量保证书编号 | SCO_DATA_DIC(D) |
| 2 | MTC_STS | VARCHAR2(1) | N |  |  | 空 |
| 3 | MTC_DTM | VARCHAR2(14) | N |  |  | 空 |
| 4 | SMP_NO | VARCHAR2(14) | N |  | 시편번호 | SCO_DATA_DIC(D) |
| 5 | LOT_NO | VARCHAR2(14) | Y |  | LOT NO(BATCH NO) | SCO_DATA_DIC(D) |
| 6 | TEST_CNT | NUMBER | Y |  | 시험회수 | SCO_DATA_DIC(D) |
| 7 | AGE_TST3_SIDE_EXP_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击3试样侧膨胀值平均值实绩1 | SCO_DATA_DIC(D) |
| 8 | AGE_TST3_SIDE_EXP_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击3试样侧膨胀值单值实绩 | SCO_DATA_DIC(D) |
| 9 | AGE_TST3_SIDE_EXP_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击3试样侧膨胀值单值实绩2 | SCO_DATA_DIC(D) |
| 10 | AGE_TST3_SIDE_EXP_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击3试样侧膨胀值单值实绩3 | SCO_DATA_DIC(D) |
| 11 | AGE_TST4_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击4测试平均值实绩 | SCO_DATA_DIC(D) |
| 12 | AGE_TST4_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击4测试单值实绩1 | SCO_DATA_DIC(D) |
| 13 | AGE_TST4_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击4测试单值实绩2 | SCO_DATA_DIC(D) |
| 14 | AGE_TST4_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击4测试单值实绩3 | SCO_DATA_DIC(D) |
| 15 | AGE_TST4_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 纤维断面率4平均值实绩 | SCO_DATA_DIC(D) |
| 16 | AGE_TST4_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 纤维断面率4单值实绩1 | SCO_DATA_DIC(D) |
| 17 | AGE_TST4_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 纤维断面率4单值实绩2 | SCO_DATA_DIC(D) |
| 18 | AGE_TST4_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 纤维断面率4单值实绩3 | SCO_DATA_DIC(D) |
| 19 | AGE_TST4_SIDE_EXP_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击4试样侧膨胀值平均值实绩1 | SCO_DATA_DIC(D) |
| 20 | AGE_TST4_SIDE_EXP_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击4试样侧膨胀值单值实绩 | SCO_DATA_DIC(D) |
| 21 | AGE_TST4_SIDE_EXP_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击4试样侧膨胀值单值实绩2 | SCO_DATA_DIC(D) |
| 22 | AGE_TST4_SIDE_EXP_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击4试样侧膨胀值单值实绩3 | SCO_DATA_DIC(D) |
| 23 | AGE_TST5_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击5测试平均值实绩 | SCO_DATA_DIC(D) |
| 24 | AGE_TST5_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击5测试单值实绩1 | SCO_DATA_DIC(D) |
| 25 | AGE_TST5_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击5测试单值实绩2 | SCO_DATA_DIC(D) |
| 26 | AGE_TST5_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击5测试单值实绩3 | SCO_DATA_DIC(D) |
| 27 | AGE_TST5_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 纤维断面率5平均值实绩 | SCO_DATA_DIC(D) |
| 28 | AGE_TST5_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 纤维断面率5单值实绩1 | SCO_DATA_DIC(D) |
| 29 | AGE_TST5_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 纤维断面率5单值实绩2 | SCO_DATA_DIC(D) |
| 30 | AGE_TST5_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 纤维断面率5单值实绩3 | SCO_DATA_DIC(D) |
| 31 | AGE_TST5_SIDE_EXP_AVG_RSLT | VARCHAR2(10) | Y |  | 时效冲击5试样侧膨胀值平均值实绩1 | SCO_DATA_DIC(D) |
| 32 | AGE_TST5_SIDE_EXP_IND_RSLT1 | VARCHAR2(10) | Y |  | 时效冲击5试样侧膨胀值单值实绩 | SCO_DATA_DIC(D) |
| 33 | AGE_TST5_SIDE_EXP_IND_RSLT2 | VARCHAR2(10) | Y |  | 时效冲击5试样侧膨胀值单值实绩2 | SCO_DATA_DIC(D) |
| 34 | AGE_TST5_SIDE_EXP_IND_RSLT3 | VARCHAR2(10) | Y |  | 时效冲击5试样侧膨胀值单值实绩3 | SCO_DATA_DIC(D) |
| 35 | NDT_TEMP_RSLT | VARCHAR2(10) | Y |  | NDT温度实绩 | SCO_DATA_DIC(D) |
| 36 | CTOD_VAL_RSLT | VARCHAR2(10) | Y |  | CTOD值实绩 | SCO_DATA_DIC(D) |
| 37 | NP_JHRC_HARD_RSLT | VARCHAR2(10) | Y |  | 淬透性指数_JHRC硬度实绩 | SCO_DATA_DIC(D) |
| 38 | NP_JHRC_DIST_RSLT | VARCHAR2(10) | Y |  | 淬透性指数_JHRC距离实绩 | SCO_DATA_DIC(D) |
| 39 | NP_JHV_HARD_RSLT | VARCHAR2(10) | Y |  | 淬透性指数_JHV硬度实绩 | SCO_DATA_DIC(D) |
| 40 | NP_JHV_DIST_RSLT | VARCHAR2(10) | Y |  | 淬透性指数_JHV距离实绩 | SCO_DATA_DIC(D) |
| 41 | TSL1_YP_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1屈服强度实绩 | SCO_DATA_DIC(L) |
| 42 | TSL1_TS_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1抗拉强度实绩 | SCO_DATA_DIC(D) |
| 43 | TSL1_YP_TS_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1屈强比YP/TS实绩 | SCO_DATA_DIC(D) |
| 44 | TSL1_RT05_RM_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1屈强比Rt0.5/Rm实绩 | SCO_DATA_DIC(D) |
| 45 | TSL1_RT15_RT05_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1屈强比Rt1.5/Rt0.5实绩 | SCO_DATA_DIC(D) |
| 46 | TSL1_RT20_RT10_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1屈强比Rt2.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 47 | TSL1_RT50_RT10_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1屈强比Rt5.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 48 | TSL1_CT_EX_RA_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1断后伸长率实绩 | SCO_DATA_DIC(D) |
| 49 | TSL1_CT_RA_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1均匀伸长率实绩 | SCO_DATA_DIC(D) |
| 50 | TSL1_RA_RSLT | VARCHAR2(10) | Y |  | 拉伸试验1断面收缩率实绩 | SCO_DATA_DIC(D) |
| 51 | TSL2_YP_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2屈服强度实绩 | SCO_DATA_DIC(D) |
| 52 | TSL2_TS_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2抗拉强度实绩 | SCO_DATA_DIC(D) |
| 53 | TSL2_YP_TS_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2屈强比YP/TS实绩 | SCO_DATA_DIC(D) |
| 54 | TSL2_RT05_RM_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2屈强比Rt0.5/Rm实绩 | SCO_DATA_DIC(D) |
| 55 | TSL2_RT15_RT05_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2屈强比Rt1.5/Rt0.5实绩 | SCO_DATA_DIC(D) |
| 56 | TSL2_RT20_RT10_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2屈强比Rt2.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 57 | TSL2_RT50_RT10_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2屈强比Rt5.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 58 | TSL2_CT_EX_RA_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2断后伸长率实绩 | SCO_DATA_DIC(D) |
| 59 | TSL2_CT_RA_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2均匀伸长率实绩 | SCO_DATA_DIC(D) |
| 60 | TSL2_RA_RSLT | VARCHAR2(10) | Y |  | 拉伸试验2断面收缩率实绩 | SCO_DATA_DIC(D) |
| 61 | IMPACT1_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验1平均值实绩 | SCO_DATA_DIC(D) |
| 62 | IMPACT1_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验1单值实绩1 | SCO_DATA_DIC(D) |
| 63 | IMPACT1_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验1单值实绩2 | SCO_DATA_DIC(D) |
| 64 | IMPACT1_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验1单值实绩3 | SCO_DATA_DIC(D) |
| 65 | IMPACT1_SF_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验1纤维断面率平均值实绩 | SCO_DATA_DIC(D) |
| 66 | IMPACT1_SF_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验1纤维断面率单值实绩1 | SCO_DATA_DIC(D) |
| 67 | IMPACT1_SF_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验1纤维断面率单值实绩2 | SCO_DATA_DIC(D) |
| 68 | IMPACT1_SF_RATIO_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验1纤维断面率单值实绩3 | SCO_DATA_DIC(D) |
| 69 | IMPACT1_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验1试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 70 | IMPACT1_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验1试样侧膨胀值单值实绩1 | SCO_DATA_DIC(D) |
| 71 | IMPACT1_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验1试样侧膨胀值单值实绩2 | SCO_DATA_DIC(D) |
| 72 | IMPACT1_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验1试样侧膨胀值单值实绩3 | SCO_DATA_DIC(D) |
| 73 | IMPACT2_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验2平均值实绩 | SCO_DATA_DIC(D) |
| 74 | IMPACT2_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验2单值实绩1 | SCO_DATA_DIC(D) |
| 75 | IMPACT2_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验2单值实绩2 | SCO_DATA_DIC(D) |
| 76 | IMPACT2_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验2单值实绩3 | SCO_DATA_DIC(D) |
| 77 | IMPACT2_SF_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验2纤维断面率平均值实绩 | SCO_DATA_DIC(D) |
| 78 | IMPACT2_SF_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验2纤维断面率单值实绩1 | SCO_DATA_DIC(D) |
| 79 | IMPACT2_SF_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验2纤维断面率单值实绩2 | SCO_DATA_DIC(D) |
| 80 | IMPACT2_SF_RATIO_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验2纤维断面率单值实绩3 | SCO_DATA_DIC(D) |
| 81 | IMPACT2_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验2试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 82 | IMPACT2_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验2试样侧膨胀值单值实绩1 | SCO_DATA_DIC(D) |
| 83 | IMPACT2_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验2试样侧膨胀值单值实绩2 | SCO_DATA_DIC(D) |
| 84 | IMPACT2_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验2试样侧膨胀值单值实绩3 | SCO_DATA_DIC(D) |
| 85 | IMPACT3_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验3平均值实绩 | SCO_DATA_DIC(D) |
| 86 | IMPACT3_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验3单值实绩1 | SCO_DATA_DIC(D) |
| 87 | IMPACT3_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验3单值实绩2 | SCO_DATA_DIC(D) |
| 88 | IMPACT3_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验3单值实绩3 | SCO_DATA_DIC(D) |
| 89 | IMPACT3_SF_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验3纤维断面率平均值实绩 | SCO_DATA_DIC(D) |
| 90 | IMPACT3_SF_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验3纤维断面率单值实绩1 | SCO_DATA_DIC(D) |
| 91 | IMPACT3_SF_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验3纤维断面率单值实绩2 | SCO_DATA_DIC(D) |
| 92 | IMPACT3_SF_RATIO_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验3纤维断面率单值实绩3 | SCO_DATA_DIC(D) |
| 93 | IMPACT3_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验3试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 94 | IMPACT3_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验3试样侧膨胀值单值实绩1 | SCO_DATA_DIC(D) |
| 95 | IMPACT3_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验3试样侧膨胀值单值实绩2 | SCO_DATA_DIC(D) |
| 96 | IMPACT3_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验3试样侧膨胀值单值实绩3 | SCO_DATA_DIC(D) |
| 97 | IMPACT4_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验4平均值实绩 | SCO_DATA_DIC(D) |
| 98 | IMPACT4_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验4单值实绩1 | SCO_DATA_DIC(D) |
| 99 | IMPACT4_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验4单值实绩2 | SCO_DATA_DIC(D) |
| 100 | IMPACT4_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验4单值实绩3 | SCO_DATA_DIC(D) |
| 101 | IMPACT4_SF_RATIO_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验4纤维断面率平均值实绩 | SCO_DATA_DIC(D) |
| 102 | IMPACT4_SF_RATIO_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验4纤维断面率单值实绩1 | SCO_DATA_DIC(D) |
| 103 | IMPACT4_SF_RATIO_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验4纤维断面率单值实绩2 | SCO_DATA_DIC(D) |
| 104 | IMPACT4_SF_RATIO_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验4纤维断面率单值实绩3 | SCO_DATA_DIC(D) |
| 105 | IMPACT4_SMP_AVG_RSLT | VARCHAR2(10) | Y |  | 冲击试验4试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 106 | IMPACT4_SMP_IND_RSLT1 | VARCHAR2(10) | Y |  | 冲击试验4试样侧膨胀值单值实绩1 | SCO_DATA_DIC(D) |
| 107 | IMPACT4_SMP_IND_RSLT2 | VARCHAR2(10) | Y |  | 冲击试验4试样侧膨胀值单值实绩2 | SCO_DATA_DIC(D) |
| 108 | IMPACT4_SMP_IND_RSLT3 | VARCHAR2(10) | Y |  | 冲击试验4试样侧膨胀值单值实绩3 | SCO_DATA_DIC(D) |
| 109 | TST_COAT_WGT_TOT_AVG_RSLT | VARCHAR2(10) | Y |  | 镀锌层试验两面平均实绩 | SCO_DATA_DIC(D) |
| 110 | TST_COAT_WGT_UPPER_AVG_RSLT | VARCHAR2(10) | Y |  | 镀锌层试验上表面平均实绩 | SCO_DATA_DIC(D) |
| 111 | TST_COAT_WGT_LOWER_AVG_RSLT | VARCHAR2(10) | Y |  | 镀锌层试验下表面平均实绩 | SCO_DATA_DIC(D) |
| 112 | TSL1_EL_RSLT | VARCHAR2(10) | Y |  |  | 空 |
| 113 | PW_TSL_YP_CD | VARCHAR2(1) | Y |  | 模拟焊后 拉伸测试屈服强度类型 | SCO_DATA_DIC(D) |
| 114 | PW_TSL_YP_RSLT | NUMBER | Y |  | 模拟焊后 拉伸测试屈服强度实绩 | SCO_DATA_DIC(D) |
| 115 | PW_TSL_YP_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸测试屈服强度判定 | SCO_DATA_DIC(D) |
| 116 | PW_TSL_TS_RSLT | NUMBER | Y |  | 模拟焊后 拉伸测试抗拉强度实绩 | SCO_DATA_DIC(D) |
| 117 | PW_TSL_TS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸测试抗拉强度判定 | SCO_DATA_DIC(D) |
| 118 | PW_TSL_YP_TS_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比YP/TS实绩 | SCO_DATA_DIC(D) |
| 119 | PW_TSL_YP_TS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比YP/TS判定 | SCO_DATA_DIC(D) |
| 120 | PW_TSL_RT05_RM_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比Rt0.5/Rm实绩 | SCO_DATA_DIC(D) |
| 121 | PW_TSL_RT05_RM_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比Rt0.5/Rm判定 | SCO_DATA_DIC(D) |
| 122 | PW_TSL_RT15_RT05_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5实绩 | SCO_DATA_DIC(D) |
| 123 | PW_TSL_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5判定 | SCO_DATA_DIC(D) |
| 124 | PW_TSL_RT20_RT10_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 125 | PW_TSL_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0判定 | SCO_DATA_DIC(D) |
| 126 | PW_TSL_RT50_RT10_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 127 | PW_TSL_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0判定 | SCO_DATA_DIC(D) |
| 128 | PW_TSL_CT_EX_RA_RSLT | NUMBER | Y |  | 模拟焊后 拉抻测试断后伸长率实绩 | SCO_DATA_DIC(D) |
| 129 | PW_TSL_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 模拟焊后 拉抻测试断后伸长率类型 | SCO_DATA_DIC(D) |
| 130 | PW_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉抻测试断后伸长率判定 | SCO_DATA_DIC(D) |
| 131 | PW_TSL_CT_RA_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验均匀伸长率实绩 | SCO_DATA_DIC(D) |
| 132 | PW_TSL_CT_RA_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验均匀伸长率判定 | SCO_DATA_DIC(D) |
| 133 | PW_TSL_RA_RSLT | NUMBER | Y |  | 模拟焊后 拉伸试验断面收缩率实绩 | SCO_DATA_DIC(D) |
| 134 | PW_TSL_RA_JDG | VARCHAR2(1) | Y |  | 模拟焊后 拉伸试验断面收缩率判定 | SCO_DATA_DIC(D) |
| 135 | PW_TSL_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 模拟焊后 消应力处理_保温温度实绩 | SCO_DATA_DIC(D) |
| 136 | PW_TSL_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 模拟焊后 消应力处理_保温时间实绩 | SCO_DATA_DIC(D) |
| 137 | PW_TSL_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 模拟焊后 消应力处理_冷却方式 | SCO_DATA_DIC(D) |
| 138 | PW_TSL_STRESS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 消应力处理_判定 | SCO_DATA_DIC(D) |
| 139 | PW_IMPACT_TEMP_RSLT | NUMBER | Y |  | 模拟焊后 冲击测试温度实绩 | SCO_DATA_DIC(D) |
| 140 | PW_IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 模拟焊后 冲击测试缺口类型 | SCO_DATA_DIC(D) |
| 141 | PW_IMPACT_ENERGY_CD | VARCHAR2(1) | Y |  | 模拟焊后 冲击试样能量值类型 | SCO_DATA_DIC(D) |
| 142 | PW_IMPACT_AVG_RSLT | NUMBER | Y |  | 模拟焊后 冲击测试平均值实绩 | SCO_DATA_DIC(D) |
| 143 | PW_IMPACT_IND_RSLT1 | NUMBER | Y |  | 模拟焊后 冲击测试单值实绩1 | SCO_DATA_DIC(D) |
| 144 | PW_IMPACT_IND_RSLT2 | NUMBER | Y |  | 模拟焊后 冲击测试单值实绩2 | SCO_DATA_DIC(D) |
| 145 | PW_IMPACT_IND_RSLT3 | NUMBER | Y |  | 模拟焊后 冲击测试单值实绩3 | SCO_DATA_DIC(D) |
| 146 | PW_IMPACT_IND_JDG | VARCHAR2(1) | Y |  | 模拟焊后 冲击测试单值判定 | SCO_DATA_DIC(D) |
| 147 | PW_IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 模拟焊后 纤维断面率平均值实绩 | SCO_DATA_DIC(D) |
| 148 | PW_IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 模拟焊后 纤维断面率单值实绩1 | SCO_DATA_DIC(D) |
| 149 | PW_IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 模拟焊后 纤维断面率单值实绩2 | SCO_DATA_DIC(D) |
| 150 | PW_IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 模拟焊后 纤维断面率单值实绩3 | SCO_DATA_DIC(D) |
| 151 | PW_IMPACT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 模拟焊后 纤维断面率单值判定 | SCO_DATA_DIC(D) |
| 152 | PW_IMPACT_SMP_AVG_RSLT | NUMBER | Y |  | 模拟焊后 冲击试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 153 | PW_IMPACT_SMP_IND_RSLT1 | NUMBER | Y |  | 模拟焊后 冲击试样侧膨胀值单值实绩1 | SCO_DATA_DIC(D) |
| 154 | PW_IMPACT_SMP_IND_RSLT2 | NUMBER | Y |  | 模拟焊后 冲击试样侧膨胀值单值实绩2 | SCO_DATA_DIC(D) |
| 155 | PW_IMPACT_SMP_IND_RSLT3 | NUMBER | Y |  | 模拟焊后 冲击试样侧膨胀值单值实绩3 | SCO_DATA_DIC(D) |
| 156 | PW_IMPACT_SMP_IND_JDG | VARCHAR2(1) | Y |  | 模拟焊后 冲击试样侧膨胀值单值判定 | SCO_DATA_DIC(D) |
| 157 | PW_MGRPHY_MTLGRP_TY | VARCHAR2(20) | Y |  | 模拟焊后 组织类型 | SCO_DATA_DIC(D) |
| 158 | PW_MGRPHY_MTLGRP_TY_PROVIDE | VARCHAR2(1) | Y |  | 模拟焊后 组织类型是否提供 | SCO_DATA_DIC(D) |
| 159 | PW_MGRPHY_BAND_STRC_MAX_RSLT | NUMBER | Y |  | 模拟焊后 带状组织等级上限实绩 | SCO_DATA_DIC(D) |
| 160 | PW_MGRPHY_BAND_STRC_MAX_JDG | VARCHAR2(1) | Y |  | 模拟焊后 带状组织等级上限判定 | SCO_DATA_DIC(D) |
| 161 | PW_MGRPHY_RSLT | NUMBER | Y |  |  | 空 |
| 162 | PW_MGRPHY_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 163 | PW_MGRPHY_FGS_RSLT | NUMBER | Y |  | 模拟焊后 铁素体晶粒度实绩 | SCO_DATA_DIC(D) |
| 164 | PW_MGRPHY_FGS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 铁素体晶粒度判定 | SCO_DATA_DIC(D) |
| 165 | PW_MGRPHY_AGS_RSLT | NUMBER | Y |  | 模拟焊后 奥氏体晶粒度实绩 | SCO_DATA_DIC(D) |
| 166 | PW_MGRPHY_AGS_JDG | VARCHAR2(1) | Y |  | 模拟焊后 奥氏体晶粒度判定 | SCO_DATA_DIC(D) |
| 167 | PW_MGRPHY_GRNSZ_OCCP_RSLT | NUMBER | Y |  | 模拟焊后 金相测试基相的体积分数实绩 | SCO_DATA_DIC(D) |
| 168 | PW_MGRPHY_GRNSZ_OCCP_JDG | VARCHAR2(1) | Y |  | 模拟焊后 金相测试基相的体积分数判定 | SCO_DATA_DIC(D) |
| 169 | PW_BEND_DIA | NUMBER | Y |  | 模拟焊后 弯曲测试弯心直径 | SCO_DATA_DIC(D) |
| 170 | PW_BEND_ANGLE | NUMBER | Y |  | 模拟焊后 弯曲测试弯曲角度 | SCO_DATA_DIC(D) |
| 171 | PW_BEND_RSLT | VARCHAR2(1) | Y |  | 模拟焊后 弯曲测试实绩 | SCO_DATA_DIC(D) |
| 172 | PW_BEND_JDG | VARCHAR2(1) | Y |  | 模拟焊后 弯曲测试判定 | SCO_DATA_DIC(D) |
| 173 | PW_Z_TSL_CUT_IND_RSLT1 | NUMBER | Y |  |  | 空 |
| 174 | PW_Z_TSL_CUT_IND_RSLT2 | NUMBER | Y |  |  | 空 |
| 175 | PW_Z_TSL_CUT_IND_RSLT3 | NUMBER | Y |  |  | 空 |
| 176 | PW_Z_TSL_CUT_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 177 | PW_Z_TSL_CUT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 178 | PW_Z_TSL_CUT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 179 | PW_Z_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 180 | PW_Z_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 181 | PW_Z_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 182 | PW_Z_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 183 | PW_Z_TSL_CT_EX_RA_RSLT | NUMBER | Y |  |  | 空 |
| 184 | PW_Z_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 185 | PW_HIGH_TEMP_TSL_STAND_CD | VARCHAR2(20) | Y |  |  | 空 |
| 186 | PW_HIGH_TEMP_TSL_TEMP_RSLT | NUMBER | Y |  |  | 空 |
| 187 | PW_HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 188 | PW_HIGH_TEMP_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 189 | PW_HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  |  | 空 |
| 190 | PW_HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 191 | PW_HIGH_TEMP_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 192 | PW_HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  |  | 空 |
| 193 | PW_HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  |  | 空 |
| 194 | PW_HIGH_TEMP_TSL_EL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 195 | PW_HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  |  | 空 |
| 196 | PW_HIGH_TEMP_TSL_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 197 | PW_SSCC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 198 | PW_SSCC_STRESS_TY | VARCHAR2(1) | Y |  |  | 空 |
| 199 | PW_SSCC_STRESS_TST_VAL_RSLT | NUMBER | Y |  |  | 空 |
| 200 | PW_SSCC_STRESS_TST_VAL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 201 | PW_SSCC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 202 | PW_HIC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 203 | PW_HIC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 204 | PW_HIC_CLR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 205 | PW_HIC_CLR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 206 | PW_HIC_CLR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 207 | PW_HIC_CLR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 208 | PW_HIC_CLR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 209 | PW_HIC_CLR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 210 | PW_HIC_CLR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 211 | PW_HIC_CLR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 212 | PW_HIC_CLR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 213 | PW_HIC_CLR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 214 | PW_HIC_CLR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 215 | PW_HIC_CLR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 216 | PW_HIC_CLR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 217 | PW_HIC_CLR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 218 | PW_HIC_CLR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 219 | PW_HIC_CLR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 220 | PW_HIC_CSR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 221 | PW_HIC_CSR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 222 | PW_HIC_CSR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 223 | PW_HIC_CSR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 224 | PW_HIC_CSR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 225 | PW_HIC_CSR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 226 | PW_HIC_CSR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 227 | PW_HIC_CSR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 228 | PW_HIC_CSR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 229 | PW_HIC_CSR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 230 | PW_HIC_CSR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 231 | PW_HIC_CSR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 232 | PW_HIC_CSR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 233 | PW_HIC_CSR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 234 | PW_HIC_CSR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 235 | PW_HIC_CSR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 236 | PW_HIC_CTR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 237 | PW_HIC_CTR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 238 | PW_HIC_CTR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 239 | PW_HIC_CTR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 240 | PW_HIC_CTR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 241 | PW_HIC_CTR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 242 | PW_HIC_CTR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 243 | PW_HIC_CTR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 244 | PW_HIC_CTR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 245 | PW_HIC_CTR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 246 | PW_HIC_CTR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 247 | PW_HIC_CTR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 248 | PW_HIC_CTR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 249 | PW_HIC_CTR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 250 | PW_HIC_CTR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 251 | PW_HIC_CTR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 252 | PW_HARD_KIND | VARCHAR2(1) | Y |  |  | 空 |
| 253 | PW_HARD_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 254 | PW_HARD_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 255 | PW_HARD_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 256 | PW_HARD_RSLT1 | NUMBER | Y |  | 硬度测试实绩4 | SCO_DATA_DIC(D) |
| 257 | PW_HARD_RSLT2 | NUMBER | Y |  | 硬度测试实绩5 | SCO_DATA_DIC(D) |
| 258 | PW_HARD_RSLT3 | NUMBER | Y |  | 硬度测试实绩6 | SCO_DATA_DIC(D) |
| 259 | PW_HARD_RSLT4 | NUMBER | Y |  | 硬度测试实绩4 | SCO_DATA_DIC(D) |
| 260 | PW_HARD_RSLT5 | NUMBER | Y |  | 硬度测试实绩5 | SCO_DATA_DIC(D) |
| 261 | PW_HARD_RSLT6 | NUMBER | Y |  | 硬度测试实绩6 | SCO_DATA_DIC(D) |
| 262 | PW_HARD_RSLT7 | NUMBER | Y |  | 硬度测试实绩7 | SCO_DATA_DIC(D) |
| 263 | PW_HARD_RSLT8 | NUMBER | Y |  | 硬度测试实绩8 | SCO_DATA_DIC(D) |
| 264 | PW_HARD_RSLT9 | NUMBER | Y |  | 硬度测试实绩9 | SCO_DATA_DIC(D) |
| 265 | MXPW_TSL_YP_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸测试屈服强度类型 | SCO_DATA_DIC(D) |
| 266 | MXPW_TSL_YP_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸测试屈服强度实绩 | SCO_DATA_DIC(D) |
| 267 | MXPW_TSL_YP_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸测试屈服强度判定 | SCO_DATA_DIC(D) |
| 268 | MXPW_TSL_TS_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸测试抗拉强度实绩 | SCO_DATA_DIC(D) |
| 269 | MXPW_TSL_TS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸测试抗拉强度判定 | SCO_DATA_DIC(D) |
| 270 | MXPW_TSL_YP_TS_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比YP/TS实绩 | SCO_DATA_DIC(D) |
| 271 | MXPW_TSL_YP_TS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比YP/TS判定 | SCO_DATA_DIC(D) |
| 272 | MXPW_TSL_RT05_RM_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比Rt0.5/Rm实绩 | SCO_DATA_DIC(D) |
| 273 | MXPW_TSL_RT05_RM_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比Rt0.5/Rm判定 | SCO_DATA_DIC(D) |
| 274 | MXPW_TSL_RT15_RT05_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5实绩 | SCO_DATA_DIC(D) |
| 275 | MXPW_TSL_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5判定 | SCO_DATA_DIC(D) |
| 276 | MXPW_TSL_RT20_RT10_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 277 | MXPW_TSL_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0判定 | SCO_DATA_DIC(D) |
| 278 | MXPW_TSL_RT50_RT10_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 279 | MXPW_TSL_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0判定 | SCO_DATA_DIC(D) |
| 280 | MXPW_TSL_CT_EX_RA_RSLT | NUMBER | Y |  | 最大模拟焊后 拉抻测试断后伸长率实绩 | SCO_DATA_DIC(D) |
| 281 | MXPW_TSL_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 拉抻测试断后伸长率类型 | SCO_DATA_DIC(D) |
| 282 | MXPW_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉抻测试断后伸长率判定 | SCO_DATA_DIC(D) |
| 283 | MXPW_TSL_CT_RA_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验均匀伸长率实绩 | SCO_DATA_DIC(D) |
| 284 | MXPW_TSL_CT_RA_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验均匀伸长率判定 | SCO_DATA_DIC(D) |
| 285 | MXPW_TSL_RA_RSLT | NUMBER | Y |  | 最大模拟焊后 拉伸试验断面收缩率实绩 | SCO_DATA_DIC(D) |
| 286 | MXPW_TSL_RA_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 拉伸试验断面收缩率判定 | SCO_DATA_DIC(D) |
| 287 | ESB_FLAG | VARCHAR2(1) | Y |  |  | 空 |
| 288 | ESB_DATE | VARCHAR2(14) | Y |  |  | 空 |
| 289 | PK_ID | VARCHAR2(45) | N |  | Interface Primay Key ID | SCO_DATA_DIC(D) |
| 290 | PK_ID_D | VARCHAR2(60) | Y |  |  | 空 |

### SQM_WSP_MTC_MECH_INF_3

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=21｜被读 7 过程 / 被写 7 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：2　**主键**：（无显式主键）　**语义覆盖**：117/299

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | MTC_NO | VARCHAR2(11) | N |  | 质量保证书编号 | SCO_DATA_DIC(D) |
| 2 | MTC_STS | VARCHAR2(1) | N |  |  | 空 |
| 3 | MTC_DTM | VARCHAR2(14) | N |  |  | 空 |
| 4 | SMP_NO | VARCHAR2(14) | N |  | 시편번호 | SCO_DATA_DIC(D) |
| 5 | LOT_NO | VARCHAR2(14) | Y |  | LOT NO(BATCH NO) | SCO_DATA_DIC(D) |
| 6 | TEST_CNT | NUMBER | Y |  | 시험회수 | SCO_DATA_DIC(D) |
| 7 | MXPW_TSL_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 最大模拟焊后 消应力处理_保温温度实绩 | SCO_DATA_DIC(D) |
| 8 | MXPW_TSL_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 最大模拟焊后 消应力处理_保温时间实绩 | SCO_DATA_DIC(D) |
| 9 | MXPW_TSL_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 消应力处理_冷却方式 | SCO_DATA_DIC(D) |
| 10 | MXPW_TSL_STRESS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 消应力处理_判定 | SCO_DATA_DIC(D) |
| 11 | MXPW_IMPACT_TEMP_RSLT | NUMBER | Y |  | 最大模拟焊后 冲击测试温度实绩 | SCO_DATA_DIC(D) |
| 12 | MXPW_IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 冲击测试缺口类型 | SCO_DATA_DIC(D) |
| 13 | MXPW_IMPACT_ENERGY_CD | VARCHAR2(1) | Y |  | 最大模拟焊后 冲击试样能量值类型 | SCO_DATA_DIC(D) |
| 14 | MXPW_IMPACT_AVG_RSLT | NUMBER | Y |  | 最大模拟焊后 冲击测试平均值实绩 | SCO_DATA_DIC(D) |
| 15 | MXPW_IMPACT_IND_RSLT1 | NUMBER | Y |  | 最大模拟焊后 冲击测试单值实绩1 | SCO_DATA_DIC(D) |
| 16 | MXPW_IMPACT_IND_RSLT2 | NUMBER | Y |  | 最大模拟焊后 冲击测试单值实绩2 | SCO_DATA_DIC(D) |
| 17 | MXPW_IMPACT_IND_RSLT3 | NUMBER | Y |  | 最大模拟焊后 冲击测试单值实绩3 | SCO_DATA_DIC(D) |
| 18 | MXPW_IMPACT_IND_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 冲击测试单值判定 | SCO_DATA_DIC(D) |
| 19 | MXPW_IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 最大模拟焊后 纤维断面率平均值实绩 | SCO_DATA_DIC(D) |
| 20 | MXPW_IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 最大模拟焊后 纤维断面率单值实绩1 | SCO_DATA_DIC(D) |
| 21 | MXPW_IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 最大模拟焊后 纤维断面率单值实绩2 | SCO_DATA_DIC(D) |
| 22 | MXPW_IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 最大模拟焊后 纤维断面率单值实绩3 | SCO_DATA_DIC(D) |
| 23 | MXPW_IMPACT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 纤维断面率单值判定 | SCO_DATA_DIC(D) |
| 24 | MXPW_IMPACT_SMP_AVG_RSLT | NUMBER | Y |  | 最大模拟焊后 冲击试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 25 | MXPW_IMPACT_SMP_IND_RSLT1 | NUMBER | Y |  | 最大模拟焊后 冲击试样侧膨胀值单值实绩1 | SCO_DATA_DIC(D) |
| 26 | MXPW_IMPACT_SMP_IND_RSLT2 | NUMBER | Y |  | 最大模拟焊后 冲击试样侧膨胀值单值实绩2 | SCO_DATA_DIC(D) |
| 27 | MXPW_IMPACT_SMP_IND_RSLT3 | NUMBER | Y |  | 最大模拟焊后 冲击试样侧膨胀值单值实绩3 | SCO_DATA_DIC(D) |
| 28 | MXPW_IMPACT_SMP_IND_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 冲击试样侧膨胀值单值判定 | SCO_DATA_DIC(D) |
| 29 | MXPW_MGRPHY_MTLGRP_TY | VARCHAR2(20) | Y |  | 最大模拟焊后 组织类型 | SCO_DATA_DIC(D) |
| 30 | MXPW_MGRPHY_MTLGRP_TY_PROVIDE | VARCHAR2(1) | Y |  | 最大模拟焊后 组织类型是否提供 | SCO_DATA_DIC(D) |
| 31 | MXPW_MGRPHY_BAND_STRC_MAX_RSLT | NUMBER | Y |  | 最大模拟焊后 带状组织等级上限实绩 | SCO_DATA_DIC(D) |
| 32 | MXPW_MGRPHY_BAND_STRC_MAX_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 带状组织等级上限判定 | SCO_DATA_DIC(D) |
| 33 | MXPW_MGRPHY_RSLT | NUMBER | Y |  |  | 空 |
| 34 | MXPW_MGRPHY_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 35 | MXPW_MGRPHY_FGS_RSLT | NUMBER | Y |  | 最大模拟焊后 铁素体晶粒度实绩 | SCO_DATA_DIC(D) |
| 36 | MXPW_MGRPHY_FGS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 铁素体晶粒度判定 | SCO_DATA_DIC(D) |
| 37 | MXPW_MGRPHY_AGS_RSLT | NUMBER | Y |  | 最大模拟焊后 奥氏体晶粒度实绩 | SCO_DATA_DIC(D) |
| 38 | MXPW_MGRPHY_AGS_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 奥氏体晶粒度判定 | SCO_DATA_DIC(D) |
| 39 | MXPW_MGRPHY_GRNSZ_OCCP_RSLT | NUMBER | Y |  | 最大模拟焊后 金相测试基相的体积分数实绩 | SCO_DATA_DIC(D) |
| 40 | MXPW_MGRPHY_GRNSZ_OCCP_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 金相测试基相的体积分数判定 | SCO_DATA_DIC(D) |
| 41 | MXPW_BEND_DIA | NUMBER | Y |  | 最大模拟焊后 弯曲测试弯心直径 | SCO_DATA_DIC(D) |
| 42 | MXPW_BEND_ANGLE | NUMBER | Y |  | 最大模拟焊后 弯曲测试弯曲角度 | SCO_DATA_DIC(D) |
| 43 | MXPW_BEND_RSLT | VARCHAR2(1) | Y |  | 最大模拟焊后 弯曲测试实绩 | SCO_DATA_DIC(D) |
| 44 | MXPW_BEND_JDG | VARCHAR2(1) | Y |  | 最大模拟焊后 弯曲测试判定 | SCO_DATA_DIC(D) |
| 45 | MXPW_Z_TSL_CUT_IND_RSLT1 | NUMBER | Y |  |  | 空 |
| 46 | MXPW_Z_TSL_CUT_IND_RSLT2 | NUMBER | Y |  |  | 空 |
| 47 | MXPW_Z_TSL_CUT_IND_RSLT3 | NUMBER | Y |  |  | 空 |
| 48 | MXPW_Z_TSL_CUT_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 49 | MXPW_Z_TSL_CUT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 50 | MXPW_Z_TSL_CUT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 51 | MXPW_Z_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 52 | MXPW_Z_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 53 | MXPW_Z_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 54 | MXPW_Z_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 55 | MXPW_Z_TSL_CT_EX_RA_RSLT | NUMBER | Y |  |  | 空 |
| 56 | MXPW_Z_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 57 | MXPW_HIGH_TEMP_TSL_STAND_CD | VARCHAR2(20) | Y |  |  | 空 |
| 58 | MXPW_HIGH_TEMP_TSL_TEMP_RSLT | NUMBER | Y |  |  | 空 |
| 59 | MXPW_HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 60 | MXPW_HIGH_TEMP_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 61 | MXPW_HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  |  | 空 |
| 62 | MXPW_HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 63 | MXPW_HIGH_TEMP_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 64 | MXPW_HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  |  | 空 |
| 65 | MXPW_HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  |  | 空 |
| 66 | MXPW_HIGH_TEMP_TSL_EL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 67 | MXPW_HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  |  | 空 |
| 68 | MXPW_HIGH_TEMP_TSL_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 69 | MXPW_SSCC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 70 | MXPW_SSCC_STRESS_TY | VARCHAR2(1) | Y |  |  | 空 |
| 71 | MXPW_SSCC_STRESS_TST_VAL_RSLT | NUMBER | Y |  |  | 空 |
| 72 | MXPW_SSCC_STRESS_TST_VAL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 73 | MXPW_SSCC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 74 | MXPW_HIC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 75 | MXPW_HIC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 76 | MXPW_HIC_CLR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 77 | MXPW_HIC_CLR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 78 | MXPW_HIC_CLR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 79 | MXPW_HIC_CLR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 80 | MXPW_HIC_CLR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 81 | MXPW_HIC_CLR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 82 | MXPW_HIC_CLR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 83 | MXPW_HIC_CLR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 84 | MXPW_HIC_CLR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 85 | MXPW_HIC_CLR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 86 | MXPW_HIC_CLR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 87 | MXPW_HIC_CLR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 88 | MXPW_HIC_CLR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 89 | MXPW_HIC_CLR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 90 | MXPW_HIC_CLR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 91 | MXPW_HIC_CLR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 92 | MXPW_HIC_CSR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 93 | MXPW_HIC_CSR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 94 | MXPW_HIC_CSR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 95 | MXPW_HIC_CSR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 96 | MXPW_HIC_CSR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 97 | MXPW_HIC_CSR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 98 | MXPW_HIC_CSR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 99 | MXPW_HIC_CSR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 100 | MXPW_HIC_CSR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 101 | MXPW_HIC_CSR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 102 | MXPW_HIC_CSR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 103 | MXPW_HIC_CSR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 104 | MXPW_HIC_CSR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 105 | MXPW_HIC_CSR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 106 | MXPW_HIC_CSR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 107 | MXPW_HIC_CSR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 108 | MXPW_HIC_CTR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 109 | MXPW_HIC_CTR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 110 | MXPW_HIC_CTR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 111 | MXPW_HIC_CTR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 112 | MXPW_HIC_CTR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 113 | MXPW_HIC_CTR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 114 | MXPW_HIC_CTR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 115 | MXPW_HIC_CTR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 116 | MXPW_HIC_CTR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 117 | MXPW_HIC_CTR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 118 | MXPW_HIC_CTR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 119 | MXPW_HIC_CTR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 120 | MXPW_HIC_CTR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 121 | MXPW_HIC_CTR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 122 | MXPW_HIC_CTR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 123 | MXPW_HIC_CTR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 124 | MXPW_HARD_KIND | VARCHAR2(1) | Y |  |  | 空 |
| 125 | MXPW_HARD_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 126 | MXPW_HARD_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 127 | MXPW_HARD_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 128 | MNPW_TSL_YP_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸测试屈服强度类型 | SCO_DATA_DIC(D) |
| 129 | MNPW_TSL_YP_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸测试屈服强度实绩 | SCO_DATA_DIC(D) |
| 130 | MNPW_TSL_YP_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸测试屈服强度判定 | SCO_DATA_DIC(D) |
| 131 | MNPW_TSL_TS_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸测试抗拉强度实绩 | SCO_DATA_DIC(D) |
| 132 | MNPW_TSL_TS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸测试抗拉强度判定 | SCO_DATA_DIC(D) |
| 133 | MNPW_TSL_YP_TS_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比YP/TS实绩 | SCO_DATA_DIC(D) |
| 134 | MNPW_TSL_YP_TS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比YP/TS判定 | SCO_DATA_DIC(D) |
| 135 | MNPW_TSL_RT05_RM_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比Rt0.5/Rm实绩 | SCO_DATA_DIC(D) |
| 136 | MNPW_TSL_RT05_RM_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比Rt0.5/Rm判定 | SCO_DATA_DIC(D) |
| 137 | MNPW_TSL_RT15_RT05_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5实绩 | SCO_DATA_DIC(D) |
| 138 | MNPW_TSL_RT15_RT05_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比Rt1.5/Rt0.5判定 | SCO_DATA_DIC(D) |
| 139 | MNPW_TSL_RT20_RT10_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 140 | MNPW_TSL_RT20_RT10_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比Rt2.0/Rt1.0判定 | SCO_DATA_DIC(D) |
| 141 | MNPW_TSL_RT50_RT10_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0实绩 | SCO_DATA_DIC(D) |
| 142 | MNPW_TSL_RT50_RT10_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验屈强比Rt5.0/Rt1.0判定 | SCO_DATA_DIC(D) |
| 143 | MNPW_TSL_CT_EX_RA_RSLT | NUMBER | Y |  | 最小模拟焊后 拉抻测试断后伸长率实绩 | SCO_DATA_DIC(D) |
| 144 | MNPW_TSL_CT_EX_RA_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 拉抻测试断后伸长率类型 | SCO_DATA_DIC(D) |
| 145 | MNPW_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉抻测试断后伸长率判定 | SCO_DATA_DIC(D) |
| 146 | MNPW_TSL_CT_RA_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验均匀伸长率实绩 | SCO_DATA_DIC(D) |
| 147 | MNPW_TSL_CT_RA_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验均匀伸长率判定 | SCO_DATA_DIC(D) |
| 148 | MNPW_TSL_RA_RSLT | NUMBER | Y |  | 最小模拟焊后 拉伸试验断面收缩率实绩 | SCO_DATA_DIC(D) |
| 149 | MNPW_TSL_RA_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 拉伸试验断面收缩率判定 | SCO_DATA_DIC(D) |
| 150 | MNPW_TSL_STRESS_WARM_TEMP_RSLT | NUMBER | Y |  | 最小模拟焊后 消应力处理_保温温度实绩 | SCO_DATA_DIC(D) |
| 151 | MNPW_TSL_STRESS_WARM_TIME_RSLT | NUMBER | Y |  | 最小模拟焊后 消应力处理_保温时间实绩 | SCO_DATA_DIC(D) |
| 152 | MNPW_TSL_STRESS_COOL_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 消应力处理_冷却方式 | SCO_DATA_DIC(D) |
| 153 | MNPW_TSL_STRESS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 消应力处理_判定 | SCO_DATA_DIC(D) |
| 154 | MNPW_IMPACT_TEMP_RSLT | NUMBER | Y |  | 最小模拟焊后 冲击测试温度实绩 | SCO_DATA_DIC(D) |
| 155 | MNPW_IMPACT_CREAK_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 冲击测试缺口类型 | SCO_DATA_DIC(D) |
| 156 | MNPW_IMPACT_ENERGY_CD | VARCHAR2(1) | Y |  | 最小模拟焊后 冲击试样能量值类型 | SCO_DATA_DIC(D) |
| 157 | MNPW_IMPACT_AVG_RSLT | NUMBER | Y |  | 最小模拟焊后 冲击测试平均值实绩 | SCO_DATA_DIC(D) |
| 158 | MNPW_IMPACT_IND_RSLT1 | NUMBER | Y |  | 最小模拟焊后 冲击测试单值实绩1 | SCO_DATA_DIC(D) |
| 159 | MNPW_IMPACT_IND_RSLT2 | NUMBER | Y |  | 最小模拟焊后 冲击测试单值实绩2 | SCO_DATA_DIC(D) |
| 160 | MNPW_IMPACT_IND_RSLT3 | NUMBER | Y |  | 最小模拟焊后 冲击测试单值实绩3 | SCO_DATA_DIC(D) |
| 161 | MNPW_IMPACT_IND_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 冲击测试单值判定 | SCO_DATA_DIC(D) |
| 162 | MNPW_IMPACT_SF_RATIO_AVG_RSLT | NUMBER | Y |  | 最小模拟焊后 纤维断面率平均值实绩 | SCO_DATA_DIC(D) |
| 163 | MNPW_IMPACT_SF_RATIO_IND_RSLT1 | NUMBER | Y |  | 最小模拟焊后 纤维断面率单值实绩1 | SCO_DATA_DIC(D) |
| 164 | MNPW_IMPACT_SF_RATIO_IND_RSLT2 | NUMBER | Y |  | 最小模拟焊后 纤维断面率单值实绩2 | SCO_DATA_DIC(D) |
| 165 | MNPW_IMPACT_SF_RATIO_IND_RSLT3 | NUMBER | Y |  | 最小模拟焊后 纤维断面率单值实绩3 | SCO_DATA_DIC(D) |
| 166 | MNPW_IMPACT_SF_RATIO_IND_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 纤维断面率单值判定 | SCO_DATA_DIC(D) |
| 167 | MNPW_IMPACT_SMP_AVG_RSLT | NUMBER | Y |  | 最小模拟焊后 冲击试样侧膨胀值平均值实绩 | SCO_DATA_DIC(D) |
| 168 | MNPW_IMPACT_SMP_IND_RSLT1 | NUMBER | Y |  | 最小模拟焊后 冲击试样侧膨胀值单值实绩1 | SCO_DATA_DIC(D) |
| 169 | MNPW_IMPACT_SMP_IND_RSLT2 | NUMBER | Y |  | 最小模拟焊后 冲击试样侧膨胀值单值实绩2 | SCO_DATA_DIC(D) |
| 170 | MNPW_IMPACT_SMP_IND_RSLT3 | NUMBER | Y |  | 最小模拟焊后 冲击试样侧膨胀值单值实绩3 | SCO_DATA_DIC(D) |
| 171 | MNPW_IMPACT_SMP_IND_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 冲击试样侧膨胀值单值判定 | SCO_DATA_DIC(D) |
| 172 | MNPW_MGRPHY_MTLGRP_TY | VARCHAR2(20) | Y |  | 最小模拟焊后 组织类型 | SCO_DATA_DIC(D) |
| 173 | MNPW_MGRPHY_MTLGRP_TY_PROVIDE | VARCHAR2(1) | Y |  | 最小模拟焊后 组织类型是否提供 | SCO_DATA_DIC(D) |
| 174 | MNPW_MGRPHY_BAND_STRC_MAX_RSLT | NUMBER | Y |  | 最小模拟焊后 带状组织等级上限实绩 | SCO_DATA_DIC(D) |
| 175 | MNPW_MGRPHY_BAND_STRC_MAX_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 带状组织等级上限判定 | SCO_DATA_DIC(D) |
| 176 | MNPW_MGRPHY_RSLT | NUMBER | Y |  |  | 空 |
| 177 | MNPW_MGRPHY_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 178 | MNPW_MGRPHY_FGS_RSLT | NUMBER | Y |  | 最小模拟焊后 铁素体晶粒度实绩 | SCO_DATA_DIC(D) |
| 179 | MNPW_MGRPHY_FGS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 铁素体晶粒度判定 | SCO_DATA_DIC(D) |
| 180 | MNPW_MGRPHY_AGS_RSLT | NUMBER | Y |  | 最小模拟焊后 奥氏体晶粒度实绩 | SCO_DATA_DIC(D) |
| 181 | MNPW_MGRPHY_AGS_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 奥氏体晶粒度判定 | SCO_DATA_DIC(D) |
| 182 | MNPW_MGRPHY_GRNSZ_OCCP_RSLT | NUMBER | Y |  | 最小模拟焊后 金相测试基相的体积分数实绩 | SCO_DATA_DIC(D) |
| 183 | MNPW_MGRPHY_GRNSZ_OCCP_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 金相测试基相的体积分数判定 | SCO_DATA_DIC(D) |
| 184 | MNPW_BEND_DIA | NUMBER | Y |  | 最小模拟焊后 弯曲测试弯心直径 | SCO_DATA_DIC(D) |
| 185 | MNPW_BEND_ANGLE | NUMBER | Y |  | 最小模拟焊后 弯曲测试弯曲角度 | SCO_DATA_DIC(D) |
| 186 | MNPW_BEND_RSLT | VARCHAR2(1) | Y |  | 最小模拟焊后 弯曲测试实绩 | SCO_DATA_DIC(D) |
| 187 | MNPW_BEND_JDG | VARCHAR2(1) | Y |  | 最小模拟焊后 弯曲测试判定 | SCO_DATA_DIC(D) |
| 188 | MNPW_Z_TSL_CUT_IND_RSLT1 | NUMBER | Y |  |  | 空 |
| 189 | MNPW_Z_TSL_CUT_IND_RSLT2 | NUMBER | Y |  |  | 空 |
| 190 | MNPW_Z_TSL_CUT_IND_RSLT3 | NUMBER | Y |  |  | 空 |
| 191 | MNPW_Z_TSL_CUT_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 192 | MNPW_Z_TSL_CUT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 193 | MNPW_Z_TSL_CUT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 194 | MNPW_Z_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 195 | MNPW_Z_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 196 | MNPW_Z_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 197 | MNPW_Z_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 198 | MNPW_Z_TSL_CT_EX_RA_RSLT | NUMBER | Y |  |  | 空 |
| 199 | MNPW_Z_TSL_CT_EX_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 200 | MNPW_HIGH_TEMP_TSL_STAND_CD | VARCHAR2(20) | Y |  |  | 空 |
| 201 | MNPW_HIGH_TEMP_TSL_TEMP_RSLT | NUMBER | Y |  |  | 空 |
| 202 | MNPW_HIGH_TEMP_TSL_TS_RSLT | NUMBER | Y |  |  | 空 |
| 203 | MNPW_HIGH_TEMP_TSL_TS_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 204 | MNPW_HIGH_TEMP_TSL_YP_TY | VARCHAR2(1) | Y |  |  | 空 |
| 205 | MNPW_HIGH_TEMP_TSL_YP_RSLT | NUMBER | Y |  |  | 空 |
| 206 | MNPW_HIGH_TEMP_TSL_YP_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 207 | MNPW_HIGH_TEMP_TSL_EL_CD | VARCHAR2(1) | Y |  |  | 空 |
| 208 | MNPW_HIGH_TEMP_TSL_EL_RSLT | NUMBER | Y |  |  | 空 |
| 209 | MNPW_HIGH_TEMP_TSL_EL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 210 | MNPW_HIGH_TEMP_TSL_RA_RSLT | NUMBER | Y |  |  | 空 |
| 211 | MNPW_HIGH_TEMP_TSL_RA_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 212 | MNPW_SSCC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 213 | MNPW_SSCC_STRESS_TY | VARCHAR2(1) | Y |  |  | 空 |
| 214 | MNPW_SSCC_STRESS_TST_VAL_RSLT | NUMBER | Y |  |  | 空 |
| 215 | MNPW_SSCC_STRESS_TST_VAL_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 216 | MNPW_SSCC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 217 | MNPW_HIC_SMP_TRANS_STAND | VARCHAR2(20) | Y |  |  | 空 |
| 218 | MNPW_HIC_SOLUTION_KIND | VARCHAR2(20) | Y |  |  | 空 |
| 219 | MNPW_HIC_CLR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 220 | MNPW_HIC_CLR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 221 | MNPW_HIC_CLR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 222 | MNPW_HIC_CLR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 223 | MNPW_HIC_CLR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 224 | MNPW_HIC_CLR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 225 | MNPW_HIC_CLR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 226 | MNPW_HIC_CLR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 227 | MNPW_HIC_CLR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 228 | MNPW_HIC_CLR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 229 | MNPW_HIC_CLR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 230 | MNPW_HIC_CLR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 231 | MNPW_HIC_CLR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 232 | MNPW_HIC_CLR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 233 | MNPW_HIC_CLR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 234 | MNPW_HIC_CLR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 235 | MNPW_HIC_CSR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 236 | MNPW_HIC_CSR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 237 | MNPW_HIC_CSR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 238 | MNPW_HIC_CSR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 239 | MNPW_HIC_CSR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 240 | MNPW_HIC_CSR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 241 | MNPW_HIC_CSR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 242 | MNPW_HIC_CSR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 243 | MNPW_HIC_CSR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 244 | MNPW_HIC_CSR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 245 | MNPW_HIC_CSR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 246 | MNPW_HIC_CSR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 247 | MNPW_HIC_CSR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 248 | MNPW_HIC_CSR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 249 | MNPW_HIC_CSR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 250 | MNPW_HIC_CSR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 251 | MNPW_HIC_CTR_EACH1_RSLT1 | NUMBER | Y |  |  | 空 |
| 252 | MNPW_HIC_CTR_EACH1_RSLT2 | NUMBER | Y |  |  | 空 |
| 253 | MNPW_HIC_CTR_EACH1_RSLT3 | NUMBER | Y |  |  | 空 |
| 254 | MNPW_HIC_CTR_EACH2_RSLT1 | NUMBER | Y |  |  | 空 |
| 255 | MNPW_HIC_CTR_EACH2_RSLT2 | NUMBER | Y |  |  | 空 |
| 256 | MNPW_HIC_CTR_EACH2_RSLT3 | NUMBER | Y |  |  | 空 |
| 257 | MNPW_HIC_CTR_EACH3_RSLT1 | NUMBER | Y |  |  | 空 |
| 258 | MNPW_HIC_CTR_EACH3_RSLT2 | NUMBER | Y |  |  | 空 |
| 259 | MNPW_HIC_CTR_EACH3_RSLT3 | NUMBER | Y |  |  | 空 |
| 260 | MNPW_HIC_CTR_EACH_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 261 | MNPW_HIC_CTR_SPCMN_AVG1_RSLT | NUMBER | Y |  |  | 空 |
| 262 | MNPW_HIC_CTR_SPCMN_AVG2_RSLT | NUMBER | Y |  |  | 空 |
| 263 | MNPW_HIC_CTR_SPCMN_AVG3_RSLT | NUMBER | Y |  |  | 空 |
| 264 | MNPW_HIC_CTR_SPCMN_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 265 | MNPW_HIC_CTR_TOT_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 266 | MNPW_HIC_CTR_TOT_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 267 | MNPW_HARD_KIND | VARCHAR2(1) | Y |  |  | 空 |
| 268 | MNPW_HARD_AVG_RSLT | NUMBER | Y |  |  | 空 |
| 269 | MNPW_HARD_IND_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 270 | MNPW_HARD_AVG_JDG | VARCHAR2(1) | Y |  |  | 空 |
| 271 | MNPW_HARD_RSLT1 | NUMBER | Y |  | 硬度测试实绩4 | SCO_DATA_DIC(D) |
| 272 | MNPW_HARD_RSLT2 | NUMBER | Y |  | 硬度测试实绩5 | SCO_DATA_DIC(D) |
| 273 | MNPW_HARD_RSLT3 | NUMBER | Y |  | 硬度测试实绩6 | SCO_DATA_DIC(D) |
| 274 | MNPW_HARD_RSLT4 | NUMBER | Y |  | 硬度测试实绩4 | SCO_DATA_DIC(D) |
| 275 | MNPW_HARD_RSLT5 | NUMBER | Y |  | 硬度测试实绩5 | SCO_DATA_DIC(D) |
| 276 | MNPW_HARD_RSLT6 | NUMBER | Y |  | 硬度测试实绩6 | SCO_DATA_DIC(D) |
| 277 | MNPW_HARD_RSLT7 | NUMBER | Y |  | 硬度测试实绩7 | SCO_DATA_DIC(D) |
| 278 | MNPW_HARD_RSLT8 | NUMBER | Y |  | 硬度测试实绩8 | SCO_DATA_DIC(D) |
| 279 | MNPW_HARD_RSLT9 | NUMBER | Y |  | 硬度测试实绩9 | SCO_DATA_DIC(D) |
| 280 | MXPW_HARD_RSLT1 | NUMBER | Y |  | 硬度测试实绩4 | SCO_DATA_DIC(D) |
| 281 | MXPW_HARD_RSLT2 | NUMBER | Y |  | 硬度测试实绩5 | SCO_DATA_DIC(D) |
| 282 | MXPW_HARD_RSLT3 | NUMBER | Y |  | 硬度测试实绩6 | SCO_DATA_DIC(D) |
| 283 | MXPW_HARD_RSLT4 | NUMBER | Y |  | 硬度测试实绩4 | SCO_DATA_DIC(D) |
| 284 | MXPW_HARD_RSLT5 | NUMBER | Y |  | 硬度测试实绩5 | SCO_DATA_DIC(D) |
| 285 | MXPW_HARD_RSLT6 | NUMBER | Y |  | 硬度测试实绩6 | SCO_DATA_DIC(D) |
| 286 | MXPW_HARD_RSLT7 | NUMBER | Y |  | 硬度测试实绩7 | SCO_DATA_DIC(D) |
| 287 | MXPW_HARD_RSLT8 | NUMBER | Y |  | 硬度测试实绩8 | SCO_DATA_DIC(D) |
| 288 | MXPW_HARD_RSLT9 | NUMBER | Y |  | 硬度测试实绩9 | SCO_DATA_DIC(D) |
| 289 | Z1_TSL_CUT_IND_RSLT1 | VARCHAR2(10) | Y |  |  | 空 |
| 290 | Z1_TSL_CUT_IND_RSLT2 | VARCHAR2(10) | Y |  |  | 空 |
| 291 | Z1_TSL_CUT_IND_RSLT3 | VARCHAR2(10) | Y |  |  | 空 |
| 292 | Z1_TSL_CUT_AVG_RSLT | VARCHAR2(10) | Y |  |  | 空 |
| 293 | Z1_TSL_YP_RSLT | VARCHAR2(10) | Y |  |  | 空 |
| 294 | Z1_TSL_TS_RSLT | VARCHAR2(10) | Y |  |  | 空 |
| 295 | Z1_TSL_CT_EX_RA_RSLT | VARCHAR2(10) | Y |  |  | 空 |
| 296 | ESB_FLAG | VARCHAR2(1) | Y |  |  | 空 |
| 297 | ESB_DATE | VARCHAR2(14) | Y |  |  | 空 |
| 298 | PK_ID | VARCHAR2(45) | N |  | Interface Primay Key ID | SCO_DATA_DIC(D) |
| 299 | PK_ID_D | VARCHAR2(60) | Y |  |  | 空 |

### SCH_SLAB_DESIGN_ORD

- **Owner**：`MESAPUSER`（Oracle；同库同用户直接写表名，跨 schema 才加 `MESAPUSER.` 前缀）
- **画像**：P0｜中心度 SCORE=20｜被读 12 过程 / 被写 4 过程｜操作 DELETE/INSERT/UPDATE
- **行数(克隆库)**：2　**主键**：ORD_NO、ORD_LN　**语义覆盖**：141/146

| # | 字段 | 类型 | 空 | 主键 | 语义 | 来源 |
|---|------|------|----|----|------|------|
| 1 | CRT_USER_ID | VARCHAR2(20) | Y |  | 创建人 | DB注释(中文) |
| 2 | CRT_OBJ_ID | VARCHAR2(100) | Y |  | Created Object ID_ | DB注释(非中文) |
| 3 | CRT_TM | TIMESTAMP(7) | Y |  | 创建时间 | DB注释(中文) |
| 4 | UPD_USER_ID | VARCHAR2(20) | Y |  | 更新人 | DB注释(中文) |
| 5 | UPD_OBJ_ID | VARCHAR2(30) | Y |  | Updated Object ID_ | DB注释(非中文) |
| 6 | UPD_TM | TIMESTAMP(7) | Y |  | 更新时间 | DB注释(中文) |
| 7 | ARCHIVE_FL | VARCHAR2(1) | Y |  | Archive Flag_ | DB注释(非中文) |
| 8 | ORD_NO | VARCHAR2(10) | N | ✓ | 订单编号 | DB注释(中文) |
| 9 | ORD_LN | VARCHAR2(3) | N | ✓ | 订单行号 | DB注释(中文) |
| 10 | ORD_PROG_STS | VARCHAR2(2) | Y |  | 订单进程状态 | DB注释(中文) |
| 11 | HR_ROLL_UNIT_CD | VARCHAR2(1) | Y |  | ??Roll????_????Roll???? | DB注释(非中文) |
| 12 | ORD_QTY_TOL_TY | VARCHAR2(1) | Y |  | 重量偏差 | DB注释(中文) |
| 13 | ORD_QTY_TOL_MAX | NUMBER | Y |  | 重量偏差最大值 | DB注释(中文) |
| 14 | ORD_QTY_TOL_MIN | NUMBER | Y |  | 重量偏差最小值 | DB注释(中文) |
| 15 | ORD_LN_QTY | NUMBER | Y |  | 订单总重 | DB注释(中文) |
| 16 | BFHM | NUMBER | Y |  | 需投入量 | DB注释(中文) |
| 17 | BFHM_MIN | NUMBER | Y |  | 需投入量最小值 | DB注释(中文) |
| 18 | BFHM_MAX | NUMBER | Y |  | 需投入量最大值 | DB注释(中文) |
| 19 | SLAB_DGN_TOTAL_WGT | NUMBER | Y |  | 铸坯设计总重量 | DB注释(中文) |
| 20 | ORD_DLV_DT | VARCHAR2(8) | Y |  | 订单交货期 | DB注释(中文) |
| 21 | PLURAL_DGN_ORD_YN | VARCHAR2(1) | Y |  | 是否复数设计 | DB注释(中文) |
| 22 | POSS_PASS_PLANT_CD | VARCHAR2(30) | Y |  | 可通过工厂 | DB注释(中文) |
| 23 | CONF_PASS_PLANT_CD | VARCHAR2(30) | Y |  | 确定通过工厂 | DB注释(中文) |
| 24 | CC_FAC_FL | VARCHAR2(1) | Y |  | 连铸工厂 | DB注释(中文) |
| 25 | RLG_POSS_WGT_MAX | NUMBER | Y |  | 可轧制最大单重 | DB注释(中文) |
| 26 | CC_YIELD | NUMBER | Y |  | 连铸成材率 | DB注释(中文) |
| 27 | HR_YIELD | NUMBER | Y |  | 热轧成材率 | DB注释(中文) |
| 28 | HR_CRCTN_YIELD | NUMBER | Y |  | 热轧精整成材率 | DB注释(中文) |
| 29 | PPL_YIELD | NUMBER | Y |  | ??PPL ??_??PPL??? | DB注释(非中文) |
| 30 | PCM_YIELD | NUMBER | Y |  | ??PCM ??_??PCM??? | DB注释(非中文) |
| 31 | CAL_YIELD | NUMBER | Y |  | ??CAL ??_??CAL??? | DB注释(非中文) |
| 32 | CGL_YIELD | NUMBER | Y |  | ??CGL ??_??CGL??? | DB注释(非中文) |
| 33 | RCL_YIELD | NUMBER | Y |  | ??RCL ??_??RCL??? | DB注释(非中文) |
| 34 | TOT_YIELD | NUMBER | Y |  | 总成材率 | DB注释(中文) |
| 35 | CUST_CD | VARCHAR2(30) | Y |  | 订单用户代码 | DB注释(中文) |
| 36 | PROD_GRP | VARCHAR2(2) | Y |  | 品种 | DB注释(中文) |
| 37 | PROD_CD | VARCHAR2(3) | Y |  | 小品种 | DB注释(中文) |
| 38 | ORD_TY | VARCHAR2(2) | Y |  | 订单类型 | DB注释(中文) |
| 39 | DELV_COND_CD | VARCHAR2(2) | Y |  | 交接条件代码 | DB注释(中文) |
| 40 | URGENT_TY | VARCHAR2(1) | Y |  | 是否紧急订单 | DB注释(中文) |
| 41 | WGT_DCN_MTH_CD | VARCHAR2(2) | Y |  | 计重方式 | DB注释(中文) |
| 42 | PACK_PROD_WGT_CNT_CD | VARCHAR2(10) | Y |  | 包装单重及张数分类 | DB注释(中文) |
| 43 | PACK_PROD_WGT_CNT_MIN | NUMBER | Y |  | 包装重量下限 | DB注释(中文) |
| 44 | PACK_PROD_WGT_CNT_MAX | NUMBER | Y |  | 包装重量上限 | DB注释(中文) |
| 45 | PCKL_WELD_CD | VARCHAR2(3) | Y |  | ??????_?????? | DB注释(非中文) |
| 46 | SKINPASS_TY | VARCHAR2(1) | Y |  | 平整分类 | DB注释(中文) |
| 47 | STEEL_GRVT | NUMBER | Y |  | 密度 | DB注释(中文) |
| 48 | SPEC_CD | VARCHAR2(50) | Y |  | 国家标准及牌号 | DB注释(中文) |
| 49 | HR_TS_TGT | VARCHAR2(4) | Y |  | TS目标值 | DB注释(中文) |
| 50 | SURF_TREAT_CD | VARCHAR2(3) | Y |  | 粗糙度 | DB注释(中文) |
| 51 | PSTREAT_CD | VARCHAR2(2) | Y |  | 后处理方法代码 | DB注释(中文) |
| 52 | DIFF_TEMP_GRADE | VARCHAR2(2) | Y |  | ?????_????? | DB注释(非中文) |
| 53 | PACK_MTH_CD | VARCHAR2(5) | Y |  | 包装方式 | DB注释(中文) |
| 54 | INCMP_STEEL_NO | VARCHAR2(10) | Y |  | 内控钢种 | DB注释(中文) |
| 55 | ORD_USAGE | VARCHAR2(4) | Y |  | 订单用途 | DB注释(中文) |
| 56 | HRL_MFC_STD_NO | VARCHAR2(11) | Y |  | 热轧制造标准 | DB注释(中文) |
| 57 | CRL_MFC_STD_NO | VARCHAR2(11) | Y |  | ????????_???????? | DB注释(非中文) |
| 58 | QA_CRL_STEEL_CD | VARCHAR2(4) | Y |  | ????????_???????? | DB注释(非中文) |
| 59 | SMS_2ND_RFN_CD | VARCHAR2(3) | Y |  | 炼钢2次精炼代码 | DB注释(中文) |
| 60 | CC_CSTP_RESTRIC_CD | VARCHAR2(1) | Y |  | 铸坯指定代码 | DB注释(中文) |
| 61 | QLT_HCR_FL | VARCHAR2(1) | Y |  | 冷热送分类 | DB注释(中文) |
| 62 | CC_CSTP_REPAIR_TY | VARCHAR2(6) | Y |  | ????????_????scarfing?? | DB注释(非中文) |
| 63 | HRL_INT_SP_FL | VARCHAR2(1) | Y |  | ??????SkinPass??_??????????(SkinPass) | DB注释(非中文) |
| 64 | HRL_SP_COMPOSITE_FL | VARCHAR2(1) | Y |  | ????SkinPass??_????????(SkinPass) | DB注释(非中文) |
| 65 | CRL_ANN_GRD_CD | VARCHAR2(3) | Y |  | ????Grade??_????Grade?? | DB注释(非中文) |
| 66 | HRL_PROD_THK_AIM | NUMBER | Y |  | 轧制目标厚度 | DB注释(中文) |
| 67 | HRL_PROD_WTH_AIM | NUMBER | Y |  | 轧制目标宽度 | DB注释(中文) |
| 68 | HRL_THK_SET_AIM | NUMBER | Y |  | 热轧厚度Set目标值 | DB注释(中文) |
| 69 | HRL_THK_SET_TOL_MIN | NUMBER | Y |  | 热轧厚度Set允许公差下限 | DB注释(中文) |
| 70 | HRL_THK_SET_TOL_MAX | NUMBER | Y |  | 热轧厚度Set允许公差上限 | DB注释(中文) |
| 71 | ORD_THK | NUMBER | Y |  | 订单厚度 | DB注释(中文) |
| 72 | ORD_WTH | NUMBER | Y |  | 订单宽度 | DB注释(中文) |
| 73 | PROD_CALC_UNIT_WGT | NUMBER | Y |  | ????_???? | DB注释(非中文) |
| 74 | CC_CSTP_COOLING_TY | VARCHAR2(1) | Y |  | 连铸铸片冷却方式 | DB注释(中文) |
| 75 | SLAB_DGN_WTH_RNG_MIN | NUMBER | Y |  | 铸坯设计宽度最小值 | DB注释(中文) |
| 76 | SLAB_DGN_WTH_RNG_MAX | NUMBER | Y |  | 铸坯设计宽度最大值 | DB注释(中文) |
| 77 | SLAB_DGN_LTH_RNG_MIN | NUMBER | Y |  | 铸坯设计长度最小值 | DB注释(中文) |
| 78 | SLAB_DGN_LTH_RNG_MAX | NUMBER | Y |  | 铸坯设计长度最大值 | DB注释(中文) |
| 79 | SLAB_DGN_AIM_WGT | NUMBER | Y |  | 铸坯设计目标重量 | DB注释(中文) |
| 80 | SLAB_DGN_WGT_RNG_MIN | NUMBER | Y |  | 铸坯设计重量最小值 | DB注释(中文) |
| 81 | SLAB_DGN_WGT_RNG_MAX | NUMBER | Y |  | 铸坯设计重量最大值 | DB注释(中文) |
| 82 | SLAB_DGN_PCS | NUMBER | Y |  | 铸坯设计件数 | DB注释(中文) |
| 83 | SLAB_DGN_DIV_PCS | NUMBER | Y |  | 分卷数 | DB注释(中文) |
| 84 | SLAB_DGN_NORMAL_YN | VARCHAR2(1) | Y |  | 铸坯设计是否正常标记 | DB注释(中文) |
| 85 | PACK_CONV_SLAB_WGT_MIN | NUMBER | Y |  | ????Slab??Min_ | DB注释(非中文) |
| 86 | PACK_CONV_SLAB_WGT_MAX | NUMBER | Y |  | ????Slab??Max_ | DB注释(非中文) |
| 87 | SLAB_DGN_REQ_WGT_MIN | NUMBER | Y |  | 铸坯设计需求重量最小值 | DB注释(中文) |
| 88 | SLAB_DGN_REQ_WGT_MAX | NUMBER | Y |  | 铸坯设计需求重量最大值 | DB注释(中文) |
| 89 | SLAB_DGN_REQ_WGT | NUMBER | Y |  | 铸坯设计需求重量 | DB注释(中文) |
| 90 | SLAB_DGN_THK | NUMBER | Y |  | 铸坯设计厚度 | DB注释(中文) |
| 91 | SLAB_DGN_WTH | NUMBER | Y |  | 铸坯设计宽度 | DB注释(中文) |
| 92 | SLAB_DGN_LTH | NUMBER | Y |  | 铸坯设计长度 | DB注释(中文) |
| 93 | SLAB_DGN_WGT | NUMBER | Y |  | 铸坯设计重量 | DB注释(中文) |
| 94 | SLAB_DGN_REQ_WGT_ADD_FL | VARCHAR2(1) | Y |  | SLAB?????????_ | DB注释(非中文) |
| 95 | CMP_QCERT_NO | VARCHAR2(11) | Y |  | 公司保证编号(材质记号) | DB注释(中文) |
| 96 | TS_GRD | VARCHAR2(4) | Y |  | TS_Grade_TS_Grade | DB注释(非中文) |
| 97 | ORD_COAT_WGT_CD | VARCHAR2(7) | Y |  | 订单镀锌量代码 | DB注释(中文) |
| 98 | ORD_EDGE_TY | VARCHAR2(1) | Y |  | 订单切边分类 | DB注释(中文) |
| 99 | SAME_WTH_CD | NUMBER | Y |  | ?????_ | DB注释(非中文) |
| 100 | SAME_WTH_LIMIT_CNT | NUMBER | Y |  | ??? ????_ | DB注释(非中文) |
| 101 | SAME_THK_CD | NUMBER | Y |  | ??????_ | DB注释(非中文) |
| 102 | SAME_THK_LIMIT_CNT | NUMBER | Y |  | ????????_ | DB注释(非中文) |
| 103 | ROLL_THK_ALLOW_MIN | NUMBER | Y |  | ROLL????MIN_ | DB注释(非中文) |
| 104 | ROLL_THK_ALLOW_MAX | NUMBER | Y |  | ROLL????MAX_ | DB注释(非中文) |
| 105 | SLAB_DGN_MSG | VARCHAR2(500) | Y |  | 铸坯设计信息提示 | DB注释(中文) |
| 106 | HTM_MTH_CD | VARCHAR2(1) | Y |  | 交货状态（厚板） | DB注释(中文) |
| 107 | TARGET_FL | VARCHAR2(1) | Y |  | 对象区分 | DB注释(中文) |
| 108 | DE_P_YN | VARCHAR2(1) | Y |  | 脱磷作业分类 | DB注释(中文) |
| 109 | BFHM_OLD | NUMBER | Y |  | 原需投入量 | DB注释(中文) |
| 110 | ADD_QTY | NUMBER | Y |  | 追加量 | DB注释(中文) |
| 111 | ORD_LN_PCS | NUMBER | Y |  | 订单件数 | DB注释(中文) |
| 112 | BFHMQ | NUMBER | Y |  | 需投入钢板张数 | DB注释(中文) |
| 113 | BFHMQ_MIN | NUMBER | Y |  |  | 空 |
| 114 | BFHMQ_MAX | NUMBER | Y |  |  | 空 |
| 115 | STD_STLGRD | VARCHAR2(20) | Y |  | 牌号 | DB注释(中文) |
| 116 | INSP_AGENCY_CD | VARCHAR2(3) | Y |  | 检查机构代码 | DB注释(中文) |
| 117 | TRNSF_MTH_CD | VARCHAR2(2) | Y |  | 运输方式 | DB注释(中文) |
| 118 | UST_MTH_CD | VARCHAR2(2) | Y |  | 探伤 | DB注释(中文) |
| 119 | PLT_HEATING_CD | VARCHAR2(1) | Y |  | 热处理方式 | DB注释(中文) |
| 120 | PLT_PROD_LTH_AIM | NUMBER | Y |  | 长度 | DB注释(中文) |
| 121 | TE_PIC_SMP_INDI_SMP_CD | VARCHAR2(7) | Y |  | ¿¿¿¿¿¿Sampling¿¿ | SCO_DATA_DIC(D) |
| 122 | GAS_CUT_FL | VARCHAR2(1) | Y |  | GAS절단구분 | SCO_DATA_DIC(D) |
| 123 | PLT_YIELD | NUMBER | Y |  |  | 空 |
| 124 | SMS_MFC_STD_NO | VARCHAR2(15) | Y |  | 炼钢制造标准 | DB注释(中文) |
| 125 | ORD_SIZE_TY | VARCHAR2(1) | Y |  | 定尺类型 | DB注释(中文) |
| 126 | ORD_WTH_MAX | NUMBER | Y |  | 订单宽度最大值 | DB注释(中文) |
| 127 | ORD_LTH_MAX | NUMBER | Y |  | 订单长度最大值 | DB注释(中文) |
| 128 | ORD_LTH_TOL_CD | VARCHAR2(1) | Y |  | 订单长度公差指定代码 | DB注释(中文) |
| 129 | ORD_LTH_TOL_MIN | NUMBER | Y |  | 订单长度下偏差 | DB注释(中文) |
| 130 | ORD_LTH_TOL_MAX | NUMBER | Y |  | 订单长度上偏差 | DB注释(中文) |
| 131 | ORD_PLT_CD | VARCHAR2(1) | Y |  | 厚板产线 | DB注释(中文) |
| 132 | ORD_LTH | NUMBER | Y |  | 订单长度 | DB注释(中文) |
| 133 | DGN_OVROLL_QTY | NUMBER | Y |  | 余材支数 | DB注释(中文) |
| 134 | DGN_OVROLL_WGT | NUMBER | Y |  | 余材重量 | DB注释(中文) |
| 135 | CCM_NO | VARCHAR2(1) | Y |  | 连铸机号 | DB注释(中文) |
| 136 | PLT_THK_CD | VARCHAR2(2) | Y |  |  | 空 |
| 137 | PLT_WTH_CD | VARCHAR2(2) | Y |  |  | 空 |
| 138 | DGN_PLT_LTH | NUMBER | Y |  | 钢板设计长度 | DB注释(中文) |
| 139 | DGN_PLT_WTH | NUMBER | Y |  | 钢板设计宽度 | DB注释(中文) |
| 140 | DGN_PLT_WGT | NUMBER | Y |  | 钢板设计重量 | DB注释(中文) |
| 141 | DGN_MPLT_CNT | NUMBER | Y |  | 设计母块数 | DB注释(中文) |
| 142 | DGN_TOT_PLT_WGT | NUMBER | Y |  | 设计总重量 | DB注释(中文) |
| 143 | HRL_PROD_FTHK_AIM | NUMBER | Y |  | 型钢腹板厚度 | DB注释(中文) |
| 144 | HRL_PROD_YTHK_AIM | NUMBER | Y |  | 型钢翼缘厚度 | DB注释(中文) |
| 145 | ORD_FTHK | NUMBER | Y |  | 订单腹板厚度 | DB注释(中文) |
| 146 | ORD_YTHK | NUMBER | Y |  | 订单翼缘厚度 | DB注释(中文) |
