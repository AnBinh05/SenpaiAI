# 🔗 KẾT NỐI FRONTEND VỚI BACKEND

## ✅ ĐÃ CẤU HÌNH SẴN

### Backend
- **URL**: `http://localhost:8000`
- **CORS**: Đã cho phép `localhost:3000` và `localhost:5173`

### Frontend  
- **URL**: `http://localhost:3000`
- **API URL**: `http://localhost:8000` (từ file `.env`)

---

## 🚀 CÁCH CHẠY

### 1. Chạy Backend
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Chạy Frontend
```powershell
cd frontend
npm run dev
```

---

## ✅ KIỂM TRA

1. **Backend**: Mở http://localhost:8000/docs
2. **Frontend**: Mở http://localhost:3000
3. **Test kết nối**: Chạy `.\test-connection.ps1`

---

## 🔍 NẾU CÓ LỖI

- **CORS Error**: Kiểm tra backend có chạy và CORS đã cấu hình đúng port
- **Network Error**: Kiểm tra backend có đang chạy không
- **401 Unauthorized**: Đăng nhập lại để lấy token mới

Xem chi tiết trong file `HUONG_DAN_KET_NOI_FE_BE.md`
























