<template>
  <div class="home-view">
    <section class="hero-card">
      <div class="hero-copy">
        <span class="eyebrow">JUYEON FINANCE GUIDE</span>
        <h1>
          내 금융생활의<br>
          <strong>주연이 되는 첫 은행 찾기</strong>
        </h1>

        <div class="hero-mascot" aria-hidden="true">
          <img :src="heroCharacterImage" alt="" />
        </div>

        <section
          class="feature-stage"
          aria-label="주요 기능 소개"
          @mouseenter="pauseFeatureSlider"
          @mouseleave="resumeFeatureSlider"
        >
          <button
            type="button"
            class="feature-arrow feature-arrow-prev"
            aria-label="이전 기능 보기"
            @click="prevFeatureSlide"
          >
            ‹
          </button>
          <button
            type="button"
            class="feature-arrow feature-arrow-next"
            aria-label="다음 기능 보기"
            @click="nextFeatureSlide"
          >
            ›
          </button>

          <Transition :name="featureTransitionName" mode="out-in">
            <article :key="currentFeatureSlide.key" class="feature-slide">
              <div class="feature-slide-top">
                <span class="feature-badge">{{ currentFeatureSlide.badge }}</span>
                <div class="feature-status">
                  <span class="feature-count">{{ currentFeatureIndex + 1 }} / {{ featureSlides.length }}</span>
                  <button
                    type="button"
                    class="feature-play-toggle"
                    :aria-label="isFeatureSliderPaused ? '기능 소개 자동 재생' : '기능 소개 일시정지'"
                    @click.stop="toggleFeatureSlider"
                  >
                    <span v-if="isFeatureSliderPaused">▶</span>
                    <span v-else>Ⅱ</span>
                  </button>
                </div>
              </div>

              <div class="feature-slide-content">
                <div class="feature-copy-stack">
                  <div class="feature-text">
                    <h2>{{ currentFeatureSlide.title }}</h2>
                    <p>{{ currentFeatureSlide.description }}</p>
                  </div>

                  <ul class="feature-points" aria-label="기능 핵심 포인트">
                    <li v-for="point in currentFeatureSlide.points" :key="point">{{ point }}</li>
                  </ul>
                </div>

                <div class="feature-actions">
                  <button type="button" class="btn-primary" @click="goFeaturePrimary">
                    {{ currentFeatureSlide.primaryLabel }}
                  </button>
                  <button
                    v-if="currentFeatureSlide.secondaryLabel"
                    type="button"
                    class="btn-secondary"
                    @click="goFeatureSecondary"
                  >
                    {{ currentFeatureSlide.secondaryLabel }}
                  </button>
                </div>
              </div>
            </article>
          </Transition>


          <div class="feature-dots" aria-label="기능 소개 슬라이드 선택">
            <button
              v-for="(slide, index) in featureSlides"
              :key="slide.key"
              type="button"
              :class="{ active: index === currentFeatureIndex }"
              :aria-label="`${slide.badge} 보기`"
              @click="selectFeatureSlide(index)"
            ></button>
          </div>
        </section>

        <p v-if="loginRequiredMessage" class="auth-required-message">
          {{ loginRequiredMessage }}
        </p>
      </div>

    </section>

    <section class="home-grid">
      <article class="card popular-products">
        <div class="section-heading compact">
          <div>
            <h3>금리 높은 금융상품</h3>
          </div>
          <RouterLink :to="{ name: 'products' }" class="section-link">전체 보기</RouterLink>
        </div>

        <p v-if="productLoading" class="state-message">상품을 불러오는 중입니다...</p>
        <p v-else-if="productError" class="state-message error">{{ productError }}</p>

        <template v-else>
          <div v-if="previewProductGroups.length" class="product-group-list">
            <section
              v-for="group in previewProductGroups"
              :key="group.type"
              class="product-group"
            >
              <div class="product-group-heading">
                <strong>{{ group.title }}</strong>
                <em>TOP 2</em>
              </div>

              <div class="product-list">
                <RouterLink
                  v-for="product in group.items"
                  :key="getProductKey(product)"
                  class="product-row"
                  :to="{
                    name: 'product-detail',
                    params: { id: product.id },
                    query: { type: product.product_type || group.type }
                  }"
                >
                  <div class="product-logo-stack">
                    <BankLogo :bank-name="getBankName(product)" :size="40" :rounded="13" />
                  </div>

                  <div class="product-main">
                    <strong>{{ product.name || '상품명 없음' }}</strong>
                    <p>{{ getBankName(product) }} · {{ getProductTerm(product) }}</p>
                  </div>

                  <em>{{ formatRate(product.max_interest_rate) }}</em>
                </RouterLink>
              </div>
            </section>
          </div>

          <div v-else class="empty-box">
            표시할 상품이 없습니다. 상품 저장 API를 먼저 실행해보세요.
          </div>
        </template>
      </article>

      <article class="card recommend-card">
        <div class="section-heading compact">
          <div>
            <h3>은행 추천 테스트</h3>
          </div>
        </div>

        <div class="process-steps">
          <div v-for="step in processSteps" :key="step.label" class="process-step">
            <span>{{ step.icon }}</span>
            <strong>{{ step.label }}</strong>
          </div>
        </div>


        <button type="button" class="btn-primary block-button" @click="goProtectedPage('main-bank')">
          테스트 시작하기
        </button>
      </article>

      <article class="card exchange-card">
        <div class="section-heading compact">
          <div>
            <h3>주요 환율</h3>
            <p>{{ exchangeDateText }}</p>
          </div>
          <RouterLink :to="{ name: 'exchange' }" class="section-link">자세히</RouterLink>
        </div>

        <p v-if="exchangeLoading" class="state-message">환율 정보를 불러오는 중입니다...</p>
        <p v-else-if="exchangeError" class="state-message error">{{ exchangeError }}</p>

        <template v-else>
          <div class="exchange-list">
            <div v-for="currency in previewCurrencies" :key="currency.code" class="exchange-row">
              <span>{{ currency.flag }}</span>
              <strong>{{ currency.code }}</strong>
              <p>{{ currency.name }}</p>
              <em>{{ currency.rateText }}</em>
            </div>
          </div>

          <div v-if="previewCurrencies.length === 0" class="empty-box">
            표시할 환율 정보가 없습니다.
          </div>
        </template>
      </article>

      <article class="card community-card">
        <div class="section-heading compact">
          <div>
            <h3>커뮤니티 최신 반응</h3>
          </div>
          <RouterLink :to="{ name: 'community' }" class="section-link">입장하기</RouterLink>
        </div>

        <p v-if="communityLoading" class="state-message">게시글을 불러오는 중입니다...</p>
        <p v-else-if="communityError" class="state-message error">{{ communityError }}</p>

        <div v-else class="post-list community-list">
          <RouterLink
            v-for="post in previewPosts"
            :key="post.id"
            :to="getPostLink(post)"
            class="post-row"
          >
            <span>{{ getCategoryIcon(post.category) }}</span>
            <div>
              <strong>{{ post.title }}</strong>
              <p>{{ getPostMeta(post) }}</p>
            </div>
          </RouterLink>

          <div v-if="previewPosts.length === 0" class="empty-box">
            아직 등록된 게시글이 없습니다.
          </div>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import * as productApi from '@/api/products'
