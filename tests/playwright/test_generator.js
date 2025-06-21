const fs = require('fs');
const path = require('path');

class TestGenerator {
  constructor(formsData) {
    this.formsData = formsData;
    this.testCases = [];
  }

  generateTests() {
    Object.entries(this.formsData).forEach(([pageName, forms]) => {
      forms.forEach((form, formIndex) => {
        this.generateFormTests(pageName, form, formIndex);
      });
    });

    this.saveGeneratedTests();
  }

  generateFormTests(pageName, form, formIndex) {
    const testSuite = {
      pageName,
      formId: form.formId,
      tests: []
    };

    // Generate happy path test
    testSuite.tests.push(this.generateHappyPathTest(form));

    // Generate validation tests for each field
    form.fields.forEach(field => {
      if (field.type !== 'submit' && field.type !== 'button') {
        testSuite.tests.push(...this.generateFieldValidationTests(field));
      }
    });

    // Generate edge case tests
    testSuite.tests.push(...this.generateEdgeCaseTests(form));

    this.testCases.push(testSuite);
  }

  generateHappyPathTest(form) {
    const validData = this.getValidDataForForm(form);
    
    return {
      name: `should submit ${form.formId} with valid data`,
      type: 'happy_path',
      steps: [
        ...Object.entries(validData).map(([fieldName, value]) => ({
          action: 'fill',
          locator: this.getFieldLocator(form, fieldName),
          value: value
        })),
        {
          action: 'click',
          locator: this.getSubmitButtonLocator(form)
        },
        {
          action: 'expect',
          condition: 'success_indicator_visible'
        }
      ]
    };
  }

  generateFieldValidationTests(field) {
    const tests = [];

    // Required field test
    if (field.required) {
      tests.push({
        name: `should validate required ${field.name} field`,
        type: 'validation',
        steps: [
          {
            action: 'fill',
            locator: field.locator,
            value: ''
          },
          {
            action: 'blur',
            locator: field.locator
          },
          {
            action: 'expect',
            condition: 'validation_error_visible',
            locator: `${field.locator}-error, ${field.locator}:invalid`
          }
        ]
      });
    }

    // Email validation
    if (field.type === 'email') {
      const invalidEmails = ['invalid-email', 'test@', '@domain.com', 'test.com'];
      
      tests.push({
        name: `should validate ${field.name} email format`,
        type: 'validation',
        steps: invalidEmails.map(email => ({
          action: 'fill_and_validate',
          locator: field.locator,
          value: email,
          expectError: true
        }))
      });
    }

    // Length validation
    if (field.minLength) {
      tests.push({
        name: `should validate ${field.name} minimum length`,
        type: 'validation',
        steps: [
          {
            action: 'fill',
            locator: field.locator,
            value: 'A'.repeat(field.minLength - 1)
          },
          {
            action: 'blur',
            locator: field.locator
          },
          {
            action: 'expect',
            condition: 'validation_error_visible'
          }
        ]
      });
    }

    // Pattern validation
    if (field.pattern) {
      tests.push({
        name: `should validate ${field.name} pattern`,
        type: 'validation',
        steps: [
          {
            action: 'fill',
            locator: field.locator,
            value: 'invalid-pattern-123!@#'
          },
          {
            action: 'blur',
            locator: field.locator
          },
          {
            action: 'expect',
            condition: 'validation_error_visible'
          }
        ]
      });
    }

    return tests;
  }

  generateEdgeCaseTests(form) {
    return [
      {
        name: `should handle special characters in ${form.formId}`,
        type: 'edge_case',
        steps: [
          {
            action: 'fill_form_with_special_chars',
            form: form.formId
          },
          {
            action: 'submit',
            locator: this.getSubmitButtonLocator(form)
          },
          {
            action: 'expect',
            condition: 'no_script_execution'
          }
        ]
      },
      {
        name: `should handle long text inputs in ${form.formId}`,
        type: 'edge_case',
        steps: [
          {
            action: 'fill_form_with_long_text',
            form: form.formId
          },
          {
            action: 'submit',
            locator: this.getSubmitButtonLocator(form)
          },
          {
            action: 'expect',
            condition: 'graceful_handling'
          }
        ]
      },
      {
        name: `should prevent multiple submissions of ${form.formId}`,
        type: 'edge_case',
        steps: [
          {
            action: 'fill_form_with_valid_data',
            form: form.formId
          },
          {
            action: 'click_multiple_times',
            locator: this.getSubmitButtonLocator(form),
            times: 3
          },
          {
            action: 'expect',
            condition: 'single_submission_only'
          }
        ]
      }
    ];
  }

