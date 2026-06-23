<template>
  <div class="mypage-view">
    <section class="page-header">
      <h1>마이페이지</h1>
      <p>관심상품으로 저장한 예금과 적금을 확인할 수 있습니다.</p>
    </section>

    <section class="mypage-section">
      <h2>관심상품 목록</h2>

      <p v-if="loading" class="status-message">
        관심상품을 불러오는 중입니다...
      </p>

      <p v-else-if="errorMessage" class="status-message error">
        {{ errorMessage }}
      </p>

      <div v-else>
        <p v-if="favoriteProducts.length === 0" class="status-message">
          등록된 관심상품이 없습니다.
        </p>

        <template v-else>
          <section class="favorite-group">
            <div class="group-header">
              <h3>관심 정기예금</h3>
              <span>{{ depositFavorites.length }}개</span>
            </div>

            <p v-if="depositFavorites.length === 0" class="empty-message">
              등록된 관심 정기예금이 없습니다.
            </p>

            <div
              v-for="favorite in depositFavorites"
              :key="favorite.id"
              class="favorite-card"
            >
              <div>
                <span class="product-type-badge">정기예금</span>
                <h4>{{ getProductName(favorite) }}</h4>

                <p>은행명: {{ getBankName(favorite) }}</p>
                <p>최고 금리: {{ formatRate(getMaxInterestRate(favorite)) }}</p>
              </div>

              <RouterLink
                class="detail-link"
                :to="{
                  name: 'product-detail',
                  params: { id: getProductId(favorite) },
                  query: { type: getProductType(favorite) }
                }"
              >
                상세 보기
              </RouterLink>
            </div>
          </section>

          <section class="favorite-group">
            <div class="group-header">
              <h3>관심 적금</h3>
              <span>{{ savingFavorites.length }}개</span>
            </div>

            <p v-if="savingFavorites.length === 0" class="empty-message">
              등록된 관심 적금이 없습니다.
            </p>

            <div
              v-for="favorite in savingFavorites"
              :key="favorite.id"
              class="favorite-card"
            >
              <div>
                <span class="product-type-badge saving">적금</span>
                <h4>{{ getProductName(favorite) }}</h4>

                <p>은행명: {{ getBankName(favorite) }}</p>
                <p>최고 금리: {{ formatRate(getMaxInterestRate(favorite)) }}</p>
              </div>

              <RouterLink
                class="detail-link"
                :to="{
                  name: 'product-detail',
                  params: { id: getProductId(favorite) },
                  query: { type: getProductType(favorite) }
                }"
              >
                상세 보기
              </RouterLink>
            </div>
          </section>
        </template>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { getFavoriteProducts } from '@/api/favorites'

const favoriteProducts = ref([])
const loading = ref(false)
const errorMessage = ref('')

const getProduct = (favorite) => {
  return favorite.product || favorite
}

const depositFavorites = computed(() => {
  return favoriteProducts.value.filter((favorite) => {
    const product = getProduct(favorite)
    return product.product_type === 'deposit'
  })
})

const savingFavorites = computed(() => {
  return favoriteProducts.value.filter((favorite) => {
    const product = getProduct(favorite)
    return product.product_type === 'saving'
  })
})

const formatRate = (rate) => {
  if (rate === null || rate === undefined || rate === '') {
    return '정보 없음'
  }

  return `${Number(rate).toFixed(2)}%`
}

const getProductId = (favorite) => {
  const product = getProduct(favorite)
  return product.id
}

const getProductType = (favorite) => {
  const product = getProduct(favorite)
  return product.product_type || 'deposit'
}

const getProductName = (favorite) => {
  const product = getProduct(favorite)
  return product.name || '상품명 없음'
}

const getBankName = (favorite) => {
  const product = getProduct(favorite)
  return product.bank?.name || '은행명 없음'
}

const getMaxInterestRate = (favorite) => {
  const product = getProduct(favorite)

  if (
    product.max_interest_rate !== null &&
    product.max_interest_rate !== undefined &&
    product.max_interest_rate !== ''
  ) {
    return product.max_interest_rate
  }

  if (!product.options || product.options.length === 0) {
    return null
  }

  const rates = product.options
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
    return null
  }

  return Math.max(...rates)
}

const fetchFavoriteProducts = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await getFavoriteProducts()

    console.log('관심상품 목록 응답:', response.data)

    favoriteProducts.value = response.data
  } catch (error) {
    console.error(error)

    if (error.response?.status === 401) {
      errorMessage.value = '로그인이 필요한 기능입니다.'
      return
    }

    errorMessage.value = '관심상품 목록을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchFavoriteProducts()
})
</script>

<style scoped>
.mypage-view {
  min-height: 100vh;
  padding: 28px;
  background-color: #f6f7f9;
}

.page-header {
  padding-bottom: 18px;
  margin-bottom: 18px;
  border-bottom: 1px solid #ddd;
}

.page-header h1 {
  margin: 0;
  font-size: 26px;
  color: #111;
}

.page-header p {
  margin: 8px 0 0;
  color: #666;
}

.mypage-section {
  padding: 22px;
  background-color: #fff;
  border: 1px solid #ddd;
}

.mypage-section h2 {
  margin: 0 0 20px;
  font-size: 20px;
}

.status-message {
  padding: 18px;
  background-color: #fafafa;
  border: 1px solid #eee;
  color: #555;
}

.status-message.error {
  color: #c0392b;
}

.favorite-group {
  margin-top: 24px;
}

.favorite-group:first-child {
  margin-top: 0;
}

.group-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.group-header h3 {
  margin: 0;
  font-size: 18px;
}

.group-header span {
  color: #777;
  font-size: 14px;
}

.empty-message {
  padding: 14px;
  margin: 0;
  background-color: #fafafa;
  border: 1px solid #eee;
  color: #777;
}

.favorite-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 16px;
  margin-bottom: 12px;
  border: 1px solid #ddd;
  background-color: #fff;
}

.product-type-badge {
  display: inline-block;
  padding: 4px 9px;
  margin-bottom: 8px;
  border-radius: 999px;
  background-color: #333;
  color: #fff;
  font-size: 12px;
  font-weight: 800;
}

.product-type-badge.saving {
  background-color: #555;
}

.favorite-card h4 {
  margin: 0 0 8px;
  font-size: 17px;
  color: #111;
}

.favorite-card p {
  margin: 4px 0;
  color: #555;
  font-size: 14px;
}

.detail-link {
  flex-shrink: 0;
  padding: 9px 12px;
  border: 1px solid #333;
  color: #222;
  background-color: #fff;
  text-decoration: none;
  font-weight: 800;
}

@media (max-width: 640px) {
  .mypage-view {
    padding: 18px;
  }

  .favorite-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .detail-link {
    width: 100%;
    text-align: center;
  }
}
</style>