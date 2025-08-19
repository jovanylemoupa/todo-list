<template>
  <div class="app-layout">
    <AppHeader />
    
    <div class="app-content">
      <AppSidebar v-if="showSidebar" />
      
      <main class="main-content" :class="{ 'with-sidebar': showSidebar }">
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
  position: relative;
}

.main-content {
  flex: 1;
  padding: 2rem 0;
  background: var(--color-gray-50);
  overflow-y: auto;
  overflow-x: hidden;
  height: calc(100vh - 80px);
}

.main-content.with-sidebar {
  margin-left: 250px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.toast-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 1000;
}

@media (max-width: 768px) {
  .main-content {
    padding: 1rem 0;
    height: calc(100vh - 60px);
  }
  
  .main-content.with-sidebar {
    margin-left: 0;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 0.5rem;
  }
}
</style>