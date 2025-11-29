@echo off
REM Script tự động tạo database PostgreSQL
echo ========================================
echo   TAO DATABASE POSTGRESQL
echo ========================================
echo.

REM Kiểm tra PostgreSQL
where psql >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Không tìm thấy psql trong PATH
    echo Vui lòng thêm PostgreSQL bin vào PATH hoặc dùng đường dẫn đầy đủ
    echo Thường là: C:\Program Files\PostgreSQL\15\bin\psql.exe
    pause
    exit /b 1
)

echo Bước 1: Kết nối với PostgreSQL...
echo.
echo ⚠️  Bạn sẽ được yêu cầu nhập password của user 'postgres'
echo    (Password bạn đã đặt khi cài PostgreSQL)
echo.

REM Tạo file SQL tạm
echo CREATE DATABASE senpai_db; > temp_create_db.sql
echo CREATE USER senpai WITH PASSWORD 'senpai123'; >> temp_create_db.sql
echo GRANT ALL PRIVILEGES ON DATABASE senpai_db TO senpai; >> temp_create_db.sql
echo \c senpai_db >> temp_create_db.sql
echo GRANT ALL ON SCHEMA public TO senpai; >> temp_create_db.sql
echo ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO senpai; >> temp_create_db.sql
echo ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO senpai; >> temp_create_db.sql

echo Đang chạy script SQL...
psql -U postgres -f temp_create_db.sql

if %errorlevel% equ 0 (
    echo.
    echo ✅ Đã tạo database và user thành công!
    echo.
    del temp_create_db.sql
) else (
    echo.
    echo ❌ Có lỗi xảy ra. Vui lòng chạy thủ công:
    echo.
    echo psql -U postgres
    echo.
    echo Sau đó copy các lệnh từ file create_database.sql
    echo.
)

pause


























