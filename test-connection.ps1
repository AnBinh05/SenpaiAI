# Script kiểm tra kết nối Frontend - Backend
Write-Host "🔍 KIỂM TRA KẾT NỐI FRONTEND - BACKEND" -ForegroundColor Cyan
Write-Host ""

# Kiểm tra Backend
Write-Host "1. Kiểm tra Backend (http://localhost:8000)..." -ForegroundColor Yellow
try {
    $backendResponse = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 5 -UseBasicParsing
    if ($backendResponse.StatusCode -eq 200) {
        Write-Host "   ✅ Backend đang chạy!" -ForegroundColor Green
        Write-Host "   Status: $($backendResponse.StatusCode)" -ForegroundColor Green
    }
} catch {
    Write-Host "   ❌ Backend KHÔNG chạy hoặc không thể kết nối!" -ForegroundColor Red
    Write-Host "   Lỗi: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   💡 Hãy chạy backend trước: cd backend && .\.venv\Scripts\Activate.ps1 && uvicorn app.main:app --reload" -ForegroundColor Yellow
}

Write-Host ""

# Kiểm tra Frontend
Write-Host "2. Kiểm tra Frontend (http://localhost:3000)..." -ForegroundColor Yellow
try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:3000" -Method GET -TimeoutSec 5 -UseBasicParsing
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "   ✅ Frontend đang chạy!" -ForegroundColor Green
        Write-Host "   Status: $($frontendResponse.StatusCode)" -ForegroundColor Green
    }
} catch {
    Write-Host "   ❌ Frontend KHÔNG chạy hoặc không thể kết nối!" -ForegroundColor Red
    Write-Host "   Lỗi: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   💡 Hãy chạy frontend trước: cd frontend && npm run dev" -ForegroundColor Yellow
}

Write-Host ""

# Kiểm tra file .env
Write-Host "3. Kiểm tra cấu hình Frontend..." -ForegroundColor Yellow
$envFile = "frontend\.env"
if (Test-Path $envFile) {
    Write-Host "   ✅ File .env tồn tại" -ForegroundColor Green
    $envContent = Get-Content $envFile
    if ($envContent -match "VITE_API_BASE_URL") {
        Write-Host "   ✅ Có cấu hình VITE_API_BASE_URL" -ForegroundColor Green
        Write-Host "   Nội dung: $envContent" -ForegroundColor Gray
    } else {
        Write-Host "   ⚠️  Thiếu VITE_API_BASE_URL trong .env" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ File .env không tồn tại!" -ForegroundColor Red
    Write-Host "   💡 Tạo file: Copy-Item frontend\env.example frontend\.env" -ForegroundColor Yellow
}

Write-Host ""

# Kiểm tra CORS
Write-Host "4. Kiểm tra CORS configuration..." -ForegroundColor Yellow
$configFile = "backend\app\core\config.py"
if (Test-Path $configFile) {
    $configContent = Get-Content $configFile -Raw
    if ($configContent -match "localhost:3000" -or $configContent -match "localhost:5173") {
        Write-Host "   ✅ CORS đã cấu hình cho frontend ports" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  CORS có thể chưa cấu hình đúng" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ Không tìm thấy file config.py" -ForegroundColor Red
}

Write-Host ""
Write-Host "📋 TÓM TẮT:" -ForegroundColor Cyan
Write-Host "   - Backend: http://localhost:8000/docs (Swagger UI)" -ForegroundColor White
Write-Host "   - Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   - API Base URL: http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "💡 Nếu có lỗi, xem file HUONG_DAN_KET_NOI_FE_BE.md để biết cách sửa" -ForegroundColor Yellow



