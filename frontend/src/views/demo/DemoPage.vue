<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { aiDemoQuery } from '@/api/demo'

// ── 状态 ────────────────────────────────────────────────────────
const activeTab = ref('sql')
const loading = ref(false)

const form = reactive({
  question: '',
  mode: 'sql',
  executeSql: false
})

const result = ref(null)

// ── 预设示例 ─────────────────────────────────────────────────────
const sqlExamples = [
  '查询过去7天内所有状态为 OPEN 的工单，按优先级降序、创建时间降序排列，返回工单编号、标题、优先级、创建人和创建时间',
  '查询每个处理人在本月处理的工单数量，并计算平均响应时长（分钟），按工单数量降序排列',
  '查询超过 SLA 承诺响应时间且状态仍为 OPEN 的工单列表，附上 SLA 等级和已超时分钟数'
]

const dmlExamples = [
  '将编号为 TKT-2026-001 的工单状态从 OPEN 更新为 IN_PROGRESS，同时记录开始处理时间',
  '批量关闭所有创建时间超过 90 天且状态仍为 DRAFT 的工单，关闭原因填写"超期自动关闭"',
  '为 IT 部门新增一条 SLA 规则：P1 优先级工单响应时间 30 分钟，解决时间 4 小时'
]

const feExamples = [
  '生成一个 ITSM 工单列表页组件，包含工单编号、标题、状态（彩色标签）、优先级、创建人、创建时间列，支持按状态和优先级筛选，支持分页',
  '生成一个工单详情卡片组件，展示工单基本信息、当前状态流转步骤条和操作历史时间线',
  '生成一个 SLA 指标仪表盘组件，用环形图展示本月工单按时完成率，用折线图展示近 7 天每日工单量趋势'
]

// ── 方法 ─────────────────────────────────────────────────────────
function onTabChange(tab) {
  form.mode = tab
  form.question = ''
  form.executeSql = false
  result.value = null
}

function useExample(text) {
  form.question = text
}

async function submit() {
  if (!form.question.trim()) {
    ElMessage.warning('请输入需求描述')
    return
  }
  loading.value = true
  result.value = null
  try {
    result.value = await aiDemoQuery({
      question: form.question,
      mode: form.mode,
      executeSql: form.executeSql
    })
  } catch (_) {
    // 错误已在拦截器中处理
  } finally {
    loading.value = false
  }
}

function copyCode() {
  if (!result.value?.generatedCode) return
  navigator.clipboard.writeText(result.value.generatedCode)
  ElMessage.success('代码已复制到剪贴板')
}

// 结果集列名提取
function getColumns(rows) {
  if (!rows || rows.length === 0) return []
  return Object.keys(rows[0])
}

// 执行类型中文标签
const execTypeLabel = {
  SELECT: 'SELECT 查询',
  DML_PREVIEW: 'DML 预演（已回滚）',
  BLOCKED: '安全拦截',
  SKIPPED: '未执行',
}
</script>

