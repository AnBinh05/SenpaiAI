# 📊 Thông Tin Kết Nối PostgreSQL

## 🔐 Thông Tin Kết Nối Mặc Định

### Thông Tin Cơ Bản:
```
Host:     localhost (hoặc 127.0.0.1)
Port:     5432
Database: senpai_db
Username: senpai
Password: senpai123
```

### Connection String (URL):
```
postgresql://senpai:senpai123@localhost:5432/senpai_db
```

## 📁 File Cấu Hình

### 1. File Config Python
📁 `backend/app/core/config.py`
```python
database_url: str = "postgresql://senpai:senpai123@localhost:5432/senpai_db"
```

### 2. File Environment Variables
📁 `backend/.env` (tạo từ `backend/env.example`)
```env
DATABASE_URL=postgresql://senpai:senpai123@localhost:5432/senpai_db
```

### 3. Docker Compose Config
📁 `docker-compose.yml`
```yaml
POSTGRES_DB: senpai_db
POSTGRES_USER: senpai
POSTGRES_PASSWORD: senpai123
POSTGRES_PORT: 5432
```

## 🔌 Cách Kết Nối

### 1. Kết Nối Từ Python (SQLAlchemy)
```python
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://senpai:senpai123@localhost:5432/senpai_db"
engine = create_engine(DATABASE_URL)
```

### 2. Kết Nối Từ Command Line (psql)
```bash
psql -h localhost -p 5432 -U senpai -d senpai_db
# Password: senpai123
```

### 3. Kết Nối Từ DBeaver / pgAdmin
- **Host:** localhost
- **Port:** 5432
- **Database:** senpai_db
- **Username:** senpai
- **Password:** senpai123

### 4. Connection String cho các công cụ khác
```
jdbc:postgresql://localhost:5432/senpai_db?user=senpai&password=senpai123
```

## 🐳 Kết Nối Khi Dùng Docker

### Nếu chạy PostgreSQL bằng Docker:
```bash
# Host vẫn là localhost
# Port: 5432 (đã map từ container)
# Database: senpai_db
# User: senpai
# Password: senpai123
```

### Kết nối từ container khác:
```
postgresql://senpai:senpai123@postgres:5432/senpai_db
```
(Lưu ý: dùng tên service `postgres` thay vì `localhost`)

## ⚙️ Thay Đổi Thông Tin Kết Nối

### Cách 1: Sửa file `.env`
📁 `backend/.env`
```env
DATABASE_URL=postgresql://username:password@host:port/database_name
```

### Cách 2: Sửa trong `config.py`
📁 `backend/app/core/config.py`
```python
database_url: str = "postgresql://your_user:your_pass@your_host:5432/your_db"
```

### Cách 3: Dùng Environment Variable
```powershell
$env:DATABASE_URL="postgresql://user:pass@host:5432/db"
```

## 🔍 Kiểm Tra Kết Nối

### Test từ Python:
```python
from app.core.database import engine

# Test connection
with engine.connect() as conn:
    result = conn.execute("SELECT 1")
    print("✅ Database connected!")
```

### Test từ Command Line:
```bash
psql -h localhost -p 5432 -U senpai -d senpai_db -c "SELECT version();"
```

## 📋 Các Bảng Trong Database

Sau khi chạy migration, database sẽ có các bảng:
- `users` - Người dùng
- `chat_history` - Lịch sử chat
- `learning_sessions` - Phiên học tập
- `documents` - Tài liệu học tập
- `grammar_rules` - Quy tắc ngữ pháp
- `vocabulary` - Từ vựng

## ⚠️ Lưu Ý Bảo Mật

**QUAN TRỌNG:** 
- Đổi password trong production!
- Không commit file `.env` lên Git
- Sử dụng biến môi trường cho thông tin nhạy cảm

## 🚀 Khởi Động PostgreSQL

### Cách 1: Dùng Docker
```bash
docker-compose up postgres
```

### Cách 2: Cài đặt Local
1. Tải PostgreSQL từ https://www.postgresql.org/download/
2. Tạo database:
```sql
CREATE DATABASE senpai_db;
CREATE USER senpai WITH PASSWORD 'senpai123';
GRANT ALL PRIVILEGES ON DATABASE senpai_db TO senpai;
```
























