from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from models.user_group_model import UserGroupResponse
from services import user_group_service
from database import get_db
from views import user_group_view

router = APIRouter()


@router.get("/{user_id}", response_model=list[UserGroupResponse])
def get_groups_of_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return user_group_service.get_groups_of_user(db, user_id)
    except ValueError as e:
        return user_group_view.error_response(str(e), 404)


@router.post("/assign")
def assign_users_for_group(
    group_id: int = Body(..., embed=True),
    user_ids: list[int] = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    try:
        result = user_group_service.assign_users_for_group(db, group_id, user_ids)
        return user_group_view.success_response(
            [UserGroupResponse.from_orm(r).model_dump() for r in result],
            "Assigned users for group successfully",
        )
    except ValueError as e:
        return user_group_view.error_response(str(e), 400)
