import { test, expect } from '@playwright/test';

// Get backend port from environment variable or use default
const BACKEND_PORT = process.env.BACKEND_PORT || '8080';

test.describe('Health Checks', () => {
  test('frontend health check should return healthy', async ({ request }) => {
    const response = await request.get('/health');
    expect(response.ok()).toBeTruthy();
    expect(await response.text()).toBe('healthy\n');
  });

  test('backend health check should return healthy', async ({ request }) => {
    const response = await request.fetch(`http://localhost:${BACKEND_PORT}/api/health`);
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data).toEqual({ status: 'healthy' });
  });
});