<template>
  <div class="home-page">
    <section class="page-title">
      <p class="breadcrumb">FinBank</p>
      <h1>금융 생활 시작 가이드</h1>
    </section>

    <section class="hero-section">
      <div class="hero-slide">
        <p class="hero-label">{{ activeHero.badge }}</p>
        <h2>{{ activeHero.title }}</h2>
        <p class="hero-description">{{ activeHero.description }}</p>

        <div class="hero-points">
          <span v-for="point in activeHero.points" :key="point">
            {{ point }}
          </span>
        </div>

        <div class="hero-buttons">
          <RouterLink :to="activeHero.primaryTo" class="primary-btn">
            {{ activeHero.primaryText }} →
          </RouterLink>

          <RouterLink
            v-if="activeHero.secondaryTo"
            :to="activeHero.secondaryTo"
            class="secondary-btn"
          >
            {{ activeHero.secondaryText }} →
          </RouterLink>
        </div>
      </div>

      <div class="hero-control-row">
        <button type="button" class="hero-arrow" @click="prevHeroSlide">
          ‹
        </button>

        <div class="hero-dots" aria-label="서비스 요약 슬라이드 선택">
          <button
            v-for="(slide, index) in heroSlides"
            :key="slide.badge"
            type="button"
            class="hero-dot"
            :class="{ active: activeHeroIndex === index }"
            :aria-label="`${index + 1}번 슬라이드 보기`"
            @click="setHeroSlide(index)"
          ></button>
        </div>

        <button type="button" class="hero-arrow" @click="nextHeroSlide">
          ›
        </button>
      </div>
    </section>

    <section class="bank-summary-section">
      <div class="section-header">
        <div>
          <h3>5대 은행 한눈에 보기</h3>
          <p>주거래은행 테스트 추천 기준에 사용한 은행별 핵심 특징입니다.</p>
        </div>

        <RouterLink to="/main-bank" class="all-link">
          주거래은행 찾기
        </RouterLink>
      </div>

      <div class="bank-grid">
        <article v-for="bank in bankSummaries" :key="bank.name" class="bank-card">
          <div class="bank-top">
            <span class="bank-icon">{{ bank.icon }}</span>
            <div>
              <h4>{{ bank.name }}</h4>
              <p>{{ bank.type }}</p>
            </div>
          </div>

          <p class="bank-description">
            {{ bank.description }}
          </p>

          <div class="tag-list">
            <span v-for="tag in bank.tags" :key="`${bank.name}-${tag}`">
              {{ tag }}
            </span>
          </div>
        </article>
      </div>
    </section>

    <section class="preview-section">
      <div class="section-header">
        <div>
          <h3>인기 예금 상품 TOP 3</h3>
          <p>최고 금리 기준으로 예금 상품을 먼저 보여줍니다.</p>
        </div>

        <RouterLink to="/products" class="all-link">
          전체 상품 보기
        </RouterLink>
      </div>

      <p v-if="productLoading" class="message">
        상품을 불러오는 중입니다...
      </p>

      <p v-else-if="depositErrorMessage" class="error-message">
        {{ depositErrorMessage }}
      </p>

      <div v-else-if="topDepositProducts.length > 0" class="preview-grid">
        <article
          v-for="product in topDepositProducts"
          :key="getProductKey(product, 'deposit')"
          class="preview-card"
        >
          <p class="bank-name">
            {{ getBankName(product) }}
          </p>

          <h4>{{ product.name }}</h4>

          <div class="rate-bar">
            <span
              class="rate-fill"
              :style="{ width: getRateWidth(product.max_interest_rate) }"
            ></span>
          </div>

          <div class="product-info">
            <span>최고 금리</span>
            <strong>{{ formatRate(product.max_interest_rate) }}</strong>
          </div>

          <p class="join-way">
            가입 방법: {{ product.join_way || '정보 없음' }}
          </p>

          <RouterLink
            :to="{
              name: 'product-detail',
              params: { id: product.id },
              query: { type: 'deposit' }
            }"
            class="detail-link"
          >
            상품 보러가기
          </RouterLink>
        </article>
      </div>

      <div v-else class="empty-box">
        <h4>조회된 예금 상품이 없습니다.</h4>
        <p>상품 데이터가 아직 준비되지 않았습니다. 잠시 후 다시 시도해주세요.</p>
      </div>
    </section>

    <section class="preview-section">
      <div class="section-header">
        <div>
          <h3>인기 적금 상품 TOP 3</h3>
          <p>최고 금리 기준으로 적금 상품을 먼저 보여줍니다.</p>
        </div>

        <RouterLink to="/products" class="all-link">
          전체 상품 보기
        </RouterLink>
      </div>

      <p v-if="productLoading" class="message">
        상품을 불러오는 중입니다...
      </p>

      <p v-else-if="savingErrorMessage" class="error-message">
        {{ savingErrorMessage }}
      </p>

      <div v-else-if="topSavingProducts.length > 0" class="preview-grid">
        <article
          v-for="product in topSavingProducts"
          :key="getProductKey(product, 'saving')"
          class="preview-card"
        >
          <p class="bank-name">
            {{ getBankName(product) }}
          </p>

          <h4>{{ product.name }}</h4>

          <div class="rate-bar">
            <span
              class="rate-fill"
              :style="{ width: getRateWidth(product.max_interest_rate) }"
            ></span>
          </div>

          <div class="product-info">
            <span>최고 금리</span>
            <strong>{{ formatRate(product.max_interest_rate) }}</strong>
          </div>

          <p class="join-way">
            가입 방법: {{ product.join_way || '정보 없음' }}
          </p>

          <RouterLink
            :to="{
              name: 'product-detail',
              params: { id: product.id },
              query: { type: 'saving' }
            }"
            class="detail-link"
          >
            상품 보러가기
          </RouterLink>
        </article>
      </div>

      <div v-else class="empty-box">
        <h4>조회된 적금 상품이 없습니다.</h4>
        <p>적금 상품 데이터가 아직 준비되지 않았습니다. 잠시 후 다시 시도해주세요.</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import * as productApi from '@/api/products'

