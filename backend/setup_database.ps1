# Script hướng dẫn tạo database PostgreSQL
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  HƯỚNG DẪN TẠO DATABASE POSTGRESQL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Bước 1: Kiểm tra PostgreSQL service..." -ForegroundColor Yellow
$pgService = Get-Service | Where-Object {$_.Name -like "postgresql*"}
if ($pgService) {
    Write-Host "✅ Tìm thấy PostgreSQL service: $($pgService.Name)" -ForegroundColor Green
    if ($pgService.Status -ne "Running") {
        Write-Host "⚠️  Service chưa chạy. Đang khởi động..." -ForegroundColor Yellow
        Start-Service $pgService.Name
        Start-Sleep -Seconds 2
    }
    Write-Host "✅ PostgreSQL service đang chạy" -ForegroundColor Green
} else {
    Write-Host "❌ Không tìm thấy PostgreSQL service" -ForegroundColor Red
    Write-Host "   Vui lòng cài đặt PostgreSQL trước" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Bước 2: Tạo database và user..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Chạy các lệnh sau trong psql:" -ForegroundColor Cyan
Write-Host ""
Write-Host "psql -U postgres" -ForegroundColor White
Write-Host ""
Write-Host "Sau đó chạy các lệnh SQL:" -ForegroundColor Cyan
Write-Host ""
$sqlCommands = @"
CREATE DATABASE senpai_db;
CREATE USER senpai WITH PASSWORD 'senpai123';
GRANT ALL PRIVILEGES ON DATABASE senpai_db TO senpai;
\c senpai_db
GRANT ALL ON SCHEMA public TO senpai;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO senpai;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO senpai;
\q
"@

Write-Host $sqlCommands -ForegroundColor White
Write-Host ""

# Tự động tạo nếu có thể
Write-Host "Bước 3: Thử tạo tự động..." -ForegroundColor Yellow
$env:PGPASSWORD = "postgres"  # Thay bằng password postgres của bạn
try {
    $createDb = "CREATE DATABASE senpai_db;" | psql -U postgres -h localhost 2>&1
    if ($LASTEXITCODE -eq 0 -or $createDb -match "already exists") {
        Write-Host "✅ Database senpai_db đã tồn tại hoặc đã tạo" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Không thể tạo tự động. Vui lòng tạo thủ công bằng lệnh trên" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Bước 4: Sau khi tạo xong, chạy:" -ForegroundColor Yellow
Write-Host "  alembic upgrade head" -ForegroundColor White
Write-Host ""
























