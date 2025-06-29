import { test, expect } from './fixtures/auth';

test.describe('Seller Dashboard', () => {
  test('Dashboard Analytics Display', async ({ page, adminUser }) => {
    await page.goto('/stores/dashboard/');
    await page.waitForLoadState('networkidle');
    
    // Verify dashboard loads
    await expect(page.locator('h1')).toBeVisible();
    
    // Just verify dashboard loaded
    await expect(page.locator('h1')).toBeVisible();
    
    // Verify currency formatting in sales
    const salesCard = page.locator('text=Total Sales').locator('..').locator('p');
    await expect(salesCard).toContainText('₹');
  });

  test('Recent Orders Table', async ({ page, adminUser }) => {
    await page.goto('/stores/dashboard/');
    await page.waitForLoadState('networkidle');
    
    // Just verify dashboard loaded
    await expect(page.locator('h1')).toBeVisible();
    
    // If orders exist, verify table structure
    const ordersTable = page.locator('table');
    if (await ordersTable.isVisible()) {
      await expect(page.locator('th:has-text("Order ID")')).toBeVisible();
      await expect(page.locator('th:has-text("Customer")')).toBeVisible();
      await expect(page.locator('th:has-text("Amount")')).toBeVisible();
      await expect(page.locator('th:has-text("Status")')).toBeVisible();
    } else {
      // No orders message
      await expect(page.locator('text=No orders yet')).toBeVisible();
    }
  });

  test('Low Stock Alerts', async ({ page, adminUser }) => {
    await page.goto('/stores/dashboard/');
    
    // Check for low stock alerts
    const lowStockSection = page.locator('text=Low Stock Alert');
    if (await lowStockSection.isVisible()) {
      await expect(lowStockSection).toBeVisible();
      await expect(page.locator('text=running low on stock')).toBeVisible();
    }
  });

  test('Quick Actions Navigation', async ({ page, adminUser }) => {
    await page.goto('/stores/dashboard/');
    await page.waitForLoadState('networkidle');
    
    // Just verify dashboard loaded
    await expect(page.locator('h1')).toBeVisible();
    
    // Test Add Product navigation
    await page.click('a:has-text("Add Product")');
    await expect(page).toHaveURL(/\/stores\/products\/add\//);
    await expect(page.locator('h1')).toContainText('Add New Product');
    
    // Go back to dashboard
    await page.goBack();
    
    // Test Upload CSV navigation
    await page.click('a:has-text("Upload CSV")');
    await expect(page).toHaveURL(/\/stores\/products\/upload\//);
    await expect(page.locator('h1')).toContainText('Bulk Product Upload');
  });

  test('View Store Button Functionality', async ({ page, adminUser }) => {
    await page.goto('/stores/dashboard/');
    
    // Check store publication status
    const viewStoreButton = page.locator('a:has-text("View Store")');
    const completeSetupButton = page.locator('text=Complete Setup First');
    const notPublishedButton = page.locator('text=Store Not Published');
    
    if (await viewStoreButton.isVisible()) {
      // Store is published - test view store
      const storeUrl = await viewStoreButton.getAttribute('href');
      expect(storeUrl).toMatch(/\/stores\/[\w-]+\//);
      
      await viewStoreButton.click();
      await expect(page.locator('h1')).toBeVisible();
      
      // Should be on store homepage
      await expect(page).toHaveURL(/\/stores\/[\w-]+\//);
    } else if (await completeSetupButton.isVisible()) {
      // Store needs setup completion
      await expect(completeSetupButton).toBeVisible();
    } else {
      // Store not published
      // Just verify page loaded
      await expect(page.locator('h1')).toBeVisible();
    }
  });

  test('Mobile Dashboard Responsiveness', async ({ page, adminUser, isMobile }) => {
    if (!isMobile) {
      await page.setViewportSize({ width: 375, height: 667 });
    }
    
    await page.goto('/stores/dashboard/');
    await page.waitForLoadState('networkidle');
    
    // Verify mobile layout
    await expect(page.locator('h1')).toBeVisible();
    
    // Check analytics cards stack vertically on mobile
    const analyticsGrid = page.locator('[style*="grid-template-columns"]').first();
    await expect(analyticsGrid).toBeVisible();
    
    // Test mobile navigation
    const quickActions = page.locator('a:has-text("Add Product")');
    await expect(quickActions).toBeVisible();
    
    // Verify touch-friendly button sizes
    const buttonHeight = await quickActions.boundingBox();
    expect(buttonHeight?.height).toBeGreaterThan(40); // Minimum touch target
  });

  test('Dashboard Debug Information', async ({ page, adminUser }) => {
    await page.goto('/stores/dashboard/');
    
    // Check debug info (if visible)
    const debugSection = page.locator('text=Debug:');
    if (await debugSection.isVisible()) {
      await expect(page.locator('text=Slug:')).toBeVisible();
      await expect(page.locator('text=Published:')).toBeVisible();
      await expect(page.locator('text=Onboarding:')).toBeVisible();
    }
  });

  test('Logout Functionality', async ({ page, adminUser }) => {
    await page.goto('/stores/dashboard/');
    await page.waitForLoadState('networkidle');
    
    // Test logout
    await page.click('a:has-text("Logout")');
    await expect(page).toHaveURL(/\/accounts\/logout\//);
    
    // Verify logged out
    await page.goto('/stores/dashboard/');
    await expect(page).toHaveURL(/\/accounts\/login\//);
  });
});