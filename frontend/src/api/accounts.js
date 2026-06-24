import api from './api'

// 회원가입
export const signup = (signupData) => {
  return api.post('/accounts/signup/', signupData)
}

// 로그인
export const login = (loginData) => {
  return api.post('/accounts/login/', loginData)
}

// 프로필 조회
export const getProfile = () => {
  return api.get('/accounts/profile/')
}

// 프로필 수정
export const updateProfile = (profileData) => {
  if (profileData instanceof FormData) {
    return api.patch('/accounts/profile/update/', profileData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  }

  return api.patch('/accounts/profile/update/', profileData)
}

// 프로필 선택지 조회
export const getProfileOptions = () => {
  return api.get('/accounts/profile/options/')
}