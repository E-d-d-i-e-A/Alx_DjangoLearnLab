from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    This serializer handles the conversion between Book model instances and JSON format.
    It includes custom validation to ensure data integrity.
    
    Fields:
        id (int): Auto-generated primary key (read-only).
        title (str): The title of the book.
        publication_year (int): The year the book was published.
        author (int): Foreign key reference to the Author model.
    
    Validation:
        The publication_year field has custom validation to ensure it is not in the future.
        This is implemented in the validate_publication_year method.
    
    Meta:
        model: Book - The model this serializer is based on.
        fields: List of fields to include in serialization.
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation for the publication_year field.
        
        Ensures that the publication year is not in the future. This prevents
        users from creating book records with invalid future publication dates.
        
        Args:
            value (int): The publication year to validate.
            
        Returns:
            int: The validated publication year if it passes validation.
            
        Raises:
            serializers.ValidationError: If the publication year is greater than
                                        the current year.
        
        Example:
            If current year is 2024:
            - validate_publication_year(2020) -> Returns 2020 (valid)
            - validate_publication_year(2025) -> Raises ValidationError (invalid)
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
    
    This serializer demonstrates advanced serialization with nested relationships.
    It includes all books associated with an author by using a nested BookSerializer.
    
    Fields:
        id (int): Auto-generated primary key (read-only).
        name (str): The author's full name.
        books (list): Nested serialization of all books written by this author.
    
    Nested Relationship Handling:
        The 'books' field is a nested serializer that dynamically serializes all
        books related to an author. This is achieved through:
        
        1. The BookSerializer is used to serialize each book.
        2. many=True indicates this is a one-to-many relationship (one author, many books).
        3. read_only=True means books are only included during serialization (GET requests),
           not during deserialization (POST/PUT requests).
        4. The field name 'books' corresponds to the related_name='books' defined in
           the Book model's ForeignKey field.
    
    How the relationship works:
        - When an Author instance is serialized, Django automatically follows the
          reverse relationship (author.books) to fetch all related Book instances.
        - Each Book instance is then serialized using the BookSerializer.
        - The result is a nested JSON structure where each author includes an array
          of their books with full book details.
    
    Example JSON output:
        {
            "id": 1,
            "name": "J.K. Rowling",
            "books": [
                {
                    "id": 1,
                    "title": "Harry Potter and the Philosopher's Stone",
                    "publication_year": 1997,
                    "author": 1
                },
                {
                    "id": 2,
                    "title": "Harry Potter and the Chamber of Secrets",
                    "publication_year": 1998,
                    "author": 1
                }
            ]
        }
    
    Meta:
        model: Author - The model this serializer is based on.
        fields: List of fields to include, including the nested 'books' field.
    """
    
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

---
