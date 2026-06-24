<template>
  <main class="recommend-page">
    <section class="page-header">
      <p class="eyebrow">Product Recommendation</p>
      <h1>예적금 추천</h1>
      <p>
        사용자의 저축 방식, 희망 기간, 주거래은행, 우대조건 선호도를 바탕으로
        적합한 예금·적금 상품을 추천합니다.
      </p>
    </section>

    <section class="recommend-layout">
      <form class="condition-card" @submit.prevent="handleRecommend">
        <h2>추천 조건</h2>

        <div class="form-group">
          <label for="saving-style">저축 방식</label>
          <select id="saving-style" v-model="form.saving_style">
            <option value="unknown">아직 잘 모르겠어요</option>
            <option value="lump">목돈을 한 번에 넣고 싶어요</option>
            <option value="monthly">매달 조금씩 모으고 싶어요</option>
          </select>
        </div>

        <div class="form-group">
          <label for="product-type">추천 상품 유형</label>
          <select id="product-type" v-model="form.product_type">
            <option value="auto">저축 방식에 맞춰 자동 추천</option>
            <option value="deposit">예금만 추천</option>
            <option value="saving">적금만 추천</option>
          </select>
        </div>

        <div class="form-group">
          <label for="preferred-term">희망 저축 기간</label>
          <select id="preferred-term" v-model="form.preferred_term">
            <option value="any">상관없음</option>
            <option value="1">1개월</option>
            <option value="3">3개월</option>
            <option value="6">6개월</option>
            <option value="12">12개월</option>
            <option value="24">24개월</option>
            <option value="36">36개월</option>
          </select>
        </div>

        <div class="form-group">
          <label for="main-bank">내 주거래은행</label>
          <select id="main-bank" v-model="form.main_bank">
            <option value="없음">아직 없음</option>
            <option value="국민은행">KB국민은행</option>
            <option value="신한은행">신한은행</option>
            <option value="우리은행">우리은행</option>
            <option value="하나은행">하나은행</option>
            <option value="농협은행">NH농협은행</option>
            <option value="광주은행">광주은행</option>
            <option value="기업은행">IBK기업은행</option>
            <option value="카카오뱅크">카카오뱅크</option>
            <option value="케이뱅크">케이뱅크</option>
            <option value="토스뱅크">토스뱅크</option>
            <option value="부산은행">부산은행</option>
            <option value="대구은행">대구은행</option>
            <option value="전북은행">전북은행</option>
            <option value="경남은행">경남은행</option>
            <option value="제주은행">제주은행</option>
          </select>
        </div>

        <div class="form-group">
          <label for="bank-filter">은행 추천 범위</label>
          <select id="bank-filter" v-model="form.bank_filter">
            <option value="all">전체 은행에서 추천</option>
            <option value="main_bank_first">내 주거래은행 우선 추천</option>
            <option value="main_bank_only">내 주거래은행 상품만 보기</option>
          </select>
        </div>

        <div class="form-group">
          <label for="condition-preference">우대조건 선호</label>
          <select id="condition-preference" v-model="form.condition_preference">
            <option value="unknown">잘 모르겠어요</option>
            <option value="simple">복잡한 조건은 싫어요</option>
            <option value="can_meet">조건을 맞춰볼 수 있어요</option>
          </select>
        </div>

        <div class="form-group">
          <label for="join-preference">가입 방식</label>
          <select id="join-preference" v-model="form.join_preference">
            <option value="any">상관없음</option>
            <option value="online">인터넷/스마트폰 가입 선호</option>
            <option value="branch">영업점 방문 가입 선호</option>
          </select>
        </div>

        <button type="submit" class="submit-button" :disabled="loading">
          {{ loading ? '추천 중...' : '추천받기' }}
        </button>

        <button
          type="button"
          class="reset-button"
          @click="handleReset"
        >
          조건 초기화
        </button>

        <p v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </p>
      </form>

      <section class="result-section">
        <div class="result-header">
          <div>
            <p class="eyebrow">Recommended Products</p>
            <h2>추천 결과</h2>
          </div>

          <span v-if="recommendations.length > 0">
            총 {{ recommendations.length }}개 추천
          </span>
        </div>

        <div v-if="!hasSearched" class="empty-box">
          왼쪽에서 조건을 선택한 뒤 추천받기를 눌러주세요.
        </div>

        <div v-else-if="recommendations.length === 0" class="empty-box">
          조건에 맞는 추천 상품이 없습니다.
          은행 필터를 전체 은행으로 바꾸거나 기간 조건을 완화해보세요.
        </div>

        <div v-else class="recommend-list">
          <article
            v-for="item in recommendations"
            :key="`${item.product_id}-${item.save_trm}`"
            class="recommend-card"
          >
            <div class="card-top">
              <div>
                <span class="bank-name">{{ item.bank_name }}</span>
                <h3>{{ item.product_name }}</h3>
              </div>

              <strong class="score">{{ item.score }}점</strong>
            </div>

            <div class="badge-row">
              <span>{{ item.product_type_label }}</span>
              <span>{{ item.save_trm }}개월</span>
              <span>{{ item.condition_label }}</span>
            </div>

            <div class="rate-grid">
              <div>
                <span>기본 금리</span>
                <strong>{{ formatRate(item.base_rate) }}%</strong>
              </div>

              <div>
                <span>최고 금리</span>
                <strong>{{ formatRate(item.max_rate) }}%</strong>
              </div>

              <div>
                <span>조건 반영 금리</span>
                <strong>{{ formatRate(item.effective_rate) }}%</strong>
              </div>
            </div>

            <div class="reason-box">
              <h4>추천 이유</h4>

              <ul>
                <li
                  v-for="reason in item.reasons"
                  :key="reason"
                >
                  {{ reason }}
                </li>
              </ul>
            </div>

            <p class="condition-description">
              {{ item.condition_description }}
            </p>

            <div class="detail-info">
              <p>
                <strong>가입 방법</strong>
                <span>{{ item.join_way || '정보 없음' }}</span>
              </p>

              <p>
                <strong>가입 대상</strong>
                <span>{{ item.join_member || '정보 없음' }}</span>
              </p>
            </div>

            <div class="card-actions">
              <RouterLink
                class="detail-link"
                :to="{
                  name: 'product-detail',
                  params: { id: item.product_id },
                  query: { type: item.product_type }
                }"
              >
                상세보기
              </RouterLink>

              <button
                type="button"
                class="favorite-button"
                @click="handleFavoriteClick"
              >
                관심상품 등록
              </button>
            </div>
          </article>
        </div>
      </section>
    </section>
  </main>
