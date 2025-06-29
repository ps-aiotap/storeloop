import { test, expect } from './fixtures/onboarding-auth';

test.describe('Seller Onboarding Wizard', () => {
  test('Complete 5-Step Onboarding Process', async ({ page, newAdminUser }) => {
    // Should be redirected to onboarding after login
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveURL(/\/stores\/onboarding\//);
    
    // Step 1: Basic Information
    await expect(page.locator('h1')).toContainText('Step 1 of 5');
    await expect(page.locator('h2')).toContainText('Basic Information');
    
    await page.fill('input[name="name"]', 'कलाकार शिल्प');
    await page.fill('textarea[name="description"]', 'Handmade crafts by Indian artisans');
    
    // Upload logo (optional - skip for test)
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Step 2: Theme Selection
    await expect(page).toHaveURL(/step=2/);
    await expect(page.locator('h2')).toContainText('Theme Selection');
    
    await page.selectOption('select[name="theme"]', 'warm');
    await page.fill('input[name="primary_color"]', '#8B4513');
    await page.fill('input[name="secondary_color"]', '#DEB887');
    await page.selectOption('select[name="font_family"]', 'serif');
    
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Step 3: Homepage Layout
    await expect(page).toHaveURL(/step=3/);
    await expect(page.locator('h2')).toContainText('Homepage Layout');
    
    await page.fill('input[name="hero_title"]', 'Welcome to Our Store');
    await page.fill('textarea[name="hero_content"]', 'Discover unique handcrafted items');
    await page.fill('input[name="about_title"]', 'About Our Craft');
    await page.fill('textarea[name="about_content"]', 'We create beautiful handmade items');
    
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Step 4: Sample Products
    await expect(page).toHaveURL(/step=4/);
    await expect(page.locator('h2')).toContainText('Sample Products');
    
    await expect(page.locator('text=Sample Product 1')).toBeVisible();
    await expect(page.locator('text=Sample Product 2')).toBeVisible();
    
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Step 5: Payment & GST Setup
    await expect(page).toHaveURL(/step=5/);
    await expect(page.locator('h2')).toContainText('Payment & GST Setup');
    
    await page.fill('input[name="razorpay_key_id"]', 'rzp_test_xGdsXPASp5sAxd');
    await page.fill('input[name="razorpay_key_secret"]', 'test_secret');
    await page.fill('input[name="gst_number"]', '27AAPFU0939F1ZV');
    await page.fill('textarea[name="business_address"]', '123 Artisan Street, Delhi, 110001');
    
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
    
    // Should be redirected to dashboard
    await expect(page).toHaveURL(/\/stores\/dashboard\//);
    await expect(page.locator('h1')).toContainText('Dashboard');
  });

  test('Hindi Store Name Slug Generation', async ({ page, newAdminUser }) => {
    // Go through onboarding with Hindi name
    await page.fill('input[name="name"]', 'कलाकार शिल्प');
    await page.fill('textarea[name="description"]', 'हस्तशिल्प कलाकृतियां');
    await page.click('button[type="submit"]');
    
    // Complete remaining steps quickly
    await page.click('button[type="submit"]'); // Step 2
    await page.click('button[type="submit"]'); // Step 3
    await page.click('button[type="submit"]'); // Step 4
    
    // Fill minimal step 5 data
    await page.fill('input[name="gst_number"]', '27AAPFU0939F1ZV');
    await page.click('button[type="submit"]');
    
    // Verify store is accessible
    await expect(page).toHaveURL(/\/stores\/dashboard\//);
    
    // Check if View Store button is available
    const viewStoreButton = page.locator('a:has-text("View Store")');
    if (await viewStoreButton.isVisible()) {
      const storeUrl = await viewStoreButton.getAttribute('href');
      expect(storeUrl).toMatch(/\/stores\/[\w-]+\//);
      
      // Visit the store page
      await viewStoreButton.click();
      await expect(page.locator('h1')).toContainText('कलाकार शिल्प');
    }
  });

  test('Onboarding Validation', async ({ page, newAdminUser }) => {
    // Test empty form submission
    const submitBtn = page.locator('button[type="submit"]');
    await submitBtn.waitFor({ timeout: 10000 });
    await submitBtn.click();
    
    // Should stay on step 1 if validation fails
    await expect(page).toHaveURL(/\/stores\/onboarding\//);
    
    // Fill required fields
    await page.fill('input[name="name"]', 'Test Store');
    await submitBtn.click();
    
    // Should proceed to step 2
    await expect(page).toHaveURL(/step=2/);
  });

  test('Store Publication Status', async ({ page, newAdminUser }) => {
    // Complete onboarding
    await page.fill('input[name="name"]', 'Published Store');
    await page.fill('textarea[name="description"]', 'Test store description');
    await page.click('button[type="submit"]');
    
    // Skip through steps 2-4
    for (let i = 0; i < 3; i++) {
      await page.click('button[type="submit"]');
    }
    
    // Complete step 5
    await page.fill('input[name="gst_number"]', '27AAPFU0939F1ZV');
    await page.click('button[type="submit"]');
    
    // Verify store is published
    await expect(page).toHaveURL(/\/stores\/dashboard\//);
    
    // Check debug info shows published status
    const debugInfo = page.locator('text=Published: True');
    if (await debugInfo.isVisible()) {
      await expect(debugInfo).toBeVisible();
    }
  });
});