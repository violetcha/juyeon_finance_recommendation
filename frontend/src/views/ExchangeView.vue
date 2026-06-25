<template>
  <main class="exchange-page">
    <section class="page-hero-row">
      <h1 class="page-title">
        <span class="title-blue">환율</span>
        <span> 계산 · 시세 확인</span>
      </h1>
    </section>

    <section class="exchange-grid">
      <article class="calculator-card card">
        <div class="card-title-row">
          <div>
            <h2>환율 계산기</h2>
            
          </div>
        </div>

        <div class="date-box">
          <label for="selected-date">조회 날짜</label>
          <input
            id="selected-date"
            v-model="selectedDate"
            type="date"
            @change="handleSelectedDateChange"
          >
        </div>

        <p v-if="loading" class="state-message compact">환율 정보를 불러오는 중입니다...</p>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <div class="converter-box">
          <div class="currency-input-card">
            <label>보내는 통화</label>
            <div class="currency-line">
              <select v-model="fromCurrency">
                <option
                  v-for="currency in currencyOptions"
                  :key="currency.code"
                  :value="currency.code"
                >
                  {{ currency.code }} · {{ currency.name }}
                </option>
              </select>

              <input
                v-model.number="amount"
                type="number"
                min="0"
                placeholder="금액"
              >
            </div>
            <span>{{ getRateText(fromCurrency) }}</span>
          </div>

          <button type="button" class="swap-button" @click="swapCurrencies">
            ⇅
          </button>

          <div class="currency-input-card">
            <label>받는 통화</label>
            <div class="currency-line">
              <select v-model="toCurrency">
                <option
                  v-for="currency in currencyOptions"
                  :key="currency.code"
                  :value="currency.code"
                >
                  {{ currency.code }} · {{ currency.name }}
                </option>
              </select>

              <input
                :value="formattedResult"
                type="text"
                readonly
              >
            </div>
            <span>{{ getRateText(toCurrency) }}</span>
          </div>
        </div>

        <div class="result-strip">
          <span>계산 결과</span>
          <strong>{{ formatAmount(amount) }} {{ fromCurrency }} = {{ formattedResult }} {{ toCurrency }}</strong>
        </div>

        <button type="button" class="primary-button" @click="fetchRates">
          환율 새로고침
        </button>

      </article>

      <article class="rates-card card">
        <div class="card-title-row">
          <div>
            <h2>실시간 주요 통화 시세</h2>
            <p>{{ baseDate || selectedDate }} 기준 · 주요 통화만 요약 표시</p>
          </div>

          <button type="button" class="outline-button" @click="isRateDrawerOpen = true">
            전체 통화 보기
          </button>
        </div>

        <div class="rate-table">
          <div class="rate-table-head">
            <span>통화</span>
            <span>매매기준율</span>
            <span>전일대비</span>
            <span>등락률</span>
          </div>

          <button
            v-for="rate in mainCurrencyRates"
            :key="rate.code"
            type="button"
            class="rate-row"
            @click="selectRateFromTable(rate)"
          >
            <div class="currency-name">
              <strong>{{ rate.code }}</strong>
              <span>{{ rate.name }}</span>
            </div>

            <strong>{{ formatRate(rate.ratePerUnit) }}</strong>

            <span :class="getChangeClass(rate.code)">
              {{ formatRateChange(rate.code) }}
            </span>

            <span :class="getChangeClass(rate.code)">
              {{ formatChangeRate(rate.code) }}
            </span>
          </button>

          <p v-if="!loading && mainCurrencyRates.length === 0" class="state-message compact">
            표시할 환율 데이터가 없습니다.
          </p>
        </div>
      </article>
    </section>

    <section id="exchange-chart" class="chart-grid">
      <article class="chart-card card">
        <div class="card-title-row">
          <div>
            <h2>{{ chartCurrency }}/KRW 환율 추이</h2>
            
          </div>
        </div>

        <div class="chart-controls">
          <select v-model="chartCurrency" :disabled="chartCurrencyOptions.length === 0">
            <option
              v-for="currency in chartCurrencyOptions"
              :key="currency.code"
              :value="currency.code"
            >
              {{ currency.code }} · {{ currency.name }}
            </option>
          </select>

          <div class="preset-group">
            <button type="button" @click="setExchangePreset(7)">1W</button>
            <button type="button" @click="setExchangePreset(14)">2W</button>
            <button type="button" @click="setExchangePreset(30)">1M</button>
          </div>

          <div class="chart-date-action-group">
            <input v-model="startDate" type="date">
            <input v-model="endDate" type="date">

            <button type="button" class="primary-button small" :disabled="!chartCurrency || historyLoading" @click="fetchHistory">
              그래프 조회
            </button>
          </div>
        </div>

        <p v-if="historyLoading" class="state-message compact">기간별 환율 데이터를 불러오는 중입니다...</p>
        <p v-if="historyError" class="error-message">{{ historyError }}</p>

        <div class="canvas-wrap chart-surface">
          <svg
            v-if="exchangeChart.points.length > 0"
            class="line-chart"
            viewBox="0 0 1000 340"
            role="img"
            :aria-label="`${chartCurrency}/KRW 환율 추이 그래프`"
            @mouseleave="hoveredExchangePoint = null"
          >
            <defs>
              <linearGradient id="exchangeGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#1116b8" stop-opacity="0.18" />
                <stop offset="100%" stop-color="#1116b8" stop-opacity="0.02" />
              </linearGradient>
            </defs>

            <g>
              <line
                v-for="tick in exchangeChart.yTicks"
                :key="tick.label"
                x1="64"
                x2="960"
                :y1="tick.y"
                :y2="tick.y"
                class="chart-grid-line"
              />
              <text
                v-for="tick in exchangeChart.yTicks"
                :key="`${tick.label}-text`"
                x="50"
                :y="tick.y + 4"
                class="chart-y-label"
                text-anchor="end"
              >
                {{ tick.label }}
              </text>
            </g>

            <path :d="exchangeChart.areaPath" fill="url(#exchangeGradient)" />
            <polyline :points="exchangeChart.polyline" class="chart-line exchange" />

            <circle
              v-for="point in exchangeChart.points"
              :key="point.date"
              :cx="point.x"
              :cy="point.y"
              r="4"
              class="chart-point exchange"
            >
              <title>{{ point.date }} · {{ formatRate(point.value) }} KRW</title>
            </circle>

            <circle
              v-for="point in exchangeChart.points"
              :key="`${point.date}-hover`"
              :cx="point.x"
              :cy="point.y"
              r="12"
              class="chart-hover-target"
              @mouseenter="hoveredExchangePoint = point"
              @mousemove="hoveredExchangePoint = point"
            />

            <g
              v-if="hoveredExchangePoint"
              class="chart-tooltip"
              :transform="getTooltipTransform(hoveredExchangePoint)"
            >
              <rect width="194" height="62" rx="14" />
              <text x="14" y="24" class="tooltip-date">
                {{ hoveredExchangePoint.date }}
              </text>
              <text x="14" y="46" class="tooltip-value">
                {{ chartCurrency }}/KRW {{ formatRate(hoveredExchangePoint.value) }}
              </text>
            </g>

            <text x="64" y="326" class="chart-x-label">{{ exchangeChart.firstLabel }}</text>
            <text x="960" y="326" class="chart-x-label" text-anchor="end">{{ exchangeChart.lastLabel }}</text>
          </svg>

          <p v-else class="state-message compact">
            그래프를 표시할 데이터가 없습니다.
          </p>
        </div>

        <p v-if="historyRows.length > 0" class="chart-caption">
          {{ historyRows[0].date }} ~ {{ historyRows[historyRows.length - 1].date }}
          · {{ chartCurrency }} 기준 · {{ historyRows.length }}건
        </p>
      </article>

      <article class="summary-card card">
        <div class="card-title-row">
          <div>
            <h2>오늘의 환율 요약</h2>
            <p>현재 그래프 통화 기준</p>
          </div>
        </div>

        <dl class="summary-list">
          <div>
            <dt>현재 기준환율</dt>
            <dd>{{ formatRate(getCurrentRate(chartCurrency)) }} KRW</dd>
          </div>
          <div>
            <dt>조회 기간 시작</dt>
            <dd>{{ historyRows[0]?.date || '-' }}</dd>
          </div>
          <div>
            <dt>조회 기간 종료</dt>
            <dd>{{ historyRows[historyRows.length - 1]?.date || '-' }}</dd>
          </div>
          <div>
            <dt>기간 내 최저</dt>
            <dd>{{ formatRate(exchangeSummary.min) }} KRW</dd>
          </div>
          <div>
            <dt>기간 내 최고</dt>
            <dd>{{ formatRate(exchangeSummary.max) }} KRW</dd>
          </div>
          <div>
            <dt>기간 변동률</dt>
            <dd :class="exchangeSummary.changeRate >= 0 ? 'up' : 'down'">
              {{ exchangeSummary.changeRate >= 0 ? '+' : '' }}{{ formatRate(exchangeSummary.changeRate) }}%
            </dd>
          </div>
        </dl>
      </article>
    </section>

    <div
      v-if="isRateDrawerOpen"
      class="drawer-backdrop"
      @click="isRateDrawerOpen = false"
    ></div>

    <aside class="rate-drawer" :class="{ open: isRateDrawerOpen }">
      <div class="drawer-header">
        <div>
          <p class="eyebrow">RATE LIST</p>
          <h2>전체 환율 목록</h2>
          <span>총 {{ rates.length }}개 통화</span>
        </div>

        <button type="button" @click="isRateDrawerOpen = false">
          ✕
        </button>
      </div>

      <input
        v-model.trim="drawerKeyword"
        class="drawer-search"
        type="text"
        placeholder="통화 코드 또는 통화명 검색"
      >

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

        <p v-if="filteredDrawerRates.length === 0" class="state-message compact">
          검색된 통화가 없습니다.
        </p>
      </div>
    </aside>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '@/api/api'

