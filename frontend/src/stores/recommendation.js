import { computed, reactive, ref } from 'vue'
import { defineStore } from 'pinia'

const STORAGE_KEY = 'productRecommendationState:pinia'

const defaultForm = {
  product_type: 'auto',
  preferred_term: '12',
  main_bank: '없음',
  bank_filter: 'all',
  condition_preference: 'unknown',
  join_preference: 'online',
}

const getRecommendationKey = (item) => {
  if (!item) {
    return null
  }

  return `${item.product_type}-${item.product_id}-${item.option_id || item.save_trm}`
}

export const useRecommendationStore = defineStore('recommendation', () => {
  const form = reactive({ ...defaultForm })
  const recommendations = ref([])
  const selectedRecommendationKey = ref(null)
  const profileUsed = ref(null)
  const hasSearched = ref(false)
  const successMessage = ref('')
  const noticeTone = ref('success')
  const restored = ref(false)

  const visibleRecommendations = computed(() => recommendations.value.slice(0, 3))

  const persist = () => {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        form: { ...form },
        recommendations: recommendations.value,
        selectedRecommendationKey: selectedRecommendationKey.value,
        profileUsed: profileUsed.value,
        hasSearched: hasSearched.value,
        successMessage: successMessage.value,
        noticeTone: noticeTone.value,
      })
    )
  }

  const restore = () => {
    if (restored.value) {
      return
    }

    const savedState = localStorage.getItem(STORAGE_KEY)

    if (!savedState) {
      restored.value = true
      return
    }

    try {
      const parsedState = JSON.parse(savedState)

      Object.assign(form, {
        ...defaultForm,
        ...(parsedState.form || {}),
      })

      recommendations.value = Array.isArray(parsedState.recommendations)
        ? parsedState.recommendations
        : []

      selectedRecommendationKey.value =
        parsedState.selectedRecommendationKey ||
        (recommendations.value[0] ? getRecommendationKey(recommendations.value[0]) : null)

      profileUsed.value = parsedState.profileUsed || null
      hasSearched.value = Boolean(parsedState.hasSearched)
      successMessage.value = parsedState.successMessage || ''
      noticeTone.value = parsedState.noticeTone || 'success'
    } catch (error) {
      console.error('추천 상태 복원 실패:', error)
      localStorage.removeItem(STORAGE_KEY)
    } finally {
      restored.value = true
    }
  }

  const setResults = ({ items = [], selectedKey = null, profile = null } = {}) => {
    recommendations.value = Array.isArray(items) ? items : []
    selectedRecommendationKey.value =
      selectedKey ||
      (recommendations.value[0] ? getRecommendationKey(recommendations.value[0]) : null)
    profileUsed.value = profile || profileUsed.value
    hasSearched.value = true
    persist()
  }

  const updateRecommendations = (updater) => {
    recommendations.value =
      typeof updater === 'function'
        ? updater(recommendations.value)
        : Array.isArray(updater)
          ? updater
          : recommendations.value

    persist()
  }

  const setSelectedRecommendationKey = (key) => {
    selectedRecommendationKey.value = key
    persist()
  }

  const setHasSearched = (value) => {
    hasSearched.value = Boolean(value)
    persist()
  }

  const setNotice = (message = '', tone = 'success') => {
    successMessage.value = message
    noticeTone.value = tone
    persist()
  }

  const clearResultsOnly = () => {
    recommendations.value = []
    selectedRecommendationKey.value = null
    hasSearched.value = false
    successMessage.value = ''
    noticeTone.value = 'success'
    persist()
  }

  const reset = () => {
    Object.assign(form, { ...defaultForm })
    recommendations.value = []
    selectedRecommendationKey.value = null
    profileUsed.value = null
    hasSearched.value = false
    successMessage.value = ''
    noticeTone.value = 'success'
    restored.value = true
    localStorage.removeItem(STORAGE_KEY)
  }

  return {
    form,
    recommendations,
    selectedRecommendationKey,
    profileUsed,
    hasSearched,
    successMessage,
    noticeTone,
    visibleRecommendations,
    defaultForm,
    restore,
    persist,
    setResults,
    updateRecommendations,
    setSelectedRecommendationKey,
    setHasSearched,
    setNotice,
    clearResultsOnly,
    reset,
  }
})
