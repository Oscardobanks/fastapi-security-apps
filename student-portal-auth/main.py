from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List
import json
import hashlib
import os

app = FastAPI(title="Secure Student Portal API",
              description="A simple student portal where students can register, login and view grades.")

security = HTTPBasic()


class Student(BaseModel):
    username: str
    password: str
    grades: List[float] = []


class StudentRegister(BaseModel):
    username: str
    password: str


class StudentResponse(BaseModel):
    username: str
    grades: List[float]


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def load_students() -> dict:
    try:
        if not os.path.exists("students.json"):
            return {}
        with open("students.json", "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading students: {e}")
        return {}


def save_students(student: dict) -> bool:
    try:
        with open("students.json", "w") as file:
            json.dump(student, file, indent=2)
        return True
    except Exception as e:
        print(f"Error saving students: {e}")
        return False


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    students = load_students()

    hashed_password = hash_password(credentials.password)

    if (credentials.username in students and students[credentials.username]["password"] == hashed_password):
        return credentials.username
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password", headers={
                            "WWW-Authenticate": "Basic realm='Login Required'"})


# API Endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to the Secure Student Portal API!"}


@app.post("/register", response_model=dict)
def register_student(student: StudentRegister):
    try:
        students = load_students()
        if student.username in students:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

        hashed_password = hash_password(student.password)
        students[student.username] = {
            "password": hashed_password, "grades": []}

        save_students(students)
        return {"message": "Student registered successfully", "username": student.username}
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid student registration data")
    except Exception as e:
        print(f"Error registering student: {e}")
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@app.post("/login/")
def login(credentials: HTTPBasicCredentials = Depends(security)):
    try:
        get_current_user(credentials)
        return {"message": "User Login successfully!"}
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid login credentials")
    except Exception as e:
        print(f"Error logging in: {e}")
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@app.get("/grades/", response_model=StudentResponse)
def get_grades(current_user: str = Depends(get_current_user)):
    try:
        students = load_students()
        if current_user not in students:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        student_data = students[current_user]

        return StudentResponse(username=current_user, grades=student_data["grades"])
    except Exception as e:
        print(f"Error getting grades: {e}")
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
