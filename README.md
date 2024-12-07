# Blog Posting Backend - Django

Welcome to the **Blog Posting Backend** project! This repository is the backend implementation of a blog posting application built using **Django**. It provides robust features for creating, managing, and interacting with blogs, including user authentication, blog CRUD operations, comment functionality, and a like system.

---

## Features

- **User Management**
  - User registration, login, and profile management.
  - Authentication with JSON Web Tokens (JWT).
- **Blog Management**
  - Create, read, update, and delete (CRUD) operations for blogs.
  - Each blog includes a title, content, author, and timestamp.
- **Commenting System**
  - Users can comment on blogs.
  - Edit and delete own comments.
- **Like System**
  - Users can like or unlike blogs.
  - Tracks like count for each blog.
- **Pagination**
  - Efficiently handles a large number of blogs with pagination.

---

## Installation

### Prerequisites
- **Python 3.8+**
- **Django 4.x**
- **PostgreSQL** (or other databases supported by Django)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/blog-posting-backend.git
   cd blog-posting-backend



### Project Structure 


**blog-posting-backend/
├── accounts/                   # User and blog-related functionality
│   ├── migrations/             # Database migrations
│   ├── models.py               # Django models for User, Blog, and Comment
│   ├── serializers.py          # Serializers for API responses
│   ├── views.py                # Views for handling requests
│   ├── urls.py                 # URL routing for the accounts app
│   ├── tests.py                # Unit tests for the accounts app
├── blog_posting_backend/       # Main project settings
│   ├── __init__.py
│   ├── settings.py             # Settings for the Django project
│   ├── urls.py                 # Global URL routing
│   ├── wsgi.py                 # WSGI configuration
│   ├── asgi.py                 # ASGI configuration
├── manage.py                   # Django management script
├── requirements.txt            # List of required dependencies
├── .env                        # Environment variables for sensitive data
└── README.md                   # Project documentation
**
