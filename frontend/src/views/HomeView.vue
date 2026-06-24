<template>
  <div class="home-view">
    <section class="hero-section">
      <div class="hero-content">
        <span class="eyebrow">FIRST FINANCE GUIDE</span>
        <h1>
          사회초년생을 위한<br>
          <strong>금융생활 시작 가이드</strong>
        </h1>
        <p>
          실제 금융상품, 환율, 커뮤니티 데이터를 한 화면에서 확인하고
          나에게 맞는 금융생활을 시작해보세요.
        </p>

        <div class="hero-actions">
          <RouterLink :to="{ name: 'recommend' }" class="btn-primary">
            나에게 맞는 상품 찾기
            <span>→</span>
          </RouterLink>
          <RouterLink :to="{ name: 'main-bank' }" class="btn-secondary">
            은행 추천 받기
          </RouterLink>
        </div>
      </div>

      <div class="hero-visual" aria-hidden="true">
        <div class="visual-card chart-card">
          <span>등록 금융상품</span>
          <strong>{{ productLoading ? '조회 중' : `${totalProductCount}개` }}</strong>
          <div class="mini-chart">
            <i></i><i></i><i></i><i></i><i></i>
          </div>
        </div>
        <div class="person-card">
          <div class="person-face">🙂</div>
          <div>
            <strong>실시간 데이터 요약</strong>
            <span>상품 · 환율 · 커뮤니티</span>
          </div>
        </div>
        <div class="coin-stack">₩</div>
        <div class="piggy">🐷</div>
      </div>
    </section>

    <section class="feature-grid" aria-label="주요 기능">
      <RouterLink
        v-for="feature in features"
        :key="feature.title"
        :to="feature.to"
        class="feature-card"
      >
        <span class="feature-icon" :class="feature.tone">{{ feature.icon }}</span>
        <div>
          <h2>{{ feature.title }}</h2>
          <p>{{ feature.description }}</p>
        </div>
        <strong>›</strong>
      </RouterLink>
    </section>

    <section class="dashboard-grid">
      <article class="card popular-products">
        <div class="section-heading compact">
          <div>
            <h3>인기 금융 상품</h3>
            <p>DB에 저장된 예금·적금 중 최고 금리 기준으로 보여줍니다.</p>
          </div>
          <RouterLink :to="{ name: 'products' }" class="section-link">더보기</RouterLink>
        </div>

        <p v-if="productLoading" class="state-message">상품을 불러오는 중입니다...</p>
        <p v-else-if="productError" class="state-message error">{{ productError }}</p>

        <div v-else class="product-list">
          <RouterLink
            v-for="product in previewProducts"
            :key="getProductKey(product)"
            class="product-row"
            :to="{
              name: 'product-detail',
              params: { id: product.id },
              query: { type: product.product_type || 'deposit' }
            }"
          >
            <span class="product-icon" :class="getProductTone(product)">
              {{ getProductIcon(product) }}
            </span>
            <div class="product-main">
              <div>
                <span class="badge" :class="getProductTone(product)">
                  {{ getProductTypeLabel(product) }}
                </span>
                <strong>{{ product.name || '상품명 없음' }}</strong>
              </div>
              <p>{{ getBankName(product) }} · {{ getProductTerm(product) }}</p>
            </div>
            <em>{{ formatRate(product.max_interest_rate) }}</em>
          </RouterLink>

          <div v-if="previewProducts.length === 0" class="empty-box">
            표시할 상품이 없습니다. 상품 저장 API를 먼저 실행해보세요.
          </div>
        </div>
      </article>

      <article class="card recommend-process">
        <div class="section-heading compact">
          <div>
            <h3>은행 추천, 이렇게 진행돼요</h3>
            <p>간단한 입력으로 맞춤 주거래은행을 찾습니다.</p>
          </div>
        </div>

        <div class="process-steps">
          <div v-for="step in processSteps" :key="step.label" class="process-step">
            <span>{{ step.icon }}</span>
            <strong>{{ step.label }}</strong>
          </div>
        </div>

        <p class="process-copy">
          3분이면 충분합니다. 금융 생활 패턴과 접근성을 분석해 가장 적합한 은행을 추천합니다.
        </p>

        <RouterLink :to="{ name: 'main-bank' }" class="btn-primary process-button">
          은행 추천 테스트 시작하기
        </RouterLink>
      </article>

      <article class="card exchange-card">
        <div class="section-heading compact">
          <div>
            <h3>오늘의 환율</h3>
            <p>{{ exchangeDateText }}</p>
          </div>
          <RouterLink :to="{ name: 'exchange' }" class="section-link">더보기</RouterLink>
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
              <b class="base">기준</b>
            </div>
          </div>

          <div v-if="usdRate" class="converter-preview">
            <span>USD</span>
            <strong>1</strong>
            <span>=</span>
            <strong>{{ formatNumber(usdRate.ratePerUnit) }}</strong>
            <span>KRW</span>
          </div>

          <div v-if="previewCurrencies.length === 0" class="empty-box">
            표시할 환율 정보가 없습니다.
          </div>
        </template>
      </article>

      <article class="card community-card">
        <div class="section-heading compact">
          <div>
            <h3>커뮤니티 인기 글</h3>
            <p>실제 게시판 글을 반응 순으로 보여줍니다.</p>
          </div>
          <RouterLink :to="{ name: 'community' }" class="section-link">더보기</RouterLink>
        </div>

        <p v-if="communityLoading" class="state-message">게시글을 불러오는 중입니다...</p>
        <p v-else-if="communityError" class="state-message error">{{ communityError }}</p>

        <div v-else class="post-list">
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

    <section class="promo-card">
      <div class="promo-icon">📊</div>
      <div>
        <strong>실제 데이터 기반 금융 요약</strong>
        <p>
          현재 상품 {{ totalProductCount }}개,
          커뮤니티 글 {{ communityPosts.length }}개를 기준으로 홈 화면을 구성합니다.
        </p>
      </div>
      <RouterLink :to="{ name: 'products' }" class="btn-secondary">상품 보러가기</RouterLink>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import * as productApi from '@/api/products'
