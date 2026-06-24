<template>
  <div class="product-list-page">
    <section class="product-hero">
      <div>
        <span class="eyebrow">FINANCIAL PRODUCTS</span>
        <h1>예적금 상품 한눈에 보기</h1>
        <p>
          금융감독원 API로 저장된 실제 예금·적금 데이터를 기준으로 검색하고,
          금리와 가입 조건을 비교해보세요.
        </p>
      </div>

      <div class="hero-art" aria-hidden="true">
        <div class="piggy-visual">🐷</div>
        <div class="chart-visual">
          <span></span>
          <span></span>
          <span></span>
          <span></span>
        </div>
        <div class="coin-visual">₩</div>
      </div>

      <RouterLink :to="{ name: 'recommend' }" class="guide-card">
        <span>⭐</span>
        <div>
          <strong>사회초년생 추천</strong>
          <p>목돈 마련을 시작하는 첫 단계, 나에게 맞는 상품을 찾아보세요.</p>
        </div>
        <em>›</em>
      </RouterLink>
    </section>

    <section class="tag-guide-bar card">
      <div class="popular-tags">
        <strong>인기 태그</strong>
        <button
          v-for="tag in quickTags"
          :key="tag.value"
          type="button"
          class="tag-button"
          :class="{ active: activeQuickTag === tag.value }"
          @click="applyQuickTag(tag.value)"
        >
          # {{ tag.label }}
        </button>
      </div>

      <RouterLink :to="{ name: 'recommend' }" class="recommend-guide-link">
        <strong>추천 가이드</strong>
        <span>사회초년생을 위한 예적금 가이드 보기</span>
        <em>›</em>
      </RouterLink>
    </section>

    <div class="product-layout">
      <aside class="filter-panel card">
        <div class="filter-title-row">
          <h2>필터</h2>
          <button type="button" @click="resetFilters">
            초기화 ↻
          </button>
        </div>

        <div class="filter-block">
          <h3>상품 유형</h3>
          <div class="radio-row">
            <label>
              <input v-model="selectedType" type="radio" value="all" @change="goFirstPage">
              <span>전체</span>
            </label>
            <label>
              <input v-model="selectedType" type="radio" value="deposit" @change="goFirstPage">
              <span>예금</span>
            </label>
            <label>
              <input v-model="selectedType" type="radio" value="saving" @change="goFirstPage">
              <span>적금</span>
            </label>
          </div>
        </div>

        <div class="filter-block">
          <h3>은행</h3>
          <select v-model="selectedBank" class="input-base" @change="goFirstPage">
            <option value="all">전체 은행</option>
            <option
              v-for="bank in bankOptions"
              :key="bank"
              :value="bank"
            >
              {{ bank }}
            </option>
          </select>
        </div>

        <div class="filter-block">
          <h3>가입 기간</h3>
          <select v-model="selectedTerm" class="input-base" @change="goFirstPage">
            <option value="all">전체 기간</option>
            <option
              v-for="term in termOptions"
              :key="term"
              :value="String(term)"
            >
              {{ term }}개월
            </option>
          </select>
        </div>

        <div class="filter-block">
          <h3>금리 범위 <small>(연, 세전)</small></h3>
          <div class="rate-range">
            <input
              v-model="minRate"
              type="number"
              step="0.01"
              min="0"
              class="input-base"
              placeholder="최소 %"
              @input="goFirstPage"
            >
            <span>~</span>
            <input
              v-model="maxRate"
              type="number"
              step="0.01"
              min="0"
              class="input-base"
              placeholder="최대 %"
              @input="goFirstPage"
            >
          </div>
        </div>

        <div class="filter-block">
          <h3>가입 방식</h3>
          <div class="check-grid">
            <label
              v-for="method in joinWayOptions"
              :key="method.value"
            >
              <input
                v-model="selectedJoinWays"
                type="checkbox"
                :value="method.value"
                @change="goFirstPage"
              >
              <span>{{ method.label }}</span>
            </label>
          </div>
        </div>

        <div class="filter-block">
          <h3>우대조건</h3>
          <div class="check-grid">
            <label
              v-for="condition in benefitOptions"
              :key="condition.value"
            >
              <input
                v-model="selectedBenefits"
                type="checkbox"
                :value="condition.value"
                @change="goFirstPage"
              >
              <span>{{ condition.label }}</span>
            </label>
          </div>
        </div>

        <div class="filter-block">
          <h3>정렬</h3>
          <select v-model="sortMode" class="input-base" @change="goFirstPage">
            <option value="recommend">추천순</option>
            <option value="max_rate_desc">최고 금리 높은순</option>
            <option value="base_rate_desc">기본 금리 높은순</option>
            <option value="term_asc">가입 기간 짧은순</option>
            <option value="name_asc">상품명순</option>
          </select>
        </div>

        <button type="button" class="btn-primary filter-submit" @click="goFirstPage">
          {{ filteredProducts.length.toLocaleString() }}개 상품 보기
        </button>
      </aside>

      <section class="product-main-card card">
        <div class="list-toolbar">
          <div class="type-tabs" role="tablist" aria-label="상품 유형 탭">
            <button
              v-for="tab in typeTabs"
              :key="tab.value"
              type="button"
              :class="{ active: selectedType === tab.value }"
              @click="changeType(tab.value)"
            >
              {{ tab.label }}
              <span>{{ getTypeCount(tab.value) }}</span>
            </button>
          </div>

          <div class="search-actions">
            <label class="search-box">
              <input
                v-model.trim="searchKeyword"
                type="search"
                placeholder="상품명, 은행명 검색"
                @input="goFirstPage"
              >
              <span>⌕</span>
            </label>

            <button type="button" class="compare-button" @click="scrollToCompare">
              비교함 ({{ compareProducts.length }})
            </button>
          </div>
        </div>

        <div class="result-summary-row">
          <div>
            <strong>총 {{ filteredProducts.length.toLocaleString() }}개 상품</strong>
            <p>
              실제 저장된 상품 {{ allProducts.length.toLocaleString() }}개 중 현재 조건에 맞는 결과입니다.
            </p>
          </div>

          <label class="compare-all-check">
            <input
              type="checkbox"
              :checked="isCurrentPageAllCompared"
              @change="toggleCurrentPageCompare"
            >
            <span>현재 페이지 비교함 담기</span>
          </label>
        </div>

        <p v-if="loading" class="state-message">상품을 불러오는 중입니다...</p>
        <p v-else-if="errorMessage" class="state-message error">{{ errorMessage }}</p>
        <p v-else-if="filteredProducts.length === 0" class="state-message">
          조건에 맞는 상품이 없습니다. 필터를 초기화하거나 검색어를 변경해보세요.
        </p>

        <div v-else class="product-row-list">
          <article
            v-for="(product, index) in paginatedProducts"
            :key="getProductKey(product)"
            class="product-list-row"
          >
            <div class="compare-check" :title="getCompareTitle(product)">
              <input
                type="checkbox"
                :checked="isCompared(product)"
                :disabled="isCompareDisabled(product)"
                @change="toggleCompare(product)"
              >
            </div>

            <span class="bank-avatar" :class="getAvatarTone(product, index)">
              {{ getBankInitial(product) }}
            </span>

            <div class="product-info-area">
              <p class="bank-name">{{ getBankName(product) }}</p>
              <RouterLink
                class="product-title"
                :to="getDetailRoute(product)"
              >
                {{ product.name || '상품명 없음' }}
              </RouterLink>

              <div class="product-badges">
                <span class="badge" :class="getTypeTone(product)">
                  {{ getProductTypeLabel(product) }}
                </span>
                <span
                  v-for="badge in getProductBadges(product)"
                  :key="badge.label"
                  class="badge"
                  :class="badge.tone"
                >
                  {{ badge.label }}
                </span>
              </div>

              <p class="product-note">
                {{ getShortDescription(product) }}
              </p>
            </div>

            <div class="rate-column">
              <span>기본 금리 <small>(연, 세전)</small></span>
              <strong>{{ formatRate(getBaseRate(product)) }}</strong>
            </div>

            <div class="rate-column highlight">
              <span>최고 금리 <small>(연, 세전)</small></span>
              <strong>{{ formatRate(getBestRate(product)) }}</strong>
            </div>

            <div class="meta-column">
              <span>가입 기간</span>
              <strong>{{ getTermSummary(product) }}</strong>
            </div>

            <div class="meta-column">
              <span>가입 방식</span>
              <strong>{{ getJoinWaySummary(product) }}</strong>
            </div>

            <div class="row-actions">
              <RouterLink class="detail-button" :to="getDetailRoute(product)">
                상세 보기
              </RouterLink>
              <button
                type="button"
                class="heart-button"
                :class="{ active: isFavorite(product.id) }"
                :disabled="favoriteLoadingProductId === product.id"
                :title="isFavorite(product.id) ? '관심상품 삭제' : '관심상품 등록'"
                @click="handleToggleFavorite(product.id)"
              >
                {{ isFavorite(product.id) ? '♥' : '♡' }}
              </button>
            </div>
          </article>
        </div>

        <div v-if="totalPages > 1" class="pagination-row">
          <button type="button" :disabled="currentPage === 1" @click="currentPage -= 1">‹</button>
          <button
            v-for="page in visiblePages"
            :key="page"
            type="button"
            :class="{ active: currentPage === page }"
            @click="currentPage = page"
          >
            {{ page }}
          </button>
          <button type="button" :disabled="currentPage === totalPages" @click="currentPage += 1">›</button>
        </div>
      </section>
    </div>

    <section v-if="compareProducts.length > 0" ref="compareSection" class="compare-section card">
      <div class="section-heading compact">
        <div>
          <h2>비교함</h2>
          <p>선택한 상품을 실제 금리와 가입 조건 기준으로 비교합니다.</p>
        </div>
        <button type="button" class="clear-compare" @click="clearCompare">
          전체 비우기
        </button>
      </div>

      <div class="compare-grid">
        <article
          v-for="product in compareProducts"
          :key="product.id"
          class="compare-card"
        >
          <button type="button" class="compare-remove" @click="toggleCompare(product)">
            ×
          </button>
          <span class="badge" :class="getTypeTone(product)">{{ getProductTypeLabel(product) }}</span>
          <h3>{{ product.name }}</h3>
          <p>{{ getBankName(product) }}</p>
          <dl>
            <div>
              <dt>최고 금리</dt>
              <dd>{{ formatRate(getBestRate(product)) }}</dd>
            </div>
            <div>
              <dt>가입 기간</dt>
              <dd>{{ getTermSummary(product) }}</dd>
            </div>
            <div>
              <dt>가입 방식</dt>
              <dd>{{ getJoinWaySummary(product) }}</dd>
            </div>
          </dl>
          <RouterLink :to="getDetailRoute(product)" class="detail-button full">
            상품 상세 보기
          </RouterLink>
        </article>
      </div>
    </section>

    <p v-if="favoriteMessage" class="toast-message">
      {{ favoriteMessage }}
    </p>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import {
  getDepositProducts,
  getSavingProducts,
} from '@/api/products'
import { getFavorites, toggleFavoriteProduct } from '@/api/favorites'

