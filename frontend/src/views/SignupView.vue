<template>
  <main class="signup-page">
    <section class="signup-visual-panel">
      <p class="eyebrow">JOIN FIRST FINANCE</p>
      <h1>
        간단하게 가입하고<br>
        <span>맞춤 금융 추천</span>을 받아보세요
      </h1>
      <p class="visual-description">
        회원가입 때 입력한 금융 프로필은 실제 예적금 추천, 주거래은행 비교,
        가입대상 필터링에 활용됩니다.
      </p>

      <ul class="join-benefit-list">
        <li>
          <span>🎂</span>
          <div>
            <strong>나이·성별 조건 반영</strong>
            <p>가입대상에 맞지 않는 상품은 추천에서 제외합니다.</p>
          </div>
        </li>
        <li>
          <span>💰</span>
          <div>
            <strong>저축 가능 금액 분석</strong>
            <p>월 저축 가능 금액과 목돈 규모를 함께 봅니다.</p>
          </div>
        </li>
        <li>
          <span>🏦</span>
          <div>
            <strong>주거래은행 기반 추천</strong>
            <p>선호 은행과 가까운 은행 정보를 연결합니다.</p>
          </div>
        </li>
      </ul>

      <div class="signup-illustration" aria-hidden="true">
        <div class="person-card">🧑‍💼</div>
        <div class="gift-card">🎁</div>
        <div class="chart-card">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <div class="lock-card">🔒</div>
      </div>
    </section>

    <section class="signup-shell">
      <div class="auth-tabs">
        <RouterLink :to="{ name: 'login' }">
          로그인
        </RouterLink>
        <button type="button" class="active">
          회원가입
        </button>
      </div>

      <div class="signup-card-body">
        <div class="signup-main-card">
          <div class="signup-header">
            <p class="eyebrow">SIGN UP</p>
            <h1>회원가입</h1>
            <p>
              예적금 추천을 위해 기본 정보와 금융 프로필을 입력해주세요.
            </p>
          </div>

          <div class="step-indicator">
            <div :class="['step-item', { active: currentStep === 1, done: currentStep > 1 }]">
              <span>1</span>
              <strong>기본 정보</strong>
            </div>

            <div class="step-line"></div>

            <div :class="['step-item', { active: currentStep === 2 }]">
              <span>2</span>
              <strong>금융 정보</strong>
            </div>
          </div>

          <form class="signup-form" @submit.prevent="handleSubmit">
            <section v-if="currentStep === 1" class="form-section">
              <div class="section-title">
                <h2>기본 정보</h2>
                <p>로그인과 상품 추천 가능 여부를 판단하는 정보입니다.</p>
              </div>

              <div class="form-grid two">
                <div class="form-group">
                  <div class="label-row">
                    <label for="username">아이디</label>
                    <span
                      v-if="usernameCheck.message"
                      :class="['inline-check-message', usernameCheck.available ? 'success' : 'error']"
                    >
                      {{ usernameCheck.message }}
                    </span>
                  </div>

                  <div class="input-with-button">
                    <input
                      id="username"
                      v-model.trim="form.username"
                      type="text"
                      placeholder="아이디를 입력하세요"
                      autocomplete="username"
                      @input="resetUsernameCheck"
                    >
                    <button
                      type="button"
                      class="check-button"
                      :disabled="usernameCheck.loading || !form.username"
                      @click="handleCheckUsername"
                    >
                      {{ usernameCheck.loading ? '확인중' : '중복확인' }}
                    </button>
                  </div>
                </div>

                <div class="form-group">
                  <div class="label-row">
                    <label for="email">이메일</label>
                    <span
                      v-if="emailCheck.message"
                      :class="['inline-check-message', emailCheck.available ? 'success' : 'error']"
                    >
                      {{ emailCheck.message }}
                    </span>
                  </div>

                  <div class="input-with-button">
                    <input
                      id="email"
                      v-model.trim="form.email"
                      type="email"
                      placeholder="이메일을 입력하세요"
                      autocomplete="email"
                      @input="resetEmailCheck"
                    >
                    <button
                      type="button"
                      class="check-button"
                      :disabled="emailCheck.loading || !form.email"
                      @click="handleCheckEmail"
                    >
                      {{ emailCheck.loading ? '확인중' : '중복확인' }}
                    </button>
                  </div>
                </div>

                <div class="form-group">
                  <div class="label-row">
                    <label for="password1">비밀번호</label>
                    <span v-if="passwordValidationMessage" class="inline-check-message error">
                      {{ passwordValidationMessage }}
                    </span>
                  </div>

                  <input
                    id="password1"
                    v-model="form.password"
                    type="password"
                    placeholder="비밀번호를 입력하세요"
                    autocomplete="new-password"
                  >
                </div>

                <div class="form-group">
                  <div class="label-row">
                    <label for="password2">비밀번호 확인</label>
                    <span v-if="passwordConfirmValidationMessage" class="inline-check-message error">
                      {{ passwordConfirmValidationMessage }}
                    </span>
                  </div>

                  <input
                    id="password2"
                    v-model="form.password_confirm"
                    type="password"
                    placeholder="비밀번호를 다시 입력하세요"
                    autocomplete="new-password"
                  >
                </div>

                <div class="form-group">
                  <label for="age">나이</label>
                  <select id="age" v-model.number="form.age">
                    <option :value="null">나이를 선택하세요</option>
                    <option
                      v-for="option in profileOptions.age"
                      :key="option.value"
                      :value="option.value"
                    >
                      {{ option.label }}
                    </option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="gender">성별</label>
                  <select id="gender" v-model="form.gender">
                    <option value="unknown">성별을 선택하세요</option>
                    <option
                      v-for="option in profileOptions.gender.filter((item) => item.value !== 'unknown')"
                      :key="option.value"
                      :value="option.value"
                    >
                      {{ option.label }}
                    </option>
                  </select>
                  <p class="field-help">
                    성별 전용 상품을 추천에서 제외하거나 반영하는 데 사용됩니다.
                  </p>
                </div>

                <div class="form-group">
                  <label for="mainBank">주거래은행</label>
                  <select id="mainBank" v-model="form.main_bank">
                    <option value="">주거래은행을 선택하세요</option>
                    <option
                      v-for="option in profileOptions.main_bank"
                      :key="option.value"
                      :value="option.value"
                    >
                      {{ option.label }}
                    </option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="address">거주 지역</label>
                  <select id="address" v-model="form.address">
                    <option value="">거주 지역을 선택하세요</option>
                    <option
                      v-for="option in profileOptions.address"
                      :key="option.value"
                      :value="option.value"
                    >
                      {{ option.label }}
                    </option>
                  </select>
                </div>
              </div>

              <label class="checkbox-label">
                <input
                  v-model="form.personal_info_agree"
                  type="checkbox"
                >
                예적금 추천을 위한 개인정보 활용에 동의합니다.
              </label>
            </section>

            <section v-else class="form-section">
              <div class="section-title">
                <h2>금융 정보</h2>
                <p>입력한 금융 정보는 실제 예적금 상품 추천에 활용됩니다.</p>
              </div>

              <div class="form-grid">
                <div class="form-group">
                  <label for="monthlyIncome">월 소득 구간</label>
                  <select id="monthlyIncome" v-model="form.monthly_income_range">
                    <option value="">월 소득 구간을 선택하세요</option>
                    <option
                      v-for="option in profileOptions.monthly_income_range"
                      :key="option.value"
                      :value="option.value"
                    >
                      {{ option.label }}
                    </option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="monthlySaving">월 저축 가능 금액</label>
                  <select id="monthlySaving" v-model="form.monthly_saving_amount">
                    <option value="">월 저축 가능 금액을 선택하세요</option>
                    <option
                      v-for="option in profileOptions.monthly_saving_amount"
                      :key="option.value"
                      :value="option.value"
                    >
                      {{ option.label }}
                    </option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="lumpSum">현재 보유 목돈</label>
                  <select id="lumpSum" v-model="form.lump_sum_amount">
                    <option value="">현재 보유 목돈을 선택하세요</option>
                    <option
                      v-for="option in profileOptions.lump_sum_amount"
                      :key="option.value"
                      :value="option.value"
                    >
                      {{ option.label }}
                    </option>
                  </select>
                </div>
              </div>

              <div class="summary-box">
                <h3>입력한 기본 정보</h3>
                <div class="summary-grid">
                  <p>
                    <strong>아이디</strong>
                    <span>{{ form.username }}</span>
                  </p>
                  <p>
                    <strong>이메일</strong>
                    <span>{{ form.email || '미입력' }}</span>
                  </p>
                  <p>
                    <strong>나이</strong>
                    <span>{{ form.age ? `${form.age}세` : '미입력' }}</span>
                  </p>
                  <p>
                    <strong>성별</strong>
                    <span>{{ getGenderLabel(form.gender) }}</span>
                  </p>
                  <p>
                    <strong>주거래은행</strong>
                    <span>{{ form.main_bank || '미입력' }}</span>
                  </p>
                  <p>
                    <strong>거주 지역</strong>
                    <span>{{ form.address || '미입력' }}</span>
                  </p>
                </div>
              </div>
            </section>

            <p v-if="errorMessage" class="error-message">
              {{ errorMessage }}
            </p>

            <div class="button-row">
              <button
                v-if="currentStep === 2"
                type="button"
                class="secondary-button"
                :disabled="submitting"
                @click="goPreviousStep"
              >
                이전
              </button>

              <button
                type="submit"
                class="submit-button"
                :disabled="submitting"
              >
                <span v-if="currentStep === 1">다음 단계로</span>
                <span v-else>{{ submitting ? '가입 중...' : '회원가입 완료' }}</span>
              </button>
            </div>
          </form>
        </div>

        <aside class="signup-guide-panel">
          <h2>가입 후 바로 이용할 수 있어요</h2>
          <p>
            회원가입 후 맞춤 추천, 관심상품, 커뮤니티 기능을 이용할 수 있습니다.
          </p>

          <ul>
            <li>
              <span>✓</span>
              나이와 성별로 가입 불가능 상품 제외
            </li>
            <li>
              <span>✓</span>
              월 저축 가능 금액으로 상품 조건 비교
            </li>
            <li>
              <span>✓</span>
              주거래은행과 선호 은행 반영
            </li>
            <li>
              <span>✓</span>
              거주 지역 기반 은행 접근성 확인
            </li>
          </ul>

          <RouterLink :to="{ name: 'login' }" class="outline-cta">
            이미 계정이 있어요
          </RouterLink>
        </aside>
      </div>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { signup, getProfileOptions } from '@/api/accounts'
