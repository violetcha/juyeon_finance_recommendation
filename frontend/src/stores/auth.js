import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { login, getProfile } from '@/api/accounts'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(null)
  const loading = ref(false)
  const errorMessage = ref('')

  const isLoggedIn = computed(() => !!token.value)

  const setAuth = (authToken, authUser = null) => {
    token.value = authToken || ''
    user.value = authUser

    if (authToken) {
      localStorage.setItem('token', authToken)
      return
    }

    localStorage.removeItem('token')
  }

  const loginUser = async (loginData) => {
    loading.value = true
    errorMessage.value = ''

    try {
      const response = await login(loginData)
      const responseToken = response.data.token

      if (!responseToken) {
        throw new Error('로그인 응답에 토큰이 없습니다.')
      }

      setAuth(responseToken, response.data.user || null)

      return response
    } catch (error) {
      errorMessage.value =
        error.response?.data?.message ||
        error.message ||
        '로그인 중 문제가 발생했습니다.'

      throw error
    } finally {
      loading.value = false
    }
  }

  const fetchUser = async () => {
    if (!token.value) {
      user.value = null
      return null
    }

    try {
      const response = await getProfile()
      user.value = response.data
      return response.data
    } catch (error) {
      if (error.response?.status === 401) {
        clearAuth()
      }

      throw error
    }
  }

  const clearAuth = () => {
    setAuth('', null)
  }

  const logoutUser = () => {
    clearAuth()
  }

  return {
    token,
    user,
    loading,
    errorMessage,
    isLoggedIn,
    setAuth,
    loginUser,
    fetchUser,
    clearAuth,
    logoutUser,
  }
})
