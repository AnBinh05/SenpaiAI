# ⚡ Hướng Dẫn Nhanh Tạo Database

## 🔴 Lỗi Hiện Tại
```
password authentication failed for user "senpai"
```
→ User `senpai` chưa được tạo trong PostgreSQL

## ✅ Giải Pháp

### Cách 1: Dùng psql (Nhanh nhất)

```powershell
# 1. Kết nối với PostgreSQL (dùng user postgres)
psql -U postgres

# 2. Nhập password của user postgres (thường là password bạn đặt khi cài)
# 3. Chạy các lệnh sau:
```

```sql
-- Tạo database
CREATE DATABASE senpai_db;

-- Tạo user
CREATE USER senpai WITH PASSWORD 'senpai123';

-- Cấp quyền
GRANT ALL PRIVILEGES ON DATABASE senpai_db TO senpai;

-- Kết nối vào database mới
\c senpai_db

-- Cấp quyền schema
GRANT ALL ON SCHEMA public TO senpai;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO senpai;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO senpai;

-- Thoát
\q
```

### Cách 2: Dùng pgAdmin (GUI)

1. Mở **pgAdmin 4**
2. Kết nối với server PostgreSQL
3. Click chuột phải **Databases** → **Create** → **Database**
   - Name: `senpai_db`
4. Click chuột phải **Login/Group Roles** → **Create** → **Login/Group Role**
   - Name: `senpai`
   - Password: `senpai123`
   - Privileges: ✓ Can login?
5. Click chuột phải database `senpai_db` → **Properties** → **Security**
   - Add user `senpai` với quyền **ALL**

### Cách 3: Dùng SQL Script

```powershell
# Chạy script SQL
psql -U postgres -f create_database.sql
```

## ✅ Sau Khi Tạo Xong

```powershell
cd D:\AIII\backend
.\.venv\Scripts\Activate.ps1

# Test kết nối
python test_db_connection.py

# Chạy migration
alembic upgrade head

# Chạy ứng dụng
uvicorn app.main:app --reload
```

## 🔍 Kiểm Tra

```powershell
# Test kết nối
psql -h localhost -p 5432 -U senpai -d senpai_db
# Password: senpai123
```

Nếu kết nối thành công → ✅ Database đã sẵn sàng!
























