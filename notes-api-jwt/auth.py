from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, date
import jwt
import json
import hashlib
import os

SECRET_KEY = "GJfZuQZQnpzaGkDh8bV0xOTtJ21ouy_2tOWMYHT5lZ8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize JWT Bearer authentication scheme
security = HTTPBearer()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def load_users() -> dict:
    try:
        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                return json.load(file)
        else:
            return {}
    except Exception as e:
        print(f"Error loading users: {e}")
        return {}


def save_users(users: dict) -> bool:
    try:
        with open("users.json", "w") as file:
            json.dump(users, file, indent=2)
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False


def load_notes() -> dict:
    try:
        if os.path.exists("notes.json"):
            with open("notes.json", "r") as file:
                data = json.load(file)
                # Convert date strings back to date objects
                for username, user_notes in data.items():
                    for note in user_notes:
                        if isinstance(note['date'], str):
                            note['date'] = datetime.strptime(
                                note['date'], "%Y-%m-%d").date()
                return data
        else:
            return {}
    except Exception as e:
        print(f"Error loading notes: {e}")
        return {}


def save_notes(notes: dict) -> bool:
    try:
        # Convert date objects to strings for JSON serialization
        notes_for_json = {}
        for username, user_notes in notes.items():
            notes_for_json[username] = []
            for note in user_notes:
                note_dict = note.copy()
                if isinstance(note_dict['date'], date):
                    note_dict['date'] = note_dict['date'].strftime("%Y-%m-%d")
                notes_for_json[username].append(note_dict)

        with open("notes.json", "w") as file:
            json.dump(notes_for_json, file, indent=2)
        return True
    except Exception as e:
        print(f"Error saving notes: {e}")
        return False

# JWT token functions


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()

    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add expiration time to token payload
    to_encode.update({"exp": expire})

    # Create and return the JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    try:
        # Extract token from Bearer authorization header
        token = credentials.credentials

        # Decode and verify the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract username from token payload
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return username

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def authenticate_user(username: str, password: str) -> bool:
    users = load_users()
    hashed_password = hash_password(password)

    return (username in users and
            users[username]["password"] == hashed_password)
