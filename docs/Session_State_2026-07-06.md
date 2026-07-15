# 会话状态 / 交接 · 2026-07-06（末次更新 2026-07-15）

> 本文件为工作状态快照，供恢复/交接。记录：进度、交付物、关键发现、产物位置（含临时产物再生成命令）、未决事项、恢复指南。

> **2026-07-14~15 本轮交付索引**（详见下方各「增量」段，全部已提交并同步 origin + 远程机，HEAD `08cf2d1`）：
> ① 远程开发机+venv 就绪　② 真实库新 IP `10.30.10.111:25521/XEPDB1`（仅远程可达）+ 中韩英术语对照表
> ③ S3-0 全套素材落远程持久目录 `/home/xintong/mes-s3-data/s3-0/` + 一键 `regen_s3_0.sh`（8步可复现）
> ④ P0 表卡片 95 张（语义 87%）　⑤ 脱敏链路补全 7 类 + 素材审计认证「可外发」（0 命中）
> **当前状态**：⭐ **S3-1/S3-2 批训练完成 + 验收前置全交付 + RAG 调优 + S3-3 状态机起步（2026-07-15）**。见「增量⑥/⑦」。已推送 origin + 远程同步（HEAD 见增量⑦）。

## ★ 2026-07-15 增量⑥：S3-1/S3-2 批训练已执行（调 Kimi 实训）

- **需求单**：新建 `docs/REQ-MES-AI-20260715-001_批训练需求单.md`（TL+IT 授权，含**今日预算红线临时授权**留痕：§12 300万→临时 8M 闸，实际用 3.83M，明日恢复）。
- **驱动**：新增 `scripts/kb-ingest/run_s3_training.py`——经 ai-gateway `/v1/ai/chat`（脱敏门强制）跑 Kimi 理解训练；支持 `--phase tables/procs/smoke`、`--dedup/--shards/--shard-id/--proc-max-tokens/--missing`（可复现/续跑/补漏）。
- **认证**：IT 给的 Kimi 平台 key 放远程 `kimikey`（sk-，51位，运行时 env，不落盘；已加 `.gitignore`+`.git/info/exclude` 双重忽略。注意：远程 `~/.kimi-code` OAuth 是另一套、未用）。
- **结果**：**表 95/95、存储过程 1308/1309（99.9%）**，总 **3.83M tokens**。质量抽检好（韩文语义译中、状态字段标待解码、零臆断）。
- **产物**（远程持久，非仓库）：`/home/xintong/mes-s3-data/s3-train/{tables,procs}/*.md` + `_index_*.jsonl`；报告 `docs/S3-1_表字段理解报告.md`、`docs/S3-2_存储过程理解报告.md`。
- **网关起法**（远程）：`bash /home/xintong/mes-s3-data/orch2.sh`（重启高预算网关→3分片全量procs→128k补超宽表）；单跑：起 uvicorn（env 注入 AI_API_KEY/AI_MODEL）后 `AI_GATEWAY_URL=http://127.0.0.1:8000 python run_s3_training.py --phase ...`。
- **验收前置进展（2026-07-15 续）**：
  - ✅ **补跑 1+13**：procs 1308→**1314**（剩 ~8 个 >4000 行 fallback 段待二次切分）。
  - ✅ **断言种子**(T3-4-2)：`build_assertion_seeds.py` 从 proc_parser 静态分析确定性产 **657 条**→`/assertions/{state-machine,sql-logic,api-behavior}`（Critical 89主键/High 171状态流转/Medium 397），已提交；纳基准库须 TL 审批。
  - ✅ **RAG 入库**：`ingest_s3_cards.py`（复用多语言 embedding，§14 合规）→95表+1314过程=**4339 chunk** 入集合 `mes_s3_understanding`（落 `scripts/kb-ingest/data/chromadb`，gitignored 可重生成）；过程召回 0.7+。**⚠️ gotcha**：远程内网不通 huggingface，须 `HF_ENDPOINT=https://hf-mirror.com` 拉模型（已缓存）。
