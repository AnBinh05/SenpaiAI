# 🔗 HƯỚNG DẪN KẾT NỐI FRONTEND VỚI BACKEND

## ✅ Đã Cấu Hình Sẵn

### 1. Backend (FastAPI)
- **Port**: `8000`
- **URL**: `http://localhost:8000`
- **CORS**: Đã cho phép các origin:
  - `http://localhost:3000` (Vite port 3000)
  - `http://127.0.0.1:3000`
  - `http://localhost:5173` (Vite mặc định)
  - `http://127.0.0.1:5173`

### 2. Frontend (React + Vite)
- **Port**: `3000` (theo vite.config.ts)
- **URL**: `http://localhost:3000`
- **API Base URL**: `http://localhost:8000` (từ file `.env`)

### 3. File Cấu Hình
- ✅ `frontend/.env` - Đã tạo với `VITE_API_BASE_URL=http://localhost:8000`
- ✅ `backend/app/core/config.py` - CORS đã cấu hình đúng
- ✅ `frontend/src/services/api.ts` - Đã có axios interceptor cho token

---

## 🚀 CÁCH CHẠY ỨNG DỤNG

### Bước 1: Chạy Backend

```powershell
# Mở terminal 1
cd D:\AIII\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Kiểm tra**: Mở browser vào `http://localhost:8000/docs` - phải thấy Swagger UI

### Bước 2: Chạy Frontend

```powershell
# Mở terminal 2
cd D:\AIII\frontend
npm run dev
```

**Kiểm tra**: Mở browser vào `http://localhost:3000` - phải thấy ứng dụng React

---

## 🔍 KIỂM TRA KẾT NỐI

### 1. Kiểm Tra Backend Hoạt Động

Mở browser vào:
- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Root**: http://localhost:8000/

### 2. Kiểm Tra Frontend Kết Nối Backend

1. Mở **Developer Tools** (F12) trong browser
2. Vào tab **Network**
3. Thử đăng nhập/đăng ký trong frontend
4. Xem có request nào gửi đến `http://localhost:8000` không

### 3. Kiểm Tra CORS

Nếu thấy lỗi CORS trong console:
```
Access to XMLHttpRequest at 'http://localhost:8000/...' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Giải pháp**: Đảm bảo backend đang chạy và CORS đã cấu hình đúng port.

---

## 🐛 XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi 1: "Network Error" hoặc "Failed to fetch"

**Nguyên nhân**: Backend chưa chạy hoặc sai port

**Giải pháp**:
1. Kiểm tra backend có đang chạy không: `http://localhost:8000/health`
2. Kiểm tra file `frontend/.env` có đúng `VITE_API_BASE_URL=http://localhost:8000`
3. Restart frontend sau khi sửa `.env`

### Lỗi 2: CORS Error

**Nguyên nhân**: Backend CORS chưa cho phép origin của frontend

**Giải pháp**:
1. Kiểm tra port frontend đang chạy (3000 hay 5173?)
2. Kiểm tra `backend/app/core/config.py` có port đó trong `allowed_origins`
3. Restart backend sau khi sửa

### Lỗi 3: "401 Unauthorized"

**Nguyên nhân**: Token hết hạn hoặc chưa đăng nhập

**Giải pháp**:
1. Đăng nhập lại để lấy token mới
2. Kiểm tra token có trong `localStorage` không (F12 → Application → Local Storage)

### Lỗi 4: Frontend không load

**Nguyên nhân**: Dependencies chưa cài hoặc port bị chiếm

**Giải pháp**:
```powershell
cd frontend
npm install
npm run dev
```

---

## 📝 CẤU HÌNH CHI TIẾT

### File `frontend/.env`
```env
VITE_API_BASE_URL=http://localhost:8000
```

### File `backend/app/core/config.py`
```python
allowed_origins: List[str] = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
```

### File `frontend/src/services/api.ts`
```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
```

---

## 🧪 TEST KẾT NỐI

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

### Test 2: Đăng Ký User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"test123"}'
```

### Test 3: Đăng Nhập
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

---

## ✅ CHECKLIST KẾT NỐI

- [ ] Backend đang chạy trên port 8000
- [ ] Frontend đang chạy trên port 3000 (hoặc 5173)
- [ ] File `frontend/.env` tồn tại và có `VITE_API_BASE_URL=http://localhost:8000`
- [ ] Backend CORS có port của frontend trong `allowed_origins`
- [ ] Không có lỗi CORS trong browser console
- [ ] Có thể đăng nhập/đăng ký từ frontend
- [ ] Token được lưu vào localStorage sau khi đăng nhập

---

## 🎯 QUY TRÌNH HOẠT ĐỘNG

```
1. User mở frontend (http://localhost:3000)
   ↓
2. Frontend gọi API đến backend (http://localhost:8000)
   ↓
3. Backend kiểm tra CORS → Cho phép (vì localhost:3000 trong allowed_origins)
   ↓
4. Backend xử lý request và trả về response
   ↓
5. Frontend nhận response và hiển thị kết quả
```

---

## 💡 MẸO

1. **Luôn mở Developer Tools** (F12) để xem network requests
2. **Kiểm tra Console** để xem lỗi JavaScript
3. **Kiểm tra Network tab** để xem request/response
4. **Restart cả FE và BE** sau khi sửa cấu hình

---

## 🔄 NẾU VẪN KHÔNG KẾT NỐI ĐƯỢC

1. Kiểm tra firewall có chặn port 8000/3000 không
2. Kiểm tra có process nào đang dùng port 8000/3000 không
3. Thử đổi port frontend trong `vite.config.ts`
4. Thử đổi port backend trong lệnh uvicorn
5. Xem log của backend và frontend để tìm lỗi cụ thể










