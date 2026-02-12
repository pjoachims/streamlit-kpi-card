import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    outDir: 'build',
    rollupOptions: {
      output: {
        manualChunks: {
          // Split recharts into separate chunk for parallel loading & caching
          recharts: ['recharts', 'd3-shape', 'd3-scale', 'd3-interpolate', 'd3-color', 'd3-format', 'd3-time', 'd3-time-format', 'd3-path', 'd3-array'],
        }
      }
    }
  },
  test: {
    environment: 'jsdom',
  },
  server: {
    port: 3001
  }
})