<template>
  <div class="demo-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <div>
        <h2>AI 能力演示</h2>
        <p class="page-desc">基于 ITSM 知识库（RAG）的 SQL 生成与数据库直连执行演示，展示芯智云匠 AI 对业务数据库的理解与操作能力</p>
      </div>
      <el-tag type="success" size="large" effect="dark">
        <el-icon style="margin-right: 4px"><Connection /></el-icon>
        知识库：ITSM DB 30张表 + API 71接口
      </el-tag>
    </div>

    <el-row :gutter="24">
      <!-- 左侧：输入区 -->
      <el-col :span="10">
        <el-card class="input-card" shadow="never">
          <template #header>
            <div class="card-header">
              <el-icon><Edit /></el-icon>
              <span style="margin-left: 8px">需求输入</span>
            </div>
          </template>

          <!-- 模式 Tab -->
          <el-tabs v-model="activeTab" @tab-change="onTabChange">
            <el-tab-pane label="SQL 查询" name="sql">
              <template #label>
                <el-icon><Search /></el-icon>
                <span style="margin-left: 4px">SQL 查询</span>
              </template>
            </el-tab-pane>
            <el-tab-pane label="数据变更" name="dml">
              <template #label>
                <el-icon><Edit /></el-icon>
                <span style="margin-left: 4px">数据变更</span>
              </template>
            </el-tab-pane>
            <el-tab-pane label="前端组件" name="fe_component">
              <template #label>
                <el-icon><Monitor /></el-icon>
                <span style="margin-left: 4px">前端组件</span>
              </template>
            </el-tab-pane>
          </el-tabs>

          <!-- 模式说明 -->
          <el-alert
            v-if="activeTab === 'sql'"
            type="info" show-icon :closable="false"
            title="AI 将基于 ITSM 数据库结构知识，生成满足需求的 SELECT 查询 SQL"
            style="margin-bottom: 16px"
          />
          <el-alert
            v-else-if="activeTab === 'dml'"
            type="warning" show-icon :closable="false"
            title="AI 将生成 INSERT/UPDATE/DELETE SQL。演示模式下在事务内执行后自动回滚，实际数据不变"
            style="margin-bottom: 16px"
          />
          <el-alert
            v-else
            type="success" show-icon :closable="false"
            title="AI 将基于 ITSM 接口文档，生成完整的 Vue 3 组件代码（含 Element Plus）"
            style="margin-bottom: 16px"
          />

          <!-- 示例需求 -->
          <div class="examples-section">
            <div class="examples-title">示例需求（点击填入）</div>
            <div
              v-for="(ex, idx) in (activeTab === 'sql' ? sqlExamples : activeTab === 'dml' ? dmlExamples : feExamples)"
              :key="idx"
              class="example-item"
              @click="useExample(ex)"
            >
              <el-icon><ArrowRight /></el-icon>
              <span>{{ ex }}</span>
            </div>
          </div>

          <!-- 需求输入框 -->
          <el-form>
            <el-form-item>
              <el-input
                v-model="form.question"
                type="textarea"
                :rows="5"
                placeholder="用中文描述你的需求，AI 将基于 ITSM 知识库生成对应代码..."
                show-word-limit
                maxlength="500"
                style="font-size: 14px"
              />
            </el-form-item>

            <!-- SQL/DML 执行开关 -->
            <el-form-item v-if="activeTab !== 'fe_component'">
              <div style="display: flex; align-items: center; gap: 12px">
                <el-switch
                  v-model="form.executeSql"
                  active-text="连接 ITSM 测试库执行"
                  inactive-text="仅生成代码"
                />
                <el-tooltip
                  content="开启后将在 ITSM 测试数据库上实际执行生成的 SQL。DML 操作会在事务内执行后自动回滚（展示能力但不修改数据）"
                  placement="top"
                >
                  <el-icon style="color: #9ca3af; cursor: help"><InfoFilled /></el-icon>
                </el-tooltip>
              </div>
            </el-form-item>

            <el-button
              type="primary"
              size="large"
              :loading="loading"
              :icon="loading ? '' : 'MagicStick'"
              style="width: 100%"
              @click="submit"
            >
              {{ loading ? 'AI 正在生成中...' : '生成' }}
            </el-button>
          </el-form>
        </el-card>
      </el-col>

      <!-- 右侧：结果区 -->
      <el-col :span="14">
        <!-- 加载中 -->
        <el-card v-if="loading" shadow="never" class="result-card loading-card">
          <el-skeleton :rows="12" animated />
          <div class="loading-tip">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>AI 正在检索知识库并生成代码，请稍候...</span>
          </div>
        </el-card>

        <!-- 空状态 -->
        <el-card v-else-if="!result" shadow="never" class="result-card empty-card">
          <el-empty description="在左侧输入需求，点击「生成」查看 AI 输出">
            <template #image>
              <el-icon :size="64" color="#d1d5db"><MagicStick /></el-icon>
            </template>
          </el-empty>
        </el-card>

        <!-- 结果 -->
        <template v-else>
          <!-- 上：生成代码 -->
          <el-card shadow="never" class="result-card" style="margin-bottom: 16px">
            <template #header>
              <div class="card-header">
                <div style="display: flex; align-items: center; gap: 8px">
                  <el-icon><Document /></el-icon>
                  <span>{{ activeTab === 'fe_component' ? 'Vue 3 组件代码' : 'AI 生成 SQL' }}</span>
                  <el-tag size="small" type="info">{{ result.tokensUsed }} tokens</el-tag>
                  <el-tag size="small">{{ result.aiResponseTimeMs }}ms</el-tag>
                </div>
                <el-button size="small" :icon="'CopyDocument'" @click="copyCode">复制</el-button>
              </div>
            </template>

            <div class="code-block">
              <pre><code>{{ result.generatedCode }}</code></pre>
            </div>

            <!-- 说明 -->
            <div class="explanation-block" v-if="result.explanation">
              <div class="explanation-title">
                <el-icon><InfoFilled /></el-icon>
                <span>AI 说明</span>
              </div>
              <div class="explanation-text">{{ result.explanation }}</div>
            </div>

            <!-- RAG 上下文 -->
            <div v-if="result.contextDocs?.length" style="margin-top: 12px">
              <el-collapse>
                <el-collapse-item title="📚 RAG 检索到的知识库上下文">
                  <div
                    v-for="(doc, idx) in result.contextDocs"
                    :key="idx"
                    class="context-doc"
                  >
                    <div class="context-doc-header">
                      <el-tag size="small" type="info">{{ doc.docType }}</el-tag>
                      <span class="context-source">{{ doc.source }}</span>
                      <el-tag size="small" :type="doc.relevanceScore > 0.5 ? 'success' : 'warning'">
                        相关度 {{ (doc.relevanceScore * 100).toFixed(0) }}%
                      </el-tag>
                    </div>
                    <div class="context-preview">{{ doc.contentPreview }}...</div>
                  </div>
                </el-collapse-item>
              </el-collapse>
            </div>
          </el-card>

          <!-- 下：SQL 执行结果 -->
          <el-card
            v-if="result.executionResult"
            shadow="never"
            class="result-card"
          >
            <template #header>
              <div class="card-header">
                <div style="display: flex; align-items: center; gap: 8px">
                  <el-icon><DataAnalysis /></el-icon>
                  <span>执行结果</span>
                  <el-tag
                    size="small"
                    :type="result.executionResult.success ? 'success' : 'danger'"
                  >
                    {{ execTypeLabel[result.executionResult.execType] || result.executionResult.execType }}
                  </el-tag>
                  <el-tag v-if="result.executionResult.elapsedMs" size="small">
                    {{ result.executionResult.elapsedMs }}ms
                  </el-tag>
                </div>
              </div>
            </template>

            <!-- 失败 -->
            <el-alert
              v-if="!result.executionResult.success"
              type="error"
              :title="result.executionResult.errorMessage"
              show-icon
              :closable="false"
            />

            <!-- 提示信息 -->
            <el-alert
              v-if="result.executionResult.notice"
              type="info"
              :title="result.executionResult.notice"
              show-icon
              :closable="false"
              style="margin-bottom: 12px"
            />

            <!-- SELECT 结果表格 -->
            <template v-if="result.executionResult.execType === 'SELECT' && result.executionResult.success">
              <div v-if="!result.executionResult.rows?.length">
                <el-empty description="查询结果为空" :image-size="60" />
              </div>
              <el-table
                v-else
                :data="result.executionResult.rows"
                border
                stripe
                size="small"
                max-height="360"
                style="width: 100%"
              >
                <el-table-column
                  v-for="col in getColumns(result.executionResult.rows)"
                  :key="col"
                  :prop="col"
                  :label="col"
                  min-width="120"
                  show-overflow-tooltip
                />
              </el-table>
              <div style="text-align: right; color: #6b7280; font-size: 12px; margin-top: 8px">
                共 {{ result.executionResult.totalRows }} 行
              </div>
            </template>

            <!-- DML 预演结果 -->
            <template v-else-if="result.executionResult.execType === 'DML_PREVIEW' && result.executionResult.success">
              <el-result
                icon="success"
                :title="`DML 执行成功（影响 ${result.executionResult.affectedRows} 行）`"
                sub-title="演示模式：事务已自动回滚，ITSM 测试库数据实际未修改"
              />
            </template>
          </el-card>
        </template>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.demo-page {
  max-width: 1400px;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 24px;
}

