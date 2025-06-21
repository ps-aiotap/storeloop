const { spawn } = require('child_process');
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function startServerAndTest() {
  console.log('🚀 Starting Django server...');
  
  const projectRoot = path.resolve(__dirname, '../../');
  const isWindows = process.platform === 'win32';
  
  // Start Django server
  const serverCmd = isWindows 
    ? 'storeloop-venv\\Scripts\\activate.bat && python manage.py runserver'
    : 'source storeloop-venv/bin/activate && python manage.py runserver';
    
  const server = spawn('cmd', ['/c', serverCmd], { 
    cwd: projectRoot,
    shell: true 
  });
  
  server.stdout.on('data', (data) => {
    console.log(data.toString());
  });
  
  server.stderr.on('data', (data) => {
    console.error(data.toString());
  });
  
  // Wait for server to start
  console.log('⏳ Waiting for server to start...');
  await new Promise(resolve => setTimeout(resolve, 5000));
  
  // Test server
  try {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    
    console.log('🔍 Testing server connection...');
    await page.goto('http://localhost:8000/', { timeout: 10000 });
    console.log('✅ Server is running!');
    
    // Discover forms
    const forms = await page.evaluate(() => {
      const formElements = document.querySelectorAll('form');
      return Array.from(formElements).map((form, index) => ({
        id: form.id || `form-${index}`,
        action: form.action || '',
        method: form.method || 'GET',
        fields: Array.from(form.querySelectorAll('input, textarea, select')).map(field => ({
          name: field.name || '',
          type: field.type || '',
          id: field.id || '',
          required: field.required || false
        }))
      }));
    });
    
    console.log(`📋 Found ${forms.length} forms on homepage`);
    
    // Save results
    const results = { homepage: forms };
    fs.writeFileSync(path.join(__dirname, 'discovered_forms.json'), JSON.stringify(results, null, 2));
    
    await browser.close();
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    // Stop server
    console.log('🛑 Stopping server...');
    server.kill();
  }
}

startServerAndTest();