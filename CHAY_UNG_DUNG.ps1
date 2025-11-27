# Script chạy ứng dụng SenpaiAI (PowerShell)
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   CHAY UNG DUNG SENPAIAI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "$PSScriptRoot\backend"

# Kiểm tra virtual environment
if (-not (Test-Path ".venv")) {
    Write-Host "❌ Virtual environment chưa được tạo!" -ForegroundColor Red
    Write-Host "Vui lòng chạy install.bat trước" -ForegroundColor Yellow
    exit 1
}

# Kích hoạt virtual environment
& .\.venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "🚀 Đang khởi động server..." -ForegroundColor Green
Write-Host ""
Write-Host "📱 API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "📖 ReDoc: http://localhost:8000/redoc" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Nhấn Ctrl+C để dừng server" -ForegroundColor Yellow
Write-Host ""

# Chạy server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
























