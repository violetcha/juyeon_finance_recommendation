import api from './api'

// 회원가입
export const signup = (signupData) => {
  return api.post('/accounts/signup/', signupData)
}

// 로그인
export const login = (loginData) => {
  return api.post('/accounts/login/', loginData)
}

// 로그아웃
export const logout = () => {
  return api.post('/accounts/logout/')
}

// 아이디 찾기
export const findUsername = (findData) => {
  return api.post('/accounts/find-username/', findData)
}

// 비밀번호 재설정
export const resetPassword = (resetData) => {
  return api.post('/accounts/reset-password/', resetData)
}

// 비밀번호 변경
export const changePassword = (passwordData) => {
  return api.post('/accounts/password/change/', passwordData)
}

// 회원탈퇴
export const withdraw = (withdrawData) => {
  return api.delete('/accounts/withdraw/', {
    data: withdrawData,
  })
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
