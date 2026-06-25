<template>
  <div
    class="chatbot-floating"
    :class="{ dragging: isDragging }"
    :style="floatingStyle"
  >
    <button
      v-if="!isOpen"
      type="button"
      class="chatbot-open-button"
      @pointerdown="startClosedPointer"
    >
      <img :src="chatbotMascot" alt="주여니" class="chatbot-mascot-button" />
    </button>

    <section v-else class="chatbot-panel">
      <header class="chatbot-header" @pointerdown="startPanelPointer">
        <div class="chatbot-title-area">
          <span class="header-mascot-ring">
            <img :src="chatbotMascot" alt="주여니" class="chatbot-header-mascot" />
          </span>
          <div>
            <strong>주여니</strong>
            <span>금융 설명 챗봇</span>
          </div>
        </div>

        <button type="button" class="close-button" @click.stop="isOpen = false">
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
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import api from '@/api/api'
import chatbotMascot from '@/assets/branding/chatbot-mascot.png'

const isOpen = ref(false)
const inputMessage = ref('')
const loading = ref(false)
const messageListRef = ref(null)

const position = reactive({
  x: Math.max(24, window.innerWidth - 116),
  y: Math.max(80, window.innerHeight - 116),
})

const dragState = reactive({
  active: false,
  moved: false,
  mode: 'closed',
  startX: 0,
  startY: 0,
  offsetX: 0,
  offsetY: 0,
})

const isDragging = computed(() => dragState.active && dragState.moved)

const floatingStyle = computed(() => ({
  left: `${position.x}px`,
  top: `${position.y}px`,
}))

const messages = ref([
  {
    id: 1,
    role: 'bot',
    content: `안녕하세요! 저는 주여니예요!
예금, 적금, 금리, 우대금리, 환율 같은 금융용어를 설명해드릴게요.`,
  },
])

const quickQuestions = [
  '예금과 적금 차이',
  '우대금리가 뭐야?',
  '중도해지하면 어떻게 돼?',
]

const getWidgetSize = () => {
  if (isOpen.value) {
    return {
      width: 370,
      height: 540,
    }
  }

  return {
    width: 88,
    height: 88,
  }
}

const clampPosition = (nextX = position.x, nextY = position.y) => {
  const { width, height } = getWidgetSize()
  const padding = 12
  const maxX = Math.max(padding, window.innerWidth - width - padding)
  const maxY = Math.max(padding, window.innerHeight - height - padding)

  position.x = Math.min(Math.max(padding, nextX), maxX)
  position.y = Math.min(Math.max(padding, nextY), maxY)
}

const beginPointer = (event, mode) => {
  if (event.button !== undefined && event.button !== 0) {
    return
  }

  if (
    event.target?.closest?.(
      '.close-button, .quick-questions button, .chatbot-input-row input, .chatbot-input-row button'
    )
  ) {
    return
  }

  dragState.active = true
  dragState.moved = false
  dragState.mode = mode
  dragState.startX = event.clientX
  dragState.startY = event.clientY
  dragState.offsetX = event.clientX - position.x
  dragState.offsetY = event.clientY - position.y

  window.addEventListener('pointermove', handlePointerMove)
  window.addEventListener('pointerup', handlePointerUp, { once: true })
  window.addEventListener('pointercancel', cancelPointer, { once: true })
  window.addEventListener('blur', cancelPointer, { once: true })
}

const startClosedPointer = (event) => {
  beginPointer(event, 'closed')
}

const startPanelPointer = (event) => {
  beginPointer(event, 'panel')
}

const handlePointerMove = (event) => {
  if (!dragState.active) {
    return
  }

  const deltaX = Math.abs(event.clientX - dragState.startX)
  const deltaY = Math.abs(event.clientY - dragState.startY)

  if (deltaX > 5 || deltaY > 5) {
    dragState.moved = true
  }

  if (!dragState.moved) {
    return
  }

  event.preventDefault()
  clampPosition(event.clientX - dragState.offsetX, event.clientY - dragState.offsetY)
}

const cleanupPointerListeners = () => {
  window.removeEventListener('pointermove', handlePointerMove)
  window.removeEventListener('pointerup', handlePointerUp)
  window.removeEventListener('pointercancel', cancelPointer)
  window.removeEventListener('blur', cancelPointer)
}

const handlePointerUp = async () => {
  const shouldOpen = dragState.active && !dragState.moved && dragState.mode === 'closed'

  cleanupPointerListeners()

  dragState.active = false
  dragState.moved = false

  if (shouldOpen) {
    await openChatbot()
  }
}

const cancelPointer = () => {
  cleanupPointerListeners()
  dragState.active = false
  dragState.moved = false
}

const openChatbot = async () => {
  isOpen.value = true

  await nextTick()
  clampPosition()
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
      ? `${serverMessage}

원인: ${serverError}`
      : serverMessage || '챗봇 응답 생성 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'

    await addMessage('bot', errorMessage)
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}

onMounted(() => {
  clampPosition()
  window.addEventListener('resize', () => clampPosition())
})

onBeforeUnmount(() => {
  cleanupPointerListeners()
})
</script>

<style scoped>
.chatbot-floating {
  position: fixed;
  left: 24px;
  top: 24px;
  z-index: 9999;
  font-family:
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    sans-serif;
  user-select: none;
  touch-action: none;
}

