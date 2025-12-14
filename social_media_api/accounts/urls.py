from django.urls import path
from .views import (
    UserRegistrationView, 
    UserLoginView, 
    UserProfileView,
    follow_user,
    unfollow_user,
    list_followers,
    list_following
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow-user'),
    path('followers/', list_followers, name='list-followers'),
    path('following/', list_following, name='list-following'),
]