- （增量⑥的「仍未决」已在增量⑦全部推进，见下。）

## ★ 2026-07-15 增量⑦：验收前置全交付 + RAG 检索调优 + S3-3 状态机（T3-3-1）

> 本轮全部已提交并推送 origin + 远程逐文件核对同步，**HEAD `aab1555`**（+ 会话状态本次提交）。今日累计 Token ≈**3.95M**（训练3.83M + SQL验证66.8K + 标签26K + 状态机24K；TL 授权临时超 §12 至 8M，明日恢复）。

**验收前置（承接增量⑥「仍未决」）**：
- ✅ **SQL 场景验证**(T3-1-4/5)：`run_sql_validation.py`（6模块×5=30题锚定真实表→RAG召回→Kimi出SQL→规则自动初评）。产 `docs/S3-1_SQL验证报告.md`，自动初评均分 69.9/100；**人工语义终评≥85% 待 TL**（每题带评分列）。**暴露表选择偏弱**→触发下方 RAG 调优。
- ✅ **BIZ 抽检单**(T3-2-4)：`build_biz_sample.py` 分层抽样 → `docs/S3-2_BIZ抽检抽样单.md`（40条，10模块，待 BIZ 填「正确/部分/错误」）。
- ✅ **rag_service 查询端**：`retrieve_for_mes[_table/_proc]` 接 `mes_s3_understanding`，§14 合规（同模型+显式 query_embeddings），49 测试通过。

**RAG 表召回调优（表级 Top-3 命中 ~1/10 → 7/10）**：
- 锚点 chunk（`ingest_s3_cards.py`：每卡片加「表名+用途+字段中文语义」摘要块）+ 按表去重（`rag_service`）→ 5/10。集合重入库为 **5155 chunk**。
- **标签驱动 hybrid**：`build_table_labels.py` 用 Kimi 抽95表中文名+别名→`src/ai-gateway/app/services/mes_table_labels.json`；`retrieve_for_mes` = 向量去重 + 标签 bigram 词法经 **RRF 融合**（无标签自动降级）→ **7/10**。剩3个真歧义长尾（钢卷/热卷、客户/产品「主数据」）。
- 曾试朴素 bigram 全文 hybrid，反降到 2-3/10（样板话噪声），已弃；标签驱动才有效。

**S3-3 业务流程理解（以过程为锚）起步**：
- ✅ **T3-3-1 状态机反推**：`run_s3_state_machine.py` 从过程 `set_assignments`（列=字面量状态写入）反推 + SCO 代码字典(`glossary_code_mapping.csv`)解码 + Kimi 合成。产 `docs/S3-3_业务流程理解报告.md`（**34 状态字段**：质保书 MTC_STS_CD 2→9 由签发过程触发、计划 PLAN_ROLL_STS、炉次 HEAT_STS…）+ 34 卡片落远程 `s3-train/state_machine/`。**局限**：静态只捕字面量赋值，变量赋值状态不可见（已标「待确认」）。
- ✅ **T3-3-2 追溯链路**：`run_s3_traceability.py` 从**表结构（同表共键=血缘桥表）+ P0 过程读写血缘**反推批次/卷/试样跨表跨过程追溯链 + Kimi 合成【正向/反向追溯 + 关键桥接点 + 断点待确认】。追溯脊：订单`ORD_NO`→计划炉次`PLAN_HEAT_NO`→浇铸`CAST_NO`/炉次`HEAT_NO`→板坯`SLAB_NO`→钢板`PLT_NO`/钢卷`COIL_NO`→试样`SMP_NO`→质保`MTC_NO`→捆包`BUND_NO`（14 核心键实测全在库，13 条边全有证据）。产 S3-3 报告**第二部分**（幂等追加，marker `<!-- T3-3-2-TRACEABILITY -->`；含核心实体载体画像+13边明细+全链路总览）+ 13 卡片落远程 `s3-train/traceability/`，21.6K tokens。**关键发现**：PLT→MTC 无直接桥表(0)须经 SMP 中转（总览已标断点）；PLT_NO 84 表集中 SPR 精整、MTC_NO 全在 SQM 质量、HEAT_NO 集中 SMS 炼钢——子系统归属自洽。**局限**：桥过程仅 Top60 P0 覆盖(120 单元)、动态 SQL 不可见（已标「待确认」）。+14 单测（`test_traceability.py`，kb-ingest 全套 **193 通过**）。
- ⬜ **S3-3 未完**：T3-3-3 核心流程(BSQM/BSCH)、T3-3-4 验证题≥15、T3-3-5 报告完稿。

