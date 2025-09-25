from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)


class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str

    class Config:
        orm_mode = True
        from_attributes = True
