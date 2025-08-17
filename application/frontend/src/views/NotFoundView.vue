<template>
  <div class="not-found-view">
    <div class="not-found-content">
      <div class="not-found-icon">🔍</div>
      <h1 class="not-found-title">Page non trouvée</h1>
      <p class="not-found-message">
        Désolé, la page que vous recherchez n'existe pas ou a été déplacée.
      </p>
      <div class="not-found-actions">
        <BaseButton @click="goHome">
          Retour à l'accueil
        </BaseButton>
        <BaseButton variant="secondary" @click="goBack">
          Retour en arrière
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import BaseButton from '@/components/ui/BaseButton.vue'

const router = useRouter()

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.not-found-view {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}

.not-found-content {
  text-align: center;
  max-width: 500px;
  padding: 2rem;
}

.not-found-icon {
  font-size: 5rem;
  margin-bottom: 1rem;
  opacity: 0.6;
}

.not-found-title {
  font-size: 2rem;
  font-weight: 600;
  color: var(--color-gray-900);
  margin: 0 0 1rem 0;
}

.not-found-message {
  color: var(--color-gray-600);
  line-height: 1.6;
  margin: 0 0 2rem 0;
}

.not-found-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

@media (max-width: 768px) {
  .not-found-actions {
    flex-direction: column;
  }
}
</style>