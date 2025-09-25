from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.role_model import RoleCreate, RoleResponse
from services import role_service
from database import get_db
from views import role_view

router = APIRouter()


@router.get("/", response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    return role_service.get_roles(db)


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = role_service.get_role(db, role_id)
    if role:
        return role
    return role_view.error_response("Role not found", 404)


@router.post("/", response_model=RoleResponse)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return role_service.create_role(db, role)


@router.put("/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role: RoleCreate, db: Session = Depends(get_db)):
    updated = role_service.update_role(db, role_id, role)
    if updated:
        return updated
    return role_view.error_response("Role not found", 404)


@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    deleted = role_service.delete_role(db, role_id)
    if deleted:
        return role_view.success_response({"role_id": deleted.role_id}, "Role deleted")
    return role_view.error_response("Role not found", 404)
