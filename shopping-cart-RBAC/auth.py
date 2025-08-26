from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import json
import hashlib
import os

# Initialize HTTP Basic authentication
security = HTTPBasic()


class User(BaseModel):
    username: str
    role: str


class UserCreate(BaseModel):
    username: str
    password: str
    roles: str


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def load_users() -> dict:
    try:
        if not os.path.exists("users.json"):
            return {}
        with open("users.json", "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading users: {e}")
        return {}


def save_users(user: dict) -> bool:
    try:
        with open("users.json", "w") as file:
            json.dump(user, file, indent=2)
        return True
    except Exception as e:
        print(f"Error saving user: {e}")
        return False


def create_user(username: str, password: str, role: str = "customer") -> bool:
    users = load_users()

    if (username) in users:
        return False

    users[username] = {
        "username": username,
        "password": hash_password(password),
        "role": role
    }

    return save_users(users)


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> User:
    users = load_users()

    hashed_password = hash_password(credentials.password)

    if (credentials.username in users and users[credentials.username]["password"] == hashed_password):
        return User(username=credentials.username, role=users[credentials.username]["role"])
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password", headers={
                            "WWW-Authenticate": "Basic realm='Login Required'"})


def require_admin_role(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Admin access is required")
    return current_user


def require_customer_or_admin_role(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in ["customer", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid User role")
    return current_user


def is_admin(user: User) -> bool:
    return user.role == "admin"


def is_customer(user: User) -> bool:
    return user.role == "customer"


def initialize_default_users():
    users = load_users()

    if not users:
        print("Creating default users...")
        create_user("admin", "admin123", "admin")
        create_user("customer1", "password123", "customer")
        print("Default users created successfully.")


initialize_default_users()
