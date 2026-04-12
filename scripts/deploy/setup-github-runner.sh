#!/usr/bin/env bash
# ============================================================
# 芯智云匠 MES AI 平台 · GitHub Actions 自托管 Runner 注册脚本
# 文档编号: AI-MES-CICD-2026-004
# 关联任务: T1-4-1
# 作者: AI
# 日期: 2026-04-12
#
# 使用方式：
#   1. 在 GitHub 仓库页面获取 Runner Token：
#      Settings → Actions → Runners → New self-hosted runner
#   2. 执行：
#      export RUNNER_TOKEN=<从GitHub复制的Token>
#      bash scripts/deploy/setup-github-runner.sh
#
# 说明：Runner 将以 systemd 服务方式运行，开机自启
# ============================================================

set -euo pipefail

RUNNER_TOKEN="${RUNNER_TOKEN:?请设置环境变量 RUNNER_TOKEN（从 GitHub Settings→Actions→Runners 获取）}"
REPO_URL="https://github.com/caoyb888/mesai"
RUNNER_VERSION="2.321.0"
RUNNER_DIR="/home/ubuntu/actions-runner"
RUNNER_USER="ubuntu"

echo "=== 安装 GitHub Actions 自托管 Runner ==="
echo "仓库: ${REPO_URL}"

# ── 下载 Runner 包 ────────────────────────────────────────────
mkdir -p "${RUNNER_DIR}"
cd "${RUNNER_DIR}"

if [ ! -f "run.sh" ]; then
    echo "[1/4] 下载 Runner v${RUNNER_VERSION}..."
    curl -sL "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz" \
        | tar -xz
fi

# ── 注册 Runner ───────────────────────────────────────────────
echo "[2/4] 注册 Runner..."
./config.sh \
    --url "${REPO_URL}" \
    --token "${RUNNER_TOKEN}" \
    --name "mesai-test-server" \
    --labels "self-hosted,test-env,mesai" \
    --work "_work" \
    --unattended \
    --replace

# ── 安装为 systemd 服务 ───────────────────────────────────────
echo "[3/4] 安装 systemd 服务..."
sudo ./svc.sh install "${RUNNER_USER}"
sudo ./svc.sh start

# ── 验证 ─────────────────────────────────────────────────────
echo "[4/4] 验证服务状态..."
sudo systemctl status "actions.runner.caoyb888-mesai.mesai-test-server" --no-pager | head -10

echo ""
echo "✓ Runner 注册完成"
echo "  在 GitHub 仓库 Settings → Actions → Runners 页面确认 Runner 状态为 Idle"
echo "  日志查看: sudo journalctl -u actions.runner.* -f"
