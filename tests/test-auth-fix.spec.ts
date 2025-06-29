import { test, expect } from './fixtures/auth';

test.describe('Auth Fix Test - Chromium Only', () => {
  test('Dashboard loads correctly after login', async ({ page, adminUser }) => {
    await page.goto('/stores/dashboard/');
    
    // Should be on dashboard
    await expect(page).toHaveURL(/\/stores\/dashboard\//);
    
    // Should see dashboard elements
    await expect(page.locator('text=Total Orders')).toBeVisible();
    await expect(page.locator('text=Total Sales')).toBeVisible();
  });
});