.page-header h2 {
  font-size: 22px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 6px;
}

.page-desc {
  color: #6b7280;
  font-size: 14px;
  margin: 0;
  max-width: 600px;
}

.input-card,
.result-card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.examples-section {
  margin-bottom: 16px;
}

.examples-title {
  font-size: 12px;
  color: #9ca3af;
  margin-bottom: 8px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.example-item {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  padding: 8px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  color: #374151;
  border: 1px solid #e5e7eb;
  margin-bottom: 6px;
  transition: all 0.15s;
  line-height: 1.4;
}

.example-item:hover {
  border-color: #3b82f6;
  color: #1d4ed8;
  background: #eff6ff;
}

.example-item .el-icon {
  margin-top: 2px;
  flex-shrink: 0;
  color: #9ca3af;
}

.code-block {
  background: #0d1117;
  border-radius: 6px;
  padding: 16px;
  overflow-x: auto;
  max-height: 320px;
  overflow-y: auto;
}

.code-block pre {
  margin: 0;
}

.code-block code {
  color: #e6edf3;
  font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', Consolas, monospace;
  font-size: 13px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-all;
}

.explanation-block {
  margin-top: 12px;
  padding: 12px;
  background: #f8fafc;
  border-left: 3px solid #3b82f6;
  border-radius: 0 6px 6px 0;
}

.explanation-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #1e40af;
  margin-bottom: 6px;
}

.explanation-text {
  font-size: 13px;
  color: #374151;
  line-height: 1.6;
  white-space: pre-wrap;
}

.context-doc {
  padding: 10px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  margin-bottom: 8px;
}

.context-doc-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.context-source {
  font-size: 12px;
  color: #6b7280;
  flex: 1;
}

.context-preview {
  font-size: 12px;
  color: #4b5563;
  line-height: 1.5;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.loading-card {
  min-height: 400px;
}

.loading-tip {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #6b7280;
  margin-top: 24px;
  font-size: 14px;
}

.empty-card {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
