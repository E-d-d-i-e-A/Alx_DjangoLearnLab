# CRUD Operations Documentation for Book Model

## Overview
This document demonstrates all CRUD (Create, Read, Update, Delete) operations performed on the Book model in the Django shell.

---

## 1. CREATE Operation

### Command:
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(f"Book created: {book.title} by {book.author} ({book.publication_year})")
```

### Output:
```
Book created: 1984 by George Orwell (1949)
```

### Description:
Created a new Book instance with:
- Title: "1984"
- Author: "George Orwell"
- Publication Year: 1949

---

## 2. RETRIEVE Operation

### Command:
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

### Output:
```
Title: 1984
Author: George Orwell
Publication Year: 1949
```

### Description:
Retrieved the book titled "1984" and displayed all its attributes.

---

## 3. UPDATE Operation

### Command:
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated title: {book.title}")
```

### Output:
```
Updated title: Nineteen Eighty-Four
```

### Description:
Updated the book title from "1984" to "Nineteen Eighty-Four" and saved the changes.

---

## 4. DELETE Operation

### Command:
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print("Book deleted successfully")

# Confirm deletion
all_books = Book.objects.all()
print(f"Total books in database: {all_books.count()}")
```

### Output:
```
Book deleted successfully
Total books in database: 0
```

### Description:
Deleted the book from the database and confirmed by checking the total count of books.

---

## Summary
All CRUD operations were successfully performed:
- ✅ Created a Book instance
- ✅ Retrieved the book and displayed its attributes
- ✅ Updated the book's title
- ✅ Deleted the book and confirmed deletion

## Django ORM Methods Used
- `objects.create()` - Create and save a new object
- `objects.get()` - Retrieve a single object
- `.save()` - Save changes to an existing object
- `.delete()` - Delete an object from the database
- `objects.all()` - Retrieve all objects
- `.count()` - Count the number of objects
```
