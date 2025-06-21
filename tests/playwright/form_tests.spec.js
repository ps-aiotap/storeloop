const { test, expect } = require('@playwright/test');

// Test data generators
const testData = {
  valid: {
    name: 'John Doe',
    email: 'john.doe@example.com',
    phone: '+1234567890',
    address_line1: '123 Main Street',
    city: 'New York',
    state: 'NY',
    postal_code: '10001',
    country: 'USA',
    message: 'This is a test message',
    subject: 'Test Subject'
  },
  invalid: {
    email: ['invalid-email', 'test@', '@domain.com', 'test.com'],
    name: ['', 'A', '12345', '   ', 'Name with 🚀 emoji'],
    phone: ['123', 'abc123', '++123456789', '123-456-78901234567890'],
    postal_code: ['123', 'ABCDE', '1234567890123'],
    longText: 'A'.repeat(1000)
  }
};

test.describe('Login Form Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:8000/accounts/login/');
  });

  test('should login with valid credentials', async ({ page }) => {
    await page.fill('#id_username', 'testuser');
    await page.fill('#id_password', 'testpass123');
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL(/\/$/);
  });

  test('should show error for empty username', async ({ page }) => {
    await page.fill('#id_password', 'testpass123');
    await page.click('button[type="submit"]');
    
    await expect(page.locator('#id_username:invalid')).toBeVisible();
  });

  test('should show error for empty password', async ({ page }) => {
    await page.fill('#id_username', 'testuser');
    await page.click('button[type="submit"]');
    
    await expect(page.locator('#id_password:invalid')).toBeVisible();
  });

  test('should handle special characters in username', async ({ page }) => {
    await page.fill('#id_username', 'test@user!#$');
    await page.fill('#id_password', 'testpass123');
    await page.click('button[type="submit"]');
    
    await expect(page.locator('.alert, .error')).toBeVisible();
  });
});

test.describe('Checkout Form Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:8000/orders/checkout/1/');
  });

  test('should complete checkout with valid data', async ({ page }) => {
    await page.fill('#name', testData.valid.name);
    await page.fill('#email', testData.valid.email);
    await page.fill('#phone', testData.valid.phone);
    await page.fill('#address_line1', testData.valid.address_line1);
    await page.fill('#city', testData.valid.city);
    await page.fill('#state', testData.valid.state);
    await page.fill('#postal_code', testData.valid.postal_code);
    await page.fill('#country', testData.valid.country);
    
    await page.click('#pay-button');
    
    // Should trigger Razorpay modal or show validation success
    await expect(page.locator('.razorpay-container, .success-message')).toBeVisible({ timeout: 5000 });
  });

  test('should validate required name field', async ({ page }) => {
    await page.fill('#email', testData.valid.email);
    await page.click('#pay-button');
    
    await expect(page.locator('#name-error')).toBeVisible();
    await expect(page.locator('#name-error')).toContainText('required');
  });

  test('should validate name minimum length', async ({ page }) => {
    await page.fill('#name', 'A');
    await page.blur('#name');
    
    await expect(page.locator('#name-error')).toBeVisible();
    await expect(page.locator('#name-error')).toContainText('3 characters');
  });

  test('should validate email format', async ({ page }) => {
    for (const invalidEmail of testData.invalid.email) {
      await page.fill('#email', invalidEmail);
      await page.blur('#email');
      
      await expect(page.locator('#email-error')).toBeVisible();
      await expect(page.locator('#email-error')).toContainText('valid email');
    }
  });

  test('should validate phone format', async ({ page }) => {
    for (const invalidPhone of testData.invalid.phone) {
      await page.fill('#phone', invalidPhone);
      await page.blur('#phone');
      
      await expect(page.locator('#phone-error')).toBeVisible();
    }
  });

  test('should validate postal code format', async ({ page }) => {
    for (const invalidPostal of testData.invalid.postal_code) {
      await page.fill('#postal_code', invalidPostal);
      await page.blur('#postal_code');
      
      await expect(page.locator('#postal_code-error')).toBeVisible();
    }
  });

  test('should handle long text inputs', async ({ page }) => {
    await page.fill('#name', testData.invalid.longText);
    await page.fill('#address_line1', testData.invalid.longText);
    
    // Should either truncate or show validation error
    const nameValue = await page.inputValue('#name');
    const addressValue = await page.inputValue('#address_line1');
    
    expect(nameValue.length).toBeLessThanOrEqual(200);
    expect(addressValue.length).toBeLessThanOrEqual(500);
  });

  test('should handle whitespace-only inputs', async ({ page }) => {
    await page.fill('#name', '   ');
    await page.fill('#email', '   ');
    await page.click('#pay-button');
    
    await expect(page.locator('#name-error')).toBeVisible();
    await expect(page.locator('#email-error')).toBeVisible();
  });

  test('should prevent multiple form submissions', async ({ page }) => {
    await page.fill('#name', testData.valid.name);
    await page.fill('#email', testData.valid.email);
    await page.fill('#address_line1', testData.valid.address_line1);
    await page.fill('#city', testData.valid.city);
    await page.fill('#state', testData.valid.state);
    await page.fill('#postal_code', testData.valid.postal_code);
    await page.fill('#country', testData.valid.country);
    
    // Click multiple times rapidly
    await Promise.all([
      page.click('#pay-button'),
      page.click('#pay-button'),
      page.click('#pay-button')
    ]);
    
    // Should only process once
    const payButton = page.locator('#pay-button');
    await expect(payButton).toBeDisabled();
  });
});

