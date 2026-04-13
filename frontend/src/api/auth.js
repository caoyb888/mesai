/**
 * 鉴权相关 API
 */
import request from './index'

/** 用户登录 */
export function login(data) {
  return request.post('/system/auth/login', data)
}

/** 刷新 Token */
export function refreshToken(data) {
  return request.post('/system/auth/refresh', data)
}

/** 登出 */
export function logout() {
  return request.post('/system/auth/logout')
}
