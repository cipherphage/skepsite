<script setup>
defineProps({
  currentStep: { type: Number, required: true },
  totalSteps:  { type: Number, required: true },
  stepNames:   { type: Array,  required: true },
})
</script>

<template>
  <!-- Desktop stepper -->
  <nav class="stepper" aria-label="Registration steps">
    <ol style="display:contents; list-style:none;">
      <li
        v-for="(name, i) in stepNames"
        :key="i"
        class="stepper-step"
        :class="{
          'is-completed': i + 1 < currentStep,
          'is-active':    i + 1 === currentStep,
        }"
      >
        <div
          class="stepper-circle"
          :aria-label="i + 1 < currentStep
            ? `Step ${i + 1}: ${name} — completed`
            : i + 1 === currentStep
              ? `Step ${i + 1}: ${name} — current`
              : `Step ${i + 1}: ${name} — upcoming`"
          :aria-current="i + 1 === currentStep ? 'step' : undefined"
        >
          <!-- Completed: checkmark -->
          <svg v-if="i + 1 < currentStep" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <!-- Active or future: step number -->
          <span v-else aria-hidden="true">{{ i + 1 }}</span>
        </div>
        <span class="stepper-label">{{ name }}</span>
      </li>
    </ol>
  </nav>

  <!-- Mobile fallback -->
  <div class="stepper-mobile" aria-hidden="true">
    <div class="stepper-mobile-text">Step {{ currentStep }} of {{ totalSteps }}: {{ stepNames[currentStep - 1] }}</div>
    <div class="stepper-mobile-bar">
      <div
        class="stepper-mobile-fill"
        :style="{ width: ((currentStep - 1) / (totalSteps - 1) * 100) + '%' }"
      ></div>
    </div>
  </div>
</template>
