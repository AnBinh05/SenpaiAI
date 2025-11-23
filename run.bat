@echo off
REM SenpaiAI Quick Start Script for Windows
echo.
echo ========================================
echo   SenpaiAI - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "backend\.venv" (
    echo ❌ Backend virtual environment not found!
    echo Please run install.bat first to install dependencies.
    pause
    exit /b 1
)

REM Activate backend virtual environment
echo [1/2] Starting Backend...
cd backend
call .venv\Scripts\activate.bat

REM Start backend server
start "SenpaiAI Backend" cmd /k "cd backend && .venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
cd ..

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend (if Node.js is available)
echo [2/2] Starting Frontend...
cd frontend
if exist "node_modules" (
    start "SenpaiAI Frontend" cmd /k "npm run dev"
    echo.
    echo ✅ Frontend starting on http://localhost:5173
) else (
    echo ⚠️  Frontend dependencies not installed. Run install.bat first.
)
cd ..

echo.
echo ========================================
echo   SenpaiAI is starting!
echo ========================================
echo.
echo 📱 Frontend: http://localhost:5173 (or 3000)
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo 💡 Press Ctrl+C in the server windows to stop
echo.
pause







