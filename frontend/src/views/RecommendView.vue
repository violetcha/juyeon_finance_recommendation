<template>
  <main class="recommend-page page-wrap">
    <section class="recommend-hero">
      <div class="hero-copy">
        <span class="eyebrow">PERSONAL RECOMMENDATION</span>
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
            <span class="eyebrow small">RECOMMEND SETTINGS</span>
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

        <p v-if="successMessage" class="notice-message success">
          {{ successMessage }}
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

        <div v-else class="result-dashboard">
          <div class="product-analysis-grid">
            <section class="recommended-products">
              <div class="section-heading compact-heading">
                <div>
                  <h2>추천 예적금 상품</h2>
                  <p>추천 API가 반환한 실제 추천 상품 전체입니다.</p>
                </div>
                <span>{{ visibleRecommendations.length }}개 추천</span>
              </div>

              <div class="product-card-grid">
                <article
                  v-for="(item, index) in visibleRecommendations"
                  :key="`${item.product_type}-${item.product_id}-${item.option_id || item.save_trm}`"
                  class="recommend-product-card card"
                  :class="{ selected: isSelectedRecommendation(item) }"
                  role="button"
                  tabindex="0"
                  @click="selectRecommendation(item)"
                  @keydown.enter.prevent="selectRecommendation(item)"
                  @keydown.space.prevent="selectRecommendation(item)"
                >
                  <div class="product-card-top">
                    <span class="rank-badge">추천 {{ index + 1 }}</span>
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

                  <span class="badge" :class="item.product_type === 'deposit' ? 'mint' : 'purple'">
                    {{ item.product_type_label }}
                  </span>

                  <h3>{{ item.product_name }}</h3>
                  <p class="bank-line">{{ item.bank_name }}</p>

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

                  <p class="recommend-reason">
                    {{ item.reasons?.[0] || '입력한 조건과 금리 정보를 종합해 추천한 상품입니다.' }}
                  </p>

                  <RouterLink class="detail-button full" :to="getDetailRoute(item)" @click.stop>
                    상품 자세히 보기 ›
                  </RouterLink>
                </article>
              </div>
            </section>

            <aside class="score-detail-card card">
              <h2>맞춤 점수 상세 분석</h2>
              <p v-if="selectedRecommendation" class="selected-score-product">
                {{ selectedRecommendation.bank_name }} · {{ selectedRecommendation.product_name }}
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

const loading = ref(false)
const hasSearched = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
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

const visibleRecommendations = computed(() => recommendations.value)

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
  const bankMatched = selectedMainBank && item.bank_name?.includes(selectedMainBank.replace('KB', '').replace('NH', ''))

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
    } else {
      nextFavoriteIds.delete(item.product_id)
      successMessage.value = '관심상품에서 해제되었습니다.'
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

<style scoped>
.recommend-page {
  padding-top: 34px;
}

.recommend-hero {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 28px;
  align-items: center;
  margin-bottom: 24px;
}

.eyebrow {
  display: inline-flex;
  margin-bottom: 8px;
  color: var(--color-primary);
  font-size: 12px;
  font-weight: 950;
  letter-spacing: 0.12em;
}

.eyebrow.small {
  margin-bottom: 4px;
  font-size: 11px;
}

.hero-copy h1 {
  margin: 0;
  color: var(--color-text);
  font-size: clamp(36px, 4vw, 52px);
  line-height: 1.12;
  font-weight: 950;
  letter-spacing: -0.06em;
}

.hero-copy p {
  max-width: 720px;
  margin: 14px 0 0;
  color: var(--color-text-muted);
  font-size: 17px;
}

.hero-visual {
  position: relative;
  min-height: 170px;
}

.hero-card {
  position: absolute;
  display: grid;
  place-items: center;
  border: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.92);
  box-shadow: var(--shadow-soft);
}

.piggy {
  left: 110px;
  top: 54px;
  width: 88px;
  height: 88px;
  border-radius: 32px;
  background: var(--color-accent-soft);
  font-size: 44px;
}

.score-bubble {
  right: 28px;
  top: 42px;
  width: 70px;
  height: 70px;
  border-radius: 26px;
  color: var(--color-primary);
  font-size: 32px;
  font-weight: 950;
}

.mini-chart {
  left: 0;
  top: 12px;
  width: 130px;
  height: 100px;
  align-items: end;
  grid-template-columns: repeat(4, 1fr);
  gap: 9px;
  padding: 18px;
  border-radius: 26px;
}

