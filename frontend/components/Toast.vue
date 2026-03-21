<script setup>
import { computed } from 'vue'

const props = defineProps({
  type:    { type: String, default: 'info' },
  title:   { type: String, required: true },
  message: { type: String, default: '' },
})

defineEmits(['dismiss'])

const duration = computed(() => {
  return props.type === 'error' || props.type === 'warning' ? 10000 : 5000
})

const role = computed(() => {
  return props.type === 'error' || props.type === 'warning' ? 'alert' : 'status'
})

const ariaLive = computed(() => {
  return props.type === 'error' || props.type === 'warning' ? 'assertive' : 'polite'
})
</script>

<template>
  <div
    class="toast"
    :class="`toast--${type}`"
    :role="role"
    :aria-live="ariaLive"
  >
    <!-- Icon -->
    <div class="toast-icon" aria-hidden="true">
      <!-- Success -->
      <svg v-if="type === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
        <polyline points="22 4 12 14.01 9 11.01"/>
      </svg>
      <!-- Error -->
      <svg v-else-if="type === 'error'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16">
        <circle cx="12" cy="12" r="10"/>
        <line x1="15" y1="9" x2="9" y2="15"/>
        <line x1="9" y1="9" x2="15" y2="15"/>
      </svg>
      <!-- Warning -->
      <svg v-else-if="type === 'warning'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16">
        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
        <line x1="12" y1="9" x2="12" y2="13"/>
        <line x1="12" y1="17" x2="12.01" y2="17"/>
      </svg>
      <!-- Info -->
      <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
    </div>

    <!-- Body -->
    <div class="toast-body">
      <div class="toast-title">{{ title }}</div>
      <div v-if="message" class="toast-message">{{ message }}</div>
    </div>

    <!-- Dismiss -->
    <button
      type="button"
      class="toast-dismiss"
      @click="$emit('dismiss')"
      aria-label="Dismiss notification"
    >
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
        <line x1="18" y1="6" x2="6" y2="18"/>
        <line x1="6" y1="6" x2="18" y2="18"/>
      </svg>
    </button>

    <!-- Progress bar -->
    <div
      class="toast-progress"
      :style="{ animationDuration: duration + 'ms' }"
      aria-hidden="true"
    ></div>
  </div>
</template>
