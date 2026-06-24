<template>
  <div class="mypage-view">
    <section class="page-header">
      <h1>마이페이지</h1>
      <p>내 금융 프로필, 관심상품, 저장한 유튜브 영상을 확인할 수 있습니다.</p>
    </section>

    <p v-if="pageLoading" class="status-message">
      마이페이지 정보를 불러오는 중입니다...
    </p>

    <p v-else-if="pageErrorMessage" class="status-message error">
      {{ pageErrorMessage }}
    </p>

    <template v-else>
      <div class="mypage-top-layout">
        <section class="profile-section">
          <div class="profile-card">
            <div class="profile-image">
              <img
                v-if="profileImagePreview || profileImageUrl"
                :src="profileImagePreview || profileImageUrl"
                alt="프로필 이미지"
              />
              <span v-else>
                {{ profileInitial }}
              </span>
            </div>

            <div class="profile-title">
              <h2>{{ profileUser.username || '사용자' }}</h2>
              <p>{{ profileUser.email || '이메일 정보 없음' }}</p>
            </div>

            <div v-if="!isEditingProfile" class="profile-info-list">
              <div class="profile-info-row">
                <span>나이</span>
                <strong>{{ profileForm.age || '미입력' }}</strong>
              </div>

              <div class="profile-info-row">
                <span>월 소득 구간</span>
                <strong>{{ getOptionLabel('monthly_income_range', profileForm.monthly_income_range) }}</strong>
              </div>

              <div class="profile-info-row">
                <span>월 저축 가능 금액</span>
                <strong>{{ getOptionLabel('monthly_saving_amount', profileForm.monthly_saving_amount) }}</strong>
              </div>

              <div class="profile-info-row">
                <span>현재 보유 목돈</span>
                <strong>{{ getOptionLabel('lump_sum_amount', profileForm.lump_sum_amount) }}</strong>
              </div>

              <div class="profile-info-row">
                <span>주거래은행</span>
                <strong>{{ profileForm.main_bank || '미입력' }}</strong>
              </div>

              <div class="profile-info-row">
                <span>거주 지역</span>
                <strong>{{ profileForm.address || '미입력' }}</strong>
              </div>

              <div class="profile-info-row">
                <span>개인정보 동의</span>
                <strong>{{ profileForm.personal_info_agree ? '동의' : '미동의' }}</strong>
              </div>

              <p v-if="profileMessage" class="form-message success">
                {{ profileMessage }}
              </p>

              <button type="button" class="primary-button full" @click="startEditProfile">
                프로필 수정 / 계정 관리
              </button>
            </div>

            <form v-else class="profile-edit-form" @submit.prevent="handleUpdateProfile">
              <div class="image-edit-box">
                <div class="profile-image small">
                  <img
                    v-if="profileImagePreview || profileImageUrl"
                    :src="profileImagePreview || profileImageUrl"
                    alt="프로필 이미지 미리보기"
                  />
                  <span v-else>
                    {{ profileInitial }}
                  </span>
                </div>

                <label class="file-label">
                  프로필 사진
                  <input
                    type="file"
                    accept="image/*"
                    @change="handleProfileImageChange"
                  />
                </label>

                <p class="help-text">
                  JPG, PNG 등 이미지 파일을 선택할 수 있습니다.
                </p>
              </div>

              <label>
                이메일
                <input v-model="profileForm.email" type="email" />
              </label>

              <label>
                나이
                <select v-model.number="profileForm.age">
                  <option :value="null">나이를 선택하세요</option>
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
                월 소득 구간
                <select v-model="profileForm.monthly_income_range">
                  <option value="">월 소득 구간을 선택하세요</option>
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
                  <option value="">월 저축 가능 금액을 선택하세요</option>
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
                  <option value="">현재 보유 목돈을 선택하세요</option>
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
                  <option value="">주거래은행을 선택하세요</option>
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
                  <option value="">거주 지역을 선택하세요</option>
                  <option
                    v-for="option in profileOptions.address"
                    :key="option.value"
                    :value="option.value"
                  >
                    {{ option.label }}
                  </option>
                </select>
              </label>

              <p v-if="profileMessage" class="form-message">
                {{ profileMessage }}
              </p>

              <div class="form-actions">
                <button type="submit" class="primary-button" :disabled="profileSaving">
                  {{ profileSaving ? '저장 중...' : '저장' }}
                </button>

                <button type="button" class="secondary-button" @click="cancelEditProfile">
                  취소
                </button>
              </div>
            </form>
          </div>

          <div v-if="isEditingProfile" class="account-manage-card">
            <h2>비밀번호 변경</h2>
            <p class="account-manage-description">
              보안을 위해 현재 비밀번호 확인 후 새 비밀번호로 변경합니다.
            </p>

            <form class="account-manage-form" @submit.prevent="handleChangePassword">
              <label>
                현재 비밀번호
                <input
                  v-model="passwordForm.current_password"
                  type="password"
                  autocomplete="current-password"
                >
              </label>

              <label>
                새 비밀번호
                <input
                  v-model="passwordForm.new_password"
                  type="password"
                  autocomplete="new-password"
                >
              </label>

              <label>
                새 비밀번호 확인
                <input
                  v-model="passwordForm.new_password_confirm"
                  type="password"
                  autocomplete="new-password"
                >
              </label>

              <p v-if="passwordMessage" class="form-message">
                {{ passwordMessage }}
              </p>

              <button type="submit" class="primary-button full" :disabled="passwordSaving">
                {{ passwordSaving ? '변경 중...' : '비밀번호 변경' }}
              </button>
            </form>
          </div>

          <div v-if="isEditingProfile" class="account-manage-card danger">
            <h2>회원탈퇴</h2>
            <p class="danger-description">
              탈퇴하면 계정이 비활성화되어 다시 로그인할 수 없습니다.
            </p>

            <form class="account-manage-form" @submit.prevent="handleWithdraw">
              <label>
                비밀번호 확인
                <input
                  v-model="withdrawPassword"
                  type="password"
                  autocomplete="current-password"
                >
              </label>

              <p v-if="withdrawMessage" class="form-message">
                {{ withdrawMessage }}
              </p>

              <button type="submit" class="delete-button full" :disabled="withdrawSaving">
                {{ withdrawSaving ? '탈퇴 처리 중...' : '회원탈퇴' }}
              </button>
            </form>
          </div>
        </section>

        <section class="favorites-section">
          <div class="section-title-row">
            <div>
              <h2>관심상품 목록</h2>
              <p>저장한 예금과 적금 상품입니다.</p>
            </div>
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

              <p v-if="depositFavorites.length === 0" class="empty-message">
                등록된 관심 정기예금이 없습니다.
              </p>

              <div
                v-for="favorite in depositFavorites"
                :key="favorite.id"
                class="favorite-card"
              >
                <div>
                  <span class="product-type-badge">정기예금</span>
                  <h4>{{ getProductName(favorite) }}</h4>
                  <p>은행명: {{ getBankName(favorite) }}</p>
                  <p>최고 금리: {{ formatRate(getMaxInterestRate(favorite)) }}</p>
                </div>

                <div class="card-actions">
                  <RouterLink
                    class="detail-link"
                    :to="{
                      name: 'product-detail',
                      params: { id: getProductId(favorite) },
                      query: { type: getProductType(favorite) }
                    }"
                  >
                    상세 보기
                  </RouterLink>

                  <button
                    type="button"
                    class="delete-button"
                    @click="handleRemoveFavorite(favorite)"
                  >
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

              <p v-if="savingFavorites.length === 0" class="empty-message">
                등록된 관심 적금이 없습니다.
              </p>

              <div
                v-for="favorite in savingFavorites"
                :key="favorite.id"
                class="favorite-card"
              >
                <div>
                  <span class="product-type-badge saving">적금</span>
                  <h4>{{ getProductName(favorite) }}</h4>
                  <p>은행명: {{ getBankName(favorite) }}</p>
                  <p>최고 금리: {{ formatRate(getMaxInterestRate(favorite)) }}</p>
                </div>

                <div class="card-actions">
                  <RouterLink
                    class="detail-link"
                    :to="{
                      name: 'product-detail',
                      params: { id: getProductId(favorite) },
                      query: { type: getProductType(favorite) }
                    }"
                  >
                    상세 보기
                  </RouterLink>

                  <button
                    type="button"
                    class="delete-button"
                    @click="handleRemoveFavorite(favorite)"
                  >
                    삭제
                  </button>
                </div>
              </div>
            </section>
          </template>
        </section>
      </div>

      <section class="videos-section">
        <div class="section-title-row">
          <div>
            <h2>저장한 유튜브 영상</h2>
            <p>추천 정보와 금융 지식을 다시 볼 수 있습니다.</p>
          </div>
        </div>

        <p v-if="savedVideos.length === 0" class="empty-message">
          저장한 유튜브 영상이 없습니다.
        </p>

        <div v-else class="video-grid">
          <article
            v-for="video in savedVideos"
            :key="video.id"
            class="video-card"
          >
            <img
              v-if="video.thumbnail_url"
              :src="video.thumbnail_url"
              :alt="video.title"
              class="video-thumbnail"
            />

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

                <button
                  type="button"
                  class="delete-button"
                  @click="handleDeleteVideo(video.video_id)"
                >
                  삭제
                </button>
              </div>
            </div>
          </article>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  getProfile,
  getProfileOptions,
  updateProfile,
  changePassword,
  withdraw,
} from '@/api/accounts'
import { getFavoriteProducts, toggleFavoriteProduct } from '@/api/favorites'
import { getSavedVideos, deleteSavedVideo } from '@/api/videos'

