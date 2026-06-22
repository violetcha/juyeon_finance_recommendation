<template>
  <div class="chatbot-floating">
    <button
      v-if="!isOpen"
      type="button"
      class="chatbot-open-button"
      @click="openChatbot"
    >
      <span class="chatbot-icon">💬</span>
      <span class="chatbot-label">금융 챗봇</span>
    </button>

    <section v-else class="chatbot-panel">
      <header class="chatbot-header">
        <div>
          <p>FinBank AI</p>
          <strong>금융 설명 챗봇</strong>
        </div>

        <button type="button" class="close-button" @click="isOpen = false">
          ×
        </button>
      </header>

      <div ref="messageListRef" class="chatbot-messages">
        <div
          v-for="message in messages"
          :key="message.id"
          class="message-row"
          :class="message.role"
        >
          <div class="message-bubble">
            <p>{{ message.content }}</p>
          </div>
        </div>

        <div v-if="loading" class="message-row bot">
          <div class="message-bubble loading-bubble">
            답변을 생성하는 중입니다...
          </div>
        </div>
      </div>

      <div class="quick-questions">
        <button
          v-for="question in quickQuestions"
          :key="question"
          type="button"
          @click="sendQuickQuestion(question)"
        >
          {{ question }}
        </button>
      </div>

      <form class="chatbot-input-row" @submit.prevent="sendMessage">
        <input
          v-model.trim="inputMessage"
          type="text"
          placeholder="금융용어를 물어보세요"
          :disabled="loading"
        />

        <button type="submit" :disabled="loading || !inputMessage">
          전송
        </button>
      </form>
    </section>
  </div>
</template>

<script setup>
import { nextTick, ref } from 'vue'
import api from '@/api/api'

const isOpen = ref(false)
const inputMessage = ref('')
const loading = ref(false)
const messageListRef = ref(null)

const messages = ref([
  {
    id: 1,
    role: 'bot',
    content:
      '안녕하세요. 예금, 적금, 금리, 우대금리, 환율 같은 금융용어를 쉽게 설명해드릴게요.',
  },
])

const quickQuestions = [
  '예금과 적금 차이',
  '우대금리가 뭐야?',
  '중도해지하면 어떻게 돼?',
]

const openChatbot = async () => {
  isOpen.value = true
  await scrollToBottom()
}

const scrollToBottom = async () => {
  await nextTick()

  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight
  }
}

const addMessage = async (role, content) => {
  messages.value.push({
    id: Date.now() + Math.random(),
    role,
    content,
  })

  await scrollToBottom()
}

const sendQuickQuestion = async (question) => {
  if (loading.value) return

  inputMessage.value = question
  await sendMessage()
}

const sendMessage = async () => {
  const message = inputMessage.value.trim()

  if (!message || loading.value) {
    return
  }

  inputMessage.value = ''

  await addMessage('user', message)

  loading.value = true

  try {
    const response = await api.post('/chatbot/explain/', {
      message,
    })

    const answer =
      response.data?.data?.answer ||
      response.data?.message ||
      '답변을 가져오지 못했습니다.'

    await addMessage('bot', answer)
  } catch (error) {
    console.error('챗봇 오류:', error)

    const serverMessage = error.response?.data?.message
    const serverError = error.response?.data?.error

    const errorMessage = serverError
      ? `${serverMessage}\n\n원인: ${serverError}`
      : serverMessage || '챗봇 응답 생성 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'

    await addMessage('bot', errorMessage)
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}
</script>

<style scoped>
.chatbot-floating {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 9999;
  font-family:
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    sans-serif;
}

.chatbot-open-button {
  display: flex;
  align-items: center;
  gap: 8px;
  border: none;
  border-radius: 999px;
  padding: 14px 18px;
  background: #111827;
  color: white;
  font-weight: 800;
  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.28);
  cursor: pointer;
}

.chatbot-icon {
  font-size: 20px;
}

.chatbot-label {
  font-size: 14px;
}

.chatbot-panel {
  width: 360px;
  height: 540px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  background: white;
  box-shadow: 0 18px 44px rgba(15, 23, 42, 0.25);
}

.chatbot-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 18px 16px;
  background: #111827;
  color: white;
}

.chatbot-header p {
  margin: 0 0 4px;
  color: #cbd5e1;
  font-size: 12px;
  font-weight: 800;
}

.chatbot-header strong {
  font-size: 17px;
}

.close-button {
  width: 34px;
  height: 34px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.12);
  color: white;
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
}

.chatbot-messages {
  flex: 1;
  overflow-y: auto;
  padding: 18px;
  background: #f9fafb;
}

.message-row {
  display: flex;
  margin-bottom: 12px;
}

.message-row.user {
  justify-content: flex-end;
}

.message-row.bot {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 78%;
  border-radius: 16px;
  padding: 11px 13px;
  font-size: 14px;
  line-height: 1.55;
  word-break: keep-all;
  white-space: pre-wrap;
}

.message-bubble p {
  margin: 0;
}

.message-row.bot .message-bubble {
  border-bottom-left-radius: 4px;
  background: white;
  color: #111827;
  border: 1px solid #e5e7eb;
}

.message-row.user .message-bubble {
  border-bottom-right-radius: 4px;
  background: #2563eb;
  color: white;
}

.loading-bubble {
  color: #6b7280 !important;
}

.quick-questions {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 12px 14px;
  border-top: 1px solid #e5e7eb;
  background: white;
}

.quick-questions button {
  flex-shrink: 0;
  border: 1px solid #d1d5db;
  border-radius: 999px;
  padding: 8px 10px;
  background: white;
  color: #374151;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}

.quick-questions button:hover {
  border-color: #2563eb;
  color: #2563eb;
}

.chatbot-input-row {
  display: flex;
  gap: 8px;
  padding: 14px;
  border-top: 1px solid #e5e7eb;
  background: white;
}

.chatbot-input-row input {
  flex: 1;
  min-width: 0;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  padding: 11px 12px;
  color: #111827;
  font-size: 14px;
}

.chatbot-input-row button {
  border: none;
  border-radius: 12px;
  padding: 0 14px;
  background: #2563eb;
  color: white;
  font-weight: 800;
  cursor: pointer;
}

.chatbot-input-row button:disabled,
.chatbot-input-row input:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

@media (max-width: 520px) {
  .chatbot-floating {
    right: 14px;
    bottom: 14px;
    left: 14px;
  }

  .chatbot-panel {
    width: 100%;
    height: 520px;
  }

  .chatbot-open-button {
    margin-left: auto;
  }
}
</style>