<template>
  <div class="empty-state">
    <div class="empty-icon">
      {{ icon }}
    </div>
    <h3 class="empty-title">{{ title }}</h3>
    <p class="empty-message">{{ message }}</p>
    <BaseButton
      v-if="actionText"
      @click="$emit('action')"
      class="empty-action"
    >
      {{ actionText }}
    </BaseButton>
  </div>
</template>

<script setup lang="ts">
import BaseButton from '@/components/ui/BaseButton.vue'

interface Props {
  icon?: string
  title?: string
  message: string
  actionText?: string
}

withDefaults(defineProps<Props>(), {
  icon: '📝',
  title: 'Aucun élément'
})

defineEmits<{
  action: []
}>()
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  text-align: center;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.6;
}

.empty-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-gray-900);
  margin: 0 0 0.5rem 0;
}

.empty-message {
  color: var(--color-gray-600);
  margin: 0 0 1.5rem 0;
  max-width: 400px;
  line-height: 1.5;
}

.empty-action {
  margin-top: 0.5rem;
}
</style>