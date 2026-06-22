<template>
  <main class="asset-page">
    <section class="page-header">
      <p class="eyebrow">Spot Asset Chart</p>
      <h1>금·은 가격 변동 시각화</h1>
      <p>
        제공된 금·은 가격 엑셀 데이터를 기반으로 기간별 가격 변동을 확인합니다.
      </p>
    </section>

    <section class="asset-card">
      <div class="toolbar">
        <div class="asset-buttons">
          <button
            type="button"
            :class="{ active: selectedAsset === 'gold' }"
            @click="changeAsset('gold')"
          >
            금 Gold
          </button>

          <button
            type="button"
            :class="{ active: selectedAsset === 'silver' }"
            @click="changeAsset('silver')"
          >
            은 Silver
          </button>
        </div>

        <div class="date-filters">
            <label>
            시작일
            <input
                v-model="startDate"
                type="date"
                :min="MIN_ASSET_DATE"
                :max="MAX_ASSET_DATE"
            />
            </label>

            <label>
            종료일
            <input
                v-model="endDate"
                type="date"
                :min="MIN_ASSET_DATE"
                :max="MAX_ASSET_DATE"
            />
            </label>

          <button type="button" class="search-button" @click="fetchPrices">
            조회
          </button>

          <button type="button" class="reset-button" @click="resetFilters">
            초기화
          </button>
        </div>
      </div>

      <p v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </p>

      <p v-if="loading" class="message">
        데이터를 불러오는 중입니다...
      </p>

      <template v-else>
        <section v-if="summary" class="summary-grid">
          <article class="summary-box">
            <span>조회 기간</span>
            <strong>{{ summary.first_date }} ~ {{ summary.latest_date }}</strong>
          </article>

          <article class="summary-box">
            <span>최근 종가</span>
            <strong>{{ formatPrice(summary.latest_close) }}</strong>
          </article>

          <article class="summary-box">
            <span>기간 변동</span>
            <strong :class="summary.change >= 0 ? 'up' : 'down'">
              {{ summary.change >= 0 ? '+' : '' }}{{ formatPrice(summary.change) }}
            </strong>
          </article>

          <article class="summary-box">
            <span>변동률</span>
            <strong :class="summary.change_rate >= 0 ? 'up' : 'down'">
              {{ summary.change_rate >= 0 ? '+' : '' }}{{ summary.change_rate }}%
            </strong>
          </article>
        </section>

        <section class="chart-area">
          <canvas ref="chartCanvas"></canvas>
        </section>

        <section v-if="priceRows.length" class="table-section">
          <div class="table-header">
            <h2>가격 데이터</h2>
            <p>총 {{ priceRows.length }}건</p>
          </div>

          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>날짜</th>
                  <th>종가</th>
                  <th>시가</th>
                  <th>고가</th>
                  <th>저가</th>
                  <th>거래량</th>
                </tr>
              </thead>

              <tbody>
                <tr v-for="row in priceRows" :key="row.date">
                  <td>{{ row.date }}</td>
                  <td>{{ formatPrice(row.close) }}</td>
                  <td>{{ formatPrice(row.open) }}</td>
                  <td>{{ formatPrice(row.high) }}</td>
                  <td>{{ formatPrice(row.low) }}</td>
                  <td>{{ formatVolume(row.volume) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </template>
    </section>
  </main>
</template>

<script setup>
import { nextTick, onMounted, ref } from 'vue'
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'
import api from '@/api/api'

Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend,
  Filler
)

const selectedAsset = ref('gold')

const MIN_ASSET_DATE = '2023-01-01'
const MAX_ASSET_DATE = '2024-12-31'

const startDate = ref(MIN_ASSET_DATE)
const endDate = ref(MAX_ASSET_DATE)
const priceRows = ref([])
const summary = ref(null)
const loading = ref(false)
const errorMessage = ref('')

const chartCanvas = ref(null)
const chartInstance = ref(null)

const assetLabelMap = {
  gold: '금',
  silver: '은',
}

const assetColorMap = {
  gold: {
    line: '#f59e0b',
    background: 'rgba(245, 158, 11, 0.16)',
  },
  silver: {
    line: '#64748b',
    background: 'rgba(100, 116, 139, 0.16)',
  },
}

const formatPrice = (value) => {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return '-'
  }

  return Number(value).toLocaleString(undefined, {
    minimumFractionDigits: 0,
    maximumFractionDigits: 3,
  })
}

const formatVolume = (value) => {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return '-'
  }

  return Number(value).toLocaleString(undefined, {
    maximumFractionDigits: 3,
  })
}

const validateDates = () => {
  if (!startDate.value || !endDate.value) {
    errorMessage.value = '시작일과 종료일을 모두 선택해주세요.'
    return false
  }

  if (startDate.value < MIN_ASSET_DATE || startDate.value > MAX_ASSET_DATE) {
    errorMessage.value = `시작일은 ${MIN_ASSET_DATE}부터 ${MAX_ASSET_DATE}까지만 선택할 수 있습니다.`
    return false
  }

  if (endDate.value < MIN_ASSET_DATE || endDate.value > MAX_ASSET_DATE) {
    errorMessage.value = `종료일은 ${MIN_ASSET_DATE}부터 ${MAX_ASSET_DATE}까지만 선택할 수 있습니다.`
    return false
  }

  if (startDate.value > endDate.value) {
    errorMessage.value = '시작일은 종료일보다 늦을 수 없습니다.'
    return false
  }

  return true
}

const destroyChart = () => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
    chartInstance.value = null
  }
}

