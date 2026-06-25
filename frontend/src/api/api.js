// src/api/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

const PUBLIC_ENDPOINT_PREFIXES = [
  '/accounts/login/',
  '/accounts/signup/',
  '/accounts/check-username/',
  '/accounts/check-email/',
  '/accounts/find-username/',
  '/accounts/reset-password/',
  '/accounts/profile/options/',
  '/products/',
  '/exchanges/',
  '/assets/',
  '/community/',
  '/maps/',
  '/videos/search/',
]

const isPublicRequest = (config) => {
  const method = String(config.method || 'get').toLowerCase()
  const url = String(config.url || '')

  if (!['get', 'head', 'options'].includes(method)) {
    return PUBLIC_ENDPOINT_PREFIXES.some((prefix) => url.startsWith(prefix) && prefix.startsWith('/accounts/'))
  }

  return PUBLIC_ENDPOINT_PREFIXES.some((prefix) => url.startsWith(prefix))
}

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')

  if (token && !isPublicRequest(config)) {
    config.headers.Authorization = `Token ${token}`
  }

  if (isPublicRequest(config) && config.headers?.Authorization) {
    delete config.headers.Authorization
  }

  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const requestUrl = String(error.config?.url || '')
      const isAuthCheckRequest = requestUrl.startsWith('/accounts/profile/')

      if (isAuthCheckRequest) {
        localStorage.removeItem('token')
        window.dispatchEvent(new Event('logout-success'))
      }
    }

    return Promise.reject(error)
  }
)

export default api
