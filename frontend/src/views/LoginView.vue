<template>
  <div class="login-view">
    <h1>로그인</h1>

    <p v-if="successMessage" class="success-message">
      {{ successMessage }}
    </p>

    <form class="login-form" @submit.prevent="handleLogin">
      <div>
        <label for="username">아이디</label>
        <input
          id="username"
          v-model.trim="username"
          type="text"
          placeholder="아이디를 입력하세요"
          autocomplete="username"
        >
      </div>

      <div>
        <label for="password">비밀번호</label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="비밀번호를 입력하세요"
          autocomplete="current-password"
        >
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? '로그인 중...' : '로그인' }}
      </button>
    </form>

    <p class="signup-link">
      아직 계정이 없으신가요?
      <RouterLink :to="{ name: 'signup' }">
        회원가입
      </RouterLink>
    </p>

    <p class="account-help-links">
      <RouterLink :to="{ name: 'find-username' }">
        아이디 찾기
      </RouterLink>
      <span>|</span>
      <RouterLink :to="{ name: 'reset-password' }">
        비밀번호 재설정
      </RouterLink>
    </p>

    <p v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { login } from '@/api/accounts'

const router = useRouter()
const route = useRoute()

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const loading = ref(false)

const getErrorMessage = (error) => {
  if (error.response?.data?.message) {
    return error.response.data.message
  }

  if (error.response?.status === 400) {
    return '아이디 또는 비밀번호가 올바르지 않습니다.'
  }

  if (error.response?.status === 401) {
    return '로그인이 필요한 요청입니다.'
  }

  return '로그인 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.'
}

const handleLogin = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (!username.value || !password.value) {
    errorMessage.value = '아이디와 비밀번호를 입력해주세요.'
    return
  }

  loading.value = true

  try {
    const response = await login({
      username: username.value,
      password: password.value,
    })

    const token = response.data.token

    if (!token) {
      errorMessage.value = '로그인 처리 중 문제가 발생했습니다.'
      return
    }

    localStorage.setItem('token', token)
    window.dispatchEvent(new Event('login-success'))

    router.push({ name: 'home' })
  } catch (error) {
    console.error(error)
    errorMessage.value = getErrorMessage(error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (route.query.signup === 'success') {
    successMessage.value = '회원가입이 완료되었습니다. 로그인해주세요.'
  }
})
</script>

<style scoped>
.login-view {
  max-width: 420px;
  margin: 0 auto;
  padding: 40px 24px;
}

.login-view h1 {
  margin: 0 0 24px;
  font-size: 28px;
  color: #111;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.login-form label {
  display: block;
  margin-bottom: 6px;
  color: #333;
  font-size: 14px;
  font-weight: 700;
}

.login-form input {
  width: 100%;
  height: 42px;
  padding: 0 10px;
  border: 1px solid #ccc;
  box-sizing: border-box;
  font-size: 14px;
}

.login-form button {
  width: 100%;
  margin-top: 4px;
  padding: 12px 16px;
  border: 1px solid #222;
  background-color: #222;
  color: #fff;
  font-weight: 800;
  cursor: pointer;
}

.login-form button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.signup-link {
  margin-top: 18px;
  color: #555;
  font-size: 14px;
}

.signup-link a {
  color: #2563eb;
  font-weight: 800;
  text-decoration: none;
}

.error-message,
.success-message {
  margin-top: 16px;
  padding: 12px;
  font-size: 14px;
}

.error-message {
  background-color: #fff5f5;
  border: 1px solid #f0caca;
  color: #c0392b;
}

.success-message {
  margin-top: 0;
  margin-bottom: 16px;
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #15803d;
}

.account-help-links {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 12px;
  color: #777;
  font-size: 14px;
}

.account-help-links a {
  color: #2563eb;
  font-weight: 700;
  text-decoration: none;
}
</style>