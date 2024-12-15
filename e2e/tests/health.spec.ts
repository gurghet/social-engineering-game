import { test, expect } from '@playwright/test';

test.describe('Health Checks', () => {
  test('frontend health check should return healthy', async ({ request }) => {
    const response = await request.get('/health');
    expect(response.ok()).toBeTruthy();
    expect(await response.text()).toBe('healthy\n');
  });

  test('backend health check should return healthy', async ({ request }) => {
    const response = await request.get('/api/health');
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data).toEqual({ status: 'healthy' });
  });
});
