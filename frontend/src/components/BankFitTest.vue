<template>
  <div class="bank-test">
    <div v-if="!result">
      <div class="test-header">
        <p class="label">주거래은행 추천 테스트</p>
        <h2>나에게 맞는 은행은?</h2>
      </div>

      <div class="progress-wrap">
        <div class="progress-text">
          {{ currentIndex + 1 }} / {{ questions.length }}
        </div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
        </div>
      </div>

      <div class="question-card">
        <h3>{{ currentQuestion.title }}</h3>

        <button
          v-for="option in currentQuestion.options"
          :key="option.text"
          class="option-btn"
          :disabled="isLoadingLocation"
          @click="selectOption(option)"
        >
          {{ option.text }}
        </button>

        <p v-if="isLoadingLocation" class="loading-text">
          현재 위치 기준 가까운 은행을 계산하는 중입니다...
        </p>
      </div>
    </div>

    <div v-else class="result-card">
      <p class="label">추천 결과</p>
      <h2>{{ result.name }}</h2>
      <h3>{{ result.typeName }}</h3>
      <p class="summary">{{ result.summary }}</p>

      <div class="reason-box">
        <h4>추천 이유</h4>
        <ul>
          <li v-for="reason in resultReasons" :key="reason">
            {{ reason }}
          </li>
        </ul>
      </div>

      <div v-if="nearestBankInfo[resultCode]" class="near-box">
        <h4>현재 위치 기준 가까운 지점</h4>
        <p>
          {{ nearestBankInfo[resultCode].placeName }}
          · 약 {{ Math.round(nearestBankInfo[resultCode].distance) }}m
        </p>
      </div>

      <div class="score-box">
        <h4>은행별 점수</h4>
        <div v-for="item in sortedScores" :key="item.code" class="score-row">
          <span>{{ item.name }}</span>
          <strong>{{ item.score.toFixed(1) }}점</strong>
        </div>
      </div>

      <button class="main-btn" @click="$emit('recommend', resultCode)">
        추천 은행 지도에서 보기
      </button>

      <button class="sub-btn" @click="resetTest">
        다시 테스트하기
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { BANK_PROFILES, BANK_TEST_QUESTIONS } from '@/data/bankFitTestData'

defineEmits(['recommend'])

const questions = BANK_TEST_QUESTIONS
const currentIndex = ref(0)
const resultCode = ref(null)
const result = ref(null)

const isLoadingLocation = ref(false)
const locationScoreCache = ref(null)
const nearestBankInfo = ref({})

const selectedTagCount = ref({})
const historyStack = ref([])

const scores = ref({
  KB: 0,
  SHINHAN: 0,
  HANA: 0,
  WOORI: 0,
  NH: 0,
})

const currentQuestion = computed(() => questions[currentIndex.value])

const progressPercent = computed(() => {
  return ((currentIndex.value + 1) / questions.length) * 100
})

const sortedScores = computed(() => {
  return Object.entries(scores.value)
    .map(([code, score]) => ({
      code,
      name: BANK_PROFILES[code].name,
      score,
    }))
    .sort((a, b) => b.score - a.score)
})

const resultReasons = computed(() => {
  if (!resultCode.value) return []

  const bankProfile = BANK_PROFILES[resultCode.value]
  const reasons = []

  const matchedTags = Object.keys(selectedTagCount.value)
    .filter((tag) => bankProfile.tagWeights[tag])
    .sort((a, b) => {
      return bankProfile.tagWeights[b] - bankProfile.tagWeights[a]
    })
    .slice(0, 3)

  matchedTags.forEach((tag) => {
    reasons.push(`응답에서 '${tag}' 성향이 높게 반영되었습니다.`)
  })

  if (nearestBankInfo.value[resultCode.value]) {
    const distance = Math.round(nearestBankInfo.value[resultCode.value].distance)
    reasons.push(`현재 위치 기준 가까운 지점이 약 ${distance}m 거리에 있습니다.`)
  }

  if (reasons.length === 0) {
    reasons.push('선택한 응답과 은행의 공식 특징 태그가 가장 많이 일치했습니다.')
  }

  return reasons
})

const createSnapshot = () => ({
  currentIndex: currentIndex.value,
  resultCode: resultCode.value,
  result: result.value,
  selectedTagCount: { ...selectedTagCount.value },
  nearestBankInfo: { ...nearestBankInfo.value },
  scores: { ...scores.value },
})

