from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Post(models.Model):
    """
    Blog Post model.
    
    Represents a blog post with title, content, publication date, author, and tags.
    
    Fields:
        title (CharField): The title of the blog post (max 200 characters).
        content (TextField): The main content/body of the blog post.
        published_date (DateTimeField): Automatically set to the date/time when post is created.
        author (ForeignKey): Link to User model - the author of the post.
                            One user can have multiple posts (one-to-many relationship).
                            When user is deleted, their posts are also deleted (CASCADE).
        tags (TaggableManager): Manages tags for the post using django-taggit.
                               Allows many-to-many relationship between posts and tags.
                               Multiple posts can share the same tag.
    
    Methods:
        __str__: Returns the post title as string representation.
    
    Meta:
        ordering: Posts are ordered by publication date (newest first).
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = TaggableManager()
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-published_date']


class Comment(models.Model):
    """
    Comment model for blog posts.
    
    Represents a comment on a blog post with content, author, and timestamps.
    
    Fields:
        post (ForeignKey): Link to Post model - the post being commented on.
                          One post can have multiple comments (one-to-many relationship).
                          When post is deleted, all comments are deleted (CASCADE).
        author (ForeignKey): Link to User model - the user who wrote the comment.
                            One user can write multiple comments (one-to-many relationship).
                            When user is deleted, their comments are deleted (CASCADE).
        content (TextField): The text content of the comment.
        created_at (DateTimeField): Automatically set when comment is created.
        updated_at (DateTimeField): Automatically updated when comment is modified.
    
    Methods:
        __str__: Returns a string showing author and post being commented on.
    
    Meta:
        ordering: Comments are ordered by creation date (oldest first).
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    class Meta:
        ordering = ['created_at']
