from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, index=True)
    description = Column(String)


class RoleCreate(BaseModel):
    role_name: str
    description: str


class RoleResponse(BaseModel):
    id: int
    role_name: str
    description: str

    class Config:
        orm_mode = True
