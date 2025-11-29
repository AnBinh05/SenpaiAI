# 🚀 HƯỚNG DẪN CHẠY ỨNG DỤNG SENPAIAI

## ⚡ CÁCH CHẠY NHANH NHẤT

### Cách 1: Dùng Script (Dễ nhất) ⭐

**PowerShell:**
```powershell
cd D:\AIII
.\CHAY_UNG_DUNG.ps1
```

**Hoặc CMD:**
```cmd
cd D:\AIII
CHAY_UNG_DUNG.bat
```

### Cách 2: Chạy Thủ Công

```powershell
# Bước 1: Vào thư mục backend
cd D:\AIII\backend

# Bước 2: Kích hoạt virtual environment
.\.venv\Scripts\Activate.ps1

# Bước 3: Chạy server
uvicorn app.main:app --reload
```

## 📋 CHI TIẾT TỪNG BƯỚC

### Bước 1: Mở PowerShell
- Nhấn `Win + X` → Chọn "Windows PowerShell" hoặc "Terminal"

### Bước 2: Di chuyển đến thư mục dự án
```powershell
cd D:\AIII\backend
```

### Bước 3: Kích hoạt Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

**Kết quả:** Bạn sẽ thấy `(.venv)` ở đầu dòng prompt:
```
(.venv) PS D:\AIII\backend>
```

### Bước 4: Chạy Server
```powershell
uvicorn app.main:app --reload
```

**Hoặc với đầy đủ tham số:**
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## ✅ KẾT QUẢ MONG ĐỢI

Khi chạy thành công, bạn sẽ thấy:

```
INFO:     Will watch for changes in these directories: ['D:\\AIII\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 🌐 TRUY CẬP ỨNG DỤNG

Sau khi server chạy, mở trình duyệt và truy cập:

- **🏠 API Root**: http://localhost:8000
- **📚 API Documentation (Swagger)**: http://localhost:8000/docs
- **📖 ReDoc**: http://localhost:8000/redoc
- **❤️ Health Check**: http://localhost:8000/health

## 🛑 DỪNG SERVER

Nhấn `Ctrl + C` trong cửa sổ PowerShell đang chạy server.

## 🔄 CHẠY FRONTEND (Tùy chọn)

Nếu muốn chạy cả frontend, mở terminal mới:

```powershell
# Terminal mới
cd D:\AIII\frontend
npm install  # Nếu chưa cài
npm run dev
```

Frontend sẽ chạy tại: **http://localhost:5173**

## ⚠️ LƯU Ý QUAN TRỌNG

1. ✅ **PostgreSQL phải đang chạy** - Database đã được tạo sẵn
2. ✅ **Virtual environment phải được kích hoạt** - Thấy `(.venv)` ở đầu dòng
3. ✅ **Port 8000 phải trống** - Nếu bị chiếm, đổi port: `--port 8001`

## 🐛 XỬ LÝ LỖI

### Lỗi: "ModuleNotFoundError"
**Nguyên nhân:** Virtual environment chưa được kích hoạt
**Giải pháp:**
```powershell
.\.venv\Scripts\Activate.ps1
```

### Lỗi: "Address already in use"
**Nguyên nhân:** Port 8000 đang được sử dụng
**Giải pháp:** Đổi port
```powershell
uvicorn app.main:app --reload --port 8001
```

### Lỗi: "Could not connect to database"
**Nguyên nhân:** PostgreSQL service chưa chạy
**Giải pháp:**
```powershell
Get-Service postgresql*
Start-Service postgresql-x64-18  # Thay bằng version của bạn
```

## 📝 TÓM TẮT NHANH

```powershell
# Cách nhanh nhất
cd D:\AIII\backend
.\start.ps1

# Hoặc chạy thủ công
cd D:\AIII\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

## 🎯 SAU KHI CHẠY THÀNH CÔNG

1. ✅ Mở trình duyệt: http://localhost:8000/docs
2. ✅ Test API endpoints
3. ✅ Đăng ký user mới
4. ✅ Bắt đầu sử dụng SenpaiAI!

---

**💡 Mẹo:** Giữ cửa sổ PowerShell mở để server tiếp tục chạy. Server sẽ tự động reload khi bạn sửa code (nhờ `--reload`).


























