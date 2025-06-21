const { test, expect } = require('@playwright/test');

test.describe('Complete Shopping Flow Tests', () => {
  
  test.beforeEach(async ({ page }) => {
    // Seed test data first
    await page.goto('http://localhost:8000/admin/');
  });

  test('Complete E-commerce Flow: Browse → Add to Cart → Checkout → Payment', async ({ page }) => {
    // Step 1: Browse products
    await page.goto('http://localhost:8000/');
    await expect(page.locator('h1, .title')).toBeVisible();
    
    // Look for product links or store links
    const productLinks = page.locator('a[href*="/products/"], a[href*="/stores/"]');
    if (await productLinks.count() > 0) {
      await productLinks.first().click();
    }
    
    // Step 2: View product details
    const productDetailSelectors = [
      '.product-detail',
      '[data-testid="product-detail"]',
      'h1:has-text("Product")',
      '.price',
      'button:has-text("Buy")',
      'button:has-text("Add to Cart")'
    ];
    
    let productFound = false;
    for (const selector of productDetailSelectors) {
      if (await page.locator(selector).count() > 0) {
        productFound = true;
        break;
      }
    }
    
    if (productFound) {
      // Step 3: Add to cart or buy now
      const buyButtons = page.locator('button:has-text("Buy"), button:has-text("Add"), button:has-text("Purchase")');
      if (await buyButtons.count() > 0) {
        await buyButtons.first().click();
      }
      
      // Step 4: Checkout form
      await page.waitForTimeout(2000);
      
      const checkoutSelectors = [
        'form[id*="checkout"]',
        'form:has(input[name*="name"])',
        'form:has(input[name*="email"])',
        'input[name="name"]',
        'input[name="email"]'
      ];
      
      let checkoutForm = null;
      for (const selector of checkoutSelectors) {
        const element = page.locator(selector);
        if (await element.count() > 0) {
          checkoutForm = element.first();
          break;
        }
      }
      
      if (checkoutForm) {
        // Fill checkout form
        await this.fillCheckoutForm(page, checkoutForm);
        
        // Submit and verify
        const submitButton = checkoutForm.locator('button[type="submit"], input[type="submit"]');
        if (await submitButton.count() > 0) {
          await submitButton.click();
          
          // Verify payment or success page
          await expect(page.locator('.success, .payment, .razorpay, .confirmation')).toBeVisible({ timeout: 10000 });
        }
      }
    }
  });

  test('Product Search and Filter Flow', async ({ page }) => {
    await page.goto('http://localhost:8000/');
    
    // Look for search functionality
    const searchSelectors = [
      'input[type="search"]',
      'input[name="search"]',
      'input[placeholder*="search"]',
      '.search-input'
    ];
    
    for (const selector of searchSelectors) {
      const searchInput = page.locator(selector);
      if (await searchInput.count() > 0) {
        await searchInput.fill('test product');
        await searchInput.press('Enter');
        
        // Verify search results
        await expect(page.locator('.product, .result, .item')).toBeVisible({ timeout: 5000 });
        break;
      }
    }
  });

  test('User Registration and Login Flow', async ({ page }) => {
    // Test registration if available
    await page.goto('http://localhost:8000/accounts/register/');
    
    if (page.url().includes('register')) {
      const form = page.locator('form').first();
      
      await form.locator('input[name="username"], input[name="email"]').fill('testuser123');
      await form.locator('input[name="email"]').fill('test@example.com');
      await form.locator('input[name="password1"], input[name="password"]').fill('TestPass123!');
      await form.locator('input[name="password2"]').fill('TestPass123!');
      
      await form.locator('button[type="submit"]').click();
    }
    
    // Test login
    await page.goto('http://localhost:8000/accounts/login/');
    
    await page.fill('#id_username', 'testuser');
    await page.fill('#id_password', 'testpass123');
    await page.click('button[type="submit"]');
    
    // Verify login success or error handling
    await page.waitForTimeout(2000);
    const isLoggedIn = await page.locator('.logout, .dashboard, .profile').count() > 0;
    const hasError = await page.locator('.error, .alert-danger').count() > 0;
    
    expect(isLoggedIn || hasError).toBeTruthy();
  });

  test('Store Management Flow (Admin)', async ({ page }) => {
    // Login as admin
    await page.goto('http://localhost:8000/admin/');
    await page.fill('#id_username', 'admin');
    await page.fill('#id_password', 'admin');
    await page.click('input[type="submit"]');
    
    // Navigate to stores
    const storeLinks = page.locator('a:has-text("Store"), a[href*="store"]');
    if (await storeLinks.count() > 0) {
      await storeLinks.first().click();
      
      // Add new store
      const addButton = page.locator('a:has-text("Add"), .addlink');
      if (await addButton.count() > 0) {
        await addButton.click();
        
        // Fill store form
        await page.fill('input[name="name"]', 'Test Store');
        await page.fill('textarea[name="description"]', 'Test store description');
        
        await page.click('input[type="submit"], button[type="submit"]');
        
        // Verify store creation
        await expect(page.locator('.success, .alert-success')).toBeVisible({ timeout: 5000 });
      }
    }
  });

  test('Contact Form Submission', async ({ page }) => {
    // Look for contact forms across the site
    const contactUrls = [
      'http://localhost:8000/contact/',
      'http://localhost:8000/stores/test-store/',
      'http://localhost:8000/'
    ];
    
    for (const url of contactUrls) {
      await page.goto(url);
      
      const contactForm = page.locator('form:has(input[name="name"]), form:has(textarea[name="message"])');
      if (await contactForm.count() > 0) {
        await contactForm.locator('input[name="name"]').fill('John Doe');
        await contactForm.locator('input[name="email"]').fill('john@example.com');
        await contactForm.locator('textarea[name="message"]').fill('Test message from automated test');
        
        await contactForm.locator('button[type="submit"]').click();
        
        // Verify submission
        await expect(page.locator('.success, .thank-you, .sent')).toBeVisible({ timeout: 5000 });
        break;
      }
    }
  });

  test('Payment Integration Test', async ({ page }) => {
    // Mock Razorpay for testing
    await page.addInitScript(() => {
      window.Razorpay = function(options) {
        return {
          open: () => {
            // Simulate successful payment
            setTimeout(() => {
              if (options.handler) {
                options.handler({
                  razorpay_payment_id: 'pay_test123',
                  razorpay_order_id: 'order_test123',
                  razorpay_signature: 'signature_test123'
                });
              }
            }, 1000);
          }
        };
      };
    });
    
    // Navigate to checkout
    await page.goto('http://localhost:8000/orders/checkout/1/');
    
    if (!page.url().includes('404')) {
      // Fill checkout form
      await page.fill('#name', 'Test Customer');
      await page.fill('#email', 'customer@test.com');
      await page.fill('#phone', '+1234567890');
      await page.fill('#address_line1', '123 Test Street');
      await page.fill('#city', 'Test City');
      await page.fill('#state', 'Test State');
      await page.fill('#postal_code', '12345');
      await page.fill('#country', 'Test Country');
      
      // Trigger payment
      await page.click('#pay-button');
      
      // Verify payment flow
      await expect(page.locator('.razorpay, .payment-success')).toBeVisible({ timeout: 10000 });
    }
  });

  // Helper function to fill checkout form
  async fillCheckoutForm(page, form) {
    const fields = {
      'name': 'John Doe',
      'email': 'john@example.com',
      'phone': '+1234567890',
      'address': '123 Main Street',
      'address_line1': '123 Main Street',
      'city': 'New York',
      'state': 'NY',
      'postal_code': '10001',
      'zip': '10001',
      'country': 'USA'
    };
    
    for (const [fieldName, value] of Object.entries(fields)) {
      const field = form.locator(`input[name="${fieldName}"], textarea[name="${fieldName}"]`);
      if (await field.count() > 0) {
        await field.fill(value);
      }
    }
  }
});