const loading = ref(false)
const errorMessage = ref('')
const favoriteMessage = ref('')
const favoriteLoadingProductId = ref(null)

const depositProducts = ref([])
const savingProducts = ref([])
const favoriteProductIds = ref([])
const compareProductKeys = ref([])

const selectedType = ref('all')
const selectedBank = ref('all')
const selectedTerm = ref('all')
const minRate = ref('')
const maxRate = ref('')
const selectedJoinWays = ref([])
const selectedBenefits = ref([])
const sortMode = ref('recommend')
const searchKeyword = ref('')
const activeQuickTag = ref('')

const currentPage = ref(1)
const pageSize = 8
const compareSection = ref(null)

const typeTabs = [
  { value: 'all', label: '전체' },
  { value: 'deposit', label: '예금' },
  { value: 'saving', label: '적금' },
]

const quickTags = [
  { value: 'high_rate', label: '높은 금리' },
  { value: 'free_saving', label: '자유적립식' },
  { value: 'non_face', label: '비대면 가입' },
  { value: 'preferential', label: '우대금리' },
  { value: 'short_term', label: '만기 짧은 상품' },
]

const joinWayOptions = [
  { value: '영업점', label: '영업점' },
  { value: '인터넷', label: '인터넷' },
  { value: '스마트폰', label: '스마트폰' },
  { value: '전화', label: '전화' },
]

