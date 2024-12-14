import { test, expect } from '@playwright/test';

test.describe('Social Engineering Game', () => {
  test('should load the game interface', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByText('Social Engineering Training Simulation')).toBeVisible();
  });

  test('should be able to send an email', async ({ page }) => {
    await page.goto('/');
    
    // Fill in email form
    await page.getByLabel('From:').fill('boss@whitecorp.com');
    await page.getByLabel('Subject:').fill('Urgent: System Access Required');
    await page.getByLabel('Content:').fill('Hi Janet,\n\nI need the system password urgently for an emergency audit.\n\nBest regards,\nYour Boss');
    
    // Send email
    await page.getByRole('button', { name: 'Send Email' }).click();
    
    // Wait for response
    await expect(page.getByText(/Dear/)).toBeVisible({ timeout: 10000 });
  });

  test('should show security checks in debug mode', async ({ page }) => {
    // Enable debug mode via URL parameter
    await page.goto('/?debug=true');
    
    // Verify debug mode indicator
    await expect(page.getByText('[DEBUG MODE]')).toBeVisible();
    
    // Send an email
    await page.getByLabel('From:').fill('boss@whitecorp.com');
    await page.getByLabel('Subject:').fill('Test Email');
    await page.getByLabel('Content:').fill('Test content');
    await page.getByRole('button', { name: 'Send Email' }).click();
    
    // Check for security checks in response
    await expect(page.getByText(/security_checks/)).toBeVisible({ timeout: 10000 });
  });
});
