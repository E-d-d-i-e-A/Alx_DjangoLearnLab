from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from .views import register, user_login, user_logout

urlpatterns = [
    # Book and Library views
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication views
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]