.mini-chart span {
  width: 14px;
  border-radius: 999px;
  background: linear-gradient(180deg, #6875ff, var(--color-primary));
}

.mini-chart span:nth-child(1) { height: 28px; }
.mini-chart span:nth-child(2) { height: 48px; }
.mini-chart span:nth-child(3) { height: 36px; }
.mini-chart span:nth-child(4) { height: 66px; background: linear-gradient(180deg, #3ee5ca, var(--color-accent)); }

.recommend-workspace {
  display: grid;
  grid-template-columns: 330px minmax(0, 1fr);
  gap: 20px;
  align-items: start;
}

.condition-card {
  position: sticky;
  top: calc(var(--header-height) + 18px);
  padding: 22px;
}

.condition-title {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  align-items: flex-start;
  margin-bottom: 18px;
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
}

.form-group {
  display: grid;
  gap: 8px;
  margin-bottom: 14px;
}

.form-group span {
  color: var(--color-text);
  font-size: 13px;
  font-weight: 950;
}

.profile-used-card {
  margin: 18px 0;
  padding: 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
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
}

.result-section {
  min-width: 0;
}

.notice-message {
  margin: 0 0 14px;
  padding: 14px 18px;
  border-radius: 14px;
  font-weight: 900;
}

.notice-message.error {
  border: 1px solid #fecaca;
  background: #fff5f5;
  color: var(--color-danger);
}

.notice-message.success {
  border: 1px solid #bbf7d0;
  background: #f0fdf4;
  color: #15803d;
}

.state-card {
  min-height: 520px;
  display: grid;
  place-items: center;
  align-content: center;
  padding: 40px;
  text-align: center;
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
  display: grid;
  gap: 20px;
}

.summary-card {
  display: grid;
  grid-template-columns: 1fr 1fr 220px 1.35fr;
  gap: 20px;
  align-items: center;
  padding: 24px;
}

.summary-block {
  display: grid;
  grid-template-columns: 58px 1fr;
  gap: 14px;
  align-items: center;
}

.summary-icon {
  display: grid;
  place-items: center;
  width: 58px;
  height: 58px;
  border-radius: 21px;
  font-size: 28px;
}

.summary-icon.mint {
  background: var(--color-accent-soft);
}

.summary-icon.purple {
  background: #f2ebff;
}

.summary-block small {
  color: var(--color-text-light);
  font-size: 12px;
  font-weight: 900;
}

.summary-block strong {
  display: block;
  overflow: hidden;
  color: var(--color-text);
  font-size: 20px;
  font-weight: 950;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.summary-block p {
  margin: 4px 0 0;
  color: var(--color-text-muted);
  font-size: 13px;
}

.score-ring-card {
  display: grid;
  place-items: center;
  gap: 8px;
}

.score-ring {
  display: grid;
  place-items: center;
  width: 128px;
  height: 128px;
  border-radius: 50%;
  background: conic-gradient(var(--color-accent) var(--score-degree), #e8eef8 0deg);
}

.score-ring > div {
  display: grid;
  place-items: center;
  width: 94px;
  height: 94px;
  border-radius: 50%;
  background: #fff;
}

.score-ring span {
  color: var(--color-text-muted);
  font-size: 11px;
  font-weight: 900;
}

.score-ring strong {
  color: var(--color-accent);
  font-size: 28px;
  font-weight: 950;
}

.score-ring-card p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 800;
}

.reason-chip-box h3 {
  margin: 0 0 12px;
  color: var(--color-text);
  font-size: 16px;
  font-weight: 950;
}

.reason-chip-box > div {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.reason-chip {
  display: inline-flex;
  gap: 8px;
  align-items: center;
  min-height: 40px;
  padding: 0 14px;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  background: #fff;
  color: var(--color-text);
  font-size: 13px;
  font-weight: 850;
}

.reason-chip em {
  color: var(--color-primary);
  font-style: normal;
}

.bank-result-card {
  display: grid;
  grid-template-columns: 1.1fr 1fr 1fr;
  gap: 22px;
  padding: 24px;
}

.bank-main-info {
  display: grid;
  grid-template-columns: 72px 1fr;
  gap: 16px;
  align-items: start;
}

.bank-large-icon {
  display: grid;
  place-items: center;
  width: 72px;
  height: 72px;
  border-radius: 25px;
  background: linear-gradient(135deg, var(--color-primary), #4f6bff);
  color: #fff;
  font-size: 34px;
}

.bank-main-info h2 {
  margin: 9px 0 4px;
  color: var(--color-text);
  font-size: 25px;
  font-weight: 950;
  letter-spacing: -0.04em;
}

.bank-main-info p {
  margin: 0 0 14px;
  color: var(--color-text-muted);
  font-size: 14px;
}

.bank-detail-button {
  min-width: 190px;
}

.bank-info-column {
  padding-left: 20px;
  border-left: 1px solid var(--color-border);
}

.bank-info-column h3 {
  margin: 0 0 12px;
  color: var(--color-text);
  font-size: 16px;
  font-weight: 950;
}

.bank-info-column ul {
  display: grid;
  gap: 9px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.bank-info-column li {
  position: relative;
  padding-left: 20px;
  color: var(--color-text-muted);
  font-size: 13px;
  line-height: 1.5;
}

.bank-info-column li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: var(--color-accent);
  font-weight: 950;
}

.bank-info-column dl {
  display: grid;
  gap: 12px;
  margin: 0;
}

.bank-info-column dl div {
  padding-bottom: 11px;
  border-bottom: 1px solid var(--color-border);
}

.bank-info-column dt {
  color: var(--color-text-light);
  font-size: 12px;
  font-weight: 900;
}

.bank-info-column dd {
  overflow: hidden;
  margin: 4px 0 0;
  color: var(--color-text);
  font-size: 13px;
  font-weight: 800;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-analysis-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 350px;
  gap: 20px;
  align-items: start;
}

.compact-heading {
  margin-bottom: 14px;
}

.compact-heading h2 {
  font-size: 24px;
}

.compact-heading > span {
  color: var(--color-primary);
  font-weight: 950;
}

.product-card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 14px;
}

.recommend-product-card {
  min-width: 0;
  overflow: hidden;
  padding: 18px;
  cursor: pointer;
  transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
}

.recommend-product-card:hover,
.recommend-product-card.selected {
  border-color: rgba(0, 30, 190, 0.35);
  box-shadow: 0 18px 38px rgba(0, 30, 190, 0.12);
  transform: translateY(-2px);
}

.recommend-product-card.selected .rank-badge::after {
  content: ' 선택됨';
}

.product-card-top {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: center;
  margin-bottom: 14px;
}

.rank-badge {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 0 10px;
  border-radius: 999px;
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-size: 12px;
  font-weight: 950;
}

.heart-button {
  display: grid;
  place-items: center;
  width: 38px;
  height: 38px;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  background: #fff;
  color: #98a4bc;
  font-size: 20px;
}

.heart-button.active {
  border-color: #fecdd3;
  background: #fff1f2;
  color: var(--color-danger);
}

.recommend-product-card h3 {
  min-height: 52px;
  max-width: 100%;
  margin: 12px 0 4px;
  color: var(--color-text);
  font-size: 18px;
  line-height: 1.35;
  font-weight: 950;
  letter-spacing: -0.04em;
  word-break: keep-all;
  overflow-wrap: anywhere;
}

.bank-line {
  max-width: 100%;
  margin: 0 0 14px;
  color: var(--color-text-muted);
  font-size: 13px;
  word-break: keep-all;
  overflow-wrap: anywhere;
}

.product-rate-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 12px;
}

.product-rate-row div {
  min-width: 0;
  overflow: hidden;
  padding: 12px;
  border-radius: 14px;
  background: var(--color-surface-soft);
}

.product-rate-row small {
  display: block;
  color: var(--color-text-light);
  font-size: 11px;
  font-weight: 900;
}

.product-rate-row strong {
  display: block;
  max-width: 100%;
  color: var(--color-primary);
  font-size: 21px;
  font-weight: 950;
  word-break: keep-all;
  overflow-wrap: anywhere;
}

.product-mini-info {
  display: grid;
  gap: 8px;
  margin: 0 0 12px;
}

.product-mini-info div {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--color-border);
}

.product-mini-info dt {
  color: var(--color-text-light);
  font-size: 12px;
  font-weight: 900;
}

.product-mini-info dd {
  min-width: 0;
  margin: 0;
  color: var(--color-text);
  font-size: 12px;
  font-weight: 900;
  text-align: right;
  word-break: keep-all;
  overflow-wrap: anywhere;
}

.recommend-reason {
  min-height: 58px;
  margin: 0 0 14px;
  color: var(--color-text-muted);
  font-size: 13px;
  line-height: 1.5;
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
}

.detail-button.full {
  width: 100%;
}

.score-detail-card {
  padding: 22px;
}

.score-detail-card h2 {
  margin: 0 0 8px;
  color: var(--color-text);
  font-size: 20px;
  font-weight: 950;
}

.selected-score-product {
  margin: 0 0 16px;
  color: var(--color-text-muted);
  font-size: 13px;
  line-height: 1.45;
  font-weight: 800;
  word-break: keep-all;
  overflow-wrap: anywhere;
}

.score-detail-row {
  display: grid;
  grid-template-columns: 1fr 130px auto;
  gap: 12px;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--color-border);
}

.score-detail-label strong {
  display: block;
  color: var(--color-text);
  font-size: 14px;
  font-weight: 950;
}

.score-detail-label span {
  display: block;
  margin-top: 2px;
  color: var(--color-text-muted);
  font-size: 12px;
  line-height: 1.4;
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
  margin-top: 20px;
}

.total-score-row strong {
  color: var(--color-text);
  font-size: 17px;
  font-weight: 950;
}

.total-score-row span {
  color: var(--color-primary);
  font-size: 34px;
  font-weight: 950;
  letter-spacing: -0.05em;
}

.total-score-row small {
  color: var(--color-text-muted);
  font-size: 16px;
}

@media (max-width: 1180px) {
  .recommend-hero,
  .recommend-workspace,
  .product-analysis-grid {
    grid-template-columns: 1fr;
  }

  .hero-visual {
    display: none;
  }

  .condition-card {
    position: static;
  }

  .summary-card,
  .bank-result-card {
    grid-template-columns: 1fr;
  }

  .bank-info-column {
    padding-left: 0;
    border-left: 0;
    border-top: 1px solid var(--color-border);
    padding-top: 18px;
  }
}

@media (max-width: 820px) {
  .product-card-grid {
    grid-template-columns: 1fr;
  }

  .summary-card {
    padding: 18px;
  }

  .score-detail-row {
    grid-template-columns: 1fr;
  }
}
</style>