const today = new Date()
const toDateInputValue = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const getDateBefore = (days, base = new Date()) => {
  const date = new Date(base)
  date.setDate(date.getDate() - days)
  return toDateInputValue(date)
}

const getPreviousDay = (dateString) => {
  const date = new Date(dateString)
  date.setDate(date.getDate() - 1)
  return toDateInputValue(date)
}

const selectedDate = ref(toDateInputValue(today))
const amount = ref(1000)
const fromCurrency = ref('KRW')
const toCurrency = ref('USD')

const rates = ref([])
const previousRateMap = ref({})
const baseDate = ref('')
const loading = ref(false)
const errorMessage = ref('')

const startDate = ref(getDateBefore(7))
const endDate = ref(toDateInputValue(today))
const chartCurrency = ref('USD')
const historyRows = ref([])
const historyLoading = ref(false)
const historyError = ref('')


const isRateDrawerOpen = ref(false)
const drawerKeyword = ref('')
const hoveredExchangePoint = ref(null)

const krwRate = {
  code: 'KRW',
  name: '대한민국 원',
  ratePerUnit: 1,
  displayUnit: '1 KRW',
}

const mainCurrencyOrder = ['USD', 'JPY', 'EUR', 'CNY', 'GBP']

const currencyIconMap = {
  KRW: '🇰🇷',
  USD: '🇺🇸',
  JPY: '🇯🇵',
  EUR: '🇪🇺',
  CNY: '🇨🇳',
  GBP: '🇬🇧',
  CAD: '🇨🇦',
  AUD: '🇦🇺',
  HKD: '🇭🇰',
  SGD: '🇸🇬',
  CHF: '🇨🇭',
}

const currencyOptions = computed(() => {
  return [krwRate, ...rates.value]
})

const chartCurrencyOptions = computed(() => {
  return rates.value
})

const mainCurrencyRates = computed(() => {
  return mainCurrencyOrder
    .map((code) => rates.value.find((rate) => rate.code === code))
    .filter(Boolean)
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
  const numericAmount = Number(amount.value)

  if (!from || !to || Number.isNaN(numericAmount) || numericAmount < 0) {
    return 0
  }

  const amountInKrw = numericAmount * from.ratePerUnit
  return amountInKrw / to.ratePerUnit
})

const formattedResult = computed(() => {
  return formatAmount(convertedAmount.value)
})

const exchangeSummary = computed(() => {
  const values = historyRows.value
    .map((row) => Number(row.rate))
    .filter((value) => !Number.isNaN(value))

  if (values.length === 0) {
    return {
      min: null,
      max: null,
      changeRate: 0,
    }
  }

  const first = values[0]
  const latest = values[values.length - 1]
  const changeRate = first ? ((latest - first) / first) * 100 : 0

  return {
    min: Math.min(...values),
    max: Math.max(...values),
    changeRate,
  }
})


