from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.group_model import GroupCreate, GroupResponse
from services import group_service
from database import get_db
from views import group_view

router = APIRouter()


@router.get("/", response_model=list[GroupResponse])
def get_groups(db: Session = Depends(get_db)):
    return group_service.get_groups(db)


@router.get("/{group_id}", response_model=GroupResponse)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = group_service.get_group(db, group_id)
    if group:
        return group
    return group_view.error_response("Group not found", 404)


@router.post("/", response_model=GroupResponse)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    return group_service.create_group(db, group)


@router.put("/{group_id}", response_model=GroupResponse)
def update_group(group_id: int, group: GroupCreate, db: Session = Depends(get_db)):
    updated = group_service.update_group(db, group_id, group)
    if updated:
        return updated
    return group_view.error_response("Group not found", 404)


@router.delete("/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    deleted = group_service.delete_group(db, group_id)
    if deleted:
        return group_view.success_response({"group_id": deleted.group_id}, "Group deleted")
    return group_view.error_response("Group not found", 404)
