# Waste Management System

A full-stack web application for managing waste collection, recycling, and company tie-ups.

## Features

- User registration and authentication
- Waste pickup scheduling
- Company waste material requests
- Admin dashboard for management
- Recycling information and education
- Contact and support system

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Backend**: Django 4.2.7
- **Database**: SQLite (development)

## Quick Start

### 1. Start the Server

```bash
START_SERVER.bat
```

Or manually:

```bash
cd C:\Users\LENOVO\Desktop\new
venv\Scripts\activate
python manage.py runserver
```

### 2. Access the Application

- Homepage: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- Login: admin / admin123

## Project Structure

```
waste_management/
├── core/              # Core app (home, about, contact)
├── users/             # User authentication and profiles
├── companies/         # Company registration and waste requests
├── pickups/           # Waste pickup scheduling
├── templates/         # HTML templates
├── static/            # CSS, JS, images
├── waste_management/  # Project settings
└── manage.py          # Django management script
```

## Available Pages

- Home
- About Us
- Services
- How It Works
- Book Pickup
- Recycling & Sustainability
- Company Tie-Up
- Pricing/Plans
- FAQ
- Contact Us
- User Dashboard
- Company Dashboard
- Admin Dashboard

## Admin Access

- URL: http://localhost:8000/admin
- Username: admin
- Password: admin123

## Database

- Type: SQLite
- File: db.sqlite3
- Location: Project root directory

## Development

### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Collect Static Files

```bash
python manage.py collectstatic
```

## Support

For issues or questions, use the contact form at http://localhost:8000/contact/

## License

All rights reserved.
