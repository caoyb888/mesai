/**
 * Axios 封装层
 * 芯智云匠 MES AI 演示前端
 * 所有 HTTP 请求通过此层发出，禁止在组件中直接调用 axios
 */

import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import router from '@/router'

const request = axios.create({
  baseURL: '/api',
  timeout: 120000 // AI 调用最长 120 秒
})

// 请求拦截：注入 JWT Token
request.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    if (userStore.token) {
      config.headers['Authorization'] = `Bearer ${userStore.token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截：统一处理错误
request.interceptors.response.use(
  (response) => {
    const data = response.data
    // 后端统一 ResultVO 格式：{ code: 0, data: ..., message: ... }
    if (data.code !== 0) {
      ElMessage.error(data.message || '请求失败')
      return Promise.reject(new Error(data.message))
    }
    return data.data
  },
  (error) => {
    if (error.response?.status === 401) {
      const userStore = useUserStore()
      userStore.logout()
      router.push('/login')
      ElMessage.error('登录已过期，请重新登录')
    } else if (error.response?.status === 403) {
      ElMessage.error('权限不足')
    } else if (error.code === 'ECONNABORTED') {
      ElMessage.error('请求超时，AI 正在处理中，请稍后重试')
    } else {
      ElMessage.error(error.response?.data?.message || '网络异常，请检查服务状态')
    }
    return Promise.reject(error)
  }
)

export default request
