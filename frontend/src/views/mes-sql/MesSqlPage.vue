<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { mesSqlQuery } from '@/api/mesSql'

// ── 状态 ────────────────────────────────────────────────────────
const loading = ref(false)

const form = reactive({
  question: '',
  executeSql: true
})

const result = ref(null)

// ── 预设示例 ─────────────────────────────────────────────────────
const examples = [
  '查询最近一个月热轧钢卷的轧制实绩，包含卷号、炉次号、轧制日期',
  '统计每个牌号的板坯数量，按数量倒序排列',
  '查询质量判定为不合格的钢卷卷号及判定时间',
  '按加热炉分组统计近7天的钢坯加热炉次数'
]

// ── 计算属性 ─────────────────────────────────────────────────────
const exec = computed(() => result.value?.executionResult || null)

// 执行结果表格的动态列（取首行的字段名）
const resultColumns = computed(() => {
  const rows = exec.value?.rows
  if (!rows || !rows.length) return []
  return Object.keys(rows[0])
})

// 执行结果提示的样式类型
const execAlertType = computed(() => {
  if (!exec.value) return 'info'
  if (exec.value.execType === 'BLOCKED') return 'error'
  if (!exec.value.success) return 'warning'
  return 'success'
})

// ── 方法 ─────────────────────────────────────────────────────────
function useExample(text) {
  form.question = text
}

async function submit() {
  if (!form.question.trim()) {
    ElMessage.warning('请输入你的取数需求')
    return
  }
  loading.value = true
  result.value = null
  try {
    result.value = await mesSqlQuery({
      question: form.question,
      executeSql: form.executeSql
    })
  } catch (_) {
    // 错误已在 axios 拦截器中统一提示
  } finally {
    loading.value = false
  }
}

function copySql() {
  if (!result.value?.sql) return
  navigator.clipboard.writeText(result.value.sql)
  ElMessage.success('SQL 已复制到剪贴板')
}

// 单元格值展示（对象/空值友好化）
function cellText(val) {
  if (val === null || val === undefined) return ''
  if (typeof val === 'object') return JSON.stringify(val)
  return String(val)
}
</script>

