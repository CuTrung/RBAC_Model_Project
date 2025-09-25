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
        
class AssignPermissionsForRole(BaseModel):
    role_id: str
    permission_ids: list[str]

class AssignPermissionsForRoleResponse(BaseModel):
    role_id: str

    class Config:
        orm_mode = True


