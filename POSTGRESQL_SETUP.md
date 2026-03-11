# PostgreSQL Setup Guide

## Quick Setup (3 Steps)

### Step 1: Create Database in pgAdmin4

1. **Open pgAdmin4**
2. **Connect to PostgreSQL 18** (enter your password)
3. **Right-click on "PostgreSQL 18"** → Select "Query Tool"
4. **Copy and paste this SQL:**

```sql
CREATE USER waste_admin WITH PASSWORD 'admin123';
CREATE DATABASE waste_management_db OWNER waste_admin;
GRANT ALL PRIVILEGES ON DATABASE waste_management_db TO waste_admin;
ALTER DATABASE waste_management_db OWNER TO waste_admin;
```

5. **Click Execute** (▶ button) or press F5
6. **You should see:** "Query returned successfully"

### Step 2: Run Setup Script

```bash
setup_postgresql_db.bat
```

This will:
- Test PostgreSQL connection
- Run migrations
- Create admin user
- Load initial data

### Step 3: Start Server

```bash
START_SERVER.bat
```

Or manually:
```bash
venv\Scripts\activate
python manage.py runserver
```

---

## Manual Setup (If Script Fails)

### 1. Check PostgreSQL Service

**Windows:**
1. Press `Win + R`
2. Type: `services.msc`
3. Find "postgresql-x64-18" (or your version)
4. Right-click → Start

### 2. Create Database Manually

**In pgAdmin4:**
1. Right-click "Databases" → Create → Database
2. Name: `waste_management_db`
3. Owner: `waste_admin` (create user first if needed)
4. Save

**Create User:**
```sql
CREATE USER waste_admin WITH PASSWORD 'admin123';
ALTER USER waste_admin CREATEDB;
```

### 3. Update .env File

The `.env` file should have:
```
DB_NAME=waste_management_db
DB_USER=waste_admin
DB_PASSWORD=admin123
DB_HOST=localhost
DB_PORT=5432
```

### 4. Test Connection

```bash
venv\Scripts\activate
python -c "from django.db import connection; connection.ensure_connection(); print('Connected!')"
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

Enter:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123`

### 7. Load Initial Data

```bash
python setup.py
```

This loads:
- Waste types (Plastic, Paper, Metal, etc.)
- Sample blog posts

---

## Connection Details

**Database Configuration:**
- **Engine:** PostgreSQL
- **Database:** waste_management_db
- **User:** waste_admin
- **Password:** admin123
- **Host:** localhost
- **Port:** 5432

**Admin Access:**
- **URL:** http://localhost:8000/admin/
- **Username:** admin
- **Password:** admin123

---

## Troubleshooting

### Error: "password authentication failed"

**Solution:**
1. Check password in `.env` file
2. Make sure user `waste_admin` exists
3. Try resetting password:
```sql
ALTER USER waste_admin WITH PASSWORD 'admin123';
```

### Error: "database does not exist"

**Solution:**
1. Create database in pgAdmin4
2. Or run:
```sql
CREATE DATABASE waste_management_db OWNER waste_admin;
```

### Error: "could not connect to server"

**Solution:**
1. Start PostgreSQL service (services.msc)
2. Check if PostgreSQL is running on port 5432
3. Check firewall settings

### Error: "role waste_admin does not exist"

**Solution:**
```sql
CREATE USER waste_admin WITH PASSWORD 'admin123';
GRANT ALL PRIVILEGES ON DATABASE waste_management_db TO waste_admin;
```

---

## Switching from SQLite to PostgreSQL

If you were using SQLite before:

1. **Backup SQLite data** (optional):
```bash
python manage.py dumpdata > backup.json
```

2. **Switch to PostgreSQL** (already done in settings.py)

3. **Run migrations:**
```bash
python manage.py migrate
```

4. **Load backup** (optional):
```bash
python manage.py loaddata backup.json
```

5. **Or start fresh:**
```bash
python setup.py
python manage.py createsuperuser
```

---

## Verify Setup

### Check Database Connection
```bash
python manage.py dbshell
```

You should see PostgreSQL prompt:
```
waste_management_db=>
```

Type `\dt` to see tables, `\q` to quit.

### Check Migrations
```bash
python manage.py showmigrations
```

All should have `[X]` marks.

### Check Admin Access
1. Start server: `python manage.py runserver`
2. Go to: http://localhost:8000/admin/
3. Login: admin / admin123

---

## Production Notes

For production deployment:

1. **Change passwords** in `.env`
2. **Use strong SECRET_KEY**
3. **Set DEBUG=False**
4. **Configure ALLOWED_HOSTS**
5. **Use environment variables**
6. **Enable SSL/TLS**
7. **Set up database backups**

---

## Quick Commands

```bash
# Start PostgreSQL service
services.msc

# Test connection
python -c "from django.db import connection; connection.ensure_connection()"

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver

# Database shell
python manage.py dbshell
```

---

## Summary

✅ **Database:** PostgreSQL 18  
✅ **Database Name:** waste_management_db  
✅ **User:** waste_admin  
✅ **Password:** admin123  
✅ **Configuration:** Already set in settings.py  

**Just run:** `setup_postgresql_db.bat` and follow the prompts!
