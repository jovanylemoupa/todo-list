import apiService from './api.service'
import type { Category, CreateCategoryRequest } from '@/types/category'

export const categoriesService = {
  async getCategories(): Promise<Category[]> {
    return await apiService.get<Category[]>('/categories/')
  },

  async getCategory(id: number): Promise<Category> {
    return await apiService.get<Category>(`/categories/${id}/`)
  },

  async createCategory(categoryData: CreateCategoryRequest): Promise<Category> {
    return await apiService.post<Category>('/categories/', categoryData)
  },

  async updateCategory(
    id: number,
    categoryData: Partial<CreateCategoryRequest>,
  ): Promise<Category> {
    return await apiService.put<Category>(`/categories/${id}/`, categoryData)
  },

  async deleteCategory(id: number): Promise<void> {
    return await apiService.delete<void>(`/categories/${id}/`)
  },
}
