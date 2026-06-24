<template>
  <main class="recommend-page page-wrap">
    <section class="recommend-hero">
      <div class="hero-copy">
        <h1>맞춤 추천 결과</h1>
        <p>
          마이페이지 금융 프로필과 추천 조건을 바탕으로 실제 저장된 예금·적금 상품 중
          가장 적합한 상품을 분석합니다.
        </p>
      </div>

      <div class="hero-visual" aria-hidden="true">
        <div class="hero-card mini-chart">
          <span></span>
          <span></span>
          <span></span>
          <span></span>
        </div>
        <div class="hero-card piggy">🐷</div>
        <div class="hero-card score-bubble">%</div>
      </div>
    </section>

    <section class="recommend-workspace">
      <form class="condition-card card" @submit.prevent="handleRecommend">
        <div class="condition-title">
          <div>
            <h2>추천 조건</h2>
          </div>
          <button type="button" class="reset-text-button" @click="handleReset">
            초기화 ↻
          </button>
        </div>

        <label class="form-group">
          <span>상품 유형</span>
          <select v-model="form.product_type" class="input-base">
            <option value="auto">전체 상품 추천</option>
            <option value="deposit">예금 - 목돈을 한 번에 맡기기</option>
            <option value="saving">적금 - 매달 조금씩 모으기</option>
          </select>
        </label>

        <label class="form-group">
          <span>희망 저축 기간</span>
          <select v-model="form.preferred_term" class="input-base">
            <option value="any">상관없음</option>
            <option value="1">1개월</option>
            <option value="3">3개월</option>
            <option value="6">6개월</option>
            <option value="12">12개월</option>
            <option value="24">24개월</option>
            <option value="36">36개월</option>
          </select>
        </label>

        <label class="form-group">
          <span>내 주거래은행</span>
          <select v-model="form.main_bank" class="input-base">
            <option value="없음">마이페이지 정보 사용 또는 아직 없음</option>
            <option value="국민은행">국민은행</option>
            <option value="신한은행">신한은행</option>
            <option value="하나은행">하나은행</option>
            <option value="우리은행">우리은행</option>
            <option value="NH농협은행">NH농협은행</option>
            <option value="부산은행">부산은행</option>
            <option value="경남은행">경남은행</option>
            <option value="광주은행">광주은행</option>
            <option value="전북은행">전북은행</option>
            <option value="제주은행">제주은행</option>
            <option value="IBK기업은행">IBK기업은행</option>
            <option value="SC제일은행">SC제일은행</option>
            <option value="iM뱅크">iM뱅크</option>
            <option value="KDB산업은행">KDB산업은행</option>
            <option value="수협은행">수협은행</option>
            <option value="카카오뱅크">카카오뱅크</option>
            <option value="토스뱅크">토스뱅크</option>
            <option value="케이뱅크">케이뱅크</option>
          </select>
        </label>

        <label class="form-group">
          <span>은행 추천 범위</span>
          <select v-model="form.bank_filter" class="input-base">
            <option value="all">전체 은행에서 추천</option>
            <option value="main_bank_first">내 주거래은행 우선 추천</option>
            <option value="main_bank_only">내 주거래은행 상품만 보기</option>
          </select>
        </label>

        <label class="form-group">
          <span>우대조건 선호</span>
          <select v-model="form.condition_preference" class="input-base">
            <option value="unknown">잘 모르겠어요</option>
            <option value="simple">복잡한 조건은 싫어요</option>
            <option value="can_meet">조건을 맞춰볼 수 있어요</option>
          </select>
        </label>

        <label class="form-group">
          <span>가입 방식</span>
          <select v-model="form.join_preference" class="input-base">
            <option value="any">상관없음</option>
            <option value="online">인터넷/스마트폰 가입 선호</option>
            <option value="branch">영업점 방문 가입 선호</option>
          </select>
        </label>

        <div class="profile-used-card">
          <strong>반영되는 프로필</strong>
          <p>{{ profileSummaryText }}</p>
        </div>

        <button type="submit" class="btn-primary recommend-submit" :disabled="loading">
          {{ loading ? '추천 분석 중...' : '맞춤 추천 받기' }}
        </button>
      </form>

      <section class="result-section">
        <p v-if="errorMessage" class="notice-message error">
          {{ errorMessage }}
        </p>

        <div v-if="loading" class="state-card card">
          <div class="loading-icon">⌛</div>
          <h2>추천 결과를 분석하고 있습니다.</h2>
          <p>실제 저장된 금융상품 데이터와 선택 조건을 비교하는 중입니다.</p>
        </div>

        <div v-else-if="!hasSearched" class="state-card card">
          <div class="empty-illustration">📊</div>
          <h2>조건을 선택하면 맞춤 결과가 표시됩니다.</h2>
          <p>
            상품 유형, 기간, 주거래은행, 가입 방식을 선택한 뒤
            맞춤 추천 받기를 눌러주세요.
          </p>
        </div>

        <div v-else-if="recommendations.length === 0" class="state-card card">
          <div class="empty-illustration">🔎</div>
          <h2>조건에 맞는 추천 상품이 없습니다.</h2>
          <p>은행 필터를 전체 은행으로 바꾸거나 기간 조건을 완화해보세요.</p>
        </div>

        <div v-else class="result-dashboard card">
          <div class="product-analysis-grid">
            <section class="recommended-products">
              <div class="section-heading compact-heading">
                <div>
                  <h2>추천 예적금 상품</h2>
                </div>
                <span>{{ visibleRecommendations.length }}개 추천</span>
              </div>

              <div class="product-card-grid recommendation-row-list">
                <article
                  v-for="(item, index) in visibleRecommendations"
                  :key="`${item.product_type}-${item.product_id}-${item.option_id || item.save_trm}`"
                  class="recommend-product-card card recommendation-row-card"
                  :class="{ selected: isSelectedRecommendation(item) }"
                  role="button"
                  tabindex="0"
                  @click="selectRecommendation(item)"
                  @keydown.enter.prevent="selectRecommendation(item)"
                  @keydown.space.prevent="selectRecommendation(item)"
                >
                  <div class="recommend-row-top">
                    <span class="rank-badge">추천 {{ index + 1 }}</span>
                    <div class="recommend-row-actions">
                      <span class="badge" :class="item.product_type === 'deposit' ? 'mint' : 'purple'">
                        {{ item.product_type_label }}
                      </span>
                      <button
                        type="button"
                        class="heart-button"
                        :class="{ active: isFavoriteProduct(item.product_id) }"
                        :disabled="favoriteLoadingProductId === item.product_id"
                        :title="isFavoriteProduct(item.product_id) ? '관심상품 해제' : '관심상품 등록'"
                        @click.stop="handleFavoriteClick(item)"
                      >
                        {{ isFavoriteProduct(item.product_id) ? '♥' : '♡' }}
                      </button>
                    </div>
                  </div>

                  <div class="recommend-row-body">
                    <div class="product-title-block">
                      <h3>{{ item.product_name }}</h3>
                      <p class="bank-line">{{ displayBankName(item.bank_name) }}</p>
                    </div>

                    <div class="product-rate-row">
                      <div>
                        <small>기본 금리</small>
                        <strong>{{ formatRate(item.base_rate) }}%</strong>
                      </div>
                      <div>
                        <small>최고 금리</small>
                        <strong>{{ formatRate(item.max_rate) }}%</strong>
                      </div>
                    </div>

                    <dl class="product-mini-info">
                      <div>
                        <dt>가입 기간</dt>
                        <dd>{{ item.save_trm }}개월</dd>
                      </div>
                      <div>
                        <dt>조건</dt>
                        <dd>{{ item.condition_label }}</dd>
                      </div>
                    </dl>
                  </div>

                  <RouterLink class="detail-button full" :to="getDetailRoute(item)" @click.stop>
                    상품 자세히 보기 ›
                  </RouterLink>
                </article>
              </div>

              <p
                v-if="successMessage"
                class="notice-message result-notice"
                :class="noticeTone"
              >
                {{ successMessage }}
              </p>
            </section>

            <aside class="score-detail-card card">
              <h2>맞춤 점수 상세 분석</h2>
              <p v-if="selectedRecommendation" class="selected-score-product">
                {{ displayBankName(selectedRecommendation.bank_name) }} · {{ selectedRecommendation.product_name }}
              </p>

              <div
                v-for="detail in scoreDetails"
                :key="detail.label"
                class="score-detail-row"
              >
                <div class="score-detail-label">
                  <strong>{{ detail.label }}</strong>
                  <span>{{ detail.description }}</span>
                </div>
                <div class="score-bar-wrap">
                  <span :style="{ width: `${Math.min(100, Math.max(0, (detail.score / detail.max) * 100))}%` }"></span>
                </div>
                <em>{{ detail.score }} / {{ detail.max }}</em>
              </div>

              <div class="total-score-row">
                <strong>총점</strong>
                <span>{{ scoreDetailTotalScore }}<small>/ {{ scoreDetailMaxScore }}</small></span>
              </div>
            </aside>
          </div>
        </div>
      </section>
    </section>
  </main>