import { getPosts } from '@/api/community'
import { getExchangeRates } from '@/api/exchanges'
import BankLogo from '@/components/BankLogo.vue'
import { getBankDisplayName } from '@/constants/bankLogoMap'
import heroCharacterImage from '@/assets/juyeon-character.png'


const router = useRouter()
const loginRequiredMessage = ref('')
let loginWarningTimer = null

const productLoading = ref(false)
const productError = ref('')
const depositProducts = ref([])
const savingProducts = ref([])

const exchangeLoading = ref(false)
const exchangeError = ref('')
const exchangeDate = ref('')
const exchangeRates = ref([])

const communityLoading = ref(false)
const communityError = ref('')
const communityPosts = ref([])

const processSteps = [
  { icon: '📝', label: '설문 시작' },
  { icon: '📊', label: '패턴 분석' },
  { icon: '🎯', label: '추천 결과' },
  { icon: '✅', label: '비교·선택' },
]

const featureSlides = [
  {
    key: 'recommend',
    badge: '맞춤추천',
    title: '내 조건에 맞는 예적금 상품 추천',
    description: '예치 금액, 저축 기간, 선호 은행을 기준으로 예금·적금 상품을 한눈에 비교합니다.',
    points: ['조건 기반 추천', '금리·기간 비교', '상품 상세 연결'],
    routeName: 'recommend',
    requiresAuth: true,
    primaryLabel: '맞춤 상품 추천받기',
    secondaryLabel: '전체 상품 보기',
    secondaryRouteName: 'products',
  },
  {
    key: 'main-bank',
    badge: '주거래은행',
    title: '내 금융생활의 첫 주거래은행 찾기',
    description: '금융성향 테스트와 주변 은행 정보를 함께 보고 첫 주거래은행을 선택합니다.',
    points: ['성향 테스트', '은행별 특징', '주변 지점 확인'],
    routeName: 'main-bank',
    requiresAuth: true,
    primaryLabel: '주거래은행 찾기',
    secondaryLabel: '맞춤추천 보기',
    secondaryRouteName: 'recommend',
    secondaryRequiresAuth: true,
  },
  {
    key: 'market',
    badge: '환율·금은',
    title: '주요 통화 시세와 금·은 가격 확인',
    description: '한국 원화 기준 환율 계산과 주요 통화, 금·은 가격 흐름을 함께 확인합니다.',
    points: ['KRW 기준 계산', '기간별 그래프', '금·은 시세'],
    routeName: 'exchange',
    primaryLabel: '환율 보러가기',
    secondaryLabel: '금·은 시세보기',
    secondaryRouteName: 'spot-assets',
  },
  {
    key: 'community',
    badge: '커뮤니티',
    title: '금융 고민과 상품 정보를 함께 공유',
    description: '예적금 후기와 은행 이용 경험, 금융 팁을 게시글과 댓글로 나눕니다.',
    points: ['게시글 작성', '댓글 소통', '좋아요 기반 반응'],
    routeName: 'community',
    primaryLabel: '커뮤니티 입장하기',
    secondaryLabel: '상품 먼저 보기',
    secondaryRouteName: 'products',
  },
]

