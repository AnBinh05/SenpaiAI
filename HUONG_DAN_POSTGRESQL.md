# 🐘 Hướng Dẫn Chạy và Kết Nối PostgreSQL

## 📋 Bước 1: Khởi Động PostgreSQL Service

### Trên Windows:

#### Cách 1: Dùng Services (Khuyến nghị)
1. Nhấn `Win + R` → gõ `services.msc` → Enter
2. Tìm service **"postgresql-x64-XX"** (XX là version)
3. Click chuột phải → **Start** (nếu chưa chạy)

#### Cách 2: Dùng Command Line
```powershell
# Kiểm tra service
Get-Service postgresql*

# Khởi động service
Start-Service postgresql-x64-15  # Thay 15 bằng version của bạn
```

#### Cách 3: Dùng pg_ctl
```powershell
# Tìm đường dẫn PostgreSQL (thường là)
cd "C:\Program Files\PostgreSQL\15\bin"

# Khởi động
.\pg_ctl.exe -D "C:\Program Files\PostgreSQL\15\data" start
```

## 📋 Bước 2: Tạo Database và User

### Cách 1: Dùng psql (Command Line)

```powershell
# Kết nối với PostgreSQL (dùng user postgres mặc định)
psql -U postgres

# Hoặc nếu cần password
psql -U postgres -h localhost
```

Sau khi vào psql, chạy các lệnh sau:

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

-- Thoát
\q
```

### Cách 2: Dùng pgAdmin (GUI)

1. Mở **pgAdmin 4**
2. Kết nối với server PostgreSQL (localhost)
3. Click chuột phải **Databases** → **Create** → **Database**
   - Name: `senpai_db`
   - Owner: `postgres`
4. Click chuột phải **Login/Group Roles** → **Create** → **Login/Group Role**
   - Name: `senpai`
   - Password: `senpai123`
   - Privileges: Check **Can login?**
5. Click chuột phải database `senpai_db` → **Properties** → **Security**
   - Add user `senpai` với quyền **ALL**

## 📋 Bước 3: Kiểm Tra Kết Nối

### Test từ Command Line:
```powershell
psql -h localhost -p 5432 -U senpai -d senpai_db
# Password: senpai123
```

Nếu kết nối thành công, bạn sẽ thấy:
```
senpai_db=#
```

### Test từ Python:
```python
# Tạo file test_db.py
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://senpai:senpai123@localhost:5432/senpai_db"
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("✅ Kết nối thành công!")
        print(result.fetchone()[0])
except Exception as e:
    print(f"❌ Lỗi kết nối: {e}")
```

Chạy:
```powershell
cd D:\AIII\backend
.\.venv\Scripts\Activate.ps1
python test_db.py
```

## 📋 Bước 4: Tạo Bảng (Migration)

Sau khi database đã sẵn sàng, chạy migration:

```powershell
cd D:\AIII\backend
.\.venv\Scripts\Activate.ps1

# Chạy migration để tạo bảng
alembic upgrade head
```

Hoặc bảng sẽ tự động tạo khi chạy server lần đầu (đã cấu hình trong `main.py`)

## 📋 Bước 5: Chạy Ứng Dụng

```powershell
cd D:\AIII\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

## 🔍 Kiểm Tra Database Đã Tạo Bảng Chưa

### Từ psql:
```sql
\c senpai_db
\dt  -- Liệt kê tất cả bảng
```

### Từ Python:
```python
from app.core.database import engine
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()
print("Các bảng đã tạo:", tables)
```

## ⚠️ Troubleshooting

### Lỗi: "could not connect to server"
**Giải pháp:**
- Kiểm tra PostgreSQL service đã chạy chưa
- Kiểm tra port 5432 có bị chặn không
- Kiểm tra firewall

### Lỗi: "password authentication failed"
**Giải pháp:**
- Kiểm tra lại password
- Kiểm tra file `pg_hba.conf` (thường ở `C:\Program Files\PostgreSQL\15\data\`)

### Lỗi: "database does not exist"
**Giải pháp:**
- Tạo database bằng lệnh `CREATE DATABASE senpai_db;`

### Lỗi: "permission denied"
**Giải pháp:**
- Cấp quyền cho user:
```sql
GRANT ALL PRIVILEGES ON DATABASE senpai_db TO senpai;
GRANT ALL ON SCHEMA public TO senpai;
```

## 📝 Tóm Tắt Nhanh

1. ✅ Khởi động PostgreSQL service
2. ✅ Tạo database: `senpai_db`
3. ✅ Tạo user: `senpai` / password: `senpai123`
4. ✅ Cấp quyền cho user
5. ✅ Test kết nối
6. ✅ Chạy migration: `alembic upgrade head`
7. ✅ Chạy ứng dụng: `uvicorn app.main:app --reload`

## 🔗 Thông Tin Kết Nối

```
Host: localhost
Port: 5432
Database: senpai_db
Username: senpai
Password: senpai123
URL: postgresql://senpai:senpai123@localhost:5432/senpai_db
```
























