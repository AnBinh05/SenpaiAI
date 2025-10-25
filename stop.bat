@echo off
REM SenpaiAI Stop Script for Windows

echo 🛑 Stopping SenpaiAI services...

REM Stop and remove containers
docker-compose down

REM Optional: Remove volumes (uncomment if you want to reset data)
REM echo 🗑️  Removing volumes...
REM docker-compose down -v

echo ✅ SenpaiAI services stopped!
echo 💡 To start again: start.bat
pause

