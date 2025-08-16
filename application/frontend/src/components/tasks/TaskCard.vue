<template>
  <div
    :class="cardClasses"
    @click="$emit('click', task)"
  >
    <div class="card-body">
      <div class="flex justify-between items-start mb-4">
        <h3 class="font-semibold text-lg">{{ task.title }}</h3>
        <div class="flex gap-2">
          <span :class="priorityBadgeClasses">{{ task.priority }}</span>
          <span v-if="task.is_urgent" class="badge badge-danger">Urgent</span>
        </div>
      </div>
      
      <p v-if="task.description" class="text-gray-600 mb-4">
        {{ task.description }}
      </p>
      
      <div class="flex justify-between items-center">
        <div class="flex items-center gap-2">
          <span class="text-sm text-gray-500">
            📅 {{ formatDate(task.due_date) }}
          </span>
          <span v-if="task.category" class="badge badge-gray">
            {{ task.category.name }}
          </span>
        </div>
        
        <div class="flex gap-2">
          <BaseButton
            variant="secondary"
            size="sm"
            @click.stop="$emit('edit', task)"
          >
            ✏️ Modifier
          </BaseButton>
          
          <BaseButton
            variant="primary"
            size="sm"
            v-if="task.status !== 'Terminée'"
            @click.stop="$emit('complete', task)"
          >
            ✅ Terminer
          </BaseButton>
          
          <BaseButton
            variant="danger"
            size="sm"
            @click.stop="$emit('delete', task)"
          >
            🗑️ Supprimer
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Task } from '@/types/task'
import BaseButton from '@/components/ui/BaseButton.vue'
import { formatDate } from '@/utils/formatters'

interface Props {
  task: Task
}

const props = defineProps<Props>()

const emit = defineEmits<{
  click: [task: Task]
  edit: [task: Task]
  complete: [task: Task]
  delete: [task: Task]
}>()

const cardClasses = computed(() => [
  'card',
  'cursor-pointer',
  'transition',
  `priority-${props.task.priority.toLowerCase()}`,
  {
    'urgent-task': props.task.is_urgent,
    'overdue-task': props.task.is_overdue
  }
])

const priorityBadgeClasses = computed(() => [
  'badge',
  {
    'badge-danger': props.task.priority === 'Haute',
    'badge-warning': props.task.priority === 'Moyenne',
    'badge-success': props.task.priority === 'Basse'
  }
])
</script>