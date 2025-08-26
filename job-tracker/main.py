from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date
import json
import hashlib
import os

app = FastAPI(title="Job Application Tracker API",
              description="A secure API where users can track their job applications")

# Initialize HTTP Basic authentication
security = HTTPBasic()


class User(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    password: str


class JobApplication(BaseModel):
    id: Optional[int] = None
    job_title: str
    company: str
    date_applied: date
    status: str = "Applied"


class JobApplicationCreate(BaseModel):
    job_title: str
    company: str
    date_applied: date
    status: str = "Applied"


class JobApplicationResponse(BaseModel):
    id: int
    job_title: str
    company: str
    date_applied: date
    status: str
    username: str


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


def load_applications() -> dict:
    try:
        if not os.path.exists("applications.json"):
            return {}
        with open("applications.json", "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading applications: {e}")
        return {}


def save_applications(applications: dict) -> bool:
    try:
        with open("applications.json", "w") as file:
            json.dump(applications, file, indent=2)
        return True
    except Exception as e:
        print(f"Error saving applications: {e}")
        return False


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    users = load_users()
    hashed_password = hash_password(credentials.password)

    # verify credentials
    if (credentials.username in users and users[credentials.username]["password"] == hashed_password):
        return credentials.username
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


# API Endpoints
@app.post("/register/")
def register_user(user: UserCreate):
    try:
        users = load_users()
        if user.username in users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

        users[user.username] = {
            "password": hash_password(user.password)
        }
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to register user")
    except Exception as e:
        print(f"Error registering user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server error. Failed to register user")


@app.post("/applications/", response_model=JobApplicationResponse)
def add_job_application(application: JobApplicationCreate, current_user: str = Depends(get_current_user)):
    try:
        applications = load_applications()
        if application.job_title in applications:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Job title already exists")

        if current_user not in applications:
            applications[current_user] = []

        user_apps = applications[current_user]
        if user_apps:
            max_id = max(app["id"] for app in user_apps)
            new_id = max_id + 1
        else:
            new_id = 1

        # Create new application with generated ID
        new_application = {
            "id": new_id,
            "job_title": application.job_title,
            "company": application.company,
            "date_applied": application.date_applied,
            "status": application.status,
        }

        applications[current_user].append(new_application)

        if (save_applications(applications)):
            return JobApplicationResponse(**new_application)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save application")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error. Failed to add job application")


@app.get("/applications/", response_model=List[JobApplicationResponse])
def get_my_applications(current_user: str = Depends(get_current_user)):
    try:
        applications = load_applications()
        if current_user not in applications:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user_applications = applications.get(current_user, [])

        response_applications = []
        for app in user_applications:
            response_applications.append(JobApplicationResponse(**app))
            return response_applications
    except Exception as e:
        print(f"Error getting applications: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@app.get("/applications/{application_id}", response_model=JobApplicationResponse)
def get_job_application(application_id: int, current_user: str = Depends(get_current_user)):
    try:
        applications = load_applications()
        user_applications = applications.get(current_user, [])

        if current_user not in applications:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        for app in user_applications:
            if app["id"] == application_id:
                return JobApplicationResponse(**app)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
