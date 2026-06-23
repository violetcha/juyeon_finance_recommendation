<template>
  <main class="exchange-page">
    <section class="page-header">
      <p class="eyebrow">Exchange Calculator</p>
      <h1>환율 계산기</h1>
      <p>
        한국수출입은행 환율 데이터를 기반으로 날짜별 환율 계산과 기간별 환율 추이를 확인합니다.
      </p>
    </section>

    <section class="exchange-card">
      <div class="top-bar">
        <div class="date-control">
          <label for="selected-date" class="label">조회 날짜</label>
          <input
            id="selected-date"
            v-model="selectedDate"
            type="date"
            @change="fetchRates"
          />
          <p class="date-help">
            API 기준일: <strong>{{ baseDate || '조회 전' }}</strong>
            <span v-if="baseDate && selectedDate !== baseDate">
              · 선택일 데이터가 없어 가까운 이전 영업일 기준으로 표시
            </span>
          </p>
        </div>

        <div class="top-actions">
          <button type="button" class="outline-button" @click="isRateDrawerOpen = true">
            환율 목록 보기
          </button>

          <button type="button" class="refresh-button" @click="fetchRates">
            환율 새로고침
          </button>
        </div>
      </div>

      <p v-if="loading" class="message">환율 정보를 불러오는 중입니다...</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <section class="calculator">
        <div class="amount-box">
          <label for="amount">금액</label>
          <input
            id="amount"
            v-model.number="amount"
            type="number"
            min="0"
            placeholder="금액을 입력하세요"
          />
        </div>

        <div class="currency-row">
          <div class="currency-box">
            <label for="from-currency">보내는 통화</label>
            <select id="from-currency" v-model="fromCurrency">
              <option
                v-for="currency in currencyOptions"
                :key="currency.code"
                :value="currency.code"
              >
                {{ currency.code }} · {{ currency.name }}
              </option>
            </select>
          </div>

          <button type="button" class="swap-button" @click="swapCurrencies">
            ⇄
          </button>

          <div class="currency-box">
            <label for="to-currency">받는 통화</label>
            <select id="to-currency" v-model="toCurrency">
              <option
                v-for="currency in currencyOptions"
                :key="currency.code"
                :value="currency.code"
              >
                {{ currency.code }} · {{ currency.name }}
              </option>
            </select>
          </div>
        </div>

        <div class="result-box">
          <p>계산 결과</p>
          <strong>{{ formattedResult }} {{ toCurrency }}</strong>
          <span>
            {{ formatAmount(amount) }} {{ fromCurrency }}
            =
            {{ formattedResult }} {{ toCurrency }}
          </span>
        </div>
      </section>

      <section class="info-grid">
        <article>
          <span>보내는 통화</span>
          <strong>{{ getRateText(fromCurrency) }}</strong>
        </article>

        <article>
          <span>받는 통화</span>
          <strong>{{ getRateText(toCurrency) }}</strong>
        </article>

        <article>
          <span>계산 방식</span>
          <strong>KRW 기준 교차환산</strong>
        </article>
      </section>

      <section class="history-section">
        <div class="history-header">
          <div>
            <p class="eyebrow">Exchange Trend</p>
            <h2>기간별 환율 그래프</h2>
            <p>최대 31일 범위에서 선택한 통화의 환율 추이를 확인합니다.</p>
          </div>
        </div>

        <div class="history-controls">
          <div class="history-field">
            <label for="chart-currency">그래프 통화</label>
            <select id="chart-currency" v-model="chartCurrency">
              <option
                v-for="currency in chartCurrencyOptions"
                :key="currency.code"
                :value="currency.code"
              >
                {{ currency.code }} · {{ currency.name }}
              </option>
            </select>
          </div>

          <div class="history-field">
            <label for="start-date">시작일</label>
            <input id="start-date" v-model="startDate" type="date" />
          </div>

          <div class="history-field">
            <label for="end-date">종료일</label>
            <input id="end-date" v-model="endDate" type="date" />
          </div>

          <button type="button" class="history-button" @click="fetchHistory">
            그래프 조회
          </button>
        </div>

        <p v-if="historyLoading" class="message">기간별 환율 데이터를 불러오는 중입니다...</p>
        <p v-if="historyError" class="error-message">{{ historyError }}</p>

        <div class="chart-card">
          <canvas ref="chartCanvas"></canvas>
        </div>

        <p v-if="historyRows.length > 0" class="chart-caption">
          {{ historyRows[0].date }} ~ {{ historyRows[historyRows.length - 1].date }}
          · {{ chartCurrency }} 기준
        </p>
      </section>
    </section>

    <div
      v-if="isRateDrawerOpen"
      class="drawer-backdrop"
      @click="isRateDrawerOpen = false"
    ></div>

    <aside class="rate-drawer" :class="{ open: isRateDrawerOpen }">
      <div class="drawer-header">
        <div>
          <p class="eyebrow">Rate List</p>
          <h2>환율 목록</h2>
          <span>총 {{ rates.length }}개 통화</span>
        </div>

        <button type="button" @click="isRateDrawerOpen = false">
          ✕
        </button>
      </div>

      <div class="drawer-search">
        <input
          v-model.trim="drawerKeyword"
          type="text"
          placeholder="통화 코드 또는 통화명 검색"
        />
      </div>

      <div class="drawer-list">
        <button
          v-for="rate in filteredDrawerRates"
          :key="rate.code"
          type="button"
          class="drawer-rate-item"
          @click="selectRateFromDrawer(rate)"
        >
          <div>
            <strong>{{ rate.code }}</strong>
            <span>{{ rate.name }}</span>
          </div>

          <em>{{ formatRate(rate.ratePerUnit) }} KRW</em>
        </button>

        <p v-if="filteredDrawerRates.length === 0" class="drawer-empty">
          검색된 통화가 없습니다.
        </p>
      </div>

      <div class="drawer-safe-area"></div>
    </aside>
  </main>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
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