**Phase-1 就绪清单**：`docs/Phase1_验收就绪清单.md`（DoD 逐项三态核对 + 交付物 + TL 复现入口）。**明确 Phase-1 尚未可签字验收**——缺 S3-3 完整 + 三项人工评分 + ITM 签字。

**仍待人工/未完**：SQL 人工终评≥85%、BIZ 抽检填写、断言纳基准库审核、ITM 签字；S3-3 T3-3-3~5；~8 超大过程二次切分；hybrid 泛化后缀去噪。

**网关起法（复用）**：远程脚本 `bash /home/xintong/mes-s3-data/{sqlval,labels,statemachine,trace}.sh`（各自含重启网关）；RAG 入库 `bash rag_ingest.sh`。均需 `kimikey` + `HF_ENDPOINT=https://hf-mirror.com`。

## ★ 2026-07-14 增量⑤：脱敏链路已补全 + 训练素材审计认证「可外发」

- **补全脱敏引擎**：`src/ai-gateway/app/services/desensitize.py` 从 Sprint1 的 3 类存根 → **CLAUDE.md 4.2 全 7 类**（DB连接串/内网IP/身份证/工号/批次/厂区/设备SN）。网关（唯一外发咽喉）已在调它，故补全即全链路生效。新增 `desensitize_verbose()` 供审计。
- **精准锚定，防误伤业务语义**（关键）：厂区码仅匹配 `FAB-XX-NN`，**不抹钢厂厂区码 LZ/RZ/SHIP**；内网IP 仅私网/CGNAT 段，不误判版本号 `2.1.2.1`；设备SN 按 CLAUDE.md 带星号示例 `AB****3456` 匹配，**不误伤业务码 MSG00108/SPGC0030**。
- **新增审计门** `scripts/desensitize/audit_materials.py`（复用同一引擎，单一真源）：对 P0源码/表卡片/术语表逐条审，产 `desensitize_audit_report.md`，含 `--strict` CI 门禁。
- **真实素材审计闭环**：首轮 846 命中（IP版本号8 + DEVICE_SN业务码838）经核验**全为误报** → 收紧规则后**重跑 0 命中** → 报告结论「✅ 素材可外发」。证实 P0 源码 0 真实 PII（与历史发现一致）。
- 已并入 `regen_s3_0.sh`（现 **8 步**，末步自动出审计报告）。产物 `docs/desensitize_audit_report.md`（合规证据，已提交）。
- 单测：ai-gateway +20 脱敏 / desensitize +6 审计；**全套 234 通过**。

## ★ 2026-07-14 增量④：P0 表卡片已生成（T3-1 素材）