</template>

<script setup>
import { reactive, ref, watch, onMounted, computed } from 'vue'
import { recommendProducts } from '@/api/recommendations'
import { getProfile } from '@/api/accounts'
import { getFavoriteProducts, toggleFavoriteProduct } from '@/api/favorites'
import { getBankDisplayName } from '@/constants/bankLogoMap'

const loading = ref(false)
const hasSearched = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const noticeTone = ref('success')
const recommendations = ref([])
const selectedRecommendationKey = ref(null)
const currentUserId = ref(null)
const profileUsed = ref(null)
const favoriteProductIds = ref(new Set())
const favoriteLoadingProductId = ref(null)

const defaultForm = {
  product_type: 'auto',
  preferred_term: '12',
  main_bank: '없음',
  bank_filter: 'all',
  condition_preference: 'unknown',
  join_preference: 'online',
}

const form = reactive({ ...defaultForm })

const getSavingStyleByProductType = () => {
  if (form.product_type === 'deposit') {
    return 'lump'
  }

  if (form.product_type === 'saving') {
    return 'monthly'
  }

  return 'unknown'
}

const getPersistedForm = () => ({
  product_type: form.product_type,
  preferred_term: form.preferred_term,
  main_bank: form.main_bank,
  bank_filter: form.bank_filter,
  condition_preference: form.condition_preference,
  join_preference: form.join_preference,
})