const drawChart = async () => {
  await nextTick()

  destroyChart()

  if (!chartCanvas.value || priceRows.value.length === 0) {
    return
  }

  const colors = assetColorMap[selectedAsset.value]

  chartInstance.value = new Chart(chartCanvas.value, {
    type: 'line',
    data: {
      labels: priceRows.value.map((row) => row.date),
      datasets: [
        {
          label: `${assetLabelMap[selectedAsset.value]} 종가`,
          data: priceRows.value.map((row) => row.close),
          borderColor: colors.line,
          backgroundColor: colors.background,
          borderWidth: 2,
          pointRadius: priceRows.value.length > 60 ? 0 : 3,
          pointHoverRadius: 5,
          tension: 0.25,
          fill: true,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
        },
        tooltip: {
          callbacks: {
            label(context) {
              return `${context.dataset.label}: ${formatPrice(context.raw)}`
            },
          },
        },
      },
      scales: {
        x: {
          ticks: {
            maxRotation: 45,
            minRotation: 0,
            autoSkip: true,
            maxTicksLimit: 12,
          },
          grid: {
            display: false,
          },
        },
        y: {
          ticks: {
            callback(value) {
              return formatPrice(value)
            },
          },
        },
      },
    },
  })
}

const fetchPrices = async () => {
  errorMessage.value = ''

  if (!validateDates()) {
    destroyChart()
    priceRows.value = []
    summary.value = null
    return
  }

  loading.value = true

  let shouldDrawChart = false

  try {
    const response = await api.get('/assets/prices/', {
      params: {
        asset: selectedAsset.value,
        start_date: startDate.value,
        end_date: endDate.value,
      },
    })

    priceRows.value = response.data.rows || []
    summary.value = response.data.summary

    if (response.data.message) {
      errorMessage.value = response.data.message
    }

    shouldDrawChart = true
  } catch (error) {
    console.error(error)

    priceRows.value = []
    summary.value = null
    destroyChart()

    errorMessage.value =
      error.response?.data?.message ||
      '금·은 가격 데이터를 불러오는 중 오류가 발생했습니다.'
  } finally {
    loading.value = false
  }

  if (shouldDrawChart) {
    await drawChart()
  }
}

const changeAsset = async (asset) => {
  selectedAsset.value = asset
  await fetchPrices()
}

const resetFilters = async () => {
  startDate.value = MIN_ASSET_DATE
  endDate.value = MAX_ASSET_DATE
  await fetchPrices()
}

onMounted(() => {
  fetchPrices()
})
</script>

<style scoped>
.asset-page {
  max-width: 1180px;
  margin: 0 auto;
  padding: 40px 20px 80px;
}

.page-header {
  margin-bottom: 28px;
}

.eyebrow {
  margin: 0 0 8px;
  color: #2563eb;
  font-weight: 800;
}

.page-header h1 {
  margin: 0 0 10px;
  font-size: 34px;
  color: #111827;
}

.page-header p {
  margin: 0;
  color: #6b7280;
  line-height: 1.6;
}

.asset-card {
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  background: #ffffff;
  padding: 22px;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
}

.toolbar {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-end;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.asset-buttons {
  display: flex;
  gap: 10px;
}

.asset-buttons button,
.search-button,
.reset-button {
  border: none;
  border-radius: 10px;
  padding: 11px 16px;
  font-weight: 800;
  cursor: pointer;
}

.asset-buttons button {
  background: #f3f4f6;
  color: #374151;
}

.asset-buttons button.active {
  background: #111827;
  color: white;
}

.date-filters {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  flex-wrap: wrap;
}

.date-filters label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: #6b7280;
  font-size: 13px;
  font-weight: 700;
}

.date-filters input {
  border: 1px solid #d1d5db;
  border-radius: 10px;
  padding: 10px 12px;
  min-width: 150px;
}

.search-button {
  background: #2563eb;
  color: white;
}

.reset-button {
  background: #f3f4f6;
  color: #374151;
}

.message {
  color: #6b7280;
}

.error-message {
  margin: 10px 0 18px;
  padding: 12px 14px;
  border-radius: 10px;
  background: #fef2f2;
  color: #dc2626;
  font-weight: 700;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-bottom: 22px;
}

.summary-box {
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 16px;
  background: #f9fafb;
}

.summary-box span {
  display: block;
  margin-bottom: 8px;
  color: #6b7280;
  font-size: 13px;
  font-weight: 700;
}

.summary-box strong {
  color: #111827;
  font-size: 18px;
}

.summary-box strong.up {
  color: #dc2626;
}

.summary-box strong.down {
  color: #2563eb;
}

.chart-area {
  position: relative;
  height: 430px;
  padding: 18px;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  background: #ffffff;
}

.chart-area canvas {
  width: 100% !important;
  height: 100% !important;
}

.table-section {
  margin-top: 28px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.table-header h2 {
  margin: 0;
  font-size: 22px;
}

.table-header p {
  margin: 0;
  color: #6b7280;
  font-weight: 700;
}

.table-wrap {
  overflow-x: auto;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 760px;
}

th,
td {
  padding: 12px 14px;
  border-bottom: 1px solid #e5e7eb;
  text-align: right;
}

th:first-child,
td:first-child {
  text-align: left;
}

th {
  background: #f9fafb;
  color: #374151;
  font-size: 13px;
}

td {
  color: #111827;
}

tbody tr:hover {
  background: #f9fafb;
}

@media (max-width: 900px) {
  .summary-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .toolbar {
    align-items: stretch;
  }

  .date-filters {
    width: 100%;
  }
}

@media (max-width: 640px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }

  .asset-buttons,
  .date-filters {
    flex-direction: column;
    align-items: stretch;
  }

  .date-filters input,
  .search-button,
  .reset-button {
    width: 100%;
  }

  .chart-area {
    height: 340px;
  }
}
</style>