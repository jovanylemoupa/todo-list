<template>
  <aside class="app-sidebar">
    <div class="sidebar-content">
      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item">
          <span class="nav-icon">🏠</span>
          <span class="nav-text">Accueil</span>
        </router-link>
        
        <router-link to="/tasks" class="nav-item">
          <span class="nav-icon">📝</span>
          <span class="nav-text">Tâches</span>
        </router-link>
        
        <router-link to="/about" class="nav-item">
          <span class="nav-icon">ℹ️</span>
          <span class="nav-text">À propos</span>
        </router-link>

        <router-link to="/categories" class="nav-item">
          <span class="nav-icon">📂</span>
          <span class="nav-text">Catégorie</span>
        </router-link>

      </nav>
      
      <div class="sidebar-footer">
        <div class="sidebar-stats">
          <div class="stat">
            <span class="stat-label">Total</span>
            <span class="stat-value">{{ totalTasks }}</span>
          </div>
          <div v-if="urgentCount > 0" class="stat urgent">
            <span class="stat-label">Urgentes</span>
            <span class="stat-value">{{ urgentCount }}</span>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useTasksStore } from '@/stores/tasks'

const tasksStore = useTasksStore()

const totalTasks = computed(() => tasksStore.tasks.length)
const urgentCount = computed(() => tasksStore.urgentTasks.length)
</script>

<style scoped>
.app-sidebar {
  width: 250px;
  background: white;
  border-right: 1px solid var(--color-gray-200);
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 80px);
}

.sidebar-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  color: var(--color-gray-700);
  text-decoration: none;
  transition: all var(--transition-fast);
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background: var(--color-gray-50);
  color: var(--color-gray-900);
}

.nav-item.router-link-active {
  background: var(--color-primary-light);
  color: var(--color-primary-dark);
  border-left-color: var(--color-primary);
  font-weight: 500;
}

.nav-icon {
  font-size: 1.25rem;
  width: 1.5rem;
  text-align: center;
}

.nav-text {
  font-size: 0.875rem;
}

.sidebar-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--color-gray-200);
  background: var(--color-gray-50);
}

.sidebar-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
}

.stat-label {
  color: var(--color-gray-600);
}

.stat-value {
  font-weight: 600;
  color: var(--color-gray-900);
}

.stat.urgent .stat-label {
  color: var(--color-danger);
}

.stat.urgent .stat-value {
  color: var(--color-danger);
  background: rgba(239, 68, 68, 0.1);
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
}

@media (max-width: 768px) {
  .app-sidebar {
    display: none;
  }
}
</style>