from django.db import models

class Author(models.Model):
    """
    Author Model
    Stores basic information about an author.
    One Author → Many Books.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book Model
    Represents a book written by an author.
    Establishes a one-to-many relationship.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"
    )

    def __str__(self):
        return self.title
