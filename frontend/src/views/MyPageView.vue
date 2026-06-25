<template>
  <div class="mypage-view">
    <section class="page-header">
      <h1>마이페이지</h1>
    </section>

    <p v-if="pageLoading" class="status-message">
      마이페이지 정보를 불러오는 중입니다...
    </p>

    <p v-else-if="pageErrorMessage" class="status-message error">
      {{ pageErrorMessage }}
    </p>

    <template v-else>
      <section class="profile-hero-card card">
        <div class="profile-main-info">
          <div class="profile-image large">
            <img
              v-if="profileImagePreview || profileImageUrl"
              :src="profileImagePreview || profileImageUrl"
              alt="프로필 이미지"
            />
            <span v-else>{{ profileInitial }}</span>
          </div>

          <div class="profile-title">
            <div class="title-row">
              <h2>{{ profileUser.username || '사용자' }}님</h2>
            </div>
            <p>{{ profileUser.email || '이메일 정보 없음' }}</p>
          </div>
        </div>

        <button type="button" class="edit-profile-button" @click="startEditProfile">
          ✎ 프로필 수정
        </button>

        <div class="profile-summary-grid">
          <div class="summary-item">
            <span class="summary-icon age">{{ ageIconText }}</span>
            <div>
              <small>나이</small>
              <strong>{{ profileForm.age ? `${profileForm.age}세` : '미입력' }}</strong>
            </div>
          </div>

          <div class="summary-item">
            <span class="summary-icon" :class="genderIconClass">{{ genderIcon }}</span>
            <div>
              <small>성별</small>
              <strong>{{ genderLabel }}</strong>
            </div>
          </div>

          <div class="summary-item">
            <span class="summary-icon income">₩</span>
            <div>
              <small>월 소득 구간</small>
              <strong>{{ getOptionLabel('monthly_income_range', profileForm.monthly_income_range) }}</strong>
            </div>
          </div>

          <div class="summary-item">
            <span class="summary-icon saving">🐷</span>
            <div>
              <small>월 저축 가능 금액</small>
              <strong>{{ getOptionLabel('monthly_saving_amount', profileForm.monthly_saving_amount) }}</strong>
            </div>
          </div>

          <div class="summary-item">
            <span class="summary-icon lump-sum">🪙</span>
            <div>
              <small>현재 보유 목돈</small>
              <strong>{{ getOptionLabel('lump_sum_amount', profileForm.lump_sum_amount) }}</strong>
            </div>
          </div>

          <div class="summary-item">
            <span class="summary-icon bank">🏦</span>
            <div>
              <small>주거래은행</small>
              <strong>{{ profileForm.main_bank || '미입력' }}</strong>
            </div>
          </div>

          <div class="summary-item">
            <span class="summary-icon location">지역</span>
            <div>
              <small>거주 지역</small>
              <strong>{{ profileForm.address || '미입력' }}</strong>
            </div>
          </div>

          <div class="summary-item">
            <span class="summary-icon consent">✓</span>
            <div>
              <small>개인정보 동의</small>
              <strong>{{ profileForm.personal_info_agree ? '동의 완료' : '미동의' }}</strong>
            </div>
          </div>
        </div>
      </section>

      <section v-if="isEditingProfile" class="profile-edit-panel card">
        <div class="section-title-row compact">
          <div>
            <h2>프로필 수정</h2>
          </div>
          <button type="button" class="secondary-button" @click="cancelEditProfile">
            닫기
          </button>
        </div>

        <form class="profile-edit-form" @submit.prevent="handleUpdateProfile">
          <div class="image-edit-box">
            <div class="profile-image small">
              <img
                v-if="profileImagePreview || profileImageUrl"
                :src="profileImagePreview || profileImageUrl"
                alt="프로필 이미지 미리보기"
              />
              <span v-else>{{ profileInitial }}</span>
            </div>

            <label class="file-label">
              프로필 사진
              <input
                type="file"
                accept="image/*"
                @change="handleProfileImageChange"
              />
            </label>

            <p class="help-text">JPG, PNG 등 이미지 파일을 선택할 수 있습니다.</p>
          </div>

          <div class="edit-form-grid">
            <label>
              이메일
              <input v-model="profileForm.email" type="email" />
            </label>

            <label>
              나이
              <select v-model.number="profileForm.age">
                <option :value="null" disabled hidden>나이를 선택하세요</option>
                <option
                  v-for="option in profileOptions.age"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
            </label>

            <label>
              성별
              <select v-model="profileForm.gender">
                <option
                  v-for="option in profileOptions.gender"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
            </label>

            <label>
              월 소득 구간
              <select v-model="profileForm.monthly_income_range">
                <option value="" disabled hidden>월 소득 구간을 선택하세요</option>
                <option
                  v-for="option in profileOptions.monthly_income_range"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
            </label>

            <label>
              월 저축 가능 금액
              <select v-model="profileForm.monthly_saving_amount">
                <option value="" disabled hidden>월 저축 가능 금액을 선택하세요</option>
                <option
                  v-for="option in profileOptions.monthly_saving_amount"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
            </label>

            <label>
              현재 보유 목돈
              <select v-model="profileForm.lump_sum_amount">
                <option value="" disabled hidden>현재 보유 목돈을 선택하세요</option>
                <option
                  v-for="option in profileOptions.lump_sum_amount"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
            </label>

            <label>
              주거래은행
              <select v-model="profileForm.main_bank">
                <option value="" disabled hidden>주거래은행을 선택하세요</option>
                <option
                  v-for="option in profileOptions.main_bank"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
            </label>

            <label>
              거주 지역
              <select v-model="profileForm.address">
                <option value="" disabled hidden>거주 지역을 선택하세요</option>
                <option
                  v-for="option in profileOptions.address"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
            </label>
          </div>

          <p v-if="profileMessage" class="form-message success">
            {{ profileMessage }}
          </p>

          <div class="form-actions">
            <button type="submit" class="primary-button" :disabled="profileSaving">
              {{ profileSaving ? '저장 중...' : '프로필 저장' }}
            </button>

            <button type="button" class="secondary-button" @click="cancelEditProfile">
              취소
            </button>
          </div>
        </form>
      </section>
