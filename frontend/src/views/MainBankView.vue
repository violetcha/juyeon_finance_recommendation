<!-- frontend/src/views/MainBankView.vue -->

<template>
  <main class="main-bank-page">
    <section class="page-hero-row">
      <h1 class="page-title">
        <span class="title-blue">내주변</span>
        <span>  주거래은행</span>
      </h1>

      <div class="page-hero-actions">
        <button type="button" class="hero-outline-button" @click="scrollToVideoSection">
          ▶ 영상 보기
        </button>
      </div>
    </section>

<section class="bank-map-section">
      <aside class="bank-list">
        <BankFitTest
          ref="bankFitTestRef"
          :key="bankFitTestKey"
          class="bank-fit-test-panel"
          @recommend="handleRecommendBank"
        />

        <section class="test-control-panel">
          <div class="control-icon">↺</div>
          <div>
            <h3>이전 질문 다시 선택</h3>
            <p>선택을 바꾸고 싶다면 이전 질문으로 돌아가거나 처음부터 다시 시작할 수 있습니다.</p>
          </div>

          <div class="control-buttons">
            <button type="button" class="control-button outline" @click="handlePreviousQuestion">
              ← 이전 질문
            </button>
            <button type="button" class="control-button primary" @click="handleRestartTest">
              ↻ 처음부터 다시
            </button>
          </div>
        </section>
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
                <select
                  id="gugun-filter"
                  v-model="selectedGugun"
                  :disabled="!selectedSido"
                  @change="handleGugunChange"
                >
                  <option value="">시/군/구 선택</option>
                  <option v-for="gugun in gugunOptions" :key="gugun" :value="gugun">
                    {{ gugun }}
                  </option>
                </select>
              </div>

              <div class="filter-box">
                <label for="dong-filter">읍/면/동</label>
                <select id="dong-filter" v-model="selectedDong" :disabled="!selectedGugun">
                  <option value="">읍/면/동 선택</option>
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

            <p v-if="mapError" class="map-error">
              {{ mapError }}
            </p>

            <p v-if="mapMessage" class="map-message">
              {{ mapMessage }}
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

            <p v-if="routeLoading">경로를 불러오는 중입니다...</p>

            <p v-else-if="routeError" class="route-error">
              {{ routeError }}
            </p>

            <p v-else-if="routeSummary" class="route-summary">
              자동차 기준 약 {{ routeSummary.distanceText }} · {{ routeSummary.durationText }}
              <span v-if="routeSummary.taxiText">
                · 예상 택시비 {{ routeSummary.taxiText }}
              </span>
            </p>
          </div>

          <button type="button" @click="openKakaoDirection">
            카카오맵 길찾기 열기
          </button>
        </div>
      </section>
    </section>

    <section ref="videoSection" id="bank-guide-videos" class="video-section">
      <div class="video-header">
        <div>
          <h2>주거래은행 선택 가이드 영상</h2>
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
        <article v-for="video in videos" :key="getVideoId(video)" class="video-card">
          <button class="thumbnail-button" type="button" @click="selectVideo(video)">
            <img :src="video.thumbnail_url" :alt="video.title" />
          </button>

          <div class="video-info">
            <h3>{{ video.title }}</h3>
            <p>{{ video.channel_title }}</p>

            <div class="video-buttons">
              <button type="button" @click="selectVideo(video)">재생</button>

              <button
                type="button"
                class="save-button"
                :class="{ saved: isSavedVideo(video) }"
                :disabled="savingVideoId === getVideoId(video)"
                @click="handleToggleSaveVideo(video)"
              >
                <span v-if="savingVideoId === getVideoId(video)">처리 중...</span>
                <span v-else-if="isSavedVideo(video)">저장됨</span>
                <span v-else>저장</span>
              </button>
            </div>
          </div>
        </article>
      </div>

      <section v-if="selectedVideo && selectedVideoEmbedUrl" class="player-section">
        <h3>{{ selectedVideo.title }}</h3>

        <div class="iframe-box">
          <iframe
            v-if="selectedVideo?.video_id"
            :key="selectedVideo.video_id"
            :src="`https://www.youtube.com/embed/${selectedVideo.video_id}`"
            :title="selectedVideo.title"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          ></iframe>
        </div>
      </section>

      <p v-else-if="selectedVideo && !selectedVideo.video_id" class="error">
        영상 ID가 없어 재생할 수 없습니다. 다시 검색해주세요.
      </p>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '@/api/api'
import { searchVideos, saveVideo, getSavedVideos, deleteSavedVideo } from '@/api/videos'
import BankFitTest from '@/components/BankFitTest.vue'

const mapContainer = ref(null)
const map = ref(null)
const markers = ref([])
const routeLine = ref(null)
const currentInfoWindow = ref(null)
const baseMarker = ref(null)
const routeSummary = ref(null)
const routeLoading = ref(false)
const routeError = ref('')
const routeBorderLine = ref(null)
const startRouteMarker = ref(null)
const endRouteMarker = ref(null)
const mapError = ref('')
const mapMessage = ref('')
const videoSection = ref(null)
const bankFitTestRef = ref(null)
const bankFitTestKey = ref(0)

const BANK_SEARCH_RADIUS = 1500
const MAX_BANK_RESULTS = 15

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

const bankCodeToKeywordMap = {
  KB: '국민은행',
  SHINHAN: '신한은행',
  HANA: '하나은행',
  WOORI: '우리은행',
  NH: '농협은행',
}

