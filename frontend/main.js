import { createApp } from 'vue'
import ThemeToggle from './components/ThemeToggle.vue'
import CookieConsent from './components/CookieConsent.vue'
import RegistrationWizard from './components/RegistrationWizard.vue'
import ConstellationGrid from './components/ConstellationGrid.vue'
import DonationCallout from './components/DonationCallout.vue'
import PresentationCountdown from './components/PresentationCountdown.vue'

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

// Mount donation callouts
document.querySelectorAll('[id^="donation-callout-"]').forEach((el) => {
  const variant = el.dataset.variant || 'full'
  createApp(DonationCallout, { variant }).mount(el)
})

// Mount presentation countdown
const countdownEl = document.getElementById('presentation-countdown-mount')
if (countdownEl) {
  createApp(PresentationCountdown, {
    deadline: countdownEl.dataset.deadline,
    editingOpen: countdownEl.dataset.editingOpen === 'true',
  }).mount(countdownEl)
}