</template>

<script setup>
import { reactive, ref, watch, onMounted, computed } from 'vue'
import { recommendProducts } from '@/api/recommendations'
import { getProfile } from '@/api/accounts'

const loading = ref(false)
const hasSearched = ref(false)
const errorMessage = ref('')
const recommendations = ref([])
const currentUserId = ref(null)

const defaultForm = {
  saving_style: 'unknown',
  product_type: 'auto',
  preferred_term: '12',
  main_bank: '없음',
  bank_filter: 'all',
  condition_preference: 'unknown',
  join_preference: 'online',
}

const form = reactive({ ...defaultForm })

const storageKey = computed(() => {
  if (!currentUserId.value) {
    return null
  }

  return `productRecommendationState:user:${currentUserId.value}`
})

const handleReset = () => {
  Object.assign(form, { ...defaultForm })

  recommendations.value = []
  hasSearched.value = false
  errorMessage.value = ''

  if (storageKey.value) {
    localStorage.removeItem(storageKey.value)
  }
}

const loadCurrentUser = async () => {
  try {
    const response = await getProfile()
    currentUserId.value = response.data.id
  } catch (error) {
    console.error('현재 사용자 정보 조회 실패:', error)
    currentUserId.value = null
  }
}

const restoreRecommendationState = () => {
  if (!storageKey.value) {
    return
  }

  const savedState = localStorage.getItem(storageKey.value)

  if (!savedState) {
    return
  }

  try {
    const parsedState = JSON.parse(savedState)

    if (parsedState.form) {
      Object.assign(form, {
        ...defaultForm,
        ...parsedState.form,
      })
    }

    if (Array.isArray(parsedState.recommendations)) {
      recommendations.value = parsedState.recommendations
    }

    if (typeof parsedState.hasSearched === 'boolean') {
      hasSearched.value = parsedState.hasSearched
    }
  } catch (error) {
    console.error('추천 조건 복원 실패:', error)
    localStorage.removeItem(storageKey.value)
  }
}

const saveRecommendationState = () => {
  if (!storageKey.value) {
    return
  }

  localStorage.setItem(
    storageKey.value,
    JSON.stringify({
      userId: currentUserId.value,
      form: { ...form },
      recommendations: recommendations.value,
      hasSearched: hasSearched.value,
    })
  )
}

onMounted(async () => {
  await loadCurrentUser()
  restoreRecommendationState()
})

watch(
  form,
  () => {
    saveRecommendationState()
  },
  { deep: true }
)

const handleRecommend = async () => {
  loading.value = true
  hasSearched.value = true
  errorMessage.value = ''
  recommendations.value = []

  saveRecommendationState()

  try {
    // 추천 API 내부에서 상품 DB를 조회함
    // 백엔드 목록 API가 DB가 비어 있으면 자동 저장하는 구조이므로
    // 프론트에서는 /save/ API를 직접 호출하지 않음
    const response = await recommendProducts({
      saving_style: form.saving_style,
      product_type: form.product_type,
      preferred_term: form.preferred_term,
      main_bank: form.main_bank,
      bank_filter: form.bank_filter,
      condition_preference: form.condition_preference,
      join_preference: form.join_preference,
    })

    recommendations.value = response.data.recommendations || []

    saveRecommendationState()
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error.response?.data?.message ||
      '추천 상품을 불러오지 못했습니다. recommendations API를 확인해주세요.'

    saveRecommendationState()
  } finally {
    loading.value = false
  }
}

