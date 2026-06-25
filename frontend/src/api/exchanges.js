import api from '@/api/api'

export const getExchangeRates = (params = {}) => {
  return api.get('/exchanges/rates/', { params })
}

export const getExchangeHistory = (params = {}) => {
  return api.get('/exchanges/history/', { params })
}

export const calculateExchange = (payload) => {
  return api.post('/exchanges/calculate/', payload)
}