const currentFeatureIndex = ref(0)
const currentFeatureDirection = ref('next')
const isFeatureSliderPaused = ref(false)
const FEATURE_SLIDE_INTERVAL = 4200
let featureSlideTimer = null

const currentFeatureSlide = computed(() => {
  return featureSlides[currentFeatureIndex.value] || featureSlides[0]
})

const featureTransitionName = computed(() => {
  return currentFeatureDirection.value === 'prev' ? 'feature-slide-prev' : 'feature-slide-next'
})

const stopFeatureSlider = () => {
  if (featureSlideTimer) {
    window.clearInterval(featureSlideTimer)
    featureSlideTimer = null
  }
}

const setFeatureSlide = (index, direction = 'next', restart = true) => {
  currentFeatureDirection.value = direction
  currentFeatureIndex.value = (index + featureSlides.length) % featureSlides.length

  if (restart) {
    startFeatureSlider()
  }
}

const startFeatureSlider = () => {
  stopFeatureSlider()

  if (isFeatureSliderPaused.value) {
    return
  }

  featureSlideTimer = window.setInterval(() => {
    setFeatureSlide(currentFeatureIndex.value + 1, 'next', false)
  }, FEATURE_SLIDE_INTERVAL)
}

const pauseFeatureSlider = () => {
  stopFeatureSlider()
}

const resumeFeatureSlider = () => {
  startFeatureSlider()
}

const toggleFeatureSlider = () => {
  isFeatureSliderPaused.value = !isFeatureSliderPaused.value

  if (isFeatureSliderPaused.value) {
    stopFeatureSlider()
    return
  }

  startFeatureSlider()
}

const nextFeatureSlide = () => {
  setFeatureSlide(currentFeatureIndex.value + 1, 'next')
}

const prevFeatureSlide = () => {
  setFeatureSlide(currentFeatureIndex.value - 1, 'prev')
}

const selectFeatureSlide = (index) => {
  if (index === currentFeatureIndex.value) {
    return
  }

  const direction = index > currentFeatureIndex.value ? 'next' : 'prev'
  setFeatureSlide(index, direction)
}

const moveToFeatureRoute = (routeName, requiresAuth = false) => {
  if (!routeName) {
    return
  }

  if (requiresAuth && !localStorage.getItem('token')) {
    showLoginRequiredMessage()
    return
  }

  router.push({ name: routeName })
}

const goFeaturePrimary = () => {
  const slide = currentFeatureSlide.value
  moveToFeatureRoute(slide.routeName, slide.requiresAuth)
}

const goFeatureSecondary = () => {
  const slide = currentFeatureSlide.value
  moveToFeatureRoute(slide.secondaryRouteName, slide.secondaryRequiresAuth)
}

const showLoginRequiredMessage = () => {
  loginRequiredMessage.value = '로그인 후 이용할 수 있습니다.'

  if (loginWarningTimer) {
    window.clearTimeout(loginWarningTimer)
  }

  loginWarningTimer = window.setTimeout(() => {
    loginRequiredMessage.value = ''
    loginWarningTimer = null
  }, 2200)
}

const goProtectedPage = (routeName) => {
  if (!localStorage.getItem('token')) {
    showLoginRequiredMessage()
    return
  }

  router.push({ name: routeName })
}

const currencyMeta = {
  USD: { flag: '🇺🇸', name: '미국 달러' },
  JPY: { flag: '🇯🇵', name: '일본 엔' },
  EUR: { flag: '🇪🇺', name: '유로' },
  CNY: { flag: '🇨🇳', name: '중국 위안' },
  GBP: { flag: '🇬🇧', name: '영국 파운드' },
}

const totalProductCount = computed(() => {
  return depositProducts.value.length + savingProducts.value.length
})

const sortProductsByRate = (products, productType) => {
  return products
    .map((item) => ({ ...item, product_type: productType }))
    .sort((a, b) => Number(b.max_interest_rate || 0) - Number(a.max_interest_rate || 0))
}