const activeHeroIndex = ref(0)
const depositProducts = ref([])
const savingProducts = ref([])
const productLoading = ref(false)
const depositErrorMessage = ref('')
const savingErrorMessage = ref('')

const heroSlides = [
  {
    badge: '예적금 추천',
    title: '내 조건에 맞는 예금·적금을 찾아보세요',
    description:
      '상품 유형, 가입 기간, 주거래은행, 우대조건, 가입 방식을 기준으로 적합한 상품을 비교할 수 있습니다.',
    points: ['예금·적금 비교', '최고금리 확인', '우대조건 반영'],
    primaryText: '예적금 추천받기',
    primaryTo: '/recommend',
    secondaryText: '상품 전체보기',
    secondaryTo: '/products',
  },
  {
    badge: '주거래은행 찾기',
    title: '나에게 맞는 주거래은행을 찾아보세요',
    description:
      '은행별 공식 특징 태그와 현재 위치 기준 지점 접근성을 함께 반영해 주거래은행 후보를 추천합니다.',
    points: ['은행 성향 테스트', '주변 지점 지도', '길찾기 연결'],
    primaryText: '주거래은행 찾기',
    primaryTo: '/main-bank',
    secondaryText: '은행 요약 보기',
    secondaryTo: '/main-bank',
  },
  {
    badge: '환율 정보',
    title: '환율 흐름을 확인하고 비교해보세요',
    description:
      '주요 통화 환율과 변동 흐름을 확인해 여행, 환전, 외화 관리에 참고할 수 있습니다.',
    points: ['환율 조회', '통화별 비교', '환전 참고 정보'],
    primaryText: '환율 정보 보기',
    primaryTo: '/exchange',
    secondaryText: '예적금 상품 보기',
    secondaryTo: '/products',
  },
  {
    badge: '금은 시세',
    title: '금·은 가격 흐름을 한눈에 확인하세요',
    description:
      '금과 은 시세 정보를 통해 안전자산 가격 흐름과 투자 참고 정보를 확인할 수 있습니다.',
    points: ['금 시세', '은 시세', '가격 흐름 확인'],
    primaryText: '금은 시세 보기',
    primaryTo: '/gold-silver',
    secondaryText: '금융상품 보기',
    secondaryTo: '/products',
  },
]

