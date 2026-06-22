<template>
  <main class="exchange-page">
    <section class="page-header">
      <p class="eyebrow">Exchange Calculator</p>
      <h1>환율 계산기</h1>
      <p>
        한국수출입은행 환율 데이터를 기반으로 원화와 주요 외화를 계산합니다.
      </p>
    </section>

    <section class="exchange-card">
      <div class="top-bar">
        <div>
          <p class="label">환율 기준일</p>
          <strong>{{ baseDate || '조회 전' }}</strong>
        </div>

        <button type="button" class="refresh-button" @click="fetchRates">
          환율 새로고침
        </button>
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

      <section class="table-section">
        <div class="table-header">
          <h2>환율 목록</h2>
          <p>총 {{ rates.length }}개 통화</p>
        </div>

        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>통화 코드</th>
                <th>통화명</th>
                <th>매매기준율</th>
                <th>기준 단위</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="rate in rates" :key="rate.code">
                <td>{{ rate.code }}</td>
                <td>{{ rate.name }}</td>
                <td>{{ formatRate(rate.ratePerUnit) }} KRW</td>
                <td>{{ rate.displayUnit }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '@/api/api'

const amount = ref(1000)
const fromCurrency = ref('KRW')
const toCurrency = ref('USD')

const rates = ref([])
const baseDate = ref('')
const loading = ref(false)
const errorMessage = ref('')

const krwRate = {
  code: 'KRW',
  name: '대한민국 원',
  ratePerUnit: 1,
  displayUnit: '1 KRW',
}

const currencyOptions = computed(() => {
  return [krwRate, ...rates.value]
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
    return {
      code: code.replace('(100)', ''),
      unit: 100,
      displayUnit: `100 ${code.replace('(100)', '')}`,
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
  const rawRate = parseRateNumber(item.rate)

  return {
    code: parsedUnit.code,
    name: item.currency_name || parsedUnit.code,
    rawRate,
    unit: parsedUnit.unit,
    ratePerUnit: rawRate / parsedUnit.unit,
    displayUnit: parsedUnit.displayUnit,
  }
}

const fetchRates = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await api.get('/exchanges/rates/')

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
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error.response?.data?.message ||
      '환율 정보를 불러오지 못했습니다. 백엔드 exchanges API를 확인해주세요.'
  } finally {
    loading.value = false
  }
}

const swapCurrencies = () => {
  const temp = fromCurrency.value
  fromCurrency.value = toCurrency.value
  toCurrency.value = temp
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

onMounted(() => {
  fetchRates()
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
  align-items: center;
  gap: 12px;
  margin-bottom: 22px;
  flex-wrap: wrap;
}

.label {
  margin: 0 0 6px;
  color: #6b7280;
  font-size: 13px;
  font-weight: 800;
}

.refresh-button {
  border: none;
  border-radius: 10px;
  padding: 11px 16px;
  background: #111827;
  color: white;
  font-weight: 800;
  cursor: pointer;
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
.currency-box {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.amount-box label,
.currency-box label {
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

.table-section {
  margin-top: 28px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
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
  min-width: 680px;
}

th,
td {
  padding: 13px 14px;
  border-bottom: 1px solid #e5e7eb;
  text-align: right;
}

th:first-child,
td:first-child,
th:nth-child(2),
td:nth-child(2) {
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

@media (max-width: 760px) {
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