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