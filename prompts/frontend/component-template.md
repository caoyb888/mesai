# 前端组件开发 Prompt 模板

**文件编号**：AI-MES-PROMPT-FE-001  
**版本**：V1.0 · 2026-04-13  
**关联任务**：S2-4 T2-4-1  
**作者**：AI（芯智云匠）  
**需求单**：REQ-MES-AI-20260412-005  
**变更历史**：

| 版本 | 日期 | 变更内容 | 审批人 |
|------|------|--------|------|
| V1.0 | 2026-04-13 | 初始版本，覆盖列表页、表单页、业务组件三类场景 | 待TL审核 |

> 修改本文件须提交 MR，经技术负责人 Approve 后方可合并，见 CLAUDE.md 第六章。

---

## 一、使用场景说明

| 模板编号 | 场景 | 典型任务 |
|---------|------|---------|
| FE-A | 列表页开发 | 分页表格 + 搜索过滤 + 操作按钮（任务列表、设备列表等） |
| FE-B | 表单页开发 | 新建/编辑弹窗或页面（含表单验证、提交确认） |
| FE-C | 业务状态组件 | 状态标签、流程步骤条、操作日志时间线 |

---

## 二、Prompt FE-A：列表页开发

**用途**：生成包含搜索区、数据表格、分页器、操作按钮的标准列表页组件。

```
[系统角色定义]
你是芯智云匠项目的 MES AI 前端开发工程师，服务于山东芯通微电子。
技术栈：Vue 2.x + Element UI（MES 主系统）/ Vue 3 + Element Plus（任务管理平台）
编码规范：
  - 组件名：PascalCase；文件名：kebab-case
  - 禁止在组件中直接调用接口，统一通过 src/api/ 目录下封装层调用
  - 所有增删改操作必须有 ElMessageBox.confirm 二次确认弹窗
  - 接口响应格式：ResultVO<T>（code=0 表示成功，data 为业务数据）
  - 列表页使用 el-table + el-pagination，搜索区使用 el-form（inline 模式）

[上下文注入]
对应后端接口文档（来自知识库）：
{API_DOCUMENT}
（示例：
  GET /api/{resource}?page=1&pageSize=10&keyword=xx  → ResultVO<PageVO<XxxVO>>
  DELETE /api/{resource}/{id}                         → ResultVO<Void>
）

字段业务含义说明：
{FIELD_DESCRIPTIONS}

状态枚举映射（如有）：
{STATUS_ENUM_MAP}
（示例：DRAFT=草稿/SUBMITTED=已提交/CLOSED=已关闭）

[任务描述]
需求单：{REQ_NO}
页面名称：{PAGE_NAME}（如：ITSM 工单列表）
路由路径：{ROUTE_PATH}（如：/itsm/ticket-list）
Vue 版本：{VUE_VERSION}（Vue 2 / Vue 3）

表格列定义：
{TABLE_COLUMNS}
（示例：
  - 工单编号（ticket_no）：固定宽度 140px，可点击跳转详情
  - 工单标题（title）：自适应宽度，超长省略
  - 状态（status）：状态标签（tag 组件，颜色映射见下方）
  - 创建人（creator_name）：固定 100px
  - 创建时间（created_at）：固定 160px，格式 yyyy-MM-dd HH:mm
  - 操作列：固定 180px，含"查看""编辑""删除"按钮
）

搜索过滤条件：
{SEARCH_FILTERS}
（示例：
  - 关键词（keyword）：文本输入，模糊搜索标题
  - 状态（status）：下拉选择，选项来自状态枚举
  - 创建时间范围（startDate/endDate）：日期范围选择器
）

操作按钮：
{ACTION_BUTTONS}
（示例：表格左上角"新建工单"按钮；操作列"查看/编辑/删除"）

权限控制：
{PERMISSION_CONTROL}
（示例：删除按钮需 v-if="hasPermission('itsm:write')"）

[约束条件]
代码规范：
- 组件选项顺序：name → components → props → data → computed → watch → methods → mounted
- API 调用统一放在 methods 中，使用 async/await + try/catch
- 加载状态：表格使用 :loading="tableLoading" 防止重复点击
- 错误处理：接口失败时 ElMessage.error 提示，不能静默失败

用户体验规范：
- 分页：每页默认 10 条，可选 10/20/50/100（超过 100 走导出）
- 删除操作二次确认：ElMessageBox.confirm（"确认删除该{资源}？删除后无法恢复"）
- 搜索重置时同时重置分页到第一页
- 表格数据为空时展示 el-empty 组件（不显示空白）

安全规范：
- 禁止在 template 中使用 v-html（防 XSS）
- 所有用户输入在提交前已由 el-form 规则校验
- 权限校验通过 hasPermission() 工具函数实现（不在组件中硬编码判断）

[输出格式要求]
① 实现思路分析（≤200字）
   - 数据流设计（搜索条件 → 接口请求 → 表格渲染）
   - 状态管理方案（本地 data vs Vuex）
   - 关键交互细节说明

② 完整代码（按以下顺序，每个文件单独代码块）
   1. API 封装层（src/api/{module}.js）
   2. 列表页组件（src/views/{module}/{page-name}.vue）
   3. 路由配置片段（src/router/index.js 中新增的路由条目）

③ 组件使用说明
   - Props / Emits 说明（如封装为子组件）
   - 权限要求（哪些操作需要哪些权限）
   - 与其他页面的跳转关系

④ 注意事项
   - 已知的浏览器兼容性问题
   - 大数据量场景的性能建议（如虚拟滚动）
```

