<template>
  <div class="category-card">
    <!-- En-tête avec couleur -->
    <div 
      class="category-header"
      :style="{ backgroundColor: category.color || '#6366f1' }"
    >
      <div class="category-icon">
        📁
      </div>
      
      <!-- Menu dropdown -->
      <div class="category-menu" @click.stop>
        <button @click="toggleMenu" class="menu-trigger">⋯</button>
        
        <div v-if="showMenu" class="menu-dropdown">
          <button @click="handleEdit" class="menu-item">
            ✏️ Modifier
          </button>
          <button @click="handleDelete" class="menu-item">
            🗑️ Supprimer
          </button>
        </div>
      </div>
    </div>
    
    <!-- Contenu -->
    <div class="category-content">
      <h3 class="category-name">{{ category.name }}</h3>
      
      <p v-if="category.description" class="category-description">
        {{ category.description }}
      </p>
      
      <div class="category-stats">
        <div class="stat-item">
          <span class="stat-label">Créée:</span>
          <span class="stat-value">{{ formatDate(category.created_at) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type { Category } from '@/types/category'
import { formatDate } from '@/utils/formatters'

const props = defineProps<{
  category: Category
}>()

const emit = defineEmits<{
  edit: [category: Category]
  delete: [category: Category]
}>()

const showMenu = ref(false)

const toggleMenu = () => {
  showMenu.value = !showMenu.value
}

const handleEdit = () => {
  emit('edit', props.category)
  showMenu.value = false
}

const handleDelete = () => {
  emit('delete', props.category)
  showMenu.value = false
}

const handleClickOutside = () => {
  showMenu.value = false
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.category-card {
  background: white;
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-gray-200);
  overflow: hidden;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.category-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.category-header {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.category-icon {
  font-size: 2rem;
  opacity: 0.9;
}

/* Menu ajouté */
.category-menu {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}

.menu-trigger {
  width: 1.5rem;
  height: 1.5rem;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  color: white;
  cursor: pointer;
  font-size: 1rem;
}

.menu-trigger:hover {
  background: rgba(255, 255, 255, 0.3);
}

.menu-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border: 1px solid var(--color-gray-200);
  z-index: 50;
  min-width: 120px;
}

.menu-item {
  display: block;
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 0.875rem;
  text-align: left;
}

.menu-item:hover {
  background: var(--color-gray-50);
}

.category-content {
  padding: 1.5rem;
}

.category-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-gray-900);
  margin-bottom: 0.5rem;
}

.category-description {
  color: var(--color-gray-600);
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.category-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-label {
  font-size: 0.75rem;
  color: var(--color-gray-500);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-size: 0.875rem;
  color: var(--color-gray-900);
  font-weight: 500;
}
</style>