import api from '@/api/api'

const router = useRouter()


const checkUsername = (username) => {
  return api.get('/accounts/check-username/', {
    params: { username },
  })
}

const checkEmail = (email) => {
  return api.get('/accounts/check-email/', {
    params: { email },
  })
}


const finalMainBankOptions = [
  '국민은행',
  '신한은행',
  '하나은행',
  '우리은행',
  'NH농협은행',
  '부산은행',
  '경남은행',
  '광주은행',
  '전북은행',
  '제주은행',
  'IBK기업은행',
  'SC제일은행',
  'iM뱅크',
  'KDB산업은행',
  '수협은행',
  '카카오뱅크',
  '토스뱅크',
  '케이뱅크',
].map((name) => ({
  value: name,
  label: name,
}))

const currentStep = ref(1)
const errorMessage = ref('')
const submitting = ref(false)

const usernameCheck = ref({
  loading: false,
  available: false,
  checkedValue: '',
  message: '',
})

const emailCheck = ref({
  loading: false,
  available: false,
  checkedValue: '',
  message: '',
})

const form = ref({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
  age: null,
  gender: 'unknown',
  monthly_income_range: '',
  monthly_saving_amount: '',
  lump_sum_amount: '',
  main_bank: '',
  address: '',
  personal_info_agree: false,
})

