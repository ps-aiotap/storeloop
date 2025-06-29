@echo off
echo Setting up test environment...

REM Activate virtual environment
call storeloop-venv\Scripts\activate.bat

REM Setup database and test data
echo Setting up database...
python manage.py migrate --run-syncdb
python manage.py setup_test_data

REM Run Playwright tests
echo Running Playwright tests...
cd tests
npx playwright test --reporter=html

echo Tests completed!
pause