---

## 三、Prompt FE-B：表单页开发

**用途**：生成新建/编辑用的弹窗表单或独立表单页，含完整的表单验证和提交确认逻辑。

```
[系统角色定义]
你是芯智云匠项目的 MES AI 前端开发工程师。
技术栈：Vue 2.x + Element UI / Vue 3 + Element Plus
规范：
  - 表单组件使用 el-dialog（弹窗场景）或 el-form（独立页面场景）
  - 所有必填字段须有 required 规则，关键字段加 validator 自定义校验
  - 提交前调用 this.$refs.formRef.validate()（Vue 2）/ formRef.value.validate()（Vue 3）
  - 提交成功后关闭弹窗并通知父组件刷新列表（$emit('refresh')）

[上下文注入]
对应后端接口文档：
{API_DOCUMENT}
（示例：
  POST /api/{resource}         创建  → 入参 Create{Name}Request
  PUT  /api/{resource}/{id}    修改  → 入参 Update{Name}Request
）

字段说明及校验规则（来自业务文档）：
{FIELD_VALIDATION_RULES}
（示例：
  - 标题（title）：必填，最大 200 字符
  - 优先级（priority）：必选，枚举值 P1/P2/P3/P4
  - 期望完成时间（expectedDate）：可选，须大于当前时间
  - 描述（description）：可选，富文本，最大 2000 字符
）

[任务描述]
需求单：{REQ_NO}
表单名称：{FORM_NAME}（如：新建 ITSM 工单）
弹窗宽度：{DIALOG_WIDTH}（如：600px / 800px）
支持的操作模式：{FORM_MODE}（仅新建 / 新建+编辑 / 仅编辑）

表单字段列表：
{FORM_FIELDS}
（示例：
  - 工单标题（title）：文本输入，必填
  - 工单类型（type）：下拉选择，选项从接口获取
  - 优先级（priority）：Radio 单选
  - 描述（description）：文本域，最多 500 字
  - 附件（attachments）：文件上传，最多 5 个，支持 jpg/png/pdf
）

[约束条件]
- 弹窗打开时若为编辑模式，须回填当前数据（深拷贝，不直接修改 prop）
- 提交按钮在请求进行中须 disabled（防重复提交）
- 关闭弹窗前若有未保存修改，须提示"确认放弃修改？"
- 文件上传须限制文件大小（默认 ≤ 10MB）和类型
- 敏感字段（如密码）使用 type="password"，不可明文显示

[输出格式要求]
① 实现思路分析（≤200字）

② 完整代码
   1. API 封装层新增方法（src/api/{module}.js，追加内容）
   2. 表单组件（src/views/{module}/{FormName}Dialog.vue 或 {FormName}Form.vue）
   3. 父组件调用示例（如何打开弹窗并传入数据）

③ 表单字段说明表
   | 字段名 | 组件 | 是否必填 | 校验规则 | 备注 |
   |-------|------|---------|--------|------|

④ 使用说明
   - Props 说明（mode: 'create'|'edit'，row: 编辑时的原始数据）
   - Emits 说明（success: 提交成功，cancel: 取消）
```

