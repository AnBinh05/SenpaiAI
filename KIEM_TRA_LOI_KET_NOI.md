# 🔍 HƯỚNG DẪN KIỂM TRA LỖI KẾT NỐI

## ❌ Lỗi gặp phải

```
Lỗi kết nối. Vui lòng kiểm tra backend đang chạy.
```

## 🔍 Các nguyên nhân có thể

### 1. Backend không chạy
**Kiểm tra:**
```bash
# Kiểm tra backend có đang chạy không
curl http://localhost:8000/health
```

**Khắc phục:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Backend chạy sai port
**Kiểm tra:**
- Backend đang chạy trên port nào? (mặc định: 8000)
- Frontend đang kết nối đến port nào?

**Khắc phục:**
- Kiểm tra file `frontend/.env` có `VITE_API_BASE_URL=http://localhost:8000`
- Hoặc kiểm tra `frontend/src/services/api.ts` line 3

### 3. CORS Error
**Kiểm tra:**
- Mở DevTools (F12) → Console tab
- Xem có lỗi CORS không

**Khắc phục:**
- Kiểm tra `backend/app/core/config.py` - `allowed_origins` có chứa frontend URL không
- Frontend thường chạy trên `http://localhost:5173` (Vite) hoặc `http://localhost:3000`

### 4. Database Connection Error
**Kiểm tra:**
```bash
cd backend
python -c "from app.core.database import engine; engine.connect()"
```

**Khắc phục:**
- Đảm bảo PostgreSQL đang chạy
- Kiểm tra `DATABASE_URL` trong `backend/.env`

### 5. Authentication Token hết hạn
**Kiểm tra:**
- Mở DevTools (F12) → Application → Local Storage
- Xem có `access_token` không

**Khắc phục:**
- Đăng xuất và đăng nhập lại
- Hoặc xóa localStorage và refresh

## 🛠️ CÁCH KIỂM TRA TỪNG BƯỚC

### Bước 1: Kiểm tra Backend
```bash
# Terminal 1: Chạy backend
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Test API
curl http://localhost:8000/health
# Kết quả mong đợi: {"status":"healthy","message":"SenpaiAI is running properly"}
```

### Bước 2: Kiểm tra Frontend Config
```bash
# Kiểm tra file frontend/.env
cat frontend/.env
# Hoặc nếu không có, kiểm tra frontend/src/services/api.ts
# Phải có: VITE_API_BASE_URL=http://localhost:8000
```

### Bước 3: Kiểm tra Browser Console
1. Mở trang web
2. Nhấn F12 → Console tab
3. Xem có lỗi gì không:
   - `ERR_CONNECTION_REFUSED` → Backend không chạy
   - `CORS error` → CORS config sai
   - `401 Unauthorized` → Token hết hạn

### Bước 4: Kiểm tra Network Tab
1. F12 → Network tab
2. Refresh trang
3. Tìm request `/chat/history`
4. Xem Status code:
   - `200` → OK
   - `401` → Unauthorized (đăng nhập lại)
   - `500` → Server error (xem Response)
   - `Failed` → Network error (backend không chạy)

## ✅ CHECKLIST KHẮC PHỤC

- [ ] Backend đang chạy trên port 8000
- [ ] Frontend config đúng URL backend
- [ ] CORS đã cấu hình đúng
- [ ] Database đang chạy và kết nối được
- [ ] User đã đăng nhập (có token)
- [ ] Không có firewall chặn port 8000

## 🚀 QUY TRÌNH KHẮC PHỤC NHANH

1. **Kiểm tra backend:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Nếu không response, start backend:**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Kiểm tra frontend config:**
   - File `frontend/.env` hoặc `frontend/src/services/api.ts`
   - Đảm bảo `VITE_API_BASE_URL=http://localhost:8000`

4. **Clear cache và refresh:**
   - Ctrl+Shift+R (hard refresh)
   - Hoặc xóa localStorage và đăng nhập lại

5. **Kiểm tra CORS:**
   - Xem Console có lỗi CORS không
   - Nếu có, thêm frontend URL vào `allowed_origins` trong backend config

## 📝 LƯU Ý

- Backend phải chạy **trước** khi mở frontend
- Port 8000 không được sử dụng bởi ứng dụng khác
- Nếu dùng Docker, đảm bảo ports được map đúng
- Firewall có thể chặn localhost connections




