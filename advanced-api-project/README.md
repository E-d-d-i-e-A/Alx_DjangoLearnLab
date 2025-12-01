Advanced API Project - Django REST Framework
Overview
This Django REST Framework project demonstrates advanced API development concepts including custom serializers with nested relationships, generic views for CRUD operations, permission-based access control, and query optimization through filtering, searching, and ordering.
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

BookListView (ListAPIView) - List all books with filtering, searching, ordering
BookDetailView (RetrieveAPIView) - Retrieve single book by ID
BookCreateView (CreateAPIView) - Create new book entries
BookUpdateView (UpdateAPIView) - Update existing books (PUT/PATCH)
BookDeleteView (DestroyAPIView) - Delete books

3. Permission-Based Access Control
Views are protected using Django REST Framework's permission classes:

IsAuthenticatedOrReadOnly: Applied to ListView and DetailView

Public read access for all users
Write operations require authentication


IsAuthenticated: Applied to CreateView, UpdateView, DeleteView

All operations require authentication
Unauthenticated users receive 401 Unauthorized



4. Advanced Query Capabilities
Filtering
Filter books by exact field values using DjangoFilterBackend:

title - Filter by book title
author - Filter by author ID
publication_year - Filter by publication year
Multiple filters can be combined

Searching
Text search across multiple fields using SearchFilter:

Searches in title field
Searches in author__name field (related model)
Case-insensitive partial matching

Ordering
Sort results by specified fields using OrderingFilter:

Available ordering fields: title, publication_year
Supports ascending (default) and descending (prefix with -)
Default ordering: title (ascending)

API Endpoints
Public Endpoints (No Authentication Required)
List All Books

URL: /api/books/
Method: GET
Description: Retrieve list of all books with filtering, searching, and ordering capabilities
Query Parameters:

Filtering: ?title=<value>, ?author=<id>, ?publication_year=<year>
Searching: ?search=<term>
Ordering: ?ordering=<field> or ?ordering=-<field>


Response: 200 OK with array of book objects

Examples:
GET /api/books/
GET /api/books/?author=1
GET /api/books/?publication_year=2020
GET /api/books/?search=django
GET /api/books/?ordering=-publication_year
GET /api/books/?search=python&publication_year=2020&ordering=title
Get Book Detail

URL: /api/books/<id>/
Method: GET
Description: Retrieve a single book by ID
Response: 200 OK with book object

Protected Endpoints (Authentication Required)
Create Book

URL: /api/books/create/
Method: POST
Permissions: Authenticated users only
Request Body:

json{
    "title": "Book Title",
    "publication_year": 2024,
    "author": 1
}

Response: 201 Created with new book object

Update Book

URL: /api/books/<id>/update/
Methods: PUT (full update), PATCH (partial update)
Permissions: Authenticated users only
Request Body (PUT):

json{
    "title": "Updated Title",
    "publication_year": 2024,
    "author": 1
}

Request Body (PATCH):

json{
    "title": "Updated Title Only"
}

Response: 200 OK with updated book object

Delete Book

URL: /api/books/<id>/delete/
Method: DELETE
Permissions: Authenticated users only
Response: 204 No Content

Models
Author

name (CharField): Author's full name
Relationship: One-to-many with Book model

Book

title (CharField): Book title
publication_year (IntegerField): Year published
author (ForeignKey): Reference to Author model
Relationship: Many-to-one with Author model
Related Name: books for reverse lookup

Configuration
Settings

INSTALLED_APPS: Includes rest_framework, django_filters, api
REST_FRAMEWORK: Configured with default filter backends

DjangoFilterBackend for field filtering
SearchFilter for text search
OrderingFilter for result ordering



URL Configuration

Main URLs: /api/ includes all API endpoints
Admin interface: /admin/

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
    "publication_year": 2024,
    "author": 1
  }'
Using Postman

Base URL: http://localhost:8000/api/
For Public Endpoints:

No authentication needed
Add query parameters in Params tab


For Protected Endpoints:

Add header: Authorization: Token YOUR_TOKEN_HERE
Set appropriate HTTP method
Add request body for POST/PUT/PATCH



Setup Instructions

Clone the repository:

bashgit clone https://github.com/YOUR_USERNAME/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/advanced-api-project

Create virtual environment:

bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

bashpip install -r requirements.txt

Run migrations:

bashpython manage.py migrate

Create superuser:

bashpython manage.py createsuperuser

Run development server:

bashpython manage.py runserver

Access the API:

API endpoints: http://localhost:8000/api/
Admin interface: http://localhost:8000/admin/



Dependencies

Django >= 4.2.0
djangorestframework >= 3.14.0
django-filter >= 23.0

Project Structure
advanced-api-project/
├── advanced_api_project/
│   ├── settings.py          # Project settings and configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py
├── api/
│   ├── models.py            # Author and Book models
│   ├── serializers.py       # Custom serializers with validation
│   ├── views.py             # Generic API views with filters
│   ├── urls.py              # API endpoint routing
│   └── admin.py             # Admin configuration
├── manage.py
├── requirements.txt
└── README.md
Key Implementation Details
View Configurations

filter_backends: List of filter backend classes applied to views
filterset_fields: Fields available for exact match filtering
search_fields: Fields included in text search
ordering_fields: Fields available for ordering results
ordering: Default ordering applied to queryset

Permission Classes

Configured at view level using permission_classes attribute
Evaluated before view logic executes
Return 401 Unauthorized for unauthenticated users on protected endpoints

Serializer Validation

Custom validation methods follow naming pattern: validate_<field_name>
Called automatically during serialization
Raise serializers.ValidationError for invalid data

Future Enhancements

Add pagination for large datasets
Implement throttling to prevent API abuse
Add API versioning
Implement caching for improved performance
Add more custom permissions for fine-grained access control
Implement soft deletes instead of permanent deletion


Repository: Alx_DjangoLearnLab
Directory: advanced-api-project
Framework: Django REST Framework
Last Updated: 2025
