# LibraryProject - Django Introduction

## Project Overview
This is my first Django project created as part of the ALX Django Learning Lab. The project demonstrates basic Django setup and configuration.

## Setup Instructions

### Prerequisites
- Python 3.x installed
- pip package manager

### Installation Steps

1. **Install Django:**
```bash
   pip install django
```

2. **Create Django Project:**
```bash
   django-admin startproject LibraryProject
```

3. **Navigate to Project:**
```bash
   cd LibraryProject
```

4. **Run Development Server:**
```bash
   python manage.py runserver
```

5. **View Application:**
   - Open browser and go to: `http://127.0.0.1:8000/`
   - You should see the Django welcome page

## Project Structure
```
LibraryProject/
├── LibraryProject/
│   ├── __init__.py
│   ├── settings.py      # Project configuration
│   ├── urls.py          # URL routing
│   ├── asgi.py          # ASGI config
│   └── wsgi.py          # WSGI config
├── manage.py            # Django command-line utility
└── README.md            # This file
```

## Key Files Explained

### `settings.py`
- Contains all project configuration
- Database settings
- Installed apps
- Middleware configuration
- Static files settings

### `urls.py`
- URL declarations for the project
- Acts as a "table of contents" for your Django site
- Maps URLs to views

### `manage.py`
- Command-line utility for Django project
- Used to run server, create apps, migrations, etc.
- Don't modify this file

## Commands Reference
```bash
# Run development server
python manage.py runserver

# Create new app
python manage.py startapp appname

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## Next Steps
- Create Django applications
- Set up models and databases
- Create views and templates
- Configure URLs

## Author
**Edidiong Aquatang**
- GitHub: [@E-d-d-i-e-A](https://github.com/E-d-d-i-e-A)
- ALX Software Engineering Program

## Date
October 29, 2025

---

*This project is part of the ALX Django Learning Lab curriculum.*
