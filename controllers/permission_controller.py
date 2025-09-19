from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.permission_model import PermissionCreate, PermissionResponse
from services import permission_service
from views import permission_view
from database import get_db

router = APIRouter()

@router.get("/", response_model=list[PermissionResponse])
def get_permissions(db: Session = Depends(get_db)):
    permissions = permission_service.get_permissions(db)
    return permissions

@router.get("/{permission_id}", response_model=PermissionResponse)
def get_permission(permission_id: str, db: Session = Depends(get_db)):
    permission = permission_service.get_permission(db, permission_id)
    if permission:
        return permission
    return permission_view.error_response("Permission not found", 404)

@router.post("/", response_model=PermissionResponse)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    return permission_service.create_permission(db, permission)

@router.put("/{permission_id}", response_model=PermissionResponse)
def update_permission(permission_id: str, permission: PermissionCreate, db: Session = Depends(get_db)):
    updated = permission_service.update_permission(db, permission_id, permission)
    if updated:
        return updated
    return permission_view.error_response("Permission not found", 404)

@router.delete("/{permission_id}")
def delete_permission(permission_id: str, db: Session = Depends(get_db)):
    deleted = permission_service.delete_permission(db, permission_id)
    if deleted:
        return permission_view.success_response({"permission_id": deleted.permission_id}, "Permission deleted")
    return permission_view.error_response("Permission not found", 404)
