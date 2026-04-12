# CI/CD 流水线配置说明

**文档编号**: AI-MES-CICD-2026-006  
**关联任务**: T1-4-1 ~ T1-4-5  
**作者**: AI  
**日期**: 2026-04-12  

---

## 一、流水线概览

遵循 CLAUDE.md §8.1 回归测试顺序，共 5 个 Stage：

```
代码推送
  ↓
Stage 1: Gitleaks 硬编码扫描（零容忍，失败立即阻断）
  ↓ 通过
Stage 2: pytest 单元测试（覆盖率 ≥ 70%）
  ↓ 通过
Stage 3: SonarQube 质量扫描（0 Blocker + 0 Critical）
  ↓ 通过（仅 self-hosted runner 可访问内网 Sonar）
Stage 4: Docker 镜像构建 + 健康检查
  ↓ 通过
Stage 5: 自动部署至测试环境（仅 develop 分支 push 触发）
```

**触发条件**：
- `push` 到 `develop` 或 `feature/**` 分支
- `pull_request` 到 `main` 或 `develop`

---

## 二、GitHub Secrets 配置

在 GitHub 仓库 `Settings → Secrets and variables → Actions` 中添加：

| Secret 名称 | 值 | 说明 |
|------------|---|------|
| `AI_API_KEY` | Kimi API Key | AI 网关调用密钥（开发阶段） |
| `SONAR_TOKEN` | 见步骤四（从 SonarQube 管理界面生成） | SonarQube 分析 Token |
| `SONAR_HOST_URL` | `http://<Server-B-IP>:9100` | SonarQube 服务地址（填入 Server B 真实 IP） |
| `DB_URL` | MySQL 连接串 | AI 平台数据库（格式见 .env.example） |
| `WECHAT_WEBHOOK_URL` | 企业微信 Webhook | 告警通知（可选） |

> ⚠️ `GITLEAKS_LICENSE`：Gitleaks 开源版无需 License，留空即可（去掉 workflow 中该行）

---

## 三、自托管 Runner 注册

Stage 3（SonarQube）和 Stage 4/5（Docker/部署）在 `self-hosted` Runner 上运行，需要提前注册：

```bash
# 1. 在 GitHub 仓库获取 Token：
#    Settings → Actions → Runners → New self-hosted runner → Linux → 复制 Token

# 2. 注册 Runner（在 Server B 上执行）：
export RUNNER_TOKEN=<从GitHub复制的Token>
bash scripts/deploy/setup-github-runner.sh
```

注册成功后，Runner 标签为 `self-hosted, test-env, mesai`，CI 自动识别。

---

## 四、SonarQube 服务信息

| 项目 | 内容 |
|------|------|
| 服务地址 | `http://localhost:9100`（Server B 本机访问） |
| 管理员账号 | `admin` |
| 管理员密码 | 见部署记录（已修改默认密码） |
| 项目 Key | `mes-ai-platform` |
| 质量门禁 | `MES-AI-Gate`（Blocker=0, Critical=0） |
| Docker 容器 | `docker ps --filter name=sonarqube` |
| 日志查看 | `docker logs sonarqube -f` |

---

## 五、本地验证（无需 GitHub）

```bash
# 在项目根目录执行，模拟 CI 所有 Stage
bash scripts/deploy/validate-pipeline.sh
```

---

## 六、手动部署（紧急情况）

```bash
# 在 Server B 上手动执行部署（绕过 CI，需 IT 审核专员授权）
export DEPLOY_IMAGE_TAG=latest
export AI_API_KEY=<kimi-api-key>
export DB_URL=<db-url>
bash scripts/deploy/deploy-ai-gateway.sh
```

---

## 七、Pipeline 文件清单

| 文件 | 说明 |
|------|------|
| `.github/workflows/ci-pipeline.yml` | 主 CI 流水线（GitHub Actions） |
| `sonar-project.properties` | SonarQube 项目配置 |
| `scripts/deploy/deploy-ai-gateway.sh` | 蓝绿部署脚本（含自动回退） |
| `scripts/deploy/setup-github-runner.sh` | Self-hosted Runner 注册脚本 |
| `scripts/deploy/validate-pipeline.sh` | 本地 Pipeline 验证脚本 |
