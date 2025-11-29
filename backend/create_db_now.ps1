# Script tạo database với password đã biết
$password = "binh07042005"
$env:PGPASSWORD = $password

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   ĐANG TẠO DATABASE..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Tìm psql
$psql = $null
$paths = @(
    "C:\Program Files\PostgreSQL\16\bin\psql.exe",
    "C:\Program Files\PostgreSQL\15\bin\psql.exe",
    "C:\Program Files\PostgreSQL\14\bin\psql.exe",
    "C:\Program Files\PostgreSQL\13\bin\psql.exe"
)

foreach ($path in $paths) {
    if (Test-Path $path) {
        $psql = $path
        break
    }
}

if (-not $psql) {
    $psqlCmd = Get-Command psql -ErrorAction SilentlyContinue
    if ($psqlCmd) {
        $psql = $psqlCmd.Path
    }
}

if (-not $psql) {
    Write-Host "❌ Không tìm thấy psql.exe" -ForegroundColor Red
    Write-Host "Vui lòng thêm PostgreSQL vào PATH hoặc chỉ định đường dẫn" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Tìm thấy PostgreSQL: $psql" -ForegroundColor Green
Write-Host ""

# Tạo SQL commands
$sqlCommands = @"
-- Tạo database
CREATE DATABASE senpai_db;
"@

$sqlCommands2 = @"
-- Tạo user
CREATE USER senpai WITH PASSWORD 'senpai123';
GRANT ALL PRIVILEGES ON DATABASE senpai_db TO senpai;
"@

$sqlCommands3 = @"
-- Cấp quyền trong database
GRANT ALL ON SCHEMA public TO senpai;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO senpai;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO senpai;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
"@

Write-Host "Bước 1: Tạo database..." -ForegroundColor Yellow
try {
    $result1 = $sqlCommands | & $psql -U postgres 2>&1
    if ($LASTEXITCODE -eq 0 -or $result1 -match "CREATE DATABASE" -or $result1 -match "already exists") {
        Write-Host "✅ Database đã được tạo" -ForegroundColor Green
    } else {
        Write-Host "⚠️  $result1" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Database có thể đã tồn tại" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Bước 2: Tạo user và cấp quyền..." -ForegroundColor Yellow
try {
    $result2 = $sqlCommands2 | & $psql -U postgres 2>&1
    if ($LASTEXITCODE -eq 0 -or $result2 -match "CREATE ROLE" -or $result2 -match "GRANT" -or $result2 -match "already exists") {
        Write-Host "✅ User đã được tạo và cấp quyền" -ForegroundColor Green
    } else {
        Write-Host "⚠️  $result2" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  User có thể đã tồn tại" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Bước 3: Cấp quyền trong database..." -ForegroundColor Yellow
try {
    $result3 = $sqlCommands3 | & $psql -U postgres -d senpai_db 2>&1
    if ($LASTEXITCODE -eq 0 -or $result3 -match "GRANT" -or $result3 -match "CREATE EXTENSION") {
        Write-Host "✅ Đã cấp quyền trong database" -ForegroundColor Green
    } else {
        Write-Host "⚠️  $result3" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Có thể đã cấp quyền rồi" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   ✅ HOÀN TẤT!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Đang kiểm tra kết nối..." -ForegroundColor Cyan

# Test kết nối
$testResult = "SELECT version();" | & $psql -U senpai -d senpai_db -h localhost 2>&1
if ($LASTEXITCODE -eq 0 -or $testResult -match "PostgreSQL") {
    Write-Host "✅ Kết nối thành công!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Thông tin:" -ForegroundColor Cyan
    Write-Host "  Database: senpai_db" -ForegroundColor White
    Write-Host "  User: senpai" -ForegroundColor White
    Write-Host "  Password: senpai123" -ForegroundColor White
    Write-Host ""
    Write-Host "Bước tiếp theo:" -ForegroundColor Cyan
    Write-Host "  alembic upgrade head" -ForegroundColor White
} else {
    Write-Host "⚠️  Cần kiểm tra lại kết nối" -ForegroundColor Yellow
    Write-Host $testResult -ForegroundColor Yellow
}

$env:PGPASSWORD = $null
Write-Host ""

