const storageKey = computed(() => {
  if (!currentUserId.value) {
    return null
  }

  return `productRecommendationState:user:${currentUserId.value}`
})

const topRecommendation = computed(() => recommendations.value[0] || null)

const selectedRecommendation = computed(() => {
  if (recommendations.value.length === 0) {
    return null
  }

  const selectedItem = recommendations.value.find((item) => getRecommendationKey(item) === selectedRecommendationKey.value)

  return selectedItem || recommendations.value[0]
})

const visibleRecommendations = computed(() => recommendations.value.slice(0, 3))

const recommendedBankName = computed(() => {
  if (topRecommendation.value?.bank_name) {
    return topRecommendation.value.bank_name
  }

  if (profileUsed.value?.main_bank) {
    return profileUsed.value.main_bank
  }

  return form.main_bank && form.main_bank !== '없음' ? form.main_bank : '추천 대기 중'
})

const scoreDetailTotalScore = computed(() => {
  return scoreDetails.value.reduce((total, detail) => total + Number(detail.score || 0), 0)
})

const scoreDetailMaxScore = computed(() => {
  return scoreDetails.value.reduce((total, detail) => total + Number(detail.max || 20), 0) || 100
})

const compatibilityScore = computed(() => {
  if (!topRecommendation.value) {
    return 0
  }

  return Math.min(scoreDetailMaxScore.value, Math.max(0, Math.round(scoreDetailTotalScore.value)))
})

const scoreRingStyle = computed(() => ({
  '--score-degree': `${compatibilityScore.value * 3.6}deg`,
}))

const scoreComment = computed(() => {
  if (compatibilityScore.value >= 90) {
    return '조건과 매우 잘 맞는 상품입니다.'
  }

  if (compatibilityScore.value >= 75) {
    return '주요 조건과 대체로 잘 맞습니다.'
  }

  if (compatibilityScore.value >= 60) {
    return '조건 일부가 일치하는 상품입니다.'
  }

  return '조건을 완화하면 더 좋은 추천을 받을 수 있습니다.'
})

const bankSummaryText = computed(() => {
  if (!topRecommendation.value) {
    return '추천 결과를 기다리고 있습니다.'
  }

  return `${topRecommendation.value.product_type_label} 상품 기준 ${formatRate(topRecommendation.value.max_rate)}% 최고 금리`
})

const profileSummaryText = computed(() => {
  if (!profileUsed.value) {
    return '로그인 사용자의 마이페이지 프로필이 있으면 함께 반영됩니다.'
  }

  const parts = []

  if (profileUsed.value.age) {
    parts.push(`${profileUsed.value.age}세`)
  }

  if (profileUsed.value.gender && profileUsed.value.gender !== 'unknown') {
    parts.push(getGenderLabel(profileUsed.value.gender))
  }

  if (profileUsed.value.main_bank) {
    parts.push(`주거래은행 ${profileUsed.value.main_bank}`)
  }

  if (profileUsed.value.monthly_saving_amount) {
    parts.push(`저축 가능 금액 ${getSavingAmountLabel(profileUsed.value.monthly_saving_amount)}`)
  }

  if (profileUsed.value.lump_sum_amount) {
    parts.push(`목돈 ${getLumpSumLabel(profileUsed.value.lump_sum_amount)}`)
  }

  return parts.length > 0 ? parts.join(' · ') : '마이페이지 프로필 정보가 아직 충분하지 않습니다.'
})

const reasonChips = computed(() => {
  if (!topRecommendation.value) {
    return []
  }

  const chips = []
  const item = topRecommendation.value

  if (Number(item.max_rate) > 0) {
    chips.push({ icon: '%', label: `최고 ${formatRate(item.max_rate)}% 금리` })
  }

  if (item.save_trm) {
    chips.push({ icon: '📅', label: `${item.save_trm}개월 기간` })
  }

  if (item.join_way) {
    chips.push({ icon: '📱', label: getJoinWaySummary(item.join_way) })
  }

  if (item.condition_label) {
    chips.push({ icon: '✅', label: item.condition_label })
  }

  if (item.gender_eligibility_rule) {
    chips.push({ icon: '👤', label: item.gender_eligibility_rule })
  }

  if (item.bank_name) {
    chips.push({ icon: '🏦', label: item.bank_name })
  }

  return chips.slice(0, 5)
})

