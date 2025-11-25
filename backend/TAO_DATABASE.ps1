.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000# Script tự động tạo database PostgreSQL (PowerShell)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   TAO DATABASE POSTGRESQL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kiểm tra psql
$psqlPath = Get-Command psql -ErrorAction SilentlyContinue
if (-not $psqlPath) {
    Write-Host "❌ Không tìm thấy psql trong PATH" -ForegroundColor Red
    Write-Host "Thử tìm trong thư mục PostgreSQL..." -ForegroundColor Yellow
    
    $possiblePaths = @(
        "C:\Program Files\PostgreSQL\15\bin\psql.exe",
        "C:\Program Files\PostgreSQL\14\bin\psql.exe",
        "C:\Program Files\PostgreSQL\13\bin\psql.exe"
    )
    
    $found = $false
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            $env:Path += ";$(Split-Path $path)"
            Write-Host "✅ Tìm thấy PostgreSQL tại: $path" -ForegroundColor Green
            $found = $true
            break
        }
    }
    
    if (-not $found) {
        Write-Host "❌ Không tìm thấy PostgreSQL" -ForegroundColor Red
        Write-Host "Vui lòng cài PostgreSQL hoặc thêm vào PATH" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "Bước 1: Kiểm tra PostgreSQL service..." -ForegroundColor Yellow
$pgService = Get-Service | Where-Object {$_.Name -like "postgresql*"}
if ($pgService) {
    if ($pgService.Status -ne "Running") {
        Write-Host "⚠️  Service chưa chạy. Đang khởi động..." -ForegroundColor Yellow
        Start-Service $pgService.Name
        Start-Sleep -Seconds 3
    }
    Write-Host "✅ PostgreSQL service đang chạy" -ForegroundColor Green
} else {
    Write-Host "⚠️  Không tìm thấy PostgreSQL service" -ForegroundColor Yellow
    Write-Host "   Tiếp tục thử kết nối..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Bước 2: Tạo database và user..." -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  Bạn sẽ được yêu cầu nhập password của user 'postgres'" -ForegroundColor Yellow
Write-Host "   (Password bạn đã đặt khi cài PostgreSQL)" -ForegroundColor Yellow
Write-Host ""

# Tạo file SQL
$sqlContent = @"
CREATE DATABASE senpai_db;
CREATE USER senpai WITH PASSWORD 'senpai123';
GRANT ALL PRIVILEGES ON DATABASE senpai_db TO senpai;
\c senpai_db
GRANT ALL ON SCHEMA public TO senpai;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO senpai;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO senpai;
"@

$sqlContent | Out-File -FilePath "temp_create_db.sql" -Encoding utf8

Write-Host "Đang chạy script SQL..." -ForegroundColor Cyan
Write-Host ""

# Chạy psql
$env:PGPASSWORD = Read-Host "Nhập password của user 'postgres'" -AsSecureString
$plainPassword = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($env:PGPASSWORD)
)
$env:PGPASSWORD = $plainPassword

try {
    psql -U postgres -f temp_create_db.sql
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Đã tạo database và user thành công!" -ForegroundColor Green
        Write-Host ""
        Remove-Item "temp_create_db.sql" -ErrorAction SilentlyContinue
        
        Write-Host "Bước tiếp theo:" -ForegroundColor Cyan
        Write-Host "  alembic upgrade head" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "❌ Có lỗi xảy ra. Vui lòng chạy thủ công:" -ForegroundColor Red
        Write-Host ""
        Write-Host "psql -U postgres" -ForegroundColor White
        Write-Host ""
        Write-Host "Sau đó copy các lệnh từ file create_database.sql" -ForegroundColor Yellow
    }
} catch {
    Write-Host ""
    Write-Host "❌ Lỗi: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Vui lòng chạy thủ công:" -ForegroundColor Yellow
    Write-Host "  psql -U postgres" -ForegroundColor White
    Write-Host "  Sau đó chạy các lệnh SQL từ file create_database.sql" -ForegroundColor Yellow
} finally {
    Remove-Item "temp_create_db.sql" -ErrorAction SilentlyContinue
    $env:PGPASSWORD = $null
}

Write-Host ""












