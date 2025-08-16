<template>
  <div :class="containerClasses">
    <div :class="spinnerClasses"></div>
    <p v-if="message" class="loading-message">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  size?: 'sm' | 'md' | 'lg'
  centered?: boolean
  message?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  centered: false
})

const containerClasses = computed(() => [
  'loading-container',
  {
    'loading-centered': props.centered
  }
])

const spinnerClasses = computed(() => [
  'spinner',
  `spinner-${props.size}`
])
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-centered {
  justify-content: center;
  min-height: 200px;
}

.spinner {
  border: 2px solid var(--color-gray-200);
  border-top: 2px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.spinner-sm {
  width: 1rem;
  height: 1rem;
}

.spinner-md {
  width: 2rem;
  height: 2rem;
}

.spinner-lg {
  width: 3rem;
  height: 3rem;
}

.loading-message {
  color: var(--color-gray-600);
  font-size: 0.875rem;
  margin: 0;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>