const profileOptions = ref({
  age: [],
  gender: [
    { value: 'unknown', label: '선택 안 함' },
    { value: 'male', label: '남성' },
    { value: 'female', label: '여성' },
  ],
  monthly_income_range: [],
  monthly_saving_amount: [],
  lump_sum_amount: [],
  main_bank: finalMainBankOptions,
  address: [],
})


const passwordValidationMessage = computed(() => {
  if (!form.value.password) {
    return ''
  }

  if (form.value.password.length < 8) {
    return '8자 이상 입력해주세요.'
  }

  return ''
})

const passwordConfirmValidationMessage = computed(() => {
  if (!form.value.password_confirm) {
    return ''
  }

  if (form.value.password !== form.value.password_confirm) {
    return '비밀번호가 일치하지 않습니다.'
  }

  return ''
})

const resetUsernameCheck = () => {
  usernameCheck.value = {
    loading: false,
    available: false,
    checkedValue: '',
    message: '',
  }
}

const resetEmailCheck = () => {
  emailCheck.value = {
    loading: false,
    available: false,
    checkedValue: '',
    message: '',
  }
}

const handleCheckUsername = async () => {
  if (!form.value.username) {
    usernameCheck.value.message = '아이디를 입력해주세요.'
    usernameCheck.value.available = false
    return
  }

  usernameCheck.value.loading = true
  usernameCheck.value.message = ''

  try {
    const response = await checkUsername(form.value.username)

    usernameCheck.value = {
      loading: false,
      available: Boolean(response.data.available),
      checkedValue: form.value.username,
      message: response.data.message || '확인이 완료되었습니다.',
    }
  } catch (error) {
    usernameCheck.value = {
      loading: false,
      available: false,
      checkedValue: '',
      message: error.response?.data?.message || '아이디 중복 확인에 실패했습니다.',
    }
  }
}

