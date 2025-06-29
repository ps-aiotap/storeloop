@echo off
echo ========================================
echo StoreLoop Deployment and Testing Script
echo ========================================
echo.

:: Set error handling
setlocal enabledelayedexpansion

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

:: Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ and try again
    pause
    exit /b 1
)

echo Step 1: Setting up Python environment...
echo ==========================================

:: Activate virtual environment
if exist "storeloop-venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call storeloop-venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv storeloop-venv
    call storeloop-venv\Scripts\activate.bat
    
    echo Installing Python dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install Python dependencies
        pause
        exit /b 1
    )
)

echo Step 2: Database setup and migrations...
echo ==========================================

:: Check if PostgreSQL is running (optional)
echo Checking database connection...
python manage.py check --database default
if errorlevel 1 (
    echo WARNING: Database connection failed, using SQLite fallback
    echo USE_SQLITE=True > .env.local
)

:: Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Database migration failed
    pause
    exit /b 1
)

:: Create test data
echo Creating test data...
python manage.py shell -c "
from django.contrib.auth.models import User
from stores.models import Store, Product, SellerProfile

# Create admin user if not exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Admin user created')

# Create NGO admin if not exists
if not User.objects.filter(username='ngo_admin').exists():
    user = User.objects.create_user('ngo_admin', 'ngo@example.com', 'password')
    SellerProfile.objects.create(user=user, is_partner_admin=True, language_preference='hi')
    print('NGO admin created')

# Create sample data if needed
if Store.objects.count() < 3:
    exec(open('products/management/commands/seed_sample_data.py').read())
    print('Sample data created')
"

echo Step 3: Starting Django development server...
echo ===============================================

:: Start Django server in background
echo Starting Django server on http://localhost:8000...
start /B python manage.py runserver 127.0.0.1:8000

:: Wait for server to start
echo Waiting for server to start...
timeout /t 10 /nobreak >nul

:: Check if server is running
curl -s http://localhost:8000 >nul 2>&1
if errorlevel 1 (
    echo ERROR: Django server failed to start
    echo Please check the console for errors
    pause
    exit /b 1
)

echo ✓ Django server is running at http://localhost:8000

echo Step 4: Setting up Playwright tests...
echo ======================================

cd tests

:: Install Node.js dependencies
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    npm install
    if errorlevel 1 (
        echo ERROR: Failed to install Node.js dependencies
        cd ..
        pause
        exit /b 1
    )
)

:: Install Playwright browsers
echo Installing Playwright browsers...
npx playwright install
if errorlevel 1 (
    echo ERROR: Failed to install Playwright browsers
    cd ..
    pause
    exit /b 1
)

echo Step 5: Running Playwright tests...
echo ===================================

:: Run authentication tests first
echo Running authentication tests...
npx playwright test authentication.spec.ts --reporter=line
if errorlevel 1 (
    echo WARNING: Authentication tests failed
    set TEST_FAILURES=1
)

:: Run buyer flow tests
echo Running buyer flow tests...
npx playwright test buyer-flows.spec.ts --reporter=line
if errorlevel 1 (
    echo WARNING: Buyer flow tests failed
    set TEST_FAILURES=1
)

:: Run seller onboarding tests
echo Running seller onboarding tests...
npx playwright test seller-onboarding.spec.ts --reporter=line
if errorlevel 1 (
    echo WARNING: Seller onboarding tests failed
    set TEST_FAILURES=1
)

:: Run seller dashboard tests
echo Running seller dashboard tests...
npx playwright test seller-dashboard.spec.ts --reporter=line
if errorlevel 1 (
    echo WARNING: Seller dashboard tests failed
    set TEST_FAILURES=1
)

:: Run product management tests
echo Running product management tests...
npx playwright test product-management.spec.ts --reporter=line
if errorlevel 1 (
    echo WARNING: Product management tests failed
    set TEST_FAILURES=1
)

:: Run NGO admin tests
echo Running NGO admin tests...
npx playwright test ngo-admin.spec.ts --reporter=line
if errorlevel 1 (
    echo WARNING: NGO admin tests failed
    set TEST_FAILURES=1
)

:: Generate HTML report
echo Generating test report...
npx playwright show-report --host=127.0.0.1 --port=9323 >nul 2>&1 &

cd ..

echo Step 6: Deployment Summary...
echo ==============================

echo.
echo ✓ Django server: http://localhost:8000
echo ✓ Test report: http://127.0.0.1:9323
echo ✓ Admin login: admin / admin123
echo ✓ NGO login: ngo_admin / password
echo.

if defined TEST_FAILURES (
    echo ⚠️  Some tests failed - check the detailed report
    echo    Test failures saved to: tests/test-results/
    echo    Screenshots available in failure folders
) else (
    echo ✅ All tests passed successfully!
)

echo.
echo Key URLs to test manually:
echo - Homepage: http://localhost:8000/
echo - Store listing: http://localhost:8000/stores/
echo - Admin login: http://localhost:8000/accounts/login/
echo - Django admin: http://localhost:8000/admin/
echo.

echo Deployment complete! Press any key to open the application...
pause >nul

:: Open browser to homepage
start http://localhost:8000

echo.
echo To stop the server, press Ctrl+C in the Django console
echo To view test results, visit: http://127.0.0.1:9323
echo.
pause