const regionData = {
  서울특별시: {
    강남구: ['역삼동', '삼성동', '대치동', '논현동', '청담동', '압구정동', '신사동'],
    강동구: ['천호동', '성내동', '길동', '명일동', '고덕동'],
    강북구: ['수유동', '미아동', '번동'],
    강서구: ['화곡동', '등촌동', '가양동', '마곡동'],
    관악구: ['봉천동', '신림동', '남현동'],
    광진구: ['구의동', '자양동', '화양동', '군자동'],
    구로구: ['구로동', '신도림동', '개봉동', '고척동'],
    금천구: ['가산동', '독산동', '시흥동'],
    노원구: ['상계동', '중계동', '하계동', '월계동'],
    도봉구: ['창동', '방학동', '쌍문동'],
    동대문구: ['청량리동', '회기동', '장안동', '답십리동'],
    동작구: ['상도동', '사당동', '노량진동', '흑석동'],
    마포구: ['공덕동', '서교동', '합정동', '상암동', '망원동'],
    서대문구: ['신촌동', '홍제동', '연희동', '북가좌동'],
    서초구: ['서초동', '반포동', '양재동', '방배동'],
    성동구: ['성수동', '왕십리동', '행당동', '금호동'],
    성북구: ['성북동', '안암동', '정릉동', '길음동'],
    송파구: ['잠실동', '문정동', '가락동', '방이동'],
    양천구: ['목동', '신정동', '신월동'],
    영등포구: ['여의도동', '영등포동', '당산동', '문래동'],
    용산구: ['이태원동', '한남동', '용산동', '청파동'],
    은평구: ['불광동', '응암동', '진관동', '갈현동'],
    종로구: ['종로1가', '종로2가', '사직동', '삼청동', '혜화동'],
    중구: ['명동', '소공동', '회현동', '필동', '을지로동'],
    중랑구: ['면목동', '상봉동', '중화동', '묵동'],
  },
  부산광역시: {
    중구: ['중앙동', '남포동', '부평동'],
    서구: ['충무동', '동대신동', '서대신동'],
    동구: ['초량동', '범일동', '수정동'],
    영도구: ['동삼동', '영선동', '봉래동'],
    부산진구: ['부전동', '전포동', '가야동', '양정동'],
    동래구: ['온천동', '명륜동', '사직동', '안락동'],
    남구: ['대연동', '문현동', '용호동'],
    북구: ['화명동', '덕천동', '구포동'],
    해운대구: ['우동', '중동', '좌동', '재송동', '반여동'],
    사하구: ['하단동', '당리동', '괴정동'],
    금정구: ['장전동', '구서동', '부곡동'],
    강서구: ['명지동', '대저동', '녹산동'],
    연제구: ['연산동', '거제동'],
    수영구: ['광안동', '남천동', '민락동'],
    사상구: ['괘법동', '감전동', '주례동'],
    기장군: ['기장읍', '정관읍', '일광읍'],
  },
  대구광역시: {
    중구: ['동성로', '삼덕동', '성내동', '대봉동'],
    동구: ['신천동', '효목동', '방촌동', '동호동'],
    서구: ['평리동', '내당동', '비산동'],
    남구: ['대명동', '봉덕동', '이천동'],
    북구: ['산격동', '칠성동', '태전동', '복현동'],
    수성구: ['범어동', '만촌동', '수성동', '황금동'],
    달서구: ['상인동', '월성동', '이곡동', '두류동'],
    달성군: ['화원읍', '논공읍', '다사읍', '유가읍'],
    군위군: ['군위읍', '소보면', '효령면'],
  },
  인천광역시: {
    중구: ['운서동', '영종동', '신포동'],
    동구: ['송림동', '화수동'],
    미추홀구: ['주안동', '용현동', '학익동'],
    연수구: ['송도동', '연수동', '동춘동'],
    남동구: ['구월동', '논현동', '만수동'],
    부평구: ['부평동', '삼산동', '청천동'],
    계양구: ['계산동', '작전동', '효성동'],
    서구: ['청라동', '검단동', '가정동'],
    강화군: ['강화읍', '선원면', '길상면'],
    옹진군: ['영흥면', '백령면', '대청면'],
  },
  광주광역시: {
    광산구: ['수완동', '월계동', '첨단동', '신창동', '운남동', '우산동', '하남동', '송정동', '도산동'],
    북구: ['용봉동', '일곡동', '문흥동', '운암동', '두암동', '양산동', '신용동'],
    서구: ['치평동', '상무동', '쌍촌동', '화정동', '농성동', '금호동', '풍암동'],
    동구: ['충장동', '동명동', '계림동', '산수동', '지산동', '학동'],
    남구: ['봉선동', '주월동', '진월동', '효덕동', '백운동', '방림동'],
  },
  대전광역시: {
    동구: ['중앙동', '가양동', '용전동'],
    중구: ['은행동', '대흥동', '태평동'],
    서구: ['둔산동', '월평동', '갈마동', '탄방동'],
    유성구: ['봉명동', '궁동', '전민동', '노은동'],
    대덕구: ['송촌동', '법동', '중리동'],
  },
  울산광역시: {
    중구: ['성남동', '태화동', '우정동'],
    남구: ['삼산동', '달동', '신정동', '무거동'],
    동구: ['방어동', '전하동', '일산동'],
    북구: ['연암동', '화봉동', '호계동'],
    울주군: ['범서읍', '언양읍', '온산읍'],
  },
  세종특별자치시: {
    세종특별자치시: ['조치원읍', '한솔동', '새롬동', '도담동', '아름동', '종촌동', '고운동', '보람동', '소담동', '나성동'],
  },
  경기도: {
    수원시: ['인계동', '영통동', '광교동', '정자동'],
    성남시: ['분당동', '서현동', '정자동', '판교동'],
    의정부시: ['의정부동', '호원동', '민락동'],
    안양시: ['평촌동', '범계동', '안양동'],
    부천시: ['중동', '상동', '심곡동'],
    광명시: ['철산동', '하안동', '소하동'],
    평택시: ['평택동', '비전동', '송탄동'],
    안산시: ['고잔동', '중앙동', '선부동'],
    고양시: ['일산동', '마두동', '화정동'],
    과천시: ['중앙동', '별양동'],
    구리시: ['인창동', '수택동'],
    남양주시: ['다산동', '별내동', '화도읍'],
    오산시: ['오산동', '원동'],
    시흥시: ['정왕동', '배곧동', '은행동'],
    군포시: ['산본동', '금정동'],
    의왕시: ['내손동', '고천동'],
    하남시: ['신장동', '미사동'],
    용인시: ['수지구', '기흥구', '처인구'],
    파주시: ['금촌동', '운정동', '문산읍'],
    이천시: ['창전동', '중리동'],
    안성시: ['공도읍', '안성동'],
    김포시: ['장기동', '구래동', '사우동'],
    화성시: ['동탄동', '봉담읍', '향남읍'],
    광주시: ['경안동', '오포읍', '초월읍'],
    양주시: ['옥정동', '덕정동'],
    포천시: ['소흘읍', '신읍동'],
    여주시: ['홍문동', '가남읍'],
    연천군: ['연천읍', '전곡읍'],
    가평군: ['가평읍', '청평면'],
    양평군: ['양평읍', '용문면'],
  },
  강원특별자치도: {
    춘천시: ['퇴계동', '석사동', '후평동'],
    원주시: ['무실동', '단계동', '중앙동'],
    강릉시: ['교동', '포남동', '옥천동'],
    동해시: ['천곡동', '북삼동'],
    태백시: ['황지동', '장성동'],
    속초시: ['교동', '조양동'],
    삼척시: ['남양동', '교동'],
    홍천군: ['홍천읍'],
    횡성군: ['횡성읍'],
    영월군: ['영월읍'],
    평창군: ['평창읍', '진부면'],
    정선군: ['정선읍', '고한읍'],
    철원군: ['갈말읍', '동송읍'],
    화천군: ['화천읍'],
    양구군: ['양구읍'],
    인제군: ['인제읍'],
    고성군: ['간성읍'],
    양양군: ['양양읍'],
  },
  충청북도: {
    청주시: ['성안동', '가경동', '오창읍'],
    충주시: ['성내동', '연수동'],
    제천시: ['중앙동', '청전동'],
    보은군: ['보은읍'],
    옥천군: ['옥천읍'],
    영동군: ['영동읍'],
    증평군: ['증평읍'],
    진천군: ['진천읍', '덕산읍'],
    괴산군: ['괴산읍'],
    음성군: ['음성읍', '금왕읍'],
    단양군: ['단양읍'],
  },
  충청남도: {
    천안시: ['불당동', '두정동', '신부동'],
    공주시: ['신관동', '웅진동'],
    보령시: ['대천동'],
    아산시: ['온양동', '배방읍'],
    서산시: ['동문동', '예천동'],
    논산시: ['취암동', '강경읍'],
    계룡시: ['금암동'],
    당진시: ['당진동', '송악읍'],
    금산군: ['금산읍'],
    부여군: ['부여읍'],
    서천군: ['서천읍'],
    청양군: ['청양읍'],
    홍성군: ['홍성읍', '홍북읍'],
    예산군: ['예산읍'],
    태안군: ['태안읍'],
  },
  전북특별자치도: {
    전주시: ['효자동', '서신동', '중앙동'],
    군산시: ['수송동', '나운동'],
    익산시: ['영등동', '모현동'],
    정읍시: ['수성동'],
    남원시: ['도통동'],
    김제시: ['요촌동'],
    완주군: ['봉동읍', '삼례읍'],
    진안군: ['진안읍'],
    무주군: ['무주읍'],
    장수군: ['장수읍'],
    임실군: ['임실읍'],
    순창군: ['순창읍'],
    고창군: ['고창읍'],
    부안군: ['부안읍'],
  },
  전라남도: {
    목포시: ['상동', '하당동', '용당동'],
    여수시: ['학동', '여서동', '문수동'],
    순천시: ['연향동', '조례동', '중앙동'],
    나주시: ['빛가람동', '성북동'],
    광양시: ['중마동', '광양읍'],
    담양군: ['담양읍'],
    곡성군: ['곡성읍'],
    구례군: ['구례읍'],
    고흥군: ['고흥읍'],
    보성군: ['보성읍'],
    화순군: ['화순읍'],
    장흥군: ['장흥읍'],
    강진군: ['강진읍'],
    해남군: ['해남읍'],
    영암군: ['영암읍', '삼호읍'],
    무안군: ['무안읍', '삼향읍'],
    함평군: ['함평읍'],
    영광군: ['영광읍'],
    장성군: ['장성읍'],
    완도군: ['완도읍'],
    진도군: ['진도읍'],
    신안군: ['압해읍'],
  },
  경상북도: {
    포항시: ['죽도동', '대이동', '양덕동'],
    경주시: ['성건동', '황성동'],
    김천시: ['평화동', '신음동'],
    안동시: ['옥동', '송현동'],
    구미시: ['인동동', '송정동'],
    영주시: ['휴천동', '가흥동'],
    영천시: ['완산동'],
    상주시: ['남성동'],
    문경시: ['점촌동'],
    경산시: ['중방동', '하양읍'],
    의성군: ['의성읍'],
    청송군: ['청송읍'],
    영양군: ['영양읍'],
    영덕군: ['영덕읍'],
    청도군: ['청도읍'],
    고령군: ['대가야읍'],
    성주군: ['성주읍'],
    칠곡군: ['왜관읍', '석적읍'],
    예천군: ['예천읍', '호명면'],
    봉화군: ['봉화읍'],
    울진군: ['울진읍'],
    울릉군: ['울릉읍'],
  },
  경상남도: {
    창원시: ['중앙동', '상남동', '합성동'],
    진주시: ['평거동', '가좌동', '중앙동'],
    통영시: ['무전동', '북신동'],
    사천시: ['사천읍', '벌리동'],
    김해시: ['내외동', '장유동', '삼계동'],
    밀양시: ['내이동'],
    거제시: ['고현동', '옥포동'],
    양산시: ['물금읍', '중앙동'],
    의령군: ['의령읍'],
    함안군: ['가야읍'],
    창녕군: ['창녕읍'],
    고성군: ['고성읍'],
    남해군: ['남해읍'],
    하동군: ['하동읍'],
    산청군: ['산청읍'],
    함양군: ['함양읍'],
    거창군: ['거창읍'],
    합천군: ['합천읍'],
  },
  제주특별자치도: {
    제주시: ['이도동', '노형동', '연동', '아라동'],
    서귀포시: ['서귀동', '중문동', '대정읍'],
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
  const dongs = regionData[selectedSido.value]?.[selectedGugun.value] || []
  return ['전체', ...dongs]
})


