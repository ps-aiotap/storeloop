const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const ServerManager = require('./server_manager');

class FormDiscovery {
  constructor() {
    this.browser = null;
    this.page = null;
    this.formsData = {};
    this.serverManager = new ServerManager();
  }

  async init() {
    await this.serverManager.startServer();
    this.browser = await chromium.launch({ headless: false });
    this.page = await this.browser.newPage();
  }

  async discoverForms() {
    // First discover available URLs
    const URLDiscovery = require('./url_discovery');
    const urlDiscovery = new URLDiscovery();
    await urlDiscovery.init();
    await urlDiscovery.discoverUrls();
    await urlDiscovery.browser.close();
    await urlDiscovery.serverManager.stopServer();
    
    // Load discovered URLs
    let pages = [];
    try {
      const discoveredUrls = JSON.parse(fs.readFileSync(path.join(__dirname, 'discovered_urls.json'), 'utf8'));
      pages = discoveredUrls.map((item, index) => ({
        name: item.title || `Page${index + 1}`,
        url: item.url
      }));
    } catch {
      // Fallback to default pages
      pages = [
        { name: 'Homepage', url: 'http://localhost:8000/' },
        { name: 'Login', url: 'http://localhost:8000/accounts/login/' }
      ];
    }
    
    console.log(`🎯 Testing ${pages.length} discovered pages`);
    
    // Restart server for form discovery
    await this.serverManager.startServer();

    for (const pageInfo of pages) {
      try {
        await this.page.goto(pageInfo.url, { waitUntil: 'networkidle' });
        await this.page.waitForTimeout(2000);
        
        const forms = await this.extractForms();
        this.formsData[pageInfo.name] = forms;
        
        console.log(`✅ Discovered ${forms.length} forms on ${pageInfo.name}`);
      } catch (error) {
        console.log(`❌ Error discovering forms on ${pageInfo.name}: ${error.message}`);
        this.formsData[pageInfo.name] = [];
      }
    }

    await this.saveFormsData();
    await this.browser.close();
    await this.serverManager.stopServer();
  }

  async extractForms() {
    return await this.page.evaluate(() => {
      const forms = [];
      const formElements = document.querySelectorAll('form');

      formElements.forEach((form, formIndex) => {
        const formData = {
          formId: form.id || `form-${formIndex}`,
          action: form.action || '',
          method: form.method || 'GET',
          fields: []
        };

        const fields = form.querySelectorAll('input, textarea, select, button[type="submit"]');
        
        fields.forEach(field => {
          const fieldData = {
            tag: field.tagName.toLowerCase(),
            type: field.type || '',
            name: field.name || '',
            id: field.id || '',
            label: getFieldLabel(field),
            placeholder: field.placeholder || '',
            required: field.required || false,
            pattern: field.pattern || '',
            minLength: field.minLength || null,
            maxLength: field.maxLength || null,
            testId: field.getAttribute('data-testid') || '',
            ariaLabel: field.getAttribute('aria-label') || '',
            locator: generateLocator(field)
          };

          if (field.tagName.toLowerCase() === 'select') {
            fieldData.options = Array.from(field.options).map(option => ({
              value: option.value,
              text: option.textContent.trim()
            }));
          }

          formData.fields.push(fieldData);
        });

        forms.push(formData);
      });

      function generateLocator(field) {
        if (field.getAttribute('data-testid')) {
          return `[data-testid="${field.getAttribute('data-testid')}"]`;
        }
        if (field.id) {
          return `#${field.id}`;
        }
        if (field.name) {
          return `[name="${field.name}"]`;
        }
        return field.tagName.toLowerCase();
      }

      function getFieldLabel(field) {
        if (field.id) {
          const label = document.querySelector(`label[for="${field.id}"]`);
          if (label) return label.textContent.trim();
        }
        
        const parentLabel = field.closest('label');
        if (parentLabel) return parentLabel.textContent.trim();
        
        const prevLabel = field.previousElementSibling;
        if (prevLabel && prevLabel.tagName.toLowerCase() === 'label') {
          return prevLabel.textContent.trim();
        }
        
        return field.placeholder || field.name || '';
      }

      return forms;
    });
  }

  async saveFormsData() {
    const outputPath = path.join(__dirname, 'discovered_forms.json');
    fs.writeFileSync(outputPath, JSON.stringify(this.formsData, null, 2));
    console.log(`📄 Forms data saved to ${outputPath}`);
  }
}

(async () => {
  const discovery = new FormDiscovery();
  await discovery.init();
  await discovery.discoverForms();
})();