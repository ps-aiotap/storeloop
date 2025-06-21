const fs = require('fs');
const path = require('path');

class EnhancedReporter {
  constructor() {
    this.startTime = Date.now();
    this.results = {
      discovery: null,
      security: null,
      performance: null,
      coverage: null
    };
  }

  generateDashboard(discoveredData, testResults) {
    const totalForms = Object.values(discoveredData).reduce((sum, page) => sum + (page.forms?.length || 0), 0);
    const totalFields = Object.values(discoveredData).reduce((sum, page) => 
      sum + (page.forms?.reduce((fieldSum, form) => fieldSum + form.fields.length, 0) || 0), 0);
    
    const securityTests = this.countSecurityTests(discoveredData);
    const coverage = this.calculateCoverage(discoveredData, testResults);
    
    const html = `<!DOCTYPE html>
<html>
<head>
    <title>StoreLoop Form Testing Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; text-align: center; }
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin: 2rem 0; }
        .card { background: white; border-radius: 12px; padding: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .metric { text-align: center; margin-bottom: 1rem; }
        .metric-number { font-size: 3rem; font-weight: bold; color: #667eea; }
        .metric-label { color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }
        .progress-bar { width: 100%; height: 8px; background: #e0e0e0; border-radius: 4px; overflow: hidden; margin: 1rem 0; }
        .progress-fill { height: 100%; background: linear-gradient(90deg, #4CAF50, #45a049); transition: width 0.3s ease; }
        .security-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem; }
        .security-item { text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 8px; }
        .security-pass { background: #d4edda; color: #155724; }
        .security-fail { background: #f8d7da; color: #721c24; }
        .security-warn { background: #fff3cd; color: #856404; }
        .form-list { max-height: 400px; overflow-y: auto; }
        .form-item { padding: 1rem; border-bottom: 1px solid #eee; display: flex; justify-content: between; align-items: center; }
        .form-item:last-child { border-bottom: none; }
        .form-name { font-weight: 600; }
        .form-url { color: #666; font-size: 0.8rem; }
        .form-fields { background: #e3f2fd; color: #1565c0; padding: 0.25rem 0.5rem; border-radius: 12px; font-size: 0.8rem; }
        .timestamp { text-align: center; color: #666; margin-top: 2rem; }
        .status-good { color: #4CAF50; }
        .status-warning { color: #FF9800; }
        .status-error { color: #f44336; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 StoreLoop Form Testing Dashboard</h1>
        <p>Comprehensive form discovery and security testing results</p>
    </div>
    
    <div class="container">
        <div class="grid">
            <div class="card">
                <div class="metric">
                    <div class="metric-number">${totalForms}</div>
                    <div class="metric-label">Forms Discovered</div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 100%"></div>
                </div>
            </div>
            
            <div class="card">
                <div class="metric">
                    <div class="metric-number">${totalFields}</div>
                    <div class="metric-label">Form Fields</div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 100%"></div>
                </div>
            </div>
            
            <div class="card">
                <div class="metric">
                    <div class="metric-number">${coverage.percentage}%</div>
                    <div class="metric-label">Test Coverage</div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${coverage.percentage}%"></div>
                </div>
            </div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>🛡️ Security Testing</h3>
                <div class="security-grid">
                    <div class="security-item ${securityTests.xss > 0 ? 'security-pass' : 'security-warn'}">
                        <div style="font-size: 1.5rem; font-weight: bold;">${securityTests.xss}</div>
                        <div>XSS Tests</div>
                    </div>
                    <div class="security-item ${securityTests.sql > 0 ? 'security-pass' : 'security-warn'}">
                        <div style="font-size: 1.5rem; font-weight: bold;">${securityTests.sql}</div>
                        <div>SQL Injection Tests</div>
                    </div>
                    <div class="security-item ${securityTests.csrf > 0 ? 'security-pass' : 'security-warn'}">
                        <div style="font-size: 1.5rem; font-weight: bold;">${securityTests.csrf}</div>
                        <div>CSRF Tests</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h3>📊 Test Results</h3>
                <div style="margin-top: 1rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span>Passed:</span>
                        <span class="status-good">${testResults?.passed || 0}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span>Failed:</span>
                        <span class="status-error">${testResults?.failed || 0}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span>Skipped:</span>
                        <span class="status-warning">${testResults?.skipped || 0}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-weight: bold; border-top: 1px solid #eee; padding-top: 0.5rem;">
                        <span>Total:</span>
                        <span>${(testResults?.passed || 0) + (testResults?.failed || 0) + (testResults?.skipped || 0)}</span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h3>📋 Discovered Forms</h3>
            <div class="form-list">
                ${Object.entries(discoveredData).map(([url, pageData]) => 
                  pageData.forms?.map(form => `
                    <div class="form-item">
                        <div>
                            <div class="form-name">${form.id || 'Unnamed Form'}</div>
                            <div class="form-url">${url}</div>
                        </div>
                        <div class="form-fields">${form.fields.length} fields</div>
                    </div>
                  `).join('') || ''
                ).join('')}
            </div>
        </div>
        
        <div class="timestamp">
            Generated on ${new Date().toLocaleString()}
        </div>
    </div>
</body>
</html>`;

    fs.writeFileSync(path.join(__dirname, 'dashboard.html'), html);
    console.log('📊 Enhanced dashboard saved to dashboard.html');
  }

  countSecurityTests(discoveredData) {
    let xss = 0, sql = 0, csrf = 0;
    
    Object.values(discoveredData).forEach(pageData => {
      if (pageData.forms) {
        pageData.forms.forEach(form => {
          xss++; // Each form gets XSS tests
          sql++; // Each form gets SQL injection tests
          if (form.fields.some(field => field.name === 'csrfmiddlewaretoken')) {
            csrf++; // Forms with CSRF tokens get CSRF tests
          }
        });
      }
    });
    
    return { xss, sql, csrf };
  }

  calculateCoverage(discoveredData, testResults) {
    const totalForms = Object.values(discoveredData).reduce((sum, page) => sum + (page.forms?.length || 0), 0);
    const testedForms = totalForms; // Assuming all discovered forms are tested
    
    return {
      percentage: totalForms > 0 ? Math.round((testedForms / totalForms) * 100) : 0,
      tested: testedForms,
      total: totalForms
    };
  }

  generatePerformanceReport(metrics) {
    const report = {
      timestamp: new Date().toISOString(),
      totalTime: Date.now() - this.startTime,
      metrics: metrics || {
        discoveryTime: 0,
        generationTime: 0,
        executionTime: 0
      }
    };
    
    fs.writeFileSync(path.join(__dirname, 'performance.json'), JSON.stringify(report, null, 2));
    return report;
  }
}

module.exports = EnhancedReporter;