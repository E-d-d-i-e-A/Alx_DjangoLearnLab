# Update Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated title: {book.title}")
```

## Expected Output
```
Updated title: Nineteen Eighty-Four
```

## Explanation
- Retrieved the book with title "1984"
- Changed the title to "Nineteen Eighty-Four"
- Called `save()` method to persist changes to the database
- Confirmed the update by printing the new title