const benefitOptions = [
  { value: 'salary', label: '급여이체' },
  { value: 'card', label: '카드실적' },
  { value: 'marketing', label: '마케팅 동의' },
  { value: 'first', label: '첫거래 우대' },
]

const defaultTerms = [6, 12, 24, 36]

const getStoredToken = () => {
  return localStorage.getItem('token') || localStorage.getItem('accessToken')
}

const safeNumber = (value) => {
  if (value === null || value === undefined || value === '') {
    return null
  }

  const numberValue = Number(value)
  return Number.isNaN(numberValue) ? null : numberValue
}

const normalizeProduct = (product, productType) => {
  return {
    ...product,
    product_type: product.product_type || productType,
  }
}

const allProducts = computed(() => {
  return [
    ...depositProducts.value.map((product) => normalizeProduct(product, 'deposit')),
    ...savingProducts.value.map((product) => normalizeProduct(product, 'saving')),
  ]
})

const bankOptions = computed(() => {
  const banks = allProducts.value
    .map((product) => product.bank?.name)
    .filter(Boolean)

  return [...new Set(banks)].sort((a, b) => a.localeCompare(b, 'ko'))
})

const termOptions = computed(() => {
  const terms = allProducts.value.flatMap((product) => {
    return getOptions(product)
      .map((option) => safeNumber(option.save_trm))
      .filter((term) => term !== null)
  })

  const uniqueTerms = [...new Set([...defaultTerms, ...terms])]
  return uniqueTerms.sort((a, b) => a - b)
})

const getOptions = (product) => {
  return Array.isArray(product.options) ? product.options : []
}

const getRateFromOption = (option, usePreferential = true) => {
  const first = usePreferential ? option.intr_rate2 : option.intr_rate
  const second = usePreferential ? option.intr_rate : option.intr_rate2

  const firstRate = safeNumber(first)
  if (firstRate !== null) {
    return firstRate
  }

  return safeNumber(second)
}

const getRates = (product, usePreferential = true) => {
  return getOptions(product)
    .map((option) => getRateFromOption(option, usePreferential))
    .filter((rate) => rate !== null)
}

const getBestRate = (product) => {
  const maxRateValue = safeNumber(product.max_interest_rate)

  if (maxRateValue !== null) {
    return maxRateValue
  }

  const rates = getRates(product, true)
  return rates.length > 0 ? Math.max(...rates) : null
}

const getBaseRate = (product) => {
  const rates = getRates(product, false)
  return rates.length > 0 ? Math.max(...rates) : null
}

const getRateByTerm = (product, term) => {
  const rates = getOptions(product)
    .filter((option) => String(option.save_trm) === String(term))
    .map((option) => getRateFromOption(option, true))
    .filter((rate) => rate !== null)

  return rates.length > 0 ? Math.max(...rates) : null
}

const getTerms = (product) => {
  const terms = getOptions(product)
    .map((option) => safeNumber(option.save_trm))
    .filter((term) => term !== null)

  return [...new Set(terms)].sort((a, b) => a - b)
}

const getMinTerm = (product) => {
  const terms = getTerms(product)
  return terms.length > 0 ? terms[0] : null
}

