<template>
  <main class="asset-page">
    <section class="page-hero-row">
      <h1>금·은 시세</h1>
    </section>

    <section class="asset-section card">
      <div class="asset-header">
        <div>
          <h2>금·은 가격 변동 시각화</h2>
          <p>금·은 가격 데이터를 기간별 그래프와 표로 확인합니다.</p>
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
          데이터 조회
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
            <span>기간 변동</span>
            <strong :class="assetSummary.change >= 0 ? 'up' : 'down'">
              {{ assetSummary.change >= 0 ? '+' : '' }}{{ formatAssetPrice(assetSummary.change) }}
            </strong>
          </article>
          <article>
            <span>변동률</span>
            <strong :class="assetSummary.change_rate >= 0 ? 'up' : 'down'">
              {{ assetSummary.change_rate >= 0 ? '+' : '' }}{{ formatAssetPrice(assetSummary.change_rate) }}%
            </strong>
          </article>
          <article>
            <span>기간 최저</span>
            <strong>{{ formatAssetPrice(assetSummary.min_close) }}</strong>
          </article>
          <article>
            <span>기간 최고</span>
            <strong>{{ formatAssetPrice(assetSummary.max_close) }}</strong>
          </article>
        </div>

        <div class="asset-content-grid">
          <section class="asset-chart-panel">
            <div class="canvas-wrap asset">
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
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '@/api/api'

const selectedAsset = ref('gold')
const MIN_ASSET_DATE = '2023-01-01'
const MAX_ASSET_DATE = '2024-12-31'
const assetStartDate = ref('2024-01-01')
const assetEndDate = ref('2024-12-31')
const assetRows = ref([])
const assetSummary = ref(null)
const assetLoading = ref(false)
const assetError = ref('')
const hoveredAssetPoint = ref(null)

const assetLabelMap = {
  gold: '금',
  silver: '은',
}

const toDateInputValue = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const getDateBefore = (days, base) => {
  const date = new Date(base)
  date.setDate(date.getDate() - days)
  return toDateInputValue(date)
}

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

const fetchAssetPrices = async () => {
  assetLoading.value = true
  assetError.value = ''
  hoveredAssetPoint.value = null

  if (assetStartDate.value > assetEndDate.value) {
    assetError.value = '시작일은 종료일보다 늦을 수 없습니다.'
    assetRows.value = []
    assetSummary.value = null
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

onMounted(() => {
  fetchAssetPrices()
})
</script>

<style scoped>
.asset-page {
  width: min(var(--container-width, 1360px), calc(100% - 48px));
  margin: 0 auto;
  padding: 30px 0 72px;
}

.page-hero-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin: 0 0 24px;
}

.page-hero-row h1 {
  margin: 0;
  color: #07142f;
  font-size: clamp(34px, 3.7vw, 48px);
  line-height: 1.08;
  font-weight: 950;
  letter-spacing: -0.072em;
}

.card {
  border: 1px solid var(--color-border);
  border-radius: 22px;
  background: #fff;
  box-shadow: 0 18px 44px rgba(15, 27, 61, 0.07);
}

.asset-section {
  padding: 24px;
}

.asset-header,
.table-title {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: flex-start;
  margin-bottom: 18px;
}

.asset-header h2,
.table-title h3 {
  margin: 0;
  color: var(--color-text);
  font-size: 24px;
  font-weight: 950;
  letter-spacing: -0.045em;
}

.asset-header p,
.table-title p {
  margin: 6px 0 0;
  color: var(--color-text-muted);
  font-size: 13px;
  line-height: 1.5;
}

.asset-buttons {
  display: flex;
  gap: 8px;
}

.asset-buttons button {
  min-height: 44px;
  padding: 0 14px;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  background: #fff;
  color: var(--color-text-muted);
  font-weight: 950;
  cursor: pointer;
}

.asset-buttons button.active {
  border-color: var(--color-primary);
  background: var(--color-primary);
  color: #fff;
}

.asset-filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: flex-end;
  margin-bottom: 16px;
  padding: 14px;
  border-radius: 18px;
  background: var(--color-surface-soft);
}

.asset-filter-row label {
  display: grid;
  gap: 6px;
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 900;
}

.asset-filter-row input {
  min-height: 45px;
  padding: 0 13px;
  border: 1px solid var(--color-border-strong);
  border-radius: 13px;
  background: #fff;
  color: var(--color-text);
  outline: none;
  font-weight: 800;
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

.primary-button {
  min-height: 44px;
  border: 0;
  border-radius: 13px;
  padding: 0 16px;
  background: var(--color-primary);
  color: #fff;
  font-weight: 950;
  cursor: pointer;
  box-shadow: 0 14px 24px rgba(17, 22, 184, 0.18);
}

.primary-button.small {
  min-height: 40px;
  white-space: nowrap;
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

.up {
  color: var(--color-danger) !important;
}

.down {
  color: var(--color-accent) !important;
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

.canvas-wrap {
  position: relative;
  min-height: 420px;
  height: 420px;
  border: 1px solid var(--color-border);
  border-radius: 18px;
  background: #fff;
  padding: 18px;
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

@media (max-width: 1180px) {
  .asset-content-grid {
    grid-template-columns: 1fr;
  }

  .asset-summary-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .asset-page {
    width: min(100% - 28px, var(--container-width));
  }

  .page-hero-row,
  .asset-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .asset-filter-row {
    flex-direction: column;
    align-items: stretch;
  }

  .asset-summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
