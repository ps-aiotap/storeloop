import { test as base, expect } from '@playwright/test';
import { exec } from 'child_process';
import { promisify } from 'util';

// Set default timeout for auth fixtures
base.setTimeout(60000);

const execAsync = promisify(exec);

type AuthFixtures = {
  adminUser: void;
  ngoUser: void;
};

export const test = base.extend<AuthFixtures>({
  adminUser: async ({ page }, use) => {
    // Reset admin user and create store
    try {
      await execAsync('python manage.py reset_admin', { cwd: 'C:\\Data\\vagrant\\code\\storeloop', timeout: 10000 });
    } catch (e) {}
    
    // Login and complete onboarding
    await page.goto('/accounts/login/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button[type="submit"]');
    // Wait for any redirect to complete
    await page.waitForTimeout(3000);
    
    // If not on dashboard, might be on onboarding - complete it
    if (!page.url().includes('/dashboard/')) {
      await page.goto('/stores/dashboard/');
    }
    

    
    await use();
  },

  ngoUser: async ({ page }, use) => {
    // Login as NGO partner admin with retry logic
    let loginAttempts = 0;
    const maxAttempts = 3;
    
    while (loginAttempts < maxAttempts) {
      try {
        await page.goto('/accounts/login/', { timeout: 30000 });
        await page.fill('input[name="username"]', 'ngo_admin');
        await page.fill('input[name="password"]', 'password');
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL(/\/stores\/partner-dashboard\//, { timeout: 15000 });
        break;
      } catch (e) {
        loginAttempts++;
        if (loginAttempts >= maxAttempts) {
          throw e;
        }
        await page.waitForTimeout(2000);
      }
    }
    
    await use();
  },
});

export { expect } from '@playwright/test';