const topReasons = computed(() => {
  const reasons = topRecommendation.value?.reasons || []

  if (reasons.length > 0) {
    return reasons
  }

  return ['입력한 조건과 금리 정보를 종합해 추천한 상품입니다.']
})

const scoreDetails = computed(() => {
  const item = selectedRecommendation.value

  if (!item) {
    return []
  }

  const maxRate = Number(item.max_rate || 0)
  const baseRate = Number(item.base_rate || 0)
  const termMatched = form.preferred_term === 'any' || Number(form.preferred_term) === Number(item.save_trm)
  const joinWay = String(item.join_way || '')
  const conditionLabel = String(item.condition_label || '')
  const selectedMainBank = form.main_bank !== '없음' ? form.main_bank : profileUsed.value?.main_bank
  const normalizedSelectedMainBank = String(selectedMainBank || '')
    .replace('KB', '')
    .replace('KEB', '')
    .replace('NH', '')
    .replace('IBK', '')
    .replace('KDB', '')
    .replace('iM', '')
    .replace('뱅크', '은행')

  const bankMatched = selectedMainBank && item.bank_name?.includes(normalizedSelectedMainBank)

  return [
    {
      label: '금리',
      description: '기본금리와 최고금리를 함께 반영했습니다.',
      max: 20,
      score: clampScore(Math.round(maxRate * 3 + baseRate * 1.5)),
    },
    {
      label: '기간',
      description: termMatched ? '희망 기간과 일치합니다.' : '희망 기간과 다소 차이가 있습니다.',
      max: 20,
      score: termMatched ? 20 : 12,
    },
    {
      label: '가입 편의성',
      description: joinWay ? getJoinWaySummary(joinWay) : '가입 방식 정보가 제한적입니다.',
      max: 20,
      score: joinWay.includes('인터넷') || joinWay.includes('스마트폰') || joinWay.includes('모바일') ? 18 : 12,
    },
    {
      label: '우대조건',
      description: conditionLabel || '우대조건 확인이 필요합니다.',
      max: 20,
      score: conditionLabel.includes('단순') ? 19 : conditionLabel.includes('활용') ? 17 : 13,
    },
    {
      label: '프로필 반영',
      description: bankMatched ? '주거래은행 조건이 반영되었습니다.' : '프로필과 조건을 보조 반영했습니다.',
      max: 20,
      score: bankMatched ? 18 : profileUsed.value ? 14 : 10,
    },
  ]
})

const clampScore = (value) => Math.min(20, Math.max(0, value))

const getGenderLabel = (value) => {
  const labels = {
    male: '남성',
    female: '여성',
    unknown: '성별 미입력',
  }

  return labels[value] || value
}

const getSavingAmountLabel = (value) => {
  const labels = {
    under_10: '10만원 미만',
    '10_30': '10만원 이상 30만원 미만',
    '30_50': '30만원 이상 50만원 미만',
    '50_100': '50만원 이상 100만원 미만',
    over_100: '100만원 이상',
  }

  return labels[value] || value
}

const getLumpSumLabel = (value) => {
  const labels = {
    none: '없음',
    under_100: '100만원 미만',
    '100_500': '100만원 이상 500만원 미만',
    '500_1000': '500만원 이상 1000만원 미만',
    '1000_3000': '1000만원 이상 3000만원 미만',
    over_3000: '3000만원 이상',
  }

  return labels[value] || value
}

const getJoinWaySummary = (joinWay) => {
  const text = String(joinWay || '')

  if (text.includes('인터넷') || text.includes('스마트폰') || text.includes('모바일')) {
    return '비대면 가입 가능'
  }

  if (text.includes('영업점') || text.includes('방문')) {
    return '영업점 가입 가능'
  }

  return text.slice(0, 18)
}

const getDetailRoute = (item) => ({
  name: 'product-detail',
  params: { id: item.product_id },
  query: { type: item.product_type },
})

const handleReset = () => {
  Object.assign(form, { ...defaultForm })
  delete form.saving_style

  recommendations.value = []
  selectedRecommendationKey.value = null
  hasSearched.value = false
  errorMessage.value = ''
  successMessage.value = ''
  noticeTone.value = 'success'

  if (storageKey.value) {
    localStorage.removeItem(storageKey.value)
  }
}

