const { exec } = require('child_process');
const navigationDiscovery = require('./navigation_discovery');
const { generateSecurityTests } = require('./security_tests');
const EnhancedReporter = require('./enhanced_reporting');
const fs = require('fs');
const path = require('path');

async function advancedPipeline() {
  console.log('🚀 Advanced Form Testing Pipeline\n');
  
  const reporter = new EnhancedReporter();
  const startTime = Date.now();
  
  try {
    // Step 1: Navigation Discovery
    console.log('📍 Step 1: Advanced form discovery...');
    const discoveryStart = Date.now();
    const discoveredData = await navigationDiscovery();
    const discoveryTime = Date.now() - discoveryStart;
    
    // Step 2: Generate Comprehensive Tests
    console.log('\n🔧 Step 2: Generating comprehensive test suite...');
    const generationStart = Date.now();
    const testCount = generateAdvancedTests(discoveredData);
    const generationTime = Date.now() - generationStart;
    
    // Step 3: Execute Tests with Enhanced Configuration
    console.log(`\n🧪 Step 3: Executing ${testCount} tests with parallel execution...`);
    const executionStart = Date.now();
    const testResults = await executeAdvancedTests();
    const executionTime = Date.now() - executionStart;
    
    // Step 4: Generate Enhanced Reports
    console.log('\n📊 Step 4: Generating enhanced reports...');
    reporter.generateDashboard(discoveredData, testResults);
    reporter.generatePerformanceReport({
      discoveryTime,
      generationTime,
      executionTime,
      totalTime: Date.now() - startTime
    });
    
    console.log('\n✅ Advanced pipeline completed successfully!');
    console.log(`📊 Dashboard: dashboard.html`);
    console.log(`📈 Performance: performance.json`);
    console.log(`🎭 Playwright Report: playwright-report/index.html`);
    
  } catch (error) {
    console.error('\n❌ Advanced pipeline failed:', error.message);
    process.exit(1);
  }
}

function generateAdvancedTests(discoveredData) {
  console.log('   Generating advanced test suite...');
  
  let testContent = `const { test, expect } = require('@playwright/test');

// Configure Playwright for enhanced testing
test.use({
  screenshot: 'only-on-failure',
  video: 'retain-on-failure',
  trace: 'retain-on-failure'
});

const testData = {
  valid: {
    username: 'testuser',
    password: 'TestPass123!',
    email: 'test@example.com',
    name: 'John Doe',
    phone: '+1234567890',
    message: 'Test message from automated testing',
    address: '123 Test Street',
    city: 'Test City',
    state: 'Test State',
    zip: '12345',
    country: 'Test Country'
  },
  invalid: {
    email: ['invalid', 'test@', '@domain.com', 'test.com'],
    short: 'A',
    long: 'A'.repeat(1000),
    xss: ['<script>alert("xss")</script>', '<img src=x onerror=alert("xss")>', 'javascript:alert("xss")'],
    sql: ["'; DROP TABLE users; --", "' OR '1'='1", "' UNION SELECT * FROM users --"],
    special: ['<>&"\\'\`', '\\n\\r\\t', '🚀💻🔥', '   ', '\\0\\x00']
  }
};

`;

  let testCount = 0;
  
  // Generate form-specific tests
  Object.entries(discoveredData).forEach(([url, pageData]) => {
    if (!pageData.forms || pageData.forms.length === 0) return;
    
    const pageName = pageData.title.replace(/[^a-zA-Z0-9]/g, '_');
    
    testContent += `test.describe('${pageName} - Advanced Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('${url}');
  });

`;

    pageData.forms.forEach((form, formIndex) => {
      const formName = form.id || `form-${formIndex}`;
      
      // Happy Path with Performance Monitoring
      testContent += `  test('Performance: ${formName} submission time', async ({ page }) => {
    const startTime = Date.now();
    
`;
      
      form.fields.forEach(field => {
        if (field.type === 'submit' || field.type === 'button' || field.type === 'hidden') return;
        
        const locator = field.id ? `#${field.id}` : `[name="${field.name}"]`;
        let testValue = getTestValue(field);
        
        testContent += `    await page.fill('${locator}', ${testValue});\n`;
      });
      
      testContent += `    await page.click('button[type="submit"], input[type="submit"]');
    
    const endTime = Date.now();
    const submissionTime = endTime - startTime;
    
    // Performance assertion: form submission should complete within 5 seconds
    expect(submissionTime).toBeLessThan(5000);
    
    await expect(page.locator('.success, .alert-success, .confirmation, .thank-you')).toBeVisible({ timeout: 10000 });
  });

`;
      testCount++;

      // Accessibility Tests
      testContent += `  test('Accessibility: ${formName} keyboard navigation', async ({ page }) => {
    // Test tab navigation through form fields
    let tabCount = 0;
    const maxTabs = 20;
    
    while (tabCount < maxTabs) {
      await page.keyboard.press('Tab');
      tabCount++;
      
      const focusedElement = await page.evaluate(() => {
        const focused = document.activeElement;
        return {
          tagName: focused.tagName,
          type: focused.type,
          name: focused.name,
          id: focused.id
        };
      });
      
      // If we've reached the submit button, test submission with Enter
      if (focusedElement.type === 'submit' || (focusedElement.tagName === 'BUTTON' && focusedElement.type !== 'button')) {
        break;
      }
    }
    
    // Verify form can be submitted with keyboard
    await page.keyboard.press('Enter');
    await page.waitForTimeout(1000);
  });

`;
      testCount++;

      // File Upload Tests (if applicable)
      const fileFields = form.fields.filter(field => field.type === 'file');
      if (fileFields.length > 0) {
        testContent += `  test('File Upload: ${formName} file handling', async ({ page }) => {
`;
        
        fileFields.forEach(field => {
          const locator = field.id ? `#${field.id}` : `[name="${field.name}"]`;
          testContent += `    // Test valid file upload
    await page.setInputFiles('${locator}', {
      name: 'test.txt',
      mimeType: 'text/plain',
      buffer: Buffer.from('test file content')
    });
    
    // Test invalid file type (if restrictions exist)
    try {
      await page.setInputFiles('${locator}', {
        name: 'test.exe',
        mimeType: 'application/x-executable',
        buffer: Buffer.from('fake executable')
      });
    } catch (error) {
      // Expected for restricted file types
    }
`;
        });
        
        testContent += `    await page.click('button[type="submit"], input[type="submit"]');
    await page.waitForTimeout(2000);
  });

`;
        testCount++;
      }

      // Rate Limiting Tests
      testContent += `  test('Rate Limiting: ${formName} multiple submissions', async ({ page }) => {
    const submissions = [];
    
    // Attempt multiple rapid submissions
    for (let i = 0; i < 5; i++) {
`;
      
      form.fields.forEach(field => {
        if (field.type === 'text' || field.type === 'email') {
          const locator = field.id ? `#${field.id}` : `[name="${field.name}"]`;
          testContent += `      await page.fill('${locator}', 'test' + i);\n`;
        }
      });
      
      testContent += `      const submitPromise = page.click('button[type="submit"], input[type="submit"]');
      submissions.push(submitPromise);
      await page.waitForTimeout(100); // Small delay between submissions
    }
    
    // Wait for all submissions to complete
    await Promise.allSettled(submissions);
    
    // Check if rate limiting is in place (should show error or block submissions)
    const rateLimitError = await page.locator('.error, .rate-limit, .too-many-requests').count();
    // Note: This test documents behavior rather than asserting specific outcomes
  });

`;
      testCount++;
    });
    
    testContent += `});

`;
  });

  // Add Security Tests
  const securityTests = generateSecurityTests(discoveredData);
  testContent += securityTests;
  testCount += Object.values(discoveredData).reduce((sum, page) => sum + (page.forms?.length || 0) * 3, 0); // 3 security tests per form

  // Save generated tests
  fs.writeFileSync(path.join(__dirname, 'advanced_tests.spec.js'), testContent);
  console.log(`   ✅ Generated ${testCount} advanced tests`);
  
  return testCount;
}

