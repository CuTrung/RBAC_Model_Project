from sqlalchemy import Column, String
from database import Base
from pydantic import BaseModel
import uuid


class Permission(Base):
    __tablename__ = "permissions"

    permission_id = Column(
        String,                      
        primary_key=True,
        default=lambda: str(uuid.uuid4()),  
        unique=True,
        nullable=False
    )
    permission_name = Column(String, nullable=False)
    description = Column(String)
    resource_id = Column(String)

class PermissionCreate(BaseModel):
    permission_name: str
    description: str
    resource_id: str

class PermissionResponse(BaseModel):
    permission_id: str
    permission_name: str
    description: str
    resource_id: str

    class Config:
        orm_mode = True

class PermissionsOfRole(BaseModel):
    permission_id: str
    permission_name: str

    class Config:
        orm_mode = True