const topDepositProducts = computed(() => {
  return sortProductsByRate(depositProducts.value, 'deposit').slice(0, 2)
})

const topSavingProducts = computed(() => {
  return sortProductsByRate(savingProducts.value, 'saving').slice(0, 2)
})

const previewProductGroups = computed(() => {
  return [
    {
      type: 'deposit',
      title: '예금 금리 TOP',
      items: topDepositProducts.value,
    },
    {
      type: 'saving',
      title: '적금 금리 TOP',
      items: topSavingProducts.value,
    },
  ].filter((group) => group.items.length > 0)
})

const previewCurrencies = computed(() => {
  const preferredCodes = ['USD', 'JPY', 'EUR', 'CNY']

  return exchangeRates.value
    .filter((rate) => preferredCodes.includes(rate.code))
    .sort((a, b) => preferredCodes.indexOf(a.code) - preferredCodes.indexOf(b.code))
    .slice(0, 4)
})

const usdRate = computed(() => {
  return exchangeRates.value.find((rate) => rate.code === 'USD') || null
})

const exchangeDateText = computed(() => {
  if (exchangeDate.value) {
    return `${exchangeDate.value} 기준`
  }

  return '실시간 환율 데이터'
})

const previewPosts = computed(() => {
  return [...communityPosts.value]
    .sort((a, b) => {
      const scoreA = getPostScore(a)
      const scoreB = getPostScore(b)

      if (scoreB !== scoreA) {
        return scoreB - scoreA
      }

      return new Date(b.created_at || 0) - new Date(a.created_at || 0)
    })
    .slice(0, 6)
})

const normalizeProducts = (data) => {
  if (Array.isArray(data)) return data
  if (Array.isArray(data?.results)) return data.results
  if (Array.isArray(data?.products)) return data.products
  if (Array.isArray(data?.deposits)) return data.deposits
  if (Array.isArray(data?.savings)) return data.savings
  return []
}

const normalizePosts = (data) => {
  if (Array.isArray(data)) return data
  if (Array.isArray(data?.results)) return data.results
  if (Array.isArray(data?.posts)) return data.posts
  return []
}

const normalizeExchangeRates = (data) => {
  const rows = Array.isArray(data?.rates) ? data.rates : []

  return rows.map((rate) => {
    const code = rate.normalized_code || String(rate.currency_code || '').replace('(100)', '').trim()
    const meta = currencyMeta[code] || {}
    const ratePerUnit = Number(rate.rate_per_unit ?? rate.raw_rate ?? 0)

    return {
      code,
      flag: meta.flag || '💱',
      name: rate.currency_name || meta.name || code,
      ratePerUnit,
      rateText: `${formatNumber(ratePerUnit)}원`,
    }
  }).filter((rate) => rate.code && Number.isFinite(rate.ratePerUnit) && rate.ratePerUnit > 0)
}

const getProductKey = (product) => {
  return `${product.product_type}-${product.id || product.fin_prdt_cd || product.name}`
}

const getRawBankName = (product) => {
  return product.bank?.name || product.bank_name || product.kor_co_nm || '은행 정보 없음'
}

const getBankName = (product) => {
  return getBankDisplayName(getRawBankName(product)) || '은행 정보 없음'
}

const getProductTypeLabel = (product) => {
  return product.product_type === 'saving' ? '적금' : '예금'
}

const getProductTone = (product) => {
  return product.product_type === 'saving' ? 'purple' : 'mint'
}

const getProductTerm = (product) => {
  const terms = product.options
    ?.map((option) => Number(option.save_trm))
    .filter((term) => Number.isFinite(term))

  if (!terms || terms.length === 0) {
    return '가입기간 확인'
  }

  const minTerm = Math.min(...terms)
  const maxTerm = Math.max(...terms)

  return minTerm === maxTerm ? `${minTerm}개월` : `${minTerm}~${maxTerm}개월`
}

const formatRate = (rate) => {
  if (rate === null || rate === undefined || rate === '') {
    return '정보 없음'
  }

  return `연 ${Number(rate).toFixed(2)}%`
}

