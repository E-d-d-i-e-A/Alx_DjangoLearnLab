from django.urls import path
from . import views
from .views import LibraryDetailView

urlpatterns = [
    # Function-based view URL - lists all books
    path('books/', views.list_books, name='list_books'),
    
    # Class-based view URL - displays library details
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]