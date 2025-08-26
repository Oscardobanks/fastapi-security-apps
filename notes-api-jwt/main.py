from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from datetime import timedelta, date
from auth import hash_password, authenticate_user, create_access_token, load_users, save_users, load_notes, save_notes, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES


app = FastAPI(title="Notes API with JWT Authentication",
              description="A secure notes management API using JWT tokens")


class User(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str


class Note(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    date: date  # Will be set to current date if not provided


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    date: date
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int  # seconds until expiration


@app.get("/")
def read_root():
    return {"message": "Welcome to the Notes API with JWT Authentication!"}


@app.post("/register/")
def register_user(user: User):
    try:
        users = load_users()

        # Check if username already exists
        if user.username in users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

        # Hash password and save user
        users[user.username] = {
            "password": hash_password(user.password)
        }

        if save_users(users):
            return {"message": f"User {user.username} registered successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save user"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@app.post("/login/", response_model=Token)
def login(user: User):
    try:
        # Authenticate user
        if not authenticate_user(user.username, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@app.post("/notes/", response_model=NoteResponse)
def add_note(
    note: NoteCreate,
    current_user: str = Depends(verify_token)
):
    try:
        notes = load_notes()

        # Initialize user's notes list if it doesn't exist
        if current_user not in notes:
            notes[current_user] = []

        # Generate new ID for the note
        user_notes = notes[current_user]
        if user_notes:
            max_id = max(n["id"] for n in user_notes)
            new_id = max_id + 1
        else:
            new_id = 1

        # Create new note with current date
        new_note = {
            "id": new_id,
            "title": note.title,
            "content": note.content,
            "date": date.today()
        }

        # Add to user's notes
        notes[current_user].append(new_note)

        # Save to file
        if save_notes(notes):
            return NoteResponse(
                id=new_id,
                title=note.title,
                content=note.content,
                date=new_note["date"],
                username=current_user
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save note"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add note: {str(e)}"
        )


@app.get("/notes/", response_model=List[NoteResponse])
def get_my_notes(current_user: str = Depends(verify_token)):
    try:
        notes = load_notes()

        # Get only the current user's notes
        user_notes = notes.get(current_user, [])

        # Convert to response model
        response_notes = []
        for note in user_notes:
            response_notes.append(NoteResponse(
                id=note["id"],
                title=note["title"],
                content=note["content"],
                date=note["date"],
                username=current_user
            ))

        return response_notes

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve notes: {str(e)}"
        )


@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_note_by_id(
    note_id: int,
    current_user: str = Depends(verify_token)
):
    try:
        notes = load_notes()
        user_notes = notes.get(current_user, [])

        # Find the note with matching ID
        for note in user_notes:
            if note["id"] == note_id:
                return NoteResponse(
                    id=note["id"],
                    title=note["title"],
                    content=note["content"],
                    date=note["date"],
                    username=current_user
                )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve note: {str(e)}"
        )


@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    updated_note: NoteCreate,
    current_user: str = Depends(verify_token)
):
    try:
        notes = load_notes()
        user_notes = notes.get(current_user, [])

        # Find and update the note
        for note in user_notes:
            if note["id"] == note_id:
                note["title"] = updated_note.title
                note["content"] = updated_note.content

                # Save updated notes
                if save_notes(notes):
                    return NoteResponse(
                        id=note["id"],
                        title=note["title"],
                        content=note["content"],
                        date=note["date"],
                        username=current_user
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to update note"
                    )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update note: {str(e)}"
        )


@app.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    current_user: str = Depends(verify_token)
):
    try:
        notes = load_notes()
        user_notes = notes.get(current_user, [])

        # Find and remove the note
        for i, note in enumerate(user_notes):
            if note["id"] == note_id:
                removed_note = user_notes.pop(i)

                # Save updated notes
                if save_notes(notes):
                    return {"message": f"Note '{removed_note['title']}' deleted successfully"}
                else:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to delete note"
                    )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete note: {str(e)}"
        )


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
