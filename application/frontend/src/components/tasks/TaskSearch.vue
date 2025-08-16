<template>
  <div class="task-search">
    <div class="search-input-container">
      <span class="search-icon">🔍</span>
      <input
        v-model="searchQuery"
        type="text"
        class="search-input"
        placeholder="Rechercher dans les tâches..."
        @input="handleInput"
        @keyup.enter="handleSearch"
      />
      <button
        v-if="searchQuery"
        @click="clearSearch"
        class="clear-button"
      >
        ✕
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { debounce } from '@/utils/helpers'

interface Props {
  modelValue?: string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: ''
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  search: [query: string]
}>()

const searchQuery = ref(props.modelValue)

// Debounced search
const debouncedSearch = debounce((query: string) => {
  emit('search', query)
}, 300)

const handleInput = () => {
  emit('update:modelValue', searchQuery.value)
  debouncedSearch(searchQuery.value)
}

const handleSearch = () => {
  emit('search', searchQuery.value)
}

const clearSearch = () => {
  searchQuery.value = ''
  emit('update:modelValue', '')
  emit('search', '')
}

watch(() => props.modelValue, (newValue) => {
  searchQuery.value = newValue
})
</script>

<style scoped>
.task-search {
  width: 100%;
  max-width: 400px;
}

.search-input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 1rem;
  color: var(--color-gray-400);
  z-index: 1;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  font-size: 0.875rem;
  border: 1px solid var(--color-gray-300);
  border-radius: var(--border-radius-lg);
  background: white;
  transition: all var(--transition-fast);
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.clear-button {
  position: absolute;
  right: 0.75rem;
  background: none;
  border: none;
  color: var(--color-gray-400);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 50%;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
}

.clear-button:hover {
  background: var(--color-gray-100);
  color: var(--color-gray-600);
}
</style>