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
    </div>
    
    <!-- Contenu -->
    <div class="category-content">
      <h3 class="category-name">{{ category.name }}</h3>
      
      <p v-if="category.description" class="category-description">
        {{ category.description }}
      </p>
      
      <div class="category-stats">
        <div class="stat-item">
          <span class="stat-label">Tâches:</span>
          <span class="stat-value">{{ category.task_count || 0 }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Créée:</span>
          <span class="stat-value">{{ formatDate(category.created_at) }}</span>
        </div>
      </div>
    </div>
    
    <!-- Actions -->
    <div class="category-actions">
      <BaseButton
        size="sm"
        @click="$emit('edit', category)"
      >
        ✏️ Modifier
      </BaseButton>
      
      <BaseButton
        size="sm"
        class="text-red-600 hover:text-red-700"
        @click="$emit('delete', category)"
      >
        🗑️ Supprimer
      </BaseButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Category } from '@/types/category'
import { formatDate } from '@/utils/formatters';
import BaseButton from '@/components/ui/BaseButton.vue'

defineProps<{
  category: Category
}>()

defineEmits<{
  edit: [category: Category]
  delete: [category: Category]
}>()
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

.category-actions {
  display: flex;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--color-gray-100);
  background: var(--color-gray-50);
}

.category-actions .btn {
  flex: 1;
}
</style>