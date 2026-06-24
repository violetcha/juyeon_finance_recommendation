import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import ProductListView from '@/views/ProductListView.vue'
import ProductDetailView from '@/views/ProductDetailView.vue'
import RecommendView from '@/views/RecommendView.vue'
import ExchangeView from '@/views/ExchangeView.vue'
import CommunityView from '@/views/CommunityView.vue'
import MyPageView from '@/views/MyPageView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import MainBankView from '@/views/MainBankView.vue'
import FindUsernameView from '@/views/FindUsernameView.vue'
import ResetPasswordView from '@/views/ResetPasswordView.vue'

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
    },
    {
      path: '/exchange',
      name: 'exchange',
      component: ExchangeView,
    },
    {
      path: '/map',
      name: 'map',
      component: MainBankView,
    },
    {
      path: '/main-bank',
      name: 'main-bank',
      component: MainBankView,
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
    {
      path: '/spot-assets',
      name: 'SpotAsset',
      component: () => import('@/views/SpotAssetView.vue'),
    },
  ],
})

export default router