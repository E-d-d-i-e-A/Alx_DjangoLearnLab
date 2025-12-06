from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from taggit.models import Tag
from .models import Post, Comment
from .forms import CustomUserCreationForm, UserUpdateForm, CommentForm


# ==================== Authentication Views ====================

def register(request):
    """User registration view."""
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
    """User login view."""
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
    """User logout view."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile(request):
    """User profile view."""
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
    """Display all blog posts."""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5


class PostDetailView(DetailView):
    """
    Display a single blog post with comments.
    
    Shows the full post content and all associated comments.
    Includes a comment form for authenticated users.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        """Add comment form and comments to context."""
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new blog post."""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'tags']
    
    def form_valid(self, form):
        """Set the post author to the current user before saving."""
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Return URL to redirect after successful post creation."""
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing blog post."""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'tags']
    
    def form_valid(self, form):
        """Process the form after validation."""
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """Check if the current user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        """Return URL to redirect after successful post update."""
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a blog post."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    
    def delete(self, request, *args, **kwargs):
        """Process the deletion and show success message."""
        messages.success(self.request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        """Check if the current user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author


# ==================== Comment CRUD Views ====================

class CommentCreateView(LoginRequiredMixin, CreateView):
    """Create a new comment on a blog post."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        """Set the comment author and post before saving."""
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        messages.success(self.request, 'Your comment has been added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the post detail page after comment creation."""
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing comment."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        """Process the form after validation."""
        messages.success(self.request, 'Your comment has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """Check if the current user is the author of the comment."""
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        """Redirect to the post detail page after comment update."""
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a comment."""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def delete(self, request, *args, **kwargs):
        """Process the deletion and show success message."""
        messages.success(self.request, 'Your comment has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        """Check if the current user is the author of the comment."""
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        """Redirect to the post detail page after comment deletion."""
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})


# ==================== Search and Tag Views ====================

def search_posts(request):
    """
    Search for blog posts based on title, content, or tags.
    
    Uses Django's Q objects to perform complex lookups across multiple fields.
    Searches in post title, content, and associated tags.
    
    Args:
        request: HTTP request with 'q' parameter containing search query
        
    Returns:
        Rendered search results page with matching posts
    """
    query = request.GET.get('q', '')
    posts = Post.objects.none()
    
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    context = {
        'posts': posts,
        'query': query
    }
    return render(request, 'blog/search_results.html', context)


def posts_by_tag(request, tag_name):
    """
    Display all posts associated with a specific tag.
    
    Filters posts by tag name and displays them in a list view.
    
    Args:
        request: HTTP request
        tag_name: Name of the tag to filter by
        
    Returns:
        Rendered page with posts filtered by tag
    """
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(tags__name__in=[tag_name])
    
    context = {
        'posts': posts,
        'tag': tag
    }
    return render(request, 'blog/posts_by_tag.html', context)


# ==================== Legacy Home View ====================

def home(request):
    """Legacy home view - redirects to post list."""
    return redirect('post-list')
