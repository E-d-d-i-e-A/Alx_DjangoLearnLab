# API Project - Django REST Framework

## Overview
This is a Django REST Framework project for building APIs. The project includes a Book API with full CRUD operations using ViewSets and Routers.

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
    ├── views.py          # BookList & BookViewSet
    ├── urls.py           # API routing with DefaultRouter
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

### Book API (ListAPIView)

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

---

### Book API with CRUD Operations (ViewSet)

The ViewSet provides full CRUD functionality for managing books.

#### 1. List All Books
**Endpoint:** `GET /api/books_all/`

**Description:** Retrieves a list of all books

**Example Request:**
```bash
curl http://127.0.0.1:8000/api/books_all/
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

---

#### 2. Retrieve a Single Book
**Endpoint:** `GET /api/books_all/<id>/`

**Description:** Retrieves details of a specific book by ID

**Example Request:**
```bash
curl http://127.0.0.1:8000/api/books_all/1/
```

**Example Response:**
```json
{
    "id": 1,
    "title": "1984",
    "author": "George Orwell"
}
```

---

#### 3. Create a New Book
**Endpoint:** `POST /api/books_all/`

**Description:** Creates a new book

**Request Body (JSON):**
```json
{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald"
}
```

**Example Request (cURL):**
```bash
curl -X POST http://127.0.0.1:8000/api/books_all/ \
  -H "Content-Type: application/json" \
  -d '{"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}'
```

**Example Response:**
```json
{
    "id": 3,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald"
}
```

---

#### 4. Update a Book (Full Update)
**Endpoint:** `PUT /api/books_all/<id>/`

**Description:** Updates all fields of an existing book

**Request Body (JSON):**
```json
{
    "title": "1984 (Updated Edition)",
    "author": "George Orwell"
}
```

**Example Request (cURL):**
```bash
curl -X PUT http://127.0.0.1:8000/api/books_all/1/ \
  -H "Content-Type: application/json" \
  -d '{"title": "1984 (Updated Edition)", "author": "George Orwell"}'
```

**Example Response:**
```json
{
    "id": 1,
    "title": "1984 (Updated Edition)",
    "author": "George Orwell"
}
```

---

#### 5. Partial Update a Book
**Endpoint:** `PATCH /api/books_all/<id>/`

**Description:** Updates specific fields of an existing book

**Request Body (JSON):**
```json
{
    "title": "1984 - Revised"
}
```

**Example Request (cURL):**
```bash
curl -X PATCH http://127.0.0.1:8000/api/books_all/1/ \
  -H "Content-Type: application/json" \
  -d '{"title": "1984 - Revised"}'
```

**Example Response:**
```json
{
    "id": 1,
    "title": "1984 - Revised",
    "author": "George Orwell"
}
```

---

#### 6. Delete a Book
**Endpoint:** `DELETE /api/books_all/<id>/`

**Description:** Deletes a specific book

**Example Request (cURL):**
```bash
curl -X DELETE http://127.0.0.1:8000/api/books_all/1/
```

**Example Response:**
```
HTTP 204 No Content
```

---

## API Summary Table

| Operation | HTTP Method | Endpoint | Description |
|-----------|-------------|----------|-------------|
| List | GET | `/api/books/` | List all books (ListAPIView) |
| List | GET | `/api/books_all/` | List all books (ViewSet) |
| Retrieve | GET | `/api/books_all/<id>/` | Get single book |
| Create | POST | `/api/books_all/` | Create new book |
| Update | PUT | `/api/books_all/<id>/` | Full update |
| Partial Update | PATCH | `/api/books_all/<id>/` | Partial update |
| Delete | DELETE | `/api/books_all/<id>/` | Delete book |

---

## Models

### Book Model
Located in `api/models.py`

**Fields:**
- `id` (Integer, auto-generated): Primary key
- `title` (CharField, max_length=200): Book title
- `author` (CharField, max_length=100): Book author

---

## Serializers

### BookSerializer
Located in `api/serializers.py`

**Purpose:** Converts Book model instances to JSON format

**Fields:** All fields (id, title, author)

---

## Views

### BookList (ListAPIView)
**Purpose:** Returns list of all books (read-only)

**URL:** `/api/books/`

**HTTP Method:** GET only

---

### BookViewSet (ModelViewSet)
**Purpose:** Full CRUD operations on books

**URL Prefix:** `/api/books_all/`

**Supported Operations:**
- `list()` - GET /books_all/
- `create()` - POST /books_all/
- `retrieve()` - GET /books_all/<id>/
- `update()` - PUT /books_all/<id>/
- `partial_update()` - PATCH /books_all/<id>/
- `destroy()` - DELETE /books_all/<id>/

---

## Router Configuration

### DefaultRouter
Located in `api/urls.py`
```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')
```

**Automatically generates URLs:**
- `/books_all/` - List and Create
- `/books_all/<id>/` - Retrieve, Update, Delete

---

## Testing the API

### Method 1: Using cURL

#### List All Books
```bash
curl http://127.0.0.1:8000/api/books_all/
```

#### Get Single Book
```bash
curl http://127.0.0.1:8000/api/books_all/1/
```

#### Create New Book
```bash
curl -X POST http://127.0.0.1:8000/api/books_all/ \
  -H "Content-Type: application/json" \
  -d '{"title": "New Book", "author": "New Author"}'