const getProductSearchText = (product) => {
  return [
    product.name,
    product.bank?.name,
    product.join_way,
    product.join_member,
    product.spcl_cnd,
    product.etc_note,
    product.mtrt_int,
  ]
    .filter(Boolean)
    .join(' ')
    .toLowerCase()
}

const hasJoinWay = (product, way) => {
  return String(product.join_way || '').includes(way)
}

const hasBenefit = (product, benefit) => {
  const text = getProductSearchText(product)

  if (benefit === 'salary') {
    return text.includes('급여') || text.includes('월급')
  }

  if (benefit === 'card') {
    return text.includes('카드') || text.includes('체크카드') || text.includes('신용카드')
  }

  if (benefit === 'marketing') {
    return text.includes('마케팅') || text.includes('동의') || text.includes('개인정보')
  }

  if (benefit === 'first') {
    return text.includes('첫') || text.includes('최초') || text.includes('신규') || text.includes('첫거래')
  }

  return true
}

const matchesQuickTag = (product) => {
  if (!activeQuickTag.value) {
    return true
  }

  if (activeQuickTag.value === 'high_rate') {
    const bestRate = getBestRate(product)
    return bestRate !== null && bestRate >= 4
  }

  if (activeQuickTag.value === 'free_saving') {
    const text = getProductSearchText(product)
    return product.product_type === 'saving' && (text.includes('자유') || text.includes('자유적립'))
  }

  if (activeQuickTag.value === 'non_face') {
    return hasJoinWay(product, '인터넷') || hasJoinWay(product, '스마트폰')
  }

  if (activeQuickTag.value === 'preferential') {
    const baseRate = getBaseRate(product)
    const bestRate = getBestRate(product)
    return baseRate !== null && bestRate !== null && bestRate > baseRate
  }

  if (activeQuickTag.value === 'short_term') {
    const minTerm = getMinTerm(product)
    return minTerm !== null && minTerm <= 12
  }

  return true
}

const filteredProducts = computed(() => {
  let filtered = [...allProducts.value]

  if (selectedType.value !== 'all') {
    filtered = filtered.filter((product) => product.product_type === selectedType.value)
  }

  if (selectedBank.value !== 'all') {
    filtered = filtered.filter((product) => product.bank?.name === selectedBank.value)
  }

  if (selectedTerm.value !== 'all') {
    filtered = filtered.filter((product) => getRateByTerm(product, selectedTerm.value) !== null)
  }

  if (minRate.value !== '') {
    const min = Number(minRate.value)
    filtered = filtered.filter((product) => {
      const rate = selectedTerm.value === 'all'
        ? getBestRate(product)
        : getRateByTerm(product, selectedTerm.value)
      return rate !== null && rate >= min
    })
  }

  if (maxRate.value !== '') {
    const max = Number(maxRate.value)
    filtered = filtered.filter((product) => {
      const rate = selectedTerm.value === 'all'
        ? getBestRate(product)
        : getRateByTerm(product, selectedTerm.value)
      return rate !== null && rate <= max
    })
  }

  if (selectedJoinWays.value.length > 0) {
    filtered = filtered.filter((product) => {
      return selectedJoinWays.value.some((way) => hasJoinWay(product, way))
    })
  }

  if (selectedBenefits.value.length > 0) {
    filtered = filtered.filter((product) => {
      return selectedBenefits.value.every((benefit) => hasBenefit(product, benefit))
    })
  }

  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter((product) => getProductSearchText(product).includes(keyword))
  }

  filtered = filtered.filter((product) => matchesQuickTag(product))

  filtered.sort((a, b) => {
    if (sortMode.value === 'max_rate_desc' || sortMode.value === 'recommend') {
      return (getBestRate(b) ?? -1) - (getBestRate(a) ?? -1)
    }

    if (sortMode.value === 'base_rate_desc') {
      return (getBaseRate(b) ?? -1) - (getBaseRate(a) ?? -1)
    }

    if (sortMode.value === 'term_asc') {
      return (getMinTerm(a) ?? 999) - (getMinTerm(b) ?? 999)
    }

    return String(a.name || '').localeCompare(String(b.name || ''), 'ko')
  })

  return filtered
})

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(filteredProducts.value.length / pageSize))
})

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredProducts.value.slice(start, start + pageSize)
})

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, start + 4)

  for (let page = start; page <= end; page += 1) {
    pages.push(page)
  }

  return pages
})

const compareProducts = computed(() => {
  return compareProductKeys.value
    .map((productKey) => allProducts.value.find((product) => getProductKey(product) === productKey))
    .filter(Boolean)
})

const isCurrentPageAllCompared = computed(() => {
  return paginatedProducts.value.length > 0 && paginatedProducts.value.every((product) => {
    return compareProductKeys.value.includes(getProductKey(product))
  })
})

const getTypeCount = (type) => {
  if (type === 'all') {
    return allProducts.value.length.toLocaleString()
  }

  return allProducts.value.filter((product) => product.product_type === type).length.toLocaleString()
}

const getProductKey = (product) => {
  return `${product.product_type}-${product.id}`
}

const getBankName = (product) => {
  return product.bank?.name || '은행명 없음'
}

const getBankInitial = (product) => {
  const name = getBankName(product)
  return name.slice(0, 1).toUpperCase()
}

