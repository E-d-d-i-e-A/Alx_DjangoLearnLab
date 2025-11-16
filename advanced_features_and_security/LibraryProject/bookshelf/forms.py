from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    """
    Secure form for creating and editing books.
    Uses Django's built-in form validation and sanitization.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter year'}),
        }
    
    def clean_title(self):
        """
        Validate and sanitize book title.
        Prevents XSS by escaping special characters.
        """
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError('Title is required.')
        # Django automatically escapes special characters
        return title.strip()
    
    def clean_author(self):
        """
        Validate and sanitize author name.
        """
        author = self.cleaned_data.get('author')
        if not author:
            raise forms.ValidationError('Author is required.')
        return author.strip()
    
    def clean_publication_year(self):
        """
        Validate publication year.
        """
        year = self.cleaned_data.get('publication_year')
        if year and (year < 1000 or year > 9999):
            raise forms.ValidationError('Please enter a valid 4-digit year.')
        return year


class ExampleForm(forms.Form):
    """
    Example form demonstrating secure input handling.
    """
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=True
    )
    
    def clean_name(self):
        """Sanitize name input"""
        name = self.cleaned_data.get('name')
        return name.strip()
    
    def clean_message(self):
        """Sanitize message input"""
        message = self.cleaned_data.get('message')
        return message.strip()