import { getPosts } from '@/api/community'
import { getExchangeRates } from '@/api/exchanges'

const router = useRouter()

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

const features = [
  {
    icon: '💳',
    tone: 'mint',
    title: '예적금 추천',
    description: '실제 금감원 상품 데이터를 비교하고 추천받아요.',
    to: { name: 'products' },
  },
  {
    icon: '🏦',
    tone: 'blue',
    title: '주거래은행 추천',
    description: '나의 생활 패턴과 접근성에 맞는 은행을 찾아드려요.',
    to: { name: 'main-bank' },
  },
  {
    icon: '💱',
    tone: 'green',
    title: '환율 계산/시세 확인',
    description: '한국수출입은행 환율 데이터를 기반으로 계산해요.',
    to: { name: 'exchange' },
  },
  {
    icon: '💬',
    tone: 'purple',
    title: '금융 커뮤니티',
    description: '실제 게시글과 댓글로 금융 고민을 나눠보세요.',
    to: { name: 'community' },
  },
]

const processSteps = [
  { icon: '📝', label: '설문 시작' },
  { icon: '📊', label: '패턴 분석' },
  { icon: '🎯', label: '추천 결과' },
  { icon: '✅', label: '비교·선택' },
]

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

const previewProducts = computed(() => {
  const deposits = depositProducts.value.map((item) => ({ ...item, product_type: 'deposit' }))
  const savings = savingProducts.value.map((item) => ({ ...item, product_type: 'saving' }))

  return [...deposits, ...savings]
    .sort((a, b) => Number(b.max_interest_rate || 0) - Number(a.max_interest_rate || 0))
    .slice(0, 3)
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
    .slice(0, 4)
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

const getBankName = (product) => {
  return product.bank?.name || product.bank_name || product.kor_co_nm || '은행 정보 없음'
}

const getProductTypeLabel = (product) => {
  return product.product_type === 'saving' ? '적금' : '예금'
}

const getProductTone = (product) => {
  return product.product_type === 'saving' ? 'purple' : 'mint'
}

const getProductIcon = (product) => {
  return product.product_type === 'saving' ? '📁' : '💼'
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
  if (router.hasRoute('post-detail')) {
    return {
      name: 'post-detail',
      params: { id: post.id },
    }
  }

  return { name: 'community' }
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
})
</script>

<style scoped>
.home-view {
  width: min(var(--container-width), calc(100% - 48px));
  margin: 0 auto;
  padding: 42px 0 58px;
}

.hero-section {
  min-height: 360px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 520px;
  gap: 42px;
  align-items: center;
  padding: clamp(32px, 5vw, 58px);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.92), rgba(244, 247, 255, 0.96)),
    radial-gradient(circle at 78% 32%, rgba(36, 199, 174, 0.17), transparent 30%);
  box-shadow: var(--shadow-card);
  overflow: hidden;
}

