<script setup>
import { computed } from 'vue'

const props = defineProps({
  step:     { type: Number, required: true },
  formData: { type: Object, required: true },
  errors:   { type: Object, default: () => ({}) },
})

const emit = defineEmits(['update:formData'])

function update(field, value) {
  emit('update:formData', { ...props.formData, [field]: value })
}

function toggleArrayItem(field, item) {
  const arr = [...(props.formData[field] ?? [])]
  const idx = arr.indexOf(item)
  if (idx === -1) arr.push(item)
  else arr.splice(idx, 1)
  update(field, arr)
}

const dietaryOptions = [
  'Vegetarian', 'Vegan', 'Gluten-free', 'Nut allergy', 'Dairy-free', 'Kosher', 'Halal', 'Other',
]

const howHeardOptions = [
  { value: '', label: 'Select one…' },
  { value: 'nycskeptics', label: 'NYC Skeptics newsletter or website' },
  { value: 'social_media', label: 'Social media' },
  { value: 'friend', label: 'Friend or colleague' },
  { value: 'previous_attendee', label: 'Previous attendee' },
  { value: 'search', label: 'Web search' },
  { value: 'meetup', label: 'Meetup.com' },
  { value: 'other', label: 'Other' },
]
</script>

<template>
  <!-- Step 1: Personal Info -->
  <div v-if="step === 1" class="wizard-step-form">
    <div>
      <h2 class="wizard-step-title" tabindex="-1">Personal Information</h2>
      <p class="wizard-step-subtitle">Tell us who you are. Your information is kept private.</p>
    </div>

    <div class="form-grid-2">
      <div class="form-group">
        <label for="first-name" class="form-label">
          First Name <span class="sr-only">(required)</span>
        </label>
        <input
          id="first-name"
          type="text"
          class="form-input"
          :class="{ 'has-error': errors.first_name }"
          :value="formData.first_name"
          @input="update('first_name', $event.target.value)"
          autocomplete="given-name"
          required
          aria-required="true"
          :aria-describedby="errors.first_name ? 'first-name-error' : undefined"
        >
        <div v-if="errors.first_name" class="form-error" id="first-name-error" role="alert">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          {{ errors.first_name }}
        </div>
      </div>

      <div class="form-group">
        <label for="last-name" class="form-label">
          Last Name <span class="sr-only">(required)</span>
        </label>
        <input
          id="last-name"
          type="text"
          class="form-input"
          :class="{ 'has-error': errors.last_name }"
          :value="formData.last_name"
          @input="update('last_name', $event.target.value)"
          autocomplete="family-name"
          required
          aria-required="true"
          :aria-describedby="errors.last_name ? 'last-name-error' : undefined"
        >
        <div v-if="errors.last_name" class="form-error" id="last-name-error" role="alert">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          {{ errors.last_name }}
        </div>
      </div>
    </div>

    <div class="form-group">
      <label for="email" class="form-label">
        Email Address <span class="sr-only">(required)</span>
      </label>
      <input
        id="email"
        type="email"
        class="form-input"
        :class="{ 'has-error': errors.email }"
        :value="formData.email"
        @input="update('email', $event.target.value)"
        autocomplete="email"
        required
        aria-required="true"
        :aria-describedby="errors.email ? 'email-error email-help' : 'email-help'"
      >
      <p class="form-help" id="email-help">Your confirmation will be sent here.</p>
      <div v-if="errors.email" class="form-error" id="email-error" role="alert">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        {{ errors.email }}
      </div>
    </div>

    <div class="form-group">
      <label for="phone" class="form-label">Phone Number</label>
      <input
        id="phone"
        type="tel"
        class="form-input"
        :value="formData.phone"
        @input="update('phone', $event.target.value)"
        autocomplete="tel"
        placeholder="(555) 000-0000"
      >
      <p class="form-help">Optional. Only used if we need to reach you about your registration.</p>
    </div>

    <div class="form-group">
      <label for="how-heard" class="form-label">How did you hear about Skepticamp NYC?</label>
      <select
        id="how-heard"
        class="form-select"
        :value="formData.how_heard"
        @change="update('how_heard', $event.target.value)"
      >
        <option v-for="opt in howHeardOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
      </select>
    </div>
  </div>

  <!-- Step 2: Attendance -->
  <div v-else-if="step === 2" class="wizard-step-form">
    <div>
      <h2 class="wizard-step-title" tabindex="-1">How Will You Attend?</h2>
      <p class="wizard-step-subtitle">Tell us how you plan to join us.</p>
    </div>

    <fieldset style="border:none; padding:0;">
      <legend class="form-label" style="margin-bottom:var(--space-sm);">
        Attendance Format <span class="sr-only">(required)</span>
      </legend>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:var(--space-md);">
        <label
          class="card"
          :class="formData.attendance_format === 'in_person' ? 'card--selected' : ''"
          style="cursor:pointer; display:flex; align-items:center; gap:var(--space-sm); padding:var(--space-md);"
          :style="formData.attendance_format === 'in_person' ? 'border-color:var(--border-accent); background:var(--accent-primary-subtle);' : ''"
        >
          <input type="radio" name="attendance_format" value="in_person"
                 :checked="formData.attendance_format === 'in_person'"
                 @change="update('attendance_format', 'in_person')"
                 class="sr-only">
          <div>
            <div style="font-weight:600; color:var(--text-primary);">In Person</div>
            <div style="font-size:0.8125rem; color:var(--text-secondary);">151 W. 30th St, NYC</div>
          </div>
        </label>

        <label
          class="card"
          style="cursor:pointer; display:flex; align-items:center; gap:var(--space-sm); padding:var(--space-md);"
          :style="formData.attendance_format === 'online' ? 'border-color:var(--border-accent); background:var(--accent-primary-subtle);' : ''"
        >
          <input type="radio" name="attendance_format" value="online"
                 :checked="formData.attendance_format === 'online'"
                 @change="update('attendance_format', 'online')"
                 class="sr-only">
          <div>
            <div style="font-weight:600; color:var(--text-primary);">Online</div>
            <div style="font-size:0.8125rem; color:var(--text-secondary);">Stream from anywhere</div>
          </div>
        </label>
      </div>
    </fieldset>

    <div class="form-group">
      <label for="donation" class="form-label">Optional Donation</label>
      <div style="display:flex; align-items:center; gap:0;">
        <span style="height:44px; display:flex; align-items:center; padding:0 12px; background:var(--bg-card); border:1px solid var(--border-default); border-right:none; border-radius:var(--radius-md) 0 0 var(--radius-md); color:var(--text-muted); font-size:1rem;">$</span>
        <input
          id="donation"
          type="number"
          class="form-input"
          :value="formData.donation_amount"
          @input="update('donation_amount', $event.target.value)"
          style="border-radius:0 var(--radius-md) var(--radius-md) 0;"
          placeholder="20"
          min="1"
          max="500"
        >
      </div>
      <p class="form-help">100% of donations support NYC Skeptics events. Completely optional.</p>
    </div>
  </div>

  <!-- Step 3: Accessibility -->
  <div v-else-if="step === 3" class="wizard-step-form">
    <div>
      <h2 class="wizard-step-title" tabindex="-1">Accessibility & Dietary Needs</h2>
      <p class="wizard-step-subtitle">Help us make the event comfortable for everyone. All information is optional.</p>
    </div>

    <fieldset style="border:none; padding:0;">
      <legend class="form-label" style="margin-bottom:var(--space-sm);">Dietary Restrictions</legend>
      <div class="checkbox-group" style="display:grid; grid-template-columns:1fr 1fr; gap:var(--space-sm);">
        <label v-for="opt in dietaryOptions" :key="opt" class="checkbox-item">
          <input
            type="checkbox"
            :checked="formData.dietary_needs.includes(opt)"
            @change="toggleArrayItem('dietary_needs', opt)"
          >
          <span class="checkbox-visual" aria-hidden="true">
            <svg width="10" height="10" viewBox="0 0 14 14" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="2 7 6 11 12 3"/>
            </svg>
          </span>
          <span class="checkbox-label">{{ opt }}</span>
        </label>
      </div>
    </fieldset>

    <div class="form-group">
      <label for="accessibility" class="form-label">Accessibility Requirements</label>
      <textarea
        id="accessibility"
        class="form-textarea"
        :value="formData.accessibility_needs"
        @input="update('accessibility_needs', $event.target.value)"
        rows="4"
        placeholder="e.g. wheelchair access needed, sign language interpreter, large-print materials…"
      ></textarea>
      <p class="form-help">We'll do our best to accommodate all needs. The venue is wheelchair accessible.</p>
    </div>
  </div>

  <!-- Step 4: Review -->
  <div v-else-if="step === 4" class="wizard-step-form">
    <div>
      <h2 class="wizard-step-title" tabindex="-1">Review &amp; Submit</h2>
      <p class="wizard-step-subtitle">Please review your details before submitting.</p>
    </div>

    <!-- Summary card -->
    <div class="card" style="background:var(--bg-card);">
      <dl style="display:grid; gap:var(--space-sm);">
        <div style="display:flex; justify-content:space-between; padding-bottom:var(--space-sm); border-bottom:1px solid var(--border-subtle);">
          <dt style="color:var(--text-muted); font-size:0.875rem;">Name</dt>
          <dd style="color:var(--text-primary); font-weight:500; text-align:right;">{{ formData.first_name }} {{ formData.last_name }}</dd>
        </div>
        <div style="display:flex; justify-content:space-between; padding-bottom:var(--space-sm); border-bottom:1px solid var(--border-subtle);">
          <dt style="color:var(--text-muted); font-size:0.875rem;">Email</dt>
          <dd style="color:var(--text-primary); font-weight:500;">{{ formData.email }}</dd>
        </div>
        <div style="display:flex; justify-content:space-between; padding-bottom:var(--space-sm); border-bottom:1px solid var(--border-subtle);">
          <dt style="color:var(--text-muted); font-size:0.875rem;">Format</dt>
          <dd style="color:var(--text-primary); font-weight:500;">{{ formData.attendance_format === 'in_person' ? 'In Person' : 'Online' }}</dd>
        </div>
        <div v-if="formData.donation_amount" style="display:flex; justify-content:space-between;">
          <dt style="color:var(--text-muted); font-size:0.875rem;">Donation</dt>
          <dd style="color:var(--text-primary); font-weight:500;">${{ formData.donation_amount }}</dd>
        </div>
      </dl>
    </div>

    <!-- Legal checkboxes -->
    <div style="display:grid; gap:var(--space-md);">
      <label class="checkbox-item" :style="errors.code_of_conduct_accepted ? 'color:var(--state-error);' : ''">
        <input
          type="checkbox"
          :checked="formData.code_of_conduct_accepted"
          @change="update('code_of_conduct_accepted', $event.target.checked)"
          :aria-describedby="errors.code_of_conduct_accepted ? 'coc-error' : undefined"
        >
        <span class="checkbox-visual" aria-hidden="true">
          <svg width="10" height="10" viewBox="0 0 14 14" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="2 7 6 11 12 3"/>
          </svg>
        </span>
        <span class="checkbox-label">
          I agree to the Skepticamp NYC Code of Conduct — to engage respectfully and inclusively with all participants.
          <span style="color:var(--state-error);" aria-hidden="true"> *</span>
        </span>
      </label>
      <div v-if="errors.code_of_conduct_accepted" class="form-error" id="coc-error" role="alert">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        {{ errors.code_of_conduct_accepted }}
      </div>

      <label class="checkbox-item" :style="errors.gdpr_consent ? 'color:var(--state-error);' : ''">
        <input
          type="checkbox"
          :checked="formData.gdpr_consent"
          @change="update('gdpr_consent', $event.target.checked)"
          :aria-describedby="errors.gdpr_consent ? 'gdpr-error' : undefined"
        >
        <span class="checkbox-visual" aria-hidden="true">
          <svg width="10" height="10" viewBox="0 0 14 14" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="2 7 6 11 12 3"/>
          </svg>
        </span>
        <span class="checkbox-label">
          I consent to my data being used to manage my event registration, in accordance with the
          <a href="/privacy/" target="_blank" style="color:var(--text-accent);">Privacy Policy</a>.
          <span style="color:var(--state-error);" aria-hidden="true"> *</span>
        </span>
      </label>
      <div v-if="errors.gdpr_consent" class="form-error" id="gdpr-error" role="alert">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        {{ errors.gdpr_consent }}
      </div>
    </div>

    <p style="font-size:0.8125rem; color:var(--text-muted);">
      <span style="color:var(--state-error);">*</span> Required fields.
      Your data will never be sold or shared for marketing purposes.
    </p>
  </div>
</template>
