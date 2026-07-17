<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { mesQaAsk } from '@/api/mesQa'

// ── 状态 ────────────────────────────────────────────────────────
const loading = ref(false)

const form = reactive({
  question: '',
  kind: 'auto'
})

const result = ref(null)

// ── 检索范围说明 ─────────────────────────────────────────────────
const kindOptions = [
  { value: 'auto', label: '智能混合', desc: '表 + 存储过程混合检索（默认）' },
  { value: 'table', label: '仅表结构', desc: '只检索表卡片（实绩表/主键/字段）' },
  { value: 'proc', label: '仅存储过程', desc: '只检索存储过程卡片（业务流程）' }
]

// ── 预设示例（按检索范围分组）─────────────────────────────────────
const examplesByKind = {
  auto: [
    '板坯是按炉次管理的吗？相关的核心表有哪些？',
    '一卷热轧钢卷从炼钢到成品，实绩数据大致分布在哪些表？',
    '质量判定不合格的钢卷，会记录在哪里，是通过什么过程处理的？'
  ],
  table: [
    '热轧钢卷的轧制实绩数据保存在哪张表？主键是什么？',
    '炼钢加热炉的实绩表是哪张，关键字段有哪些？',
    '钢卷的质量判定结果存放在哪张表，怎么和钢卷主表关联？'
  ],
  proc: [
    '质保书是通过哪些存储过程签发的？主流程是怎样的？',
    '钢卷入库/出库是由哪个存储过程处理的？',
    '生产计划下发到产线，涉及哪些核心存储过程？'
  ]
}

const currentExamples = computed(() => examplesByKind[form.kind] || [])

// ── 方法 ─────────────────────────────────────────────────────────
function useExample(text) {
  form.question = text
}

async function submit() {
  if (!form.question.trim()) {
    ElMessage.warning('请输入你的业务问题')
    return
  }
  loading.value = true
  result.value = null
  try {
    result.value = await mesQaAsk({
      question: form.question,
      kind: form.kind
    })
  } catch (_) {
    // 错误已在 axios 拦截器中统一提示
  } finally {
    loading.value = false
  }
}

function copyAnswer() {
  if (!result.value?.answer) return
  navigator.clipboard.writeText(result.value.answer)
  ElMessage.success('回答已复制到剪贴板')
}

const kindLabel = {
  auto: '智能混合',
  table: '仅表结构',
  proc: '仅存储过程'
}
</script>

<template>
  <div class="mesqa-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <div>
        <h2>MES 数据问答</h2>
        <p class="page-desc">面向真实 MES 库（钢板 / 卷材钢厂）的自然语言问答：基于 S3 理解知识库检索真实表 / 字段 / 存储过程作答，回答严格接地、防臆造</p>
      </div>
      <el-tag type="success" size="large" effect="dark">
        <el-icon style="margin-right: 4px"><Connection /></el-icon>
        知识库：S3 理解卡片（表 + 存储过程）
      </el-tag>
    </div>

    <el-row :gutter="24">
      <!-- 左侧：输入区 -->
      <el-col :span="10">
        <el-card class="input-card" shadow="never">
          <template #header>
            <div class="card-header">
              <el-icon><ChatDotRound /></el-icon>
              <span style="margin-left: 8px">业务问题</span>
            </div>
          </template>

          <!-- 检索范围 -->
          <div class="field-label">检索范围</div>
          <el-radio-group v-model="form.kind" class="kind-group">
            <el-radio-button
              v-for="opt in kindOptions"
              :key="opt.value"
              :value="opt.value"
            >
              {{ opt.label }}
            </el-radio-button>
          </el-radio-group>
          <el-alert
            :title="kindOptions.find(o => o.value === form.kind)?.desc"
            type="info" show-icon :closable="false"
            style="margin: 12px 0 16px"
          />

          <!-- 示例问题 -->
          <div class="examples-section">
            <div class="examples-title">示例问题（点击填入）</div>
            <div
              v-for="(ex, idx) in currentExamples"
              :key="idx"
              class="example-item"
              @click="useExample(ex)"
            >
              <el-icon><ArrowRight /></el-icon>
              <span>{{ ex }}</span>
            </div>
          </div>

          <!-- 问题输入框 -->
          <el-form>
            <el-form-item>
              <el-input
                v-model="form.question"
                type="textarea"
                :rows="5"
                placeholder="用中文描述你的业务问题，AI 将基于 MES 知识库检索真实表 / 字段 / 过程作答..."
                show-word-limit
                maxlength="500"
                style="font-size: 14px"
                @keydown.ctrl.enter="submit"
              />
            </el-form-item>

            <el-button
              type="primary"
              size="large"
              :loading="loading"
              :icon="loading ? '' : 'Search'"
              style="width: 100%"
              @click="submit"
            >
              {{ loading ? 'AI 正在检索并作答...' : '提问（Ctrl+Enter）' }}
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
            <span>AI 正在检索知识库并生成回答，请稍候...</span>
          </div>
        </el-card>

        <!-- 空状态 -->
        <el-card v-else-if="!result" shadow="never" class="result-card empty-card">
          <el-empty description="在左侧输入业务问题，点击「提问」查看 AI 回答">
            <template #image>
              <el-icon :size="64" color="#d1d5db"><ChatDotRound /></el-icon>
            </template>
          </el-empty>
        </el-card>

        <!-- 结果 -->
        <template v-else>
          <el-card shadow="never" class="result-card">
            <template #header>
              <div class="card-header">
                <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap">
                  <el-icon><ChatLineRound /></el-icon>
                  <span>AI 回答</span>
                  <el-tag size="small" type="success">{{ kindLabel[result.kind] || result.kind }}</el-tag>
                  <el-tag size="small" type="info">{{ result.tokensUsed }} tokens</el-tag>
                  <el-tag size="small">{{ result.aiResponseTimeMs }}ms</el-tag>
                  <el-tag v-if="result.model" size="small" type="warning">{{ result.model }}</el-tag>
                </div>
                <el-button size="small" :icon="'CopyDocument'" @click="copyAnswer">复制</el-button>
              </div>
            </template>

            <!-- 回答正文 -->
            <div class="answer-block">{{ result.answer }}</div>

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

            <!-- 接地提示 -->
            <el-alert
              type="info" show-icon :closable="false"
              title="回答仅依据知识库检索到的真实表 / 字段 / 存储过程；上下文无依据处会明示「知识库中未检索到」，推断内容会标注「（推断）」"
              style="margin-top: 16px"
            />
          </el-card>
        </template>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.mesqa-page {
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

.field-label {
  font-size: 12px;
  color: #9ca3af;
  margin-bottom: 8px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.kind-group {
  width: 100%;
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

.answer-block {
  font-size: 14px;
  color: #1f2937;
  line-height: 1.75;
  white-space: pre-wrap;
  word-break: break-word;
  background: #f8fafc;
  border-left: 3px solid #10b981;
  border-radius: 0 6px 6px 0;
  padding: 16px;
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