const handleCheckEmail = async () => {
  if (!form.value.email) {
    emailCheck.value.message = '이메일을 입력해주세요.'
    emailCheck.value.available = false
    return
  }

  emailCheck.value.loading = true
  emailCheck.value.message = ''

  try {
    const response = await checkEmail(form.value.email)

    emailCheck.value = {
      loading: false,
      available: Boolean(response.data.available),
      checkedValue: form.value.email,
      message: response.data.message || '확인이 완료되었습니다.',
    }
  } catch (error) {
    emailCheck.value = {
      loading: false,
      available: false,
      checkedValue: '',
      message: error.response?.data?.message || '이메일 중복 확인에 실패했습니다.',
    }
  }
}

const getFirstErrorFromObject = (data) => {
  if (!data) {
    return ''
  }

  if (typeof data === 'string') {
    return data
  }

  if (Array.isArray(data)) {
    return data[0] || ''
  }

  if (typeof data === 'object') {
    if (data.message) {
      return getFirstErrorFromObject(data.message)
    }

    const firstValue = Object.values(data)[0]
    return getFirstErrorFromObject(firstValue)
  }

  return ''
}

const getSignupErrorMessage = (error) => {
  const message = getFirstErrorFromObject(error.response?.data)

  if (message) {
    return message
  }

  if (error.response?.status === 400) {
    return '입력값을 확인해주세요.'
  }

  return '회원가입 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.'
}

const getGenderLabel = (value) => {
  const option = profileOptions.value.gender.find((item) => item.value === value)
  return option?.label || '미입력'
}

const fetchProfileOptions = async () => {
  try {
    const response = await getProfileOptions()
    profileOptions.value = {
      ...response.data,
      gender: response.data.gender || [
        { value: 'unknown', label: '선택 안 함' },
        { value: 'male', label: '남성' },
        { value: 'female', label: '여성' },
      ],
      main_bank: finalMainBankOptions,
    }
  } catch (error) {
    console.error(error)
    errorMessage.value = '금융 프로필 선택지를 불러오지 못했습니다.'
  }
}

const validateStepOne = () => {
  if (!form.value.username) {
    errorMessage.value = '아이디를 입력해주세요.'
    return false
  }

  if (!form.value.password) {
    errorMessage.value = '비밀번호를 입력해주세요.'
    return false
  }

  if (passwordValidationMessage.value) {
    errorMessage.value = passwordValidationMessage.value
    return false
  }

  if (!form.value.password_confirm) {
    errorMessage.value = '비밀번호 확인을 입력해주세요.'
    return false
  }

  if (passwordConfirmValidationMessage.value) {
    errorMessage.value = passwordConfirmValidationMessage.value
    return false
  }

  if (!usernameCheck.value.available || usernameCheck.value.checkedValue !== form.value.username) {
    errorMessage.value = '아이디 중복 확인을 완료해주세요.'
    return false
  }

  if (form.value.email && (!emailCheck.value.available || emailCheck.value.checkedValue !== form.value.email)) {
    errorMessage.value = '이메일 중복 확인을 완료해주세요.'
    return false
  }

  if (!form.value.age) {
    errorMessage.value = '나이를 선택해주세요.'
    return false
  }

  if (!form.value.gender || form.value.gender === 'unknown') {
    errorMessage.value = '성별을 선택해주세요. 성별 전용 상품 추천 여부를 판단하는 데 사용됩니다.'
    return false
  }

  if (!form.value.main_bank) {
    errorMessage.value = '주거래은행을 선택해주세요.'
    return false
  }

  if (!form.value.address) {
    errorMessage.value = '거주 지역을 선택해주세요.'
    return false
  }

  if (!form.value.personal_info_agree) {
    errorMessage.value = '개인정보 활용에 동의해주세요.'
    return false
  }

  return true
}