const router = useRouter()
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
  monthly_income_range: [],
  monthly_saving_amount: [],
  lump_sum_amount: [],
  main_bank: [],
  address: [],
})

const isEditingProfile = ref(false)
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

const getBankName = (favorite) => {
  const product = getProduct(favorite)
  return product.bank?.name || product.bank_name || product.kor_co_nm || '은행명 없음'
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
  profileOptions.value = response.data
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

    localStorage.removeItem('token')
    window.dispatchEvent(new Event('login-success'))

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

    localStorage.removeItem('token')
    window.dispatchEvent(new Event('login-success'))

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
  min-height: 100vh;
  padding: 28px;
  background-color: #f6f7f9;
}

.page-header {
  padding-bottom: 18px;
  margin-bottom: 18px;
  border-bottom: 1px solid #ddd;
}

.page-header h1 {
  margin: 0;
  font-size: 26px;
  color: #111;
}

.page-header p {
  margin: 8px 0 0;
  color: #666;
}

.status-message {
  padding: 18px;
  background-color: #fafafa;
  border: 1px solid #eee;
  color: #555;
}

.status-message.error {
  color: #c0392b;
}

.mypage-top-layout {
  display: grid;
  grid-template-columns: 340px 1fr;
  gap: 20px;
  align-items: flex-start;
}

