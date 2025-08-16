<template>
  <div class="task-filters">
    <p>Filtres (en cours de développement)</p>
  </div>
</template>

<script setup lang="ts">
// Composant minimal pour éviter les erreurs
defineProps<{
  filters: any
}>()

defineEmits<{
  'update:filters': [filters: any]
}>()
</script>

<style scoped>
.task-filters {
  padding: 1rem;
  background: var(--color-gray-100);
  border-radius: var(--border-radius);
  text-align: center;
  color: var(--color-gray-600);
}
</style>