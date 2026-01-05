# 📝 Hướng Dẫn Nhập Lệnh SQL

## 🎯 Các Cách Nhập Lệnh SQL

### Cách 1: Dùng Script Tự Động (Dễ nhất) ⭐

```powershell
cd D:\AIII\backend
.\TAO_DATABASE.ps1
```

Script sẽ tự động:
- Tìm PostgreSQL
- Tạo database và user
- Bạn chỉ cần nhập password của user `postgres`

### Cách 2: Dùng Command Line (psql)

#### Bước 1: Mở PowerShell hoặc CMD

#### Bước 2: Kết nối với PostgreSQL
```powershell
psql -U postgres
```

**Lưu ý:** 
- Nếu không tìm thấy `psql`, dùng đường dẫn đầy đủ:
  ```
  "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres
  ```
- Bạn sẽ được yêu cầu nhập **password của user postgres**
  (Password bạn đã đặt khi cài PostgreSQL)

#### Bước 3: Sau khi vào psql, bạn sẽ thấy:
```
postgres=#
```

Đây là **prompt của psql** - nơi bạn nhập lệnh SQL

#### Bước 4: Nhập từng lệnh SQL (copy/paste):

```sql
CREATE DATABASE senpai_db;
```

Nhấn **Enter** → Bạn sẽ thấy `CREATE DATABASE`

Tiếp tục:
```sql
CREATE USER senpai WITH PASSWORD 'senpai123';
```

Nhấn **Enter** → Bạn sẽ thấy `CREATE ROLE`

Tiếp tục:
```sql
GRANT ALL PRIVILEGES ON DATABASE senpai_db TO senpai;
```

Nhấn **Enter** → Bạn sẽ thấy `GRANT`

Tiếp tục:
```sql
\c senpai_db
```

Nhấn **Enter** → Bạn sẽ thấy `You are now connected to database "senpai_db"`

Tiếp tục:
```sql
GRANT ALL ON SCHEMA public TO senpai;
```

Nhấn **Enter**

Tiếp tục:
```sql
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO senpai;
```

Nhấn **Enter**

Tiếp tục:
```sql
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO senpai;
```

Nhấn **Enter**

#### Bước 5: Thoát psql
```sql
\q
```

Nhấn **Enter** → Quay về PowerShell

### Cách 3: Dùng pgAdmin (GUI - Không cần nhập lệnh)

1. Mở **pgAdmin 4** (tìm trong Start Menu)
2. Kết nối với server PostgreSQL (click vào server)
3. Click chuột phải **Databases** → **Create** → **Database**
   - Name: `senpai_db`
   - Click **Save**
4. Click chuột phải **Login/Group Roles** → **Create** → **Login/Group Role**
   - **General tab:**
     - Name: `senpai`
   - **Definition tab:**
     - Password: `senpai123`
   - **Privileges tab:**
     - ✓ Can login?
   - Click **Save**
5. Click chuột phải database `senpai_db` → **Properties** → **Security**
   - Click **+** để thêm
   - Grantee: `senpai`
   - Privileges: Chọn **ALL**
   - Click **Save**

## 📸 Hình Ảnh Minh Họa

### Khi vào psql thành công:
```
C:\Users\YourName> psql -U postgres
Password for user postgres: [nhập password]
psql (15.0)
Type "help" for help.

postgres=# 
```

### Sau khi nhập lệnh:
```
postgres=# CREATE DATABASE senpai_db;
CREATE DATABASE

postgres=# CREATE USER senpai WITH PASSWORD 'senpai123';
CREATE ROLE

postgres=# GRANT ALL PRIVILEGES ON DATABASE senpai_db TO senpai;
GRANT

postgres=# \c senpai_db
You are now connected to database "senpai_db" as user "postgres".

senpai_db=# GRANT ALL ON SCHEMA public TO senpai;
GRANT

senpai_db=# \q
C:\Users\YourName>
```

## ⚡ Cách Nhanh Nhất

**Chạy script tự động:**
```powershell
cd D:\AIII\backend
.\TAO_DATABASE.ps1
```

Script sẽ hỏi password và tự động tạo tất cả!

## ❓ Câu Hỏi Thường Gặp

**Q: Không biết password của user postgres?**
A: Đây là password bạn đã đặt khi cài PostgreSQL. Nếu quên, có thể reset hoặc tạo user mới.

**Q: Lệnh `psql` không tìm thấy?**
A: Thêm PostgreSQL vào PATH hoặc dùng đường dẫn đầy đủ:
```
"C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres
```

**Q: Có thể copy/paste nhiều lệnh cùng lúc không?**
A: Có! Bạn có thể copy tất cả lệnh và paste vào psql, mỗi lệnh sẽ chạy khi nhấn Enter.




























