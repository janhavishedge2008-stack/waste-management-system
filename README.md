# EcoWaste Management System

A full-stack waste management platform built with Django and PostgreSQL.

## Stack
- Python 3.14 / Django 5.0
- PostgreSQL 17
- Bootstrap 5, Chart.js, Leaflet.js

## Roles
- **Regular User** — schedule pickups, earn reward points, track status
- **Company** — manage waste requests, view available inventory
- **Worker** — view assigned pickups, update collection status
- **Admin** — full dashboard, analytics, manual assignment, inventory

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver
```

## Access
- Site: http://localhost:8000/
- Admin: http://localhost:8000/admin/ — `admin / admin123`

## Database
PostgreSQL — `waste_management_db` (configured in `.env`)
