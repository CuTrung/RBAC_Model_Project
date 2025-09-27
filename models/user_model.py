from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel
import uuid


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        String,                      
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    user_id: str
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True
        from_attributes = True
