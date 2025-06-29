import { test as base, expect } from '@playwright/test';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

type OnboardingAuthFixtures = {
  newAdminUser: void;
};

export const test = base.extend<OnboardingAuthFixtures>({
  newAdminUser: async ({ page }, use) => {
    // Create fresh admin user without completed store
    try {
      await execAsync('python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username=\'newadmin\').delete(); User.objects.create_user(\'newadmin\', \'admin@test.com\', \'admin123\')"', { cwd: 'C:\\Data\\vagrant\\code\\storeloop', timeout: 10000 });
    } catch (e) {}
    
    // Login - should redirect to onboarding
    await page.goto('/accounts/login/');
    await page.fill('input[name="username"]', 'newadmin');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button[type="submit"]');
    await page.waitForURL(/\/stores\/onboarding\//, { timeout: 45000 });
    
    await use();
  },
});

export { expect } from '@playwright/test';