# 🔧 SỬA LỖI 500 INTERNAL SERVER ERROR

## ✅ ĐÃ SỬA

1. ✅ **Thêm error handling** trong endpoint `/auth/register`
2. ✅ **Thêm field `updated_at`** vào User schema (optional)
3. ✅ **Cải thiện exception handler** để log lỗi chi tiết

## 🔍 KIỂM TRA DATABASE

Database connection và tables đã được kiểm tra và hoạt động tốt:
- ✅ Database connection: OK
- ✅ Table `users`: Tồn tại
- ✅ User model: Hoạt động

## 🚀 CÁCH KIỂM TRA LỖI

### 1. Xem Log Chi Tiết

Khi có lỗi 500, backend sẽ in traceback đầy đủ ra console. Hãy xem terminal chạy backend để thấy lỗi cụ thể.

### 2. Test Database Connection

Chạy script test:
```powershell
cd backend
.\.venv\Scripts\python.exe test_db_connection.py
```

### 3. Test API Trực Tiếp

Dùng Swagger UI hoặc curl:
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"test123"}'
```

## 🐛 CÁC LỖI THƯỜNG GẶP

### Lỗi 1: Database Connection Failed
**Triệu chứng**: `psycopg2.OperationalError`

**Giải pháp**:
1. Kiểm tra PostgreSQL đang chạy
2. Kiểm tra database `senpai_db` đã được tạo
3. Kiểm tra user `senpai` và password `senpai123`

### Lỗi 2: Table Does Not Exist
**Triệu chứng**: `relation "users" does not exist`

**Giải pháp**:
```powershell
cd backend
alembic upgrade head
```

### Lỗi 3: Serialization Error
**Triệu chứng**: Lỗi khi serialize response model

**Giải pháp**: Đã sửa bằng cách thêm `updated_at: Optional[datetime]` vào User schema

## 📝 RESTART BACKEND

Sau khi sửa code, restart backend:

```powershell
# Dừng backend (Ctrl+C)
# Sau đó chạy lại:
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## ✅ KIỂM TRA SAU KHI SỬA

1. **Backend đang chạy**: http://localhost:8000/health
2. **Swagger UI**: http://localhost:8000/docs
3. **Test đăng ký**: POST `/auth/register` với:
   ```json
   {
     "email": "test@example.com",
     "username": "testuser",
     "password": "test123"
   }
   ```

## 💡 NẾU VẪN CÒN LỖI

1. **Xem log backend** - Traceback sẽ hiển thị lỗi cụ thể
2. **Kiểm tra database** - Chạy `test_db_connection.py`
3. **Kiểm tra dependencies** - Đảm bảo đã cài đủ packages
4. **Kiểm tra environment variables** - File `.env` có đúng không

---

**Lưu ý**: Sau khi sửa code, **phải restart backend** để áp dụng thay đổi!


























