<!--
文件用途：真实 MES 理解训练 Phase-1 验收就绪清单（供 TL/ITM 评审）
作者：AI（芯智云匠 MES AI 开发工程师）
日期：2026-07-15
关联需求单：REQ-MES-AI-20260715-001
-->

# Phase-1 验收就绪清单 · 真实 MES 系统理解训练

| 项 | 内容 |
|----|------|
| 文件编号 | AI-MES-PHASE1-READY-2026 |
| 日期 | 2026-07-15 |
| 需求单 | REQ-MES-AI-20260715-001（批训练，TL+IT 已授权）|
| 关联 | Sprint3_Training_Plan_2026.md（DoD 见其第七章）|
| 分支 | `feature/real-mes-integration`（HEAD `7bd313b`，本机/origin/远程三方对齐）|

> **就绪度定位（诚实）**：本清单汇总已完成的**自动化交付**（2026-07-15 训练/验证素材 + 2026-07-16 S3-3 业务流程理解完稿）。**Phase-1 尚未达到"可签字验收"**——三项准确率的**人工终评/BIZ 评分未做**、**《系统理解总报告》(S3-4-1) 未出**。S3-3 业务流程理解 AI 侧已完成（成稿报告 + 验证题库，接地校验全命中）。本清单用于 TL 评审「训练与验证素材是否就绪、可否进入人工评分与收尾」。

---

## 一、总体结论

| 维度 | 状态 |
|------|------|
| 训练素材（S3-0）| ✅ 就绪（95 表卡片 / 1401 子程序 / 术语表 / 代码字典 / 依赖图谱 / 脱敏审计 0 命中）|
| 表/字段理解（S3-1）| ✅ 训练完成（95/95 卡片）；SQL 验证题库+自动初评就绪，**人工终评待做** |
| 存储过程理解（S3-2）| ✅ 训练完成（1314 卡片）；BIZ 抽检单就绪，**BIZ 抽检待做** |
| 业务流程理解（S3-3）| ✅ **AI 侧完成**（状态机34/追溯边13/核心流程组12/验证题21 接地26/26）；成稿 `docs/S3-3_业务流程理解报告.md`，**BIZ 评分待做** |
| 断言种子（S3-4-2）| ✅ 657 条入 `/assertions/` |
| 系统理解总报告（S3-4-1）| ⬜ **未出**（待 S3-3 + 人工评分后汇总）|
| 知识库 RAG 可召回 | ✅ 表+过程卡片入 `mes_s3_understanding`，查询端接入，表召回 Top-3 7/10、过程 0.7+ |
| 全程脱敏 | ✅ 素材审计 0 命中；外发经网关脱敏门；密钥双重 gitignore 无泄漏 |
| Token 预算 | ✅ 今日约 3.92M（TL 授权临时超 §12 300 万，8M 闸内；明日恢复默认）|

---

## 二、Sprint 3 DoD 逐项核对

| DoD 条目 | 状态 | 证据 / 说明 |
|---------|------|------------|
| 表/SQL 准确率 ≥85% | ⏳ **待人工终评** | 自动初评均分 69.9/100（`docs/S3-1_SQL验证报告.md`，30 题）；语义正确率须 TL 人工评分 |
| 存储过程准确率 ≥85% | ⏳ **待 BIZ 抽检** | 抽样单 40 条（`docs/S3-2_BIZ抽检抽样单.md`）待 BIZ 判定 |
| 业务流程准确率 ≥90% | ⏳ **待 BIZ 评分** | S3-3 AI 侧完成（成稿报告 + 21 题验证库，接地 26/26 全命中）；准确率须 BIZ 对验证题评分 |
| 卡片/术语/字典入知识库可 RAG | ✅ | `mes_s3_understanding` 5155 chunk；`rag_service.retrieve_for_mes[_table/_proc]` |
| 断言种子 ≥3×P0 入 /assertions/ | ✅ | 657 条（Critical 89 主键 / High 171 状态流转 / Medium 397 写副作用+表关系），覆盖 149 资产 |
| 全程脱敏（无泄漏 + 审计完整）| ✅ | `docs/desensitize_audit_report.md` 0 命中；网关脱敏门；Gitleaks 规则含密钥忽略 |
| 系统理解总报告经 ITM 签字 | ⬜ **未出/未签** | 待 S3-3 + 人工评分后汇总 |
| Token 在预算内，P1/P2 排期 | ⏳ 部分 | 今日 3.92M（授权超额内）；P1/P2 排期待定 |

---

## 三、交付物清单

### 文档（`docs/`）
| 文件 | 用途 |
|------|------|
| `REQ-MES-AI-20260715-001_批训练需求单.md` | 训练授权载体（含预算红线临时授权留痕 + 执行记录）|
| `S3-1_表字段理解报告.md` | 表/字段理解报告（95/95）|
| `S3-2_存储过程理解报告.md` | 存储过程理解报告（1308+补跑）|
| `S3-1_SQL验证报告.md` | SQL 场景验证（30 题 + 自动初评 + 人工评分列）|
| `S3-2_BIZ抽检抽样单.md` | BIZ 过程抽检单（40 条待填）|
| `Phase1_验收就绪清单.md` | 本文件 |

