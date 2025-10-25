-- Database initialization script for SenpaiAI
-- This script sets up the initial database structure

-- Create database if it doesn't exist
-- (This is handled by the POSTGRES_DB environment variable)

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Set timezone
SET timezone = 'UTC';

-- Create custom types
DO $$ BEGIN
    CREATE TYPE jlpt_level AS ENUM ('N5', 'N4', 'N3', 'N2', 'N1');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE document_type AS ENUM ('grammar', 'vocabulary', 'lesson', 'example', 'culture');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Create indexes for better performance
-- (Tables will be created by Alembic migrations)

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE senpai_db TO senpai;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO senpai;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO senpai;

