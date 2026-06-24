<template>
  <div class="home-view">
    <section class="hero-card">
      <div class="hero-copy">
        <span class="eyebrow">JUYEON FINANCE GUIDE</span>
        <h1>
          내 금융생활의<br>
          <strong>주연이 되는 첫 은행 찾기</strong>
        </h1>
        <p>
          주연은 사회초년생이 주거래은행과 예적금 상품을 한 번에 비교하고,
          환율·커뮤니티 데이터까지 연결해 금융생활을 시작하도록 돕는 서비스입니다.
        </p>

        <div class="hero-actions">
          <RouterLink :to="{ name: 'recommend' }" class="btn-primary">
            맞춤 상품 추천받기
            <span>→</span>
          </RouterLink>
          <RouterLink :to="{ name: 'main-bank' }" class="btn-secondary">
            주거래은행 찾기
          </RouterLink>
        </div>
      </div>

      <aside class="hero-panel" aria-label="서비스 요약">
        <div class="panel-header">
          <span>추천 흐름</span>
          <strong>Profile → Bank → Product</strong>
        </div>

        <div class="metric-grid">
          <div>
            <span>등록 상품</span>
            <strong>{{ productLoading ? '조회 중' : `${totalProductCount}개` }}</strong>
          </div>
          <div>
            <span>커뮤니티 글</span>
            <strong>{{ communityPosts.length }}개</strong>
          </div>
          <div>
            <span>USD 기준</span>
            <strong>{{ usdRate ? `${formatNumber(usdRate.ratePerUnit)}원` : '-' }}</strong>
          </div>
        </div>

        <ol class="flow-list">
          <li v-for="step in processSteps" :key="step.label">
            <span>{{ step.icon }}</span>
            <strong>{{ step.label }}</strong>
          </li>
        </ol>
      </aside>
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


        <RouterLink :to="{ name: 'main-bank' }" class="btn-primary block-button">
          테스트 시작하기
        </RouterLink>
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
import { computed, onMounted, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import * as productApi from '@/api/products'
import { getPosts } from '@/api/community'
import { getExchangeRates } from '@/api/exchanges'
import BankLogo from '@/components/BankLogo.vue'
import { getBankDisplayName } from '@/constants/bankLogoMap'

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
  padding: 42px 0 64px;
}

.hero-card {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 430px;
  gap: 34px;
  align-items: stretch;
  padding: clamp(30px, 5vw, 54px);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.96), rgba(244, 248, 255, 0.98)),
    radial-gradient(circle at 84% 20%, rgba(16, 185, 129, 0.16), transparent 32%);
  box-shadow: var(--shadow-card);
}

.eyebrow {
  display: inline-flex;
  margin-bottom: 12px;
  color: var(--color-primary);
  font-size: 12px;
  font-weight: 950;
  letter-spacing: 0.11em;
}

.hero-copy h1 {
  margin: 0;
  color: var(--color-text);
  font-size: clamp(36px, 4.8vw, 58px);
  line-height: 1.16;
  font-weight: 950;
  letter-spacing: -0.07em;
}

.hero-copy h1 strong {
  color: var(--color-primary);
  font-weight: 950;
}

.hero-copy p {
  max-width: 640px;
  margin: 22px 0 0;
  color: var(--color-text-muted);
  font-size: 17px;
  line-height: 1.76;
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
  .home-view {
    width: min(100% - 28px, var(--container-width));
    padding-top: 24px;
  }

  .hero-card {
    padding: 26px 20px;
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