const bankSummaries = [
  {
    name: 'KB국민은행',
    icon: '🟡',
    type: '대중성 · 전국 접근성',
    description:
      '기본 금융생활을 안정적으로 시작하고, 넓은 고객 기반과 지점 접근성을 중요하게 보는 사용자에게 적합합니다.',
    tags: ['대중성', '전국접근성', '생활금융', '그룹연계'],
  },
  {
    name: '신한은행',
    icon: '🔵',
    type: '디지털 · 자산관리',
    description:
      '앱 중심 금융생활, 자산관리, 소비분석, 통합 금융 서비스를 자주 이용하는 사용자에게 적합합니다.',
    tags: ['디지털금융', '통합앱', '자산관리', '소비분석'],
  },
  {
    name: '하나은행',
    icon: '🟢',
    type: '외환 · 글로벌',
    description:
      '환전, 외화, 해외송금, 여행 관련 금융 서비스를 중요하게 보는 사용자에게 적합합니다.',
    tags: ['외환', '환전', '해외송금', '글로벌'],
  },
  {
    name: '우리은행',
    icon: '🔷',
    type: '생활관리 · 공과금',
    description:
      '생활비, 공과금, 소비관리, 금융일정처럼 일상 금융을 체계적으로 관리하려는 사용자에게 적합합니다.',
    tags: ['생활금융', '공과금', '소비관리', '금융일정'],
  },
  {
    name: 'NH농협은행',
    icon: '🌱',
    type: '지역금융 · 방문상담',
    description:
      '지역 기반 금융, 방문 상담, 공공성, 서민금융 이미지를 중요하게 보는 사용자에게 적합합니다.',
    tags: ['지역금융', '지역접근성', '공공성', '방문상담'],
  },
]

const activeHero = computed(() => heroSlides[activeHeroIndex.value])

const topDepositProducts = computed(() => {
  return getTopProducts(depositProducts.value, 3)
})

const topSavingProducts = computed(() => {
  return getTopProducts(savingProducts.value, 3)
})

const setHeroSlide = (index) => {
  activeHeroIndex.value = index
}

const prevHeroSlide = () => {
  activeHeroIndex.value =
    activeHeroIndex.value === 0 ? heroSlides.length - 1 : activeHeroIndex.value - 1
}

const nextHeroSlide = () => {
  activeHeroIndex.value =
    activeHeroIndex.value === heroSlides.length - 1 ? 0 : activeHeroIndex.value + 1
}

const normalizeProducts = (data) => {
  if (Array.isArray(data)) return data
  if (Array.isArray(data?.results)) return data.results
  if (Array.isArray(data?.products)) return data.products
  if (Array.isArray(data?.deposits)) return data.deposits
  if (Array.isArray(data?.savings)) return data.savings
  return []
}

const getTopProducts = (products, count) => {
  return [...products]
    .sort((a, b) => {
      const rateA = Number(a.max_interest_rate || 0)
      const rateB = Number(b.max_interest_rate || 0)
      return rateB - rateA
    })
    .slice(0, count)
}

const getBankName = (product) => {
  return product.bank?.name || product.bank_name || product.kor_co_nm || '은행 정보 없음'
}

const getProductKey = (product, type) => {
  return `${type}-${product.id || product.fin_prdt_cd || product.name}`
}

const formatRate = (rate) => {
  if (rate === null || rate === undefined || rate === '') {
    return '정보 없음'
  }

  return `${Number(rate).toFixed(2)}%`
}

