import api from '@/api/api'

// 예금 상품 저장
export const saveDepositProducts = () => {
  return api.get('/products/deposits/save/')
}

// 예금 상품 목록 조회
export const getDepositProducts = () => {
  return api.get('/products/deposits/')
}

// 예금 상품 상세 조회
export const getDepositProductDetail = (productId) => {
  return api.get(`/products/deposits/${productId}/`)
}

// 적금 상품 저장
export const saveSavingProducts = () => {
  return api.get('/products/savings/save/')
}

// 적금 상품 목록 조회
export const getSavingProducts = () => {
  return api.get('/products/savings/')
}

// 적금 상품 상세 조회
export const getSavingProductDetail = (productId) => {
  return api.get(`/products/savings/${productId}/`)
}

// 추가: 예금 + 적금 데이터를 DB에 저장
export const initializeProducts = async () => {
  const initialized = sessionStorage.getItem('productsInitialized')

  if (initialized === 'true') {
    return
  }

  await Promise.all([
    saveDepositProducts(),
    saveSavingProducts(),
  ])

  sessionStorage.setItem('productsInitialized', 'true')
}