const formatNumber = (number) => {
  if (!Number.isFinite(Number(number))) {
    return '-'
  }

  return Number(number).toLocaleString('ko-KR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
}

const getPostScore = (post) => {
  return Number(post.like_count || 0) * 3 + Number(post.comment_count || 0) * 2 + Number(post.view_count || 0)
}

const getCategoryIcon = (category) => {
  const icons = {
    free: '💬',
    product: '💳',
    review: '⭐',
    tip: '💡',
  }

  return icons[category] || '📌'
}

const getPostMeta = (post) => {
  const likeCount = Number(post.like_count || 0)
  const commentCount = Number(post.comment_count || 0)
  const viewCount = Number(post.view_count || 0)
  const timeText = getRelativeTime(post.created_at)

  return `좋아요 ${likeCount} · 댓글 ${commentCount} · 조회 ${viewCount}${timeText ? ` · ${timeText}` : ''}`
}

const getRelativeTime = (value) => {
  if (!value) {
    return ''
  }

  const created = new Date(value)

  if (Number.isNaN(created.getTime())) {
    return ''
  }

  const diffMs = Date.now() - created.getTime()
  const diffMinutes = Math.floor(diffMs / 1000 / 60)

  if (diffMinutes < 1) return '방금 전'
  if (diffMinutes < 60) return `${diffMinutes}분 전`

  const diffHours = Math.floor(diffMinutes / 60)
  if (diffHours < 24) return `${diffHours}시간 전`

  const diffDays = Math.floor(diffHours / 24)
  if (diffDays < 7) return `${diffDays}일 전`

  return created.toLocaleDateString('ko-KR')
}

const getPostLink = (post) => {
  if (!post?.id) {
    return { name: 'community' }
  }

  return {
    path: '/community',
    query: {
      post: post.id,
    },
  }
}

const fetchPreviewProducts = async () => {
  productLoading.value = true
  productError.value = ''

  try {
    const [depositResult, savingResult] = await Promise.allSettled([
      productApi.getDepositProducts(),
      productApi.getSavingProducts(),
    ])

    if (depositResult.status === 'fulfilled') {
      depositProducts.value = normalizeProducts(depositResult.value.data)
    }

    if (savingResult.status === 'fulfilled') {
      savingProducts.value = normalizeProducts(savingResult.value.data)
    }

    if (depositResult.status === 'rejected' && savingResult.status === 'rejected') {
      productError.value = '상품 정보를 불러오지 못했습니다. 백엔드 서버와 상품 API를 확인해주세요.'
    }
  } catch (error) {
    console.error(error)
    productError.value = '상품 정보를 불러오지 못했습니다.'
  } finally {
    productLoading.value = false
  }
}

const fetchExchangeSummary = async () => {
  exchangeLoading.value = true
  exchangeError.value = ''

  try {
    const response = await getExchangeRates()

    exchangeDate.value = response.data?.date || ''
    exchangeRates.value = normalizeExchangeRates(response.data)
  } catch (error) {
    console.error(error)
    exchangeError.value = error.response?.data?.message || '환율 정보를 불러오지 못했습니다. EXCHANGE_API_KEY와 백엔드 서버를 확인해주세요.'
  } finally {
    exchangeLoading.value = false
  }
}

const fetchCommunitySummary = async () => {
  communityLoading.value = true
  communityError.value = ''

  try {
    const response = await getPosts()
    communityPosts.value = normalizePosts(response.data)
  } catch (error) {
    console.error(error)
    communityError.value = '커뮤니티 글을 불러오지 못했습니다.'
  } finally {
    communityLoading.value = false
  }
}

onMounted(() => {
  fetchPreviewProducts()
  fetchExchangeSummary()
  fetchCommunitySummary()
  startFeatureSlider()
})

onBeforeUnmount(() => {
  stopFeatureSlider()

  if (loginWarningTimer) {
    window.clearTimeout(loginWarningTimer)
  }
})
</script>

<style scoped>
.home-view {
  width: min(var(--container-width), calc(100% - 48px));
  margin: 0 auto;
  padding: 42px 0 64px;
}

.hero-card {
  position: relative;
  display: block;
  padding: clamp(30px, 4.6vw, 54px);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.97), rgba(244, 248, 255, 0.98)),
    radial-gradient(circle at 86% 16%, rgba(16, 185, 129, 0.14), transparent 34%);
  box-shadow: var(--shadow-card);
  overflow: hidden;
}

.eyebrow {
  display: inline-flex;
  margin-bottom: 12px;
  color: var(--color-primary);
  font-size: 12px;
  font-weight: 950;
  letter-spacing: 0.11em;
}

.hero-copy {
  width: 100%;
  min-width: 0;
  max-width: none;
}

.hero-copy h1 {
  max-width: 760px;
  margin: 0;
  color: var(--color-text);
  font-size: clamp(36px, 4.8vw, 58px);
  line-height: 1.16;
  font-weight: 950;
  letter-spacing: -0.07em;
  word-break: keep-all;
}

.hero-copy h1 strong {
  color: var(--color-primary);
  font-weight: 950;
}

.hero-mascot {
  position: absolute;
  top: clamp(18px, 3vw, 34px);
  right: clamp(34px, 5.6vw, 76px);
  z-index: 1;
  width: clamp(150px, 17vw, 230px);
  max-height: 182px;
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  pointer-events: none;
}

.hero-mascot::before {
  content: '';
  position: absolute;
  right: 8%;
  top: 12%;
  width: 86%;
  height: 76%;
  border-radius: 999px;
  background: radial-gradient(circle, rgba(37, 99, 235, 0.10), transparent 68%);
  filter: blur(8px);
}