const validateStepTwo = () => {
  if (!form.value.monthly_income_range) {
    errorMessage.value = '월 소득 구간을 선택해주세요.'
    return false
  }

  if (!form.value.monthly_saving_amount) {
    errorMessage.value = '월 저축 가능 금액을 선택해주세요.'
    return false
  }

  if (!form.value.lump_sum_amount) {
    errorMessage.value = '현재 보유 목돈을 선택해주세요.'
    return false
  }

  return true
}

const goNextStep = () => {
  errorMessage.value = ''

  if (!validateStepOne()) {
    return
  }

  currentStep.value = 2
}

const goPreviousStep = () => {
  errorMessage.value = ''
  currentStep.value = 1
}

const submitSignup = async () => {
  errorMessage.value = ''

  if (!validateStepTwo()) {
    return
  }

  submitting.value = true

  try {
    await signup({
      username: form.value.username,
      email: form.value.email,
      password: form.value.password,
      password_confirm: form.value.password_confirm,
      age: form.value.age,
      gender: form.value.gender,
      monthly_income_range: form.value.monthly_income_range,
      monthly_saving_amount: form.value.monthly_saving_amount,
      lump_sum_amount: form.value.lump_sum_amount,
      main_bank: form.value.main_bank,
      address: form.value.address,
      personal_info_agree: form.value.personal_info_agree,
    })

    router.push({
      name: 'login',
      query: {
        signup: 'success',
      },
    })
  } catch (error) {
    console.error(error)
    errorMessage.value = getSignupErrorMessage(error)
  } finally {
    submitting.value = false
  }
}

const handleSubmit = () => {
  if (currentStep.value === 1) {
    goNextStep()
    return
  }

  submitSignup()
}

onMounted(() => {
  fetchProfileOptions()
})
</script>

<style scoped>
.signup-page {
  width: min(var(--container-width), calc(100% - 48px));
  margin: 0 auto;
  padding: 54px 0 70px;
  display: grid;
  grid-template-columns: minmax(0, 0.78fr) minmax(660px, 1.22fr);
  gap: 38px;
  align-items: center;
}

.eyebrow {
  margin: 0 0 10px;
  color: var(--color-primary);
  font-size: 12px;
  font-weight: 950;
  letter-spacing: 0.12em;
}

.signup-visual-panel h1 {
  margin: 0;
  color: var(--color-text);
  font-size: clamp(38px, 4.6vw, 54px);
  line-height: 1.16;
  font-weight: 950;
  letter-spacing: -0.065em;
}

.signup-visual-panel h1 span {
  color: var(--color-primary);
}

.visual-description {
  max-width: 480px;
  margin: 22px 0 0;
  color: var(--color-text-muted);
  font-size: 17px;
  line-height: 1.7;
}

.join-benefit-list {
  display: grid;
  gap: 18px;
  margin: 30px 0 0;
  padding: 0;
  list-style: none;
}

.join-benefit-list li {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.join-benefit-list span {
  display: grid;
  place-items: center;
  width: 46px;
  height: 46px;
  border: 1px solid var(--color-border);
  border-radius: 16px;
  background: #fff;
  flex-shrink: 0;
  box-shadow: var(--shadow-soft);
}

.join-benefit-list strong {
  color: var(--color-text);
  font-size: 16px;
  font-weight: 950;
}

.join-benefit-list p {
  margin: 5px 0 0;
  color: var(--color-text-muted);
  font-size: 14px;
  line-height: 1.55;
}

.signup-illustration {
  position: relative;
  height: 190px;
  margin-top: 26px;
}

.person-card,
.gift-card,
.chart-card,
.lock-card {
  position: absolute;
  display: grid;
  place-items: center;
  border: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.95);
  box-shadow: var(--shadow-soft);
}

.person-card {
  left: 150px;
  top: 12px;
  width: 150px;
  height: 132px;
  border-radius: 40px;
  background: #eff6ff;
  font-size: 72px;
}

.gift-card {
  left: 54px;
  bottom: 20px;
  width: 76px;
  height: 76px;
  border-radius: 26px;
  background: #f3e8ff;
  font-size: 38px;
}

.chart-card {
  right: 84px;
  top: 22px;
  width: 82px;
  height: 66px;
  grid-template-columns: repeat(3, 12px);
  gap: 8px;
  align-items: end;
  padding: 13px;
  border-radius: 22px;
}

