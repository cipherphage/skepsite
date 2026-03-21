import { createApp } from 'vue'
import ThemeToggle from './components/ThemeToggle.vue'
import CookieConsent from './components/CookieConsent.vue'
import RegistrationWizard from './components/RegistrationWizard.vue'
import ConstellationGrid from './components/ConstellationGrid.vue'

// Mount theme toggle
const themeToggleEl = document.getElementById('theme-toggle-mount')
if (themeToggleEl) {
  createApp(ThemeToggle).mount(themeToggleEl)
}

// Mount cookie consent
const cookieConsentEl = document.getElementById('cookie-consent-mount')
if (cookieConsentEl) {
  createApp(CookieConsent).mount(cookieConsentEl)
}

// Mount registration wizard if on a wizard page
const wizardEl = document.getElementById('registration-wizard')
if (wizardEl) {
  const app = createApp(RegistrationWizard, {
    wizardType: wizardEl.dataset.wizardType,
    csrfToken: wizardEl.dataset.csrfToken,
    submitUrl: wizardEl.dataset.submitUrl,
  })
  app.mount(wizardEl)
}

// Mount constellation grids
document.querySelectorAll('.constellation-grid-mount').forEach((el) => {
  createApp(ConstellationGrid).mount(el)
})
