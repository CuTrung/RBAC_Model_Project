from sqlalchemy.orm import Session
from models.user_model import User, UserCreate


def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise ValueError("Không tìm thấy người dùng")
    return user


def create_user(db: Session, user: UserCreate):
    new_user = User(username=user.username, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user_id: int, updated_user: UserCreate):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        user.username = updated_user.username
        user.email = updated_user.email
        # Hash password trước khi lưu
        from passlib.context import CryptContext

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user.password = pwd_context.hash(updated_user.password)
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
