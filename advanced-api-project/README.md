Advanced API Project
Django REST Framework project with custom views and permissions.
API Endpoints
Public Endpoints (No Authentication)

GET /api/books/ - List all books
GET /api/books/<id>/ - Get single book

Protected Endpoints (Authentication Required)

POST /api/books/create/ - Create new book
PUT /api/books/<id>/update/ - Update book (full)
PATCH /api/books/<id>/update/ - Update book (partial)
DELETE /api/books/<id>/delete/ - Delete book

Permissions

Read: Everyone can read
Write/Delete: Only authenticated users

Testing
Get all books:
GET http://localhost:8000/api/books/
Create book (needs authentication):
POST http://localhost:8000/api/books/create/
Headers: Authorization: Token YOUR_TOKEN
Body:
{
"title": "New Book",
"publication_year": 2024,
"author": 1
}
Setup

Install: pip install -r requirements.txt
Migrate: python manage.py migrate
Create superuser: python manage.py createsuperuser
Run: python manage.py runserver