const exchangeChart = computed(() => {
  return buildChartData(
    historyRows.value.map((row) => ({
      date: row.date,
      value: Number(row.rate),
    })),
    formatRate
  )
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

const buildRateMap = (rateItems) => {
  return rateItems.reduce((acc, rate) => {
    acc[rate.code] = rate.ratePerUnit
    return acc
  }, {})
}


const hasValidRates = () => {
  return rates.value.length > 0
}

const resolveDefaultCurrency = () => {
  if (rates.value.some((item) => item.code === 'USD')) {
    return 'USD'
  }

  return rates.value[0]?.code || ''
}

const syncSelectedCurrencies = () => {
  if (!hasValidRates()) {
    chartCurrency.value = ''
    return
  }

  const defaultCurrency = resolveDefaultCurrency()

  if (!rates.value.some((item) => item.code === fromCurrency.value) && fromCurrency.value !== 'KRW') {
    fromCurrency.value = 'KRW'
  }

  if (!rates.value.some((item) => item.code === toCurrency.value) && toCurrency.value !== 'KRW') {
    toCurrency.value = defaultCurrency
  }

  if (fromCurrency.value === toCurrency.value) {
    toCurrency.value = defaultCurrency
  }

  if (!rates.value.some((item) => item.code === chartCurrency.value)) {
    chartCurrency.value = defaultCurrency
  }
}

const fetchPreviousRates = async (dateString) => {
  previousRateMap.value = {}

  try {
    const previousDate = getPreviousDay(dateString)
    const response = await api.get('/exchanges/rates/', {
      params: {
        date: previousDate,
      },
    })

    const normalized = (response.data.rates || [])
      .map(normalizeRate)
      .filter((item) => item.code && item.ratePerUnit > 0)

    previousRateMap.value = buildRateMap(normalized)
  } catch (error) {
    console.error(error)
    previousRateMap.value = {}
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

    const normalizedRates = (response.data.rates || [])
      .map(normalizeRate)
      .filter((item) => item.code && item.ratePerUnit > 0)

    if (normalizedRates.length === 0) {
      rates.value = []
      historyRows.value = []
      errorMessage.value = '환율 데이터가 비어 있습니다.'
      return false
    }

    rates.value = normalizedRates
    syncSelectedCurrencies()

    await fetchPreviousRates(baseDate.value || selectedDate.value)

    return true
  } catch (error) {
    console.error(error)

    rates.value = []
    previousRateMap.value = {}
    historyRows.value = []

    errorMessage.value =
      error.response?.data?.message ||
      '환율 정보를 불러오지 못했습니다. 백엔드 exchanges API를 확인해주세요.'

    return false
  } finally {
    loading.value = false
  }
}

const fetchHistory = async () => {
  historyError.value = ''

  if (!chartCurrency.value) {
    historyRows.value = []
    historyError.value = '통화 목록을 먼저 불러와야 그래프를 조회할 수 있습니다.'
    return false
  }

  if (startDate.value > endDate.value) {
    historyRows.value = []
    historyError.value = '시작일은 종료일보다 늦을 수 없습니다.'
    return false
  }

  historyLoading.value = true

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
      return false
    }

    return true
  } catch (error) {
    console.error(error)
    historyRows.value = []

    historyError.value =
      error.response?.data?.message ||
      '기간별 환율 데이터를 불러오지 못했습니다. 기간은 최대 31일까지만 선택해주세요.'

    return false
  } finally {
    historyLoading.value = false
  }
}

const handleSelectedDateChange = async () => {
  const loaded = await fetchRates()

  if (!loaded) {
    return
  }

  endDate.value = baseDate.value || selectedDate.value
  startDate.value = getDateBefore(7, new Date(endDate.value))

  await fetchHistory()
}

const buildChartData = (items, formatter, reducePoints = false) => {
  const validItems = items
    .filter((item) => item.date && !Number.isNaN(Number(item.value)))
    .map((item) => ({
      date: item.date,
      value: Number(item.value),
    }))

  const width = 1000
  const height = 340
  const left = 64
  const right = 40
  const top = 28
  const bottom = 42
  const chartWidth = width - left - right
  const chartHeight = height - top - bottom

  if (validItems.length === 0) {
    return {
      points: [],
      focusPoints: [],
      polyline: '',
      areaPath: '',
      yTicks: [],
      firstLabel: '',
      lastLabel: '',
    }
  }

  const values = validItems.map((item) => item.value)
  let min = Math.min(...values)
  let max = Math.max(...values)

  if (min === max) {
    min -= 1
    max += 1
  }

  const padding = (max - min) * 0.08
  min -= padding
  max += padding

  const points = validItems.map((item, index) => {
    const x = validItems.length === 1
      ? left + chartWidth / 2
      : left + (chartWidth * index) / (validItems.length - 1)

    const y = top + chartHeight - ((item.value - min) / (max - min)) * chartHeight

    return {
      ...item,
      x: Number(x.toFixed(2)),
      y: Number(y.toFixed(2)),
    }
  })

  const polyline = points.map((point) => `${point.x},${point.y}`).join(' ')
  const areaPath = [
    `M ${points[0].x} ${top + chartHeight}`,
    `L ${polyline.replaceAll(',', ' ')}`,
    `L ${points[points.length - 1].x} ${top + chartHeight}`,
    'Z',
  ].join(' ')

  const tickCount = 5
  const yTicks = Array.from({ length: tickCount }, (_, index) => {
    const ratio = index / (tickCount - 1)
    const value = max - (max - min) * ratio
    const y = top + chartHeight * ratio

    return {
      y: Number(y.toFixed(2)),
      label: formatter(value),
    }
  })

  let focusPoints = points

  if (reducePoints && points.length > 18) {
    const step = Math.ceil(points.length / 14)
    focusPoints = points.filter((_, index) => index % step === 0)
    const last = points[points.length - 1]

    if (!focusPoints.includes(last)) {
      focusPoints.push(last)
    }
  }

  return {
    points,
    focusPoints,
    polyline,
    areaPath,
    yTicks,
    firstLabel: points[0].date,
    lastLabel: points[points.length - 1].date,
  }
}


const getTooltipTransform = (point) => {
  if (!point) {
    return 'translate(0, 0)'
  }

  const tooltipWidth = 210
  const tooltipHeight = 62
  const minX = 68
  const maxX = 960 - tooltipWidth
  const x = Math.min(Math.max(point.x - tooltipWidth / 2, minX), maxX)

  const y = point.y < 100
    ? point.y + 18
    : point.y - tooltipHeight - 18

  return `translate(${x}, ${Math.max(y, 18)})`
}

const swapCurrencies = () => {
  const temp = fromCurrency.value
  fromCurrency.value = toCurrency.value
  toCurrency.value = temp
}

const selectRateFromTable = (rate) => {
  if (!rate?.code) {
    return
  }

  chartCurrency.value = rate.code
  fromCurrency.value = 'KRW'
  toCurrency.value = rate.code
  setExchangePreset(7)
}

const selectRateFromDrawer = (rate) => {
  selectRateFromTable(rate)
  isRateDrawerOpen.value = false
}

const setExchangePreset = async (days) => {
  if (!hasValidRates()) {
    const loaded = await fetchRates()

    if (!loaded) {
      return
    }
  }

  syncSelectedCurrencies()

  endDate.value = baseDate.value || selectedDate.value || toDateInputValue(today)
  startDate.value = getDateBefore(days, new Date(endDate.value))
  await fetchHistory()
}

