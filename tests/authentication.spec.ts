import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('Login Page Display', async ({ page }) => {
    await page.goto('/accounts/login/');
    
    // Verify login page elements
    await expect(page.locator('h1')).toContainText('StoreLoop');
    await expect(page.locator('h2')).toContainText('Login to Your Store');
    
    // Check form fields
    await expect(page.locator('input[name="username"]')).toBeVisible();
    await expect(page.locator('input[name="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
    
    // Check demo credentials display
    await expect(page.locator('text=Demo Accounts')).toBeVisible();
    await expect(page.locator('text=admin / admin123')).toBeVisible();
    await expect(page.locator('text=ngo_admin / password')).toBeVisible();
  });

  test('Successful Admin Login', async ({ page }) => {
    await page.goto('/accounts/login/');
    
    // Fill login form
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button[type="submit"]');
    
    // Should redirect to onboarding or dashboard
    await expect(page).toHaveURL(/\/stores\/(onboarding|dashboard)\//);
  });

  test('Successful NGO Admin Login', async ({ page }) => {
    await page.goto('/accounts/login/');
    
    // Fill login form
    await page.fill('input[name="username"]', 'ngo_admin');
    await page.fill('input[name="password"]', 'password');
    await page.click('button[type="submit"]');
    
    // Should redirect to partner dashboard
    await expect(page).toHaveURL(/\/stores\/partner-dashboard\//);
  });

  test('Invalid Login Credentials', async ({ page }) => {
    await page.goto('/accounts/login/');
    
    // Try invalid credentials
    await page.fill('input[name="username"]', 'invalid');
    await page.fill('input[name="password"]', 'wrong');
    await page.click('button[type="submit"]');
    
    // Should stay on login page with error
    await expect(page).toHaveURL(/\/accounts\/login\//);
    
    // Check for error message (if displayed)
    const errorMessage = page.locator('.errorlist').first();
    if (await errorMessage.count() > 0) {
      await expect(errorMessage).toBeVisible();
    }
  });

  test('Empty Login Form', async ({ page }) => {
    await page.goto('/accounts/login/');
    
    // Try to submit empty form
    await page.click('button[type="submit"]');
    
    // Should stay on login page
    await expect(page).toHaveURL(/\/accounts\/login\//);
    
    // Check for HTML5 validation or error messages
    const usernameField = page.locator('input[name="username"]');
    const passwordField = page.locator('input[name="password"]');
    
    // Fields should be required
    await expect(usernameField).toHaveAttribute('required');
    await expect(passwordField).toHaveAttribute('required');
  });

  test('Logout Functionality', async ({ page }) => {
    // Login first
    await page.goto('/accounts/login/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button[type="submit"]');
    
    // Navigate to dashboard
    await page.goto('/stores/dashboard/');
    
    // Logout
    await page.click('a:has-text("Logout")');
    await expect(page).toHaveURL(/\/accounts\/logout\//);
    
    // Verify logged out by trying to access protected page
    await page.goto('/stores/dashboard/');
    await expect(page).toHaveURL(/\/accounts\/login\//);
  });

  test('Protected Route Access', async ({ page }) => {
    // Try to access protected routes without login
    const protectedRoutes = [
      '/stores/dashboard/',
      '/stores/onboarding/',
      '/stores/partner-dashboard/',
      '/stores/products/add/',
      '/stores/products/upload/'
    ];
    
    for (const route of protectedRoutes) {
      await page.goto(route);
      // Should redirect to login
      await expect(page).toHaveURL(/\/accounts\/login\//);
    }
  });

  test('Login Form Styling', async ({ page }) => {
    await page.goto('/accounts/login/');
    
    // Check form styling
    const form = page.locator('form');
    await expect(form).toBeVisible();
    
    // Check button styling
    const submitButton = page.locator('button[type="submit"]');
    const buttonStyle = await submitButton.getAttribute('style');
    expect(buttonStyle).toContain('#3B82F6'); // Blue color
    
    // Check input field styling
    const usernameInput = page.locator('input[name="username"]');
    const inputStyle = await usernameInput.getAttribute('style');
    expect(inputStyle).toContain('padding');
  });

  test('Login Page Mobile Responsiveness', async ({ page, isMobile }) => {
    if (!isMobile) {
      await page.setViewportSize({ width: 375, height: 667 });
    }
    
    await page.goto('/accounts/login/');
    
    // Verify mobile layout
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator('form')).toBeVisible();
    
    // Check form width on mobile
    const form = page.locator('form').locator('..');
    const formStyle = await form.getAttribute('style');
    expect(formStyle).toContain('max-width');
    
    // Test form interaction on mobile
    await page.fill('input[name="username"]', 'test');
    await page.fill('input[name="password"]', 'test');
    
    // Button should be touch-friendly
    const button = page.locator('button[type="submit"]');
    const buttonBox = await button.boundingBox();
    expect(buttonBox?.height).toBeGreaterThan(40);
  });

  test('Session Persistence', async ({ page }) => {
    // Login
    await page.goto('/accounts/login/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button[type="submit"]');
    
    // Navigate away and back
    await page.goto('/');
    await page.goto('/stores/dashboard/');
    
    // Should still be logged in
    await expect(page).toHaveURL(/\/stores\/dashboard\//);
    await expect(page.locator('h1')).toContainText('Dashboard');
  });
});