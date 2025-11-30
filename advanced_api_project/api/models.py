from django.db import models


class Author(models.Model):
    """
    Author model representing a book author.
    
    An author can write multiple books (one-to-many relationship).
    The related_name 'books' allows accessing an author's books via author.books.all()
    
    Fields:
        name (CharField): The full name of the author (max 200 characters)
    """
    name = models.CharField(max_length=200)
    
    def __str__(self):
        """String representation of the Author model"""
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Book(models.Model):
    """
    Book model representing a published book.
    
    Each book is linked to one author through a ForeignKey relationship.
    When an author is deleted, their books are also deleted (CASCADE behavior).
    
    Fields:
        title (CharField): The title of the book (max 200 characters)
        publication_year (IntegerField): The year the book was published
        author (ForeignKey): Reference to the Author who wrote this book
    
    Relationships:
        - Many-to-One with Author: Multiple books can have the same author
        - Accessible from Author via reverse relationship: author.books.all()
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,
        related_name='books'
    )
    
    def __str__(self):
        """String representation of the Book model"""
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        ordering = ['-publication_year']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
