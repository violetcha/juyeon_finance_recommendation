<template>
  <main class="exchange-page">
    <section class="exchange-hero">
      <div>
        <p class="eyebrow">EXCHANGE & ASSET DATA</p>
        <h1>환율 계산 · 시세 확인</h1>
        <p>
          한국수출입은행 환율 API와 금·은 엑셀 데이터를 기반으로
          환율 계산, 기간별 그래프, 금·은 가격 변동을 한 화면에서 확인합니다.
        </p>

        <div class="hero-actions">
          <a href="#exchange-chart" class="hero-link primary">환율 그래프 보기</a>
          <a href="#asset-section" class="hero-link">금·은 시세 보기</a>
        </div>
      </div>

      <div class="hero-art" aria-hidden="true">
        <div class="screen-card">
          <span></span>
          <span></span>
          <span></span>
          <span></span>
        </div>
        <div class="globe-card">🌐</div>
        <div class="coin-card">₩</div>
        <div class="percent-card">%</div>
      </div>
    </section>

    <section class="exchange-grid">
      <article class="calculator-card card">
        <div class="card-title-row">
          <div>
            <h2>환율 계산기</h2>
            <p>선택한 기준일의 실제 환율 데이터로 계산합니다.</p>
          </div>
        </div>

        <div class="date-box">
          <label for="selected-date">조회 날짜</label>
          <input
            id="selected-date"
            v-model="selectedDate"
            type="date"
            @change="fetchRates"
          >
          <p>
            API 기준일:
            <strong>{{ baseDate || '조회 전' }}</strong>
            <span v-if="baseDate && selectedDate !== baseDate">
              · 선택일 데이터가 없어 가까운 이전 영업일 기준
            </span>
          </p>
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
                  {{ getCurrencyIcon(currency.code) }} {{ currency.code }} · {{ currency.name }}
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
                  {{ getCurrencyIcon(currency.code) }} {{ currency.code }} · {{ currency.name }}
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
          계산 기준 환율 새로고침
        </button>

        <p class="disclaimer">
          고시환율은 참고용이며, 실제 환전 시 적용 환율은 금융기관별로 다를 수 있습니다.
        </p>
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
              <strong>{{ getCurrencyIcon(rate.code) }} {{ rate.code }}</strong>
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
            <p>최대 31일 범위에서 실제 API 응답 데이터로 그래프를 표시합니다.</p>
          </div>
        </div>

        <div class="chart-controls">
          <select v-model="chartCurrency">
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

          <input v-model="startDate" type="date">
          <input v-model="endDate" type="date">

          <button type="button" class="primary-button small" @click="fetchHistory">
            그래프 조회
          </button>
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

    <section id="asset-section" class="asset-section card">
      <div class="asset-header">
        <div>
          <p class="eyebrow">GOLD & SILVER DATA</p>
          <h2>금·은 가격 변동 시각화</h2>
          <p>
            기존 금·은 페이지의 실제 엑셀 기반 데이터를 환율 페이지 안에서 더 길게 확인합니다.
          </p>
        </div>

        <div class="asset-buttons">
          <button
            type="button"
            :class="{ active: selectedAsset === 'gold' }"
            @click="changeAsset('gold')"
          >
            🟡 금 Gold
          </button>

          <button
            type="button"
            :class="{ active: selectedAsset === 'silver' }"
            @click="changeAsset('silver')"
          >
            ⚪ 은 Silver
          </button>
        </div>
      </div>

      <div class="asset-filter-row">
        <div class="preset-group">
          <button type="button" @click="setAssetPreset(30)">1M</button>
          <button type="button" @click="setAssetPreset(90)">3M</button>
          <button type="button" @click="setAssetPreset(365)">1Y</button>
          <button type="button" @click="setAssetAll">전체</button>
        </div>

        <label>
          시작일
          <input
            v-model="assetStartDate"
            type="date"
            :min="MIN_ASSET_DATE"
            :max="MAX_ASSET_DATE"
          >
        </label>

        <label>
          종료일
          <input
            v-model="assetEndDate"
            type="date"
            :min="MIN_ASSET_DATE"
            :max="MAX_ASSET_DATE"
          >
        </label>

        <button type="button" class="primary-button small" @click="fetchAssetPrices">
          금·은 데이터 조회
        </button>
      </div>

      <p v-if="assetLoading" class="state-message compact">금·은 데이터를 불러오는 중입니다...</p>
      <p v-if="assetError" class="error-message">{{ assetError }}</p>

      <template v-if="assetSummary">
        <div class="asset-summary-grid">
          <article>
            <span>조회 기간</span>
            <strong>{{ assetSummary.first_date }} ~ {{ assetSummary.latest_date }}</strong>
          </article>
          <article>
            <span>최근 종가</span>
            <strong>{{ formatAssetPrice(assetSummary.latest_close) }}</strong>
          </article>
          <article>
            <span>기간 최저</span>
            <strong>{{ formatAssetPrice(assetSummary.min_close) }}</strong>
          </article>
          <article>
            <span>기간 최고</span>
            <strong>{{ formatAssetPrice(assetSummary.max_close) }}</strong>
          </article>
          <article>
            <span>기간 변동</span>
            <strong :class="assetSummary.change >= 0 ? 'up' : 'down'">
              {{ assetSummary.change >= 0 ? '+' : '' }}{{ formatAssetPrice(assetSummary.change) }}
            </strong>
          </article>
          <article>
            <span>변동률</span>
            <strong :class="assetSummary.change_rate >= 0 ? 'up' : 'down'">
              {{ assetSummary.change_rate >= 0 ? '+' : '' }}{{ formatRate(assetSummary.change_rate) }}%
            </strong>
          </article>
        </div>

        <div class="asset-content-grid">
          <section class="asset-chart-panel">
            <div class="canvas-wrap asset chart-surface">
              <svg
                v-if="assetChart.points.length > 0"
                class="line-chart"
                viewBox="0 0 1000 340"
                role="img"
                :aria-label="`${assetLabelMap[selectedAsset]} 가격 추이 그래프`"
                @mouseleave="hoveredAssetPoint = null"
              >
                <defs>
                  <linearGradient id="assetGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop :stop-color="selectedAsset === 'gold' ? '#f59e0b' : '#64748b'" offset="0%" stop-opacity="0.2" />
                    <stop :stop-color="selectedAsset === 'gold' ? '#f59e0b' : '#64748b'" offset="100%" stop-opacity="0.02" />
                  </linearGradient>
                </defs>

                <g>
                  <line
                    v-for="tick in assetChart.yTicks"
                    :key="tick.label"
                    x1="64"
                    x2="960"
                    :y1="tick.y"
                    :y2="tick.y"
                    class="chart-grid-line"
                  />
                  <text
                    v-for="tick in assetChart.yTicks"
                    :key="`${tick.label}-text`"
                    x="50"
                    :y="tick.y + 4"
                    class="chart-y-label"
                    text-anchor="end"
                  >
                    {{ tick.label }}
                  </text>
                </g>

                <path :d="assetChart.areaPath" fill="url(#assetGradient)" />
                <polyline
                  :points="assetChart.polyline"
                  class="chart-line"
                  :class="selectedAsset === 'gold' ? 'gold' : 'silver'"
                />

                <circle
                  v-for="point in assetChart.focusPoints"
                  :key="point.date"
                  :cx="point.x"
                  :cy="point.y"
                  r="4"
                  class="chart-point"
                  :class="selectedAsset === 'gold' ? 'gold' : 'silver'"
                >
                  <title>{{ point.date }} · {{ formatAssetPrice(point.value) }}</title>
                </circle>

                <circle
                  v-for="point in assetChart.points"
                  :key="`${point.date}-asset-hover`"
                  :cx="point.x"
                  :cy="point.y"
                  r="10"
                  class="chart-hover-target"
                  @mouseenter="hoveredAssetPoint = point"
                  @mousemove="hoveredAssetPoint = point"
                />

                <g
                  v-if="hoveredAssetPoint"
                  class="chart-tooltip"
                  :transform="getTooltipTransform(hoveredAssetPoint)"
                >
                  <rect width="210" height="62" rx="14" />
                  <text x="14" y="24" class="tooltip-date">
                    {{ hoveredAssetPoint.date }}
                  </text>
                  <text x="14" y="46" class="tooltip-value">
                    {{ assetLabelMap[selectedAsset] }} {{ formatAssetPrice(hoveredAssetPoint.value) }}
                  </text>
                </g>

                <text x="64" y="326" class="chart-x-label">{{ assetChart.firstLabel }}</text>
                <text x="960" y="326" class="chart-x-label" text-anchor="end">{{ assetChart.lastLabel }}</text>
              </svg>

              <p v-else class="state-message compact">
                그래프를 표시할 금·은 데이터가 없습니다.
              </p>
            </div>
          </section>

          <section class="asset-table-panel">
            <div class="table-title">
              <h3>가격 데이터</h3>
              <p>총 {{ assetRows.length.toLocaleString() }}건</p>
            </div>

            <div class="asset-table-wrap">
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
                  <tr v-for="row in assetRows" :key="row.date">
                    <td>{{ row.date }}</td>
                    <td>{{ formatAssetPrice(row.close) }}</td>
                    <td>{{ formatAssetPrice(row.open) }}</td>
                    <td>{{ formatAssetPrice(row.high) }}</td>
                    <td>{{ formatAssetPrice(row.low) }}</td>
                    <td>{{ formatVolume(row.volume) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>
        </div>
      </template>
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
            <strong>{{ getCurrencyIcon(rate.code) }} {{ rate.code }}</strong>
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
const fromCurrency = ref('USD')
const toCurrency = ref('KRW')

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

const selectedAsset = ref('gold')
const MIN_ASSET_DATE = '2023-01-01'
const MAX_ASSET_DATE = '2024-12-31'
const assetStartDate = ref('2024-01-01')
const assetEndDate = ref('2024-12-31')
const assetRows = ref([])
const assetSummary = ref(null)
const assetLoading = ref(false)
const assetError = ref('')

const isRateDrawerOpen = ref(false)
const drawerKeyword = ref('')
const hoveredExchangePoint = ref(null)
const hoveredAssetPoint = ref(null)

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

const assetLabelMap = {
  gold: '금',
  silver: '은',
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

const assetChart = computed(() => {
  return buildChartData(
    assetRows.value.map((row) => ({
      date: row.date,
      value: Number(row.close),
    })),
    formatAssetPrice,
    true
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

    rates.value = (response.data.rates || [])
      .map(normalizeRate)
      .filter((item) => item.code && item.ratePerUnit > 0)

    if (rates.value.length === 0) {
      errorMessage.value = '환율 데이터가 비어 있습니다.'
      return
    }

    if (!rates.value.some((item) => item.code === fromCurrency.value) && fromCurrency.value !== 'KRW') {
      fromCurrency.value = rates.value.some((item) => item.code === 'USD') ? 'USD' : rates.value[0].code
    }

    if (!rates.value.some((item) => item.code === toCurrency.value) && toCurrency.value !== 'KRW') {
      toCurrency.value = rates.value.some((item) => item.code === 'USD') ? 'USD' : rates.value[0].code
    }

    if (!rates.value.some((item) => item.code === chartCurrency.value)) {
      chartCurrency.value = rates.value.some((item) => item.code === 'USD') ? 'USD' : rates.value[0].code
    }

    await fetchPreviousRates(baseDate.value || selectedDate.value)
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
      return
    }
  } catch (error) {
    console.error(error)
    historyRows.value = []

    historyError.value =
      error.response?.data?.message ||
      '기간별 환율 데이터를 불러오지 못했습니다. 기간은 최대 31일까지만 선택해주세요.'
  } finally {
    historyLoading.value = false
  }
}

const fetchAssetPrices = async () => {
  assetLoading.value = true
  assetError.value = ''

  if (assetStartDate.value > assetEndDate.value) {
    assetError.value = '시작일은 종료일보다 늦을 수 없습니다.'
    assetLoading.value = false
    return
  }

  try {
    const response = await api.get('/assets/prices/', {
      params: {
        asset: selectedAsset.value,
        start_date: assetStartDate.value,
        end_date: assetEndDate.value,
      },
    })

    assetRows.value = response.data.rows || []
    assetSummary.value = response.data.summary || null

    if (assetRows.value.length === 0) {
      assetError.value = response.data.message || '선택한 기간에 해당하는 금·은 데이터가 없습니다.'
      return
    }
  } catch (error) {
    console.error(error)

    assetRows.value = []
    assetSummary.value = null

    assetError.value =
      error.response?.data?.message ||
      '금·은 가격 데이터를 불러오지 못했습니다. assets API와 엑셀 파일을 확인해주세요.'
  } finally {
    assetLoading.value = false
  }
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
  chartCurrency.value = rate.code
  toCurrency.value = rate.code
  setExchangePreset(7)
}

const selectRateFromDrawer = (rate) => {
  selectRateFromTable(rate)
  isRateDrawerOpen.value = false
}

const setExchangePreset = async (days) => {
  endDate.value = baseDate.value || selectedDate.value || toDateInputValue(today)
  startDate.value = getDateBefore(days, new Date(endDate.value))
  await fetchHistory()
}

const setAssetPreset = async (days) => {
  assetEndDate.value = MAX_ASSET_DATE
  assetStartDate.value = getDateBefore(days, new Date(MAX_ASSET_DATE))

  if (assetStartDate.value < MIN_ASSET_DATE) {
    assetStartDate.value = MIN_ASSET_DATE
  }

  await fetchAssetPrices()
}

const setAssetAll = async () => {
  assetStartDate.value = MIN_ASSET_DATE
  assetEndDate.value = MAX_ASSET_DATE
  await fetchAssetPrices()
}

const changeAsset = async (asset) => {
  selectedAsset.value = asset
  await fetchAssetPrices()
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
  await fetchRates()
  await fetchHistory()
  await fetchAssetPrices()
})

</script>

<style scoped>
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
</style>
