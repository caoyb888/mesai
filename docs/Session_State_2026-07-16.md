# 会话状态快照 · 2026-07-16

> 关联：`REQ-MES-AI-20260716-001`（P1 批训练）、`REQ-MES-AI-20260715-001`（P0）、CLAUDE.md
> 记忆：`.claude/.../memory/s3-batch-training-done.md`、`mes-real-db-pivot.md`、`remote-dev-machine.md`
> 远程开发机：`ssh xintong@100.95.76.81`（内网 IP `10.30.10.49`），项目 `/home/xintong/xintongmesai`，venv `.venv`

---

## 一、本次进展（P1 次核心资产批训练，全部完成）

Phase-1（P0）已评审通过在先。本轮把理解从 P0 扩到 P1，并补断言种子。

| 阶段 | 结果 | 产物 |
|----|----|----|
| **P1 表批** | ✅ 261 卡片（清 demo 垃圾表 `YOUR_TABLE_NAME`），~65.2 万 token | `s3-train-p1/tables/` |
| **P1 过程批** | ✅ 训练 2209 单元 → 2206 卡片，**实耗 5.34M token**（TL 授权 8M 闸/仅本次，已恢复默认 300 万）| `s3-train-p1/procs/` |
| **脱敏审计** | ✅ §4.2 七类，源码+卡片 **0 命中** | `s3-train-p1/desensitize_audit_p1_procs.md` |
| **入库** | ✅ 表 1002 + 过程 8009 chunk（无 --reset）→ 集合 `mes_s3_understanding` **5155→14166** | ChromaDB `scripts/kb-ingest/data/chromadb` |
| **抽检** | ✅ 核心表/过程 Top-3 可召回（空表薄卡召回弱＝P2 调优项）| — |
| **P1 断言种子** | ✅ **980 条**（ST515/SQ325/AP140；Critical235/High280/Medium465；覆盖 375 资产）| `assertions/*/*_seeds_p1.jsonl` |

**集合 `mes_s3_understanding` = 14166 chunk**（P0 5155 + P1 表 1002 + P1 过程 8009）。
**断言库 = 1637 条**（P0 657 + P1 980）；ID：P0 `AS-{ST|SQ|AP}-NNNN`、P1 带 `-P1-` 段 + `phase:P1`，零冲突。

本轮提交：`eca2231`（过程批授权留痕）、`4d8efa9`（过程批完成回填）、`6ab94d9`（P1 断言种子）。分支 `feature/real-mes-integration`。

---

## 二、关键环境与坑（复盘）

- **DB 连接**：`10.30.10.111:25521/XEPDB1`（Oracle XE，用户 SYSTEM）。
  **端口非默认 1521 而是 25521**（1521 拒绝）。凭据仅存**内网机 repo 外** `/home/xintong/mes-s3-data/p1/mesdb.env`（chmod600，**不入 git、不写代码/命令行**，§4.1）。db_introspect 只读 `os.getenv` 注入。
- **远程完全离线**：跑加载 SentenceTransformer 的脚本（ingest/validate）**必须** `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1`（模型已缓存 `~/.cache/huggingface/hub/`），否则卡 HF Hub HEAD 重试报错。训练本身不加载 HF（走 Kimi 网关）。
- **网关 8M 闸机制**：`/home/xintong/mes-s3-data/orch_p1_procs.sh` 的 `restart_gw` = `pkill uvicorn` 后带 `TOKEN_PAUSE_THRESHOLD=8000000` + kimi provider 重启网关。**闸阈值网关启动时读 env，改闸须重启网关**。默认 config 降级 250 万 / 暂停 300 万。
- **入库幂等**：`ingest_s3_cards.py` chunk_id 决定式（upsert）；**追加 P1 严禁 `--reset`**（会清空 P0）。换模型才全量重入（§14）。

---

## 三、恢复指南（P1 相关可重跑，均在内网机）

```bash
# 前置：DB 凭据（内网机 env，不落 git）
set -a; source /home/xintong/mes-s3-data/p1/mesdb.env; set +a
cd /home/xintong/xintongmesai; PY=.venv/bin/python; P1=/home/xintong/mes-s3-data/p1

# 源码自省 + 切分（静态，0 token）
$PY scripts/kb-ingest/db_introspect.py --owner MESAPUSER --use-dba \
    --source-units-file $P1/p1_units.txt --out $P1/meta_p1.json
$PY scripts/kb-ingest/plsql_splitter.py --input $P1/meta_p1.json \
    --out-json $P1/split_p1.json --out-report $P1/split_p1_report.md

# 过程批（须 TL 8M 闸授权；经网关脱敏门）
bash /home/xintong/mes-s3-data/orch_p1_procs.sh   # 3 分片, 输入 split_p1, 输出 s3-train-p1

# 脱敏审计 → 入库（离线）→ 抽检
$PY scripts/desensitize/audit_materials.py --material $P1/meta_p1.json \
    --material <卡片合并> --out-report .../desensitize_audit_p1_procs.md
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 $PY scripts/kb-ingest/ingest_s3_cards.py \
    --procs-dir /home/xintong/mes-s3-data/s3-train-p1/procs \
    --collection mes_s3_understanding --validate         # 不加 --reset

# P1 断言种子（静态，0 token）
$PY scripts/kb-ingest/build_table_cards.py --meta $P1/meta_p1.json \
    --dict-csv docs/data_dictionary_full.csv --p0-tables $P1/p1_tables_clean.txt \
    --tables-csv /home/xintong/mes-s3-data/s3-0/graph_mes/tables.csv \
    --out-md /tmp/p1_table_cards.md --out-jsonl $P1/p1_table_cards.jsonl
$PY scripts/kb-ingest/build_assertion_seeds.py --meta $P1/meta_p1.json \
    --cards $P1/p1_table_cards.jsonl --out $P1/assertions-p1
```

---

## 四、未决事项（待 TL / BIZ / 后续 Sprint）

1. **P1 断言种子 TL 审核** → 纳入基准库（§7.3，候选状态）。P0 657 条同样待审。
2. **超大过程 16 件二次切分**（>1200 行，本批 `--proc-max-tokens 1200` 跳过）。需追加训练 token 预算闸。
3. **空表薄卡召回调优**（P2）：行数=0 的 P1 表结构-only 卡片语义锚点弱，被富文本过程卡挤出 Top-3；可加中文表名别名增强 anchor。
4. **P1 清单残留**：`p1_tables.txt` 仍含 2 条 `SCOAPUSER.` 前缀 + bare/schema 重复（本应剔除，未出卡不影响入库）；`p1_tables_clean.txt` 已剔 demo 表。
5. **断言生成器缺陷**：cards/procs 分段采番在同批内产重复 ID（P0 657→568 唯一）；P1 已连番一意化，P0 待整理。
6. ITM 脱敏合规形式签字（需求单 H 末行；网关脱敏门已强制生效）。

---

*会话状态快照 · 2026-07-16 · P1 批训练全流程完成（训练+审计+入库+抽检+断言种子）*
