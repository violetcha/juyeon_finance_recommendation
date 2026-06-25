<template>
  <main class="account-helper-page">
    <section class="helper-visual-card">
      <h1>
        비밀번호를<br>
        <span>새로 설정하기</span>
      </h1>

      <div class="helper-benefits">
        <article>
          <span>🔐</span>
          <div>
            <strong>아이디와 이메일 확인</strong>
            <p>가입 정보가 일치할 때만 새 비밀번호로 변경합니다.</p>
          </div>
        </article>

        <article>
          <span>✅</span>
          <div>
            <strong>새 비밀번호 적용</strong>
            <p>변경 후 로그인 화면에서 새 비밀번호로 접속하세요.</p>
          </div>
        </article>
      </div>
    </section>

    <section class="account-helper-card">
      <div class="helper-tabs">
        <RouterLink :to="{ name: 'login' }">로그인</RouterLink>
        <button type="button" class="active">비밀번호 재설정</button>
      </div>

      <div class="helper-body">
        <div class="helper-heading">
          <h1>비밀번호 재설정</h1>
        </div>

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
      </div>
    </section>
  </main>
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
.account-helper-page {
  width: min(1180px, calc(100% - 48px));
  margin: 0 auto;
  padding: 34px 0 64px;
  display: grid;
  grid-template-columns: 460px minmax(520px, 620px);
  gap: 40px;
  justify-content: center;
  align-items: stretch;
}

.helper-visual-card,
.account-helper-card {
  border: 1px solid var(--color-border);
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: var(--shadow-soft);
}

.helper-visual-card {
  min-height: 620px;
  padding: 34px;
}

.helper-visual-card h1 {
  margin: 0;
  color: var(--color-text);
  font-size: 48px;
  line-height: 1.16;
  font-weight: 950;
  letter-spacing: -0.065em;
}

.helper-visual-card h1 span {
  color: var(--color-primary);
}

.helper-benefits {
  display: grid;
  gap: 24px;
  margin-top: 42px;
}

.helper-benefits article {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.helper-benefits article > span {
  display: grid;
  place-items: center;
  width: 48px;
  height: 48px;
  flex: 0 0 48px;
  border: 1px solid var(--color-border);
  border-radius: 16px;
  background: #eef4ff;
}

.helper-benefits strong {
  color: var(--color-text);
  font-size: 16px;
  font-weight: 950;
}

.helper-benefits p {
  margin: 6px 0 0;
  color: var(--color-text-muted);
  font-size: 14px;
  line-height: 1.55;
}

.account-helper-card {
  min-height: 620px;
  overflow: hidden;
}

.helper-tabs {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface-soft);
}

.helper-tabs a,
.helper-tabs button {
  display: grid;
  place-items: center;
  min-height: 64px;
  border: 0;
  background: transparent;
  color: var(--color-text-muted);
  font-size: 18px;
  font-weight: 950;
  text-decoration: none;
}

.helper-tabs .active {
  background: #fff;
  color: var(--color-primary);
  box-shadow: inset 0 -3px 0 var(--color-primary);
}

.helper-body {
  width: min(100%, 430px);
  min-height: 520px;
  margin: 0 auto;
  padding: 42px 34px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.helper-heading h1 {
  margin: 0 0 28px;
  color: var(--color-text);
  font-size: 34px;
  font-weight: 950;
  letter-spacing: -0.05em;
}

.account-form {
  display: grid;
  gap: 16px;
}

.account-form label {
  display: grid;
  gap: 8px;
  color: var(--color-text);
  font-size: 14px;
  font-weight: 950;
}

.account-form input {
  width: 100%;
  min-height: 50px;
  box-sizing: border-box;
  border: 1px solid var(--color-border-strong);
  border-radius: 15px;
  padding: 0 14px;
  color: var(--color-text);
  font-size: 14px;
  font-weight: 800;
  outline: none;
}

.account-form input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px rgba(17, 22, 184, 0.08);
}

.account-form button {
  min-height: 52px;
  border: 0;
  border-radius: 15px;
  background: var(--color-primary);
  color: #fff;
  font-size: 16px;
  font-weight: 950;
  box-shadow: 0 16px 28px rgba(17, 22, 184, 0.2);
  cursor: pointer;
}

.account-form button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.message {
  margin: 16px 0 0;
  padding: 12px 14px;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 850;
}

.message.success {
  border: 1px solid #bbf7d0;
  background: #f0fdf4;
  color: #15803d;
}

.message.error {
  border: 1px solid #fecaca;
  background: #fff1f2;
  color: #dc2626;
}

.link-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-top: 20px;
}

.link-row a {
  color: var(--color-primary);
  font-size: 14px;
  font-weight: 950;
  text-decoration: none;
}

@media (max-width: 980px) {
  .account-helper-page {
    grid-template-columns: 1fr;
  }

  .helper-visual-card,
  .account-helper-card {
    min-height: 0;
  }
}

@media (max-width: 640px) {
  .account-helper-page {
    width: min(100% - 28px, var(--container-width));
    padding-top: 20px;
  }

  .helper-visual-card h1 {
    font-size: 40px;
  }

  .helper-body {
    padding: 30px 24px;
  }

  .link-row {
    flex-direction: column;
  }
}
</style>
