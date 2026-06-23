import api from '@/api/api'

export const saveDepositProducts = () => {
  return api.get('/products/deposits/save/')
}

export const getDepositProducts = () => {
  return api.get('/products/deposits/')
}

export const getDepositProductDetail = (productId) => {
  return api.get(`/products/deposits/${productId}/`)
}

// 추가: 적금 상품 저장
export const saveSavingProducts = () => {
  return api.get('/products/savings/save/')
}

// 추가: 적금 상품 목록 조회
export const getSavingProducts = () => {
  return api.get('/products/savings/')
}

// 추가: 적금 상품 상세 조회
export const getSavingProductDetail = (productId) => {
  return api.get(`/products/savings/${productId}/`)
}