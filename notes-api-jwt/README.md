# Task 4: Notes API with JWT Token Authentication

A FastAPI-based notes management API with JWT (JSON Web Token) authentication for secure access.

## Features

- User registration and authentication
- JWT token-based authentication
- Create, read, update, and delete notes
- User-specific note isolation
- Token expiration and verification
- Bearer token authentication scheme

## Project Structure

```
notes-api-jwt/
├── main.py          # Main FastAPI application with JWT auth
├── requirements.txt # Python dependencies
├── users.json       # User credentials (created automatically)
├── notes.json       # Notes data per user (created automatically)
└── README.md        # This file
```

## Installation

1. Install required packages:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install fastapi uvicorn PyJWT python-multipart
```

2. Run the application:

```bash
cd notes-api-jwt
python main.py
```

## API Endpoints

### Authentication Endpoints

#### Register User

- **POST** `/register/`
- **Body**:

```json
{
  "username": "johndoe",
  "password": "securepassword"
}
```

#### Login (Get JWT Token)

- **POST** `/login/`
- **Body**:

```json
{
  "username": "johndoe",
  "password": "securepassword"
}
```

- **Response**:

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Protected Endpoints (Require JWT Token)

#### Add Note

- **POST** `/notes/`
- **Authentication**: Bearer Token required
- **Body**:

```json
{
  "title": "My First Note",
  "content": "This is the content of my note."
}
```

#### Get My Notes

- **GET** `/notes/`
- **Authentication**: Bearer Token required
- **Response**: Array of user's notes

#### Get Specific Note

- **GET** `/notes/{note_id}`
- **Authentication**: Bearer Token required

#### Update Note

- **PUT** `/notes/{note_id}`
- **Authentication**: Bearer Token required
- **Body**:

```json
{
  "title": "Updated Title",
  "content": "Updated content"
}
```

#### Delete Note

- **DELETE** `/notes/{note_id}`
- **Authentication**: Bearer Token required

#### Get Current User Info

- **GET** `/me/`
- **Authentication**: Bearer Token required

#### Verify Token

- **GET** `/verify-token/`
- **Authentication**: Bearer Token required

## How to Test

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/register/" \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass123"}'
```

### 2. Login to Get Token

```bash
curl -X POST "http://localhost:8000/login/" \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass123"}'
```

**Save the token from the response for subsequent requests.**

### 3. Add a Note (Using Token)

```bash
curl -X POST "http://localhost:8000/notes/" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_TOKEN_HERE" \
-d '{
    "title": "Shopping List",
    "content": "- Milk\n- Bread\n- Eggs"
}'
```

### 4. Get All Notes

```bash
curl -X GET "http://localhost:8000/notes/" \
-H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 5. Update a Note

```bash
curl -X PUT "http://localhost:8000/notes/1" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_TOKEN_HERE" \
-d '{
    "title": "Updated Shopping List",
    "content": "- Milk\n- Bread\n- Eggs\n- Butter"
}'
```

### 6. Delete a Note

```bash
curl -X DELETE "http://localhost:8000/notes/1" \
-H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## JWT Token Usage

### Token Format

The API uses Bearer tokens in the Authorization header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Token Expiration

- Tokens expire after 30 minutes by default
- Expired tokens will return 401 Unauthorized
- Login again to get a new token

### Token Structure

JWT tokens contain:

- **Header**: Algorithm and token type
- **Payload**: User info (username) and expiration
- **Signature**: Verification signature

## Interactive Documentation

Visit `http://localhost:8000/docs` for Swagger UI:

1. Click "Authorize" button
2. Enter `Bearer YOUR_TOKEN_HERE`
3. Test all endpoints interactively

## Security Features

### JWT Authentication

- Stateless authentication (no server-side sessions)
- Tokens contain encrypted user information
- Automatic expiration prevents indefinite access
- Bearer token scheme follows OAuth 2.0 standards

### Password Security

- Passwords hashed using SHA-256
- Original passwords never stored
- Secure credential verification

### User Isolation

- Notes are completely isolated per user
- JWT token identifies the authenticated user
- No cross-user data access possible

## File Storage Structure

### users.json

```json
{
  "testuser": {
    "password": "hashed_password_here"
  },
  "anotheruser": {
    "password": "another_hashed_password"
  }
}
```

### notes.json

```json
{
  "testuser": [
    {
      "id": 1,
      "title": "Shopping List",
      "content": "- Milk\n- Bread\n- Eggs",
      "date": "2024-01-20"
    }
  ],
  "anotheruser": [
    {
      "id": 1,
      "title": "Meeting Notes",
      "content": "Discussed project timeline",
      "date": "2024-01-21"
    }
  ]
}
```

## Error Handling

The API handles various scenarios:

- **401 Unauthorized**: Invalid/expired/missing token
- **404 Not Found**: Note doesn't exist or belong to user
- **400 Bad Request**: Invalid input data
- **500 Internal Server Error**: File I/O or processing errors

## Production Considerations

For production deployment:

1. **Change SECRET_KEY**: Use a strong, random secret key
2. **Use Environment Variables**: Store secrets in environment variables
3. **HTTPS Only**: Always use HTTPS in production
4. **Database**: Replace JSON files with a proper database
5. **Stronger Hashing**: Use bcrypt instead of SHA-256
6. **Token Refresh**: Implement refresh token mechanism
