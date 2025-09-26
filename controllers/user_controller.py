import re
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from models.user_model import UserCreate, UserResponse
from services import user_service
from views import user_view
from database import get_db
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    # Đảm bảo password là chuỗi (str)
    if not isinstance(password, str):
        password = str(password)
    # Cắt password về tối đa 72 ký tự (không phải bytes)
    safe_password = password[:72]
    return pwd_context.hash(safe_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def is_valid_email(email: str) -> bool:
    # Regex kiểm tra email cơ bản
    pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def is_not_empty(value: str) -> bool:
    return bool(value and value.strip())


def is_valid_username(username: str) -> bool:
    return len(username) >= 4


def is_valid_password(password: str) -> bool:
    return len(password) >= 6


@router.post("/", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Kiểm tra các trường không được bỏ trống
    if not is_not_empty(user.username):
        return user_view.error_response("Tên đăng nhập không được bỏ trống", 400)
    if not is_not_empty(user.email):
        return user_view.error_response("Email không được bỏ trống", 400)
    if not is_not_empty(user.password):
        return user_view.error_response("Mật khẩu không được bỏ trống", 400)
    if not is_valid_username(user.username):
        return user_view.error_response("Tên đăng nhập phải từ 4 ký tự trở lên", 400)
    if not is_valid_password(user.password):
        return user_view.error_response("Mật khẩu phải từ 6 ký tự trở lên", 400)
    if not is_valid_email(user.email):
        return user_view.error_response("Email không hợp lệ", 400)
    if user_service.get_user_by_username(db, user.username):
        return user_view.error_response("Tên đăng nhập đã tồn tại", 400)
    if user_service.get_user_by_email(db, user.email):
        return user_view.error_response("Email đã tồn tại", 400)
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    new_user = user_service.create_user(db, user)
    return user_view.success_response(
        UserResponse.from_orm(new_user).model_dump(), "Đăng ký thành công"
    )


@router.post("/login")
def login(
    username: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)
):
    user = user_service.get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        return user_view.error_response("Tên đăng nhập hoặc mật khẩu không đúng", 401)
    access_token = create_access_token({"sub": user.username})
    return user_view.success_response(
        {"access_token": access_token, "token_type": "bearer"}, "Đăng nhập thành công"
    )


@router.post("/logout")
def logout():
    return user_view.success_response({}, "Đăng xuất thành công")


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

@router.get("/{user_id}/permissions", response_model=UserResponse)
def get_permissions_of_user(user_id: int, db: Session = Depends(get_db)):
    permissionsOfUser = user_service.get_permissions_of_user(db, user_id)
    if permissionsOfUser:
        return permissionsOfUser
    return user_view.error_response("User not found", 404)