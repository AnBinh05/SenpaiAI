@echo off
REM Start SenpaiAI Backend Server
echo Starting SenpaiAI Backend...
cd /d %~dp0
call .venv\Scripts\activate.bat
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


























