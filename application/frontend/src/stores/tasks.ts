import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type {
  Task,
  CreateTaskRequest,
  UpdateTaskRequest,
  TaskFilters,
  TaskSort,
  Pagination,
} from '@/types/task'
import { tasksService } from '@/services/tasks.service'
import { useToast } from '@/composables/useToast'

export const useTasksStore = defineStore('tasks', () => {
  const { showToast } = useToast()

  // State
  const tasks = ref<Task[]>([])
  const currentTask = ref<Task | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const filters = ref<TaskFilters>({
    category_id: undefined,
    priority: undefined,
    status: undefined,
    search: '',
  })

  const sort = ref<TaskSort>({
    field: 'due_date',
    order: 'asc',
  })

  const pagination = ref<Pagination>({
    page: 1,
    size: 20,
    total: 0,
    pages: 0,
  })

  // Getters
  const filteredTasks = computed(() => {
    let result = tasks.value

    if (filters.value.search) {
      const searchTerm = filters.value.search.toLowerCase()
      result = result.filter(
        (task) =>
          task.title.toLowerCase().includes(searchTerm) ||
          (task.description && task.description.toLowerCase().includes(searchTerm)),
      )
    }

    return result
  })

  const urgentTasks = computed(() =>
    tasks.value.filter((task) => task.is_urgent && task.status !== 'Terminée'),
  )

  const overdueTasks = computed(() =>
    tasks.value.filter((task) => task.is_overdue && task.status !== 'Terminée'),
  )

  const completedTasks = computed(() => tasks.value.filter((task) => task.status === 'Terminée'))

  const tasksByPriority = computed(() => {
    const grouped: Record<string, Task[]> = { Haute: [], Moyenne: [], Basse: [] }
    tasks.value.forEach((task) => {
      if (grouped[task.priority]) {
        grouped[task.priority].push(task)
      }
    })
    return grouped
  })

  // Actions
  const fetchTasks = async (params: Partial<TaskFilters & TaskSort & Pagination> = {}) => {
    loading.value = true
    error.value = null

    try {
      const queryParams = {
        ...filters.value,
        sort_by: sort.value.field,
        sort_order: sort.value.order,
        page: pagination.value.page,
        size: pagination.value.size,
        ...params,
      }

      const response = await tasksService.getTasks(queryParams)

      tasks.value = response.items
      pagination.value = {
        page: response.page,
        size: response.size,
        total: response.total,
        pages: response.pages,
      }
    } catch (err: any) {
      error.value = err.message
      console.error('Erreur lors du chargement des tâches:', err)
    } finally {
      loading.value = false
    }
  }

  const createTask = async (taskData: CreateTaskRequest): Promise<Task> => {
    loading.value = true

    try {
      const newTask = await tasksService.createTask(taskData)
      tasks.value.unshift(newTask)
      pagination.value.total += 1

      showToast('Tâche créée avec succès !', 'success')
      return newTask
    } catch (err: any) {
      console.error('Erreur lors de la création:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateTask = async (id: number, taskData: UpdateTaskRequest): Promise<Task> => {
    loading.value = true

    try {
      const updatedTask = await tasksService.updateTask(id, taskData)

      const index = tasks.value.findIndex((task) => task.id === id)
      if (index !== -1) {
        tasks.value[index] = updatedTask
      }

      showToast('Tâche mise à jour !', 'success')
      return updatedTask
    } catch (err: any) {
      console.error('Erreur lors de la mise à jour:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteTask = async (id: number): Promise<void> => {
    loading.value = true

    try {
      await tasksService.deleteTask(id)

      const index = tasks.value.findIndex((task) => task.id === id)
      if (index !== -1) {
        tasks.value.splice(index, 1)
        pagination.value.total -= 1
      }

      showToast('Tâche supprimée !', 'success')
    } catch (err: any) {
      console.error('Erreur lors de la suppression:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const completeTask = async (id: number): Promise<Task> => {
    try {
      const completedTask = await tasksService.completeTask(id)

      const index = tasks.value.findIndex((task) => task.id === id)
      if (index !== -1) {
        tasks.value[index] = completedTask
      }

      showToast('Tâche terminée !', 'success')
      return completedTask
    } catch (err: any) {
      console.error('Erreur lors de la completion:', err)
      throw err
    }
  }

  const setFilters = (newFilters: Partial<TaskFilters>): void => {
    filters.value = { ...filters.value, ...newFilters }
    pagination.value.page = 1
  }

  const setSort = (field: TaskSort['field'], order: TaskSort['order'] = 'asc'): void => {
    sort.value = { field, order }
    pagination.value.page = 1
  }

  const resetFilters = (): void => {
    filters.value = {
      category_id: undefined,
      priority: undefined,
      status: undefined,
      search: '',
    }
    pagination.value.page = 1
  }

  return {
    // State
    tasks,
    currentTask,
    loading,
    error,
    filters,
    sort,
    pagination,

    // Getters
    filteredTasks,
    urgentTasks,
    overdueTasks,
    completedTasks,
    tasksByPriority,

    // Actions
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    completeTask,
    setFilters,
    setSort,
    resetFilters,
  }
})
