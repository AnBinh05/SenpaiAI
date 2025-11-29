# 🔑 Hướng Dẫn Lấy Token Để Sử Dụng API

## 📋 Tóm Tắt

Bạn cần **đăng ký/đăng nhập** để lấy **access token**, sau đó nhập token đó vào trường "Value" trong modal authorization.

---

## 🚀 Cách 1: Đăng Ký Tài Khoản Mới

### Bước 1: Tìm Endpoint Đăng Ký
Trong Swagger UI (http://localhost:8000/docs), tìm endpoint:
- **POST** `/auth/register`

### Bước 2: Nhấn "Try it out"

### Bước 3: Nhập Thông Tin
```json
{
  "email": "test@example.com",
  "username": "testuser",
  "password": "password123"
}
```

### Bước 4: Nhấn "Execute"
Bạn sẽ nhận được thông tin user (chưa có token).

---

## 🔐 Cách 2: Đăng Nhập Để Lấy Token (Khuyến nghị)

### Bước 1: Tìm Endpoint Đăng Nhập
Trong Swagger UI, tìm endpoint:
- **POST** `/auth/login`

### Bước 2: Nhấn "Try it out"

### Bước 3: Nhập Thông Tin Đăng Nhập
```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

### Bước 4: Nhấn "Execute"

### Bước 5: Copy Token
Bạn sẽ nhận được response như sau:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Copy phần `access_token`** (chuỗi dài bắt đầu bằng `eyJ...`)

---

## ✅ Sử Dụng Token

### Bước 1: Nhấn Nút "Authorize" (🔒) ở đầu trang Swagger

### Bước 2: Trong Modal "Available authorizations"
- Tìm trường **"Value:"**
- **Dán token** bạn đã copy vào đây
- **KHÔNG** cần thêm chữ "Bearer" phía trước, chỉ cần token

### Bước 3: Nhấn "Authorize"

### Bước 4: Nhấn "Close"

---

## 🎯 Ví Dụ Cụ Thể

### 1. Đăng Ký User Mới
```bash
POST http://localhost:8000/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "myuser",
  "password": "mypassword123"
}
```

### 2. Đăng Nhập
```bash
POST http://localhost:8000/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "mypassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzA0MDAwMDAwfQ.abc123...",
  "token_type": "bearer"
}
```

### 3. Copy Token
Copy toàn bộ chuỗi: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzA0MDAwMDAwfQ.abc123...`

### 4. Dán Vào Modal Authorization
- Nhấn nút **"Authorize"** (🔒)
- Dán token vào trường **"Value:"**
- Nhấn **"Authorize"** trong modal

---

## ⚠️ Lưu Ý Quan Trọng

1. ✅ **Chỉ cần token**, không cần thêm "Bearer" phía trước
2. ✅ Token có thời hạn (mặc định 30 phút)
3. ✅ Nếu token hết hạn, đăng nhập lại để lấy token mới
4. ✅ Sau khi authorize, tất cả các API endpoints sẽ tự động dùng token này

---

## 🔄 Quy Trình Đầy Đủ

```
1. Đăng ký user mới (POST /auth/register)
   ↓
2. Đăng nhập (POST /auth/login) → Lấy access_token
   ↓
3. Copy access_token
   ↓
4. Nhấn nút "Authorize" (🔒) ở đầu trang
   ↓
5. Dán token vào trường "Value:"
   ↓
6. Nhấn "Authorize" trong modal
   ↓
7. Đóng modal
   ↓
8. Bây giờ bạn có thể test các API endpoints khác!
```

---

## 🧪 Test Sau Khi Authorize

Sau khi authorize thành công, thử các endpoints:
- ✅ `GET /auth/me` - Xem thông tin user hiện tại
- ✅ `POST /chat/message` - Gửi tin nhắn chat
- ✅ `POST /analysis/grammar` - Phân tích ngữ pháp
- ✅ `GET /library/documents` - Xem tài liệu

Tất cả sẽ hoạt động với token bạn đã nhập!

---

## 💡 Mẹo

- **Lưu token** vào một file text tạm để dùng lại
- Token sẽ tự động được lưu trong browser session
- Nếu gặp lỗi 401 Unauthorized, token có thể đã hết hạn → đăng nhập lại

