.hero-mascot img {
  position: relative;
  z-index: 1;
  width: 100%;
  height: auto;
  max-height: 182px;
  object-fit: contain;
  object-position: center top;
  filter: drop-shadow(0 18px 28px rgba(15, 23, 42, 0.12));
  user-select: none;
}

.hero-copy p {
  max-width: 700px;
  margin: 18px 0 0;
  color: var(--color-text-muted);
  font-size: 17px;
  line-height: 1.76;
  word-break: keep-all;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 30px;
}

.hero-actions .btn-primary,
.hero-actions .btn-secondary {
  min-width: 190px;
}

.feature-stage {
  position: relative;
  width: 100%;
  box-sizing: border-box;
  min-height: 386px;
  margin-top: 28px;
  padding: 40px 92px 70px;
  border: 1px solid rgba(37, 99, 235, 0.18);
  border-radius: 28px;
  background:
    radial-gradient(circle at 88% 14%, rgba(255, 255, 255, 0.34), transparent 34%),
    radial-gradient(circle at 12% 0%, rgba(255, 255, 255, 0.18), transparent 28%),
    linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #38bdf8 100%);
  box-shadow: 0 26px 58px rgba(37, 99, 235, 0.24);
  overflow: hidden;
}

.feature-stage::before {
  content: '';
  position: absolute;
  inset: auto -74px -112px auto;
  width: 286px;
  height: 286px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.16);
  pointer-events: none;
}

.feature-stage::after {
  content: '';
  position: absolute;
  inset: -88px auto auto -72px;
  width: 232px;
  height: 232px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.10);
  pointer-events: none;
}

.feature-slide {
  position: relative;
  z-index: 3;
  display: flex;
  flex-direction: column;
  min-height: 276px;
  color: #fff;
}

.feature-slide-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.feature-badge,
.feature-count,
.feature-play-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 30px;
  padding: 0 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.18);
  color: rgba(255, 255, 255, 0.94);
  font-size: 12px;
  font-weight: 950;
  letter-spacing: -0.01em;
  white-space: nowrap;
}

.feature-status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.feature-count {
  background: rgba(15, 23, 42, 0.16);
}

.feature-play-toggle {
  width: 34px;
  min-width: 34px;
  padding: 0;
  border: 0;
  cursor: pointer;
  font-family: inherit;
  line-height: 1;
  background: rgba(15, 23, 42, 0.18);
  transition: background 0.18s ease, transform 0.18s ease;
}

.feature-play-toggle:hover {
  background: rgba(15, 23, 42, 0.26);
  transform: translateY(-1px);
}

.feature-slide-content {
  position: relative;
  display: block;
  flex: 1;
  min-height: 220px;
  padding-top: 36px;
}

.feature-copy-stack {
  min-width: 0;
  max-width: calc(100% - 92px);
  padding-top: 18px;
}

.feature-text {
  width: 100%;
  max-width: 100%;
}

.feature-text h2 {
  margin: 0;
  color: #fff;
  font-size: clamp(32px, 3.45vw, 48px);
  line-height: 1.13;
  font-weight: 950;
  letter-spacing: -0.055em;
  word-break: keep-all;
  overflow-wrap: normal;
  white-space: nowrap;
}

.feature-text p {
  max-width: 940px;
  margin: 18px 0 0;
  color: rgba(255, 255, 255, 0.91);
  font-size: 16px;
  line-height: 1.68;
  word-break: keep-all;
  white-space: nowrap;
}

.feature-points {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 26px 0 0;
  padding: 0;
  list-style: none;
}

.feature-points li {
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 0 13px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.16);
  color: rgba(255, 255, 255, 0.95);
  font-size: 13px;
  font-weight: 850;
  white-space: nowrap;
}

.feature-actions {
  position: absolute;
  right: 0;
  bottom: 2px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 12px;
  width: 260px;
  margin: 0;
  padding-top: 0;
}

.feature-actions .btn-primary,
.feature-actions .btn-secondary {
  width: 100%;
  min-width: 0;
  height: 48px;
  border: 0;
  cursor: pointer;
  font-family: inherit;
  justify-content: center;
}

.feature-actions .btn-primary {
  background: #fff;
  color: var(--color-primary);
  box-shadow: 0 16px 34px rgba(15, 23, 42, 0.18);
}

.feature-actions .btn-primary:hover {
  transform: translateY(-1px);
  background: #f8fbff;
}

.feature-actions .btn-secondary {
  background: rgba(255, 255, 255, 0.14);
  color: #fff;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.2);
}

.feature-stage > button.feature-arrow {
  all: unset;
  position: absolute;
  top: 50%;
  z-index: 8;
  width: 58px;
  height: 96px;
  box-sizing: border-box;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  color: rgba(255, 255, 255, 0.94);
  font-size: 62px;
  font-weight: 700;
  line-height: 1;
  cursor: pointer;
  text-shadow: 0 8px 24px rgba(15, 23, 42, 0.24);
  transform: translateY(-50%);
  transition: transform 0.18s ease, color 0.18s ease, background 0.18s ease;
}

