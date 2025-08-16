<template>
  <div class="app-layout">
    <AppHeader />
    
    <div class="app-content">
      <AppSidebar v-if="showSidebar" />
      
      <main class="main-content">
        <div class="container">
          <router-view />
        </div>
      </main>
    </div>
    
    <!-- Toast Container -->
    <div id="toast-container" class="toast-container"></div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AppHeader from './AppHeader.vue'
import AppSidebar from './AppSidebar.vue'

const showSidebar = ref(true)
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-content {
  display: flex;
  flex: 1;
}

.main-content {
  flex: 1;
  padding: 2rem 0;
  background: var(--color-gray-50);
}

@media (max-width: 768px) {
  .main-content {
    padding: 1rem 0;
  }
}
</style>