import apiService from './api.service.ts'
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

    return await apiService.get<TasksResponse>('/tasks/', { params: cleanParams })
  },

  async getTask(id: number): Promise<Task> {
    return await apiService.get<Task>(`/tasks/${id}/`)
  },

  async createTask(taskData: CreateTaskRequest): Promise<Task> {
    return await apiService.post<Task>('/tasks/', taskData)
  },

  async updateTask(id: number, taskData: UpdateTaskRequest): Promise<Task> {
    return await apiService.put<Task>(`/tasks/${id}/`, taskData)
  },

  async deleteTask(id: number): Promise<void> {
    return await apiService.delete<void>(`/tasks/${id}/`)
  },

  async completeTask(id: number): Promise<Task> {
    return await apiService.patch<Task>(`/tasks/${id}/complete/`)
  },

  async searchTasks(query: string): Promise<Task[]> {
    if (query.trim().length < 2) {
      return []
    }
    return await apiService.get<Task[]>('/tasks/search/', { params: { q: query } })
  },

  async getUrgentTasks(): Promise<Task[]> {
    return await apiService.get<Task[]>('/tasks/urgent/list/')
  },

  async getOverdueTasks(): Promise<Task[]> {
    return await apiService.get<Task[]>('/tasks/overdue/list/')
  },

  async getStatistics(): Promise<any> {
    return await apiService.get<any>('/tasks/statistics/')
  },

  async reorderTasks(taskIds: number[], positions: number[]): Promise<void> {
    return await apiService.put<void>('/tasks/reorder/', {
      task_ids: taskIds,
      positions: positions,
    })
  },
}
