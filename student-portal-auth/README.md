# Task 1: Secure Student Portal API

A FastAPI-based student portal where students can register, login, and view their grades securely.

## Features

- Student registration with username and password
- Secure login using HTTP Basic Authentication
- Password hashing for security
- Grade viewing for authenticated students
- JSON file storage for student data
- Error handling for file operations

## Project Structure

```
student-portal-auth/
├── main.py          # Main FastAPI application
├── students.json    # JSON file to store student data (created automatically)
└── README.md        # This file
```

## Installation

1. Install required packages:

```bash
pip install fastapi uvicorn
```

2. Run the application:

```bash
cd student-portal-auth
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload
```

## API Endpoints

### 1. Root Endpoint

- **GET** `/` - Welcome message

### 2. Register Student

- **POST** `/register/`
- **Body**:

```json
{
  "username": "john_doe",
  "password": "mypassword"
}
```

- **Response**: Success message

### 3. Login

- **POST** `/login/`
- **Authentication**: HTTP Basic (username and password)
- **Response**: Login confirmation

### 4. Get Grades

- **GET** `/grades/`
- **Authentication**: HTTP Basic (username and password)
- **Response**:

```json
{
  "username": "john_doe",
  "grades": [85.5, 92.0, 78.5]
}
```

### 5. Add Grade (For Testing)

- **POST** `/grades/add/?grade=95.0`
- **Authentication**: HTTP Basic (username and password)
- **Response**: Confirmation message

## How to Test

1. **Register a student**:

```bash
curl -X POST "http://localhost:8000/register/" \
-H "Content-Type: application/json" \
-d '{"username": "student1", "password": "password123"}'
```

2. **Login**:

```bash
curl -X POST "http://localhost:8000/login/" \
-u "student1:password123"
```

3. **Add a grade** (for testing):

```bash
curl -X POST "http://localhost:8000/grades/add/?grade=95.0" \
-u "student1:password123"
```

4. **View grades**:

```bash
curl -X GET "http://localhost:8000/grades/" \
-u "student1:password123"
```

## Interactive Documentation

Visit `http://localhost:8000/docs` for Swagger UI documentation where you can test all endpoints interactively.

## Security Features

- Passwords are hashed using SHA-256 before storage
- HTTP Basic Authentication for protected routes
- Input validation using Pydantic models
- Proper error handling and status codes

## File Storage

Student data is stored in `students.json` with the following structure:

```json
{
  "student1": {
    "password": "hashed_password_here",
    "grades": [85.5, 92.0, 78.5]
  }
}
```

## Error Handling

The application includes comprehensive error handling for:

- File read/write operations
- JSON parsing errors
- Invalid credentials
- Duplicate usernames
- Invalid grade values
