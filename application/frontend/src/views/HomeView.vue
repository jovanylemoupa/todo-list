<template>
  <div class="home-view">
    <div class="hero-section">
      <h1 class="hero-title">
        Gérez vos tâches efficacement
      </h1>
      <p class="hero-subtitle">
        Une application simple et moderne pour organiser votre quotidien
      </p>
      <BaseButton @click="goToTasks" size="lg">
        Commencer
      </BaseButton>
    </div>

    <div class="stats-section">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">📝</div>
          <div class="stat-content">
            <div class="stat-number">{{ totalTasks }}</div>
            <div class="stat-label">Tâches totales</div>
          </div>
        </div>

        <div class="stat-card urgent">
          <div class="stat-icon">🚨</div>
          <div class="stat-content">
            <div class="stat-number">{{ urgentTasks }}</div>
            <div class="stat-label">Tâches urgentes</div>
          </div>
        </div>

        <div class="stat-card completed">
          <div class="stat-icon">✅</div>
          <div class="stat-content">
            <div class="stat-number">{{ completedTasks }}</div>
            <div class="stat-label">Tâches terminées</div>
          </div>
        </div>

        <div class="stat-card pending">
          <div class="stat-icon">⏳</div>
          <div class="stat-content">
            <div class="stat-number">{{ pendingTasks }}</div>
            <div class="stat-label">En attente</div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="recentTasks.length > 0" class="recent-section">
      <h2 class="section-title">Tâches récentes</h2>
      <div class="recent-tasks">
        <TaskCard
          v-for="task in recentTasks"
          :key="task.id"
          :task="task"
          @edit="editTask"
          @complete="completeTask"
          @delete="deleteTask"
        />
      </div>
      <div class="section-footer">
        <BaseButton variant="secondary" @click="goToTasks">
          Voir toutes les tâches
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTasksStore } from '@/stores/tasks'
import type { Task } from '@/types/task'
import BaseButton from '@/components/ui/BaseButton.vue'
import TaskCard from '@/components/tasks/TaskCard.vue'

const router = useRouter()
const tasksStore = useTasksStore()

// Computed
const totalTasks = computed(() => tasksStore.tasks.length)
const urgentTasks = computed(() => tasksStore.urgentTasks.length)
const completedTasks = computed(() => tasksStore.completedTasks.length)
const pendingTasks = computed(() => 
  tasksStore.tasks.filter(task => task.status !== 'Terminée').length
)

const recentTasks = computed(() => 
  tasksStore.tasks
    .filter(task => task.status !== 'Terminée')
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 3)
)

// Methods
const goToTasks = () => {
  router.push('/tasks')
}

const editTask = (task: Task) => {
  router.push(`/tasks?edit=${task.id}`)
}

const completeTask = async (task: Task) => {
  try {
    await tasksStore.completeTask(task.id)
  } catch (error) {
    console.error('Erreur lors de la completion:', error)
  }
}

const deleteTask = async (task: Task) => {
  try {
    await tasksStore.deleteTask(task.id)
  } catch (error) {
    console.error('Erreur lors de la suppression:', error)
  }
}

// Lifecycle
onMounted(async () => {
  await tasksStore.fetchTasks()
})
</script>

<style scoped>
.home-view {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  text-align: center;
  padding: 4rem 0;
  background: linear-gradient(135deg, var(--color-primary-light), var(--color-primary));
  border-radius: var(--border-radius-xl);
  margin-bottom: 3rem;
  color: white;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.hero-subtitle {
  font-size: 1.25rem;
  margin: 0 0 2rem 0;
  opacity: 0.9;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.stats-section {
  margin-bottom: 3rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: white;
  padding: 2rem;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all var(--transition-normal);
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.stat-card.urgent {
  border-left: 4px solid var(--color-danger);
}

.stat-card.completed {
  border-left: 4px solid var(--color-success);
}

.stat-card.pending {
  border-left: 4px solid var(--color-warning);
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-gray-900);
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--color-gray-600);
  margin-top: 0.25rem;
}

.recent-section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 1.5rem 0;
  color: var(--color-gray-900);
}

.recent-tasks {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.section-footer {
  text-align: center;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .recent-tasks {
    grid-template-columns: 1fr;
  }
}
</style>