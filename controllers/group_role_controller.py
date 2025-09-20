from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.group_role_model import GroupRoleCreate, GroupRoleResponse
from services import group_role_service
from database import get_db
from views import group_role_view

router = APIRouter()


@router.get("/", response_model=list[GroupRoleResponse])
def get_group_roles(db: Session = Depends(get_db)):
    return group_role_service.get_group_roles(db)


@router.get("/{group_role_id}", response_model=GroupRoleResponse)
def get_group_role(group_role_id: int, db: Session = Depends(get_db)):
    group_role = group_role_service.get_group_role(db, group_role_id)
    if group_role:
        return group_role
    return group_role_view.error_response("GroupRole not found", 404)


@router.post("/", response_model=GroupRoleResponse)
def create_group_role(group_role: GroupRoleCreate, db: Session = Depends(get_db)):
    return group_role_service.create_group_role(db, group_role)


@router.delete("/{group_role_id}")
def delete_group_role(group_role_id: int, db: Session = Depends(get_db)):
    deleted = group_role_service.delete_group_role(db, group_role_id)
    if deleted:
        return group_role_view.success_response({"id": deleted.id}, "GroupRole deleted")
    return group_role_view.error_response("GroupRole not found", 404)
