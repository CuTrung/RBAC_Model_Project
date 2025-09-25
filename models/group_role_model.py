from sqlalchemy import Column, Integer, ForeignKey
from database import Base
from pydantic import BaseModel


class GroupRole(Base):
    __tablename__ = "group_roles"

    group_role_id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.group_id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)


class GroupRoleCreate(BaseModel):
    group_id: int
    role_id: int


class GroupRoleResponse(BaseModel):
    group_role_id: int
    group_id: int
    role_id: int

    class Config:
        orm_mode = True
        from_attributes = True
