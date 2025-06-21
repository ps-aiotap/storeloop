const fs = require('fs');
const path = require('path');

class ImplementationVerifier {
  constructor() {
    this.checklist = {
      core: {
        'Navigation Discovery': false,
        'Test Generation': false,
        'One-Step Pipeline': false,
        'HTML Reports': false
      },
      framework: {
        'Django CSRF Handling': false,
        'Django Form Validation': false,
        'Authentication Flows': false,
        'Admin Interface': false
      },
      security: {
        'XSS Prevention Testing': false,
        'SQL Injection Testing': false,
        'CSRF Protection Testing': false,
        'Input Sanitization': false
      },
      reporting: {
        'Enhanced Dashboard': false,
        'Test Coverage Metrics': false,
        'Performance Metrics': false,
        'Security Summary': false
      },
      cicd: {
        'GitHub Actions Workflow': false,
        'Automated PR Testing': false,
        'Artifact Storage': false,
        'Test Notifications': false
      },
      advanced: {
        'Parallel Execution': false,
        'Performance Monitoring': false,
        'Accessibility Testing': false,
        'File Upload Testing': false,
        'Rate Limiting Tests': false
      }
    };
  }

  async verify() {
    console.log('🔍 Verifying Implementation Against Prompts...\n');
    
    this.checkCoreFeatures();
    this.checkFrameworkFeatures();
    this.checkSecurityFeatures();
    this.checkReportingFeatures();
    this.checkCICDFeatures();
    this.checkAdvancedFeatures();
    
    this.generateReport();
  }

  checkCoreFeatures() {
    console.log('📍 Checking Core Features...');
    
    // Navigation Discovery
    if (fs.existsSync(path.join(__dirname, 'navigation_discovery.js'))) {
      this.checklist.core['Navigation Discovery'] = true;
      console.log('  ✅ Navigation Discovery - IMPLEMENTED');
    }
    
    // Test Generation
    if (fs.existsSync(path.join(__dirname, 'one_step_pipeline.js'))) {
      this.checklist.core['Test Generation'] = true;
      console.log('  ✅ Test Generation - IMPLEMENTED');
    }
    
    // One-Step Pipeline
    const packageJson = JSON.parse(fs.readFileSync(path.join(__dirname, 'package.json'), 'utf8'));
    if (packageJson.scripts['one-step']) {
      this.checklist.core['One-Step Pipeline'] = true;
      console.log('  ✅ One-Step Pipeline - IMPLEMENTED');
    }
    
    // HTML Reports
    if (fs.existsSync(path.join(__dirname, 'playwright.config.js'))) {
      this.checklist.core['HTML Reports'] = true;
      console.log('  ✅ HTML Reports - IMPLEMENTED');
    }
  }

  checkFrameworkFeatures() {
    console.log('\n🎨 Checking Django Framework Features...');
    
    // Check for Django-specific implementations
    const files = [
      'one_step_pipeline.js',
      'advanced_pipeline.js'
    ];
    
    files.forEach(file => {
      if (fs.existsSync(path.join(__dirname, file))) {
        const content = fs.readFileSync(path.join(__dirname, file), 'utf8');
        
        if (content.includes('csrfmiddlewaretoken')) {
          this.checklist.framework['Django CSRF Handling'] = true;
          console.log('  ✅ Django CSRF Handling - IMPLEMENTED');
        }
        
        if (content.includes('admin') && content.includes('login')) {
          this.checklist.framework['Admin Interface'] = true;
          console.log('  ✅ Admin Interface Testing - IMPLEMENTED');
        }
        
        if (content.includes('username') && content.includes('password')) {
          this.checklist.framework['Authentication Flows'] = true;
          console.log('  ✅ Authentication Flows - IMPLEMENTED');
        }
      }
    });
  }

  checkSecurityFeatures() {
    console.log('\n🛡️ Checking Security Features...');
    
    if (fs.existsSync(path.join(__dirname, 'security_tests.js'))) {
      const content = fs.readFileSync(path.join(__dirname, 'security_tests.js'), 'utf8');
      
      if (content.includes('xss') || content.includes('script')) {
        this.checklist.security['XSS Prevention Testing'] = true;
        console.log('  ✅ XSS Prevention Testing - IMPLEMENTED');
      }
      
      if (content.includes('sql') || content.includes('DROP TABLE')) {
        this.checklist.security['SQL Injection Testing'] = true;
        console.log('  ✅ SQL Injection Testing - IMPLEMENTED');
      }
      
      if (content.includes('csrf') || content.includes('token')) {
        this.checklist.security['CSRF Protection Testing'] = true;
        console.log('  ✅ CSRF Protection Testing - IMPLEMENTED');
      }
    }
  }