const selectedVideoEmbedUrl = computed(() => {
  const videoId = selectedVideo.value?.video_id

  if (!videoId) {
    return ''
  }

  return `https://www.youtube.com/embed/${videoId}?rel=0&modestbranding=1&playsinline=1&origin=${window.location.origin}`
})

const videoKeyword = ref('주거래은행 선택 기준')
const videos = ref([])
const selectedVideo = ref(null)
const videoLoading = ref(false)
const videoError = ref('')
const savedVideoIds = ref(new Set())
const savingVideoId = ref(null)

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
  mapError.value = ''
  mapMessage.value = ''

  try {
    await loadKakaoMapScript()

    const center = new window.kakao.maps.LatLng(userLocation.value.lat, userLocation.value.lng)

    map.value = new window.kakao.maps.Map(mapContainer.value, {
      center,
      level: 4,
    })

    window.kakao.maps.event.addListener(map.value, 'click', closeMapOverlays)
  } catch (error) {
    console.error(error)
    mapError.value = error.message || '카카오 지도를 불러오지 못했습니다.'
  }
}

const handleSidoChange = () => {
  selectedGugun.value = gugunOptions.value[0] || ''
  selectedDong.value = '전체'
}

const handleGugunChange = () => {
  selectedDong.value = '전체'
}