.profile-section {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.profile-card,
.favorites-section,
.videos-section {
  padding: 22px;
  background-color: #fff;
  border: 1px solid #ddd;
}

.profile-card {
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.profile-image {
  width: 88px;
  height: 88px;
  margin: 0 auto 14px;
  border-radius: 50%;
  background-color: #222;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 800;
  overflow: hidden;
}

.profile-image.small {
  width: 72px;
  height: 72px;
  margin: 0;
  font-size: 26px;
}

.profile-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-image span {
  display: flex;
  align-items: center;
  justify-content: center;
}

.profile-title {
  text-align: center;
  margin-bottom: 18px;
}

.profile-title h2 {
  margin: 0;
  font-size: 22px;
}

.profile-title p {
  margin: 6px 0 0;
  color: #666;
  font-size: 14px;
}

.profile-info-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.profile-info-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.profile-info-row span {
  color: #666;
  font-size: 14px;
}

.profile-info-row strong {
  color: #111;
  font-size: 14px;
  text-align: right;
}

.profile-edit-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.image-edit-box {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 14px;
  border: 1px solid #eee;
  background-color: #fafafa;
}

.profile-edit-form label,
.file-label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: #333;
  font-size: 14px;
  font-weight: 700;
}

.profile-edit-form input,
.profile-edit-form select {
  height: 40px;
  padding: 0 10px;
  border: 1px solid #ccc;
  background-color: #fff;
  font-size: 14px;
}

.file-label input {
  height: auto;
  padding: 8px;
}

.help-text {
  margin: 0;
  color: #777;
  font-size: 12px;
}

.form-message {
  margin: 0;
  color: #c0392b;
  font-size: 14px;
}

.form-message.success {
  color: #16a34a;
}

.form-actions {
  display: flex;
  gap: 8px;
}

.primary-button,
.secondary-button,
.delete-button,
.detail-link {
  cursor: pointer;
  font-weight: 800;
  text-decoration: none;
}

.primary-button {
  padding: 10px 13px;
  border: 1px solid #222;
  background-color: #222;
  color: #fff;
}

.primary-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.primary-button.full {
  width: 100%;
  margin-top: 14px;
}

.secondary-button {
  padding: 10px 13px;
  border: 1px solid #aaa;
  background-color: #fff;
  color: #333;
}

.section-title-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 18px;
}