const today = new Date()

const toDateInputValue = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

const getDateBefore = (days) => {
  const date = new Date()
  date.setDate(date.getDate() - days)
  return toDateInputValue(date)
}

const amount = ref(1000)
const fromCurrency = ref('KRW')
const toCurrency = ref('USD')

const selectedDate = ref(toDateInputValue(today))
const startDate = ref(getDateBefore(7))
const endDate = ref(toDateInputValue(today))
const chartCurrency = ref('USD')

const rates = ref([])
const baseDate = ref('')
const loading = ref(false)
const errorMessage = ref('')

const historyRows = ref([])
const historyLoading = ref(false)
const historyError = ref('')
const chartCanvas = ref(null)
const chartInstance = ref(null)

const isRateDrawerOpen = ref(false)
const drawerKeyword = ref('')

const krwRate = {
  code: 'KRW',
  name: '대한민국 원',
  ratePerUnit: 1,
  displayUnit: '1 KRW',
}

const currencyOptions = computed(() => {
  return [krwRate, ...rates.value]
})

const chartCurrencyOptions = computed(() => {
  return rates.value
})

const filteredDrawerRates = computed(() => {
  const keyword = drawerKeyword.value.toLowerCase()

  if (!keyword) {
    return rates.value
  }

  return rates.value.filter((rate) => {
    return (
      rate.code.toLowerCase().includes(keyword) ||
      rate.name.toLowerCase().includes(keyword)
    )
  })
})

const selectedFromRate = computed(() => {
  return currencyOptions.value.find((item) => item.code === fromCurrency.value)
})

const selectedToRate = computed(() => {
  return currencyOptions.value.find((item) => item.code === toCurrency.value)
})

const convertedAmount = computed(() => {
  const from = selectedFromRate.value
  const to = selectedToRate.value

  if (!from || !to) {
    return 0
  }

  const numericAmount = Number(amount.value)

  if (!numericAmount || numericAmount < 0) {
    return 0
  }

  const amountInKrw = numericAmount * from.ratePerUnit
  return amountInKrw / to.ratePerUnit
})

const formattedResult = computed(() => {
  return formatAmount(convertedAmount.value)
})

const parseRateNumber = (value) => {
  if (value === null || value === undefined) {
    return 0
  }

  return Number(String(value).replaceAll(',', '').trim()) || 0
}

const parseCurrencyUnit = (currencyCode) => {
  const code = String(currencyCode || '').trim()

  if (code.includes('(100)')) {
    const normalizedCode = code.replace('(100)', '').trim()

    return {
      code: normalizedCode,
      unit: 100,
      displayUnit: `100 ${normalizedCode}`,
    }
  }

  return {
    code,
    unit: 1,
    displayUnit: `1 ${code}`,
  }
}

const normalizeRate = (item) => {
  const parsedUnit = parseCurrencyUnit(item.currency_code)
  const rawRate = item.raw_rate || parseRateNumber(item.rate)
  const ratePerUnit = item.rate_per_unit || rawRate / parsedUnit.unit

  return {
    code: item.normalized_code || parsedUnit.code,
    name: item.currency_name || parsedUnit.code,
    rawRate,
    unit: item.unit || parsedUnit.unit,
    ratePerUnit,
    displayUnit: item.display_unit || parsedUnit.displayUnit,
  }
}