const getRateWidth = (rate) => {
  const numberRate = Number(rate)

  if (Number.isNaN(numberRate) || numberRate <= 0) {
    return '0%'
  }

  const percent = Math.min((numberRate / 5) * 100, 100)

  return `${percent}%`
}

const fetchPreviewProducts = async () => {
  productLoading.value = true
  depositErrorMessage.value = ''
  savingErrorMessage.value = ''

  try {
    const depositPromise =
      typeof productApi.getDepositProducts === 'function'
        ? productApi.getDepositProducts()
        : Promise.reject(new Error('getDepositProducts 함수가 없습니다.'))

    const savingPromise =
      typeof productApi.getSavingProducts === 'function'
        ? productApi.getSavingProducts()
        : Promise.reject(new Error('getSavingProducts 함수가 없습니다.'))

    const [depositResult, savingResult] = await Promise.allSettled([
      depositPromise,
      savingPromise,
    ])

    if (depositResult.status === 'fulfilled') {
      depositProducts.value = normalizeProducts(depositResult.value.data)
    } else {
      console.error(depositResult.reason)
      depositErrorMessage.value =
        '예금 상품을 불러오지 못했습니다. /api/products/deposits/ API를 확인해주세요.'
    }

    if (savingResult.status === 'fulfilled') {
      savingProducts.value = normalizeProducts(savingResult.value.data)
    } else {
      console.error(savingResult.reason)
      savingErrorMessage.value =
        '적금 상품을 불러오지 못했습니다. 적금 상품 API 또는 getSavingProducts 함수를 확인해주세요.'
    }
  } finally {
    productLoading.value = false
  }
}

onMounted(() => {
  fetchPreviewProducts()
})
</script>

<style scoped>
.home-page {
  width: 100%;
  max-width: 1180px;
  margin: 0 auto;
  padding: clamp(18px, 3vw, 32px);
  box-sizing: border-box;
}

.page-title {
  padding-bottom: 18px;
  border-bottom: 1px solid #e5e7eb;
}

.breadcrumb {
  margin: 0 0 6px;
  color: #2563eb;
  font-size: 13px;
  font-weight: 800;
}

.page-title h1 {
  margin: 0;
  color: #111827;
  font-size: clamp(24px, 3vw, 36px);
}

.hero-section {
  position: relative;
  margin-top: 24px;
  padding: clamp(34px, 5vw, 56px) clamp(18px, 4vw, 44px) 30px;
  border: 1px solid #e5e7eb;
  border-radius: 22px;
  background:
    linear-gradient(135deg, rgba(37, 99, 235, 0.08), rgba(17, 24, 39, 0.04)),
    #ffffff;
  text-align: center;
  box-sizing: border-box;
  overflow: hidden;
}

.hero-slide {
  min-height: 250px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.hero-label {
  margin: 0 0 14px;
  color: #2563eb;
  font-size: 14px;
  font-weight: 800;
}

.hero-section h2 {
  max-width: 760px;
  margin: 0;
  color: #111827;
  font-size: clamp(24px, 3vw, 38px);
  line-height: 1.45;
}

.hero-description {
  max-width: 660px;
  margin: 18px auto 0;
  color: #4b5563;
  font-size: 15px;
  line-height: 1.7;
}

.hero-points {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 20px;
}

.hero-points span {
  padding: 8px 12px;
  border: 1px solid #dbeafe;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.72);
  color: #2563eb;
  font-size: 13px;
  font-weight: 800;
}

.hero-buttons {
  display: flex;
  justify-content: center;
  gap: 14px;
  margin-top: 30px;
  flex-wrap: wrap;
}

.primary-btn,
.secondary-btn {
  min-width: min(230px, 100%);
  padding: 14px 20px;
  border-radius: 12px;
  font-weight: 800;
  text-align: center;
  text-decoration: none;
  box-sizing: border-box;
}

.primary-btn {
  border: 1px solid #2563eb;
  background-color: #2563eb;
  color: white;
}

.secondary-btn {
  border: 1px solid #d1d5db;
  background-color: white;
  color: #111827;
}

.hero-control-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 14px;
  margin-top: 8px;
}