const restoreSnapshot = (snapshot) => {
  currentIndex.value = snapshot.currentIndex
  resultCode.value = snapshot.resultCode
  result.value = snapshot.result
  selectedTagCount.value = { ...snapshot.selectedTagCount }
  nearestBankInfo.value = { ...snapshot.nearestBankInfo }
  scores.value = { ...snapshot.scores }
}

const selectOption = async (option) => {
  historyStack.value.push(createSnapshot())

  if (option.location) {
    await applyLocationScores()
  }

  if (option.tags) {
    applyTagScores(option.tags)
  }

  goNextOrShowResult()
}

const applyTagScores = (tags) => {
  tags.forEach((tag) => {
    selectedTagCount.value[tag] = (selectedTagCount.value[tag] || 0) + 1
  })

  Object.entries(BANK_PROFILES).forEach(([bankCode, profile]) => {
    tags.forEach((tag) => {
      const weight = profile.tagWeights[tag] || 0
      scores.value[bankCode] += weight
    })
  })
}

const goNextOrShowResult = () => {
  if (currentIndex.value < questions.length - 1) {
    currentIndex.value += 1
  } else {
    showResult()
  }
}

const showResult = () => {
  const [topBankCode] = Object.entries(scores.value).sort((a, b) => b[1] - a[1])[0]

  resultCode.value = topBankCode
  result.value = BANK_PROFILES[topBankCode]
}

const resetTest = () => {
  currentIndex.value = 0
  resultCode.value = null
  result.value = null
  selectedTagCount.value = {}
  nearestBankInfo.value = {}
  locationScoreCache.value = null
  historyStack.value = []

  scores.value = {
    KB: 0,
    SHINHAN: 0,
    HANA: 0,
    WOORI: 0,
    NH: 0,
  }
}

const goPreviousQuestion = () => {
  if (historyStack.value.length === 0) {
    resetTest()
    return
  }

  const snapshot = historyStack.value.pop()
  restoreSnapshot(snapshot)
}

defineExpose({
  resetTest,
  goPreviousQuestion,
})

const applyLocationScores = async () => {
  try {
    isLoadingLocation.value = true

    const { locationScores, nearestInfo } = await getLocationScoresOnce()

    Object.entries(locationScores).forEach(([bankCode, point]) => {
      scores.value[bankCode] += point
    })

    nearestBankInfo.value = nearestInfo
    selectedTagCount.value['위치접근성'] = (selectedTagCount.value['위치접근성'] || 0) + 1
  } catch (error) {
    alert(error.message)

    // 위치 권한 거부 시 완전히 무시하면 테스트가 깨지므로, 위치 점수 없이 진행
  } finally {
    isLoadingLocation.value = false
  }
}

const getLocationScoresOnce = async () => {
  if (locationScoreCache.value) {
    return locationScoreCache.value
  }

  const userPosition = await getCurrentPosition()

  const locationScores = {
    KB: 0,
    SHINHAN: 0,
    HANA: 0,
    WOORI: 0,
    NH: 0,
  }

  const nearestInfo = {}

  for (const [bankCode, profile] of Object.entries(BANK_PROFILES)) {
    const nearest = await searchNearbyBank(profile.searchName, userPosition)

    if (!nearest) continue

    nearestInfo[bankCode] = nearest

    const distance = nearest.distance

    if (distance <= 500) {
      locationScores[bankCode] += 3
    } else if (distance <= 1000) {
      locationScores[bankCode] += 2
    } else if (distance <= 2000) {
      locationScores[bankCode] += 1
    }
  }

  const result = {
    locationScores,
    nearestInfo,
  }

  locationScoreCache.value = result

  return result
}

const getCurrentPosition = () => {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('현재 위치 기능을 지원하지 않는 브라우저입니다.'))
      return
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        resolve({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        })
      },
      () => {
        reject(new Error('현재 위치 권한을 허용해야 위치 기반 점수를 계산할 수 있습니다.'))
      }
    )
  })
}

const searchNearbyBank = (keyword, userPosition) => {
  return new Promise((resolve, reject) => {
    if (!window.kakao || !window.kakao.maps || !window.kakao.maps.services) {
      reject(new Error('카카오맵 services 라이브러리가 로드되지 않았습니다.'))
      return
    }

    const ps = new window.kakao.maps.services.Places()

    ps.keywordSearch(
      keyword,
      (data, status) => {
        if (status !== window.kakao.maps.services.Status.OK || data.length === 0) {
          resolve(null)
          return
        }

        const places = data.map((place) => {
          const placeLat = Number(place.y)
          const placeLng = Number(place.x)

          return {
            placeName: place.place_name,
            address: place.road_address_name || place.address_name,
            lat: placeLat,
            lng: placeLng,
            distance: getDistanceMeter(
              userPosition.lat,
              userPosition.lng,
              placeLat,
              placeLng
            ),
          }
        })

        const nearest = places.sort((a, b) => a.distance - b.distance)[0]

        resolve(nearest)
      },
      {
        location: new window.kakao.maps.LatLng(userPosition.lat, userPosition.lng),
        radius: 3000,
        sort: window.kakao.maps.services.SortBy.DISTANCE,
      }
    )
  })
}

