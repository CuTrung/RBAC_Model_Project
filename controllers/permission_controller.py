from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.permission_model import PermissionCreate, PermissionResponse, PermissionUpdate
from services import permission_service
from views import permission_view
from database import get_db

router = APIRouter()

@router.get("/", response_model=list[PermissionResponse])
def get_permissions(db: Session = Depends(get_db)):
    try:
        return permission_view.success_response(
            permission_service.get_permissions(db)
        )
    except ValueError as ve:
        return permission_view.error_response(str(ve), 400)

@router.get("/{permission_id}", response_model=PermissionResponse)
def get_permission(permission_id: str, db: Session = Depends(get_db)):
    try:
        return permission_view.success_response(
            permission_service.get_permission(db, permission_id)
        )
    except ValueError as ve:
        return permission_view.error_response(str(ve), 400)

@router.post("/", response_model=PermissionResponse)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    try:
        return permission_view.success_response(
            permission_service.create_permission(db, permission), 
            "Tạo permission thành công"
        )
    except ValueError as ve:
        return permission_view.error_response(str(ve), 400)
    

@router.put("/{permission_id}", response_model=PermissionResponse)
def update_permission(permission_id: str, permission: PermissionUpdate, db: Session = Depends(get_db)):
    try:
        return permission_view.success_response(
            permission_service.update_permission(db, permission_id, permission), 
            "Cập nhật permisson thành công"
        )
    except ValueError as ve:
        return permission_view.error_response(str(ve), 400)


@router.delete("/{permission_id}")
def delete_permission(permission_id: str, db: Session = Depends(get_db)):
    try:
        return permission_view.success_response(
            permission_service.delete_permission(db, permission_id), 
            "Xóa permission thành công"
        )
    except ValueError as ve:
        return permission_view.error_response(str(ve), 400)

    
