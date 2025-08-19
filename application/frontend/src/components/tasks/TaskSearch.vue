<template>
  <div class="search-container">
    <div class="search-input-wrapper">
      <button 
        @click="handleSearch"
        class="search-icon-btn"
        type="button"
        :disabled="loading"
      >
        🔍
      </button>
      
      <input
        v-model="searchQuery"
        @input="handleInput"
        @keyup.enter="handleSearch"
        @keyup.escape="clearSearch"
        type="text"
        class="search-input"
        :placeholder="placeholder"
        :disabled="loading"
      />
      
      <button
        v-if="isSearching && searchQuery"
        @click="clearSearch"
        class="clear-button"
        type="button"
      >
        ✕
      </button>
      
      <div v-if="loading" class="search-spinner">
        <div class="spinner"></div>
      </div>
    </div>
    
    <div v-if="isSearching && searchQuery" class="search-indicator">
      <span class="search-text">
        🔍 Recherche : "{{ searchQuery }}"
      </span>
      <button @click="clearSearch" class="search-clear-btn">
        Tout afficher
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface Props {
  modelValue: string
  placeholder?: string
  loading?: boolean
  isSearching?: boolean
}

interface Emits {
  (e: 'update:modelValue', value: string): void
  (e: 'search', query: string): void
  (e: 'clear'): void
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Rechercher...',
  loading: false,
  isSearching: false
})

const emit = defineEmits<Emits>()

const searchQuery = ref(props.modelValue)
let searchTimeout: NodeJS.Timeout | null = null

// Sync avec v-model
watch(() => props.modelValue, (newValue) => {
  searchQuery.value = newValue
})

const handleInput = () => {
  emit('update:modelValue', searchQuery.value)
}

const handleSearch = () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  
  emit('search', searchQuery.value.trim())
}


const clearSearch = () => {
  searchQuery.value = ''
  emit('update:modelValue', '')
  emit('search', '')
  emit('clear')
}
</script>

<style scoped>
.search-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon-btn {
  position: absolute;
  left: 0.5rem;
  background: none;
  border: none;
  color: #6b7280;
  font-size: 1rem;
  z-index: 1;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.search-icon-btn:hover:not(:disabled) {
  background: #f3f4f6;
  color: #374151;
}

.search-icon-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: white;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-input:disabled {
  background: #f9fafb;
  cursor: not-allowed;
  opacity: 0.7;
}

.clear-button {
  position: absolute;
  right: 1rem;
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0.25rem;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.clear-button:hover {
  background: #f3f4f6;
  color: #374151;
}

.search-spinner {
  position: absolute;
  right: 1rem;
}

.spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid #e5e7eb;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Indicateur de recherche */
.search-indicator {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
}

.search-text {
  color: #1e40af;
  font-weight: 500;
}

.search-clear-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.search-clear-btn:hover {
  background: #2563eb;
}

/* Responsive */
@media (max-width: 768px) {
  .search-indicator {
    flex-direction: column;
    gap: 0.5rem;
    align-items: stretch;
  }
  
  .search-clear-btn {
    align-self: center;
  }
}
</style>