<div class="content-grid">
        <section class="favorites-section card">
          <div class="section-title-row">
            <div>
              <h2>관심상품</h2>
              <p>저장한 예금과 적금 상품입니다.</p>
            </div>
            <span class="count-pill">{{ favoriteProducts.length }}</span>
          </div>

          <p v-if="favoriteProducts.length === 0" class="empty-message">
            등록된 관심상품이 없습니다.
          </p>

          <template v-else>
            <section class="favorite-group">
              <div class="group-header">
                <h3>관심 정기예금</h3>
                <span>{{ depositFavorites.length }}개</span>
              </div>

              <p v-if="depositFavorites.length === 0" class="empty-message compact">
                등록된 관심 정기예금이 없습니다.
              </p>

              <div
                v-for="favorite in depositFavorites"
                :key="favorite.id"
                class="favorite-card"
              >
                <span class="favorite-bank-logo">
                  <img
                    v-if="getFavoriteBankLogo(favorite)"
                    :src="getFavoriteBankLogo(favorite)"
                    :alt="`${getBankName(favorite)} 로고`"
                  >
                  <em v-else>{{ getBankName(favorite).slice(0, 1) }}</em>
                </span>
                <div class="favorite-info">
                  <span class="product-type-badge">예금</span>
                  <h4>{{ getProductName(favorite) }}</h4>
                  <p>{{ getBankName(favorite) }} · 최고 금리 {{ formatRate(getMaxInterestRate(favorite)) }}</p>
                </div>

                <div class="card-actions">
                  <RouterLink class="detail-link" :to="{ name: 'product-detail', params: { id: getProductId(favorite) }, query: { type: getProductType(favorite) } }">
                    상세 보기
                  </RouterLink>
                  <button type="button" class="delete-button icon" @click="handleRemoveFavorite(favorite)">
                    삭제
                  </button>
                </div>
              </div>
            </section>

            <section class="favorite-group">
              <div class="group-header">
                <h3>관심 적금</h3>
                <span>{{ savingFavorites.length }}개</span>
              </div>

              <p v-if="savingFavorites.length === 0" class="empty-message compact">
                등록된 관심 적금이 없습니다.
              </p>

              <div
                v-for="favorite in savingFavorites"
                :key="favorite.id"
                class="favorite-card"
              >
                <span class="favorite-bank-logo">
                  <img
                    v-if="getFavoriteBankLogo(favorite)"
                    :src="getFavoriteBankLogo(favorite)"
                    :alt="`${getBankName(favorite)} 로고`"
                  >
                  <em v-else>{{ getBankName(favorite).slice(0, 1) }}</em>
                </span>
                <div class="favorite-info">
                  <span class="product-type-badge saving">적금</span>
                  <h4>{{ getProductName(favorite) }}</h4>
                  <p>{{ getBankName(favorite) }} · 최고 금리 {{ formatRate(getMaxInterestRate(favorite)) }}</p>
                </div>

                <div class="card-actions">
                  <RouterLink class="detail-link" :to="{ name: 'product-detail', params: { id: getProductId(favorite) }, query: { type: getProductType(favorite) } }">
                    상세 보기
                  </RouterLink>
                  <button type="button" class="delete-button icon" @click="handleRemoveFavorite(favorite)">
                    삭제
                  </button>
                </div>
              </div>
            </section>
          </template>
        </section>

        <section class="videos-section card">
          <div class="section-title-row">
            <div>
              <h2>저장한 유튜브 영상</h2>
              <p>추천 정보와 금융 지식을 다시 볼 수 있습니다.</p>
            </div>
            <span class="count-pill">{{ savedVideos.length }}</span>
          </div>

          <p v-if="savedVideos.length === 0" class="empty-message">
            저장한 유튜브 영상이 없습니다.
          </p>

          <div v-else class="video-grid">
            <article v-for="video in savedVideos" :key="video.id" class="video-card">
              <a
                class="video-thumb-wrap"
                :href="`https://www.youtube.com/watch?v=${video.video_id}`"
                target="_blank"
                rel="noopener noreferrer"
              >
                <img
                  v-if="video.thumbnail_url"
                  :src="video.thumbnail_url"
                  :alt="video.title"
                  class="video-thumbnail"
                />
                <span class="play-button">▶</span>
              </a>

              <div class="video-content">
                <h3>{{ video.title }}</h3>
                <p>{{ video.channel_title || '채널 정보 없음' }}</p>

                <div class="card-actions">
                  <a
                    class="detail-link"
                    :href="`https://www.youtube.com/watch?v=${video.video_id}`"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    유튜브 보기
                  </a>

                  <button type="button" class="delete-button icon" @click="handleDeleteVideo(video.video_id)">
                    삭제
                  </button>
                </div>
              </div>
            </article>
          </div>
        </section>
      </div>

      <section class="account-shortcuts">
        <button type="button" class="account-shortcut-card" @click="openAccountPanel('password')">
          <span>🔒</span>
          <div>
            <strong>비밀번호 변경</strong>
            <p>안전한 계정 관리를 위해 비밀번호를 주기적으로 변경해주세요.</p>
          </div>
          <em>›</em>
        </button>

        <button type="button" class="account-shortcut-card danger" @click="openAccountPanel('withdraw')">
          <span>👤</span>
          <div>
            <strong>회원탈퇴</strong>
            <p>더 이상 서비스를 이용하지 않는다면 계정을 비활성화할 수 있습니다.</p>
          </div>
          <em>›</em>
        </button>
      </section>


      <section ref="passwordPanelRef" v-if="activeAccountPanel === 'password'" class="account-action-panel card">
        <div class="section-title-row compact">
          <div>
            <h2>비밀번호 변경</h2>
          </div>
        </div>

        <form class="account-manage-form single" @submit.prevent="handleChangePassword">
          <label>
            현재 비밀번호
            <input v-model="passwordForm.current_password" type="password" autocomplete="current-password">
          </label>

          <label>
            새 비밀번호
            <input v-model="passwordForm.new_password" type="password" autocomplete="new-password">
          </label>

          <label>
            새 비밀번호 확인
            <input v-model="passwordForm.new_password_confirm" type="password" autocomplete="new-password">
          </label>

          <p v-if="passwordMessage" class="form-message">{{ passwordMessage }}</p>

          <div class="form-actions">
            <button type="submit" class="primary-button" :disabled="passwordSaving">
              {{ passwordSaving ? '변경 중...' : '비밀번호 변경' }}
            </button>

            <button type="button" class="secondary-button" @click="closeAccountPanel">
              취소
            </button>
          </div>
        </form>
      </section>

      <section ref="withdrawPanelRef" v-if="activeAccountPanel === 'withdraw'" class="account-action-panel danger card">
        <div class="section-title-row compact">
          <div>
            <h2>회원탈퇴</h2>
            <p>탈퇴하면 계정이 비활성화되어 다시 로그인할 수 없습니다.</p>
          </div>
        </div>

        <form class="account-manage-form single" @submit.prevent="handleWithdraw">
          <label>
            비밀번호 확인
            <input v-model="withdrawPassword" type="password" autocomplete="current-password">
          </label>

          <p v-if="withdrawMessage" class="form-message">{{ withdrawMessage }}</p>

          <div class="form-actions">
            <button type="submit" class="delete-button" :disabled="withdrawSaving">
              {{ withdrawSaving ? '탈퇴 처리 중...' : '회원탈퇴' }}
            </button>

            <button type="button" class="secondary-button" @click="closeAccountPanel">
              취소
            </button>
          </div>
        </form>
      </section>

      
    </template>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  getProfile,
  getProfileOptions,
  updateProfile,
  changePassword,
  withdraw,
} from '@/api/accounts'
import { getFavoriteProducts, toggleFavoriteProduct } from '@/api/favorites'
import { getSavedVideos, deleteSavedVideo } from '@/api/videos'
import { getBankDisplayName, getBankLogo } from '@/constants/bankLogoMap'

