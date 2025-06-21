const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function discoverForms() {
  console.log('🔍 Starting simple form discovery...');
  
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  const testUrls = [
    'http://localhost:8000/',
    'http://localhost:8000/admin/',
    'http://localhost:8000/accounts/login/'
  ];
  
  const results = {};
  
  for (const url of testUrls) {
    try {
      console.log(`📍 Testing: ${url}`);
      await page.goto(url, { timeout: 5000 });
      
      const forms = await page.evaluate(() => {
        const formElements = document.querySelectorAll('form');
        return Array.from(formElements).map((form, index) => ({
          id: form.id || `form-${index}`,
          action: form.action || '',
          method: form.method || 'GET',
          fieldCount: form.querySelectorAll('input, textarea, select').length
        }));
      });
      
      const pageName = url.split('/').pop() || 'homepage';
      results[pageName] = forms;
      
      console.log(`  ✅ Found ${forms.length} forms with ${forms.reduce((sum, f) => sum + f.fieldCount, 0)} total fields`);
      
    } catch (error) {
      console.log(`  ❌ Error: ${error.message}`);
      results[url] = [];
    }
  }
  
  // Save results
  const outputPath = path.join(__dirname, 'simple_forms.json');
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log(`📄 Results saved to ${outputPath}`);
  
  await browser.close();
  return results;
}

if (require.main === module) {
  discoverForms();
}

module.exports = discoverForms;