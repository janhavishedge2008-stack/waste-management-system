@echo off
echo ================================================================================
echo              POSTGRESQL DATABASE SETUP
echo ================================================================================
echo.
echo This script will help you set up PostgreSQL database.
echo.
echo STEP 1: Make sure PostgreSQL is running
echo ----------------------------------------
echo Press Win+R, type "services.msc", find PostgreSQL service and start it.
echo.
pause
echo.

echo STEP 2: Create database and user in pgAdmin4
echo ---------------------------------------------
echo.
echo Open pgAdmin4 and run this SQL:
echo.
echo CREATE USER waste_admin WITH PASSWORD 'admin123';
echo CREATE DATABASE waste_management_db OWNER waste_admin;
echo GRANT ALL PRIVILEGES ON DATABASE waste_management_db TO waste_admin;
echo ALTER DATABASE waste_management_db OWNER TO waste_admin;
echo.
echo Copy the above SQL commands and execute in pgAdmin4 Query Tool.
echo.
pause
echo.

cd /d "%~dp0"
call venv\Scripts\activate

echo STEP 3: Testing PostgreSQL connection
echo --------------------------------------
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waste_management.settings'); import django; django.setup(); from django.db import connection; connection.ensure_connection(); print('✓ Connected to PostgreSQL successfully!')"

if errorlevel 1 (
    echo.
    echo ✗ Connection failed!
    echo.
    echo Please check:
    echo 1. PostgreSQL service is running
    echo 2. Database 'waste_management_db' exists
    echo 3. User 'waste_admin' exists with password 'admin123'
    echo 4. Password in .env file is correct
    echo.
    pause
    exit /b 1
)

echo.
echo STEP 4: Running migrations
echo --------------------------
python manage.py makemigrations
python manage.py migrate

if errorlevel 1 (
    echo.
    echo ✗ Migration failed!
    pause
    exit /b 1
)

echo.
echo STEP 5: Creating superuser
echo --------------------------
echo.
echo Enter admin credentials:
python manage.py createsuperuser

echo.
echo STEP 6: Loading initial data
echo ----------------------------
python setup.py

echo.
echo ================================================================================
echo                         SETUP COMPLETE!
echo ================================================================================
echo.
echo Database: PostgreSQL (waste_management_db)
echo User: waste_admin
echo.
echo To start the server:
echo    python manage.py runserver
echo.
echo Then open: http://localhost:8000
echo Admin: http://localhost:8000/admin
echo.
pause