.eyebrow {
  display: inline-flex;
  margin-bottom: 12px;
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 1000;
  letter-spacing: 0.08em;
}

.hero-content h1 {
  margin: 0;
  color: var(--color-text);
  font-size: clamp(34px, 4.8vw, 58px);
  line-height: 1.18;
  font-weight: 1000;
  letter-spacing: -0.07em;
}

.hero-content h1 strong {
  color: var(--color-primary);
  font-weight: 1000;
}

.hero-content p {
  max-width: 560px;
  margin: 22px 0 0;
  color: var(--color-text-muted);
  font-size: 17px;
  line-height: 1.75;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 32px;
}

.hero-actions .btn-primary,
.hero-actions .btn-secondary {
  min-width: 190px;
}

.hero-visual {
  position: relative;
  min-height: 290px;
}

.visual-card,
.person-card,
.coin-stack,
.piggy {
  position: absolute;
  border: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: var(--shadow-soft);
}

.chart-card {
  top: 4px;
  left: 42px;
  width: 190px;
  padding: 20px;
  border-radius: 24px;
}

.chart-card span,
.person-card span {
  display: block;
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 800;
}

.chart-card strong {
  display: block;
  margin: 6px 0 14px;
  color: var(--color-primary);
  font-size: 34px;
  font-weight: 1000;
}

.mini-chart {
  display: flex;
  align-items: end;
  gap: 6px;
  height: 58px;
}

.mini-chart i {
  width: 20%;
  border-radius: 999px;
  background: linear-gradient(180deg, var(--color-accent), var(--color-primary));
}

.mini-chart i:nth-child(1) { height: 34%; }
.mini-chart i:nth-child(2) { height: 52%; }
.mini-chart i:nth-child(3) { height: 42%; }
.mini-chart i:nth-child(4) { height: 72%; }
.mini-chart i:nth-child(5) { height: 92%; }

.person-card {
  right: 16px;
  top: 74px;
  width: 300px;
  min-height: 160px;
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 26px;
  border-radius: 34px;
}

.person-face {
  width: 92px;
  height: 92px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 28px;
  background: linear-gradient(135deg, var(--color-primary-soft), var(--color-accent-soft));
  font-size: 48px;
}

.person-card strong {
  display: block;
  color: var(--color-text);
  font-size: 20px;
  font-weight: 1000;
}

.coin-stack {
  right: 84px;
  bottom: 14px;
  width: 86px;
  height: 86px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 28px;
  background: #fff8e6;
  color: var(--color-orange);
  font-size: 42px;
  font-weight: 1000;
}

.piggy {
  left: 94px;
  bottom: 32px;
  width: 92px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: var(--color-accent-soft);
  font-size: 42px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin-top: 22px;
}

.feature-card {
  min-height: 118px;
  display: grid;
  grid-template-columns: 58px minmax(0, 1fr) 18px;
  gap: 14px;
  align-items: center;
  padding: 20px;
  border: 1px solid var(--color-border);
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: var(--shadow-soft);
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.feature-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-card);
}

.feature-icon,
.product-icon {
  width: 56px;
  height: 56px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 19px;
  font-size: 25px;
}

.feature-icon.mint,
.product-icon.mint {
  background: var(--color-accent-soft);
}

.feature-icon.blue {
  background: var(--color-primary-soft);
}

.feature-icon.green {
  background: #e9f9ef;
}

.feature-icon.purple,
.product-icon.purple {
  background: #f2ebff;
}

.feature-card h2 {
  margin: 0 0 6px;
  color: var(--color-text);
  font-size: 18px;
  font-weight: 1000;
}

.feature-card p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 14px;
  line-height: 1.5;
}

