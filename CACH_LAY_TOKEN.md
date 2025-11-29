# 🔑 CÁCH LẤY TOKEN ĐỂ NHẬP VÀO SWAGGER UI

## ⚡ CÁCH NHANH NHẤT

### Bước 1: Đăng Nhập
1. Trong Swagger UI (http://localhost:8000/docs)
2. Tìm endpoint: **POST** `/auth/login`
3. Nhấn **"Try it out"**
4. Nhập:
   ```json
   {
     "email": "test@example.com",
     "password": "password123"
   }
   ```
5. Nhấn **"Execute"**

### Bước 2: Copy Token
Bạn sẽ thấy response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Copy toàn bộ chuỗi `access_token`** (chuỗi dài bắt đầu bằng `eyJ...`)

### Bước 3: Nhập Token
1. Nhấn nút **"Authorize"** (🔒) ở đầu trang Swagger
2. Dán token vào trường **"Value:"**
3. Nhấn **"Authorize"** trong modal
4. Nhấn **"Close"**

## ✅ XONG!

Bây giờ bạn có thể test tất cả các API endpoints!

---

## 📝 Nếu Chưa Có Tài Khoản

### Đăng Ký Trước:
1. Tìm endpoint: **POST** `/auth/register`
2. Nhấn **"Try it out"**
3. Nhập:
   ```json
   {
     "email": "test@example.com",
     "username": "testuser",
     "password": "password123"
   }
   ```
4. Nhấn **"Execute"**
5. Sau đó đăng nhập như trên

---

## ⚠️ LƯU Ý

- ✅ **Chỉ cần token**, không cần thêm "Bearer"
- ✅ Token có thời hạn (30 phút)
- ✅ Nếu hết hạn, đăng nhập lại


























