from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to retrieve list of all books.
    
    Authentication: Required (IsAuthenticated)
    Permissions: Any authenticated user can view
    
    GET /api/books/ - Returns list of all books in JSON format
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling all CRUD operations on Book model.
    
    Authentication: Token Authentication required
    Permissions: 
    - IsAuthenticated: Required for all operations
    
    Provides:
    - list: GET /books_all/ - List all books (authenticated users)
    - create: POST /books_all/ - Create a new book (authenticated users)
    - retrieve: GET /books_all/<id>/ - Get a specific book (authenticated users)
    - update: PUT /books_all/<id>/ - Update a book (authenticated users)
    - partial_update: PATCH /books_all/<id>/ - Partially update a book (authenticated users)
    - destroy: DELETE /books_all/<id>/ - Delete a book (authenticated users)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for all actions
