<template>
  <div class="home-page">
    <section class="page-title">
      <p class="breadcrumb">FinBank</p>
      <h1>금융 생활 시작 가이드</h1>
    </section>

    <section class="hero-section">
      <p class="hero-label">예적금 · 주거래은행 · 환율 · 금은 시세</p>
      <h2>
        나에게 맞는 예적금과 주거래은행을<br />
        한 번에 찾아보세요
      </h2>

      <div class="hero-buttons">
        <RouterLink to="/main-bank" class="primary-btn">
          주거래은행 추천 시작하기 →
        </RouterLink>

        <RouterLink to="/products" class="secondary-btn">
          예금 상품 전체보기 →
        </RouterLink>
      </div>
    </section>

    <section class="preview-section">
      <div class="section-header">
        <div>
          <h3>인기 예금 상품 미리보기</h3>
          <p>최고 금리 기준으로 예금 상품을 먼저 보여줍니다.</p>
        </div>

        <RouterLink to="/products" class="all-link">
          전체 상품 보기
        </RouterLink>
      </div>

      <p v-if="loading" class="message">
        상품을 불러오는 중입니다...
      </p>

      <p v-else-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </p>

      <div v-else-if="previewProducts.length > 0" class="preview-grid">
        <article
          v-for="product in previewProducts"
          :key="product.id"
          class="preview-card"
        >
          <p class="bank-name">
            {{ product.bank?.name || '은행 정보 없음' }}
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
            :to="{ name: 'product-detail', params: { id: product.id } }"
            class="detail-link"
          >
            상품 보러가기
          </RouterLink>
        </article>
      </div>

      <div v-else class="empty-box">
        <h4>저장된 예금 상품이 없습니다.</h4>
        <p>
          먼저 백엔드에서 금융감독원 예금 상품 저장 API를 한 번 실행해야 합니다.
        </p>

        <code>http://127.0.0.1:8000/api/products/deposits/save/</code>

        <RouterLink to="/products" class="detail-link empty-link">
          상품조회 페이지로 이동
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { getDepositProducts } from '@/api/products'

const products = ref([])
const loading = ref(false)
const errorMessage = ref('')

const previewProducts = computed(() => {
  return [...products.value]
    .sort((a, b) => {
      const rateA = Number(a.max_interest_rate || 0)
      const rateB = Number(b.max_interest_rate || 0)
      return rateB - rateA
    })
    .slice(0, 4)
})

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

  // 예금 금리 5%를 100% 기준으로 잡음
  const percent = Math.min((numberRate / 5) * 100, 100)

  return `${percent}%`
}

const fetchPreviewProducts = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await getDepositProducts()

    products.value = Array.isArray(response.data) ? response.data : []
  } catch (error) {
    console.error(error)
    errorMessage.value =
      '예금 상품을 불러오지 못했습니다. /api/products/deposits/ API를 확인해주세요.'
  } finally {
    loading.value = false
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
  margin-top: 24px;
  padding: clamp(36px, 6vw, 64px) clamp(20px, 4vw, 44px);
  border: 1px solid #e5e7eb;
  border-radius: 22px;
  background:
    linear-gradient(135deg, rgba(37, 99, 235, 0.08), rgba(17, 24, 39, 0.04)),
    #ffffff;
  text-align: center;
  box-sizing: border-box;
}

.hero-label {
  margin: 0 0 16px;
  color: #2563eb;
  font-size: 14px;
  font-weight: 800;
}

.hero-section h2 {
  margin: 0;
  color: #111827;
  font-size: clamp(24px, 3vw, 38px);
  line-height: 1.45;
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

.preview-section {
  margin-top: 34px;
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
  font-size: 22px;
}

.section-header p {
  margin: 0;
  color: #6b7280;
  font-size: 14px;
}

.all-link {
  flex-shrink: 0;
  color: #2563eb;
  font-weight: 800;
  text-decoration: none;
}

.preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(255px, 1fr));
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
  margin: 0 0 12px;
  color: #6b7280;
}

.empty-box code {
  display: block;
  margin-bottom: 16px;
  padding: 12px;
  overflow-x: auto;
  border-radius: 10px;
  background: #111827;
  color: white;
}

.empty-link {
  max-width: 220px;
  background: white;
}

@media (max-width: 640px) {
  .home-page {
    padding: 14px;
  }

  .hero-section h2 br {
    display: none;
  }

  .primary-btn,
  .secondary-btn {
    width: 100%;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .product-info {
    flex-direction: column;
  }
}
</style>