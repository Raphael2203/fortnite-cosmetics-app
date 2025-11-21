import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    // proxy helpful during development when frontend dev server runs on host
    proxy: {
      // forward API endpoints to backend (adjust target if your backend listens on a different host)
      '^/auth': { target: 'http://localhost:8000', changeOrigin: true, secure: false },
      '^/cosmetics': { target: 'http://localhost:8000', changeOrigin: true, secure: false },
      '^/purchases': { target: 'http://localhost:8000', changeOrigin: true, secure: false },
      '^/users': { target: 'http://localhost:8000', changeOrigin: true, secure: false },
    }
  }
})
