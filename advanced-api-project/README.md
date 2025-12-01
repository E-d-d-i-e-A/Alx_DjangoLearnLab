# Advanced API Project - Django REST Framework
Overview
This Django REST Framework project demonstrates advanced API development concepts including custom serializers with nested relationships, generic views for CRUD operations, permission-based access control, and advanced query capabilities through filtering, searching, and ordering.
Features Implemented
1. Custom Serializers with Nested Relationships

BookSerializer: Handles Book model serialization with custom validation

Custom Validation: publication_year field validates that the year is not in the future
Fields: id, title, publication_year, author


AuthorSerializer: Includes nested BookSerializer for related books

Demonstrates one-to-many relationship serialization
Fields: id, name, books (nested)
Related books are serialized dynamically using related_name='books'



2. Generic Views for CRUD Operations
All views use Django REST Framework's generic views for efficient API development:

BookListView - ListAPIView for retrieving all books
BookDetailView - RetrieveAPIView for retrieving single book by ID
BookCreateView - CreateAPIView for adding new books
BookUpdateView - UpdateAPIView for modifying existing books
BookDeleteView - DestroyAPIView for removing books

3. Permission-Based Access Control
Views are protected using Django REST Framework's permission classes:

IsAuthenticatedOrReadOnly: Applied to ListView and DetailView

Allows GET requests from anyone
Requires authentication for POST, PUT, PATCH, DELETE


IsAuthenticated: Applied to CreateView, UpdateView, DeleteView

Requires authentication for all operations
Unauthenticated users receive 401 Unauthorized



4. Advanced Query Capabilities
Filtering

Backend: DjangoFilterBackend
Filterable Fields: title, author, publication_year
Usage: Filter books by exact field values
Examples:

/api/books/?title=Django for Beginners
/api/books/?author=1
/api/books/?publication_year=2020



Searching

Backend: SearchFilter
Searchable Fields: title, author__name
Usage: Text search across multiple fields with case-insensitive partial matching
Examples:

/api/books/?search=django
/api/books/?search=python
/api/books/?search=rowling



Ordering

Backend: OrderingFilter
Orderable Fields: title, publication_year
Default Ordering: title (ascending)
Usage: Sort results by specified fields, use - prefix for descending
Examples:

/api/books/?ordering=title
/api/books/?ordering=-publication_year



API Endpoints
Public Endpoints (No Authentication Required)
List All Books

URL: /api/books/
Method: GET
Permissions: Read-only for all users
Description: Retrieve list of all books with filtering, searching, and ordering capabilities

Query Parameters:

Filtering: ?title=<value>, ?author=<id>, ?publication_year=<year>
Searching: ?search=<term>
Ordering: ?ordering=<field> or ?ordering=-<field> for descending

Examples:
/api/books/
/api/books/?author=1
/api/books/?publication_year=2020
/api/books/?search=django
/api/books/?ordering=-publication_year
/api/books/?search=python&publication_year=2020&ordering=title
Get Book Detail

URL: /api/books/<id>/
Method: GET
Permissions: Read-only for all users
Description: Retrieve a single book by ID

Protected Endpoints (Authentication Required)
Create Book

URL: /api/books/create/
Method: POST
Permissions: Authenticated users only
Request Body:

json{
    "title": "Book Title",
    "publication_year": 2025,
    "author": 1
}
Update Book

URL: /api/books/<id>/update/
Methods: PUT (full update), PATCH (partial update)
Permissions: Authenticated users only
Request Body (PUT - all fields required):

json{
    "title": "Updated Title",
    "publication_year": 2025,
    "author": 1
}

Request Body (PATCH - partial update):

json{
    "title": "Updated Title Only"
}
Delete Book

URL: /api/books/<id>/delete/
Method: DELETE
Permissions: Authenticated users only
Response: 204 No Content on successful deletion

Models
Author

name (CharField): Author's full name
Relationship: One-to-many with Book model

Book

title (CharField): Book title
publication_year (IntegerField): Year published (validated to not be in future)
author (ForeignKey): Reference to Author model
Relationship: Many-to-one with Author model
Related Name: books for reverse lookup from Author to Books