const loadCurrentUser = async () => {
  try {
    const response = await getProfile()
    currentUserId.value = response.data.id
    profileUsed.value = response.data.profile || null
  } catch (error) {
    console.error('현재 사용자 정보 조회 실패:', error)
    currentUserId.value = null
    profileUsed.value = null
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
        product_type: parsedState.form.product_type || defaultForm.product_type,
        preferred_term: parsedState.form.preferred_term || defaultForm.preferred_term,
        main_bank: parsedState.form.main_bank || defaultForm.main_bank,
        bank_filter: parsedState.form.bank_filter || defaultForm.bank_filter,
        condition_preference:
          parsedState.form.condition_preference || defaultForm.condition_preference,
        join_preference: parsedState.form.join_preference || defaultForm.join_preference,
      })
      delete form.saving_style
    }

    if (Array.isArray(parsedState.recommendations)) {
      recommendations.value = parsedState.recommendations
      selectedRecommendationKey.value = recommendations.value[0]
        ? getRecommendationKey(recommendations.value[0])
        : null
    }

    if (parsedState.profileUsed) {
      profileUsed.value = parsedState.profileUsed
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
      form: getPersistedForm(),
      recommendations: recommendations.value,
      profileUsed: profileUsed.value,
      hasSearched: hasSearched.value,
    })
  )
}

const extractFavoriteProductId = (favorite) => {
  if (favorite.product_id) {
    return favorite.product_id
  }

  if (typeof favorite.product === 'number') {
    return favorite.product
  }

  if (favorite.product?.id) {
    return favorite.product.id
  }

  if (favorite.product?.product_id) {
    return favorite.product.product_id
  }

  return null
}

const loadFavoriteProducts = async () => {
  const token = localStorage.getItem('token')

  if (!token) {
    favoriteProductIds.value = new Set()
    return
  }

  try {
    const response = await getFavoriteProducts()
    const favorites = response.data || []

    favoriteProductIds.value = new Set(
      favorites
        .map((favorite) => extractFavoriteProductId(favorite))
        .filter((productId) => productId !== null)
    )

    applyFavoriteStateToRecommendations()
  } catch (error) {
    console.error('관심상품 목록 조회 실패:', error)
    favoriteProductIds.value = new Set()
  }
}

const applyFavoriteStateToRecommendations = () => {
  recommendations.value = recommendations.value.map((item) => ({
    ...item,
    is_favorite: favoriteProductIds.value.has(item.product_id),
  }))

  saveRecommendationState()
}

const isFavoriteProduct = (productId) => {
  return favoriteProductIds.value.has(productId)
}

