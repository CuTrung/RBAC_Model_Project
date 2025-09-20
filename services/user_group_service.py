from sqlalchemy.orm import Session
from models.user_group_model import UserGroup, UserGroupCreate


def get_user_groups(db: Session):
    return db.query(UserGroup).all()


def get_user_group(db: Session, user_group_id: int):
    return db.query(UserGroup).filter(UserGroup.id == user_group_id).first()


def create_user_group(db: Session, user_group: UserGroupCreate):
    new_user_group = UserGroup(user_id=user_group.user_id, group_id=user_group.group_id)
    db.add(new_user_group)
    db.commit()
    db.refresh(new_user_group)
    return new_user_group


def delete_user_group(db: Session, user_group_id: int):
    user_group = db.query(UserGroup).filter(UserGroup.id == user_group_id).first()
    if user_group:
        db.delete(user_group)
        db.commit()
    return user_group
