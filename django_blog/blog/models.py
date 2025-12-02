from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Blog Post model.
    
    Represents a blog post with title, content, publication date, and author.
    
    Fields:
        title (CharField): The title of the blog post (max 200 characters).
        content (TextField): The main content/body of the blog post.
        published_date (DateTimeField): Automatically set to the date/time when post is created.
        author (ForeignKey): Link to User model - the author of the post.
                            One user can have multiple posts (one-to-many relationship).
                            When user is deleted, their posts are also deleted (CASCADE).
    
    Methods:
        __str__: Returns the post title as string representation.
    
    Meta:
        ordering: Posts are ordered by publication date (newest first).
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-published_date']
