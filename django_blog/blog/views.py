from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .forms import CustomUserCreationForm, UserUpdateForm


# ==================== Authentication Views ====================

def register(request):
    """
    User registration view.
    
    Handles user registration using CustomUserCreationForm.
    On successful registration, logs in the user and redirects to home.
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
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile(request):
    """
    User profile view.
    
    Allows authenticated users to view and update their profile.
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


# ==================== Blog Post CRUD Views ====================

class PostListView(ListView):
    """
    Display all blog posts.
    
    ListView for displaying all published blog posts ordered by
    publication date (newest first). Accessible to all users.
    
    Attributes:
        model: Post model
        template_name: Template for rendering the list
        context_object_name: Name for the list in template context
        ordering: Order posts by publication date (descending)
        paginate_by: Number of posts per page
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5


class PostDetailView(DetailView):
    """
    Display a single blog post.
    
    DetailView for showing the full content of a single blog post.
    Accessible to all users.
    
    Attributes:
        model: Post model
        template_name: Template for rendering the detail view
        context_object_name: Name for the post in template context
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new blog post.
    
    CreateView for authenticated users to create new blog posts.
    Automatically sets the author to the currently logged-in user.
    
    Attributes:
        model: Post model
        template_name: Template for rendering the form
        fields: Fields to include in the form
        success_url: URL to redirect after successful creation
    
    Mixins:
        LoginRequiredMixin: Ensures only authenticated users can access
    """
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        """
        Set the post author to the current user before saving.
        
        Args:
            form: The valid form instance
            
        Returns:
            HttpResponse redirect to success_url
        """
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Return URL to redirect after successful post creation."""
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update an existing blog post.
    
    UpdateView for post authors to edit their own posts.
    Only the author of the post can edit it.
    
    Attributes:
        model: Post model
        template_name: Template for rendering the form
        fields: Fields to include in the form
    
    Mixins:
        LoginRequiredMixin: Ensures only authenticated users can access
        UserPassesTestMixin: Ensures only the post author can edit
    """
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        """
        Process the form after validation.
        
        Args:
            form: The valid form instance
            
        Returns:
            HttpResponse redirect to success_url
        """
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """
        Check if the current user is the author of the post.
        
        Returns:
            bool: True if user is the post author, False otherwise
        """
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        """Return URL to redirect after successful post update."""
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a blog post.
    
    DeleteView for post authors to delete their own posts.
    Only the author of the post can delete it.
    
    Attributes:
        model: Post model
        template_name: Template for rendering the confirmation page
        success_url: URL to redirect after successful deletion
    
    Mixins:
        LoginRequiredMixin: Ensures only authenticated users can access
        UserPassesTestMixin: Ensures only the post author can delete
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    
    def delete(self, request, *args, **kwargs):
        """
        Process the deletion and show success message.
        
        Returns:
            HttpResponse redirect to success_url
        """
        messages.success(self.request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        """
        Check if the current user is the author of the post.
        
        Returns:
            bool: True if user is the post author, False otherwise
        """
        post = self.get_object()
        return self.request.user == post.author


# ==================== Legacy Home View ====================

def home(request):
    """
    Legacy home view - redirects to post list.
    
    This view is kept for backward compatibility.
    Consider using PostListView directly.
    """
    return redirect('post-list')