const handleBankFilterChange = async () => {
  selectedSummaryBank.value = summaryBanks.find((bank) => bank.keyword === selectedBankKeyword.value) || null
  await searchNearbyBanks()
}

const buildRegionKeyword = () => {
  return [selectedSido.value, selectedGugun.value, selectedDong.value]
    .filter((part) => part && part !== '전체')
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
  mapError.value = ''
  mapMessage.value = ''

  if (!selectedSido.value || !selectedGugun.value) {
    mapError.value = '광역시/도와 시/군/구를 선택해주세요. 동은 전체로 두어도 됩니다.'
    return
  }

  if (!map.value || !window.kakao?.maps) {
    mapError.value = '지도가 아직 준비되지 않았습니다.'
    return
  }

  const regionKeyword = buildRegionKeyword()

  try {
    const location = await geocodeRegion(regionKeyword)

    userLocation.value = location
    currentSearchLabel.value = regionKeyword

    const center = new window.kakao.maps.LatLng(location.lat, location.lng)

    map.value.setCenter(center)
    map.value.setLevel(4)

    setBaseMarker(center, regionKeyword, 'green')

    await searchNearbyBanks()
  } catch (error) {
    console.error(error)
    mapError.value = error.message || '지역 검색 중 오류가 발생했습니다.'
  }
}

const moveToUserLocation = () => {
  mapError.value = ''
  mapMessage.value = ''

  if (!navigator.geolocation) {
    mapError.value = '브라우저에서 위치 기능을 지원하지 않습니다.'
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
      map.value.setLevel(4)

      setBaseMarker(center, '내 현재 위치', 'red')

      await searchNearbyBanks()
    },
    () => {
      mapError.value = '위치 권한을 허용하지 않아 현재 위치를 사용할 수 없습니다. 지역 선택 검색을 이용해주세요.'
    }
  )
}

const selectSummaryBank = async (bank) => {
  selectedSummaryBank.value = bank
  selectedBankKeyword.value = bank.keyword
  await searchNearbyBanks()
}

const handleRecommendBank = async (payload) => {
  const bankCode = typeof payload === 'string' ? payload : payload?.bankCode
  const recommendLocation = typeof payload === 'object' ? payload?.userPosition : null
  const keyword = bankCodeToKeywordMap[bankCode]

  if (!keyword) {
    mapError.value = '추천 은행 정보를 확인할 수 없습니다.'
    return
  }

  selectedBankKeyword.value = keyword
  selectedSummaryBank.value = summaryBanks.find((bank) => bank.keyword === keyword) || null

  mapError.value = ''
  mapMessage.value = `${keyword} 추천 결과를 지도에 반영했습니다.`

  if (recommendLocation?.lat && recommendLocation?.lng && map.value && window.kakao?.maps) {
    userLocation.value = {
      lat: recommendLocation.lat,
      lng: recommendLocation.lng,
    }

    currentSearchLabel.value = '은행 성향 테스트 위치'

    const center = new window.kakao.maps.LatLng(recommendLocation.lat, recommendLocation.lng)

    map.value.setCenter(center)
    map.value.setLevel(4)

    setBaseMarker(center, '은행 성향 테스트 위치', 'red')
  }

  if (map.value) {
    await searchNearbyBanks()
  }
}

const escapeHtml = (value = '') => {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;')
}

const getBaseMarkerContent = (color = 'green') => {
  const colorMap = {
    green: {
      main: '#16a34a',
      light: 'rgba(22, 163, 74, 0.22)',
      border: '#ffffff',
    },
    red: {
      main: '#dc2626',
      light: 'rgba(220, 38, 38, 0.22)',
      border: '#ffffff',
    },
  }

  const theme = colorMap[color] || colorMap.green

  return `
    <div style="
      position: relative;
      width: 34px;
      height: 44px;
    ">
      <div style="
        position: absolute;
        left: 50%;
        top: 0;
        width: 34px;
        height: 34px;
        transform: translateX(-50%);
        border-radius: 50% 50% 50% 0;
        background: ${theme.main};
        border: 3px solid ${theme.border};
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.28);
        rotate: -45deg;
      ">
        <div style="
          position: absolute;
          left: 50%;
          top: 50%;
          width: 12px;
          height: 12px;
          transform: translate(-50%, -50%);
          border-radius: 50%;
          background: white;
        "></div>
      </div>

      <div style="
        position: absolute;
        left: 50%;
        top: -8px;
        width: 48px;
        height: 48px;
        transform: translateX(-50%);
        border-radius: 50%;
        background: ${theme.light};
        z-index: -1;
      "></div>
    </div>
  `
}

const setBaseMarker = (position, label, color = 'green') => {
  if (baseMarker.value) {
    baseMarker.value.setMap(null)
  }

  baseMarker.value = new window.kakao.maps.CustomOverlay({
    map: map.value,
    position,
    content: getBaseMarkerContent(color),
    xAnchor: 0.5,
    yAnchor: 1,
    zIndex: 30,
  })
}

