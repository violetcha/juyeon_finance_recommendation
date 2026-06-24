<template>
  <div class="app-shell">
    <NavBar />

    <main class="app-main">
      <RouterView />
    </main>

    <ChatbotFloatingButton />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import ChatbotFloatingButton from '@/components/ChatbotFloatingButton.vue'
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background:
    radial-gradient(circle at 12% -10%, rgba(31, 79, 216, 0.08), transparent 28%),
    radial-gradient(circle at 88% 4%, rgba(16, 185, 129, 0.08), transparent 30%),
    var(--color-bg);
  color: var(--color-text);
}

.app-main {
  flex: 1;
  width: 100%;
}
</style>
