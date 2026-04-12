#!/usr/bin/env bash
# ============================================================
# 芯智云匠 MES AI 平台 · 数据库初始化执行脚本
# 文档编号: AI-MES-DB-2026-006
# 关联任务: T1-3-1 ~ T1-3-7
# 作者: AI
# 日期: 2026-04-12
# 说明: 按版本号顺序执行 V1~V5 初始化 SQL，所有脚本均幂等
#       执行前须确认：
#         1. 已设置环境变量 DB_HOST / DB_PORT / DB_USER / DB_PASS
#         2. 目标数据库账号具有 CREATE DATABASE 权限
#         3. 当前目录为项目根目录
# ============================================================

set -euo pipefail

# ── 颜色定义 ──────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ── 从环境变量读取连接信息（禁止硬编码，遵循 CLAUDE.md 4.1）──
DB_HOST="${DB_HOST:?请设置环境变量 DB_HOST（AI 平台 MySQL 地址）}"
DB_PORT="${DB_PORT:-3306}"
DB_USER="${DB_USER:?请设置环境变量 DB_USER（数据库用户名）}"
DB_PASS="${DB_PASS:?请设置环境变量 DB_PASS（数据库密码，明文仅在本地终端使用，禁止写入脚本）}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/db-init-$(date +%Y%m%d-%H%M%S).log"

# ── MySQL 连接命令封装 ─────────────────────────────────────────
mysql_exec() {
    local sql_file="$1"
    mysql \
        --host="${DB_HOST}" \
        --port="${DB_PORT}" \
        --user="${DB_USER}" \
        --password="${DB_PASS}" \
        --default-character-set=utf8mb4 \
        --connect-timeout=10 \
        < "${sql_file}"
}

# ── 日志函数 ───────────────────────────────────────────────────
log() { echo -e "$1" | tee -a "${LOG_FILE}"; }

# ── 主流程 ────────────────────────────────────────────────────
log "${BLUE}============================================================${NC}"
log "${BLUE} 芯智云匠 MES AI 平台 · 数据库初始化${NC}"
log "${BLUE} 执行时间: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
log "${BLUE} 目标数据库: ${DB_HOST}:${DB_PORT}（用户: ${DB_USER}）${NC}"
log "${BLUE}============================================================${NC}"

# ── 1. 连通性检查 ─────────────────────────────────────────────
log "\n${YELLOW}[1/6] 检查数据库连通性...${NC}"
if ! mysql \
    --host="${DB_HOST}" \
    --port="${DB_PORT}" \
    --user="${DB_USER}" \
    --password="${DB_PASS}" \
    --connect-timeout=5 \
    -e "SELECT 1;" > /dev/null 2>&1; then
    log "${RED}✗ 无法连接到数据库，请检查环境变量和网络${NC}"
    exit 1
fi
log "${GREEN}✓ 数据库连接正常${NC}"

# ── 2. 按版本顺序执行 SQL 脚本 ────────────────────────────────
SCRIPTS=(
    "V1__mes_ai_task_schema.sql:T1-3-1 mes_ai_task Schema（10张表）"
    "V2__mes_ai_monitor_schema.sql:T1-3-2 mes_ai_monitor Schema（3张表）"
    "V3__mes_ai_knowledge_schema.sql:T1-3-3 mes_ai_knowledge Schema（6张表）"
    "V4__mes_ai_audit_schema.sql:T1-3-4 mes_ai_audit Schema（3张表）"
    "V5__init_base_data.sql:T1-3-7 基础数据初始化（断言种子、文档目录）"
)

STEP=2
FAILED=0
for entry in "${SCRIPTS[@]}"; do
    SCRIPT_FILE="${entry%%:*}"
    DESCRIPTION="${entry##*:}"
    FULL_PATH="${SCRIPT_DIR}/${SCRIPT_FILE}"

    log "\n${YELLOW}[${STEP}/6] 执行: ${SCRIPT_FILE}${NC}"
    log "          ${DESCRIPTION}"

    if [ ! -f "${FULL_PATH}" ]; then
        log "${RED}✗ 脚本文件不存在: ${FULL_PATH}${NC}"
        FAILED=$((FAILED + 1))
        STEP=$((STEP + 1))
        continue
    fi

    if mysql_exec "${FULL_PATH}" >> "${LOG_FILE}" 2>&1; then
        log "${GREEN}✓ 执行成功${NC}"
    else
        log "${RED}✗ 执行失败，请查看日志: ${LOG_FILE}${NC}"
        FAILED=$((FAILED + 1))
    fi
    STEP=$((STEP + 1))
done

# ── 3. 执行结果验证 ───────────────────────────────────────────
log "\n${YELLOW}[6/6] 验证 Schema 与表数量...${NC}"
VERIFY_SQL="
SELECT table_schema AS \`Schema\`, COUNT(*) AS \`表数量\`
FROM information_schema.tables
WHERE table_schema IN ('mes_ai_task', 'mes_ai_monitor', 'mes_ai_knowledge', 'mes_ai_audit')
  AND table_type = 'BASE TABLE'
GROUP BY table_schema
ORDER BY table_schema;
"
RESULT=$(mysql \
    --host="${DB_HOST}" \
    --port="${DB_PORT}" \
    --user="${DB_USER}" \
    --password="${DB_PASS}" \
    --default-character-set=utf8mb4 \
    -e "${VERIFY_SQL}" 2>/dev/null)

log "${RESULT}" | tee -a "${LOG_FILE}"

# 期望：mes_ai_audit=3, mes_ai_knowledge=6, mes_ai_monitor=3, mes_ai_task=10
TOTAL_TABLES=$(echo "${RESULT}" | grep -oP '\d+$' | paste -sd'+' | bc 2>/dev/null || echo "0")
log "\n已创建表总数: ${TOTAL_TABLES}（预期 22 张）"

# ── 汇总 ──────────────────────────────────────────────────────
log "\n${BLUE}============================================================${NC}"
if [ "${FAILED}" -eq 0 ]; then
    log "${GREEN}✓ 所有初始化脚本执行完成，无错误${NC}"
    log "${GREEN}  执行日志: ${LOG_FILE}${NC}"
else
    log "${RED}✗ 有 ${FAILED} 个脚本执行失败，请检查日志: ${LOG_FILE}${NC}"
    exit 1
fi
log "${BLUE}============================================================${NC}"
