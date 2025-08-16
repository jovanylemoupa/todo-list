<template>
  <div class="task-sort">
    <p>Tri (en cours de développement)</p>
  </div>
</template>

<script setup lang="ts">
// Composant minimal pour éviter les erreurs
defineProps<{
  sort: any
}>()

defineEmits<{
  'update:sort': [sort: any]
}>()
</script>

<style scoped>
.task-sort {
  padding: 1rem;
  background: var(--color-gray-100);
  border-radius: var(--border-radius);
  text-align: center;
  color: var(--color-gray-600);
}
</style>