<template>
  <header class="navbar">
    <div class="nav-inner">
      <RouterLink
        :to="{ name: 'home' }"
        class="logo"
        aria-label="주연 홈"
        @click="closeMenu"
      >
        <img :src="juyeonLogo" alt="주연" class="logo-image" />
      </RouterLink>

      <button
        type="button"
        class="mobile-toggle"
        :aria-expanded="isMenuOpen"
        aria-label="메뉴 열기"
        @click="isMenuOpen = !isMenuOpen"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      <nav class="nav-menu" :class="{ open: isMenuOpen }" aria-label="주요 메뉴">
        <RouterLink
          v-for="link in navLinks"
          :key="link.name"
          :to="{ name: link.name }"
          @click="handleNavClick($event, link)"
        >
          {{ link.label }}
        </RouterLink>
      </nav>

      <div class="nav-actions" :class="{ open: isMenuOpen }">
        <template v-if="isLoggedIn">
          <RouterLink
            :to="{ name: 'mypage' }"
            class="nav-action-btn nav-action-btn--primary"
            @click="closeMenu"
          >
            내 정보
          </RouterLink>

          <button type="button" class="nav-action-btn" @click="handleLogout">
            로그아웃
          </button>
        </template>

        <template v-else>
          <RouterLink
            :to="{ name: 'login' }"
            class="nav-action-btn"
            @click="closeMenu"
          >
            로그인
          </RouterLink>

          <RouterLink
            :to="{ name: 'signup' }"
            class="nav-action-btn nav-action-btn--primary"
            @click="closeMenu"
          >
            회원가입
          </RouterLink>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { logout } from '@/api/accounts'
import { showAuthNotice } from '@/utils/authNotice'
import juyeonLogo from '@/assets/branding/juyeon-logo.png'

const router = useRouter()

const isMenuOpen = ref(false)
const isLoggedIn = ref(!!localStorage.getItem('token'))

const navLinks = [
  { name: 'products', label: '예적금' },
  { name: 'main-bank', label: '주거래은행', requiresAuth: true },
  { name: 'recommend', label: '맞춤추천', requiresAuth: true },
  { name: 'exchange', label: '환율' },
  { name: 'spot-assets', label: '금·은 시세' },
  { name: 'community', label: '커뮤니티' },
]

const closeMenu = () => {
  isMenuOpen.value = false
}

const checkLoginStatus = () => {
  isLoggedIn.value = !!localStorage.getItem('token')
}

const handleNavClick = (event, link) => {
  if (link.requiresAuth && !isLoggedIn.value) {
    event.preventDefault()
    closeMenu()

    showAuthNotice('로그인 후 이용할 수 있습니다.')

    const redirectTarget = router.resolve({ name: link.name }).fullPath

    router.push({
      name: 'login',
      query: {
        redirect: redirectTarget,
      },
    })

    return
  }

  closeMenu()
}

const clearRecommendationStorage = () => {
  const removeKeys = []

  for (let i = 0; i < localStorage.length; i += 1) {
    const key = localStorage.key(i)

    if (
      key &&
      (
        key.startsWith('productRecommendationState:') ||
        key === 'productRecommendationState:last'
      )
    ) {
      removeKeys.push(key)
    }
  }

  removeKeys.forEach((key) => {
    localStorage.removeItem(key)
  })
}

const handleLogout = async () => {
  clearRecommendationStorage()

  try {
    if (localStorage.getItem('token')) {
      await logout()
    }
  } catch (error) {
    console.error('로그아웃 API 호출 실패:', error)
  } finally {
    localStorage.removeItem('token')
    isLoggedIn.value = false
    closeMenu()

    window.dispatchEvent(new Event('logout-success'))

    router.push({ name: 'login' })
  }
}

onMounted(() => {
  checkLoginStatus()

  window.addEventListener('storage', checkLoginStatus)
  window.addEventListener('login-success', checkLoginStatus)
  window.addEventListener('logout-success', checkLoginStatus)
})

