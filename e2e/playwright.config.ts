import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: false, // Run tests sequentially due to rate limiting
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1, // Force single worker to prevent rate limiting issues
  reporter: process.env.CI ? 'html' : 'list',
  use: {
    baseURL: process.env.PLAYWRIGHT_TEST_BASE_URL || 'http://localhost',
    trace: 'retain-on-failure',
    video: 'retain-on-failure',
    headless: true,
    // Increase timeouts for rate-limited operations
    actionTimeout: 15000,
    navigationTimeout: 15000,
  },
  timeout: 60000, // Global timeout per test
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: process.env.CI ? undefined : {
    command: 'docker compose up --build',
    url: 'http://localhost',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
