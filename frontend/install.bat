@echo off
chcp 65001 >nul
echo ========================================
echo SenpaiAI Frontend - Auto Install Script
echo ========================================
echo.

REM Kiểm tra Node.js
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ⚠ Node.js chưa được cài đặt!
    echo.
    echo Có 2 cách để cài đặt Node.js:
    echo.
    echo CÁCH 1: Tải và cài đặt thủ công (Khuyến nghị)
    echo 1. Truy cập: https://nodejs.org/
    echo 2. Tải phiên bản LTS (Long Term Support)
    echo 3. Chạy file .msi đã tải và làm theo hướng dẫn
    echo 4. Khởi động lại Command Prompt sau khi cài đặt
    echo.
    echo CÁCH 2: Sử dụng winget (Windows Package Manager)
    echo Chạy lệnh: winget install OpenJS.NodeJS.LTS
    echo.
    
    REM Thử cài đặt bằng winget
    where winget >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo Đang thử cài đặt Node.js bằng winget...
        winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
        echo.
        echo ⚠ Vui lòng khởi động lại Command Prompt và chạy lại script này!
        pause
        exit /b
    ) else (
        echo Đang mở trang tải Node.js...
        start https://nodejs.org/
        pause
        exit /b
    )
)

REM Kiểm tra npm
where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ⚠ npm không khả dụng. Vui lòng cài đặt lại Node.js.
    pause
    exit /b 1
)

echo ✓ Node.js và npm đã sẵn sàng
echo.

REM Kiểm tra file package.json
if not exist "package.json" (
    echo ✗ Không tìm thấy file package.json!
    echo Vui lòng đảm bảo bạn đang ở đúng thư mục frontend.
    pause
    exit /b 1
)

echo Đang cài đặt dependencies...
echo.

npm install

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✓ Cài đặt thành công!
    echo ========================================
    echo.
    echo Tiếp theo, bạn có thể:
    echo 1. Tạo file .env: copy env.example .env
    echo 2. Chạy ứng dụng: npm run dev
    echo.
) else (
    echo.
    echo ✗ Cài đặt thất bại!
    echo Vui lòng kiểm tra lỗi ở trên và thử lại.
    pause
    exit /b 1
)

pause