.hero-arrow {
  width: 34px;
  height: 34px;
  border: 1px solid #d1d5db;
  border-radius: 999px;
  background: white;
  color: #111827;
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
}

.hero-dots {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.hero-dot {
  width: 9px;
  height: 9px;
  padding: 0;
  border: none;
  border-radius: 999px;
  background: #cbd5e1;
  cursor: pointer;
}

.hero-dot.active {
  width: 26px;
  background: #2563eb;
}

.bank-summary-section,
.preview-section {
  margin-top: 38px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 16px;
  margin-bottom: 16px;
}

.section-header h3 {
  margin: 0 0 6px;
  color: #111827;
  font-size: 24px;
}

.section-header p {
  margin: 0;
  color: #6b7280;
  font-size: 14px;
  line-height: 1.6;
}

.all-link {
  flex-shrink: 0;
  color: #2563eb;
  font-weight: 800;
  text-decoration: none;
}

.bank-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 16px;
}

.bank-card {
  padding: 18px;
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  background: white;
  box-sizing: border-box;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
}

.bank-top {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  margin-bottom: 14px;
}

.bank-icon {
  display: inline-flex;
  width: 38px;
  height: 38px;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: #f3f4f6;
  font-size: 20px;
  flex-shrink: 0;
}

.bank-top h4 {
  margin: 0 0 4px;
  color: #111827;
  font-size: 17px;
}

.bank-top p {
  margin: 0;
  color: #2563eb;
  font-size: 13px;
  font-weight: 800;
}

.bank-description {
  margin: 0;
  color: #374151;
  font-size: 14px;
  line-height: 1.65;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 14px;
}

.tag-list span {
  padding: 5px 8px;
  border-radius: 999px;
  background: #eff6ff;
  color: #2563eb;
  font-size: 12px;
  font-weight: 800;
}

.preview-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.preview-card {
  padding: 20px;
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  background: white;
  box-sizing: border-box;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
}

.bank-name {
  margin: 0 0 10px;
  color: #6b7280;
  font-size: 13px;
  font-weight: 800;
}

.preview-card h4 {
  min-height: 44px;
  margin: 0 0 16px;
  color: #111827;
  font-size: 17px;
  line-height: 1.4;
}

.rate-bar {
  position: relative;
  height: 10px;
  margin-bottom: 16px;
  overflow: hidden;
  border-radius: 999px;
  background-color: #e5e7eb;
}

.rate-fill {
  position: absolute;
  inset: 0 auto 0 0;
  border-radius: 999px;
  background-color: #2563eb;
}

.product-info {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
  color: #374151;
  font-size: 14px;
}

.product-info strong {
  color: #111827;
  font-size: 20px;
  white-space: nowrap;
}

.join-way {
  min-height: 20px;
  margin: 0 0 16px;
  color: #6b7280;
  font-size: 13px;
}

.detail-link {
  display: block;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  color: #111827;
  text-align: center;
  font-weight: 800;
  text-decoration: none;
}

.detail-link:hover {
  border-color: #2563eb;
  color: #2563eb;
}

.message {
  color: #6b7280;
}

.error-message {
  padding: 14px;
  border-radius: 12px;
  background: #fef2f2;
  color: #dc2626;
  font-weight: 700;
}

.empty-box {
  padding: 24px;
  border: 1px dashed #d1d5db;
  border-radius: 18px;
  background: #f9fafb;
}

.empty-box h4 {
  margin: 0 0 8px;
  color: #111827;
}

.empty-box p {
  margin: 0;
  color: #6b7280;
}

@media (max-width: 1100px) {
  .bank-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 860px) {
  .preview-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .home-page {
    padding: 14px;
  }

  .primary-btn,
  .secondary-btn {
    width: 100%;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .bank-grid {
    grid-template-columns: 1fr;
  }

  .product-info {
    flex-direction: column;
  }
}
</style>
