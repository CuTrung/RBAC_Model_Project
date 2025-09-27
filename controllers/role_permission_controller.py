from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm import Session
from models.role_permission_model import RolePermissionResponse
from services import role_permission_service
from services import role_service
from views import role_permission_view
from database import get_db

router = APIRouter()

@router.get("/{role_id}/permissions")
def get_permissions_of_role(role_id: str, db: Session = Depends(get_db)):
    try:
        return role_permission_view.success_response(
            role_permission_service.get_permissions_of_role(db, role_id), 
            "Lấy permissions của role thành công"
        )
    except ValueError as e:
        return role_permission_view.error_response(str(e), 404)

@router.post("/assign")
def assign_permissions_for_role(
    role_id: str = Body(..., embed=True),
    permission_ids: list[str] = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    try:
        result = role_permission_service.assign_permissions_for_role(db, role_id, permission_ids)
        message = "Xóa toàn bộ permission khỏi role thành công" 
        
        if len(result) > 0:
            message = "Gán permission cho role thành công"

        return role_permission_view.success_response(result, message)
    except ValueError as ve:
        return role_permission_view.error_response(str(ve), status.HTTP_400_BAD_REQUEST)



