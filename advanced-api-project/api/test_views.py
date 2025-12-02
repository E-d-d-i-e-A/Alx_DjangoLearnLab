from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Author, Book
from datetime import datetime


class BookAPITestCase(APITestCase):
    """
    Test suite for Book API endpoints.
    
    This test case covers CRUD operations, filtering, searching, ordering,
    and permission/authentication tests for the Book API.
    """
    
    def setUp(self):
        """
        Set up test data and authentication.
        
        Creates:
            - Test users (authenticated and unauthenticated)
            - Test authors
            - Test books
            - API client for making requests
        """
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create API client
        self.client = APIClient()
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='Animal Farm',
            publication_year=1945,
            author=self.author2
        )
        
        # Define URLs
        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')
    
    def test_list_books_unauthenticated(self):
        """
        Test that unauthenticated users can view the list of books.
        
        Expected:
            - Status code: 200 OK
            - Returns all books in database
        """
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_list_books_authenticated(self):
        """
        Test that authenticated users can view the list of books.
        
        Expected:
            - Status code: 200 OK
            - Returns all books in database
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_retrieve_book_detail(self):
        """
        Test retrieving a single book by ID.
        
        Expected:
            - Status code: 200 OK
            - Returns correct book data
        """
        detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Harry Potter')
        self.assertEqual(response.data['publication_year'], 1997)
    
    def test_create_book_authenticated(self):
        """
        Test creating a book with authenticated user.
        
        Expected:
            - Status code: 201 Created
            - Book is saved in database
            - Returns created book data
        """
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'New Book',
            'publication_year': 2020,
            'author': self.author1.id
        }
        
        response = self.client.post(self.create_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(response.data['title'], 'New Book')
    
    def test_create_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books.
        
        Expected:
            - Status code: 401 Unauthorized
            - Book is not created
        """
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2020,
            'author': self.author1.id
        }
        
        response = self.client.post(self.create_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 3)
    
    def test_update_book_authenticated(self):
        """
        Test updating a book with authenticated user.
        
        Expected:
            - Status code: 200 OK
            - Book data is updated in database
        """
        self.client.force_authenticate(user=self.user)
        
        update_url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Updated Harry Potter',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.client.put(update_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Harry Potter')
    
    def test_update_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot update books.
        
        Expected:
            - Status code: 401 Unauthorized
            - Book is not updated
        """
        update_url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Unauthorized Update',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.client.put(update_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Harry Potter')
    
    def test_partial_update_book(self):
        """
        Test partial update (PATCH) of a book.
        
        Expected:
            - Status code: 200 OK
            - Only specified fields are updated
        """
        self.client.force_authenticate(user=self.user)
        
        update_url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {'title': 'Partially Updated Title'}
        
        response = self.client.patch(update_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated Title')
        self.assertEqual(self.book1.publication_year, 1997)
    
    def test_delete_book_authenticated(self):
        """
        Test deleting a book with authenticated user.
        
        Expected:
            - Status code: 204 No Content
            - Book is removed from database
        """
        self.client.force_authenticate(user=self.user)
        
        delete_url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())
    
    def test_delete_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot delete books.
        
        Expected:
            - Status code: 401 Unauthorized
            - Book is not deleted
        """
        delete_url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 3)
    
    def test_filter_books_by_title(self):
        """
        Test filtering books by title.
        
        Expected:
            - Status code: 200 OK
            - Returns only books matching the title filter
        """
        response = self.client.get(self.list_url, {'title': 'Harry Potter'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter')
    
    def test_filter_books_by_author(self):
        """
        Test filtering books by author ID.
        
        Expected:
            - Status code: 200 OK
            - Returns only books by specified author
        """
        response = self.client.get(self.list_url, {'author': self.author2.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication year.
        
        Expected:
            - Status code: 200 OK
            - Returns only books from specified year
        """
        response = self.client.get(self.list_url, {'publication_year': 1949})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')
    
    def test_search_books_by_title(self):
        """
        Test searching books by title.
        
        Expected:
            - Status code: 200 OK
            - Returns books matching search term in title
        """
        response = self.client.get(self.list_url, {'search': 'Harry'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter')
    
    def test_search_books_by_author_name(self):
        """
        Test searching books by author name.
        
        Expected:
            - Status code: 200 OK
            - Returns books by authors matching search term
        """
        response = self.client.get(self.list_url, {'search': 'Orwell'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_order_books_by_title_ascending(self):
        """
        Test ordering books by title in ascending order.
        
        Expected:
            - Status code: 200 OK
            - Books are ordered alphabetically by title
        """
        response = self.client.get(self.list_url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, ['1984', 'Animal Farm', 'Harry Potter'])
    
    def test_order_books_by_title_descending(self):
        """
        Test ordering books by title in descending order.
        
        Expected:
            - Status code: 200 OK
            - Books are ordered reverse alphabetically by title
        """
        response = self.client.get(self.list_url, {'ordering': '-title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, ['Harry Potter', 'Animal Farm', '1984'])
    
    def test_order_books_by_publication_year(self):
        """
        Test ordering books by publication year.
        
        Expected:
            - Status code: 200 OK
            - Books are ordered by publication year
        """
        response = self.client.get(self.list_url, {'ordering': 'publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [1945, 1949, 1997])
    
    def test_combined_filter_search_order(self):
        """
        Test combining filtering, searching, and ordering.
        
        Expected:
            - Status code: 200 OK
            - Returns filtered, searched, and ordered results
        """
        response = self.client.get(
            self.list_url,
            {
                'search': 'Orwell',
                'ordering': '-publication_year'
            }
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [1949, 1945])
    
    def test_create_book_with_future_year(self):
        """
        Test that creating a book with future publication year fails.
        
        Expected:
            - Status code: 400 Bad Request
            - Validation error returned
        """
        self.client.force_authenticate(user=self.user)
        
        future_year = datetime.now().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        
        response = self.client.post(self.create_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_with_invalid_data(self):
        """
        Test creating a book with missing required fields.
        
        Expected:
            - Status code: 400 Bad Request
            - Validation errors returned
        """
        self.client.force_authenticate(user=self.user)
        
        data = {'title': 'Incomplete Book'}
        
        response = self.client.post(self.create_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieve_nonexistent_book(self):
        """
        Test retrieving a book that doesn't exist.
        
        Expected:
            - Status code: 404 Not Found
        """
        detail_url = reverse('book-detail', kwargs={'pk': 9999})
        response = self.client.get(detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_nonexistent_book(self):
        """
        Test updating a book that doesn't exist.
        
        Expected:
            - Status code: 404 Not Found
        """
        self.client.force_authenticate(user=self.user)
        
        update_url = reverse('book-update', kwargs={'pk': 9999})
        data = {
            'title': 'Nonexistent',
            'publication_year': 2020,
            'author': self.author1.id
        }
        
        response = self.client.put(update_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_nonexistent_book(self):
        """
        Test deleting a book that doesn't exist.
        
        Expected:
            - Status code: 404 Not Found
        """
        self.client.force_authenticate(user=self.user)
        
        delete_url = reverse('book-delete', kwargs={'pk': 9999})
        response = self.client.delete(delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AuthorAPITestCase(APITestCase):
    """
    Test suite for Author serialization with nested books.
    """
    
    def setUp(self):
        """Set up test data for author tests."""
        self.author = Author.objects.create(name='Test Author')
        self.book1 = Book.objects.create(
            title='Book 1',
            publication_year=2020,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title='Book 2',
            publication_year=2021,
            author=self.author
        )
    
    def test_author_books_relationship(self):
        """
        Test that books are correctly related to authors.
        
        Expected:
            - Author has correct number of books
            - Books belong to correct author
        """
        self.assertEqual(self.author.books.count(), 2)
        self.assertIn(self.book1, self.author.books.all())
        self.assertIn(self.book2, self.author.books.all())
