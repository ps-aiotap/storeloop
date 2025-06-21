const { exec } = require('child_process');
const completeDiscovery = require('./complete_discovery');
const generateCompleteTests = require('./complete_test_generator');

async function runComplete() {
  console.log('🚀 Complete StoreLoop Testing Pipeline\n');
  
  try {
    // Step 1: Discover all forms
    console.log('📋 Step 1: Discovering all forms across application...');
    await completeDiscovery();
    
    // Step 2: Generate comprehensive tests
    console.log('\n🔧 Step 2: Generating comprehensive tests...');
    const testCount = generateCompleteTests();
    
    // Step 3: Run all tests
    console.log(`\n🧪 Step 3: Running ${testCount} generated tests...`);
    await runTests();
    
    console.log('\n✅ Complete pipeline finished!');
    console.log('📊 Check playwright-report/index.html for detailed results');
    
  } catch (error) {
    console.error('\n❌ Pipeline failed:', error.message);
  }
}

function runTests() {
  return new Promise((resolve, reject) => {
    exec('npx playwright test complete_tests.spec.js --reporter=html', (error, stdout, stderr) => {
      if (stdout) console.log(stdout);
      if (stderr) console.log(stderr);
      
      // Don't reject on test failures, just log them
      if (error && !error.message.includes('Test failed')) {
        reject(error);
      } else {
        resolve();
      }
    });
  });
}

if (require.main === module) {
  runComplete();
}

module.exports = runComplete;