const getCurrencyIcon = (code) => {
  return currencyIconMap[code] || '💱'
}

const getCurrentRate = (code) => {
  const currency = currencyOptions.value.find((item) => item.code === code)
  return currency?.ratePerUnit ?? null
}

const getRateChange = (code) => {
  const current = getCurrentRate(code)
  const previous = previousRateMap.value[code]

  if (!current || !previous) {
    return null
  }

  return current - previous
}

const getChangeRate = (code) => {
  const change = getRateChange(code)
  const previous = previousRateMap.value[code]

  if (change === null || !previous) {
    return null
  }

  return (change / previous) * 100
}

const getChangeClass = (code) => {
  const change = getRateChange(code)

  if (change === null) {
    return ''
  }

  return change >= 0 ? 'up' : 'down'
}

const formatRateChange = (code) => {
  const change = getRateChange(code)

  if (change === null) {
    return '-'
  }

  return `${change >= 0 ? '▲' : '▼'} ${formatRate(Math.abs(change))}`
}

const formatChangeRate = (code) => {
  const rate = getChangeRate(code)

  if (rate === null) {
    return '-'
  }

  return `${rate >= 0 ? '+' : ''}${formatRate(rate)}%`
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
  if (value === null || value === undefined || value === '') {
    return '-'
  }

  const numberValue = Number(value)

  if (Number.isNaN(numberValue)) {
    return '-'
  }

  return numberValue.toLocaleString(undefined, {
    minimumFractionDigits: 0,
    maximumFractionDigits: 4,
  })
}

const formatAssetPrice = (value) => {
  if (value === null || value === undefined || value === '') {
    return '-'
  }

  const numberValue = Number(value)

  if (Number.isNaN(numberValue)) {
    return '-'
  }

  return numberValue.toLocaleString(undefined, {
    minimumFractionDigits: 0,
    maximumFractionDigits: 3,
  })
}

const formatVolume = (value) => {
  if (value === null || value === undefined || value === '') {
    return '-'
  }

  return Number(value).toLocaleString(undefined, {
    maximumFractionDigits: 3,
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
  const loaded = await fetchRates()

  if (loaded) {
    endDate.value = baseDate.value || selectedDate.value || toDateInputValue(today)
    startDate.value = getDateBefore(7, new Date(endDate.value))
    await fetchHistory()
  }
})

</script>

<style scoped>
.page-title {
  color: #0f172a;
  font-size: 42px;
  font-weight: 900;
  letter-spacing: -0.04em;
  line-height: 1.15;
}

.title-blue {
  color: #2454d6;
}

.exchange-page {
  width: min(var(--container-width), calc(100% - 48px));
  margin: 0 auto;
  padding: 36px 0 64px;
}

.exchange-hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 440px;
  gap: 30px;
  align-items: center;
  min-height: 190px;
  margin-bottom: 24px;
}

.eyebrow {
  margin: 0 0 10px;
  color: var(--color-primary);
  font-size: 12px;
  font-weight: 950;
  letter-spacing: 0.12em;
}

.exchange-hero h1 {
  margin: 0;
  color: var(--color-text);
  font-size: clamp(38px, 5vw, 54px);
  line-height: 1.08;
  font-weight: 950;
  letter-spacing: -0.06em;
}

.exchange-hero p {
  max-width: 620px;
  margin: 16px 0 0;
  color: var(--color-text-muted);
  font-size: 17px;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 22px;
}

.hero-link {
  display: inline-flex;
  align-items: center;
  min-height: 40px;
  padding: 0 15px;
  border: 1px solid var(--color-border-strong);
  border-radius: 999px;
  background: #fff;
  color: var(--color-text);
  font-size: 13px;
  font-weight: 950;
  text-decoration: none;
}

.hero-link.primary {
  border-color: var(--color-primary);
  background: var(--color-primary);
  color: #fff;
}

.hero-link.ghost {
  color: var(--color-primary);
}

.hero-art {
  position: relative;
  height: 150px;
}

.screen-card,
.globe-card,
.coin-card,
.percent-card {
  position: absolute;
  display: grid;
  place-items: center;
  border: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.92);
  box-shadow: var(--shadow-soft);
}

.screen-card {
  left: 20px;
  top: 24px;
  width: 132px;
  height: 92px;
  grid-template-columns: repeat(4, 14px);
  align-items: end;
  justify-content: center;
  gap: 11px;
  padding: 18px;
  border-radius: 28px;
}

