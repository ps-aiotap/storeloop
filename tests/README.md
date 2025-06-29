# StoreLoop Playwright Test Suite

Comprehensive end-to-end testing for the StoreLoop Indian Artisan Platform using Playwright and TypeScript.

## 🎯 Test Coverage

### **Buyer Flows**
- ✅ Homepage navigation and feature discovery
- ✅ Store listing and discovery
- ✅ Individual store browsing
- ✅ Product catalog viewing
- ✅ Shopping cart functionality
- ✅ Mobile shopping experience
- ✅ Currency display (₹ Indian Rupees)
- ✅ Error handling (404 pages)

### **Seller Flows**
- ✅ 5-step onboarding wizard
- ✅ Hindi store name support and slug generation
- ✅ Seller dashboard analytics
- ✅ Product management (add/edit)
- ✅ Bulk CSV/Excel upload
- ✅ AI description generation
- ✅ Mobile dashboard responsiveness
- ✅ Store publication workflow

### **NGO Partner Admin**
- ✅ Multi-store management dashboard
- ✅ Aggregate analytics across stores
- ✅ Store switching functionality
- ✅ Artisan support features
- ✅ Hindi interface support

### **Authentication & Security**
- ✅ Login/logout functionality
- ✅ Protected route access
- ✅ Session persistence
- ✅ Form validation
- ✅ Mobile authentication

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- Django development server running

### Installation
```bash
# Install Playwright dependencies
cd tests
npm install
npx playwright install

# Run all tests
npm test

# Run specific test suites
npm run test:buyer
npm run test:seller
npm run test:ngo
npm run test:auth
```

### Using the Deployment Script
```bash
# Windows - Complete deployment and testing
deploy.bat

# This will:
# 1. Set up Python environment
# 2. Run database migrations
# 3. Create test data
# 4. Start Django server
# 5. Run all Playwright tests
# 6. Generate HTML report
```

## 📊 Test Reports

Tests generate multiple report formats:
- **HTML Report**: `test-results/html-report/index.html`
- **JSON Results**: `test-results/results.json`
- **JUnit XML**: `test-results/results.xml`

View reports:
```bash
npm run test:report
```

## 🔧 Configuration

### Environment Variables
Create `.env.test` for test-specific configuration:
```env
DEBUG=True
USE_SQLITE=True
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
NGO_USERNAME=ngo_admin
NGO_PASSWORD=password
```

### Browser Configuration
Tests run on multiple browsers:
- Desktop Chrome
- Desktop Firefox
- Desktop Safari
- Mobile Chrome (Pixel 5)
- Mobile Safari (iPhone 12)

## 📱 Mobile Testing

Run mobile-specific tests:
```bash
npm run test:mobile
```

Mobile tests verify:
- Responsive design
- Touch-friendly interfaces
- Mobile navigation
- Cart functionality on mobile
- Form usability on small screens

## 🌐 Cross-Browser Testing

Run tests across all browsers:
```bash
npm run test:cross-browser
```

## 🐛 Debugging

### Debug Mode
```bash
npm run test:debug
```

### UI Mode
```bash
npm run test:ui
```

### Screenshots and Videos
- Screenshots: Captured on test failure
- Videos: Recorded for failed tests
- Traces: Available for debugging

## 📝 Test Structure

```
tests/
├── fixtures/
│   └── auth.ts              # Authentication fixtures
├── pages/                   # Page object models (future)
├── utils/                   # Test utilities (future)
├── buyer-flows.spec.ts      # Buyer journey tests
├── seller-onboarding.spec.ts # 5-step wizard tests
├── seller-dashboard.spec.ts  # Dashboard functionality
├── product-management.spec.ts # Product CRUD tests
├── ngo-admin.spec.ts        # NGO partner tests
├── authentication.spec.ts   # Login/logout tests
├── playwright.config.ts     # Playwright configuration
└── package.json            # Dependencies and scripts
```

## 🎨 Test Features

### Hindi Language Support
Tests verify:
- Hindi store names (कलाकार शिल्प)
- Hindi product names (मिट्टी का दीया)
- Hindi UI elements
- Proper slug generation for Hindi text

### Indian-Specific Features
- ₹ (Rupee) currency display
- GST number validation
- Indian address formats
- WhatsApp integration (stub testing)

### Mobile-First Design
- Touch-friendly button sizes (>40px height)
- Responsive grid layouts
- Mobile navigation patterns
- Cart functionality on mobile

## 🔍 Key Test Scenarios

### Critical User Journeys
1. **New Seller Onboarding**: Complete 5-step wizard
2. **Product Management**: Add products with Hindi names
3. **Store Discovery**: Browse and find stores
4. **Mobile Shopping**: Complete purchase on mobile
5. **NGO Management**: Manage multiple artisan stores

### Edge Cases
- Empty form submissions
- Invalid login credentials
- Non-existent URLs (404 handling)
- Mobile viewport testing
- Cross-browser compatibility

## 📈 Performance Considerations

Tests include:
- Page load time verification
- Image loading checks
- Form submission responsiveness
- Mobile performance validation

## 🛠️ Maintenance

### Adding New Tests
1. Create new `.spec.ts` file
2. Use existing fixtures for authentication
3. Follow naming conventions
4. Add to package.json scripts if needed

### Updating Selectors
- Use stable selectors (data-testid preferred)
- Avoid brittle CSS selectors
- Test across different browsers
- Consider mobile viewport differences

## 🚨 Troubleshooting

### Common Issues
1. **Server not running**: Ensure Django server is at localhost:8000
2. **Database issues**: Run migrations before testing
3. **Browser installation**: Run `npx playwright install`
4. **Test data**: Ensure admin/ngo_admin users exist

### Debug Commands
```bash
# Check server status
curl http://localhost:8000

# Verify test data
python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.all())"

# Run single test with debug
npx playwright test authentication.spec.ts --debug
```

## 📋 Test Checklist

Before running tests, ensure:
- [ ] Django server running on localhost:8000
- [ ] Database migrations applied
- [ ] Test users created (admin, ngo_admin)
- [ ] Sample stores and products exist
- [ ] Node.js dependencies installed
- [ ] Playwright browsers installed

## 🎯 Success Criteria

Tests verify StoreLoop's key differentiators:
- ✅ Zero transaction fees (vs competitors)
- ✅ Hindi UI support
- ✅ AI description generation
- ✅ WhatsApp integration
- ✅ GST compliance
- ✅ NGO multi-store management
- ✅ Mobile-first design
- ✅ Indian artisan focus

---

**Ready to test StoreLoop's unique features for Indian artisans! 🇮🇳**