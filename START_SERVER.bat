@echo off
echo ================================================================================
echo              WASTE MANAGEMENT SYSTEM - STARTING SERVER
echo ================================================================================
echo.
echo Database: SQLite (db.sqlite3)
echo Admin Login: admin / admin123
echo.
echo Starting server...
echo.

cd /d "%~dp0"
call venv\Scripts\activate
python manage.py runserver

echo.
echo Server stopped.
pause
