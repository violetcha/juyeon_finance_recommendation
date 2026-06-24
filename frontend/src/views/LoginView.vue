<template>
  <main class="auth-page">
    <section class="auth-visual-panel">
      <p class="eyebrow">JUYEON FINANCE START</p>
      <h1>
        주연과 함께<br>
        <span>똑똑한 금융생활</span>을 시작하세요
      </h1>
      <p class="visual-description">
        예적금 추천, 주거래은행 찾기, 환율·금은 시세, 금융 커뮤니티까지
        한 계정으로 편하게 이용할 수 있어요.
      </p>

      <div class="benefit-list">
        <article>
          <span class="benefit-icon mint">↗</span>
          <div>
            <strong>나에게 맞는 금융 추천</strong>
            <p>프로필을 기반으로 예적금과 은행을 추천해드려요.</p>
          </div>
        </article>

        <article>
          <span class="benefit-icon purple">💬</span>
          <div>
            <strong>금융 커뮤니티 참여</strong>
            <p>후기와 질문을 나누며 금융 정보를 함께 확인해요.</p>
          </div>
        </article>

        <article>
          <span class="benefit-icon blue">🔒</span>
          <div>
            <strong>안전하고 편리한 서비스</strong>
            <p>로그인 후 관심상품과 저장 영상을 관리할 수 있어요.</p>
          </div>
        </article>
      </div>

      <div class="auth-illustration" aria-hidden="true">
        <div class="person-card">👨‍💻</div>
        <div class="piggy-card">🐷</div>
        <div class="chart-card">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <div class="coin-stack">₩</div>
      </div>

      <div class="signup-benefit-card">
        <span>🎁</span>
        <div>
          <strong>가입 후 맞춤 추천 준비 완료</strong>
          <p>금융 프로필을 채우면 추천 정확도가 더 좋아집니다.</p>
        </div>
      </div>
    </section>

    <section class="auth-card">
      <div class="auth-tabs">
        <button type="button" class="active">
          로그인
        </button>
        <RouterLink :to="{ name: 'signup' }">
          회원가입
        </RouterLink>
      </div>

      <div class="auth-card-body">
        <div class="form-panel">
          <div class="form-heading">
            <p class="eyebrow">LOGIN</p>
            <h2>로그인</h2>
            <p>아이디와 비밀번호를 입력해 주세요.</p>
          </div>

          <p v-if="successMessage" class="success-message">
            {{ successMessage }}
          </p>

          <form class="login-form" @submit.prevent="handleLogin">
            <div class="form-group">
              <label for="username">아이디</label>
              <input
                id="username"
                v-model.trim="username"
                type="text"
                placeholder="아이디를 입력하세요"
                autocomplete="username"
              >
            </div>

            <div class="form-group">
              <label for="password">비밀번호</label>
              <div class="password-field">
                <input
                  id="password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="비밀번호를 입력하세요"
                  autocomplete="current-password"
                >
                <button
                  type="button"
                  :aria-label="showPassword ? '비밀번호 숨기기' : '비밀번호 보기'"
                  @click="showPassword = !showPassword"
                >
                  {{ showPassword ? '숨김' : '보기' }}
                </button>
              </div>
            </div>

            <div class="form-help-row">
              <label class="save-id">
                <input v-model="rememberId" type="checkbox">
                아이디 저장
              </label>

              <div class="account-help-links">
                <RouterLink :to="{ name: 'find-username' }">
                  아이디 찾기
                </RouterLink>
                <span>|</span>
                <RouterLink :to="{ name: 'reset-password' }">
                  비밀번호 재설정
                </RouterLink>
              </div>
            </div>

            <button type="submit" class="submit-button" :disabled="loading">
              {{ loading ? '로그인 중...' : '로그인' }}
            </button>
          </form>

          <p v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </p>

          <div class="auth-notice">
            <span>🔐</span>
            <div>
              <strong>안전한 금융생활을 위해</strong>
              <p>공용 PC에서는 로그인 후 반드시 로그아웃해주세요.</p>
            </div>
          </div>
        </div>

        <aside class="signup-guide-panel">
          <div class="guide-heading">
            <h3>간편하게 회원가입하고<br>더 많은 서비스를 경험하세요.</h3>
            <p>가입 후 금융 프로필을 입력하면 실제 데이터 기반 추천을 받을 수 있습니다.</p>
          </div>

          <ul class="profile-benefits">
            <li>
              <span>🎂</span>
              <div>
                <strong>나이·성별</strong>
                <p>가입대상과 전용 상품 조건을 추천에 반영합니다.</p>
              </div>
            </li>
            <li>
              <span>💼</span>
              <div>
                <strong>월 소득 구간</strong>
                <p>저축 가능성과 상품 조건을 함께 봅니다.</p>
              </div>
            </li>
            <li>
              <span>💰</span>
              <div>
                <strong>월 저축 가능 금액</strong>
                <p>목표 금액에 맞는 상품을 추천합니다.</p>
              </div>
            </li>
            <li>
              <span>🏦</span>
              <div>
                <strong>주거래은행</strong>
                <p>선호 은행과 추천 상품을 연결합니다.</p>
              </div>
            </li>
            <li>
              <span>📍</span>
              <div>
                <strong>거주 지역</strong>
                <p>주변 은행 접근성 비교에 활용됩니다.</p>
              </div>
            </li>
          </ul>

          <RouterLink :to="{ name: 'signup' }" class="outline-cta">
            회원가입 시작하기
          </RouterLink>
        </aside>
      </div>
    </section>
  </main>
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
const showPassword = ref(false)
const rememberId = ref(false)

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

    if (rememberId.value) {
      localStorage.setItem('savedUsername', username.value)
    } else {
      localStorage.removeItem('savedUsername')
    }

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
  const savedUsername = localStorage.getItem('savedUsername')

  if (savedUsername) {
    username.value = savedUsername
    rememberId.value = true
  }

  if (route.query.signup === 'success') {
    successMessage.value = '회원가입이 완료되었습니다. 로그인해주세요.'
  }
})
</script>

