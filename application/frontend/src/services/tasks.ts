import apiService from './api'
import type {
  Task,
  CreateTaskRequest,
  UpdateTaskRequest,
  TasksResponse,
  TaskFilters,
  TaskSort,
  Pagination,
} from '@/types/task'

export interface TaskQueryParams
  extends Partial<TaskFilters>,
    Partial<TaskSort>,
    Partial<Pagination> {}

export const tasksService = {
  // ✅ Ajouter trailing slash pour éviter les redirections 307
  async getTasks(params: TaskQueryParams = {}): Promise<TasksResponse> {
    // Nettoyer les paramètres vides
    const cleanParams = Object.entries(params).reduce(
      (acc, [key, value]) => {
        if (value !== null && value !== undefined && value !== '') {
          acc[key] = value
        }
        return acc
      },
      {} as Record<string, any>,
    )

    return await apiService.get<TasksResponse>('/tasks/', { params: cleanParams }) // ✅ /tasks/ au lieu de /tasks
  },

  async getTask(id: number): Promise<Task> {
    return await apiService.get<Task>(`/tasks/${id}/`) // ✅ Ajouter trailing slash
  },

  async createTask(taskData: CreateTaskRequest): Promise<Task> {
    return await apiService.post<Task>('/tasks/', taskData) // ✅ /tasks/ au lieu de /tasks
  },

  async updateTask(id: number, taskData: UpdateTaskRequest): Promise<Task> {
    return await apiService.put<Task>(`/tasks/${id}/`, taskData) // ✅ Ajouter trailing slash
  },

  async deleteTask(id: number): Promise<void> {
    return await apiService.delete<void>(`/tasks/${id}/`) // ✅ Ajouter trailing slash
  },

  async completeTask(id: number): Promise<Task> {
    return await apiService.patch<Task>(`/tasks/${id}/complete/`) // ✅ Ajouter trailing slash
  },

  async searchTasks(query: string): Promise<Task[]> {
    if (query.trim().length < 2) {
      return []
    }
    return await apiService.get<Task[]>('/tasks/search/', { params: { q: query } }) // ✅ OK déjà
  },

  async getUrgentTasks(): Promise<Task[]> {
    return await apiService.get<Task[]>('/tasks/urgent/list/') // ✅ Ajouter trailing slash
  },

  async getStatistics(): Promise<any> {
    return await apiService.get<any>('/tasks/statistics/') // ✅ OK déjà
  },

  async reorderTasks(taskIds: number[], positions: number[]): Promise<void> {
    return await apiService.put<void>('/tasks/reorder/', {
      // ✅ OK déjà
      task_ids: taskIds,
      positions: positions,
    })
  },
}
