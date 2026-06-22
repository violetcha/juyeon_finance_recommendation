<!-- frontend/src/views/MainBankView.vue -->

<template>
  <main class="main-bank-page">
    <section class="page-header">
      <p class="eyebrow">Main Bank Finder</p>
      <h1>내 주변 주거래은행 찾기</h1>
      <p>
        5대 은행의 특징을 비교하고, 원하는 지역과 은행을 선택해 주변 지점을 지도에서 확인할 수 있습니다.
        금융 가이드 영상은 검색 후 마이페이지에 저장할 수 있습니다.
      </p>
    </section>

    <section class="bank-map-section">
      <aside class="bank-list">
        <h2>5대 은행 요약</h2>

        <button
          v-for="bank in summaryBanks"
          :key="bank.name"
          class="bank-card"
          :class="{ active: selectedSummaryBank?.name === bank.name }"
          type="button"
          @click="selectSummaryBank(bank)"
        >
          <div class="bank-card-header">
            <span class="bank-icon">{{ bank.icon }}</span>
            <strong>{{ bank.name }}</strong>
          </div>
          <p>{{ bank.description }}</p>
          <small>{{ bank.keyword }}</small>
        </button>
      </aside>

      <section class="map-area">
        <div class="map-toolbar">
          <div class="search-panel">
            <div class="filter-row">
              <div class="filter-box">
                <label for="sido-filter">광역시/도</label>
                <select id="sido-filter" v-model="selectedSido" @change="handleSidoChange">
                  <option value="">광역시/도 선택</option>
                  <option v-for="sido in sidoOptions" :key="sido" :value="sido">
                    {{ sido }}
                  </option>
                </select>
              </div>

              <div class="filter-box">
                <label for="gugun-filter">시/군/구</label>
                <select id="gugun-filter" v-model="selectedGugun" :disabled="!selectedSido" @change="handleGugunChange">
                  <option value="">시/군/구 선택</option>
                  <option v-for="gugun in gugunOptions" :key="gugun" :value="gugun">
                    {{ gugun }}
                  </option>
                </select>
              </div>

              <div class="filter-box">
                <label for="dong-filter">읍/면/동</label>
                <select id="dong-filter" v-model="selectedDong" :disabled="!selectedGugun">
                  <option value="">동 선택</option>
                  <option v-for="dong in dongOptions" :key="dong" :value="dong">
                    {{ dong }}
                  </option>
                </select>
              </div>

              <div class="filter-box bank-select-box">
                <label for="bank-filter">은행명</label>
                <select id="bank-filter" v-model="selectedBankKeyword" @change="handleBankFilterChange">
                  <option v-for="bankName in bankOptions" :key="bankName" :value="bankName">
                    {{ bankName }}
                  </option>
                </select>
              </div>
            </div>

            <div class="button-row">
              <button type="button" class="search-button" @click="searchBySelectedRegion">
                선택 지역 기준 찾기
              </button>
              <button type="button" class="location-button" @click="moveToUserLocation">
                내 위치 기준 찾기
              </button>
            </div>

            <p class="search-base">
              검색 기준: {{ currentSearchLabel }} / 검색 은행: {{ selectedBankKeyword }}
            </p>
          </div>
        </div>

        <div ref="mapContainer" class="map"></div>

        <div v-if="selectedPlace" class="selected-place">
          <div>
            <p class="selected-label">선택한 지점</p>
            <h3>{{ selectedPlace.place_name || selectedPlace.name }}</h3>
            <p>{{ selectedPlace.road_address_name || selectedPlace.address_name || selectedPlace.address }}</p>
            <p v-if="selectedPlace.distance">
              검색 기준 위치에서 약 {{ Number(selectedPlace.distance).toLocaleString() }}m
            </p>
          </div>

          <button type="button" @click="openKakaoDirection">
            카카오맵 길찾기 열기
          </button>
        </div>
      </section>
    </section>

    <section class="video-section">
      <div class="video-header">
        <div>
          <p class="eyebrow">Financial Guide</p>
          <h2>주거래은행 선택 가이드 영상</h2>
          <p>
            기본 영상 3개를 먼저 보여주고, 검색어를 입력하면 다른 금융 가이드 영상도 확인할 수 있습니다.
          </p>
        </div>
      </div>

      <form class="video-search" @submit.prevent="handleVideoSearch">
        <input
          v-model.trim="videoKeyword"
          type="text"
          placeholder="예: 주거래은행 선택 기준, 사회초년생 적금, 예금 적금 차이"
        />
        <button type="submit">검색</button>
      </form>

      <p v-if="videoLoading" class="message">영상을 불러오는 중입니다...</p>
      <p v-else-if="videoError" class="error">{{ videoError }}</p>

      <div v-else class="video-grid">
        <article v-for="video in videos" :key="video.id" class="video-card">
          <button class="thumbnail-button" type="button" @click="selectVideo(video)">
            <img :src="video.thumbnail" :alt="video.title" />
          </button>

          <div class="video-info">
            <h3>{{ video.title }}</h3>
            <p>{{ video.channelTitle }}</p>

            <div class="video-buttons">
              <button type="button" @click="selectVideo(video)">재생</button>
              <button type="button" class="save-button" @click="handleSaveVideo(video)">
                저장
              </button>
            </div>
          </div>
        </article>
      </div>

      <section v-if="selectedVideo" class="player-section">
        <h3>{{ selectedVideo.title }}</h3>

        <div class="iframe-box">
          <iframe
            :src="`https://www.youtube.com/embed/${selectedVideo.id}`"
            :title="selectedVideo.title"
            allowfullscreen
          ></iframe>
        </div>
      </section>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '@/api/api'