.chatbot-floating.dragging {
  cursor: grabbing;
}

.chatbot-open-button {
  width: 88px;
  height: 88px;
  display: grid;
  place-items: center;
  border: 0;
  border-radius: 999px;
  padding: 0;
  background: linear-gradient(135deg, #2454d6 0%, #12306b 58%, #0b1f49 100%);
  box-shadow:
    0 20px 42px rgba(18, 48, 107, 0.24),
    inset 0 1px 0 rgba(255, 255, 255, 0.18);
  cursor: grab;
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease;
}

.chatbot-open-button:hover {
  transform: translateY(-2px);
  box-shadow:
    0 24px 48px rgba(18, 48, 107, 0.28),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.chatbot-open-button:active {
  cursor: grabbing;
}

.chatbot-mascot-button {
  width: 76px;
  height: 76px;
  object-fit: contain;
  display: block;
  pointer-events: none;
  filter: drop-shadow(0 8px 16px rgba(31, 79, 216, 0.14));
}

.chatbot-panel {
  display: flex;
  flex-direction: column;
  width: 370px;
  height: 540px;
  overflow: hidden;
  border: 1px solid #cbd8ee;
  border-radius: 24px;
  background: #fff;
  box-shadow: 0 22px 54px rgba(15, 27, 61, 0.18);
}

.chatbot-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 18px 14px;
  background:
    radial-gradient(circle at 88% 18%, rgba(66, 211, 162, 0.24), transparent 28%),
    linear-gradient(135deg, #f8fbff 0%, #eef4ff 52%, #eafff7 100%);
  color: #0f1b3d;
  border-bottom: 1px solid #dbe4f0;
  cursor: grab;
}

.chatbot-header:active {
  cursor: grabbing;
}

.chatbot-title-area {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chatbot-title-area > div {
  display: grid;
  gap: 3px;
}

.header-mascot-ring {
  width: 56px;
  height: 56px;
  display: grid;
  place-items: center;
  border-radius: 18px;
  background: linear-gradient(135deg, #12306b, #2454d6);
  box-shadow: 0 10px 20px rgba(31, 79, 216, 0.14);
}

.chatbot-header-mascot {
  width: 48px;
  height: 48px;
  object-fit: contain;
  pointer-events: none;
}

.chatbot-header strong {
  color: #0f1b3d;
  font-size: 20px;
  font-weight: 950;
  letter-spacing: -0.045em;
}

.chatbot-header span {
  color: #61708a;
  font-size: 12px;
  font-weight: 850;
}

.close-button {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border: 1px solid #d5e0f2;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.85);
  color: #516179;
  font-size: 23px;
  line-height: 1;
  cursor: pointer;
}

.close-button:hover {
  border-color: #2454d6;
  color: #2454d6;
}

.chatbot-messages {
  flex: 1;
  overflow-y: auto;
  padding: 18px;
  background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
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
  border-radius: 18px;
  padding: 12px 14px;
  line-height: 1.55;
  font-size: 14px;
  word-break: keep-all;
  white-space: pre-line;
}

.message-row.bot .message-bubble {
  border: 1px solid #dbe4f0;
  background: #fff;
  color: #182238;
  border-top-left-radius: 8px;
}

.message-row.user .message-bubble {
  background: linear-gradient(135deg, #2454d6, #12306b);
  color: #fff;
  border-top-right-radius: 8px;
}

.message-bubble p {
  margin: 0;
}

.loading-bubble {
  color: #6c7a92;
  font-weight: 750;
}

.quick-questions {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  overflow-x: auto;
  border-top: 1px solid #eef3fa;
  background: #fff;
}

.quick-questions button {
  flex: 0 0 auto;
  min-height: 34px;
  padding: 0 12px;
  border: 1px solid #d6e0f0;
  border-radius: 999px;
  background: #f7faff;
  color: #273955;
  font-size: 12px;
  font-weight: 850;
  cursor: pointer;
}

.quick-questions button:hover {
  border-color: #2454d6;
  color: #2454d6;
}

.chatbot-input-row {
  display: flex;
  gap: 8px;
  padding: 14px 16px 16px;
  border-top: 1px solid #e6edf7;
  background: #fff;
}

.chatbot-input-row input {
  flex: 1;
  min-width: 0;
  height: 42px;
  border: 1px solid #d1dbea;
  border-radius: 14px;
  padding: 0 13px;
  color: #172033;
  font-size: 14px;
  outline: none;
}

.chatbot-input-row input:focus {
  border-color: #2454d6;
  box-shadow: 0 0 0 3px rgba(36, 84, 214, 0.12);
}

.chatbot-input-row button {
  height: 42px;
  min-width: 68px;
  border: 0;
  border-radius: 14px;
  background: #2454d6;
  color: #fff;
  font-weight: 900;
  cursor: pointer;
}

.chatbot-input-row button:disabled,
.chatbot-input-row input:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

@media (max-width: 520px) {
  .chatbot-panel {
    width: calc(100vw - 24px);
    height: min(540px, calc(100vh - 24px));
  }

  .chatbot-open-button {
    width: 78px;
    height: 78px;
  }

  .chatbot-mascot-button {
    width: 68px;
    height: 68px;
  }
}
</style>