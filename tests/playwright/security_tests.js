const { test, expect } = require('@playwright/test');

const securityPayloads = {
  sql: [
    "'; DROP TABLE users; --",
    "' OR '1'='1",
    "' UNION SELECT * FROM users --",
    "admin'--",
    "' OR 1=1#"
  ],
  xss: [
    '<script>alert("xss")</script>',
    '<img src=x onerror=alert("xss")>',
    'javascript:alert("xss")',
    '<svg onload=alert("xss")>',
    '"><script>alert("xss")</script>'
  ],
  csrf: {
    invalidToken: 'invalid_csrf_token_12345',
    emptyToken: '',
    oldToken: 'old_token_from_previous_session'
  }
};

function generateSecurityTests(discoveredData) {
  let testContent = `const { test, expect } = require('@playwright/test');

test.describe('Security Tests', () => {
`;

  Object.entries(discoveredData).forEach(([url, pageData]) => {
    if (!pageData.forms || pageData.forms.length === 0) return;

    pageData.forms.forEach((form, formIndex) => {
      // SQL Injection Tests
      testContent += `  test('SQL Injection - ${form.id || `form-${formIndex}`} at ${url}', async ({ page }) => {
    await page.goto('${url}');
    
    const sqlPayloads = ${JSON.stringify(securityPayloads.sql)};
    
    for (const payload of sqlPayloads) {
`;

      form.fields.forEach(field => {
        if (field.type === 'text' || field.type === 'email' || field.type === 'search') {
          const locator = field.id ? `#${field.id}` : `[name="${field.name}"]`;
          testContent += `      await page.fill('${locator}', payload);\n`;
        }
      });

      testContent += `      await page.click('button[type="submit"], input[type="submit"]');
      
      // Check for SQL error messages
      const errorSelectors = ['.error', '.alert-danger', '.sql-error', '[class*="error"]'];
      let hasError = false;
      
      for (const selector of errorSelectors) {
        const errorElement = page.locator(selector);
        if (await errorElement.count() > 0) {
          const errorText = await errorElement.textContent();
          expect(errorText.toLowerCase()).not.toContain('sql');
          expect(errorText.toLowerCase()).not.toContain('database');
          expect(errorText.toLowerCase()).not.toContain('mysql');
          expect(errorText.toLowerCase()).not.toContain('postgresql');
          hasError = true;
        }
      }
      
      // Verify page doesn't crash
      await expect(page.locator('body')).toBeVisible();
    }
  });

`;

      // XSS Tests
      testContent += `  test('XSS Prevention - ${form.id || `form-${formIndex}`} at ${url}', async ({ page }) => {
    await page.goto('${url}');
    
    const xssPayloads = ${JSON.stringify(securityPayloads.xss)};
    const alerts = [];
    
    page.on('dialog', dialog => {
      alerts.push(dialog.message());
      dialog.dismiss();
    });
    
    for (const payload of xssPayloads) {
`;

      form.fields.forEach(field => {
        if (field.type === 'text' || field.type === 'textarea' || field.type === 'email') {
          const locator = field.id ? `#${field.id}` : `[name="${field.name}"]`;
          testContent += `      await page.fill('${locator}', payload);\n`;
        }
      });

      testContent += `      await page.click('button[type="submit"], input[type="submit"]');
      await page.waitForTimeout(1000);
      
      // Verify no script execution
      expect(alerts).toHaveLength(0);
      
      // Check if payload is properly encoded in response
      const pageContent = await page.content();
      expect(pageContent).not.toContain('<script>alert("xss")</script>');
    }
  });

`;

      // CSRF Tests
      const hasCSRFToken = form.fields.some(field => field.name === 'csrfmiddlewaretoken');
      if (hasCSRFToken) {
        testContent += `  test('CSRF Protection - ${form.id || `form-${formIndex}`} at ${url}', async ({ page }) => {
    await page.goto('${url}');
    
    // Test 1: Submit without CSRF token
    await page.evaluate(() => {
      const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
      if (csrfInput) csrfInput.remove();
    });
    
`;

        form.fields.forEach(field => {
          if (field.type === 'text' || field.type === 'email' || field.type === 'password') {
            const locator = field.id ? `#${field.id}` : `[name="${field.name}"]`;
            testContent += `    await page.fill('${locator}', 'test');\n`;
          }
        });

        testContent += `    await page.click('button[type="submit"], input[type="submit"]');
    
    // Should show CSRF error or redirect to error page
    await page.waitForTimeout(2000);
    const hasCSRFError = await page.locator('.error, .alert-danger, [class*="error"]').count() > 0;
    const is403Page = page.url().includes('403') || await page.locator('h1:has-text("403")').count() > 0;
    
    expect(hasCSRFError || is403Page).toBeTruthy();
    
    // Test 2: Submit with invalid CSRF token
    await page.goto('${url}');
    await page.evaluate(() => {
      const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
      if (csrfInput) csrfInput.value = 'invalid_token_12345';
    });
    
`;

        form.fields.forEach(field => {
          if (field.type === 'text' || field.type === 'email' || field.type === 'password') {
            const locator = field.id ? `#${field.id}` : `[name="${field.name}"]`;
            testContent += `    await page.fill('${locator}', 'test');\n`;
          }
        });

        testContent += `    await page.click('button[type="submit"], input[type="submit"]');
    
    await page.waitForTimeout(2000);
    const hasInvalidTokenError = await page.locator('.error, .alert-danger, [class*="error"]').count() > 0;
    const is403PageInvalid = page.url().includes('403') || await page.locator('h1:has-text("403")').count() > 0;
    
    expect(hasInvalidTokenError || is403PageInvalid).toBeTruthy();
  });

`;
      }
    });
  });

  testContent += `});
`;

  return testContent;
}

module.exports = { generateSecurityTests, securityPayloads };