from django.contrib import admin
from .models import Book

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    """Custom admin configuration for Book model."""
    
    # Display these fields in the admin list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add filters for these fields in the sidebar
    list_filter = ('author', 'publication_year')
    
    # Add search functionality for these fields
    search_fields = ('title', 'author')

# Register the Book model with the custom admin configuration
admin.site.register(Book, BookAdmin)
