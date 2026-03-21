<script setup>
import { ref, onMounted } from 'vue'

const STORAGE_KEY = 'skepcamp_cookie_consent'

const isVisible = ref(false)
const showPreferences = ref(false)
const analyticsEnabled = ref(false)

onMounted(() => {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (!stored) {
    // Show after 400ms delay so it doesn't compete with hero animation
    setTimeout(() => { isVisible.value = true }, 400)
  }
})

function acceptAll() {
  save({ necessary: true, analytics: true })
}

function declineAll() {
  save({ necessary: true, analytics: false })
}

function savePreferences() {
  save({ necessary: true, analytics: analyticsEnabled.value })
  showPreferences.value = false
}

function save(prefs) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs))
  isVisible.value = false
}

function openPreferences() {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored) {
    try { analyticsEnabled.value = JSON.parse(stored).analytics ?? false } catch {}
  }
  showPreferences.value = true
}

function closePreferences() {
  showPreferences.value = false
}

function handleBackdropClick(e) {
  if (e.target === e.currentTarget) closePreferences()
}

function handleEsc(e) {
  if (e.key === 'Escape') {
    if (showPreferences.value) { closePreferences() }
    else { declineAll() }
  }
}
</script>

<template>
  <!-- Cookie banner -->
  <div
    v-if="isVisible"
    class="cookie-banner"
    :class="{ 'is-visible': isVisible }"
    role="region"
    aria-label="Cookie consent"
    @keydown="handleEsc"
  >
    <div class="cookie-banner-inner">
      <div class="cookie-banner-text">
        <div class="cookie-banner-heading">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
               style="display:inline; margin-right:6px; color:var(--accent-primary); vertical-align:middle;" aria-hidden="true">
            <path d="M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2c0 1.1.9 2 2 2s2-.9 2-2c0 1.1.9 2 2 2s2-.9 2-2c1.1 0 2 .9 2 2s.9 2 2 2c0 5.523-4.477 10-10 10z"/>
            <circle cx="8.5" cy="12" r="1.5" fill="currentColor"/>
            <circle cx="15.5" cy="10" r="1.5" fill="currentColor"/>
            <circle cx="12" cy="16" r="1.5" fill="currentColor"/>
          </svg>
          This site uses cookies
        </div>
        <p class="cookie-banner-body">
          We use cookies to remember your theme preference and measure visit traffic (if you allow).
          We never sell your data.
          <a href="/privacy/" style="color:var(--text-accent);">Privacy policy</a>
        </p>
      </div>
      <div class="cookie-banner-actions">
        <button type="button" class="btn btn-ghost btn-sm" @click="openPreferences">
          Manage preferences
        </button>
        <button type="button" class="btn btn-secondary btn-sm" @click="declineAll">
          Decline all
        </button>
        <button type="button" class="btn btn-primary btn-sm" @click="acceptAll">
          Accept all
        </button>
      </div>
    </div>
  </div>

  <!-- Preferences modal -->
  <Teleport to="body">
    <div
      v-if="showPreferences"
      class="modal-backdrop"
      role="dialog"
      aria-modal="true"
      aria-labelledby="pref-modal-title"
      @click="handleBackdropClick"
      @keydown.esc="closePreferences"
    >
      <div class="modal">
        <div class="modal-header">
          <div>
            <div class="modal-title" id="pref-modal-title">Cookie Preferences</div>
            <p class="modal-subtitle">Choose which cookies you allow us to use.</p>
          </div>
          <button type="button" class="modal-close" @click="closePreferences" aria-label="Close dialog">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <!-- Necessary cookies (always on) -->
        <div style="display:flex; justify-content:space-between; align-items:center; padding:var(--space-md) 0; border-bottom:1px solid var(--border-default);">
          <div>
            <div style="font-weight:600; color:var(--text-primary); font-size:0.9375rem;">Necessary</div>
            <p style="font-size:0.8125rem; color:var(--text-secondary); margin-top:4px;">
              Required for the site to function. Includes session and CSRF protection.
            </p>
          </div>
          <div
            class="toggle-track is-on"
            role="switch"
            aria-checked="true"
            aria-disabled="true"
            aria-label="Necessary cookies — always enabled"
            style="opacity:0.6; cursor:default; flex-shrink:0;"
          >
            <span class="toggle-thumb"></span>
          </div>
        </div>

        <!-- Analytics cookies -->
        <div style="display:flex; justify-content:space-between; align-items:center; padding:var(--space-md) 0;">
          <div>
            <div style="font-weight:600; color:var(--text-primary); font-size:0.9375rem;">Analytics</div>
            <p style="font-size:0.8125rem; color:var(--text-secondary); margin-top:4px;">
              Helps us understand how visitors use the site. No personal data shared with third parties.
            </p>
          </div>
          <button
            type="button"
            class="toggle-track"
            :class="{ 'is-on': analyticsEnabled }"
            role="switch"
            :aria-checked="analyticsEnabled ? 'true' : 'false'"
            aria-label="Analytics cookies"
            @click="analyticsEnabled = !analyticsEnabled"
            style="flex-shrink:0; border:none;"
          >
            <span class="toggle-thumb"></span>
          </button>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary btn-md" @click="closePreferences">Cancel</button>
          <button type="button" class="btn btn-primary btn-md" @click="savePreferences">Save preferences</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
