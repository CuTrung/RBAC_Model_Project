from sqlalchemy.orm import Session
from models.group_model import Group, GroupCreate
from utils.validation.model import check_unique, check_exists
from services import user_group_service
from services import group_role_service

def get_groups(db: Session):
    return db.query(Group).all()


def get_group(db: Session, group_id: str):
    return db.query(Group).filter(Group.group_id == group_id).first()


def create_group(db: Session, group: GroupCreate):
    check_unique(db, Group, group_name=group.group_name)
    
    new_group = Group(
        group_name=group.group_name,
        description=group.description
    )
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

def update_group(db: Session, group_id: str, updated_group: GroupCreate):
    check_exists(db, Group, group_id=group_id)
    check_unique(db, Group, group_name=updated_group.group_name)
    
    group = get_group(db, group_id)
    group.group_name = updated_group.group_name
    group.description = updated_group.description
    
    db.commit()
    db.refresh(group)
    return group


def delete_group(db: Session, group_id: str):
    check_exists(db, Group, group_id=group_id)
    group = get_group(db, group_id)
    db.delete(group)
    
    user_group_service.remove_group_from_users(db, group_id)
    group_role_service.remove_group_from_roles(db, group_id)
    
    db.commit()
    return group
