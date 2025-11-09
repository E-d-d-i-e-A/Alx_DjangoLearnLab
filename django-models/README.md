# Django Models - Advanced Relationships

This project demonstrates advanced Django model relationships including ForeignKey, ManyToMany, and OneToOne fields.

## Project Structure
```
django-models/
└── LibraryProject/
    └── relationship_app/
        ├── models.py          # Model definitions
        ├── query_samples.py   # Sample queries
        └── ...
```

## Models

### Author
- **name**: CharField
- Relationship: One-to-Many with Book (one author can write many books)

### Book
- **title**: CharField
- **author**: ForeignKey to Author
- Relationship: Many-to-One with Author, Many-to-Many with Library

### Library
- **name**: CharField
- **books**: ManyToManyField to Book
- Relationship: Many-to-Many with Book, One-to-One with Librarian

### Librarian
- **name**: CharField
- **library**: OneToOneField to Library
- Relationship: One-to-One with Library (each library has one librarian)

## Relationships Explained

### ForeignKey (Author -> Book)
- One author can have many books
- Each book has exactly one author
- Example: George Orwell wrote "1984" and "Animal Farm"

### ManyToManyField (Library -> Book)
- A library can have many books
- A book can be in many libraries
- Example: "1984" can be in Central Library and City Library

### OneToOneField (Librarian -> Library)
- Each library has exactly one librarian
- Each librarian manages exactly one library
- Example: John Smith is the librarian of Central Library

## Sample Queries

### Query all books by a specific author:
```python
from relationship_app.query_samples import query_books_by_author
query_books_by_author("George Orwell")
```

### List all books in a library:
```python
from relationship_app.query_samples import list_books_in_library
list_books_in_library("Central Library")
```

### Retrieve the librarian for a library:
```python
from relationship_app.query_samples import retrieve_librarian_for_library
retrieve_librarian_for_library("Central Library")
```

## Setup Instructions

1. **Create the app:**
```bash
   python manage.py startapp relationship_app
```

2. **Add to INSTALLED_APPS in settings.py:**
```python
   INSTALLED_APPS = [
       ...
       'relationship_app',
   ]
```

3. **Make migrations:**
```bash
   python manage.py makemigrations relationship_app
```

4. **Apply migrations:**
```bash
   python manage.py migrate
```

5. **Test queries in Django shell:**
```bash
   python manage.py shell
   >>> from relationship_app.query_samples import *
   >>> query_books_by_author("George Orwell")
```

## Author
**Edidiong Aquatang**
- GitHub: [@E-d-d-i-e-A](https://github.com/E-d-d-i-e-A)
- ALX Software Engineering Program
