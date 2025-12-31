# Django Blog Platform API

A full-featured blogging platform built with Django and Django REST Framework, featuring user authentication, post management, commenting, tagging, and search functionality.

## 🚀 Features

### Core Functionality
- ✅ User registration and authentication
- ✅ User profile management
- ✅ Create, read, update, and delete blog posts
- ✅ Comment on posts
- ✅ Tag posts with multiple categories
- ✅ Search posts by title, content, or tags
- ✅ Filter posts by specific tags

### Security & Permissions
- ✅ Session-based authentication
- ✅ Permission-based access control (only authors can edit/delete their content)
- ✅ CSRF protection on all forms
- ✅ Secure password hashing

### User Experience
- ✅ Responsive design for mobile and desktop
- ✅ Pagination (5 posts per page)
- ✅ Success/error messages for all actions
- ✅ Clean, modern UI with smooth animations

## 🛠️ Technologies Used

- **Backend:** Django 4.2
- **Database:** SQLite (development)
- **Authentication:** Django built-in authentication
- **Tagging:** django-taggit
- **Frontend:** HTML5, CSS3, JavaScript
- **Version Control:** Git & GitHub

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## 🔧 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/E-d-d-i-e-A/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/django_blog
```

### 2. Create virtual environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser (admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account.

### 6. Run the development server
```bash
python manage.py runserver
```

### 7. Access the application
- **Homepage:** http://127.0.0.1:8000/
- **Posts List:** http://127.0.0.1:8000/posts/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## 📖 Usage Guide

### For Users

1. **Register an Account**
   - Click "Register" in the navigation
   - Fill in username, email, and password
   - You'll be automatically logged in

2. **Create a Post**
   - Click "New Post" after logging in
   - Enter title, content, and tags (comma-separated)
   - Click "Create Post"

3. **Comment on Posts**
   - Open any post
   - Scroll to the comments section
   - Write your comment and click "Post Comment"

4. **Search for Posts**
   - Use the search bar in the navigation
   - Search by title, content, or tags

5. **Filter by Tags**
   - Click any tag badge to see all posts with that tag

### For Administrators

Access the admin panel at `/admin/` to:
- Manage all users
- Moderate posts and comments
- View system statistics

## 🗂️ Project Structure
```
django_blog/
├── django_blog/
│   ├── settings.py      # Project settings
│   ├── urls.py          # Main URL routing
│   └── wsgi.py
├── blog/
│   ├── models.py        # Database models (Post, Comment)
│   ├── views.py         # View logic
│   ├── forms.py         # Custom forms
│   ├── urls.py          # App URL routing
│   ├── admin.py         # Admin configuration
│   ├── templates/       # HTML templates
│   │   └── blog/
│   │       ├── base.html
│   │       ├── post_list.html
│   │       ├── post_detail.html
│   │       ├── post_form.html
│   │       └── ...
│   └── static/          # Static files
│       └── blog/
│           ├── css/
│           └── js/
├── manage.py
├── requirements.txt
└── README.md
```

## 🔌 API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/register/` | GET, POST | User registration | No |
| `/login/` | GET, POST | User login | No |
| `/logout/` | POST | User logout | Yes |
| `/profile/` | GET, POST | View/edit profile | Yes |
| `/posts/` | GET | List all posts | No |
| `/post/new/` | GET, POST | Create new post | Yes |
| `/post/<id>/` | GET | View single post | No |
| `/post/<id>/update/` | GET, POST | Update post | Yes (Author) |
| `/post/<id>/delete/` | GET, POST | Delete post | Yes (Author) |
| `/post/<id>/comments/new/` | POST | Add comment | Yes |
| `/comment/<id>/update/` | GET, POST | Update comment | Yes (Author) |
| `/comment/<id>/delete/` | GET, POST | Delete comment | Yes (Author) |
| `/search/` | GET | Search posts | No |
| `/tags/<slug>/` | GET | Filter by tag | No |

## 🧪 Testing

To test the application:

1. **Create test users** through registration
2. **Create test posts** with various tags
3. **Test permissions** by trying to edit others' posts (should fail)
4. **Test search** with different queries
5. **Test commenting** on posts
6. **Test tag filtering** by clicking tag badges

## 🐛 Known Issues

- No image upload for posts yet
- Search is case-insensitive but could be improved with full-text search
- No email notifications for comments

## 🚀 Future Enhancements

- [ ] Rich text editor for post content
- [ ] Image upload for posts
- [ ] User follow/unfollow system
- [ ] Email notifications
- [ ] Draft post functionality
- [ ] Post view counter
- [ ] Social media sharing

## 👨‍💻 Author

**Edidiong Aquatang**
- GitHub: [@E-d-d-i-e-A](https://github.com/E-d-d-i-e-A)
- Email: eaquatang@gmail.com
- Location: Lagos, Nigeria
- Program: ALX Software Engineering - Back-End Track

## 📝 License

This project is created as part of the ALX Software Engineering Capstone Project.

## 🙏 Acknowledgments

- ALX Africa for the opportunity and guidance
- Django and Django REST Framework documentation
- The open-source community

---

**Project Status:** ✅ Complete  
**Last Updated:** December 2025  
**ALX Capstone Project** - Week 5 Final Submission
```

---

## **Step 2: Create Your Loom Video Script**

Here's a script for your 5-minute demo video:

### **[0:00 - 0:30] Introduction**
```
"Hello! My name is Edidiong Aquatang, and I'm a back-end development student in the ALX Software Engineering program.

Today, I'm excited to present my capstone project - a Django Blog Platform API. This is a full-featured blogging application that I built from scratch over the past 5 weeks."
```

### **[0:30 - 1:00] Project Overview**
```
"This project solves the problem of needing a secure, scalable blogging platform where users can:
- Create and manage their own blog posts
- Comment on posts
- Organize content with tags
- Search for posts easily

The application features user authentication, permission-based access control, and advanced features like search and filtering."
```

### **[1:00 - 2:00] Demo - User Authentication**
```
"Let me show you how it works. First, I'll register a new user account...
[Show registration form, fill it out, submit]

As you can see, after registration, I'm automatically logged in and redirected to the posts page. Now I can see my profile link in the navigation."
```

### **[2:00 - 3:00] Demo - Creating a Post**
```
"Now let's create a blog post. I'll click 'New Post'...
[Show create post form]

I can add a title, write my content, and add tags separated by commas. Let me create a post about Python and Django...
[Fill form and submit]

Great! The post is created and I can see it displays with my username, the date, and the tags I added."
```

### **[3:00 - 3:45] Demo - Comments & Search**
```
"Now let me add a comment to this post...
[Add a comment]

Perfect! I can also search for posts using the search bar. Let me search for 'Python'...
[Use search, show results]

And I can filter posts by clicking on tags...
[Click a tag badge, show filtered results]"
```

### **[3:45 - 4:30] Demo - Permissions**
```
"One important feature is permissions. Only post authors can edit or delete their own posts. 

Let me show you - when I view my own post, I see Edit and Delete buttons...
[Show edit/delete buttons on own post]

But if I were to view someone else's post, those buttons wouldn't appear because I don't have permission to modify their content."
```

### **[4:30 - 5:00] Conclusion**
```
"So that's my Django Blog Platform! The key features are:
- User authentication and profiles
- Full CRUD for posts and comments
- Tagging system
- Search and filtering
- Permission-based access control

While there are still improvements I'd like to make - like adding image uploads and rich text editing - I'm proud of what I've built in 5 weeks.

Thank you for watching, and you can find the complete code on my GitHub repository. Thank you!"
