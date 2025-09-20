from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.user_group_model import UserGroupCreate, UserGroupResponse
from services import user_group_service
from database import get_db
from views import user_group_view

router = APIRouter()


@router.get("/", response_model=list[UserGroupResponse])
def get_user_groups(db: Session = Depends(get_db)):
    return user_group_service.get_user_groups(db)


@router.get("/{user_group_id}", response_model=UserGroupResponse)
def get_user_group(user_group_id: int, db: Session = Depends(get_db)):
    user_group = user_group_service.get_user_group(db, user_group_id)
    if user_group:
        return user_group
    return user_group_view.error_response("UserGroup not found", 404)


@router.post("/", response_model=UserGroupResponse)
def create_user_group(user_group: UserGroupCreate, db: Session = Depends(get_db)):
    return user_group_service.create_user_group(db, user_group)


@router.delete("/{user_group_id}")
def delete_user_group(user_group_id: int, db: Session = Depends(get_db)):
    deleted = user_group_service.delete_user_group(db, user_group_id)
    if deleted:
        return user_group_view.success_response({"id": deleted.id}, "UserGroup deleted")
    return user_group_view.error_response("UserGroup not found", 404)
