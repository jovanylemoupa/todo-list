<template>
  <div
    :class="cardClasses"
    @click="$emit('click', task)"
  >
    <div class="card-body">
      <div class="card-header">
        <h3 class="task-title">{{ task.title }}</h3>
        
        <div class="task-menu" @click.stop>
          <button 
            @click="toggleMenu"
            class="menu-trigger"
            :class="{ active: showMenu }"
          >
            ⋯
          </button>
          
          <div v-if="showMenu" class="menu-dropdown">
            <button @click="handleEdit" class="menu-item">
              <span class="menu-icon">✏️</span>
              <span>Modifier</span>
            </button>
            
            <button 
              v-if="task.status !== 'Terminée'"
              @click="handleComplete"
              class="menu-item"
            >
              <span class="menu-icon">✅</span>
              <span>Terminer</span>
            </button>
            
            <button @click="handleDelete" class="menu-item delete">
              <span class="menu-icon">🗑️</span>
              <span>Supprimer</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Badges priorité + urgent -->
      <div class="badges-row">
        <span :class="priorityBadgeClasses">{{ task.priority }}</span>
        <span v-if="task.is_urgent" class="urgent-badge">
          🚨 URGENT
        </span>
      </div>
      
      <!-- Description (limitée) -->
      <div v-if="task.description" class="task-description">
        {{ truncatedDescription }}
      </div>
      
      <!-- Infos compactes -->
      <div class="task-info">
        <div class="info-row">
          <span class="info-item">
            📅 {{ formatDate(task.due_date) }}
          </span>
        </div>
        
        <div class="info-row">
          <span v-if="task.category" class="category-badge">
            📂 {{ task.category.name }}
          </span>
          <span :class="statusBadgeClasses">
            {{ getStatusIcon() }} {{ task.status }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'
import type { Task } from '@/types/task'
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

const showMenu = ref(false)

const cardClasses = computed(() => [
  'task-card',
  `priority-${props.task.priority.toLowerCase()}`,
  {
    'urgent-task': props.task.is_urgent,
    'overdue-task': props.task.is_overdue,
    'completed-task': props.task.status === 'Terminée'
  }
])

const priorityBadgeClasses = computed(() => [
  'priority-badge',
  `priority-${props.task.priority.toLowerCase()}`
])

const statusBadgeClasses = computed(() => [
  'status-badge',
  {
    'status-pending': props.task.status === 'En attente',
    'status-progress': props.task.status === 'En cours',
    'status-completed': props.task.status === 'Terminée'
  }
])

const truncatedDescription = computed(() => {
  if (!props.task.description) return ''
  return props.task.description.length > 60 
    ? props.task.description.substring(0, 60) + '...'
    : props.task.description
})

const getStatusIcon = () => {
  switch (props.task.status) {
    case 'En attente': return '⏳'
    case 'En cours': return '🔄'
    case 'Terminée': return '✅'
    default: return '📋'
  }
}

const toggleMenu = () => {
  showMenu.value = !showMenu.value
}

const closeMenu = () => {
  showMenu.value = false
}

const handleEdit = () => {
  emit('edit', props.task)
  closeMenu()
}

const handleComplete = () => {
  emit('complete', props.task)
  closeMenu()
}

const handleDelete = () => {
  emit('delete', props.task)
  closeMenu()
}

const handleClickOutside = () => {
  if (showMenu.value) {
    closeMenu()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.task-card {
  background: white;
  border-radius: 12px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.task-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

/* Bordures de priorité */
.task-card.priority-haute {
  border-left: 4px solid #ef4444;
}

.task-card.priority-moyenne {
  border-left: 4px solid #f59e0b;
}

.task-card.priority-basse {
  border-left: 4px solid #10b981;
}

.task-card.urgent-task {
  background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
  border-color: #ef4444;
}

.task-card.overdue-task {
  background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%);
  border-color: #f59e0b;
}

.task-card.completed-task {
  background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%);
  opacity: 0.9;
}

.card-body {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  height: 100%;
}

/* Header compact */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.task-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  line-height: 1.3;
  word-break: break-word;
  flex: 1;
  min-width: 0;
}

/* Menu */
.task-menu {
  position: relative;
  flex-shrink: 0;
}

.menu-trigger {
  width: 1.75rem;
  height: 1.75rem;
  border: none;
  background: #f3f4f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1rem;
  color: #6b7280;
  transition: all 0.2s ease;
}

.menu-trigger:hover,
.menu-trigger.active {
  background: #e5e7eb;
  color: #374151;
}

.menu-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border-radius: 6px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  border: 1px solid #e5e7eb;
  z-index: 50;
  min-width: 130px;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 0.8rem;
  transition: background-color 0.15s ease;
  text-align: left;
}

.menu-item:hover {
  background: #f9fafb;
}

.menu-item.delete:hover {
  background: #fef2f2;
  color: #dc2626;
}

.menu-icon {
  font-size: 0.875rem;
}

/* Badges */
.badges-row {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.priority-badge {
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.priority-badge.priority-haute {
  background: #fef2f2;
  color: #dc2626;
}

.priority-badge.priority-moyenne {
  background: #fffbeb;
  color: #d97706;
}

.priority-badge.priority-basse {
  background: #f0fdf4;
  color: #059669;
}

.urgent-badge {
  background: #dc2626;
  color: white;
  padding: 0.125rem 0.375rem;
  border-radius: 9999px;
  font-size: 0.6rem;
  font-weight: 700;
}

/* Description */
.task-description {
  color: #6b7280;
  font-size: 0.8rem;
  line-height: 1.4;
  margin: 0;
  word-break: break-word;
}

/* Infos compactes */
.task-info {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.info-item {
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 500;
}

.category-badge {
  background: #f3f4f6;
  color: #6b7280;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.7rem;
  font-weight: 500;
}

.status-badge {
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.65rem;
  font-weight: 600;
  white-space: nowrap;
}

.status-badge.status-pending {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.status-progress {
  background: #dbeafe;
  color: #1e40af;
}

.status-badge.status-completed {
  background: #d1fae5;
  color: #065f46;
}

/* Responsive */
@media (max-width: 768px) {
  .card-body {
    padding: 0.75rem;
    gap: 0.5rem;
  }
  
  .task-title {
    font-size: 0.9rem;
  }
  
  .task-description {
    font-size: 0.75rem;
  }
  
  .info-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
}
</style>