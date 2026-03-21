import { ref } from 'vue'

let nextId = 0
const toasts = ref([])

export function useToast() {
  function add({ type = 'info', title, message, duration }) {
    const id = ++nextId
    const toast = { id, type, title, message }

    // Default durations: success/info = 5s, error/warning = persist (10s)
    const autoClose = duration ?? (type === 'error' || type === 'warning' ? 10000 : 5000)

    toasts.value.push(toast)

    if (autoClose > 0) {
      setTimeout(() => remove(id), autoClose)
    }

    return id
  }

  function remove(id) {
    const idx = toasts.value.findIndex((t) => t.id === id)
    if (idx !== -1) toasts.value.splice(idx, 1)
  }

  function success(title, message) {
    return add({ type: 'success', title, message })
  }

  function error(title, message) {
    return add({ type: 'error', title, message })
  }

  function info(title, message) {
    return add({ type: 'info', title, message })
  }

  function warning(title, message) {
    return add({ type: 'warning', title, message })
  }

  return { toasts, add, remove, success, error, info, warning }
}