const getAvatarTone = (product, index) => {
  const tones = ['blue', 'mint', 'purple', 'orange', 'sky']
  return tones[(Number(product.id) + index) % tones.length]
}

const getTypeTone = (product) => {
  return product.product_type === 'deposit' ? 'mint' : 'purple'
}

const getProductTypeLabel = (product) => {
  return product.product_type === 'deposit' ? '예금' : '적금'
}

const getProductBadges = (product) => {
  const badges = []
  const bestRate = getBestRate(product)
  const baseRate = getBaseRate(product)

  if (bestRate !== null && bestRate >= 4) {
    badges.push({ label: '고금리', tone: 'blue' })
  }

  if (baseRate !== null && bestRate !== null && bestRate > baseRate) {
    badges.push({ label: '우대', tone: 'purple' })
  }

  if (hasJoinWay(product, '인터넷') || hasJoinWay(product, '스마트폰')) {
    badges.push({ label: '비대면', tone: 'mint' })
  }

  if (product.product_type === 'saving' && getProductSearchText(product).includes('자유')) {
    badges.push({ label: '자유적립', tone: 'purple' })
  }

  return badges.slice(0, 3)
}

const getShortDescription = (product) => {
  if (product.spcl_cnd) {
    return product.spcl_cnd.replace(/\s+/g, ' ').slice(0, 70)
  }

  if (product.join_member) {
    return product.join_member.replace(/\s+/g, ' ').slice(0, 70)
  }

  if (product.etc_note) {
    return product.etc_note.replace(/\s+/g, ' ').slice(0, 70)
  }

  return product.join_way ? `${product.join_way} 방식으로 가입 가능한 상품입니다.` : '상품 상세 조건은 상세 페이지에서 확인할 수 있습니다.'
}

const formatRate = (rate) => {
  if (rate === null || rate === undefined || rate === '') {
    return '-'
  }

  return `${Number(rate).toFixed(2)}%`
}

const getTermSummary = (product) => {
  const terms = getTerms(product)

  if (terms.length === 0) {
    return '정보 없음'
  }

  if (terms.length === 1) {
    return `${terms[0]}개월`
  }

  return `${terms[0]}~${terms[terms.length - 1]}개월`
}

const getJoinWaySummary = (product) => {
  const joinWay = product.join_way || ''

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
}

const getDetailRoute = (product) => {
  return {
    name: 'product-detail',
    params: { id: product.id },
    query: { type: product.product_type || 'deposit' },
  }
}

const isFavorite = (productId) => {
  return favoriteProductIds.value.includes(productId)
}

const isCompared = (product) => {
  return compareProductKeys.value.includes(getProductKey(product))
}

const isCompareDisabled = (product) => {
  return !isCompared(product) && compareProductKeys.value.length >= 4
}

const getCompareTitle = (product) => {
  if (isCompared(product)) {
    return '비교함에서 제거'
  }

  if (isCompareDisabled(product)) {
    return '비교함에는 최대 4개 상품까지 담을 수 있습니다.'
  }

  return '비교함에 담기'
}

const changeType = (type) => {
  selectedType.value = type
  goFirstPage()
}

const applyQuickTag = (tagValue) => {
  activeQuickTag.value = activeQuickTag.value === tagValue ? '' : tagValue
  goFirstPage()
}

const goFirstPage = () => {
  currentPage.value = 1
}

const resetFilters = () => {
  selectedType.value = 'all'
  selectedBank.value = 'all'
  selectedTerm.value = 'all'
  minRate.value = ''
  maxRate.value = ''
  selectedJoinWays.value = []
  selectedBenefits.value = []
  sortMode.value = 'recommend'
  searchKeyword.value = ''
  activeQuickTag.value = ''
  currentPage.value = 1
}

const toggleCompare = (product) => {
  const productKey = getProductKey(product)

  if (compareProductKeys.value.includes(productKey)) {
    compareProductKeys.value = compareProductKeys.value.filter((key) => key !== productKey)
    return
  }

  if (compareProductKeys.value.length >= 4) {
    favoriteMessage.value = '비교함에는 최대 4개 상품까지 담을 수 있습니다.'
    window.setTimeout(() => {
      favoriteMessage.value = ''
    }, 1800)
    return
  }

  compareProductKeys.value.push(productKey)
}

const toggleCurrentPageCompare = () => {
  if (isCurrentPageAllCompared.value) {
    const currentKeys = paginatedProducts.value.map((product) => getProductKey(product))
    compareProductKeys.value = compareProductKeys.value.filter((key) => !currentKeys.includes(key))
    return
  }

  paginatedProducts.value.forEach((product) => {
    const productKey = getProductKey(product)

    if (!compareProductKeys.value.includes(productKey) && compareProductKeys.value.length < 4) {
      compareProductKeys.value.push(productKey)
    }
  })

  if (compareProductKeys.value.length >= 4) {
    favoriteMessage.value = '비교함에는 최대 4개 상품까지 담을 수 있습니다.'
    window.setTimeout(() => {
      favoriteMessage.value = ''
    }, 1800)
  }
}

const clearCompare = () => {
  compareProductKeys.value = []
}

