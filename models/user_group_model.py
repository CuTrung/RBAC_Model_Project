from sqlalchemy import Column, Integer, ForeignKey
from database import Base
from pydantic import BaseModel


class UserGroup(Base):
    __tablename__ = "user_groups"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.group_id"), primary_key=True)


class UserGroupCreate(BaseModel):
    user_id: int
    group_id: int


class UserGroupResponse(BaseModel):
    user_id: int
    username: str = None
    group_id: int
    group_name: str = None

    class Config:
        orm_mode = True
        from_attributes = True
