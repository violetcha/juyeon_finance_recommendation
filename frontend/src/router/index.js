import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import ProductListView from '@/views/ProductListView.vue'
import ProductDetailView from '@/views/ProductDetailView.vue'
import RecommendView from '@/views/RecommendView.vue'
import ExchangeView from '@/views/ExchangeView.vue'
import SpotAssetView from '@/views/SpotAssetView.vue'
import CommunityView from '@/views/CommunityView.vue'
import MyPageView from '@/views/MyPageView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import MainBankView from '@/views/MainBankView.vue'
import FindUsernameView from '@/views/FindUsernameView.vue'
import ResetPasswordView from '@/views/ResetPasswordView.vue'
import { showAuthNotice } from '@/utils/authNotice'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/products',
      name: 'products',
      component: ProductListView,
    },
    {
      path: '/products/:id',
      name: 'product-detail',
      component: ProductDetailView,
    },
    {
      path: '/recommend',
      name: 'recommend',
      component: RecommendView,
      meta: { requiresAuth: true },
    },
    {
      path: '/exchange',
      name: 'exchange',
      component: ExchangeView,
    },
    {
      path: '/spot-assets',
      name: 'spot-assets',
      component: SpotAssetView,
    },
    {
      path: '/map',
      name: 'map',
      component: MainBankView,
      meta: { requiresAuth: true },
    },
    {
      path: '/main-bank',
      name: 'main-bank',
      component: MainBankView,
      meta: { requiresAuth: true },
    },
    {
      path: '/community',
      name: 'community',
      component: CommunityView,
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: MyPageView,
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
    },
    {
      path: '/find-username',
      name: 'find-username',
      component: FindUsernameView,
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: ResetPasswordView,
    },
  ],
})

router.beforeEach((to) => {
  const isLoggedIn = !!localStorage.getItem('token')

  if (to.meta.requiresAuth && !isLoggedIn) {
    showAuthNotice('로그인 후 이용할 수 있습니다.')
    return {
      name: 'login',
      query: {
        redirect: to.fullPath,
      },
    }
  }

  return true
})

export default router