const getDistanceMeter = (lat1, lng1, lat2, lng2) => {
  const R = 6371000
  const toRad = (value) => (value * Math.PI) / 180

  const dLat = toRad(lat2 - lat1)
  const dLng = toRad(lng2 - lng1)

  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) *
      Math.cos(toRad(lat2)) *
      Math.sin(dLng / 2) ** 2

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))

  return R * c
}
</script>

<style scoped>
.bank-test {
  border: 1px solid #dbe4f0;
  border-radius: 22px;
  padding: 22px;
  background: #fff;
  box-shadow: 0 18px 48px rgba(15, 27, 61, 0.06);
}

.label {
  margin: 0 0 8px;
  color: #1116b8;
  font-size: 12px;
  font-weight: 950;
  letter-spacing: 0.08em;
}

.test-header h2,
.result-card h2 {
  margin: 0 0 10px;
  color: #0f1b3d;
  font-size: 24px;
  line-height: 1.22;
  font-weight: 950;
  letter-spacing: -0.05em;
}

.desc,
.summary {
  margin: 0;
  color: #52627a;
  font-size: 14px;
  line-height: 1.65;
}

.progress-wrap {
  margin: 22px 0 20px;
}

.progress-text {
  margin-bottom: 8px;
  color: #0f1b3d;
  font-size: 14px;
  font-weight: 900;
}

.progress-bar {
  width: 100%;
  height: 7px;
  overflow: hidden;
  border-radius: 999px;
  background: #e6edf7;
}

.progress-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #1116b8, #2f7cff, #2dd4bf);
}

.question-card h3 {
  margin: 0 0 14px;
  color: #0f1b3d;
  font-size: 17px;
  line-height: 1.45;
  font-weight: 950;
}

.option-btn {
  display: block;
  width: 100%;
  padding: 14px 15px;
  margin-bottom: 10px;
  border: 1px solid #dbe4f0;
  border-radius: 14px;
  background: #fff;
  color: #0f1b3d;
  text-align: left;
  cursor: pointer;
  font-size: 14px;
  font-weight: 760;
  line-height: 1.45;
}

.option-btn:hover {
  border-color: #1116b8;
  background: #f2f5ff;
  color: #1116b8;
  transform: translateY(-1px);
}

.option-btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.loading-text {
  margin: 12px 0 0;
  color: #1116b8;
  font-size: 14px;
  font-weight: 850;
}

.result-card h3 {
  margin: 0 0 14px;
  color: #52627a;
  font-size: 16px;
}

.reason-box,
.near-box,
.score-box {
  margin-top: 16px;
  padding: 15px;
  border: 1px solid #edf2f7;
  border-radius: 16px;
  background: #f8fbff;
}

.reason-box h4,
.near-box h4,
.score-box h4 {
  margin: 0 0 10px;
  color: #0f1b3d;
  font-size: 14px;
  font-weight: 950;
}

.reason-box ul {
  padding-left: 18px;
  margin: 0;
  color: #52627a;
}

.reason-box li {
  margin-bottom: 7px;
  line-height: 1.5;
}

.near-box p {
  margin: 0;
  color: #52627a;
  line-height: 1.55;
}

.score-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 9px 0;
  border-bottom: 1px solid #e6edf7;
  color: #52627a;
  font-size: 14px;
}

.score-row:last-child {
  border-bottom: none;
}

.score-row strong {
  color: #1116b8;
}

.main-btn,
.sub-btn {
  width: 100%;
  min-height: 44px;
  padding: 0 14px;
  border-radius: 13px;
  margin-top: 12px;
  cursor: pointer;
  font-weight: 900;
}

.main-btn {
  border: none;
  background: #1116b8;
  color: white;
  box-shadow: 0 14px 26px rgba(17, 22, 184, 0.18);
}

.sub-btn {
  border: 1px solid #dbe4f0;
  background: white;
  color: #0f1b3d;
}

.main-btn:hover,
.sub-btn:hover {
  transform: translateY(-1px);
}
</style>
