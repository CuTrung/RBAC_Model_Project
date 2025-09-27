from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.group_model import GroupCreate, GroupResponse, GroupUpdate
from services import group_service
from views import group_view
from database import get_db

router = APIRouter()

@router.get("/", response_model=list[GroupResponse])
def get_groups(db: Session = Depends(get_db)):
    try:
        return group_view.success_response(
            group_service.get_groups(db)
        )
    except ValueError as ve:
        return group_view.error_response(str(ve), 400)

@router.get("/{group_id}", response_model=GroupResponse)
def get_group(group_id: str, db: Session = Depends(get_db)):
    try:
        return group_view.success_response(
            group_service.get_group(db, group_id)
        )
    except ValueError as ve:
        return group_view.error_response(str(ve), 400)

@router.post("/", response_model=GroupResponse)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    try:
        return group_view.success_response(
            group_service.create_group(db, group), 
            "Tạo group thành công"
        )
    except ValueError as ve:
        return group_view.error_response(str(ve), 400)
    
@router.put("/{group_id}", response_model=GroupResponse)
def update_group(group_id: str, group: GroupUpdate, db: Session = Depends(get_db)):
    try:
        return group_view.success_response(
            group_service.update_group(db, group_id, group), 
            "Cập nhật group thành công"
        )
    except ValueError as ve:
        return group_view.error_response(str(ve), 400)


@router.delete("/{group_id}")
def delete_group(group_id: str, db: Session = Depends(get_db)):
    try:
        return group_view.success_response(
            group_service.delete_group(db, group_id), 
            "Xóa group thành công"
        )
    except ValueError as ve:
        return group_view.error_response(str(ve), 400)

    
