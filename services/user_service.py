from sqlalchemy import select
from sqlalchemy.orm import Session
from models.user_model import User, UserCreate, UserUpdate
from models.permission_model import Permission
from models.resource_model import Resource
from models.role_permission_model import RolePermission
from models.user_group_model import UserGroup
from models.group_role_model import GroupRole
from utils.validation.model import check_unique, check_exists
from utils.string import coalesce, hash, verify
from utils.jwt import create_access_token, verify_token, Depends, oauth2_scheme
from services import user_group_service


def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.user_id == user_id).first()


def create_user(db: Session, user: UserCreate):
    check_unique(db, User, username=user.username)
    check_unique(db, User, email=user.email)
    
    new_user = User(
        username=user.username,
        email=user.email,
        password= hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user_id: str, updated_user: UserUpdate):
    check_exists(db, User, user_id=user_id)
    check_unique(db, User, username=updated_user.username)
    check_unique(db, User, email=updated_user.email)
    
    user = get_user(db, user_id)
    user.username = coalesce(updated_user.username, user.username)
    user.email = coalesce(updated_user.email, user.email)
    user.password = coalesce(hash(updated_user.password) if updated_user.password else user.password)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: str):
    check_exists(db, User, user_id=user_id)
    user = get_user(db, user_id)
    db.delete(user)
    
    user_group_service.remove_user_from_groups(db, user_id)
    
    db.commit()
    return user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def login(db: Session, username: str, password: str):
    user = db.query(User).filter((User.email == username) | (User.username == username)).first()
    if not user or not verify(password, user.password):
        raise ValueError("username hoặc password không đúng")

    return create_access_token({
        "username": user.username, 
        "email": user.email,
        "user_id": user.user_id
    })

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)
        

def get_permissions_of_user(db: Session, user_id: str):
    check_exists(db, User, user_id=user_id)
    
    stmt = (
        select(
            User.user_id,
            Permission.permission_id,
            Permission.permission_name,
            Resource.resource_id,
            Resource.resource_name
        )
        .outerjoin(UserGroup, UserGroup.user_id == User.user_id)
        .outerjoin(GroupRole, GroupRole.group_id == UserGroup.group_id)
        .outerjoin(RolePermission, RolePermission.role_id == GroupRole.role_id)
        .outerjoin(Permission, Permission.permission_id == RolePermission.permission_id)
        .outerjoin(Resource, Resource.resource_id == Permission.resource_id)
        .filter(User.user_id == user_id)
    )
    return db.execute(stmt).mappings().all()
