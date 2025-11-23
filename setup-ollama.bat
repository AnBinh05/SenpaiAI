@echo off
REM Ollama Setup Script for SenpaiAI (Windows)

echo 🎌 Setting up Ollama for SenpaiAI...

REM Check if Ollama is installed
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ollama is not installed. Please install Ollama first:
    echo    Visit: https://ollama.ai/download
    pause
    exit /b 1
)

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo 🚀 Starting Ollama service...
    start /b ollama serve
    timeout /t 5 /nobreak >nul
)

echo 📥 Pulling required models...

REM Pull Gemma 2B model
echo Pulling Gemma 2B model...
ollama pull gemma:2b

REM Pull Gemma 7B model
echo Pulling Gemma 7B model...
ollama pull gemma:7b

REM Pull embedding model
echo Pulling embedding model...
ollama pull nomic-embed-text

REM Pull other useful models
echo Pulling additional models...
ollama pull llama2:7b
ollama pull mistral:7b

echo.
echo ✅ Ollama setup completed!
echo.
echo Available models:
ollama list
echo.
echo 💡 Recommended models for SenpaiAI:
echo    - gemma:2b (fast, lightweight)
echo    - gemma:7b (better quality)
echo    - nomic-embed-text (for embeddings)
echo.
echo 🎌 SenpaiAI is ready to use with Ollama!
pause










