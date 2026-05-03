# 📚 LMS Backend API

A production-ready **Learning Management System (LMS)** REST API built with Django REST Framework. Features JWT authentication, role-based permissions, email verification, automated testing, and is fully deployed on Railway.

🔗 **Live API:** `https://web-production-a16182.up.railway.app`

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [API Endpoints](#-api-endpoints)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Running Tests](#-running-tests)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)

---

## ✨ Features

- 🔐 **JWT Authentication** — Secure login with access and refresh tokens
- ✅ **Email Verification** — Users must verify email before logging in (powered by django-allauth)
- 👥 **Role-Based Permissions** — Different access levels for students, instructors, and admins
- 📄 **Pagination** — All list endpoints return paginated results
- 🔍 **Filtering & Search** — Filter courses by status, search by title/description, sort by price or date
- 🚦 **Throttling** — Rate limiting to protect against abuse
- ⚡ **Performance Optimized** — `select_related` and `prefetch_related` to prevent N+1 queries
- 🧪 **Automated Tests** — 13 tests covering authentication, permissions, and business logic
- 🌐 **Deployed** — Live on Railway with PostgreSQL database

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Programming language |
| Django 5.2 | Web framework |
| Django REST Framework | API toolkit |
| PostgreSQL | Production database |
| Simple JWT | JWT authentication |
| django-allauth | Email verification & auth |
| dj-rest-auth | REST auth endpoints |
| Whitenoise | Static file serving |
| Gunicorn | Production web server |
| Railway | Cloud deployment |
| pytest | Automated testing |
| django-filter | Filtering & search |

---

## 📡 API Endpoints

### Authentication
```
POST   /api/accounts/registration/              Register new user (sends verification email)
POST   /api/accounts/registration/verify-email/ Verify email with key from email
POST   /api/accounts/login/                     Login and get JWT tokens
POST   /api/accounts/logout/                    Logout
POST   /api/accounts/token/refresh/             Refresh access token
POST   /api/accounts/password/reset/            Request password reset email
POST   /api/accounts/password/reset/confirm/    Confirm password reset
GET    /api/accounts/user/                      Get current user details
PUT    /api/accounts/user/                      Update current user details
```

### Courses
```
GET    /api/courses/                            List all courses (public)
POST   /api/courses/                            Create course (admin only)
GET    /api/courses/{id}/                       Get course detail (public)
PUT    /api/courses/{id}/                       Update course (admin only)
DELETE /api/courses/{id}/                       Delete course (admin only)
```

### Lessons
```
GET    /api/courses/{id}/lessons/               List lessons for a course
POST   /api/courses/{id}/lessons/               Create lesson (course instructor only)
GET    /api/courses/{id}/lessons/{id}/          Get lesson detail
PUT    /api/courses/{id}/lessons/{id}/          Update lesson (course instructor only)
DELETE /api/courses/{id}/lessons/{id}/          Delete lesson (course instructor only)
```

### Enrollments
```
GET    /api/courses/{id}/enrollments/           List enrollments (admin sees all, students see own)
POST   /api/courses/{id}/enrollments/           Enroll in course (authenticated users)
GET    /api/my-enrollments/                     List all courses student is enrolled in
```

### Instructors
```
GET    /api/instructors/                        List all course instructors
POST   /api/instructors/                        Assign instructor to course (admin only)
GET    /api/instructors/{id}/                   Get instructor detail
PUT    /api/instructors/{id}/                   Update instructor (admin only)
DELETE /api/instructors/{id}/                   Remove instructor (admin only)
```

---

## 🔑 Permission System

| Action | Student | Instructor | Admin |
|--------|---------|------------|-------|
| View courses | ✅ | ✅ | ✅ |
| Create/edit/delete course | ❌ | ❌ | ✅ |
| View lessons | ✅ | ✅ | ✅ |
| Create/edit/delete lesson | ❌ | ✅ (own course only) | ✅ |
| Enroll in course | ✅ | ✅ | ✅ |
| View all enrollments | ❌ (own only) | ❌ | ✅ |

---

## 🔍 Filtering & Search

```
# Search courses
GET /api/courses/?search=django

# Filter by status
GET /api/courses/?published=true

# Sort by price
GET /api/courses/?ordering=price
GET /api/courses/?ordering=-price

# Sort by date
GET /api/courses/?ordering=-created_at

# Combine filters
GET /api/courses/?search=python&published=true&ordering=-price

# Pagination
GET /api/courses/?page=2
GET /api/courses/?page_size=5
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL
- Git

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/lms-backend.git
cd lms-backend
```

**2. Create and activate virtual environment**
```bash
python -m venv env
# Windows
env\Scripts\activate
# Mac/Linux
source env/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create `.env` file** (see Environment Variables section below)

**5. Run migrations**
```bash
python manage.py migrate
```

**6. Create superuser**
```bash
python manage.py createsuperuser
```

**7. Run the development server**
```bash
python manage.py runserver
```

Your API is now running at `http://127.0.0.1:8000`

---

## 🔐 Environment Variables

Create a `.env` file in the root directory with the following:

```env
# Django
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

# Email (Gmail)
EMAIL_HOST_USER=your_gmail@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
```

### Getting Gmail App Password

1. Go to [Google Account](https://myaccount.google.com) → Security
2. Enable 2-Step Verification
3. Search for **App Passwords**
4. Generate a password for Mail → Windows Computer
5. Use the generated 16-character password as `EMAIL_HOST_PASSWORD`

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest Courses/test_courses.py

# Run specific test class
pytest Courses/test_courses.py::TestCourseEndpoints

# Run specific test
pytest Courses/test_courses.py::TestCourseEndpoints::test_admin_can_create_course
```

### Test Coverage

```
TestCourseEndpoints (7 tests)
  ✅ Anyone can list courses
  ✅ Anyone can retrieve a single course
  ✅ Admin can create a course
  ✅ Student cannot create a course
  ✅ Unauthenticated user cannot create a course
  ✅ Admin can delete a course
  ✅ Student cannot delete a course

TestEnrollmentEndpoints (3 tests)
  ✅ Student can enroll in a course
  ✅ Student cannot enroll twice
  ✅ Student only sees their own enrollments

TestAuthentication (3 tests)
  ✅ Valid user gets access and refresh tokens
  ✅ Wrong password returns 401
  ✅ Protected endpoint requires token
```

---

## 📁 Project Structure

```
lms-backend/
├── backend/                  # Main project folder
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── celery.py             # Celery configuration
├── accounts/                 # Authentication app
│   ├── models.py             # CustomUser model
│   ├── views.py              # Auth views
│   ├── serializers.py        # Auth serializers
│   └── adapters.py           # Allauth custom adapter
├── Courses/                  # Courses app
│   ├── models.py             # Course, Lesson, Enrollment, CourseInstructor
│   ├── views.py              # ViewSets
│   ├── Serializers.py        # Serializers with validation
│   ├── permissions.py        # Custom permission classes
│   ├── exceptions.py         # Custom exception handler
│   ├── pagination.py         # Custom pagination
│   └── test_courses.py       # Automated tests
├── manage.py
├── requirements.txt
├── Procfile                  # Railway deployment
├── runtime.txt               # Python version for Railway
└── .env                      # Environment variables (not committed)
```

---

## 🌐 Deployment

This project is deployed on **Railway** with:

- **Web service** — Django app running with Gunicorn
- **PostgreSQL** — Managed database provided by Railway
- **Automatic deploys** — Every push to `main` branch triggers a new deployment
- **HTTPS** — SSL certificate provided automatically by Railway

### Deploy your own instance

1. Fork this repository
2. Create a new project on [Railway](https://railway.app)
3. Connect your GitHub repository
4. Add a PostgreSQL plugin
5. Set the environment variables in Railway's Variables tab
6. Set the start command:
   ```
   python manage.py migrate && python manage.py collectstatic --noinput && gunicorn backend.wsgi --log-file -
   ```
7. Railway deploys automatically!

---

## 📬 API Response Format

### Success Response
```json
{
    "success": true,
    "pagination": {
        "total": 10,
        "page_size": 10,
        "next": null,
        "previous": null
    },
    "results": []
}
```

### Error Response
```json
{
    "success": false,
    "error": {
        "code": "validation_error",
        "message": "Invalid input.",
        "details": {
            "title": ["Title must be at least 5 characters."]
        }
    }
}
```

---

## 👨‍💻 Author

**Pujan Pandey**

- GitHub: [@yourusername](https://github.com/PujanPandey07)


---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
