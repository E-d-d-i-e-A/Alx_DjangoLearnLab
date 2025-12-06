from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for Post model.
    
    Customizes the admin interface for managing blog posts.
    """
    list_display = ['title', 'author', 'published_date']
    list_filter = ['published_date', 'author']
    search_fields = ['title', 'content']
    date_hierarchy = 'published_date'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Comment model.
    
    Customizes the admin interface for managing comments.
    """
    list_display = ['author', 'post', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'author']
    search_fields = ['content', 'author__username', 'post__title']
    date_hierarchy = 'created_at'