.screen-card span {
  display: block;
  width: 14px;
  border-radius: 999px;
  background: linear-gradient(180deg, #6875ff, var(--color-primary));
}

.screen-card span:nth-child(1) { height: 28px; }
.screen-card span:nth-child(2) { height: 54px; }
.screen-card span:nth-child(3) { height: 42px; }
.screen-card span:nth-child(4) { height: 72px; background: linear-gradient(180deg, #3ee5ca, var(--color-accent)); }

.globe-card {
  left: 172px;
  top: 0;
  width: 116px;
  height: 116px;
  border-radius: 42px;
  background: var(--color-accent-soft);
  font-size: 58px;
}

.coin-card {
  right: 44px;
  bottom: 24px;
  width: 76px;
  height: 76px;
  border-radius: 28px;
  background: #fff7e5;
  color: #d97706;
  font-size: 36px;
  font-weight: 950;
}

.percent-card {
  right: 144px;
  top: 22px;
  width: 62px;
  height: 62px;
  border-radius: 22px;
  color: var(--color-primary);
  font-size: 30px;
  font-weight: 950;
}

.card {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: #fff;
  box-shadow: var(--shadow-soft);
}

.exchange-grid {
  display: grid;
  grid-template-columns: minmax(360px, 0.9fr) minmax(0, 1.4fr);
  gap: 18px;
  align-items: stretch;
}

.calculator-card,
.rates-card,
.chart-card,
.summary-card,
.asset-section {
  padding: 22px;
}

.card-title-row,
.asset-header,
.table-title {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: flex-start;
  margin-bottom: 18px;
}

.card-title-row h2,
.asset-header h2,
.table-title h3 {
  margin: 0;
  color: var(--color-text);
  font-size: 22px;
  font-weight: 950;
  letter-spacing: -0.04em;
}

.card-title-row p,
.asset-header p,
.table-title p {
  margin: 6px 0 0;
  color: var(--color-text-muted);
  font-size: 13px;
  line-height: 1.5;
}

.date-box {
  display: grid;
  gap: 8px;
  margin-bottom: 16px;
}

.date-box label,
.asset-filter-row label {
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 900;
}

.date-box input,
.currency-line select,
.currency-line input,
.chart-controls select,
.chart-controls input,
.asset-filter-row input,
.drawer-search {
  min-height: 44px;
  border: 1px solid var(--color-border-strong);
  border-radius: 14px;
  background: #fff;
  color: var(--color-text);
  outline: none;
  font-weight: 800;
}

.date-box input,
.chart-controls select,
.chart-controls input,
.asset-filter-row input,
.drawer-search {
  padding: 0 13px;
}

.date-box p {
  margin: 0;
  color: var(--color-text-light);
  font-size: 12px;
}

.converter-box {
  display: grid;
  gap: 12px;
}

.currency-input-card {
  padding: 15px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface-soft);
}

.currency-input-card label {
  display: block;
  margin-bottom: 8px;
  color: var(--color-text-muted);
  font-size: 12px;
  font-weight: 950;
}

.currency-input-card span {
  display: block;
  margin-top: 8px;
  color: var(--color-text-light);
  font-size: 12px;
  text-align: right;
}

.currency-line {
  display: grid;
  grid-template-columns: 170px minmax(0, 1fr);
  gap: 8px;
}

.currency-line select,
.currency-line input {
  width: 100%;
  box-sizing: border-box;
  padding: 0 12px;
}

.currency-line input {
  color: var(--color-text);
  font-size: 22px;
  font-weight: 950;
  text-align: right;
}

.swap-button {
  justify-self: center;
  width: 42px;
  height: 42px;
  border: 1px solid var(--color-border);
  border-radius: 50%;
  background: #fff;
  color: var(--color-primary);
  font-size: 22px;
  font-weight: 950;
}

.result-strip {
  display: grid;
  gap: 4px;
  margin: 16px 0;
  padding: 14px 16px;
  border-radius: var(--radius-md);
  background: var(--color-primary-soft);
}

.result-strip span {
  color: var(--color-primary);
  font-size: 12px;
  font-weight: 950;
}

.result-strip strong {
  color: var(--color-text);
  font-size: 17px;
}

.primary-button,
.outline-button {
  min-height: 44px;
  border-radius: 14px;
  padding: 0 16px;
  font-weight: 950;
  cursor: pointer;
}

.primary-button {
  border: 0;
  background: var(--color-primary);
  color: #fff;
  box-shadow: 0 14px 24px rgba(17, 22, 184, 0.18);
}

.primary-button.small {
  min-height: 40px;
  white-space: nowrap;
}

.outline-button {
  border: 1px solid var(--color-border-strong);
  background: #fff;
  color: var(--color-primary);
}

.calculator-card > .primary-button {
  width: 100%;
}

.disclaimer {
  margin: 12px 0 0;
  color: var(--color-text-muted);
  font-size: 12px;
  line-height: 1.5;
}

.rate-table {
  display: grid;
}

.rate-table-head,
.rate-row {
  display: grid;
  grid-template-columns: minmax(150px, 1.3fr) 120px 100px 90px;
  gap: 12px;
  align-items: center;
}

.rate-table-head {
  padding: 11px 0;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-muted);
  font-size: 12px;
  font-weight: 950;
}

.rate-row {
  width: 100%;
  min-height: 64px;
  border: 0;
  border-bottom: 1px solid var(--color-border);
  background: transparent;
  color: var(--color-text);
  text-align: left;
  cursor: pointer;
}

.rate-row:hover {
  background: var(--color-surface-soft);
}

.currency-name {
  display: grid;
  gap: 3px;
}

.currency-name strong {
  font-size: 15px;
}

.currency-name span {
  color: var(--color-text-muted);
  font-size: 12px;
  font-weight: 800;
}

.rate-row > strong {
  font-size: 15px;
}

.up {
  color: var(--color-danger);
}

.down {
  color: var(--color-accent);
}

.chart-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 330px;
  gap: 18px;
  margin-top: 18px;
}

.chart-controls,
.asset-filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: flex-end;
  margin-bottom: 16px;
}

.chart-controls select {
  min-width: 190px;
}

.preset-group {
  display: flex;
  gap: 6px;
}

.preset-group button {
  min-height: 36px;
  padding: 0 11px;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  background: #fff;
  color: var(--color-primary);
  font-weight: 950;
  cursor: pointer;
}

.canvas-wrap {
  position: relative;
  height: 330px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: #fff;
  padding: 18px;
}

.canvas-wrap.asset {
  height: 420px;
}

.line-chart {
  width: 100%;
  height: 100%;
  display: block;
}

.chart-grid-line {
  stroke: rgba(148, 163, 184, 0.22);
  stroke-width: 1;
}

.chart-y-label,
.chart-x-label {
  fill: #64748b;
  font-size: 12px;
  font-weight: 800;
}

.chart-line {
  fill: none;
  stroke-width: 4;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.chart-line.exchange {
  stroke: #1116b8;
}

.chart-line.gold {
  stroke: #f59e0b;
}

.chart-line.silver {
  stroke: #64748b;
}

.chart-point {
  stroke: #fff;
  stroke-width: 2;
}

.chart-point.exchange {
  fill: #1116b8;
}

.chart-point.gold {
  fill: #f59e0b;
}

.chart-point.silver {
  fill: #64748b;
}

.chart-hover-target {
  fill: transparent;
  cursor: pointer;
}

.chart-tooltip {
  pointer-events: none;
}

.chart-tooltip rect {
  fill: rgba(15, 27, 61, 0.96);
  stroke: rgba(255, 255, 255, 0.18);
  stroke-width: 1;
  filter: drop-shadow(0 14px 24px rgba(15, 23, 42, 0.24));
}

.chart-tooltip .tooltip-date {
  fill: #cbd5e1;
  font-size: 12px;
  font-weight: 850;
}

.chart-tooltip .tooltip-value {
  fill: #ffffff;
  font-size: 14px;
  font-weight: 950;
}

.chart-caption {
  margin: 10px 0 0;
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 800;
}

.summary-list {
  display: grid;
  gap: 0;
  margin: 0;
}

.summary-list div {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  padding: 13px 0;
  border-bottom: 1px solid var(--color-border);
}

.summary-list dt {
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 900;
}

.summary-list dd {
  margin: 0;
  color: var(--color-text);
  font-size: 14px;
  font-weight: 950;
  text-align: right;
}

.asset-section {
  margin-top: 18px;
}

.asset-buttons {
  display: flex;
  gap: 8px;
}

.asset-buttons button {
  min-height: 42px;
  padding: 0 14px;
  border: 1px solid var(--color-border);
  border-radius: 14px;
  background: #fff;
  color: var(--color-text-muted);
  font-weight: 950;
}

.asset-buttons button.active {
  border-color: var(--color-primary);
  background: var(--color-primary);
  color: #fff;
}

.asset-filter-row label {
  display: grid;
  gap: 6px;
}

.asset-summary-grid {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 12px;
  margin: 18px 0;
}

.asset-summary-grid article {
  padding: 15px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface-soft);
}

.asset-summary-grid span {
  display: block;
  margin-bottom: 8px;
  color: var(--color-text-muted);
  font-size: 12px;
  font-weight: 900;
}