import { searchVideos, saveVideo } from '@/api/videos'

const mapContainer = ref(null)
const map = ref(null)
const markers = ref([])
const routeLine = ref(null)
const currentInfoWindow = ref(null)
const baseMarker = ref(null)

const userLocation = ref({
  lat: 35.190307,
  lng: 126.824798,
})

const selectedPlace = ref(null)

const summaryBanks = [
  {
    name: 'KB국민은행',
    keyword: '국민은행',
    icon: '🟡',
    description:
      '전국 지점망과 생활금융 서비스가 강점인 은행입니다. 급여이체, 카드, 적금 등 기본 금융생활을 시작하기 좋습니다.',
  },
  {
    name: '신한은행',
    keyword: '신한은행',
    icon: '🔵',
    description:
      '모바일 금융과 자산관리 서비스가 강점입니다. 앱 기반 금융생활을 자주 이용하는 사용자에게 적합합니다.',
  },
  {
    name: '하나은행',
    keyword: '하나은행',
    icon: '🟢',
    description:
      '외환, 환전, 글로벌 금융 서비스에 강점이 있습니다. 여행, 유학, 환전 관심이 있는 사용자에게 좋습니다.',
  },
  {
    name: '우리은행',
    keyword: '우리은행',
    icon: '🔷',
    description:
      '급여통장, 생활금융, 공공기관 연계 서비스가 강점입니다. 안정적인 주거래은행 후보로 볼 수 있습니다.',
  },
  {
    name: 'NH농협은행',
    keyword: '농협은행',
    icon: '🌱',
    description:
      '지역 접근성과 생활 밀착 금융이 강점입니다. 지방 거주자나 가까운 지점 접근성을 중시하는 사용자에게 적합합니다.',
  },
]

const selectedSummaryBank = ref(summaryBanks[0])

const bankOptions = [
  '전체 은행',
  '국민은행',
  '신한은행',
  '하나은행',
  '우리은행',
  '농협은행',
  '기업은행',
  'SC제일은행',
  '씨티은행',
  '산업은행',
  '수협은행',
  '광주은행',
  '전북은행',
  '대구은행',
  '부산은행',
  '경남은행',
  '제주은행',
  '새마을금고',
  '신협',
  '우체국',
]

const selectedBankKeyword = ref('국민은행')

