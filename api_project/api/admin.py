from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface for Book model.
    """
    list_display = ['title', 'author']
    search_fields = ['title', 'author']
