<template>
  <div class="product-list-view">
    <section class="page-header">
      <p class="breadcrumb">화면 ③ 상품 탐색</p>
      <h1>예적금 상품 비교</h1>
      <p class="description">
        원하는 조건으로 예금과 적금을 필터링하고 기간별 금리를 비교해보세요.
      </p>
    </section>

    <section class="filter-section">
      <h2>검색 필터</h2>

      <div class="filter-grid">
        <div class="filter-field">
          <label>은행명</label>
          <select v-model="selectedBank">
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

        <div class="filter-field">
          <label>상품 구분</label>
          <div class="type-buttons">
            <button
              type="button"
              :class="{ active: selectedType === 'deposit' }"
              @click="changeProductType('deposit')"
            >
              예금
            </button>

            <button
              type="button"
              :class="{ active: selectedType === 'saving' }"
              @click="changeProductType('saving')"
            >
              적금
            </button>
          </div>
        </div>

        <div class="filter-field">
          <label>가입 기간</label>
          <select v-model="selectedTerm">
            <option value="all">전체 기간</option>
            <option value="6">6개월</option>
            <option value="12">12개월</option>
            <option value="24">24개월</option>
            <option value="36">36개월</option>
          </select>
        </div>

        <div class="filter-field">
          <label>금리 최소</label>
          <input
            v-model="minRate"
            type="number"
            step="0.01"
            placeholder="예: 3.0"
          />
        </div>

        <div class="filter-field">
          <label>가입 방식</label>
          <select v-model="selectedJoinWay">
            <option value="all">전체</option>
            <option value="영업점">영업점</option>
            <option value="인터넷">인터넷</option>
            <option value="스마트폰">스마트폰</option>
            <option value="전화">전화</option>
          </select>
        </div>
      </div>

      <div class="filter-actions">
        <button type="button" class="reset-btn" @click="resetFilters">
          초기화
        </button>
      </div>
    </section>

    <p v-if="loading" class="status-message">상품을 불러오는 중입니다...</p>
    <p v-else-if="errorMessage" class="status-message error">{{ errorMessage }}</p>

    <section v-else class="list-section">
      <div class="list-header">
        <div>
          <h2>
            상품 목록
            <span>총 {{ displayedProducts.length }}개</span>
          </h2>

          <p class="sort-guide">
            기간별 금리 제목을 클릭하면 해당 기간 기준으로 정렬됩니다.
          </p>
        </div>

        <p v-if="favoriteMessage" class="favorite-message">
          {{ favoriteMessage }}
        </p>
      </div>

      <p v-if="displayedProducts.length === 0" class="status-message">
        조회된 상품이 없습니다.
      </p>

      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>은행명</th>
              <th class="product-name-col">상품명</th>
              <th>
                <button type="button" class="sort-button" @click="toggleSort('6')">
                  6개월 {{ getSortIcon('6') }}
                </button>
              </th>
              <th>
                <button type="button" class="sort-button" @click="toggleSort('12')">
                  12개월 {{ getSortIcon('12') }}
                </button>
              </th>
              <th>
                <button type="button" class="sort-button" @click="toggleSort('24')">
                  24개월 {{ getSortIcon('24') }}
                </button>
              </th>
              <th>
                <button type="button" class="sort-button" @click="toggleSort('36')">
                  36개월 {{ getSortIcon('36') }}
                </button>
              </th>
              <th>가입 방법</th>
              <th>상세</th>
              <th>관심</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="product in displayedProducts"
              :key="product.id"
            >
              <td>
                <strong>{{ product.bank?.name || '정보 없음' }}</strong>
                <span class="bank-code">{{ product.bank?.code }}</span>
              </td>

              <td class="product-name-col">
                <p class="product-name">{{ product.name }}</p>
                <span class="product-type">
                  {{ selectedType === 'deposit' ? '정기예금' : '적금' }}
                </span>
              </td>

              <td>{{ formatRate(getRateByTerm(product, '6')) }}</td>
              <td>{{ formatRate(getRateByTerm(product, '12')) }}</td>
              <td>{{ formatRate(getRateByTerm(product, '24')) }}</td>
              <td>{{ formatRate(getRateByTerm(product, '36')) }}</td>

              <td class="join-way">
                {{ product.join_way || '정보 없음' }}
              </td>

              <td>
                <RouterLink
                  class="detail-link"
                  :to="{
                    name: 'product-detail',
                    params: { id: product.id },
                    query: { type: selectedType }
                  }"
                >
                  상세보기
                </RouterLink>
              </td>

              <td>
                <button
                  type="button"
                  class="favorite-btn"
                  :class="{ active: isFavorite(product.id) }"
                  :disabled="favoriteLoadingProductId === product.id"
                  @click="handleToggleFavorite(product.id)"
                >
                  <span v-if="favoriteLoadingProductId === product.id">
                    처리 중
                  </span>
                  <span v-else>
                    {{ isFavorite(product.id) ? '삭제' : '등록' }}
                  </span>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import {
  getDepositProducts,
  getSavingProducts,
} from '@/api/products'
import { getFavorites, toggleFavoriteProduct } from '@/api/favorites'

