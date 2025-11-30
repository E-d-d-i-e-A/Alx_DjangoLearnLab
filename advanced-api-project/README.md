# Advanced API Project - Custom Serializers

## Overview
This project demonstrates advanced Django REST Framework concepts, focusing on custom serializers with nested relationships and custom validation.

## Features
- Custom serializers for complex data structures
- Nested serialization (Author with Books)
- Custom validation (publication year)
- One-to-many relationships
- Django admin integration

## Models

### Author Model
- **name**: CharField - Author's full name

### Book Model
- **title**: CharField - Book title
- **publication_year**: IntegerField - Year published
- **author**: ForeignKey - Link to Author (one-to-many)

## Serializers

### BookSerializer
Serializes Book model with custom validation:
- Ensures `publication_year` is not in the future
- All fields included: id, title, publication_year, author

### AuthorSerializer
Serializes Author model with nested books:
- Includes author name
- Nested BookSerializer for related books
- Read-only books field

## Setup Instructions

### 1. Install Dependencies
```bash
pip install django djangorestframework
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Run Server
```bash
python manage.py runserver
```

### 5. Access Admin
Visit: `http://127.0.0.1:8000/admin/`

## Testing Serializers

### Using Django Shell
```bash
python manage.py shell
```
```python
from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer

# Create an author
author = Author.objects.create(name="George Orwell")

# Create books
book1 = Book.objects.create(
    title="1984",
    publication_year=1949,
    author=author
)

book2 = Book.objects.create(
    title="Animal Farm",
    publication_year=1945,
    author=author
)

# Test BookSerializer
book_serializer = BookSerializer(book1)
print(book_serializer.data)
# Output: {'id': 1, 'title': '1984', 'publication_year': 1949, 'author': 1}

# Test AuthorSerializer with nested books
author_serializer = AuthorSerializer(author)
print(author_serializer.data)
# Output: {
#     'id': 1,
#     'name': 'George Orwell',
#     'books': [
#         {'id': 1, 'title': '1984', 'publication_year': 1949, 'author': 1},
#         {'id': 2, 'title': 'Animal Farm', 'publication_year': 1945, 'author': 1}
#     ]
# }

# Test validation - future year (should fail)
from datetime import datetime
future_year = datetime.now().year + 1

serializer = BookSerializer(data={
    'title': 'Future Book',
    'publication_year': future_year,
    'author': author.id
})

print(serializer.is_valid())  # False
print(serializer.errors)
# {'publication_year': ['Publication year cannot be in the future. Current year is 2025.']}
```

## Relationship Explanation

### One-to-Many Relationship
- **Author → Books**: One author can write many books
- **ForeignKey**: Each book has one author
- **related_name='books'**: Access author's books via `author.books.all()`

### Nested Serialization
The `AuthorSerializer` includes nested `BookSerializer`:
```python
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
```

**How it works:**
1. When serializing an Author, Django automatically fetches related books
2. Uses the `books` related_name from the ForeignKey
3. Each book is serialized using BookSerializer
4. `many=True` handles multiple book instances
5. `read_only=True` means books are output-only

## Custom Validation

### Publication Year Validation
Ensures books can't have future publication dates:
```python
def validate_publication_year(self, value):
    current_year = datetime.now().year
    
    if value > current_year:
        raise serializers.ValidationError(
            f"Publication year cannot be in the future. Current year is {current_year}."
        )
    
    return value
```

## Project Structure
```
advanced-api-project/
├── manage.py
├── README.md
├── advanced-api-project/
│   ├── __init__.py
│   ├── settings.py          # REST framework configured
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── api/
    ├── __init__.py
    ├── models.py             # Author and Book models
    ├── serializers.py        # Custom serializers
    ├── admin.py              # Admin configuration
    ├── apps.py
    ├── views.py
    └── tests.py
```

## Testing Checklist
- [ ] Create Author via admin
- [ ] Create Books linked to Author
- [ ] Test BookSerializer in shell
- [ ] Test AuthorSerializer with nested books
- [ ] Test validation with future year (should fail)
- [ ] Test validation with valid year (should pass)

## Author
**Edidiong Aquatang**
- GitHub: [@E-d-d-i-e-A](https://github.com/E-d-d-i-e-A)
- ALX Software Engineering Program
```
