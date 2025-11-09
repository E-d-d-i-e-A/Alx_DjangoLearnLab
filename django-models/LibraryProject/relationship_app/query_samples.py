from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    """
    Query all books by a specific author.
    Uses ForeignKey relationship (Author -> Book).
    """
    try:
        # Get the author by name
        author = Author.objects.get(name=author_name)
        
        # Query all books by this author using objects.filter()
        books = Book.objects.filter(author=author)
        
        print(f"\nBooks by {author_name}:")
        for book in books:
            print(f"  - {book.title}")
        
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return None


def list_books_in_library(library_name):
    """
    List all books in a library.
    Uses ManyToManyField relationship (Library -> Book).
    """
    try:
        # Get the library by name
        library = Library.objects.get(name=library_name)
        
        # Query all books in this library using the ManyToMany field
        books = library.books.all()
        
        print(f"\nBooks in {library_name}:")
        for book in books:
            print(f"  - {book.title}")
        
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None


def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library.
    Uses OneToOneField relationship (Librarian -> Library).
    """
    try:
        # Get the library by name
        library = Library.objects.get(name=library_name)
        
        # Retrieve the librarian using Librarian.objects.get()
        librarian = Librarian.objects.get(library=library)
        
        print(f"\nLibrarian for {library_name}:")
        print(f"  - {librarian.name}")
        
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library_name}.")
        return None


# Example usage (uncomment to test in Django shell)
# if __name__ == "__main__":
#     # Query books by author
#     query_books_by_author("George Orwell")
#     
#     # List books in a library
#     list_books_in_library("Central Library")
#     
#
