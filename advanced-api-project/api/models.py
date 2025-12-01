from django.db import models


class Author(models.Model):
    """
    Author model representing book authors.
    
    Fields:
        name (CharField): String field storing the author's full name (max 200 characters).
    
    Relationships:
        Has a one-to-many relationship with the Book model.
        One author can have multiple books through the reverse relationship 'books'.
    
    Methods:
        __str__: Returns the author's name as the string representation.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Book(models.Model):
    """
    Book model representing books in the library system.
    
    Fields:
        title (CharField): String field for the book's title (max 300 characters).
        publication_year (IntegerField): Integer field for the year the book was published.
        author (ForeignKey): Foreign key linking to the Author model, establishing 
                            a many-to-one relationship from Book to Author.
    
    Relationships:
        Each book belongs to one author (many-to-one relationship).
        The relationship is established through the 'author' foreign key field.
        The related_name='books' allows reverse lookup from Author to Books
        using author.books.all().
        
        When an Author is deleted, all related Books are also deleted (CASCADE).
    
    Methods:
        __str__: Returns the book's title and publication year as string representation.
    """
    title = models.CharField(max_length=300)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

    class Meta:
        ordering = ['title']

---
