<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const GRID_SIZE = 5
const PROXIMITY_RADIUS = 60
const ACCENT_COLORS = ['var(--accent-primary)', 'var(--accent-secondary)', 'var(--state-success)']

const containerRef = ref(null)
const dots = ref([])
const isMobile = ref(false)
const pulseTimers = []

function buildGrid() {
  const grid = []
  for (let row = 0; row < GRID_SIZE; row++) {
    for (let col = 0; col < GRID_SIZE; col++) {
      const isCenterRegion = row >= 1 && row <= 3 && col >= 1 && col <= 3
      grid.push({
        id: row * GRID_SIZE + col,
        row,
        col,
        scale: 1,
        opacity: isCenterRegion ? 0.6 : 0.3,
        color: isCenterRegion ? ACCENT_COLORS[Math.floor(Math.random() * ACCENT_COLORS.length)] : 'var(--text-muted)',
        isCenterRegion,
      })
    }
  }
  return grid
}

function onMouseMove(e) {
  if (isMobile.value || !containerRef.value) return

  const rect = containerRef.value.getBoundingClientRect()
  const mouseX = e.clientX - rect.left
  const mouseY = e.clientY - rect.top
  const dotSize = rect.width / GRID_SIZE

  dots.value.forEach((dot, i) => {
    const dotX = (dot.col + 0.5) * dotSize
    const dotY = (dot.row + 0.5) * dotSize
    const dist = Math.hypot(mouseX - dotX, mouseY - dotY)

    if (dist < PROXIMITY_RADIUS) {
      const factor = 1 - dist / PROXIMITY_RADIUS
      dots.value[i] = {
        ...dot,
        scale: 1 + factor * 0.5,
        opacity: Math.min(1, dot.opacity + factor * 0.4),
      }
    } else {
      dots.value[i] = {
        ...dot,
        scale: 1,
        opacity: dot.isCenterRegion ? 0.6 : 0.3,
      }
    }
  })
}

function startMobilePulses() {
  dots.value.forEach((dot, i) => {
    const delay = 2000 + Math.random() * 3000
    const timer = setInterval(() => {
      dots.value[i] = { ...dots.value[i], scale: 1.3, opacity: 1 }
      setTimeout(() => {
        if (dots.value[i]) {
          dots.value[i] = { ...dots.value[i], scale: 1, opacity: dot.isCenterRegion ? 0.6 : 0.3 }
        }
      }, 400)
    }, delay)
    pulseTimers.push(timer)
  })
}

onMounted(() => {
  dots.value = buildGrid()
  isMobile.value = window.matchMedia('(max-width: 1023px)').matches

  if (isMobile.value) {
    startMobilePulses()
  } else {
    containerRef.value?.addEventListener('mousemove', onMouseMove, { passive: true })
  }
})

onBeforeUnmount(() => {
  pulseTimers.forEach(clearInterval)
  containerRef.value?.removeEventListener('mousemove', onMouseMove)
})
</script>

<template>
  <div
    ref="containerRef"
    style="display:grid; grid-template-columns: repeat(5, 1fr); gap:20px; padding:20px; width:100%; height:100%; align-items:center;"
    aria-hidden="true"
    role="presentation"
  >
    <div
      v-for="dot in dots"
      :key="dot.id"
      style="display:flex; align-items:center; justify-content:center;"
    >
      <span
        :style="{
          display: 'block',
          width: '8px',
          height: '8px',
          borderRadius: '50%',
          background: dot.color,
          opacity: dot.opacity,
          transform: `scale(${dot.scale})`,
          transition: 'transform 200ms cubic-bezier(0.16,1,0.3,1), opacity 200ms',
        }"
      ></span>
    </div>
  </div>
</template>