- **新增 `scripts/kb-ingest/build_table_cards.py`**（+11 单测，全套 179 通过）：为 Top100 P0 表拼装表卡片 = **结构**（盘点 JSON）+ **列语义**（字典 CSV，克隆库注释全空故字典是唯一源）+ **热度画像**（依赖图 tables.csv：被读/写过程数、操作、中心度）。纯本地、**未调外部 AI**。
- **实跑结果**：**95 张卡片**（Top100 中 5 张为视图/SCOAPUSER 表正确排除：VW_*、SCO_CODE_DETAIL）；字段 **13072**，**语义覆盖 87%**（11430，缺口 1642）。
- 卡片头部含**防前缀误导须知**（CLAUDE.md 14.2 精神，Oracle 版）：P0 表属 `MESAPUSER`，同用户直接写表名，勿把 owner 当表名前缀。
- 产物：`docs/p0_table_cards.md`（1.2MB，已提交，供 TL 评审 + RAG 切块）；机读 `p0_table_cards.jsonl`（远程持久目录，2MB，可重生成）。
- **已并入一键编排**：`regen_s3_0.sh` 扩为 7 步（末步生成表卡片），全流程仍一条命令可复现。

## ★ 2026-07-14 增量③：S3-0 全套素材已落远程持久目录 + 一键可复现

- **新增两脚本固化 S3-0 重生成**（已提交 commit 3850bd3，168 单测通过）：
  - `scripts/kb-ingest/select_p0_topn.py`：从 procs/tables.csv 按中心度取 Top60 包体 + Top100 表，**固化此前即席的 Top-N 选取**（解决 `p0_phase1` 名单不可复现的缺口）。
  - `scripts/kb-ingest/regen_s3_0.sh`：六步一键重生成（盘点→建图→选P0→拉源码→切分→对账）。
- **已在远程实跑，全套素材落 `/home/xintong/mes-s3-data/s3-0/`**（持久、非仓库，约 1 分钟跑完）：
  - `meta_mes_nosrc.json`(22MB,结构) / `meta_p0.json`(33MB,Top60源码) / `split_all.json`(1401子程序) / `split_report.md`
  - `graph_mes/`：`core_assets.md` / `procs.csv` / `tables.csv` / `p0_units.txt` / **`p0_phase1_units.txt`(Top60)** / `p0_phase1_tables.txt`(Top100)
  - `dict_reconcile_report.md` / `discrepancies.csv`(58508 差异) / glossary_*（增量②产物）
- **逐项复现历史基线**：建图 过程5101/表2249/环77；P0 核心包 BSCT_COST/BSQM_MTC_ISSUE/BSMS_OPER_BOF/BSPR_HEAT_FCE；切分 60包→1401子程序；最大包 BSCH_BATCHA_PLT_JOB2 15929行→44子程序。
- **一键重生成命令**（远程）：`MES_DB_USER=SYSTEM MES_DB_PASSWORD=<口令> MES_DB_DSN=10.30.10.111:25521/XEPDB1 PYTHON=/home/xintong/xintongmesai/.venv/bin/python bash scripts/kb-ingest/regen_s3_0.sh /home/xintong/mes-s3-data/s3-0`

## ★ 2026-07-14 增量②：真实库接入（新 IP）+ 中韩英术语对照表 T3-0-5 落地

- **真实库地址变更**：`10.30.10.111:25521/XEPDB1`（SYSTEM，Oracle 21c XE，MESAPUSER 1860 表，与原 `100.84.68.115` 同一套库换 IP）。**沙箱侧该网段不可达，仅远程测试机可达** → 一切接库操作走远程。口令仅运行时 env，不落盘。
- 远程 venv 已装 `oracledb 4.0.1`（不在钉版 requirements 内，单独装）。
- **T3-0-5 中韩英术语对照表已交付**（新工具 `scripts/kb-ingest/build_glossary.py` + 14 单测）：
  - 源 `SCOAPUSER.SCO_CODE_DETAIL`（use_yn=Y 12702 行）→ **逐格 Unicode 判语种**（不按列假设，因列≠语言）→ 去重 **9698 术语**。
  - 覆盖：含中 4498 / 含韩 2506 / 含英 4475 / **中韩齐全 574**；**三语齐全=0（结构性**：源表仅两列名字，第三语必缺）。
  - **重要事实**：该克隆字典已大量本地化为中文，**韩文仅约占 1/5**；英文缺口 5223、中文缺口 5200 = 后续 Kimi 补译 TODO（外部 AI，须训练需求单 + 脱敏，未决 #4）。
  - 纯 stdlib、**未调外部 AI**、无需求单阻塞。产物：`docs/glossary_zh_ko_en.md` + `docs/glossary_zh_ko_en.csv`（9698 术语，RAG 资产）。
  - 源码内韩文术语（非字典）未并入，属增量（需 `meta_p0.json` 重生成）。
  - 远程持久产物目录：`/home/xintong/mes-s3-data/s3-0/`（非仓库，可重生成）。