<style scoped>
.auth-page {
  width: min(var(--container-width), calc(100% - 48px));
  margin: 0 auto;
  padding: 64px 0 70px;
  display: grid;
  grid-template-columns: minmax(0, 0.92fr) minmax(620px, 1.08fr);
  gap: 46px;
  align-items: center;
}

.eyebrow {
  margin: 0 0 10px;
  color: var(--color-primary);
  font-size: 12px;
  font-weight: 950;
  letter-spacing: 0.12em;
}

.auth-visual-panel h1 {
  margin: 0;
  color: var(--color-text);
  font-size: clamp(40px, 5vw, 58px);
  line-height: 1.16;
  font-weight: 950;
  letter-spacing: -0.065em;
}

.auth-visual-panel h1 span {
  color: var(--color-primary);
}

.visual-description {
  max-width: 460px;
  margin: 24px 0 0;
  color: var(--color-text-muted);
  font-size: 17px;
  line-height: 1.75;
}

.benefit-list {
  display: grid;
  gap: 22px;
  margin-top: 34px;
}

.benefit-list article,
.signup-benefit-card,
.profile-benefits li,
.auth-notice {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.benefit-icon,
.profile-benefits span,
.auth-notice span,
.signup-benefit-card > span {
  display: grid;
  place-items: center;
  width: 48px;
  height: 48px;
  border-radius: 16px;
  flex-shrink: 0;
  font-weight: 950;
}

.benefit-icon.mint {
  background: var(--color-accent-soft);
  color: var(--color-accent);
}

.benefit-icon.purple {
  background: #f3e8ff;
  color: #7c3aed;
}

.benefit-icon.blue {
  background: #eaf0ff;
  color: var(--color-primary);
}

.benefit-list strong,
.signup-benefit-card strong,
.profile-benefits strong,
.auth-notice strong {
  color: var(--color-text);
  font-size: 16px;
  font-weight: 950;
}

.benefit-list p,
.signup-benefit-card p,
.profile-benefits p,
.auth-notice p {
  margin: 6px 0 0;
  color: var(--color-text-muted);
  font-size: 14px;
  line-height: 1.55;
}

.auth-illustration {
  position: relative;
  height: 220px;
  margin-top: 24px;
}

.person-card,
.piggy-card,
.chart-card,
.coin-stack {
  position: absolute;
  display: grid;
  place-items: center;
  border: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.95);
  box-shadow: var(--shadow-soft);
}

