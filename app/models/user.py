from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    """
    User model for the database.
    Represents a user in the system.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

    todos = relationship("Todo", back_populates="owner")