.chart-card span {
  display: block;
  width: 12px;
  border-radius: 999px;
  background: linear-gradient(180deg, #6875ff, var(--color-primary));
}

.chart-card span:nth-child(1) { height: 24px; }
.chart-card span:nth-child(2) { height: 42px; }
.chart-card span:nth-child(3) { height: 54px; background: linear-gradient(180deg, #3ee5ca, var(--color-accent)); }

.lock-card {
  right: 20px;
  bottom: 16px;
  width: 68px;
  height: 68px;
  border-radius: 24px;
  background: var(--color-accent-soft);
  font-size: 34px;
}

.signup-shell {
  border: 1px solid var(--color-border);
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.95);
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
  min-height: 62px;
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

.signup-card-body {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 300px;
}

.signup-main-card {
  padding: 34px;
  border-right: 1px solid var(--color-border);
}

.signup-header h1 {
  margin: 0;
  color: var(--color-text);
  font-size: 30px;
  font-weight: 950;
  letter-spacing: -0.04em;
}

.signup-header p {
  margin: 8px 0 0;
  color: var(--color-text-muted);
  line-height: 1.55;
}

.step-indicator {
  display: flex;
  align-items: center;
  margin: 26px 0;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--color-text-light);
  font-size: 14px;
  font-weight: 950;
}

.step-item span {
  display: inline-grid;
  place-items: center;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #e5e7eb;
  color: var(--color-text-muted);
}

.step-item.active,
.step-item.done {
  color: var(--color-primary);
}

.step-item.active span,
.step-item.done span {
  background: var(--color-primary);
  color: #fff;
}

.step-line {
  flex: 1;
  height: 1px;
  margin: 0 12px;
  background: var(--color-border);
}

.signup-form {
  display: grid;
  gap: 18px;
}

.form-section {
  padding-top: 4px;
}

.section-title h2 {
  margin: 0;
  color: var(--color-text);
  font-size: 21px;
  font-weight: 950;
}

.section-title p {
  margin: 7px 0 18px;
  color: var(--color-text-muted);
  font-size: 14px;
}

.form-grid {
  display: grid;
  gap: 15px;
}

.form-grid.two {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.form-group label {
  display: block;
  margin-bottom: 7px;
  color: var(--color-text);
  font-size: 13px;
  font-weight: 950;
}

.form-group input,
.form-group select {
  width: 100%;
  min-height: 46px;
  box-sizing: border-box;
  border: 1px solid var(--color-border-strong);
  border-radius: 14px;
  background: #fff;
  color: var(--color-text);
  outline: none;
  padding: 0 13px;
  font-size: 14px;
  font-weight: 800;
}

.form-group input:focus,
.form-group select:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px rgba(17, 22, 184, 0.08);
}

.field-help {
  margin: 6px 0 0;
  color: var(--color-text-light);
  font-size: 12px;
  line-height: 1.5;
}

.checkbox-label {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-top: 16px;
  color: var(--color-text-muted);
  font-size: 14px;
  font-weight: 850;
  cursor: pointer;
}

.checkbox-label input {
  accent-color: var(--color-primary);
}

.summary-box {
  margin-top: 18px;
  padding: 18px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface-soft);
}

.summary-box h3 {
  margin: 0 0 12px;
  color: var(--color-text);
  font-size: 17px;
  font-weight: 950;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px 16px;
}

.summary-grid p {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin: 0;
  color: var(--color-text-muted);
  font-size: 13px;
}

.summary-grid strong {
  color: var(--color-text-muted);
}

.summary-grid span {
  color: var(--color-text);
  font-weight: 900;
  text-align: right;
}

.error-message {
  margin: 0;
  padding: 13px 14px;
  border: 1px solid #fecaca;
  border-radius: 14px;
  background: #fff5f5;
  color: var(--color-danger);
  font-size: 14px;
  font-weight: 850;
}

.button-row {
  display: flex;
  gap: 10px;
}

.submit-button,
.secondary-button {
  flex: 1;
  min-height: 48px;
  border-radius: 14px;
  font-weight: 950;
  cursor: pointer;
}

.submit-button {
  border: 0;
  background: var(--color-primary);
  color: #fff;
  box-shadow: 0 14px 24px rgba(17, 22, 184, 0.18);
}

.secondary-button {
  border: 1px solid var(--color-border-strong);
  background: #fff;
  color: var(--color-text);
}

.submit-button:disabled,
.secondary-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.signup-guide-panel {
  padding: 34px 28px;
  background: linear-gradient(180deg, #fff 0%, #f8fbff 100%);
}

.signup-guide-panel h2 {
  margin: 0;
  color: var(--color-text);
  font-size: 22px;
  line-height: 1.35;
  font-weight: 950;
}

.signup-guide-panel p {
  margin: 10px 0 22px;
  color: var(--color-text-muted);
  font-size: 14px;
  line-height: 1.65;
}

.signup-guide-panel ul {
  display: grid;
  gap: 14px;
  margin: 0 0 26px;
  padding: 0;
  list-style: none;
}

.signup-guide-panel li {
  display: flex;
  gap: 10px;
  color: var(--color-text-muted);
  font-size: 13px;
  line-height: 1.55;
  font-weight: 800;
}

.signup-guide-panel li span {
  display: grid;
  place-items: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--color-accent-soft);
  color: var(--color-accent);
  font-size: 12px;
  font-weight: 950;
  flex-shrink: 0;
}

.outline-cta {
  display: grid;
  place-items: center;
  min-height: 46px;
  border: 1px solid var(--color-primary);
  border-radius: 14px;
  color: var(--color-primary);
  background: #fff;
  font-weight: 950;
  text-decoration: none;
}

@media (max-width: 1160px) {
  .signup-page {
    grid-template-columns: 1fr;
  }

  .signup-visual-panel {
    display: none;
  }
}

@media (max-width: 840px) {
  .signup-page {
    width: min(100% - 28px, var(--container-width));
    padding: 28px 0 44px;
  }

  .signup-card-body {
    grid-template-columns: 1fr;
  }

  .signup-main-card {
    border-right: 0;
    border-bottom: 1px solid var(--color-border);
  }

  .signup-guide-panel {
    display: none;
  }

  .form-grid.two,
  .summary-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 560px) {
  .signup-main-card {
    padding: 26px 22px;
  }

  .step-item strong {
    display: none;
  }

  .button-row {
    flex-direction: column;
  }
}

/* === 주연: 회원가입 페이지 정리 - 안전 수정본 === */
.signup-page {
  padding: 34px 0 64px !important;
  grid-template-columns: minmax(420px, 0.9fr) minmax(680px, 1.1fr) !important;
  gap: 38px !important;
  align-items: start !important;
}

.signup-visual-panel {
  min-height: 600px;
  padding: 34px;
  border: 1px solid var(--color-border);
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.84);
  box-shadow: var(--shadow-soft);
}

