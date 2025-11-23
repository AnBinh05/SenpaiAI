# Script tự động tạo database - không cần nhập password nhiều lần
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   TỰ ĐỘNG TẠO DATABASE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Tìm psql
$psqlPath = $null
$possiblePaths = @(
    "C:\Program Files\PostgreSQL\16\bin\psql.exe",
    "C:\Program Files\PostgreSQL\15\bin\psql.exe",
    "C:\Program Files\PostgreSQL\14\bin\psql.exe",
    "C:\Program Files\PostgreSQL\13\bin\psql.exe"
)

foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $psqlPath = $path
        $env:Path += ";$(Split-Path $path)"
        Write-Host "✅ Tìm thấy PostgreSQL: $path" -ForegroundColor Green
        break
    }
}

if (-not $psqlPath) {
    $psqlCmd = Get-Command psql -ErrorAction SilentlyContinue
    if ($psqlCmd) {
        $psqlPath = $psqlCmd.Path
        Write-Host "✅ Tìm thấy psql trong PATH: $psqlPath" -ForegroundColor Green
    } else {
        Write-Host "❌ Không tìm thấy PostgreSQL" -ForegroundColor Red
        Write-Host "Vui lòng cài PostgreSQL hoặc thêm vào PATH" -ForegroundColor Yellow
        exit 1
    }
}

# Kiểm tra service
Write-Host ""
Write-Host "Kiểm tra PostgreSQL service..." -ForegroundColor Yellow
$pgService = Get-Service | Where-Object {$_.Name -like "postgresql*"}
if ($pgService) {
    if ($pgService.Status -ne "Running") {
        Write-Host "Khởi động PostgreSQL service..." -ForegroundColor Yellow
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
$sqlContent = @"
-- Tạo database (bỏ qua nếu đã tồn tại)
SELECT 'CREATE DATABASE senpai_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'senpai_db')\gexec

-- Tạo user (bỏ qua nếu đã tồn tại)
DO `$`$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'senpai') THEN
      CREATE USER senpai WITH PASSWORD 'senpai123';
   END IF;
END
`$`$;

-- Cấp quyền
GRANT ALL PRIVILEGES ON DATABASE senpai_db TO senpai;
"@

$sqlContent | Out-File -FilePath "temp_db_setup.sql" -Encoding utf8

# Tạo file SQL cho database mới
$sqlContent2 = @"
GRANT ALL ON SCHEMA public TO senpai;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO senpai;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO senpai;
"@

$sqlContent2 | Out-File -FilePath "temp_db_setup2.sql" -Encoding utf8

Write-Host ""
Write-Host "⚠️  Cần password của user 'postgres' để tạo database" -ForegroundColor Yellow
Write-Host "   (Password bạn đã đặt khi cài PostgreSQL)" -ForegroundColor Yellow
Write-Host ""

$password = Read-Host "Nhập password của user 'postgres'" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
$env:PGPASSWORD = $plainPassword

Write-Host ""
Write-Host "Đang tạo database và user..." -ForegroundColor Cyan

# Chạy lệnh tạo database
try {
    $output1 = & $psqlPath -U postgres -f temp_db_setup.sql 2>&1
    Write-Host $output1
    
    if ($LASTEXITCODE -eq 0 -or $output1 -match "already exists" -or $output1 -match "CREATE DATABASE" -or $output1 -match "CREATE ROLE") {
        Write-Host "✅ Database và user đã được tạo/cập nhật" -ForegroundColor Green
        
        # Cấp quyền trong database
        Write-Host ""
        Write-Host "Đang cấp quyền trong database..." -ForegroundColor Cyan
        $output2 = & $psqlPath -U postgres -d senpai_db -f temp_db_setup2.sql 2>&1
        Write-Host $output2
        
        if ($LASTEXITCODE -eq 0 -or $output2 -match "GRANT") {
            Write-Host ""
            Write-Host "✅ Đã tạo database và user thành công!" -ForegroundColor Green
            Write-Host ""
            Write-Host "Thông tin kết nối:" -ForegroundColor Cyan
            Write-Host "  Database: senpai_db" -ForegroundColor White
            Write-Host "  User: senpai" -ForegroundColor White
            Write-Host "  Password: senpai123" -ForegroundColor White
            Write-Host ""
            Write-Host "Bước tiếp theo:" -ForegroundColor Cyan
            Write-Host "  alembic upgrade head" -ForegroundColor White
        } else {
            Write-Host "⚠️  Có thể đã tạo xong, nhưng có cảnh báo" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ Có lỗi xảy ra" -ForegroundColor Red
        Write-Host $output1 -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Lỗi: $_" -ForegroundColor Red
} finally {
    Remove-Item "temp_db_setup.sql" -ErrorAction SilentlyContinue
    Remove-Item "temp_db_setup2.sql" -ErrorAction SilentlyContinue
    $env:PGPASSWORD = $null
}

Write-Host ""





