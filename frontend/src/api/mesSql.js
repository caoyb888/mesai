/**
 * MES 取数 API
 * 对应后端 POST /mes-sql/query（Spring Boot → AI 网关 /v1/ai/mes-sql）
 *
 * 恢复原始系统设计：AI 基于 MES 数据库结构知识生成 Oracle 只读 SELECT，
 * 经安全校验后在只读数据源执行并返回结果。
 *
 * @author AI（芯智云匠）
 * @date 2026-07-18
 * @related REQ-MES-AI-20260716-001
 */
import request from './index'

/**
 * 提交 MES 取数需求
 * @param {Object} params
 * @param {string} params.question - 自然语言取数需求（5~500 字）
 * @param {number} [params.topN] - RAG 检索条数（1~10，可选）
 * @param {boolean} [params.executeSql] - 是否在只读数据源执行（默认 true）
 */
export function mesSqlQuery(params) {
  return request.post('/mes-sql/query', params)
}
