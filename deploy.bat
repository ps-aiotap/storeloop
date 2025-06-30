@echo off
echo ========================================
echo StoreLoop 1-Click Deployment Script
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "manage.py" (
    echo ERROR: manage.py not found. Please run this script from the StoreLoop root directory.
    pause
    exit /b 1
)

echo [1/8] Reading configuration and starting Docker containers...
REM Read database settings from .env file
set DB_PASSWORD=postgres
set DB_NAME=storeloop
set DB_USER=postgres
if exist ".env" (
    for /f "tokens=1,2 delims==" %%a in (.env) do (
        if "%%a"=="DB_PASSWORD" set DB_PASSWORD=%%b
        if "%%a"=="DB_NAME" set DB_NAME=%%b
        if "%%a"=="DB_USER" set DB_USER=%%b
    )
)
docker run -d --name storeloop-postgres -e POSTGRES_DB=%DB_NAME% -e POSTGRES_USER=%DB_USER% -e POSTGRES_PASSWORD=%DB_PASSWORD% -p 5434:5432 postgres:latest 2>nul
docker run -d --name storeloop-redis -p 6379:6379 redis:7-alpine 2>nul
echo Docker containers started with DB: %DB_NAME%, User: %DB_USER%

echo.
echo [2/8] Waiting for PostgreSQL to be ready...
timeout /t 10 /nobreak >nul
echo PostgreSQL should be ready.

echo.
echo [3/8] Activating virtual environment...
if exist "storeloop-venv\Scripts\activate.bat" (
    call storeloop-venv\Scripts\activate.bat
) else (
    echo WARNING: Virtual environment not found. Using system Python.
)

echo.
echo [4/8] Installing/updating dependencies...
pip install -r requirements.txt --quiet

echo.
echo [5/8] Setting up database...
python manage.py makemigrations
python manage.py migrate

echo.
echo [6/8] Creating admin user and sample data...
python manage.py reset_admin
python manage.py seed_sample_data --users 2 --stores 3 --products 8

echo.
echo [7/8] Starting Celery worker in background...
start /b celery -A core worker --loglevel=info

echo.
echo [8/8] Starting Django development server...
echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Access your application at:
echo - Main site: http://localhost:8000
echo - Admin: http://localhost:8000/admin
echo - Login: admin / admin123
echo - Database: %DB_NAME% (User: %DB_USER%)
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python manage.py runserver