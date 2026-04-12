#!/bin/bash
# ============================================================
# Redis 序列号计数器初始化脚本
# 文档编号: AI-MES-GIT-2026-001
# 关联任务: T0-2-4
# 关联文档: docs/MES_AI_Database_Design.md 第 8.4 节
# 作者: AI
# 日期: 2026-04-12
#
# 用途:
#   1. 验证 Redis 连通性
#   2. 预热当日 task_no 序列键（可选，避免首次请求延迟）
#   3. 设置键的过期时间（当日 23:59:59 自动过期）
#
# 使用方式:
#   ./redis-seq-init.sh [--host <host>] [--port <port>] [--db <db>]
#   环境变量优先级 > 命令行参数 > 默认值
#
# 环境变量:
#   REDIS_HOST  Redis 地址（默认 127.0.0.1）
#   REDIS_PORT  Redis 端口（默认 6379）
#   REDIS_DB    Redis 数据库编号（默认 0）
#   REDIS_AUTH  Redis 密码（为空则不认证）
# ============================================================

set -euo pipefail

# ── 颜色 ─────────────────────────────────────────────────────
RED='\033[0;31m'; YELLOW='\033[1;33m'; GREEN='\033[0;32m'
CYAN='\033[0;36m'; NC='\033[0m'

log_info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# ── 参数解析 ─────────────────────────────────────────────────
REDIS_HOST="${REDIS_HOST:-127.0.0.1}"
REDIS_PORT="${REDIS_PORT:-6379}"
REDIS_DB="${REDIS_DB:-0}"
REDIS_AUTH="${REDIS_AUTH:-}"

while [[ $# -gt 0 ]]; do
  case $1 in
    --host) REDIS_HOST="$2"; shift 2 ;;
    --port) REDIS_PORT="$2"; shift 2 ;;
    --db)   REDIS_DB="$2";   shift 2 ;;
    --auth) REDIS_AUTH="$2"; shift 2 ;;
    *) log_warn "未知参数: $1"; shift ;;
  esac
done

# ── 工具函数 ─────────────────────────────────────────────────
# 执行 redis-cli 命令（自动附加认证和 DB 选择）
redis_cmd() {
  if [[ -n "${REDIS_AUTH}" ]]; then
    redis-cli -h "${REDIS_HOST}" -p "${REDIS_PORT}" -n "${REDIS_DB}" \
              -a "${REDIS_AUTH}" --no-auth-warning "$@"
  else
    redis-cli -h "${REDIS_HOST}" -p "${REDIS_PORT}" -n "${REDIS_DB}" "$@"
  fi
}

# 计算当日 23:59:59 距现在的剩余秒数（用于设置 TTL）
seconds_until_midnight() {
  local now
  now=$(date +%s)
  local today_midnight
  today_midnight=$(date -d "tomorrow 00:00:00" +%s 2>/dev/null \
                   || date -v+1d -v0H -v0M -v0S +%s)   # macOS 兼容
  echo $(( today_midnight - now ))
}

# ── 主流程 ───────────────────────────────────────────────────
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║      芯智云匠 · Redis 序列号计数器初始化                ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# 步骤1: 检查 redis-cli 工具
log_info "步骤1: 检查 redis-cli 工具..."
if ! command -v redis-cli &>/dev/null; then
  log_error "redis-cli 未找到，请安装 Redis 客户端工具"
  exit 1
fi
log_ok "redis-cli 可用: $(redis-cli --version)"

# 步骤2: 连通性测试
log_info "步骤2: 测试 Redis 连通性 → ${REDIS_HOST}:${REDIS_PORT} db=${REDIS_DB}..."
PING_RESULT=$(redis_cmd PING 2>&1 || true)
if [[ "${PING_RESULT}" != "PONG" ]]; then
  log_error "Redis 连接失败，响应：${PING_RESULT}"
  log_error "请确认 Redis 已启动，且地址/端口/密码正确"
  exit 1
fi
log_ok "Redis 连通正常（PONG）"

# 步骤3: 预热当日 task_no 序列键
TODAY=$(date +%Y%m%d)
SEQ_KEY="seq:TASK_NO:${TODAY}"
TTL=$(seconds_until_midnight)

log_info "步骤3: 检查当日序列键 → ${SEQ_KEY}..."
EXISTS=$(redis_cmd EXISTS "${SEQ_KEY}")

if [[ "${EXISTS}" == "1" ]]; then
  CURRENT_VAL=$(redis_cmd GET "${SEQ_KEY}")
  CURRENT_TTL=$(redis_cmd TTL "${SEQ_KEY}")
  log_warn "键已存在，当前值: ${CURRENT_VAL}，剩余TTL: ${CURRENT_TTL}s（不重置）"
else
  # 初始化为 0（第一次 INCR 后变为 1，生成 REQ-MES-AI-YYYYMMDD-001）
  redis_cmd SET "${SEQ_KEY}" 0 EX "${TTL}" > /dev/null
  log_ok "序列键已初始化 → ${SEQ_KEY} = 0，TTL=${TTL}s（当日 23:59:59 自动过期）"
fi

# 步骤4: 模拟生成前3个序列号，验证格式正确
log_info "步骤4: 模拟生成序列号验证格式..."
for i in 1 2 3; do
  SEQ=$(redis_cmd INCR "${SEQ_KEY}")
  TASK_NO=$(printf "REQ-MES-AI-%s-%03d" "${TODAY}" "${SEQ}")
  log_ok "  模拟第 ${i} 个: ${TASK_NO}"
done

# 重置回 0（模拟完毕，恢复初始状态；TTL 不变）
redis_cmd SET "${SEQ_KEY}" 0 KEEPTTL > /dev/null
log_ok "序列键已重置为 0（模拟验证结束）"

# 步骤5: 输出当前 Redis 中所有序列键（巡检用）
log_info "步骤5: 当前 Redis 中所有 seq:TASK_NO:* 键..."
KEYS=$(redis_cmd KEYS "seq:TASK_NO:*" 2>&1)
if [[ -z "${KEYS}" ]]; then
  log_warn "  无历史序列键"
else
  while IFS= read -r key; do
    val=$(redis_cmd GET "${key}")
    ttl=$(redis_cmd TTL "${key}")
    echo "       ${key} = ${val}  TTL=${ttl}s"
  done <<< "${KEYS}"
fi

echo ""
log_ok "✅ Redis 序列号计数器初始化完成"
echo ""
echo "  序列号格式: REQ-MES-AI-{YYYYMMDD}-{NNN}"
echo "  Redis Key:  seq:TASK_NO:{YYYYMMDD}"
echo "  过期策略:   每日 00:00 自动过期，从 001 重新计数"
echo "  降级策略:   Redis 不可用时自动切换至 ai_seq_counter 表（MySQL 乐观锁）"
echo "  详见:       docs/MES_AI_Database_Design.md 第 8.4 节"
echo ""
