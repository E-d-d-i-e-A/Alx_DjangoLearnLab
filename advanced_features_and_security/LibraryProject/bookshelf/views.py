from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from .models import Book
from .forms import BookForm
from .forms import ExampleForm


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View to list all books with secure search functionality.
    Prevents SQL injection by using Django ORM.
    """
    # Get search query from GET parameters
    search_query = request.GET.get('search', '')
    
    # Secure search using Django ORM - prevents SQL injection
    # DO NOT use raw SQL or string formatting for queries
    if search_query:
        # Safe parameterized query using Django ORM
        books = Book.objects.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query)
        )
    else:
        books = Book.objects.all()
    
    context = {
        'books': books,
        'search_query': search_query,
    }
    return render(request, 'bookshelf/book_list.html', context)


@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    View to create a new book using secure form handling.
    Uses Django forms for automatic input validation and sanitization.
    """
    if request.method == 'POST':
        # Use Django forms for secure input handling
        form = BookForm(request.POST)
        if form.is_valid():
            # Form validation automatically prevents XSS and SQL injection
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {'form': form})


@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    View to edit an existing book securely.
    Uses get_object_or_404 to prevent information disclosure.
    """
    # Secure object retrieval - returns 404 if not found
    # Prevents information disclosure about object existence
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {'form': form, 'book': book})


@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    View to delete a book with CSRF protection.
    Only accepts POST requests to prevent CSRF attacks.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        # CSRF token is automatically validated by Django middleware
        book.delete()
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


def example_form_view(request):
    """
    Example view demonstrating secure form handling.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process sanitized data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Process the data securely
            return redirect('book_list')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})