.signup-visual-panel > .eyebrow,
.signup-header > .eyebrow,
.visual-description,
.signup-illustration,
.signup-header > p,
.section-title > p,
.field-help {
  display: none !important;
}

.signup-visual-panel h1 {
  margin: 0 !important;
  font-size: clamp(38px, 4.8vw, 56px) !important;
  line-height: 1.15 !important;
  letter-spacing: -0.065em !important;
}

.signup-visual-panel h1 span {
  color: var(--color-primary);
}

.join-benefit-list {
  margin-top: 38px !important;
  gap: 24px !important;
}

.signup-shell {
  border-radius: 26px !important;
}

.auth-tabs button,
.auth-tabs a {
  min-height: 64px !important;
}

.signup-card-body {
  grid-template-columns: minmax(0, 1fr) 300px !important;
}

.signup-main-card,
.signup-guide-panel {
  padding: 34px 34px !important;
}

.signup-header h1 {
  margin: 0 !important;
  font-size: 32px !important;
}

.step-indicator {
  margin-top: 26px !important;
}

.section-title {
  margin-bottom: 18px !important;
}

.section-title h2 {
  margin-bottom: 0 !important;
}

.signup-guide-panel {
  background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
}

.signup-guide-panel h2 {
  margin-top: 0 !important;
  font-size: 24px !important;
  line-height: 1.35 !important;
  letter-spacing: -0.04em !important;
}

.signup-guide-panel > p,
.signup-guide-panel > ul {
  display: none !important;
}

.signup-guide-panel .outline-cta {
  margin-top: 22px !important;
}

@media (max-width: 1120px) {
  .signup-page {
    grid-template-columns: 1fr !important;
  }

  .signup-visual-panel {
    min-height: 0;
  }
}

@media (max-width: 860px) {
  .signup-card-body {
    grid-template-columns: 1fr !important;
  }
}

