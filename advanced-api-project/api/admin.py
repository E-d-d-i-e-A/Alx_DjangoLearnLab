from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Author model.
    
    Provides a user-friendly interface in Django admin for managing authors.
    """
    list_display = ['id', 'name', 'book_count']
    search_fields = ['name']
    ordering = ['name']
    
    def book_count(self, obj):
        """Display the number of books by this author"""
        return obj.books.count()
    
    book_count.short_description = 'Number of Books'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Book model.
    
    Provides a user-friendly interface in Django admin for managing books.
    """
    list_display = ['id', 'title', 'author', 'publication_year']
    list_filter = ['publication_year', 'author']
    search_fields = ['title', 'author__name']
    ordering = ['-publication_year']
