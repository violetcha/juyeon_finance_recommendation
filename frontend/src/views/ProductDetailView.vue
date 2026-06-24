<template>
  <main class="product-detail-page">
    <RouterLink :to="{ name: 'products' }" class="back-link">
      ← 예적금 상품 목록으로
    </RouterLink>

    <p v-if="loading" class="state-message">상품 상세 정보를 불러오는 중입니다...</p>
    <p v-else-if="errorMessage" class="state-message error">{{ errorMessage }}</p>

    <template v-else-if="product">
      <section class="detail-hero card">
        <div class="hero-main">
          <span class="bank-avatar" :class="avatarTone">
            {{ bankInitial }}
          </span>

          <div class="hero-title-area">
            <div class="badge-row">
              <span class="badge" :class="productType === 'saving' ? 'purple' : 'mint'">
                {{ productTypeLabel }}
              </span>
              <span v-if="hasNonFaceJoin" class="badge mint">비대면 가능</span>
              <span v-if="hasPreferentialRate" class="badge purple">우대금리</span>
              <span v-if="isShortTermProduct" class="badge blue">단기 가능</span>
            </div>

            <p class="bank-name">{{ bankName }}</p>
            <h1>{{ product.name }}</h1>
            <p class="hero-description">
              실제 저장된 금융상품 데이터 기준으로 가입 조건, 우대 조건, 기간별 금리 옵션을 확인합니다.
            </p>
          </div>
        </div>

        <div class="hero-rate-card">
          <span>최고 금리</span>
          <strong>{{ formatRateValue(bestRate) }}</strong>
          <p>연, 세전 기준</p>

          <button
            type="button"
            class="heart-button"
            :class="{ active: isFavorite }"
            :disabled="favoriteLoading"
            @click="handleFavoriteClick"
          >
            <span v-if="favoriteLoading">처리 중</span>
            <span v-else>{{ isFavorite ? '♥ 관심상품' : '♡ 관심상품' }}</span>
          </button>
        </div>
      </section>

      <section class="summary-grid">
        <article class="summary-card card">
          <span>기본 금리</span>
          <strong>{{ formatRateValue(baseRate) }}</strong>
          <p>옵션 중 가장 높은 기본금리</p>
        </article>

        <article class="summary-card card">
          <span>가입 기간</span>
          <strong>{{ termSummary }}</strong>
          <p>기간별 금리 옵션 기준</p>
        </article>

        <article class="summary-card card">
          <span>가입 방식</span>
          <strong>{{ joinWaySummary }}</strong>
          <p>{{ product.join_way || '상세 가입 방식 정보 없음' }}</p>
        </article>

        <article class="summary-card card">
          <span>가입 한도</span>
          <strong>{{ formatLimit(product.max_limit) }}</strong>
          <p>상품 공시 기준</p>
        </article>
      </section>

      <p v-if="favoriteMessage" class="toast-message">
        {{ favoriteMessage }}
      </p>

      <section class="content-layout">
        <div class="main-column">
          <section class="card rate-section">
            <div class="section-heading">
              <div>
                <p class="eyebrow">RATE OPTIONS</p>
                <h2>기간별 금리 옵션</h2>
                <p>
                  {{ productType === 'saving'
                    ? '적금은 적립 방식과 기간에 따라 금리가 다를 수 있습니다.'
                    : '예금은 가입 기간에 따라 기본 금리와 최고 우대 금리가 다를 수 있습니다.'
                  }}
                </p>
              </div>
            </div>

            <div v-if="sortedOptions.length > 0" class="rate-visual-list">
              <article
                v-for="option in sortedOptions"
                :key="option.id"
                class="rate-option-card"
              >
                <div class="option-meta">
                  <strong>{{ option.save_trm }}개월</strong>
                  <span>{{ option.intr_rate_type_nm || '이자 유형 정보 없음' }}</span>
                  <em v-if="productType === 'saving'">
                    {{ option.rsrv_type_nm || '적립 유형 정보 없음' }}
                  </em>
                </div>

                <div class="rate-bars">
                  <div class="rate-bar-row">
                    <span>기본</span>
                    <div class="bar-track">
                      <i :style="{ width: getRateBarWidth(option.intr_rate) }"></i>
                    </div>
                    <strong>{{ formatRate(option.intr_rate) }}</strong>
                  </div>

                  <div class="rate-bar-row highlight">
                    <span>최고</span>
                    <div class="bar-track">
                      <i :style="{ width: getRateBarWidth(option.intr_rate2 || option.intr_rate) }"></i>
                    </div>
                    <strong>{{ formatRate(option.intr_rate2) }}</strong>
                  </div>
                </div>
              </article>
            </div>

            <p v-else class="empty-message">
              금리 옵션 정보가 없습니다.
            </p>
          </section>

          <section class="card info-section">
            <div class="section-heading">
              <div>
                <p class="eyebrow">PRODUCT CONDITIONS</p>
                <h2>상품 조건 상세</h2>
              </div>
            </div>

            <div class="info-block">
              <h3>우대 조건</h3>
              <p>{{ product.spcl_cnd || '우대 조건 정보가 없습니다.' }}</p>
            </div>

            <div class="info-block">
              <h3>만기 후 이자율</h3>
              <p>{{ product.mtrt_int || '만기 후 이자율 정보가 없습니다.' }}</p>
            </div>

            <div class="info-block">
              <h3>기타 유의사항</h3>
              <p>{{ product.etc_note || '기타 유의사항 정보가 없습니다.' }}</p>
            </div>
          </section>
        </div>

        <aside class="side-column">
          <section class="card side-card">
            <div class="section-heading compact">
              <div>
                <p class="eyebrow">JOIN INFO</p>
                <h2>가입 정보</h2>
              </div>
            </div>

            <dl class="info-list">
              <div>
                <dt>은행 코드</dt>
                <dd>{{ product.bank?.code || '정보 없음' }}</dd>
              </div>
              <div>
                <dt>상품 코드</dt>
                <dd>{{ product.fin_prdt_cd || '정보 없음' }}</dd>
              </div>
              <div>
                <dt>가입 대상</dt>
                <dd>{{ product.join_member || '정보 없음' }}</dd>
              </div>
              <div>
                <dt>가입 제한</dt>
                <dd>{{ joinDenyLabel }}</dd>
              </div>
            </dl>
          </section>

          <section class="card side-card eligibility-card">
            <div class="section-heading compact">
              <div>
                <p class="eyebrow">CHECK POINT</p>
                <h2>추천 확인 포인트</h2>
              </div>
            </div>

            <ul>
              <li>
                <span>1</span>
                가입대상 문구에 나이·성별 조건이 있는지 확인하세요.
              </li>
              <li>
                <span>2</span>
                최고 금리는 우대조건 충족 시 적용될 수 있습니다.
              </li>
              <li>
                <span>3</span>
                실제 가입 가능 여부는 금융회사 최종 안내를 확인해야 합니다.
              </li>
            </ul>
          </section>

          <section class="card side-card date-card">
            <div class="section-heading compact">
              <div>
                <p class="eyebrow">DISCLOSURE</p>
                <h2>공시 정보</h2>
              </div>
            </div>

            <dl class="info-list">
              <div>
                <dt>공시 월</dt>
                <dd>{{ product.dcls_month || '정보 없음' }}</dd>
              </div>
              <div>
                <dt>공시 시작일</dt>
                <dd>{{ formatDisclosureDate(product.dcls_strt_day) }}</dd>
              </div>
              <div>
                <dt>공시 종료일</dt>
                <dd>{{ formatDisclosureDate(product.dcls_end_day) }}</dd>
              </div>
              <div>
                <dt>제출일</dt>
                <dd>{{ formatDisclosureDate(product.fin_co_subm_day) }}</dd>
              </div>
            </dl>
          </section>
        </aside>
      </section>
    </template>
  </main>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import {
  getDepositProductDetail,
  getSavingProductDetail,
} from '@/api/products'
import { getFavorites, toggleFavoriteProduct } from '@/api/favorites'