const formatRate = (value) => {
  const numberValue = Number(value)

  if (Number.isNaN(numberValue)) {
    return '0'
  }

  return numberValue.toLocaleString(undefined, {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  })
}

const handleFavoriteClick = () => {
  alert('관심상품 등록 기능은 다음 단계에서 마이페이지와 연결할 예정입니다.')
}
</script>

<style scoped>
.recommend-page {
  max-width: 1180px;
  margin: 0 auto;
  padding: 40px 20px 80px;
}

.page-header {
  margin-bottom: 28px;
}

.eyebrow {
  margin: 0 0 8px;
  color: #2563eb;
  font-size: 14px;
  font-weight: 900;
}

.page-header h1 {
  margin: 0 0 10px;
  color: #111827;
  font-size: 36px;
}

.page-header p {
  margin: 0;
  color: #6b7280;
  line-height: 1.6;
}

.recommend-layout {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 24px;
  align-items: start;
}

.condition-card,
.result-section {
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  background: #ffffff;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
}

.condition-card {
  position: sticky;
  top: 24px;
  padding: 22px;
}

.condition-card h2,
.result-header h2 {
  margin: 0 0 18px;
  color: #111827;
  font-size: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.form-group label {
  color: #4b5563;
  font-size: 13px;
  font-weight: 900;
}

.form-group select {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  padding: 12px 13px;
  background: #ffffff;
  color: #111827;
  font-size: 14px;
}

.submit-button {
  width: 100%;
  border: none;
  border-radius: 12px;
  padding: 14px;
  background: #111827;
  color: #ffffff;
  font-weight: 900;
  cursor: pointer;
}

.submit-button:hover {
  background: #1f2937;
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  margin: 14px 0 0;
  color: #dc2626;
  font-weight: 700;
}

.result-section {
  padding: 24px;
  min-height: 520px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 18px;
}

.result-header span {
  color: #2563eb;
  font-size: 14px;
  font-weight: 900;
}

.empty-box {
  border: 1px dashed #d1d5db;
  border-radius: 16px;
  padding: 40px 20px;
  color: #6b7280;
  text-align: center;
  background: #f9fafb;
}

.recommend-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.recommend-card {
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  padding: 22px;
  background: #ffffff;
}

.card-top {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: flex-start;
  margin-bottom: 14px;
}

.bank-name {
  display: block;
  margin-bottom: 6px;
  color: #2563eb;
  font-size: 13px;
  font-weight: 900;
}

.card-top h3 {
  margin: 0;
  color: #111827;
  font-size: 22px;
}

.score {
  flex-shrink: 0;
  border-radius: 999px;
  padding: 9px 13px;
  background: #eff6ff;
  color: #2563eb;
  font-size: 16px;
}

.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.badge-row span {
  border-radius: 999px;
  padding: 6px 10px;
  background: #f3f4f6;
  color: #374151;
  font-size: 13px;
  font-weight: 800;
}

.rate-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 18px;
}

.rate-grid div {
  border-radius: 14px;
  padding: 14px;
  background: #f9fafb;
}

.rate-grid span {
  display: block;
  margin-bottom: 6px;
  color: #6b7280;
  font-size: 13px;
  font-weight: 800;
}

.rate-grid strong {
  color: #111827;
  font-size: 20px;
}

.reason-box {
  border-radius: 14px;
  padding: 16px;
  background: #111827;
  color: #ffffff;
}

.reason-box h4 {
  margin: 0 0 10px;
  font-size: 15px;
}

.reason-box ul {
  margin: 0;
  padding-left: 20px;
}

.reason-box li {
  margin: 6px 0;
  color: #e5e7eb;
  line-height: 1.5;
}

.condition-description {
  margin: 14px 0 0;
  color: #6b7280;
  line-height: 1.5;
}

.detail-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-top: 16px;
}

.detail-info p {
  margin: 0;
  border-radius: 12px;
  padding: 12px;
  background: #f9fafb;
}

.detail-info strong {
  display: block;
  margin-bottom: 6px;
  color: #4b5563;
  font-size: 13px;
}

.detail-info span {
  color: #111827;
  line-height: 1.5;
}

.card-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 18px;
}

.detail-link,
.favorite-button {
  display: inline-flex;
  align-items: center;
  border: none;
  border-radius: 10px;
  padding: 10px 14px;
  font-weight: 900;
  text-decoration: none;
  cursor: pointer;
}

.detail-link {
  background: #2563eb;
  color: #ffffff;
}

.favorite-button {
  background: #f3f4f6;
  color: #111827;
}

.favorite-button:hover {
  background: #e5e7eb;
}

.reset-button {
  width: 100%;
  margin-top: 10px;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  padding: 13px;
  background: #ffffff;
  color: #374151;
  font-weight: 900;
  cursor: pointer;
}

.reset-button:hover {
  background: #f9fafb;
}

@media (max-width: 960px) {
  .recommend-layout {
    grid-template-columns: 1fr;
  }

  .condition-card {
    position: static;
  }

  .rate-grid,
  .detail-info {
    grid-template-columns: 1fr;
  }
}
</style>