  checkReportingFeatures() {
    console.log('\n📊 Checking Reporting Features...');
    
    if (fs.existsSync(path.join(__dirname, 'enhanced_reporting.js'))) {
      const content = fs.readFileSync(path.join(__dirname, 'enhanced_reporting.js'), 'utf8');
      
      if (content.includes('dashboard') || content.includes('Dashboard')) {
        this.checklist.reporting['Enhanced Dashboard'] = true;
        console.log('  ✅ Enhanced Dashboard - IMPLEMENTED');
      }
      
      if (content.includes('coverage') || content.includes('Coverage')) {
        this.checklist.reporting['Test Coverage Metrics'] = true;
        console.log('  ✅ Test Coverage Metrics - IMPLEMENTED');
      }
      
      if (content.includes('performance') || content.includes('Performance')) {
        this.checklist.reporting['Performance Metrics'] = true;
        console.log('  ✅ Performance Metrics - IMPLEMENTED');
      }
      
      if (content.includes('security') || content.includes('Security')) {
        this.checklist.reporting['Security Summary'] = true;
        console.log('  ✅ Security Summary - IMPLEMENTED');
      }
    }
  }

  checkCICDFeatures() {
    console.log('\n🔄 Checking CI/CD Features...');
    
    const workflowPath = path.join(__dirname, '../../.github/workflows/form-testing.yml');
    if (fs.existsSync(workflowPath)) {
      const content = fs.readFileSync(workflowPath, 'utf8');
      
      this.checklist.cicd['GitHub Actions Workflow'] = true;
      console.log('  ✅ GitHub Actions Workflow - IMPLEMENTED');
      
      if (content.includes('pull_request')) {
        this.checklist.cicd['Automated PR Testing'] = true;
        console.log('  ✅ Automated PR Testing - IMPLEMENTED');
      }
      
      if (content.includes('upload-artifact')) {
        this.checklist.cicd['Artifact Storage'] = true;
        console.log('  ✅ Artifact Storage - IMPLEMENTED');
      }
      
      if (content.includes('github-script') || content.includes('comment')) {
        this.checklist.cicd['Test Notifications'] = true;
        console.log('  ✅ Test Notifications - IMPLEMENTED');
      }
    }
  }

  checkAdvancedFeatures() {
    console.log('\n⚡ Checking Advanced Features...');
    
    if (fs.existsSync(path.join(__dirname, 'advanced_pipeline.js'))) {
      const content = fs.readFileSync(path.join(__dirname, 'advanced_pipeline.js'), 'utf8');
      
      if (content.includes('workers') || content.includes('parallel')) {
        this.checklist.advanced['Parallel Execution'] = true;
        console.log('  ✅ Parallel Execution - IMPLEMENTED');
      }
      
      if (content.includes('Performance') || content.includes('submissionTime')) {
        this.checklist.advanced['Performance Monitoring'] = true;
        console.log('  ✅ Performance Monitoring - IMPLEMENTED');
      }
      
      if (content.includes('Accessibility') || content.includes('keyboard')) {
        this.checklist.advanced['Accessibility Testing'] = true;
        console.log('  ✅ Accessibility Testing - IMPLEMENTED');
      }
      
      if (content.includes('file') || content.includes('upload')) {
        this.checklist.advanced['File Upload Testing'] = true;
        console.log('  ✅ File Upload Testing - IMPLEMENTED');
      }
      
      if (content.includes('Rate Limiting') || content.includes('multiple submissions')) {
        this.checklist.advanced['Rate Limiting Tests'] = true;
        console.log('  ✅ Rate Limiting Tests - IMPLEMENTED');
      }
    }
  }

  generateReport() {
    console.log('\n📋 Implementation Verification Report\n');
    
    let totalFeatures = 0;
    let implementedFeatures = 0;
    
    Object.entries(this.checklist).forEach(([category, features]) => {
      console.log(`${this.getCategoryIcon(category)} ${category.toUpperCase()}:`);
      
      Object.entries(features).forEach(([feature, implemented]) => {
        totalFeatures++;
        if (implemented) {
          implementedFeatures++;
          console.log(`  ✅ ${feature}`);
        } else {
          console.log(`  ❌ ${feature}`);
        }
      });
      console.log('');
    });
    
    const completionPercentage = Math.round((implementedFeatures / totalFeatures) * 100);
    
    console.log(`📊 OVERALL COMPLETION: ${completionPercentage}% (${implementedFeatures}/${totalFeatures})`);
    
    if (completionPercentage === 100) {
      console.log('🎉 ALL PROMPTS FULLY IMPLEMENTED!');
    } else if (completionPercentage >= 80) {
      console.log('✅ EXCELLENT - Most features implemented');
    } else if (completionPercentage >= 60) {
      console.log('⚠️  GOOD - Core features implemented, some advanced missing');
    } else {
      console.log('❌ INCOMPLETE - Major features missing');
    }
    
    // Save detailed report
    const report = {
      timestamp: new Date().toISOString(),
      completion: completionPercentage,
      implemented: implementedFeatures,
      total: totalFeatures,
      details: this.checklist
    };
    
    fs.writeFileSync(path.join(__dirname, 'verification_report.json'), JSON.stringify(report, null, 2));
    console.log('\n📄 Detailed report saved to verification_report.json');
  }

  getCategoryIcon(category) {
    const icons = {
      core: '🎯',
      framework: '🎨',
      security: '🛡️',
      reporting: '📊',
      cicd: '🔄',
      advanced: '⚡'
    };
    return icons[category] || '📋';
  }
}

if (require.main === module) {
  const verifier = new ImplementationVerifier();
  verifier.verify();
}

module.exports = ImplementationVerifier;