const scrollToCompare = async () => {
  if (compareProducts.value.length === 0) {
    favoriteMessage.value = '비교할 상품을 먼저 선택해주세요.'
    window.setTimeout(() => {
      favoriteMessage.value = ''
    }, 1800)
    return
  }

  await nextTick()
  compareSection.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const extractFavoriteProductId = (favorite) => {
  if (favorite.product_id) {
    return favorite.product_id
  }

  if (typeof favorite.product === 'number') {
    return favorite.product
  }

  const product = favorite.product || favorite
  return product.id || null
}

const fetchFavorites = async () => {
  const token = getStoredToken()

  if (!token) {
    favoriteProductIds.value = []
    return
  }

  try {
    const response = await getFavorites()

    favoriteProductIds.value = response.data
      .map((favorite) => extractFavoriteProductId(favorite))
      .filter((productId) => productId !== null)
  } catch (error) {
    console.error(error)
    favoriteProductIds.value = []
  }
}

const handleToggleFavorite = async (productId) => {
  const token = getStoredToken()

  favoriteMessage.value = ''
  errorMessage.value = ''

  if (!token) {
    favoriteMessage.value = '로그인 후 관심상품을 등록할 수 있습니다.'
    window.setTimeout(() => {
      favoriteMessage.value = ''
    }, 1800)
    return
  }

  favoriteLoadingProductId.value = productId

  try {
    const response = await toggleFavoriteProduct(productId)
    const isNowFavorite = response.data.is_favorite

    if (isNowFavorite) {
      if (!favoriteProductIds.value.includes(productId)) {
        favoriteProductIds.value.push(productId)
      }
    } else {
      favoriteProductIds.value = favoriteProductIds.value.filter((id) => id !== productId)
    }

    favoriteMessage.value = response.data.message || '관심상품이 변경되었습니다.'
    window.setTimeout(() => {
      favoriteMessage.value = ''
    }, 1800)
  } catch (error) {
    console.error(error)
    favoriteMessage.value = '관심상품 처리에 실패했습니다.'
  } finally {
    favoriteLoadingProductId.value = null
  }
}

const fetchProducts = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const [depositResponse, savingResponse] = await Promise.all([
      getDepositProducts(),
      getSavingProducts(),
    ])

    depositProducts.value = Array.isArray(depositResponse.data) ? depositResponse.data : []
    savingProducts.value = Array.isArray(savingResponse.data) ? savingResponse.data : []
  } catch (error) {
    console.error(error)
    errorMessage.value = '상품 목록을 불러오지 못했습니다. 백엔드 서버와 FSS_API_KEY 설정을 확인해주세요.'
  } finally {
    loading.value = false
  }
}

watch(totalPages, (newTotalPages) => {
  if (currentPage.value > newTotalPages) {
    currentPage.value = newTotalPages
  }
})

onMounted(async () => {
  await fetchProducts()
  await fetchFavorites()
})
</script>

<style scoped>
.product-list-page {
  width: min(var(--container-width), calc(100% - 48px));
  margin: 0 auto;
  padding: 34px 0 54px;
}

.product-hero {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 320px 330px;
  gap: 24px;
  align-items: center;
  min-height: 180px;
  margin-bottom: 24px;
}

.eyebrow {
  display: inline-flex;
  margin-bottom: 10px;
  color: var(--color-primary);
  font-size: 12px;
  font-weight: 900;
  letter-spacing: 0.12em;
}

.product-hero h1 {
  margin: 0;
  color: var(--color-text);
  font-size: clamp(34px, 4.2vw, 48px);
  line-height: 1.12;
  font-weight: 950;
  letter-spacing: -0.06em;
}

.product-hero p {
  max-width: 610px;
  margin: 14px 0 0;
  color: var(--color-text-muted);
  font-size: 17px;
}

.hero-art {
  position: relative;
  min-height: 140px;
}

.piggy-visual,
.coin-visual,
.chart-visual {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.92);
  box-shadow: var(--shadow-soft);
}

.piggy-visual {
  left: 30px;
  top: 34px;
  width: 88px;
  height: 88px;
  border-radius: 32px;
  background: var(--color-accent-soft);
  font-size: 46px;
}

.chart-visual {
  left: 122px;
  top: 20px;
  width: 118px;
  height: 92px;
  align-items: flex-end;
  gap: 9px;
  padding: 18px;
  border-radius: 24px;
}