const getRoutePointContent = (label, color = 'blue') => {
  const colorMap = {
    blue: '#2563eb',
    red: '#ef4444',
  }

  const mainColor = colorMap[color] || colorMap.blue
  const safeLabel = escapeHtml(label)

  return `
    <div style="
      position: relative;
      width: 42px;
      height: 54px;
      text-align: center;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    ">
      <div style="
        position: absolute;
        left: 50%;
        top: 0;
        transform: translateX(-50%);
        padding: 5px 8px;
        border-radius: 999px;
        background: ${mainColor};
        color: white;
        font-size: 11px;
        font-weight: 800;
        white-space: nowrap;
        box-shadow: 0 3px 8px rgba(0,0,0,0.25);
        z-index: 2;
      ">
        ${safeLabel}
      </div>

      <div style="
        position: absolute;
        left: 50%;
        top: 22px;
        width: 28px;
        height: 28px;
        transform: translateX(-50%) rotate(-45deg);
        border-radius: 50% 50% 50% 0;
        background: ${mainColor};
        border: 3px solid white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.28);
      ">
        <div style="
          position: absolute;
          left: 50%;
          top: 50%;
          width: 8px;
          height: 8px;
          transform: translate(-50%, -50%);
          border-radius: 50%;
          background: white;
        "></div>
      </div>
    </div>
  `
}

const clearRoutePointMarkers = () => {
  if (startRouteMarker.value) {
    startRouteMarker.value.setMap(null)
    startRouteMarker.value = null
  }

  if (endRouteMarker.value) {
    endRouteMarker.value.setMap(null)
    endRouteMarker.value = null
  }
}

const setRoutePointMarkers = (startPosition, endPosition) => {
  clearRoutePointMarkers()

  startRouteMarker.value = new window.kakao.maps.CustomOverlay({
    map: map.value,
    position: startPosition,
    content: getRoutePointContent('출발', 'blue'),
    xAnchor: 0.5,
    yAnchor: 1,
    zIndex: 50,
  })

  endRouteMarker.value = new window.kakao.maps.CustomOverlay({
    map: map.value,
    position: endPosition,
    content: getRoutePointContent('도착', 'red'),
    xAnchor: 0.5,
    yAnchor: 1,
    zIndex: 50,
  })
}

