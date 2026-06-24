<template>
  <div class="signup-view">
    <section class="signup-card">
      <div class="signup-header">
        <h1>회원가입</h1>
        <p>예적금 추천을 위해 기본 정보와 금융 프로필을 입력해주세요.</p>
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
          <h2>기본 정보</h2>
          <p class="section-description">
            로그인과 사용자 확인에 필요한 정보를 입력해주세요.
          </p>

          <div class="form-group">
            <label for="username">아이디</label>
            <input
              id="username"
              v-model.trim="form.username"
              type="text"
              placeholder="아이디를 입력하세요"
              autocomplete="username"
            >
          </div>

          <div class="form-group">
            <label for="email">이메일</label>
            <input
              id="email"
              v-model.trim="form.email"
              type="email"
              placeholder="이메일을 입력하세요"
              autocomplete="email"
            >
          </div>

          <div class="form-group">
            <label for="password1">비밀번호</label>
            <input
              id="password1"
              v-model="form.password"
              type="password"
              placeholder="비밀번호를 입력하세요"
              autocomplete="new-password"
            >
          </div>

          <div class="form-group">
            <label for="password2">비밀번호 확인</label>
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

          <label class="checkbox-label">
            <input
              v-model="form.personal_info_agree"
              type="checkbox"
            >
            예적금 추천을 위한 개인정보 활용에 동의합니다.
          </label>
        </section>

        <section v-else class="form-section">
          <h2>금융 정보</h2>
          <p class="section-description">
            입력한 금융 정보는 예적금 상품 추천에 활용됩니다.
          </p>

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

          <div class="summary-box">
            <h3>입력한 기본 정보</h3>
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
              <strong>주거래은행</strong>
              <span>{{ form.main_bank || '미입력' }}</span>
            </p>
            <p>
              <strong>거주 지역</strong>
              <span>{{ form.address || '미입력' }}</span>
            </p>
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
            <span v-if="currentStep === 1">다음</span>
            <span v-else>{{ submitting ? '가입 중...' : '회원가입 완료' }}</span>
          </button>
        </div>
      </form>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { signup, getProfileOptions } from '@/api/accounts'

const router = useRouter()

const currentStep = ref(1)
const errorMessage = ref('')
const submitting = ref(false)

const form = ref({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
  age: null,
  monthly_income_range: '',
  monthly_saving_amount: '',
  lump_sum_amount: '',
  main_bank: '',
  address: '',
  personal_info_agree: false,
})

const profileOptions = ref({
  age: [],
  monthly_income_range: [],
  monthly_saving_amount: [],
  lump_sum_amount: [],
  main_bank: [],
  address: [],
})

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

const fetchProfileOptions = async () => {
  try {
    const response = await getProfileOptions()
    profileOptions.value = response.data
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

  if (!form.value.password_confirm) {
    errorMessage.value = '비밀번호 확인을 입력해주세요.'
    return false
  }

  if (form.value.password !== form.value.password_confirm) {
    errorMessage.value = '비밀번호가 일치하지 않습니다.'
    return false
  }

  if (!form.value.age) {
    errorMessage.value = '나이를 선택해주세요.'
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
.signup-view {
  min-height: 100vh;
  padding: 28px;
  background-color: #f6f7f9;
}

.signup-card {
  max-width: 560px;
  margin: 0 auto;
  padding: 28px;
  background-color: #fff;
  border: 1px solid #ddd;
}

.signup-header {
  margin-bottom: 24px;
}

.signup-header h1 {
  margin: 0;
  font-size: 26px;
  color: #111;
}

.signup-header p {
  margin: 8px 0 0;
  color: #666;
  font-size: 14px;
}

.step-indicator {
  display: flex;
  align-items: center;
  margin-bottom: 26px;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #999;
  font-size: 14px;
  font-weight: 800;
}

.step-item span {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background-color: #e5e7eb;
  color: #666;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.step-item.active {
  color: #111;
}

.step-item.active span,
.step-item.done span {
  background-color: #222;
  color: #fff;
}

.step-line {
  flex: 1;
  height: 1px;
  margin: 0 12px;
  background-color: #ddd;
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.form-section {
  padding-top: 18px;
  border-top: 1px solid #eee;
}

.form-section h2 {
  margin: 0 0 8px;
  font-size: 18px;
  color: #111;
}

.section-description {
  margin: 0 0 14px;
  color: #666;
  font-size: 14px;
}

.form-group {
  margin-bottom: 14px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  color: #333;
  font-size: 14px;
  font-weight: 700;
}

.form-group input,
.form-group select {
  width: 100%;
  height: 42px;
  padding: 0 10px;
  border: 1px solid #ccc;
  box-sizing: border-box;
  background-color: #fff;
  font-size: 14px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #333;
  font-size: 14px;
  cursor: pointer;
}

.checkbox-label input {
  width: auto;
  height: auto;
}

.summary-box {
  margin-top: 18px;
  padding: 16px;
  background-color: #fafafa;
  border: 1px solid #eee;
}

.summary-box h3 {
  margin: 0 0 12px;
  font-size: 16px;
  color: #111;
}

.summary-box p {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin: 8px 0;
  color: #555;
  font-size: 14px;
}

.summary-box strong {
  color: #333;
}

.summary-box span {
  text-align: right;
  color: #111;
}

.error-message {
  margin: 0;
  padding: 12px;
  background-color: #fff5f5;
  border: 1px solid #f0caca;
  color: #c0392b;
  font-size: 14px;
}

.button-row {
  display: flex;
  gap: 10px;
}

.submit-button,
.secondary-button {
  flex: 1;
  padding: 12px 16px;
  font-weight: 800;
  cursor: pointer;
}

.submit-button {
  border: 1px solid #222;
  background-color: #222;
  color: #fff;
}

.secondary-button {
  border: 1px solid #aaa;
  background-color: #fff;
  color: #333;
}

.submit-button:disabled,
.secondary-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .signup-view {
    padding: 18px;
  }

  .signup-card {
    padding: 22px;
  }

  .step-item strong {
    display: none;
  }

  .button-row {
    flex-direction: column;
  }
}
</style>