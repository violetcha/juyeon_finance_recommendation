<template>
  <footer class="app-footer">
    <div class="footer-inner">
      <section class="footer-brand">
        <RouterLink :to="{ name: 'home' }" class="footer-logo">
          <span>주</span>
          주연
        </RouterLink>
        <p>주거래은행과 예적금 상품을 연결하는 금융생활 시작 가이드입니다.</p>
      </section>

      <section class="footer-info">
        <nav class="footer-links" aria-label="푸터 메뉴">
          <RouterLink :to="{ name: 'products' }">예적금</RouterLink>
          <RouterLink :to="{ name: 'recommend' }">맞춤추천</RouterLink>
          <RouterLink :to="{ name: 'main-bank' }">주거래은행</RouterLink>
          <RouterLink :to="{ name: 'exchange' }">환율</RouterLink>
          <RouterLink :to="{ name: 'community' }">커뮤니티</RouterLink>
        </nav>

        <p>
          주연은 학습용 금융 추천 프로젝트입니다. 실제 금융상품 가입 전에는 각 금융기관의 공시와 약관을 확인해야 합니다.<br>
          © Juyeon Finance Guide. All rights reserved.
        </p>
      </section>

      <section class="footer-note">
        <strong>Project</strong>
        <p>주거래은행 추천 · 예적금 비교 · 환율 조회 · 커뮤니티</p>
      </section>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.app-footer {
  margin-top: 30px;
  border-top: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.76);
  backdrop-filter: blur(12px);
}

.footer-inner {
  width: min(var(--container-width), calc(100% - 48px));
  margin: 0 auto;
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr) 260px;
  gap: 32px;
  padding: 32px 0 38px;
  color: var(--color-text-muted);
}

.footer-logo {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  color: var(--color-text);
  font-size: 22px;
  font-weight: 950;
  letter-spacing: -0.05em;
}

.footer-logo span {
  width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 11px;
  background: var(--color-primary);
  color: #fff;
  font-size: 17px;
  font-weight: 950;
}

.footer-brand p,
.footer-info p,
.footer-note p {
  margin: 0;
  font-size: 13px;
  line-height: 1.7;
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 18px;
  margin-bottom: 12px;
}

.footer-links a {
  color: var(--color-text);
  font-size: 13px;
  font-weight: 800;
}

.footer-note {
  padding: 18px;
  border: 1px solid var(--color-border);
  border-radius: 18px;
  background: var(--color-surface);
}

.footer-note strong {
  display: block;
  margin-bottom: 6px;
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 900;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

@media (max-width: 980px) {
  .footer-inner {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .footer-inner {
    width: min(100% - 28px, var(--container-width));
  }
}
</style>
