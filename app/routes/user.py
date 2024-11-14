from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.user import User, UserCreate, UserLogin, GoogleLogin, UserUpdate
from ..crud import user as user_crud
from ..auth.jwt_handler import AuthHandler
from ..auth.google_auth import GoogleAuth
from typing import Optional
from fastapi import status

router = APIRouter()
auth_handler = AuthHandler()
google_auth = GoogleAuth()

@router.post("/register", response_model=User)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    - **email**: A valid email address
    - **password**: A strong password
    
    Returns the created user information.
    """
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a token.
    
    - **email**: The user's email address
    - **password**: The user's password
    
    Returns an access token if authentication is successful.
    """
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user is None or not auth_handler.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = auth_handler.encode_token(str(db_user.id))
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users/me", response_model=User)
async def read_users_me(db: Session = Depends(get_db), user_id: str = Depends(auth_handler.auth_wrapper)):
    """
    Get the current authenticated user.
    
    Returns the user information for the authenticated user.
    """
    db_user = user_crud.get_user(db, user_id=int(user_id))
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/login/google")
async def google_login(google_data: GoogleLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user using Google OAuth token.
    
    - **token**: The Google OAuth ID token
    
    Returns an access token if authentication is successful.
    """
    user_data = await google_auth.verify_google_token(google_data.token)
    
    if not user_data['email_verified']:
        raise HTTPException(
            status_code=400,
            detail="Google account email not verified"
        )
    
    db_user = user_crud.get_or_create_google_user(db, email=user_data['email'])
    token = auth_handler.encode_token(str(db_user.id))
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "email": db_user.email,
            "id": db_user.id
        }
    }

@router.put("/users/profile", response_model=User)
async def update_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(auth_handler.auth_wrapper)
):
    """
    Update the current user's profile.
    
    - **email**: New email address (optional)
    - **password**: New password (optional)
    
    Returns the updated user information.
    """
    # Check if email is being updated and is already taken
    if user_update.email:
        existing_user = user_crud.get_user_by_email(db, email=user_update.email)
        if existing_user and existing_user.id != int(current_user_id):
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
    
    updated_user = user_crud.update_user(
        db=db,
        user_id=int(current_user_id),
        user_update=user_update
    )
    
    if not updated_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    return updated_user