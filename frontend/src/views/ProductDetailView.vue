<template>
  <div class="product-detail-view">
    <div class="page-header">
      <p class="breadcrumb">상품 상세</p>
      <h1>{{ productTypeLabel }} 상품 상세</h1>
      <p class="description">
        상품의 가입 조건, 우대 조건, 기간별 금리 옵션을 확인해보세요.
      </p>
    </div>

    <p v-if="loading" class="status-message">상품 정보를 불러오는 중입니다...</p>
    <p v-else-if="errorMessage" class="status-message error">{{ errorMessage }}</p>

    <div v-else-if="product" class="detail-layout">
      <section class="product-summary-card">
        <div class="summary-header">
          <div>
            <p class="bank-name">{{ product.bank?.name }}</p>
            <h2>{{ product.name }}</h2>
          </div>

          <span class="product-type-badge">
            {{ productTypeLabel }}
          </span>
        </div>

        <div class="max-rate-box">
          <span>최고 금리</span>
          <strong>{{ getProductMaxRate(product) }}</strong>
        </div>

        <div class="summary-grid">
          <div>
            <span>은행 코드</span>
            <strong>{{ product.bank?.code || '정보 없음' }}</strong>
          </div>

          <div>
            <span>가입 방법</span>
            <strong>{{ product.join_way || '정보 없음' }}</strong>
          </div>

          <div>
            <span>가입 대상</span>
            <strong>{{ product.join_member || '정보 없음' }}</strong>
          </div>

          <div>
            <span>가입 한도</span>
            <strong>{{ formatLimit(product.max_limit) }}</strong>
          </div>
        </div>

        <div class="favorite-area">
          <button
            class="favorite-button"
            :class="{ active: isFavorite }"
            :disabled="favoriteLoading"
            @click="handleFavoriteClick"
          >
            <span v-if="favoriteLoading">
              처리 중...
            </span>
            <span v-else>
              {{ isFavorite ? '관심상품 삭제' : '관심상품 등록' }}
            </span>
          </button>

          <p v-if="favoriteMessage" class="favorite-message">
            {{ favoriteMessage }}
          </p>
        </div>
      </section>

      <section class="detail-card">
        <h3>상품 설명</h3>

        <div class="info-block">
          <h4>우대 조건</h4>
          <p>{{ product.spcl_cnd || '정보 없음' }}</p>
        </div>

        <div class="info-block">
          <h4>만기 후 이자율</h4>
          <p>{{ product.mtrt_int || '정보 없음' }}</p>
        </div>

        <div class="info-block">
          <h4>기타 유의사항</h4>
          <p>{{ product.etc_note || '정보 없음' }}</p>
        </div>

        <div class="date-grid">
          <p>공시 시작일: {{ product.dcls_strt_day || '정보 없음' }}</p>
          <p>공시 종료일: {{ product.dcls_end_day || '없음' }}</p>
          <p>공시 제출일: {{ product.fin_co_subm_day || '정보 없음' }}</p>
        </div>
      </section>

      <section class="detail-card option-section">
        <div class="section-title-row">
          <h3>금리 옵션</h3>
          <p>
            {{ productType === 'saving'
              ? '적금은 정액적립식/자유적립식에 따라 금리가 다를 수 있습니다.'
              : '기간별 기본 금리와 최고 우대 금리를 확인하세요.'
            }}
          </p>
        </div>

        <div v-if="product.options && product.options.length > 0" class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>저축 기간</th>
                <th>이자 유형</th>
                <th v-if="productType === 'saving'">적립 유형</th>
                <th>기본 금리</th>
                <th>최고 우대 금리</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="option in sortedOptions"
                :key="option.id"
              >
                <td>{{ option.save_trm }}개월</td>
                <td>{{ option.intr_rate_type_nm || '정보 없음' }}</td>
                <td v-if="productType === 'saving'">
                  {{ option.rsrv_type_nm || '정보 없음' }}
                </td>
                <td>{{ formatRate(option.intr_rate) }}</td>
                <td class="rate-highlight">{{ formatRate(option.intr_rate2) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <p v-else class="empty-message">금리 옵션 정보가 없습니다.</p>
      </section>

      <RouterLink :to="{ name: 'products' }" class="back-link">
        목록으로 돌아가기
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
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

    return rsrvA.localeCompare(rsrvB)
  })
})

const formatRate = (rate) => {
  if (rate === null || rate === undefined || rate === '') {
    return '정보 없음'
  }

  return `${Number(rate).toFixed(2)}%`
}

const formatLimit = (limit) => {
  if (limit === null || limit === undefined || limit === '') {
    return '정보 없음'
  }

  return `${Number(limit).toLocaleString()}원`
}