Setup Instructions
1. Clone Repository
bashgit clone https://github.com/E-d-d-i-e-A/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/advanced-api-project
2. Create Virtual Environment
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bashpip install -r requirements.txt
4. Run Migrations
bashpython manage.py makemigrations
python manage.py migrate
5. Create Superuser
bashpython manage.py createsuperuser
6. Run Development Server
bashpython manage.py runserver
7. Access the API

API Endpoints: http://localhost:8000/api/
Admin Interface: http://localhost:8000/admin/

Testing the API
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
Create book (requires authentication):
bashcurl -X POST http://localhost:8000/api/books/create/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Book",
    "publication_year": 2025,
    "author": 1
  }'
```

### Using Postman

#### Step 1: Set Base URL
`http://localhost:8000/api/`

#### Step 2: For Public Endpoints
- No authentication needed
- Add query parameters in **Params** tab:
  - Key: `search`, Value: `django`
  - Key: `ordering`, Value: `-publication_year`
  - Key: `publication_year`, Value: `2020`

#### Step 3: For Protected Endpoints
1. Set HTTP method (POST, PUT, PATCH, DELETE)
2. Add header: `Authorization: Token YOUR_TOKEN_HERE`
3. Add request body in **Body** tab (select raw/JSON)

## Project Structure
```
advanced-api-project/
├── manage.py
├── requirements.txt
├── README.md                     # This file
├── db.sqlite3
├── advanced_api_project/
│   ├── __init__.py
│   ├── settings.py              # REST_FRAMEWORK configured
│   ├── urls.py                  # Main URL routing
│   ├── wsgi.py
│   └── asgi.py
└── api/
    ├── __init__.py
    ├── models.py                 # Author and Book models
    ├── serializers.py            # Custom serializers with validation
    ├── views.py                  # Generic views with filters
    ├── urls.py                   # API endpoint routing
    ├── admin.py                  # Admin configuration
    └── apps.py
Configuration Details
Settings Configuration

INSTALLED_APPS:

rest_framework - Django REST Framework
django_filters - Filtering backend
api - Application


REST_FRAMEWORK: Default filter backends configuration

DjangoFilterBackend - Field filtering
SearchFilter - Text search
OrderingFilter - Result ordering



View Configuration

filter_backends: List of filter backend classes
filterset_fields: Fields available for filtering
search_fields: Fields included in text search
ordering_fields: Fields available for ordering
ordering: Default ordering applied to queryset

Dependencies

Django: >= 4.2.0, < 5.0.0
djangorestframework: >= 3.14.0, < 4.0.0
django-filter: >= 23.0

Security Features

Permission-Based Access Control: Fine-grained control over API operations
Authentication Required: Write operations protected by authentication
Read-Only Public Access: Safe public access to list and detail views
Custom Validation: Publication year validation prevents future dates
Exception Handling: Proper HTTP status codes for unauthorized access

Troubleshooting
Permission Denied (403 Forbidden)
Causes:

User is not authenticated
User doesn't have required permissions

Solution:

Ensure you're sending authentication token in headers
Verify user account is active
Check user has proper permissions

Filtering Not Working
Causes:

django-filter not installed
Not added to INSTALLED_APPS
Filter backend not configured

Solution:
bashpip install django-filter
Add to settings.py:
pythonINSTALLED_APPS = [
    ...
    'django_filters',
]
Search Returns No Results
Causes:

Search term doesn't match any records
Search fields not properly configured

Solution:

Verify search_fields in view includes correct model fields
Try broader search terms
Check data exists in database

Author
Edidiong Aquatang

GitHub: @E-d-d-i-e-A
Email: eaquatang@gmail.com
Location: Lagos, Nigeria
Program: ALX Software Engineering - Back-End Track

Technologies Used

Django: 4.2+
Django REST Framework: 3.14+
django-filter: 23.0+
Python: 3.x
Database: SQLite (development)


Repository: Alx_DjangoLearnLab
Directory: advanced-api-project
Framework: Django REST Framework
Last Updated: 2025
