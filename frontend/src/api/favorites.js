import api from './api'

export const getFavorites = () => {
  return api.get('/favorites/')
}

export const getFavoriteProducts = () => {
  return getFavorites()
}

export const addFavorite = (productId) => {
  return api.post(`/favorites/${productId}/`, {})
}

export const toggleFavoriteProduct = (productId) => {
  return api.post(`/favorites/${productId}/`, {})
}
