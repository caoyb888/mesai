# Git 分支策略规范

**文档编号**：AI-MES-GIT-2026-001  
**版本**：V1.0 · 2026-04-12  
**关联任务**：T0-2-2  
**作者**：AI  

---

## 一、分支模型总览

本项目采用 **简化 Git Flow** 模型，共三类分支：

```
main        ← 生产就绪代码，只接受来自 develop 的 MR（经 IT 审核专员审批）
  └─ develop ← 集成分支，所有功能开发完成后合并至此
       └─ feature/{story-id}-{short-desc}  ← 功能开发分支，开发完成后 MR → develop
       └─ fix/{issue-id}-{short-desc}      ← 缺陷修复分支
       └─ hotfix/{issue-id}-{short-desc}   ← 紧急热修复（直接从 main 切出，修完合并 main + develop）
```

---

## 二、分支命名规范

| 分支类型 | 命名格式 | 示例 |
|--------|--------|------|
| 主干 | `main` | `main` |
| 集成 | `develop` | `develop` |
| 功能 | `feature/{story-id}-{短描述}` | `feature/S1-3-db-init` |
| 缺陷修复 | `fix/{req-no}-{短描述}` | `fix/REQ-20260415-003-task-status` |
| 紧急热修复 | `hotfix/{req-no}-{短描述}` | `hotfix/REQ-20260501-001-login-500` |
| 发布准备 | `release/{版本号}` | `release/1.0.0` |

**规则**：
- 分支名全小写，单词间用 `-` 连接
- `{story-id}` 对应 Sprint Plan 中的 Story 编号（如 `S1-3`）
- `{req-no}` 对应需求单编号（如 `REQ-20260415-003`）

---

## 三、各分支保护规则（GitHub Branch Protection）

### 3.1 main 分支

| 规则 | 配置值 |
|------|------|
| 禁止直接 Push | ✅ 开启 |
| 要求 Pull Request | ✅ 开启 |
| 最少 Reviewer 数 | **2**（TL + IT审核专员） |
| 要求所有对话解决 | ✅ 开启 |
| 要求状态检查通过 | ✅ 开启（见下方 CI 检查项） |
| 禁止 Force Push | ✅ 开启 |
| 禁止删除分支 | ✅ 开启 |

**必须通过的 CI 状态检查**：
1. `gitleaks` — 硬编码扫描（0 违规）
2. `sonarqube` — 代码质量（0 Critical）
3. `unit-test` — 单元测试（覆盖率 ≥ 70%）
4. `assertion-baseline` — 断言库基准测试（Critical 100%）
5. `regression-test` — 流量回放回归测试（P0 差异 = 0）

### 3.2 develop 分支

| 规则 | 配置值 |
|------|------|
| 禁止直接 Push | ✅ 开启 |
| 要求 Pull Request | ✅ 开启 |
| 最少 Reviewer 数 | **1**（TL 或指定 AE） |
| 要求状态检查通过 | ✅ 开启（见下方 CI 检查项） |
| 禁止 Force Push | ✅ 开启 |
| 禁止删除分支 | ✅ 开启 |

**必须通过的 CI 状态检查**：
1. `gitleaks` — 硬编码扫描
2. `sonarqube` — 代码质量
3. `unit-test` — 单元测试

### 3.3 feature/* / fix/* 分支

| 规则 | 配置值 |
|------|------|
| 允许开发者直接 Push | ✅（无保护，开发者工作分支） |
| MR 合并至 develop 时 | 触发完整 CI 流水线 |
| 合并后自动删除 | ✅ 建议开启（保持仓库整洁） |

---

## 四、工作流（开发者操作步骤）

### 4.1 新功能开发

```bash
# 1. 从最新 develop 签出功能分支
git checkout develop
git pull origin develop
git checkout -b feature/S1-3-db-init

# 2. 开发、提交（遵循 CLAUDE.md 5.4 提交规范）
git add src/main/resources/sql/V1__init_tables.sql
git commit -m "[REQ-MES-AI-20260415-001] feat: 初始化22张业务表DDL"

# 3. 推送并发起 Pull Request（目标分支：develop）
git push origin feature/S1-3-db-init
# → 在 GitHub 上创建 PR，填写说明，指定 Reviewer
```

### 4.2 紧急热修复

```bash
# 1. 从 main 签出 hotfix 分支
git checkout main
git pull origin main
git checkout -b hotfix/REQ-20260501-001-login-500

# 2. 修复、提交
git commit -m "[REQ-MES-AI-20260501-001] fix: 修复登录接口500异常"

# 3. 分别 MR → main 和 MR → develop（两个 PR）
git push origin hotfix/REQ-20260501-001-login-500
```

### 4.3 版本发布

```bash
# 1. 从 develop 签出 release 分支
git checkout -b release/1.0.0 develop

# 2. 仅做版本号修改和发布前最终修复，禁止新功能提交
# 3. MR → main（需 TL + IT 审核专员双 Approve）
# 4. main 合并后打 Tag
git tag -a v1.0.0 -m "Release v1.0.0 - MVP上线"
git push origin v1.0.0
# 5. MR → develop（同步 release 阶段的修复）
```

---

## 五、Commit Message 规范（来自 CLAUDE.md 5.4）

```
格式：[REQ-MES-AI-YYYYMMDD-XXX] <类型>: <简短描述>

类型：feat | fix | refactor | perf | docs | test | chore

示例：
[REQ-MES-AI-20260415-003] feat: 新增设备点检记录功能（含前端页面和后端接口）
[REQ-MES-AI-20260420-005] fix: 修复工单状态机非法跳转校验缺失问题
[REQ-MES-AI-20260425-007] docs: 更新接口文档，补充分页参数说明
```

**禁止**：
- 一次 commit 混合多个不相关需求
- `fix: fix bug` 等无意义提交信息
- 无需求单编号的功能性提交

---

## 六、分支生命周期管理

| 分支 | 创建时机 | 删除时机 |
|------|--------|--------|
| `main` | 项目初始化 | 永不删除 |
| `develop` | 项目初始化 | 永不删除 |
| `feature/*` | 开始 Story 开发时 | MR 合并 develop 后立即删除 |
| `fix/*` | 缺陷修复时 | MR 合并 develop 后立即删除 |
| `hotfix/*` | 紧急修复时 | 合并 main + develop 后删除 |
| `release/*` | 准备发布时 | 合并 main + develop 后删除 |

---

*芯智云匠 · Git 分支策略规范 V1.0 · 2026-04-12*  
*T0-2-2 交付物 · 关联：AI-MES-TECH-2026-001*
