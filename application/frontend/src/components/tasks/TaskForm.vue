<template>
  <form @submit.prevent="handleSubmit" class="task-form">
    <BaseInput
      v-model="form.title"
      label="Titre"
      placeholder="Titre de la tâche"
      required
      :error="errors.title"
    />

    <div class="form-group">
      <label class="form-label">Description</label>
      <textarea
        v-model="form.description"
        class="form-textarea"
        placeholder="Description de la tâche (optionnel)"
        rows="3"
      ></textarea>
    </div>

    <div class="form-row">
      <BaseSelect
        :model-value="form.category_id"
        @update:model-value="updateCategoryId"
        label="Catégorie"
        :options="categoryOptions"
        placeholder="Choisir une catégorie"
        required
        :error="errors.category_id"
      />

      <BaseSelect
        :model-value="form.priority"
        @update:model-value="updatePriority"
        label="Priorité"
        :options="priorityOptions"
        placeholder="Choisir une priorité"
        required
        :error="errors.priority"
      />
    </div>

    <BaseInput
      v-model="form.due_date"
      label="Date d'échéance"
      type="date"
      required
      :error="errors.due_date"
    />

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
        {{ task ? 'Modifier' : 'Créer' }}
      </BaseButton>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import type { Task, CreateTaskRequest, Priority } from '@/types/task'
import { useValidation } from '@/composables/useValidation'
import { useCategoriesStore } from '@/stores/categories'
import { PRIORITIES } from '@/utils/constants'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

interface Props {
  task?: Task | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  submit: [data: CreateTaskRequest]
  cancel: []
}>()

const categoriesStore = useCategoriesStore()
const { errors, rules, validateForm } = useValidation()

const loading = ref(false)

const form = reactive<CreateTaskRequest>({
  title: '',
  description: '',
  category_id: 0,
  priority: 'Moyenne' as Priority,
  due_date: ''
})

const validationSchema = {
  title: [rules.required(), rules.minLength(3)],
  category_id: [rules.required()],
  priority: [rules.required()],
  due_date: [rules.required(), rules.futureDate()]
}

const categoryOptions = computed(() =>
  categoriesStore.categories.map(cat => ({
    value: cat.id,
    label: cat.name
  }))
)

const priorityOptions = computed(() =>
  PRIORITIES.map(priority => ({
    value: priority,
    label: priority
  }))
)

const getSubmitData = () => {
  const submitData = { ...form }
  
  if (submitData.due_date) {
    // Convertir '2025-08-16' en datetime ISO complet (fin de journée)
    submitData.due_date = submitData.due_date + 'T23:59:59.000Z'
  }
  
  return submitData
}

const updateCategoryId = (value: string | number) => {
  form.category_id = Number(value)
}

const updatePriority = (value: string | number) => {
  form.priority = value as Priority
}

const handleSubmit = async () => {
  if (!validateForm(form, validationSchema)) {
    return
  }

  loading.value = true
  
  try {
    const submitData = getSubmitData()
    emit('submit', submitData)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await categoriesStore.fetchCategories()
  
  if (props.task) {
    form.title = props.task.title
    form.description = props.task.description || ''
    form.category_id = props.task.category_id
    form.priority = props.task.priority
    // Extraire seulement la partie date du datetime
    form.due_date = props.task.due_date.split('T')[0]
  } else {
    // Set default date to tomorrow
    const tomorrow = new Date()
    tomorrow.setDate(tomorrow.getDate() + 1)
    form.due_date = tomorrow.toISOString().split('T')[0]
  }
})
</script>

<style scoped>
.task-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
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
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>