@media (max-width: 760px) {
  .signup-page {
    width: min(100% - 28px, var(--container-width)) !important;
    padding-top: 20px !important;
  }

  .form-grid.two,
  .form-grid {
    grid-template-columns: 1fr !important;
  }
}


/* === 주연: 회원가입 페이지 최종 레이아웃/은행목록 재조정 === */
.signup-page {
  width: min(1280px, calc(100% - 48px)) !important;
  padding: 28px 0 64px !important;
  grid-template-columns: 520px minmax(640px, 720px) !important;
  gap: 42px !important;
  align-items: stretch !important;
  justify-content: center !important;
}

.signup-visual-panel {
  width: 100% !important;
  min-height: 620px !important;
  box-sizing: border-box !important;
}

.signup-visual-panel h1 {
  font-size: 48px !important;
  line-height: 1.18 !important;
  letter-spacing: -0.06em !important;
  word-break: keep-all !important;
}

.join-benefit-list {
  margin-top: 42px !important;
}

.signup-shell {
  min-height: 620px !important;
}

.signup-card-body {
  display: grid !important;
  grid-template-columns: 1fr !important;
}

.signup-guide-panel {
  display: none !important;
}

.signup-main-card {
  padding: 38px 46px !important;
}

.signup-header h1 {
  font-size: 34px !important;
}

.form-grid.two {
  grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
  column-gap: 18px !important;
  row-gap: 18px !important;
}

.form-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  gap: 18px !important;
}

.form-group input,
.form-group select {
  min-height: 50px !important;
  font-size: 14px !important;
}

.checkbox-label {
  margin-top: 18px !important;
}

.button-row {
  margin-top: 24px !important;
}

.submit-button {
  min-height: 52px !important;
}

@media (max-width: 1120px) {
  .signup-page {
    grid-template-columns: 1fr !important;
  }

  .signup-visual-panel,
  .signup-shell {
    min-height: 0 !important;
  }
}

@media (max-width: 860px) {
  .signup-main-card {
    padding: 28px 24px !important;
  }

  .form-grid.two,
  .form-grid {
    grid-template-columns: 1fr !important;
  }
}

@media (max-width: 760px) {
  .signup-page {
    width: min(100% - 28px, var(--container-width)) !important;
    padding-top: 18px !important;
  }

  .signup-visual-panel h1 {
    font-size: 40px !important;
  }
}


/* === 주연: 회원가입 금융 정보 select 글씨 잘림 보정 === */
.form-section .form-grid:not(.two) {
  grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
}

.form-section .form-grid:not(.two) .form-group:last-child {
  grid-column: 1 / -1 !important;
}

.form-group select {
  width: 100% !important;
  min-width: 0 !important;
  padding: 0 42px 0 16px !important;
  font-size: 14px !important;
  text-overflow: ellipsis !important;
}

.summary-box {
  margin-top: 20px !important;
}

@media (max-width: 760px) {
  .form-section .form-grid:not(.two),
  .form-grid.two {
    grid-template-columns: 1fr !important;
  }

  .form-section .form-grid:not(.two) .form-group:last-child {
    grid-column: auto !important;
  }
}


/* === 주연: 회원가입 중복확인/비밀번호 검증 UI === */
.label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 8px;
}

.label-row label {
  margin-bottom: 0 !important;
}

.inline-check-message {
  flex: 0 1 auto;
  font-size: 12px;
  font-weight: 900;
  white-space: nowrap;
}

.inline-check-message.success {
  color: #10b981;
}

.inline-check-message.error {
  color: #ef4444;
}

.input-with-button {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 92px;
  gap: 8px;
  align-items: center;
}

.input-with-button input {
  min-width: 0;
}

.check-button {
  height: 50px;
  border: 1px solid var(--color-primary);
  border-radius: 14px;
  background: #fff;
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 950;
  cursor: pointer;
}

.check-button:disabled {
  border-color: var(--color-border-strong);
  color: var(--color-text-muted);
  background: var(--color-surface-soft);
  cursor: not-allowed;
}

.check-button:not(:disabled):hover {
  background: #eef4ff;
}

@media (max-width: 760px) {
  .label-row {
    align-items: flex-start;
    flex-direction: column;
  }

  .input-with-button {
    grid-template-columns: 1fr;
  }

  .check-button {
    width: 100%;
  }

  .inline-check-message {
    white-space: normal;
  }
}

</style>
