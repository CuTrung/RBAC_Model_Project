from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm import Session
from models.user_group_model import UserGroupResponse
from services import user_group_service
from database import get_db
from views import user_group_view

router = APIRouter()


@router.get("/{group_id}/users", response_model=list[UserGroupResponse])
def get_users_of_group(group_id: str, db: Session = Depends(get_db)):
    try:
        return user_group_view.success_response(
            user_group_service.get_users_of_group(db, group_id), 
            "Lấy users của group thành công"
        )
    except ValueError as e:
        return user_group_view.error_response(str(e), 404)


@router.post("/assign")
def assign_users_for_group(
    group_id: str = Body(..., embed=True),
    user_ids: list[str] = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    try:
        result = user_group_service.assign_users_for_group(db, group_id, user_ids)
        message = "Xóa toàn bộ user khỏi group thành công" 
        
        if len(result) > 0:
            message = "Gán user cho group thành công"

        return user_group_view.success_response(result, message)
    except ValueError as ve:
        return user_group_view.error_response(str(ve), status.HTTP_400_BAD_REQUEST)
