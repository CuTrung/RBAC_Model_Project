from sqlalchemy import Column, String, ForeignKey
from database import Base
from pydantic import BaseModel
import uuid


class Permission(Base):
    __tablename__ = "permissions"

    permission_id = Column(
        String,                      
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    permission_name = Column(String, unique=True, nullable=False,)
    description = Column(String)
    resource_id = Column(String, ForeignKey("resources.resource_id"))

class PermissionCreate(BaseModel):
    permission_name: str
    description: str
    resource_id: str | None = None

class PermissionUpdate(BaseModel):
    permission_name: str | None = None
    description: str | None = None
    resource_id: str | None = None

class PermissionResponse(BaseModel):
    permission_id: str
    permission_name: str
    description: str
    resource_id: str | None = None

    class Config:
        orm_mode = True

class PermissionsOfRole(BaseModel):
    permission_id: str
    permission_name: str

    class Config:
        orm_mode = True
