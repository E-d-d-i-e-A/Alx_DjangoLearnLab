from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Post
from .forms import CustomUserCreationForm, UserUpdateForm


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


def register(request):
    """
    User registration view.
    
    Handles user registration using CustomUserCreationForm.
    On successful registration, logs in the user and redirects to home.
    
    Args:
        request: HTTP request object
        
    Returns:
        GET: Renders registration form
        POST: Processes form and redirects to home on success
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}! You are now logged in.')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})


def user_login(request):
    """
    User login view.
    
    Handles user authentication using Django's AuthenticationForm.
    On successful login, redirects to home or next page.
    
    Args:
        request: HTTP request object
        
    Returns:
        GET: Renders login form
        POST: Authenticates user and redirects on success
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'blog/login.html', {'form': form})


def user_logout(request):
    """
    User logout view.
    
    Logs out the current user and redirects to home page.
    
    Args:
        request: HTTP request object
        
    Returns:
        Redirects to home page with logout confirmation message
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile(request):
    """
    User profile view.
    
    Allows authenticated users to view and update their profile.
    Requires user to be logged in (login_required decorator).
    
    Args:
        request: HTTP request object
        
    Returns:
        GET: Renders profile page with update form
        POST: Processes form update and redirects to profile
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'blog/profile.html', context)
