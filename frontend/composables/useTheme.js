import { ref, onMounted } from 'vue'

const STORAGE_KEY = 'skepcamp_theme'

export function useTheme() {
  const theme = ref('dark')

  function getStoredTheme() {
    return localStorage.getItem(STORAGE_KEY)
  }

  function applyTheme(value) {
    const html = document.documentElement
    html.classList.remove('dark', 'light')
    html.classList.add(value)
    localStorage.setItem(STORAGE_KEY, value)
    theme.value = value
  }

  function toggle() {
    applyTheme(theme.value === 'dark' ? 'light' : 'dark')
  }

  onMounted(() => {
    const stored = getStoredTheme()
    const preferred = stored || (
      window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    )
    theme.value = preferred
    // Don't re-apply — inline script in base.html already set the class.
  })

  return { theme, toggle, applyTheme }
}
