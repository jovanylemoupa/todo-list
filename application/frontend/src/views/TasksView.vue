<template>
  <div class="tasks-view">
    <!-- En-tête avec actions -->
    <div class="tasks-header">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold">Gestion des Tâches</h2>
        <BaseButton @click="openCreateModal">
          ➕ Nouvelle Tâche
        </BaseButton>
      </div>
      
      <div class="filters-section card p-4 mb-6">
        <TaskSearch
          v-model="searchQuery"
          @search="handleSearch"
        />
      </div>
    </div>
    
    <!-- Liste des tâches -->
    <div class="tasks-content">
      <LoadingSpinner v-if="loading" />
      
      <EmptyState
        v-else-if="!loading && tasks.length === 0"
        message="Aucune tâche trouvée"
        action-text="Créer une tâche"
        @action="openCreateModal"
      />
      
      <TaskList
        v-else
        :tasks="tasks"
        @edit="openEditModal"
        @delete="confirmDelete"
        @complete="completeTask"
      />
    </div>
    
    <BaseModal
      v-model="showModal"
      :title="modalTitle"
      size="lg"
    >
      <TaskForm
        :task="currentTask"
        @submit="handleSubmit"
        @cancel="closeModal"
      />
    </BaseModal>
    
    <ConfirmDialog
      v-model="showConfirmDialog"
      title="Supprimer la tâche"
      message="Êtes-vous sûr de vouloir supprimer cette tâche ?"
      confirm-text="Supprimer"
      @confirm="deleteTask"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useTasksStore } from '@/stores/tasks'
import type { Task } from '@/types/task'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import TaskList from '@/components/tasks/TaskList.vue'
import TaskForm from '@/components/tasks/TaskForm.vue'
import TaskSearch from '@/components/tasks/TaskSearch.vue'

const tasksStore = useTasksStore()

// State
const showModal = ref(false)
const showConfirmDialog = ref(false)
const currentTask = ref<Task | null>(null)
const taskToDelete = ref<number | null>(null)
const searchQuery = ref('')

// Computed
const loading = computed(() => tasksStore.loading)
const tasks = computed(() => tasksStore.filteredTasks)

const modalTitle = computed(() =>
  currentTask.value ? 'Modifier la tâche' : 'Nouvelle tâche'
)

// Methods
const openCreateModal = () => {
  currentTask.value = null
  showModal.value = true
}

const openEditModal = (task: Task) => {
  currentTask.value = task
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  currentTask.value = null
}

const handleSubmit = async (taskData: any) => {
  try {
    if (currentTask.value) {
      await tasksStore.updateTask(currentTask.value.id, taskData)
    } else {
      await tasksStore.createTask(taskData)
    }
    closeModal()
    await tasksStore.fetchTasks()
  } catch (error) {
    console.error('Erreur lors de la sauvegarde:', error)
  }
}

const confirmDelete = (task: Task) => {
  taskToDelete.value = task.id
  showConfirmDialog.value = true
}

const deleteTask = async () => {
  if (taskToDelete.value) {
    try {
      await tasksStore.deleteTask(taskToDelete.value)
      await tasksStore.fetchTasks()
    } catch (error) {
      console.error('Erreur lors de la suppression:', error)
    }
  }
  showConfirmDialog.value = false
  taskToDelete.value = null
}

const completeTask = async (task: Task) => {
  try {
    await tasksStore.completeTask(task.id)
    await tasksStore.fetchTasks()
  } catch (error) {
    console.error('Erreur lors de la completion:', error)
  }
}

const handleSearch = (query: string) => {
  tasksStore.setFilters({ search: query })
  tasksStore.fetchTasks()
}

// Lifecycle
onMounted(async () => {
  await tasksStore.fetchTasks()
})
</script>

<style scoped>
.tasks-view {
  max-width: 1200px;
  margin: 0 auto;
}

.filters-section {
  background: white;
  border-radius: var(--border-radius-lg);
}

.tasks-content {
  min-height: 400px;
}
</style>