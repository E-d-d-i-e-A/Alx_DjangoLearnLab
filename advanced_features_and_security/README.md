# Advanced Features and Security - Django Project

## Overview
This Django project demonstrates advanced features including custom user models, permissions, and groups for role-based access control.

## Features Implemented

### 1. Custom User Model
- **Model**: `CustomUser` extends Django's `AbstractUser`
- **Additional Fields**:
  - `date_of_birth`: DateField for user's birth date
  - `profile_photo`: ImageField for profile picture
- **Custom Manager**: `CustomUserManager` handles user creation with custom fields
- **Configuration**: `AUTH_USER_MODEL = 'bookshelf.CustomUser'` in settings.py

### 2. Custom Permissions
The `Book` model includes custom permissions for fine-grained access control:

- **can_view**: Permission to view books
- **can_create**: Permission to create new books
- **can_edit**: Permission to edit existing books
- **can_delete**: Permission to delete books

### 3. Permission-Protected Views
All book-related views are protected with `@permission_required` decorator:

- `book_list` - Requires `can_view` permission
- `book_create` - Requires `can_create` permission
- `book_edit` - Requires `can_edit` permission
- `book_delete` - Requires `can_delete` permission

## Groups and Roles

### Recommended Groups Setup

#### Viewers
**Permissions**: `can_view`
- Can browse and view books only

#### Editors
**Permissions**: `can_view`, `can_create`, `can_edit`
- Can view, create, and edit books

#### Admins
**Permissions**: `can_view`, `can_create`, `can_edit`, `can_delete`
- Full access to all book operations

## Setup Instructions

### 1. Install Dependencies
```bash
pip install Django Pillow
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Create Groups and Assign Permissions
1. Access Django admin: `http://127.0.0.1:8000/admin/`
2. Navigate to **Groups**
3. Create groups: Viewers, Editors, Admins
4. Assign permissions to each group:
   - **Viewers**: bookshelf | book | Can view book
   - **Editors**: Can view, Can create, Can edit
   - **Admins**: Can view, Can create, Can edit, Can delete

### 5. Assign Users to Groups
1. Go to **Users** in admin
2. Select a user
3. Add them to appropriate group(s)
4. Save

## Testing Permissions

### Test Case 1: Viewer Access
1. Create user: `viewer_test`
2. Add to group: `Viewers`
3. Login and attempt operations:
   - ✅ Can view book list
   - ❌ Cannot create books (403 Forbidden)
   - ❌ Cannot edit books (403 Forbidden)
   - ❌ Cannot delete books (403 Forbidden)

### Test Case 2: Editor Access
1. Create user: `editor_test`
2. Add to group: `Editors`
3. Login and attempt operations:
   - ✅ Can view books
   - ✅ Can create books
   - ✅ Can edit books
   - ❌ Cannot delete books (403 Forbidden)

### Test Case 3: Admin Access
1. Create user: `admin_test`
2. Add to group: `Admins`
3. Login and attempt operations:
   - ✅ Can view books
   - ✅ Can create books
   - ✅ Can edit books
   - ✅ Can delete books

## Project Structure
```
advanced_features_and_security/
├── README.md
└── LibraryProject/
    ├── manage.py
    ├── db.sqlite3
    ├── LibraryProject/
    │   ├── __init__.py
    │   ├── settings.py          # AUTH_USER_MODEL configured
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    └── bookshelf/
        ├── __init__.py
        ├── models.py             # CustomUser, CustomUserManager, Book
        ├── admin.py              # CustomUserAdmin, BookAdmin
        ├── views.py              # Permission-protected views
        ├── urls.py               # URL patterns
        ├── apps.py
        └── tests.py
```

## Models

### CustomUser
```python
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
```

### Book
```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    class Meta:
        permissions = [
            ('can_view', 'Can view book'),
            ('can_create', 'Can create book'),
            ('can_edit', 'Can edit book'),
            ('can_delete', 'Can delete book'),
        ]
```

## Security Features

1. **Permission-based Access Control**: All sensitive operations require specific permissions
2. **Group-based Role Management**: Users are assigned to groups with predefined permissions
3. **raise_exception=True**: Returns 403 Forbidden instead of redirecting unauthorized users
4. **Custom User Model**: Extensible user model for future enhancements

## API Endpoints

- `GET /books/` - List all books (requires `can_view`)
- `GET/POST /books/create/` - Create new book (requires `can_create`)
- `GET/POST /books/<id>/edit/` - Edit book (requires `can_edit`)
- `GET/POST /books/<id>/delete/` - Delete book (requires `can_delete`)

## Author
**Edidiong Aquatang**
- GitHub: [@E-d-d-i-e-A](https://github.com/E-d-d-i-e-A)
- LinkedIn: [linkedin.com/in/edidiong-aquatang-42aba82b7](https://linkedin.com/in/edidiong-aquatang-42aba82b7)
- Email: eaquatang@gmail.com
- Location: Port Harcourt, Rivers State, Nigeria
- Program: ALX Software Engineering - Back-End Track

## Technologies Used
- Django 5.1.3
- Python 3.x
- SQLite (Development)
- Pillow (Image handling)

## License
This project is part of the ALX Software Engineering program.
