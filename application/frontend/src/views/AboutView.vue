<template>
  <div class="about-view">
    <div class="about-content">
      <div class="about-header">
        <h1 class="about-title">À propos de Todo List</h1>
        <p class="about-subtitle">
          Une application moderne de gestion de tâches construite avec Vue.js 3 et TypeScript
        </p>
      </div>

      <div class="features-section">
        <h2 class="section-title">Fonctionnalités</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">📝</div>
            <h3 class="feature-title">Gestion complète</h3>
            <p class="feature-description">
              Créez, modifiez et supprimez vos tâches en toute simplicité
            </p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">🏷️</div>
            <h3 class="feature-title">Catégorisation</h3>
            <p class="feature-description">
              Organisez vos tâches par catégories (Personnel, Professionnel, etc.)
            </p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3 class="feature-title">Priorités</h3>
            <p class="feature-description">
              Définissez des priorités (Haute, Moyenne, Basse) pour vos tâches
            </p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h3 class="feature-title">Recherche</h3>
            <p class="feature-description">
              Trouvez rapidement vos tâches avec la recherche textuelle
            </p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3 class="feature-title">Filtres avancés</h3>
            <p class="feature-description">
              Filtrez par catégorie, priorité ou statut pour une vue personnalisée
            </p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">📱</div>
            <h3 class="feature-title">Responsive</h3>
            <p class="feature-description">
              Interface adaptée à tous les écrans, mobile et desktop
            </p>
          </div>
        </div>
      </div>

      <div class="tech-section">
        <h2 class="section-title">Technologies utilisées</h2>
        <div class="tech-grid">
          <div class="tech-item">
            <span class="tech-name">Vue.js 3</span>
            <span class="tech-description">Framework JavaScript progressif</span>
          </div>
          <div class="tech-item">
            <span class="tech-name">TypeScript</span>
            <span class="tech-description">JavaScript avec typage statique</span>
          </div>
          <div class="tech-item">
            <span class="tech-name">Pinia</span>
            <span class="tech-description">Gestion d'état pour Vue.js</span>
          </div>
          <div class="tech-item">
            <span class="tech-name">Vue Router</span>
            <span class="tech-description">Routage côté client</span>
          </div>
          <div class="tech-item">
            <span class="tech-name">Axios</span>
            <span class="tech-description">Client HTTP pour les API</span>
          </div>
          <div class="tech-item">
            <span class="tech-name">CSS pur</span>
            <span class="tech-description">Styles modernes sans framework</span>
          </div>
        </div>
      </div>

      <div class="contact-section">
        <h2 class="section-title">Contact</h2>
        <p class="contact-text">
          Cette application a été développée dans le cadre d'un exercice technique pour un poste d'alternant Master Dev Informatique.
        </p>
        <div class="contact-actions">
          <BaseButton @click="goHome">
            Retour à l'accueil
          </BaseButton>
          <BaseButton variant="secondary" @click="goToTasks">
            Voir les tâches
          </BaseButton>
        </div>
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

const goToTasks = () => {
  router.push('/tasks')
}
</script>

<style scoped>
.about-view {
  max-width: 1000px;
  margin: 0 auto;
}

.about-content {
  background: white;
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.about-header {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  color: white;
  padding: 3rem 2rem;
  text-align: center;
}

.about-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
}

.about-subtitle {
  font-size: 1.125rem;
  margin: 0;
  opacity: 0.9;
}

.features-section,
.tech-section,
.contact-section {
  padding: 2rem;
  border-bottom: 1px solid var(--color-gray-200);
}

.contact-section {
  border-bottom: none;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 1.5rem 0;
  color: var(--color-gray-900);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.feature-card {
  padding: 1.5rem;
  border: 1px solid var(--color-gray-200);
  border-radius: var(--border-radius-lg);
  text-align: center;
  transition: all var(--transition-normal);
}

.feature-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--color-primary-light);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  color: var(--color-gray-900);
}

.feature-description {
  color: var(--color-gray-600);
  margin: 0;
  line-height: 1.5;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.tech-item {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  background: var(--color-gray-50);
  border-radius: var(--border-radius);
  border-left: 4px solid var(--color-primary);
}

.tech-name {
  font-weight: 600;
  color: var(--color-gray-900);
  margin-bottom: 0.25rem;
}

.tech-description {
  font-size: 0.875rem;
  color: var(--color-gray-600);
}

.contact-text {
  color: var(--color-gray-700);
  line-height: 1.6;
  margin: 0 0 1.5rem 0;
}

.contact-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

@media (max-width: 768px) {
  .about-header {
    padding: 2rem 1rem;
  }
  
  .about-title {
    font-size: 2rem;
  }
  
  .features-section,
  .tech-section,
  .contact-section {
    padding: 1.5rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .contact-actions {
    flex-direction: column;
  }
}
</style>