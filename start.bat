@echo off
REM SenpaiAI Startup Script for Windows

echo 🎌 Starting SenpaiAI - Japanese Learning Assistant...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

REM Check if Ollama is running (optional)
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ollama is running - using free local LLM
) else (
    echo ⚠️  Ollama not detected - will use OpenAI API (requires API key)
)

REM Check if .env files exist
if not exist "backend\.env" (
    echo ⚠️  Backend .env file not found. Creating from template...
    copy backend\env.example backend\.env
    echo 📝 Please edit backend\.env and configure your LLM provider
)

if not exist "frontend\.env" (
    echo ⚠️  Frontend .env file not found. Creating from template...
    copy frontend\env.example frontend\.env
)

REM Start services
echo 🚀 Starting all services with Docker Compose...
docker-compose up -d

REM Wait for services to be ready
echo ⏳ Waiting for services to start...
timeout /t 15 /nobreak >nul

REM Check if services are running
echo 🔍 Checking service status...
docker-compose ps

echo.
echo ✅ SenpaiAI is starting up!
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🤖 Ollama API: http://localhost:11434
echo.
echo 💡 To view logs: docker-compose logs -f
echo 🛑 To stop: docker-compose down
echo.
echo 🎌 Happy learning Japanese with SenpaiAI!
pause