onBeforeUnmount(() => {
  window.removeEventListener('storage', checkLoginStatus)
  window.removeEventListener('login-success', checkLoginStatus)
  window.removeEventListener('logout-success', checkLoginStatus)
})
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 50;
  height: var(--header-height);
  border-bottom: 1px solid rgba(227, 232, 242, 0.9);
  background: rgba(255, 255, 255, 0.86);
  backdrop-filter: blur(18px);
}

.nav-inner {
  position: relative;
  width: min(var(--container-width), calc(100% - 48px));
  height: 100%;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 28px;
}

.logo {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  height: 100%;
  padding: 0 4px;
  text-decoration: none;
}

.logo-image {
  display: block;
  width: auto;
  height: 42px;
  max-width: 132px;
  object-fit: contain;
  filter: drop-shadow(0 4px 8px rgba(9, 38, 91, 0.08));
}

.nav-menu {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(16px, 2.7vw, 34px);
}

.nav-menu a {
  position: relative;
  padding: 22px 0;
  color: var(--color-text-muted);
  font-size: 15px;
  font-weight: 800;
  text-decoration: none;
  white-space: nowrap;
  transition: color 0.16s ease;
}

.nav-menu a::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: 13px;
  height: 2px;
  border-radius: 999px;
  background: var(--color-primary);
  transform: scaleX(0);
  transform-origin: center;
  transition: transform 0.16s ease;
}

.nav-menu a.router-link-active,
.nav-menu a:hover {
  color: var(--color-primary);
}

.nav-menu a.router-link-active::after,
.nav-menu a:hover::after {
  transform: scaleX(1);
}

.nav-actions {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-action-btn {
  height: 42px;
  padding: 0 18px;
  border-radius: 14px;
  border: 1.5px solid #cfd9ea;
  background: #fff;
  color: #0f172a;
  font-family: inherit;
  font-size: 14px;
  font-weight: 800;
  line-height: 1;
  text-decoration: none;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition:
    transform 0.18s ease,
    background-color 0.18s ease,
    border-color 0.18s ease,
    color 0.18s ease,
    box-shadow 0.18s ease;
}

.nav-action-btn:hover {
  transform: translateY(-1px);
  background: #f8fbff;
  border-color: #b8c7e3;
}

.nav-action-btn--primary {
  background: #2454d6;
  color: #fff;
  border-color: #2454d6;
  box-shadow: 0 10px 22px rgba(36, 84, 214, 0.18);
}

.nav-action-btn--primary:hover {
  background: #1f49bb;
  border-color: #1f49bb;
  color: #fff;
  box-shadow: 0 12px 26px rgba(36, 84, 214, 0.24);
}

.mobile-toggle {
  display: none;
  margin-left: auto;
  width: 42px;
  height: 42px;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  background: #fff;
  color: var(--color-text);
  cursor: pointer;
}

.mobile-toggle span {
  display: block;
  width: 18px;
  height: 2px;
  margin: 4px auto;
  border-radius: 999px;
  background: currentColor;
}

@media (max-width: 980px) {
  .navbar {
    height: auto;
    min-height: var(--header-height);
  }

  .nav-inner {
    position: relative;
    min-height: var(--header-height);
    flex-wrap: wrap;
    width: min(100% - 28px, var(--container-width));
    gap: 0;
  }

  .mobile-toggle {
    display: inline-block;
  }

  .nav-menu,
  .nav-actions {
    display: none;
    width: 100%;
  }

  .nav-menu.open,
  .nav-actions.open {
    display: flex;
  }

  .nav-menu {
    flex-direction: column;
    align-items: stretch;
    gap: 0;
    padding: 10px 0;
  }

  .nav-menu a {
    padding: 12px 0;
  }

  .nav-menu a::after {
    display: none;
  }

  .nav-actions {
    padding: 0 0 16px;
    flex-wrap: wrap;
  }

  .nav-action-btn {
    flex: 1;
    min-width: 120px;
  }
}
</style>