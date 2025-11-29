# Script tìm PostgreSQL và tạo database tự động
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   TỰ ĐỘNG TẠO DATABASE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Tìm psql.exe
Write-Host "Đang tìm PostgreSQL..." -ForegroundColor Yellow
$psqlPath = $null

# Tìm trong các thư mục phổ biến
$searchPaths = @(
    "C:\Program Files\PostgreSQL",
    "C:\Program Files (x86)\PostgreSQL",
    "$env:ProgramFiles\PostgreSQL",
    "$env:ProgramFiles(x86)\PostgreSQL"
)

foreach ($basePath in $searchPaths) {
    if (Test-Path $basePath) {
        $found = Get-ChildItem $basePath -Recurse -Filter "psql.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) {
            $psqlPath = $found.FullName
            Write-Host "✅ Tìm thấy PostgreSQL: $psqlPath" -ForegroundColor Green
            break
        }
    }
}

# Tìm trong PATH
if (-not $psqlPath) {
    $psqlCmd = Get-Command psql -ErrorAction SilentlyContinue
    if ($psqlCmd) {
        $psqlPath = $psqlCmd.Path
        Write-Host "✅ Tìm thấy psql trong PATH: $psqlPath" -ForegroundColor Green
    }
}

if (-not $psqlPath) {
    Write-Host "❌ Không tìm thấy psql.exe" -ForegroundColor Red
    Write-Host ""
    Write-Host "Vui lòng:" -ForegroundColor Yellow
    Write-Host "1. Tìm thủ công: Tìm file psql.exe trong thư mục PostgreSQL" -ForegroundColor White
    Write-Host "2. Hoặc thêm PostgreSQL vào PATH" -ForegroundColor White
    Write-Host ""
    Write-Host "Thường ở: C:\Program Files\PostgreSQL\XX\bin\psql.exe" -ForegroundColor Cyan
    Write-Host "   (XX là version: 13, 14, 15, 16...)" -ForegroundColor Cyan
    exit 1
}

# Kiểm tra service
Write-Host ""
Write-Host "Kiểm tra PostgreSQL service..." -ForegroundColor Yellow
$pgService = Get-Service | Where-Object {$_.Name -like "postgresql*"}
if ($pgService) {
    if ($pgService.Status -ne "Running") {
        Write-Host "Khởi động PostgreSQL..." -ForegroundColor Yellow
        Start-Service $pgService.Name
        Start-Sleep -Seconds 3
    }
    Write-Host "✅ PostgreSQL service đang chạy" -ForegroundColor Green
} else {
    Write-Host "⚠️  Không tìm thấy service, tiếp tục..." -ForegroundColor Yellow
}

# Tạo file SQL
Write-Host ""
Write-Host "Tạo script SQL..." -ForegroundColor Yellow

# File 1: Tạo database và user
$sql1 = @"
-- Tạo database (nếu chưa có)
SELECT 'CREATE DATABASE senpai_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'senpai_db')\gexec

-- Tạo user (nếu chưa có)
DO `$`$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'senpai') THEN
      CREATE USER senpai WITH PASSWORD 'senpai123';
   END IF;
END
`$`$;

-- Cấp quyền database
GRANT ALL PRIVILEGES ON DATABASE senpai_db TO senpai;
"@

$sql1 | Out-File -FilePath "temp_setup1.sql" -Encoding utf8

# File 2: Cấp quyền trong database
$sql2 = @"
GRANT ALL ON SCHEMA public TO senpai;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO senpai;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO senpai;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
"@

$sql2 | Out-File -FilePath "temp_setup2.sql" -Encoding utf8

Write-Host "✅ Đã tạo script SQL" -ForegroundColor Green

# Yêu cầu password
Write-Host ""
Write-Host "⚠️  Cần password của user 'postgres'" -ForegroundColor Yellow
Write-Host "   (Password bạn đã đặt khi cài PostgreSQL)" -ForegroundColor Yellow
Write-Host ""

$securePassword = Read-Host "Nhập password của user 'postgres'" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
$env:PGPASSWORD = $plainPassword

Write-Host ""
Write-Host "Đang tạo database và user..." -ForegroundColor Cyan

# Chạy lệnh 1: Tạo database và user
try {
    Write-Host "Bước 1: Tạo database và user..." -ForegroundColor Yellow
    $output1 = & $psqlPath -U postgres -f temp_setup1.sql 2>&1 | Out-String
    
    if ($LASTEXITCODE -eq 0 -or $output1 -match "CREATE DATABASE" -or $output1 -match "CREATE ROLE" -or $output1 -match "GRANT" -or $output1 -match "already exists") {
        Write-Host "✅ Database và user đã được tạo/cập nhật" -ForegroundColor Green
        
        # Chạy lệnh 2: Cấp quyền trong database
        Write-Host ""
        Write-Host "Bước 2: Cấp quyền trong database..." -ForegroundColor Yellow
        $output2 = & $psqlPath -U postgres -d senpai_db -f temp_setup2.sql 2>&1 | Out-String
        
        if ($LASTEXITCODE -eq 0 -or $output2 -match "GRANT" -or $output2 -match "CREATE EXTENSION") {
            Write-Host "✅ Đã cấp quyền thành công" -ForegroundColor Green
            Write-Host ""
            Write-Host "========================================" -ForegroundColor Green
            Write-Host "   ✅ HOÀN TẤT!" -ForegroundColor Green
            Write-Host "========================================" -ForegroundColor Green
            Write-Host ""
            Write-Host "Thông tin kết nối:" -ForegroundColor Cyan
            Write-Host "  Database: senpai_db" -ForegroundColor White
            Write-Host "  User: senpai" -ForegroundColor White
            Write-Host "  Password: senpai123" -ForegroundColor White
            Write-Host "  Host: localhost" -ForegroundColor White
            Write-Host "  Port: 5432" -ForegroundColor White
            Write-Host ""
            Write-Host "Bước tiếp theo:" -ForegroundColor Cyan
            Write-Host "  alembic upgrade head" -ForegroundColor White
            Write-Host ""
        } else {
            Write-Host "⚠️  Có thể đã thành công, nhưng có cảnh báo:" -ForegroundColor Yellow
            Write-Host $output2 -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ Có lỗi:" -ForegroundColor Red
        Write-Host $output1 -ForegroundColor Red
        Write-Host ""
        Write-Host "Có thể database/user đã tồn tại. Tiếp tục kiểm tra..." -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Lỗi: $_" -ForegroundColor Red
} finally {
    Remove-Item "temp_setup1.sql" -ErrorAction SilentlyContinue
    Remove-Item "temp_setup2.sql" -ErrorAction SilentlyContinue
    $env:PGPASSWORD = $null
}

Write-Host ""


