.asset-summary-grid strong {
  color: var(--color-text);
  font-size: 16px;
  font-weight: 950;
}

.asset-content-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 460px;
  gap: 18px;
  align-items: stretch;
}

.asset-chart-panel,
.asset-table-panel {
  min-width: 0;
}

.asset-table-wrap {
  overflow: auto;
  max-height: 420px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.asset-table-wrap table {
  width: 100%;
  min-width: 620px;
  border-collapse: collapse;
}

.asset-table-wrap th,
.asset-table-wrap td {
  padding: 11px 12px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
  font-size: 13px;
  text-align: right;
}

.asset-table-wrap th:first-child,
.asset-table-wrap td:first-child {
  text-align: left;
}

.asset-table-wrap th {
  position: sticky;
  top: 0;
  z-index: 1;
  background: var(--color-surface-soft);
  color: var(--color-text-muted);
  font-weight: 950;
}

.state-message {
  color: var(--color-text-muted);
  font-weight: 800;
}

.state-message.compact {
  margin: 10px 0;
  padding: 13px 14px;
  border: 1px dashed var(--color-border-strong);
  border-radius: var(--radius-md);
  background: var(--color-surface-soft);
  text-align: center;
}

.error-message {
  margin: 10px 0 16px;
  padding: 13px 14px;
  border: 1px solid #fecaca;
  border-radius: var(--radius-md);
  background: #fff5f5;
  color: var(--color-danger);
  font-weight: 900;
}

.drawer-backdrop {
  position: fixed;
  inset: 0;
  z-index: 70;
  background: rgba(15, 23, 42, 0.32);
}

.rate-drawer {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 80;
  display: flex;
  flex-direction: column;
  width: min(420px, 100%);
  height: 100vh;
  padding: 24px;
  border-left: 1px solid var(--color-border);
  background: #fff;
  box-shadow: -24px 0 50px rgba(15, 23, 42, 0.16);
  transform: translateX(100%);
  transition: transform 0.24s ease;
}

.rate-drawer.open {
  transform: translateX(0);
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 16px;
}

.drawer-header h2 {
  margin: 0;
  color: var(--color-text);
  font-size: 24px;
}

.drawer-header span {
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 800;
}

.drawer-header button {
  width: 36px;
  height: 36px;
  border: 0;
  border-radius: 50%;
  background: var(--color-surface-soft);
  color: var(--color-text);
  font-weight: 950;
}

.drawer-search {
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 14px;
}

.drawer-list {
  display: grid;
  gap: 8px;
  overflow-y: auto;
  padding-bottom: 28px;
}

.drawer-rate-item {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  align-items: center;
  padding: 13px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: #fff;
  color: var(--color-text);
  text-align: left;
}

.drawer-rate-item div {
  display: grid;
  gap: 3px;
}

.drawer-rate-item span {
  color: var(--color-text-muted);
  font-size: 12px;
  font-weight: 800;
}

.drawer-rate-item em {
  color: var(--color-primary);
  font-style: normal;
  font-weight: 950;
}

@media (max-width: 1180px) {
  .exchange-hero,
  .exchange-grid,
  .chart-grid,
  .asset-content-grid {
    grid-template-columns: 1fr;
  }

  .hero-art {
    display: none;
  }

  .summary-card {
    order: -1;
  }

  .asset-summary-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .exchange-page {
    width: min(100% - 28px, var(--container-width));
  }

  .rate-table-head {
    display: none;
  }

  .rate-row {
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    padding: 12px 0;
  }

  .currency-line {
    grid-template-columns: 1fr;
  }

  .asset-summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .asset-header,
  .card-title-row {
    flex-direction: column;
  }
}

/* === 주연 공통 톤 보정: 환율 페이지 === */
.exchange-page {
  width: min(var(--container-width, 1360px), calc(100% - 48px));
  padding: 28px 0 72px;
}

.exchange-hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 24px;
  align-items: center;
  margin-bottom: 22px;
}

.hero-copy {
  display: grid;
  gap: 16px;
}

.exchange-hero h1 {
  margin: 0;
  font-size: clamp(36px, 4vw, 48px);
  line-height: 1.08;
  letter-spacing: -0.07em;
}

.hero-actions {
  margin-top: 0;
}

.hero-link {
  min-height: 42px;
  border-radius: 13px;
}

.hero-art {
  display: flex;
  align-items: center;
  gap: 16px;
}

.hero-icon-card {
  display: grid;
  justify-items: center;
  gap: 10px;
  min-width: 122px;
  padding: 18px 18px 16px;
  border: 1px solid var(--color-border);
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.88);
  box-shadow: 0 14px 36px rgba(15, 27, 61, 0.06);
}

.hero-icon-card strong {
  color: var(--color-text);
  font-size: 15px;
  font-weight: 900;
  white-space: nowrap;
}

.hero-graph-icon {
  display: flex;
  align-items: end;
  gap: 8px;
  height: 48px;
}

