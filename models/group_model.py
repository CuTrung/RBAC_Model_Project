from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel
import uuid

class Group(Base):
    __tablename__ = "groups"

    group_id = Column(
        String,                      
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    group_name = Column(String, unique=True, index=True)
    description = Column(String)


class GroupCreate(BaseModel):
    group_name: str
    description: str

class GroupUpdate(BaseModel):
    group_name: str | None = None
    description: str | None = None


class GroupResponse(BaseModel):
    group_id: str
    group_name: str
    description: str

    class Config:
        orm_mode = True
        from_attributes = True
