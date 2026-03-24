<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'full',
    validator: (v) => ['full', 'compact'].includes(v),
  },
})

const PAYPAL_BUTTON_ID = '83MUR59PT8XBS'
const presetAmounts = [10, 25, 50, 100]

const selectedPreset = ref(null)
const customAmount = ref('')

const donationAmount = computed(() => {
  if (customAmount.value) return customAmount.value
  if (selectedPreset.value !== null) return selectedPreset.value
  return null
})

function selectPreset(amount) {
  if (selectedPreset.value === amount) {
    selectedPreset.value = null
  } else {
    selectedPreset.value = amount
    customAmount.value = ''
  }
}

function onCustomInput(event) {
  customAmount.value = event.target.value
  if (event.target.value) {
    selectedPreset.value = null
  }
}

function submitDonation() {
  // Build and submit a PayPal donate form programmatically.
  const form = document.createElement('form')
  form.action = 'https://www.paypal.com/donate'
  form.method = 'post'
  form.target = '_top'

  const buttonInput = document.createElement('input')
  buttonInput.type = 'hidden'
  buttonInput.name = 'hosted_button_id'
  buttonInput.value = PAYPAL_BUTTON_ID
  form.appendChild(buttonInput)

  // PayPal hosted buttons accept an 'amount' parameter
  const amount = donationAmount.value
  if (amount && Number(amount) > 0) {
    const amountInput = document.createElement('input')
    amountInput.type = 'hidden'
    amountInput.name = 'amount'
    amountInput.value = String(amount)
    form.appendChild(amountInput)
  }

  form.style.display = 'none'
  document.body.appendChild(form)
  form.submit()
}
</script>

<template>
  <!-- Full variant: standalone section for homepage/about -->
  <div v-if="variant === 'full'" class="donation-callout donation-callout--full">
    <div class="donation-callout-inner">
      <div class="donation-callout-text">
        <p class="text-overline" style="margin-bottom:var(--space-sm);">Support Science Education</p>
        <h2 class="donation-callout-heading">
          Keep Skepticamp NYC Free for Everyone
        </h2>
        <p class="donation-callout-body">
          Skepticamp NYC has been free since 2009 — and we intend to keep it that way. But venues, A/V equipment,
          refreshments, and live streaming all cost money. Your donation to
          <a href="https://www.nycskeptics.org/" target="_blank" rel="noopener noreferrer" class="donation-link">New York City Skeptics</a>,
          a 501(c)(3) nonprofit, helps us keep the doors open and the microphones on.
        </p>
        <p class="donation-callout-note">
          Every dollar goes directly toward making this event happen. Donations are tax-deductible.
        </p>
      </div>

      <div class="donation-callout-action">
        <fieldset class="donation-presets" role="group" aria-label="Select a donation amount">
          <legend class="sr-only">Preset donation amounts</legend>
          <button
            v-for="amount in presetAmounts"
            :key="amount"
            type="button"
            class="donation-pill"
            :class="{ 'donation-pill--active': selectedPreset === amount && !customAmount }"
            :aria-pressed="selectedPreset === amount && !customAmount ? 'true' : 'false'"
            @click="selectPreset(amount)"
          >
            ${{ amount }}
          </button>
        </fieldset>

        <div class="donation-custom-wrap">
          <label for="donation-custom-full" class="sr-only">Custom donation amount in dollars</label>
          <span class="donation-custom-prefix" aria-hidden="true">$</span>
          <input
            id="donation-custom-full"
            type="number"
            class="donation-custom-input"
            :value="customAmount"
            @input="onCustomInput"
            placeholder="Other amount"
            min="1"
            max="10000"
            aria-label="Custom donation amount"
          >
        </div>

        <button
          type="button"
          class="btn btn-secondary-accent btn-lg donation-cta"
          aria-label="Donate to NYC Skeptics via PayPal"
          @click="submitDonation"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
          </svg>
          Donate via PayPal
        </button>
        <p class="donation-callout-note" style="margin-top:var(--space-xs); text-align:center;">
          You'll be securely redirected to PayPal to complete your donation.
        </p>
      </div>
    </div>
  </div>

  <!-- Compact variant: for embedding in registration forms -->
  <div v-else class="donation-callout donation-callout--compact">
    <p class="donation-compact-message">
      Skepticamp NYC is free thanks to generous donors. Consider a small contribution to
      <a href="https://www.nycskeptics.org/" target="_blank" rel="noopener noreferrer" class="donation-link">NYC Skeptics</a>,
      a 501(c)(3) nonprofit, to help cover event costs.
    </p>

    <fieldset class="donation-presets donation-presets--compact" role="group" aria-label="Select a donation amount">
      <legend class="sr-only">Preset donation amounts</legend>
      <button
        v-for="amount in presetAmounts"
        :key="amount"
        type="button"
        class="donation-pill donation-pill--sm"
        :class="{ 'donation-pill--active': selectedPreset === amount && !customAmount }"
        :aria-pressed="selectedPreset === amount && !customAmount ? 'true' : 'false'"
        @click="selectPreset(amount)"
      >
        ${{ amount }}
      </button>
    </fieldset>

    <div class="donation-custom-wrap donation-custom-wrap--compact">
      <label for="donation-custom-compact" class="sr-only">Custom donation amount in dollars</label>
      <span class="donation-custom-prefix" aria-hidden="true">$</span>
      <input
        id="donation-custom-compact"
        type="number"
        class="donation-custom-input"
        :value="customAmount"
        @input="onCustomInput"
        placeholder="Other amount"
        min="1"
        max="10000"
        aria-label="Custom donation amount"
      >
    </div>

    <button
      type="button"
      class="btn btn-secondary-accent btn-md donation-cta"
      aria-label="Donate to NYC Skeptics via PayPal"
      @click="submitDonation"
    >
      Donate via PayPal
    </button>

    <p class="donation-callout-note" style="margin-top:var(--space-xs);">
      100% of donations support NYC Skeptics events. Completely optional.
      You'll be securely redirected to PayPal.
    </p>
  </div>
</template>
