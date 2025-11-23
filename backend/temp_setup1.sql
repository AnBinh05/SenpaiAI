-- Tạo database (nếu chưa có)
SELECT 'CREATE DATABASE senpai_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'senpai_db')\gexec

-- Tạo user (nếu chưa có)
DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'senpai') THEN
      CREATE USER senpai WITH PASSWORD 'senpai123';
   END IF;
END
$$;

-- Cấp quyền database
GRANT ALL PRIVILEGES ON DATABASE senpai_db TO senpai;
