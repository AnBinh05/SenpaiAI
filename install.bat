@echo off
REM SenpaiAI Installation Script for Windows
echo.
echo ========================================
echo   SenpaiAI Installation Script
echo ========================================
echo.

REM Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)
python --version
echo ✅ Python found

REM Check Node.js
echo.
echo [2/5] Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)
node --version
echo ✅ Node.js found

REM Setup Backend
echo.
echo [3/5] Setting up Backend...
cd backend

REM Create virtual environment if not exists
if not exist ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install dependencies
echo Installing Python dependencies...
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install backend dependencies
    cd ..
    pause
    exit /b 1
)

echo ✅ Backend dependencies installed

REM Create .env file if not exists
if not exist ".env" (
    echo Creating .env file from template...
    copy env.example .env >nul
    echo ⚠️  Please edit backend\.env to configure your settings
)

cd ..

REM Setup Frontend
echo.
echo [4/5] Setting up Frontend...
cd frontend

REM Install dependencies
echo Installing Node.js dependencies...
call npm install

if %errorlevel% neq 0 (
    echo ❌ Failed to install frontend dependencies
    cd ..
    pause
    exit /b 1
)

echo ✅ Frontend dependencies installed

REM Create .env file if not exists
if not exist ".env" (
    echo Creating .env file from template...
    copy env.example .env >nul
)

cd ..

REM Summary
echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo ✅ Backend: Dependencies installed in backend\.venv
echo ✅ Frontend: Dependencies installed in frontend\node_modules
echo.
echo 📝 Next steps:
echo    1. Edit backend\.env if needed
echo    2. Edit frontend\.env if needed
echo    3. Run start.bat to start the application
echo.
echo 💡 To activate backend virtual environment manually:
echo    cd backend
echo    .venv\Scripts\activate
echo.
pause







