# Library Management System API using Django Rest
<img src="https://github.com/user-attachments/assets/684e2803-1d37-49b7-9233-2da694912b21" alt="Custom Icon" width="1050" height="300">

![GitHub Language Count](https://img.shields.io/github/languages/count/saifee3/library-management-system?style=flat-square&color=green)
![GitHub License](https://img.shields.io/github/license/saifee3/library-management-system?style=flat-square&color=orange)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square)
![Django Version](https://img.shields.io/badge/django-4.2%2B-blue?style=flat-square)
![Build Status](https://img.shields.io/badge/build-passing-success?style=flat-square)


## Project Overview

Welcome to the 📚 Library Management System API 📚, a robust and scalable solution built with Django for managing library operations. This API enables efficient management of authors, books, and borrowers while implementing role-based access control to ensure data security and integrity.

## Key Features

- 🛡️ **Role-Based Access Control**: Admin, staff, and regular user roles with appropriate permissions
- 📖 **Book Management**: CRUD operations for books with ISBN validation
- ✒️ **Author Management**: CRUD operations for authors
- 🤝 **Borrowing System**: Users can borrow and return books with borrowing limits
- 🔍 **Search & Filtering**: Powerful search capabilities for books
- ⚡ **Caching**: Optimized performance with caching for frequently accessed data
- ⏱️ **Automated Updates**: Signals for automatic updates when books are borrowed

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Database system (SQLite for development)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/library-management-system.git
   cd library-management-system
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## API Documentation

### Authentication

- **Register User**
  ```http
  POST /api/user/register/
  ```
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

- **Login**
  ```http
  POST /api/user/login/
  ```
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

### Authors

- **Create Author** (Staff Only)
  ```http
  POST /api/authors/
  ```
  ```json
  {
    "name": "string",
    "bio": "string"
  }
  ```

- **Get Author Details**
  ```http
  GET /api/authors/<id>/
  ```

- **Update Author** (Staff Only)
  ```http
  PUT /api/authors/<id>/
  ```

- **Delete Author** (Staff Only)
  ```http
  DELETE /api/authors/<id>/
  ```

### Books

- **Create Book** (Staff Only)
  ```http
  POST /api/books/
  ```
  ```json
  {
    "title": "string",
    "isbn": "string",
    "author_id": "integer",
    "published_date": "YYYY-MM-DD"
  }
  ```

- **Get Book Details**
  ```http
  GET /api/books/<id>/
  ```

- **Update Book** (Staff Only)
  ```http
  PUT /api/books/<id>/
  ```

- **Delete Book** (Staff Only)
  ```http
  DELETE /api/books/<id>/
  ```

### Borrowing Books

- **Borrow Book**
  ```http
  POST /api/borrowing/borrow/
  ```
  ```json
  {
    "book_id": "integer"
  }
  ```

- **Return Book**
  ```http
  POST /api/borrowing/return/
  ```
  ```json
  {
    "book_id": "integer"
  }
  ```

### Library Statistics & Search

- **Search Books**
  ```http
  GET /api/library/search/?title=string&author=string&available=true
  ```

- **Library Statistics** (Staff Only)
  ```http
  GET /api/library/statistics/
  ```

- **Active Borrowers** (Staff Only)
  ```http
  GET /api/library/borrowers/
  ```

## Project Structure

```
library-management-system/
├── Library/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── signals.py
│   ├── tests/
│   ├── urls.py
│   └── views.py
├── requirements.txt
├── manage.py
└── README.md
```


## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits
- **[Django](https://www.djangoproject.com/)** - The web framework used to build this API.  
- **[Django REST Framework](https://www.django-rest-framework.org/)** - The toolkit for building RESTful APIs.  
- **[Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)** - Used for secure authentication.  
- **[SQLite](https://www.sqlite.org/)** - The default database for local development.  
- **[Real Python](https://realpython.com/django-rest-framework-quick-start/)** - Banner image sourced from their tutorial.  

