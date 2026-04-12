# 芯智云匠 · 前端组件设计规范

## 山东芯通 MES AI 智能体资产化项目

| 项目 | 内容 |
|------|------|
| 文件编号 | AI-MES-FESPEC-2026-001 |
| 版本号 | V1.0 |
| 编写日期 | 2026-04-12 |
| 编写单位 | 乙方技术团队 |
| 关联技术规范 | AI-MES-TECHSPEC-2026-001（V1.0） |
| 关联API规范 | AI-MES-API-2026-001（V1.1） |
| 关联开发规范 | CLAUDE.md（AI-MES-CLAUDE-2026-001 · V1.0） |
| 技术栈 | Vue 3 · Element Plus 2.x · Pinia · Vue Router 4 · TypeScript |
| 文件状态 | 正式发布 |

> **文档目的**：本规范定义前端工程的完整架构约定，包括目录结构、路由设计、组件层级划分、状态管理约定、权限守卫实现和编码风格，确保多人协作时代码风格统一、模块边界清晰、权限控制一致。所有前端开发人员必须在开始编码前完整阅读本文档。

---

## 目录

1. [工程目录结构](#一工程目录结构)
2. [页面路由设计](#二页面路由设计)
3. [组件层级划分](#三组件层级划分)
4. [状态管理约定（Pinia）](#四状态管理约定pinia)
5. [权限守卫实现](#五权限守卫实现)
6. [组件编码规范](#六组件编码规范)
7. [样式规范](#七样式规范)
8. [API 调用规范](#八api-调用规范)
9. [WebSocket 实时推送规范](#九websocket-实时推送规范)
10. [公共组件库设计](#十公共组件库设计)
11. [页面级组件设计](#十一页面级组件设计)
12. [错误处理与用户反馈规范](#十二错误处理与用户反馈规范)
13. [附录](#十三附录)

---

## 一、工程目录结构

```
src/
├── main.ts                    # 应用入口
├── App.vue                    # 根组件
│
├── router/                    # 路由（见第二章）
│   ├── index.ts               # 路由实例创建与导出
│   ├── guards.ts              # 全局路由守卫
│   └── modules/               # 按模块拆分路由配置
│       ├── task.ts
│       ├── review.ts
│       ├── deploy.ts
│       ├── monitor.ts
│       ├── knowledge.ts
│       ├── assertion.ts
│       ├── cost.ts
│       └── system.ts
│
├── stores/                    # Pinia 状态管理（见第四章）
│   ├── index.ts               # 统一导出所有 store
│   ├── user.ts                # 用户身份与权限（核心 store）
│   ├── task.ts                # 任务管理状态
│   ├── notification.ts        # 全局消息通知
│   └── ws.ts                  # WebSocket 连接状态
│
├── api/                       # API 请求封装（见第八章）
│   ├── request.ts             # axios 实例（拦截器、Token、错误处理）
│   ├── task.ts                # 任务管理接口
│   ├── review.ts              # 评审与授权接口
│   ├── deploy.ts              # 部署管理接口
│   ├── monitor.ts             # 运维监控接口
│   ├── knowledge.ts           # 知识库接口
│   ├── assertion.ts           # 断言库接口
│   ├── cost.ts                # 成本统计接口
│   └── system.ts              # 系统管理接口
│
├── types/                     # TypeScript 类型定义
│   ├── common.ts              # 通用类型（ResultVO、PageVO、枚举等）
│   ├── task.ts                # 任务相关类型
│   ├── review.ts              # 评审授权类型
│   ├── deploy.ts              # 部署管理类型
│   ├── monitor.ts             # 监控巡检类型
│   ├── knowledge.ts           # 知识库类型
│   ├── assertion.ts           # 断言库类型
│   ├── cost.ts                # 成本统计类型
│   └── user.ts                # 用户与权限类型
│
├── layouts/                   # 布局组件（见第三章 3.1 节）
│   ├── DefaultLayout.vue      # 主布局（侧边栏 + 顶部栏 + 内容区）
│   ├── BlankLayout.vue        # 空白布局（登录页、错误页专用）
│   ├── components/
│   │   ├── AppSidebar.vue     # 侧边导航栏
│   │   ├── AppHeader.vue      # 顶部栏（用户信息、通知、退出）
│   │   └── AppBreadcrumb.vue  # 面包屑导航
│   └── composables/
│       └── useMenus.ts        # 根据角色权限动态生成菜单
│
├── views/                     # 页面视图（见第三章 3.2 节 & 第十一章）
│   ├── login/
│   │   └── LoginPage.vue
│   ├── task/
│   │   ├── TaskBoardPage.vue          # 任务看板（Kanban）
│   │   ├── TaskListPage.vue           # 任务列表（表格）
│   │   ├── TaskDetailPage.vue         # 任务详情（多选项卡）
│   │   ├── TaskCreatePage.vue         # 新建需求单
│   │   └── TaskEditPage.vue           # 编辑需求单（DRAFT/REJECTED）
│   ├── review/
│   │   ├── ReviewPendingPage.vue      # 待评审列表
│   │   └── ApprovalGatePage.vue       # 人工授权网关
│   ├── deploy/
│   │   ├── DeployListPage.vue         # 部署申请列表
│   │   └── DeployDetailPage.vue       # 部署详情与审批
│   ├── monitor/
│   │   ├── InspectionListPage.vue     # 巡检报告列表
│   │   ├── InspectionDetailPage.vue   # 巡检报告详情
│   │   ├── AlertListPage.vue          # 告警记录
│   │   └── MetricsDashboardPage.vue   # 系统指标仪表盘
│   ├── knowledge/
│   │   ├── KnowledgeDocListPage.vue   # 知识文档列表
│   │   └── KnowledgeSearchPage.vue    # 知识库检索测试
│   ├── assertion/
│   │   ├── AssertionListPage.vue      # 断言列表
│   │   └── AssertionBatchPage.vue     # 批次执行与结果
│   ├── cost/
│   │   ├── CostDailyPage.vue          # Token 日消耗
│   │   └── CostStatPage.vue           # 多维度成本统计
│   ├── system/
│   │   └── UserManagePage.vue         # 用户管理
│   └── error/
│       ├── 403Page.vue
│       └── 404Page.vue
│
├── components/                # 业务 & 基础公共组件（见第三章 3.3 节 & 第十章）
│   ├── business/              # 业务组件（跨页面复用的业务逻辑组件）
│   │   ├── task/
│   │   │   ├── TaskCard.vue           # 看板卡片
│   │   │   ├── TaskStatusTag.vue      # 状态标签（带颜色映射）
│   │   │   ├── TaskPriorityTag.vue    # 优先级标签
│   │   │   ├── TaskProgressBar.vue    # 执行进度条（实时更新）
│   │   │   ├── TaskStatusFlow.vue     # 状态流转图（可视化）
│   │   │   ├── TaskTimeline.vue       # 操作历史时间线
│   │   │   ├── TaskStagePanel.vue     # 执行阶段面板
│   │   │   └── ApprovalGateModal.vue  # 授权确认弹窗（方案确认）
│   │   ├── monitor/
│   │   │   ├── MetricCard.vue         # 指标卡片（磁盘/内存/连接数）
│   │   │   └── AlertLevelTag.vue      # 告警级别标签
│   │   └── cost/
│   │       └── TokenUsageChart.vue    # Token 消耗趋势图
│   │
│   └── base/                  # 基础组件（无业务逻辑，可跨项目复用）
│       ├── BaseTable.vue              # 封装 el-table（分页 + 加载 + 空状态）
│       ├── BaseForm.vue               # 封装 el-form（统一布局和校验）
│       ├── BaseSearchBar.vue          # 统一搜索栏（筛选条件收起/展开）
│       ├── BaseConfirmModal.vue       # 二次确认弹窗（数据修改通用）
│       ├── BaseExportButton.vue       # Excel 导出按钮（含下载逻辑封装）
│       ├── BaseStatusDot.vue          # 状态圆点指示器
│       ├── BaseEmptyState.vue         # 空数据状态展示
│       └── BasePageHeader.vue         # 页面顶部标题 + 操作按钮区域
│
├── composables/               # 可复用逻辑（Composition API Hooks）
│   ├── usePageQuery.ts        # 分页查询通用逻辑（page/pageSize/loading/reset）
│   ├── useExport.ts           # Excel 导出通用逻辑
│   ├── useConfirm.ts          # 二次确认弹窗逻辑
│   ├── usePermission.ts       # 权限判断工具
│   ├── useWebSocket.ts        # WebSocket 连接管理
│   └── useTaskStatus.ts       # 任务状态映射（中文/颜色/图标）
│
├── directives/                # 自定义指令
│   └── permission.ts          # v-permission 指令（按钮级权限控制）
│
├── utils/                     # 工具函数
│   ├── format.ts              # 日期/数字/状态格式化
│   ├── download.ts            # 文件下载工具
│   └── validate.ts            # 表单校验规则
│
├── constants/                 # 前端常量
│   ├── task.ts                # 任务状态、类型、优先级的枚举与映射
│   ├── permission.ts          # 权限标识常量
│   └── route.ts               # 路由名称常量（避免字符串散落）
│
└── assets/                    # 静态资源
    ├── styles/
    │   ├── variables.scss     # 设计 Token（颜色、间距、字体）
    │   ├── element-override.scss  # Element Plus 主题覆盖
    │   └── global.scss        # 全局基础样式（reset + 工具类）
    └── icons/                 # SVG 图标
```

---

## 二、页面路由设计

### 2.1 路由整体结构

```
/                              → 重定向到 /task/board
│
├── /login                     → LoginPage（BlankLayout，公开路由）
│
├── /                          → DefaultLayout（登录后布局）
│   │
│   ├── /task                  → 任务管理模块
│   │   ├── /task/board        → TaskBoardPage      任务看板
│   │   ├── /task/list         → TaskListPage       任务列表
│   │   ├── /task/create       → TaskCreatePage     新建需求单
│   │   ├── /task/:id          → TaskDetailPage     任务详情
│   │   └── /task/:id/edit     → TaskEditPage       编辑需求单
│   │
│   ├── /review                → 评审与授权模块
│   │   ├── /review/pending    → ReviewPendingPage  待评审列表
│   │   └── /review/approvals  → ApprovalGatePage   人工授权网关
│   │
│   ├── /deploy                → 部署管理模块
│   │   ├── /deploy/list       → DeployListPage     部署申请列表
│   │   └── /deploy/:id        → DeployDetailPage   部署详情与审批
│   │
│   ├── /monitor               → 运维监控模块
│   │   ├── /monitor/dashboard → MetricsDashboardPage  系统指标仪表盘
│   │   ├── /monitor/inspections        → InspectionListPage   巡检报告列表
│   │   ├── /monitor/inspections/:id   → InspectionDetailPage  巡检详情
│   │   └── /monitor/alerts    → AlertListPage      告警记录
│   │
│   ├── /knowledge             → 知识库模块
│   │   ├── /knowledge/docs    → KnowledgeDocListPage   知识文档管理
│   │   └── /knowledge/search  → KnowledgeSearchPage    知识检索测试
│   │
│   ├── /assertion             → 断言库模块
│   │   ├── /assertion/list    → AssertionListPage  断言列表
│   │   └── /assertion/batches → AssertionBatchPage 批次执行与结果
│   │
│   ├── /cost                  → 成本统计模块
│   │   ├── /cost/daily        → CostDailyPage      Token 日消耗
│   │   └── /cost/stat         → CostStatPage       多维度统计
│   │
│   └── /system                → 系统管理模块
│       └── /system/users      → UserManagePage     用户管理
│
├── /403                       → 403Page（无权限）
└── /404                       → 404Page（路由不存在）
```

### 2.2 路由 Meta 约定

每条路由的 `meta` 字段统一定义以下属性，**不得随意新增未定义的 meta 字段**：

```typescript
// src/types/common.ts
export interface RouteMeta {
  /** 页面标题（显示在浏览器 Tab 和面包屑中） */
  title: string
  /** 所需权限标识，undefined 表示已登录即可访问 */
  permission?: Permission
  /** 所需角色（角色满足其一即可，比权限粒度粗，二选一使用）*/
  roles?: Role[]
  /** 是否显示在侧边栏导航中 */
  inMenu?: boolean
  /** 侧边栏图标（Element Plus icon 组件名） */
  icon?: string
  /** 是否在面包屑中隐藏（详情页等不需要面包屑的页面） */
  hideBreadcrumb?: boolean
  /** 是否需要缓存（keep-alive，列表页建议开启） */
  keepAlive?: boolean
  /** 排序权重（菜单显示顺序，数字越小越靠前） */
  menuOrder?: number
}
```

### 2.3 路由模块定义示例

```typescript
// src/router/modules/task.ts
import type { RouteRecordRaw } from 'vue-router'
import { PERMISSIONS } from '@/constants/permission'

export const taskRoutes: RouteRecordRaw[] = [
  {
    path: '/task/board',
    name: 'TaskBoard',
    component: () => import('@/views/task/TaskBoardPage.vue'),
    meta: {
      title: '任务看板',
      permission: PERMISSIONS.TASK_READ,
      inMenu: true,
      icon: 'KanbanIcon',
      keepAlive: false,
      menuOrder: 10
    }
  },
  {
    path: '/task/list',
    name: 'TaskList',
    component: () => import('@/views/task/TaskListPage.vue'),
    meta: {
      title: '任务列表',
      permission: PERMISSIONS.TASK_READ,
      inMenu: true,
      icon: 'ListIcon',
      keepAlive: true,        // 列表页开启缓存，返回时保留筛选状态
      menuOrder: 11
    }
  },
  {
    path: '/task/create',
    name: 'TaskCreate',
    component: () => import('@/views/task/TaskCreatePage.vue'),
    meta: {
      title: '新建需求单',
      permission: PERMISSIONS.TASK_WRITE,
      inMenu: false           // 不显示在菜单中，从看板/列表页入口进入
    }
  },
  {
    path: '/task/:id',
    name: 'TaskDetail',
    component: () => import('@/views/task/TaskDetailPage.vue'),
    meta: {
      title: '任务详情',
      permission: PERMISSIONS.TASK_READ,
      inMenu: false,
      hideBreadcrumb: false
    }
  },
  {
    path: '/task/:id/edit',
    name: 'TaskEdit',
    component: () => import('@/views/task/TaskEditPage.vue'),
    meta: {
      title: '编辑需求单',
      permission: PERMISSIONS.TASK_WRITE,
      inMenu: false
    }
  }
]
```

### 2.4 权限与菜单可见性映射

| 路由路径 | 页面 | 所需权限 | 可见角色 |
|--------|------|--------|--------|
| `/task/board` | 任务看板 | `task:read` | 全部（BUSINESS_USER 仅见自己的） |
| `/task/list` | 任务列表 | `task:read` | 全部 |
| `/task/create` | 新建需求单 | `task:write` | BUSINESS_USER、TECH_LEAD |
| `/task/:id` | 任务详情 | `task:read` | 全部（BUSINESS_USER 仅自己的） |
| `/task/:id/edit` | 编辑需求单 | `task:write` | BUSINESS_USER、TECH_LEAD（仅 DRAFT/REJECTED） |
| `/review/pending` | 待评审列表 | `task:review` | IT_REVIEWER、IT_MANAGER、TECH_LEAD |
| `/review/approvals` | 人工授权网关 | `approval:write` | IT_REVIEWER、IT_MANAGER、TECH_LEAD |
| `/deploy/list` | 部署申请列表 | `task:read` | IT_REVIEWER、IT_MANAGER、TECH_LEAD |
| `/deploy/:id` | 部署详情与审批 | `deploy:approve` | IT_MANAGER、TECH_LEAD |
| `/monitor/dashboard` | 系统指标仪表盘 | `monitor:read` | IT_REVIEWER、IT_MANAGER、TECH_LEAD、MANAGER |
| `/monitor/inspections` | 巡检报告列表 | `monitor:read` | IT_REVIEWER、IT_MANAGER、TECH_LEAD、MANAGER |
| `/monitor/alerts` | 告警记录 | `monitor:read` | IT_REVIEWER、IT_MANAGER、TECH_LEAD、MANAGER |
| `/knowledge/docs` | 知识文档管理 | `knowledge:upload` | IT_REVIEWER、IT_MANAGER、TECH_LEAD |
| `/knowledge/search` | 知识检索测试 | `knowledge:upload` | IT_REVIEWER、IT_MANAGER、TECH_LEAD |
| `/assertion/list` | 断言列表 | `assertion:manage` | TECH_LEAD |
| `/assertion/batches` | 批次执行结果 | `assertion:manage` | TECH_LEAD |
| `/cost/daily` | Token 日消耗 | `cost:read` | IT_REVIEWER、IT_MANAGER、TECH_LEAD、MANAGER |
| `/cost/stat` | 多维度统计 | `cost:read` | IT_REVIEWER、IT_MANAGER、TECH_LEAD、MANAGER |
| `/system/users` | 用户管理 | `system:admin` | IT_MANAGER、TECH_LEAD |

### 2.5 路由常量定义

```typescript
// src/constants/route.ts
// 路由名称集中管理，禁止在组件中直接使用字符串
export const ROUTE_NAMES = {
  LOGIN:               'Login',
  TASK_BOARD:          'TaskBoard',
  TASK_LIST:           'TaskList',
  TASK_CREATE:         'TaskCreate',
  TASK_DETAIL:         'TaskDetail',
  TASK_EDIT:           'TaskEdit',
  REVIEW_PENDING:      'ReviewPending',
  APPROVAL_GATE:       'ApprovalGate',
  DEPLOY_LIST:         'DeployList',
  DEPLOY_DETAIL:       'DeployDetail',
  MONITOR_DASHBOARD:   'MonitorDashboard',
  INSPECTION_LIST:     'InspectionList',
  INSPECTION_DETAIL:   'InspectionDetail',
  ALERT_LIST:          'AlertList',
  KNOWLEDGE_DOC_LIST:  'KnowledgeDocList',
  KNOWLEDGE_SEARCH:    'KnowledgeSearch',
  ASSERTION_LIST:      'AssertionList',
  ASSERTION_BATCH:     'AssertionBatch',
  COST_DAILY:          'CostDaily',
  COST_STAT:           'CostStat',
  SYSTEM_USERS:        'SystemUsers',
  ERROR_403:           'Error403',
  ERROR_404:           'Error404'
} as const
```

---

## 三、组件层级划分

### 3.1 布局层（Layouts）

布局组件负责页面骨架，**不包含业务逻辑**：

```
DefaultLayout.vue
├── AppSidebar.vue    ← 侧边导航，根据角色权限动态渲染菜单项
├── AppHeader.vue     ← 顶部栏（用户名、角色、通知铃铛、退出登录）
├── AppBreadcrumb.vue ← 面包屑（根据路由 meta.title 自动生成）
└── <router-view />   ← 页面内容区（含 keep-alive）

BlankLayout.vue       ← 仅 <router-view />，用于登录页、403、404
```

**侧边栏菜单生成规则**（`useMenus.ts`）：

```typescript
// src/layouts/composables/useMenus.ts
export function useMenus() {
  const userStore = useUserStore()

  // 从路由表中筛选：inMenu=true 且当前用户有权限的路由
  const menus = computed(() =>
    router.getRoutes()
      .filter(r => r.meta?.inMenu)
      .filter(r => {
        const perm = r.meta?.permission as Permission | undefined
        return !perm || userStore.hasPermission(perm)
      })
      .sort((a, b) => (a.meta?.menuOrder ?? 99) - (b.meta?.menuOrder ?? 99))
  )

  return { menus }
}
```

### 3.2 页面层（Views）

**职责**：数据获取、页面级状态管理、将数据传递给业务组件。

**约束**：
- 每个页面对应路由中的一个叶节点
- 文件名以 `Page.vue` 结尾（强制区分于可复用组件）
- 页面自身不写复杂 DOM，**复杂 UI 块提取为业务组件**
- 页面可直接调用 `api/` 下的接口，也可通过 store 间接调用
- 页面负责处理路由参数（`useRoute().params.id`）

```
页面层组件大小参考：
├── 简单页面（表单/详情展示）：< 150 行模板 + script
├── 中等页面（含搜索表格）：< 250 行
└── 超过 250 行：必须将 UI 块抽为业务组件
```

### 3.3 业务组件层（components/business）

**职责**：封装跨页面复用的、含业务语义的 UI 组件。

**约束**：
- 通过 `props` 接收数据，`emit` 向上通知事件，**禁止在业务组件内直接调用 API**
- 允许读取 store 中的只读状态（如权限判断），**禁止在业务组件中修改全局 store**
- 文件名使用 PascalCase（如 `TaskCard.vue`），放入对应模块子目录
- 包含明确的 `props` 类型定义和 `emits` 声明

```typescript
// ✅ 正确：业务组件通过 props 接收数据
// components/business/task/TaskCard.vue
const props = defineProps<{
  task: TaskListItem
  showProgress?: boolean
}>()

const emit = defineEmits<{
  (e: 'click', task: TaskListItem): void
  (e: 'quick-approve', taskId: number): void
}>()

// ❌ 禁止：业务组件内直接调用 API
const res = await getTaskDetail(props.task.id)  // 禁止！应由页面层处理
```

### 3.4 基础组件层（components/base）

**职责**：无业务逻辑的通用 UI 组件，可跨项目复用。

**约束**：
- **绝对禁止**引入 `api/`、`stores/`、`types/` 中的业务类型
- 仅依赖 `props`、`emit`、`slots` 进行通信
- 对 Element Plus 组件的二次封装须有明确的增量价值（统一样式、统一行为）

```
BaseTable.vue          ← el-table + 分页 + 加载骨架 + 空状态的统一封装
BaseForm.vue           ← el-form 统一布局（label 对齐、宽度规范）
BaseSearchBar.vue      ← 筛选条件区域（折叠/展开、重置按钮）
BaseConfirmModal.vue   ← 二次确认弹窗（所有数据写操作必须使用）
BaseExportButton.vue   ← Excel 导出按钮（含 loading 状态和下载触发逻辑）
BaseStatusDot.vue      ← 状态圆点（传入 color 和 text）
BaseEmptyState.vue     ← 空数据占位（统一图标和文案风格）
BasePageHeader.vue     ← 页面标题 + 面包屑 + 右侧操作按钮区域
```

### 3.5 组件层级关系图

```
DefaultLayout
└── Page（views/）
    ├── BasePageHeader          ← 标题区（基础）
    ├── BaseSearchBar           ← 搜索筛选区（基础）
    ├── BaseTable               ← 数据表格（基础）
    │   └── [slot: column]
    │       ├── TaskStatusTag   ← 状态标签（业务）
    │       ├── TaskPriorityTag ← 优先级标签（业务）
    │       └── [操作按钮区]
    │           └── BaseConfirmModal  ← 二次确认（基础）
    └── [Modal/Drawer]
        └── BusinessComponent   ← 弹窗内的业务组件
```

### 3.6 组件通信规则

| 通信场景 | 推荐方式 | 禁止方式 |
|--------|--------|--------|
| 父 → 子数据传递 | `props` | `provide/inject`（非必要不用） |
| 子 → 父事件通知 | `emit` | 直接修改 props（禁止） |
| 兄弟组件通信 | 提升到共同父组件或 store | 直接引用（禁止） |
| 跨层级只读状态 | `provide/inject`（仅限布局层） 或 store | — |
| 全局共享状态 | Pinia store | EventBus（禁止） |
| 路由参数传递 | `vue-router` `params`/`query` | `$root`（禁止） |

---

## 四、状态管理约定（Pinia）

### 4.1 Store 设计原则

- **每个业务域一个 store**，禁止将所有状态放入单一巨型 store
- **store 命名**：`use{模块}Store`，文件名 `{模块}.ts`
- **store 内容**：只存放需要跨组件共享的状态；组件内局部状态用 `ref/reactive`
- **store 不直接处理 UI 逻辑**（不调用 `ElMessage`、不操作 DOM）

### 4.2 用户身份 Store（核心）

```typescript
// src/stores/user.ts
import { defineStore } from 'pinia'
import type { UserInfo, Permission, Role } from '@/types/user'
import { login, logout } from '@/api/system'

export const useUserStore = defineStore('user', () => {
  // ── State ──────────────────────────────────────────────────────
  const token = ref<string>(localStorage.getItem('accessToken') ?? '')
  const refreshToken = ref<string>(localStorage.getItem('refreshToken') ?? '')
  const userInfo = ref<UserInfo | null>(null)

  // ── Getters ────────────────────────────────────────────────────

  /** 是否已登录 */
  const isLoggedIn = computed(() => !!token.value && !!userInfo.value)

  /** 当前角色 */
  const role = computed(() => userInfo.value?.role ?? '')

  /** 权限列表（字符串数组） */
  const permissions = computed(() => userInfo.value?.permissions ?? [])

  /** 判断是否拥有指定权限 */
  function hasPermission(permission: Permission): boolean {
    return permissions.value.includes(permission)
  }

  /** 判断是否拥有指定角色之一 */
  function hasRole(...roles: Role[]): boolean {
    return roles.includes(role.value as Role)
  }

  /** 是否只能查看自己的任务（BUSINESS_USER 限制） */
  const isOwnTaskOnly = computed(() =>
    role.value === 'BUSINESS_USER'
  )

  // ── Actions ────────────────────────────────────────────────────

  /** 登录：获取 Token 并存储用户信息 */
  async function doLogin(username: string, password: string) {
    const res = await login({ username, password })
    token.value = res.data.accessToken
    refreshToken.value = res.data.refreshToken
    userInfo.value = res.data.userInfo
    localStorage.setItem('accessToken', token.value)
    localStorage.setItem('refreshToken', refreshToken.value)
  }

  /** 登出：清除所有状态 */
  async function doLogout() {
    try {
      await logout()
    } finally {
      clearToken()
    }
  }

  /** 清除 Token（Token 过期/被吊销时调用） */
  function clearToken() {
    token.value = ''
    refreshToken.value = ''
    userInfo.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }

  return {
    token, refreshToken, userInfo,
    isLoggedIn, role, permissions, isOwnTaskOnly,
    hasPermission, hasRole,
    doLogin, doLogout, clearToken
  }
})
```

### 4.3 任务管理 Store

```typescript
// src/stores/task.ts
// 只存跨页面共享的任务状态；单页面使用的数据用组件内 ref 管理
export const useTaskStore = defineStore('task', () => {

  // ── 看板/列表共享的筛选条件（列表页 → 详情页 → 返回列表页保持筛选）
  const lastQueryParams = ref<PageQueryTaskDTO>({
    page: 1, pageSize: 20, sortBy: 'updatedAt', sortOrder: 'desc'
  })

  // ── 各状态任务计数（用于看板列头角标、菜单角标）
  const statusCounts = ref<Record<string, number>>({})

  /** 刷新各状态计数（看板页面挂载时调用） */
  async function refreshStatusCounts() {
    const res = await getTaskStatusCounts()
    statusCounts.value = res.data
  }

  /** 保存列表页查询条件（切换到详情页再返回时恢复） */
  function saveQueryParams(params: PageQueryTaskDTO) {
    lastQueryParams.value = { ...params }
  }

  return { lastQueryParams, statusCounts, refreshStatusCounts, saveQueryParams }
})
```

### 4.4 通知 Store

```typescript
// src/stores/notification.ts
// 管理系统内部通知（评审待办角标、授权超时提醒等）
export const useNotificationStore = defineStore('notification', () => {

  /** 待评审任务数（IT_REVIEWER 角色使用） */
  const pendingReviewCount = ref(0)

  /** 待授权任务数（IT_REVIEWER、IT_MANAGER 使用） */
  const pendingApprovalCount = ref(0)

  /** 未确认告警数（运维人员使用） */
  const unconfirmedAlertCount = ref(0)

  /** 轮询刷新角标数（每 60 秒一次，仅登录后启动） */
  let pollTimer: ReturnType<typeof setInterval> | null = null

  function startPolling() {
    refreshCounts()
    pollTimer = setInterval(refreshCounts, 60_000)
  }

  function stopPolling() {
    if (pollTimer) clearInterval(pollTimer)
  }

  async function refreshCounts() {
    const userStore = useUserStore()
    if (!userStore.isLoggedIn) return

    if (userStore.hasPermission('task:review')) {
      const res = await getPendingReviewCount()
      pendingReviewCount.value = res.data.count
    }
    if (userStore.hasPermission('approval:write')) {
      const res = await getPendingApprovalCount()
      pendingApprovalCount.value = res.data.count
    }
    if (userStore.hasPermission('monitor:read')) {
      const res = await getUnconfirmedAlertCount()
      unconfirmedAlertCount.value = res.data.count
    }
  }

  return {
    pendingReviewCount, pendingApprovalCount, unconfirmedAlertCount,
    startPolling, stopPolling, refreshCounts
  }
})
```

### 4.5 Store 使用约定汇总

| 约定项 | 规则 |
|--------|------|
| store 中存什么 | 跨组件/跨页面的共享状态、用户身份、通知角标 |
| store 中不存什么 | 单页面临时状态（用组件内 `ref`）、表单数据、弹窗可见性 |
| action 中可以做什么 | 调用 `api/`、修改 state、触发其他 action |
| action 中不可以做什么 | 调用 `ElMessage`、操作 DOM、访问 `useRoute` |
| 禁止模式 | store 相互循环依赖；在 setup 外调用 store（须在 `onMounted` 或 `setup` 内调用） |
| 数据持久化 | 仅 `user.ts` 中的 token 持久化到 `localStorage`，其他 store 不持久化 |

---

## 五、权限守卫实现

### 5.1 路由级守卫（最高优先级）

```typescript
// src/router/guards.ts
import { ROUTE_NAMES } from '@/constants/route'

/**
 * 全局前置路由守卫
 * 执行顺序：
 *   1. 未登录 → 重定向登录页
 *   2. 无权限 → 重定向 403
 *   3. 通过 → 正常渲染
 */
export function setupRouterGuards(router: Router) {
  router.beforeEach(async (to, from, next) => {
    const userStore = useUserStore()

    // ── 步骤1：公开路由（login、403、404）直接放行
    if (to.name === ROUTE_NAMES.LOGIN
     || to.name === ROUTE_NAMES.ERROR_403
     || to.name === ROUTE_NAMES.ERROR_404) {
      // 已登录用户访问登录页 → 重定向首页
      if (to.name === ROUTE_NAMES.LOGIN && userStore.isLoggedIn) {
        return next({ name: ROUTE_NAMES.TASK_BOARD })
      }
      return next()
    }

    // ── 步骤2：未登录 → 跳转登录，并记录目标地址（登录后回跳）
    if (!userStore.isLoggedIn) {
      return next({
        name: ROUTE_NAMES.LOGIN,
        query: { redirect: to.fullPath }
      })
    }

    // ── 步骤3：检查路由所需权限
    const requiredPermission = to.meta?.permission as Permission | undefined
    if (requiredPermission && !userStore.hasPermission(requiredPermission)) {
      return next({ name: ROUTE_NAMES.ERROR_403 })
    }

    // ── 步骤4：检查路由所需角色（permission 和 roles 二选一，permission 优先）
    const requiredRoles = to.meta?.roles as Role[] | undefined
    if (requiredRoles && !userStore.hasRole(...requiredRoles)) {
      return next({ name: ROUTE_NAMES.ERROR_403 })
    }

    // ── 步骤5：动态设置 document.title
    document.title = to.meta?.title
      ? `${to.meta.title} - 芯智云匠`
      : '芯智云匠 · MES AI'

    next()
  })
}
```

### 5.2 组件级权限控制（`v-permission` 指令）

用于控制**按钮、操作区域**的显示/隐藏，细粒度到 DOM 元素级别：

```typescript
// src/directives/permission.ts
import type { Directive } from 'vue'
import { useUserStore } from '@/stores/user'
import type { Permission } from '@/types/user'

/**
 * v-permission 自定义指令
 *
 * 用法：
 *   v-permission="'task:write'"           单一权限
 *   v-permission="['task:write', 'task:review']"  任一权限满足即显示
 *
 * 无权限时：DOM 节点从页面移除（不是 display:none，而是完全不渲染）
 */
export const permissionDirective: Directive = {
  mounted(el, binding) {
    const userStore = useUserStore()
    const required = binding.value

    const hasAccess = Array.isArray(required)
      ? required.some(p => userStore.hasPermission(p as Permission))
      : userStore.hasPermission(required as Permission)

    if (!hasAccess) {
      // 从 DOM 中移除，而不是隐藏（防止通过 CSS 绕过）
      el.parentNode?.removeChild(el)
    }
  }
}

// src/main.ts 注册
app.directive('permission', permissionDirective)
```

**使用示例**：

```vue
<template>
  <!-- 单一权限：只有 task:write 权限的用户才能看到新建按钮 -->
  <el-button v-permission="'task:write'" type="primary" @click="goCreate">
    新建需求单
  </el-button>

  <!-- 多权限（任一满足）：IT 评审员或 IT 负责人才能看到导出按钮 -->
  <BaseExportButton
    v-permission="['task:export', 'system:admin']"
    @export="handleExport"
  />

  <!-- 操作按钮组 -->
  <el-table-column label="操作" width="200">
    <template #default="{ row }">
      <!-- 评审按钮：仅 IT 角色可见 -->
      <el-button v-permission="'task:review'" link @click="handleReview(row)">
        评审
      </el-button>
      <!-- 验收按钮：有验收权限且任务处于待验收状态 -->
      <el-button
        v-permission="'task:accept'"
        v-if="row.status === 'PENDING_REVIEW'"
        link
        @click="handleAccept(row)"
      >
        验收
      </el-button>
    </template>
  </el-table-column>
</template>
```

### 5.3 逻辑层权限判断（usePermission）

用于 `v-if` 内嵌逻辑，或在 `<script setup>` 中做条件处理：

```typescript
// src/composables/usePermission.ts
import { useUserStore } from '@/stores/user'
import type { Permission, Role } from '@/types/user'

export function usePermission() {
  const userStore = useUserStore()

  /** 是否有指定权限（响应式） */
  const hasPermission = (permission: Permission) =>
    computed(() => userStore.hasPermission(permission))

  /** 是否有指定角色之一（响应式） */
  const hasRole = (...roles: Role[]) =>
    computed(() => userStore.hasRole(...roles))

  /** 是否可以操作某个任务（考虑 BUSINESS_USER 的数据隔离） */
  const canOperateTask = (task: { submitterId: number }) =>
    computed(() => {
      if (userStore.hasPermission('task:review')) return true   // IT 以上全可操作
      return task.submitterId === userStore.userInfo?.userId    // 业务人员只能操作自己的
    })

  return { hasPermission, hasRole, canOperateTask }
}
```

**在组件中使用**：

```vue
<script setup lang="ts">
const { hasPermission, canOperateTask } = usePermission()

// 是否显示部署按钮
const canDeploy = hasPermission('deploy:approve')
</script>

<template>
  <!-- 使用 computed 结果直接绑定 v-if -->
  <el-button v-if="canDeploy.value" @click="handleDeploy">审批部署</el-button>

  <!-- 数据隔离：BUSINESS_USER 只能编辑自己的任务 -->
  <el-button
    v-if="canOperateTask(task).value"
    @click="handleEdit(task.id)"
  >
    编辑
  </el-button>
</template>
```

### 5.4 权限控制分层决策

```
用户请求操作
      │
      ▼
┌─────────────────────────────────────────────────────┐
│  第1层：路由守卫（router/guards.ts）                 │
│  → 控制"能不能进入这个页面"                         │
│  → 无权限跳转 /403                                  │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│  第2层：v-permission 指令（显示/隐藏操作按钮）       │
│  → 控制"页面上哪些操作入口可见"                     │
│  → DOM 节点完全移除，防止 CSS 绕过                  │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│  第3层：业务逻辑判断（usePermission / canOperate）   │
│  → 控制"数据隔离"（如 BUSINESS_USER 只看自己的）    │
│  → 控制"状态相关"（如只有 PENDING_REVIEW 才能验收） │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│  第4层：后端 API 鉴权（最终防线）                   │
│  → 即使前端漏检，后端 RBAC 强制拦截，返回 403       │
└─────────────────────────────────────────────────────┘
```

> **原则**：前端权限控制是用户体验层，**后端 API 是唯一可信防线**。前端权限判断出错不会导致安全漏洞，因为后端 RBAC 会最终拦截。

---

## 六、组件编码规范

### 6.1 `<script setup>` 内部组织顺序

所有组件的 `<script setup>` 内容**必须按以下顺序组织**，禁止随意混排：

```typescript
<script setup lang="ts">
// ─── 1. 第三方库 import ──────────────────────────────────────────
import { ref, reactive, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

// ─── 2. 内部模块 import（api / stores / composables / types）─────
import { getTaskList, createTask } from '@/api/task'
import { useTaskStore } from '@/stores/task'
import { usePageQuery } from '@/composables/usePageQuery'
import { usePermission } from '@/composables/usePermission'
import type { TaskListItem, CreateTaskDTO } from '@/types/task'

// ─── 3. 子组件 import ────────────────────────────────────────────
import TaskStatusTag from '@/components/business/task/TaskStatusTag.vue'
import BaseTable from '@/components/base/BaseTable.vue'

// ─── 4. Props 和 Emits 定义 ──────────────────────────────────────
const props = defineProps<{
  initialStatus?: string
}>()

const emit = defineEmits<{
  (e: 'created', taskId: number): void
}>()

// ─── 5. Router / Route ───────────────────────────────────────────
const router = useRouter()
const route = useRoute()

// ─── 6. Store ────────────────────────────────────────────────────
const taskStore = useTaskStore()

// ─── 7. Composables ──────────────────────────────────────────────
const { queryParams, loading, resetQuery } = usePageQuery()
const { hasPermission } = usePermission()

// ─── 8. 响应式状态（ref / reactive）─────────────────────────────
const taskList = ref<TaskListItem[]>([])
const total = ref(0)
const selectedTask = ref<TaskListItem | null>(null)
const showCreateModal = ref(false)

// ─── 9. 计算属性（computed）─────────────────────────────────────
const canCreate = hasPermission('task:write')
const filteredList = computed(() => /* ... */ taskList.value)

// ─── 10. 方法（以功能分组，非字母顺序）─────────────────────────
// 10a. 数据加载
async function loadTaskList() { /* ... */ }

// 10b. 事件处理
function handleSearch() { /* ... */ }
function handleReset() { resetQuery(); loadTaskList() }
async function handleDelete(task: TaskListItem) { /* ... */ }

// 10c. 导航
function goToDetail(id: number) {
  router.push({ name: ROUTE_NAMES.TASK_DETAIL, params: { id } })
}

// ─── 11. 生命周期钩子 ────────────────────────────────────────────
onMounted(() => {
  loadTaskList()
})
</script>
```

### 6.2 Props 设计约定

```typescript
// ✅ 正确：明确类型，有合理默认值，必填项标注
const props = withDefaults(defineProps<{
  taskId: number           // 必填，无默认值
  showActions?: boolean    // 可选，有默认值
  maxHeight?: number       // 可选，有默认值
}>(), {
  showActions: true,
  maxHeight: 400
})

// ❌ 禁止：使用 any 类型
defineProps<{ data: any }>()

// ❌ 禁止：Props 名与 HTML 属性同名（如 class、style、id）
// ❌ 禁止：Props 直接修改（需要 computed setter 或 emit update:xxx）
```

### 6.3 命名规范速查

| 对象 | 规范 | 示例 |
|------|------|------|
| 组件文件名 | PascalCase | `TaskStatusTag.vue` |
| 页面文件名 | PascalCase + `Page` 后缀 | `TaskListPage.vue` |
| Composable 文件名 | camelCase + `use` 前缀 | `usePageQuery.ts` |
| store 文件名 | camelCase | `task.ts` |
| API 文件名 | camelCase | `task.ts` |
| 类型文件名 | camelCase | `task.ts` |
| Props 名 | camelCase | `taskId`、`showActions` |
| Emit 事件名 | camelCase（kebab-case 在模板中） | `taskCreated` / `@task-created` |
| CSS 类名 | kebab-case | `.task-status-tag` |
| 模板中组件引用 | PascalCase | `<TaskStatusTag />` |

### 6.4 禁止的写法

```typescript
// ❌ 禁止1：mutate props
props.task.status = 'CLOSED'    // 禁止！应 emit 事件由父组件处理

// ❌ 禁止2：在模板中写复杂逻辑
// 模板中只允许简单变量引用和方法调用，复杂逻辑抽为 computed
<span>{{ tasks.filter(t => t.status === 'DRAFT').length }}</span>   // 禁止
<span>{{ draftCount }}</span>   // 正确：用 computed 属性

// ❌ 禁止3：组件直接调用 API
const res = await getTaskDetail(id)   // 页面层可以，业务组件不可以

// ❌ 禁止4：硬编码路由字符串
router.push('/task/list')             // 禁止
router.push({ name: ROUTE_NAMES.TASK_LIST })   // 正确

// ❌ 禁止5：没有 v-key 的 v-for
<div v-for="task in taskList">...</div>        // 禁止
<div v-for="task in taskList" :key="task.id">  // 正确
```

---

## 七、样式规范

### 7.1 设计 Token（全局 CSS 变量）

```scss
// src/assets/styles/variables.scss
// 所有颜色、间距、字体必须引用此文件中的变量，禁止散落的魔法值

:root {
  // ── 品牌色 ────────────────────────────────────
  --color-primary:    #409EFF;   // Element Plus 主色
  --color-success:    #67C23A;
  --color-warning:    #E6A23C;
  --color-danger:     #F56C6C;
  --color-info:       #909399;

  // ── 任务状态色（与 TaskStatusTag.vue 保持同步）─
  --status-draft:          #909399;  // 草稿：灰色
  --status-submitted:      #409EFF;  // 已提交：蓝色
  --status-reviewing:      #E6A23C;  // 评审中：橙色
  --status-approved:       #409EFF;  // 已批准：蓝色
  --status-rejected:       #F56C6C;  // 已拒绝：红色
  --status-ai-running:     #6366f1;  // AI执行中：紫色
  --status-pending-review: #F59E0B;  // 待验收：琥珀色
  --status-accepted:       #67C23A;  // 已验收：绿色
  --status-deploying:      #06B6D4;  // 部署中：青色
  --status-closed:         #67C23A;  // 已关闭：绿色
  --status-rollback:       #F56C6C;  // 已回退：红色
  --status-failed:         #F56C6C;  // 已失败：红色

  // ── 告警级别色 ───────────────────────────────
  --alert-critical: #F56C6C;
  --alert-high:     #E6A23C;
  --alert-medium:   #409EFF;
  --alert-low:      #909399;

  // ── 间距 ──────────────────────────────────────
  --spacing-xs:  4px;
  --spacing-sm:  8px;
  --spacing-md:  16px;
  --spacing-lg:  24px;
  --spacing-xl:  32px;

  // ── 字体大小 ──────────────────────────────────
  --font-size-sm:  12px;
  --font-size-md:  14px;  // 正文默认
  --font-size-lg:  16px;
  --font-size-xl:  20px;

  // ── 圆角 ──────────────────────────────────────
  --radius-sm:  4px;
  --radius-md:  8px;
  --radius-lg:  12px;

  // ── 阴影 ──────────────────────────────────────
  --shadow-card: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
}
```

### 7.2 样式编写约定

```scss
/* ✅ 正确：scoped + BEM-like 命名 */
<style scoped>
.task-card {
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);

  &__title {
    font-size: var(--font-size-lg);
    font-weight: 600;
  }

  &__status {
    margin-top: var(--spacing-sm);
  }

  /* 状态修饰符 */
  &--running {
    border-left: 3px solid var(--color-primary);
  }
}
</style>

/* ❌ 禁止：魔法值、全局类污染 */
<style>
.card { padding: 16px; }  /* 非 scoped，污染全局 */
.title { color: #409EFF; } /* 魔法值，应用变量 */
</style>
```

### 7.3 禁止覆盖 Element Plus 组件内部样式

```scss
/* ❌ 禁止：使用 :deep() 覆盖 EP 内部实现细节（版本升级后可能失效） */
:deep(.el-table__header-wrapper) {
  background: red;
}

/* ✅ 正确：使用 EP 提供的 CSS 变量覆盖 */
.my-table {
  --el-table-header-bg-color: #f0f5ff;
}
```

例外：在 `element-override.scss` 中集中统一覆盖，需注明覆盖原因：

```scss
// src/assets/styles/element-override.scss
// 统一覆盖 Element Plus 默认样式，集中管理，禁止在组件内散落覆盖

/* 原因：表格默认行高过小，中文密集场景阅读体验差 */
.el-table td.el-table__cell {
  padding: 10px 0;
}
```

---

## 八、API 调用规范

### 8.1 axios 实例配置（完整实现）

```typescript
// src/api/request.ts
import axios, { type AxiosInstance } from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import router from '@/router'
import { ROUTE_NAMES } from '@/constants/route'

// baseURL 通过环境变量注入，禁止硬编码 IP
const request: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30_000,
  headers: { 'Content-Type': 'application/json; charset=UTF-8' }
})

// ── 请求拦截 ──────────────────────────────────────────────────────
request.interceptors.request.use(config => {
  const userStore = useUserStore()
  if (userStore.token) {
    config.headers['Authorization'] = `Bearer ${userStore.token}`
  }
  // RequestId 用于后端链路追踪
  config.headers['X-Request-Id'] =
    `req-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`
  return config
})

// ── 响应拦截 ──────────────────────────────────────────────────────
request.interceptors.response.use(
  response => {
    // 文件下载：直接返回整个 response（调用方处理 Blob）
    if (response.config.responseType === 'blob') return response

    const { code, message, data } = response.data

    if (code === 0) return response.data   // 成功：返回 ResultVO

    // Token 失效类错误 → 清除状态，跳登录页
    if ([20001, 20002, 20003, 20004].includes(code)) {
      useUserStore().clearToken()
      router.push({ name: ROUTE_NAMES.LOGIN })
      return Promise.reject(new Error(message))
    }

    // 其他业务错误 → 全局提示（调用方也可 catch 自定义处理）
    ElMessage.error(message || '操作失败')
    return Promise.reject(new Error(message))
  },
  error => {
    // HTTP 层错误（网络断开、超时、服务器 500 等）
    const status = error.response?.status
    const msgMap: Record<number, string> = {
      401: '登录已过期，请重新登录',
      403: '您没有权限执行此操作',
      500: '服务器内部错误，请联系管理员',
      503: '服务暂时不可用，请稍后再试'
    }
    ElMessage.error(msgMap[status] ?? error.message ?? '网络错误')

    if (status === 401) {
      useUserStore().clearToken()
      router.push({ name: ROUTE_NAMES.LOGIN })
    }
    return Promise.reject(error)
  }
)

export default request
```

### 8.2 API 模块文件规范

```typescript
// src/api/task.ts
import request from './request'
import type {
  TaskListItem, TaskDetail, CreateTaskDTO,
  PageQueryTaskDTO, AcceptTaskDTO
} from '@/types/task'
import type { PageVO } from '@/types/common'

// ── 标准 CRUD ─────────────────────────────────────────────────────

export const getTaskList = (params: PageQueryTaskDTO) =>
  request.get<{ data: PageVO<TaskListItem> }>('/tasks', { params })
    .then(res => res.data)   // 统一 .then 展开，调用方直接拿到 data

export const getTaskDetail = (id: number) =>
  request.get<{ data: TaskDetail }>(`/tasks/${id}`)
    .then(res => res.data)

export const createTask = (data: CreateTaskDTO) =>
  request.post<{ data: { id: number; taskNo: string } }>('/tasks', data)
    .then(res => res.data)

export const updateTask = (id: number, data: Partial<CreateTaskDTO>) =>
  request.put<{ data: { taskId: number } }>(`/tasks/${id}`, data)
    .then(res => res.data)

export const submitTask = (taskId: number) =>
  request.post<{ data: unknown }>(`/tasks/${taskId}/submit`)
    .then(res => res.data)

export const acceptTask = (taskId: number, data: AcceptTaskDTO) =>
  request.post<{ data: unknown }>(`/tasks/${taskId}/accept`, data)
    .then(res => res.data)

// ── 导出接口（返回 Blob）─────────────────────────────────────────

export const exportTaskList = (params: Omit<PageQueryTaskDTO, 'page' | 'pageSize'>) =>
  request.get('/tasks/export', {
    params,
    responseType: 'blob',
    headers: {
      Accept: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }
  })   // 此处不 .then 展开，由 useExport composable 处理 Blob

// ── 状态计数（看板角标）─────────────────────────────────────────

export const getTaskStatusCounts = () =>
  request.get<{ data: Record<string, number> }>('/tasks/status-counts')
    .then(res => res.data)
```

---

## 九、WebSocket 实时推送规范

### 9.1 连接管理 Composable

```typescript
// src/composables/useWebSocket.ts
import { Client } from '@stomp/stompjs'
import { useUserStore } from '@/stores/user'

/**
 * 任务执行进展 WebSocket 订阅
 * 在 TaskDetailPage 的 onMounted 中调用，onUnmounted 中断开
 *
 * @param taskId  要订阅的任务 ID
 * @param onProgress  收到进展消息的回调
 */
export function useTaskProgressWS(
  taskId: Ref<number>,
  onProgress: (msg: WsProgressMessage) => void
) {
  const userStore = useUserStore()
  let client: Client | null = null

  function connect() {
    client = new Client({
      // WebSocket URL 通过环境变量注入，禁止硬编码
      brokerURL: `${import.meta.env.VITE_WS_BASE_URL}/ws/tasks/${taskId.value}/progress`
                 + `?token=${userStore.token}`,
      reconnectDelay: 30_000,   // 断线 30 秒内自动重连
      onConnect: () => {
        client!.subscribe(`/topic/task/${taskId.value}/progress`, (frame) => {
          try {
            const msg: WsProgressMessage = JSON.parse(frame.body)
            onProgress(msg)
          } catch (e) {
            console.error('[WebSocket] 消息解析失败', e)
          }
        })
      },
      onDisconnect: () => {
        // 不在此处显示 UI 提示，由重连机制自动恢复
      },
      onStompError: (frame) => {
        console.error('[WebSocket] STOMP 错误', frame)
      }
    })
    client.activate()
  }

  function disconnect() {
    client?.deactivate()
    client = null
  }

  return { connect, disconnect }
}
```

### 9.2 在页面中使用

```typescript
// views/task/TaskDetailPage.vue（关键 WebSocket 逻辑）
const progressPct = ref(0)
const currentStage = ref('')
const logLines = ref<string[]>([])

// WebSocket 仅在任务处于 AI_RUNNING 状态时连接
const { connect, disconnect } = useTaskProgressWS(
  computed(() => Number(route.params.id)),
  (msg: WsProgressMessage) => {
    if (msg.type === 'PROGRESS_UPDATE') {
      progressPct.value = msg.progressPct
      currentStage.value = msg.stage
    }
    if (msg.type === 'LOG_LINE') {
      logLines.value.push(msg.message)
      // 日志超过 500 行时裁剪（防止内存溢出）
      if (logLines.value.length > 500) logLines.value.shift()
    }
    if (msg.type === 'APPROVAL_REQUIRED') {
      // 方案确认阶段：弹出授权弹窗
      showApprovalModal.value = true
      pendingGateId.value = msg.gateId
    }
    if (msg.type === 'TASK_COMPLETED' || msg.type === 'TASK_FAILED') {
      disconnect()              // 任务结束，断开 WebSocket
      loadTaskDetail()          // 刷新任务详情
    }
  }
)

onMounted(() => {
  if (taskDetail.value?.status === 'AI_RUNNING') connect()
})

onUnmounted(() => {
  disconnect()   // 离开页面必须断开
})

// 监听状态变化（从非 AI_RUNNING 变为 AI_RUNNING 时自动连接）
watch(() => taskDetail.value?.status, (newStatus, oldStatus) => {
  if (newStatus === 'AI_RUNNING' && oldStatus !== 'AI_RUNNING') connect()
  if (newStatus !== 'AI_RUNNING') disconnect()
})
```

---

## 十、公共组件库设计

### 10.1 BaseTable — 标准数据表格

**封装能力**：分页、加载态、空状态、自动序号列（可关闭）。

```vue
<!-- 使用示例 -->
<BaseTable
  :data="taskList"
  :loading="loading"
  :total="total"
  v-model:page="queryParams.page"
  v-model:page-size="queryParams.pageSize"
  @page-change="loadTaskList"
>
  <el-table-column prop="taskNo" label="任务编号" width="200" />
  <el-table-column prop="title" label="需求标题" min-width="200" show-overflow-tooltip />
  <el-table-column label="状态" width="120">
    <template #default="{ row }">
      <TaskStatusTag :status="row.status" />
    </template>
  </el-table-column>
</BaseTable>
```

**Props 定义**：

```typescript
interface Props {
  data: unknown[]
  loading?: boolean
  total?: number            // 总条数（传入时显示分页）
  page?: number             // 当前页（v-model:page）
  pageSize?: number         // 每页条数（v-model:page-size）
  showIndex?: boolean       // 是否显示序号列，默认 true
  rowKey?: string           // 行唯一键，默认 'id'
  emptyText?: string        // 空状态文案
}
```

### 10.2 TaskStatusTag — 任务状态标签

**状态 → 颜色 → 中文** 的统一映射，确保全系统状态颜色一致：

```typescript
// src/composables/useTaskStatus.ts
// 唯一数据源：所有状态映射从这里获取，禁止在其他地方硬编码颜色/文字
export const TASK_STATUS_CONFIG: Record<TaskStatus, { label: string; color: string; type: 'success'|'warning'|'danger'|'info'|'' }> = {
  DRAFT:          { label: '草稿',    color: 'var(--status-draft)',          type: 'info'    },
  SUBMITTED:      { label: '已提交',  color: 'var(--status-submitted)',      type: ''        },
  REVIEWING:      { label: '评审中',  color: 'var(--status-reviewing)',      type: 'warning' },
  APPROVED:       { label: '已批准',  color: 'var(--status-approved)',       type: ''        },
  REJECTED:       { label: '已退回',  color: 'var(--status-rejected)',       type: 'danger'  },
  AI_RUNNING:     { label: 'AI执行中',color: 'var(--status-ai-running)',     type: ''        },
  PENDING_REVIEW: { label: '待验收',  color: 'var(--status-pending-review)', type: 'warning' },
  ACCEPTED:       { label: '已验收',  color: 'var(--status-accepted)',       type: 'success' },
  DEPLOYING:      { label: '部署中',  color: 'var(--status-deploying)',      type: ''        },
  CLOSED:         { label: '已完成',  color: 'var(--status-closed)',         type: 'success' },
  ROLLBACK:       { label: '已回退',  color: 'var(--status-rollback)',       type: 'danger'  },
  FAILED:         { label: '已失败',  color: 'var(--status-failed)',         type: 'danger'  },
}
```

### 10.3 BaseConfirmModal — 二次确认弹窗

所有涉及数据修改（增删改）的操作**必须**经过此组件，禁止直接执行：

```typescript
// src/composables/useConfirm.ts
// 封装 ElMessageBox.confirm，统一弹窗风格
export function useConfirm() {
  async function confirm(options: {
    title?: string
    message: string
    type?: 'warning' | 'danger'
    confirmText?: string
  }): Promise<boolean> {
    try {
      await ElMessageBox.confirm(options.message, options.title ?? '操作确认', {
        confirmButtonText: options.confirmText ?? '确认',
        cancelButtonText: '取消',
        type: options.type === 'danger' ? 'warning' : 'warning',
        confirmButtonClass: options.type === 'danger' ? 'el-button--danger' : ''
      })
      return true
    } catch {
      return false   // 用户点取消，返回 false，调用方据此决定是否继续
    }
  }
  return { confirm }
}

// 使用示例
const { confirm } = useConfirm()

async function handleDelete(task: TaskListItem) {
  const ok = await confirm({
    message: `确认删除需求单「${task.title}」？删除后不可恢复。`,
    type: 'danger',
    confirmText: '确认删除'
  })
  if (!ok) return

  await deleteTask(task.id)
  ElMessage.success('删除成功')
  loadTaskList()
}
```

### 10.4 BaseExportButton — Excel 导出按钮

```typescript
// src/composables/useExport.ts
export function useExport() {
  const exporting = ref(false)

  /**
   * 触发文件下载
   * @param apiFn    返回 Blob 的 API 函数
   * @param filename 下载文件名（含 .xlsx 后缀）
   */
  async function downloadExcel(
    apiFn: () => Promise<unknown>,
    filename: string
  ) {
    exporting.value = true
    try {
      const response = await apiFn() as { data: Blob; headers: Record<string, string> }
      const blob = new Blob([response.data], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      a.click()
      URL.revokeObjectURL(url)
      ElMessage.success('导出成功')
    } catch {
      ElMessage.error('导出失败，请重试')
    } finally {
      exporting.value = false
    }
  }

  return { exporting, downloadExcel }
}
```

### 10.5 usePageQuery — 分页查询通用逻辑

```typescript
// src/composables/usePageQuery.ts
// 所有带分页的列表页必须使用本 composable，禁止各自重复实现分页逻辑
export function usePageQuery<T extends { page: number; pageSize: number }>(
  defaultParams?: Partial<T>
) {
  const loading = ref(false)

  const queryParams = reactive<T>({
    page: 1,
    pageSize: 20,
    ...defaultParams
  } as T)

  function resetQuery() {
    queryParams.page = 1
    // 保留 pageSize，重置其他筛选条件
    Object.keys(queryParams).forEach(key => {
      if (key !== 'page' && key !== 'pageSize') {
        ;(queryParams as Record<string, unknown>)[key] = undefined
      }
    })
  }

  function handlePageChange(page: number) {
    queryParams.page = page
  }

  function handleSizeChange(size: number) {
    queryParams.pageSize = size
    queryParams.page = 1
  }

  return { loading, queryParams, resetQuery, handlePageChange, handleSizeChange }
}
```

---

## 十一、页面级组件设计

### 11.1 TaskDetailPage — 任务详情页（最复杂页面）

**组件树结构**：

```
TaskDetailPage.vue（页面层，负责数据获取和 WebSocket 管理）
├── BasePageHeader.vue          ← 标题 + 状态 + 操作按钮区
├── el-tabs（5个选项卡）
│   ├── Tab: 需求详情
│   │   └── TaskInfoPanel.vue  ← 业务组件：展示需求单 A/B/C 各部分
│   ├── Tab: 执行进展
│   │   ├── TaskStagePanel.vue ← 业务组件：5阶段进度可视化
│   │   └── TaskLogViewer.vue  ← 业务组件：实时日志滚动视图
│   ├── Tab: 代码文件
│   │   └── TaskArtifactList.vue  ← 业务组件：代码交付物列表（含扫描状态）
│   ├── Tab: 测试报告
│   │   └── TaskTestReportPanel.vue  ← 业务组件：测试报告展示
│   └── Tab: 审批记录
│       └── TaskApprovalHistory.vue  ← 业务组件：评审/授权/部署历史
├── TaskStatusFlow.vue          ← 右侧面板：状态流转图
├── TaskTimeline.vue            ← 操作历史时间线
└── ApprovalGateModal.vue       ← 方案确认授权弹窗（WebSocket 触发显示）
```

**操作按钮的权限与状态双重控制**：

```vue
<!-- 操作按钮区：权限（v-permission） + 状态（v-if）双重控制 -->
<template #actions>
  <!-- 提交：仅 task:write 权限 + DRAFT 状态 -->
  <el-button
    v-permission="'task:write'"
    v-if="task.status === 'DRAFT'"
    type="primary"
    @click="handleSubmit"
  >
    提交评审
  </el-button>

  <!-- 评审：仅 task:review 权限 + REVIEWING 状态 -->
  <el-button
    v-permission="'task:review'"
    v-if="task.status === 'REVIEWING'"
    type="warning"
    @click="handleReview"
  >
    开始评审
  </el-button>

  <!-- 验收：仅 task:accept 权限 + PENDING_REVIEW 状态 -->
  <el-button
    v-permission="'task:accept'"
    v-if="task.status === 'PENDING_REVIEW'"
    type="success"
    @click="handleAccept"
  >
    验收
  </el-button>

  <!-- 申请部署：仅 task:accept 权限 + ACCEPTED 状态 -->
  <el-button
    v-permission="'task:accept'"
    v-if="task.status === 'ACCEPTED'"
    type="primary"
    plain
    @click="handleApplyDeploy"
  >
    申请部署
  </el-button>
</template>
```

### 11.2 TaskBoardPage — 任务看板

**Kanban 列定义**（状态分组）：

```typescript
// 看板列定义：将任务状态分组为4个可见列
const BOARD_COLUMNS = [
  {
    key: 'pending',
    label: '待评审',
    statuses: ['DRAFT', 'SUBMITTED', 'REVIEWING'],
    color: 'var(--color-info)'
  },
  {
    key: 'running',
    label: '进行中',
    statuses: ['APPROVED', 'AI_RUNNING'],
    color: 'var(--color-primary)'
  },
  {
    key: 'review',
    label: '待验收',
    statuses: ['PENDING_REVIEW'],
    color: 'var(--color-warning)'
  },
  {
    key: 'done',
    label: '已完成',
    statuses: ['ACCEPTED', 'DEPLOYING', 'CLOSED'],
    color: 'var(--color-success)'
  }
]
```

### 11.3 ApprovalGateModal — 授权确认弹窗

此组件在任务执行阶段（`PLAN` 阶段完成后）由 WebSocket 消息触发显示，是 AI 执行流程中的关键人机交互节点：

```vue
<!-- components/business/task/ApprovalGateModal.vue -->
<template>
  <el-dialog
    v-model="visible"
    title="需要您的授权"
    width="640px"
    :close-on-click-modal="false"  <!-- 不允许点外关闭，必须明确选择 -->
    :close-on-press-escape="false"
  >
    <el-alert type="warning" :closable="false" style="margin-bottom: 16px">
      <template #title>
        任务 {{ gate?.taskNo }} 等待您授权后继续执行
      </template>
    </el-alert>

    <!-- AI 生成的实现方案摘要 -->
    <div class="approval-content">
      <div class="approval-content__section">
        <h4>📋 实现方案摘要</h4>
        <div class="plan-summary">{{ gate?.gateContent }}</div>
      </div>
    </div>

    <template #footer>
      <el-button type="danger" plain @click="handleReject">
        ❌ 退回需求
      </el-button>
      <el-button @click="handleModify">
        ✏️ 要求修改方案
      </el-button>
      <el-button type="primary" @click="handleApprove">
        ✅ 批准，开始执行
      </el-button>
    </template>
  </el-dialog>
</template>
```

---

## 十二、错误处理与用户反馈规范

### 12.1 消息反馈统一规范

| 场景 | 组件 | 持续时间 |
|------|------|--------|
| 操作成功（增删改） | `ElMessage.success` | 2 秒自动关闭 |
| 业务失败（如状态非法） | `ElMessage.error` | 3 秒自动关闭 |
| 警告提示 | `ElMessage.warning` | 3 秒自动关闭 |
| 危险操作确认 | `ElMessageBox.confirm` | 用户手动关闭 |
| 表单校验错误 | `el-form-item` 内联提示 | 始终显示 |
| 全局严重错误（服务不可用） | `ElNotification.error` | 5 秒 |

**禁止**：使用 `window.alert()`、`window.confirm()`、`console.log()` 在生产代码中。

### 12.2 接口错误的分级处理

```typescript
// 大多数情况：axios 拦截器已统一 ElMessage.error，调用方无需额外处理
await submitTask(taskId)
ElMessage.success('提交成功')   // 成功时提示，失败由拦截器处理

// 特殊情况：需要自定义错误处理（如区分不同错误码）
try {
  await approveTask(taskId, data)
  ElMessage.success('评审通过')
} catch (error: unknown) {
  // axios 拦截器已显示通用错误提示
  // 此处可做额外处理（如刷新数据、重置表单）
  queryParams.page = 1
  await loadTaskList()
}
```

### 12.3 加载状态统一规范

```vue
<template>
  <!-- 页面级加载：用 el-skeleton 骨架屏，不用转圈 loading -->
  <el-skeleton v-if="pageLoading" :rows="10" animated />

  <!-- 表格加载：通过 BaseTable 的 :loading prop 展示 -->
  <BaseTable :loading="tableLoading" :data="list" />

  <!-- 按钮操作加载：按钮 :loading 属性 -->
  <el-button :loading="submitting" @click="handleSubmit">
    {{ submitting ? '提交中...' : '提交评审' }}
  </el-button>
</template>
```

---

## 十三、附录

### 附录 A：权限常量定义

```typescript
// src/constants/permission.ts
export const PERMISSIONS = {
  TASK_READ:        'task:read',
  TASK_WRITE:       'task:write',
  TASK_REVIEW:      'task:review',
  TASK_ACCEPT:      'task:accept',
  TASK_EXPORT:      'task:export',
  APPROVAL_WRITE:   'approval:write',
  DEPLOY_APPROVE:   'deploy:approve',
  EXEC_LOG_WRITE:   'exec_log:write',
  ARTIFACT_WRITE:   'artifact:write',
  MONITOR_READ:     'monitor:read',
  MONITOR_EXPORT:   'monitor:export',
  KNOWLEDGE_UPLOAD: 'knowledge:upload',
  ASSERTION_MANAGE: 'assertion:manage',
  COST_READ:        'cost:read',
  COST_EXPORT:      'cost:export',
  SYSTEM_ADMIN:     'system:admin'
} as const

export type Permission = typeof PERMISSIONS[keyof typeof PERMISSIONS]

export const ROLES = {
  BUSINESS_USER:  'BUSINESS_USER',
  IT_REVIEWER:    'IT_REVIEWER',
  IT_MANAGER:     'IT_MANAGER',
  TECH_LEAD:      'TECH_LEAD',
  AI_AGENT:       'AI_AGENT',
  MANAGER:        'MANAGER'
} as const

export type Role = typeof ROLES[keyof typeof ROLES]
```

### 附录 B：环境变量配置

```bash
# .env.development
VITE_API_BASE_URL=http://localhost:8080/api/v1
VITE_WS_BASE_URL=ws://localhost:8080

# .env.test
VITE_API_BASE_URL=https://ai-mes-test.xingtong.internal/api/v1
VITE_WS_BASE_URL=wss://ai-mes-test.xingtong.internal

# .env.production
VITE_API_BASE_URL=https://ai-mes.xingtong.internal/api/v1
VITE_WS_BASE_URL=wss://ai-mes.xingtong.internal

# 禁止在代码中出现 .env 文件中的具体值（IP/域名）
# 所有 URL 通过 import.meta.env.VITE_* 引用
```

### 附录 C：新页面开发 Checklist

开发新页面或组件时，对照以下清单确认：

```
页面路由
□ 路由已在对应 modules/*.ts 文件中定义
□ meta.title、meta.permission、meta.inMenu 已正确配置
□ 路由名称已添加至 ROUTE_NAMES 常量

权限控制
□ 路由守卫通过 meta.permission 控制页面准入
□ 操作按钮使用 v-permission 指令控制可见性
□ 业务逻辑层使用 usePermission / canOperateTask 做数据隔离

组件规范
□ 文件名：页面用 XxxPage.vue，组件用 XxxComponent.vue
□ <script setup> 内容按 [import → props/emits → router/store → composables → ref/reactive → computed → methods → lifecycle] 顺序排列
□ 业务组件不直接调用 API（仅通过 props 接收数据）
□ 所有 v-for 有对应 :key

数据修改操作
□ 所有数据增删改操作有二次确认（useConfirm）
□ 操作按钮有 :loading 状态（操作中禁止重复点击）
□ 操作成功后有 ElMessage.success 提示

样式规范
□ 颜色/间距使用 CSS 变量（src/assets/styles/variables.scss）
□ style 标签有 scoped 属性
□ 无魔法值（不直接写 #409EFF、16px 等）

API 调用
□ 接口函数在 src/api/ 对应模块文件中定义
□ 组件不直接引用 axios
□ 文件导出接口使用 useExport composable

TypeScript
□ Props、Emits 有完整类型定义
□ API 返回值有对应类型声明
□ 无 any 类型（特殊情况须注释说明）
```

### 附录 D：文档版本历史

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|------|--------|
| V1.0 | 2026-04-12 | 项目经理 | 初稿编写，覆盖路由、组件层级、状态管理、权限守卫全部内容 |

---

*芯智云匠——山东芯通 MES 岗位 AI 智能体资产化项目*
*前端组件设计规范 · AI-MES-FESPEC-2026-001 · V1.0 · 2026年4月12日*
*本文件受版本控制，修改须经技术负责人批准，变更记录见 Git 历史*
