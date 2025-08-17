<template>
  <div class="categories-view">
    <!-- En-tête -->
    <div class="categories-header">
      <div class="flex justify-between items-center mb-6">
        <div>
          <h2 class="text-2xl font-bold">Gestion des Catégories</h2>
          <p class="text-gray-600 mt-1">
            {{ categories.length }} {{ categories.length > 1 ? 'catégories' : 'catégorie' }}
          </p>
        </div>
        <BaseButton @click="openCreateModal">
          ➕ Nouvelle Catégorie
        </BaseButton>
      </div>
    </div>

    <!-- Contenu principal -->
    <div class="categories-content">
      <LoadingSpinner v-if="loading" />
      
      <EmptyState
        v-else-if="!loading && categories.length === 0"
        message="Aucune catégorie trouvée"
        action-text="Créer une catégorie"
        @action="openCreateModal"
      />
      
      <!-- Grille des catégories -->
      <div v-else class="categories-grid">
        <CategoryCard
          v-for="category in categories"
          :key="category.id"
          :category="category"
          @edit="openEditModal"
          @delete="confirmDelete"
        />
      </div>
    </div>

    <!-- Modal de création/édition -->
    <BaseModal
      v-model="showModal"
      :title="modalTitle"
      size="md"
    >
      <CategoryForm
        :category="currentCategory"
        @submit="handleSubmit"
        @cancel="closeModal"
      />
    </BaseModal>

    <!-- Dialog de confirmation -->
    <ConfirmDialog
      v-model="showConfirmDialog"
      title="Supprimer la catégorie"
      :message="`Êtes-vous sûr de vouloir supprimer la catégorie '${categoryToDelete?.name}' ?`"
      confirm-text="Supprimer"
      @confirm="deleteCategory"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useCategoriesStore } from '@/stores/categories'
import type { Category, CreateCategoryRequest } from '@/types/category'

// Composants
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import CategoryCard from '@/components/categories/CategoryCard.vue'
import CategoryForm from '@/components/categories/CategoryForm.vue'

const categoriesStore = useCategoriesStore()

// State
const showModal = ref(false)
const showConfirmDialog = ref(false)
const currentCategory = ref<Category | null>(null)
const categoryToDelete = ref<Category | null>(null)

// Computed
const loading = computed(() => categoriesStore.loading)
const categories = computed(() => categoriesStore.categories)

const modalTitle = computed(() =>
  currentCategory.value ? 'Modifier la catégorie' : 'Nouvelle catégorie'
)

// Methods
const openCreateModal = () => {
  currentCategory.value = null
  showModal.value = true
}

const openEditModal = (category: Category) => {
  currentCategory.value = category
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  currentCategory.value = null
}

const handleSubmit = async (categoryData: CreateCategoryRequest) => {
  try {
    if (currentCategory.value) {
      await categoriesStore.updateCategory(currentCategory.value.id, categoryData)
    } else {
      await categoriesStore.createCategory(categoryData)
    }
    closeModal()
  } catch (error) {
    console.error('Erreur lors de la sauvegarde:', error)
  }
}

const confirmDelete = (category: Category) => {
  categoryToDelete.value = category
  showConfirmDialog.value = true
}

const deleteCategory = async () => {
  if (categoryToDelete.value) {
    try {
      await categoriesStore.deleteCategory(categoryToDelete.value.id)
    } catch (error) {
      console.error('Erreur lors de la suppression:', error)
    }
  }
  showConfirmDialog.value = false
  categoryToDelete.value = null
}

// Lifecycle
onMounted(async () => {
  await categoriesStore.fetchCategories()
})
</script>

<style scoped>
.categories-view {
  max-width: 1200px;
  margin: 0 auto;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .categories-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style>