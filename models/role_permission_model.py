from sqlalchemy import Column, String
from database import Base
from pydantic import BaseModel
from models.permission_model import PermissionsOfRole


class RolePermission(Base):
    __tablename__ = "rolePermissions"

    role_id = Column(String)
    permission_id = Column(String)

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