.person-card {
  left: 180px;
  top: 30px;
  width: 170px;
  height: 150px;
  border-radius: 42px;
  background: #eff6ff;
  font-size: 82px;
}

.piggy-card {
  left: 104px;
  bottom: 18px;
  width: 86px;
  height: 70px;
  border-radius: 28px;
  background: var(--color-accent-soft);
  font-size: 42px;
}

.chart-card {
  right: 112px;
  top: 10px;
  width: 88px;
  height: 72px;
  grid-template-columns: repeat(3, 12px);
  gap: 8px;
  align-items: end;
  padding: 14px;
  border-radius: 22px;
}

.chart-card span {
  display: block;
  width: 12px;
  border-radius: 999px;
  background: linear-gradient(180deg, #6875ff, var(--color-primary));
}

.chart-card span:nth-child(1) { height: 26px; }
.chart-card span:nth-child(2) { height: 42px; }
.chart-card span:nth-child(3) { height: 56px; background: linear-gradient(180deg, #3ee5ca, var(--color-accent)); }

.coin-stack {
  right: 64px;
  bottom: 30px;
  width: 70px;
  height: 70px;
  border-radius: 26px;
  background: #fff7e5;
  color: #d97706;
  font-size: 34px;
  font-weight: 950;
}

.signup-benefit-card {
  max-width: 500px;
  margin-top: 20px;
  padding: 18px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: rgba(255, 255, 255, 0.88);
  box-shadow: var(--shadow-soft);
}

.signup-benefit-card > span {
  background: #eff6ff;
}

.auth-card {
  border: 1px solid var(--color-border);
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: var(--shadow-card);
  overflow: hidden;
}

.auth-tabs {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface-soft);
}

.auth-tabs button,
.auth-tabs a {
  display: grid;
  place-items: center;
  min-height: 66px;
  border: 0;
  background: transparent;
  color: var(--color-text-muted);
  font-size: 18px;
  font-weight: 950;
  text-decoration: none;
}

.auth-tabs .active {
  background: #fff;
  color: var(--color-primary);
  box-shadow: inset 0 -3px 0 var(--color-primary);
}

.auth-card-body {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 0.92fr;
  gap: 0;
}

.form-panel,
.signup-guide-panel {
  padding: 36px 34px;
}

.form-panel {
  border-right: 1px solid var(--color-border);
}

.form-heading h2 {
  margin: 0;
  color: var(--color-text);
  font-size: 28px;
  font-weight: 950;
}

.form-heading p,
.guide-heading p {
  margin: 8px 0 0;
  color: var(--color-text-muted);
  line-height: 1.55;
}

.login-form {
  display: grid;
  gap: 18px;
  margin-top: 26px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: var(--color-text);
  font-size: 14px;
  font-weight: 950;
}

.form-group input,
.password-field input {
  width: 100%;
  min-height: 48px;
  box-sizing: border-box;
  border: 1px solid var(--color-border-strong);
  border-radius: 14px;
  background: #fff;
  color: var(--color-text);
  outline: none;
  padding: 0 14px;
  font-size: 14px;
  font-weight: 800;
}

.form-group input:focus,
.password-field input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px rgba(17, 22, 184, 0.08);
}

.password-field {
  position: relative;
}

.password-field input {
  padding-right: 64px;
}

.password-field button {
  position: absolute;
  right: 10px;
  top: 50%;
  border: 0;
  background: transparent;
  color: var(--color-text-muted);
  font-size: 12px;
  font-weight: 950;
  transform: translateY(-50%);
  cursor: pointer;
}

.form-help-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  font-size: 13px;
}

