# Script tự động cài đặt Node.js và dependencies cho SenpaiAI Frontend
# Chạy script này với quyền Administrator

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SenpaiAI Frontend - Auto Install Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kiểm tra Node.js đã được cài đặt chưa
$nodeInstalled = $false
try {
    $nodeVersion = node --version 2>$null
    if ($nodeVersion) {
        Write-Host "✓ Node.js đã được cài đặt: $nodeVersion" -ForegroundColor Green
        $nodeInstalled = $true
    }
} catch {
    $nodeInstalled = $false
}

# Nếu chưa có Node.js, hướng dẫn cài đặt
if (-not $nodeInstalled) {
    Write-Host "⚠ Node.js chưa được cài đặt!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Có 2 cách để cài đặt Node.js:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "CÁCH 1: Tải và cài đặt thủ công (Khuyến nghị)" -ForegroundColor Yellow
    Write-Host "1. Truy cập: https://nodejs.org/" -ForegroundColor White
    Write-Host "2. Tải phiên bản LTS (Long Term Support)" -ForegroundColor White
    Write-Host "3. Chạy file .msi đã tải và làm theo hướng dẫn" -ForegroundColor White
    Write-Host "4. Khởi động lại PowerShell sau khi cài đặt" -ForegroundColor White
    Write-Host ""
    Write-Host "CÁCH 2: Sử dụng Chocolatey (nếu đã cài)" -ForegroundColor Yellow
    Write-Host "Chạy lệnh: choco install nodejs-lts -y" -ForegroundColor White
    Write-Host ""
    Write-Host "CÁCH 3: Sử dụng winget (Windows Package Manager)" -ForegroundColor Yellow
    Write-Host "Chạy lệnh: winget install OpenJS.NodeJS.LTS" -ForegroundColor White
    Write-Host ""
    
    # Thử cài đặt bằng winget nếu có
    $wingetAvailable = $false
    try {
        $wingetVersion = winget --version 2>$null
        if ($wingetVersion) {
            $wingetAvailable = $true
            Write-Host "Đang thử cài đặt Node.js bằng winget..." -ForegroundColor Cyan
            winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
            Write-Host ""
            Write-Host "⚠ Vui lòng khởi động lại PowerShell và chạy lại script này!" -ForegroundColor Yellow
            exit
        }
    } catch {
        Write-Host "winget không khả dụng. Vui lòng cài đặt Node.js thủ công." -ForegroundColor Red
    }
    
    if (-not $wingetAvailable) {
        Write-Host "Nhấn phím bất kỳ để mở trang tải Node.js..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        Start-Process "https://nodejs.org/"
        exit
    }
}

# Kiểm tra npm
try {
    $npmVersion = npm --version 2>$null
    if ($npmVersion) {
        Write-Host "✓ npm đã được cài đặt: $npmVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ npm không khả dụng. Vui lòng cài đặt lại Node.js." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Đang cài đặt dependencies..." -ForegroundColor Cyan
Write-Host ""

# Kiểm tra file package.json
if (-not (Test-Path "package.json")) {
    Write-Host "✗ Không tìm thấy file package.json!" -ForegroundColor Red
    Write-Host "Vui lòng đảm bảo bạn đang ở đúng thư mục frontend." -ForegroundColor Yellow
    exit 1
}

# Cài đặt dependencies
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✓ Cài đặt thành công!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Tiếp theo, bạn có thể:" -ForegroundColor Cyan
    Write-Host "1. Tạo file .env: Copy-Item env.example .env" -ForegroundColor White
    Write-Host "2. Chạy ứng dụng: npm run dev" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "✗ Cài đặt thất bại!" -ForegroundColor Red
    Write-Host "Vui lòng kiểm tra lỗi ở trên và thử lại." -ForegroundColor Yellow
    exit 1
}