.feature-card > strong {
  color: var(--color-text);
  font-size: 30px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1.15fr 1fr 0.9fr;
  gap: 18px;
  margin-top: 22px;
}

.dashboard-grid > .card {
  padding: 22px;
}

.popular-products {
  grid-row: span 2;
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

.product-list,
.post-list,
.exchange-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.product-row {
  display: grid;
  grid-template-columns: 56px minmax(0, 1fr) auto;
  gap: 14px;
  align-items: center;
  padding: 14px;
  border: 1px solid var(--color-border);
  border-radius: 18px;
  background: var(--color-surface-soft);
}

.product-main strong {
  display: block;
  margin-top: 5px;
  color: var(--color-text);
  font-size: 16px;
  font-weight: 1000;
}

.product-main p {
  margin: 4px 0 0;
  color: var(--color-text-muted);
  font-size: 13px;
}

.product-row em {
  color: var(--color-accent);
  font-size: 21px;
  font-style: normal;
  font-weight: 1000;
  white-space: nowrap;
}

.process-steps {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-top: 8px;
}

.process-step {
  min-height: 88px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 8px;
  border: 1px solid var(--color-border);
  border-radius: 18px;
  background: var(--color-surface-soft);
  text-align: center;
}

.process-step span {
  font-size: 28px;
}

.process-step strong {
  font-size: 13px;
  font-weight: 1000;
}

.process-copy {
  margin: 18px 0;
  color: var(--color-text-muted);
}

.process-button {
  width: 100%;
}

.exchange-row {
  display: grid;
  grid-template-columns: 34px 48px minmax(0, 1fr) auto auto;
  gap: 8px;
  align-items: center;
  padding: 11px 0;
  border-bottom: 1px solid var(--color-border);
}

.exchange-row:last-child {
  border-bottom: 0;
}

.exchange-row strong,
.exchange-row em,
.exchange-row b {
  font-weight: 1000;
  font-style: normal;
}

.exchange-row p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 13px;
}

.exchange-row b.base {
  padding: 3px 8px;
  border-radius: 999px;
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-size: 12px;
}

.converter-preview {
  display: grid;
  grid-template-columns: auto 1fr auto 1.5fr auto;
  align-items: center;
  gap: 8px;
  margin-top: 18px;
  padding: 12px;
  border-radius: 16px;
  background: var(--color-primary-soft);
  color: var(--color-primary);
}

.converter-preview span,
.converter-preview strong {
  text-align: center;
  font-weight: 1000;
}

.post-row {
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr);
  gap: 12px;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid var(--color-border);
}

.post-row:last-child {
  border-bottom: 0;
}

.post-row > span {
  width: 42px;
  height: 42px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 15px;
  background: var(--color-primary-soft);
}

.post-row strong {
  display: block;
  color: var(--color-text);
  font-size: 14px;
  font-weight: 950;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.post-row p {
  margin: 3px 0 0;
  color: var(--color-text-light);
  font-size: 12px;
}

.promo-card {
  display: grid;
  grid-template-columns: 72px minmax(0, 1fr) auto;
  align-items: center;
  gap: 18px;
  margin-top: 22px;
  padding: 22px 28px;
  border: 1px solid var(--color-border);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: var(--shadow-soft);
}

.promo-icon {
  width: 72px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 24px;
  background: var(--color-primary-soft);
  font-size: 38px;
}

.promo-card strong {
  color: var(--color-text);
  font-size: 20px;
  font-weight: 1000;
}

.promo-card p {
  margin: 4px 0 0;
  color: var(--color-text-muted);
}

.state-message,
.empty-box {
  padding: 16px;
  border-radius: 16px;
  background: var(--color-surface-soft);
  color: var(--color-text-muted);
}

.state-message.error {
  background: #fff1f2;
  color: var(--color-danger);
  font-weight: 800;
}

@media (max-width: 1180px) {
  .hero-section {
    grid-template-columns: 1fr;
  }

  .hero-visual {
    display: none;
  }

  .feature-grid,
  .dashboard-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .home-view {
    width: min(100% - 28px, var(--container-width));
    padding-top: 24px;
  }

  .feature-grid,
  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .product-row,
  .promo-card {
    grid-template-columns: 1fr;
  }

  .product-row em {
    justify-self: start;
  }

  .process-steps {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
