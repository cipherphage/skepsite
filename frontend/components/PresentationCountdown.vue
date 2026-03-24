<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  deadline: {
    type: String,
    required: true,
  },
  editingOpen: {
    type: Boolean,
    default: true,
  },
})

const now = ref(Date.now())
const srAnnouncement = ref('')
let timer = null
let srTimer = null

const deadlineMs = computed(() => new Date(props.deadline).getTime())
const remaining = computed(() => Math.max(0, deadlineMs.value - now.value))
const isExpired = computed(() => remaining.value <= 0)

const SEVEN_DAYS = 7 * 24 * 60 * 60 * 1000

const display = computed(() => {
  if (isExpired.value) return null
  const total = remaining.value
  const days = Math.floor(total / (1000 * 60 * 60 * 24))
  const hours = Math.floor((total % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  const minutes = Math.floor((total % (1000 * 60 * 60)) / (1000 * 60))
  const seconds = Math.floor((total % (1000 * 60)) / 1000)

  // When more than 7 days out, show a simpler format without ticking seconds
  if (total > SEVEN_DAYS) {
    return `${days} days, ${hours} hours remaining`
  }

  const parts = []
  if (days > 0) parts.push(`${days}d`)
  if (hours > 0 || days > 0) parts.push(`${String(hours).padStart(2, '0')}h`)
  parts.push(`${String(minutes).padStart(2, '0')}m`)
  parts.push(`${String(seconds).padStart(2, '0')}s`)
  return parts.join(' ')
})

function updateSrAnnouncement() {
  if (isExpired.value) {
    srAnnouncement.value = 'The editing deadline has passed.'
  } else {
    srAnnouncement.value = `Editing closes in ${display.value}`
  }
}

onMounted(() => {
  timer = setInterval(() => {
    now.value = Date.now()
  }, 1000)
  // Announce to screen readers every 5 minutes, not every second
  updateSrAnnouncement()
  srTimer = setInterval(updateSrAnnouncement, 5 * 60 * 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
  if (srTimer) clearInterval(srTimer)
})
</script>

<template>
  <div
    class="countdown-banner"
    :class="{ 'countdown-banner--expired': isExpired }"
    role="timer"
    :aria-label="isExpired ? 'Editing deadline has passed' : 'Time remaining to edit presentation'"
  >
    <template v-if="isExpired">
      The editing deadline has passed. Your presentation details are now locked.
    </template>
    <template v-else>
      <span>Editing closes in:</span>
      <div class="countdown-digits">{{ display }}</div>
    </template>
  </div>
  <!-- Screen reader announcement updated every 5 minutes -->
  <div aria-live="polite" class="sr-only">{{ srAnnouncement }}</div>
</template>
