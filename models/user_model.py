from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel

# ORM model (dùng cho DB)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)


# Pydantic schema (dùng cho request/response)
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