  getValidDataForForm(form) {
    const validData = {};
    
    form.fields.forEach(field => {
      if (field.type === 'submit' || field.type === 'button') return;
      
      switch (field.type) {
        case 'email':
          validData[field.name] = 'test@example.com';
          break;
        case 'tel':
          validData[field.name] = '+1234567890';
          break;
        case 'text':
          if (field.name.includes('name')) {
            validData[field.name] = 'John Doe';
          } else if (field.name.includes('address')) {
            validData[field.name] = '123 Main Street';
          } else if (field.name.includes('city')) {
            validData[field.name] = 'New York';
          } else if (field.name.includes('state')) {
            validData[field.name] = 'NY';
          } else if (field.name.includes('country')) {
            validData[field.name] = 'USA';
          } else if (field.name.includes('postal') || field.name.includes('zip')) {
            validData[field.name] = '10001';
          } else {
            validData[field.name] = 'Test Value';
          }
          break;
        case 'textarea':
          validData[field.name] = 'This is a test message with sufficient content.';
          break;
        case 'password':
          validData[field.name] = 'TestPassword123!';
          break;
        case 'select-one':
          if (field.options && field.options.length > 1) {
            validData[field.name] = field.options[1].value;
          }
          break;
        default:
          validData[field.name] = 'Test Value';
      }
    });
    
    return validData;
  }

  getFieldLocator(form, fieldName) {
    const field = form.fields.find(f => f.name === fieldName);
    return field ? field.locator : `[name="${fieldName}"]`;
  }

  getSubmitButtonLocator(form) {
    const submitButton = form.fields.find(f => f.type === 'submit');
    if (submitButton) return submitButton.locator;
    
    const button = form.fields.find(f => f.tag === 'button');
    if (button) return button.locator;
    
    return 'button[type="submit"], input[type="submit"]';
  }

  saveGeneratedTests() {
    const outputPath = path.join(__dirname, 'generated_tests.json');
    fs.writeFileSync(outputPath, JSON.stringify(this.testCases, null, 2));
    console.log(`📄 Generated tests saved to ${outputPath}`);
    
    // Also generate Playwright test file
    this.generatePlaywrightTestFile();
  }

  generatePlaywrightTestFile() {
    let testContent = `const { test, expect } = require('@playwright/test');\n\n`;
    
    // Add test data
    testContent += `const testData = {
  valid: {
    name: 'John Doe',
    email: 'test@example.com',
    phone: '+1234567890',
    address_line1: '123 Main Street',
    city: 'New York',
    state: 'NY',
    postal_code: '10001',
    country: 'USA',
    message: 'This is a test message',
    password: 'TestPassword123!'
  },
  invalid: {
    email: ['invalid-email', 'test@', '@domain.com'],
    shortText: 'A',
    longText: '${'A'.repeat(1000)}',
    specialChars: '<script>alert("xss")</script>',
    sqlInjection: "'; DROP TABLE users; --"
  }
};\n\n`;

    this.testCases.forEach(testSuite => {
      testContent += `test.describe('${testSuite.pageName} - ${testSuite.formId} Tests', () => {\n`;
      testContent += `  test.beforeEach(async ({ page }) => {\n`;
      testContent += `    await page.goto('http://localhost:8000/${this.getPageUrl(testSuite.pageName)}');\n`;
      testContent += `  });\n\n`;

      testSuite.tests.forEach(testCase => {
        testContent += `  test('${testCase.name}', async ({ page }) => {\n`;
        testContent += this.generateTestSteps(testCase.steps);
        testContent += `  });\n\n`;
      });

      testContent += `});\n\n`;
    });

    const outputPath = path.join(__dirname, 'generated_form_tests.spec.js');
    fs.writeFileSync(outputPath, testContent);
    console.log(`📄 Generated Playwright tests saved to ${outputPath}`);
  }

  generateTestSteps(steps) {
    let stepsContent = '';
    
    steps.forEach(step => {
      switch (step.action) {
        case 'fill':
          stepsContent += `    await page.fill('${step.locator}', '${step.value}');\n`;
          break;
        case 'click':
          stepsContent += `    await page.click('${step.locator}');\n`;
          break;
        case 'blur':
          stepsContent += `    await page.locator('${step.locator}').blur();\n`;
          break;
        case 'expect':
          if (step.condition === 'success_indicator_visible') {
            stepsContent += `    await expect(page.locator('.success-message, .alert-success')).toBeVisible();\n`;
          } else if (step.condition === 'validation_error_visible') {
            stepsContent += `    await expect(page.locator('${step.locator || '.error-message'}')).toBeVisible();\n`;
          }
          break;
        case 'fill_and_validate':
          stepsContent += `    await page.fill('${step.locator}', '${step.value}');\n`;
          stepsContent += `    await page.locator('${step.locator}').blur();\n`;
          if (step.expectError) {
            stepsContent += `    await expect(page.locator('.error-message')).toBeVisible();\n`;
          }
          break;
      }
    });
    
    return stepsContent;
  }

  getPageUrl(pageName) {
    const urls = {
      'Homepage': '',
      'Login': 'accounts/login/',
      'Checkout': 'orders/checkout/1/',
      'ContactForm': 'stores/test-store/',
      'HomepageEditor': 'stores/test-store/homepage/editor/'
    };
    
    return urls[pageName] || '';
  }
}

// Usage
if (require.main === module) {
  try {
    const formsData = JSON.parse(fs.readFileSync(path.join(__dirname, 'discovered_forms.json'), 'utf8'));
    const generator = new TestGenerator(formsData);
    generator.generateTests();
  } catch (error) {
    console.error('Error generating tests:', error.message);
    console.log('Please run form_discovery.js first to generate forms data.');
  }
}

module.exports = TestGenerator;