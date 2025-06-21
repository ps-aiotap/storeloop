const fs = require('fs');
const path = require('path');

function generateCompleteTests() {
  console.log('🔧 Generating comprehensive tests...');
  
  const formsData = JSON.parse(fs.readFileSync(path.join(__dirname, 'complete_forms.json'), 'utf8'));
  
  let testContent = `const { test, expect } = require('@playwright/test');

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
    long: '${'A'.repeat(500)}',
    xss: '<script>alert("xss")</script>',
    sql: "'; DROP TABLE users; --"
  }
};

`;

  Object.entries(formsData).forEach(([pageName, pageData]) => {
    if (pageData.forms.length === 0) return;
    
    testContent += `test.describe('${pageName.charAt(0).toUpperCase() + pageName.slice(1)} Page Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('${pageData.url}');
  });

`;

    pageData.forms.forEach((form, formIndex) => {
      const formName = form.id || `form-${formIndex}`;
      
      // Happy path test
      testContent += `  test('should submit ${formName} with valid data', async ({ page }) => {
    const form = page.locator('form').nth(${formIndex});
`;
      
      form.fields.forEach(field => {
        if (field.type === 'submit' || field.type === 'button') return;
        
        const locator = field.id ? `#${field.id}` : `[name="${field.name}"]`;
        let testValue = 'testvalue';
        
        if (field.type === 'email') testValue = 'testData.valid.email';
        else if (field.type === 'password') testValue = 'testData.valid.password';
        else if (field.name.includes('username')) testValue = 'testData.valid.username';
        else if (field.name.includes('name')) testValue = 'testData.valid.name';
        else if (field.name.includes('phone')) testValue = 'testData.valid.phone';
        else if (field.name.includes('message')) testValue = 'testData.valid.message';
        
        testContent += `    await form.locator('${locator}').fill(${testValue});\n`;
      });
      
      testContent += `    await form.locator('button[type="submit"], input[type="submit"]').click();
    await expect(page.locator('.success, .alert-success')).toBeVisible({ timeout: 5000 });
  });

`;

      // Validation tests
      form.fields.forEach(field => {
        if (field.required && field.type !== 'submit' && field.type !== 'button') {
          const locator = field.id ? `#${field.id}` : `[name="${field.name}"]`;
          
          testContent += `  test('should validate required ${field.name || field.id} field', async ({ page }) => {
    const form = page.locator('form').nth(${formIndex});
    await form.locator('button[type="submit"], input[type="submit"]').click();
    await expect(form.locator('${locator}:invalid')).toBeVisible();
  });

`;
        }
        
        if (field.type === 'email') {
          const locator = field.id ? `#${field.id}` : `[name="${field.name}"]`;
          
          testContent += `  test('should validate ${field.name || field.id} email format', async ({ page }) => {
    const form = page.locator('form').nth(${formIndex});
    for (const invalidEmail of testData.invalid.email) {
      await form.locator('${locator}').fill(invalidEmail);
      await form.locator('${locator}').blur();
      await expect(form.locator('${locator}:invalid')).toBeVisible();
    }
  });

`;
        }
      });
      
      // Security tests
      testContent += `  test('should handle XSS attempts in ${formName}', async ({ page }) => {
    const form = page.locator('form').nth(${formIndex});
`;
      
      form.fields.forEach(field => {
        if (field.type === 'text' || field.type === 'textarea') {
          const locator = field.id ? `#${field.id}` : `[name="${field.name}"]`;
          testContent += `    await form.locator('${locator}').fill(testData.invalid.xss);\n`;
        }
      });
      
      testContent += `    await form.locator('button[type="submit"], input[type="submit"]').click();
    
    const alerts = [];
    page.on('dialog', dialog => {
      alerts.push(dialog.message());
      dialog.dismiss();
    });
    
    await page.waitForTimeout(1000);
    expect(alerts).toHaveLength(0);
  });

`;
    });
    
    testContent += `});

`;
  });
  
  // Save generated tests
  fs.writeFileSync(path.join(__dirname, 'complete_tests.spec.js'), testContent);
  
  const totalTests = Object.values(formsData).reduce((sum, page) => {
    return sum + page.forms.reduce((formSum, form) => {
      const requiredFields = form.fields.filter(f => f.required && f.type !== 'submit').length;
      const emailFields = form.fields.filter(f => f.type === 'email').length;
      return formSum + 1 + requiredFields + emailFields + 1; // happy path + validation + security
    }, 0);
  }, 0);
  
  console.log(`✅ Generated ${totalTests} tests in complete_tests.spec.js`);
  return totalTests;
}

if (require.main === module) {
  generateCompleteTests();
}

module.exports = generateCompleteTests;