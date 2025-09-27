from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.role_model import RoleCreate, RoleResponse, RoleUpdate
from services import role_service
from views import role_view
from database import get_db

router = APIRouter()

@router.get("/", response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    try:
        return role_view.success_response(
            role_service.get_roles(db)
        )
    except ValueError as ve:
        return role_view.error_response(str(ve), 400)

@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: str, db: Session = Depends(get_db)):
    try:
        return role_view.success_response(
            role_service.get_role(db, role_id)
        )
    except ValueError as ve:
        return role_view.error_response(str(ve), 400)

@router.post("/", response_model=RoleResponse)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    try:
        return role_view.success_response(
            role_service.create_role(db, role), 
            "Tạo role thành công"
        )
    except ValueError as ve:
        return role_view.error_response(str(ve), 400)
    

@router.put("/{role_id}", response_model=RoleResponse)
def update_role(role_id: str, role: RoleUpdate, db: Session = Depends(get_db)):
    try:
        return role_view.success_response(
            role_service.update_role(db, role_id, role), 
            "Cập nhật role thành công"
        )
    except ValueError as ve:
        return role_view.error_response(str(ve), 400)


@router.delete("/{role_id}")
def delete_role(role_id: str, db: Session = Depends(get_db)):
    try:
        return role_view.success_response(
            role_service.delete_role(db, role_id), 
            "Xóa role thành công"
        )
    except ValueError as ve:
        return role_view.error_response(str(ve), 400)

    
