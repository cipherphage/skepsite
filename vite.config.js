import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: 'static/dist',
    manifest: true,
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'frontend/main.js'),
      }
    }
  },
  server: {
    port: 5173,
    origin: 'http://localhost:5173',
  }
})
