-- Script tạo database và user cho SenpaiAI
-- Chạy script này với user postgres (superuser)

-- Tạo database
CREATE DATABASE senpai_db
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Tạo user
CREATE USER senpai WITH PASSWORD 'senpai123';

-- Cấp quyền cho database
GRANT ALL PRIVILEGES ON DATABASE senpai_db TO senpai;

-- Kết nối vào database mới
\c senpai_db

-- Cấp quyền schema public
GRANT ALL ON SCHEMA public TO senpai;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO senpai;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO senpai;

-- Tạo extension nếu cần
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Xong!
-- Bây giờ bạn có thể kết nối với:
-- Database: senpai_db
-- User: senpai
-- Password: senpai123





