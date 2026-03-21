# Waste Management System

A comprehensive Django-based web application for managing waste collection, recycling, and company partnerships.

## Features

- User registration and authentication
- Pickup request scheduling
- Company waste material requests
- Blog management with search
- Dynamic statistics dashboard
- Admin panel with analytics
- PostgreSQL database

## Quick Start

### 1. Setup Database

The database is already configured. If you need to recreate it:

```bash
venv\Scripts\python.exe setup_postgres_auto.py
```

### 2. Start Server

```bash
START_SERVER.bat
```

Or:

```bash
RUN_THIS.bat
```

### 3. Access Application

- Website: http://localhost:8000/
- Admin Panel: http://localhost:8000/admin/
- Login: admin / admin123

## Database Configuration

- Database: waste_management_db
- User: waste_admin
- Password: admin123
- Host: localhost
- Port: 5432

## Technologies

- Django 5.0
- PostgreSQL 17
- Bootstrap 5
- Python 3.14

## Project Structure

```
waste_management/
├── core/              # Home, blog, services
├── users/             # User authentication
├── companies/         # Company partnerships
├── pickups/           # Pickup scheduling
├── templates/         # HTML templates
├── static/            # CSS, JS, images
└── waste_management/  # Project settings
```

## Admin Features

- User management (regular & company)
- Pickup requests with statistics
- Company waste requests
- Blog post management
- Contact messages
- Waste types management

## License

MIT License
