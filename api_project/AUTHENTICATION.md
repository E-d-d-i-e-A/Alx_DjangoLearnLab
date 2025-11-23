# Authentication and Permissions Documentation

## Overview
This API uses Token Authentication to secure endpoints. Users must obtain a token and include it in their requests to access protected resources.

## Authentication Method

### Token Authentication
- **Type:** Token-based authentication
- **Header:** `Authorization: Token <your-token-here>`
- **Security:** Tokens are stored securely in the database

## How Authentication Works

### 1. User Registration
First, create a user account (via Django admin or custom registration endpoint):
```bash
# Create superuser
python manage.py createsuperuser

# Or create regular user via Django shell
python manage.py shell
```
```python
from django.contrib.auth.models import User

user = User.objects.create_user(
    username='testuser',
    password='testpass123',
    email='test@example.com'
)
```

### 2. Obtain Authentication Token
**Endpoint:** `POST /api/auth/token/`

**Request Body:**
```json
{
    "username": "testuser",
    "password": "testpass123"
}
```

**Example cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

**Response:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### 3. Use Token in Requests
Include the token in the `Authorization` header for all subsequent requests:

**Header Format:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## API Endpoints and Permissions

### Public Endpoints (No Authentication Required)
- `POST /api/auth/token/` - Obtain authentication token

### Protected Endpoints (Authentication Required)

All endpoints require authentication token:

| Endpoint | Method | Permission | Description |
|----------|--------|------------|-------------|
| `/api/books/` | GET | IsAuthenticated | List all books |
| `/api/books_all/` | GET | IsAuthenticated | List all books (ViewSet) |
| `/api/books_all/` | POST | IsAuthenticated | Create new book |
| `/api/books_all/<id>/` | GET | IsAuthenticated | Retrieve specific book |
| `/api/books_all/<id>/` | PUT | IsAuthenticated | Update book (full) |
| `/api/books_all/<id>/` | PATCH | IsAuthenticated | Update book (partial) |
| `/api/books_all/<id>/` | DELETE | IsAuthenticated | Delete book |

## Permission Classes

### IsAuthenticated
**Description:** Requires user to be authenticated

**Usage:** Applied to all Book API endpoints

**Behavior:**
- ✅ Authenticated users: Full access
- ❌ Unauthenticated users: 401 Unauthorized

### Future Permissions (Examples)
You can add more granular permissions:

#### IsAdminUser
```python
from rest_framework.permissions import IsAdminUser

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]  # Only admin users
```

#### Custom Permissions
```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
```

## Testing Authentication

### Test 1: Access Without Token (Should Fail)
```bash
curl http://127.0.0.1:8000/api/books/
```

**Expected Response:**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

**Status Code:** 401 Unauthorized

---

### Test 2: Obtain Token
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

**Expected Response:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**Status Code:** 200 OK

---

### Test 3: Access With Token (Should Succeed)
```bash
curl http://127.0.0.1:8000/api/books/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Expected Response:**
```json
[
    {
        "id": 1,
        "title": "1984",
        "author": "George Orwell"
    }
]
```

**Status Code:** 200 OK

---

### Test 4: Create Book With Token
```bash
curl -X POST http://127.0.0.1:8000/api/books_all/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Book", "author": "New Author"}'
```

**Expected Response:**
```json
{
    "id": 2,
    "title": "New Book",
    "author": "New Author"
}
```

**Status Code:** 201 Created

---

### Test 5: Invalid Token (Should Fail)
```bash
curl http://127.0.0.1:8000/api/books/ \
  -H "Authorization: Token invalid-token-123"
```

**Expected Response:**
```json
{
    "detail": "Invalid token."
}
```

**Status Code:** 401 Unauthorized

---

## Using Postman

### Step 1: Obtain Token
1. Method: POST
2. URL: `http://127.0.0.1:8000/api/auth/token/`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
    "username": "testuser",
    "password": "testpass123"
}
```
5. Click "Send"
6. Copy the token from response

### Step 2: Use Token in Requests
1. Method: GET (or POST, PUT, DELETE)
2. URL: `http://127.0.0.1:8000/api/books/`
3. Headers:
   - Key: `Authorization`
   - Value: `Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`