const handleRecommend = async () => {
  loading.value = true
  hasSearched.value = true
  errorMessage.value = ''
  successMessage.value = ''
  noticeTone.value = 'success'
  recommendations.value = []
  selectedRecommendationKey.value = null

  saveRecommendationState()

  try {
    const response = await recommendProducts({
      saving_style: getSavingStyleByProductType(),
      product_type: form.product_type,
      preferred_term: form.preferred_term,
      main_bank: form.main_bank,
      bank_filter: form.bank_filter,
      condition_preference: form.condition_preference,
      join_preference: form.join_preference,
    })

    recommendations.value = response.data.recommendations || []
    selectedRecommendationKey.value = recommendations.value[0] ? getRecommendationKey(recommendations.value[0]) : null
    profileUsed.value = response.data.profile_used || profileUsed.value
    applyFavoriteStateToRecommendations()

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

const handleFavoriteClick = async (item) => {
  const token = localStorage.getItem('token')

  errorMessage.value = ''
  successMessage.value = ''
  noticeTone.value = 'success'

  if (!token) {
    errorMessage.value = '로그인 후 관심상품을 등록할 수 있습니다.'
    return
  }

  favoriteLoadingProductId.value = item.product_id

  try {
    const response = await toggleFavoriteProduct(item.product_id)
    const isFavorite = response.data.is_favorite

    const nextFavoriteIds = new Set(favoriteProductIds.value)

    if (isFavorite) {
      nextFavoriteIds.add(item.product_id)
      successMessage.value = '관심상품에 등록되었습니다.'
      noticeTone.value = 'success'
    } else {
      nextFavoriteIds.delete(item.product_id)
      successMessage.value = '관심상품에서 해제되었습니다.'
      noticeTone.value = 'danger'
    }

    favoriteProductIds.value = nextFavoriteIds

    recommendations.value = recommendations.value.map((recommendation) => {
      if (recommendation.product_id !== item.product_id) {
        return recommendation
      }

      return {
        ...recommendation,
        is_favorite: isFavorite,
      }
    })

    saveRecommendationState()
  } catch (error) {
    console.error('관심상품 처리 실패:', error)

    errorMessage.value =
      error.response?.data?.message ||
      '관심상품 처리 중 문제가 발생했습니다.'
  } finally {
    favoriteLoadingProductId.value = null
  }
}


const getRecommendationKey = (item) => {
  if (!item) {
    return ''
  }

  return `${item.product_type}-${item.product_id}-${item.option_id || item.save_trm || 'default'}`
}

const selectRecommendation = (item) => {
  selectedRecommendationKey.value = getRecommendationKey(item)
}

const isSelectedRecommendation = (item) => {
  return getRecommendationKey(item) === getRecommendationKey(selectedRecommendation.value)
}

const displayBankName = (bankName) => getBankDisplayName(bankName)

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

onMounted(async () => {
  await loadCurrentUser()
  restoreRecommendationState()
  await loadFavoriteProducts()
})

watch(
  form,
  () => {
    saveRecommendationState()
  },
  { deep: true }
)
</script>

<!-- FINAL OVERRIDE: 추천 카드 가로형 행 배치 보정 -->
<!-- FINAL OVERRIDE: 맞춤추천 결과 카드 가독성 재정리 -->
<style scoped>
/* FINAL FIX: 맞춤추천 카드 행형 정리 + 알림 위치/은행명 표기 */
.recommend-page {
  padding-top: 18px !important;
}

.recommend-hero {
  margin-bottom: 20px !important;
}

.result-dashboard.card {
  padding: 20px !important;
}

.product-analysis-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 260px;
  gap: 14px;
  align-items: start;
}

.score-detail-card {
  width: 100% !important;
  padding: 18px !important;
  border-radius: 20px !important;
}

.score-detail-card h2 {
  font-size: 18px !important;
}

.selected-score-product {
  margin-bottom: 10px !important;
  font-size: 12px !important;
}

.section-heading.compact-heading {
  margin-bottom: 12px !important;
}

.section-heading.compact-heading h2 {
  margin: 0 !important;
  font-size: 22px !important;
}

.recommendation-row-list {
  display: grid !important;
  grid-template-columns: 1fr !important;
  gap: 14px !important;
}

.recommendation-row-card,
.recommend-product-card.recommendation-row-card,
.recommend-product-card.recommendation-row-card:nth-child(3) {
  display: block !important;
  min-height: 0 !important;
  padding: 18px 20px !important;
  border-radius: 20px !important;
  overflow: hidden !important;
}

.recommend-row-top {
  display: flex !important;
  justify-content: space-between !important;
  align-items: flex-start !important;
  gap: 16px !important;
  margin-bottom: 12px !important;
}

.recommend-row-actions {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  flex: 0 0 auto !important;
}

.recommend-row-actions .badge {
  margin: 0 !important;
}

.rank-badge {
  align-self: flex-start !important;
}

.recommend-row-body {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  align-items: start;
}

.product-title-block {
  grid-column: 1 / -1;
  min-width: 0;
}

.product-title-block h3,
.recommend-product-card h3 {
  display: block;
  min-height: 0;
  margin: 0 0 4px;
  color: var(--color-text);
  font-size: 18px;
  line-height: 1.28;
  font-weight: 950;
  letter-spacing: -0.045em;
  writing-mode: horizontal-tb;
  white-space: normal;
  word-break: keep-all;
  overflow-wrap: anywhere;
  text-orientation: mixed;
}

.product-title-block .bank-line,
.bank-line {
  margin: 0 !important;
  font-size: 13px !important;
}

.recommendation-row-card .product-rate-row {
  grid-column: 1 / span 2;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin: 0;
  min-width: 0;
}

.recommendation-row-card .product-rate-row > div {
  padding: 12px 10px !important;
  border-radius: 14px !important;
}

.recommendation-row-card .product-rate-row strong {
  font-size: 18px !important;
}

.recommendation-row-card .product-mini-info {
  grid-column: 3 / span 2;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin: 0;
  min-width: 0;
}

.recommendation-row-card .product-mini-info div {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
  min-width: 0;
  padding: 12px 10px;
  border: 0;
  border-radius: 14px;
  background: var(--color-surface-soft);
}

.recommendation-row-card .detail-button.full {
  width: 100%;
  margin-top: 12px;
}

.result-notice.notice-message {
  margin: 14px 0 0 !important;
}

@media (max-width: 1260px) {
  .product-analysis-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 260px;
  gap: 14px;
  align-items: start;
}

  .score-detail-card {
    position: static !important;
  }
}

@media (max-width: 900px) {
  .recommend-row-body {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  align-items: start;
}
}
</style>

<style scoped>
.recommend-page {
  width: min(var(--container-width, 1360px), calc(100% - 48px));
  margin: 0 auto;
  padding: 18px 0 72px;
}

.recommend-hero {
  margin: 0 0 22px;
}

.hero-copy h1 {
  margin: 0;
  color: var(--color-text);
  font-size: clamp(38px, 4vw, 52px);
  line-height: 1.08;
  font-weight: 950;
  letter-spacing: -0.07em;
}

.hero-copy p,
.hero-visual,
.eyebrow,
.eyebrow.small {
  display: none;
}

