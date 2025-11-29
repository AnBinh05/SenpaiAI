# 🔄 HƯỚNG DẪN CHẠY LẠI BACKEND

## Cách 1: Restart trong cùng terminal (Nếu đang chạy)

1. **Dừng server:**
   - Nhấn `Ctrl + C` trong terminal đang chạy backend
   - Đợi đến khi thấy "Application shutdown complete"

2. **Chạy lại:**
   ```bash
   cd backend
   .\.venv\Scripts\Activate.ps1
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Cách 2: Chạy từ đầu (Terminal mới)

1. **Mở terminal mới** (PowerShell hoặc CMD)

2. **Chạy các lệnh:**
   ```powershell
   cd D:\AIII\backend
   .\.venv\Scripts\Activate.ps1
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Cách 3: Sử dụng script có sẵn

Nếu có file `start.bat` hoặc `start.ps1`:
```bash
cd backend
.\start.ps1
```

## ✅ Kiểm tra backend đã chạy

Sau khi chạy, bạn sẽ thấy:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 🔍 Test backend

Mở browser và truy cập:
- http://localhost:8000/health
- http://localhost:8000/docs (API documentation)

## ⚠️ Lưu ý

- Backend phải chạy **trước** khi mở frontend
- Port 8000 không được sử dụng bởi ứng dụng khác
- Nếu lỗi port đã được sử dụng, đổi port hoặc dừng ứng dụng khác

