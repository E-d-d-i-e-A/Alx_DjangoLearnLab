# Social Media API

A Django REST Framework-based social media API with user authentication and profile management.

## Project Setup

### Installation

1. Install required packages:
```bash
pip install django djangorestframework
```

2. Create the Django project:
```bash
django-admin startproject social_media_api
cd social_media_api
python manage.py startapp accounts
```

### Configuration

1. Update `settings.py`:
   - Add `'rest_framework'`, `'rest_framework.authtoken'`, and `'accounts'` to `INSTALLED_APPS`
   - Set `AUTH_USER_MODEL = 'accounts.CustomUser'`
   - Configure REST Framework authentication

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Start the development server:
```bash
python manage.py runserver
```

## User Model

The custom user model extends Django's `AbstractUser` with additional fields:

- **bio**: Text field for user biography (max 500 characters)
- **profile_picture**: Image field for user profile pictures
- **followers**: ManyToMany relationship for following/follower system (non-symmetrical)

## API Endpoints

### 1. User Registration
- **URL**: `/api/accounts/register/`
- **Method**: POST
- **Authentication**: Not required
- **Request Body**:
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123",
    "bio": "This is my bio",
    "profile_picture": null
}
```
- **Response**: Returns user data and authentication token

### 2. User Login
- **URL**: `/api/accounts/login/`
- **Method**: POST
- **Authentication**: Not required
- **Request Body**:
```json
{
    "username": "testuser",
    "password": "securepassword123"
}
```
- **Response**: Returns authentication token and user profile

### 3. User Profile
- **URL**: `/api/accounts/profile/`
- **Method**: GET, PUT, PATCH
- **Authentication**: Required (Token)
- **Headers**:
```
Authorization: Token <your-token-here>
```
- **Response**: Returns or updates authenticated user's profile

## Authentication

This API uses Token Authentication. After registration or login, include the token in the Authorization header:

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## Testing with Postman

1. **Register a new user**:
   - POST to `http://localhost:8000/api/accounts/register/`
   - Include username, email, and password in body
   - Save the returned token

2. **Login**:
   - POST to `http://localhost:8000/api/accounts/login/`
   - Include username and password
   - Save the returned token

3. **Access Profile**:
   - GET to `http://localhost:8000/api/accounts/profile/`
   - Add header: `Authorization: Token <your-token>`

## Project Structure

```
social_media_api/
├── social_media_api/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── accounts/
│   ├── models.py          # Custom User model
│   ├── serializers.py     # API serializers
│   ├── views.py           # API views
│   ├── urls.py            # App URL patterns
│   └── ...
└── manage.py
```

## Repository

- **GitHub repository**: Alx_DjangoLearnLab
- **Directory**: social_media_api