.feature-stage > button.feature-arrow:hover {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  transform: translateY(-50%) scale(1.04);
}

.feature-stage > button.feature-arrow-prev {
  left: 18px;
}

.feature-stage > button.feature-arrow-next {
  right: 18px;
}


.feature-dots {
  position: absolute;
  left: 50%;
  bottom: 24px;
  transform: translateX(-50%);
  z-index: 2;
  display: inline-flex;
  align-items: center;
  gap: 7px;
}

.feature-dots button {
  width: 8px;
  height: 8px;
  padding: 0;
  border: 0;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.48);
  cursor: pointer;
  transition: width 0.2s ease, background 0.2s ease;
}

.feature-dots button.active {
  width: 26px;
  background: #fff;
}

.feature-slide-next-enter-active,
.feature-slide-next-leave-active,
.feature-slide-prev-enter-active,
.feature-slide-prev-leave-active {
  transition: opacity 0.28s ease, transform 0.28s ease;
}

.feature-slide-next-enter-from {
  opacity: 0;
  transform: translateX(72px);
}

.feature-slide-next-leave-to {
  opacity: 0;
  transform: translateX(-72px);
}

.feature-slide-prev-enter-from {
  opacity: 0;
  transform: translateX(-72px);
}

.feature-slide-prev-leave-to {
  opacity: 0;
  transform: translateX(72px);
}

@media (max-width: 1040px) {
  .feature-stage {
    padding: 36px 72px 66px;
  }

  .feature-slide-content {
    display: block;
    min-height: auto;
    padding-top: 28px;
  }

  .feature-copy-stack {
    max-width: 100%;
  }

  .feature-text p {
    white-space: normal;
  }

  .feature-actions {
    position: static;
    flex-direction: row;
    width: auto;
    margin-top: 28px;
  }

  .feature-actions .btn-primary,
  .feature-actions .btn-secondary {
    width: auto;
    min-width: 172px;
  }

  .feature-text h2 {
    white-space: normal;
  }
}

.hero-panel {
  display: flex;
  flex-direction: column;
  gap: 18px;
  padding: 24px;
  border: 1px solid var(--color-border);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.86);
  box-shadow: var(--shadow-soft);
}

.panel-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
}

.panel-header span,
.metric-grid span {
  color: var(--color-text-muted);
  font-size: 12px;
  font-weight: 850;
}

.panel-header strong {
  color: var(--color-text);
  font-size: 14px;
  font-weight: 950;
  text-align: right;
}

.metric-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}

.metric-grid div {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  border: 1px solid var(--color-border);
  border-radius: 16px;
  background: var(--color-surface);
}

.metric-grid strong {
  color: var(--color-primary);
  font-size: 20px;
  font-weight: 950;
}

.flow-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.flow-list li {
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 48px;
  padding: 10px;
  border-radius: 14px;
  background: var(--color-primary-soft);
  color: var(--color-primary);
}

.flow-list span {
  font-size: 18px;
}

.flow-list strong {
  font-size: 13px;
  font-weight: 900;
}

.home-grid {
  display: grid;
  grid-template-columns: 1.08fr 0.92fr;
  gap: 18px;
  margin-top: 22px;
}

.home-grid > .card {
  padding: 22px;
}

.popular-products {
  grid-row: span 2;
}

.community-card {
  grid-column: 1 / -1;
}

.section-heading.compact {
  margin-bottom: 16px;
}

.section-heading.compact h3 {
  font-size: 21px;
}

.section-heading.compact p {
  font-size: 13px;
}

.product-group-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.product-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.product-group + .product-group {
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
}

.product-group-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.product-group-heading strong {
  color: var(--color-text);
  font-size: 16px;
  font-weight: 950;
}

.product-group-heading em {
  padding: 6px 10px;
  border-radius: 999px;
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-size: 12px;
  font-style: normal;
  font-weight: 950;
  white-space: nowrap;
}

.product-list,
.exchange-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.product-row {
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr) auto;
  gap: 10px;
  align-items: center;
  min-height: 74px;
  padding: 12px 16px;
  border: 1px solid var(--color-border);
  border-radius: 18px;
  background: var(--color-surface-soft);
}

.product-row:hover {
  border-color: var(--color-border-strong);
  background: #fff;
}

.product-logo-stack {
  display: flex;
  align-items: center;
  justify-content: center;
  align-self: center;
}

.product-row :deep(.bank-logo) {
  background: #fff;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
}