const products = ref([])
const favoriteProductIds = ref([])
const selectedType = ref('deposit')
const selectedBank = ref('all')
const selectedTerm = ref('all')
const selectedJoinWay = ref('all')
const minRate = ref('')
const sortTerm = ref('12')
const sortOrder = ref('desc')
const loading = ref(false)
const errorMessage = ref('')
const favoriteMessage = ref('')
const favoriteLoadingProductId = ref(null)

const terms = ['6', '12', '24', '36']

const getStoredToken = () => {
  return localStorage.getItem('token') || localStorage.getItem('accessToken')
}

const formatRate = (rate) => {
  if (rate === null || rate === undefined || rate === '') {
    return '-'
  }

  return `${Number(rate).toFixed(2)}%`
}

const getOptionRate = (option) => {
  if (option.intr_rate2 !== null && option.intr_rate2 !== undefined && option.intr_rate2 !== '') {
    return Number(option.intr_rate2)
  }

  if (option.intr_rate !== null && option.intr_rate !== undefined && option.intr_rate !== '') {
    return Number(option.intr_rate)
  }

  return null
}

const getRateByTerm = (product, term) => {
  if (!product.options || product.options.length === 0) {
    return null
  }

  const matchedOptions = product.options.filter((option) => {
    return String(option.save_trm) === String(term)
  })

  const rates = matchedOptions
    .map((option) => getOptionRate(option))
    .filter((rate) => rate !== null && !Number.isNaN(rate))

  if (rates.length === 0) {
    return null
  }

  return Math.max(...rates)
}

const getProductBestRate = (product) => {
  const rates = terms
    .map((term) => getRateByTerm(product, term))
    .filter((rate) => rate !== null && !Number.isNaN(rate))

  if (rates.length === 0) {
    return null
  }

  return Math.max(...rates)
}

const bankOptions = computed(() => {
  const banks = products.value
    .map((product) => product.bank?.name)
    .filter((bankName) => !!bankName)

  return [...new Set(banks)].sort()
})

const displayedProducts = computed(() => {
  let filtered = [...products.value]

  if (selectedBank.value !== 'all') {
    filtered = filtered.filter((product) => {
      return product.bank?.name === selectedBank.value
    })
  }

  if (selectedTerm.value !== 'all') {
    filtered = filtered.filter((product) => {
      return getRateByTerm(product, selectedTerm.value) !== null
    })
  }

  if (selectedJoinWay.value !== 'all') {
    filtered = filtered.filter((product) => {
      return product.join_way?.includes(selectedJoinWay.value)
    })
  }

  if (minRate.value !== '') {
    const min = Number(minRate.value)

    filtered = filtered.filter((product) => {
      if (selectedTerm.value !== 'all') {
        const rate = getRateByTerm(product, selectedTerm.value)
        return rate !== null && rate >= min
      }

      const bestRate = getProductBestRate(product)
      return bestRate !== null && bestRate >= min
    })
  }

  filtered.sort((a, b) => {
    const rateA = getRateByTerm(a, sortTerm.value)
    const rateB = getRateByTerm(b, sortTerm.value)

    if (rateA === null && rateB === null) {
      return a.name.localeCompare(b.name)
    }

    if (rateA === null) {
      return 1
    }

    if (rateB === null) {
      return -1
    }

    if (sortOrder.value === 'asc') {
      return rateA - rateB
    }

    return rateB - rateA
  })

  return filtered
})

const isFavorite = (productId) => {
  return favoriteProductIds.value.includes(productId)
}

const getSortIcon = (term) => {
  if (sortTerm.value !== term) {
    return '↕'
  }

  return sortOrder.value === 'asc' ? '▲' : '▼'
}

const toggleSort = (term) => {
  if (sortTerm.value === term) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
    return
  }

  sortTerm.value = term
  sortOrder.value = 'desc'
}

const changeProductType = async (type) => {
  selectedType.value = type
  selectedBank.value = 'all'
  selectedTerm.value = 'all'
  selectedJoinWay.value = 'all'
  minRate.value = ''
  favoriteMessage.value = ''

  await fetchProducts()
}

const resetFilters = () => {
  selectedBank.value = 'all'
  selectedTerm.value = 'all'
  selectedJoinWay.value = 'all'
  minRate.value = ''
  sortTerm.value = '12'
  sortOrder.value = 'desc'
  favoriteMessage.value = ''
}

