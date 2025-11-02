# Create Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(f"Book created: {book.title} by {book.author} ({book.publication_year})")
```

## Expected Output
```
Book created: 1984 by George Orwell (1949)
```

## Explanation
- Created a new Book instance with title "1984"
- Author: George Orwell
- Publication year: 1949
- The `create()` method saves the object to the database automatically
