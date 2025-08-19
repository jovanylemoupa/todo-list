export interface Category {
  id: number
  name: string
  color: string
  description?: string
  created_at: string
  updated_at: string
}

export interface Task {
  id: number
  title: string
  description?: string
  category_id: number
  category?: Category
  priority: Priority
  due_date: string
  status: TaskStatus
  position: number
  is_urgent: boolean
  is_overdue: boolean
  created_at: string
  updated_at: string
}

export interface CreateTaskRequest {
  title: string
  description?: string
  category_id: number
  priority: Priority
  due_date: string
}

export interface UpdateTaskRequest {
  title?: string
  description?: string
  category_id?: number
  priority?: Priority
  due_date?: string
  status?: TaskStatus
}

export type Priority = 'Haute' | 'Moyenne' | 'Basse'
export type TaskStatus = 'En attente' | 'En cours' | 'Terminée'

export interface TaskFilters {
  category_id?: number
  priority?: Priority
  status?: TaskStatus
  search?: string
}

export interface TaskSort {
  field: 'due_date' | 'priority' | 'created_at' | 'title'
  order: 'asc' | 'desc'
}

export interface Pagination {
  page: number
  size: number
  total: number
  pages: number
}

export interface TasksResponse {
  items: Task[]
  page: number
  size: number
  total: number
  pages: number
}

export interface TaskStatistics {
  total_count: number
  completed_count: number
  pending_count: number
  in_progress_count: number
  urgent_count: number
  overdue_count: number
  high_priority_count: number
  medium_priority_count: number
  low_priority_count: number
}
