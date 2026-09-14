import { defineConfig } from 'vitest/config'
import path from 'node:path'

export default defineConfig({
  test: {
    // output JUnit XML for CI reporting
    reporters: [["junit", { outputFile: path.resolve(__dirname, "test-results/vitest-junit.xml") }]],
  },
})
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vitest/config'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
  },
})
