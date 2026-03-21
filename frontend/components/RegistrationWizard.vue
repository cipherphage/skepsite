<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import ProgressStepper from './wizard/ProgressStepper.vue'
import AttendeeSteps from './wizard/AttendeeSteps.vue'
import PresenterSteps from './wizard/PresenterSteps.vue'
import VolunteerSteps from './wizard/VolunteerSteps.vue'
import Toast from './Toast.vue'

const props = defineProps({
  wizardType: { type: String, required: true }, // 'attendee' | 'presenter' | 'volunteer'
  csrfToken: { type: String, required: true },
  submitUrl: { type: String, required: true },
})

// Step counts
const STEP_COUNTS = { attendee: 4, presenter: 5, volunteer: 3 }
const totalSteps = computed(() => STEP_COUNTS[props.wizardType] ?? 3)

const currentStep = ref(1)
const direction = ref('forward')
const isSubmitting = ref(false)
const serverErrors = ref({})
const toast = ref(null)

// Form data — full flattened object for all types
const formData = ref({
  // Personal info
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  how_heard: '',
  // Attendance
  attendance_format: 'in_person',
  dietary_needs: [],
  accessibility_needs: '',
  donation_amount: '',
  // Presenter
  talk_title: '',
  talk_duration: '15',
  talk_description: '',
  audience_level: 'general',
  bio: '',
  affiliation: '',
  presented_before: null,
  av_needs: [],
  remote_presenting: false,
  preferred_session_time: '',
  // Volunteer
  volunteer_roles: [],
  volunteer_notes: '',
  volunteer_availability: 'full_day',
  volunteer_shift_details: '',
  // Legal
  gdpr_consent: false,
  code_of_conduct_accepted: false,
})

// Field-level errors
const fieldErrors = ref({})

// Step names per type
const stepNames = computed(() => {
  if (props.wizardType === 'attendee') {
    return ['Personal Info', 'Attendance', 'Accessibility', 'Review & Submit']
  } else if (props.wizardType === 'presenter') {
    return ['Personal Info', 'Your Talk', 'Logistics', 'Bio & Background', 'Review & Submit']
  } else {
    return ['Personal Info', 'Your Roles', 'Review & Submit']
  }
})

// Current step name
const currentStepName = computed(() => stepNames.value[currentStep.value - 1] ?? '')

// Announce step changes for screen readers
const announcer = typeof document !== 'undefined' ? document.getElementById('aria-announcer') : null

function announceStep() {
  if (announcer) {
    announcer.textContent = `Step ${currentStep.value} of ${totalSteps.value}: ${currentStepName.value}`
  }
}

// Validation per step
function validateStep(step) {
  const errors = {}
  if (step === 1) {
    if (!formData.value.first_name.trim()) errors.first_name = 'First name is required.'
    if (!formData.value.last_name.trim()) errors.last_name = 'Last name is required.'
    const email = formData.value.email.trim()
    if (!email) {
      errors.email = 'Email address is required.'
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errors.email = 'Please enter a valid email address.'
    }
  }
  if (props.wizardType === 'presenter' && step === 2) {
    if (!formData.value.talk_title.trim()) errors.talk_title = 'Talk title is required.'
    if (!formData.value.talk_description.trim()) errors.talk_description = 'Talk description is required.'
  }
  return errors
}

async function goNext() {
  const errors = validateStep(currentStep.value)
  if (Object.keys(errors).length > 0) {
    fieldErrors.value = errors
    // Focus first error field
    await nextTick()
    const firstError = document.querySelector('.has-error')
    if (firstError) firstError.focus()
    return
  }
  fieldErrors.value = {}

  if (currentStep.value < totalSteps.value) {
    direction.value = 'forward'
    currentStep.value++
    await nextTick()
    announceStep()
    // Focus step heading
    const heading = document.querySelector('.wizard-step-title')
    if (heading) heading.focus()
  } else {
    await submitForm()
  }
}

async function goBack() {
  if (currentStep.value > 1) {
    direction.value = 'backward'
    currentStep.value--
    fieldErrors.value = {}
    await nextTick()
    announceStep()
    const heading = document.querySelector('.wizard-step-title')
    if (heading) heading.focus()
  }
}

