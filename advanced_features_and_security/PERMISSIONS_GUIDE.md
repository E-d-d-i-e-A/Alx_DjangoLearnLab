# Permissions and Groups Setup Guide

## Overview
This application implements a role-based access control system using Django's built-in permissions and groups functionality.

## Custom Permissions

### Book Model Permissions
The `Book` model has the following custom permissions:

1. **can_view** - Allows viewing books
2. **can_create** - Allows creating new books
3. **can_edit** - Allows editing existing books
4. **can_delete** - Allows deleting books

These permissions are defined in `bookshelf/models.py`:
```python
class Meta:
    permissions = [
        ('can_view', 'Can view book'),
        ('can_create', 'Can create book'),
        ('can_edit', 'Can edit book'),
        ('can_delete', 'Can delete book'),
    ]
```

## Groups Configuration

### Recommended Groups Setup

#### 1. Viewers Group
**Permissions:**
- `can_view` - Can view books

**Purpose:** Users who can only browse and view books

#### 2. Editors Group
**Permissions:**
- `can_view` - Can view books
- `can_create` - Can create new books
- `can_edit` - Can edit existing books

**Purpose:** Users who can manage book content

#### 3. Admins Group
**Permissions:**
- `can_view` - Can view books
- `can_create` - Can create new books
- `can_edit` - Can edit existing books
- `can_delete` - Can delete books

**Purpose:** Full access to all book operations

## Setting Up Groups (Django Admin)

### Step 1: Access Django Admin
1. Run the server: `python manage.py runserver`
2. Navigate to: `http://127.0.0.1:8000/admin/`
3. Login with superuser credentials

### Step 2: Create Groups
1. Click on **"Groups"** under Authentication and Authorization
2. Click **"Add Group"**
3. Enter group name (e.g., "Viewers")
4. Select permissions from the "Available permissions" list:
   - Find `bookshelf | book | Can view book`
   - Move it to "Chosen permissions"
5. Click **"Save"**

Repeat for "Editors" and "Admins" groups with their respective permissions.

### Step 3: Assign Users to Groups
1. Go to **"Users"** in Django admin
2. Select a user
3. Scroll to "Groups" section
4. Select the appropriate group(s)
5. Click **"Save"**

## Permission Enforcement in Views

All views that handle book operations are protected with the `@permission_required` decorator:

### Example: View Books
```python
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
```

### Example: Create Book
```python
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    # Create book logic
```

### Example: Edit Book
```python
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    # Edit book logic
```

### Example: Delete Book
```python
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    # Delete book logic
```

## Testing Permissions

### Test Scenario 1: Viewer User
1. Create a user: `viewer_user`
2. Add to group: `Viewers`
3. Login as `viewer_user`
4. **Expected Results:**
   - ✅ Can access book list
   - ❌ Cannot create books (403 Forbidden)
   - ❌ Cannot edit books (403 Forbidden)
   - ❌ Cannot delete books (403 Forbidden)

### Test Scenario 2: Editor User
1. Create a user: `editor_user`
2. Add to group: `Editors`
3. Login as `editor_user`
4. **Expected Results:**
   - ✅ Can access book list
   - ✅ Can create books
   - ✅ Can edit books
   - ❌ Cannot delete books (403 Forbidden)

### Test Scenario 3: Admin User
1. Create a user: `admin_user`
2. Add to group: `Admins`
3. Login as `admin_user`
4. **Expected Results:**
   - ✅ Can access book list
   - ✅ Can create books
   - ✅ Can edit books
   - ✅ Can delete books

## Permission Format

Django permissions follow this format:
```
app_label.permission_codename
```

For our Book model:
- `bookshelf.can_view`
- `bookshelf.can_create`
- `bookshelf.can_edit`
- `bookshelf.can_delete`

## Security Notes

1. **raise_exception=True**: Returns 403 Forbidden instead of redirecting to login
2. **Permission checks**: Always performed before any action is executed
3. **Group membership**: Users can belong to multiple groups and inherit all permissions
4. **Superusers**: Automatically have all permissions, regardless of group membership

## Troubleshooting

### Permission not found
- Run migrations: `python manage.py migrate`
- Permissions are created automatically during migration

### User has permission but still denied
- Check if user is active: `user.is_active = True`
- Verify group membership in Django admin
- Clear sessions and re-login

### 403 Forbidden Error
- User doesn't have required permission
- Assign user to appropriate group or add permission directly to user

## Code Locations

- **Models with permissions**: `bookshelf/models.py`
- **Views with permission checks**: `bookshelf/views.py`
- **Admin configuration**: `bookshelf/admin.py`
- **URL patterns**: `bookshelf/urls.py` (if created)

## Author
**Edidiong Aquatang**
- GitHub: [@E-d-d-i-e-A](https://github.com/E-d-d-i-e-A)
- ALX Software Engineering Program