.hero-graph-icon span {
  display: block;
  width: 10px;
  border-radius: 999px;
  background: linear-gradient(180deg, #5b6cff 0%, #2f46df 100%);
}

.hero-graph-icon span:nth-child(1) { height: 22px; }
.hero-graph-icon span:nth-child(2) { height: 40px; }
.hero-graph-icon span:nth-child(3) { height: 28px; }
.hero-graph-icon span:nth-child(4) { height: 46px; background: linear-gradient(180deg, #4dd4b1 0%, #2bb98f 100%); }

.hero-circle-icon {
  display: grid;
  place-items: center;
  width: 62px;
  height: 62px;
  border-radius: 50%;
  background: linear-gradient(180deg, #eef4ff 0%, #f8fbff 100%);
  color: var(--color-primary);
  font-size: 34px;
  font-weight: 900;
}

.calculator-card,
.rates-card,
.chart-card,
.asset-card,
.asset-section,
.summary-card {
  padding: 24px;
}

.exchange-grid {
  grid-template-columns: 430px minmax(0, 1fr);
  gap: 20px;
  align-items: stretch;
}

.card,
.calculator-card,
.rates-card,
.chart-card,
.asset-card,
.asset-section,
.summary-card {
  border-radius: 22px;
  box-shadow: 0 18px 44px rgba(15, 27, 61, 0.07);
}

.card-title-row {
  align-items: flex-start;
  margin-bottom: 16px;
}

.card-title-row h2,
.asset-header h2 {
  margin: 0;
  font-size: 24px;
  letter-spacing: -0.045em;
}

.card-title-row p,
.asset-header p,
.exchange-hero .eyebrow,
.asset-header .eyebrow {
  display: none;
}

.date-box,
.currency-input-card,
.result-strip {
  border-radius: 16px;
}

.date-box p {
  display: none;
}

.converter-box {
  gap: 14px;
}

.currency-input-card {
  padding: 16px;
  background: var(--color-surface-soft);
  border: 1px solid var(--color-border);
}

.currency-input-card label {
  margin-bottom: 10px;
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 900;
}

.currency-input-card span {
  margin-top: 8px;
  color: var(--color-text-soft);
  font-size: 12px;
}

.currency-line {
  gap: 10px;
}

.currency-line select,
.currency-line input,
.date-box input,
.chart-controls select,
.chart-controls input,
.asset-filter-row input {
  min-height: 45px;
  border-radius: 13px;
}

.swap-button {
  width: 44px;
  height: 44px;
  border-radius: 50%;
}

.primary-button,
.outline-button {
  min-height: 44px;
  border-radius: 13px;
}

.rate-table-head,
.rate-row {
  grid-template-columns: minmax(160px, 1fr) 120px 110px 110px;
  min-height: 64px;
}

.chart-grid,
.asset-grid,
#exchange-chart,
#asset-section {
  margin-top: 20px;
}

.chart-controls,
.asset-controls,
.asset-filter-row {
  gap: 10px;
  padding: 14px;
  border-radius: 18px;
}

.canvas-wrap,
.chart-surface {
  min-height: 360px;
  border-radius: 18px;
}

.asset-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 18px;
}

.asset-buttons button {
  min-height: 44px;
  border-radius: 999px;
}

@media (max-width: 1180px) {
  .exchange-hero,
  .exchange-grid,
  .chart-grid,
  .asset-content-grid {
    grid-template-columns: 1fr;
  }

  .hero-art {
    justify-content: flex-start;
    flex-wrap: wrap;
  }

  .summary-card {
    order: -1;
  }

  .asset-summary-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .exchange-page {
    width: min(100% - 28px, var(--container-width));
  }

  .hero-art {
    display: none;
  }

  .rate-table-head {
    display: none;
  }

  .rate-row {
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    padding: 12px 0;
  }

  .currency-line,
  .chart-controls,
  .asset-filter-row {
    grid-template-columns: 1fr;
  }

  .asset-summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .asset-header,
  .card-title-row {
    flex-direction: column;
  }
}

/* === 주연: 환율 통화 선택 UI 최종 정리 === */
.exchange-hero {
  grid-template-columns: 1fr !important;
}

.hero-art,
.hero-icon-card,
.hero-circle-icon,
.hero-graph-icon {
  display: none !important;
}

.exchange-grid {
  grid-template-columns: 430px minmax(0, 1fr) !important;
}

.converter-box {
  gap: 16px !important;
}

.currency-input-card {
  padding: 18px !important;
  overflow: visible !important;
}

.currency-line {
  display: grid !important;
  grid-template-columns: minmax(0, 1.25fr) minmax(118px, 0.75fr) !important;
  gap: 12px !important;
  align-items: center !important;
}

.currency-line select,
.currency-line input {
  min-width: 0 !important;
  height: 48px !important;
  padding: 0 14px !important;
  font-size: 14px !important;
  line-height: 48px !important;
  white-space: nowrap !important;
}

.currency-line select {
  text-overflow: ellipsis !important;
}

.currency-line input {
  text-align: right !important;
  font-size: 18px !important;
  font-weight: 950 !important;
}

.currency-input-card span {
  display: block !important;
  min-height: 16px !important;
  margin-top: 8px !important;
  text-align: right !important;
}

.rate-row .currency-name strong,
.drawer-rate-item strong {
  letter-spacing: 0 !important;
}

@media (max-width: 1180px) {
  .exchange-grid {
    grid-template-columns: 1fr !important;
  }
}

@media (max-width: 760px) {
  .currency-line {
    grid-template-columns: 1fr !important;
  }
}


/* === 주연: 환율 페이지 상단 버튼 위치/간격 조정 === */
.exchange-hero {
  display: grid !important;
  grid-template-columns: minmax(0, 1fr) auto !important;
  align-items: end !important;
  gap: 24px !important;
  margin-bottom: 30px !important;
  padding-top: 2px !important;
}

.exchange-hero h1 {
  margin: 0 !important;
}

.hero-copy {
  display: contents !important;
}

.hero-actions {
  display: flex !important;
  justify-content: flex-end !important;
  align-items: center !important;
  gap: 10px !important;
  margin-top: 0 !important;
  align-self: end !important;
  transform: translateY(-2px);
}

.hero-link {
  white-space: nowrap !important;
}

.exchange-grid {
  margin-top: 0 !important;
}

@media (max-width: 760px) {
  .exchange-hero {
    grid-template-columns: 1fr !important;
    align-items: start !important;
    margin-bottom: 24px !important;
  }

  .hero-actions {
    justify-content: flex-start !important;
    flex-wrap: wrap !important;
    transform: none;
  }
}


/* === 주연: 환율 페이지 최상단 여백/앵커 이동 위치 보정 === */
.exchange-page {
  padding-top: 10px !important;
}

.exchange-hero {
  min-height: auto !important;
  margin-top: 0 !important;
  margin-bottom: 22px !important;
  padding-top: 0 !important;
  align-items: end !important;
}

.exchange-hero h1 {
  margin: 0 !important;
  line-height: 1.05 !important;
}

.hero-actions {
  transform: translateY(-4px) !important;
}

#exchange-chart,
#asset-section {
  scroll-margin-top: calc(var(--header-height, 64px) + 14px) !important;
}

.chart-grid {
  scroll-margin-top: calc(var(--header-height, 64px) + 14px) !important;
}

@media (max-width: 760px) {
  .exchange-page {
    padding-top: 14px !important;
  }

  .exchange-hero {
    margin-bottom: 20px !important;
  }

  .hero-actions {
    transform: none !important;
  }
}


/* === 주연: 페이지 상단 영역 재조정 - 제목 축소 / 버튼 남색 === */
.page-hero-row {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 20px !important;
  min-height: 0 !important;
  margin: 0 0 24px !important;
  padding-top: 0 !important;
}

.page-hero-row h1 {
  margin: 0 !important;
  color: #07142f !important;
  font-size: clamp(34px, 3.7vw, 48px) !important;
  line-height: 1.08 !important;
  font-weight: 950 !important;
  letter-spacing: -0.072em !important;
}

.page-hero-actions {
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
  flex-shrink: 0 !important;
}

.hero-primary-button,
.hero-outline-button {
  min-height: 42px !important;
  padding: 0 18px !important;
  border-radius: 14px !important;
  font-size: 14px !important;
  font-weight: 950 !important;
  cursor: pointer !important;
  transition:
    border-color 0.18s ease,
    background-color 0.18s ease,
    color 0.18s ease,
    box-shadow 0.18s ease !important;
}

.hero-primary-button {
  border: 1px solid #0b1f4d !important;
  background: #0b1f4d !important;
  color: #fff !important;
  box-shadow: 0 12px 22px rgba(11, 31, 77, 0.18) !important;
}

.hero-outline-button {
  border: 1px solid #c9d3e6 !important;
  background: #fff !important;
  color: #0b1f4d !important;
  box-shadow: 0 10px 18px rgba(15, 27, 61, 0.04) !important;
}

.hero-primary-button:hover {
  background: #071735 !important;
  border-color: #071735 !important;
}

.hero-outline-button:hover {
  border-color: #0b1f4d !important;
  background: #f8fbff !important;
  color: #0b1f4d !important;
}

@media (max-width: 760px) {
  .page-hero-row {
    align-items: flex-start !important;
    flex-direction: column !important;
    margin-bottom: 22px !important;
  }

  .page-hero-row h1 {
    font-size: 34px !important;
  }

  .page-hero-actions {
    width: 100% !important;
  }

  .hero-primary-button,
  .hero-outline-button {
    flex: 1 !important;
  }
}

.exchange-page {
  padding-top: 30px !important;
}

.exchange-page .page-hero-row {
  margin-bottom: 24px !important;
}



/* === 주연: 환율 그래프 조회 필터 정렬 보정 === */
.chart-controls {
  align-items: center !important;
  gap: 10px !important;
}

.chart-controls select,
.chart-controls input {
  height: 40px !important;
  min-height: 40px !important;
  box-sizing: border-box !important;
}

.chart-controls .preset-group {
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  height: 40px !important;
}

.chart-controls .preset-group button {
  height: 40px !important;
  min-height: 40px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 12px !important;
  line-height: 1 !important;
}

.chart-date-action-group {
  display: inline-flex !important;
  align-items: center !important;
  gap: 10px !important;
  flex-wrap: nowrap !important;
}

.chart-date-action-group input {
  width: 132px !important;
}

.chart-date-action-group .primary-button.small {
  height: 40px !important;
  min-height: 40px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 14px !important;
  line-height: 1 !important;
}

@media (max-width: 900px) {
  .chart-date-action-group {
    width: 100% !important;
    flex-wrap: wrap !important;
  }

  .chart-date-action-group input,
  .chart-date-action-group .primary-button.small {
    flex: 1 1 130px !important;
  }
}


/* === 주연: 환율 그래프 필터 한 줄·중앙 정렬 최종 보정 === */
#exchange-chart .chart-card .card-title-row {
  margin-bottom: 22px !important;
}

