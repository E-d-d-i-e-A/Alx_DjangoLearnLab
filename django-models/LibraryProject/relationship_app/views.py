from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from .models import Library
from .models import Book

# Function-based view to list all books
def list_books(request):
    """
    Function-based view that lists all books in the database.
    """
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view to display library details
class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library,
    including all books available in that library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# User Registration View
def register(request):
    """
    View for user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# Helper function to check if user is Admin
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'


# Helper function to check if user is Librarian
def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'


# Helper function to check if user is Member
def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# Admin view - Only accessible by Admin role
@user_passes_test(is_admin)
def admin_view(request):
    """
    View accessible only to users with Admin role.
    """
    return render(request, 'relationship_app/admin_view.html')


# Librarian view - Only accessible by Librarian role
@user_passes_test(is_librarian)
def librarian_view(request):
    """
    View accessible only to users with Librarian role.
    """
    return render(request, 'relationship_app/librarian_view.html')


# Member view - Only accessible by Member role
@user_passes_test(is_member)
def member_view(request):
    """
    View accessible only to users with Member role.
    """
    return render(request, 'relationship_app/member_view.html')