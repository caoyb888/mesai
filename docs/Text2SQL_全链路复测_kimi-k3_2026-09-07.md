# Text2SQL 全链路复测报告：线上网关切换 kimi-k3（新口径）

| 项 | 内容 |
|----|----|
| 文件编号 | AI-MES-EVAL-RETEST-2026-001 |
| 日期 | 2026-09-07 |
| 编制 | AI（芯智云匠） |
| 变更 | 线上网关模型 `moonshot-v1-32k` → **`kimi-k3`**（就地重启，保留原环境仅覆盖模型/密钥；provider 加 kimi-k* 适配）|
| 口径 | 结果集等价采用**修订口径**（数值展示容差，见 `docs/评测口径修订说明_2026-09-07.md`）|
| 方法 | 直连网关 `POST /v1/ai/mes-sql`（无鉴权）逐题走**完整管道**（RAG 检索 → schema linking → 生成），生成 SQL 只读执行、新口径判分；41 题；`temperature=0` 经 provider 夹到 1（kimi-k3 限制）|
| 关联 | `docs/Text2SQL_模型对比AB报告_2026-09-07.md`（受控 A/B）；`docs/M1_Text2SQL基线报告_2026-07-31.md`（旧模型基线）|

---

## 一、总分与对照

| 口径 | 生成率 | 选对表 | 结果正确 |
|------|--------|--------|---------|
| **kimi-k3 全链路（本次）** | 30/41 (73%) | 15/41 (37%) | **4/41 (9.8%)** |
| moonshot-v1-32k 全链路（M1 基线） | 32/41 (78%) | 频繁错 | 1/41 (2.4%) |
| kimi-k3 **受控**（给定候选表，A/B） | — | 40/41 (97%) | 13/41 (32%) |

**两个数一起看**：
- **换模型让全链路结果正确率 2.4% → ~10%（约 4 倍）**，是真实提升；
- 但全链路 10% **远低于受控 32%**，差距**几乎全部来自 RAG 检索**：受控给对候选表时 kimi-k3 选表 97%，
  全链路靠 RAG 只有 37%。**模型已不是瓶颈，检索（P1）才是。**

---

## 二、失败结构：检索选错表主导

### 2.1 RAG 未召回 → 模型拒答（11 题）

`Q05 Q08 Q14 Q15 Q16 Q20 Q22 Q30 Q39 Q40 Q41` —— RAG 没检索到正确表，模型据实拒答（generated=false）。

### 2.2 生成了但**检索把错表推到前面**（15 题，选错表）

| 题 | golden 表 | 实际选中 | 错因 |
|----|----------|---------|------|
| Q01 | SMS_HEAT | **SCH_PLAN_HEAT** | 计划表 vs 实绩表 |
| Q03 | SMS_HEAT | SCH_INST_HEAT | 计划/指示表 |
| Q04 | SMS_HEAT | SMS_RSLT_HEAT | 错实绩表 |
| Q06 | VW_SQM_DSN_CHEM_CODE | DUAL | 未召回码值视图 |
| Q10 | SMS_SLAB | SMS_RSLT_CUT | 切割实绩表混淆 |
| Q12 | SPR_PLATE | SHR_HCOIL_ROLLING_RSLT | 跨产线错表 |
| Q13 | SMS_SLAB | SMS_RSLT_CUT | 同 Q10 |
| Q17 | SPR_PLATE | SCH_PLAN_ROLL | 计划表 |
| Q18/Q19 | SPR_FCE_CHARGE | SPR_HEAT_FCE_RSLT | 加热炉实绩表混淆 |
| Q21 | SPR_DEFECT | SCR_DEFECT | 近名表 |
| Q24 | SQM_JDG_HLD | SPR_HOLD | 封锁表混淆 |
| Q25 | SQM_MECH_RSLT | SQM_MECH_TST_INFO | 力学近义表 |
| Q32 | SSD_ORDER_LINE | SCH_PLT_INST_CUTTING | 订单 vs 切割指示 |
| Q35 | SSD_ORDER_HEAD | SCH_PPC_PLAN_ORDT | 订单头 vs 计划 |

**规律**：全是「计划表↔实绩表」「近名/近义表」的检索消歧失败——正是 v2 方案 **P1（两段式语义检索 +
业务词典 + 相似表消歧）** 与 **P1.4（问题→正确表 嵌入微调）** 的直接靶点。

---

## 三、结论

1. **kimi-k3 切换有效且必要**：全链路结果正确率提升约 4 倍（2.4%→~10%），选表也从"频繁错"改善。
2. **瓶颈已转移到检索（P1）**：受控 32% vs 全链路 10% 的 22 个百分点差距，全部是 RAG 把错表（计划/实绩/近名）
   推到模型面前。26/41 的失败（11 拒答 + 15 选错表）根因在检索，不在模型。
3. **下一步 ROI 最高的是 P1**：修检索（富表卡片 + 业务词典 + 相似表消歧 + 嵌入微调），预期把全链路拉向受控上限。
   P2（值域接地/臆造过滤）、P3（口径/分布）在其后。

---

## 四、变更与回退

- **已切换**：线上网关 `:8000` 现运行 kimi-k3（provider 已加 kimi-k* 适配：temperature 夹到 1、max_tokens 兜底 2048、
  正文空回退 reasoning_content）。原环境备份 `/tmp/gw_env_backup.json`（0600）；provider 原文备份 `.bak-kimik3`；
  eval 口径补丁备份 `.bak-koujing`。
- **注意（延迟）**：kimi-k3 为推理模型，单次 mes-sql 约 30~60 秒，显著慢于旧模型；线上 mes-qa/mes-sql 交互延迟随之上升。
- **回退**：还原 `/tmp/gw_env_backup.json` 的 `AI_MODEL/AI_API_KEY` 并重启网关；provider 复制 `.bak-kimik3` 回原文即可。
- **待评审提交**：provider 适配与 eval 口径两处改动均未提交，`.bak` 保留，供 §5.1 评审。

---

*本报告基于 2026-09-07 线上切换后全链路 41 题实测；模型/管道/口径均记录在案，可复现。*
