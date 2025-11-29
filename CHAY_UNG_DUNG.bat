@echo off
REM Script chạy ứng dụng SenpaiAI
echo.
echo ========================================
echo   CHAY UNG DUNG SENPAIAI
echo ========================================
echo.

cd /d %~dp0\backend

REM Kiểm tra virtual environment
if not exist ".venv" (
    echo ❌ Virtual environment chưa được tạo!
    echo Vui lòng chạy install.bat trước
    pause
    exit /b 1
)

REM Kích hoạt virtual environment
call .venv\Scripts\activate.bat

REM Kiểm tra PostgreSQL
echo Đang kiểm tra PostgreSQL...
timeout /t 1 /nobreak >nul

REM Chạy server
echo.
echo 🚀 Đang khởi động server...
echo.
echo 📱 API: http://localhost:8000
echo 📚 Docs: http://localhost:8000/docs
echo.
echo 💡 Nhấn Ctrl+C để dừng server
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause


























