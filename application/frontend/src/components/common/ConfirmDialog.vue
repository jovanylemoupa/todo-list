<template>
  <BaseModal
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    :title="title"
    size="sm"
  >
    <div class="confirm-content">
      <div class="confirm-icon">⚠️</div>
      <p class="confirm-message">{{ message }}</p>
    </div>
    
    <template #footer>
      <BaseButton
        variant="secondary"
        @click="$emit('update:modelValue', false)"
      >
        {{ cancelText }}
      </BaseButton>
      <BaseButton
        variant="danger"
        @click="handleConfirm"
      >
        {{ confirmText }}
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
import BaseModal from '@/components/ui/BaseModal.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

interface Props {
  modelValue: boolean
  title?: string
  message: string
  confirmText?: string
  cancelText?: string
}

withDefaults(defineProps<Props>(), {
  title: 'Confirmation',
  confirmText: 'Confirmer',
  cancelText: 'Annuler'
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  confirm: []
}>()

const handleConfirm = () => {
  emit('confirm')
  emit('update:modelValue', false)
}
</script>

<style scoped>
.confirm-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1rem;
}

.confirm-icon {
  font-size: 3rem;
}

.confirm-message {
  color: var(--color-gray-700);
  margin: 0;
  line-height: 1.5;
}
</style>