from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.user_model import UserCreate, UserResponse, UserUpdate
from services import user_service
from views import user_view
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from utils.validation.user import is_valid_email, is_valid_password, is_valid_username, is_not_empty


router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        if not is_not_empty(user.username):
            return user_view.error_response("Tên đăng nhập không được bỏ trống")
        if not is_not_empty(user.email):
            return user_view.error_response("Email không được bỏ trống")
        if not is_not_empty(user.password):
            return user_view.error_response("Mật khẩu không được bỏ trống")
        if not is_valid_username(user.username):
            return user_view.error_response("Tên đăng nhập phải từ 4 ký tự trở lên")
        if not is_valid_password(user.password):
            return user_view.error_response("Mật khẩu phải từ 6 ký tự trở lên")
        if not is_valid_email(user.email):
            return user_view.error_response("Email không hợp lệ")
        
        new_user = user_service.create_user(db, user)
        return user_view.success_response(
            new_user,
            "Đăng ký thành công"
        )
    except ValueError as ve:
        return user_view.error_response(str(ve), 400)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    access_token = user_service.login(db, form_data.username, form_data.password)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/current-user")
def get_current_user(
    current_user: str = Depends(user_service.get_current_user), 
    db: Session = Depends(get_db)
):
    user_id = current_user["user_id"]
    permissionsOfUser = user_service.get_permissions_of_user(db, user_id)
    return user_view.success_response({
        "user_id": user_id,
        "email": current_user["email"],
        "username": current_user["username"],
        "permissions": permissionsOfUser
    })


@router.post("/logout")
def logout():
    return user_view.success_response(None, "Đăng xuất thành công")


@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    try:
        return user_view.success_response(
            user_service.get_users(db)
        )
    except ValueError as ve:
        return user_view.error_response(str(ve), 400)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    try:
        return user_view.success_response(
            user_service.get_user(db, user_id)
        )
    except ValueError as ve:
        return user_view.error_response(str(ve), 400)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        return user_view.success_response(
            user_service.update_user(db, user_id, user),
            "Cập nhật user thành công"
        )
    except ValueError as ve:
        return user_view.error_response(str(ve), 400)


@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    try:
        return user_view.success_response(
            user_service.delete_user(db, user_id), 
            "Xóa user thành công"
        )
    except ValueError as ve:
        return user_view.error_response(str(ve), 400)