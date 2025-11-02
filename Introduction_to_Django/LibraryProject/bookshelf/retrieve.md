# Retrieve Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

## Expected Output
```
Title: 1984
Author: George Orwell
Publication Year: 1949
```

## Explanation
- Used `get()` method to retrieve a single book by title
- Displayed all attributes of the retrieved book
- `get()` returns exactly one object matching the query
