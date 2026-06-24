<template>
  <div class="account-view">
    <section class="account-card">
      <h1>아이디 찾기</h1>
      <p class="description">
        가입할 때 입력한 이메일을 입력하면 아이디를 확인할 수 있습니다.
      </p>

      <form class="account-form" @submit.prevent="handleFindUsername">
        <label>
          이메일
          <input
            v-model.trim="email"
            type="email"
            placeholder="이메일을 입력하세요"
            autocomplete="email"
          >
        </label>

        <button type="submit" :disabled="loading">
          {{ loading ? '확인 중...' : '아이디 찾기' }}
        </button>
      </form>

      <p v-if="message" class="message success">
        {{ message }}
      </p>

      <p v-if="errorMessage" class="message error">
        {{ errorMessage }}
      </p>

      <div v-if="usernames.length > 0" class="result-box">
        <h2>가입된 아이디</h2>

        <div
          v-for="item in usernames"
          :key="item.username"
          class="result-row"
        >
          <strong>{{ item.username }}</strong>
          <span>가입일: {{ item.created_at }}</span>
        </div>
      </div>

      <div class="link-row">
        <RouterLink :to="{ name: 'login' }">
          로그인으로 돌아가기
        </RouterLink>
        <RouterLink :to="{ name: 'reset-password' }">
          비밀번호 재설정
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { findUsername } from '@/api/accounts'

const email = ref('')
const usernames = ref([])
const message = ref('')
const errorMessage = ref('')
const loading = ref(false)

const getErrorMessage = (error) => {
  return (
    error.response?.data?.message ||
    '아이디 찾기 중 문제가 발생했습니다.'
  )
}

const handleFindUsername = async () => {
  message.value = ''
  errorMessage.value = ''
  usernames.value = []

  if (!email.value) {
    errorMessage.value = '이메일을 입력해주세요.'
    return
  }

  loading.value = true

  try {
    const response = await findUsername({
      email: email.value,
    })

    message.value = response.data.message
    usernames.value = response.data.usernames || []
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

.result-box {
  margin-top: 18px;
  padding: 16px;
  border: 1px solid #ddd;
  background-color: #fafafa;
}

.result-box h2 {
  margin: 0 0 12px;
  font-size: 18px;
}

.result-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
  font-size: 14px;
}

.result-row:last-child {
  border-bottom: 0;
}

.result-row span {
  color: #666;
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