const fetchRates = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await api.get('/exchanges/rates/', {
      params: {
        date: selectedDate.value,
      },
    })

    baseDate.value = response.data.date || ''

    rates.value = (response.data.rates || [])
      .map(normalizeRate)
      .filter((item) => item.code && item.ratePerUnit > 0)

    if (rates.value.length === 0) {
      errorMessage.value = '환율 데이터가 비어 있습니다.'
      return
    }

    if (!rates.value.some((item) => item.code === toCurrency.value)) {
      const usd = rates.value.find((item) => item.code === 'USD')
      toCurrency.value = usd ? 'USD' : rates.value[0].code
    }

    if (!rates.value.some((item) => item.code === chartCurrency.value)) {
      const usd = rates.value.find((item) => item.code === 'USD')
      chartCurrency.value = usd ? 'USD' : rates.value[0].code
    }
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error.response?.data?.message ||
      '환율 정보를 불러오지 못했습니다. 백엔드 exchanges API를 확인해주세요.'
  } finally {
    loading.value = false
  }
}

const fetchHistory = async () => {
  historyLoading.value = true
  historyError.value = ''

  try {
    const response = await api.get('/exchanges/history/', {
      params: {
        currency: chartCurrency.value,
        start_date: startDate.value,
        end_date: endDate.value,
      },
    })

    historyRows.value = response.data.rows || []

    if (historyRows.value.length === 0) {
      historyError.value = '그래프를 그릴 환율 데이터가 없습니다.'
      destroyChart()
      return
    }

    await nextTick()
    drawChart()
  } catch (error) {
    console.error(error)

    historyRows.value = []
    destroyChart()

    historyError.value =
      error.response?.data?.message ||
      '기간별 환율 데이터를 불러오지 못했습니다.'
  } finally {
    historyLoading.value = false
  }
}

const destroyChart = () => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
    chartInstance.value = null
  }
}

const drawChart = () => {
  if (!chartCanvas.value) return

  destroyChart()

  const labels = historyRows.value.map((row) => row.date)
  const data = historyRows.value.map((row) => Number(row.rate))

  chartInstance.value = new Chart(chartCanvas.value, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: `${chartCurrency.value} 환율`,
          data,
          fill: true,
          tension: 0.35,
          pointRadius: 3,
          pointHoverRadius: 5,
          borderWidth: 3,
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
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              return `${context.dataset.label}: ${formatRate(context.raw)} KRW`
            },
          },
        },
      },
      scales: {
        y: {
          ticks: {
            callback: (value) => `${formatRate(value)} KRW`,
          },
        },
      },
    },
  })
}

const swapCurrencies = () => {
  const temp = fromCurrency.value
  fromCurrency.value = toCurrency.value
  toCurrency.value = temp
}

const selectRateFromDrawer = (rate) => {
  toCurrency.value = rate.code
  chartCurrency.value = rate.code
  isRateDrawerOpen.value = false
}

const formatAmount = (value) => {
  const numberValue = Number(value)

  if (Number.isNaN(numberValue)) {
    return '0'
  }

  return numberValue.toLocaleString(undefined, {
    minimumFractionDigits: 0,
    maximumFractionDigits: 4,
  })
}

const formatRate = (value) => {
  const numberValue = Number(value)

  if (Number.isNaN(numberValue)) {
    return '-'
  }

  return numberValue.toLocaleString(undefined, {
    minimumFractionDigits: 0,
    maximumFractionDigits: 4,
  })
}

const getRateText = (code) => {
  const currency = currencyOptions.value.find((item) => item.code === code)

  if (!currency) {
    return '-'
  }

  if (currency.code === 'KRW') {
    return '1 KRW'
  }

  return `1 ${currency.code} = ${formatRate(currency.ratePerUnit)} KRW`
}

onMounted(async () => {
  await fetchRates()
  await fetchHistory()
})

onBeforeUnmount(() => {
  destroyChart()
})
</script>

<style scoped>
.exchange-page {
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
  font-size: 36px;
  color: #111827;
}

.page-header p {
  margin: 0;
  color: #6b7280;
  line-height: 1.6;
}

.exchange-card {
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  background: #ffffff;
  padding: 24px;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 22px;
  flex-wrap: wrap;
}

