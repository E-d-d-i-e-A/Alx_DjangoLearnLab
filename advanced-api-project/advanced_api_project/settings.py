Find the INSTALLED_APPS section and make sure it looks like this:
INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'rest_framework',
'django_filters',
'api',
]
Then ADD this at the bottom of the file:
REST_FRAMEWORK = {
'DEFAULT_FILTER_BACKENDS': [
'django_filters.rest_framework.DjangoFilterBackend',
'rest_framework.filters.SearchFilter',
'rest_framework.filters.OrderingFilter',
],
}
