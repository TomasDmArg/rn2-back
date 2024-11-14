from pydantic import BaseModel, EmailStr
from typing import List, Optional
from .todo import Todo

class UserBase(BaseModel):
    """Base User schema with common attributes."""
    email: EmailStr

class UserCreate(UserBase):
    """Schema for user creation, including password."""
    password: str

class UserLogin(UserBase):
    """Schema for user login, including password."""
    password: str

class User(UserBase):
    """
    Full User schema, used for responses.
    Includes id, active status, and associated todos.
    """
    id: int
    is_active: bool
    todos: List[Todo] = []

    model_config = {
        "from_attributes": True
    }

class GoogleLogin(BaseModel):
    token: str

class UserUpdate(BaseModel):
    """Schema for user profile updates."""
    email: Optional[EmailStr] = None
    password: Optional[str] = None