const route = useRoute()

const product = ref(null)
const loading = ref(false)
const errorMessage = ref('')
const favoriteMessage = ref('')
const isFavorite = ref(false)
const favoriteLoading = ref(false)

const productType = computed(() => {
  return route.query.type === 'saving' ? 'saving' : 'deposit'
})

const productTypeLabel = computed(() => {
  return productType.value === 'saving' ? '적금' : '정기예금'
})

const bankName = computed(() => {
  return product.value?.bank?.name || '은행명 없음'
})

const bankInitial = computed(() => {
  return bankName.value.slice(0, 1)
})

const avatarTone = computed(() => {
  const tones = ['blue', 'mint', 'purple', 'orange', 'sky']
  const id = Number(product.value?.id || 0)
  return tones[id % tones.length]
})

const sortedOptions = computed(() => {
  if (!product.value?.options) {
    return []
  }

  return [...product.value.options].sort((a, b) => {
    const termA = Number(a.save_trm)
    const termB = Number(b.save_trm)

    if (termA !== termB) {
      return termA - termB
    }

    const rsrvA = a.rsrv_type_nm || ''
    const rsrvB = b.rsrv_type_nm || ''

    return rsrvA.localeCompare(rsrvB, 'ko')
  })
})

const rateNumbers = computed(() => {
  return sortedOptions.value
    .flatMap((option) => [option.intr_rate, option.intr_rate2])
    .map((value) => safeNumber(value))
    .filter((value) => value !== null)
})

