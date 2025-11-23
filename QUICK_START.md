# 🚀 Hướng dẫn chạy nhanh SenpaiAI

## ⚡ Cách chạy Backend

### Trong PowerShell:
```powershell
cd backend
.\start.ps1
```

### Trong CMD:
```cmd
cd backend
start.bat
```

### Hoặc chạy trực tiếp:
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📝 Lưu ý quan trọng:

1. **PowerShell**: Phải dùng `.\start.ps1` (có dấu chấm và backslash)
2. **CMD**: Có thể dùng `start.bat` hoặc `.\start.bat`
3. **KHÔNG** chạy `python main.py` vì file main.py nằm trong `app/` folder

## 🌐 Sau khi chạy:

- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Interactive API: http://localhost:8000/redoc

## 🛑 Dừng server:

Nhấn `Ctrl + C` trong cửa sổ terminal đang chạy server





