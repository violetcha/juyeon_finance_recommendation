<template>
  <footer class="app-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <RouterLink :to="{ name: 'home' }" class="footer-logo">
          첫금융
        </RouterLink>
        <p>금융생활의 첫 시작, 첫금융이 함께합니다.</p>
      </div>

      <div class="footer-info">
        <nav class="footer-links" aria-label="푸터 메뉴">
          <a href="#">회사소개</a>
          <a href="#">이용약관</a>
          <a href="#">개인정보처리방침</a>
          <a href="#">금융상품 한눈에</a>
          <a href="#">제휴문의</a>
          <a href="#">고객센터</a>
        </nav>

        <p>
          (주)첫금융 · 대표이사: 첫금융 · 사업자등록번호: 123-45-67890<br>
          서울특별시 강남구 테헤란로 123 · 고객센터: 02-1234-5678 · help@cheotfinance.kr<br>
          © Cheotfinance Inc. All rights reserved.
        </p>
      </div>

      <div class="footer-apps">
        <div class="socials" aria-label="SNS 링크">
          <span>◎</span>
          <span>💬</span>
          <span>▶</span>
        </div>
        <strong>첫금융 앱 다운로드</strong>
        <p>더 편리한 금융생활을 만나보세요.</p>
        <div class="store-row">
          <span>App Store</span>
          <span>Google Play</span>
        </div>
      </div>
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
  background: rgba(255, 255, 255, 0.88);
}

.footer-inner {
  width: min(var(--container-width), calc(100% - 48px));
  margin: 0 auto;
  display: grid;
  grid-template-columns: 220px 1fr 250px;
  gap: 34px;
  padding: 34px 0 40px;
  color: var(--color-text-muted);
}

.footer-logo {
  display: inline-block;
  margin-bottom: 10px;
  color: var(--color-primary);
  font-size: 30px;
  font-weight: 1000;
  letter-spacing: -0.08em;
}

.footer-brand p,
.footer-info p,
.footer-apps p {
  margin: 0;
  font-size: 13px;
  line-height: 1.75;
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  gap: 12px 20px;
  margin-bottom: 12px;
}

.footer-links a {
  color: var(--color-text);
  font-size: 13px;
  font-weight: 800;
}

.footer-apps {
  text-align: right;
}

.footer-apps strong {
  display: block;
  margin-top: 10px;
  color: var(--color-text);
  font-size: 15px;
}

.socials {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.socials span {
  width: 34px;
  height: 34px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--color-border);
  border-radius: 50%;
  background: #fff;
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 900;
}

.store-row {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 12px;
}

.store-row span {
  padding: 8px 12px;
  border: 1px solid var(--color-border-strong);
  border-radius: 10px;
  background: #fff;
  color: var(--color-text);
  font-size: 12px;
  font-weight: 900;
}

@media (max-width: 980px) {
  .footer-inner {
    grid-template-columns: 1fr;
  }

  .footer-apps {
    text-align: left;
  }

  .socials,
  .store-row {
    justify-content: flex-start;
  }
}

@media (max-width: 768px) {
  .footer-inner {
    width: min(100% - 28px, var(--container-width));
  }
}
</style>
