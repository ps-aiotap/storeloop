const { chromium } = require('playwright');

async function manualTest() {
  console.log('🔍 Manual server test...');
  console.log('Make sure Django server is running: python manage.py runserver');
  console.log('Press Ctrl+C to stop this test\n');
  
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  try {
    await page.goto('http://localhost:8000/');
    console.log('✅ Connected to server');
    
    const title = await page.title();
    console.log(`📄 Page title: ${title}`);
    
    const forms = await page.locator('form').count();
    console.log(`📋 Forms found: ${forms}`);
    
    if (forms > 0) {
      const formData = await page.evaluate(() => {
        const forms = document.querySelectorAll('form');
        return Array.from(forms).map(form => ({
          id: form.id,
          action: form.action,
          fields: form.querySelectorAll('input, textarea, select').length
        }));
      });
      console.log('📊 Form details:', formData);
    }
    
    // Keep browser open for manual inspection
    console.log('\n🔍 Browser opened for manual inspection...');
    console.log('Press Ctrl+C to close');
    
    // Wait indefinitely
    await new Promise(() => {});
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    console.log('\n💡 Make sure to:');
    console.log('1. cd ../../');
    console.log('2. storeloop-venv\\Scripts\\activate');
    console.log('3. python manage.py runserver');
  }
}

manualTest();