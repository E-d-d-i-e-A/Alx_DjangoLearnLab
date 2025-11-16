INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'relationship_app',  # ← Make sure this is here!
]

# Login redirect URL
LOGIN_REDIRECT_URL = 'list_books'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'
