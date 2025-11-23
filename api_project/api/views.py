from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to retrieve list of all books.
    
    GET /api/books/ - Returns list of all books in JSON format
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling all CRUD operations on Book model.
    
    Provides:
    - list: GET /books_all/ - List all books
    - create: POST /books_all/ - Create a new book
    - retrieve: GET /books_all/<id>/ - Get a specific book
    - update: PUT /books_all/<id>/ - Update a book
    - partial_update: PATCH /books_all/<id>/ - Partially update a book
    - destroy: DELETE /books_all/<id>/ - Delete a book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
