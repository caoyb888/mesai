/**
 * 用户状态管理（Pinia）
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('access_token') || '')
  const refreshTokenVal = ref(localStorage.getItem('refresh_token') || '')
  const username = ref(localStorage.getItem('username') || '')
  const role = ref(localStorage.getItem('role') || '')

  const isLoggedIn = computed(() => !!token.value)

  function setLoginInfo(loginVO) {
    token.value = loginVO.accessToken
    refreshTokenVal.value = loginVO.refreshToken
    username.value = loginVO.username
    role.value = loginVO.role
    localStorage.setItem('access_token', loginVO.accessToken)
    localStorage.setItem('refresh_token', loginVO.refreshToken)
    localStorage.setItem('username', loginVO.username)
    localStorage.setItem('role', loginVO.role)
  }

  function logout() {
    token.value = ''
    refreshTokenVal.value = ''
    username.value = ''
    role.value = ''
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('username')
    localStorage.removeItem('role')
  }

  return { token, refreshTokenVal, username, role, isLoggedIn, setLoginInfo, logout }
})
