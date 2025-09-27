from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm import Session
from services import group_role_service
from database import get_db
from views import group_role_view

router = APIRouter()


@router.get("/{group_id}/roles")
def get_roles_of_group(group_id: str, db: Session = Depends(get_db)):
    try:
        return group_role_view.success_response(
            group_role_service.get_roles_of_group(db, group_id), 
            "Lấy roles của group thành công"
        )
    except ValueError as e:
        return group_role_view.error_response(str(e), 404)


@router.post("/assign")
def assign_roles_for_group(
    group_id: str = Body(..., embed=True),
    role_ids: list[str] = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    try:
        result = group_role_service.assign_roles_for_group(db, group_id, role_ids)
        message = "Xóa toàn bộ role khỏi group thành công" 
        
        if len(result) > 0:
            message = "Gán role cho group thành công"
        return group_role_view.success_response(result, message)
    except ValueError as ve:
        return group_role_view.error_response(str(ve), status.HTTP_400_BAD_REQUEST)
