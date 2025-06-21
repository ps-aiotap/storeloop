const { spawn, exec } = require('child_process');
const path = require('path');

class ServerManager {
  constructor() {
    this.serverProcess = null;
    this.isRunning = false;
  }

  async checkServerRunning(url = 'http://localhost:8000') {
    try {
      const response = await fetch(url);
      return response.ok;
    } catch {
      return false;
    }
  }

  async startServer() {
    if (await this.checkServerRunning()) {
      console.log('✅ Server already running');
      this.isRunning = true;
      return true;
    }

    console.log('🚀 Starting Django server...');
    
    const projectRoot = path.resolve(__dirname, '../../');
    const isWindows = process.platform === 'win32';
    
    const command = isWindows 
      ? `cd /d "${projectRoot}" && storeloop-venv\\Scripts\\activate && python manage.py runserver`
      : `cd "${projectRoot}" && source storeloop-venv/bin/activate && python manage.py runserver`;

    return new Promise((resolve, reject) => {
      this.serverProcess = exec(command, { cwd: projectRoot });
      
      this.serverProcess.stdout.on('data', (data) => {
        console.log(data.toString());
        if (data.includes('Starting development server')) {
          setTimeout(async () => {
            if (await this.checkServerRunning()) {
              this.isRunning = true;
              resolve(true);
            } else {
              reject(new Error('Server started but not responding'));
            }
          }, 2000);
        }
      });

      this.serverProcess.stderr.on('data', (data) => {
        const error = data.toString();
        console.error(error);
        if (error.includes('ModuleNotFoundError') || error.includes('ImportError')) {
          reject(new Error('Django not installed. Please activate virtual environment and install dependencies.'));
        }
      });

      this.serverProcess.on('error', (error) => {
        reject(error);
      });

      // Timeout after 30 seconds
      setTimeout(() => {
        if (!this.isRunning) {
          reject(new Error('Server startup timeout'));
        }
      }, 30000);
    });
  }

  async stopServer() {
    if (this.serverProcess) {
      this.serverProcess.kill();
      this.serverProcess = null;
      this.isRunning = false;
      console.log('🛑 Server stopped');
    }
  }
}

module.exports = ServerManager;