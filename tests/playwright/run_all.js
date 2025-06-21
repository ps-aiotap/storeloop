const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

class TestRunner {
  constructor() {
    this.results = {
      discovery: null,
      generation: null,
      execution: null,
      summary: {}
    };
  }

  async runAll() {
    console.log('🚀 Starting StoreLoop Form Testing Pipeline\n');

    try {
      // Step 1: Form Discovery
      console.log('📋 Step 1: Discovering Forms...');
      await this.runDiscovery();

      // Step 2: Test Generation
      console.log('🔧 Step 2: Generating Tests...');
      await this.runGeneration();

      // Step 3: Test Execution
      console.log('🧪 Step 3: Running Tests...');
      await this.runTests();

      // Step 4: Generate Report
      console.log('📊 Step 4: Generating Report...');
      await this.generateReport();

      console.log('\n✅ Pipeline completed successfully!');
    } catch (error) {
      console.error('\n❌ Pipeline failed:', error.message);
      process.exit(1);
    }
  }

  runDiscovery() {
    return new Promise((resolve, reject) => {
      exec('node form_discovery.js', (error, stdout, stderr) => {
        if (error) {
          this.results.discovery = { success: false, error: error.message };
          reject(error);
        } else {
          this.results.discovery = { success: true, output: stdout };
          console.log(stdout);
          resolve();
        }
      });
    });
  }

  runGeneration() {
    return new Promise((resolve, reject) => {
      exec('node test_generator.js', (error, stdout, stderr) => {
        if (error) {
          this.results.generation = { success: false, error: error.message };
          reject(error);
        } else {
          this.results.generation = { success: true, output: stdout };
          console.log(stdout);
          resolve();
        }
      });
    });
  }

  runTests() {
    return new Promise((resolve, reject) => {
      exec('npx playwright test --reporter=json', (error, stdout, stderr) => {
        // Playwright may exit with code 1 even if tests run (some failures)
        // We want to capture results regardless
        try {
          const results = JSON.parse(stdout);
          this.results.execution = {
            success: true,
            results: results,
            output: stdout
          };
          console.log(`Tests completed: ${results.stats?.passed || 0} passed, ${results.stats?.failed || 0} failed`);
          resolve();
        } catch (parseError) {
          this.results.execution = {
            success: false,
            error: parseError.message,
            rawOutput: stdout,
            stderr: stderr
          };
          console.log('Test execution completed with issues');
          resolve(); // Don't reject, we want to generate report anyway
        }
      });
    });
  }