.save-id {
  display: inline-flex;
  gap: 7px;
  align-items: center;
  color: var(--color-text-muted);
  font-weight: 800;
}

.save-id input {
  accent-color: var(--color-primary);
}

.account-help-links {
  display: flex;
  gap: 8px;
  align-items: center;
}

.account-help-links a {
  color: var(--color-primary);
  font-weight: 950;
  text-decoration: none;
}

.account-help-links span {
  color: var(--color-border-strong);
}

.submit-button {
  min-height: 50px;
  border: 0;
  border-radius: 14px;
  background: var(--color-primary);
  color: #fff;
  font-size: 16px;
  font-weight: 950;
  cursor: pointer;
  box-shadow: 0 16px 28px rgba(17, 22, 184, 0.22);
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message,
.success-message {
  margin: 16px 0 0;
  padding: 13px 14px;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 800;
}

.error-message {
  border: 1px solid #fecaca;
  background: #fff5f5;
  color: var(--color-danger);
}

.success-message {
  border: 1px solid #bbf7d0;
  background: #f0fdf4;
  color: #15803d;
}

.auth-notice {
  margin-top: 26px;
  padding: 16px;
  border-radius: var(--radius-md);
  background: var(--color-surface-soft);
}

.auth-notice span {
  width: 38px;
  height: 38px;
  background: #eaf0ff;
}

.signup-guide-panel {
  background: linear-gradient(180deg, #fff 0%, #f8fbff 100%);
}

.guide-heading h3 {
  margin: 0;
  color: var(--color-text);
  font-size: 21px;
  line-height: 1.38;
  font-weight: 950;
}

.profile-benefits {
  display: grid;
  gap: 18px;
  margin: 26px 0;
  padding: 0;
  list-style: none;
}

.profile-benefits span {
  width: 44px;
  height: 44px;
  background: #fff;
  border: 1px solid var(--color-border);
}

.outline-cta {
  display: grid;
  place-items: center;
  min-height: 48px;
  border: 1px solid var(--color-primary);
  border-radius: 14px;
  color: var(--color-primary);
  background: #fff;
  font-weight: 950;
  text-decoration: none;
}

@media (max-width: 1120px) {
  .auth-page {
    grid-template-columns: 1fr;
  }

  .auth-visual-panel {
    display: none;
  }

  .auth-card-body {
    grid-template-columns: 1fr;
  }

  .form-panel {
    border-right: 0;
    border-bottom: 1px solid var(--color-border);
  }
}

@media (max-width: 680px) {
  .auth-page {
    width: min(100% - 28px, var(--container-width));
    padding: 28px 0 44px;
  }

  .form-panel,
  .signup-guide-panel {
    padding: 26px 22px;
  }

  .form-help-row {
    align-items: flex-start;
    flex-direction: column;
  }
}

/* Juyeon clean auth override */
.auth-page {
  align-items: start;
  padding: 48px 0 68px;
}

.auth-visual-panel {
  padding: 30px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  background: rgba(255, 255, 255, 0.82);
  box-shadow: var(--shadow-soft);
}

.auth-visual-panel h1 {
  font-size: clamp(34px, 4.4vw, 52px);
}

.auth-illustration {
  display: none;
}

.auth-card {
  border-radius: 24px;
  background: #fff;
  box-shadow: var(--shadow-card);
}

.auth-tabs {
  background: #f8fafc;
}

.form-panel,
.signup-guide-panel {
  padding: 32px;
}

.form-group input,
.password-field,
.form-group select {
  border-color: var(--color-border-strong);
  background: #fff;
}

.submit-button,
.outline-cta {
  border-radius: 13px;
}

.signup-benefit-card,
.benefit-list article,
.auth-notice,
.profile-benefits li {
  border-radius: 18px;
}

@media (max-width: 1180px) {
  .auth-page {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 680px) {
  .auth-page {
    width: min(100% - 28px, var(--container-width));
    padding: 28px 0 44px;
  }

  .form-panel,
  .signup-guide-panel {
    padding: 26px 22px;
  }
}

</style>
