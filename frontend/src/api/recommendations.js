import api from '@/api/api'

export const recommendProducts = (payload) => {
  return api.post('/recommendations/products/', payload)
}