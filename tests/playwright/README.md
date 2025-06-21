# StoreLoop Playwright Form Testing

Automated form discovery and testing for StoreLoop using Playwright.

## Setup

1. Install dependencies:
```bash
cd tests/playwright
npm install
playwright install
```

2. Start Django development server:
```bash
cd ../../
python manage.py runserver
```

3. Seed test data:
```bash
python manage.py seed_sample_data --users 2 --stores 1 --products 5
```

## Usage

### 1. Setup Environment
```bash
# Ensure Django server can start:
cd ../../
source storeloop-venv/bin/activate  # Windows: storeloop-venv\Scripts\activate
python manage.py runserver
# Test in browser: http://localhost:8000
# Ctrl+C to stop
```

### 2. Discover URLs
```bash
cd tests/playwright
npm run discover-urls
```
This will find available pages with forms.

### 3. Discover Forms
```bash
npm run discover
```
This will extract form elements from discovered pages.

### 4. Generate Tests
```bash
npm run generate
```
This will create comprehensive test cases.

### 5. Run Tests
```bash
# Run all tests
npm test

# Run with browser visible
npm run test:headed

# Full pipeline
npm run full-pipeline
```

## Test Coverage

### Happy Path Tests
- ✅ Valid form submissions
- ✅ Success confirmations
- ✅ Proper redirects

### Validation Tests
- ✅ Required field validation
- ✅ Email format validation
- ✅ Phone number validation
- ✅ Postal code validation
- ✅ Minimum length validation
- ✅ Pattern matching

### Edge Cases
- ✅ Empty inputs
- ✅ Special characters
- ✅ Long text inputs
- ✅ Multiple spaces
- ✅ Emoji handling
- ✅ Multiple form submissions

### Security Tests
- ✅ XSS prevention
- ✅ SQL injection prevention
- ✅ CSRF token validation
- ✅ Input sanitization

### Accessibility Tests
- ✅ Label associations
- ✅ Keyboard navigation
- ✅ ARIA attributes
- ✅ Focus management

## Generated Files

- `discovered_forms.json` - Form discovery results
- `generated_tests.json` - Test case definitions
- `generated_form_tests.spec.js` - Auto-generated Playwright tests
- `test-results/` - Test execution reports

## Form Structure

Each discovered form includes:
```json
{
  "formId": "checkout-form",
  "action": "/orders/checkout/",
  "method": "POST",
  "fields": [
    {
      "tag": "input",
      "type": "text",
      "name": "name",
      "id": "name",
      "label": "Name",
      "required": true,
      "locator": "#name"
    }
  ]
}
```

## Test Categories

### 🟩 Happy Path
- Valid data submission
- Success indicators
- Proper navigation

### 🟥 Validation
- Required fields
- Format validation
- Length constraints

### 🟨 Edge Cases
- Boundary values
- Special characters
- Performance limits

### 🟪 Security
- XSS prevention
- Injection attacks
- Token validation

### 🟦 Accessibility
- Screen reader support
- Keyboard navigation
- ARIA compliance