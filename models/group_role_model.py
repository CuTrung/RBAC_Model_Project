from sqlalchemy import Column, Integer, ForeignKey
from database import Base
from pydantic import BaseModel


class GroupRole(Base):
    __tablename__ = "group_roles"

    group_id = Column(Integer, ForeignKey("groups.group_id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), primary_key=True)


class GroupRoleCreate(BaseModel):
    group_id: str
    role_id: str


class GroupRoleResponse(BaseModel):
    group_id: str
    group_name: str = None
    role_id: str
    role_name: str = None

    class Config:
        orm_mode = True
        from_attributes = True
