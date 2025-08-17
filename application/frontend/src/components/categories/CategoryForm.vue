<template>
  <form @submit.prevent="handleSubmit" class="category-form">
    <BaseInput
      v-model="form.name"
      label="Nom de la catégorie"
      placeholder="Ex: Travail, Personnel, Urgent..."
      required
      :error="errors.name"
    />

    <div class="form-group">
      <label class="form-label">Description</label>
      <textarea
        v-model="form.description"
        class="form-textarea"
        placeholder="Description de la catégorie (optionnel)"
        rows="3"
      ></textarea>
    </div>

    <div class="color-picker-group">
      <label class="form-label">Couleur</label>
      <div class="color-picker">
        <div class="color-options">
          <button
            v-for="color in colorOptions"
            :key="color.value"
            type="button"
            class="color-option"
            :class="{ active: form.color === color.value }"
            :style="{ backgroundColor: color.value }"
            :title="color.name"
            @click="form.color = color.value"
          >
            <span v-if="form.color === color.value">✓</span>
          </button>
        </div>
        
        <!-- Preview -->
        <div class="color-preview">
          <div 
            class="preview-swatch"
            :style="{ backgroundColor: form.color }"
          ></div>
          <span class="preview-text">{{ form.color }}</span>
        </div>
      </div>
    </div>

    <div class="form-actions">
      <BaseButton
        type="button"
        variant="secondary"
        @click="$emit('cancel')"
      >
        Annuler
      </BaseButton>
      <BaseButton
        type="submit"
        :loading="loading"
      >
        {{ category ? 'Modifier' : 'Créer' }}
      </BaseButton>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import type { Category, CreateCategoryRequest } from '@/types/category'
import { useValidation } from '@/composables/useValidation'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

interface Props {
  category?: Category | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  submit: [data: CreateCategoryRequest]
  cancel: []
}>()

const { errors, rules, validateForm } = useValidation()

const loading = ref(false)

const form = reactive<CreateCategoryRequest>({
  name: '',
  description: '',
  color: '#6366f1'
})

const colorOptions = [
  { name: 'Bleu', value: '#6366f1' },
  { name: 'Vert', value: '#10b981' },
  { name: 'Rouge', value: '#ef4444' },
  { name: 'Orange', value: '#f59e0b' },
  { name: 'Violet', value: '#8b5cf6' },
  { name: 'Rose', value: '#ec4899' },
  { name: 'Cyan', value: '#06b6d4' },
  { name: 'Indigo', value: '#6366f1' },
  { name: 'Gris', value: '#6b7280' },
  { name: 'Noir', value: '#374151' }
]

const validationSchema = {
  name: [rules.required(), rules.minLength(2)],
  color: [rules.required()]
}

const handleSubmit = async () => {
  if (!validateForm(form, validationSchema)) {
    return
  }

  loading.value = true
  
  try {
    const submitData: CreateCategoryRequest = {
      name: form.name.trim(),
      description: form.description?.trim() || '',
      color: form.color
    }
    
    emit('submit', submitData)
  } finally {
    loading.value = false
  }
}

// Initialize form with category data if editing
onMounted(() => {
  if (props.category) {
    form.name = props.category.name
    form.description = props.category.description || ''
    form.color = props.category.color || '#6366f1'
  }
})
</script>

<style scoped>
.category-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.color-picker-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.color-picker {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.color-options {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.5rem;
}

.color-option {
  width: 40px;
  height: 40px;
  border-radius: var(--border-radius);
  border: 2px solid transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  transition: all 0.2s ease;
}

.color-option:hover {
  transform: scale(1.1);
  border-color: var(--color-gray-400);
}

.color-option.active {
  border-color: var(--color-gray-700);
  box-shadow: 0 0 0 2px var(--color-primary-500);
}

.color-preview {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: var(--color-gray-50);
  border-radius: var(--border-radius);
}

.preview-swatch {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.preview-text {
  font-family: monospace;
  font-size: 0.875rem;
  color: var(--color-gray-600);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-gray-200);
}

@media (max-width: 768px) {
  .color-options {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>