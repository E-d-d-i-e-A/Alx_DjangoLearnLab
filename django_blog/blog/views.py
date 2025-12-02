from django.shortcuts import render
from .models import Post


def home(request):
    """
    Home view - displays all blog posts.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered home.html template with list of all posts
    """
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})
