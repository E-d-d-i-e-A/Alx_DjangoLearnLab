from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book


class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for CustomUser model.
    """
    model = CustomUser
    
    # Display these fields in the user list
    list_display = ['username', 'email', 'date_of_birth', 'is_staff', 'is_active']
    
    # Add filters for these fields
    list_filter = ['is_staff', 'is_active', 'date_of_birth']
    
    # Enable search by these fields
    search_fields = ['username', 'email']
    
    # Default ordering
    ordering = ['username']
    
    # Fieldsets for editing existing users
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    
    # Fieldsets for adding new users
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )


class BookAdmin(admin.ModelAdmin):
    """
    Admin interface for Book model.
    """
    list_display = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author']
    list_filter = ['publication_year']


# Register CustomUser with CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)

# Register Book model
admin.site.register(Book, BookAdmin)