const fetchProducts = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    let response

    if (selectedType.value === 'deposit') {
      response = await getDepositProducts()
    } else {
      response = await getSavingProducts()
    }

    products.value = Array.isArray(response.data) ? response.data : []
  } catch (error) {
    console.error(error)
    errorMessage.value = '상품 목록을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
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
    errorMessage.value = '로그인 후 관심상품을 등록할 수 있습니다.'
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

      favoriteMessage.value = '관심상품에 등록되었습니다.'
    } else {
      favoriteProductIds.value = favoriteProductIds.value.filter((id) => {
        return id !== productId
      })

      favoriteMessage.value = '관심상품에서 삭제되었습니다.'
    }
  } catch (error) {
    console.error(error)

    if (error.response?.status === 401 || error.response?.status === 403) {
      errorMessage.value = '로그인 후 관심상품을 등록할 수 있습니다.'
      return
    }

    errorMessage.value = '관심상품 처리에 실패했습니다.'
  } finally {
    favoriteLoadingProductId.value = null
  }
}

onMounted(async () => {
  await fetchProducts()
  await fetchFavorites()
})
</script>

<style scoped>
.product-list-view {
  min-height: 100vh;
  padding: 28px;
  background-color: #f6f7f9;
}

.page-header {
  padding-bottom: 18px;
  margin-bottom: 18px;
  border-bottom: 1px solid #ddd;
}

.breadcrumb {
  margin: 0 0 8px;
  font-size: 13px;
  color: #777;
}

.page-header h1 {
  margin: 0;
  font-size: 26px;
  color: #111;
}

.description {
  margin: 8px 0 0;
  color: #666;
}

.filter-section {
  padding: 20px;
  margin-bottom: 18px;
  background-color: #fff;
  border: 1px solid #ddd;
}

.filter-section h2 {
  margin: 0 0 16px;
  font-size: 17px;
}

.filter-grid {
  display: grid;
  grid-template-columns: 1.2fr 1.2fr 1.2fr 1fr 1.2fr;
  gap: 14px;
}

.filter-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-field label {
  font-size: 13px;
  color: #666;
  font-weight: 700;
}

.filter-field select,
.filter-field input {
  height: 38px;
  padding: 0 12px;
  border: 1px solid #ccc;
  background-color: #fff;
  color: #333;
}

.type-buttons {
  display: flex;
}

.type-buttons button {
  flex: 1;
  height: 38px;
  border: 1px solid #ccc;
  background-color: #fff;
  color: #333;
  font-weight: 700;
  cursor: pointer;
}

.type-buttons button + button {
  border-left: none;
}

.type-buttons button.active {
  background-color: #333;
  color: #fff;
}

.filter-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 14px;
}

.reset-btn {
  height: 38px;
  padding: 0 18px;
  border: 1px solid #bbb;
  background-color: #fff;
  color: #333;
  font-weight: 700;
  cursor: pointer;
}

.status-message {
  padding: 18px;
  background-color: #fff;
  border: 1px solid #ddd;
  color: #555;
}

.status-message.error {
  color: #c0392b;
}

.list-section {
  background-color: transparent;
}

.list-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 10px;
}

.list-header h2 {
  margin: 0;
  font-size: 17px;
}

.list-header h2 span {
  font-size: 14px;
  color: #666;
}

.sort-guide {
  margin: 6px 0 0;
  font-size: 13px;
  color: #777;
}

.favorite-message {
  margin: 0;
  padding: 9px 12px;
  border: 1px solid #bbf7d0;
  background-color: #f0fdf4;
  color: #15803d;
  font-size: 13px;
  font-weight: 800;
  white-space: nowrap;
}

.table-wrap {
  overflow-x: auto;
  background-color: #fff;
  border: 1px solid #ddd;
}

table {
  width: 100%;
  min-width: 980px;
  border-collapse: collapse;
}

thead {
  background-color: #f3f3f3;
}

th,
td {
  padding: 14px 12px;
  border-bottom: 1px solid #e5e5e5;
  text-align: center;
  font-size: 14px;
}

th {
  color: #444;
  font-weight: 800;
}

td:first-child,
th:first-child {
  text-align: left;
}

.product-name-col {
  text-align: left;
  min-width: 220px;
}

.product-name {
  margin: 0 0 5px;
  font-weight: 800;
  color: #111;
}

.product-type {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 999px;
  background-color: #eee;
  font-size: 12px;
  color: #555;
}

.bank-code {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: #888;
}

.join-way {
  max-width: 180px;
  color: #555;
}

.sort-button {
  border: none;
  background: none;
  color: #222;
  font-weight: 800;
  cursor: pointer;
}

.detail-link {
  display: inline-block;
  padding: 7px 10px;
  border: 1px solid #333;
  color: #222;
  text-decoration: none;
  font-weight: 700;
}

.favorite-btn {
  min-width: 68px;
  padding: 7px 10px;
  border: 1px solid #bbb;
  background-color: #fff;
  color: #333;
  font-weight: 700;
  cursor: pointer;
}

.favorite-btn.active {
  background-color: #333;
  color: #fff;
  border-color: #333;
}

.favorite-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 1000px) {
  .filter-grid {
    grid-template-columns: 1fr 1fr;
  }

  .list-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
  }

  .favorite-message {
    white-space: normal;
  }
}

@media (max-width: 640px) {
  .product-list-view {
    padding: 18px;
  }

  .filter-grid {
    grid-template-columns: 1fr;
  }
}
</style>