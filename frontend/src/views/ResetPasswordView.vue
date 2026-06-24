<template>
  <div class="account-view">
    <section class="account-card">
      <h1>비밀번호 재설정</h1>
      <p class="description">
        아이디와 이메일이 일치하면 새 비밀번호로 변경할 수 있습니다.
      </p>

      <form class="account-form" @submit.prevent="handleResetPassword">
        <label>
          아이디
          <input
            v-model.trim="form.username"
            type="text"
            placeholder="아이디를 입력하세요"
            autocomplete="username"
          >
        </label>

        <label>
          이메일
          <input
            v-model.trim="form.email"
            type="email"
            placeholder="이메일을 입력하세요"
            autocomplete="email"
          >
        </label>

        <label>
          새 비밀번호
          <input
            v-model="form.new_password"
            type="password"
            placeholder="새 비밀번호를 입력하세요"
            autocomplete="new-password"
          >
        </label>

        <label>
          새 비밀번호 확인
          <input
            v-model="form.new_password_confirm"
            type="password"
            placeholder="새 비밀번호를 다시 입력하세요"
            autocomplete="new-password"
          >
        </label>

        <button type="submit" :disabled="loading">
          {{ loading ? '변경 중...' : '비밀번호 재설정' }}
        </button>
      </form>

      <p v-if="message" class="message success">
        {{ message }}
      </p>

      <p v-if="errorMessage" class="message error">
        {{ errorMessage }}
      </p>

      <div class="link-row">
        <RouterLink :to="{ name: 'login' }">
          로그인으로 돌아가기
        </RouterLink>
        <RouterLink :to="{ name: 'find-username' }">
          아이디 찾기
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { resetPassword } from '@/api/accounts'

const form = ref({
  username: '',
  email: '',
  new_password: '',
  new_password_confirm: '',
})

const message = ref('')
const errorMessage = ref('')
const loading = ref(false)

const getErrorMessage = (error) => {
  return (
    error.response?.data?.message ||
    '비밀번호 재설정 중 문제가 발생했습니다.'
  )
}

const validateForm = () => {
  if (!form.value.username) {
    errorMessage.value = '아이디를 입력해주세요.'
    return false
  }

  if (!form.value.email) {
    errorMessage.value = '이메일을 입력해주세요.'
    return false
  }

  if (!form.value.new_password) {
    errorMessage.value = '새 비밀번호를 입력해주세요.'
    return false
  }

  if (!form.value.new_password_confirm) {
    errorMessage.value = '새 비밀번호 확인을 입력해주세요.'
    return false
  }

  if (form.value.new_password !== form.value.new_password_confirm) {
    errorMessage.value = '새 비밀번호가 일치하지 않습니다.'
    return false
  }

  return true
}

const handleResetPassword = async () => {
  message.value = ''
  errorMessage.value = ''

  if (!validateForm()) {
    return
  }

  loading.value = true

  try {
    const response = await resetPassword({
      username: form.value.username,
      email: form.value.email,
      new_password: form.value.new_password,
      new_password_confirm: form.value.new_password_confirm,
    })

    message.value = response.data.message

    form.value.new_password = ''
    form.value.new_password_confirm = ''
  } catch (error) {
    console.error(error)
    errorMessage.value = getErrorMessage(error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.account-view {
  min-height: 100vh;
  padding: 40px 24px;
  background-color: #f6f7f9;
}

.account-card {
  max-width: 440px;
  margin: 0 auto;
  padding: 28px;
  background-color: #fff;
  border: 1px solid #ddd;
}

.account-card h1 {
  margin: 0;
  font-size: 26px;
  color: #111;
}

.description {
  margin: 10px 0 22px;
  color: #666;
  font-size: 14px;
}

.account-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.account-form label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: #333;
  font-size: 14px;
  font-weight: 700;
}

.account-form input {
  height: 42px;
  padding: 0 10px;
  border: 1px solid #ccc;
  font-size: 14px;
}

.account-form button {
  padding: 12px 16px;
  border: 1px solid #222;
  background-color: #222;
  color: #fff;
  font-weight: 800;
  cursor: pointer;
}

.account-form button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.message {
  margin-top: 16px;
  padding: 12px;
  font-size: 14px;
}

.message.success {
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #15803d;
}

.message.error {
  background-color: #fff5f5;
  border: 1px solid #f0caca;
  color: #c0392b;
}

.link-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-top: 18px;
  font-size: 14px;
}

.link-row a {
  color: #2563eb;
  font-weight: 700;
  text-decoration: none;
}
</style>