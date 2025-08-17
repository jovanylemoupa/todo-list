import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Category, CreateCategoryRequest } from '@/types/category'
import { categoriesService } from '@/services/categories.service'
import { useToast } from '@/composables/useToast'

export const useCategoriesStore = defineStore('categories', () => {
  const { showToast } = useToast()

  // State
  const categories = ref<Category[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Actions
  const fetchCategories = async () => {
    loading.value = true
    error.value = null

    try {
      categories.value = await categoriesService.getCategories()
    } catch (err: any) {
      error.value = err.message
      console.error('Erreur lors du chargement des catégories:', err)
    } finally {
      loading.value = false
    }
  }

  const createCategory = async (categoryData: CreateCategoryRequest): Promise<Category> => {
    loading.value = true

    try {
      const newCategory = await categoriesService.createCategory(categoryData)
      categories.value.push(newCategory)

      showToast('Catégorie créée avec succès !', 'success')
      return newCategory
    } catch (err: any) {
      console.error('Erreur lors de la création:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateCategory = async (
    id: number,
    categoryData: Partial<CreateCategoryRequest>,
  ): Promise<Category> => {
    loading.value = true

    try {
      const updatedCategory = await categoriesService.updateCategory(id, categoryData)

      const index = categories.value.findIndex((cat) => cat.id === id)
      if (index !== -1) {
        categories.value[index] = updatedCategory
      }

      showToast('Catégorie mise à jour !', 'success')
      return updatedCategory
    } catch (err: any) {
      console.error('Erreur lors de la mise à jour:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteCategory = async (id: number): Promise<void> => {
    loading.value = true

    try {
      await categoriesService.deleteCategory(id)

      const index = categories.value.findIndex((cat) => cat.id === id)
      if (index !== -1) {
        categories.value.splice(index, 1)
      }

      showToast('Catégorie supprimée !', 'success')
    } catch (err: any) {
      console.error('Erreur lors de la suppression:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    categories,
    loading,
    error,

    // Actions
    fetchCategories,
    createCategory,
    updateCategory,
    deleteCategory,
  }
})
