from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    API view to retrieve list of all books with filtering, searching, and ordering.
    
    Endpoint: GET /api/books/
    
    Permissions:
        - Read-only access for all users (authenticated and unauthenticated)
    
    Filtering:
        Filter books by specific field values.
        Examples:
            - /api/books/?title=Django for Beginners
            - /api/books/?author=1
            - /api/books/?publication_year=2020
            - /api/books/?author=1&publication_year=2020
    
    Searching:
        Search across title and author name fields.
        Examples:
            - /api/books/?search=django
            - /api/books/?search=python
            - /api/books/?search=rowling
    
    Ordering:
        Order results by any field. Use '-' prefix for descending order.
        Examples:
            - /api/books/?ordering=title
            - /api/books/?ordering=-publication_year
            - /api/books/?ordering=author
    
    Combined Usage:
        You can combine filtering, searching, and ordering in one request.
        Example:
            /api/books/?search=python&publication_year=2020&ordering=-title
    
    Returns:
        - List of Book instances matching the query parameters
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = ['title', 'author', 'publication_year']
    
    search_fields = ['title', 'author__name']
    
    ordering_fields = ['title', 'publication_year']
    
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single book by its ID.
    
    Endpoint: GET /books/<int:pk>/
    
    Permissions:
        - Read-only access for all users (authenticated and unauthenticated)
    
    Returns:
        - Single Book instance serialized with BookSerializer
        
    Usage:
        GET /books/1/ - Returns book with ID 1
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    API view to create a new book.
    
    Endpoint: POST /books/create/
    
    Permissions:
        - Only authenticated users can create books
        - Unauthenticated requests will receive 401 Unauthorized
    
    Request Body:
        {
            "title": "Book Title",
            "publication_year": 2024,
            "author": 1
        }
    
    Validation:
        - All fields are required
        - publication_year cannot be in the future (custom validation in serializer)
        - author must be a valid Author ID
    
    Returns:
        - 201 Created with the newly created book data
        - 400 Bad Request if validation fails
        - 401 Unauthorized if user is not authenticated
        
    Usage:
        POST /books/create/
        Headers: Authorization: Token <your-token>
        Body: JSON data with book details
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom create method to handle additional logic during book creation.
        
        This method is called after validation but before saving.
        Can be extended to add custom behavior like:
        - Setting default values
        - Logging creation events
        - Sending notifications
        """
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing book.
    
    Endpoints: 
        - PUT /books/<int:pk>/update/ - Full update (all fields required)
        - PATCH /books/<int:pk>/update/ - Partial update (only provided fields updated)
    
    Permissions:
        - Only authenticated users can update books
        - Unauthenticated requests will receive 401 Unauthorized
    
    Request Body (PUT - all fields required):
        {
            "title": "Updated Title",
            "publication_year": 2024,
            "author": 1
        }
    
    Request Body (PATCH - partial update):
        {
            "title": "Updated Title Only"
        }
    
    Validation:
        - publication_year cannot be in the future
        - author must be a valid Author ID if provided
    
    Returns:
        - 200 OK with updated book data
        - 400 Bad Request if validation fails
        - 401 Unauthorized if user is not authenticated
        - 404 Not Found if book ID doesn't exist
        
    Usage:
        PUT /books/1/update/
        PATCH /books/1/update/
        Headers: Authorization: Token <your-token>
        Body: JSON data with fields to update
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Custom update method to handle additional logic during book updates.
        
        This method is called after validation but before saving.
        Can be extended to add custom behavior like:
        - Tracking update history
        - Logging modifications
        - Triggering notifications
        """
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    API view to delete a book.
    
    Endpoint: DELETE /books/<int:pk>/delete/
    
    Permissions:
        - Only authenticated users can delete books
        - Unauthenticated requests will receive 401 Unauthorized
    
    Returns:
        - 204 No Content on successful deletion
        - 401 Unauthorized if user is not authenticated
        - 404 Not Found if book ID doesn't exist
        
    Usage:
        DELETE /books/1/delete/
        Headers: Authorization: Token <your-token>
        
    Note:
        This permanently deletes the book from the database.
        Consider implementing soft deletes for production applications.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
