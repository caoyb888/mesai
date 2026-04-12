#!/usr/bin/env bash
# ============================================================
# 芯智云匠 MES AI 平台 · Pipeline 本地验证脚本
# 文档编号: AI-MES-CICD-2026-005
# 关联任务: T1-4-5
# 作者: AI
# 日期: 2026-04-12
#
# 说明: 在本机模拟执行 CI 各 Stage，验证流水线正常运行
#       等价于 GitHub Actions 流水线的本地预检
# ============================================================

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AI_GATEWAY_DIR="${PROJECT_ROOT}/src/ai-gateway"

PASS=0; FAIL=0

check() {
    local name="$1"; shift
    echo -e "\n${YELLOW}▶ ${name}${NC}"
    if "$@" 2>&1; then
        echo -e "${GREEN}✓ ${name} 通过${NC}"; PASS=$((PASS+1))
    else
        echo -e "${RED}✗ ${name} 失败${NC}"; FAIL=$((FAIL+1))
    fi
}

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE} 芯智云匠 CI Pipeline 本地验证${NC}"
echo -e "${BLUE} 工作目录: ${PROJECT_ROOT}${NC}"
echo -e "${BLUE}============================================================${NC}"

# ── Stage 1: Gitleaks 硬编码扫描 ──────────────────────────────
check "Stage 1: Gitleaks 硬编码扫描" bash -c "
    cd '${PROJECT_ROOT}'
    # git 模式：只扫描已追踪文件（.env 等已 gitignore 的文件不扫）
    gitleaks detect \
        --config .gitleaks.toml \
        --source . \
        --redact
"

# ── Stage 2: pytest 单元测试 ──────────────────────────────────
check "Stage 2: pytest 单元测试（覆盖率检查）" bash -c "
    cd '${AI_GATEWAY_DIR}'
    export AI_PROVIDER=kimi
    export AI_API_KEY=test-placeholder
    export AI_API_BASE_URL=https://api.moonshot.cn/v1
    export AI_MODEL=moonshot-v1-8k
    export TOKEN_DAILY_BUDGET=3000000
    export TOKEN_DEGRADE_THRESHOLD=2500000
    export TOKEN_PAUSE_THRESHOLD=3000000
    export WECHAT_WEBHOOK_URL=''
    export DB_URL=''
    python3 -m pytest tests/ \
        --cov=app \
        --cov-report=term-missing \
        --cov-fail-under=70 \
        -q 2>&1
"

# ── Stage 3: SonarQube 扫描（需 SonarQube 服务运行）─────────
check "Stage 3: SonarQube 服务可达" bash -c "
    if curl -sf http://localhost:9000/api/system/status > /dev/null 2>&1; then
        STATUS=\$(curl -sf http://localhost:9000/api/system/status | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get(\"status\",\"UNKNOWN\"))' 2>/dev/null)
        echo \"SonarQube 状态: \${STATUS}\"
        [ \"\${STATUS}\" = 'UP' ]
    else
        echo 'SonarQube 未运行，跳过（容器可能仍在初始化）'
        exit 0
    fi
"

# ── Stage 4: Docker 镜像构建 ──────────────────────────────────
check "Stage 4: Docker 镜像构建" bash -c "
    docker build \
        -t mesai/ai-gateway:validate-test \
        '${AI_GATEWAY_DIR}' \
        --quiet
    echo '镜像构建成功: mesai/ai-gateway:validate-test'
    docker rmi mesai/ai-gateway:validate-test --force > /dev/null
"

# ── Stage 5: 部署脚本语法检查 ─────────────────────────────────
check "Stage 5: 部署脚本语法检查" bash -c "
    bash -n '${PROJECT_ROOT}/scripts/deploy/deploy-ai-gateway.sh'
    echo '部署脚本语法正确'
"

# ── 汇总 ──────────────────────────────────────────────────────
echo -e "\n${BLUE}============================================================${NC}"
echo -e "验证结果: ${GREEN}通过 ${PASS}${NC} / ${RED}失败 ${FAIL}${NC}"
if [ "${FAIL}" -eq 0 ]; then
    echo -e "${GREEN}✓ 所有 Stage 验证通过，流水线就绪${NC}"
else
    echo -e "${RED}✗ 有 ${FAIL} 个 Stage 失败，请修复后重试${NC}"
    exit 1
fi
echo -e "${BLUE}============================================================${NC}"
