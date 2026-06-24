<script setup>
import { computed } from 'vue'
import { getBankLogo } from '@/constants/bankLogoMap'

const props = defineProps({
  bankName: {
    type: String,
    required: true,
  },
  size: {
    type: Number,
    default: 56,
  },
  rounded: {
    type: Number,
    default: 16,
  },
})

const logoSrc = computed(() => getBankLogo(props.bankName))
const fallbackText = computed(() => props.bankName?.replace(/^주식회사\s*/, '').slice(0, 1) || '?')
</script>

<template>
  <div
    class="bank-logo"
    :style="{
      width: `${size}px`,
      height: `${size}px`,
      borderRadius: `${rounded}px`,
    }"
  >
    <img
      v-if="logoSrc"
      :src="logoSrc"
      :alt="`${bankName} 로고`"
      class="bank-logo__img"
    />
    <span v-else class="bank-logo__fallback">{{ fallbackText }}</span>
  </div>
</template>

<style scoped>
.bank-logo {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: #f8fafc;
  border: 1px solid #e5eaf3;
}

.bank-logo__img {
  width: 74%;
  height: 74%;
  object-fit: contain;
  display: block;
}

.bank-logo__fallback {
  font-size: 1.1rem;
  font-weight: 900;
  color: #1829b7;
}
</style>