const router = useRouter()
const authStore = useAuthStore()
const pageLoading = ref(false)
const pageErrorMessage = ref('')

const profileUser = ref({
  id: null,
  username: '',
  email: '',
})

const profileForm = ref({
  email: '',
  age: null,
  gender: 'unknown',
  monthly_income_range: '',
  monthly_saving_amount: '',
  lump_sum_amount: '',
  main_bank: '',
  address: '',
  personal_info_agree: true,
})

const originalProfileForm = ref(null)
const profileOptions = ref({
  age: [],
  gender: [
    { value: 'unknown', label: '선택 안 함' },
    { value: 'male', label: '남성' },
    { value: 'female', label: '여성' },
  ],
  monthly_income_range: [],
  monthly_saving_amount: [],
  lump_sum_amount: [],
  main_bank: [],
  address: [],
})

const isEditingProfile = ref(false)
const activeAccountPanel = ref('')
const passwordPanelRef = ref(null)
const withdrawPanelRef = ref(null)
const profileMessage = ref('')
const profileSaving = ref(false)
const profileImageUrl = ref('')
const profileImageFile = ref(null)
const profileImagePreview = ref('')

const passwordForm = ref({
  current_password: '',
  new_password: '',
  new_password_confirm: '',
})

const passwordMessage = ref('')
const passwordSaving = ref(false)

const withdrawPassword = ref('')
const withdrawMessage = ref('')
const withdrawSaving = ref(false)

const favoriteProducts = ref([])
const savedVideos = ref([])

const profileInitial = computed(() => {
  if (!profileUser.value.username) {
    return 'U'
  }

  return profileUser.value.username.slice(0, 1).toUpperCase()
})


const ageIconText = computed(() => {
  if (profileForm.value.age) {
    return String(profileForm.value.age)
  }

  return '나이'
})

const normalizedGender = computed(() => {
  return String(profileForm.value.gender || 'unknown').toLowerCase()
})

const genderLabel = computed(() => {
  return getOptionLabel('gender', profileForm.value.gender)
})

const genderIcon = computed(() => {
  if (['female', 'f', 'woman', '여성'].includes(normalizedGender.value)) {
    return '♀'
  }

  if (['male', 'm', 'man', '남성'].includes(normalizedGender.value)) {
    return '♂'
  }

  return '⚥'
})

const genderIconClass = computed(() => {
  if (['female', 'f', 'woman', '여성'].includes(normalizedGender.value)) {
    return 'gender-female'
  }

  if (['male', 'm', 'man', '남성'].includes(normalizedGender.value)) {
    return 'gender-male'
  }

  return 'gender-unknown'
})

const getProduct = (favorite) => {
  return favorite.product || favorite
}

const depositFavorites = computed(() => {
  return favoriteProducts.value.filter((favorite) => {
    const product = getProduct(favorite)
    return product.product_type === 'deposit'
  })
})

const savingFavorites = computed(() => {
  return favoriteProducts.value.filter((favorite) => {
    const product = getProduct(favorite)
    return product.product_type === 'saving'
  })
})

const formatRate = (rate) => {
  if (rate === null || rate === undefined || rate === '') {
    return '정보 없음'
  }

  return `${Number(rate).toFixed(2)}%`
}

const getProductId = (favorite) => {
  const product = getProduct(favorite)
  return product.id
}

const getProductType = (favorite) => {
  const product = getProduct(favorite)
  return product.product_type || 'deposit'
}

const getProductName = (favorite) => {
  const product = getProduct(favorite)
  return product.name || '상품명 없음'
}

const normalizeFinalBankDisplayName = (bankName) => {
  const displayName = getBankDisplayName(bankName)

  const finalNameMap = {
    KB국민은행: '국민은행',
    KEB하나은행: '하나은행',
  }

  return finalNameMap[displayName] || displayName
}

const getRawBankName = (favorite) => {
  const product = getProduct(favorite)
  return product.bank?.name || product.bank_name || product.kor_co_nm || product.fin_co_nm || ''
}

const getBankName = (favorite) => {
  return normalizeFinalBankDisplayName(getRawBankName(favorite)) || '은행명 없음'
}

const getFavoriteBankLogo = (favorite) => {
  return getBankLogo(getRawBankName(favorite) || getBankName(favorite))
}

const getMaxInterestRate = (favorite) => {
  const product = getProduct(favorite)

  if (
    product.max_interest_rate !== null &&
    product.max_interest_rate !== undefined &&
    product.max_interest_rate !== ''
  ) {
    return product.max_interest_rate
  }

  if (!product.options || product.options.length === 0) {
    return null
  }

  const rates = product.options
    .map((option) => {
      if (
        option.intr_rate2 !== null &&
        option.intr_rate2 !== undefined &&
        option.intr_rate2 !== ''
      ) {
        return Number(option.intr_rate2)
      }

      if (
        option.intr_rate !== null &&
        option.intr_rate !== undefined &&
        option.intr_rate !== ''
      ) {
        return Number(option.intr_rate)
      }

      return null
    })
    .filter((rate) => rate !== null && !Number.isNaN(rate))

  if (rates.length === 0) {
    return null
  }

  return Math.max(...rates)
}

const getOptionLabel = (optionKey, value) => {
  if (!value) {
    return '미입력'
  }

  const option = profileOptions.value[optionKey]?.find((item) => item.value === value)
  return option?.label || value
}

const setProfileForm = (profileData) => {
  const profile = profileData.profile || {}

  profileUser.value = {
    id: profileData.id,
    username: profileData.username,
    email: profileData.email,
  }

  profileForm.value = {
    email: profileData.email || '',
    age: profile.age,
    gender: profile.gender || 'unknown',
    monthly_income_range: profile.monthly_income_range || '',
    monthly_saving_amount: profile.monthly_saving_amount || '',
    lump_sum_amount: profile.lump_sum_amount || '',
    main_bank: profile.main_bank || '',
    address: profile.address || '',
    personal_info_agree: profile.personal_info_agree !== false,
  }

  profileImageUrl.value = profile.profile_image_url || ''
  originalProfileForm.value = { ...profileForm.value }
  clearProfileImageSelection()
}

const fetchProfileOptions = async () => {
  const response = await getProfileOptions()
  profileOptions.value = {
    ...response.data,
    gender: response.data.gender || [
      { value: 'unknown', label: '선택 안 함' },
      { value: 'male', label: '남성' },
      { value: 'female', label: '여성' },
    ],
  }
}

