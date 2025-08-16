<template>
  <header class="app-header">
    <div class="container">
      <div class="header-content">
        <div class="header-left">
          <h1 class="app-title">
            📝 Todo List
          </h1>
        </div>
        
        <nav class="header-nav">
          <router-link to="/" class="nav-link">Accueil</router-link>
          <router-link to="/tasks" class="nav-link">Tâches</router-link>
          <router-link to="/about" class="nav-link">À propos</router-link>
        </nav>
        
        <div class="header-right">
          <div class="stats">
            <span class="stat-item">
              📊 {{ totalTasks }} tâches
            </span>
            <span v-if="urgentCount > 0" class="stat-item urgent">
              🚨 {{ urgentCount }} urgentes
            </span>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useTasksStore } from '@/stores/tasks'

const tasksStore = useTasksStore()

const totalTasks = computed(() => tasksStore.tasks.length)
const urgentCount = computed(() => tasksStore.urgentTasks.length)
</script>

<style scoped>
.app-header {
  background: white;
  border-bottom: 1px solid var(--color-gray-200);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
  gap: 2rem;
}

.app-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-primary);
  margin: 0;
}

.header-nav {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  padding: 0.5rem 1rem;
  border-radius: var(--border-radius);
  text-decoration: none;
  color: var(--color-gray-600);
  font-weight: 500;
  transition: all var(--transition-fast);
}

.nav-link:hover,
.nav-link.router-link-active {
  background: var(--color-primary-light);
  color: var(--color-primary-dark);
}

.stats {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.stat-item {
  font-size: 0.875rem;
  padding: 0.25rem 0.75rem;
  background: var(--color-gray-100);
  border-radius: var(--border-radius);
  color: var(--color-gray-700);
}

.stat-item.urgent {
  background: var(--color-danger);
  color: white;
  animation: pulse 2s infinite;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }
  
  .header-nav {
    gap: 1rem;
  }
  
  .stats {
    gap: 0.5rem;
  }
}
</style>