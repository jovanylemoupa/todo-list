import { ref, reactive, computed } from 'vue'

export interface ValidationRule {
  (value: any): string | true
}

export interface ValidationRules {
  [key: string]: ValidationRule[]
}

export interface ValidationErrors {
  [key: string]: string
}

export function useValidation() {
  const errors = reactive<ValidationErrors>({})
  const isValidating = ref(false)

  const rules = {
    required:
      (message = 'Ce champ est obligatoire'): ValidationRule =>
      (value: any) => {
        return value && value.toString().trim() !== '' ? true : message
      },

    minLength:
      (min: number, message?: string): ValidationRule =>
      (value: string) => {
        if (!value) return true
        return value.length >= min ? true : message || `Minimum ${min} caractères`
      },

    maxLength:
      (max: number, message?: string): ValidationRule =>
      (value: string) => {
        if (!value) return true
        return value.length <= max ? true : message || `Maximum ${max} caractères`
      },

    futureDate:
      (message = 'La date doit être dans le futur'): ValidationRule =>
      (value: string) => {
        if (!value) return true
        const date = new Date(value)
        const today = new Date()
        today.setHours(0, 0, 0, 0)
        return date > today ? true : message
      },

    email:
      (message = 'Format email invalide'): ValidationRule =>
      (value: string) => {
        if (!value) return true
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        return emailRegex.test(value) ? true : message
      },
  }

  const validateField = (field: string, value: any, fieldRules: ValidationRule[]): boolean => {
    delete errors[field]

    for (const rule of fieldRules) {
      const result = rule(value)
      if (result !== true) {
        errors[field] = result
        return false
      }
    }

    return true
  }

  const validateForm = (data: Record<string, any>, schema: ValidationRules): boolean => {
    isValidating.value = true
    let isValid = true

    // Clear previous errors
    Object.keys(errors).forEach((key) => delete errors[key])

    // Validate each field
    for (const [field, fieldRules] of Object.entries(schema)) {
      const fieldValid = validateField(field, data[field], fieldRules)
      if (!fieldValid) {
        isValid = false
      }
    }

    isValidating.value = false
    return isValid
  }

  const clearErrors = (): void => {
    Object.keys(errors).forEach((key) => delete errors[key])
  }

  const hasErrors = computed(() => Object.keys(errors).length > 0)

  return {
    errors,
    isValidating,
    rules,
    validateField,
    validateForm,
    clearErrors,
    hasErrors,
  }
}
