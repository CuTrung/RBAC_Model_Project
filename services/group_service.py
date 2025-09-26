from sqlalchemy.orm import Session
from models.group_model import Group, GroupCreate


def get_groups(db: Session):
    return db.query(Group).all()


def get_group(db: Session, group_id: int):
    group = db.query(Group).filter(Group.group_id == group_id).first()
    if not group:
        raise ValueError("Không tìm thấy nhóm")
    return group


def create_group(db: Session, group: GroupCreate):
    new_group = Group(group_name=group.group_name, description=group.description)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


def update_group(db: Session, group_id: int, updated_group: GroupCreate):
    group = db.query(Group).filter(Group.group_id == group_id).first()
    if group:
        group.group_name = updated_group.group_name
        group.description = updated_group.description
        db.commit()
        db.refresh(group)
    return group


def delete_group(db: Session, group_id: int):
    group = db.query(Group).filter(Group.group_id == group_id).first()
    if group:
        db.delete(group)
        db.commit()
    return group
