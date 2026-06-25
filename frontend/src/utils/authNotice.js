export const AUTH_NOTICE_EVENT = 'juyeon-auth-notice'
export const DEFAULT_AUTH_NOTICE_MESSAGE = '로그인 후 이용할 수 있습니다.'

const PENDING_AUTH_NOTICE_KEY = 'juyeon:pending-auth-notice'

export const showAuthNotice = (message = DEFAULT_AUTH_NOTICE_MESSAGE) => {
  const detail = {
    message: message || DEFAULT_AUTH_NOTICE_MESSAGE,
    createdAt: Date.now(),
  }

  try {
    window.sessionStorage.setItem(PENDING_AUTH_NOTICE_KEY, JSON.stringify(detail))
  } catch (error) {
    // sessionStorage를 사용할 수 없는 환경에서는 이벤트만 사용합니다.
  }

  window.dispatchEvent(new CustomEvent(AUTH_NOTICE_EVENT, { detail }))
}

export const consumePendingAuthNotice = () => {
  try {
    const rawValue = window.sessionStorage.getItem(PENDING_AUTH_NOTICE_KEY)
    window.sessionStorage.removeItem(PENDING_AUTH_NOTICE_KEY)

    if (!rawValue) {
      return null
    }

    const parsed = JSON.parse(rawValue)

    if (!parsed?.createdAt || Date.now() - parsed.createdAt > 5000) {
      return null
    }

    return parsed
  } catch (error) {
    return null
  }
}
