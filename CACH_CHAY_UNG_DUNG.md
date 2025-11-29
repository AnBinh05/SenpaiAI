# 🚀 Hướng Dẫn Chạy Ứng Dụng SenpaiAI

## ⚡ Cách Chạy Nhanh Nhất

### Cách 1: Dùng Script (Khuyến nghị) ⭐

```powershell
cd D:\AIII\backend
.\start.ps1
```

### Cách 2: Chạy Thủ Công

```powershell
cd D:\AIII\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 Các Bước Chi Tiết

### Bước 1: Mở PowerShell
- Nhấn `Win + X` → Chọn "Windows PowerShell" hoặc "Terminal"

### Bước 2: Di chuyển đến thư mục backend
```powershell
cd D:\AIII\backend
```

### Bước 3: Kích hoạt Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

Bạn sẽ thấy `(.venv)` ở đầu dòng prompt.

### Bước 4: Chạy Server
```powershell
uvicorn app.main:app --reload
```

Hoặc với đầy đủ tham số:
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## ✅ Kết Quả Mong Đợi

Khi chạy thành công, bạn sẽ thấy:

```
INFO:     Will watch for changes in these directories: ['D:\\AIII\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 🌐 Truy Cập Ứng Dụng

Sau khi server chạy, mở trình duyệt:

- **API Root**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🛑 Dừng Server

Nhấn `Ctrl + C` trong cửa sổ PowerShell đang chạy server.

## 🔄 Chạy Frontend (Tùy chọn)

Nếu muốn chạy cả frontend:

```powershell
# Mở terminal mới
cd D:\AIII\frontend
npm install  # Nếu chưa cài
npm run dev
```

Frontend sẽ chạy tại: http://localhost:5173

## ⚠️ Lưu Ý

1. **PostgreSQL phải đang chạy** - Database đã được tạo sẵn
2. **Virtual environment phải được kích hoạt** - Thấy `(.venv)` ở đầu dòng
3. **Port 8000 phải trống** - Nếu bị chiếm, đổi port: `--port 8001`

## 🐛 Troubleshooting

### Lỗi: "ModuleNotFoundError"
**Giải pháp:** Đảm bảo virtual environment đã được kích hoạt
```powershell
.\.venv\Scripts\Activate.ps1
```

### Lỗi: "Address already in use"
**Giải pháp:** Đổi port
```powershell
uvicorn app.main:app --reload --port 8001
```

### Lỗi: "Could not connect to database"
**Giải pháp:** Kiểm tra PostgreSQL service đang chạy
```powershell
Get-Service postgresql*
```

## 📝 Tóm Tắt Nhanh

```powershell
# 1. Vào thư mục backend
cd D:\AIII\backend

# 2. Kích hoạt virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Chạy server
uvicorn app.main:app --reload
```

Hoặc đơn giản:
```powershell
cd D:\AIII\backend
.\start.ps1
```

