const getProductMaxRate = (targetProduct) => {
  if (!targetProduct) {
    return '정보 없음'
  }

  if (
    targetProduct.max_interest_rate !== null &&
    targetProduct.max_interest_rate !== undefined &&
    targetProduct.max_interest_rate !== ''
  ) {
    return `${Number(targetProduct.max_interest_rate).toFixed(2)}%`
  }

  if (!targetProduct.options || targetProduct.options.length === 0) {
    return '정보 없음'
  }

  const rates = targetProduct.options
    .map((option) => {
      if (
        option.intr_rate2 !== null &&
        option.intr_rate2 !== undefined &&
        option.intr_rate2 !== ''
      ) {
        return Number(option.intr_rate2)
      }

      if (
        option.intr_rate !== null &&
        option.intr_rate !== undefined &&
        option.intr_rate !== ''
      ) {
        return Number(option.intr_rate)
      }

      return null
    })
    .filter((rate) => rate !== null && !Number.isNaN(rate))

  if (rates.length === 0) {
    return '정보 없음'
  }

  return `${Math.max(...rates).toFixed(2)}%`
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
    errorMessage.value = '로그인 후 관심상품을 등록할 수 있습니다.'
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
  } catch (error) {
    console.error('관심상품 처리 에러:', error)

    if (error.response?.status === 401 || error.response?.status === 403) {
      errorMessage.value = '로그인 후 관심상품을 등록할 수 있습니다.'
      return
    }

    errorMessage.value = '관심상품 처리 중 오류가 발생했습니다.'
  } finally {
    favoriteLoading.value = false
  }
}

const fetchProductDetail = async () => {
  loading.value = true
  errorMessage.value = ''
  favoriteMessage.value = ''

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
    errorMessage.value = '상품 상세 정보를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProductDetail()
})
</script>

<style scoped>
.product-detail-view {
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

.status-message {
  padding: 18px;
  background-color: #fff;
  border: 1px solid #ddd;
  color: #555;
}

.status-message.error {
  color: #c0392b;
}

.detail-layout {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.product-summary-card,
.detail-card {
  padding: 22px;
  background-color: #fff;
  border: 1px solid #ddd;
}

.summary-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
}

.bank-name {
  margin: 0 0 6px;
  font-size: 14px;
  font-weight: 800;
  color: #555;
}

.summary-header h2 {
  margin: 0;
  font-size: 28px;
  color: #111;
}

.product-type-badge {
  height: fit-content;
  padding: 7px 12px;
  border-radius: 999px;
  background-color: #333;
  color: #fff;
  font-size: 13px;
  font-weight: 800;
  white-space: nowrap;
}

.max-rate-box {
  padding: 20px;
  margin-bottom: 20px;
  background-color: #f3f3f3;
}

.max-rate-box span {
  display: block;
  margin-bottom: 6px;
  color: #777;
  font-size: 14px;
}

.max-rate-box strong {
  font-size: 34px;
  color: #111;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.summary-grid div {
  padding: 14px;
  border: 1px solid #e5e5e5;
  background-color: #fafafa;
}

.summary-grid span {
  display: block;
  margin-bottom: 8px;
  color: #777;
  font-size: 13px;
  font-weight: 700;
}

.summary-grid strong {
  color: #222;
  font-size: 14px;
  line-height: 1.5;
}

.favorite-area {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.favorite-button {
  width: 180px;
  height: 42px;
  border: 1px solid #bbb;
  background-color: #fff;
  color: #333;
  font-weight: 800;
  cursor: pointer;
}

.favorite-button.active {
  background-color: #333;
  color: #fff;
  border-color: #333;
}

.favorite-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.favorite-message {
  margin: 0;
  padding: 9px 12px;
  border: 1px solid #bbf7d0;
  background-color: #f0fdf4;
  color: #15803d;
  font-size: 13px;
  font-weight: 800;
}

.detail-card h3 {
  margin: 0 0 16px;
  font-size: 20px;
}

.info-block {
  padding: 14px 0;
  border-bottom: 1px solid #eee;
}

.info-block:last-of-type {
  border-bottom: none;
}

.info-block h4 {
  margin: 0 0 8px;
  font-size: 15px;
  color: #333;
}

.info-block p {
  margin: 0;
  color: #555;
  line-height: 1.7;
  white-space: pre-line;
}

.date-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-top: 18px;
}

.date-grid p {
  padding: 12px;
  margin: 0;
  background-color: #fafafa;
  border: 1px solid #eee;
  color: #555;
  font-size: 14px;
}

.section-title-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 16px;
  margin-bottom: 14px;
}

.section-title-row h3 {
  margin: 0;
}

.section-title-row p {
  margin: 0;
  color: #777;
  font-size: 13px;
}

.table-wrap {
  overflow-x: auto;
  border: 1px solid #ddd;
}

table {
  width: 100%;
  min-width: 720px;
  border-collapse: collapse;
  background-color: #fff;
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

.rate-highlight {
  font-weight: 900;
  color: #111;
}

.empty-message {
  padding: 18px;
  background-color: #fafafa;
  border: 1px solid #eee;
  color: #666;
}

.back-link {
  width: fit-content;
  padding: 10px 14px;
  border: 1px solid #333;
  color: #222;
  background-color: #fff;
  text-decoration: none;
  font-weight: 800;
}

@media (max-width: 1000px) {
  .summary-grid,
  .date-grid {
    grid-template-columns: 1fr 1fr;
  }

  .section-title-row {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 640px) {
  .product-detail-view {
    padding: 18px;
  }

  .summary-header {
    flex-direction: column;
  }

  .summary-grid,
  .date-grid {
    grid-template-columns: 1fr;
  }

  .favorite-button {
    width: 100%;
  }
}
</style>