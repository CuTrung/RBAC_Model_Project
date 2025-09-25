from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.role_permission_model import AssignPermissionsForRole, AssignPermissionsForRoleResponse
from services import role_permission_service
from views import role_permission_view
from database import get_db

router = APIRouter()

@router.get("/{role_id}", response_model=AssignPermissionsForRoleResponse)
def get_permissions_of_role(role_id: str, db: Session = Depends(get_db)):
    permissionsOfRole = role_permission_service.get_permissions_of_role(db, role_id)
    if permissionsOfRole:
        return permissionsOfRole
    return role_permission_view.error_response("RolePermission not found", 404)

@router.post("/", response_model=AssignPermissionsForRoleResponse)
def assign_permissions_for_role(payload: AssignPermissionsForRole, db: Session = Depends(get_db)):
    return role_permission_service.assign_permissions_for_role(db, payload)



