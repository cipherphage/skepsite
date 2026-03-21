<script setup>
const props = defineProps({
  step:     { type: Number, required: true },
  formData: { type: Object, required: true },
  errors:   { type: Object, default: () => ({}) },
})

const emit = defineEmits(['update:formData'])

function update(field, value) {
  emit('update:formData', { ...props.formData, [field]: value })
}

function toggleRole(role) {
  const arr = [...(props.formData.volunteer_roles ?? [])]
  const idx = arr.indexOf(role)
  if (idx === -1) arr.push(role)
  else arr.splice(idx, 1)
  update('volunteer_roles', arr)
}

const volunteerRoles = [
  { value: 'registration', label: 'Registration desk', desc: 'Welcome attendees, check them in' },
  { value: 'av', label: 'A/V support', desc: 'Help with microphones, projector, video stream' },
  { value: 'setup', label: 'Setup & teardown', desc: 'Arrive early, stay late' },
  { value: 'hospitality', label: 'Hospitality', desc: 'Manage refreshments, guide attendees' },
  { value: 'social_media', label: 'Social media', desc: 'Live-tweet, take photos' },
  { value: 'general', label: 'General helper', desc: "I'll do whatever's needed" },
]

const howHeardOptions = [
  { value: '', label: 'Select one…' },
  { value: 'nycskeptics', label: 'NYC Skeptics newsletter or website' },
  { value: 'social_media', label: 'Social media' },
  { value: 'friend', label: 'Friend or colleague' },
  { value: 'previous_attendee', label: 'Previous attendee' },
  { value: 'search', label: 'Web search' },
  { value: 'other', label: 'Other' },
]
</script>