const maxChartRate = computed(() => {
  if (rateNumbers.value.length === 0) {
    return 1
  }

  return Math.max(...rateNumbers.value, 1)
})

const baseRate = computed(() => {
  const rates = sortedOptions.value
    .map((option) => safeNumber(option.intr_rate))
    .filter((value) => value !== null)

  return rates.length > 0 ? Math.max(...rates) : null
})

const bestRate = computed(() => {
  const directRate = safeNumber(product.value?.max_interest_rate)

  if (directRate !== null) {
    return directRate
  }

  const rates = sortedOptions.value
    .map((option) => safeNumber(option.intr_rate2) ?? safeNumber(option.intr_rate))
    .filter((value) => value !== null)

  return rates.length > 0 ? Math.max(...rates) : null
})

const terms = computed(() => {
  const values = sortedOptions.value
    .map((option) => safeNumber(option.save_trm))
    .filter((value) => value !== null)

  return [...new Set(values)].sort((a, b) => a - b)
})

const termSummary = computed(() => {
  if (terms.value.length === 0) {
    return '정보 없음'
  }

  if (terms.value.length === 1) {
    return `${terms.value[0]}개월`
  }

  return `${terms.value[0]}~${terms.value[terms.value.length - 1]}개월`
})

const joinWaySummary = computed(() => {
  const joinWay = product.value?.join_way || ''

  if (!joinWay) {
    return '정보 없음'
  }

  if (joinWay.includes('인터넷') || joinWay.includes('스마트폰')) {
    return '비대면'
  }

  if (joinWay.includes('영업점')) {
    return '영업점'
  }

  return joinWay.split(',')[0].slice(0, 12)
})

const hasNonFaceJoin = computed(() => {
  const joinWay = product.value?.join_way || ''
  return joinWay.includes('인터넷') || joinWay.includes('스마트폰')
})

const hasPreferentialRate = computed(() => {
  return bestRate.value !== null && baseRate.value !== null && bestRate.value > baseRate.value
})

const isShortTermProduct = computed(() => {
  return terms.value.some((term) => term <= 12)
})

const joinDenyLabel = computed(() => {
  const value = String(product.value?.join_deny || '').trim()

  const labels = {
    1: '제한 없음',
    2: '서민전용',
    3: '일부 제한',
  }

  return labels[value] || value || '정보 없음'
})

const safeNumber = (value) => {
  if (value === null || value === undefined || value === '') {
    return null
  }

  const numberValue = Number(value)

  if (Number.isNaN(numberValue)) {
    return null
  }

  return numberValue
}

const formatRate = (rate) => {
  const numberValue = safeNumber(rate)

  if (numberValue === null) {
    return '정보 없음'
  }

  return `${numberValue.toFixed(2)}%`
}

const formatRateValue = (rate) => {
  const numberValue = safeNumber(rate)

  if (numberValue === null) {
    return '-'
  }

  return `${numberValue.toFixed(2)}%`
}

