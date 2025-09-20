from sqlalchemy import Column, Integer, ForeignKey
from database import Base
from pydantic import BaseModel


class GroupRole(Base):
    __tablename__ = "group_roles"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)


class GroupRoleCreate(BaseModel):
    group_id: int
    role_id: int


class GroupRoleResponse(BaseModel):
    id: int
    group_id: int
    role_id: int

    class Config:
        orm_mode = True
