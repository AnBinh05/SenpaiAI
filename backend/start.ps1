# Start SenpaiAI Backend Server (PowerShell)
Write-Host "Starting SenpaiAI Backend..." -ForegroundColor Green
Set-Location $PSScriptRoot

# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Start uvicorn server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
