test.describe('Contact Form Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:8000/stores/test-store/');
  });

  test('should submit contact form with valid data', async ({ page }) => {
    const contactForm = page.locator('form[id*="contact-form"]').first();
    
    if (await contactForm.isVisible()) {
      await contactForm.locator('#name').fill(testData.valid.name);
      await contactForm.locator('#email').fill(testData.valid.email);
      await contactForm.locator('#message').fill(testData.valid.message);
      
      await contactForm.locator('button[type="submit"]').click();
      
      await expect(page.locator('.success-message, .alert-success')).toBeVisible();
    }
  });

  test('should validate required fields', async ({ page }) => {
    const contactForm = page.locator('form[id*="contact-form"]').first();
    
    if (await contactForm.isVisible()) {
      await contactForm.locator('button[type="submit"]').click();
      
      await expect(contactForm.locator('#name:invalid')).toBeVisible();
      await expect(contactForm.locator('#email:invalid')).toBeVisible();
      await expect(contactForm.locator('#message:invalid')).toBeVisible();
    }
  });

  test('should handle emoji and special characters', async ({ page }) => {
    const contactForm = page.locator('form[id*="contact-form"]').first();
    
    if (await contactForm.isVisible()) {
      await contactForm.locator('#name').fill('Test User 🚀');
      await contactForm.locator('#email').fill(testData.valid.email);
      await contactForm.locator('#message').fill('Message with emojis 🎉 and special chars @#$%');
      
      await contactForm.locator('button[type="submit"]').click();
      
      // Should either accept or show appropriate validation
      const hasError = await page.locator('.error-message').isVisible();
      const hasSuccess = await page.locator('.success-message').isVisible();
      
      expect(hasError || hasSuccess).toBeTruthy();
    }
  });
});

test.describe('Form Accessibility Tests', () => {
  test('should have proper labels for all form fields', async ({ page }) => {
    await page.goto('http://localhost:8000/accounts/login/');
    
    const inputs = page.locator('input');
    const inputCount = await inputs.count();
    
    for (let i = 0; i < inputCount; i++) {
      const input = inputs.nth(i);
      const inputId = await input.getAttribute('id');
      
      if (inputId) {
        const label = page.locator(`label[for="${inputId}"]`);
        await expect(label).toBeVisible();
      }
    }
  });

  test('should support keyboard navigation', async ({ page }) => {
    await page.goto('http://localhost:8000/accounts/login/');
    
    await page.keyboard.press('Tab');
    await expect(page.locator('#id_username')).toBeFocused();
    
    await page.keyboard.press('Tab');
    await expect(page.locator('#id_password')).toBeFocused();
    
    await page.keyboard.press('Tab');
    await expect(page.locator('button[type="submit"]')).toBeFocused();
  });

  test('should have proper ARIA attributes', async ({ page }) => {
    await page.goto('http://localhost:8000/orders/checkout/1/');
    
    const requiredFields = page.locator('input[required]');
    const fieldCount = await requiredFields.count();
    
    for (let i = 0; i < fieldCount; i++) {
      const field = requiredFields.nth(i);
      const ariaRequired = await field.getAttribute('aria-required');
      const required = await field.getAttribute('required');
      
      expect(ariaRequired === 'true' || required !== null).toBeTruthy();
    }
  });
});

test.describe('Form Security Tests', () => {
  test('should have CSRF protection', async ({ page }) => {
    await page.goto('http://localhost:8000/accounts/login/');
    
    const csrfToken = page.locator('input[name="csrfmiddlewaretoken"]');
    await expect(csrfToken).toBeVisible();
    
    const tokenValue = await csrfToken.getAttribute('value');
    expect(tokenValue).toBeTruthy();
    expect(tokenValue.length).toBeGreaterThan(10);
  });

  test('should sanitize input data', async ({ page }) => {
    await page.goto('http://localhost:8000/accounts/login/');
    
    const maliciousInput = '<script>alert("xss")</script>';
    
    await page.fill('#id_username', maliciousInput);
    await page.fill('#id_password', 'password');
    await page.click('button[type="submit"]');
    
    // Should not execute script
    const alerts = [];
    page.on('dialog', dialog => {
      alerts.push(dialog.message());
      dialog.dismiss();
    });
    
    await page.waitForTimeout(1000);
    expect(alerts).toHaveLength(0);
  });

  test('should prevent SQL injection attempts', async ({ page }) => {
    await page.goto('http://localhost:8000/accounts/login/');
    
    const sqlInjection = "'; DROP TABLE users; --";
    
    await page.fill('#id_username', sqlInjection);
    await page.fill('#id_password', 'password');
    await page.click('button[type="submit"]');
    
    // Should handle gracefully without breaking
    await expect(page.locator('body')).toBeVisible();
  });
});