from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    Converts Book model instances to JSON format and vice versa.
    Includes custom validation to ensure publication_year is not in the future.
    
    Fields:
        - id: Auto-generated primary key
        - title: Book title
        - publication_year: Year of publication (validated)
        - author: Foreign key to Author (ID only in this serializer)
    
    Custom Validation:
        - publication_year cannot be in the future
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validator for publication_year field.
        
        Ensures that the publication year is not in the future.
        This prevents users from entering invalid dates like 2050 for a book
        published today.
        
        Args:
            value (int): The publication year to validate
        
        Returns:
            int: The validated publication year
        
        Raises:
            serializers.ValidationError: If publication year is in the future
        """
        current_year = datetime.now().year
        
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested Book serialization.
    
    This serializer includes a nested representation of all books written by the author.
    When an Author is serialized, all their related books are automatically included
    in the response using the BookSerializer.
    
    Fields:
        - id: Auto-generated primary key
        - name: Author's full name
        - books: Nested list of all books by this author (read-only)
    
    Nested Serialization:
        - The 'books' field uses BookSerializer to represent related books
        - 'many=True' indicates multiple books can be associated with one author
        - 'read_only=True' means books are only shown in responses, not required for creation
    
    Relationship Handling:
        - Uses the 'books' related_name from the Author model's reverse relationship
        - Automatically fetches all books where author = this Author instance
        - Each book is serialized using the BookSerializer defined above
    
    Usage Example:
        When serializing an Author instance:
        {
            "id": 1,
            "name": "George Orwell",
            "books": [
                {
                    "id": 1,
                    "title": "1984",
                    "publication_year": 1949,
                    "author": 1
                },
                {
                    "id": 2,
                    "title": "Animal Farm",
                    "publication_year": 1945,
                    "author": 1
                }
            ]
        }
    """
    
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
