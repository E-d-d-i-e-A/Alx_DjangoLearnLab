from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


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
    
    #
