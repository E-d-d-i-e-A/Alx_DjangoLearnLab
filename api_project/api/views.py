from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to retrieve list of all books.
    
    GET /api/books/ - Returns list of all books in JSON format
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
