from sqlalchemy import Column, Integer, ForeignKey
from database import Base
from pydantic import BaseModel


class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)


class UserGroupCreate(BaseModel):
    user_id: int
    group_id: int


class UserGroupResponse(BaseModel):
    id: int
    user_id: int
    group_id: int

    class Config:
        orm_mode = True
