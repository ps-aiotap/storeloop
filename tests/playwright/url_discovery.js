const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const ServerManager = require('./server_manager');

class URLDiscovery {
  constructor() {
    this.browser = null;
    this.page = null;
    this.serverManager = new ServerManager();
    this.discoveredUrls = [];
  }

  async init() {
    await this.serverManager.startServer();
    this.browser = await chromium.launch({ headless: true });
    this.page = await this.browser.newPage();
  }

  async discoverUrls() {
    console.log('🔍 Discovering available URLs...');
    
    const testUrls = [
      'http://localhost:8000/',
      'http://localhost:8000/admin/',
      'http://localhost:8000/accounts/login/',
      'http://localhost:8000/stores/',
      'http://localhost:8000/products/'
    ];

    const visited = new Set();
    for (const url of testUrls) {
      await this.exploreUrl(url, visited);
    }
    
    await this.saveDiscoveredUrls();
    await this.browser.close();
    await this.serverManager.stopServer();
  }

  async exploreUrl(url, visited = new Set()) {
    if (visited.has(url)) return;
    visited.add(url);
    
    try {
      console.log(`📍 Exploring: ${url}`);
      await this.page.goto(url, { waitUntil: 'networkidle', timeout: 10000 });
      
      const formCount = await this.page.locator('form').count();
      if (formCount > 0) {
        this.discoveredUrls.push({
          url,
          hasForm: true,
          title: await this.page.title(),
          formCount
        });
        console.log(`  ✅ Found ${formCount} forms`);
      } else {
        console.log(`  ℹ️  No forms found`);
      }
    } catch (error) {
      console.log(`  ❌ Error exploring ${url}: ${error.message}`);
    }
  }

  async discoverStoresAndProducts() {
    try {
      // Try to access Django admin to see available data
      await this.page.goto('http://localhost:8000/admin/', { waitUntil: 'networkidle' });
      
      // Check if we can find any stores or products in the database
      const response = await this.page.evaluate(async () => {
        try {
          const storesResponse = await fetch('/api/stores/');
          const productsResponse = await fetch('/api/products/');
          return {
            stores: storesResponse.ok ? await storesResponse.json() : null,
            products: productsResponse.ok ? await productsResponse.json() : null
          };
        } catch {
          return { stores: null, products: null };
        }
      });

      console.log('📊 Database content discovery completed');
    } catch (error) {
      console.log('⚠️  Could not discover database content');
    }
  }

  async saveDiscoveredUrls() {
    const outputPath = path.join(__dirname, 'discovered_urls.json');
    fs.writeFileSync(outputPath, JSON.stringify(this.discoveredUrls, null, 2));
    console.log(`📄 Discovered URLs saved to ${outputPath}`);
    console.log(`🎯 Found ${this.discoveredUrls.length} URLs with forms`);
  }
}

// Run discovery
if (require.main === module) {
  (async () => {
    const discovery = new URLDiscovery();
    await discovery.init();
    await discovery.discoverUrls();
  })();
}

module.exports = URLDiscovery;