.recommend-workspace {
  display: grid;
  grid-template-columns: 330px minmax(0, 1fr);
  gap: 22px;
  align-items: start;
}

.condition-card {
  position: sticky;
  top: calc(var(--header-height, 64px) + 18px);
  padding: 22px;
  border-radius: 22px;
  box-shadow: 0 18px 44px rgba(15, 27, 61, 0.07);
}

.condition-title {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  align-items: flex-start;
  padding-bottom: 14px;
  margin-bottom: 16px;
  border-bottom: 1px solid var(--color-border);
}

.condition-title h2 {
  margin: 0;
  color: var(--color-text);
  font-size: 24px;
  font-weight: 950;
  letter-spacing: -0.04em;
}

.reset-text-button {
  border: 0;
  background: transparent;
  color: var(--color-primary);
  font-weight: 950;
  cursor: pointer;
}

.form-group {
  display: grid;
  gap: 8px;
  margin-bottom: 13px;
}

.form-group span {
  color: var(--color-text);
  font-size: 13px;
  font-weight: 950;
}

.input-base,
.condition-card select {
  min-height: 45px;
  border-radius: 13px;
}

.profile-used-card {
  margin: 16px 0;
  padding: 14px 15px;
  border: 1px solid var(--color-border);
  border-radius: 16px;
  background: var(--color-surface-soft);
}

.profile-used-card strong {
  display: block;
  color: var(--color-text);
  font-size: 14px;
  font-weight: 950;
}

.profile-used-card p {
  margin: 5px 0 0;
  color: var(--color-text-muted);
  font-size: 13px;
  line-height: 1.55;
}

.recommend-submit {
  width: 100%;
  min-height: 48px;
  border-radius: 13px;
}

.result-section {
  min-width: 0;
}

.notice-message {
  margin: 0 0 14px;
  padding: 13px 16px;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 950;
}

.notice-message.error,
.notice-message.danger {
  border: 1px solid #fecaca;
  background: #fff5f5;
  color: #dc2626;
}

.notice-message.success {
  border: 1px solid #bbf7d0;
  background: #f0fdf4;
  color: #15803d;
}

.result-notice {
  margin: 14px 0 0;
}

.state-card {
  min-height: 520px;
  display: grid;
  place-items: center;
  align-content: center;
  padding: 40px;
  text-align: center;
  border-radius: 22px;
}

.state-card h2 {
  margin: 12px 0 8px;
  color: var(--color-text);
  font-size: 26px;
  font-weight: 950;
}

.state-card p {
  max-width: 520px;
  margin: 0;
  color: var(--color-text-muted);
}

.empty-illustration,
.loading-icon {
  display: grid;
  place-items: center;
  width: 82px;
  height: 82px;
  border-radius: 28px;
  background: var(--color-primary-soft);
  font-size: 42px;
}

.result-dashboard {
  min-width: 0;
}

.result-dashboard.card {
  min-height: 650px;
  padding: 20px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.88);
  box-shadow: 0 20px 48px rgba(15, 27, 61, 0.08);
}

.product-analysis-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 260px;
  gap: 14px;
  align-items: start;
}

.recommended-products {
  min-width: 0;
}

.section-heading.compact-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  min-height: 38px;
  margin: 0 0 12px;
}

.section-heading.compact-heading h2 {
  margin: 0;
  color: var(--color-text);
  font-size: 22px;
  line-height: 1.2;
  font-weight: 950;
  letter-spacing: -0.045em;
}

.section-heading.compact-heading p {
  display: none;
}

.section-heading.compact-heading > span {
  flex: 0 0 auto;
  padding: 8px 12px;
  border-radius: 999px;
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 950;
  white-space: nowrap;
}

.product-card-grid,
.recommendation-row-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
}

.recommend-product-card,
.recommend-product-card:nth-child(3),
.recommendation-row-card {
  display: block;
  min-width: 0;
  min-height: 0;
  padding: 16px 18px;
  overflow: hidden;
  border-radius: 20px;
  background: #fff;
  cursor: pointer;
  transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
}

.recommend-product-card:hover,
.recommend-product-card.selected {
  border-color: rgba(0, 30, 190, 0.32);
  box-shadow: 0 16px 34px rgba(0, 30, 190, 0.1);
  transform: translateY(-1px);
}

.recommend-row-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 12px;
}

.recommend-row-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 0 0 auto;
}

.rank-badge {
  display: inline-flex;
  align-items: center;
  min-height: 26px;
  padding: 0 9px;
  border-radius: 999px;
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-size: 11px;
  font-weight: 950;
  white-space: nowrap;
}

.recommend-product-card.selected .rank-badge::after {
  content: '';
}

.badge {
  display: inline-flex;
  align-items: center;
  min-height: 25px;
  padding: 0 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 950;
  white-space: nowrap;
}

