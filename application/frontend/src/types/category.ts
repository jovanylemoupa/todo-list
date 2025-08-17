export interface Category {
  id: number
  name: string
  description?: string
  color?: string
  task_count?: number
  created_at: string
  updated_at: string
}

export interface CreateCategoryRequest {
  name: string
  description?: string
  color?: string
}

export interface UpdateCategoryRequest {
  name?: string
  description?: string
  color?: string
}
