import type { Priority, TaskStatus } from '@/types/task'

export const PRIORITIES: Priority[] = ['Haute', 'Moyenne', 'Basse']

export const TASK_STATUSES: TaskStatus[] = ['En attente', 'En cours', 'Terminée']

export const PRIORITY_COLORS = {
  Haute: '#ef4444',
  Moyenne: '#f59e0b',
  Basse: '#10b981',
} as const

export const STATUS_COLORS = {
  'En attente': '#6b7280',
  'En cours': '#3b82f6',
  Terminée: '#10b981',
} as const
