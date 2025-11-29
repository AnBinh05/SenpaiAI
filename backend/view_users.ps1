# Script PowerShell để xem danh sách users trong database
Write-Host "`n🔍 Đang xem danh sách users..." -ForegroundColor Cyan

# Kích hoạt virtual environment nếu có
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "📦 Kích hoạt virtual environment..." -ForegroundColor Yellow
    .\.venv\Scripts\Activate.ps1
}

# Chạy Python script
Write-Host "🚀 Chạy script xem users...`n" -ForegroundColor Green
python view_users.py

Write-Host "`n✅ Hoàn thành!`n" -ForegroundColor Green





