const closeMapOverlays = () => {
  if (currentInfoWindow.value) {
    currentInfoWindow.value.close()
    currentInfoWindow.value = null
  }

  selectedPlace.value = null
  routeSummary.value = null
  routeError.value = ''
  routeLoading.value = false

  if (routeLine.value) {
    routeLine.value.setMap(null)
    routeLine.value = null
  }

  if (routeBorderLine.value) {
    routeBorderLine.value.setMap(null)
    routeBorderLine.value = null
  }

  clearRoutePointMarkers()
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

  mapError.value = ''
  mapMessage.value = ''
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
      .filter((place) => !place.distance || Number(place.distance) <= BANK_SEARCH_RADIUS)
      .slice(0, MAX_BANK_RESULTS)

    if (places.length === 0) {
      mapMessage.value = `${currentSearchLabel.value} 주변의 ${keyword} 검색 결과가 없습니다.`
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

      const placeName = escapeHtml(place.place_name || place.name || keyword)
      const placeAddress = escapeHtml(place.road_address_name || place.address_name || place.address || '')

      const infoWindow = new window.kakao.maps.InfoWindow({
        content: `
          <div style="padding:8px 10px;font-size:13px;line-height:1.5;min-width:190px;max-width:260px;">
            <strong>${placeName}</strong><br />
            ${placeAddress}
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
        drawDrivingRoute(place, lat, lng)
      })

      markers.value.push(marker)
      bounds.extend(position)
    })

    if (markers.value.length > 0) {
      map.value.setBounds(bounds)
    } else {
      mapMessage.value = '은행 데이터는 받았지만 좌표가 없어 지도에 표시하지 못했습니다.'
    }
  } catch (error) {
    console.error('은행 검색 실패:', error)
    mapError.value = '은행 검색 중 오류가 발생했습니다. 백엔드 maps API를 확인해주세요.'
  }
}

const formatDistance = (meter) => {
  if (!meter && meter !== 0) return ''
  if (meter >= 1000) return `${(meter / 1000).toFixed(1)}km`
  return `${meter.toLocaleString()}m`
}

const formatDuration = (second) => {
  if (!second && second !== 0) return ''

  const minutes = Math.round(second / 60)

  if (minutes >= 60) {
    const hours = Math.floor(minutes / 60)
    const remainMinutes = minutes % 60
    return remainMinutes ? `${hours}시간 ${remainMinutes}분` : `${hours}시간`
  }

  return `${minutes}분`
}

const normalizeRouteResponse = (data) => {
  const route = data?.routes?.[0] || data?.route || data?.result?.routes?.[0]

  if (!route || route.result_code !== 0) {
    throw new Error(route?.result_msg || '경로를 찾지 못했습니다.')
  }

  const path = []

  route.sections?.forEach((section) => {
    section.roads?.forEach((road) => {
      const vertexes = road.vertexes || []

      for (let index = 0; index < vertexes.length; index += 2) {
        const lng = Number(vertexes[index])
        const lat = Number(vertexes[index + 1])

        if (!Number.isNaN(lat) && !Number.isNaN(lng)) {
          path.push(new window.kakao.maps.LatLng(lat, lng))
        }
      }
    })
  })

  if (path.length === 0) {
    throw new Error('경로 좌표가 없습니다. Mobility 응답에서 sections.roads.vertexes를 확인해주세요.')
  }

  const summary = route.summary || {}

  return {
    path,
    summary: {
      distance: Number(summary.distance || 0),
      duration: Number(summary.duration || 0),
      taxi: Number(summary.fare?.taxi || 0),
      toll: Number(summary.fare?.toll || 0),
    },
  }
}

const drawDrivingRoute = async (place, destLat, destLng) => {
  if (routeLine.value) {
    routeLine.value.setMap(null)
    routeLine.value = null
  }

  if (routeBorderLine.value) {
    routeBorderLine.value.setMap(null)
    routeBorderLine.value = null
  }

  routeSummary.value = null
  routeError.value = ''
  routeLoading.value = true

  try {
    const response = await api.get('/maps/routes/', {
      params: {
        origin_lat: userLocation.value.lat,
        origin_lng: userLocation.value.lng,
        destination_lat: destLat,
        destination_lng: destLng,
        destination_name: place.place_name || place.name || selectedBankKeyword.value,
        priority: 'RECOMMEND',
      },
    })

    const { path, summary } = normalizeRouteResponse(response.data)

    const startPosition = new window.kakao.maps.LatLng(
      userLocation.value.lat,
      userLocation.value.lng
    )

    const endPosition = new window.kakao.maps.LatLng(destLat, destLng)

    routeBorderLine.value = new window.kakao.maps.Polyline({
      path,
      strokeWeight: 11,
      strokeColor: '#ffffff',
      strokeOpacity: 0.95,
      strokeStyle: 'solid',
      zIndex: 25,
    })

    routeLine.value = new window.kakao.maps.Polyline({
      path,
      strokeWeight: 6,
      strokeColor: '#258fff',
      strokeOpacity: 1,
      strokeStyle: 'solid',
      endArrow: true,
      zIndex: 30,
    })

    routeBorderLine.value.setMap(map.value)
    routeLine.value.setMap(map.value)

    const bounds = new window.kakao.maps.LatLngBounds()

    path.forEach((position) => bounds.extend(position))
    bounds.extend(startPosition)
    bounds.extend(endPosition)

    map.value.setBounds(bounds, 80, 80, 80, 80)

    routeSummary.value = {
      ...summary,
      distanceText: formatDistance(summary.distance),
      durationText: formatDuration(summary.duration),
      taxiText: summary.taxi ? `${summary.taxi.toLocaleString()}원` : '',
      tollText: summary.toll ? `${summary.toll.toLocaleString()}원` : '',
    }
  } catch (error) {
    console.error('경로 검색 실패:', error)
    routeError.value = '경로를 그리지 못했습니다. /maps/routes/ 백엔드 API를 확인해주세요.'
  } finally {
    routeLoading.value = false
  }
}

const openKakaoDirection = () => {
  if (!selectedPlace.value) return

  const destName = selectedPlace.value.place_name || selectedPlace.value.name
  const destLat = selectedPlace.value.y || selectedPlace.value.lat
  const destLng = selectedPlace.value.x || selectedPlace.value.lng

  const url = `https://map.kakao.com/link/to/${encodeURIComponent(destName)},${destLat},${destLng}`

  window.open(url, '_blank')
}


const selectVideo = (video) => {
  selectedVideo.value = video
}

const getVideoId = (video) => {
  if (!video) {
    return ''
  }

  if (video.video_id) {
    return video.video_id
  }

  if (video.id?.videoId) {
    return video.id.videoId
  }

  if (typeof video.id === 'string') {
    return video.id
  }

  return ''
}

const isSavedVideo = (video) => {
  const videoId = getVideoId(video)
  return savedVideoIds.value.has(videoId)
}

const loadSavedVideos = async () => {
  const token = localStorage.getItem('token')

  if (!token) {
    savedVideoIds.value = new Set()
    return
  }

  try {
    const response = await getSavedVideos()
    const savedVideos = response.data || []

    savedVideoIds.value = new Set(
      savedVideos
        .map((video) => video.video_id || video.id)
        .filter((videoId) => !!videoId)
    )
  } catch (error) {
    console.error('저장 영상 목록 조회 실패:', error)
    savedVideoIds.value = new Set()
  }
}

const loadVideos = async (keyword, maxResults = 3) => {
  videoLoading.value = true
  videoError.value = ''
  selectedVideo.value = null

  try {
    const response = await searchVideos(keyword, maxResults)
    const result = Array.isArray(response.data) ? response.data : []

    videos.value = result
    selectedVideo.value = result.length > 0 ? { ...result[0] } : null
  } catch (error) {
    console.error(error)
    videoError.value = '영상을 불러오지 못했습니다. 백엔드 videos API를 확인해주세요.'
    videos.value = []
    selectedVideo.value = null
  } finally {
    videoLoading.value = false
  }
}

const handleVideoSearch = () => {
  videoError.value = ''

  if (!videoKeyword.value) {
    videoError.value = '검색어를 입력해주세요.'
    return
  }

  loadVideos(videoKeyword.value, 9)
}

const scrollToVideoSection = () => {
  videoSection.value?.scrollIntoView({
    behavior: 'smooth',
    block: 'start',
  })
}

const handlePreviousQuestion = () => {
  if (bankFitTestRef.value?.goPreviousQuestion) {
    bankFitTestRef.value.goPreviousQuestion()
    return
  }

  bankFitTestKey.value += 1
}

const handleRestartTest = () => {
  if (bankFitTestRef.value?.resetTest) {
    bankFitTestRef.value.resetTest()
    return
  }

  bankFitTestKey.value += 1
}


const handleToggleSaveVideo = async (video) => {
  const token = localStorage.getItem('token')
  const videoId = getVideoId(video)

  videoError.value = ''

  if (!token) {
    videoError.value = '로그인 후 저장할 수 있습니다.'
    return
  }

  if (!videoId) {
    videoError.value = '영상 정보를 확인할 수 없습니다.'
    return
  }

  savingVideoId.value = videoId

  try {
    const nextSavedVideoIds = new Set(savedVideoIds.value)

    if (nextSavedVideoIds.has(videoId)) {
      await deleteSavedVideo(videoId)
      nextSavedVideoIds.delete(videoId)
    } else {
      await saveVideo({
        ...video,
        id: videoId,
        video_id: videoId,
      })
      nextSavedVideoIds.add(videoId)
    }

    savedVideoIds.value = nextSavedVideoIds
  } catch (error) {
    console.error(error)

    if (error.response?.status === 401) {
      videoError.value = '로그인 후 저장할 수 있습니다.'
      return
    }

    videoError.value = '영상 저장 상태를 변경하지 못했습니다.'
  } finally {
    savingVideoId.value = null
  }
}

onMounted(async () => {
  await initMap()
  await searchBySelectedRegion()
  await loadVideos('주거래은행 선택 기준', 3)
  await loadSavedVideos()
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

.main-bank-page {
  width: min(var(--container-width, 1360px), calc(100% - 48px));
  margin: 0 auto;
  padding: 22px 0 64px;
}

.map-guide-banner {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 14px;
  align-items: center;
  padding: 14px 18px;
  margin-bottom: 24px;
  border: 1px solid #c7d7fe;
  border-radius: 16px;
  background: linear-gradient(90deg, #eff6ff, #f8fbff);
  color: #0f1b3d;
}

.banner-icon {
  display: grid;
  place-items: center;
  width: 56px;
  height: 44px;
  border-radius: 14px;
  background: #ffffff;
  box-shadow: 0 10px 24px rgba(30, 64, 175, 0.08);
  font-size: 26px;
}

.map-guide-banner strong {
  display: block;
  font-size: 15px;
  font-weight: 950;
}

.map-guide-banner p {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 13px;
  line-height: 1.5;
}

.page-header {
  margin-bottom: 24px;
}

.map-heading {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: flex-end;
}

.eyebrow {
  margin: 0 0 8px;
  color: #1116b8;
  font-size: 12px;
  font-weight: 950;
  letter-spacing: 0.12em;
}

.page-header h1 {
  margin: 0 0 10px;
  color: #0f1b3d;
  font-size: clamp(32px, 3.4vw, 44px);
  line-height: 1.15;
  font-weight: 950;
  letter-spacing: -0.06em;
}

.page-header p,
.video-header p {
  margin: 0;
  color: #64748b;
  line-height: 1.65;
}

.page-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.ghost-action {
  min-height: 42px;
  padding: 0 14px;
  border: 1px solid #dbe4f0;
  border-radius: 12px;
  background: #fff;
  color: #0f1b3d;
  font-weight: 850;
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(15, 27, 61, 0.04);
}

.ghost-action:hover {
  border-color: #1116b8;
  color: #1116b8;
}

.bank-map-section {
  display: grid;
  grid-template-columns: 320px minmax(0, 1fr);
  gap: 18px;
  align-items: stretch;
}

.bank-list {
  min-width: 0;
}

.bank-fit-test-panel {
  position: static;
}

.map-area {
  min-width: 0;
  border: 1px solid #dbe4f0;
  border-radius: 22px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 18px 48px rgba(15, 27, 61, 0.06);
}

.map-toolbar {
  padding: 18px;
  border-bottom: 1px solid #edf2f7;
  background: #fff;
}

.search-panel {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.filter-row {
  display: grid;
  grid-template-columns: repeat(4, minmax(130px, 1fr));
  gap: 12px;
}

.filter-box {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.filter-box label {
  color: #52627a;
  font-size: 12px;
  font-weight: 900;
}

.filter-box select,
.video-search input {
  width: 100%;
  min-height: 44px;
  border: 1px solid #d8e2ef;
  border-radius: 13px;
  padding: 0 13px;
  background: #fff;
  color: #0f1b3d;
  font-weight: 750;
  outline: none;
}

.filter-box select:focus,
.video-search input:focus {
  border-color: #1116b8;
  box-shadow: 0 0 0 4px rgba(17, 22, 184, 0.08);
}

.bank-select-box select {
  font-weight: 900;
}

.button-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.search-button,
.location-button,
.selected-place button,
.video-search button,
.video-buttons button {
  min-height: 42px;
  border: none;
  border-radius: 12px;
  padding: 0 16px;
  background: #1116b8;
  color: white;
  cursor: pointer;
  white-space: nowrap;
  font-weight: 900;
  box-shadow: 0 12px 24px rgba(17, 22, 184, 0.16);
}

.location-button,
.video-buttons .save-button {
  background: #0f1b3d;
}

.search-button:hover,
.location-button:hover,
.selected-place button:hover,
.video-search button:hover,
.video-buttons button:hover {
  transform: translateY(-1px);
}

.video-buttons .save-button.saved {
  background: #64748b;
  cursor: pointer;
}

.video-buttons .save-button:disabled {
  opacity: 0.75;
  cursor: wait;
}

.search-base {
  margin: 0;
  color: #64748b;
  font-size: 13px;
  font-weight: 750;
}

.map-error,
.map-message {
  margin: 0;
  padding: 11px 13px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 800;
}

.map-error {
  border: 1px solid #fecaca;
  background: #fff5f5;
  color: #dc2626;
}

.map-message {
  border: 1px solid #bfdbfe;
  background: #eff6ff;
  color: #1116b8;
}

.map {
  width: 100%;
  height: 520px;
  background: #eef4fb;
}

.selected-place {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: center;
  padding: 18px;
  border-top: 1px solid #edf2f7;
  background: linear-gradient(180deg, #fff, #f8fbff);
}

.selected-label {
  margin: 0 0 5px;
  color: #1116b8;
  font-size: 12px;
  font-weight: 950;
  letter-spacing: 0.04em;
}

.selected-place h3 {
  margin: 0 0 8px;
  color: #0f1b3d;
  font-size: 20px;
  font-weight: 950;
}

.selected-place p {
  margin: 4px 0;
  color: #52627a;
  font-size: 14px;
  line-height: 1.55;
}

.route-summary {
  font-weight: 900;
  color: #1116b8 !important;
}

.route-error {
  color: #dc2626 !important;
}

.video-section {
  scroll-margin-top: calc(var(--header-height, 72px) + 18px);
  margin-top: 46px;
  padding: 26px;
  border: 1px solid #dbe4f0;
  border-radius: 22px;
  background: #fff;
  box-shadow: 0 18px 48px rgba(15, 27, 61, 0.05);
}

.video-header {
  margin-bottom: 18px;
}

.video-header h2 {
  margin: 0 0 10px;
  color: #0f1b3d;
  font-size: 28px;
  font-weight: 950;
  letter-spacing: -0.04em;
}

.video-search {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 10px;
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
  overflow: hidden;
  border: 1px solid #dbe4f0;
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 12px 30px rgba(15, 27, 61, 0.04);
}

.thumbnail-button {
  display: block;
  width: 100%;
  border: none;
  padding: 0;
  background: #f1f5f9;
  cursor: pointer;
}

.thumbnail-button img {
  width: 100%;
  height: 170px;
  object-fit: cover;
  display: block;
}

.video-info {
  padding: 15px;
}

.video-info h3 {
  min-height: 44px;
  margin: 0 0 8px;
  color: #0f1b3d;
  font-size: 16px;
  line-height: 1.4;
  font-weight: 950;
}

.video-info p {
  margin: 0 0 12px;
  color: #64748b;
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
  color: #0f1b3d;
}

.iframe-box {
  position: relative;
  width: 100%;
  padding-top: 56.25%;
  border-radius: 18px;
  overflow: hidden;
  background: #0f1b3d;
}

.iframe-box iframe {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: 0;
}

.message {
  color: #64748b;
}

.error {
  color: #dc2626;
}

@media (max-width: 1180px) {
  .bank-map-section {
    grid-template-columns: 1fr;
  }

  .bank-fit-test-panel {
    position: static;
  }

  .filter-row {
    grid-template-columns: repeat(2, minmax(130px, 1fr));
  }
}

@media (max-width: 860px) {
  .main-bank-page {
    width: min(100% - 28px, var(--container-width, 1360px));
  }

  .map-heading,
  .selected-place {
    align-items: stretch;
    flex-direction: column;
  }

  .page-actions {
    justify-content: flex-start;
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
  .video-grid,
  .video-search {
    grid-template-columns: 1fr;
  }

  .video-search button {
    padding: 12px;
  }
}

/* === 주연: 주거래은행 페이지 최종 정리 === */
.map-guide-banner {
  display: none !important;
}

.main-bank-page {
  padding-top: 28px;
}

.map-heading {
  margin-bottom: 22px;
  align-items: center;
}

.map-heading h1 {
  margin: 0;
  font-size: clamp(36px, 4vw, 52px);
  line-height: 1.08;
  letter-spacing: -0.07em;
}

.video-jump-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  padding: 0 18px;
  border: 1px solid #cbd8ee;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.92);
  color: #1116b8;
  font-weight: 950;
  cursor: pointer;
  box-shadow: 0 12px 28px rgba(15, 27, 61, 0.06);
}

.video-jump-button:hover {
  border-color: #1116b8;
  transform: translateY(-1px);
}

.bank-map-section {
  align-items: start;
}

.bank-list {
  display: grid;
  gap: 14px;
  min-width: 0;
}

.test-control-panel {
  display: grid;
  grid-template-columns: 44px minmax(0, 1fr);
  gap: 12px;
  padding: 16px;
  border: 1px solid #dbe4f0;
  border-radius: 18px;
  background: linear-gradient(180deg, #f8fbff, #fff);
  box-shadow: 0 16px 34px rgba(15, 27, 61, 0.06);
}

.control-icon {
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border-radius: 999px;
  background: #eef4ff;
  color: #1116b8;
  font-size: 24px;
  font-weight: 950;
}

.test-control-panel h3 {
  margin: 2px 0 5px;
  color: #0f1b3d;
  font-size: 16px;
  font-weight: 950;
  letter-spacing: -0.03em;
}

.test-control-panel p {
  margin: 0;
  color: #64748b;
  font-size: 12px;
  line-height: 1.55;
}

.control-buttons {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 9px;
  margin-top: 4px;
}

.control-button {
  min-height: 42px;
  border-radius: 12px;
  font-weight: 950;
  cursor: pointer;
}

.control-button.outline {
  border: 1px solid #cbd8ee;
  background: #fff;
  color: #1116b8;
}

.control-button.primary {
  border: 0;
  background: #1116b8;
  color: #fff;
  box-shadow: 0 10px 22px rgba(17, 22, 184, 0.16);
}

.map-area {
  border-radius: 22px;
}

.video-section {
  scroll-margin-top: calc(var(--header-height, 64px) + 18px);
}

.video-header {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: flex-start;
}

.video-header h2 {
  margin-bottom: 8px;
}

.video-search {
  margin-top: 18px;
}

@media (max-width: 1180px) {
  .test-control-panel {
    position: static;
  }
}

@media (max-width: 640px) {
  .map-heading {
    align-items: flex-start;
  }

  .video-jump-button {
    width: 100%;
  }

  .control-buttons {
    grid-template-columns: 1fr;
  }
}


/* === 주연: 주거래은행 페이지 스크롤/영상 문구 보정 === */
.bank-fit-test-panel {
  position: static !important;
  top: auto !important;
}

.bank-list {
  align-self: start;
}

.video-header p {
  display: none !important;
}

.video-section {
  margin-top: 34px;
}


/* === 주연: 주거래은행 영상 단순 복구 === */
.video-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.iframe-box {
  position: relative !important;
  width: 100% !important;
  aspect-ratio: 16 / 9 !important;
  min-height: 0 !important;
  overflow: hidden !important;
  border-radius: 18px !important;
  background: #000 !important;
}

.iframe-box iframe {
  position: absolute !important;
  inset: 0 !important;
  display: block !important;
  width: 100% !important;
  height: 100% !important;
  border: 0 !important;
  background: #000 !important;
}


/* === 주연: 주거래은행 영상 재생 안정화 === */
.iframe-box {
  position: relative !important;
  width: 100% !important;
  aspect-ratio: 16 / 9 !important;
  overflow: hidden !important;
  border-radius: 18px !important;
  background: #000 !important;
}

.iframe-box iframe {
  position: absolute !important;
  inset: 0 !important;
  display: block !important;
  width: 100% !important;
  height: 100% !important;
  border: 0 !important;
  background: #000 !important;
}

.video-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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

.main-bank-page {
  padding-top: 30px !important;
}

.main-bank-page .page-hero-row {
  margin-bottom: 24px !important;
}


</style>
