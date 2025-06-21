const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

class SetupChecker {
  async checkAll() {
    console.log('🔍 Checking StoreLoop Test Setup...\n');
    
    const checks = [
      this.checkPython(),
      this.checkDjango(),
      this.checkVirtualEnv(),
      this.checkDatabase(),
      this.checkPlaywright()
    ];
    
    const results = await Promise.allSettled(checks);
    
    console.log('\n📊 Setup Summary:');
    results.forEach((result, index) => {
      const checkNames = ['Python', 'Django', 'Virtual Environment', 'Database', 'Playwright'];
      if (result.status === 'fulfilled') {
        console.log(`✅ ${checkNames[index]}: ${result.value}`);
      } else {
        console.log(`❌ ${checkNames[index]}: ${result.reason}`);
      }
    });
    
    const allPassed = results.every(r => r.status === 'fulfilled');
    
    if (allPassed) {
      console.log('\n🎉 All checks passed! Ready to run tests.');
      console.log('\nNext steps:');
      console.log('1. npm run discover-urls');
      console.log('2. npm run discover');
      console.log('3. npm run generate');
      console.log('4. npm test');
    } else {
      console.log('\n⚠️  Some checks failed. Please fix the issues above.');
    }
  }
  
  checkPython() {
    return new Promise((resolve, reject) => {
      exec('python --version', (error, stdout) => {
        if (error) {
          reject('Python not found or not in PATH');
        } else {
          resolve(stdout.trim());
        }
      });
    });
  }
  
  checkDjango() {
    return new Promise((resolve, reject) => {
      const projectRoot = path.resolve(__dirname, '../../');
      const managePy = path.join(projectRoot, 'manage.py');
      
      if (!fs.existsSync(managePy)) {
        reject('manage.py not found');
        return;
      }
      
      exec('python -c "import django; print(django.get_version())"', 
        { cwd: projectRoot }, 
        (error, stdout) => {
          if (error) {
            reject('Django not installed or virtual environment not activated');
          } else {
            resolve(`Django ${stdout.trim()}`);
          }
        }
      );
    });
  }
  
  checkVirtualEnv() {
    return new Promise((resolve, reject) => {
      const projectRoot = path.resolve(__dirname, '../../');
      const venvPath = path.join(projectRoot, 'storeloop-venv');
      
      if (fs.existsSync(venvPath)) {
        resolve('Virtual environment found');
      } else {
        reject('Virtual environment not found at storeloop-venv/');
      }
    });
  }
  
  checkDatabase() {
    return new Promise((resolve, reject) => {
      const projectRoot = path.resolve(__dirname, '../../');
      const dbPath = path.join(projectRoot, 'db.sqlite3');
      
      if (fs.existsSync(dbPath)) {
        resolve('SQLite database found');
      } else {
        reject('Database not found. Run: python manage.py migrate');
      }
    });
  }
  
  checkPlaywright() {
    return new Promise((resolve, reject) => {
      exec('npx playwright --version', (error, stdout) => {
        if (error) {
          reject('Playwright not installed. Run: npm install && playwright install');
        } else {
          resolve(stdout.trim());
        }
      });
    });
  }
}

if (require.main === module) {
  const checker = new SetupChecker();
  checker.checkAll();
}

module.exports = SetupChecker;