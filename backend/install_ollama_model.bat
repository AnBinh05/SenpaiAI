@echo off
REM Script to install Ollama models for SenpaiAI

echo ========================================
echo Installing Ollama Models for SenpaiAI
echo ========================================
echo.

REM Check if Ollama is installed
where ollama >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Ollama is not installed or not in PATH
    echo.
    echo Please install Ollama from: https://ollama.ai/download
    echo Or add Ollama to your PATH
    pause
    exit /b 1
)

echo Checking Ollama connection...
ollama list >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Ollama is not running
    echo.
    echo Please start Ollama in another terminal:
    echo   ollama serve
    echo.
    pause
    exit /b 1
)

echo Ollama is running!
echo.

REM Install default model
echo Installing default model: gemma:2b
echo This may take a few minutes...
ollama pull gemma:2b
if %ERRORLEVEL% EQU 0 (
    echo [OK] gemma:2b installed successfully
) else (
    echo [ERROR] Failed to install gemma:2b
)

echo.

REM Install embedding model
echo Installing embedding model: nomic-embed-text
echo This may take a few minutes...
ollama pull nomic-embed-text
if %ERRORLEVEL% EQU 0 (
    echo [OK] nomic-embed-text installed successfully
) else (
    echo [ERROR] Failed to install nomic-embed-text
)

echo.
echo ========================================
echo Installation complete!
echo ========================================
echo.
echo Installed models:
ollama list

pause


