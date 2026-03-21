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

const talkDescLength = computed(() => props.formData.talk_description?.length ?? 0)

const avOptions = [
  'Projector/screen',
  'HDMI connection',
  'Microphone',
  'Whiteboard',
  'Laser pointer',
  'Demo computer',
]

const audienceLevels = [
  { value: 'general', label: 'General audience — no background needed' },
  { value: 'science', label: 'Some science background helpful' },
  { value: 'technical', label: 'Technical — domain knowledge expected' },
]

const sessionTimes = [
  { value: '', label: 'No preference' },
  { value: 'morning', label: 'Morning (9:30 AM – 12 PM)' },
  { value: 'afternoon', label: 'Afternoon (1 PM – 4 PM)' },
  { value: 'late_afternoon', label: 'Late afternoon (4 PM – 6 PM)' },
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

const dietaryOptions = ['Vegetarian', 'Vegan', 'Gluten-free', 'Nut allergy', 'Dairy-free', 'Kosher', 'Halal', 'Other']
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
        <label for="p-first-name" class="form-label">First Name <span class="sr-only">(required)</span></label>
        <input id="p-first-name" type="text" class="form-input" :class="{ 'has-error': errors.first_name }"
               :value="formData.first_name" @input="update('first_name', $event.target.value)"
               autocomplete="given-name" required aria-required="true"
               :aria-describedby="errors.first_name ? 'p-first-name-error' : undefined">
        <div v-if="errors.first_name" class="form-error" id="p-first-name-error" role="alert">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          {{ errors.first_name }}
        </div>
      </div>
      <div class="form-group">
        <label for="p-last-name" class="form-label">Last Name <span class="sr-only">(required)</span></label>
        <input id="p-last-name" type="text" class="form-input" :class="{ 'has-error': errors.last_name }"
               :value="formData.last_name" @input="update('last_name', $event.target.value)"
               autocomplete="family-name" required aria-required="true"
               :aria-describedby="errors.last_name ? 'p-last-name-error' : undefined">
        <div v-if="errors.last_name" class="form-error" id="p-last-name-error" role="alert">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          {{ errors.last_name }}
        </div>
      </div>
    </div>

    <div class="form-group">
      <label for="p-email" class="form-label">Email Address <span class="sr-only">(required)</span></label>
      <input id="p-email" type="email" class="form-input" :class="{ 'has-error': errors.email }"
             :value="formData.email" @input="update('email', $event.target.value)"
             autocomplete="email" required aria-required="true"
             :aria-describedby="errors.email ? 'p-email-error p-email-help' : 'p-email-help'">
      <p class="form-help" id="p-email-help">Your confirmation and any scheduling updates will be sent here.</p>
      <div v-if="errors.email" class="form-error" id="p-email-error" role="alert">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        {{ errors.email }}
      </div>
    </div>

    <div class="form-group">
      <label for="p-phone" class="form-label">Phone Number</label>
      <input id="p-phone" type="tel" class="form-input"
             :value="formData.phone" @input="update('phone', $event.target.value)"
             autocomplete="tel" placeholder="(555) 000-0000">
    </div>

    <div class="form-group">
      <label for="p-how-heard" class="form-label">How did you hear about us?</label>
      <select id="p-how-heard" class="form-select" :value="formData.how_heard" @change="update('how_heard', $event.target.value)">
        <option v-for="opt in howHeardOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
      </select>
    </div>
  </div>

  <!-- Step 2: Your Talk -->
  <div v-else-if="step === 2" class="wizard-step-form">
    <div>
      <h2 class="wizard-step-title" tabindex="-1">Your Talk</h2>
      <p class="wizard-step-subtitle">Tell us what you'd like to present.</p>
    </div>

    <div class="form-group">
      <label for="talk-title" class="form-label">Talk Title <span class="sr-only">(required)</span></label>
      <input id="talk-title" type="text" class="form-input" :class="{ 'has-error': errors.talk_title }"
             :value="formData.talk_title" @input="update('talk_title', $event.target.value)"
             placeholder="e.g. 'Why the Moon Landings Were Real (and Why It Matters)'"
             required aria-required="true"
             :aria-describedby="errors.talk_title ? 'talk-title-error' : undefined">
      <div v-if="errors.talk_title" class="form-error" id="talk-title-error" role="alert">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        {{ errors.talk_title }}
      </div>
    </div>

    <fieldset style="border:none; padding:0;">
      <legend class="form-label" style="margin-bottom:var(--space-sm);">Talk Duration</legend>
      <div style="display:flex; gap:var(--space-md);">
        <label class="card" style="cursor:pointer; flex:1; padding:var(--space-md); display:flex; align-items:center; gap:var(--space-sm);"
               :style="formData.talk_duration === '15' ? 'border-color:var(--border-accent); background:var(--accent-primary-subtle);' : ''">
          <input type="radio" name="talk_duration" value="15" :checked="formData.talk_duration === '15'"
                 @change="update('talk_duration', '15')" class="sr-only">
          <div>
            <div style="font-weight:600; color:var(--text-primary);">15 minutes</div>
            <div style="font-size:0.8125rem; color:var(--text-secondary);">Lightning talk</div>
          </div>
        </label>
        <label class="card" style="cursor:pointer; flex:1; padding:var(--space-md); display:flex; align-items:center; gap:var(--space-sm);"
               :style="formData.talk_duration === '30' ? 'border-color:var(--border-accent); background:var(--accent-primary-subtle);' : ''">
          <input type="radio" name="talk_duration" value="30" :checked="formData.talk_duration === '30'"
                 @change="update('talk_duration', '30')" class="sr-only">
          <div>
            <div style="font-weight:600; color:var(--text-primary);">30 minutes</div>
            <div style="font-size:0.8125rem; color:var(--text-secondary);">Standard slot</div>
          </div>
        </label>
      </div>
    </fieldset>

    <div class="form-group">
      <label for="talk-desc" class="form-label">Talk Description <span class="sr-only">(required)</span></label>
      <textarea id="talk-desc" class="form-textarea" :class="{ 'has-error': errors.talk_description }"
                :value="formData.talk_description"
                @input="update('talk_description', $event.target.value)"
                rows="5"
                placeholder="Give a 2-3 sentence description of what you'll cover and why it matters. This is what attendees will see in the schedule."
                required aria-required="true" maxlength="1000"
                :aria-describedby="errors.talk_description ? 'talk-desc-error talk-desc-count' : 'talk-desc-count'">
      </textarea>
      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <div v-if="errors.talk_description" class="form-error" id="talk-desc-error" role="alert">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          {{ errors.talk_description }}
        </div>
        <span v-else></span>
        <span class="char-counter" id="talk-desc-count" aria-live="polite"
              :class="{ 'near-limit': talkDescLength > 800, 'at-limit': talkDescLength >= 1000 }">
          {{ talkDescLength }}/1000
        </span>
      </div>
    </div>

    <div class="form-group">
      <label for="audience-level" class="form-label">Audience Level</label>
      <select id="audience-level" class="form-select" :value="formData.audience_level" @change="update('audience_level', $event.target.value)">
        <option v-for="lvl in audienceLevels" :key="lvl.value" :value="lvl.value">{{ lvl.label }}</option>
      </select>
    </div>
  </div>

  <!-- Step 3: Logistics -->
  <div v-else-if="step === 3" class="wizard-step-form">
    <div>
      <h2 class="wizard-step-title" tabindex="-1">Logistics</h2>
      <p class="wizard-step-subtitle">Help us plan the day.</p>
    </div>

    <fieldset style="border:none; padding:0;">
      <legend class="form-label" style="margin-bottom:var(--space-sm);">A/V Needs</legend>
      <div class="checkbox-group" style="display:grid; grid-template-columns:1fr 1fr; gap:var(--space-sm);">
        <label v-for="opt in avOptions" :key="opt" class="checkbox-item">
          <input type="checkbox" :checked="formData.av_needs.includes(opt)"
                 @change="toggleArrayItem('av_needs', opt)">
          <span class="checkbox-visual" aria-hidden="true">
            <svg width="10" height="10" viewBox="0 0 14 14" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="2 7 6 11 12 3"/></svg>
          </span>
          <span class="checkbox-label">{{ opt }}</span>
        </label>
      </div>
    </fieldset>

    <div class="form-group">
      <label class="checkbox-item" style="cursor:pointer;">
        <input type="checkbox" :checked="formData.remote_presenting" @change="update('remote_presenting', $event.target.checked)">
        <span class="checkbox-visual" aria-hidden="true">
          <svg width="10" height="10" viewBox="0 0 14 14" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="2 7 6 11 12 3"/></svg>
        </span>
        <span class="checkbox-label">I will be presenting remotely (via video call)</span>
      </label>
    </div>

    <div class="form-group">
      <label for="session-time" class="form-label">Preferred Session Time</label>
      <select id="session-time" class="form-select" :value="formData.preferred_session_time" @change="update('preferred_session_time', $event.target.value)">
        <option v-for="opt in sessionTimes" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
      </select>
      <p class="form-help">We'll do our best to accommodate your preference, but can't guarantee it.</p>
    </div>

    <fieldset style="border:none; padding:0;">
      <legend class="form-label" style="margin-bottom:var(--space-sm);">Dietary Restrictions</legend>
      <div class="checkbox-group" style="display:grid; grid-template-columns:1fr 1fr; gap:var(--space-sm);">
        <label v-for="opt in dietaryOptions" :key="opt" class="checkbox-item">
          <input type="checkbox" :checked="formData.dietary_needs.includes(opt)"
                 @change="toggleArrayItem('dietary_needs', opt)">
          <span class="checkbox-visual" aria-hidden="true">
            <svg width="10" height="10" viewBox="0 0 14 14" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="2 7 6 11 12 3"/></svg>
          </span>
          <span class="checkbox-label">{{ opt }}</span>
        </label>
      </div>
    </fieldset>
  </div>

  <!-- Step 4: Bio & Background -->
  <div v-else-if="step === 4" class="wizard-step-form">
    <div>
      <h2 class="wizard-step-title" tabindex="-1">Bio &amp; Background</h2>
      <p class="wizard-step-subtitle">Help attendees know who they're listening to.</p>
    </div>

    <div class="form-group">
      <label for="bio" class="form-label">Short Bio</label>
      <textarea id="bio" class="form-textarea"
                :value="formData.bio" @input="update('bio', $event.target.value)"
                rows="4"
                placeholder="A brief description of who you are. What's your background? What draws you to this topic? No credentials required — passion and curiosity are credentials enough.">
      </textarea>
      <p class="form-help">This will appear in the event program if you're accepted. Max 400 characters recommended.</p>
    </div>

    <div class="form-group">
      <label for="affiliation" class="form-label">Organization / Affiliation</label>
      <input id="affiliation" type="text" class="form-input"
             :value="formData.affiliation" @input="update('affiliation', $event.target.value)"
             placeholder="University, company, or 'independent' — all are fine">
    </div>

    <fieldset style="border:none; padding:0;">
      <legend class="form-label" style="margin-bottom:var(--space-sm);">Have you presented at Skepticamp NYC before?</legend>
      <div style="display:flex; gap:var(--space-md);">
        <label class="card" style="cursor:pointer; padding:var(--space-md); display:flex; align-items:center; gap:var(--space-sm);"
               :style="formData.presented_before === true ? 'border-color:var(--border-accent); background:var(--accent-primary-subtle);' : ''">
          <input type="radio" name="presented_before" :value="true" :checked="formData.presented_before === true"
                 @change="update('presented_before', true)" class="sr-only">
          <span style="font-weight:600; color:var(--text-primary);">Yes, I have</span>
        </label>
        <label class="card" style="cursor:pointer; padding:var(--space-md); display:flex; align-items:center; gap:var(--space-sm);"
               :style="formData.presented_before === false ? 'border-color:var(--border-accent); background:var(--accent-primary-subtle);' : ''">
          <input type="radio" name="presented_before" :value="false" :checked="formData.presented_before === false"
                 @change="update('presented_before', false)" class="sr-only">
          <span style="font-weight:600; color:var(--text-primary);">First time!</span>
        </label>
      </div>
    </fieldset>
  </div>

  <!-- Step 5: Review -->
  <div v-else-if="step === 5" class="wizard-step-form">
    <div>
      <h2 class="wizard-step-title" tabindex="-1">Review &amp; Submit</h2>
      <p class="wizard-step-subtitle">Review your talk proposal before submitting.</p>
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
        <div style="display:flex; justify-content:space-between; padding-bottom:var(--space-sm); border-bottom:1px solid var(--border-subtle);">
          <dt style="color:var(--text-muted); font-size:0.875rem;">Talk</dt>
          <dd style="color:var(--text-primary); font-weight:500; text-align:right;">{{ formData.talk_title }}</dd>
        </div>
        <div style="display:flex; justify-content:space-between;">
          <dt style="color:var(--text-muted); font-size:0.875rem;">Duration</dt>
          <dd style="color:var(--text-primary); font-weight:500;">{{ formData.talk_duration }} minutes</dd>
        </div>
      </dl>
    </div>

    <div style="display:grid; gap:var(--space-md);">
      <label class="checkbox-item">
        <input type="checkbox" :checked="formData.code_of_conduct_accepted"
               @change="update('code_of_conduct_accepted', $event.target.checked)"
               :aria-describedby="errors.code_of_conduct_accepted ? 'p-coc-error' : undefined">
        <span class="checkbox-visual" aria-hidden="true">
          <svg width="10" height="10" viewBox="0 0 14 14" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="2 7 6 11 12 3"/></svg>
        </span>
        <span class="checkbox-label">
          I agree to the Skepticamp NYC Code of Conduct. <span style="color:var(--state-error);" aria-hidden="true">*</span>
        </span>
      </label>
      <div v-if="errors.code_of_conduct_accepted" class="form-error" id="p-coc-error" role="alert">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        {{ errors.code_of_conduct_accepted }}
      </div>

      <label class="checkbox-item">
        <input type="checkbox" :checked="formData.gdpr_consent"
               @change="update('gdpr_consent', $event.target.checked)"
               :aria-describedby="errors.gdpr_consent ? 'p-gdpr-error' : undefined">
        <span class="checkbox-visual" aria-hidden="true">
          <svg width="10" height="10" viewBox="0 0 14 14" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="2 7 6 11 12 3"/></svg>
        </span>
        <span class="checkbox-label">
          I consent to my data being used for event registration per the
          <a href="/privacy/" target="_blank" style="color:var(--text-accent);">Privacy Policy</a>.
          <span style="color:var(--state-error);" aria-hidden="true">*</span>
        </span>
      </label>
      <div v-if="errors.gdpr_consent" class="form-error" id="p-gdpr-error" role="alert">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        {{ errors.gdpr_consent }}
      </div>
    </div>
  </div>
</template>
