/**
 * MES 数据问答 API
 * 对应后端 POST /mes-qa/ask（Spring Boot → AI 网关 /v1/ai/mes-qa）
 *
 * @author AI（芯智云匠）
 * @date 2026-07-17
 * @related REQ-MES-AI-20260716-001
 */
import request from './index'

/**
 * 提交 MES 数据问答
 * @param {Object} params
 * @param {string} params.question - 自然语言业务问题（5~500 字）
 * @param {string} params.kind - 检索范围：auto | table | proc
 * @param {number} [params.topN] - RAG 检索条数（1~10，可选）
 */
export function mesQaAsk(params) {
  return request.post('/mes-qa/ask', params)
}