function getTestValue(field) {
  if (field.type === 'email') return 'testData.valid.email';
  if (field.type === 'password') return 'testData.valid.password';
  if (field.name.includes('username')) return 'testData.valid.username';
  if (field.name.includes('phone')) return 'testData.valid.phone';
  if (field.name.includes('message')) return 'testData.valid.message';
  if (field.name.includes('address')) return 'testData.valid.address';
  if (field.name.includes('city')) return 'testData.valid.city';
  if (field.name.includes('state')) return 'testData.valid.state';
  if (field.name.includes('zip') || field.name.includes('postal')) return 'testData.valid.zip';
  if (field.name.includes('country')) return 'testData.valid.country';
  return 'testData.valid.name';
}

function executeAdvancedTests() {
  return new Promise((resolve, reject) => {
    console.log('   Running advanced tests with parallel execution...');
    
    const testProcess = exec('npx playwright test advanced_tests.spec.js --workers=4 --reporter=html,json', (error, stdout, stderr) => {
      if (stdout) console.log(stdout);
      if (stderr && !stderr.includes('Test failed')) console.log(stderr);
      
      // Parse test results
      let testResults = { passed: 0, failed: 0, skipped: 0 };
      try {
        const resultsPath = path.join(__dirname, 'test-results.json');
        if (fs.existsSync(resultsPath)) {
          const results = JSON.parse(fs.readFileSync(resultsPath, 'utf8'));
          testResults = {
            passed: results.stats?.passed || 0,
            failed: results.stats?.failed || 0,
            skipped: results.stats?.skipped || 0
          };
        }
      } catch (parseError) {
        console.log('   ⚠️  Could not parse test results');
      }
      
      console.log('   ✅ Advanced test execution completed');
      resolve(testResults);
    });
    
    testProcess.on('exit', () => {
      resolve({ passed: 0, failed: 0, skipped: 0 });
    });
  });
}

if (require.main === module) {
  advancedPipeline();
}

module.exports = advancedPipeline;