<template>
  <div class="signup-view">
    <section class="signup-card">
      <div class="signup-header">
        <h1>회원가입</h1>
        <p>예적금 추천을 위해 기본 정보와 금융 프로필을 입력해주세요.</p>
      </div>

      <form class="signup-form" @submit.prevent="handleSignup">
        <section class="form-section">
          <h2>기본 정보</h2>

          <div class="form-group">
            <label for="username">아이디</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              placeholder="아이디를 입력하세요"
            >
          </div>

          <div class="form-group">
            <label for="email">이메일</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              placeholder="이메일을 입력하세요"
            >
          </div>

          <div class="form-group">
            <label for="password1">비밀번호</label>
            <input
              id="password1"
              v-model="form.password"
              type="password"
              placeholder="비밀번호를 입력하세요"
            >
          </div>

          <div class="form-group">
            <label for="password2">비밀번호 확인</label>
            <input
              id="password2"
              v-model="form.password_confirm"
              type="password"
              placeholder="비밀번호를 다시 입력하세요"
            >
          </div>
        </section>

        <section class="form-section">
          <h2>금융 프로필</h2>
          <p class="section-description">
            입력한 정보는 예적금 상품 추천에 활용됩니다.
          </p>

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

        <p v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </p>

        <button type="submit" class="submit-button" :disabled="submitting">
          {{ submitting ? '가입 중...' : '회원가입' }}
        </button>
      </form>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { signup, getProfileOptions } from '@/api/accounts'

const router = useRouter()

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

const errorMessage = ref('')
const submitting = ref(false)

const fetchProfileOptions = async () => {
  try {
    const response = await getProfileOptions()
    profileOptions.value = response.data
  } catch (error) {
    console.error(error)
    errorMessage.value = '금융 프로필 선택지를 불러오지 못했습니다.'
  }
}

const validateForm = () => {
  if (!form.value.username || !form.value.password || !form.value.password_confirm) {
    errorMessage.value = '아이디와 비밀번호를 모두 입력해주세요.'
    return false
  }

  if (form.value.password !== form.value.password_confirm) {
    errorMessage.value = '비밀번호가 일치하지 않습니다.'
    return false
  }

  if (!form.value.age) {
    errorMessage.value = '나이를 입력해주세요.'
    return false
  }

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

const handleSignup = async () => {
  errorMessage.value = ''

  if (!validateForm()) {
    return
  }

  submitting.value = true

  try {
    const response = await signup({
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

    console.log('회원가입 응답:', response.data)

    alert('회원가입이 완료되었습니다.')
    router.push({ name: 'login' })
  } catch (error) {
    console.error(error)

    if (error.response?.data) {
      errorMessage.value = JSON.stringify(error.response.data)
      return
    }

    errorMessage.value = '회원가입 중 오류가 발생했습니다.'
  } finally {
    submitting.value = false
  }
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
  max-width: 520px;
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

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.form-section {
  padding-top: 18px;
  border-top: 1px solid #eee;
}

.form-section:first-child {
  padding-top: 0;
  border-top: none;
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

.error-message {
  margin: 0;
  padding: 12px;
  background-color: #fff5f5;
  border: 1px solid #f0caca;
  color: #c0392b;
  font-size: 14px;
}

.submit-button {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #222;
  background-color: #222;
  color: #fff;
  font-weight: 800;
  cursor: pointer;
}

.submit-button:disabled {
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
}
</style>