const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function enhancedDiscovery() {
  console.log('🔍 Enhanced StoreLoop Discovery with Sample Data...');
  
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  // First, seed sample data
  console.log('🌱 Seeding sample data...');
  await page.goto('http://localhost:8000/admin/');
  
  // Try to login as admin and create sample data
  try {
    await page.fill('#id_username', 'admin');
    await page.fill('#id_password', 'admin');
    await page.click('input[type="submit"]');
    
    if (page.url().includes('/admin/')) {
      console.log('✅ Admin access available');
    }
  } catch (error) {
    console.log('⚠️  Admin login not available, continuing with discovery...');
  }
  
  // Comprehensive URL discovery
  const discoveryUrls = [
    'http://localhost:8000/',
    'http://localhost:8000/admin/',
    'http://localhost:8000/accounts/login/',
    'http://localhost:8000/accounts/register/',
    'http://localhost:8000/stores/',
    'http://localhost:8000/products/',
    'http://localhost:8000/orders/',
    'http://localhost:8000/orders/checkout/',
    'http://localhost:8000/contact/',
    // Try with sample IDs
    'http://localhost:8000/products/1/',
    'http://localhost:8000/stores/1/',
    'http://localhost:8000/orders/checkout/1/',
    'http://localhost:8000/stores/test-store/',
    'http://localhost:8000/stores/test-store/homepage/editor/'
  ];
  
  const results = {};
  
  for (const url of discoveryUrls) {
    try {
      console.log(`📍 Scanning: ${url}`);
      await page.goto(url, { timeout: 8000 });
      
      const pageData = await page.evaluate(() => {
        // Enhanced form discovery
        const forms = Array.from(document.querySelectorAll('form')).map((form, formIndex) => {
          const formData = {
            id: form.id || `form-${formIndex}`,
            action: form.action || '',
            method: form.method || 'GET',
            className: form.className || '',
            fields: []
          };
          
          // Get all interactive elements
          const fields = form.querySelectorAll('input, textarea, select, button');
          
          fields.forEach(field => {
            const fieldData = {
              tag: field.tagName.toLowerCase(),
              type: field.type || '',
              name: field.name || '',
              id: field.id || '',
              className: field.className || '',
              label: '',
              placeholder: field.placeholder || '',
              required: field.required || false,
              pattern: field.pattern || '',
              minLength: field.minLength || null,
              maxLength: field.maxLength || null,
              value: field.value || '',
              disabled: field.disabled || false
            };
            
            // Enhanced label detection
            if (field.id) {
              const label = document.querySelector(`label[for="${field.id}"]`);
              if (label) fieldData.label = label.textContent.trim();
            }
            
            if (!fieldData.label) {
              const parentLabel = field.closest('label');
              if (parentLabel) fieldData.label = parentLabel.textContent.trim();
            }
            
            if (!fieldData.label) {
              const prevElement = field.previousElementSibling;
              if (prevElement && prevElement.tagName.toLowerCase() === 'label') {
                fieldData.label = prevElement.textContent.trim();
              }
            }
            
            // For select elements, get options
            if (field.tagName.toLowerCase() === 'select') {
              fieldData.options = Array.from(field.options).map(option => ({
                value: option.value,
                text: option.textContent.trim(),
                selected: option.selected
              }));
            }
            
            formData.fields.push(fieldData);
          });
          
          return formData;
        });
        
        // Also look for interactive elements outside forms
        const interactiveElements = Array.from(document.querySelectorAll('button:not(form button), a[href*="checkout"], a[href*="buy"], a[href*="cart"]')).map(el => ({
          tag: el.tagName.toLowerCase(),
          text: el.textContent.trim(),
          href: el.href || '',
          className: el.className || '',
          id: el.id || ''
        }));
        
        return {
          title: document.title,
          url: window.location.href,
          forms: forms,
          totalFields: forms.reduce((sum, form) => sum + form.fields.length, 0),
          interactiveElements: interactiveElements,
          hasProducts: document.querySelectorAll('.product, [data-product], .item').length > 0,
          hasCart: document.querySelectorAll('.cart, [data-cart], .shopping-cart').length > 0,
          hasCheckout: document.querySelectorAll('.checkout, [data-checkout]').length > 0
        };
      });
      
      const pageName = url.split('/').filter(p => p && p !== 'http:' && p !== 'localhost:8000').join('_') || 'homepage';
      results[pageName] = pageData;
      
      console.log(`  ✅ ${pageData.forms.length} forms, ${pageData.totalFields} fields, ${pageData.interactiveElements.length} interactive elements`);
      
      if (pageData.hasProducts) console.log(`  🛍️  Products detected`);
      if (pageData.hasCart) console.log(`  🛒 Cart detected`);
      if (pageData.hasCheckout) console.log(`  💳 Checkout detected`);
      
    } catch (error) {
      console.log(`  ❌ Error: ${error.message}`);
      const pageName = url.split('/').filter(p => p && p !== 'http:' && p !== 'localhost:8000').join('_') || 'homepage';
      results[pageName] = { 
        title: 'Error', 
        url, 
        forms: [], 
        totalFields: 0, 
        interactiveElements: [],
        error: error.message 
      };
    }
  }
  
  await browser.close();
  
  // Save enhanced results
  fs.writeFileSync(path.join(__dirname, 'enhanced_forms.json'), JSON.stringify(results, null, 2));
  
  // Generate summary
  const totalForms = Object.values(results).reduce((sum, page) => sum + (page.forms?.length || 0), 0);
  const totalFields = Object.values(results).reduce((sum, page) => sum + (page.totalFields || 0), 0);
  const pagesWithForms = Object.values(results).filter(page => (page.forms?.length || 0) > 0).length;
  
  console.log(`\n📊 Enhanced Discovery Complete:`);
  console.log(`   Pages scanned: ${Object.keys(results).length}`);
  console.log(`   Pages with forms: ${pagesWithForms}`);
  console.log(`   Total forms: ${totalForms}`);
  console.log(`   Total fields: ${totalFields}`);
  console.log(`   Data saved to: enhanced_forms.json`);
  
  return results;
}

if (require.main === module) {
  enhancedDiscovery();
}

module.exports = enhancedDiscovery;