<template>
  <div class="messql-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <div>
        <h2>MES 取数（AI 生成 SQL）</h2>
        <p class="page-desc">面向真实 MES 库（钢板 / 卷材钢厂，Oracle）：用自然语言描述取数需求，AI 基于 S3 结构知识生成 Oracle 只读 SELECT，经安全校验后在只读数据源执行并返回结果</p>
      </div>
      <el-tag type="warning" size="large" effect="dark">
        <el-icon style="margin-right: 4px"><Lock /></el-icon>
        只读查询 · 禁写操作 · 禁 SELECT *
      </el-tag>
    </div>

    <el-row :gutter="24">
      <!-- 左侧：输入区 -->
      <el-col :span="10">
        <el-card class="input-card" shadow="never">
          <template #header>
            <div class="card-header">
              <el-icon><EditPen /></el-icon>
              <span style="margin-left: 8px">取数需求</span>
            </div>
          </template>

          <!-- 示例 -->
          <div class="examples-section">
            <div class="examples-title">示例需求（点击填入）</div>
            <div
              v-for="(ex, idx) in examples"
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
                placeholder="用中文描述取数需求，AI 将基于 MES 知识库生成 Oracle 只读 SELECT..."
                show-word-limit
                maxlength="500"
                style="font-size: 14px"
                @keydown.ctrl.enter="submit"
              />
            </el-form-item>

            <div class="exec-switch">
              <span>生成后在只读数据源执行并返回结果</span>
              <el-switch v-model="form.executeSql" />
            </div>

            <el-button
              type="primary"
              size="large"
              :loading="loading"
              :icon="loading ? '' : 'Search'"
              style="width: 100%"
              @click="submit"
            >
              {{ loading ? 'AI 正在生成 SQL...' : '生成并查询（Ctrl+Enter）' }}
            </el-button>
          </el-form>
        </el-card>
      </el-col>

      <!-- 右侧：结果区 -->
      <el-col :span="14">
        <!-- 加载中 -->
        <el-card v-if="loading" shadow="never" class="result-card loading-card">
          <el-skeleton :rows="10" animated />
          <div class="loading-tip">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>AI 正在检索知识库并生成 Oracle SELECT，请稍候...</span>
          </div>
        </el-card>

        <!-- 空状态 -->
        <el-card v-else-if="!result" shadow="never" class="result-card empty-card">
          <el-empty description="在左侧输入取数需求，点击「生成并查询」查看 AI 生成的 SQL 与结果">
            <template #image>
              <el-icon :size="64" color="#d1d5db"><Coin /></el-icon>
            </template>
          </el-empty>
        </el-card>

        <!-- 结果 -->
        <template v-else>
          <el-card shadow="never" class="result-card">
            <template #header>
              <div class="card-header">
                <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap">
                  <el-icon><Coin /></el-icon>
                  <span>取数结果</span>
                  <el-tag size="small" :type="result.generated ? 'success' : 'danger'">
                    {{ result.generated ? '已生成 SQL' : '未生成' }}
                  </el-tag>
                  <el-tag size="small" type="info">{{ result.tokensUsed }} tokens</el-tag>
                  <el-tag size="small">{{ result.aiResponseTimeMs }}ms</el-tag>
                  <el-tag v-if="result.model" size="small" type="warning">{{ result.model }}</el-tag>
                </div>
                <el-button v-if="result.generated" size="small" :icon="'CopyDocument'" @click="copySql">复制 SQL</el-button>
              </div>
            </template>

            <!-- 未生成：知识库依据不足 -->
            <el-alert
              v-if="!result.generated"
              type="warning" show-icon :closable="false"
              title="未能生成 SQL"
              :description="result.unanswerableReason || '知识库上下文中未找到可满足需求的表或字段，请调整需求描述或缩小范围后重试。'"
            />

            <template v-else>
              <!-- 生成的 SQL -->
              <div class="section-label">生成的 Oracle 只读 SELECT</div>
              <pre class="sql-block">{{ result.sql }}</pre>

              <!-- 引用的表/字段 -->
              <div v-if="result.referencedTables?.length" class="ref-line">
                <span class="ref-label">引用表：</span>
                <el-tag
                  v-for="(t, i) in result.referencedTables"
                  :key="'t' + i"
                  size="small" type="info" style="margin-right: 6px"
                >{{ t }}</el-tag>
              </div>

              <!-- 说明 -->
              <div v-if="result.explanation" class="explanation-block">{{ result.explanation }}</div>

              <!-- 执行结果 -->
              <div v-if="exec" style="margin-top: 16px">
                <div class="section-label">执行结果</div>

                <!-- 结果集表格 -->
                <template v-if="exec.execType === 'SELECT' && exec.success">
                  <el-alert
                    type="success" show-icon :closable="false"
                    :title="exec.notice + '（耗时 ' + exec.elapsedMs + 'ms）'"
                    style="margin-bottom: 10px"
                  />
                  <el-table
                    v-if="exec.rows?.length"
                    :data="exec.rows"
                    border stripe size="small"
                    max-height="360"
                    style="width: 100%"
                  >
                    <el-table-column
                      v-for="col in resultColumns"
                      :key="col"
                      :prop="col"
                      :label="col"
                      show-overflow-tooltip
                      min-width="120"
                    >
                      <template #default="scope">{{ cellText(scope.row[col]) }}</template>
                    </el-table-column>
                  </el-table>
                  <el-empty v-else description="查询成功，但结果为空" :image-size="60" />
                </template>

                <!-- 拦截 / 跳过 / 失败提示 -->
                <el-alert
                  v-else
                  :type="execAlertType" show-icon :closable="false"
                  :title="exec.execType === 'BLOCKED' ? '安全拦截：SQL 未通过校验' : (exec.execType === 'SKIPPED' ? '未执行' : '执行失败')"
                  :description="exec.errorMessage"
                />
              </div>

              <!-- RAG 上下文 -->
              <div v-if="result.contextDocs?.length" style="margin-top: 16px">
                <el-collapse>
                  <el-collapse-item :title="`📚 RAG 检索到的知识库上下文（${result.contextDocs.length} 条）`">
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
            </template>

            <!-- 安全提示 -->
            <el-alert
              type="info" show-icon :closable="false"
              title="安全边界：SQL 仅引用知识库中真实存在的表 / 字段（防臆造）；执行前经「仅 SELECT / 禁写操作 / 禁 SELECT * / 禁多语句」校验，且仅对 MES 只读数据源执行，最多返回 200 行"
              style="margin-top: 16px"
            />
          </el-card>
        </template>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.messql-page {
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
  max-width: 640px;
  line-height: 1.5;
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

.exec-switch {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  color: #4b5563;
  margin-bottom: 14px;
}

.section-label {
  font-size: 12px;
  color: #9ca3af;
  margin: 4px 0 8px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.sql-block {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  font-size: 13px;
  color: #f8fafc;
  background: #1e293b;
  border-radius: 6px;
  padding: 14px 16px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
  overflow-x: auto;
}

.ref-line {
  margin-top: 12px;
  font-size: 13px;
  line-height: 2;
}

.ref-label {
  color: #6b7280;
  margin-right: 4px;
}

.explanation-block {
  font-size: 13px;
  color: #374151;
  line-height: 1.7;
  white-space: pre-wrap;
  word-break: break-word;
  background: #f8fafc;
  border-left: 3px solid #3b82f6;
  border-radius: 0 6px 6px 0;
  padding: 12px 14px;
  margin-top: 12px;
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
  word-break: break-all;
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
