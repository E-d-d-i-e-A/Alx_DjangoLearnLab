from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Post
from taggit.forms import TagWidget


class CustomUserCreationForm(UserCreationForm):
    """
    Extended user registration form with email field.
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
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.
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
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 3:
            raise forms.ValidationError('Comment must be at least 3 characters long.')
        return content


class PostForm(forms.ModelForm):
    """
    Form for creating and updating blog posts with tags.
    
    Includes title, content, and tags fields.
    The tags field uses TagWidget() for better tag input experience.
    """
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 10
            }),
            'tags': TagWidget(attrs={
                'class': 'form-control',
                'placeholder': 'Add tags separated by commas'
            }),
        }
        labels = {
            'title': 'Post Title',
            'content': 'Post Content',
            'tags': 'Tags'
        }
