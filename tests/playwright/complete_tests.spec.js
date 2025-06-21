const { test, expect } = require('@playwright/test');

const testData = {
  valid: {
    username: 'testuser',
    password: 'testpass123',
    email: 'test@example.com',
    name: 'John Doe',
    phone: '+1234567890',
    message: 'Test message'
  },
  invalid: {
    email: ['invalid', 'test@', '@domain.com'],
    short: 'A',
    long: 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
    xss: '<script>alert("xss")</script>',
    sql: "'; DROP TABLE users; --"
  }
};

test.describe('Admin Page Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:8000/admin/login/?next=/admin/');
  });

  test('should submit login-form with valid data', async ({ page }) => {
    const form = page.locator('form').nth(0);
    await form.locator('[name="csrfmiddlewaretoken"]').fill(testvalue);
    await form.locator('#id_username').fill(testData.valid.username);
    await form.locator('#id_password').fill(testData.valid.password);
    await form.locator('[name="next"]').fill(testvalue);
    await form.locator('button[type="submit"], input[type="submit"]').click();
    await expect(page.locator('.success, .alert-success')).toBeVisible({ timeout: 5000 });
  });

  test('should validate required username field', async ({ page }) => {
    const form = page.locator('form').nth(0);
    await form.locator('button[type="submit"], input[type="submit"]').click();
    await expect(form.locator('#id_username:invalid')).toBeVisible();
  });

  test('should validate required password field', async ({ page }) => {
    const form = page.locator('form').nth(0);
    await form.locator('button[type="submit"], input[type="submit"]').click();
    await expect(form.locator('#id_password:invalid')).toBeVisible();
  });

  test('should handle XSS attempts in login-form', async ({ page }) => {
    const form = page.locator('form').nth(0);
    await form.locator('#id_username').fill(testData.invalid.xss);
    await form.locator('button[type="submit"], input[type="submit"]').click();
    
    const alerts = [];
    page.on('dialog', dialog => {
      alerts.push(dialog.message());
      dialog.dismiss();
    });
    
    await page.waitForTimeout(1000);
    expect(alerts).toHaveLength(0);
  });

});

test.describe('Login Page Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:8000/accounts/login/');
  });

  test('should submit form-0 with valid data', async ({ page }) => {
    const form = page.locator('form').nth(0);
    await form.locator('[name="csrfmiddlewaretoken"]').fill(testvalue);
    await form.locator('#id_username').fill(testData.valid.username);
    await form.locator('#id_password').fill(testData.valid.password);
    await form.locator('#id_remember').fill(testvalue);
    await form.locator('[name="next"]').fill(testvalue);
    await form.locator('button[type="submit"], input[type="submit"]').click();
    await expect(page.locator('.success, .alert-success')).toBeVisible({ timeout: 5000 });
  });

  test('should validate required username field', async ({ page }) => {
    const form = page.locator('form').nth(0);
    await form.locator('button[type="submit"], input[type="submit"]').click();
    await expect(form.locator('#id_username:invalid')).toBeVisible();
  });

  test('should validate required password field', async ({ page }) => {
    const form = page.locator('form').nth(0);
    await form.locator('button[type="submit"], input[type="submit"]').click();
    await expect(form.locator('#id_password:invalid')).toBeVisible();
  });

  test('should handle XSS attempts in form-0', async ({ page }) => {
    const form = page.locator('form').nth(0);
    await form.locator('#id_username').fill(testData.invalid.xss);
    await form.locator('button[type="submit"], input[type="submit"]').click();
    
    const alerts = [];
    page.on('dialog', dialog => {
      alerts.push(dialog.message());
      dialog.dismiss();
    });
    
    await page.waitForTimeout(1000);
    expect(alerts).toHaveLength(0);
  });

});