<template>
  <!-- Step 1: Personal Info -->
  <div v-if="step === 1" class="wizard-step-form">
    <div>
      <h2 class="wizard-step-title" tabindex="-1">Personal Information</h2>
      <p class="wizard-step-subtitle">Tell us who you are.</p>
    </div>

    <div class="form-grid-2">
      <div class="form-group">
        <label for="v-first-name" class="form-label">First Name <span class="sr-only">(required)</span></label>
        <input id="v-first-name" type="text" class="form-input" :class="{ 'has-error': errors.first_name }"
               :value="formData.first_name" @input="update('first_name', $event.target.value)"
               autocomplete="given-name" required aria-required="true"
               :aria-describedby="errors.first_name ? 'v-first-name-error' : undefined">
        <div v-if="errors.first_name" class="form-error" id="v-first-name-error" role="alert">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          {{ errors.first_name }}
        </div>
      </div>
      <div class="form-group">
        <label for="v-last-name" class="form-label">Last Name <span class="sr-only">(required)</span></label>
        <input id="v-last-name" type="text" class="form-input" :class="{ 'has-error': errors.last_name }"
               :value="formData.last_name" @input="update('last_name', $event.target.value)"
               autocomplete="family-name" required aria-required="true"
               :aria-describedby="errors.last_name ? 'v-last-name-error' : undefined">
        <div v-if="errors.last_name" class="form-error" id="v-last-name-error" role="alert">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          {{ errors.last_name }}
        </div>
      </div>
    </div>

    <div class="form-group">
      <label for="v-email" class="form-label">Email Address <span class="sr-only">(required)</span></label>
      <input id="v-email" type="email" class="form-input" :class="{ 'has-error': errors.email }"
             :value="formData.email" @input="update('email', $event.target.value)"
             autocomplete="email" required aria-required="true"
             :aria-describedby="errors.email ? 'v-email-error' : undefined">
      <div v-if="errors.email" class="form-error" id="v-email-error" role="alert">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        {{ errors.email }}
      </div>
    </div>

    <div class="form-group">
      <label for="v-phone" class="form-label">Phone Number</label>
      <input id="v-phone" type="tel" class="form-input"
             :value="formData.phone" @input="update('phone', $event.target.value)"
             autocomplete="tel" placeholder="(555) 000-0000">
      <p class="form-help">We may need to reach you on the day of the event.</p>
    </div>

    <div class="form-group">
      <label for="v-how-heard" class="form-label">How did you hear about us?</label>
      <select id="v-how-heard" class="form-select" :value="formData.how_heard" @change="update('how_heard', $event.target.value)">
        <option v-for="opt in howHeardOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
      </select>
    </div>
  </div>

  <!-- Step 2: Roles & Availability -->
  <div v-else-if="step === 2" class="wizard-step-form">
    <div>
      <h2 class="wizard-step-title" tabindex="-1">Your Roles &amp; Availability</h2>
      <p class="wizard-step-subtitle">Tell us how you'd like to help.</p>
    </div>

    <fieldset style="border:none; padding:0;">
      <legend class="form-label" style="margin-bottom:var(--space-sm);">Volunteer Roles</legend>
      <p style="font-size:0.875rem; color:var(--text-secondary); margin-bottom:var(--space-md);">Select all that interest you.</p>
      <div class="checkbox-group" style="display:grid; gap:var(--space-sm);">
        <label v-for="role in volunteerRoles" :key="role.value" class="checkbox-item" style="align-items:center;">
          <input type="checkbox" :checked="formData.volunteer_roles.includes(role.value)"
                 @change="toggleRole(role.value)">
          <span class="checkbox-visual" aria-hidden="true">
            <svg width="10" height="10" viewBox="0 0 14 14" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="2 7 6 11 12 3"/></svg>
          </span>
          <span class="checkbox-label">
            <span style="font-weight:500;">{{ role.label }}</span>
            <span style="color:var(--text-muted); margin-left:var(--space-xs);">— {{ role.desc }}</span>
          </span>
        </label>
      </div>
    </fieldset>

    <fieldset style="border:none; padding:0;">
      <legend class="form-label" style="margin-bottom:var(--space-sm);">Availability</legend>
      <div style="display:flex; gap:var(--space-md);">
        <label class="card" style="cursor:pointer; flex:1; padding:var(--space-md);"
               :style="formData.volunteer_availability === 'full_day' ? 'border-color:var(--border-accent); background:var(--state-success-subtle);' : ''">
          <input type="radio" name="vol_avail" value="full_day" :checked="formData.volunteer_availability === 'full_day'"
                 @change="update('volunteer_availability', 'full_day')" class="sr-only">
          <div style="font-weight:600; color:var(--text-primary); margin-bottom:4px;">Full Day</div>
          <div style="font-size:0.8125rem; color:var(--text-secondary);">9 AM – 7 PM (including setup)</div>
        </label>
        <label class="card" style="cursor:pointer; flex:1; padding:var(--space-md);"
               :style="formData.volunteer_availability === 'shifts' ? 'border-color:var(--border-accent); background:var(--state-success-subtle);' : ''">
          <input type="radio" name="vol_avail" value="shifts" :checked="formData.volunteer_availability === 'shifts'"
                 @change="update('volunteer_availability', 'shifts')" class="sr-only">
          <div style="font-weight:600; color:var(--text-primary); margin-bottom:4px;">Specific Shifts</div>
          <div style="font-size:0.8125rem; color:var(--text-secondary);">I can only make it for part of the day</div>
        </label>
      </div>
    </fieldset>

    <!-- Conditional shift details -->
    <Transition name="field-reveal">
      <div v-if="formData.volunteer_availability === 'shifts'" class="form-group">
        <label for="shift-details" class="form-label">Which shifts can you make?</label>
        <textarea id="shift-details" class="form-textarea"
                  :value="formData.volunteer_shift_details"
                  @input="update('volunteer_shift_details', $event.target.value)"
                  rows="3"
                  placeholder="e.g. 'I can help from 8:30 AM to 1 PM'">
        </textarea>
      </div>
    </Transition>

    <div class="form-group">
      <label for="vol-notes" class="form-label">Additional Notes</label>
      <textarea id="vol-notes" class="form-textarea"
                :value="formData.volunteer_notes"
                @input="update('volunteer_notes', $event.target.value)"
                rows="3"
                placeholder="Anything else we should know? Special skills, limitations, questions?">
      </textarea>
    </div>
  </div>

  <!-- Step 3: Review & Submit -->
  <div v-else-if="step === 3" class="wizard-step-form">
    <div>
      <h2 class="wizard-step-title" tabindex="-1">Review &amp; Submit</h2>
      <p class="wizard-step-subtitle">Almost there! Review your details.</p>
    </div>

    <div class="card" style="background:var(--bg-card);">
      <dl style="display:grid; gap:var(--space-sm);">
        <div style="display:flex; justify-content:space-between; padding-bottom:var(--space-sm); border-bottom:1px solid var(--border-subtle);">
          <dt style="color:var(--text-muted); font-size:0.875rem;">Name</dt>
          <dd style="color:var(--text-primary); font-weight:500;">{{ formData.first_name }} {{ formData.last_name }}</dd>
        </div>
        <div style="display:flex; justify-content:space-between; padding-bottom:var(--space-sm); border-bottom:1px solid var(--border-subtle);">
          <dt style="color:var(--text-muted); font-size:0.875rem;">Email</dt>
          <dd style="color:var(--text-primary); font-weight:500;">{{ formData.email }}</dd>
        </div>
        <div v-if="formData.volunteer_roles.length" style="display:flex; justify-content:space-between; padding-bottom:var(--space-sm); border-bottom:1px solid var(--border-subtle);">
          <dt style="color:var(--text-muted); font-size:0.875rem;">Roles</dt>
          <dd style="color:var(--text-primary); font-weight:500; text-align:right;">{{ formData.volunteer_roles.join(', ') }}</dd>
        </div>
        <div style="display:flex; justify-content:space-between;">
          <dt style="color:var(--text-muted); font-size:0.875rem;">Availability</dt>
          <dd style="color:var(--text-primary); font-weight:500;">{{ formData.volunteer_availability === 'full_day' ? 'Full day' : 'Specific shifts' }}</dd>
        </div>
      </dl>
    </div>

    <div style="display:grid; gap:var(--space-md);">
      <label class="checkbox-item">
        <input type="checkbox" :checked="formData.code_of_conduct_accepted"
               @change="update('code_of_conduct_accepted', $event.target.checked)"
               :aria-describedby="errors.code_of_conduct_accepted ? 'v-coc-error' : undefined">
        <span class="checkbox-visual" aria-hidden="true">
          <svg width="10" height="10" viewBox="0 0 14 14" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="2 7 6 11 12 3"/></svg>
        </span>
        <span class="checkbox-label">
          I agree to the Skepticamp NYC Code of Conduct. <span style="color:var(--state-error);" aria-hidden="true">*</span>
        </span>
      </label>
      <div v-if="errors.code_of_conduct_accepted" class="form-error" id="v-coc-error" role="alert">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        {{ errors.code_of_conduct_accepted }}
      </div>

      <label class="checkbox-item">
        <input type="checkbox" :checked="formData.gdpr_consent"
               @change="update('gdpr_consent', $event.target.checked)"
               :aria-describedby="errors.gdpr_consent ? 'v-gdpr-error' : undefined">
        <span class="checkbox-visual" aria-hidden="true">
          <svg width="10" height="10" viewBox="0 0 14 14" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="2 7 6 11 12 3"/></svg>
        </span>
        <span class="checkbox-label">
          I consent to my data being used for event registration per the
          <a href="/privacy/" target="_blank" style="color:var(--text-accent);">Privacy Policy</a>.
          <span style="color:var(--state-error);" aria-hidden="true">*</span>
        </span>
      </label>
      <div v-if="errors.gdpr_consent" class="form-error" id="v-gdpr-error" role="alert">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        {{ errors.gdpr_consent }}
      </div>
    </div>

    <p style="font-size:0.8125rem; color:var(--text-muted);">
      <span style="color:var(--state-error);">*</span> Required fields.
    </p>
  </div>
</template>
