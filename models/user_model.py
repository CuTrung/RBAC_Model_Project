from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True
        from_attributes = True