const formatLimit = (limit) => {
  const numberValue = safeNumber(limit)

  if (numberValue === null || numberValue === 0) {
    return '정보 없음'
  }

  return `${numberValue.toLocaleString()}원`
}

const formatDisclosureDate = (value) => {
  if (!value) {
    return '정보 없음'
  }

  const text = String(value)

  if (/^\d{8}$/.test(text)) {
    return `${text.slice(0, 4)}.${text.slice(4, 6)}.${text.slice(6, 8)}`
  }

  if (/^\d{14}$/.test(text)) {
    return `${text.slice(0, 4)}.${text.slice(4, 6)}.${text.slice(6, 8)} ${text.slice(8, 10)}:${text.slice(10, 12)}`
  }

  return text
}

const getRateBarWidth = (rate) => {
  const numberValue = safeNumber(rate)

  if (numberValue === null || maxChartRate.value <= 0) {
    return '0%'
  }

  return `${Math.max(4, Math.min(100, (numberValue / maxChartRate.value) * 100))}%`
}

const extractFavoriteProductId = (favorite) => {
  if (favorite.product_id) {
    return favorite.product_id
  }

  if (typeof favorite.product === 'number') {
    return favorite.product
  }

  const favoriteProduct = favorite.product || favorite
  return favoriteProduct.id || null
}

const checkFavoriteStatus = async () => {
  const token = localStorage.getItem('token')

  if (!token || !product.value) {
    isFavorite.value = false
    return
  }

  try {
    const response = await getFavorites()
    const favorites = response.data || []

    isFavorite.value = favorites.some((favorite) => {
      return extractFavoriteProductId(favorite) === product.value.id
    })
  } catch (error) {
    console.error(error)
    isFavorite.value = false
  }
}

const handleFavoriteClick = async () => {
  if (!product.value) {
    return
  }

  const token = localStorage.getItem('token')

  errorMessage.value = ''
  favoriteMessage.value = ''

  if (!token) {
    favoriteMessage.value = '로그인 후 관심상품을 등록할 수 있습니다.'
    window.setTimeout(() => {
      favoriteMessage.value = ''
    }, 1800)
    return
  }

  favoriteLoading.value = true

  try {
    const response = await toggleFavoriteProduct(product.value.id)

    if (response.data.is_favorite !== undefined) {
      isFavorite.value = response.data.is_favorite
    } else {
      isFavorite.value = !isFavorite.value
    }

    favoriteMessage.value = isFavorite.value
      ? '관심상품에 등록되었습니다.'
      : '관심상품에서 삭제되었습니다.'

    window.setTimeout(() => {
      favoriteMessage.value = ''
    }, 1800)
  } catch (error) {
    console.error('관심상품 처리 에러:', error)

    favoriteMessage.value =
      error.response?.data?.message ||
      '관심상품 처리 중 오류가 발생했습니다.'
  } finally {
    favoriteLoading.value = false
  }
}

const fetchProductDetail = async () => {
  loading.value = true
  errorMessage.value = ''
  favoriteMessage.value = ''
  product.value = null

  try {
    const productId = route.params.id
    let response

    if (productType.value === 'saving') {
      response = await getSavingProductDetail(productId)
    } else {
      response = await getDepositProductDetail(productId)
    }

    product.value = response.data

    await checkFavoriteStatus()
  } catch (error) {
    console.error(error)
    errorMessage.value =
      error.response?.data?.message ||
      '상품 상세 정보를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProductDetail()
})

watch(
  () => route.fullPath,
  () => {
    fetchProductDetail()
  }
)
</script>

<style scoped>
.product-detail-page {
  width: min(var(--container-width), calc(100% - 48px));
  margin: 0 auto;
  padding: 32px 0 64px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  margin-bottom: 18px;
  color: var(--color-primary);
  font-size: 14px;
  font-weight: 950;
  text-decoration: none;
}

.card {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: #fff;
  box-shadow: var(--shadow-soft);
}

.state-message {
  margin: 20px 0;
  padding: 22px;
  border: 1px dashed var(--color-border-strong);
  border-radius: var(--radius-md);
  background: var(--color-surface-soft);
  color: var(--color-text-muted);
  text-align: center;
  font-weight: 850;
}