```

#### Update Book
```bash
curl -X PUT http://127.0.0.1:8000/api/books_all/1/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "author": "Updated Author"}'
```

#### Partial Update
```bash
curl -X PATCH http://127.0.0.1:8000/api/books_all/1/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Only Title Changed"}'
```

#### Delete Book
```bash
curl -X DELETE http://127.0.0.1:8000/api/books_all/1/
```

---

### Method 2: Using Browser (DRF Browsable API)

Simply visit these URLs in your browser:
- `http://127.0.0.1:8000/api/books_all/` - Interactive list/create
- `http://127.0.0.1:8000/api/books_all/1/` - Interactive retrieve/update/delete

Django REST Framework provides forms to test POST, PUT, PATCH, DELETE operations!

---

### Method 3: Using Postman

#### Setup:
1. Open Postman
2. Import collection or create requests manually

#### GET Request (List Books):
- Method: GET
- URL: `http://127.0.0.1:8000/api/books_all/`
- Click "Send"

#### POST Request (Create Book):
- Method: POST
- URL: `http://127.0.0.1:8000/api/books_all/`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
```json
{
    "title": "Test Book",
    "author": "Test Author"
}
```
- Click "Send"

#### PUT Request (Update Book):
- Method: PUT
- URL: `http://127.0.0.1:8000/api/books_all/1/`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
```json
{
    "title": "Updated Book",
    "author": "Updated Author"
}
```
- Click "Send"

#### DELETE Request:
- Method: DELETE
- URL: `http://127.0.0.1:8000/api/books_all/1/`
- Click "Send"

---

### Method 4: Using Python requests
```python
import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api/books_all/'

# List all books
response = requests.get(BASE_URL)
print(response.json())

# Create a book
new_book = {'title': 'New Book', 'author': 'New Author'}
response = requests.post(BASE_URL, json=new_book)
print(response.json())

# Get single book
response = requests.get(f'{BASE_URL}1/')
print(response.json())

# Update book
updated_book = {'title': 'Updated', 'author': 'Updated Author'}
response = requests.put(f'{BASE_URL}1/', json=updated_book)
print(response.json())

# Delete book
response = requests.delete(f'{BASE_URL}1/')
print(response.status_code)  # Should be 204
```

---

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
print(Book.objects.all())
```

---

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

# Django shell
python manage.py shell
```

---

## API Response Formats

### Success Responses

#### List/Retrieve (200 OK)
```json
[
    {
        "id": 1,
        "title": "Book Title",
        "author": "Author Name"
    }
]
```

#### Create (201 Created)
```json
{
    "id": 3,
    "title": "New Book",
    "author": "New Author"
}
```

#### Update (200 OK)
```json
{
    "id": 1,
    "title": "Updated Title",
    "author": "Updated Author"
}
```

#### Delete (204 No Content)
```
(Empty response body)
```

---

### Error Responses

#### 400 Bad Request
```json
{
    "title": ["This field is required."],
    "author": ["This field is required."]
}
```

#### 404 Not Found
```json
{
    "detail": "Not found."
}
```

---

## Project Dependencies
```
Django==5.1.3
djangorestframework==3.14.0
```

---

## Author
**Edidiong Aquatang**
- GitHub: [@E-d-d-i-e-A](https://github.com/E-d-d-i-e-A)
- LinkedIn: [linkedin.com/in/edidiong-aquatang-42aba82b7](https://linkedin.com/in/edidiong-aquatang-42aba82b7)
- Email: eaquatang@gmail.com
- Program: ALX Software Engineering - Back-End Track

## License
This project is part of the ALX Software Engineering program.
```