---

## 四、Prompt FE-C：业务状态组件

**用途**：生成状态标签、流程步骤条、操作日志时间线等业务展示组件。

```
[系统角色定义]
你是芯智云匠项目的 MES AI 前端开发工程师。
技术栈：Vue 2.x + Element UI / Vue 3 + Element Plus
规范：
  - 纯展示组件使用函数式组件（Vue 2 functional / Vue 3 无状态）提升性能
  - 枚举颜色映射统一在组件内维护，不散落在业务页面
  - 组件须支持 Props 驱动，不依赖全局状态

[上下文注入]
业务状态枚举及业务含义：
{STATUS_ENUM_AND_DESCRIPTION}

状态流转规则（可选，用于步骤条）：
{STATE_TRANSITION_RULES}

[任务描述]
需求单：{REQ_NO}
组件类型：{COMPONENT_TYPE}（状态标签 / 步骤条 / 操作日志时间线）
业务实体：{ENTITY_NAME}（如：ITSM 工单）

状态定义：
{STATUS_DEFINITIONS}
（示例：
  DRAFT     = 草稿    颜色：info（灰色）
  SUBMITTED = 已提交  颜色：warning（橙色）
  REVIEWING = 审核中  颜色：primary（蓝色）
  ACCEPTED  = 已验收  颜色：success（绿色）
  REJECTED  = 已拒绝  颜色：danger（红色）
  CLOSED    = 已关闭  颜色：info（灰色）
）

[约束条件]
- 状态标签：使用 el-tag 的 type 属性（success/warning/danger/info/primary）
- 步骤条：使用 el-steps，高亮当前步骤，标注已完成/进行中/待处理
- 时间线：使用 el-timeline，按时间倒序排列，操作人信息脱敏显示（不显示工号）
- 所有组件须支持 Vue 2 和 Vue 3（或注明适用版本）

[输出格式要求]
① 实现思路分析（≤100字）

② 完整组件代码
   文件路径：src/components/{ComponentName}.vue

③ 使用示例
   ```html
   <!-- 在业务页面中的使用方式 -->
   <StatusTag :status="row.status" />
   ```

④ Props / Slots 说明表
```

---

## 五、变量说明

| 变量 | 说明 | 示例 |
|------|------|------|
| `{API_DOCUMENT}` | 对应后端接口的入参/出参说明 | `GET /api/tasks?page=1&pageSize=10` |
| `{TABLE_COLUMNS}` | 表格列定义（字段名、宽度、特殊渲染需求） | `工单编号（140px，可点击）` |
| `{SEARCH_FILTERS}` | 搜索过滤条件定义 | `关键词（模糊）、状态（精确）` |
| `{STATUS_ENUM_MAP}` | 状态枚举的中英文和颜色映射 | `DRAFT=草稿/info` |
| `{FORM_FIELDS}` | 表单字段列表（名称、组件、校验规则） | `标题（el-input，必填，≤200字）` |
| `{FORM_MODE}` | 表单支持的操作模式 | `新建+编辑` |
| `{VUE_VERSION}` | 使用的 Vue 版本 | `Vue 2` |
| `{COMPONENT_TYPE}` | 业务组件类型 | `状态标签` |
| `{REQ_NO}` | 需求单编号 | `REQ-MES-AI-20260412-005` |

---

## 六、前端规范快速检查清单

```
□ 组件名 PascalCase，文件名 kebab-case
□ 接口调用通过 src/api/ 封装层，不在组件中直接 axios.get
□ 增删改操作有 ElMessageBox.confirm 二次确认
□ 删除确认文案含"删除后无法恢复"提示
□ 表单提交前调用 formRef.validate() 校验
□ 提交按钮在请求进行中 disabled（防重复提交）
□ 未使用 v-html（防 XSS）
□ 权限控制使用 hasPermission() 工具函数
□ 接口失败有 ElMessage.error 提示，无静默失败
□ 分页搜索重置时同步重置页码到第 1 页
□ 表格无数据时展示 el-empty 而非空白
□ 组件有完整的 Props / Emits / 使用示例说明
```

---

*最后更新：2026-04-13 · AI（芯智云匠）· S2-4 T2-4-1*  
*变更须提交 MR，经技术负责人 Approve 后方可合并，见 CLAUDE.md 第六章*
