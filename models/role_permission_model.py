from sqlalchemy import Column, String, ForeignKey
from database import Base
from pydantic import BaseModel
from models.permission_model import PermissionsOfRole


class RolePermission(Base):
    __tablename__ = "rolePermissions"

    role_id = Column(String, ForeignKey("roles.role_id"), primary_key=True)
    permission_id = Column(String, ForeignKey("permissions.permission_id"), primary_key=True)

class GetPermissionsOfRoleResponse(BaseModel):
    permissions: list[PermissionsOfRole]

    class Config:
        orm_mode = True
        from_attributes = True

class RolePermissionResponse(BaseModel):
    role_id: str
    role_name: str = None
    permission_id: str
    permission_name: str = None

    class Config:
        orm_mode = True
        from_attributes = True
        