.date-control {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.date-control input,
.history-field input,
.history-field select,
.drawer-search input {
  border: 1px solid #d1d5db;
  border-radius: 10px;
  padding: 11px 12px;
  background: white;
  color: #111827;
}

.date-help {
  margin: 0;
  color: #6b7280;
  font-size: 13px;
}

.label {
  margin: 0;
  color: #6b7280;
  font-size: 13px;
  font-weight: 800;
}

.top-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.refresh-button,
.outline-button,
.history-button {
  border: none;
  border-radius: 10px;
  padding: 11px 16px;
  background: #111827;
  color: white;
  font-weight: 800;
  cursor: pointer;
}

.outline-button {
  border: 1px solid #d1d5db;
  background: white;
  color: #111827;
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

.calculator {
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 22px;
  background: #f9fafb;
}

.amount-box,
.currency-box,
.history-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.amount-box label,
.currency-box label,
.history-field label {
  color: #6b7280;
  font-size: 13px;
  font-weight: 800;
}

.amount-box input,
.currency-box select {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  padding: 13px 14px;
  background: white;
  color: #111827;
  font-size: 16px;
}

.currency-row {
  display: grid;
  grid-template-columns: 1fr 54px 1fr;
  gap: 14px;
  align-items: end;
  margin-top: 18px;
}

.swap-button {
  width: 54px;
  height: 48px;
  border: none;
  border-radius: 12px;
  background: #2563eb;
  color: white;
  font-size: 22px;
  font-weight: 900;
  cursor: pointer;
}

.result-box {
  margin-top: 22px;
  border-radius: 16px;
  padding: 24px;
  background: #111827;
  color: white;
}

.result-box p {
  margin: 0 0 8px;
  color: #d1d5db;
  font-size: 14px;
  font-weight: 800;
}

.result-box strong {
  display: block;
  margin-bottom: 8px;
  font-size: 34px;
}

.result-box span {
  color: #d1d5db;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin-top: 18px;
}

.info-grid article {
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 16px;
  background: white;
}

.info-grid span {
  display: block;
  margin-bottom: 8px;
  color: #6b7280;
  font-size: 13px;
  font-weight: 800;
}

.info-grid strong {
  color: #111827;
}

.history-section {
  margin-top: 32px;
}

.history-header {
  margin-bottom: 16px;
}

.history-header h2 {
  margin: 0 0 8px;
  font-size: 24px;
  color: #111827;
}

.history-header p {
  margin: 0;
  color: #6b7280;
}

.history-controls {
  display: grid;
  grid-template-columns: 1.2fr 1fr 1fr auto;
  gap: 12px;
  align-items: end;
  margin-bottom: 16px;
}

.history-button {
  height: 43px;
  background: #2563eb;
}

.chart-card {
  position: relative;
  height: 360px;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 16px;
  background: #ffffff;
}

.chart-card canvas {
  width: 100% !important;
  height: 100% !important;
}

.chart-caption {
  margin: 10px 0 0;
  color: #6b7280;
  font-size: 13px;
  font-weight: 700;
}

.drawer-safe-area {
  flex-shrink: 0;
  height: 110px;
}

.drawer-backdrop {
  position: fixed;
  inset: 0;
  z-index: 90;
  background: rgba(15, 23, 42, 0.35);
}

.rate-drawer {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 100;
  width: min(420px, 92vw);
  height: 100vh;
  padding: 22px;
  background: #ffffff;
  box-shadow: -18px 0 36px rgba(15, 23, 42, 0.18);
  transform: translateX(105%);
  transition: transform 0.25s ease;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.rate-drawer.open {
  transform: translateX(0);
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 16px;
}

.drawer-header h2 {
  margin: 0 0 6px;
  font-size: 24px;
}

.drawer-header span {
  color: #6b7280;
  font-size: 13px;
  font-weight: 700;
}

.drawer-header button {
  border: none;
  border-radius: 10px;
  padding: 9px 12px;
  background: #111827;
  color: white;
  cursor: pointer;
}

.drawer-search {
  margin-bottom: 14px;
}

.drawer-search input {
  width: 100%;
  box-sizing: border-box;
}

.drawer-list {
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-right: 4px;
}

.drawer-rate-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  width: 100%;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 13px;
  background: #ffffff;
  text-align: left;
  cursor: pointer;
}

.drawer-rate-item:hover {
  border-color: #2563eb;
  background: #f8fbff;
}

.drawer-rate-item strong {
  display: block;
  color: #111827;
  font-size: 16px;
}

.drawer-rate-item span {
  display: block;
  margin-top: 3px;
  color: #6b7280;
  font-size: 13px;
}

.drawer-rate-item em {
  color: #2563eb;
  font-style: normal;
  font-weight: 900;
  white-space: nowrap;
}

.drawer-empty {
  color: #6b7280;
}

@media (max-width: 900px) {
  .history-controls,
  .currency-row,
  .info-grid {
    grid-template-columns: 1fr;
  }

  .swap-button {
    width: 100%;
  }

  .result-box strong {
    font-size: 28px;
  }


}
</style>