4. Click "Send"

---

## Using Python requests Library
```python
import requests

BASE_URL = 'http://127.0.0.1:8000/api'

# Step 1: Obtain token
response = requests.post(
    f'{BASE_URL}/auth/token/',
    json={'username': 'testuser', 'password': 'testpass123'}
)
token = response.json()['token']
print(f'Token: {token}')

# Step 2: Create headers with token
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}

# Step 3: Make authenticated requests
# List books
response = requests.get(f'{BASE_URL}/books/', headers=headers)
print(response.json())

# Create book
new_book = {'title': 'Test Book', 'author': 'Test Author'}
response = requests.post(f'{BASE_URL}/books_all/', json=new_book, headers=headers)
print(response.json())

# Get specific book
response = requests.get(f'{BASE_URL}/books_all/1/', headers=headers)
print(response.json())
```

---

## Managing Tokens

### Generate Token for Existing User (Django Shell)
```bash
python manage.py shell
```
```python
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

user = User.objects.get(username='testuser')
token, created = Token.objects.get_or_create(user=user)
print(f'Token for {user.username}: {token.key}')
```

### Regenerate Token (Delete and Create New)
```python
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

user = User.objects.get(username='testuser')
Token.objects.filter(user=user).delete()
token = Token.objects.create(user=user)
print(f'New token: {token.key}')
```

### View All Tokens (Admin)
```python
from rest_framework.authtoken.models import Token

for token in Token.objects.all():
    print(f'{token.user.username}: {token.key}')
```

---

## Security Best Practices

### 1. Token Storage
- ✅ Store tokens securely (environment variables, secure storage)
- ❌ Never commit tokens to version control
- ❌ Don't expose tokens in URLs

### 2. Token Transmission
- ✅ Always use HTTPS in production
- ✅ Send tokens in Authorization header
- ❌ Don't send tokens in URL parameters

### 3. Token Management
- ✅ Regenerate tokens if compromised
- ✅ Implement token expiration (use JWT for this)
- ✅ Delete tokens on logout

### 4. User Management
- ✅ Use strong passwords
- ✅ Implement rate limiting on token endpoint
- ✅ Log authentication attempts

---

## Error Responses

### 401 Unauthorized
**Cause:** Missing or invalid token

**Response:**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

**Solution:** Include valid token in Authorization header

---

### 403 Forbidden
**Cause:** User doesn't have permission

**Response:**
```json
{
    "detail": "You do not have permission to perform this action."
}
```

**Solution:** Check user permissions or use different account

---

### 400 Bad Request (Token Endpoint)
**Cause:** Invalid credentials

**Response:**
```json
{
    "non_field_errors": [
        "Unable to log in with provided credentials."
    ]
}
```

**Solution:** Check username and password

---

## Configuration Summary

### settings.py
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',  # Required for token auth
    ...
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### views.py
```python
from rest_framework.permissions import IsAuthenticated

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    ...
```

### urls.py
```python
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    ...
]
```

---

## Troubleshooting

### Issue: "No module named 'rest_framework.authtoken'"
**Solution:** Add to INSTALLED_APPS and run migrations
```bash
python manage.py migrate
```

### Issue: Token endpoint returns 405 Method Not Allowed
**Solution:** Use POST method, not GET

### Issue: Token not working after migration
**Solution:** Run migrations for authtoken app
```bash
python manage.py migrate rest_framework.authtoken
```

---

## Next Steps

1. ✅ Token Authentication - COMPLETED
2. 🔄 Add JWT Authentication (more secure, includes expiration)
3. 🔄 Implement refresh tokens
4. 🔄 Add OAuth2 authentication
5. 🔄 Implement role-based permissions
6. 🔄 Add API rate limiting

---

## Author
**Edidiong Aquatang**
- GitHub: [@E-d-d-i-e-A](https://github.com/E-d-d-i-e-A)
- ALX Software Engineering Program

---

**Last Updated:** November 2025
