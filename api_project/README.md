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
│   ├── urls.py          # Includes api.urls
│   ├── asgi.py
│   └── wsgi.py
└── api/
    ├── __init__.py
    ├── models.py         # Book model
    ├── serializers.py    # BookSerializer
    ├── views.py          # BookList API view
    ├── urls.py           # API URL routing
    ├── admin.py
    ├── apps.py
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

## API Endpoints

### Book API

#### List All Books
**Endpoint:** `GET /api/books/`

**Description:** Retrieves a list of all books in JSON format

**Example Request:**
```bash
curl http://127.0.0.1:8000/api/books/
```

**Example Response:**
```json
[
    {
        "id": 1,
        "title": "1984",
        "author": "George Orwell"
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee"
    }
]
```

## Models

### Book Model
Located in `api/models.py`

**Fields:**
- `id` (Integer, auto-generated): Primary key
- `title` (CharField, max_length=200): Book title
- `author` (CharField, max_length=100): Book author

**Example:**
```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
```

## Serializers

### BookSerializer
Located in `api/serializers.py`

**Purpose:** Converts Book model instances to JSON format

**Fields:** All fields (id, title, author)

**Example:**
```python
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
```

## Views

### BookList (ListAPIView)
Located in `api/views.py`

**Type:** Generic List API View

**Purpose:** Returns list of all books

**HTTP Method:** GET

**URL:** `/api/books/`

**Example:**
```python
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

## URL Configuration

### API URLs (api/urls.py)
```python
urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
]
```

### Main URLs (api_project/urls.py)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

## Testing the API

### Method 1: Using cURL
```bash
# List all books
curl http://127.0.0.1:8000/api/books/
```

### Method 2: Using Browser
Simply visit: `http://127.0.0.1:8000/api/books/`

Django REST Framework provides a browsable API interface.

### Method 3: Using Python requests
```python
import requests

response = requests.get('http://127.0.0.1:8000/api/books/')
print(response.json())
```

### Method 4: Using Postman
1. Open Postman
2. Create new GET request
3. URL: `http://127.0.0.1:8000/api/books/`
4. Click "Send"

## Adding Sample Data

### Using Django Shell
```bash
python manage.py shell
```
```python
from api.models import Book

# Create sample books
Book.objects.create(title="1984", author="George Orwell")
Book.objects.create(title="To Kill a Mockingbird", author="Harper Lee")
Book.objects.create(title="The Great Gatsby", author="F. Scott Fitzgerald")

# Verify
Book.objects.all()
```

### Using Django Admin
1. Run: `python manage.py createsuperuser`
2. Start server: `python manage.py runserver`
3. Visit: `http://127.0.0.1:8000/admin/`
4. Login and add books through the admin interface

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

# Django shell
python manage.py shell
```

## API Response Format

All API responses are in JSON format:
```json
[
    {
        "id": 1,
        "title": "Book Title",
        "author": "Author Name"
    }
]
```

## Error Handling

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 500 Server Error
```json
{
    "detail": "Internal server error."
}
```

## Next Steps

After completing this setup, you can:
1. ✅ List all books (GET /api/books/)
2. 🔄 Create new books (POST endpoint)
3. 🔄 Retrieve single book (GET /api/books/<id>/)
4. 🔄 Update book (PUT/PATCH /api/books/<id>/)
5. 🔄 Delete book (DELETE /api/books/<id>/)

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

## Troubleshooting

### Issue: "No module named 'rest_framework'"
**Solution:** Install Django REST Framework
```bash
pip install djangorestframework
```

### Issue: "Table api_book doesn't exist"
**Solution:** Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Empty list returned
**Solution:** Add some books via admin or shell

### Issue: 404 on /api/books/
**Solution:** Check that api.urls is included in main urls.py

## Author
**Edidiong Aquatang**
- GitHub: [@E-d-d-i-e-A](https://github.com/E-d-d-i-e-A)
- LinkedIn: [linkedin.com/in/edidiong-aquatang-42aba82b7](https://linkedin.com/in/edidiong-aquatang-42aba82b7)
- Email: eaquatang@gmail.com
- Program: ALX Software Engineering - Back-End Track

## License
This project is part of the ALX Software Engineering program.
```