## ★ 2026-07-14 增量：远程开发机 + Python 环境就绪

本机配置低，**开发改为远程测试机为主**（编译/测试/训练走远程）。

- **远程机**：`ssh 100.95.76.81`（config 别名 `intranet-host`，用户 `xintong`，主机名 `onlyofficebak`）。免登录已配好，直连 IP 也免密。规格 **16 核 / 62G / 无 GPU / Ubuntu 22.04 / Python 3.10.12**。
- **项目目录**：`/home/xintong/xintongmesai`，从 `github.com/caoyb888/mesai.git` clone，同分支 `feature/real-mes-integration`（HEAD 与本机一致）。
- **Python 环境**：项目级 venv `/home/xintong/xintongmesai/.venv`。装了 `src/ai-gateway` + `scripts/kb-ingest` 两份 requirements，**23 个钉版全部满足**；torch 用 **CPU 版**（`2.13.0+cpu`，避开 2.5G CUDA 包）。远程原本无 pip、缺 `python3.10-venv`，已 `sudo apt` 补齐。
- **验证**：19 关键包导入 OK；**全部 177 用例真实跑通**（ai-gateway 29 passed / 覆盖 77%，kb-ingest 148 passed / 覆盖 52%※），0 失败 0 错误。
  - ※ kb-ingest 52% 是 `--cov` 把入库脚本（需真实 DB/Embedding）算进分母所致，被测解析器模块覆盖率本身高，非测试缺失。
- 无害提示：`wheel` 要 `packaging>=24` 但依赖钉 23.2，仅影响打包不影响运行。
- **日常用法**（不用 activate）：`ssh 100.95.76.81 'cd /home/xintong/xintongmesai && .venv/bin/pytest scripts/kb-ingest/tests -q'`；本机 push 后远程 `git pull` 同步。

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

## 〇、版本控制状态（2026-07-07 更新）

- 分支 **`feature/real-mes-integration`**（基于 develop），4 提交，需求单号 `REQ-MES-AI-20260706-001`（占位待补）。
- 已 push 到 `origin`；**PR #1**：https://github.com/caoyb888/mesai/pull/1 → 目标 develop，**待 TL 评审**。
- 提交拆分：feat(7工具+README) / test(6单测,148通过) / docs(4规划文档) / docs(2甲方字典)。

## 二、交付物（已提交至 `feature/real-mes-integration`，PR #1 待评审）

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

1. ~~是否 git 提交~~ → 已提交 feature 分支 + push + 建 PR #1；**待补正式需求单号**、待 TL 评审合并。
2. **P0 规模**：Phase-1 用 Top100 表 + Top60 包体，首周按 Token 消耗校准。
3. **韩文处理深度**：P0 术语精校 vs 全量译。
4. **是否开始调用 Kimi 训练**（S3-1/S3-2）——涉及外部 AI + 脱敏 + 需评审需求单。
5. 工具小优化（非阻塞）：`dependency_graph` P0 绝对上限；`proc_parser` long_number 启发式；`plsql_splitter` 14% 裸END 回退。

---

*会话状态快照 · 2026-07-06 · 记忆见 `.claude/.../memory/mes-real-db-pivot.md`*
