import { test, expect } from '@playwright/test';

test.describe('Buyer Flows', () => {
  test.beforeEach(async ({ page }) => {
    // Ensure test data exists
    await page.goto('/', { timeout: 60000 });
  });

  test('Homepage Navigation', async ({ page }) => {
    await page.goto('/');
    
    // Verify homepage loads
    await expect(page.locator('h1').first()).toContainText('Empower Indian Artisans');
    await expect(page.locator('text=Empower Indian Artisans')).toBeVisible();
    
    // Test navigation links - use more specific selectors
    await expect(page.locator('header a[href="/accounts/login/"]')).toBeVisible();
    await expect(page.locator('text=Start Your Store')).toBeVisible();
    
    // Test features section - use more specific selectors
    await expect(page.locator('h3:has-text("Hindi UI")')).toBeVisible();
    await expect(page.locator('h3:has-text("AI Descriptions")')).toBeVisible();
    await expect(page.locator('h3:has-text("WhatsApp Integration")')).toBeVisible();
    await expect(page.locator('h3:has-text("GST Compliance")')).toBeVisible();
  });

  test('Store Discovery', async ({ page }) => {
    await page.goto('/stores/');
    
    // Verify store listing page
    await expect(page.getByRole('heading', { name: 'Browse Indian Artisan Stores' })).toBeVisible();
    
    // Check if stores are displayed
    const storeCards = page.locator('[style*="border: 1px solid #e5e7eb"]');
    await expect(storeCards.first()).toBeVisible();
    
    // Test store card elements
    await expect(page.locator('text=Visit Store').first()).toBeVisible();
    await expect(page.locator('text=Products').first()).toBeVisible();
  });

  test('Store Homepage and Product Browsing', async ({ page }) => {
    // Go directly to test store
    await page.goto('/stores/test-artisan-store/');
    
    // Verify store homepage loads
    await expect(page.locator('h1')).toContainText('Test Artisan Store');
    
    // Check for products section
    await expect(page.locator('text=Our Products')).toBeVisible();
    
    // Test product cards
    const productCards = page.locator('[style*="border: 1px solid #e5e7eb"]');
    await expect(productCards.first()).toBeVisible();
    
    // Check for buy buttons
    const buyButtons = page.locator('button:has-text("Buy Now"), button:has-text("Add to Cart")');
    await expect(buyButtons.first()).toBeVisible();
  });

  test('Shopping Cart Functionality', async ({ page }) => {
    await page.goto('/stores/test-artisan-store/');
    
    // Check cart elements exist
    await expect(page.locator('#cart-count')).toBeVisible();
    await expect(page.locator('#cart-toggle-btn')).toBeVisible();
    
    // Look for Add to Cart button
    const addToCartButton = page.locator('button:has-text("Add to Cart")').first();
    await expect(addToCartButton).toBeVisible();
    
    // Click the button
    await addToCartButton.click();
    
    // Just verify cart sidebar can be opened
    await page.click('#cart-toggle-btn');
    await expect(page.locator('#cart-sidebar')).toBeVisible();
  });

  test('Mobile Shopping Experience', async ({ page, isMobile }) => {
    if (!isMobile) {
      // Simulate mobile viewport
      await page.setViewportSize({ width: 375, height: 667 });
    }
    
    await page.goto('/stores/');
    
    // Verify mobile-responsive design
    const storeGrid = page.locator('[style*="grid-template-columns"]');
    await expect(storeGrid).toBeVisible();
    
    // Test mobile navigation
    const firstStoreLink = page.locator('a[href*="/stores/"]').first();
    if (await firstStoreLink.isVisible()) {
      await firstStoreLink.click();
      
      // Verify mobile store page
      await expect(page.locator('h1')).toBeVisible();
      
      // Test mobile cart functionality
      const cartButton = page.locator('#cart-toggle-btn');
      if (await cartButton.isVisible()) {
        await cartButton.click();
        await expect(page.locator('#cart-sidebar')).toBeVisible();
      }
    }
  });

  test('Error Handling - 404 Page', async ({ page }) => {
    await page.goto('/non-existent-page');
    
    // Verify 404 page
    await expect(page.locator('h1')).toContainText('404');
    await expect(page.locator('text=Page Not Found')).toBeVisible();
    
    // Test navigation links on 404 page
    await expect(page.locator('text=Go Home')).toBeVisible();
    await expect(page.locator('a[href="/accounts/login/"]')).toBeVisible();
  });

  test('Currency Display', async ({ page }) => {
    await page.goto('/stores/test-artisan-store/');
    
    // Verify Indian Rupee symbol is used
    const priceElements = page.locator('text=/₹\\d+/');
    await expect(priceElements.first()).toBeVisible();
    
    // Ensure no dollar signs are present
    const dollarElements = page.locator('text=/\\$\\d+/');
    await expect(dollarElements).toHaveCount(0);
  });
});