from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel
import uuid

class Role(Base):
    __tablename__ = "roles"

    role_id = Column(
        String,                      
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    role_name = Column(String, unique=True, index=True)
    description = Column(String)


class RoleCreate(BaseModel):
    role_name: str
    description: str


class RoleResponse(BaseModel):
    role_id: str
    role_name: str
    description: str

    class Config:
        orm_mode = True
        from_attributes = True
