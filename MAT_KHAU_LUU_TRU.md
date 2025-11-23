# 🔐 Mật Khẩu Được Lưu Trữ Ở Đâu?

## 📍 Vị Trí Lưu Trữ

Mật khẩu được lưu trong **PostgreSQL Database**, cụ thể:

- **Database:** `senpai_db`
- **Bảng:** `users`
- **Cột:** `hashed_password`
- **Host:** `localhost:5432`
- **User:** `senpai`
- **Password:** `senpai123`

## 🔒 Cách Mật Khẩu Được Bảo Vệ

### ⚠️ QUAN TRỌNG: Mật khẩu KHÔNG BAO GIỜ được lưu dạng văn bản gốc!

1. **Khi đăng ký tài khoản:**
   - Người dùng nhập mật khẩu (ví dụ: `mypassword123`)
   - Hệ thống hash mật khẩu bằng **bcrypt** (thuật toán mã hóa một chiều)
   - Chỉ lưu **hash** vào database, KHÔNG lưu mật khẩu gốc

2. **Khi đăng nhập:**
   - Người dùng nhập mật khẩu
   - Hệ thống hash mật khẩu nhập vào
   - So sánh hash mới với hash đã lưu trong database
   - Nếu khớp → đăng nhập thành công

### Ví dụ:

```
Mật khẩu gốc: "mypassword123"
↓ (bcrypt hash)
Hash lưu trong DB: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5"
```

## 📂 Code Xử Lý Mật Khẩu

### 1. File Hash Mật Khẩu
📁 `backend/app/core/auth.py`

```python
def get_password_hash(password: str) -> str:
    """Hash a password."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')
```

### 2. File Đăng Ký
📁 `backend/app/api/auth.py`

```python
# Dòng 45: Hash mật khẩu trước khi lưu
hashed_password = get_password_hash(user.password)

# Dòng 49: Lưu hash vào database
db_user = UserDB(
    email=user.email,
    username=user.username,
    hashed_password=hashed_password,  # ← Lưu hash, không phải mật khẩu gốc
    ...
)
```

### 3. Model Database
📁 `backend/app/models/database.py`

```python
class User(Base):
    __tablename__ = "users"
    
    hashed_password = Column(String, nullable=False)  # ← Cột lưu hash
```

## 🔍 Cách Xem Dữ Liệu Trong Database

### Cách 1: Dùng psql (Command Line)

```powershell
# Kết nối vào PostgreSQL
psql -h localhost -p 5432 -U senpai -d senpai_db
# Password: senpai123

# Xem tất cả users
SELECT id, email, username, hashed_password, created_at FROM users;

# Xem chi tiết một user
SELECT * FROM users WHERE email = 'your-email@example.com';
```

### Cách 2: Dùng Python Script

Chạy script `backend/view_users.py` (sẽ tạo bên dưới)

### Cách 3: Dùng DBeaver / pgAdmin

1. Kết nối với thông tin:
   - Host: `localhost`
   - Port: `5432`
   - Database: `senpai_db`
   - Username: `senpai`
   - Password: `senpai123`

2. Mở bảng `users` và xem cột `hashed_password`

## ⚠️ Lưu Ý Bảo Mật

1. **KHÔNG THỂ khôi phục mật khẩu gốc từ hash**
   - Hash là một chiều, không thể đảo ngược
   - Nếu quên mật khẩu, phải đặt lại mật khẩu mới

2. **Hash luôn khác nhau mỗi lần**
   - Cùng một mật khẩu sẽ tạo hash khác nhau (do salt ngẫu nhiên)
   - Nhưng bcrypt vẫn có thể so sánh và xác thực được

3. **Không chia sẻ hash**
   - Hash vẫn có thể bị dùng để brute force
   - Bảo vệ database như bảo vệ mật khẩu gốc

## 🛠️ Script Xem Users

Tạo file `backend/view_users.py` để xem danh sách users và hash mật khẩu.

