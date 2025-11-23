# API Project - Django REST Framework

## Overview
This is a Django REST Framework project for building APIs. The project includes a Book API with CRUD operations.

## Project Setup

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Installation Steps

#### 1. Install Django
```bash
pip install django
```

#### 2. Install Django REST Framework
```bash
pip install djangorestframework
```

#### 3. Project Structure
```
api_project/
├── manage.py
├── api_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── api/
    ├── __init__.py
    ├── models.py
    ├── admin.py
    ├── apps.py
    ├── views.py
    └── tests.py
```

### Database Setup

#### 1. Create Migrations
```bash
python manage.py makemigrations
```

#### 2. Apply Migrations
```bash
python manage.py migrate
```

### Running the Server

#### Start Development Server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

### Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

Then access admin at: `http://127.0.0.1:8000/admin/`

## Models

### Book Model
Located in `api/models.py`

**Fields:**
- `title` (CharField, max_length=200): Book title
- `author` (CharField, max_length=100): Book author

**Example:**
```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
```

## Installed Apps

The following apps are configured in `settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Django REST Framework
    'api',  # API app
]
```

## Testing the Setup

### 1. Check Server is Running
```bash
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### 2. Access Admin Panel
1. Create superuser: `python manage.py createsuperuser`
2. Visit: `http://127.0.0.1:8000/admin/`
3. Login with credentials
4. You should see "Books" under API section

### 3. Verify Migrations
```bash
python manage.py showmigrations
```

Should show:
```
api
 [X] 0001_initial
```

## Next Steps

After completing this setup, you can:
1. Create serializers for the Book model
2. Define API views (ViewSets)
3. Configure URL routing for API endpoints
4. Test API endpoints with tools like Postman or cURL

## Common Commands
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Check for issues
python manage.py check
```

## Project Dependencies
```
Django==5.1.3
djangorestframework==3.14.0
```

To save dependencies:
```bash
pip freeze > requirements.txt
```

To install from requirements:
```bash
pip install -r requirements.txt
```

## Author
**Edidiong Aquatang**
- GitHub: [@E-d-d-i-e-A](https://github.com/E-d-d-i-e-A)
- LinkedIn: [linkedin.com/in/edidiong-aquatang-42aba82b7](https://linkedin.com/in/edidiong-aquatang-42aba82b7)
- Email: eaquatang@gmail.com
- Program: ALX Software Engineering - Back-End Track

## License
This project is part of the ALX Software Engineering program.
```

**Commit message:** `Add comprehensive README for API project setup`

---

## 📱 Step-by-Step File Creation Order:

### **Step 1: Create api app files**

Create these in `api_project/api/` directory:

1. **api/__init__.py** (FILE 3) - Empty file
2. **api/apps.py** (FILE 2)
3. **api/models.py** (FILE 1) ← **IMPORTANT**
4. **api/admin.py** (FILE 4)
5. **api/views.py** (FILE 5)
6. **api/tests.py** (FILE 6)

### **Step 2: Create api_project config files**

Create these in `api_project/api_project/` directory:

7. **api_project/__init__.py** (FILE 8) - Empty file
8. **api_project/settings.py** (FILE 7) ← **CRITICAL**
9. **api_project/urls.py** (FILE 9)
10. **api_project/asgi.py** (FILE 10)
11. **api_project/wsgi.py** (FILE 11)

### **Step 3: Create root files**

12. **manage.py** (FILE 12)
13. **README.md** (FILE 13)

---

## 🎯 Final File Structure:
```
api_project/
├── README.md
├── manage.py
├── db.sqlite3 (created after migrations)
├── api_project/
│   ├── __init__.py
│   ├── settings.py          ← REST framework configured
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── api/
    ├── __init__.py
    ├── models.py             ← Book model
    ├── admin.py              ← Book admin registered
    ├── apps.py
    ├── views.py
    ├── tests.py
    └── migrations/
        └── __init__.py (created automatically)