const regionData = {
  광주광역시: {
    광산구: ['수완동', '월계동', '첨단동', '신창동', '운남동', '우산동', '하남동', '송정동', '도산동'],
    북구: ['용봉동', '일곡동', '문흥동', '운암동', '두암동', '양산동', '신용동'],
    서구: ['치평동', '상무동', '쌍촌동', '화정동', '농성동', '금호동', '풍암동'],
    동구: ['충장동', '동명동', '계림동', '산수동', '지산동', '학동'],
    남구: ['봉선동', '주월동', '진월동', '효덕동', '백운동', '방림동'],
  },
  서울특별시: {
    강남구: ['역삼동', '삼성동', '대치동', '논현동', '청담동', '압구정동'],
    중구: ['명동', '소공동', '회현동', '필동', '을지로동'],
    종로구: ['종로1가', '종로2가', '사직동', '삼청동', '혜화동'],
    마포구: ['공덕동', '서교동', '합정동', '상암동', '망원동'],
  },
  부산광역시: {
    해운대구: ['우동', '중동', '좌동', '재송동', '반여동'],
    부산진구: ['부전동', '전포동', '가야동', '양정동'],
    동래구: ['온천동', '명륜동', '사직동', '안락동'],
  },
  대구광역시: {
    중구: ['동성로', '삼덕동', '성내동', '대봉동'],
    수성구: ['범어동', '만촌동', '수성동', '황금동'],
  },
  대전광역시: {
    서구: ['둔산동', '월평동', '갈마동', '탄방동'],
    유성구: ['봉명동', '궁동', '전민동', '노은동'],
  },
}

const selectedSido = ref('광주광역시')
const selectedGugun = ref('광산구')
const selectedDong = ref('수완동')
const currentSearchLabel = ref('광주광역시 광산구 수완동')

const sidoOptions = computed(() => Object.keys(regionData))
const gugunOptions = computed(() => {
  if (!selectedSido.value) return []
  return Object.keys(regionData[selectedSido.value] || {})
})
const dongOptions = computed(() => {
  if (!selectedSido.value || !selectedGugun.value) return []
  return regionData[selectedSido.value]?.[selectedGugun.value] || []
})

const videoKeyword = ref('주거래은행 선택 기준')
const videos = ref([])
const selectedVideo = ref(null)
const videoLoading = ref(false)
const videoError = ref('')

