<template>
  <header class="navbar">
    <div class="nav-inner">
      <RouterLink :to="{ name: 'home' }" class="logo" aria-label="주연 홈" @click="closeMenu">
        <span class="logo-mark">주</span>
        <span class="logo-text">주연</span>
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
          @click="closeMenu"
        >
          {{ link.label }}
        </RouterLink>
      </nav>

      <div class="nav-actions" :class="{ open: isMenuOpen }">
        <template v-if="isLoggedIn">
          <RouterLink :to="{ name: 'mypage' }" class="mypage-btn" @click="closeMenu">
            내 정보
          </RouterLink>
          <button type="button" class="login-btn" @click="handleLogout">
            로그아웃
          </button>
        </template>

        <template v-else>
          <RouterLink :to="{ name: 'login' }" class="login-btn" @click="closeMenu">
            로그인
          </RouterLink>
          <RouterLink :to="{ name: 'signup' }" class="signup-btn" @click="closeMenu">
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

const router = useRouter()
const isMenuOpen = ref(false)
const isLoggedIn = ref(!!localStorage.getItem('token'))

const navLinks = [
  { name: 'products', label: '예적금' },
  { name: 'recommend', label: '맞춤추천' },
  { name: 'main-bank', label: '주거래은행' },
  { name: 'exchange', label: '환율' },
  { name: 'community', label: '커뮤니티' },
]

const closeMenu = () => {
  isMenuOpen.value = false
}

const checkLoginStatus = () => {
  isLoggedIn.value = !!localStorage.getItem('token')
}

const handleLogout = () => {
  localStorage.removeItem('token')
  isLoggedIn.value = false
  closeMenu()
  alert('로그아웃되었습니다.')
  router.push({ name: 'home' })
}

onMounted(() => {
  checkLoginStatus()
  window.addEventListener('storage', checkLoginStatus)
  window.addEventListener('login-success', checkLoginStatus)
})

onBeforeUnmount(() => {
  window.removeEventListener('storage', checkLoginStatus)
  window.removeEventListener('login-success', checkLoginStatus)
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
  gap: 9px;
  color: var(--color-text);
  font-size: 22px;
  font-weight: 950;
  letter-spacing: -0.05em;
}

.logo-mark {
  width: 34px;
  height: 34px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  color: #fff;
  font-size: 18px;
  font-weight: 950;
  letter-spacing: -0.04em;
  box-shadow: 0 10px 20px rgba(31, 79, 216, 0.18);
}

.logo-text {
  font-weight: 950;
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

.login-btn,
.signup-btn,
.mypage-btn {
  min-height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  font-weight: 850;
  white-space: nowrap;
}

.login-btn,
.mypage-btn {
  padding: 0 15px;
  border: 1px solid var(--color-border-strong);
  background: #fff;
  color: var(--color-text);
}

.signup-btn {
  padding: 0 16px;
  border: 1px solid var(--color-primary);
  background: var(--color-primary);
  color: #fff;
  box-shadow: 0 10px 20px rgba(31, 79, 216, 0.18);
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
}
</style>
