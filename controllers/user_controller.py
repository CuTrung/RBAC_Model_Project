from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.user_model import UserCreate, UserResponse
from services import user_service
from views import user_view
from database import get_db

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = user_service.get_users(db)
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user(db, user_id)
    if user:
        return user
    return user_view.error_response("User not found", 404)

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    updated = user_service.update_user(db, user_id, user)
    if updated:
        return updated
    return user_view.error_response("User not found", 404)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = user_service.delete_user(db, user_id)
    if deleted:
        return user_view.success_response({"user_id": deleted.user_id}, "User deleted")
    return user_view.error_response("User not found", 404)
