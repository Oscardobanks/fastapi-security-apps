# FastAPI Security Learning Journey

A comprehensive collection of 4 FastAPI projects demonstrating progressive authentication and security concepts for beginners. Each project builds upon security knowledge from basic HTTP authentication to advanced JWT token management.

## 🎯 Repository Purpose

This repository contains hands-on FastAPI projects designed to teach:

- **Authentication methods** (HTTP Basic, JWT tokens)
- **Authorization patterns** (role-based access, user isolation)
- **Security best practices** (password hashing, token management)
- **API design principles** (RESTful endpoints, proper error handling)
- **Data persistence** (JSON file storage with error handling)

## 📚 Projects Overview

| Project                                 | Authentication Method            | Key Concepts                                    |
| --------------------------------------- | -------------------------------- | ----------------------------------------------- |
| [Student Portal](#-student-portal-auth) | HTTP Basic Auth                  | Basic authentication, password hashing          |
| [Shopping Cart](#-shopping-cart-RBAC)   | HTTP Basic Auth + Roles          | Role-based access control, dependency injection |
| [Job Tracker](#-job-tracker)            | HTTP Basic Auth + User Isolation | User data separation, filtered responses        |
| [Notes API](#-notes-api-jwt)            | JWT Bearer Tokens                | Token-based auth, stateless sessions            |

## 🚀 Quick Start

### Prerequisites

```bash
python 3.7+
pip install fastapi uvicorn
```

### Run Any Project

```bash
# Clone the repository
git clone https://github.com/yourusername/fastapi-security-apps.git
cd fastapi-security-apps

# Navigate to any project folder
cd student-portal-auth  # or any other project

# Install dependencies (for JWT project)
pip install -r requirements.txt  # if requirements.txt exists

# Run the application
python main.py

# Or use uvicorn directly
uvicorn main:app --reload
```

### Access Interactive Documentation

Visit `http://localhost:8000/docs` for each project's Swagger UI.

## 📁 Project Structure

```
fastapi-security-apps/
├── README.md                           # This file
├── .gitignore                         # Git ignore patterns
├── student-portal-auth/         # Task 1: HTTP Basic Auth
│   ├── main.py
│   ├── README.md
│   └── students.json (auto-generated)
├── shopping-cart-rbac/                # Task 2: Role-Based Access
│   ├── main.py
│   ├── auth.py
│   ├── README.md
│   ├── users.json (auto-generated)
│   ├── products.json (auto-generated)
│   └── cart.json (auto-generated)
├── job-tracker/        # Task 3: User Data Isolation
│   ├── main.py
│   ├── README.md
│   ├── users.json (auto-generated)
│   └── applications.json (auto-generated)
└── notes-api-jwt/                     # Task 4: JWT Authentication
    ├── main.py
    ├── requirements.txt
    ├── README.md
    ├── users.json (auto-generated)
    └── notes.json (auto-generated)
```

## 🔐 Student Portal API

**Folder**: `student-portal-auth`

**Concepts Learned**:

- HTTP Basic Authentication
- Password hashing (SHA-256)
- Pydantic models and validation
- JSON file operations with error handling
- FastAPI dependencies

**Key Features**:

- Student registration with secure password storage
- Login authentication using HTTP Basic Auth
- Grade management for authenticated students
- Comprehensive error handling

**Quick Test**:

```bash
cd student-portal-auth
python main.py

# Register student
curl -X POST "http://localhost:8000/register/" \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "password123"}'

# View grades
curl -X GET "http://localhost:8000/grades/" -u "student1:password123"
```

## 🛒 Shopping Cart API

**Folder**: `shopping-cart-rbac`

**Concepts Learned**:

- Role-based access control (RBAC)
- Dependency injection for authorization
- Modular authentication (`auth.py`)
- Admin vs customer permissions
- Multi-file JSON data management

**Key Features**:

- Admin-only product management
- Public product browsing
- Authenticated shopping cart operations
- Default admin and customer accounts

**Quick Test**:

```bash
cd shopping-cart-rbac
python main.py

# Add product (admin only)
curl -X POST "http://localhost:8000/admin/add_product/" \
  -H "Content-Type: application/json" \
  -u "admin:admin123" \
  -d '{"name": "Laptop", "price": 999.99, "description": "Gaming laptop", "stock": 5}'

# Add to cart (any user)
curl -X POST "http://localhost:8000/cart/add/" \
  -H "Content-Type: application/json" \
  -u "customer1:password123" \
  -d '{"product_id": 1, "quantity": 1}'
```

## 📋 Job Application Tracker

**Folder**: `job-tracker`

**Concepts Learned**:

- User data isolation and security
- Filtered API responses by authenticated user
- CRUD operations with user context
- Date handling in APIs
- Per-user data separation

**Key Features**:

- Complete job application lifecycle
- User can only see their own applications
- Date tracking for applications
- Status updates (Applied, Interview, Rejected, etc.)

**Quick Test**:

```bash
cd job-tracker
python main.py

# Register user
curl -X POST "http://localhost:8000/register/" \
  -H "Content-Type: application/json" \
  -d '{"username": "jobseeker", "password": "seekjob123"}'

# Add job application
curl -X POST "http://localhost:8000/applications/" \
  -H "Content-Type: application/json" \
  -u "jobseeker:seekjob123" \
  -d '{"job_title": "Python Developer", "company": "Tech Corp", "date_applied": "2024-01-20", "status": "Applied"}'
```

## 📝 Notes API with JWT

**Folder**: `notes-api-jwt`

**Concepts Learned**:

- JWT (JSON Web Token) authentication
- Bearer token implementation
- Token expiration and validation
- Stateless authentication
- Advanced security patterns

**Key Features**:

- JWT token generation and validation
- Token-based CRUD operations
- Automatic token expiration (30 minutes)
- Secure note management per user
- Token verification endpoints

**Quick Test**:

```bash
cd notes-api-jwt
pip install -r requirements.txt
python main.py

# Register and login
curl -X POST "http://localhost:8000/register/" \
  -H "Content-Type: application/json" \
  -d '{"username": "noteuser", "password": "notes123"}'

# Get token
TOKEN=$(curl -s -X POST "http://localhost:8000/login/" \
  -H "Content-Type: application/json" \
  -d '{"username": "noteuser", "password": "notes123"}' | jq -r '.access_token')

# Add note with token
curl -X POST "http://localhost:8000/notes/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title": "My First Note", "content": "This is a secure note!"}'
```

## 🎓 Learning Path

**Recommended Order**:

1. **Start with Student Portal** - Learn basic FastAPI and HTTP Basic Auth
2. **Move to Shopping Cart** - Understand roles and permissions
3. **Try Job Tracker** - Master user data isolation
4. **Finish with Notes API** - Implement modern JWT authentication

## 🛠 Development Setup

### Environment Setup

```bash
# Create virtual environment (recommended)
python -m venv fastapi-env
source fastapi-env/bin/activate  # On Windows: fastapi-env\Scripts\activate

# Install dependencies for all projects
pip install fastapi uvicorn PyJWT python-multipart
```

### Testing Tools

- **Swagger UI**: Built-in at `/docs` for each project
- **cURL**: Command-line testing (examples provided)
- **Postman**: Import OpenAPI specs from `/openapi.json`
- **httpie**: `pip install httpie` for prettier CLI requests

## 🔒 Security Features Demonstrated

### Authentication Methods

- **HTTP Basic Auth**: Username/password in headers
- **JWT Tokens**: Stateless, encrypted tokens
- **Bearer Tokens**: Modern OAuth 2.0 standard

### Security Practices

- **Password Hashing**: Never store plain text passwords
- **User Isolation**: Users can only access their own data
- **Role-Based Access**: Different permissions for different user types
- **Token Expiration**: Automatic session timeout
- **Input Validation**: Pydantic models prevent invalid data
- **Error Handling**: Secure error messages without information leakage

## 📖 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **JWT.io**: Understanding JSON Web Tokens
- **HTTP Status Codes**: MDN Web Docs
- **REST API Best Practices**: Various online resources
- **OAuth 2.0 Specification**: For advanced authentication patterns

## 🤝 Contributing

This is a learning repository! Feel free to:

- Add more authentication examples
- Improve documentation and comments
- Fix bugs or add features
- Suggest better security practices
- Add tests for the endpoints

## ⚠️ Important Notes

### For Learning Only

- **Not Production Ready**: Use proper databases, not JSON files
- **Simple Hashing**: Use bcrypt instead of SHA-256 in production
- **Secret Management**: Use environment variables for secrets
- **HTTPS Only**: Always use HTTPS in production environments

### Default Credentials

- **Shopping Cart Admin**: `admin` / `admin123`
- **Shopping Cart Customer**: `customer1` / `password123`

## 📄 License

This project is created for educational purposes. Feel free to use, modify, and learn from the code.

---

**Happy Learning! 🚀**

_Each project includes detailed README files with specific instructions, testing examples, and learning objectives._
