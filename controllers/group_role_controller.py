from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from models.group_role_model import GroupRoleResponse
from services import group_role_service
from database import get_db
from views import group_role_view

router = APIRouter()


@router.get("/{group_id}")
def get_roles_of_group(group_id: int, db: Session = Depends(get_db)):
    try:
        result = group_role_service.get_roles_of_group(db, group_id)
        return group_role_view.success_response(
            result, "Get roles of group successfully"
        )
    except ValueError as e:
        return group_role_view.error_response(str(e), 404)


@router.post("/assign")
def assign_roles_for_group(
    group_id: int = Body(..., embed=True),
    role_ids: list[int] = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    try:
        result = group_role_service.assign_roles_for_group(db, group_id, role_ids)
        return group_role_view.success_response(
            result, "Assigned roles for group successfully"
        )
    except ValueError as e:
        return group_role_view.error_response(str(e), 400)