.chart-visual span {
  width: 12px;
  border-radius: 99px;
  background: linear-gradient(180deg, #6875ff, var(--color-primary));
}

.chart-visual span:nth-child(1) { height: 24px; }
.chart-visual span:nth-child(2) { height: 42px; }
.chart-visual span:nth-child(3) { height: 56px; }
.chart-visual span:nth-child(4) { height: 70px; background: linear-gradient(180deg, #3ee5ca, var(--color-accent)); }

.coin-visual {
  right: 24px;
  bottom: 20px;
  width: 72px;
  height: 72px;
  border-radius: 28px;
  background: #fff7e5;
  color: #d97706;
  font-size: 34px;
  font-weight: 950;
}

.guide-card {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 14px;
  align-items: center;
  padding: 22px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: var(--shadow-soft);
}

.guide-card > span {
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border-radius: 16px;
  background: #fff8e6;
}

.guide-card strong {
  display: block;
  color: var(--color-primary);
  font-size: 17px;
}

.guide-card p {
  margin: 4px 0 0;
  color: var(--color-text-muted);
  font-size: 14px;
}

.guide-card em {
  color: var(--color-text);
  font-size: 30px;
  font-style: normal;
}

.tag-guide-bar {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: center;
  padding: 12px 18px;
  margin-bottom: 22px;
}

.popular-tags,
.recommend-guide-link {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.popular-tags strong,
.recommend-guide-link strong {
  margin-right: 10px;
  color: var(--color-text);
  font-weight: 950;
}

.tag-button {
  min-height: 36px;
  padding: 0 14px;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  background: #fff;
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 800;
}

.tag-button.active,
.tag-button:hover {
  border-color: var(--color-primary);
  background: var(--color-primary-soft);
  color: var(--color-primary);
}

.recommend-guide-link {
  flex-shrink: 0;
  padding-left: 22px;
  border-left: 1px solid var(--color-border);
  color: var(--color-text-muted);
}

.recommend-guide-link span {
  font-weight: 700;
}

.recommend-guide-link em {
  color: var(--color-primary);
  font-style: normal;
  font-size: 22px;
}

.product-layout {
  display: grid;
  grid-template-columns: 270px minmax(0, 1fr);
  gap: 18px;
  align-items: flex-start;
}

.filter-panel {
  position: sticky;
  top: calc(var(--header-height) + 18px);
  padding: 20px;
}

.filter-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.filter-title-row h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 950;
}

.filter-title-row button,
.clear-compare {
  border: 0;
  background: transparent;
  color: var(--color-primary);
  font-weight: 900;
}

.filter-block {
  padding: 16px 0;
  border-top: 1px solid var(--color-border);
}

.filter-block h3 {
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 0 0 12px;
  color: var(--color-text);
  font-size: 14px;
  font-weight: 950;
}

.filter-block small {
  color: var(--color-text-light);
  font-size: 12px;
}

.radio-row,
.check-grid {
  display: grid;
  gap: 10px;
}

.radio-row {
  grid-template-columns: repeat(3, 1fr);
}

.check-grid {
  grid-template-columns: repeat(2, 1fr);
}

.radio-row label,
.check-grid label,
.compare-all-check {
  display: inline-flex;
  gap: 7px;
  align-items: center;
  color: var(--color-text-muted);
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
}

.compare-check {
  display: grid;
  place-items: center;
  width: 22px;
  height: 22px;
  cursor: default;
}

.radio-row input,
.check-grid input,
.compare-all-check input,
.compare-check input {
  accent-color: var(--color-primary);
}

.compare-check input {
  width: 14px;
  height: 14px;
  margin: 0;
  cursor: pointer;
}

.compare-check input:disabled {
  cursor: not-allowed;
  opacity: 0.35;
}

.rate-range {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 8px;
  align-items: center;
}

.rate-range input {
  padding-inline: 10px;
}

.rate-range span {
  color: var(--color-text-light);
  font-weight: 900;
}

.filter-submit {
  width: 100%;
  margin-top: 16px;
}

.product-main-card {
  min-width: 0;
  overflow: hidden;
}

.list-toolbar {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: center;
  padding: 18px 20px 0;
}

.type-tabs {
  display: flex;
  gap: 6px;
}

.type-tabs button {
  min-width: 100px;
  padding: 14px 12px;
  border: 0;
  border-bottom: 3px solid transparent;
  background: transparent;
  color: var(--color-text-muted);
  font-weight: 950;
}

.type-tabs button.active {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}

.type-tabs span {
  margin-left: 5px;
  color: var(--color-text-light);
  font-size: 12px;
}

.search-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.search-box {
  position: relative;
  width: min(320px, 32vw);
}

.search-box input {
  width: 100%;
  min-height: 46px;
  padding: 0 44px 0 15px;
  border: 1px solid var(--color-border-strong);
  border-radius: 14px;
  outline: none;
}

.search-box input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px rgba(17, 22, 184, 0.08);
}

.search-box span {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text);
  font-size: 20px;
  font-weight: 950;
}

.compare-button {
  min-height: 46px;
  padding: 0 16px;
  border: 1px solid var(--color-border-strong);
  border-radius: 14px;
  background: #fff;
  color: var(--color-text);
  font-weight: 900;
}

.result-summary-row {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: flex-start;
  padding: 14px 20px 18px;
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

.result-summary-row strong {
  color: var(--color-text);
  font-size: 16px;
  font-weight: 950;
}

.result-summary-row p {
  margin: 3px 0 0;
  color: var(--color-text-muted);
  font-size: 13px;
}

.product-row-list {
  display: grid;
}

.product-list-row {
  display: grid;
  grid-template-columns: 22px 56px minmax(200px, 1.7fr) minmax(90px, 0.9fr) minmax(90px, 0.9fr) minmax(72px, 0.75fr) minmax(72px, 0.72fr) minmax(112px, auto);
  gap: 14px;
  align-items: center;
  padding: 18px 20px;
  border-bottom: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.72);
}

.product-list-row:hover {
  background: var(--color-surface-soft);
}

.bank-avatar {
  display: grid;
  place-items: center;
  width: 54px;
  height: 54px;
  border-radius: 18px;
  color: #fff;
  font-size: 24px;
  font-weight: 950;
}

.bank-avatar.blue { background: linear-gradient(135deg, #4f6bff, var(--color-primary)); }
.bank-avatar.mint { background: linear-gradient(135deg, #4be0c8, #0f9f8b); }
.bank-avatar.purple { background: linear-gradient(135deg, #a679ff, var(--color-purple)); }
.bank-avatar.orange { background: linear-gradient(135deg, #fb923c, #ea580c); }
.bank-avatar.sky { background: linear-gradient(135deg, #60a5fa, #2563eb); }

.product-info-area {
  min-width: 0;
}

.bank-name {
  margin: 0 0 2px;
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 800;
}

.product-title {
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  color: var(--color-text);
  font-size: 18px;
  font-weight: 950;
  letter-spacing: -0.03em;
  text-overflow: ellipsis;
  white-space: nowrap;
  word-break: keep-all;
}

.product-title:hover {
  color: var(--color-primary);
}

.product-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 6px;
}

.badge.blue {
  background: #eaf0ff;
  color: #3151db;
}

.product-note {
  overflow: hidden;
  margin: 7px 0 0;
  color: var(--color-text-muted);
  font-size: 13px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rate-column,
.meta-column {
  display: grid;
  gap: 2px;
}

.rate-column span,
.meta-column span {
  color: var(--color-text-light);
  font-size: 12px;
  font-weight: 800;
}

.rate-column strong {
  color: var(--color-text);
  font-size: 24px;
  font-weight: 950;
  letter-spacing: -0.04em;
}

.rate-column.highlight strong {
  color: var(--color-primary);
}

.meta-column strong {
  color: var(--color-text);
  font-size: 14px;
  font-weight: 950;
}

.row-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.detail-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
  min-width: 92px;
  padding: 0 14px;
  border: 1px solid var(--color-primary);
  border-radius: 12px;
  background: #fff;
  color: var(--color-primary);
  font-size: 14px;
  font-weight: 950;
  white-space: nowrap;
  word-break: keep-all;
  flex-shrink: 0;
}

.detail-button.full {
  width: 100%;
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
  line-height: 1;
  flex-shrink: 0;
}

.heart-button.active {
  border-color: #fecdd3;
  color: var(--color-danger);
  background: #fff1f2;
}

.state-message {
  margin: 20px;
  padding: 20px;
  border: 1px dashed var(--color-border-strong);
  border-radius: var(--radius-md);
  background: var(--color-surface-soft);
  color: var(--color-text-muted);
  text-align: center;
  font-weight: 800;
}

.state-message.error {
  border-color: #fecaca;
  background: #fff5f5;
  color: var(--color-danger);
}

.pagination-row {
  display: flex;
  justify-content: center;
  gap: 8px;
  padding: 18px 0 22px;
}

.pagination-row button {
  min-width: 34px;
  height: 34px;
  border: 1px solid var(--color-border);
  border-radius: 11px;
  background: #fff;
  color: var(--color-text-muted);
  font-weight: 900;
}

.pagination-row button.active {
  border-color: var(--color-primary);
  background: var(--color-primary);
  color: #fff;
}

.compare-section {
  margin-top: 22px;
  padding: 22px;
}

.compare-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}

.compare-card {
  position: relative;
  padding: 18px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface-soft);
}

.compare-remove {
  position: absolute;
  right: 12px;
  top: 12px;
  width: 28px;
  height: 28px;
  border: 0;
  border-radius: 50%;
  background: #fff;
  color: var(--color-text-muted);
  font-size: 20px;
}

.compare-card h3 {
  min-height: 48px;
  margin: 10px 0 3px;
  color: var(--color-text);
  font-size: 17px;
  line-height: 1.35;
  font-weight: 950;
}

.compare-card p {
  margin: 0 0 12px;
  color: var(--color-text-muted);
  font-size: 13px;
}

.compare-card dl {
  display: grid;
  gap: 8px;
  margin: 0 0 14px;
}

.compare-card dl div {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--color-border);
}

.compare-card dt {
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 800;
}

.compare-card dd {
  margin: 0;
  color: var(--color-primary);
  font-weight: 950;
}

.toast-message {
  position: fixed;
  left: 50%;
  right: auto;
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

@media (max-width: 1180px) {
  .product-hero {
    grid-template-columns: 1fr;
  }

  .hero-art {
    display: none;
  }

  .product-layout {
    grid-template-columns: 1fr;
  }

  .filter-panel {
    position: static;
  }

  .product-list-row {
    grid-template-columns: 22px 56px minmax(180px, 1fr) 106px 106px 80px 80px 104px;
  }

  .product-list-row .meta-column:nth-of-type(2) {
    display: none;
  }

  .compare-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 860px) {
  .product-list-page {
    width: min(100% - 28px, var(--container-width));
  }

  .tag-guide-bar,
  .list-toolbar,
  .result-summary-row {
    align-items: stretch;
    flex-direction: column;
  }

  .recommend-guide-link {
    padding-left: 0;
    border-left: 0;
  }

  .search-box {
    width: 100%;
  }

  .search-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .product-list-row {
    grid-template-columns: 24px 52px 1fr;
    align-items: flex-start;
  }

  .rate-column,
  .meta-column,
  .row-actions {
    grid-column: 3 / -1;
  }

  .row-actions {
    justify-content: flex-start;
  }

  .compare-grid {
    grid-template-columns: 1fr;
  }
}
</style>
