from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..auth.jwt_handler import AuthHandler
import os
from fastapi import HTTPException, status

auth_handler = AuthHandler()

def get_user(db: Session, user_id: int):
    """Retrieve a user by id."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Retrieve a user by email."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    """Create a new user."""
    hashed_password = auth_handler.get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_or_create_google_user(db: Session, email: str):
    """Get existing user or create new one for Google login."""
    db_user = get_user_by_email(db, email=email)
    if db_user:
        return db_user
    
    # Create new user with a random password since they'll use Google auth
    db_user = User(
        email=email,
        hashed_password=auth_handler.get_password_hash(os.urandom(32).hex())
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    """Update user profile."""
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    
    if 'password' in update_data:
        update_data['hashed_password'] = auth_handler.get_password_hash(update_data.pop('password'))
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user profile"
        )