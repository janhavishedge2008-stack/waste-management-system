@echo off
cls
echo ================================================================================
echo                    WASTE MANAGEMENT SYSTEM
echo ================================================================================
echo.
echo All setup complete! Database ready, admin user created.
echo.
echo Starting server...
echo.
echo Website: http://localhost:8000/
echo Admin Panel: http://localhost:8000/admin/
echo Login: admin / admin123
echo.
echo Press Ctrl+C to stop the server
echo ================================================================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat
python manage.py runserver

pause
