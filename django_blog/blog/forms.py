from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment


class CustomUserCreationForm(UserCreationForm):
    """
    Extended user registration form with email field.
    
    Extends Django's built-in UserCreationForm to include email field
    as a required field during registration.
    
    Fields:
        username: Username for login
        email: Email address (required)
        password1: Password
        password2: Password confirmation
    """
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
    
    def save(self, commit=True):
        """
        Save the user with email.
        
        Ensures the email is saved to the user model.
        """
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.
    
    Allows users to update their username and email address.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }


class CommentForm(forms.ModelForm):
    """
    Form for creating and updating comments.
    
    Allows users to write comments on blog posts.
    Includes validation for content field.
    
    Fields:
        content: Text content of the comment
    """
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4
            })
        }
        labels = {
            'content': 'Your Comment'
        }
    
    def clean_content(self):
        """
        Validate comment content.
        
        Ensures comment is not empty or too short.
        
        Returns:
            str: Cleaned content
            
        Raises:
            ValidationError: If content is too short
        """
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 3:
            raise forms.ValidationError('Comment must be at least 3 characters long.')
        return content