.product-row :deep(.bank-logo__img) {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.product-main {
  min-width: 0;
  align-self: center;
}

.product-main strong {
  display: block;
  color: var(--color-text);
  font-size: 15px;
  font-weight: 950;
  line-height: 1.24;
}

.product-main p {
  margin: 4px 0 0;
  color: var(--color-text-muted);
  font-size: 13px;
  line-height: 1.2;
}

.product-row em {
  align-self: center;
  color: var(--color-accent);
  font-size: 20px;
  font-style: normal;
  font-weight: 950;
  white-space: nowrap;
}

.recommend-card {
  align-self: start;
  padding-bottom: 16px !important;
}

.recommend-card .section-heading.compact {
  margin-bottom: 18px;
}

.process-steps {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.process-step {
  min-height: 96px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 8px;
  padding: 12px 8px;
  border: 1px solid var(--color-border);
  border-radius: 18px;
  background: var(--color-surface-soft);
  text-align: center;
}

.process-step span {
  font-size: 31px;
  line-height: 1;
}

.process-step strong {
  font-size: 14px;
  font-weight: 950;
}

.block-button {
  width: 100%;
  min-height: 48px;
  margin-top: 18px;
  margin-bottom: 0;
}

.exchange-row {
  display: grid;
  grid-template-columns: 32px 48px minmax(0, 1fr) auto;
  gap: 8px;
  align-items: center;
  padding: 11px 0;
  border-bottom: 1px solid var(--color-border);
}

.exchange-row:last-child {
  border-bottom: 0;
}

.exchange-row strong,
.exchange-row em {
  font-weight: 950;
  font-style: normal;
}

.exchange-row p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 13px;
}

.community-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px 16px;
}

.post-row {
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr);
  gap: 12px;
  align-items: center;
  min-height: 68px;
  padding: 12px;
  border: 1px solid var(--color-border);
  border-radius: 16px;
  background: var(--color-surface-soft);
}

.post-row:hover {
  border-color: var(--color-border-strong);
  background: #fff;
}

.post-row > span {
  width: 42px;
  height: 42px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  background: var(--color-primary-soft);
}

.post-row strong {
  display: block;
  color: var(--color-text);
  font-size: 14px;
  font-weight: 900;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.post-row p {
  margin: 3px 0 0;
  color: var(--color-text-light);
  font-size: 12px;
}

.state-message,
.empty-box {
  padding: 16px;
  border-radius: 15px;
  background: var(--color-surface-soft);
  color: var(--color-text-muted);
}

.state-message.error {
  background: #fff1f2;
  color: var(--color-danger);
  font-weight: 800;
}


.auth-required-message {
  display: inline-flex;
  align-items: center;
  min-height: 40px;
  margin: 16px 0 0;
  padding: 0 14px;
  border: 1px solid #fecaca;
  border-radius: 14px;
  background: #fff5f5;
  color: var(--color-danger);
  font-size: 14px;
  font-weight: 950;
}

button.btn-primary,
button.btn-secondary {
  border: 0;
  cursor: pointer;
  font-family: inherit;
}

@media (max-width: 980px) {
  .hero-mascot {
    opacity: 0.55;
    width: 150px;
  }

  .feature-text h2 {
    white-space: normal;
  }
}

@media (max-width: 1120px) {
  .hero-card,
  .home-grid {
    grid-template-columns: 1fr;
  }

  .popular-products,
  .community-card {
    grid-row: auto;
    grid-column: auto;
  }
}

@media (max-width: 760px) {
  .hero-mascot {
    display: none;
  }

  .home-view {
    width: min(100% - 28px, var(--container-width));
    padding-top: 24px;
  }

  .hero-card {
    padding: 26px 20px;
  }

  .feature-stage {
    min-height: 420px;
    padding: 24px 22px 84px;
  }

  .feature-slide {
    min-height: 312px;
  }

  .feature-slide-main {
    margin-top: 30px;
  }

  .feature-stage > button.feature-arrow {
    top: auto;
    bottom: 18px;
    width: 48px;
    height: 52px;
    font-size: 46px;
    transform: none;
  }

  .feature-stage > button.feature-arrow:hover {
    transform: scale(1.04);
  }

  .feature-stage > button.feature-arrow-prev {
    left: 18px;
  }

  .feature-stage > button.feature-arrow-next {
    right: 18px;
  }

  .feature-actions,
  .feature-actions .btn-primary,
  .feature-actions .btn-secondary {
    width: 100%;
  }

  .feature-dots {
    bottom: 34px;
  }

  .hero-actions,
  .hero-actions .btn-primary,
  .hero-actions .btn-secondary {
    width: 100%;
  }

  .flow-list,
  .community-list {
    grid-template-columns: 1fr;
  }

  .product-row {
    grid-template-columns: 42px minmax(0, 1fr);
    gap: 10px;
  }

  .product-row em {
    grid-column: 2;
    justify-self: start;
    margin-top: 2px;
  }

  .process-steps {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
