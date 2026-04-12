#!/usr/bin/env bash
# ============================================================
# 芯智云匠 MES AI 平台 · AI 网关部署脚本
# 文档编号: AI-MES-CICD-2026-002
# 关联任务: T1-4-4
# 作者: AI
# 日期: 2026-04-12
#
# 使用方式：
#   export DEPLOY_IMAGE_TAG=<git-sha>
#   export AI_API_KEY=<kimi-or-claude-key>
#   export DB_URL=<数据库连接串>
#   bash scripts/deploy/deploy-ai-gateway.sh
#
# 说明：
#   - 蓝绿部署：先启动新容器，健康检查通过后停旧容器
#   - 回退：若新容器健康检查失败，自动恢复旧容器
#   - 所有敏感配置通过环境变量注入，禁止硬编码（CLAUDE.md 4.1）
# ============================================================

set -euo pipefail

# ── 颜色 ──────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

# ── 配置（均来自环境变量，无硬编码）──────────────────────────
IMAGE_NAME="mesai/ai-gateway"
IMAGE_TAG="${DEPLOY_IMAGE_TAG:-latest}"
CONTAINER_NAME="mesai-ai-gateway"
CONTAINER_NAME_NEW="${CONTAINER_NAME}-new"
GATEWAY_PORT="${GATEWAY_PORT:-8000}"
HEALTH_CHECK_URL="http://localhost:${GATEWAY_PORT}/v1/ai/health"
HEALTH_CHECK_RETRIES=10
HEALTH_CHECK_INTERVAL=3

log()  { echo -e "${YELLOW}[DEPLOY]${NC} $1"; }
ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; }

# ── 部署前检查 ────────────────────────────────────────────────
log "开始部署 AI 网关 · 镜像标签: ${IMAGE_TAG}"

if [ -z "${AI_API_KEY:-}" ]; then
    fail "环境变量 AI_API_KEY 未设置，部署中止"
    exit 1
fi

# ── 记录当前运行的容器 ID（用于回退）────────────────────────
OLD_CONTAINER_ID=$(docker ps -q --filter "name=^${CONTAINER_NAME}$" 2>/dev/null || true)

# ── 启动新容器（蓝绿切换）────────────────────────────────────
log "启动新容器: ${CONTAINER_NAME_NEW}"
docker rm -f "${CONTAINER_NAME_NEW}" 2>/dev/null || true

docker run -d \
    --name "${CONTAINER_NAME_NEW}" \
    --restart unless-stopped \
    -p "${GATEWAY_PORT}:8000" \
    -e AI_PROVIDER="${AI_PROVIDER:-kimi}" \
    -e AI_API_KEY="${AI_API_KEY}" \
    -e AI_API_BASE_URL="${AI_API_BASE_URL:-https://api.moonshot.cn/v1}" \
    -e AI_MODEL="${AI_MODEL:-moonshot-v1-8k}" \
    -e AI_REQUEST_TIMEOUT="${AI_REQUEST_TIMEOUT:-120}" \
    -e AI_MAX_RETRIES="${AI_MAX_RETRIES:-3}" \
    -e TOKEN_DAILY_BUDGET="${TOKEN_DAILY_BUDGET:-3000000}" \
    -e TOKEN_DEGRADE_THRESHOLD="${TOKEN_DEGRADE_THRESHOLD:-2500000}" \
    -e TOKEN_PAUSE_THRESHOLD="${TOKEN_PAUSE_THRESHOLD:-3000000}" \
    -e DB_URL="${DB_URL:-}" \
    -e WECHAT_WEBHOOK_URL="${WECHAT_WEBHOOK_URL:-}" \
    -e LOG_LEVEL="${LOG_LEVEL:-INFO}" \
    "${IMAGE_NAME}:${IMAGE_TAG}"

# ── 健康检查 ─────────────────────────────────────────────────
log "等待新容器健康检查通过..."
HEALTHY=0
for i in $(seq 1 ${HEALTH_CHECK_RETRIES}); do
    sleep ${HEALTH_CHECK_INTERVAL}
    if curl -sf "${HEALTH_CHECK_URL}" > /dev/null 2>&1; then
        HEALTHY=1
        ok "健康检查通过（第 ${i} 次尝试）"
        break
    fi
    log "健康检查第 ${i}/${HEALTH_CHECK_RETRIES} 次，等待中..."
done

# ── 健康检查失败：回退 ────────────────────────────────────────
if [ "${HEALTHY}" -eq 0 ]; then
    fail "新容器健康检查失败，执行回退！"
    docker rm -f "${CONTAINER_NAME_NEW}" 2>/dev/null || true
    if [ -n "${OLD_CONTAINER_ID}" ]; then
        log "旧容器仍在运行，服务未中断"
    fi
    fail "部署失败，请查看容器日志: docker logs ${CONTAINER_NAME_NEW}"
    exit 1
fi

# ── 切换：停旧容器，重命名新容器 ─────────────────────────────
if [ -n "${OLD_CONTAINER_ID}" ]; then
    log "停止旧容器: ${CONTAINER_NAME}"
    docker stop "${CONTAINER_NAME}" 2>/dev/null || true
    docker rename "${CONTAINER_NAME}" "${CONTAINER_NAME}-backup-$(date +%Y%m%d%H%M%S)" 2>/dev/null || true
fi

docker rename "${CONTAINER_NAME_NEW}" "${CONTAINER_NAME}"
ok "新容器已启动并切换完成"

# ── 清理旧 backup 容器（保留最新 2 个）────────────────────────
docker ps -a --filter "name=${CONTAINER_NAME}-backup-" --format "{{.Names}}" | \
    sort -r | tail -n +3 | xargs -r docker rm -f

# ── 部署摘要 ──────────────────────────────────────────────────
RESPONSE=$(curl -sf "${HEALTH_CHECK_URL}" || echo '{}')
echo ""
ok "======= 部署完成 ======="
ok "容器名称 : ${CONTAINER_NAME}"
ok "镜像标签 : ${IMAGE_TAG}"
ok "服务地址 : ${HEALTH_CHECK_URL}"
ok "健康响应 : ${RESPONSE}"
echo ""
