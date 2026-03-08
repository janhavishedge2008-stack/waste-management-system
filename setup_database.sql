-- Waste Management System - Database Setup
-- Run this in PostgreSQL (pgAdmin or psql)

-- Create database
CREATE DATABASE waste_management_db;

-- Create user
CREATE USER waste_admin WITH PASSWORD 'admin123';

-- Configure user settings
ALTER ROLE waste_admin SET client_encoding TO 'utf8';
ALTER ROLE waste_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE waste_admin SET timezone TO 'UTC';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE waste_management_db TO waste_admin;

-- Connect to the database
\c waste_management_db

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO waste_admin;

-- Success message
SELECT 'Database setup complete!' AS status;