const loadKakaoMapScript = () => {
  return new Promise((resolve, reject) => {
    const kakaoKey = import.meta.env.VITE_KAKAO_JS_KEY

    if (!kakaoKey) {
      reject(new Error('frontend/.env에 VITE_KAKAO_JS_KEY가 없습니다.'))
      return
    }

    if (window.kakao && window.kakao.maps) {
      window.kakao.maps.load(resolve)
      return
    }

    const existingScript = document.querySelector('#kakao-map-script')
    if (existingScript) {
      existingScript.addEventListener('load', () => window.kakao.maps.load(resolve))
      return
    }

    const script = document.createElement('script')
    script.id = 'kakao-map-script'
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${kakaoKey}&autoload=false&libraries=services`
    script.async = true
    script.onload = () => window.kakao.maps.load(resolve)
    script.onerror = () => reject(new Error('Kakao Maps SDK 로딩에 실패했습니다.'))
    document.head.appendChild(script)
  })
}

const initMap = async () => {
  try {
    await loadKakaoMapScript()

    const center = new window.kakao.maps.LatLng(userLocation.value.lat, userLocation.value.lng)

    map.value = new window.kakao.maps.Map(mapContainer.value, {
      center,
      level: 5,
    })

    window.kakao.maps.event.addListener(map.value, 'click', closeMapOverlays)
  } catch (error) {
    console.error(error)
    alert(error.message || '카카오 지도를 불러오지 못했습니다.')
  }
}

const handleSidoChange = () => {
  selectedGugun.value = gugunOptions.value[0] || ''
  selectedDong.value = dongOptions.value[0] || ''
}

const handleGugunChange = () => {
  selectedDong.value = dongOptions.value[0] || ''
}

const handleBankFilterChange = async () => {
  selectedSummaryBank.value = summaryBanks.find((bank) => bank.keyword === selectedBankKeyword.value) || null
  await searchNearbyBanks()
}

const buildRegionKeyword = () => {
  return [selectedSido.value, selectedGugun.value, selectedDong.value]
    .filter(Boolean)
    .join(' ')
}

const geocodeRegion = (keyword) => {
  return new Promise((resolve, reject) => {
    const geocoder = new window.kakao.maps.services.Geocoder()

    geocoder.addressSearch(keyword, (result, status) => {
      if (status === window.kakao.maps.services.Status.OK && result.length > 0) {
        resolve({
          lat: Number(result[0].y),
          lng: Number(result[0].x),
        })
        return
      }

      const places = new window.kakao.maps.services.Places()
      places.keywordSearch(keyword, (data, keywordStatus) => {
        if (keywordStatus === window.kakao.maps.services.Status.OK && data.length > 0) {
          resolve({
            lat: Number(data[0].y),
            lng: Number(data[0].x),
          })
          return
        }

        reject(new Error('지역을 찾지 못했습니다. 광역시/도, 시/군/구, 동을 다시 선택해주세요.'))
      })
    })
  })
}

const searchBySelectedRegion = async () => {
  if (!selectedSido.value || !selectedGugun.value || !selectedDong.value) {
    alert('광역시/도, 시/군/구, 동을 모두 선택해주세요.')
    return
  }

  const regionKeyword = buildRegionKeyword()

  try {
    const location = await geocodeRegion(regionKeyword)
    userLocation.value = location
    currentSearchLabel.value = regionKeyword

    const center = new window.kakao.maps.LatLng(location.lat, location.lng)
    map.value.setCenter(center)
    map.value.setLevel(5)
    setBaseMarker(center, regionKeyword)

    await searchNearbyBanks()
  } catch (error) {
    console.error(error)
    alert(error.message || '지역 검색 중 오류가 발생했습니다.')
  }
}

const moveToUserLocation = () => {
  if (!navigator.geolocation) {
    alert('브라우저에서 위치 기능을 지원하지 않습니다.')
    return
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      userLocation.value = {
        lat: position.coords.latitude,
        lng: position.coords.longitude,
      }

      currentSearchLabel.value = '내 현재 위치'

      const center = new window.kakao.maps.LatLng(userLocation.value.lat, userLocation.value.lng)
      map.value.setCenter(center)
      map.value.setLevel(5)
      setBaseMarker(center, '내 현재 위치')

      await searchNearbyBanks()
    },
    () => {
      alert('위치 권한을 허용하지 않아 현재 위치를 사용할 수 없습니다. 지역 선택 검색을 이용해주세요.')
    }
  )
}

const selectSummaryBank = async (bank) => {
  selectedSummaryBank.value = bank
  selectedBankKeyword.value = bank.keyword
  await searchNearbyBanks()
}

const setBaseMarker = (position, label) => {
  if (baseMarker.value) {
    baseMarker.value.setMap(null)
  }

  baseMarker.value = new window.kakao.maps.Marker({
    map: map.value,
    position,
    title: label,
  })
}

const closeMapOverlays = () => {
  if (currentInfoWindow.value) {
    currentInfoWindow.value.close()
    currentInfoWindow.value = null
  }

  selectedPlace.value = null

  if (routeLine.value) {
    routeLine.value.setMap(null)
    routeLine.value = null
  }
}

const clearMarkers = () => {
  markers.value.forEach((marker) => marker.setMap(null))
  markers.value = []
  closeMapOverlays()
}

const normalizeBankResults = (data) => {
  if (Array.isArray(data)) return data
  if (data && Array.isArray(data.branches)) return data.branches
  if (data && Array.isArray(data.banks)) return data.banks
  if (data && Array.isArray(data.documents)) return data.documents
  if (data && Array.isArray(data.results)) return data.results
  return []
}

const getSearchKeyword = () => {
  return selectedBankKeyword.value === '전체 은행' ? '은행' : selectedBankKeyword.value
}

const searchNearbyBanks = async () => {
  if (!map.value) return

  clearMarkers()

  const keyword = getSearchKeyword()

  try {
    const response = await api.get('/maps/banks/', {
      params: {
        bank: keyword,
        lat: userLocation.value.lat,
        lng: userLocation.value.lng,
      },
    })

    const places = normalizeBankResults(response.data)

    if (places.length === 0) {
      alert(`${currentSearchLabel.value} 주변의 ${keyword} 검색 결과가 없습니다.`)
      return
    }

    const bounds = new window.kakao.maps.LatLngBounds()
    const basePosition = new window.kakao.maps.LatLng(userLocation.value.lat, userLocation.value.lng)
    bounds.extend(basePosition)

    places.forEach((place) => {
      const lat = Number(place.y || place.lat || place.latitude)
      const lng = Number(place.x || place.lng || place.longitude)

      if (!lat || !lng || Number.isNaN(lat) || Number.isNaN(lng)) return

      const position = new window.kakao.maps.LatLng(lat, lng)

      const marker = new window.kakao.maps.Marker({
        map: map.value,
        position,
      })

      const infoWindow = new window.kakao.maps.InfoWindow({
        content: `
          <div style="padding:8px 10px;font-size:13px;line-height:1.5;min-width:190px;max-width:260px;">
            <strong>${place.place_name || place.name || keyword}</strong><br />
            ${place.road_address_name || place.address_name || place.address || ''}
          </div>
        `,
      })

      window.kakao.maps.event.addListener(marker, 'click', () => {
        if (currentInfoWindow.value) {
          currentInfoWindow.value.close()
        }

        selectedPlace.value = place
        currentInfoWindow.value = infoWindow
        infoWindow.open(map.value, marker)
        drawSimpleRoute(lat, lng)
      })

      markers.value.push(marker)
      bounds.extend(position)
    })

    if (markers.value.length > 0) {
      map.value.setBounds(bounds)
    } else {
      alert('은행 데이터는 받았지만 좌표가 없어 지도에 표시하지 못했습니다.')
    }
  } catch (error) {
    console.error('은행 검색 실패:', error)
    alert('은행 검색 중 오류가 발생했습니다. 백엔드 maps API를 확인해주세요.')
  }
}

const drawSimpleRoute = (destLat, destLng) => {
  if (routeLine.value) {
    routeLine.value.setMap(null)
  }

  const path = [
    new window.kakao.maps.LatLng(userLocation.value.lat, userLocation.value.lng),
    new window.kakao.maps.LatLng(destLat, destLng),
  ]

  routeLine.value = new window.kakao.maps.Polyline({
    path,
    strokeWeight: 5,
    strokeOpacity: 0.8,
    strokeStyle: 'solid',
  })

  routeLine.value.setMap(map.value)
}

const openKakaoDirection = () => {
  if (!selectedPlace.value) return

  const destName = selectedPlace.value.place_name || selectedPlace.value.name
  const destLat = selectedPlace.value.y || selectedPlace.value.lat
  const destLng = selectedPlace.value.x || selectedPlace.value.lng

  const url = `https://map.kakao.com/link/to/${encodeURIComponent(destName)},${destLat},${destLng}`
  window.open(url, '_blank')
}

const loadVideos = async (keyword, maxResults = 3) => {
  videoLoading.value = true
  videoError.value = ''

  try {
    const response = await searchVideos(keyword, maxResults)
    videos.value = response.data
    selectedVideo.value = response.data[0] || null
  } catch (error) {
    console.error(error)
    videoError.value = '영상을 불러오지 못했습니다. 백엔드 videos API를 확인해주세요.'
  } finally {
    videoLoading.value = false
  }
}

const handleVideoSearch = () => {
  if (!videoKeyword.value) {
    alert('검색어를 입력해주세요.')
    return
  }

  loadVideos(videoKeyword.value, 9)
}

const selectVideo = (video) => {
  selectedVideo.value = video
}

const handleSaveVideo = async (video) => {
  try {
    await saveVideo(video)
    alert('마이페이지에 영상을 저장했습니다.')
  } catch (error) {
    console.error(error)

    if (error.response?.status === 401) {
      alert('로그인 후 저장할 수 있습니다.')
    } else {
      alert('영상 저장 중 오류가 발생했습니다.')
    }
  }
}

onMounted(async () => {
  await initMap()
  await searchBySelectedRegion()
  await loadVideos('주거래은행 선택 기준', 3)
})
</script>

<style scoped>
.main-bank-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px 80px;
}

.page-header {
  margin-bottom: 32px;
}

.eyebrow {
  margin: 0 0 8px;
  color: #2563eb;
  font-weight: 700;
}

.page-header h1 {
  margin: 0 0 12px;
  font-size: 36px;
}

.page-header p,
.video-header p {
  color: #6b7280;
  line-height: 1.6;
}

.bank-map-section {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 24px;
  align-items: stretch;
}

.bank-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.bank-list h2 {
  margin: 0 0 8px;
}

.bank-card {
  text-align: left;
  border: 1px solid #e5e7eb;
  background: white;
  border-radius: 14px;
  padding: 16px;
  cursor: pointer;
}

.bank-card.active {
  border-color: #2563eb;
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.12);
}

