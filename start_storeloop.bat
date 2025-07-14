@echo off
echo Starting StoreLoop System...

REM Check if AT Identity is running on port 8001
netstat -an | findstr :8001 >nul
if %errorlevel% neq 0 (
    echo Starting AT Identity on port 8001...
    cd /d "%~dp0\..\at_identity_project"
    start "AT Identity" cmd /k "python manage.py runserver 8001"
    timeout /t 3 >nul
) else (
    echo AT Identity already running on port 8001
)

REM Start StoreLoop on port 8000
echo Starting StoreLoop on port 8000...
cd /d "%~dp0"
echo.
echo ========================================
echo   StoreLoop Userless System Ready!
echo ========================================
echo   Login: http://localhost:8000/login/
echo   Credentials: test/test
echo ========================================
echo.
python manage.py runserver 8000