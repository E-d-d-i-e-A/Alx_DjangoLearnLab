Advanced API Project
Django REST Framework project with custom views, permissions, filtering, searching, and ordering.
Features

CRUD operations for Books
Permission-based access control
Filtering by fields
Text search across multiple fields
Ordering/sorting results
Nested serialization for Author-Book relationships

API Endpoints
Public Endpoints (No Authentication)
1. List All Books (with filtering, searching, ordering)

URL: /api/books/
Method: GET
Description: Retrieve books with advanced query capabilities

Filtering Examples:
GET /api/books/?title=Django for Beginners
GET /api/books/?author=1
GET /api/books/?publication_year=2020
GET /api/books/?author=1&publication_year=2020
Searching Examples:
GET /api/books/?search=django
GET /api/books/?search=python
GET /api/books/?search=rowling
Note: Search works across title and author name fields
Ordering Examples:
GET /api/books/?ordering=title
GET /api/books/?ordering=-publication_year
GET /api/books/?ordering=-title
Note: Use - prefix for descending order
Combined Example:
GET /api/books/?search=python&publication_year=2020&ordering=-title
2. Get Book Detail

URL: /api/books/<id>/
Method: GET
Description: Retrieve a single book by ID

Protected Endpoints (Authentication Required)
3. Create Book

URL: /api/books/create/
Method: POST
Permissions: Authenticated users only

4. Update Book

URL: /api/books/<id>/update/
Methods: PUT (full) or PATCH (partial)
Permissions: Authenticated users only

5. Delete Book

URL: /api/books/<id>/delete/
Method: DELETE
Permissions: Authenticated users only

Query Parameters Reference
Filtering
Filter by exact field values:

?title=<book_title>
?author=<author_id>
?publication_year=<year>

Searching
Search across title and author name:

?search=<search_term>

Ordering
Sort results by field:

?ordering=title (ascending)
?ordering=-title (descending)
?ordering=publication_year
?ordering=-publication_year

Implementation Details
Filtering Backend
Uses DjangoFilterBackend for exact field matching on:

title
author (by ID)
publication_year

Search Backend
Uses SearchFilter for text search on:

title field
author__name field (related field)

Ordering Backend
Uses OrderingFilter allowing sorting by:

title
publication_year

Default ordering: title (ascending)
Testing Examples
Using curl
Get all books:
bashcurl http://localhost:8000/api/books/
Filter by publication year:
bashcurl http://localhost:8000/api/books/?publication_year=2020
Search for books:
bashcurl http://localhost:8000/api/books/?search=django
Order by title (descending):
bashcurl http://localhost:8000/api/books/?ordering=-title
Combined query:
bashcurl "http://localhost:8000/api/books/?search=python&ordering=-publication_year"
Using Postman

Base URL: http://localhost:8000/api/books/
Add query parameters in the Params tab:

Key: search, Value: django
Key: ordering, Value: -publication_year
Key: publication_year, Value: 2020



Setup Instructions

Clone the repository
Create virtual environment: python -m venv venv
Activate virtual environment
Install dependencies: pip install -r requirements.txt
Run migrations: python manage.py migrate
Create superuser: python manage.py createsuperuser
Run server: python manage.py runserver
Access API at: http://localhost:8000/api/

Dependencies

Django >= 4.2.0
djangorestframework >= 3.14.0
django-filter >= 23.0
