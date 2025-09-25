from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel


class Group(Base):
    __tablename__ = "groups"

    group_id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String, unique=True, index=True)
    description = Column(String)


class GroupCreate(BaseModel):
    group_name: str
    description: str


class GroupResponse(BaseModel):
    group_id: int
    group_name: str
    description: str

    class Config:
        orm_mode = True
        from_attributes = True
