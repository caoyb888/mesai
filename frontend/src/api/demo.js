/**
 * 演示接口 API
 * 对应后端 POST /demo/query
 */
import request from './index'

/**
 * 调用 AI 代码生成演示接口
 * @param {Object} params
 * @param {string} params.question - 自然语言需求描述
 * @param {string} params.mode - sql | dml | fe_component
 * @param {boolean} params.executeSql - 是否执行 SQL（仅 sql/dml 有效）
 */
export function aiDemoQuery(params) {
  return request.post('/demo/query', params)
}