async function submitForm() {
  isSubmitting.value = true
  serverErrors.value = {}

  // Final validation
  const reviewErrors = {}
  if (!formData.value.gdpr_consent) {
    reviewErrors.gdpr_consent = 'You must accept the privacy policy to register.'
  }
  if (!formData.value.code_of_conduct_accepted) {
    reviewErrors.code_of_conduct_accepted = 'You must accept the code of conduct.'
  }
  if (Object.keys(reviewErrors).length > 0) {
    fieldErrors.value = reviewErrors
    isSubmitting.value = false
    return
  }

  try {
    const response = await fetch(props.submitUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': props.csrfToken,
      },
      body: JSON.stringify(formData.value),
    })

    const result = await response.json()

    if (result.success) {
      window.location.href = result.confirmation_url
    } else {
      isSubmitting.value = false
      if (result.errors) {
        serverErrors.value = result.errors
        fieldErrors.value = result.errors
        // If email error on step 1, go back
        if (result.errors.email && currentStep.value === totalSteps.value) {
          direction.value = 'backward'
          currentStep.value = 1
        }
      } else {
        showToast('error', 'Something went wrong', result.error || 'Please try again.')
      }
    }
  } catch (err) {
    isSubmitting.value = false
    showToast('error', 'Network Error', 'Could not connect to the server. Please try again.')
  }
}

const toastQueue = ref([])

function showToast(type, title, message) {
  const id = Date.now()
  toastQueue.value.push({ id, type, title, message })
  setTimeout(() => {
    toastQueue.value = toastQueue.value.filter((t) => t.id !== id)
  }, type === 'error' ? 10000 : 5000)
}

function dismissToast(id) {
  toastQueue.value = toastQueue.value.filter((t) => t.id !== id)
}
</script>

<template>
  <div class="wizard-root">
    <!-- Progress stepper -->
    <ProgressStepper
      :current-step="currentStep"
      :total-steps="totalSteps"
      :step-names="stepNames"
    />

    <!-- Step content with transition -->
    <div class="wizard-step-wrapper" style="margin-top:var(--space-lg);">
      <Transition
        :name="direction === 'forward' ? 'step-forward' : 'step-backward'"
        mode="out-in"
      >
        <component
          :is="wizardType === 'attendee' ? AttendeeSteps : wizardType === 'presenter' ? PresenterSteps : VolunteerSteps"
          :key="currentStep"
          :step="currentStep"
          :form-data="formData"
          :errors="{ ...fieldErrors, ...serverErrors }"
          @update:form-data="(v) => Object.assign(formData, v)"
        />
      </Transition>
    </div>

    <!-- Navigation -->
    <div class="wizard-nav">
      <button
        v-if="currentStep > 1"
        type="button"
        class="btn btn-secondary btn-md"
        @click="goBack"
        :disabled="isSubmitting"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <path d="M19 12H5M12 5l-7 7 7 7"/>
        </svg>
        Back
      </button>
      <span v-else></span>

      <button
        type="button"
        class="btn btn-primary btn-md"
        @click="goNext"
        :aria-busy="isSubmitting ? 'true' : 'false'"
        :aria-disabled="isSubmitting ? 'true' : 'false'"
      >
        <span v-if="isSubmitting" class="spinner" style="width:16px; height:16px; margin-right:6px;">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" aria-hidden="true">
            <circle class="track" cx="12" cy="12" r="9" stroke="rgba(255,255,255,0.3)" stroke-width="3" fill="none"/>
            <path d="M12 3 A 9 9 0 0 1 21 12" stroke="white" stroke-width="3" fill="none" stroke-linecap="round"/>
          </svg>
        </span>
        <span v-if="isSubmitting" class="sr-only">Loading…</span>
        <span v-else-if="currentStep < totalSteps">
          Continue
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" style="margin-left:4px;">
            <path d="M5 12h14M12 5l7 7-7 7"/>
          </svg>
        </span>
        <span v-else>
          Submit Registration
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" style="margin-left:4px;">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
        </span>
      </button>
    </div>

    <!-- Toast notifications -->
    <div class="toast-container" aria-live="polite" aria-atomic="false">
      <Toast
        v-for="t in toastQueue"
        :key="t.id"
        :type="t.type"
        :title="t.title"
        :message="t.message"
        @dismiss="dismissToast(t.id)"
      />
    </div>
  </div>
</template>
