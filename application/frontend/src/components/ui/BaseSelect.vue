<template>
  <div class="form-group">
    <label v-if="label" :for="selectId" class="form-label">
      {{ label }}
      <span v-if="required" class="text-danger">*</span>
    </label>
    
    <select
      :id="selectId"
      :value="modelValue"
      :disabled="disabled"
      :required="required"
      :class="selectClasses"
      @change="handleChange"
    >
      <option v-if="placeholder" value="">{{ placeholder }}</option>
      <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>
    
    <span v-if="error" class="form-error">{{ error }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

interface Option {
  value: string | number
  label: string
}

interface Props {
  modelValue: string | number
  options: Option[]
  label?: string
  placeholder?: string
  disabled?: boolean
  required?: boolean
  error?: string
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
  required: false
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
}>()

const selectId = ref(`select-${Math.random().toString(36).substr(2, 9)}`)

const selectClasses = computed(() => [
  'form-select',
  {
    'error': props.error,
    'disabled': props.disabled
  }
])

const handleChange = (event: Event) => {
  const target = event.target as HTMLSelectElement
  const value = target.value
  
  // Si c'est un nombre, le convertir
  const numericValue = Number(value)
  if (!isNaN(numericValue) && value !== '') {
    emit('update:modelValue', numericValue)
  } else {
    emit('update:modelValue', value)
  }
}
</script>