.section-title-row h2 {
  margin: 0;
  font-size: 20px;
}

.section-title-row p {
  margin: 6px 0 0;
  color: #666;
  font-size: 14px;
}

.empty-message {
  padding: 14px;
  margin: 0;
  background-color: #fafafa;
  border: 1px solid #eee;
  color: #777;
}

.favorite-group {
  margin-top: 24px;
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
  font-size: 18px;
}

.group-header span {
  color: #777;
  font-size: 14px;
}

.favorite-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  padding: 16px;
  margin-bottom: 12px;
  border: 1px solid #ddd;
  background-color: #fff;
}

.product-type-badge {
  display: inline-block;
  padding: 4px 9px;
  margin-bottom: 8px;
  border-radius: 999px;
  background-color: #333;
  color: #fff;
  font-size: 12px;
  font-weight: 800;
}

.product-type-badge.saving {
  background-color: #555;
}

.favorite-card h4 {
  margin: 0 0 8px;
  font-size: 17px;
  color: #111;
}

.favorite-card p {
  margin: 4px 0;
  color: #555;
  font-size: 14px;
}

.card-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.detail-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 9px 12px;
  border: 1px solid #333;
  color: #222;
  background-color: #fff;
}

.delete-button {
  padding: 9px 12px;
  border: 1px solid #c0392b;
  background-color: #fff;
  color: #c0392b;
}

.delete-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.videos-section {
  margin-top: 20px;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.video-card {
  border: 1px solid #ddd;
  background-color: #fff;
  overflow: hidden;
}

.video-thumbnail {
  width: 100%;
  height: 160px;
  object-fit: cover;
  display: block;
  background-color: #eee;
}

.video-content {
  padding: 14px;
}

.video-content h3 {
  margin: 0 0 8px;
  font-size: 16px;
  line-height: 1.35;
}

.video-content p {
  margin: 0 0 14px;
  color: #666;
  font-size: 14px;
}

.account-manage-card {
  padding: 18px;
  border: 1px solid #ddd;
  background-color: #fff;
}

.account-manage-card h2 {
  margin: 0 0 8px;
  font-size: 18px;
  color: #111;
}

.account-manage-card.danger {
  border-color: #f0caca;
  background-color: #fffafa;
}

.account-manage-description {
  margin: 0 0 14px;
  color: #666;
  font-size: 13px;
  line-height: 1.5;
}

.account-manage-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.account-manage-form label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: #333;
  font-size: 14px;
  font-weight: 700;
}

.account-manage-form input {
  height: 40px;
  padding: 0 10px;
  border: 1px solid #ccc;
  background-color: #fff;
  font-size: 14px;
}

.danger-description {
  margin: 0 0 14px;
  color: #c0392b;
  font-size: 13px;
  line-height: 1.5;
}

.delete-button.full {
  width: 100%;
}

@media (max-width: 960px) {
  .mypage-top-layout {
    grid-template-columns: 1fr;
  }

  .video-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .mypage-view {
    padding: 18px;
  }

  .favorite-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .card-actions {
    width: 100%;
  }

  .detail-link,
  .delete-button {
    flex: 1;
  }

  .video-grid {
    grid-template-columns: 1fr;
  }
}
</style>
