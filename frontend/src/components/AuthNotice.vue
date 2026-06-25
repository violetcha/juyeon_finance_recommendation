<template>
  <Transition name="auth-notice-fade">
    <div v-if="visible" class="auth-notice" role="status" aria-live="polite">
      {{ message }}
    </div>
  </Transition>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import {
  AUTH_NOTICE_EVENT,
  DEFAULT_AUTH_NOTICE_MESSAGE,
  consumePendingAuthNotice,
} from '@/utils/authNotice'

const visible = ref(false)
const message = ref(DEFAULT_AUTH_NOTICE_MESSAGE)
let hideTimer = null

const clearHideTimer = () => {
  if (hideTimer) {
    window.clearTimeout(hideTimer)
    hideTimer = null
  }
}

const showNotice = (nextMessage = DEFAULT_AUTH_NOTICE_MESSAGE) => {
  message.value = nextMessage || DEFAULT_AUTH_NOTICE_MESSAGE
  visible.value = true

  clearHideTimer()

  hideTimer = window.setTimeout(() => {
    visible.value = false
    hideTimer = null
  }, 2200)
}

const handleAuthNotice = (event) => {
  consumePendingAuthNotice()
  showNotice(event.detail?.message)
}

onMounted(() => {
  window.addEventListener(AUTH_NOTICE_EVENT, handleAuthNotice)

  const pending = consumePendingAuthNotice()
  if (pending?.message) {
    showNotice(pending.message)
  }
})

onBeforeUnmount(() => {
  window.removeEventListener(AUTH_NOTICE_EVENT, handleAuthNotice)
  clearHideTimer()
})
</script>

<style scoped>
.auth-notice {
  position: fixed;
  top: calc(var(--header-height, 72px) + 12px);
  left: 50%;
  z-index: 1200;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  max-width: min(92vw, 460px);
  padding: 0 18px;
  border: 1px solid #fecaca;
  border-radius: 999px;
  background: rgba(255, 245, 245, 0.96);
  color: #dc2626;
  font-size: 14px;
  font-weight: 950;
  line-height: 1.35;
  white-space: nowrap;
  box-shadow: 0 18px 34px rgba(220, 38, 38, 0.14);
  backdrop-filter: blur(14px);
  transform: translateX(-50%);
}

.auth-notice-fade-enter-active,
.auth-notice-fade-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}

.auth-notice-fade-enter-from,
.auth-notice-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, -8px);
}

@media (max-width: 640px) {
  .auth-notice {
    top: calc(var(--header-height, 72px) + 10px);
    max-width: calc(100vw - 28px);
    font-size: 13px;
    white-space: normal;
    text-align: center;
  }
}
</style>
