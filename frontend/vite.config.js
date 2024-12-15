import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const apiTargets = {
  e2e: 'http://server:8080',
  development: 'http://localhost:23925',
  production: 'http://backend'
}

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: apiTargets[process.env.NODE_ENV] || apiTargets.production,
        changeOrigin: true
      }
    }
  }
})
