# Task 3: Job Application Tracker with Secure Access

A FastAPI-based job application tracker where each user can only see and manage their own job applications.

## Features

- User registration and authentication
- Secure access - users can only see their own applications
- Add, view, update, and delete job applications
- Filter applications by authenticated user using dependency injection
- JSON file storage with per-user data separation

## Project Structure

```
job-tracker/
├── main.py            # Main FastAPI application
├── users.json         # User credentials (created automatically)
├── applications.json  # Job applications data (created automatically)
└── README.md          # This file
```

## Installation

1. Install required packages:

```bash
pip install fastapi uvicorn
```

2. Run the application:

```bash
cd job-tracker
python main.py
```

## API Endpoints

### User Management

#### Register User

- **POST** `/register/`
- **Body**:

```json
{
  "username": "johndoe",
  "password": "mypassword"
}
```

### Job Application Management (Authenticated Users Only)

#### Add Job Application

- **POST** `/applications/`
- **Authentication**: HTTP Basic Auth required
- **Body**:

```json
{
  "job_title": "Software Developer",
  "company": "Tech Corp",
  "date_applied": "2024-01-15",
  "status": "Applied"
}
```

#### Get My Applications

- **GET** `/applications/`
- **Authentication**: HTTP Basic Auth required
- **Response**: List of user's own applications only

#### Get Specific Application

- **GET** `/applications/{application_id}`
- **Authentication**: HTTP Basic Auth required
- **Response**: Application details (only if it belongs to the user)

#### Update Application Status

- **PUT** `/applications/{application_id}?status=Interview`
- **Authentication**: HTTP Basic Auth required
- **Response**: Updated application

#### Delete Application

- **DELETE** `/applications/{application_id}`
- **Authentication**: HTTP Basic Auth required

## How to Test

### 1. Register Users

```bash
# Register first user
curl -X POST "http://localhost:8000/register/" \
-H "Content-Type: application/json" \
-d '{"username": "alice", "password": "alice123"}'

# Register second user
curl -X POST "http://localhost:8000/register/" \
-H "Content-Type: application/json" \
-d '{"username": "bob", "password": "bob123"}'
```

### 2. Add Job Applications

```bash
# Alice adds an application
curl -X POST "http://localhost:8000/applications/" \
-H "Content-Type: application/json" \
-u "alice:alice123" \
-d '{
    "job_title": "Frontend Developer",
    "company": "Web Solutions Inc",
    "date_applied": "2024-01-20",
    "status": "Applied"
}'

# Bob adds an application
curl -X POST "http://localhost:8000/applications/" \
-H "Content-Type: application/json" \
-u "bob:bob123" \
-d '{
    "job_title": "Backend Developer",
    "company": "Server Tech Ltd",
    "date_applied": "2024-01-22",
    "status": "Interview Scheduled"
}'
```

### 3. View Applications (User-Specific)

```bash
# Alice sees only her applications
curl -X GET "http://localhost:8000/applications/" \
-u "alice:alice123"

# Bob sees only his applications
curl -X GET "http://localhost:8000/applications/" \
-u "bob:bob123"
```

### 4. Update Application Status

```bash
# Alice updates her application status
curl -X PUT "http://localhost:8000/applications/1?status=Interview" \
-u "alice:alice123"
```

## Security Features

### User Isolation

- Each user can only access their own job applications
- Authentication required for all application operations
- Applications are filtered by current logged-in user using dependency injection

### Authentication Flow

1. User registers with username/password
2. Password is hashed and stored securely
3. HTTP Basic Auth validates credentials on each request
4. `get_current_user` dependency returns authenticated username
5. All operations are filtered by this authenticated user

## File Storage Structure

### users.json

```json
{
  "alice": {
    "password": "hashed_password_here"
  },
  "bob": {
    "password": "hashed_password_here"
  }
}
```

### applications.json

```json
{
  "alice": [
    {
      "id": 1,
      "job_title": "Frontend Developer",
      "company": "Web Solutions Inc",
      "date_applied": "2024-01-20",
      "status": "Applied"
    }
  ],
  "bob": [
    {
      "id": 1,
      "job_title": "Backend Developer",
      "company": "Server Tech Ltd",
      "date_applied": "2024-01-22",
      "status": "Interview Scheduled"
    }
  ]
}
```

## Dependency Injection for Security

The `get_current_user` dependency:

1. **Authenticates** the user via HTTP Basic Auth
2. **Returns** the authenticated username
3. **Filters** all application operations to show only that user's data

This ensures complete user isolation without additional security checks in each endpoint.

## Interactive Documentation

Visit `http://localhost:8000/docs` for Swagger UI where you can:

- Test all endpoints interactively
- See request/response schemas
- Use the "Authorize" button for HTTP Basic Auth

## Error Handling

The application handles:

- Invalid credentials (401 Unauthorized)
- Accessing non-existent applications (404 Not Found)
- File I/O errors (500 Internal Server Error)
- Invalid input data (422 Validation Error)
- Attempting to access other users' applications (404 - appears as "not found" for security)
