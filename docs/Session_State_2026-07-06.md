# 会话状态 / 交接 · 2026-07-06

> 本文件为工作状态快照，供恢复/交接。记录：进度、交付物、关键发现、产物位置（含临时产物再生成命令）、未决事项、恢复指南。

## 一、当前进度

| 阶段 | 状态 |
|------|------|
| Sprint 0–2（ITSM 验证版）| 已完成（develop 分支历史）|
| **计划调整（真实 MES 接入）** | ✅ 方案定稿草稿 `docs/Plan_Adjustment_RealMES_2026.md` |
| **Sprint 2.9 工具链（自省/治理/分析/对账）** | ✅ 5 工具全部完成 + 真实库验证 |
| **S2.9 资产盘点 + 字典对账** | ✅ `docs/MES_Asset_Census_2026.md`（真实数据）|
| **Sprint 3 训练方案** | ✅ 草稿 `docs/Sprint3_Training_Plan_2026.md` |
| **S3-0 素材前置**（建图/P0 选取/代码字典/P0 深析/大包切分）| ✅ 全部落地（工具产物在 scratchpad）|
| S3-1/S3-2 实际 AI 训练 | ⬜ 未开始（需脱敏链路 + 评审需求单 + 调用 Kimi）|

## 二、交付物（均在 develop 分支，**未提交**）

**文档**（`docs/`）：
- `Plan_Adjustment_RealMES_2026.md` — 计划调整方案（含两轮实测发现）
- `MES_Asset_Census_2026.md` — 资产盘点 + 字典对账
- `Sprint3_Training_Plan_2026.md` — Sprint 3 训练方案（含 S3-0 落地进展 + 素材质量结论）
- `Session_State_2026-07-06.md` — 本文件

**工具**（`scripts/kb-ingest/`，纯 stdlib，除 db_introspect 需 `oracledb`；**kb-ingest 全套 148 单测通过**）：
| 工具 | 职责 |
|------|------|
| `db_introspect.py` | Oracle 自省（`--no-source`/`--use-dba`/`--source-units-file`；批量取行）|
| `encoding_normalizer.py` | 注释乱码修复 + 三级分级 |
| `proc_parser.py` | PL/SQL 静态分析（读写表/调用/状态流转/PII/动态SQL）|
| `dependency_graph.py` | 依赖图谱 + P0 分级 + 环检测 |
| `dict_reconcile.py` | 自省 × 字典 CSV 对账 |
| `build_dep_graph.py` | 全量建图编排（内存安全批处理）|
| `plsql_splitter.py` | 大包按子程序切分 |
| `README.md` | 工具链说明书 |

## 三、关键发现（真实库 Oracle 21c XE / XEPDB1 / AL32UTF8）

1. **规模**：MESAPUSER 1860 表 / 75965 字段 / **PL/SQL 193 万行 / 9160 单元**（4563 包 + 4421 包体）；SCOAPUSER 74 表 / 191 单元。这是一套**钢板/卷材钢厂 MES（韩系）**。
2. **克隆库列注释全空** → 字典 CSV 是唯一列语义源（59199 列可反哺）；PL/SQL 源码内含可读注释（中/英/韩混合）。
3. **依赖图谱**（修正后）：过程 5101 / 表 2249 / 环 77。高中心度核心包体：BSCT_COST、BSQM_MTC_ISSUE、BSCH_PROD_INST、BSMS_OPER_BOF、BSPR_HEAT_FCE。
4. **P0 选取**：百分位分级在万级图上撑到 2117（不可用）→ 改用中心度 Top-N（Top100 表 + Top60 包体）。
5. **代码字典** `SCOAPUSER.SCO_CODE_DETAIL`（13620 行）= 解码表且**自带中韩双语**（CD_NM 中/CD_DESC 韩），兼作术语表。
6. **训练素材**：Top60 P0 包体 221156 行；14 大包切成 1401 子程序单元；源码 0 真实硬编码（脱敏聚焦数据样本）。
7. **工具经真实脏库硬化**：proc_parser 修 3 处调用误判（类型名/子程序定义头/外连接 `(+)`）；db_introspect 加批量取行（MESAPUSER 结构 28s）。

## 四、临时产物（scratchpad，**会话结束会丢失** → 用下方命令再生成）

产物目录：`scratchpad/`（会话隔离）
- `meta_mes_nosrc.json`（22MB，MESAPUSER 结构）、`meta_p0.json`（33MB，Top60 P0 源码）
- `graph_mes3/`（core_assets.md / tables.csv / procs.csv / p0_units.txt / p0_phase1_tables.txt / p0_phase1_units.txt）
- `split_all.json`（1401 子程序单元）、`split_report.md`
- `sco_code_detail.csv`（中韩解码字典）、`sco_code_master.csv`、`sco_data_dic.csv`
- `注释乱码清单`、`discrepancies_mes.csv`（对账差异）

> 这些是**生成数据**，不入库；DB 在线时可随时重跑再生成。

## 五、恢复指南

**DB 连接**（口令由用户单独提供，**不入库不写文件**，仅运行时 env）：
```bash
# DB 在 100.84.68.115（另一台机，本机 10.8.0.13，LAN 可达），Oracle 21c XE
export MES_DB_USER=SYSTEM MES_DB_PASSWORD=<用户提供> MES_DB_DSN='100.84.68.115:25521/XEPDB1'
pip install --user --break-system-packages oracledb pytest   # 本机 PEP668
```

**再生成 S3-0 全部产物**（scratchpad 或指定目录）：
```bash
cd scripts/kb-ingest
# 1) 结构盘点
python3 db_introspect.py --owner MESAPUSER --no-source --use-dba --out meta_mes_nosrc.json
# 2) 全量建图 → P0（约7分钟）
python3 build_dep_graph.py --owner MESAPUSER --use-dba --out-dir graph_mes
# 3) 拉 Top60 P0 源码
python3 db_introspect.py --owner MESAPUSER --use-dba --source-units-file graph_mes/p0_phase1_units.txt --out meta_p0.json
# 4) 大包子程序切分
python3 plsql_splitter.py --input meta_p0.json --out-json split_all.json --out-report split_report.md
# 5) 代码字典导出（见 census 报告附的查询）/ 字典对账
python3 dict_reconcile.py --introspect meta_mes_nosrc.json --dict-csv ../../docs/data_dictionary_full.csv --out-report 对账.md
python3 -m pytest tests/ -q   # 148 通过
```

## 六、未决事项（待用户 / TL）

1. **是否 git 提交**这批成果？（CLAUDE.md 5.4 要求 `[REQ-MES-AI-YYYYMMDD-XXX]` 需求单号 + 分类型）
2. **P0 规模**：Phase-1 用 Top100 表 + Top60 包体，首周按 Token 消耗校准。
3. **韩文处理深度**：P0 术语精校 vs 全量译。
4. **是否开始调用 Kimi 训练**（S3-1/S3-2）——涉及外部 AI + 脱敏 + 需评审需求单。
5. 工具小优化（非阻塞）：`dependency_graph` P0 绝对上限；`proc_parser` long_number 启发式；`plsql_splitter` 14% 裸END 回退。

---

*会话状态快照 · 2026-07-06 · 记忆见 `.claude/.../memory/mes-real-db-pivot.md`*