### 工具（`scripts/kb-ingest/`，纯 stdlib + 项目依赖）
| 工具 | 职责 |
|------|------|
| `run_s3_training.py` | S3-1/S3-2 理解训练（经网关，去重/分片/续跑）|
| `build_assertion_seeds.py` | 断言种子生成（静态，不调 AI）|
| `ingest_s3_cards.py` | 卡片 RAG 入库（多语言 embedding，锚点 chunk）|
| `build_table_labels.py` | 表中文标签抽取（Kimi）|
| `run_sql_validation.py` | SQL 场景验证 + 自动初评 |
| `build_biz_sample.py` | BIZ 抽检抽样单生成 |

### 资产 / 数据
| 资产 | 位置 |
|------|------|
| 表中文标签（95）| `src/ai-gateway/app/services/mes_table_labels.json` |
| 断言种子（657）| `/assertions/{state-machine,sql-logic,api-behavior}/` |
| 理解卡片库（95 表 + 1314 过程）| 远程 `/home/xintong/mes-s3-data/s3-train/{tables,procs}/*.md`（持久，可重生成）|
| 向量库集合 `mes_s3_understanding`（5155 chunk）| 远程 `scripts/kb-ingest/data/chromadb`（gitignored，可重入库）|
| 查询端 | `src/ai-gateway/app/services/rag_service.py`（标签驱动 hybrid）|

---

## 四、量化指标

| 指标 | 值 |
|------|------|
| 表理解卡片 | 95 / 95 |
| 过程理解卡片 | 1314（去重 79 变体，~8 个 >4000 行超大过程待二次切分）|
| 断言种子 | 657（覆盖 149 P0 资产）|
| RAG chunk | 5155（表 401 + 过程 4754）|
| 表召回 Top-3 命中 | ~1/10 → **7/10**（锚点+去重+标签 hybrid）|
| 过程召回相似度 | 0.7+ |
| SQL 验证自动初评 | 30 题，均分 69.9/100 |
| ai-gateway 单测 | 49 passed |
| Token 消耗（今日）| ≈3.92M（训练 3.83M + SQL 66.8K + 标签 26K）|

---

## 五、待人工判定事项（无法自动化）

| # | 事项 | 负责人 | 输入素材 |
|---|------|--------|---------|
| 1 | SQL 场景语义正确率人工终评（≥85%）| TL | `docs/S3-1_SQL验证报告.md`（每题人工评分列）|
| 2 | 存储过程理解业务正确性抽检（≥85%）| BIZ | `docs/S3-2_BIZ抽检抽样单.md`（40 条）|
| 3 | 断言种子审核后纳入基准库 | TL | `/assertions/`（CLAUDE.md §7.3）|
| 4 | 《系统理解总报告》签字 | ITM | 待 S3-3 + 评分后汇总 |

---

## 六、未完成 / 长尾（诚实登记）

| 项 | 说明 | 影响 |
|----|------|------|
| **S3-3 业务流程理解** | 状态机/追溯/质量判定/调度流程理解，**AI 侧完成**（成稿报告 + 21 题验证库）；待 BIZ 评分签字 | Phase-1 验收：待 BIZ 评分 ≥90% |
| **《系统理解总报告》** | S3-4-1，未出 | 需 S3-3 + 人工评分后 |
| ~8 个 >4000 行超大过程 | 超上下文，未训 | 需二次切分后补训 |
| 表召回长尾 3/10 | 钢卷/热卷、客户/产品「主数据」真歧义 | hybrid 泛化后缀去噪可再拧 |
| SQL 表选择偏弱 | 部分题 Kimi 选错表/臆造列 | 表召回调优已缓解，人工评分中复核 |
| P1/P2 资产排期 | 未定 | 后续 Sprint |

---

## 七、本次提交索引（`REQ-MES-AI-20260715-001`，11 提交）

```
7bd313b perf: 标签驱动 hybrid 检索——表召回 5/10→7/10
b327175 perf: 表卡片 RAG 检索调优（锚点chunk + 按表去重）
89a3b47 feat: MES SQL 场景验证驱动 + 报告（T3-1-4/5）
d391454 feat: BIZ 抽检抽样单生成器 + 抽样单（T3-2-4）
c3d84a7 feat: rag_service 接入 mes_s3_understanding 查询端
192fc7d docs: 会话状态——验收前置进展
55db956 feat: S3 理解卡片 RAG 入库脚本
5428924 feat: P0 断言种子生成器 + 657 条（T3-4-2）
75d2e4c docs: 批训练需求单 + S3-1/S3-2 理解报告
b9045ce feat: S3-1/S3-2 真实 MES 理解训练驱动
58eebb7 chore: .gitignore 忽略 AI 平台密钥明文文件
```

---

## 八、TL 复现 / 验证入口（远程）

```bash
# 起网关（env 注入 key），单跑理解训练/验证
bash /home/xintong/mes-s3-data/sqlval.sh        # SQL 验证（含起网关）
# RAG 召回质量自测（表召回 hybrid）
cd /home/xintong/xintongmesai/src/ai-gateway && PYTHONPATH=. \
  HF_ENDPOINT=https://hf-mirror.com ../../.venv/bin/python -c \
  "from app.services.rag_service import get_rag_service as g; \
   print([d.metadata['source_file'] for d in g().retrieve_for_mes_table('钢卷缺陷记录',3)])"
# 断言种子 / 报告
cat assertions/manifest.md ; ls docs/S3-*.md
```

---

*芯智云匠 · Phase-1 验收就绪清单 · AI-MES-PHASE1-READY-2026 · 2026-07-15*
*本清单如实标注就绪/待人工/未完成三态；Phase-1 完整验收须补 S3-3 + 人工评分 + ITM 签字*
