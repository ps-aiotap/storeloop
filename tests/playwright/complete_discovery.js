const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function completeDiscovery() {
  console.log('🔍 Complete StoreLoop Form Discovery...');
  
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  const allUrls = [
    'http://localhost:8000/',
    'http://localhost:8000/admin/',
    'http://localhost:8000/accounts/login/',
    'http://localhost:8000/stores/',
    'http://localhost:8000/products/'
  ];
  
  const results = {};
  
  for (const url of allUrls) {
    try {
      console.log(`📍 Scanning: ${url}`);
      await page.goto(url, { timeout: 10000 });
      
      const pageData = await page.evaluate(() => {
        const forms = Array.from(document.querySelectorAll('form')).map((form, formIndex) => ({
          id: form.id || `form-${formIndex}`,
          action: form.action || '',
          method: form.method || 'GET',
          fields: Array.from(form.querySelectorAll('input, textarea, select, button')).map(field => ({
            tag: field.tagName.toLowerCase(),
            type: field.type || '',
            name: field.name || '',
            id: field.id || '',
            label: (() => {
              if (field.id) {
                const label = document.querySelector(`label[for="${field.id}"]`);
                if (label) return label.textContent.trim();
              }
              const parentLabel = field.closest('label');
              if (parentLabel) return parentLabel.textContent.trim();
              return field.placeholder || field.name || '';
            })(),
            placeholder: field.placeholder || '',
            required: field.required || false,
            pattern: field.pattern || '',
            minLength: field.minLength || null,
            maxLength: field.maxLength || null
          }))
        }));
        
        return {
          title: document.title,
          url: window.location.href,
          forms: forms,
          totalFields: forms.reduce((sum, form) => sum + form.fields.length, 0)
        };
      });
      
      const pageName = url.split('/').filter(p => p).pop() || 'homepage';
      results[pageName] = pageData;
      
      console.log(`  ✅ ${pageData.forms.length} forms, ${pageData.totalFields} fields`);
      
    } catch (error) {
      console.log(`  ❌ Error: ${error.message}`);
      const pageName = url.split('/').filter(p => p).pop() || 'homepage';
      results[pageName] = { title: 'Error', url, forms: [], totalFields: 0 };
    }
  }
  
  await browser.close();
  
  // Save detailed results
  fs.writeFileSync(path.join(__dirname, 'complete_forms.json'), JSON.stringify(results, null, 2));
  
  // Summary
  const totalForms = Object.values(results).reduce((sum, page) => sum + page.forms.length, 0);
  const totalFields = Object.values(results).reduce((sum, page) => sum + page.totalFields, 0);
  
  console.log(`\n📊 Discovery Complete:`);
  console.log(`   Pages scanned: ${Object.keys(results).length}`);
  console.log(`   Forms found: ${totalForms}`);
  console.log(`   Fields found: ${totalFields}`);
  console.log(`   Data saved to: complete_forms.json`);
  
  return results;
}

if (require.main === module) {
  completeDiscovery();
}

module.exports = completeDiscovery;