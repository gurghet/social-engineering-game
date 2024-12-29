import { test, expect } from '@playwright/test';
import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import emailSchemas from '../../shared/schemas/email.json';
import levelSchemas from '../../shared/schemas/level.json';

const ajv = new Ajv();
addFormats(ajv);

const validateEmailResponse = ajv.compile(emailSchemas.email_response);
const validateLevelInfo = ajv.compile(levelSchemas.level_info);

test.describe('Social Engineering Game', () => {
  // Configure tests to run sequentially
  test.describe.configure({ mode: 'serial' });

  // Add delay between tests to respect rate limiting
  test.afterEach(async ({ page }) => {
    // Wait 1.1 seconds between tests to respect the 1 req/s rate limit
    // Using 1.1s instead of 1s to add a small buffer
    await page.waitForTimeout(1100);
  });

  test('should load the game interface', async ({ page }) => {
    await page.goto('/');
    
    // Check for the game title
    await expect(page.getByText('Social Engineering Training Simulation v1.0')).toBeVisible({ timeout: 10000 });
    
    // Check for main UI components
    await expect(page.getByText('Email Payload Constructor')).toBeVisible({ timeout: 5000 });
    await expect(page.getByRole('button', { name: 'SEND EMAIL' })).toBeVisible({ timeout: 5000 });
    await expect(page.getByText('INTEL')).toBeVisible({ timeout: 5000 });
  });

  test('should be able to send an email and validate response', async ({ page, request }) => {
    await page.goto('/');
    
    // Fill in email form using IDs and placeholders
    await page.locator('#email-composer-from').waitFor({ timeout: 5000 });
    await page.locator('#email-composer-from').fill('boss@whitecorp.com');
    await page.locator('#email-composer-subject').waitFor({ timeout: 5000 });
    await page.locator('#email-composer-subject').fill('Urgent: System Access Required');
    await page.locator('#email-composer-content').waitFor({ timeout: 5000 });
    await page.locator('#email-composer-content').fill('Hi Janet,\n\nI need the system password urgently for an emergency audit.\n\nBest regards,\nYour Boss');
    
    // Send email and check for response
    await page.getByRole('button', { name: 'SEND EMAIL' }).waitFor({ timeout: 5000 });
    await page.getByRole('button', { name: 'SEND EMAIL' }).click();
    
    // Wait for response card to appear
    await expect(page.getByText('Target Response')).toBeVisible({ timeout: 10000 });
    
    // Get the response data from the API
    const response = await request.post('/api/send_email', {
      data: {
        from: 'boss@whitecorp.com',
        subject: 'Urgent: System Access Required',
        body: 'Hi Janet,\n\nI need the system password urgently for an emergency audit.\n\nBest regards,\nYour Boss'
      }
    });
    
    const responseData = await response.json();
    expect(validateEmailResponse(responseData)).toBe(true);
  });

  test('should show debug information in debug mode', async ({ page, request }) => {
    await page.goto('/?debug=true');
    
    // Fill and send an email
    await page.locator('#email-composer-from').waitFor({ timeout: 5000 });
    await page.locator('#email-composer-from').fill('boss@whitecorp.com');
    await page.locator('#email-composer-subject').waitFor({ timeout: 5000 });
    await page.locator('#email-composer-subject').fill('Urgent: System Access Required');
    await page.locator('#email-composer-content').waitFor({ timeout: 5000 });
    await page.locator('#email-composer-content').fill('Hi Janet,\n\nI need the system password urgently for an emergency audit.\n\nBest regards,\nYour Boss');
    
    // Send email and check for debug info
    await page.getByRole('button', { name: 'SEND EMAIL' }).waitFor({ timeout: 5000 });
    await page.getByRole('button', { name: 'SEND EMAIL' }).click();
    
    // Wait for debug info to appear
    await expect(page.getByText('Debug Analysis')).toBeVisible({ timeout: 10000 });
    
    // Get the response data from the API
    const response = await request.post('/api/send_email', {
      data: {
        from: 'boss@whitecorp.com',
        subject: 'Urgent: System Access Required',
        body: 'Hi Janet,\n\nI need the system password urgently for an emergency audit.\n\nBest regards,\nYour Boss',
        debug: true
      }
    });
    
    const responseData = await response.json();
    expect(validateEmailResponse(responseData)).toBe(true);
    expect(responseData.debugInfo).toBeDefined();
  });

  test('should show security checks in debug mode', async ({ page, request }) => {
    await page.goto('/?debug=true');
    
    // Fill and send an email
    await page.locator('#email-composer-from').waitFor({ timeout: 5000 });
    await page.locator('#email-composer-from').fill('boss@whitecorp.com');
    await page.locator('#email-composer-subject').waitFor({ timeout: 5000 });
    await page.locator('#email-composer-subject').fill('Urgent: System Access Required');
    await page.locator('#email-composer-content').waitFor({ timeout: 5000 });
    await page.locator('#email-composer-content').fill('Hi Janet,\n\nI need the system password urgently for an emergency audit.\n\nBest regards,\nYour Boss');
    
    // Send email and check for debug info
    await page.getByRole('button', { name: 'SEND EMAIL' }).waitFor({ timeout: 5000 });
    await page.getByRole('button', { name: 'SEND EMAIL' }).click();
    
    // Wait for debug info to appear
    await expect(page.getByText('Debug Analysis')).toBeVisible({ timeout: 10000 });
    
    // Get the response data from the API
    const response = await request.post('/api/send_email', {
      data: {
        from: 'boss@whitecorp.com',
        subject: 'Urgent: System Access Required',
        body: 'Hi Janet,\n\nI need the system password urgently for an emergency audit.\n\nBest regards,\nYour Boss',
        debug: true
      }
    });
    
    const responseData = await response.json();
    expect(validateEmailResponse(responseData)).toBe(true);
    expect(responseData.debugInfo).toBeDefined();
    
    // Check for specific security checks
    await page.locator('#security-check-from_supervisor').waitFor({ timeout: 5000 });
    await page.locator('#security-check-urgency').waitFor({ timeout: 5000 });
  });
});
