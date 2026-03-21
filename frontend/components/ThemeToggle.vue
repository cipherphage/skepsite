<script setup>
import { useTheme } from '../composables/useTheme.js'

const { theme, toggle } = useTheme()
</script>

<template>
  <button
    type="button"
    :role="'switch'"
    :aria-checked="theme === 'dark' ? 'true' : 'false'"
    :aria-label="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
    class="toggle-track"
    :class="{ 'is-on': theme === 'dark' }"
    @click="toggle"
    @keydown.enter.prevent="toggle"
    @keydown.space.prevent="toggle"
    style="width:40px; height:24px; cursor:pointer; border:none; flex-shrink:0;"
  >
    <span class="toggle-thumb" style="width:18px; height:18px;">
      <!-- Moon icon (dark mode active) -->
      <svg
        v-if="theme === 'dark'"
        width="12"
        height="12"
        viewBox="0 0 24 24"
        fill="currentColor"
        style="color:#0D0F1A;"
        aria-hidden="true"
      >
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
      </svg>
      <!-- Sun icon (light mode active) -->
      <svg
        v-else
        width="12"
        height="12"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.5"
        style="color:#1A6FD4;"
        aria-hidden="true"
      >
        <circle cx="12" cy="12" r="5"/>
        <line x1="12" y1="1" x2="12" y2="3"/>
        <line x1="12" y1="21" x2="12" y2="23"/>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
        <line x1="1" y1="12" x2="3" y2="12"/>
        <line x1="21" y1="12" x2="23" y2="12"/>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
      </svg>
    </span>
  </button>
</template>
