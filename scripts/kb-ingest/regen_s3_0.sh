#!/usr/bin/env bash
# =============================================================================
# S3-0 训练素材一键重生成编排脚本（Sprint 3 · S3-0）
# -----------------------------------------------------------------------------
# 用途：把「结构盘点 → 全量建图 → P0 Top-N 选取 → 拉 P0 源码 → 子程序切分 →
#       字典对账」六步固化为一条命令，产物落到指定持久目录，避免会话级 scratchpad 丢失。
# 作者：AI（芯智云匠 MES AI 开发工程师）  日期：2026-07-14
# 关联需求单：REQ-MES-AI-20260706-001（占位，待补正式单号）
# 前置：需先 export MES_DB_USER / MES_DB_PASSWORD / MES_DB_DSN（口令仅运行时 env，不落盘）。
# 用法：PYTHON=/path/.venv/bin/python bash regen_s3_0.sh <输出目录>
# =============================================================================
set -euo pipefail

OUT_DIR="${1:?用法: regen_s3_0.sh <输出目录>}"
KB_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$KB_DIR/../.." && pwd)"
PY="${PYTHON:-python3}"
DICT_CSV="$REPO_DIR/docs/data_dictionary_full.csv"
GRAPH="$OUT_DIR/graph_mes"
mkdir -p "$GRAPH"

: "${MES_DB_USER:?未设置 MES_DB_USER}"
: "${MES_DB_PASSWORD:?未设置 MES_DB_PASSWORD}"
: "${MES_DB_DSN:?未设置 MES_DB_DSN}"

echo "===== S3-0 重生成开始 · 输出目录 $OUT_DIR ====="

echo "[1/6] 结构盘点（--no-source，约 30s）..."
$PY "$KB_DIR/db_introspect.py" --owner MESAPUSER --no-source --use-dba \
    --out "$OUT_DIR/meta_mes_nosrc.json"

echo "[2/6] 全量建图（约 7 分钟）..."
$PY "$KB_DIR/build_dep_graph.py" --owner MESAPUSER --use-dba --out-dir "$GRAPH"

echo "[3/6] P0 Top-N 中心度选取（Top60 包体 + Top100 表）..."
$PY "$KB_DIR/select_p0_topn.py" \
    --procs-csv "$GRAPH/procs.csv" --tables-csv "$GRAPH/tables.csv" \
    --top-procs 60 --top-tables 100 \
    --out-units "$GRAPH/p0_phase1_units.txt" --out-tables "$GRAPH/p0_phase1_tables.txt"

echo "[4/6] 拉 Top60 P0 源码..."
$PY "$KB_DIR/db_introspect.py" --owner MESAPUSER --use-dba \
    --source-units-file "$GRAPH/p0_phase1_units.txt" --out "$OUT_DIR/meta_p0.json"

echo "[5/6] 大包子程序切分..."
$PY "$KB_DIR/plsql_splitter.py" --input "$OUT_DIR/meta_p0.json" \
    --out-json "$OUT_DIR/split_all.json" --out-report "$OUT_DIR/split_report.md"

echo "[6/6] 字典对账（活库结构 × 字典 CSV）..."
$PY "$KB_DIR/dict_reconcile.py" --introspect "$OUT_DIR/meta_mes_nosrc.json" \
    --dict-csv "$DICT_CSV" \
    --out-report "$OUT_DIR/dict_reconcile_report.md" \
    --out-csv "$OUT_DIR/discrepancies.csv"

echo "===== S3-0 重生成完成 → $OUT_DIR ====="
ls -la "$OUT_DIR" "$GRAPH"