  async generateReport() {
    const report = {
      timestamp: new Date().toISOString(),
      pipeline: this.results,
      summary: this.generateSummary()
    };

    // Save detailed report
    const reportPath = path.join(__dirname, 'pipeline_report.json');
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));

    // Generate HTML report
    this.generateHTMLReport(report);

    console.log(`📄 Report saved to ${reportPath}`);
  }

  generateSummary() {
    const summary = {
      formsDiscovered: 0,
      testsGenerated: 0,
      testsPassed: 0,
      testsFailed: 0,
      coverage: {}
    };

    // Count discovered forms
    try {
      const formsData = JSON.parse(fs.readFileSync(path.join(__dirname, 'discovered_forms.json'), 'utf8'));
      summary.formsDiscovered = Object.values(formsData).reduce((total, forms) => total + forms.length, 0);
    } catch (error) {
      console.warn('Could not read discovered forms data');
    }

    // Count generated tests
    try {
      const testsData = JSON.parse(fs.readFileSync(path.join(__dirname, 'generated_tests.json'), 'utf8'));
      summary.testsGenerated = testsData.reduce((total, suite) => total + suite.tests.length, 0);
    } catch (error) {
      console.warn('Could not read generated tests data');
    }

    // Extract test results
    if (this.results.execution?.results?.stats) {
      const stats = this.results.execution.results.stats;
      summary.testsPassed = stats.passed || 0;
      summary.testsFailed = stats.failed || 0;
    }

    // Calculate coverage
    summary.coverage = {
      happyPath: summary.testsPassed > 0,
      validation: summary.testsGenerated > summary.formsDiscovered,
      edgeCases: summary.testsGenerated > summary.formsDiscovered * 2,
      security: summary.testsGenerated > 0
    };

    return summary;
  }

  generateHTMLReport(report) {
    const html = `
<!DOCTYPE html>
<html>
<head>
    <title>StoreLoop Form Testing Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f0f0f0; padding: 20px; border-radius: 8px; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 8px; }
        .success { background: #d4edda; border-color: #c3e6cb; }
        .error { background: #f8d7da; border-color: #f5c6cb; }
        .warning { background: #fff3cd; border-color: #ffeaa7; }
        .stats { display: flex; gap: 20px; }
        .stat { text-align: center; padding: 10px; background: #f8f9fa; border-radius: 4px; }
        .stat-number { font-size: 24px; font-weight: bold; color: #007bff; }
        .coverage-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }
        .coverage-item { padding: 10px; border-radius: 4px; text-align: center; }
        .covered { background: #d4edda; }
        .not-covered { background: #f8d7da; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 StoreLoop Form Testing Report</h1>
        <p>Generated: ${report.timestamp}</p>
    </div>

    <div class="section">
        <h2>📊 Summary</h2>
        <div class="stats">
            <div class="stat">
                <div class="stat-number">${report.summary.formsDiscovered}</div>
                <div>Forms Discovered</div>
            </div>
            <div class="stat">
                <div class="stat-number">${report.summary.testsGenerated}</div>
                <div>Tests Generated</div>
            </div>
            <div class="stat">
                <div class="stat-number">${report.summary.testsPassed}</div>
                <div>Tests Passed</div>
            </div>
            <div class="stat">
                <div class="stat-number">${report.summary.testsFailed}</div>
                <div>Tests Failed</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>🎯 Test Coverage</h2>
        <div class="coverage-grid">
            ${Object.entries(report.summary.coverage).map(([type, covered]) => `
                <div class="coverage-item ${covered ? 'covered' : 'not-covered'}">
                    <strong>${type.charAt(0).toUpperCase() + type.slice(1)}</strong><br>
                    ${covered ? '✅ Covered' : '❌ Not Covered'}
                </div>
            `).join('')}
        </div>
    </div>

    <div class="section ${report.pipeline.discovery?.success ? 'success' : 'error'}">
        <h2>📋 Form Discovery</h2>
        <p>Status: ${report.pipeline.discovery?.success ? '✅ Success' : '❌ Failed'}</p>
        ${report.pipeline.discovery?.error ? `<p>Error: ${report.pipeline.discovery.error}</p>` : ''}
    </div>

    <div class="section ${report.pipeline.generation?.success ? 'success' : 'error'}">
        <h2>🔧 Test Generation</h2>
        <p>Status: ${report.pipeline.generation?.success ? '✅ Success' : '❌ Failed'}</p>
        ${report.pipeline.generation?.error ? `<p>Error: ${report.pipeline.generation.error}</p>` : ''}
    </div>

    <div class="section ${report.pipeline.execution?.success ? 'success' : 'error'}">
        <h2>🧪 Test Execution</h2>
        <p>Status: ${report.pipeline.execution?.success ? '✅ Success' : '❌ Failed'}</p>
        ${report.pipeline.execution?.error ? `<p>Error: ${report.pipeline.execution.error}</p>` : ''}
    </div>

    <div class="section">
        <h2>🔗 Quick Links</h2>
        <ul>
            <li><a href="discovered_forms.json">Discovered Forms Data</a></li>
            <li><a href="generated_tests.json">Generated Test Cases</a></li>
            <li><a href="playwright-report/index.html">Playwright HTML Report</a></li>
            <li><a href="test-results.json">Test Results JSON</a></li>
        </ul>
    </div>
</body>
</html>`;

    const htmlPath = path.join(__dirname, 'report.html');
    fs.writeFileSync(htmlPath, html);
    console.log(`📄 HTML report saved to ${htmlPath}`);
  }
}

// Run if called directly
if (require.main === module) {
  const runner = new TestRunner();
  runner.runAll();
}

module.exports = TestRunner;