.bank-card-header {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 8px;
  font-size: 18px;
}

.bank-icon {
  font-size: 22px;
}

.bank-card p {
  margin: 0 0 10px;
  color: #4b5563;
  line-height: 1.5;
}

.bank-card small {
  color: #2563eb;
  font-weight: 700;
}

.map-area {
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  overflow: hidden;
  background: white;
}

.map-toolbar {
  padding: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.search-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.filter-row {
  display: grid;
  grid-template-columns: repeat(4, minmax(130px, 1fr));
  gap: 10px;
}

.filter-box {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.filter-box label {
  font-size: 13px;
  color: #6b7280;
  font-weight: 700;
}

.filter-box select,
.video-search input {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 10px 12px;
  background: white;
  color: #111827;
}

.bank-select-box select {
  font-weight: 700;
}

.button-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.search-button,
.location-button,
.selected-place button,
.video-search button,
.video-buttons button {
  border: none;
  border-radius: 8px;
  padding: 10px 14px;
  background: #2563eb;
  color: white;
  cursor: pointer;
  white-space: nowrap;
}

.location-button,
.video-buttons .save-button {
  background: #111827;
}

.search-base {
  margin: 0;
  color: #6b7280;
  font-size: 13px;
}

.map {
  width: 100%;
  height: 520px;
}

.selected-place {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  padding: 16px;
  border-top: 1px solid #e5e7eb;
}

.selected-label {
  margin: 0 0 4px;
  color: #2563eb;
  font-size: 13px;
  font-weight: 700;
}

.selected-place h3 {
  margin: 0 0 8px;
}

.selected-place p {
  margin: 4px 0;
  color: #4b5563;
}

.video-section {
  margin-top: 56px;
}

.video-header {
  margin-bottom: 18px;
}

.video-header h2 {
  margin: 0 0 10px;
  font-size: 28px;
}

.video-search {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
}

.video-search input {
  flex: 1;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.video-card {
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  overflow: hidden;
  background: white;
}

.thumbnail-button {
  display: block;
  width: 100%;
  border: none;
  padding: 0;
  background: transparent;
  cursor: pointer;
}

.thumbnail-button img {
  width: 100%;
  height: 170px;
  object-fit: cover;
  display: block;
}

.video-info {
  padding: 14px;
}

.video-info h3 {
  min-height: 44px;
  margin: 0 0 8px;
  font-size: 16px;
  line-height: 1.4;
}

.video-info p {
  margin: 0 0 12px;
  color: #6b7280;
  font-size: 14px;
}

.video-buttons {
  display: flex;
  gap: 8px;
}

.video-buttons button {
  flex: 1;
}

.player-section {
  margin-top: 32px;
}

.player-section h3 {
  margin-bottom: 14px;
}

.iframe-box {
  position: relative;
  width: 100%;
  padding-top: 56.25%;
  border-radius: 16px;
  overflow: hidden;
  background: #111827;
}

.iframe-box iframe {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: 0;
}

.message {
  color: #6b7280;
}

.error {
  color: #dc2626;
}

@media (max-width: 1100px) {
  .filter-row {
    grid-template-columns: repeat(2, minmax(130px, 1fr));
  }
}

@media (max-width: 980px) {
  .bank-map-section {
    grid-template-columns: 1fr;
  }

  .video-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .map {
    height: 420px;
  }
}

@media (max-width: 640px) {
  .filter-row,
  .video-grid {
    grid-template-columns: 1fr;
  }

  .video-search,
  .selected-place {
    flex-direction: column;
    align-items: stretch;
  }

  .video-search button {
    padding: 12px;
  }

  .page-header h1 {
    font-size: 28px;
  }
}
</style>