const fetchProfile = async () => {
  const response = await getProfile()
  setProfileForm(response.data)
}

const fetchFavoriteProducts = async () => {
  const response = await getFavoriteProducts()
  favoriteProducts.value = response.data
}

const fetchSavedVideos = async () => {
  const response = await getSavedVideos()
  savedVideos.value = response.data
}

const fetchMyPageData = async () => {
  pageLoading.value = true
  pageErrorMessage.value = ''

  try {
    await Promise.all([
      fetchProfileOptions(),
      fetchProfile(),
      fetchFavoriteProducts(),
      fetchSavedVideos(),
    ])
  } catch (error) {
    console.error(error)

    if (error.response?.status === 401) {
      pageErrorMessage.value = '로그인이 필요한 페이지입니다.'
      return
    }

    pageErrorMessage.value = '마이페이지 정보를 불러오지 못했습니다.'
  } finally {
    pageLoading.value = false
  }
}

const startEditProfile = () => {
  profileMessage.value = ''
  passwordMessage.value = ''
  withdrawMessage.value = ''
  activeAccountPanel.value = ''
  originalProfileForm.value = { ...profileForm.value }
  isEditingProfile.value = true
}

const cancelEditProfile = () => {
  if (originalProfileForm.value) {
    profileForm.value = { ...originalProfileForm.value }
  }

  profileMessage.value = ''
  isEditingProfile.value = false
  clearProfileImageSelection()
}

const openAccountPanel = async (panelName) => {
  isEditingProfile.value = false
  activeAccountPanel.value = panelName
  passwordMessage.value = ''
  withdrawMessage.value = ''

  if (panelName === 'password') {
    clearPasswordForm()
  }

  if (panelName === 'withdraw') {
    withdrawPassword.value = ''
  }

  await nextTick()

  const targetPanel =
    panelName === 'password' ? passwordPanelRef.value : withdrawPanelRef.value

  targetPanel?.scrollIntoView({
    behavior: 'smooth',
    block: 'center',
  })
}

const closeAccountPanel = () => {
  activeAccountPanel.value = ''
  passwordMessage.value = ''
  withdrawMessage.value = ''
  clearPasswordForm()
  withdrawPassword.value = ''
}

const clearProfileImageSelection = () => {
  profileImageFile.value = null

  if (profileImagePreview.value) {
    URL.revokeObjectURL(profileImagePreview.value)
  }

  profileImagePreview.value = ''
}

const handleProfileImageChange = (event) => {
  const file = event.target.files?.[0]

  clearProfileImageSelection()

  if (!file) {
    return
  }

  if (!file.type.startsWith('image/')) {
    profileMessage.value = '이미지 파일만 업로드할 수 있습니다.'
    event.target.value = ''
    return
  }

  profileImageFile.value = file
  profileImagePreview.value = URL.createObjectURL(file)
}

const buildProfileFormData = () => {
  const formData = new FormData()

  formData.append('email', profileForm.value.email || '')
  formData.append('age', profileForm.value.age || '')
  formData.append('gender', profileForm.value.gender || 'unknown')
  formData.append('monthly_income_range', profileForm.value.monthly_income_range || '')
  formData.append('monthly_saving_amount', profileForm.value.monthly_saving_amount || '')
  formData.append('lump_sum_amount', profileForm.value.lump_sum_amount || '')
  formData.append('main_bank', profileForm.value.main_bank || '')
  formData.append('address', profileForm.value.address || '')
  formData.append('personal_info_agree', 'true')

  if (profileImageFile.value) {
    formData.append('profile_image', profileImageFile.value)
  }

  return formData
}

const handleUpdateProfile = async () => {
  profileMessage.value = ''
  profileSaving.value = true

  try {
    const formData = buildProfileFormData()
    const response = await updateProfile(formData)

    setProfileForm(response.data.user)

    profileMessage.value = '프로필이 수정되었습니다.'
    isEditingProfile.value = false
  } catch (error) {
    console.error(error)

    profileMessage.value =
      error.response?.data?.message ||
      '프로필 수정에 실패했습니다.'
  } finally {
    profileSaving.value = false
  }
}

const clearPasswordForm = () => {
  passwordForm.value = {
    current_password: '',
    new_password: '',
    new_password_confirm: '',
  }
}

const handleChangePassword = async () => {
  passwordMessage.value = ''

  if (!passwordForm.value.current_password) {
    passwordMessage.value = '현재 비밀번호를 입력해주세요.'
    return
  }

  if (!passwordForm.value.new_password) {
    passwordMessage.value = '새 비밀번호를 입력해주세요.'
    return
  }

  if (!passwordForm.value.new_password_confirm) {
    passwordMessage.value = '새 비밀번호 확인을 입력해주세요.'
    return
  }

  if (passwordForm.value.new_password !== passwordForm.value.new_password_confirm) {
    passwordMessage.value = '새 비밀번호가 일치하지 않습니다.'
    return
  }

  passwordSaving.value = true

  try {
    const response = await changePassword({
      current_password: passwordForm.value.current_password,
      new_password: passwordForm.value.new_password,
      new_password_confirm: passwordForm.value.new_password_confirm,
    })

    alert(response.data.message)

    authStore.logoutUser()

    clearPasswordForm()
    router.push({ name: 'login' })
  } catch (error) {
    console.error(error)
    passwordMessage.value =
      error.response?.data?.message ||
      '비밀번호 변경에 실패했습니다.'
  } finally {
    passwordSaving.value = false
  }
}

const handleWithdraw = async () => {
  withdrawMessage.value = ''

  if (!withdrawPassword.value) {
    withdrawMessage.value = '비밀번호를 입력해주세요.'
    return
  }

  const confirmed = window.confirm(
    '정말 회원탈퇴하시겠습니까? 탈퇴 후 같은 계정으로 로그인할 수 없습니다.'
  )

  if (!confirmed) {
    return
  }

  withdrawSaving.value = true

  try {
    const response = await withdraw({
      password: withdrawPassword.value,
    })

    alert(response.data.message)

    authStore.logoutUser()

    router.push({ name: 'home' })
  } catch (error) {
    console.error(error)
    withdrawMessage.value =
      error.response?.data?.message ||
      '회원탈퇴에 실패했습니다.'
  } finally {
    withdrawSaving.value = false
    withdrawPassword.value = ''
  }
}

const handleRemoveFavorite = async (favorite) => {
  const productId = getProductId(favorite)

  try {
    await toggleFavoriteProduct(productId)

    favoriteProducts.value = favoriteProducts.value.filter((item) => {
      return getProductId(item) !== productId
    })
  } catch (error) {
    console.error(error)
  }
}

const handleDeleteVideo = async (videoId) => {
  try {
    await deleteSavedVideo(videoId)
    savedVideos.value = savedVideos.value.filter((video) => video.video_id !== videoId)
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  fetchMyPageData()
})