.badge.mint {
  background: #dcfce7;
  color: #059669;
}

.badge.purple {
  background: #f1e6ff;
  color: #7c3aed;
}

.heart-button {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  background: #fff;
  color: #98a4bc;
  font-size: 18px;
  cursor: pointer;
}

.heart-button.active {
  border-color: #fecdd3;
  background: #fff1f2;
  color: var(--color-danger);
}

.recommend-row-body {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  align-items: start;
}

.product-title-block {
  grid-column: 1 / -1;
  min-width: 0;
}

.product-title-block h3,
.recommend-product-card h3 {
  display: block;
  min-height: 0;
  margin: 0 0 4px;
  color: var(--color-text);
  font-size: 18px;
  line-height: 1.28;
  font-weight: 950;
  letter-spacing: -0.045em;
  writing-mode: horizontal-tb;
  white-space: normal;
  word-break: keep-all;
  overflow-wrap: anywhere;
  text-orientation: mixed;
}

.product-title-block .bank-line,
.bank-line {
  display: block;
  margin: 0;
  color: var(--color-text-muted);
  font-size: 13px;
  line-height: 1.35;
  writing-mode: horizontal-tb;
  white-space: normal;
  word-break: keep-all;
  overflow-wrap: anywhere;
}

.recommend-reason {
  display: none;
}

.product-rate-row {
  grid-column: 1 / span 2;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin: 0;
  min-width: 0;
}

.product-rate-row > div {
  min-width: 0;
  padding: 12px 10px;
  border-radius: 14px;
  background: var(--color-surface-soft);
}

.product-rate-row small {
  display: block;
  margin-bottom: 4px;
  color: var(--color-text-light);
  font-size: 11px;
  font-weight: 900;
  white-space: nowrap;
}

.product-rate-row strong {
  display: block;
  color: var(--color-primary);
  font-size: 18px;
  line-height: 1.15;
  font-weight: 950;
  white-space: nowrap;
}

.product-mini-info {
  grid-column: 3 / span 2;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin: 0;
  min-width: 0;
}

.product-mini-info div {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
  min-width: 0;
  padding: 12px 10px;
  border: 0;
  border-radius: 14px;
  background: var(--color-surface-soft);
}

.product-mini-info dt {
  flex: 0 0 auto;
  color: var(--color-text-light);
  font-size: 11px;
  font-weight: 900;
  white-space: nowrap;
}

.product-mini-info dd {
  min-width: 0;
  margin: 0;
  color: var(--color-text);
  font-size: 14px;
  font-weight: 950;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.detail-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  padding: 0 14px;
  border: 1px solid var(--color-primary);
  border-radius: 12px;
  background: #fff;
  color: var(--color-primary);
  font-size: 14px;
  font-weight: 950;
  text-decoration: none;
}

.detail-button.full {
  width: 100%;
  margin-top: 12px;
}

.score-detail-card {
  width: 100%;
  padding: 18px;
  border-radius: 20px;
  background: #fff;
}

.score-detail-card h2 {
  margin: 0 0 8px;
  color: var(--color-text);
  font-size: 18px;
  font-weight: 950;
}

.selected-score-product {
  margin: 0 0 10px;
  color: var(--color-text-muted);
  font-size: 12px;
  line-height: 1.45;
  font-weight: 800;
  word-break: keep-all;
  overflow-wrap: anywhere;
}

.score-detail-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 6px;
  padding: 10px 0;
  border-bottom: 1px solid var(--color-border);
}

.score-detail-label {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.score-detail-label strong {
  color: var(--color-text);
  font-size: 13px;
  font-weight: 950;
}

.score-detail-label span {
  max-width: 150px;
  color: var(--color-text-muted);
  font-size: 11px;
  line-height: 1.4;
  text-align: right;
}

.score-bar-wrap {
  height: 6px;
  overflow: hidden;
  border-radius: 999px;
  background: #e9eef8;
}

.score-bar-wrap span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: var(--color-accent);
}

.score-detail-row em {
  justify-self: end;
  color: var(--color-accent);
  font-size: 12px;
  font-style: normal;
  font-weight: 950;
}

.total-score-row {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 12px;
  padding-top: 12px;
  margin-top: 8px;
}

.total-score-row strong {
  color: var(--color-text);
  font-size: 17px;
  font-weight: 950;
}

.total-score-row span {
  color: var(--color-primary);
  font-size: 31px;
  font-weight: 950;
  letter-spacing: -0.05em;
}

.total-score-row small {
  color: var(--color-text-muted);
  font-size: 15px;
}

@media (max-width: 1260px) {
  .recommend-workspace,
  .product-analysis-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 260px;
  gap: 14px;
  align-items: start;
}

  .condition-card,
  .score-detail-card {
    position: static;
  }
}

@media (max-width: 900px) {
  .recommend-row-body {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  align-items: start;
}
}
</style>
