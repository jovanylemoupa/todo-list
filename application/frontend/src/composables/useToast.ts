import { Toast, ToastType } from '@/types/toast.types'
import { ref } from 'vue'

const toasts = ref<Toast[]>([])

export function useToast() {
  const showToast = (message: string, type: ToastType = 'info', duration: number = 4000) => {
    const id = Math.random().toString(36).substr(2, 9)
    const toast: Toast = {
      id,
      message,
      type,
      duration,
    }

    toasts.value.push(toast)

    // Auto remove after duration
    if (duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, duration)
    }

    return id
  }

  const removeToast = (id: string) => {
    const index = toasts.value.findIndex((toast) => toast.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  const clearToasts = () => {
    toasts.value = []
  }

  return {
    toasts,
    showToast,
    removeToast,
    clearToasts,
  }
}

export type { ToastType }