.state-message.error {
  border-color: #fecaca;
  background: #fff5f5;
  color: var(--color-danger);
}

.detail-hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 260px;
  gap: 26px;
  align-items: stretch;
  padding: 30px;
  margin-bottom: 18px;
  overflow: hidden;
}

.hero-main {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  min-width: 0;
}

.bank-avatar {
  display: grid;
  place-items: center;
  width: 76px;
  height: 76px;
  border-radius: 26px;
  color: #fff;
  font-size: 30px;
  font-weight: 950;
  flex-shrink: 0;
}

.bank-avatar.blue { background: linear-gradient(135deg, #4f6bff, var(--color-primary)); }
.bank-avatar.mint { background: linear-gradient(135deg, #4be0c8, #0f9f8b); }
.bank-avatar.purple { background: linear-gradient(135deg, #a679ff, var(--color-purple)); }
.bank-avatar.orange { background: linear-gradient(135deg, #fb923c, #ea580c); }
.bank-avatar.sky { background: linear-gradient(135deg, #60a5fa, #2563eb); }

.hero-title-area {
  min-width: 0;
}

.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin-bottom: 12px;
}

.badge {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 0 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 950;
}

.badge.mint {
  background: #e7fbf7;
  color: #0f9f8b;
}

.badge.purple {
  background: #f3e8ff;
  color: #7c3aed;
}

.badge.blue {
  background: #eaf0ff;
  color: #3151db;
}

.bank-name {
  margin: 0 0 5px;
  color: var(--color-text-muted);
  font-size: 14px;
  font-weight: 900;
}

.hero-title-area h1 {
  margin: 0;
  color: var(--color-text);
  font-size: clamp(30px, 4vw, 44px);
  line-height: 1.17;
  font-weight: 950;
  letter-spacing: -0.06em;
}

.hero-description {
  max-width: 640px;
  margin: 14px 0 0;
  color: var(--color-text-muted);
  font-size: 15px;
  line-height: 1.65;
}

.hero-rate-card {
  display: grid;
  align-content: center;
  gap: 8px;
  padding: 22px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: linear-gradient(180deg, var(--color-primary-soft) 0%, #fff 100%);
  text-align: center;
}

.hero-rate-card > span {
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 950;
}

.hero-rate-card strong {
  color: var(--color-primary);
  font-size: 42px;
  line-height: 1;
  font-weight: 950;
  letter-spacing: -0.05em;
}

.hero-rate-card p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 12px;
  font-weight: 850;
}

.heart-button {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  min-height: 44px;
  margin-top: 12px;
  border: 1px solid var(--color-primary);
  border-radius: 14px;
  background: #fff;
  color: var(--color-primary);
  font-weight: 950;
  cursor: pointer;
}

.heart-button.active {
  border-color: #fecdd3;
  background: #fff1f2;
  color: var(--color-danger);
}

.heart-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}

.summary-card {
  padding: 18px;
}

.summary-card span {
  display: block;
  margin-bottom: 8px;
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 950;
}

.summary-card strong {
  display: block;
  overflow: hidden;
  color: var(--color-text);
  font-size: 20px;
  font-weight: 950;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.summary-card p {
  overflow: hidden;
  margin: 8px 0 0;
  color: var(--color-text-muted);
  font-size: 12px;
  line-height: 1.5;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.content-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 340px;
  gap: 18px;
  align-items: flex-start;
}

.main-column {
  display: grid;
  gap: 18px;
  min-width: 0;
}

.side-column {
  display: grid;
  gap: 18px;
  position: sticky;
  top: calc(var(--header-height) + 18px);
}

.rate-section,
.info-section,
.side-card {
  padding: 22px;
}

.section-heading {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  margin-bottom: 18px;
}

.section-heading.compact {
  margin-bottom: 14px;
}

.eyebrow {
  margin: 0 0 7px;
  color: var(--color-primary);
  font-size: 11px;
  font-weight: 950;
  letter-spacing: 0.12em;
}

.section-heading h2 {
  margin: 0;
  color: var(--color-text);
  font-size: 23px;
  font-weight: 950;
  letter-spacing: -0.04em;
}

.section-heading p {
  margin: 6px 0 0;
  color: var(--color-text-muted);
  font-size: 14px;
  line-height: 1.55;
}

.rate-visual-list {
  display: grid;
  gap: 12px;
}

.rate-option-card {
  display: grid;
  grid-template-columns: 190px minmax(0, 1fr);
  gap: 18px;
  align-items: center;
  padding: 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface-soft);
}

.option-meta {
  display: grid;
  gap: 5px;
}

.option-meta strong {
  color: var(--color-text);
  font-size: 20px;
  font-weight: 950;
}

.option-meta span,
.option-meta em {
  color: var(--color-text-muted);
  font-size: 12px;
  font-style: normal;
  font-weight: 850;
}

.rate-bars {
  display: grid;
  gap: 10px;
}

.rate-bar-row {
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr) 84px;
  gap: 10px;
  align-items: center;
}

.rate-bar-row span {
  color: var(--color-text-muted);
  font-size: 12px;
  font-weight: 950;
}

.rate-bar-row strong {
  color: var(--color-text);
  font-size: 14px;
  font-weight: 950;
  text-align: right;
}

.rate-bar-row.highlight strong {
  color: var(--color-primary);
}

.bar-track {
  height: 10px;
  border-radius: 999px;
  background: #e5e7eb;
  overflow: hidden;
}

.bar-track i {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #8ea0ff, var(--color-primary));
}

.rate-bar-row.highlight .bar-track i {
  background: linear-gradient(90deg, #44ddc3, var(--color-accent));
}

.info-block {
  padding: 18px 0;
  border-top: 1px solid var(--color-border);
}

.info-block:first-of-type {
  border-top: 0;
}

.info-block h3 {
  margin: 0 0 8px;
  color: var(--color-text);
  font-size: 16px;
  font-weight: 950;
}

.info-block p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 14px;
  line-height: 1.8;
  white-space: pre-line;
}

.info-list {
  display: grid;
  gap: 0;
  margin: 0;
}

.info-list div {
  display: grid;
  gap: 5px;
  padding: 12px 0;
  border-bottom: 1px solid var(--color-border);
}

.info-list div:last-child {
  border-bottom: 0;
}

.info-list dt {
  color: var(--color-text-muted);
  font-size: 12px;
  font-weight: 950;
}

.info-list dd {
  margin: 0;
  color: var(--color-text);
  font-size: 14px;
  font-weight: 900;
  line-height: 1.5;
  word-break: keep-all;
}

.eligibility-card ul {
  display: grid;
  gap: 12px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.eligibility-card li {
  display: grid;
  grid-template-columns: 24px minmax(0, 1fr);
  gap: 9px;
  color: var(--color-text-muted);
  font-size: 13px;
  line-height: 1.55;
  font-weight: 800;
}

.eligibility-card li span {
  display: grid;
  place-items: center;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-size: 12px;
  font-weight: 950;
}

.empty-message {
  margin: 0;
  padding: 24px;
  border: 1px dashed var(--color-border-strong);
  border-radius: var(--radius-md);
  background: var(--color-surface-soft);
  color: var(--color-text-muted);
  text-align: center;
  font-weight: 850;
}

.toast-message {
  position: fixed;
  left: 50%;
  bottom: 32px;
  z-index: 2000;
  min-width: 280px;
  max-width: min(520px, calc(100% - 40px));
  margin: 0;
  padding: 14px 20px;
  border-radius: 999px;
  background: rgba(15, 27, 61, 0.96);
  color: #fff;
  box-shadow: var(--shadow-card);
  font-weight: 900;
  text-align: center;
  transform: translateX(-50%);
}

@media (max-width: 1100px) {
  .detail-hero,
  .content-layout {
    grid-template-columns: 1fr;
  }

  .side-column {
    position: static;
  }

  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .product-detail-page {
    width: min(100% - 28px, var(--container-width));
    padding: 24px 0 46px;
  }

  .detail-hero {
    padding: 22px;
  }

  .hero-main {
    flex-direction: column;
  }

  .summary-grid {
    grid-template-columns: 1fr;
  }

  .rate-option-card {
    grid-template-columns: 1fr;
  }

  .rate-bar-row {
    grid-template-columns: 42px minmax(0, 1fr) 74px;
  }
}
</style>