onBeforeUnmount(() => {
  clearProfileImageSelection()
})
</script>

<style scoped>
.mypage-view {
  width: min(var(--container-width, 1320px), calc(100% - 48px));
  min-height: 100vh;
  margin: 0 auto;
  padding: 34px 0 54px;
  background: transparent;
}

.page-header {
  margin-bottom: 22px;
}

.eyebrow {
  display: inline-flex;
  margin-bottom: 10px;
  color: var(--color-primary, #1116b8);
  font-size: 12px;
  font-weight: 950;
  letter-spacing: 0.12em;
}

.page-header h1 {
  margin: 0;
  color: var(--color-text, #07142f);
  font-size: clamp(34px, 4vw, 48px);
  line-height: 1.12;
  font-weight: 950;
  letter-spacing: -0.06em;
}

.page-header p {
  margin: 10px 0 0;
  color: var(--color-text-muted, #667085);
  font-size: 16px;
}

.card,
.profile-hero-card,
.profile-edit-panel,
.favorites-section,
.videos-section {
  border: 1px solid var(--color-border, #e0e6f2);
  border-radius: var(--radius-lg, 24px);
  background: rgba(255, 255, 255, 0.96);
  box-shadow: var(--shadow-soft, 0 10px 30px rgba(15, 27, 61, 0.07));
}

.status-message {
  padding: 22px;
  border: 1px solid var(--color-border, #e0e6f2);
  border-radius: var(--radius-md, 18px);
  background: #fff;
  color: var(--color-text-muted, #667085);
  font-weight: 800;
}

.status-message.error {
  border-color: #fecaca;
  background: #fff5f5;
  color: #dc2626;
}

.profile-hero-card {
  position: relative;
  padding: 28px;
  margin-bottom: 22px;
}

.profile-main-info {
  display: flex;
  gap: 28px;
  align-items: center;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--color-border, #e0e6f2);
}

.profile-image {
  display: grid;
  place-items: center;
  flex-shrink: 0;
  overflow: hidden;
  border-radius: 999px;
  background: linear-gradient(135deg, #eaf0ff, #dffaf5);
  color: var(--color-primary, #1116b8);
  font-weight: 950;
}

.profile-image.large {
  width: 116px;
  height: 116px;
  font-size: 44px;
  box-shadow: 0 18px 38px rgba(17, 22, 184, 0.12);
}

.profile-image.small {
  width: 72px;
  height: 72px;
  font-size: 28px;
}

.profile-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-title {
  min-width: 0;
}

.title-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.profile-title h2 {
  margin: 0;
  color: var(--color-text, #07142f);
  font-size: 34px;
  font-weight: 950;
  letter-spacing: -0.05em;
}

.profile-badge,
.count-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 28px;
  padding: 0 12px;
  border-radius: 999px;
  background: var(--color-primary-soft, #eef1ff);
  color: var(--color-primary, #1116b8);
  font-size: 12px;
  font-weight: 950;
}

.profile-title p {
  margin: 8px 0 0;
  color: var(--color-text-muted, #667085);
  font-size: 15px;
}

.profile-title small {
  display: block;
  margin-top: 8px;
  color: var(--color-text-light, #8a94a6);
  font-size: 13px;
}

.edit-profile-button {
  position: absolute;
  right: 28px;
  top: 28px;
  min-height: 44px;
  padding: 0 18px;
  border: 1px solid var(--color-border-strong, #c8d2e4);
  border-radius: 14px;
  background: #fff;
  color: var(--color-text, #07142f);
  font-weight: 950;
  cursor: pointer;
}

.profile-summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
  padding-top: 22px;
}

.summary-item {
  display: flex;
  gap: 12px;
  align-items: center;
  min-width: 0;
}

.summary-icon {
  display: grid;
  place-items: center;
  width: 42px;
  height: 42px;
  border-radius: 15px;
  font-size: 18px;
  font-weight: 950;
  line-height: 1;
}

.summary-icon.age {
  background: #f4efff;
  color: #6d28d9;
  font-size: 13px;
  letter-spacing: -0.04em;
}

.summary-icon.gender-male {
  background: #eaf0ff;
  color: #2454d6;
  font-size: 23px;
}

.summary-icon.gender-female {
  background: #fff1f7;
  color: #db2777;
  font-size: 23px;
}

.summary-icon.gender-unknown {
  background: #eef2ff;
  color: #64748b;
  font-size: 21px;
}

.summary-icon.income {
  background: #fff7e5;
  color: #b45309;
  font-size: 22px;
}

.summary-icon.saving {
  background: #f3e8ff;
  color: #7c3aed;
  font-size: 19px;
}

.summary-icon.lump-sum {
  background: #dffaf5;
  color: #0f766e;
  font-size: 19px;
}

.summary-icon.bank {
  background: #eef2ff;
  color: #4338ca;
  font-size: 19px;
}

.summary-icon.location {
  background: #e0f7fa;
  color: #0891b2;
  font-size: 13px;
  letter-spacing: -0.06em;
}

.summary-icon.consent {
  background: #ecfdf3;
  color: #16a34a;
  font-size: 20px;
}

.summary-item small {
  display: block;
  margin-bottom: 3px;
  color: var(--color-text-light, #8a94a6);
  font-size: 12px;
  font-weight: 850;
}

.summary-item strong {
  display: block;
  overflow: hidden;
  color: var(--color-text, #07142f);
  font-size: 15px;
  font-weight: 950;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-edit-panel {
  padding: 24px;
  margin-bottom: 22px;
}

.section-title-row {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 18px;
}

.section-title-row.compact {
  align-items: center;
}

.section-title-row h2 {
  margin: 0;
  color: var(--color-text, #07142f);
  font-size: 22px;
  font-weight: 950;
  letter-spacing: -0.04em;
}

.section-title-row p {
  margin: 6px 0 0;
  color: var(--color-text-muted, #667085);
  font-size: 14px;
}

.profile-edit-form {
  display: grid;
  grid-template-columns: 230px 1fr;
  gap: 20px;
  padding-bottom: 22px;
  border-bottom: 1px solid var(--color-border, #e0e6f2);
}

.image-edit-box {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 18px;
  border: 1px solid var(--color-border, #e0e6f2);
  border-radius: var(--radius-md, 18px);
  background: var(--color-surface-soft, #f7f9fc);
}

.edit-form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.profile-edit-form label,
.file-label,
.account-manage-form label {
  display: flex;
  flex-direction: column;
  gap: 7px;
  color: var(--color-text, #07142f);
  font-size: 14px;
  font-weight: 900;
}

.profile-edit-form input,
.profile-edit-form select,
.account-manage-form input {
  width: 100%;
  height: 44px;
  padding: 0 13px;
  border: 1px solid var(--color-border-strong, #c8d2e4);
  border-radius: 13px;
  background-color: #fff;
  color: var(--color-text, #07142f);
  font-size: 14px;
  box-sizing: border-box;
}

.profile-edit-form input:focus,
.profile-edit-form select:focus,
.account-manage-form input:focus {
  outline: none;
  border-color: var(--color-primary, #1116b8);
  box-shadow: 0 0 0 4px rgba(17, 22, 184, 0.08);
}

.file-label input {
  height: auto;
  padding: 9px;
}

.help-text {
  margin: 0;
  color: var(--color-text-light, #8a94a6);
  font-size: 12px;
  line-height: 1.5;
}

.form-message {
  grid-column: 1 / -1;
  margin: 0;
  color: #dc2626;
  font-size: 14px;
  font-weight: 800;
}

.form-message.success {
  color: #16a34a;
}

.form-actions {
  grid-column: 2;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.primary-button,
.secondary-button,
.delete-button,
.detail-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  padding: 0 16px;
  border-radius: 13px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 950;
  text-decoration: none;
  white-space: nowrap;
}

.primary-button {
  border: 1px solid var(--color-primary, #1116b8);
  background: var(--color-primary, #1116b8);
  color: #fff;
}

.secondary-button {
  border: 1px solid var(--color-border-strong, #c8d2e4);
  background: #fff;
  color: var(--color-text, #07142f);
}

.primary-button.full,
.delete-button.full {
  width: 100%;
}

.primary-button:disabled,
.delete-button:disabled,
.secondary-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.account-management-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  margin-top: 22px;
}

.account-manage-card {
  padding: 20px;
  border: 1px solid var(--color-border, #e0e6f2);
  border-radius: var(--radius-md, 18px);
  background: #fff;
}

.account-manage-card.danger {
  border-color: #fecaca;
  background: #fffafa;
}

.account-card-title {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.account-card-title > span {
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border-radius: 15px;
  background: var(--color-primary-soft, #eef1ff);
}

.account-card-title h2 {
  margin: 0;
  color: var(--color-text, #07142f);
  font-size: 18px;
  font-weight: 950;
}

.account-card-title p,
.danger-description {
  margin: 4px 0 0;
  color: var(--color-text-muted, #667085);
  font-size: 13px;
  line-height: 1.5;
}

.account-manage-form {
  display: grid;
  gap: 12px;
}

.delete-button {
  border: 1px solid #dc2626;
  background: #fff;
  color: #dc2626;
}

.content-grid {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
  gap: 18px;
}

.favorites-section,
.videos-section {
  padding: 22px;
}

.empty-message {
  padding: 18px;
  margin: 0;
  border: 1px dashed var(--color-border-strong, #c8d2e4);
  border-radius: var(--radius-md, 18px);
  background: var(--color-surface-soft, #f7f9fc);
  color: var(--color-text-muted, #667085);
  text-align: center;
  font-weight: 800;
}

.empty-message.compact {
  padding: 12px;
  font-size: 13px;
}

.favorite-group {
  margin-top: 20px;
}

.favorite-group:first-of-type {
  margin-top: 0;
}

.group-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.group-header h3 {
  margin: 0;
  color: var(--color-text, #07142f);
  font-size: 17px;
  font-weight: 950;
}

.group-header span {
  color: var(--color-text-light, #8a94a6);
  font-size: 13px;
  font-weight: 900;
}

.favorite-card {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  gap: 14px;
  align-items: center;
  padding: 14px;
  margin-bottom: 10px;
  border: 1px solid var(--color-border, #e0e6f2);
  border-radius: var(--radius-md, 18px);
  background: #fff;
}

.favorite-icon {
  display: grid;
  place-items: center;
  width: 54px;
  height: 54px;
  border-radius: 18px;
  font-size: 23px;
}

.favorite-icon.deposit { background: #dffaf5; }
.favorite-icon.saving { background: #eef1ff; }

.product-type-badge {
  display: inline-flex;
  align-items: center;
  min-height: 24px;
  padding: 0 8px;
  margin-bottom: 6px;
  border-radius: 999px;
  background: #dffaf5;
  color: #0f9f8b;
  font-size: 12px;
  font-weight: 950;
}

.product-type-badge.saving {
  background: #f3e8ff;
  color: #7c3aed;
}

.favorite-info {
  min-width: 0;
}

.favorite-info h4 {
  overflow: hidden;
  margin: 0 0 4px;
  color: var(--color-text, #07142f);
  font-size: 16px;
  font-weight: 950;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.favorite-info p {
  margin: 0;
  color: var(--color-text-muted, #667085);
  font-size: 13px;
}

.card-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.detail-link {
  border: 1px solid var(--color-primary, #1116b8);
  background: #fff;
  color: var(--color-primary, #1116b8);
}

.delete-button.icon {
  min-height: 38px;
  padding: 0 12px;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.video-card {
  overflow: hidden;
  border: 1px solid var(--color-border, #e0e6f2);
  border-radius: var(--radius-md, 18px);
  background: #fff;
}

.video-thumb-wrap {
  position: relative;
  display: block;
  background: var(--color-surface-soft, #f7f9fc);
}

.video-thumbnail {
  width: 100%;
  height: 136px;
  object-fit: cover;
  display: block;
}

.play-button {
  position: absolute;
  left: 50%;
  top: 50%;
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border-radius: 999px;
  background: rgba(7, 20, 47, 0.72);
  color: #fff;
  transform: translate(-50%, -50%);
}

.video-content {
  padding: 14px;
}

.video-content h3 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
  min-height: 42px;
  margin: 0 0 8px;
  color: var(--color-text, #07142f);
  font-size: 15px;
  line-height: 1.4;
  font-weight: 950;
}

.video-content p {
  margin: 0 0 14px;
  color: var(--color-text-muted, #667085);
  font-size: 13px;
}

.account-shortcuts {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  margin-top: 18px;
}

.account-shortcut-card {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 16px;
  align-items: center;
  padding: 20px;
  border: 1px solid var(--color-border, #e0e6f2);
  border-radius: var(--radius-lg, 24px);
  background: #fff;
  box-shadow: var(--shadow-soft, 0 10px 30px rgba(15, 27, 61, 0.07));
  color: inherit;
  text-align: left;
  cursor: pointer;
}

.account-shortcut-card > span {
  display: grid;
  place-items: center;
  width: 54px;
  height: 54px;
  border-radius: 18px;
  background: var(--color-primary-soft, #eef1ff);
  font-size: 24px;
}

.account-shortcut-card.danger > span {
  background: #fff1f2;
}

.account-shortcut-card strong {
  color: var(--color-text, #07142f);
  font-size: 17px;
  font-weight: 950;
}

.account-shortcut-card p {
  margin: 5px 0 0;
  color: var(--color-text-muted, #667085);
  font-size: 13px;
}

.account-shortcut-card em {
  color: var(--color-primary, #1116b8);
  font-size: 28px;
  font-style: normal;
}

@media (max-width: 1080px) {
  .profile-summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .content-grid,
  .account-management-grid,
  .account-shortcuts,
  .profile-edit-form {
    grid-template-columns: 1fr;
  }

  .form-actions {
    grid-column: 1;
  }
}

@media (max-width: 720px) {
  .mypage-view {
    width: min(100% - 28px, var(--container-width, 1320px));
    padding-top: 24px;
  }

  .profile-hero-card {
    padding: 22px;
  }

  .profile-main-info {
    flex-direction: column;
    align-items: flex-start;
  }

  .edit-profile-button {
    position: static;
    width: 100%;
    margin-top: 18px;
  }

  .profile-summary-grid,
  .edit-form-grid,
  .video-grid {
    grid-template-columns: 1fr;
  }

  .favorite-card {
    grid-template-columns: auto 1fr;
  }

  .favorite-card .card-actions {
    grid-column: 1 / -1;
  }

  .section-title-row,
  .form-actions,
  .card-actions {
    flex-direction: column;
    align-items: stretch;
  }
}

/* === 주연: 마이페이지 불필요 문구 제거 + 계정 관리 분리 === */
.page-header .eyebrow,
.page-header > p,
.profile-badge,
.profile-title small {
  display: none !important;
}

.page-header {
  margin-bottom: 22px !important;
}

.profile-title {
  justify-content: center;
}

.profile-title .title-row {
  margin-bottom: 8px;
}

.profile-title p {
  margin: 0;
}

.profile-edit-panel,
.account-action-panel {
  margin-bottom: 18px;
}

.profile-edit-panel .section-title-row p {
  display: none !important;
}

.account-action-panel {
  padding: 24px;
}

.account-action-panel.danger {
  border-color: #fecaca;
  background: linear-gradient(180deg, #fff, #fff7f7);
}

.account-action-panel .account-manage-form.single {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  align-items: end;
}

.account-action-panel.danger .account-manage-form.single {
  grid-template-columns: minmax(0, 1fr);
  max-width: 520px;
}

.account-action-panel .form-actions {
  grid-column: 1 / -1;
  justify-content: flex-end;
  margin-top: 2px;
}

.account-action-panel .form-actions .primary-button,
.account-action-panel .form-actions .delete-button,
.account-action-panel .form-actions .secondary-button {
  min-width: 140px;
}

@media (max-width: 900px) {
  .account-action-panel .account-manage-form.single {
    grid-template-columns: 1fr;
  }
}


/* === 주연: 마이페이지 버튼 유지/액션 위치/프로필 사진 정렬 보정 === */
.image-edit-box {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: flex-start !important;
  text-align: center !important;
}

.image-edit-box .profile-image.small {
  margin: 0 auto 16px !important;
}

.image-edit-box .file-label {
  width: 100% !important;
  text-align: left !important;
}

.image-edit-box .help-text {
  width: 100% !important;
  text-align: left !important;
}

.account-shortcuts {
  margin-top: 18px !important;
  margin-bottom: 16px !important;
}

.account-action-panel {
  margin-top: 0 !important;
  margin-bottom: 18px !important;
}

.account-shortcut-card {
  cursor: pointer;
}

.account-shortcut-card:hover {
  transform: translateY(-1px);
}


/* === 주연: 계정관리 세로형 폼 + 관심상품 은행 로고/은행명 적용 === */
.account-action-panel {
  max-width: 560px !important;
  padding: 24px !important;
}

.account-action-panel .section-title-row {
  margin-bottom: 18px !important;
}

.account-action-panel .account-manage-form.single {
  display: grid !important;
  grid-template-columns: 1fr !important;
  gap: 14px !important;
  max-width: 430px !important;
}

.account-action-panel .account-manage-form.single label {
  display: grid !important;
  gap: 8px !important;
  font-weight: 900 !important;
}

.account-action-panel .account-manage-form.single input {
  width: 100% !important;
  min-height: 44px !important;
}

.account-action-panel .form-actions {
  display: flex !important;
  justify-content: flex-start !important;
  gap: 10px !important;
  grid-column: auto !important;
  margin-top: 2px !important;
}

.account-action-panel .form-actions .primary-button,
.account-action-panel .form-actions .delete-button,
.account-action-panel .form-actions .secondary-button {
  min-width: 120px !important;
  width: auto !important;
}

.account-action-panel.danger {
  max-width: 560px !important;
}

.favorite-bank-logo {
  display: grid;
  place-items: center;
  width: 54px;
  height: 54px;
  flex: 0 0 54px;
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 10px 24px rgba(15, 27, 61, 0.05);
}

.favorite-bank-logo img {
  width: 72%;
  height: 72%;
  object-fit: contain;
}

.favorite-bank-logo em {
  color: var(--color-primary);
  font-style: normal;
  font-size: 18px;
  font-weight: 950;
}

.favorite-card {
  align-items: center !important;
}

.favorite-info p {
  word-break: keep-all;
}


/* === 주연: 계정관리 닫기 버튼 제거 + 회원탈퇴 우측 배치 === */
.account-action-panel .section-title-row.compact {
  justify-content: flex-start !important;
}

.account-action-panel.danger {
  margin-left: auto !important;
  margin-right: 0 !important;
}

.account-action-panel:not(.danger) {
  margin-left: 0 !important;
  margin-right: auto !important;
}

.account-action-panel.danger .account-manage-form.single {
  margin-left: auto !important;
  margin-right: 0 !important;
}

.account-action-panel .form-actions {
  justify-content: flex-start !important;
}

.account-action-panel.danger .form-actions {
  justify-content: flex-start !important;
}


/* === 주연: 회원탈퇴 내부 정렬 + 계정 패널 자동 스크롤 보정 === */
.account-action-panel {
  scroll-margin-top: calc(var(--header-height, 64px) + 24px);
}

.account-action-panel.danger {
  margin-left: auto !important;
  margin-right: 0 !important;
  text-align: left !important;
}

.account-action-panel.danger .section-title-row.compact,
.account-action-panel .section-title-row.compact {
  display: flex !important;
  justify-content: flex-start !important;
  align-items: flex-start !important;
  text-align: left !important;
}

.account-action-panel.danger .account-manage-form.single,
.account-action-panel .account-manage-form.single {
  width: 100% !important;
  max-width: 430px !important;
  margin-left: 0 !important;
  margin-right: auto !important;
}

.account-action-panel.danger .account-manage-form.single label,
.account-action-panel .account-manage-form.single label {
  align-items: stretch !important;
  text-align: left !important;
}

.account-action-panel.danger .form-actions,
.account-action-panel .form-actions {
  display: flex !important;
  justify-content: flex-start !important;
  align-items: center !important;
  gap: 10px !important;
}

.account-action-panel.danger .form-actions .delete-button,
.account-action-panel .form-actions .primary-button,
.account-action-panel .form-actions .secondary-button {
  height: 42px !important;
  min-width: 118px !important;
  padding: 0 18px !important;
  border-radius: 12px !important;
}

.account-action-panel.danger .section-title-row p {
  max-width: 420px !important;
  margin-top: 6px !important;
  line-height: 1.55 !important;
}


/* === 주연: 관심상품 카드 예/적금 배지와 로고/텍스트 높이 정렬 === */
.favorite-card {
  display: grid !important;
  grid-template-columns: 58px minmax(0, 1fr) auto !important;
  gap: 14px !important;
  align-items: center !important;
  padding: 16px 14px !important;
}

.favorite-bank-logo {
  grid-column: 1 !important;
  grid-row: 1 !important;
  align-self: center !important;
  width: 54px !important;
  height: 54px !important;
}

.favorite-info {
  display: grid !important;
  grid-template-columns: auto minmax(0, 1fr) !important;
  grid-template-areas:
    "badge title"
    ". bank";
  column-gap: 10px !important;
  row-gap: 4px !important;
  align-items: center !important;
  min-width: 0 !important;
}

.favorite-info .product-type-badge {
  grid-area: badge !important;
  align-self: center !important;
  justify-self: start !important;
  margin: 0 !important;
  transform: translateY(-1px);
}

.favorite-info h4 {
  grid-area: title !important;
  margin: 0 !important;
  min-width: 0 !important;
  color: var(--color-text) !important;
  font-size: 16px !important;
  line-height: 1.25 !important;
  font-weight: 950 !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

.favorite-info p {
  grid-area: bank !important;
  margin: 0 !important;
  color: var(--color-text-muted) !important;
  font-size: 12px !important;
  line-height: 1.35 !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

.favorite-card .card-actions {
  grid-column: 3 !important;
  grid-row: 1 !important;
  align-self: center !important;
  display: flex !important;
  gap: 8px !important;
  margin-left: 8px !important;
}

@media (max-width: 720px) {
  .favorite-card {
    grid-template-columns: 54px minmax(0, 1fr) !important;
  }

  .favorite-card .card-actions {
    grid-column: 1 / -1 !important;
    grid-row: auto !important;
    margin-left: 0 !important;
    justify-content: flex-end !important;
  }

  .favorite-info {
    grid-template-columns: 1fr !important;
    grid-template-areas:
      "badge"
      "title"
      "bank";
  }
}


/* === 주연: 관심상품 예금/적금 배지와 은행 로고 위치 교체 === */
.favorite-card {
  display: grid !important;
  grid-template-columns: 50px 58px minmax(0, 1fr) auto !important;
  gap: 12px !important;
  align-items: center !important;
  padding: 16px 14px !important;
}

.favorite-card .favorite-bank-logo {
  grid-column: 2 !important;
  grid-row: 1 / span 2 !important;
  align-self: center !important;
  justify-self: center !important;
  width: 54px !important;
  height: 54px !important;
}

.favorite-card .favorite-info {
  display: contents !important;
}

.favorite-card .favorite-info .product-type-badge {
  grid-column: 1 !important;
  grid-row: 1 / span 2 !important;
  align-self: center !important;
  justify-self: center !important;
  margin: 0 !important;
  transform: none !important;
}

.favorite-card .favorite-info h4 {
  grid-column: 3 !important;
  grid-row: 1 !important;
  align-self: end !important;
  margin: 0 0 2px !important;
  min-width: 0 !important;
  color: var(--color-text) !important;
  font-size: 16px !important;
  line-height: 1.25 !important;
  font-weight: 950 !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

.favorite-card .favorite-info p {
  grid-column: 3 !important;
  grid-row: 2 !important;
  align-self: start !important;
  margin: 2px 0 0 !important;
  min-width: 0 !important;
  color: var(--color-text-muted) !important;
  font-size: 12px !important;
  line-height: 1.35 !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

.favorite-card .card-actions {
  grid-column: 4 !important;
  grid-row: 1 / span 2 !important;
  align-self: center !important;
  display: flex !important;
  gap: 8px !important;
  margin-left: 8px !important;
}

@media (max-width: 720px) {
  .favorite-card {
    grid-template-columns: 46px 54px minmax(0, 1fr) !important;
  }

  .favorite-card .card-actions {
    grid-column: 1 / -1 !important;
    grid-row: 3 !important;
    margin-left: 0 !important;
    justify-content: flex-end !important;
  }
}


/* === 주연: 마이페이지 관심상품/영상 영역 폭 조정 === */
.content-grid {
  display: grid !important;
  grid-template-columns: minmax(620px, 1.35fr) minmax(360px, 0.85fr) !important;
  gap: 20px !important;
  align-items: stretch !important;
}

.favorites-section {
  min-width: 0 !important;
}

.videos-section {
  min-width: 0 !important;
}

.favorite-card {
  grid-template-columns: 50px 58px minmax(220px, 1fr) auto !important;
}

.favorite-card .favorite-info h4 {
  max-width: none !important;
}

.account-shortcuts {
  display: grid !important;
  grid-template-columns: minmax(620px, 1.35fr) minmax(360px, 0.85fr) !important;
  gap: 20px !important;
  align-items: stretch !important;
}

.account-shortcut-card {
  width: 100% !important;
}

@media (max-width: 1180px) {
  .content-grid,
  .account-shortcuts {
    grid-template-columns: 1fr !important;
  }

  .favorite-card {
    grid-template-columns: 50px 58px minmax(0, 1fr) auto !important;
  }
}

@media (max-width: 720px) {
  .favorite-card {
    grid-template-columns: 46px 54px minmax(0, 1fr) !important;
  }
}


/* === 주연: 마이페이지 관심상품 폭 재조정 === */
/* 직전 버전이 너무 길어져서 원래 비밀번호 변경 카드 폭 정도로 되돌림 */
.content-grid {
  display: grid !important;
  grid-template-columns: minmax(520px, 1fr) minmax(460px, 1fr) !important;
  gap: 20px !important;
  align-items: stretch !important;
}

.account-shortcuts {
  display: grid !important;
  grid-template-columns: minmax(520px, 1fr) minmax(460px, 1fr) !important;
  gap: 20px !important;
  align-items: stretch !important;
}

.favorites-section,
.videos-section {
  min-width: 0 !important;
}

.favorite-card {
  grid-template-columns: 46px 54px minmax(0, 1fr) auto !important;
  gap: 10px !important;
}

.favorite-card .favorite-info h4 {
  max-width: 100% !important;
}

@media (max-width: 1180px) {
  .content-grid,
  .account-shortcuts {
    grid-template-columns: 1fr !important;
  }
}

@media (max-width: 720px) {
  .favorite-card {
    grid-template-columns: 44px 52px minmax(0, 1fr) !important;
  }
}

</style>
