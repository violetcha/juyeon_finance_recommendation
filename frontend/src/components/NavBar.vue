<template>
  <header class="navbar">
    <div class="nav-inner">
      <RouterLink :to="{ name: 'home' }" class="logo" aria-label="첫금융 홈">
        첫금융
      </RouterLink>

      <button
        type="button"
        class="mobile-toggle"
        :aria-expanded="isMenuOpen"
        aria-label="메뉴 열기"
        @click="isMenuOpen = !isMenuOpen"
      >
        ☰
      </button>

      <nav class="nav-menu" :class="{ open: isMenuOpen }" aria-label="주요 메뉴">
        <RouterLink :to="{ name: 'products' }" @click="closeMenu">
          예적금
        </RouterLink>
        <RouterLink :to="{ name: 'recommend' }" @click="closeMenu">
          맞춤추천
        </RouterLink>
        <RouterLink :to="{ name: 'main-bank' }" @click="closeMenu">
          주거래은행
        </RouterLink>
        <RouterLink :to="{ name: 'exchange' }" @click="closeMenu">
          환율
        </RouterLink>
        <RouterLink :to="{ name: 'community' }" @click="closeMenu">
          커뮤니티
        </RouterLink>
        <RouterLink :to="{ name: 'mypage' }" @click="closeMenu">
          마이페이지
        </RouterLink>
      </nav>

      <div class="nav-actions" :class="{ open: isMenuOpen }">
        <button type="button" class="search-btn" aria-label="검색">
          🔎
        </button>

        <template v-if="isLoggedIn">
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
  border-bottom: 1px solid rgba(229, 234, 243, 0.9);
  background: rgba(255, 255, 255, 0.86);
  backdrop-filter: blur(18px);
}

.nav-inner {
  width: min(var(--container-width), calc(100% - 48px));
  height: 100%;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 26px;
}

.logo {
  flex-shrink: 0;
  color: var(--color-primary);
  font-size: 30px;
  font-weight: 1000;
  letter-spacing: -0.08em;
}

.nav-menu {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(18px, 3vw, 42px);
}

.nav-menu a {
  position: relative;
  padding: 21px 0;
  color: var(--color-text);
  font-size: 15px;
  font-weight: 850;
  white-space: nowrap;
}

.nav-menu a::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: 0;
  width: 0;
  height: 3px;
  border-radius: 999px;
  background: var(--color-primary);
  transform: translateX(-50%);
  transition: width 0.18s ease;
}

.nav-menu a.router-link-active {
  color: var(--color-primary);
}

.nav-menu a.router-link-active::after,
.nav-menu a:hover::after {
  width: 100%;
}

.nav-actions {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-btn,
.login-btn,
.signup-btn {
  min-height: 42px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  font-weight: 900;
  white-space: nowrap;
}

.search-btn {
  width: 42px;
  border: 0;
  background: transparent;
  color: var(--color-text);
  font-size: 18px;
}

.login-btn {
  padding: 0 18px;
  border: 1px solid var(--color-border-strong);
  background: #fff;
  color: var(--color-text);
}

.signup-btn {
  padding: 0 18px;
  border: 1px solid var(--color-primary);
  background: var(--color-primary);
  color: #fff;
  box-shadow: 0 10px 22px rgba(17, 22, 184, 0.18);
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
  font-size: 19px;
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
    display: inline-flex;
    align-items: center;
    justify-content: center;
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
  }
}
</style>
