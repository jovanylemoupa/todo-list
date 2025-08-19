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

  const tasks = ref<Task[]>([])
  const searchResults = ref<Task[]>([])
  const isSearching = ref(false)
  const currentTask = ref<Task | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const urgentTasksData = ref<Task[]>([])
  const overdueTasksData = ref<Task[]>([])
  const statistics = ref<any>(null)

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

  const filteredTasks = computed(() => {
    if (isSearching.value) {
      return searchResults.value
    }
    return tasks.value
  })

  const urgentTasks = computed(() => {
    return urgentTasksData.value.length > 0
      ? urgentTasksData.value
      : tasks.value.filter((task) => task.is_urgent && task.status !== 'Terminée')
  })

  const overdueTasks = computed(() => {
    return overdueTasksData.value.length > 0
      ? overdueTasksData.value
      : tasks.value.filter((task) => task.is_overdue && task.status !== 'Terminée')
  })

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
        search: undefined,
      }

      const response = await tasksService.getTasks(queryParams)

      tasks.value = response.items
      pagination.value = {
        page: response.page,
        size: response.size,
        total: response.total,
        pages: response.pages,
      }

      isSearching.value = false
      searchResults.value = []
    } catch (err: any) {
      error.value = err.message
      console.error('Erreur lors du chargement des tâches:', err)
    } finally {
      loading.value = false
    }
  }

  const searchTasks = async (query: string) => {
    if (query.length < 2) {
      isSearching.value = false
      searchResults.value = []
      filters.value.search = ''
      await fetchTasks()
      return
    }

    try {
      loading.value = true
      isSearching.value = true

      const results = await tasksService.searchTasks(query)
      searchResults.value = results
      filters.value.search = query
    } catch (err: any) {
      console.error('Erreur recherche:', err)
    } finally {
      loading.value = false
    }
  }

  const createTask = async (taskData: CreateTaskRequest): Promise<Task> => {
    loading.value = true

    try {
      const newTask = await tasksService.createTask(taskData)

      await refreshPermanentData()

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

      await refreshPermanentData()

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

      await refreshPermanentData()

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

      await refreshPermanentData()

      showToast('Tâche terminée !', 'success')
      return completedTask
    } catch (err: any) {
      console.error('Erreur lors de la completion:', err)
      throw err
    }
  }

  const setFilters = async (newFilters: Partial<TaskFilters>): Promise<void> => {
    filters.value = { ...filters.value, ...newFilters }
    pagination.value.page = 1

    isSearching.value = false
    searchResults.value = []

    await fetchTasks()
  }

  const setSort = async (
    field: TaskSort['field'],
    order: TaskSort['order'] = 'asc',
  ): Promise<void> => {
    sort.value = { field, order }
    pagination.value.page = 1

    isSearching.value = false
    searchResults.value = []

    await fetchTasks()
  }

  const resetFilters = async (): Promise<void> => {
    filters.value = {
      category_id: undefined,
      priority: undefined,
      status: undefined,
      search: '',
    }
    pagination.value.page = 1

    isSearching.value = false
    searchResults.value = []

    await fetchTasks()
  }

  const fetchUrgentTasks = async () => {
    try {
      urgentTasksData.value = await tasksService.getUrgentTasks()
    } catch (err: any) {
      console.error('Erreur tâches urgentes:', err)
    }
  }

  const fetchOverdueTasks = async () => {
    try {
      overdueTasksData.value = await tasksService.getOverdueTasks()
    } catch (err: any) {
      console.error('Erreur tâches en retard:', err)
    }
  }

  const fetchStatistics = async () => {
    try {
      statistics.value = await tasksService.getStatistics()
    } catch (err: any) {
      console.error('Erreur statistiques:', err)
    }
  }

  const reorderTasks = async (taskIds: number[], positions: number[]): Promise<void> => {
    try {
      await tasksService.reorderTasks(taskIds, positions)
      await fetchTasks()
      showToast('Tâches réorganisées !', 'success')
    } catch (err: any) {
      console.error('Erreur réorganisation:', err)
      throw err
    }
  }

  const refreshPermanentData = async () => {
    await Promise.all([
      fetchTasks(), // Liste principale
      fetchUrgentTasks(), // Tâches urgentes
      fetchOverdueTasks(), // Tâches en retard
      fetchStatistics(), // Statistiques
    ])
  }

  const initializeStore = async (): Promise<void> => {
    loading.value = true
    try {
      await refreshPermanentData()
    } catch (err: any) {
      console.error('Erreur initialisation:', err)
      error.value = 'Erreur lors du chargement initial'
    } finally {
      loading.value = false
    }
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
    statistics,
    isSearching,

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
    searchTasks,
    fetchUrgentTasks,
    fetchOverdueTasks,
    fetchStatistics,
    reorderTasks,
    initializeStore,
  }
})