#exchange-chart .chart-card .chart-controls {
  display: flex !important;
  flex-wrap: nowrap !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
  width: max-content !important;
  max-width: 100% !important;
  margin: 0 auto 24px !important;
  overflow-x: auto !important;
  padding: 0 2px 2px !important;
}

#exchange-chart .chart-card .chart-controls select {
  flex: 0 0 184px !important;
  width: 184px !important;
  min-width: 184px !important;
  height: 40px !important;
}

#exchange-chart .chart-card .preset-group {
  flex: 0 0 auto !important;
  display: inline-flex !important;
  flex-wrap: nowrap !important;
  align-items: center !important;
  gap: 6px !important;
  height: 40px !important;
}

#exchange-chart .chart-card .preset-group button {
  flex: 0 0 38px !important;
  width: 38px !important;
  height: 40px !important;
  min-height: 40px !important;
  padding: 0 !important;
}

#exchange-chart .chart-card .chart-date-action-group {
  flex: 0 0 auto !important;
  width: auto !important;
  display: inline-flex !important;
  flex-wrap: nowrap !important;
  align-items: center !important;
  gap: 8px !important;
}

#exchange-chart .chart-card .chart-date-action-group input {
  flex: 0 0 118px !important;
  width: 118px !important;
  min-width: 118px !important;
  height: 40px !important;
  padding: 0 8px !important;
}

#exchange-chart .chart-card .chart-date-action-group .primary-button.small {
  flex: 0 0 auto !important;
  width: auto !important;
  height: 40px !important;
  min-height: 40px !important;
  padding: 0 14px !important;
  white-space: nowrap !important;
}

#exchange-chart .chart-card .canvas-wrap {
  margin-top: 0 !important;
}


/* === 주연: 환율 그래프 필터 폭 재조정 - 날짜 잘림 방지 === */
#exchange-chart .chart-card .card-title-row {
  margin-bottom: 18px !important;
}

#exchange-chart .chart-card .chart-controls {
  display: grid !important;
  grid-template-columns: minmax(136px, 1fr) 34px 34px 38px minmax(138px, 1fr) minmax(138px, 1fr) 82px !important;
  align-items: center !important;
  column-gap: 5px !important;
  row-gap: 0 !important;
  width: 100% !important;
  max-width: 100% !important;
  margin: 0 0 24px !important;
  padding: 0 !important;
  overflow: visible !important;
}

#exchange-chart .chart-card .chart-controls select,
#exchange-chart .chart-card .chart-controls input,
#exchange-chart .chart-card .chart-controls button {
  box-sizing: border-box !important;
  height: 38px !important;
  min-height: 38px !important;
  border-radius: 12px !important;
  font-size: 12px !important;
  line-height: 1 !important;
}

#exchange-chart .chart-card .chart-controls select {
  grid-column: 1 !important;
  width: 100% !important;
  min-width: 0 !important;
  padding: 0 30px 0 12px !important;
}

#exchange-chart .chart-card .preset-group,
#exchange-chart .chart-card .chart-date-action-group {
  display: contents !important;
}

#exchange-chart .chart-card .preset-group button {
  width: 100% !important;
  min-width: 0 !important;
  padding: 0 !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  white-space: nowrap !important;
}

#exchange-chart .chart-card .chart-date-action-group input {
  width: 100% !important;
  min-width: 0 !important;
  padding: 0 6px !important;
  font-size: 12px !important;
  font-weight: 850 !important;
}

#exchange-chart .chart-card .chart-date-action-group .primary-button.small {
  width: 100% !important;
  min-width: 0 !important;
  padding: 0 8px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  white-space: nowrap !important;
}

#exchange-chart .chart-card .canvas-wrap {
  margin-top: 0 !important;
}

@media (max-width: 760px) {
  #exchange-chart .chart-card .chart-controls {
    grid-template-columns: minmax(130px, 1fr) 34px 34px 38px !important;
    row-gap: 8px !important;
  }

  #exchange-chart .chart-card .chart-date-action-group input:first-of-type {
    grid-column: 1 / 3 !important;
  }

  #exchange-chart .chart-card .chart-date-action-group input:last-of-type {
    grid-column: 3 / 5 !important;
  }

  #exchange-chart .chart-card .chart-date-action-group .primary-button.small {
    grid-column: 1 / 5 !important;
  }
}

</style>
