import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: process.env.NODE_ENV === 'development' ? 'http://localhost:23925' : 'http://backend',
        changeOrigin: true
      }
    }
  }
})
