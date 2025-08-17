import { format, parseISO, formatDistanceToNow, isAfter } from 'date-fns'
import { fr } from 'date-fns/locale'

export function formatDate(dateString: string): string {
  try {
    const date = parseISO(dateString)
    return format(date, 'dd/MM/yyyy', { locale: fr })
  } catch (error) {
    return dateString
  }
}

export function formatDateTime(dateString: string): string {
  try {
    const date = parseISO(dateString)
    return format(date, 'dd/MM/yyyy à HH:mm', { locale: fr })
  } catch (error) {
    return dateString
  }
}

export function formatRelativeDate(dateString: string): string {
  try {
    const date = parseISO(dateString)
    return formatDistanceToNow(date, { addSuffix: true, locale: fr })
  } catch (error) {
    return dateString
  }
}

export function isDateInFuture(dateString: string): boolean {
  try {
    const date = parseISO(dateString)
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    return isAfter(date, today)
  } catch (error) {
    return false
  }
}

export function capitalizeFirstLetter(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase()
}

export function truncateText(text: string, maxLength: number = 100): string {
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength) + '...'
}
