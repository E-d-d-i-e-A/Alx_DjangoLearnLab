# Delete Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print("Book deleted successfully")

# Confirm deletion
all_books = Book.objects.all()
print(f"Total books in database: {all_books.count()}")
```

## Expected Output
```
Book deleted successfully
Total books in database: 0
```

## Explanation
- Retrieved the book with title "Nineteen Eighty-Four"
- Called `delete()` method to remove it from the database
- Confirmed deletion by querying all books
- Count should be 0 if this was the only book
