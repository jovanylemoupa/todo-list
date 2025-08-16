<template>
  <div class="task-list">
    <div v-if="tasks.length === 0" class="no-tasks">
      <EmptyState
        message="Aucune tâche trouvée"
        action-text="Créer une tâche"
        @action="$emit('create')"
      />
    </div>
    
    <div v-else class="tasks-grid">
      <TaskCard
        v-for="task in tasks"
        :key="task.id"
        :task="task"
        @click="$emit('view', task)"
        @edit="$emit('edit', task)"
        @delete="$emit('delete', task)"
        @complete="$emit('complete', task)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Task } from '@/types/task'
import TaskCard from './TaskCard.vue'
import EmptyState from '@/components/common/EmptyState.vue'

interface Props {
  tasks: Task[]
  groupBy?: 'priority' | 'category' | 'status' | null
}

withDefaults(defineProps<Props>(), {
  groupBy: null
})

defineEmits<{
  view: [task: Task]
  edit: [task: Task]
  delete: [task: Task]
  complete: [task: Task]
  create: []
}>()
</script>

<style scoped>
.task-list {
  width: 100%;
}

.tasks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
  width: 100%;
}

.no-tasks {
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 768px) {
  .tasks-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style>