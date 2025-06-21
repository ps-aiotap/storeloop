const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function navigationDiscovery() {
  console.log('🔍 Navigation-based Discovery (no assumptions)...');
  
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  const discovered = new Map();
  const visited = new Set();
  const toVisit = ['http://localhost:8000/'];
  
  while (toVisit.length > 0 && visited.size < 20) {
    const currentUrl = toVisit.shift();
    
    if (visited.has(currentUrl)) continue;
    visited.add(currentUrl);
    
    try {
      console.log(`📍 Discovering: ${currentUrl}`);
      await page.goto(currentUrl, { timeout: 8000 });
      
      const pageData = await page.evaluate(() => {
        // Extract all navigation links
        const links = Array.from(document.querySelectorAll('a[href]')).map(link => ({
          href: link.href,
          text: link.textContent.trim(),
          className: link.className
        })).filter(link => 
          link.href.startsWith(window.location.origin) && 
          !link.href.includes('#') &&
          !link.href.includes('javascript:') &&
          link.text.length > 0
        );
        
        // Extract forms with detailed field info
        const forms = Array.from(document.querySelectorAll('form')).map((form, index) => ({
          id: form.id || `form-${index}`,
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
              const prevSibling = field.previousElementSibling;
              if (prevSibling && prevSibling.tagName === 'LABEL') {
                return prevSibling.textContent.trim();
              }
              return field.placeholder || '';
            })(),
            placeholder: field.placeholder || '',
            required: field.required,
            pattern: field.pattern || ''
          }))
        }));
        
        // Extract page metadata
        const navigation = Array.from(document.querySelectorAll('nav a, .nav a, .menu a, .navigation a')).map(link => ({
          href: link.href,
          text: link.textContent.trim()
        }));
        
        return {
          title: document.title,
          url: window.location.href,
          forms: forms,
          links: links,
          navigation: navigation,
          hasProducts: document.querySelectorAll('.product, [data-product-id], .item-card').length > 0,
          hasCheckout: document.querySelectorAll('[href*="checkout"], .checkout, .buy-now').length > 0,
          hasCart: document.querySelectorAll('[href*="cart"], .cart, .shopping-cart').length > 0
        };
      });
      
      discovered.set(currentUrl, pageData);
      
      console.log(`  ✅ ${pageData.forms.length} forms, ${pageData.links.length} links`);
      if (pageData.hasProducts) console.log(`  🛍️  Products found`);
      if (pageData.hasCheckout) console.log(`  💳 Checkout found`);
      
      // Add new URLs to visit
      pageData.links.forEach(link => {
        if (!visited.has(link.href) && !toVisit.includes(link.href)) {
          toVisit.push(link.href);
        }
      });
      
      // Also check navigation links
      pageData.navigation.forEach(link => {
        if (!visited.has(link.href) && !toVisit.includes(link.href)) {
          toVisit.push(link.href);
        }
      });
      
    } catch (error) {
      console.log(`  ❌ Error: ${error.message}`);
      discovered.set(currentUrl, {
        title: 'Error',
        url: currentUrl,
        forms: [],
        links: [],
        navigation: [],
        error: error.message
      });
    }
  }
  
  await browser.close();
  
  // Convert Map to Object for JSON
  const results = Object.fromEntries(discovered);
  
  // Save results
  fs.writeFileSync(path.join(__dirname, 'navigation_discovery.json'), JSON.stringify(results, null, 2));
  
  // Generate summary
  const totalForms = Object.values(results).reduce((sum, page) => sum + (page.forms?.length || 0), 0);
  const totalFields = Object.values(results).reduce((sum, page) => 
    sum + (page.forms?.reduce((fieldSum, form) => fieldSum + form.fields.length, 0) || 0), 0);
  const pagesWithForms = Object.values(results).filter(page => (page.forms?.length || 0) > 0).length;
  
  console.log(`\n📊 Navigation Discovery Complete:`);
  console.log(`   Pages discovered: ${Object.keys(results).length}`);
  console.log(`   Pages with forms: ${pagesWithForms}`);
  console.log(`   Total forms: ${totalForms}`);
  console.log(`   Total fields: ${totalFields}`);
  console.log(`   Data saved to: navigation_discovery.json`);
  
  // List discovered URLs
  console.log(`\n🔗 Discovered URLs:`);
  Object.keys(results).forEach(url => {
    const page = results[url];
    console.log(`   ${url} - ${page.forms?.length || 0} forms`);
  });
  
  return results;
}

if (require.main === module) {
  navigationDiscovery();
}

module.exports = navigationDiscovery;